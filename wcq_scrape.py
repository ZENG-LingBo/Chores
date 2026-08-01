#!/usr/bin/env python3
"""Scrape the HKUST Class Schedule & Quota site into a CSV.

    https://w5.ab.ust.hk/wcq/cgi-bin/{TERM}/

The site is a plain CGI-driven, server-rendered HTML app: no JavaScript
rendering, no login, no JSON API. The index page links to one page per
subject (.../{TERM}/subject/COMP), and each subject page holds the course
tables.

Term codes are <2-digit academic year start><term>, where term is
10=Fall, 20=Winter, 30=Spring, 40=Summer. So 2610 is 2026-27 Fall.

Page shape, per observed markup:

    ACCT 2010 - Principles of Accounting I (3 units)
    [DELI]

    Section      Date & Time               Room                      Remarks
    L01 (1038)   TuTh 01:30PM - 02:50PM    Rm 6573, Lift 29-30 (88)
    Instructor
    DONG, Qingkai

Section columns are read from each table's own header row rather than
hardcoded, so a page that also carries Quota/Enrol/Avail/Wait columns is
picked up without a code change. Instructor arrives as a nested sub-table
inside the section row instead of as a column, so nested label/value
tables are folded into the section as extra named fields.

Usage:
    python wcq_scrape.py                    # default term
    python wcq_scrape.py 2630               # a specific term
    python wcq_scrape.py 2610 -s COMP -s MATH
    python wcq_scrape.py 2610 -o quota.csv --delay 2
"""

import argparse
import copy
import csv
import re
import sys
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

DEFAULT_TERM = "2610"
BASE_URL = "https://w5.ab.ust.hk/wcq/cgi-bin/{term}/"
USER_AGENT = "wcq-scrape/1.0 (personal course-planning use)"

# This is one small departmental CGI server. Keep a delay between requests;
# polling it aggressively for quota changes is how you get an IP blocked.
DEFAULT_DELAY = 1.0
MAX_RETRIES = 3

SUBJECT_RE = re.compile(r"^[A-Z]{4}$")
# "ACCT 2010 - Principles of Accounting I (3 units)"
COURSE_RE = re.compile(
    r"^(?P<subject>[A-Z]{4})\s+(?P<number>[0-9A-Z]+)\s*-\s*"
    r"(?P<title>.*?)\s*(?:\((?P<units>[\d.]+)\s*units?\)\s*)?$"
)
ATTRIBUTE_RE = re.compile(r"\[([A-Z0-9]+)\]")

LEAD_FIELDS = ["subject", "course_number", "course_title", "units", "attributes"]


def squash(text):
    """Collapse whitespace runs, including the &nbsp; the site is full of."""
    return " ".join(text.replace("\xa0", " ").split())


def cells(row, tag):
    """Direct-child cells only.

    BeautifulSoup's find_all recurses, so without recursive=False a nested
    table's cells get pulled into the enclosing row and duplicated.
    """
    return row.find_all(tag, recursive=False)


def own_rows(table):
    """Rows belonging to this table, not to a table nested inside it.

    find_all("tr") descends into nested tables, which would otherwise turn
    the nested Instructor sub-table's rows into bogus sections.
    """
    return [tr for tr in table.find_all("tr") if tr.find_parent("table") is table]


def cell_text(cell):
    """Cell text with nested tables stripped.

    A nested sub-table is read separately by nested_fields; leaving it in
    would smear "Instructor DONG, Qingkai" into the Remarks column.
    """
    clone = copy.copy(cell)
    for nested in clone.find_all("table"):
        nested.decompose()
    return squash(clone.get_text(" "))


def fetch(session, url, delay):
    """GET a page with a polite delay and a few retries on transient errors."""
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = session.get(url, timeout=30)
            response.raise_for_status()
            time.sleep(delay)
            return BeautifulSoup(response.text, "html.parser")
        except requests.RequestException as exc:
            if attempt == MAX_RETRIES:
                raise
            backoff = delay * 2**attempt
            print(f"  {exc} -- retrying in {backoff:.0f}s", file=sys.stderr)
            time.sleep(backoff)


def subject_urls(session, base, delay, only=None):
    """Collect the per-subject page links off the term index.

    Subject codes are uniformly four uppercase letters (96 of them as of
    2610), so anything else off that selector is navigation chrome.
    """
    soup = fetch(session, base, delay)
    urls = {}
    for anchor in soup.select('a[href*="/subject/"]'):
        code = urljoin(base, anchor["href"]).rstrip("/").rsplit("/", 1)[-1].upper()
        if SUBJECT_RE.match(code):
            urls[code] = urljoin(base, anchor["href"])
    if only:
        wanted = {s.upper() for s in only}
        missing = wanted - urls.keys()
        if missing:
            print(f"no such subject(s): {', '.join(sorted(missing))}", file=sys.stderr)
        urls = {code: url for code, url in urls.items() if code in wanted}
    return sorted(urls.items())


def parse_course(table):
    """Pull course identity out of the nearest preceding heading.

    Falls back to the raw heading text when the line doesn't match the
    usual "CODE NUMBER - Title (N units)" shape.
    """
    node = table.find_previous(["h1", "h2", "h3", "h4", "caption"])
    if not node:
        return {"course_title": ""}
    heading = squash(node.get_text(" "))
    # The [DELI]-style attribute tags sit between the heading and the table.
    between = squash("".join(str(s) for s in node.next_siblings if s is not table))
    attributes = ATTRIBUTE_RE.findall(between)

    match = COURSE_RE.match(heading)
    if not match:
        return {"course_title": heading, "attributes": ",".join(attributes)}
    return {
        "subject": match["subject"],
        "course_number": match["number"],
        "course_title": match["title"],
        "units": match["units"] or "",
        "attributes": ",".join(attributes),
    }


def nested_fields(row):
    """Fold nested label/value tables into named fields.

    Instructor is delivered this way -- a sub-table headed "Instructor"
    inside the section row rather than a column of the section table.
    """
    fields = {}
    for table in row.find_all("table"):
        labels, values = [], []
        for tr in table.find_all("tr"):
            head = [squash(c.get_text(" ")) for c in cells(tr, "th")]
            body = [squash(c.get_text(" ")) for c in cells(tr, "td")]
            labels.extend(head)
            values.extend(body)
        for i, label in enumerate(labels):
            if label and i < len(values) and values[i]:
                key = label.lower().replace(" ", "_")
                fields[key] = "; ".join(filter(None, [fields.get(key), values[i]]))
    return fields


def header_names(table):
    """Column names from the table's own header row."""
    for tr in own_rows(table):
        head = [cell_text(c) for c in cells(tr, "th")]
        if head:
            return [h.lower().replace(" & ", "_").replace(" ", "_") for h in head]
    return []


def scrape_subject(session, code, url, delay):
    soup = fetch(session, url, delay)
    rows = []
    # Only top-level tables; nested ones are handled as part of their parent row.
    for table in (t for t in soup.find_all("table") if not t.find_parent("table")):
        course = parse_course(table)
        course.setdefault("subject", code)
        names = header_names(table)
        for tr in own_rows(table):
            values = [cell_text(c) for c in cells(tr, "td")]
            nested = nested_fields(tr)
            if not any(values):
                # A continuation row -- Instructor arrives this way when it
                # isn't nested inside the section row itself. Fold it back
                # into the section it belongs to rather than emitting a
                # row with no section.
                if nested and rows:
                    rows[-1].update(nested)
                continue
            row = dict(course)
            for i, value in enumerate(values):
                row[names[i] if i < len(names) else f"col{i + 1}"] = value
            row.update(nested)
            rows.append(row)
    return rows


def write_csv(rows, out_path):
    """Union of every field seen, lead columns first, rest in first-seen order."""
    names = list(LEAD_FIELDS)
    for row in rows:
        names.extend(k for k in row if k not in names)
    with open(out_path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=names, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    return names


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("term", nargs="?", default=DEFAULT_TERM,
                        help=f"term code, e.g. 2610 (default: {DEFAULT_TERM})")
    parser.add_argument("-o", "--out", help="output CSV (default: wcq_<term>.csv)")
    parser.add_argument("-s", "--subject", action="append",
                        help="limit to a subject code; repeatable")
    parser.add_argument("--delay", type=float, default=DEFAULT_DELAY,
                        help=f"seconds between requests (default: {DEFAULT_DELAY})")
    args = parser.parse_args()

    base = BASE_URL.format(term=args.term)
    out_path = args.out or f"wcq_{args.term}.csv"

    session = requests.Session()
    session.headers["User-Agent"] = USER_AGENT

    subjects = subject_urls(session, base, args.delay, args.subject)
    if not subjects:
        print(f"no subject pages found at {base}", file=sys.stderr)
        return 1
    print(f"{len(subjects)} subject page(s) at {base}", file=sys.stderr)

    rows = []
    for code, url in subjects:
        found = scrape_subject(session, code, url, args.delay)
        print(f"  {code}: {len(found)} rows", file=sys.stderr)
        rows.extend(found)

    names = write_csv(rows, out_path)
    print(f"{len(rows)} rows, {len(names)} columns -> {out_path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())

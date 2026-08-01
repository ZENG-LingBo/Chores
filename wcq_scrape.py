#!/usr/bin/env python3
"""Scrape the HKUST Class Schedule & Quota site into a CSV.

    https://w5.ab.ust.hk/wcq/cgi-bin/{TERM}/

The site is a plain CGI-driven, server-rendered HTML app: no JavaScript
rendering, no login, no JSON API. The index page links to one page per
subject (.../{TERM}/subject/COMP), and each subject page holds the course
tables.

Term codes are <2-digit academic year start><term>, where term is
10=Fall, 20=Winter, 30=Spring, 40=Summer. So 2610 is 2026-27 Fall.

Page shape, confirmed against the live site (tools/dump_markup.py):

    div#classes
      div.course
        div.courseinfo > div.courseattrContainer > div.subject
            "ACCT 2010 - Principles of Accounting I (3 units)"
        table            -- ATTRIBUTES / DESCRIPTION / outcomes
        table.sections
          tr                          -- header: Section, Date & Time, Room,
                                         Instructor, TA/IA/GTA, Quota, Enrol,
                                         Avail, Wait, Remarks
          tr.newsect.mainRow          -- a section
          tr.mobileInstructorRow      -- mobile-only duplicate, skipped
          tr.mobileViewDetail         -- mobile-only duplicate, skipped

Only tr.mainRow carries real data; the two mobile rows repeat it for a
narrow viewport and would otherwise triple every section. A mainRow
without .newsect is an additional meeting slot for the section above it,
so it is merged into that section rather than emitted separately.

Column names come from the table's own header row, so a layout change
that adds or reorders columns does not need a code change.

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
LEAD_FIELDS = ["subject", "course_number", "course_title", "units", "attributes"]

# Seat counts are deliberately not collected. They also arrive with
# mobile-only text baked into the cell ("75 Quota/Enrol/Avail ACCT: 75/0/75"),
# so dropping them avoids having to unpick that.
DROP_FIELDS = {"quota", "enrol", "avail", "wait"}


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

    Several cells carry a nested table holding the mobile-viewport copy of
    the same data; leaving it in smears that duplicate into the value.
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


def norm(text):
    """Header label to field name: "Date & Time" -> date_time."""
    return re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")


def parse_course(course):
    """Course identity from the div.subject heading inside a div.course.

    Falls back to the raw heading text when the line doesn't match the
    usual "CODE NUMBER - Title (N units)" shape.
    """
    heading_node = course.select_one("div.subject")
    heading = cell_text(heading_node) if heading_node else ""

    # Attributes live in the course's info table, as the cell beside the
    # ATTRIBUTES header, e.g. "[BLD] Blended learning".
    attributes = ""
    for tr in course.find_all("tr"):
        head = cells(tr, "th")
        body = cells(tr, "td")
        if head and body and cell_text(head[0]).upper() == "ATTRIBUTES":
            attributes = cell_text(body[0])
            break

    match = COURSE_RE.match(heading)
    if not match:
        return {"course_title": heading, "attributes": attributes}
    return {
        "subject": match["subject"],
        "course_number": match["number"],
        "course_title": match["title"],
        "units": match["units"] or "",
        "attributes": attributes,
    }


def header_names(table):
    """Column names from the table's own header row."""
    for tr in own_rows(table):
        head = [norm(cell_text(c)) for c in cells(tr, "th")]
        if head:
            return head
    return []


def scrape_subject(session, code, url, delay):
    soup = fetch(session, url, delay)
    rows = []
    for course in soup.select("div.course"):
        info = parse_course(course)
        info.setdefault("subject", code)
        table = course.select_one("table.sections")
        if not table:
            continue
        names = header_names(table)
        # mainRow only: mobileInstructorRow and mobileViewDetail repeat the
        # same section for a narrow viewport and would triple every row.
        for tr in table.select("tr.mainRow"):
            values = [cell_text(c) for c in cells(tr, "td")]
            row = {
                names[i] if i < len(names) else f"col{i + 1}": value
                for i, value in enumerate(values)
            }
            row = {k: v for k, v in row.items() if k not in DROP_FIELDS}

            if "newsect" not in (tr.get("class") or []) and rows:
                # An extra meeting slot for the section above, not a new
                # section -- fold its time and room into that section.
                for key in ("date_time", "room"):
                    extra = row.get(key)
                    if extra:
                        rows[-1][key] = "; ".join(filter(None, [rows[-1].get(key), extra]))
                continue

            rows.append({**info, **row})
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

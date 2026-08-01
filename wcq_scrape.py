#!/usr/bin/env python3
"""Scrape the HKUST Class Schedule & Quota site into a CSV.

    https://w5.ab.ust.hk/wcq/cgi-bin/<TERM>/

The site is a plain CGI-driven, server-rendered HTML app: no JavaScript
rendering, no login, no JSON API. The index page links to one page per
subject (.../<TERM>/subject/COMP), and each subject page holds the course
tables with the quota / enrolled / available / waitlist columns.

Term codes are <2-digit academic year start><term>, where term is
10=Fall, 20=Winter, 30=Spring, 40=Summer. So 2610 is 2026-27 Fall.

Usage:
    python wcq_scrape.py                    # current default term
    python wcq_scrape.py 2630               # a specific term
    python wcq_scrape.py 2610 -s COMP -s MATH
    python wcq_scrape.py 2610 -o quota.csv --delay 2

NOTE ON MARKUP: the column layout of the section rows is emitted as-is
rather than mapped to fixed field names, because the exact table shape
should be confirmed against the live page before anything downstream
depends on it. Run once, look at the CSV, then tighten if you need
typed columns.
"""

import argparse
import csv
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


def squash(text):
    """Collapse whitespace runs, including the &nbsp; the site is full of."""
    return " ".join(text.replace("\xa0", " ").split())


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
    """Collect the per-subject page links off the term index."""
    soup = fetch(session, base, delay)
    urls = {}
    for anchor in soup.select('a[href*="/subject/"]'):
        url = urljoin(base, anchor["href"])
        urls[url.rstrip("/").rsplit("/", 1)[-1]] = url
    if only:
        wanted = {s.upper() for s in only}
        missing = wanted - urls.keys()
        if missing:
            print(f"no such subject(s): {', '.join(sorted(missing))}", file=sys.stderr)
        urls = {code: url for code, url in urls.items() if code in wanted}
    return sorted(urls.items())


def heading_for(table):
    """Nearest preceding heading text -- the course a table belongs to.

    Matching on a heading rather than a specific wrapper class keeps this
    working if the surrounding div structure changes.
    """
    node = table.find_previous(["h1", "h2", "h3", "h4", "caption"])
    return squash(node.get_text(" ")) if node else ""


def scrape_subject(session, code, url, delay):
    soup = fetch(session, url, delay)
    rows = []
    for table in soup.find_all("table"):
        course = heading_for(table)
        for tr in table.find_all("tr"):
            cells = [squash(td.get_text(" ")) for td in tr.find_all("td")]
            if any(cells):
                rows.append([code, course] + cells)
    return rows


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

    width = max((len(r) for r in rows), default=0)
    with open(out_path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["subject", "course"] + [f"col{i}" for i in range(1, width - 1)])
        writer.writerows(row + [""] * (width - len(row)) for row in rows)

    print(f"{len(rows)} rows -> {out_path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())

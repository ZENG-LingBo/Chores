#!/usr/bin/env python3
"""Print the real structure of a WCQ subject page.

The scraper has to be written against this site's actual markup, and the
markup is the part most likely to drift. Run this to see what a subject
page really looks like before changing the parser.

Deliberately compact: it answers "where does the course heading live" and
"what shape are the section rows", rather than dumping the whole document.
"""

import re
import sys

import requests
from bs4 import BeautifulSoup

term = sys.argv[1] if len(sys.argv) > 1 else "2610"
subject = sys.argv[2] if len(sys.argv) > 2 else "ACCT"

index = f"https://w5.ab.ust.hk/wcq/cgi-bin/{term}/"
page = f"{index}subject/{subject}"
headers = {"User-Agent": "wcq-scrape/1.0 (personal course-planning use)"}


def describe(tag):
    bits = tag.name
    if tag.get("class"):
        bits += "." + ".".join(tag["class"])
    if tag.get("id"):
        bits += "#" + tag["id"]
    return bits


idx = BeautifulSoup(requests.get(index, headers=headers, timeout=30).text, "html.parser")
links = idx.select('a[href*="/subject/"]')
print(f"== index: {len(links)} subject links; first 3: "
      f"{[a.get('href') for a in links[:3]]}")

html = requests.get(page, headers=headers, timeout=30).text
open("raw.html", "w", encoding="utf-8").write(html)
soup = BeautifulSoup(html, "html.parser")

tables = soup.find_all("table")
top = [t for t in tables if not t.find_parent("table")]
print(f"== {page}: {len(html)} bytes, {len(tables)} tables "
      f"({len(top)} top-level, {len(tables) - len(top)} nested)")

# Where does the course heading actually live?
node = soup.find(string=re.compile(rf"{subject}\s+\d{{4}}"))
if node:
    print(f"== course heading text: {node.strip()[:70]!r}")
    print("   ancestors:", " < ".join(describe(p) for p in node.parents if p.name)[:200])
else:
    print("== no course-heading text found")

for i, table in enumerate(top[:2]):
    rows = [tr for tr in table.find_all("tr") if tr.find_parent("table") is table]
    print(f"\n== top-level table {i}: {describe(table)}, {len(rows)} own rows")
    for j, tr in enumerate(rows[:8]):
        parts = []
        for c in tr.find_all(["th", "td"], recursive=False):
            nested = "+tbl" if c.find("table") else ""
            parts.append(f"{describe(c)}{nested}={c.get_text(' ', strip=True)[:32]!r}")
        print(f"   row {j} {describe(tr)}: {' | '.join(parts)[:260]}")

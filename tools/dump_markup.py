#!/usr/bin/env python3
"""Print the real structure of a WCQ subject page.

The scraper has to be written against this site's actual markup, and the
markup is the part most likely to drift. Run this to see what a subject
page really looks like before changing the parser.
"""

import sys

import requests
from bs4 import BeautifulSoup

term = sys.argv[1] if len(sys.argv) > 1 else "2610"
subject = sys.argv[2] if len(sys.argv) > 2 else "ACCT"

index = f"https://w5.ab.ust.hk/wcq/cgi-bin/{term}/"
page = f"{index}subject/{subject}"
headers = {"User-Agent": "wcq-scrape/1.0 (personal course-planning use)"}

idx = BeautifulSoup(requests.get(index, headers=headers, timeout=30).text, "html.parser")
links = idx.select('a[href*="/subject/"]')
print(f"== index: {len(links)} subject links")
print("   first 5:", [a.get("href") for a in links[:5]])

html = requests.get(page, headers=headers, timeout=30).text
open("raw.html", "w", encoding="utf-8").write(html)
soup = BeautifulSoup(html, "html.parser")

print(f"\n== {page}: {len(html)} bytes")
for tag in ("table", "h1", "h2", "h3", "h4"):
    print(f"   <{tag}>: {len(soup.find_all(tag))}")

tables = soup.find_all("table")
top = [t for t in tables if not t.find_parent("table")]
print(f"   top-level tables: {len(top)}, nested: {len(tables) - len(top)}")

for i, table in enumerate(top[:2]):
    print(f"\n== top-level table {i}: class={table.get('class')} id={table.get('id')}")
    rows = [tr for tr in table.find_all("tr") if tr.find_parent("table") is table]
    print(f"   own rows: {len(rows)}")
    for j, tr in enumerate(rows[:6]):
        th = [c.get_text(" ", strip=True)[:40] for c in tr.find_all("th", recursive=False)]
        td = [c.get_text(" ", strip=True)[:40] for c in tr.find_all("td", recursive=False)]
        print(f"   row {j}: class={tr.get('class')} th={th}")
        print(f"          td={td}")

print("\n== first 220 lines of prettified markup")
pretty = soup.prettify().splitlines()
start = next((n for n, line in enumerate(pretty) if subject in line and "-" in line), 0)
for line in pretty[max(0, start - 20):start + 200]:
    print(line[:200])

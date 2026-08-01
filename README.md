# Chores
Chores

## wcq_scrape.py

Scrapes the HKUST Class Schedule & Quota site
(`https://w5.ab.ust.hk/wcq/cgi-bin/<TERM>/`) into a CSV. The site is plain
server-rendered HTML, so `requests` + `BeautifulSoup` is enough — no headless
browser needed.

```sh
pip install -r requirements.txt
python wcq_scrape.py 2610              # 2026-27 Fall -> wcq_2610.csv
python wcq_scrape.py 2610 -s COMP      # just one subject
```

Term codes are `<2-digit academic year start><term>`, where term is `10`=Fall,
`20`=Winter, `30`=Spring, `40`=Summer.

Output columns are `subject, course_number, course_title, units, attributes,
section, date_time, room, remarks, instructor`, plus `quota, enrol, avail, wait`
on pages that carry them.

Section columns are read from each table's own header row rather than hardcoded,
so a page with extra columns is picked up without a code change. `Instructor`
arrives as a nested sub-table rather than a column, and is folded into the
section row either way.

Keep the request delay in place; it's a small departmental server.

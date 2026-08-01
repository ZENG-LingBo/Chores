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
section, date_time, room, instructor, ta_ia_gta, remarks`. Seat counts
(quota/enrol/avail/wait) are deliberately not collected.

Column names come from each section table's own header row rather than being
hardcoded, so a layout change that adds or reorders columns needs no code
change. Each section appears once: the site emits two extra mobile-viewport
copies of every row, and a section that meets more than once has its extra
slots merged into a single row.

`tools/dump_markup.py` prints the live page structure -- run it (or the
"Dump markup" workflow) if the site changes and the parser starts producing
blank or duplicated columns.

Keep the request delay in place; it's a small departmental server.

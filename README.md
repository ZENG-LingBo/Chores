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

## plan_schedule.py

Builds conflict-free timetables from `data/wcq_<term>.csv` for a specific set of
degree requirements (currently: ISD 2022-23, Year 4). One section per component
(lecture + tutorial + lab) is enrolled together; TBA sections are surfaced, not
dropped.

```sh
python plan_schedule.py data/wcq_2610.csv --availability
python plan_schedule.py data/wcq_2610.csv \
    --must "ISDN 4001" --must "ISDN 1001" \
    --pool "ISOM 2700,MARK 2120" --pool "COMP 3111,COMP 4331"
```

The `data/` CSV is written by the scrape workflow when dispatched with
`commit: true` -- that is how scraped data reaches a sandbox whose only
outbound channel is git.

## plan_schedule.py

Builds conflict-free timetables from `data/wcq_<term>.csv`. Courses are grouped
into enrolments (one section per component -- L, T, LA) before combining, since
HKUST enrols per component, not per section.

```sh
python plan_schedule.py data/wcq_2610.csv                         # availability
python plan_schedule.py data/wcq_2610.csv \
  --must "ISDN 4001" --must "ISDN 1001" \
  --pool "ISOM 2700,MARK 2120" --top 3                            # search
```

Hard constraints: no overlaps, no class before `--earliest` (default 10:30).
Scoring prefers fewer days on campus, less idle time between classes, and an
empty `--free-day` (default Fr). TBA-time sections are surfaced, never silently
treated as free.

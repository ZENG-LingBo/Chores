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

The section rows are written out column-for-column rather than mapped to named
fields — check the CSV against the live page before building anything on top of
it. Keep the request delay in place; it's a small departmental server.

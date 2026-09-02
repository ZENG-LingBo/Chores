#!/usr/bin/env python3
"""Convert the groupmate's coded KFeed export (data/raw/all_data.xlsx) to CSV.

The workbook is the five-session, two-arm, two-day message log with coding
columns; message text was removed by the group for language reasons. This
script only flattens it so the analysis reads a plain CSV.

Run: python3 convert_all_data.py  ->  data/defuselab-all-messages.csv
"""
import csv
import os

import openpyxl

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "data", "raw", "all_data.xlsx")
DST = os.path.join(ROOT, "data", "defuselab-all-messages.csv")


def main():
    wb = openpyxl.load_workbook(SRC, read_only=True, data_only=True)
    it = wb.worksheets[0].iter_rows(values_only=True)
    hdr = [str(c) for c in next(it)]
    with open(DST, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(hdr)
        n = 0
        for row in it:
            if any(c not in (None, "") for c in row):
                w.writerow(["" if c is None else c for c in row])
                n += 1
    print(f"wrote {DST}: {n} rows")


if __name__ == "__main__":
    main()

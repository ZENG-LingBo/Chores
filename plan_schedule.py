#!/usr/bin/env python3
"""Build conflict-free course schedules from a scraped WCQ catalogue.

Reads the CSV produced by wcq_scrape.py, restricts to the courses that
actually advance an outstanding degree requirement, and searches for
timetable combinations that satisfy the stated constraints.

The requirement buckets in REQUIREMENTS come from a SIS advisement report
and the program curriculum -- they are the "what still needs doing" side.
The CSV is the "what is actually offered and when" side. A course listed
by SIS as a Fall course may still have no section this term, so the CSV
is treated as authoritative about availability.

Usage:
    python plan_schedule.py data/wcq_2610.csv
    python plan_schedule.py data/wcq_2610.csv --earliest 10:30 --free-day Fr
"""

import argparse
import csv
import itertools
import re
import sys
from collections import defaultdict

DAYS = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
DAY_RE = re.compile(r"Mo|Tu|We|Th|Fr|Sa|Su")
SLOT_RE = re.compile(
    r"^(?P<days>(?:Mo|Tu|We|Th|Fr|Sa|Su)+)\s+"
    r"(?P<start>\d{1,2}:\d{2}[AP]M)\s*-\s*(?P<end>\d{1,2}:\d{2}[AP]M)$"
)

# Outstanding requirements. `need` is credits still required; `courses` is
# the approved list for that bucket. `required` marks a bucket where a
# specific course must be taken rather than chosen from alternatives.
REQUIREMENTS = [
    {
        "bucket": "ISD required - Final Year Design Project I",
        "need": 4, "required": True,
        "courses": ["ISDN 4001"],
        "note": "gates ISDN 4002 in Spring",
    },
    {
        "bucket": "ISD required - Introduction to ISD",
        "need": 3, "required": True,
        "courses": ["ISDN 1001"],
        "note": "Fall-only; skipping it costs a full year",
    },
    {
        "bucket": "ISD required - Academic & Prof Dev IV",
        "need": 0, "required": True,
        "courses": ["ISDN 4010"],
        "note": "0 credits",
    },
    {
        "bucket": "University English (Dept-based)",
        "need": 3,
        "courses": ["LANG 4032", "LANG 4030", "LANG 4031", "LANG 4036"],
        "note": "also clears the major's LANG requirement",
    },
    {
        "bucket": "Product Management elective",
        "need": 3,
        "courses": ["ISDN 3350", "ISDN 4200", "ISOM 2700", "ISOM 4020",
                    "MARK 2120", "TEMG 3950", "ISDN 3360"],
    },
    # Project-related elective (3000+, 9 cr) is satisfied as of 2026-09-08 --
    # the department approved a swap of already-completed courses
    # (OCES 3301 / MECH 3640, per the emailed reply) toward this bucket, so
    # it no longer needs a Fall or Spring section and is removed here.
]


def parse_time(text):
    """'01:30PM' -> minutes since midnight."""
    hour, rest = text.split(":")
    minute, meridiem = int(rest[:2]), rest[2:].upper()
    hour = int(hour) % 12 + (12 if meridiem == "PM" else 0)
    return hour * 60 + minute


def fmt_time(minutes):
    hour, minute = divmod(minutes, 60)
    suffix = "AM" if hour < 12 else "PM"
    return f"{(hour % 12) or 12}:{minute:02d}{suffix}"


def parse_slots(date_time):
    """'TuTh 01:30PM - 02:50PM; Fr 11:00AM - 11:50AM' -> [(day, start, end)].

    Returns (slots, unparsed). A section whose time is TBA or blank yields
    no slots -- those are surfaced rather than silently treated as free.
    """
    slots, unparsed = [], []
    for chunk in (c.strip() for c in date_time.split(";") if c.strip()):
        match = SLOT_RE.match(chunk)
        if not match:
            unparsed.append(chunk)
            continue
        start, end = parse_time(match["start"]), parse_time(match["end"])
        for day in DAY_RE.findall(match["days"]):
            slots.append((day, start, end))
    return slots, unparsed


def overlaps(a, b):
    """Do two slot lists collide on a shared day?"""
    for day_a, start_a, end_a in a:
        for day_b, start_b, end_b in b:
            if day_a == day_b and start_a < end_b and start_b < end_a:
                return True
    return False


def course_key(row):
    return f"{row['subject']} {row['course_number']}"


def component(section):
    """Leading letters of a section code: 'LA1 (3081)' -> 'LA'.

    HKUST splits a course into components -- lecture (L), tutorial (T),
    lab (LA) -- and you enrol in one section of each, not one section
    overall. Treating every section as an alternative silently drops the
    tutorial you are also required to attend.
    """
    match = re.match(r"[A-Za-z]+", section.strip())
    return match.group(0).upper() if match else "?"


def load_sections(path, wanted):
    """Sections for the wanted courses, grouped by course."""
    by_course = defaultdict(list)
    tba = []
    with open(path, newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            key = course_key(row)
            if key not in wanted:
                continue
            slots, unparsed = parse_slots(row.get("date_time", ""))
            row["_slots"] = slots
            row["_key"] = key
            row["_component"] = component(row.get("section", ""))
            if not slots:
                # Kept, not dropped: a TBA component still has to be
                # enrolled in, it just cannot be placed on the grid.
                tba.append(row)
            by_course[key].append(row)
    return by_course, tba


def credits(row):
    try:
        return float(row.get("units") or 0)
    except ValueError:
        return 0.0


def enrolments(rows, earliest):
    """Valid ways to enrol in one course: one section per component."""
    groups = defaultdict(list)
    for row in rows:
        groups[row["_component"]].append(row)

    valid = []
    for combo in itertools.product(*groups.values()):
        if any(start < earliest for row in combo for _, start, _ in row["_slots"]):
            continue
        if any(overlaps(combo[i]["_slots"], combo[j]["_slots"])
               for i in range(len(combo)) for j in range(i + 1, len(combo))):
            continue
        valid.append(combo)
    return valid


def course_credits(rows):
    """Credits for a course -- carried on the lecture, not summed per component."""
    return max((credits(r) for r in rows), default=0.0)


def day_span(sections):
    """Minutes between first start and last end, per day used."""
    per_day = defaultdict(list)
    for row in sections:
        for day, start, end in row["_slots"]:
            per_day[day].append((start, end))
    return {d: (min(s for s, _ in v), max(e for _, e in v))
            for d, v in per_day.items()}


def score(sections, free_day):
    """Lower is better: idle time on campus, days used, then the free day."""
    spans = day_span(sections)
    used = set(spans)
    total_span = sum(end - start for start, end in spans.values())
    class_time = sum(end - start for row in sections for _, start, end in row["_slots"])
    penalty = (total_span - class_time) + 60 * len(used)
    if free_day and free_day in used:
        penalty += 600
    return penalty


def render(sections):
    """A compact weekly grid."""
    spans = day_span(sections)
    lines = []
    for day in DAYS:
        if day not in spans:
            continue
        entries = []
        for row in sections:
            for slot_day, start, end in row["_slots"]:
                if slot_day == day:
                    entries.append((start, f"{fmt_time(start)}-{fmt_time(end)}  "
                                           f"{row['_key']} {row['section'].split()[0]}"
                                           f"  {row['room'][:30]}"))
        body = "\n         ".join(text for _, text in sorted(entries))
        lines.append(f"   {day}   {body}")
    return "\n".join(lines)


def search(by_course, must, pools, earliest, free_day, limit):
    """Conflict-free timetables: all `must` courses plus one course per pool."""
    options = []
    for key in must:
        opts = [(key, e) for e in enrolments(by_course.get(key, []), earliest)]
        if not opts:
            return [], f"{key} has no section meeting the constraints"
        options.append(opts)
    for pool in pools:
        opts = [(key, e) for key in pool
                for e in enrolments(by_course.get(key, []), earliest)]
        if not opts:
            return [], f"no course in {pool} has a section meeting the constraints"
        options.append(opts)

    results = []
    for combo in itertools.product(*options):
        picked = [key for key, _ in combo]
        if len(set(picked)) != len(picked):
            continue
        sections = [row for _, enrol in combo for row in enrol]
        if any(overlaps(sections[i]["_slots"], sections[j]["_slots"])
               for i in range(len(sections)) for j in range(i + 1, len(sections))):
            continue
        results.append((score(sections, free_day), picked, sections))
    results.sort(key=lambda r: (r[0], r[1]))
    return results[:limit], None


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("csv", help="catalogue CSV from wcq_scrape.py")
    parser.add_argument("--earliest", default="10:30",
                        help="no class may start before this (HH:MM, 24h)")
    parser.add_argument("--free-day", default="Fr",
                        help="weekday to try to keep clear, or '' for none")
    parser.add_argument("--must", action="append", default=[],
                        help="course that must be taken; repeatable")
    parser.add_argument("--pool", action="append", default=[],
                        help="comma-separated courses to choose ONE of; repeatable")
    parser.add_argument("--top", type=int, default=3)
    parser.add_argument("--availability", action="store_true",
                        help="just list what each requirement bucket offers")
    args = parser.parse_args()

    hour, minute = (int(p) for p in args.earliest.split(":"))
    earliest = hour * 60 + minute

    wanted = {c for req in REQUIREMENTS for c in req["courses"]}
    wanted |= set(args.must)
    wanted |= {c for pool in args.pool for c in pool.split(",")}
    by_course, tba = load_sections(args.csv, wanted)

    if args.availability or not (args.must or args.pool):
        print("== availability in this term's catalogue")
        for req in REQUIREMENTS:
            print(f"\n  {req['bucket']}  (need {req['need']} cr)")
            if req.get("note"):
                print(f"    note: {req['note']}")
            for key in req["courses"]:
                rows = by_course.get(key)
                if not rows:
                    continue
                comps = sorted({r["_component"] for r in rows})
                fits = len(enrolments(rows, earliest))
                print(f"    {key}  {rows[0]['course_title'][:40]:<40} "
                      f"{course_credits(rows):.0f} cr  "
                      f"components {'+'.join(comps)}  "
                      f"{fits} enrolment(s) after {args.earliest}")
            missing = [c for c in req["courses"] if c not in by_course]
            if missing:
                print(f"    not offered this term: {', '.join(missing)}")
        if tba:
            print(f"\n== {len(tba)} section(s) with no scheduled time "
                  f"(enrollable, but cannot be placed on the grid)")
            for row in tba:
                print(f"    {row['_key']} {row['section']}: "
                      f"{row.get('date_time') or '(blank)'}")
        if not (args.must or args.pool):
            return 0

    pools = [p.split(",") for p in args.pool]
    results, problem = search(by_course, args.must, pools,
                              earliest, args.free_day or None, args.top)
    print(f"\n== search: no start before {args.earliest}, "
          f"free day {args.free_day or 'none'}")
    print(f"   must: {', '.join(args.must) or '(none)'}")
    for pool in pools:
        print(f"   one of: {', '.join(pool)}")

    if problem:
        print(f"\n   INFEASIBLE: {problem}")
        return 1
    if not results:
        print("\n   INFEASIBLE: every combination has a time conflict")
        return 1

    for rank, (penalty, picked, sections) in enumerate(results, 1):
        total = sum(course_credits(by_course[k]) for k in picked)
        days = sorted(day_span(sections), key=DAYS.index)
        print(f"\n-- option {rank}   {total:g} credits   "
              f"{len(picked)} courses   days {'/'.join(days)}   score {penalty}")
        for key in picked:
            rows = by_course[key]
            print(f"     {key}  {rows[0]['course_title'][:46]:<46} "
                  f"{course_credits(rows):.0f} cr")
        print(render(sections))

        # Self-checks -- a schedule that violates these must never be shown.
        assert not any(overlaps(sections[i]["_slots"], sections[j]["_slots"])
                       for i in range(len(sections))
                       for j in range(i + 1, len(sections))), "overlap in result"
        assert all(start >= earliest for r in sections
                   for _, start, _ in r["_slots"]), "too-early class in result"
    return 0


if __name__ == "__main__":
    sys.exit(main())

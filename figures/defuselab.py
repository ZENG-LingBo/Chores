#!/usr/bin/env python3
"""Shared data, statistics, and plotting setup for the DefuseLab figures.

Every figure script in this folder imports this module, so the numbers a figure
draws are the same ones the manuscript prints. Nothing here draws anything.

Inputs  (repo-relative): data/defuselab-messages.csv  (concatenated exports, deduped by event_id)
                         data/defuselab-sessions.csv  (per participant-session rows)
                         data/defuselab-surveys.csv   (post-Day-1 outcome battery)

The Community Note appeared 15 minutes into the session (from the study
protocol; the export carries no trigger event). Messages before the onset form
the "free" phase, messages after it the "note" phase, and the reporting windows
are aligned to that boundary.
"""
import csv
import math
import os
from collections import defaultdict
from datetime import datetime

import numpy as np
from scipy import stats as st

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data")
PAPER_FIGS = os.path.join(ROOT, "paper", "figures")  # vector copies for LaTeX

NOTE_ONSET_MIN = 15.0
WINDOW_MIN = 5.0  # reporting windows; must divide NOTE_ONSET_MIN so the
                  # note falls on a window edge rather than inside a bar

# Validated palette (dataviz reference instance, light mode)
BLUE = "#2a78d6"     # baseline / free phase / Day 1
ORANGE = "#eb6834"   # intervention / note phase / highlight
LIGHT_BLUE = "#9ec5f4"
VIOLET = "#4a3aa7"   # ARMY badge (teaser diagram)
MAGENTA = "#e87ba4"  # BLINK badge (teaser diagram)
INK = "#0b0b0b"
INK2 = "#52514e"
GRID = "#e5e4e0"
SURFACE = "#ffffff"

# ---------------------------------------------------------------- loading ---

def load_messages():
    hdr = ["event_id", "cohort", "day", "arm", "fandom", "handle", "type", "is_seed",
           "toxicity_0_100", "we", "they", "thread_id", "created_at_iso", "text_raw"]
    uniq = {}
    with open(os.path.join(DATA, "defuselab-messages.csv"), encoding="utf-8-sig") as f:
        for row in csv.reader(f):
            if not row or not row[0].startswith("ev_"):
                continue
            d = dict(zip(hdr, row))
            # keep the richest duplicate (some export blocks drop thread/text columns)
            if d["event_id"] not in uniq or (d.get("text_raw") and not uniq[d["event_id"]].get("text_raw")):
                uniq[d["event_id"]] = d
    rows = sorted(uniq.values(), key=lambda r: r["created_at_iso"])
    t0 = datetime.fromisoformat(rows[0]["created_at_iso"].replace("Z", "+00:00"))
    for r in rows:
        t = datetime.fromisoformat(r["created_at_iso"].replace("Z", "+00:00"))
        r["min"] = (t - t0).total_seconds() / 60.0
        r["tox"] = float(r["toxicity_0_100"]) / 100.0
        r["we"] = int(r["we"])
        r["they"] = int(r["they"])
        r["phase"] = "free" if r["min"] < NOTE_ONSET_MIN else "note"
    return rows


def load_sessions():
    with open(os.path.join(DATA, "defuselab-sessions.csv"), encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def load_surveys():
    with open(os.path.join(DATA, "defuselab-surveys.csv"), encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    latest = {}
    for r in rows:  # keep each participant's latest submission
        k = r["participant_id"]
        if k not in latest or r["submitted_at_iso"] > latest[k]["submitted_at_iso"]:
            latest[k] = r
    return list(latest.values())


msgs = load_messages()
sessions = load_sessions()
surveys = load_surveys()

# anonymized participant codes: ARMY -> A1.., BLINK -> B1.. (sorted by handle)
handles = sorted({r["handle"] for r in msgs})
code = {}
for fan in ("army", "blink"):
    for i, h in enumerate([h for h in handles if h.startswith(fan)], 1):
        code[h] = ("A" if fan == "army" else "B") + str(i)

free = [r for r in msgs if r["phase"] == "free"]
note = [r for r in msgs if r["phase"] == "note"]
free_tox = np.array([r["tox"] for r in free])
note_tox = np.array([r["tox"] for r in note])

S = {}  # -> paper/stats.tex macros
S["nMessages"] = len(msgs)
S["nParticipants"] = len(handles)
S["sessionMinutes"] = int(round(msgs[-1]["min"]))
S["nFreeMsgs"] = len(free)
S["nNoteMsgs"] = len(note)
S["freeMean"] = f"{free_tox.mean():.3f}"
S["noteMean"] = f"{note_tox.mean():.3f}"
S["redPct"] = f"{100 * (1 - note_tox.mean() / free_tox.mean()):.0f}"

# message-level Welch test, free vs note
welch_msg = st.ttest_ind(free_tox, note_tox, equal_var=False)
t_msg, p_msg = welch_msg.statistic, welch_msg.pvalue
S["msgWelchT"] = f"{t_msg:.2f}"
S["msgWelchDf"] = f"{welch_msg.df:.1f}"
S["msgWelchP"] = f"{p_msg:.3f}"

# reporting windows, aligned to the note onset and covering the whole session:
# the final window is a full slot that the session ends partway into.
assert NOTE_ONSET_MIN % WINDOW_MIN == 0, "windows must align with the note onset"
session_end = msgs[-1]["min"]
n_win = math.ceil(session_end / WINDOW_MIN)
win_edges = [w * WINDOW_MIN for w in range(n_win + 1)]
win_means, win_ns, win_labels = [], [], []
for lo, hi in zip(win_edges[:-1], win_edges[1:]):
    ws = [r["tox"] for r in msgs if lo <= r["min"] < hi]
    win_means.append(np.mean(ws))
    win_ns.append(len(ws))
    win_labels.append(f"{lo:.0f}\u2013{hi:.0f}")
n_pre = int(NOTE_ONSET_MIN // WINDOW_MIN)  # windows before the note appears
for letter, m in zip("ABCDE", win_means):
    S["win" + letter] = f"{m:.3f}"
S["winPeak"] = f"{max(win_means[:n_pre]):.3f}"          # highest window before the note
S["winPreMin"] = f"{min(win_means[:n_pre]):.3f}"        # lowest window before the note
S["winFirstNote"] = f"{win_means[n_pre]:.3f}"           # first window after the note
S["winPostMax"] = f"{max(win_means[n_pre:]):.3f}"       # highest window after the note
S["winLast"] = f"{win_means[-1]:.3f}"
S["dropAtNote"] = f"{100 * (1 - win_means[n_pre] / max(win_means[:n_pre])):.0f}"
S["winMin"] = f"{min(win_means):.3f}"                   # lowest window of the session
S["nWindows"] = len(win_means)
S["winNs"] = ", ".join(str(n) for n in win_ns)
S["windowMin"] = f"{WINDOW_MIN:.0f}"
S["noteOnsetMin"] = f"{NOTE_ONSET_MIN:.0f}"

# peak window before the note vs trough window after it (Ray: clearest contrast)
peak_i = int(np.argmax(win_means[:n_pre]))
trough_i = n_pre + int(np.argmin(win_means[n_pre:]))
peak_msgs = [r["tox"] for r in msgs
             if win_edges[peak_i] <= r["min"] < win_edges[peak_i + 1]]
trough_msgs = [r["tox"] for r in msgs
               if win_edges[trough_i] <= r["min"] < win_edges[trough_i + 1]]
pt = st.ttest_ind(peak_msgs, trough_msgs, equal_var=False)
S["peakWin"] = win_labels[peak_i]
S["troughWin"] = win_labels[trough_i]
S["peakWinM"] = f"{np.mean(peak_msgs):.3f}"
S["troughWinM"] = f"{np.mean(trough_msgs):.3f}"
S["peakWinN"] = len(peak_msgs)
S["troughWinN"] = len(trough_msgs)
S["peakTroughT"] = f"{pt.statistic:.2f}"
S["peakTroughDf"] = f"{pt.df:.1f}"
S["peakTroughP"] = f"{pt.pvalue:.3f}"
S["peakTroughDrop"] = f"{100 * (1 - np.mean(trough_msgs) / np.mean(peak_msgs)):.0f}"

# free-phase linear trend (toxicity vs minute)
slope, intercept, r_v, p_v, se = st.linregress([r["min"] for r in free], free_tox)
S["freeSlope"] = f"{slope:.4f}"
S["freeSlopeP"] = f"{p_v:.2f}"

# per-participant phase means
per = defaultdict(lambda: {"free": [], "note": []})
for r in msgs:
    per[r["handle"]][r["phase"]].append(r["tox"])
paired = {h: (np.mean(d["free"]), np.mean(d["note"]))
          for h, d in per.items() if d["free"] and d["note"]}
diffs = np.array([b - a for a, b in paired.values()])
t_pair, p_pair = st.ttest_rel([b for _, b in paired.values()], [a for a, _ in paired.values()])
S["pairedN"] = len(paired)
S["pairedT"] = f"{t_pair:.2f}"
S["pairedDf"] = len(paired) - 1
S["pairedP"] = f"{p_pair:.3f}"
S["pairedDz"] = f"{abs(diffs.mean() / diffs.std(ddof=1)):.2f}"
S["pairedMeanDiff"] = f"{diffs.mean():.3f}"
S["pctDeclined"] = f"{100 * np.mean(diffs < 0):.0f}"
S["nDeclined"] = int((diffs < 0).sum())

# leave-one-out robustness of the group-level drop
loo = []
for h in handles:
    a = [r["tox"] for r in free if r["handle"] != h]
    b = [r["tox"] for r in note if r["handle"] != h]
    if a and b:
        loo.append(np.mean(a) - np.mean(b))
S["looMin"], S["looMax"] = f"{min(loo):.3f}", f"{max(loo):.3f}"

# concentration: top-3 posters, top cross-fandom reply pair
counts = defaultdict(int)
for r in msgs:
    counts[r["handle"]] += 1
top3 = sum(sorted(counts.values())[-3:])
S["topThreePct"] = f"{100 * top3 / len(msgs):.0f}"
author = {r["event_id"]: r["handle"] for r in msgs}
pair_counts = defaultdict(int)
replies = [r for r in msgs if r["type"] == "comment" and r["thread_id"] in author]
for r in replies:
    pa = author[r["thread_id"]]
    if pa[:4] != r["handle"][:4]:
        pair_counts[tuple(sorted((r["handle"], pa)))] += 1
top_pair, top_pair_n = max(pair_counts.items(), key=lambda kv: kv[1])
S["nReplies"] = len([r for r in msgs if r["type"] == "comment"])
S["topPairN"] = top_pair_n
S["topPairA"], S["topPairB"] = code[top_pair[0]], code[top_pair[1]]

# most active / most toxic participants
most_active = max(counts, key=counts.get)
most_toxic = max(per, key=lambda h: np.mean(per[h]["free"] + per[h]["note"]))
S["mostActiveCode"] = code[most_active]
S["mostActiveFreeN"] = len(per[most_active]["free"])
S["mostActiveNoteN"] = len(per[most_active]["note"])
S["mostActiveFreeM"] = f"{np.mean(per[most_active]['free']):.3f}"
S["mostActiveNoteM"] = f"{np.mean(per[most_active]['note']):.3f}"
S["mostToxicCode"] = code[most_toxic]
S["mostToxicM"] = f"{np.mean(per[most_toxic]['free'] + per[most_toxic]['note']):.3f}"
S["mostToxicNoteM"] = f"{np.mean(per[most_toxic]['note']):.3f}"
S["mostToxicNoteMax"] = f"{max(per[most_toxic]['note']):.2f}"


# pronoun shift
def rate(rows, key):
    return sum(r[key] for r in rows) / len(rows)


def they_prop(rows):
    return sum(r["they"] for r in rows) / max(1, sum(r["they"] + r["we"] for r in rows))


S["theyFree"], S["theyNote"] = f"{rate(free, 'they'):.2f}", f"{rate(note, 'they'):.2f}"
S["weFree"], S["weNote"] = f"{rate(free, 'we'):.2f}", f"{rate(note, 'we'):.2f}"
S["theyPropFree"], S["theyPropNote"] = f"{they_prop(free):.3f}", f"{they_prop(note):.3f}"

# --------------------------------------------------------------- sessions ---
# participant-session rows; TEST1 cohort is the fully message-logged session

def active(rows):
    return np.array([float(r["mean_toxicity"]) for r in rows if r["mean_toxicity"]])


expt = [r for r in sessions if r["arm"] == "EXPT"]
d1_all, d2_all = active([r for r in expt if r["day"] == "1"]), active([r for r in expt if r["day"] == "2"])
t_day, p_day = st.ttest_ind(d1_all, d2_all, equal_var=False)
S["dayOneN"], S["dayTwoN"] = len(d1_all), len(d2_all)
S["dayOneM"], S["dayTwoM"] = f"{d1_all.mean():.3f}", f"{d2_all.mean():.3f}"
S["dayWelchT"], S["dayWelchP"] = f"{t_day:.2f}", f"{p_day:.2f}"

test1_d2 = active([r for r in sessions if r["cohort"] == "TEST1" and r["day"] == "2"])
S["tOneDayTwoN"], S["tOneDayTwoM"] = len(test1_d2), f"{test1_d2.mean():.3f}"

# participant-level phase means for the studied session + Day-2 comparison
free_p = np.array([np.mean(d["free"]) for d in per.values() if d["free"]])
note_p = np.array([np.mean(d["note"]) for d in per.values() if d["note"]])
S["freePartM"], S["notePartM"] = f"{free_p.mean():.3f}", f"{note_p.mean():.3f}"
t_nd2, p_nd2 = st.ttest_ind(note_p, test1_d2, equal_var=False)
t_fd2, p_fd2 = st.ttest_ind(free_p, test1_d2, equal_var=False)
S["noteDayTwoT"], S["noteDayTwoP"] = f"{t_nd2:.2f}", f"{p_nd2:.2f}"
S["freeDayTwoT"], S["freeDayTwoP"] = f"{t_fd2:.2f}", f"{p_fd2:.2f}"

S["nCohorts"] = len({r["cohort"] for r in sessions})

# ---------------------------------------------------------------- surveys ---
sv = [r for r in surveys if r["arm"] == "EXPT"]
S["surveyN"] = len(sv)


def scale(rows, prefix):
    vals = []
    for r in rows:
        items = [float(r[k]) for k in r if k.startswith(prefix) and r[k]]
        if items:
            vals.append(np.mean(items))
    return np.array(vals)


SCALES = {
    "legit": ("s1_legit", "Legitimacy of the note"),
    "react": ("s1_react", "Reactance toward the note"),
    "simil": ("s1_simil", "Perceived similarity to rival fandom"),
    "perc": ("s1_perc", "Perception of rival fandom"),
    "contact": ("s1_contact", "Cross-fandom contact intentions"),
    "sess": ("s1_sess", "Session felt heated / attacked"),
    "ipt": ("s1_ipt", "Intergroup perspective taking"),
}
for _key, (_prefix, _label) in SCALES.items():
    _v = scale(sv, _prefix)
    S[_key + "M"] = f"{_v.mean():.2f}"
    S[_key + "SD"] = f"{_v.std(ddof=1):.2f}"
own = np.array([float(r["s1_therm_own"]) for r in sv])
rival = np.array([float(r["s1_therm_rival"]) for r in sv])
S["thermOwn"], S["thermRival"] = f"{own.mean():.1f}", f"{rival.mean():.1f}"
S["thermGap"] = f"{(own - rival).mean():.0f}"
S["thermGapSD"] = f"{(own - rival).std(ddof=1):.1f}"

# ---------------------------------------------------- robustness & screens ---
# Ray TODO 2: does the effect survive restricting to more active participants?
msg_counts = {h: len(per[h]["free"]) + len(per[h]["note"]) for h in per}
ROBUST_THRESHOLDS = (0, 6, 8)
robustness_rows = []
for thr in ROBUST_THRESHOLDS:
    keep = [h for h in per if msg_counts[h] >= thr]
    a = [r["tox"] for r in msgs if r["handle"] in keep and r["phase"] == "free"]
    b = [r["tox"] for r in msgs if r["handle"] in keep and r["phase"] == "note"]
    w = st.ttest_ind(a, b, equal_var=False)
    pair_h = [h for h in keep if per[h]["free"] and per[h]["note"]]
    tp = st.ttest_rel([np.mean(per[h]["note"]) for h in pair_h],
                      [np.mean(per[h]["free"]) for h in pair_h])
    robustness_rows.append({
        "thr": thr, "nPart": len(keep), "nFree": len(a), "nNote": len(b),
        "freeM": np.mean(a), "noteM": np.mean(b),
        "t": w.statistic, "p": w.pvalue,
        "pairN": len(pair_h), "pairT": tp.statistic, "pairP": tp.pvalue,
    })
for i, row in enumerate(robustness_rows):
    tag = ["All", "Six", "Eight"][i]
    S["rob" + tag + "Part"] = row["nPart"]
    S["rob" + tag + "T"] = f"{row['t']:.2f}"
    S["rob" + tag + "P"] = f"{row['p']:.3f}"
    S["rob" + tag + "PairP"] = f"{row['pairP']:.3f}"

# Ray item 9: pre-registered screens on the survey respondents
survey_items = [k for k in surveys[0] if k.startswith("s1_") and not k.startswith("s1_therm")]
def straightlined(r):
    v = [float(r[k]) for k in survey_items if r[k]]
    return np.std(v) < 0.5
def failed_heat_check(r):  # the session was designed to be heated
    return float(r["s1_sess_heated"]) <= 2
S["nStraightlined"] = sum(1 for r in surveys if straightlined(r))
S["nStraightlinedExpt"] = sum(1 for r in sv if straightlined(r))
S["nFailedHeat"] = sum(1 for r in sv if failed_heat_check(r))
S["minHeat"] = f"{min(float(r['s1_sess_heated']) for r in sv):.0f}"

# ------------------------------------ enemies online, not in real life -------
contact_items = {
    "s1_contact_friends": "Could be friends",
    "s1_contact_discuss": "Would discuss K-pop",
    "s1_contact_work": "Would work together",
    "s1_contact_share": "Would share a post",
}
contact_means = {k: np.mean([float(r[k]) for r in sv if r[k]]) for k in contact_items}
S["contactFriends"] = f"{contact_means['s1_contact_friends']:.2f}"
S["contactMax"] = f"{max(contact_means.values()):.2f}"
one_samp = st.ttest_1samp(scale(sv, "s1_contact"), 3.0)
S["contactVsMidT"] = f"{one_samp.statistic:.2f}"
S["contactVsMidP"] = f"{one_samp.pvalue:.2f}"

# =========================================================== plotting setup ==
import matplotlib  # noqa: E402  (backend must be set before pyplot import)

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch  # noqa: E402,F401

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 8,
    "axes.edgecolor": INK2, "axes.linewidth": 0.6,
    "axes.labelcolor": INK, "text.color": INK,
    "xtick.color": INK2, "ytick.color": INK2,
    "axes.titlesize": 8.5, "axes.titleweight": "bold",
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE,
    "pdf.fonttype": 42,
})


def save(fig, name):
    """Write <name>.png beside the figure scripts and <name>.pdf for LaTeX."""
    png = os.path.join(HERE, name + ".png")
    fig.savefig(png, dpi=300)
    os.makedirs(PAPER_FIGS, exist_ok=True)
    fig.savefig(os.path.join(PAPER_FIGS, name + ".pdf"))
    plt.close(fig)
    print("wrote", png, "and", os.path.join(PAPER_FIGS, name + ".pdf"))


def clean_axes(ax, ygrid=True):
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    if ygrid:
        ax.grid(axis="y", color=GRID, linewidth=0.6)
        ax.set_axisbelow(True)


def bar_labels(ax, bars, fmt="{:.3f}", dy=0.004):
    for b in bars:
        ax.text(b.get_x() + b.get_width() / 2, b.get_height() + dy,
                fmt.format(b.get_height()), ha="center", va="bottom",
                fontsize=7.5, color=INK)


def write_stats_tex():
    """Regenerate paper/stats.tex, the macros the manuscript's numbers come from."""
    def texify(k):  # LaTeX macro names cannot contain digits
        return "Stat" + k.replace("1", "One").replace("2", "Two").replace("3", "Three")

    path = os.path.join(ROOT, "paper", "stats.tex")
    with open(path, "w") as f:
        f.write("% Auto-generated by figures/make_all.py -- do not edit by hand.\n")
        for k, v in S.items():
            f.write(f"\\newcommand{{\\{texify(k)}}}{{{v}}}\n")
    return path

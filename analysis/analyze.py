#!/usr/bin/env python3
"""DefuseLab analysis: compute statistics and generate paper figures.

Inputs  (repo-relative): data/defuselab-messages.csv  (5 concatenated exports, deduped by event_id)
                         data/defuselab-sessions.csv  (per participant-session rows)
                         data/defuselab-surveys.csv   (post-Day-1 outcome battery)
Outputs: paper/figures/*.pdf and paper/stats.tex (LaTeX macros used by main.tex)

The Community Note onset is taken as 20 minutes after the first message of the
session (no explicit trigger timestamp exists in the export); messages before
the onset form the "free" phase, messages after it the "note" phase.
"""
import csv
import json
import math
import os
from collections import defaultdict
from datetime import datetime

import numpy as np
from scipy import stats as st

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
FIGS = os.path.join(ROOT, "paper", "figures")
os.makedirs(FIGS, exist_ok=True)

NOTE_ONSET_MIN = 20.0

# Validated palette (dataviz reference instance, light mode)
BLUE = "#2a78d6"     # baseline / free phase / Day 1
ORANGE = "#eb6834"   # intervention / note phase / highlight
VIOLET = "#4a3aa7"   # ARMY badge (teaser diagram)
MAGENTA = "#e87ba4"  # BLINK badge (teaser diagram)
INK = "#0b0b0b"
INK2 = "#52514e"
GRID = "#e5e4e0"
SURFACE = "#ffffff"

# ---------------------------------------------------------------- messages ---

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

S = {}  # -> stats.tex macros
S["nMessages"] = len(msgs)
S["nParticipants"] = len(handles)
S["sessionMinutes"] = int(round(msgs[-1]["min"]))
S["nFreeMsgs"] = len(free)
S["nNoteMsgs"] = len(note)
S["freeMean"] = f"{free_tox.mean():.3f}"
S["noteMean"] = f"{note_tox.mean():.3f}"
S["redPct"] = f"{100 * (1 - note_tox.mean() / free_tox.mean()):.0f}"

# message-level Welch test, free vs note
t_msg, p_msg = st.ttest_ind(free_tox, note_tox, equal_var=False)
df_msg = st.ttest_ind(free_tox, note_tox, equal_var=False).df
S["msgWelchT"] = f"{t_msg:.2f}"
S["msgWelchDf"] = f"{df_msg:.1f}"
S["msgWelchP"] = f"{p_msg:.3f}"

# 10-minute windows
win_means, win_ns = [], []
for w in range(5):
    ws = [r["tox"] for r in msgs if w * 10 <= r["min"] < (w + 1) * 10]
    win_means.append(np.mean(ws))
    win_ns.append(len(ws))
S["winA"], S["winB"] = f"{win_means[0]:.3f}", f"{win_means[1]:.3f}"
S["winC"], S["winD"], S["winE"] = (f"{m:.3f}" for m in win_means[2:])
S["winPeak"] = f"{max(win_means[:2]):.3f}"

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

S["theyFree"], S["theyNote"] = f"{rate(free, 'they'):.2f}", f"{rate(note, 'they'):.2f}"
S["weFree"], S["weNote"] = f"{rate(free, 'we'):.2f}", f"{rate(note, 'we'):.2f}"
they_prop = lambda rows: sum(r["they"] for r in rows) / max(1, sum(r["they"] + r["we"] for r in rows))
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

n_sessions = len({r["cohort"] for r in sessions})
S["nCohorts"] = n_sessions

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

scales = {
    "legit": ("s1_legit", "Legitimacy of the note"),
    "react": ("s1_react", "Reactance toward the note"),
    "simil": ("s1_simil", "Perceived similarity to rival fandom"),
    "perc": ("s1_perc", "Perception of rival fandom"),
    "contact": ("s1_contact", "Cross-fandom contact intentions"),
    "sess": ("s1_sess", "Session felt heated / attacked"),
    "ipt": ("s1_ipt", "Intergroup perspective taking"),
}
for key, (prefix, _) in scales.items():
    v = scale(sv, prefix)
    S[key + "M"] = f"{v.mean():.2f}"
    S[key + "SD"] = f"{v.std(ddof=1):.2f}"
own = np.array([float(r["s1_therm_own"]) for r in sv])
rival = np.array([float(r["s1_therm_rival"]) for r in sv])
S["thermOwn"], S["thermRival"] = f"{own.mean():.1f}", f"{rival.mean():.1f}"
S["thermGap"] = f"{(own - rival).mean():.0f}"
S["thermGapSD"] = f"{(own - rival).std(ddof=1):.1f}"

# ================================================================= figures ==
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 8,
    "axes.edgecolor": INK2, "axes.linewidth": 0.6,
    "axes.labelcolor": INK, "text.color": INK,
    "xtick.color": INK2, "ytick.color": INK2,
    "axes.titlesize": 8.5, "axes.titleweight": "bold",
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE,
    "pdf.fonttype": 42,
})



INSPECT = os.environ.get("INSPECT_DIR")

def save(fig, name):
    fig.savefig(os.path.join(FIGS, name + ".pdf"))
    if INSPECT:
        fig.savefig(os.path.join(INSPECT, name + ".png"), dpi=150)

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

# ------------------------------------------------------------ fig 1 teaser --

def rounded(ax, x, y, w, h, fc, ec, lw=0.8, r=0.015):
    p = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}",
                       fc=fc, ec=ec, lw=lw, mutation_aspect=1)
    ax.add_patch(p)
    return p


def badge(ax, x, y, fandom):
    col = VIOLET if fandom == "ARMY" else MAGENTA
    rounded(ax, x, y, 0.085, 0.055, col, col, r=0.01)
    ax.text(x + 0.0425, y + 0.0275, fandom, ha="center", va="center",
            fontsize=5.2, color="white", fontweight="bold")


def msg_lines(ax, x, y, w, n=2, color=GRID):
    for i in range(n):
        ax.plot([x, x + w * (0.95 if i < n - 1 else 0.6)], [y - 0.03 * i] * 2,
                color=color, lw=2.2, solid_capstyle="round")


fig = plt.figure(figsize=(7.0, 2.55))
gs = fig.add_gridspec(1, 2, width_ratios=[2.05, 1], wspace=0.22,
                      left=0.005, right=0.965, top=0.87, bottom=0.15)
ax = fig.add_subplot(gs[0])
ax.set_xlim(0, 1.60)
ax.set_ylim(0, 1)
ax.axis("off")

BOXW = 0.44

def stage(x0, title, edge=INK2):
    rounded(ax, x0, 0.06, BOXW, 0.92, "#fcfcfb", edge)
    ax.text(x0 + BOXW / 2, 0.865, title, ha="center", va="center",
            fontsize=6.4, fontweight="bold")

def caption(x0, text):
    ax.text(x0 + BOXW / 2, 0.175, text, ha="center", va="center", fontsize=5.9,
            color=INK2, style="italic")

# Stage 1: escalating mixed feed
stage(0.02, "Mixed feed\nescalates")
for i, fan in enumerate(["ARMY", "BLINK", "ARMY"]):
    yy = 0.66 - i * 0.16
    badge(ax, 0.055, yy, fan)
    msg_lines(ax, 0.16, yy + 0.045, 0.25, 2, "#c9c8c2")
caption(0.02, "toxicity climbs\npast a threshold")

arrow = FancyArrowPatch((0.475, 0.52), (0.565, 0.52), arrowstyle="-|>",
                        mutation_scale=11, color=INK2, lw=1.1)
ax.add_patch(arrow)

# Stage 2: the pinned Community Note with two slots
stage(0.58, "Community Note\n(pinned)", INK)
badge(ax, 0.615, 0.63, "ARMY")
msg_lines(ax, 0.72, 0.675, 0.26, 2, "#c9c8c2")
badge(ax, 0.615, 0.44, "BLINK")
msg_lines(ax, 0.72, 0.485, 0.26, 2, "#c9c8c2")
ax.text(0.80, 0.315, "one slot per fandom,\nverbatim under each badge",
        ha="center", fontsize=5.7, color=INK2)
caption(0.58, "publishes only when\nboth sides write")

arrow = FancyArrowPatch((1.035, 0.52), (1.125, 0.52), arrowstyle="-|>",
                        mutation_scale=11, color=INK2, lw=1.1)
ax.add_patch(arrow)

# Stage 3: co-signed note published
stage(1.14, "Co-signed note\npublished")
badge(ax, 1.19, 0.62, "ARMY")
badge(ax, 1.30, 0.62, "BLINK")
msg_lines(ax, 1.19, 0.52, 0.34, 3, "#c9c8c2")
caption(1.14, "assembled backstage\nby the LLM")
ax.text(0.0, 1.08, "A", fontsize=9, fontweight="bold", va="top")

# Panel B: the story in one bar pair
axb = fig.add_subplot(gs[1])
bars = axb.bar([0, 1], [free_tox.mean(), note_tox.mean()], width=0.62,
               color=[BLUE, ORANGE], edgecolor=SURFACE, linewidth=1.5)
bar_labels(axb, bars)
axb.set_xticks([0, 1])
axb.set_xticklabels([f"20 min before\nthe note (n={len(free)})",
                     f"20 min after\nthe note (n={len(note)})"], fontsize=7)
axb.set_ylabel("Mean message toxicity", fontsize=7.5)
axb.set_ylim(0, 0.42)
clean_axes(axb)
axb.annotate(f"−{S['redPct']}%", xy=(1, note_tox.mean() + 0.055),
             xytext=(0.62, free_tox.mean() + 0.02), fontsize=8.5,
             fontweight="bold", color=ORANGE,
             arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.2,
                             connectionstyle="arc3,rad=-0.25"))
axb.set_title("Toxicity around the note", fontsize=7.5, pad=4)
axb.text(-0.75, 0.475, "B", fontsize=9, fontweight="bold")
save(fig, "fig_teaser")
plt.close(fig)

# ------------------------------------------------------- fig 2: windows -----
fig, ax = plt.subplots(figsize=(3.35, 2.1), constrained_layout=True)
xs = np.arange(5)
cols = [BLUE if x < 2 else ORANGE for x in xs]
bars = ax.bar(xs, win_means, width=0.68, color=cols, edgecolor=SURFACE, linewidth=1.5)
bar_labels(ax, bars)
ax.axvline(1.5, color=INK, lw=0.9, ls=(0, (4, 2)))
ax.text(1.5, 0.435, "Community Note appears", ha="center", fontsize=6.8,
        color=INK, fontweight="bold")
ax.set_xticks(xs)
ax.set_xticklabels([f"{w*10}–{w*10+10}" for w in range(5)], fontsize=7)
ax.set_xlabel("Minutes into the session", fontsize=7.5)
ax.set_ylabel("Mean message toxicity", fontsize=7.5)
ax.set_ylim(0, 0.47)
clean_axes(ax)
handles_ = [plt.Rectangle((0, 0), 1, 1, fc=BLUE), plt.Rectangle((0, 0), 1, 1, fc=ORANGE)]
ax.legend(handles_, ["Free phase", "Note phase"], frameon=False, fontsize=7,
          loc="upper right", handlelength=1.1, handleheight=1.0, borderaxespad=0.1)
save(fig, "fig_windows")
plt.close(fig)

# ------------------------------------------------- fig 3: paired slopes -----
fig, ax = plt.subplots(figsize=(3.35, 2.5), constrained_layout=True)
# dodge right-hand labels so close endpoints stay readable
ends = sorted(((paired[h][1], h) for h in paired))
label_y = {}
prev = -1.0
for b, h in ends:
    y = max(b, prev + 0.033)
    label_y[h] = y
    prev = y
for h in sorted(paired, key=lambda h: paired[h][0]):
    a, b = paired[h]
    hot = h == most_toxic
    col = ORANGE if hot else BLUE
    ax.plot([0, 1], [a, b], color=col, lw=2.0 if hot else 1.4,
            alpha=1.0 if hot else 0.75, zorder=3 if hot else 2,
            marker="o", markersize=5, markeredgecolor=SURFACE, markeredgewidth=1.0)
    label = code[h] + (" (most toxic)" if hot else "")
    ax.annotate(label, xy=(1, b), xytext=(1.045, label_y[h]), fontsize=7,
                color=ORANGE if hot else INK2, va="center")
ax.set_xlim(-0.14, 1.62)
ax.set_xticks([0, 1])
ax.set_xticklabels([f"Free phase", f"Note phase"], fontsize=7.5)
ax.set_ylabel("Mean toxicity per participant", fontsize=7.5)
ax.set_ylim(0, 0.55)
clean_axes(ax)
ax.text(0.98, 0.055,
        f"paired t({len(paired)-1}) = {t_pair:.2f}, p = {p_pair:.3f}, "
        f"$d_z$ = {S['pairedDz']}\n{S['nDeclined']} of {len(paired)} participants declined",
        fontsize=6.8, color=INK2, va="bottom", ha="right",
        transform=ax.transAxes)
save(fig, "fig_participants")
plt.close(fig)

# ---------------------------------------------- fig 4: toxicity histogram ---
bins = np.arange(0, 1.1, 0.1)
fig, axes = plt.subplots(1, 2, figsize=(6.9, 2.15), sharey=True, constrained_layout=True)
for ax, phase, rows, mcol in ((axes[0], "Free phase", free, BLUE),
                              (axes[1], "Note phase", note, ORANGE)):
    hot = [r["tox"] for r in rows if r["handle"] == most_toxic]
    rest = [r["tox"] for r in rows if r["handle"] != most_toxic]
    ax.hist([rest, hot], bins=bins, stacked=True, color=[BLUE, ORANGE],
            edgecolor=SURFACE, linewidth=1.2, rwidth=1.0)
    # texture on the highlighted participant's segment
    n_rest, _ = np.histogram(rest, bins=bins)
    n_hot, _ = np.histogram(hot, bins=bins)
    for x0, nr, nh in zip(bins[:-1], n_rest, n_hot):
        if nh:
            ax.bar(x0 + 0.05, nh, bottom=nr, width=0.1, color="none",
                   edgecolor=SURFACE, linewidth=0.0, hatch="///")
    m = np.mean([r["tox"] for r in rows])
    ax.axvline(m, color=INK, lw=0.9, ls=(0, (4, 2)))
    ax.text(m + 0.02, 16.0, f"mean {m:.2f}", fontsize=6.8, color=INK)
    ax.set_title(f"{phase} (n = {len(rows)})", fontsize=7.5)
    ax.set_xlabel("Message toxicity", fontsize=7.5)
    ax.set_xlim(0, 1.0)
    clean_axes(ax)
axes[0].set_ylabel("Messages", fontsize=7.5)
axes[0].set_ylim(0, 21)
leg = [plt.Rectangle((0, 0), 1, 1, fc=BLUE),
       plt.Rectangle((0, 0), 1, 1, fc=ORANGE, hatch="///", ec=SURFACE)]
axes[1].legend(leg, ["All other participants", f"Most toxic participant ({code[most_toxic]})"],
               frameon=False, fontsize=7, loc="center right", handlelength=1.1)
save(fig, "fig_histogram")
plt.close(fig)

# --------------------------------------------------- fig 5: across days -----
fig, ax = plt.subplots(figsize=(3.35, 2.3), constrained_layout=True)
groups = [("Day 1\nfree phase", free_p, BLUE),
          ("Day 1\nnote phase", note_p, ORANGE),
          ("Day 2\nno feature", test1_d2, "#9ec5f4")]
rng = np.random.default_rng(7)
for i, (label, vals, col) in enumerate(groups):
    ax.bar(i, vals.mean(), width=0.6, color=col, edgecolor=SURFACE, linewidth=1.5)
    ax.text(i - 0.36, vals.mean(), f"{vals.mean():.3f}", ha="right", va="center",
            fontsize=7, color=INK)
    jitter = rng.uniform(-0.11, 0.11, len(vals))
    ax.scatter(i + jitter, vals, s=14, color=INK, zorder=3,
               edgecolor=SURFACE, linewidth=0.7)
ax.set_xticks(range(3))
ax.set_xticklabels([f"{g[0]}\n(n={len(g[1])})" for g in groups], fontsize=7)
ax.set_ylabel("Mean toxicity per participant", fontsize=7.5)
ax.set_xlim(-0.75, 2.55)
ax.set_ylim(0, 0.60)
clean_axes(ax)
ax.text(0.99, 0.985,
        f"free vs. Day 2: Welch t = {t_fd2:.2f}, p = {p_fd2:.2f} (n.s.)\n"
        f"note vs. Day 2: Welch t = {t_nd2:.2f}, p = {p_nd2:.2f} (n.s.)",
        fontsize=6.6, color=INK2, va="top", ha="right", transform=ax.transAxes)
save(fig, "fig_days")
plt.close(fig)

# ================================================================ stats.tex =
def texify(k):
    # LaTeX macro names cannot contain digits
    return "Stat" + k.replace("1", "One").replace("2", "Two").replace("3", "Three")

with open(os.path.join(ROOT, "paper", "stats.tex"), "w") as f:
    f.write("% Auto-generated by analysis/analyze.py -- do not edit by hand.\n")
    for k, v in S.items():
        f.write(f"\\newcommand{{\\{texify(k)}}}{{{v}}}\n")

print(json.dumps(S, indent=2))
print("\nParticipant codes:", {code[h]: h for h in handles})
print("Figures written to", FIGS)

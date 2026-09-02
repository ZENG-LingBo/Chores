#!/usr/bin/env python3
"""Shared data, statistics, and plotting setup for the DefuseLab figures.

Every figure script in this folder imports this module, so the numbers a figure
draws are the same ones the manuscript prints. Nothing here draws anything.

Inputs (repo-relative):
    data/defuselab-all-messages.csv   the coded KFeed message log: five sessions
                                      (S1-S5) x two arms (EXPT = Community Note,
                                      CTRL = inert feature) x two days, six
                                      participants (3 ARMY + 3 BLINK) per
                                      session-arm; flattened from
                                      data/raw/all_data.xlsx by convert_all_data.py
    data/defuselab-surveys.csv        post-Day-1 outcome battery (pilot cohorts)

Design facts read from the log and asserted below: the assigned feature
appeared 35 minutes into every Day-1 session in both arms (the `phase` column
switches from pre_note to post_note there); sessions ran ~60 minutes; Day 2
had no feature. Toxicity is the platform's 0-100 score and is reported on
that scale.
"""
import csv
import math
import os
from collections import defaultdict

import numpy as np
from scipy import stats as st

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data")
PAPER_FIGS = os.path.join(ROOT, "paper", "figures")  # vector copies for LaTeX

NOTE_ONSET_MIN = 35.0   # feature onset (both arms), checked against `phase` below
SESSION_MIN = 60.0      # nominal session length
WINDOW_MIN = 5.0        # reporting windows; the onset falls on a window edge

ARMS = ("EXPT", "CTRL")
ARM_NAME = {"EXPT": "Community Note", "CTRL": "Control"}

# Validated palette (dataviz reference instance, light mode)
BLUE = "#2a78d6"      # control arm
ORANGE = "#eb6834"    # Community Note arm / highlight
LIGHT_BLUE = "#9ec5f4"
LIGHT_ORANGE = "#f6b89d"
VIOLET = "#4a3aa7"    # ARMY badge (teaser diagram)
MAGENTA = "#e87ba4"   # BLINK badge (teaser diagram)
INK = "#0b0b0b"
INK2 = "#52514e"
GRID = "#e5e4e0"
SURFACE = "#ffffff"
ARM_COLOR = {"EXPT": ORANGE, "CTRL": BLUE}
ARM_LIGHT = {"EXPT": LIGHT_ORANGE, "CTRL": LIGHT_BLUE}

# ---------------------------------------------------------------- loading ---

PHASE = {"pre_note": "pre", "post_note": "post", "day2_no_note": "day2"}


def load_messages():
    with open(os.path.join(DATA, "defuselab-all-messages.csv"), encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        r["min"] = float(r["elapsed_min"])
        r["tox"] = float(r["toxicity_0_100"])
        r["day"] = int(r["day"])
        r["cond"] = r["condition"]
        r["phase"] = PHASE[r["phase"]]
        r["outgroup"] = r["outgroup_ref"] == "True"
        r["heavy"] = r["heavy_poster"] == "True"
        r["task"] = r["topic"] == "note_task"
    rows.sort(key=lambda r: (r["session"], r["cond"], r["day"], r["min"]))
    return rows


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
surveys = load_surveys()
SESSIONS = sorted({r["session"] for r in msgs})

# the phase column must agree with the protocol onset (a few seconds of slack)
_mis = [r for r in msgs if r["day"] == 1
        and (r["phase"] == "pre") != (r["min"] < NOTE_ONSET_MIN)]
assert len(_mis) <= 2, f"{len(_mis)} rows disagree with a {NOTE_ONSET_MIN}-min onset"

d1 = [r for r in msgs if r["day"] == 1]
d2 = [r for r in msgs if r["day"] == 2]


def rows_of(cond, phase, session=None):
    return [r for r in msgs if r["cond"] == cond and r["phase"] == phase
            and (session is None or r["session"] == session)]


def tox(rows):
    return np.array([r["tox"] for r in rows])


def fmt(x, nd=1):
    return f"{x:.{nd}f}"


def pfmt(p):
    return "<.001" if p < .001 else f"{p:.3f}"


S = {}  # -> paper/stats.tex macros

# ------------------------------------------------------------- design facts --
handles = sorted({(r["cond"], r["handle"]) for r in msgs})
S["nSessions"] = len(SESSIONS)
S["nMessages"] = len(msgs)
S["nDayOneMsgs"], S["nDayTwoMsgs"] = len(d1), len(d2)
S["nParticipants"] = len(handles)
S["nPerArm"] = len([h for h in handles if h[0] == "EXPT"])
S["nPerSession"] = len({r["handle"] for r in msgs if r["session"] == "S1" and r["cond"] == "EXPT"})
S["sessionMinutes"] = int(SESSION_MIN)
S["noteOnsetMin"] = int(NOTE_ONSET_MIN)
S["windowMin"] = int(WINDOW_MIN)
S["minSessionMsgs"] = min(len([r for r in d1 if r["session"] == s and r["cond"] == c])
                          for s in SESSIONS for c in ARMS)
S["maxSessionMsgs"] = max(len([r for r in d1 if r["session"] == s and r["cond"] == c])
                          for s in SESSIONS for c in ARMS)

# ------------------------------------------ arm x phase, message level -------
A = {c: {ph: tox(rows_of(c, ph)) for ph in ("pre", "post", "day2")} for c in ARMS}
for c in ARMS:
    k = c.lower()
    for ph, tag in (("pre", "Pre"), ("post", "Post"), ("day2", "DayTwo")):
        S[f"{k}{tag}N"] = len(A[c][ph])
        S[f"{k}{tag}M"] = fmt(A[c][ph].mean())
        S[f"{k}{tag}SD"] = fmt(A[c][ph].std(ddof=1))
        S[f"{k}{tag}HighPct"] = f"{100 * np.mean(A[c][ph] >= 60):.0f}"
    w = st.ttest_ind(A[c]["post"], A[c]["pre"], equal_var=False)
    S[f"{k}PrePostT"], S[f"{k}PrePostDf"], S[f"{k}PrePostP"] = fmt(w.statistic, 2), fmt(w.df), pfmt(w.pvalue)
    S[f"{k}PrePostDiff"] = fmt(A[c]["post"].mean() - A[c]["pre"].mean())
for ph, tag in (("pre", "Pre"), ("post", "Post"), ("day2", "DayTwo")):
    w = st.ttest_ind(A["EXPT"][ph], A["CTRL"][ph], equal_var=False)
    S[f"{tag.lower()}ArmT"] = fmt(w.statistic, 2)
    S[f"{tag.lower()}ArmDf"] = fmt(w.df)
    S[f"{tag.lower()}ArmP"] = pfmt(w.pvalue)
S["postArmGap"] = fmt(A["CTRL"]["post"].mean() - A["EXPT"]["post"].mean())

# ------------------------------------------- session level: change and DiD --
sess = {c: {ph: np.array([tox(rows_of(c, ph, s)).mean() for s in SESSIONS])
            for ph in ("pre", "post", "day2")} for c in ARMS}
change = {c: sess[c]["post"] - sess[c]["pre"] for c in ARMS}
did = change["CTRL"] - change["EXPT"]          # one value per session
did_t = st.ttest_1samp(did, 0.0)
for c in ARMS:
    k = c.lower()
    S[f"{k}ChangeM"] = fmt(change[c].mean())
    S[f"{k}ChangeMin"], S[f"{k}ChangeMax"] = fmt(change[c].min()), fmt(change[c].max())
    tt = st.ttest_rel(sess[c]["post"], sess[c]["pre"])
    S[f"{k}SessT"], S[f"{k}SessP"] = fmt(tt.statistic, 2), pfmt(tt.pvalue)
S["didM"], S["didSD"] = fmt(did.mean()), fmt(did.std(ddof=1))
S["didMin"], S["didMax"] = fmt(did.min()), fmt(did.max())
S["didT"], S["didDf"], S["didP"] = fmt(did_t.statistic, 2), len(did) - 1, pfmt(did_t.pvalue)
S["didDz"] = fmt(did.mean() / did.std(ddof=1), 2)
loo = [np.delete(did, i).mean() for i in range(len(did))]
S["looMin"], S["looMax"] = fmt(min(loo)), fmt(max(loo))
for ph, tag in (("pre", "Pre"), ("post", "Post"), ("day2", "DayTwo")):
    tt = st.ttest_rel(sess["EXPT"][ph], sess["CTRL"][ph])
    S[f"{tag.lower()}PairT"], S[f"{tag.lower()}PairP"] = fmt(tt.statistic, 2), pfmt(tt.pvalue)
    S[f"expt{tag}SessM"] = fmt(sess["EXPT"][ph].mean())
    S[f"ctrl{tag}SessM"] = fmt(sess["CTRL"][ph].mean())
S["dayTwoGap"] = fmt(sess["CTRL"]["day2"].mean() - sess["EXPT"]["day2"].mean())


# message-level OLS with the condition x phase interaction (Day 1 only)
def ols(y, X):
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ beta
    dof = len(y) - X.shape[1]
    s2 = resid @ resid / dof
    cov = s2 * np.linalg.inv(X.T @ X)
    se = np.sqrt(np.diag(cov))
    t = beta / se
    p = 2 * st.t.sf(np.abs(t), dof)
    return beta, se, t, p, dof


_y = tox(d1)
_expt = np.array([r["cond"] == "EXPT" for r in d1], float)
_post = np.array([r["phase"] == "post" for r in d1], float)
_X = np.column_stack([np.ones(len(_y)), _expt, _post, _expt * _post])
_b, _se, _t, _p, _dof = ols(_y, _X)
S["olsPostB"], S["olsPostT"], S["olsPostP"] = fmt(_b[2]), fmt(_t[2], 2), pfmt(_p[2])
S["olsArmB"], S["olsArmT"], S["olsArmP"] = fmt(_b[1]), fmt(_t[1], 2), pfmt(_p[1])
S["olsIntB"], S["olsIntSE"] = fmt(_b[3]), fmt(_se[3])
S["olsIntT"], S["olsIntP"], S["olsDf"] = fmt(_t[3], 2), pfmt(_p[3]), _dof

# ------------------------------------------- participant level (Day 1) ------
per = {}
for r in msgs:
    k = (r["cond"], r["handle"])
    if k not in per:
        per[k] = {"cond": r["cond"], "session": r["session"], "fandom": r["fandom"],
                  "heavy": r["heavy"], "pre": [], "post": [], "day2": []}
    per[k][r["phase"]].append(r["tox"])
for c in ARMS:
    k = c.lower()
    ps = [p for p in per.values() if p["cond"] == c]
    both = [p for p in ps if p["pre"] and p["post"]]
    pre_m = np.array([np.mean(p["pre"]) for p in both])
    post_m = np.array([np.mean(p["post"]) for p in both])
    diff = post_m - pre_m
    tt = st.ttest_rel(post_m, pre_m)
    S[f"{k}PairN"] = len(both)
    S[f"{k}PairDiff"] = fmt(diff.mean())
    S[f"{k}PairT"], S[f"{k}PairDf"], S[f"{k}PairP"] = fmt(tt.statistic, 2), len(both) - 1, pfmt(tt.pvalue)
    S[f"{k}PairDz"] = fmt(abs(diff.mean() / diff.std(ddof=1)), 2)
    S[f"{k}NDeclined"] = int((diff < 0).sum())
    S[f"{k}NRose"] = int((diff > 0).sum())
    S[f"{k}PctDeclined"] = f"{100 * np.mean(diff < 0):.0f}"
    S[f"{k}ActivePre"] = sum(1 for p in ps if p["pre"])
    S[f"{k}ActivePost"] = sum(1 for p in ps if p["post"])
    S[f"{k}KeptPosting"] = len(both)
    # participant-level means of pre and post (for the figure and text)
    S[f"{k}PrePartM"], S[f"{k}PostPartM"] = fmt(pre_m.mean()), fmt(post_m.mean())
    # heavy posters (one per session-arm, coded by the platform) vs the rest
    heavy = [p for p in both if p["heavy"]]
    peri = [p for p in both if not p["heavy"]]
    hd = np.array([np.mean(p["post"]) - np.mean(p["pre"]) for p in heavy])
    pd_ = np.array([np.mean(p["post"]) - np.mean(p["pre"]) for p in peri])
    S[f"{k}HeavyN"], S[f"{k}PeriN"] = len(heavy), len(peri)
    S[f"{k}HeavyPreM"] = fmt(np.mean([np.mean(p["pre"]) for p in heavy]))
    S[f"{k}HeavyPostM"] = fmt(np.mean([np.mean(p["post"]) for p in heavy]))
    S[f"{k}PeriPreM"] = fmt(np.mean([np.mean(p["pre"]) for p in peri]))
    S[f"{k}PeriPostM"] = fmt(np.mean([np.mean(p["post"]) for p in peri]))
    S[f"{k}HeavyDiff"], S[f"{k}PeriDiff"] = fmt(hd.mean()), fmt(pd_.mean())
    S[f"{k}HeavyDiffMin"], S[f"{k}HeavyDiffMax"] = fmt(hd.min()), fmt(hd.max())
    S[f"{k}PeriNDeclined"] = int((pd_ < 0).sum())
    S[f"{k}HeavyNRose"] = int((hd > 0).sum())
    w = st.ttest_ind(hd, pd_, equal_var=False)
    S[f"{k}HeavyPeriT"], S[f"{k}HeavyPeriDf"], S[f"{k}HeavyPeriP"] = fmt(w.statistic, 2), fmt(w.df), pfmt(w.pvalue)
    # heavy posters' share of the arm's messages, before and after
    for ph, tag in (("pre", "Pre"), ("post", "Post")):
        rows = rows_of(c, ph)
        S[f"{k}HeavyShare{tag}"] = f"{100 * np.mean([r['heavy'] for r in rows]):.0f}"
    S[f"{k}HeavyDayOneN"] = sum(len(p["pre"]) + len(p["post"]) for p in ps if p["heavy"])
heavy_all = [p for p in per.values() if p["heavy"]]
S["heavyBlinkN"] = sum(1 for p in heavy_all if p["fandom"] == "BLINK")
S["heavyTotalN"] = len(heavy_all)
S["heavyMsgPct"] = f"{100 * np.mean([r['heavy'] for r in d1]):.0f}"

# ---------------------------------------------------- engagement per arm ----
for c in ARMS:
    k = c.lower()
    n_pre, n_post = len(rows_of(c, "pre")), len(rows_of(c, "post"))
    tot_min = len(SESSIONS) * SESSION_MIN
    r_pre = n_pre / (len(SESSIONS) * NOTE_ONSET_MIN)
    r_post = n_post / (len(SESSIONS) * (SESSION_MIN - NOTE_ONSET_MIN))
    S[f"{k}RatePre"], S[f"{k}RatePost"] = fmt(r_pre, 2), fmt(r_post, 2)
    S[f"{k}RateRatio"] = fmt(r_post / r_pre, 2)
    S[f"{k}RateP"] = pfmt(st.binomtest(n_pre, n_pre + n_post, NOTE_ONSET_MIN / SESSION_MIN).pvalue)

# ---------------------------------------------- topic: the note as a task ---
for c in ARMS:
    k = c.lower()
    post = rows_of(c, "post")
    n_task = sum(r["task"] for r in post)
    S[f"{k}TaskN"] = n_task
    S[f"{k}TaskPct"] = f"{100 * n_task / len(post):.0f}"
    S[f"{k}TaskPreN"] = sum(r["task"] for r in rows_of(c, "pre"))
_tab = [[S["exptTaskN"], S["exptPostN"] - S["exptTaskN"]],
        [S["ctrlTaskN"], S["ctrlPostN"] - S["ctrlTaskN"]]]
S["taskFisherP"] = pfmt(st.fisher_exact(_tab).pvalue)
_task = tox([r for r in rows_of("EXPT", "post") if r["task"]])
_orig = tox([r for r in rows_of("EXPT", "post") if not r["task"]])
S["exptTaskTox"], S["exptOrigTox"] = fmt(_task.mean()), fmt(_orig.mean())
_w = st.ttest_ind(_task, _orig, equal_var=False)
S["exptTaskOrigT"], S["exptTaskOrigDf"], S["exptTaskOrigP"] = fmt(_w.statistic, 2), fmt(_w.df), pfmt(_w.pvalue)
S["exptOrigPreDiff"] = fmt(_orig.mean() - A["EXPT"]["pre"].mean())

# ---------------------------------- out-group references and pronouns -------
for c in ARMS:
    k = c.lower()
    for ph, tag in (("pre", "Pre"), ("post", "Post"), ("day2", "DayTwo")):
        rows = rows_of(c, ph)
        S[f"{k}Out{tag}"] = fmt(np.mean([r["outgroup"] for r in rows]), 2)
        S[f"{k}They{tag}"] = fmt(np.mean([r["pronoun"] == "they" for r in rows]), 2)
        S[f"{k}Named{tag}"] = fmt(np.mean([r["pronoun"] == "named" for r in rows]), 2)
    they_pre = np.mean([r["pronoun"] == "they" for r in rows_of(c, "pre")])
    they_post = np.mean([r["pronoun"] == "they" for r in rows_of(c, "post")])
    S[f"{k}TheyDropPct"] = f"{100 * (1 - they_post / they_pre):.0f}"
    _t = [[sum(r["pronoun"] == "they" for r in rows_of(c, "post")),
           sum(r["pronoun"] != "they" for r in rows_of(c, "post"))],
          [sum(r["pronoun"] == "they" for r in rows_of(c, "pre")),
           sum(r["pronoun"] != "they" for r in rows_of(c, "pre"))]]
    S[f"{k}TheyFisherP"] = pfmt(st.fisher_exact(_t).pvalue)

# ----------------------------------------------------- five-minute windows --
assert NOTE_ONSET_MIN % WINDOW_MIN == 0
n_win = int(math.ceil(SESSION_MIN / WINDOW_MIN))
win_edges = [w * WINDOW_MIN for w in range(n_win + 1)]
win_labels = [f"{lo:.0f}–{hi:.0f}" for lo, hi in zip(win_edges[:-1], win_edges[1:])]
n_pre = int(NOTE_ONSET_MIN // WINDOW_MIN)


def window_means(rows):
    means, ns = [], []
    for lo, hi in zip(win_edges[:-1], win_edges[1:]):
        v = [r["tox"] for r in rows if lo <= r["min"] < hi]
        means.append(np.mean(v) if v else np.nan)
        ns.append(len(v))
    return np.array(means), ns


win = {c: {day: window_means([r for r in msgs if r["cond"] == c and r["day"] == day])
           for day in (1, 2)} for c in ARMS}
win_sess = {c: {s: window_means([r for r in d1 if r["cond"] == c and r["session"] == s])[0]
                for s in SESSIONS} for c in ARMS}
S["nWindows"], S["nPreWindows"] = n_win, n_pre
for c in ARMS:
    k = c.lower()
    m, ns = win[c][1]
    for letter, v in zip("ABCDEFGHIJKL", m):
        S[f"{k}Win{letter}"] = fmt(v)
    S[f"{k}WinNs"] = ", ".join(str(n) for n in ns)
    S[f"{k}WinFirst"] = fmt(m[0])
    S[f"{k}WinPreMax"] = fmt(m[:n_pre].max())
    S[f"{k}WinPreMaxLabel"] = win_labels[int(np.argmax(m[:n_pre]))]
    S[f"{k}WinFirstPost"] = fmt(m[n_pre])
    S[f"{k}WinPostMin"] = fmt(m[n_pre:].min())
    S[f"{k}WinPostMinLabel"] = win_labels[n_pre + int(np.argmin(m[n_pre:]))]
    S[f"{k}WinPostMax"] = fmt(m[n_pre:].max())
    S[f"{k}WinLast"] = fmt(m[-1])
    # pre-note trend, message level
    rows = rows_of(c, "pre")
    lr = st.linregress([r["min"] for r in rows], [r["tox"] for r in rows])
    S[f"{k}PreSlope"], S[f"{k}PreSlopeP"] = fmt(lr.slope, 2), pfmt(lr.pvalue)
    rows = rows_of(c, "post")
    lr = st.linregress([r["min"] for r in rows], [r["tox"] for r in rows])
    S[f"{k}PostSlope"], S[f"{k}PostSlopeP"] = fmt(lr.slope, 2), pfmt(lr.pvalue)
    # Day 2 windows
    m2, _ = win[c][2]
    S[f"{k}DayTwoWinFirst"], S[f"{k}DayTwoWinMax"], S[f"{k}DayTwoWinMin"] = fmt(m2[0]), fmt(m2.max()), fmt(m2.min())
S["lastWinGap"] = fmt(win["CTRL"][1][0][-1] - win["EXPT"][1][0][-1])
S["dropAtNote"] = f"{100 * (1 - win['EXPT'][1][0][n_pre] / win['EXPT'][1][0][:n_pre].max()):.0f}"

# peak window before the note vs quietest window after it, EXPT (descriptive)
_m = win["EXPT"][1][0]
peak_i = int(np.argmax(_m[:n_pre]))
trough_i = n_pre + int(np.argmin(_m[n_pre:]))
peak_msgs = [r["tox"] for r in rows_of("EXPT", "pre") if win_edges[peak_i] <= r["min"] < win_edges[peak_i + 1]]
trough_msgs = [r["tox"] for r in rows_of("EXPT", "post") if win_edges[trough_i] <= r["min"] < win_edges[trough_i + 1]]
_pt = st.ttest_ind(peak_msgs, trough_msgs, equal_var=False)
S["peakWin"], S["troughWin"] = win_labels[peak_i], win_labels[trough_i]
S["peakWinM"], S["troughWinM"] = fmt(np.mean(peak_msgs)), fmt(np.mean(trough_msgs))
S["peakWinN"], S["troughWinN"] = len(peak_msgs), len(trough_msgs)
S["peakTroughT"], S["peakTroughDf"], S["peakTroughP"] = fmt(_pt.statistic, 2), fmt(_pt.df), pfmt(_pt.pvalue)
S["peakTroughDrop"] = f"{100 * (1 - np.mean(trough_msgs) / np.mean(peak_msgs)):.0f}"
# the same window in the control arm
_cm = win["CTRL"][1][0]
S["ctrlAtPeakWin"], S["ctrlAtTroughWin"] = fmt(_cm[peak_i]), fmt(_cm[trough_i])

# ----------------------------------------------------------------- Day 2 ----
for c in ARMS:
    k = c.lower()
    for ph, tag in (("pre", "Pre"), ("post", "Post")):
        tt = st.ttest_rel(sess[c]["day2"], sess[c][ph])
        S[f"{k}{tag}DayTwoT"], S[f"{k}{tag}DayTwoP"] = fmt(tt.statistic, 2), pfmt(tt.pvalue)
        w = st.ttest_ind(A[c]["day2"], A[c][ph], equal_var=False)
        S[f"{k}{tag}DayTwoMsgT"], S[f"{k}{tag}DayTwoMsgDf"], S[f"{k}{tag}DayTwoMsgP"] = fmt(w.statistic, 2), fmt(w.df), pfmt(w.pvalue)
    S[f"{k}DayTwoSessMin"], S[f"{k}DayTwoSessMax"] = fmt(sess[c]["day2"].min()), fmt(sess[c]["day2"].max())
    ps = [p for p in per.values() if p["cond"] == c and p["day2"]]
    S[f"{k}DayTwoActive"] = len(ps)
S["dayTwoSessBelow"] = int((sess["EXPT"]["day2"] < sess["CTRL"]["day2"]).sum())
S["dayTwoGapMin"] = fmt((sess["CTRL"]["day2"] - sess["EXPT"]["day2"]).min())
S["dayTwoGapMax"] = fmt((sess["CTRL"]["day2"] - sess["EXPT"]["day2"]).max())

# ------------------------------------------------ robustness (Table 2) ------
msg_count = {k: len(p["pre"]) + len(p["post"]) for k, p in per.items()}


def did_for(keep):
    """Session-level DiD restricted to the participants in `keep`."""
    out = {}
    for c in ARMS:
        pre_s, post_s = [], []
        for s in SESSIONS:
            pre_s.append(np.mean([r["tox"] for r in rows_of(c, "pre", s) if (c, r["handle"]) in keep]))
            post_s.append(np.mean([r["tox"] for r in rows_of(c, "post", s) if (c, r["handle"]) in keep]))
        out[c] = (np.array(pre_s), np.array(post_s))
    dd = (out["CTRL"][1] - out["CTRL"][0]) - (out["EXPT"][1] - out["EXPT"][0])
    tt = st.ttest_1samp(dd, 0.0)
    return out, dd, tt


ROBUST = [("All", lambda k: True),
          ("Six", lambda k: msg_count[k] >= 6),
          ("Ten", lambda k: msg_count[k] >= 10),
          ("Peri", lambda k: not per[k]["heavy"])]
for tag, rule in ROBUST:
    keep = {k for k in per if rule(k)}
    out, dd, tt = did_for(keep)
    S[f"rob{tag}Part"] = len(keep)
    S[f"rob{tag}ExptPre"], S[f"rob{tag}ExptPost"] = fmt(out["EXPT"][0].mean()), fmt(out["EXPT"][1].mean())
    S[f"rob{tag}CtrlPre"], S[f"rob{tag}CtrlPost"] = fmt(out["CTRL"][0].mean()), fmt(out["CTRL"][1].mean())
    S[f"rob{tag}Did"] = fmt(dd.mean())
    S[f"rob{tag}DidT"], S[f"rob{tag}DidP"] = fmt(tt.statistic, 2), pfmt(tt.pvalue)

# --------------------------------------------------- session for the teaser --
# the session whose DiD is the median: representative, not the best case
show_session = SESSIONS[int(np.argsort(did)[len(did) // 2])]
S["showSession"] = show_session
S["showSessionDid"] = fmt(did[SESSIONS.index(show_session)])
for c in ARMS:
    k = c.lower()
    S[f"show{k.capitalize()}Pre"] = fmt(sess[c]["pre"][SESSIONS.index(show_session)])
    S[f"show{k.capitalize()}Post"] = fmt(sess[c]["post"][SESSIONS.index(show_session)])
    S[f"show{k.capitalize()}N"] = len([r for r in d1 if r["cond"] == c and r["session"] == show_session])


def codes_for(session, cond):
    """Anonymized A1-A3 / B1-B3 codes for one session-arm, sorted by handle."""
    hs = sorted({r["handle"] for r in msgs if r["session"] == session and r["cond"] == cond})
    out, na, nb = {}, 0, 0
    for h in hs:
        if h.startswith("army"):
            na += 1
            out[h] = f"A{na}"
        else:
            nb += 1
            out[h] = f"B{nb}"
    return out


# ---------------------------------------------------------------- surveys ---
# The exported battery comes from the pilot cohorts, not from S1-S5.
sv = [r for r in surveys if r["arm"] == "EXPT"]
S["surveyN"] = len(sv)
S["surveyCohorts"] = " and ".join(sorted({r["cohort"] for r in sv}))
S["surveyNCohorts"] = len({r["cohort"] for r in sv})


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
S["thermKpop"] = f"{np.mean([float(r['s1_therm_kpop']) for r in sv]):.1f}"
for _k, _name in (("s1_simil_general", "similGeneral"), ("s1_simil_interests", "similInterests"),
                  ("s1_simil_values", "similValues"), ("s1_simil_care", "similCare")):
    S[_name] = f"{np.mean([float(r[_k]) for r in sv]):.2f}"

survey_items = [k for k in surveys[0] if k.startswith("s1_") and not k.startswith("s1_therm")]


def straightlined(r):
    v = [float(r[k]) for k in survey_items if r[k]]
    return np.std(v) < 0.5


def failed_heat_check(r):  # the session was designed to be heated
    return float(r["s1_sess_heated"]) <= 2


S["nStraightlinedExpt"] = sum(1 for r in sv if straightlined(r))
S["nFailedHeat"] = sum(1 for r in sv if failed_heat_check(r))
S["minHeat"] = f"{min(float(r['s1_sess_heated']) for r in sv):.0f}"

contact_items = ["s1_contact_friends", "s1_contact_discuss", "s1_contact_work", "s1_contact_share"]
contact_means = {k: np.mean([float(r[k]) for r in sv if r[k]]) for k in contact_items}
S["contactFriends"] = f"{contact_means['s1_contact_friends']:.2f}"
S["contactMax"] = f"{max(contact_means.values()):.2f}"
_one = st.ttest_1samp(scale(sv, "s1_contact"), 3.0)
S["contactVsMidT"], S["contactVsMidP"] = f"{_one.statistic:.2f}", f"{_one.pvalue:.2f}"

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


def stars(p):
    return "***" if p < .001 else "**" if p < .01 else "*" if p < .05 else "n.s."


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


if __name__ == "__main__":
    import json
    print(json.dumps(S, indent=1))

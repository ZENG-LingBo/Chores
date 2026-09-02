#!/usr/bin/env python3
"""Figure 6: Day 1 phases versus Day 2 without the feature, by arm, with significance.

Bars are means of the five session means; dots are the sessions, connected
across the three periods. Within each arm, Day 2 does not differ from the
Day-1 post-feature phase (paired t over sessions); across arms, Day 2 differs
in every session pair.

Run: python3 fig_days.py  ->  fig_days.png (here) + paper/figures/fig_days.pdf
"""
import numpy as np

from defuselab import (ARMS, ARM_COLOR, ARM_LIGHT, ARM_NAME, INK, INK2, SESSIONS, SURFACE,
                       clean_axes, plt, save, sess, stars)
from scipy import stats as st

PH = (("pre", "Day 1\nbefore"), ("post", "Day 1\nafter"), ("day2", "Day 2\nno feature"))
XPOS = {"EXPT": np.array([0.0, 1.0, 2.0]), "CTRL": np.array([3.4, 4.4, 5.4])}


def bracket(ax, i, j, y, label, bold=False):
    ax.plot([i, i, j, j], [y - 1.8, y, y, y - 1.8], color=INK2, lw=0.8)
    ax.text((i + j) / 2, y + 0.8, label, ha="center", va="bottom", fontsize=6.6,
            color=INK if bold else INK2, fontweight="bold" if bold else "normal")


def main():
    fig, ax = plt.subplots(figsize=(4.6, 2.7), constrained_layout=True)
    for c in ARMS:
        xs = XPOS[c]
        vals = [sess[c][ph] for ph, _ in PH]
        cols = [ARM_LIGHT[c], ARM_COLOR[c], ARM_COLOR[c]]
        for x, v, col in zip(xs, vals, cols):
            ax.bar(x, v.mean(), width=0.62, color=col, edgecolor=SURFACE, linewidth=1.5, zorder=1)
            ax.text(x, 2.5, f"{v.mean():.1f}", ha="center", va="bottom", fontsize=7,
                    fontweight="bold", color=INK if col == ARM_LIGHT[c] else SURFACE, zorder=5)
        for k, s in enumerate(SESSIONS):  # one line per session, no jitter: n = 5 fits
            ys = [v[k] for v in vals]
            ax.plot(xs, ys, color=INK2, lw=0.5, alpha=0.5, zorder=3)
            ax.scatter(xs, ys, s=12, color=INK, zorder=4, edgecolor=SURFACE, linewidth=0.6)
        ax.text(xs.mean(), -19, ARM_NAME[c] + " arm", ha="center", va="top", fontsize=7.5,
                fontweight="bold", color=ARM_COLOR[c])
        # within-arm persistence test: Day 1 after vs Day 2
        p = st.ttest_rel(sess[c]["day2"], sess[c]["post"]).pvalue
        bracket(ax, xs[1], xs[2], 90, f"{stars(p)}  p = {p:.2f}")
    # across arms on Day 2, session-paired
    p2 = st.ttest_rel(sess["EXPT"]["day2"], sess["CTRL"]["day2"]).pvalue
    bracket(ax, XPOS["EXPT"][2], XPOS["CTRL"][2], 100, f"{stars(p2)}  p = {p2:.4f}", bold=True)

    ax.set_xticks(np.concatenate([XPOS["EXPT"], XPOS["CTRL"]]))
    ax.set_xticklabels([lab for _, lab in PH] * 2, fontsize=6.6)
    ax.set_xlim(-0.6, 6.0)
    ax.set_ylim(0, 118)
    ax.set_ylabel("Mean toxicity per session (0–100)", fontsize=7.5)
    clean_axes(ax)
    ax.text(0.01, 0.985, "bars: mean of five sessions; dots: sessions; paired t over sessions",
            fontsize=6.0, color=INK2, va="top", transform=ax.transAxes)

    save(fig, "fig_days")


if __name__ == "__main__":
    main()

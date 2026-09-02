#!/usr/bin/env python3
"""Figure 5: mean toxicity in five-minute windows, both arms, both days.

Left (Day 1): the two arms climb together for 35 minutes; when the feature
appears the control arm keeps climbing and the note arm drops. Right (Day 2,
no feature): the note arm starts and stays near its Day-1 baseline; the
control arm starts where it left off. Bold lines pool the five sessions;
faint lines are the individual sessions.

Run: python3 fig_windows.py  ->  fig_windows.png (here) + paper/figures/fig_windows.pdf
"""
import numpy as np

from defuselab import (ARMS, ARM_COLOR, ARM_NAME, INK, INK2, NOTE_ONSET_MIN, SESSIONS, S,
                       clean_axes, msgs, n_pre, plt, save, win, win_edges, window_means)

XC = (np.array(win_edges[:-1]) + np.array(win_edges[1:])) / 2  # window centres


def draw(ax, day):
    for c in ARMS:
        for s in SESSIONS:
            m, _ = window_means([r for r in msgs if r["cond"] == c and r["session"] == s
                                 and r["day"] == day])
            ax.plot(XC, m, color=ARM_COLOR[c], lw=0.7, alpha=0.22, zorder=2)
        m, _ = win[c][day]
        ax.plot(XC, m, color=ARM_COLOR[c], lw=2.0, marker="o", markersize=3.4,
                markerfacecolor=ARM_COLOR[c], markeredgecolor="white", markeredgewidth=0.8,
                zorder=4)
        ax.text(XC[-1] + 1.2, m[-1], ARM_NAME[c], color=ARM_COLOR[c], fontsize=7,
                fontweight="bold", va="center", ha="left")
    ax.set_xlim(0, 71)
    ax.set_xticks(win_edges[::2] if day == 2 else [0, 10, 20, 30, 35, 40, 50, 60])
    ax.set_ylim(15, 96)
    ax.set_xlabel("Minutes into the session", fontsize=7.5)
    clean_axes(ax)


def main():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.0, 2.5), sharey=True,
                                   gridspec_kw={"width_ratios": [1.15, 1]},
                                   constrained_layout=True)

    # ---- Day 1: feature at 35 minutes ---------------------------------------
    draw(ax1, 1)
    ax1.axvline(NOTE_ONSET_MIN, color=INK, lw=0.9, ls=(0, (4, 2)), zorder=3)
    ax1.axvspan(NOTE_ONSET_MIN, 60, color="#f3f2ee", zorder=0)
    ax1.text(NOTE_ONSET_MIN + 0.8, 17, "feature appears", ha="left", va="bottom",
             fontsize=6.8, fontweight="bold", color=INK)
    m_e, m_c = win["EXPT"][1][0], win["CTRL"][1][0]
    ax1.text(XC[n_pre + 1] + 2.2, m_e[n_pre + 1] - 1.5, f"{m_e[n_pre - 1]:.0f} → {m_e[n_pre + 1]:.0f}",
             fontsize=6.8, color=ARM_COLOR["EXPT"], fontweight="bold", ha="left", va="center")
    ax1.set_title("Day 1: both arms climb, then diverge at the feature", fontsize=7.8)
    ax1.set_ylabel("Mean toxicity per 5-min window", fontsize=7.5)
    ax1.text(0.02, 0.97, "bold: five sessions pooled; faint: each session",
             transform=ax1.transAxes, fontsize=6.2, color=INK2, va="top")

    # ---- Day 2: no feature ---------------------------------------------------
    draw(ax2, 2)
    ax2.set_title("Day 2: no feature in either arm", fontsize=7.8)
    m2e, m2c = win["EXPT"][2][0], win["CTRL"][2][0]
    ax2.text(0.02, 0.97, f"note arm never climbs (max {m2e.max():.0f});\n"
             f"control starts hot ({m2c[0]:.0f} in the first window)",
             transform=ax2.transAxes, fontsize=6.2, color=INK2, va="top")

    save(fig, "fig_windows")


if __name__ == "__main__":
    main()

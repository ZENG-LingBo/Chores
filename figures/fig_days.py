#!/usr/bin/env python3
"""Figure 5: Day 1 phases versus Day 2, at the participant level.

Day 2 (no feature) sits between the two Day 1 phases and differs significantly
from neither: the reduction did not carry over once the note was gone.

Run: python3 fig_days.py  ->  fig_days.png (here) + paper/figures/fig_days.pdf
"""
import numpy as np

from defuselab import (BLUE, ORANGE, LIGHT_BLUE, INK, INK2, SURFACE, clean_axes,
                       free_p, note_p, p_fd2, p_nd2, plt, save, t_fd2, t_nd2,
                       test1_d2)


def main():
    fig, ax = plt.subplots(figsize=(3.35, 2.3), constrained_layout=True)
    groups = [("Day 1\nfree phase", free_p, BLUE),
              ("Day 1\nnote phase", note_p, ORANGE),
              ("Day 2\nno feature", test1_d2, LIGHT_BLUE)]
    rng = np.random.default_rng(7)  # fixed seed: identical jitter on every rebuild

    for i, (_label, vals, col) in enumerate(groups):
        ax.bar(i, vals.mean(), width=0.6, color=col, edgecolor=SURFACE, linewidth=1.5)
        ax.text(i - 0.36, vals.mean(), f"{vals.mean():.3f}", ha="right", va="center",
                fontsize=7, color=INK)
        ax.scatter(i + rng.uniform(-0.11, 0.11, len(vals)), vals, s=14, color=INK,
                   zorder=3, edgecolor=SURFACE, linewidth=0.7)

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


if __name__ == "__main__":
    main()

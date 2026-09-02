#!/usr/bin/env python3
"""Figure 5: Day 1 phases versus Day 2, at the participant level, with significance.

The free-to-note drop on Day 1 is significant; Day 2 (no feature) sits between
the two Day 1 phases and differs significantly from neither, so the reduction
did not carry over once the note was gone.

Run: python3 fig_days.py  ->  fig_days.png (here) + paper/figures/fig_days.pdf
"""
import numpy as np

from defuselab import (BLUE, ORANGE, LIGHT_BLUE, INK, INK2, SURFACE, clean_axes,
                       free_p, note_p, p_fd2, p_nd2, p_pair, plt, save, test1_d2)


def bracket(ax, i, j, y, label, bold=False):
    """Significance bracket between bars i and j at height y."""
    ax.plot([i, i, j, j], [y - 0.012, y, y, y - 0.012], color=INK2, lw=0.8)
    ax.text((i + j) / 2, y + 0.006, label, ha="center", va="bottom", fontsize=6.8,
            color=INK if bold else INK2, fontweight="bold" if bold else "normal")


def stars(p):
    return "***" if p < .001 else "**" if p < .01 else "*" if p < .05 else "n.s."


def main():
    fig, ax = plt.subplots(figsize=(3.35, 2.5), constrained_layout=True)
    groups = [("Day 1\nfree phase", free_p, BLUE),
              ("Day 1\nnote phase", note_p, ORANGE),
              ("Day 2\nno feature", test1_d2, LIGHT_BLUE)]
    rng = np.random.default_rng(7)  # fixed seed: identical jitter on every rebuild

    for i, (_label, vals, col) in enumerate(groups):
        ax.bar(i, vals.mean(), width=0.6, color=col, edgecolor=SURFACE, linewidth=1.5)
        ax.text(i, 0.015, f"{vals.mean():.3f}", ha="center", va="bottom",
                fontsize=7, fontweight="bold", color=SURFACE, zorder=5)
        ax.scatter(i + rng.uniform(-0.11, 0.11, len(vals)), vals, s=14, color=INK,
                   zorder=3, edgecolor=SURFACE, linewidth=0.7)

    # significance: the Day-1 drop, and Day 2 against each Day-1 phase
    bracket(ax, 0, 1, 0.56, f"{stars(p_pair)}  p = {p_pair:.3f}", bold=True)
    bracket(ax, 1, 2, 0.45, f"{stars(p_nd2)}  p = {p_nd2:.2f}")
    bracket(ax, 0, 2, 0.65, f"{stars(p_fd2)}  p = {p_fd2:.2f}")

    ax.set_xticks(range(3))
    ax.set_xticklabels([f"{g[0]}\n(n={len(g[1])})" for g in groups], fontsize=7)
    ax.set_ylabel("Mean toxicity per participant", fontsize=7.5)
    ax.set_xlim(-0.6, 2.6)
    ax.set_ylim(0, 0.74)
    clean_axes(ax)
    ax.text(0.01, 0.985, "paired t (Day 1); Welch t vs. Day 2", fontsize=6.2,
            color=INK2, va="top", transform=ax.transAxes)

    save(fig, "fig_days")


if __name__ == "__main__":
    main()

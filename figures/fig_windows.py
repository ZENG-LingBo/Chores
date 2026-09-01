#!/usr/bin/env python3
"""Figure 2: mean toxicity in ten-minute windows, with the note onset marked.

Every window after the note is lower than every window before it.

Run: python3 fig_windows.py  ->  fig_windows.png (here) + paper/figures/fig_windows.pdf
"""
import numpy as np

from defuselab import (BLUE, ORANGE, INK, SURFACE, bar_labels, clean_axes,
                       plt, save, win_means)


def main():
    fig, ax = plt.subplots(figsize=(3.35, 2.1), constrained_layout=True)
    xs = np.arange(5)
    cols = [BLUE if x < 2 else ORANGE for x in xs]  # 2 windows precede the note
    bars = ax.bar(xs, win_means, width=0.68, color=cols,
                  edgecolor=SURFACE, linewidth=1.5)
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

    keys = [plt.Rectangle((0, 0), 1, 1, fc=BLUE), plt.Rectangle((0, 0), 1, 1, fc=ORANGE)]
    ax.legend(keys, ["Free phase", "Note phase"], frameon=False, fontsize=7,
              loc="upper right", handlelength=1.1, handleheight=1.0, borderaxespad=0.1)

    save(fig, "fig_windows")


if __name__ == "__main__":
    main()

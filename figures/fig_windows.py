#!/usr/bin/env python3
"""Figure 2: mean toxicity per five-minute window across the session.

Windows are aligned to the note onset (15 minutes in), so the free/note
boundary falls on a window edge. At this resolution the shape of the effect is
visible: toxicity peaks in the window immediately before the note, halves in
the window immediately after, and no later window climbs back even to the
quietest pre-note window.

Run: python3 fig_windows.py  ->  fig_windows.png (here) + paper/figures/fig_windows.pdf
"""
import numpy as np

from defuselab import (BLUE, ORANGE, INK, INK2, SURFACE, S, clean_axes, n_pre,
                       plt, save, win_labels, win_means, win_ns)


def main():
    fig, ax = plt.subplots(figsize=(5.0, 2.3), constrained_layout=True)
    xs = np.arange(len(win_means))
    cols = [BLUE if x < n_pre else ORANGE for x in xs]
    ax.bar(xs, win_means, width=0.72, color=cols, edgecolor=SURFACE, linewidth=1.2)

    # trend overlay across the same means
    ax.plot(xs, win_means, color=INK2, lw=1.0, zorder=4, marker="o", markersize=3.0,
            markerfacecolor=SURFACE, markeredgecolor=INK2, markeredgewidth=0.9)

    # selective direct labels: the story points, not every bar
    peak_i = int(np.argmax(win_means[:n_pre]))
    low_i = int(np.argmin(win_means))
    for i in (peak_i, n_pre, low_i):
        ax.text(i, win_means[i] + 0.018, f"{win_means[i]:.3f}", ha="center",
                va="bottom", fontsize=7, color=INK, fontweight="bold")

    ax.axvline(n_pre - 0.5, color=INK, lw=0.9, ls=(0, (4, 2)))
    ax.text(n_pre - 0.42, 0.455, "Community Note appears", ha="left", va="top",
            fontsize=6.8, color=INK, fontweight="bold")

    # the halving at the boundary: the two labelled values either side of the
    # dashed line carry it, so no arrow is needed to cross the gap
    ax.text(n_pre - 0.40, 0.355, f"−{S['dropAtNote']}%\nin one window",
            ha="left", va="top", fontsize=7.5, fontweight="bold", color=ORANGE,
            linespacing=1.25)

    ax.set_xticks(xs)
    ax.set_xticklabels(win_labels, fontsize=6.5)
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

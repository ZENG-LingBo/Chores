#!/usr/bin/env python3
"""Figure 2: mean toxicity per session window, with the note onset marked.

Windows are aligned to the note onset (15 minutes in), so the boundary between
the free and note phases falls exactly on a window edge rather than inside a
bar. Toxicity falls window by window; a trend overlay traces the decline.

Run: python3 fig_windows.py  ->  fig_windows.png (here) + paper/figures/fig_windows.pdf
"""
import numpy as np

from defuselab import (BLUE, ORANGE, INK, INK2, SURFACE, bar_labels, clean_axes,
                       n_pre, plt, save, win_labels, win_means, win_ns)


def main():
    fig, ax = plt.subplots(figsize=(3.35, 2.1), constrained_layout=True)
    xs = np.arange(len(win_means))
    cols = [BLUE if x < n_pre else ORANGE for x in xs]
    bars = ax.bar(xs, win_means, width=0.62, color=cols,
                  edgecolor=SURFACE, linewidth=1.5)
    bar_labels(ax, bars)

    # trend overlay: the same means, so the window-by-window decline reads as one slope
    ax.plot(xs, win_means, color=INK2, lw=1.0, zorder=4,
            marker="o", markersize=3.2, markerfacecolor=SURFACE,
            markeredgecolor=INK2, markeredgewidth=0.9)

    # event line, labelled along itself so the label cannot collide with the legend
    ax.axvline(n_pre - 0.5, color=INK, lw=0.9, ls=(0, (4, 2)))
    ax.text(n_pre - 0.46, 0.015, "Community Note appears", rotation=90,
            ha="left", va="bottom", fontsize=6.4, color=INK, fontweight="bold")

    ax.set_xticks(xs)
    ax.set_xticklabels([f"{lab}\n(n={n})" for lab, n in zip(win_labels, win_ns)],
                       fontsize=7)
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

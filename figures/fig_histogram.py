#!/usr/bin/env python3
"""Figure 4: the toxicity distribution before and after the note.

The bulk shifts left after the note while the most toxic participant's messages
(hatched) keep occupying the right tail: the group softened, its most toxic
member did not.

Run: python3 fig_histogram.py -> fig_histogram.png + paper/figures/fig_histogram.pdf
"""
import numpy as np

from defuselab import (BLUE, ORANGE, INK, SURFACE, clean_axes, code, free,
                       most_toxic, note, plt, save)

BINS = np.arange(0, 1.1, 0.1)


def main():
    fig, axes = plt.subplots(1, 2, figsize=(6.9, 2.15), sharey=True,
                             constrained_layout=True)

    for ax, phase, rows in ((axes[0], "Free phase", free),
                            (axes[1], "Note phase", note)):
        hot = [r["tox"] for r in rows if r["handle"] == most_toxic]
        rest = [r["tox"] for r in rows if r["handle"] != most_toxic]
        ax.hist([rest, hot], bins=BINS, stacked=True, color=[BLUE, ORANGE],
                edgecolor=SURFACE, linewidth=1.2, rwidth=1.0)

        # texture on the highlighted participant's segment (identity never color-alone)
        n_rest, _ = np.histogram(rest, bins=BINS)
        n_hot, _ = np.histogram(hot, bins=BINS)
        for x0, nr, nh in zip(BINS[:-1], n_rest, n_hot):
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
    keys = [plt.Rectangle((0, 0), 1, 1, fc=BLUE),
            plt.Rectangle((0, 0), 1, 1, fc=ORANGE, hatch="///", ec=SURFACE)]
    axes[1].legend(keys, ["All other participants",
                          f"Most toxic participant ({code[most_toxic]})"],
                   frameon=False, fontsize=7, loc="center right", handlelength=1.1)

    save(fig, "fig_histogram")


if __name__ == "__main__":
    main()

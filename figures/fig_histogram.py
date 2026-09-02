#!/usr/bin/env python3
"""Figure 4: the toxicity distribution before and after the feature, by arm.

Before the feature the two arms are indistinguishable. Afterwards the control
arm's distribution moves as a block to the right, while the note arm's
spreads: its bulk moves left and a smaller mass, the heavy posters, moves
right. The note did not lower everyone; it split the room.

Run: python3 fig_histogram.py -> fig_histogram.png + paper/figures/fig_histogram.pdf
"""
import numpy as np

from defuselab import ARMS, ARM_COLOR, ARM_NAME, INK, SURFACE, A, S, clean_axes, plt, save

EDGES = np.arange(0, 101, 10)  # scores are multiples of 5, so 100 lands in the last bin
W = 4.2  # bar width in score units (two bars per 10-point bin)


def main():
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.3), sharey=True, constrained_layout=True)
    titles = {"pre": f"Before the feature (0–{S['noteOnsetMin']} min)",
              "post": f"After the feature ({S['noteOnsetMin']}–{S['sessionMinutes']} min)"}
    for ax, ph in zip(axes, ("pre", "post")):
        for j, c in enumerate(ARMS):
            v = A[c][ph]
            counts, _ = np.histogram(v, bins=EDGES)
            pct = 100 * counts / len(v)
            x = EDGES[:-1] + 5 + (j - 0.5) * W
            ax.bar(x, pct, width=W, color=ARM_COLOR[c], edgecolor=SURFACE, linewidth=0.8,
                   label=f"{ARM_NAME[c]} arm (n = {len(v)})")
            m = v.mean()
            ax.axvline(m, color=ARM_COLOR[c], lw=1.0, ls=(0, (4, 2)))
            ax.text(m + 1.2, 27 - 3.2 * j, f"mean {m:.1f}", fontsize=6.6, color=ARM_COLOR[c],
                    ha="left", va="center")
        ax.set_title(titles[ph], fontsize=7.8)
        ax.set_xlabel("Message toxicity (0–100)", fontsize=7.5)
        ax.set_xlim(0, 100)
        ax.set_xticks(EDGES)
        ax.tick_params(axis="x", labelsize=6.8)
        clean_axes(ax)
    axes[0].set_ylabel("Share of the arm's messages (%)", fontsize=7.5)
    axes[0].set_ylim(0, 36)
    axes[0].legend(frameon=False, fontsize=6.8, loc="upper left", handlelength=1.1)
    axes[1].text(0.02, 0.97, f"scores ≥ 60: note arm {S['exptPostHighPct']}%, "
                 f"control {S['ctrlPostHighPct']}%",
                 transform=axes[1].transAxes, fontsize=6.6, color=INK, va="top")

    save(fig, "fig_histogram")


if __name__ == "__main__":
    main()

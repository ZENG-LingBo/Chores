#!/usr/bin/env python3
"""Figure 3: per-participant toxicity, free phase to note phase (paired slopes).

Four of the five participants who posted in both phases became less toxic; the
most toxic one stayed the most toxic voice in the room.

Run: python3 fig_participants.py -> fig_participants.png + paper/figures/fig_participants.pdf
"""
from defuselab import (BLUE, ORANGE, INK2, SURFACE, S, clean_axes, code,
                       most_toxic, p_pair, paired, plt, save, t_pair)


def main():
    fig, ax = plt.subplots(figsize=(3.35, 2.5), constrained_layout=True)

    # dodge right-hand labels so close endpoints stay readable
    label_y, prev = {}, -1.0
    for end, h in sorted((paired[h][1], h) for h in paired):
        label_y[h] = prev = max(end, prev + 0.033)

    for h in sorted(paired, key=lambda h: paired[h][0]):
        a, b = paired[h]
        hot = h == most_toxic
        ax.plot([0, 1], [a, b], color=ORANGE if hot else BLUE,
                lw=2.0 if hot else 1.4, alpha=1.0 if hot else 0.75,
                zorder=3 if hot else 2, marker="o", markersize=5,
                markeredgecolor=SURFACE, markeredgewidth=1.0)
        ax.annotate(code[h] + (" (most toxic)" if hot else ""),
                    xy=(1, b), xytext=(1.045, label_y[h]), fontsize=7,
                    color=ORANGE if hot else INK2, va="center")

    ax.set_xlim(-0.14, 1.62)
    ax.set_xticks([0, 1])
    ax.set_xticklabels(["Free phase", "Note phase"], fontsize=7.5)
    ax.set_ylabel("Mean toxicity per participant", fontsize=7.5)
    ax.set_ylim(0, 0.55)
    clean_axes(ax)

    ax.text(0.98, 0.055,
            f"paired t({len(paired)-1}) = {t_pair:.2f}, p = {p_pair:.3f}, "
            f"$d_z$ = {S['pairedDz']}\n"
            f"{S['nDeclined']} of {len(paired)} participants declined",
            fontsize=6.8, color=INK2, va="bottom", ha="right",
            transform=ax.transAxes)

    save(fig, "fig_participants")


if __name__ == "__main__":
    main()

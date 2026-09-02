#!/usr/bin/env python3
"""Figure 1 (teaser): the Community Notes mechanism, and the headline drop.

Run: python3 fig_teaser.py   ->  fig_teaser.png (here) + paper/figures/fig_teaser.pdf
"""
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

from defuselab import (VIOLET, MAGENTA, INK, INK2, GRID, SURFACE, FancyArrowPatch,
                       FancyBboxPatch, S, code, handles, msgs, plt, save)

# sequential blue ramp from the validated palette (light = calm, dark = toxic)
TOX_RAMP = LinearSegmentedColormap.from_list(
    "tox", ["#cde2fb", "#86b6ef", "#3987e5", "#1c5cab", "#0d366b"])

BOXW = 0.44


def rounded(ax, x, y, w, h, fc, ec, lw=0.8, r=0.015):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle=f"round,pad=0,rounding_size={r}",
                                fc=fc, ec=ec, lw=lw, mutation_aspect=1))


def badge(ax, x, y, fandom):
    col = VIOLET if fandom == "ARMY" else MAGENTA
    rounded(ax, x, y, 0.085, 0.055, col, col, r=0.01)
    ax.text(x + 0.0425, y + 0.0275, fandom, ha="center", va="center",
            fontsize=5.2, color="white", fontweight="bold")


def msg_lines(ax, x, y, w, n=2, color=GRID):
    for i in range(n):
        ax.plot([x, x + w * (0.95 if i < n - 1 else 0.6)], [y - 0.03 * i] * 2,
                color=color, lw=2.2, solid_capstyle="round")


def stage(ax, x0, title, edge=INK2):
    rounded(ax, x0, 0.06, BOXW, 0.92, "#fcfcfb", edge)
    ax.text(x0 + BOXW / 2, 0.865, title, ha="center", va="center",
            fontsize=6.4, fontweight="bold")


def caption(ax, x0, text):
    ax.text(x0 + BOXW / 2, 0.175, text, ha="center", va="center", fontsize=5.9,
            color=INK2, style="italic")


def main():
    fig = plt.figure(figsize=(7.0, 2.55))
    gs = fig.add_gridspec(1, 2, width_ratios=[2.05, 1], wspace=0.22,
                          left=0.005, right=0.965, top=0.87, bottom=0.15)

    # ---- Panel A: the mechanism, in three stages -------------------------
    ax = fig.add_subplot(gs[0])
    ax.set_xlim(0, 1.60)
    ax.set_ylim(0, 1)
    ax.axis("off")

    stage(ax, 0.02, "Mixed feed\nescalates")
    for i, fan in enumerate(["ARMY", "BLINK", "ARMY"]):
        yy = 0.66 - i * 0.16
        badge(ax, 0.055, yy, fan)
        msg_lines(ax, 0.16, yy + 0.045, 0.25, 2, "#c9c8c2")
    caption(ax, 0.02, "toxicity climbs\npast a threshold")

    ax.add_patch(FancyArrowPatch((0.475, 0.52), (0.565, 0.52), arrowstyle="-|>",
                                 mutation_scale=11, color=INK2, lw=1.1))

    stage(ax, 0.58, "Community Note\n(pinned)", INK)
    badge(ax, 0.615, 0.63, "ARMY")
    msg_lines(ax, 0.72, 0.675, 0.26, 2, "#c9c8c2")
    badge(ax, 0.615, 0.44, "BLINK")
    msg_lines(ax, 0.72, 0.485, 0.26, 2, "#c9c8c2")
    ax.text(0.80, 0.315, "one slot per fandom,\nverbatim under each badge",
            ha="center", fontsize=5.7, color=INK2)
    caption(ax, 0.58, "publishes only when\nboth sides write")

    ax.add_patch(FancyArrowPatch((1.035, 0.52), (1.125, 0.52), arrowstyle="-|>",
                                 mutation_scale=11, color=INK2, lw=1.1))

    stage(ax, 1.14, "Co-signed note\npublished")
    badge(ax, 1.19, 0.62, "ARMY")
    badge(ax, 1.30, 0.62, "BLINK")
    msg_lines(ax, 1.19, 0.52, 0.34, 3, "#c9c8c2")
    caption(ax, 1.14, "assembled backstage\nby the LLM")
    ax.text(0.0, 1.08, "A", fontsize=9, fontweight="bold", va="top")

    # ---- Panel B: the session itself, one mark per message -----------------
    axb = fig.add_subplot(gs[1])
    rows = {h: i for i, h in enumerate(sorted(handles, key=lambda h: code[h]))}
    onset = float(S["noteOnsetMin"])
    for r in msgs:
        axb.scatter(r["min"], rows[r["handle"]], s=22, marker="s",
                    color=TOX_RAMP(r["tox"]), edgecolor=SURFACE, linewidth=0.5, zorder=3)
    axb.axvline(onset, color=INK, lw=0.9, ls=(0, (4, 2)), zorder=2)
    axb.axvspan(0, onset, color="#f3f2ee", zorder=0)
    axb.text(onset / 2, len(rows) - 0.35, "free", ha="center", fontsize=6.2, color=INK2)
    axb.text(onset + 0.8, len(rows) - 0.35, "note phase (note appears at 15 min)",
             ha="left", fontsize=6.2, color=INK2)
    axb.set_yticks(range(len(rows)))
    axb.set_yticklabels([code[h] for h in sorted(handles, key=lambda h: code[h])],
                        fontsize=6.8)
    axb.set_ylim(len(rows) - 0.1, -1.3)  # top-to-bottom, headroom for the label
    axb.set_xlim(-1, msgs[-1]["min"] + 2)
    axb.set_xlabel("Minutes into the session", fontsize=7.5)
    axb.tick_params(axis="x", labelsize=7)
    for side in ("top", "right", "left"):
        axb.spines[side].set_visible(False)
    axb.tick_params(axis="y", length=0)
    axb.set_title(f"One session: {S['nMessages']} messages, {S['nParticipants']} fans",
                  fontsize=7.5, pad=4)
    # colour key: three swatches instead of a colourbar
    for k, (v, lab) in enumerate(((0.05, "calm"), (0.5, "heated"), (0.95, "toxic"))):
        axb.scatter(16 + k * 11, -0.85, s=22, marker="s", color=TOX_RAMP(v),
                    edgecolor=SURFACE, linewidth=0.5, clip_on=False, zorder=4)
        axb.text(17.6 + k * 11, -0.85, lab, fontsize=6, color=INK2, va="center")
    axb.text(-4.5, -1.55, "B", fontsize=9, fontweight="bold")

    save(fig, "fig_teaser")


if __name__ == "__main__":
    main()

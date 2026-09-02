#!/usr/bin/env python3
"""Figure 1 (teaser): the Community Notes mechanism, and one session in both arms.

Panel A draws the mechanism in three stages. Panel B draws one Day-1 session
message by message in both arms: the same six-person composition, the same
35-minute trigger, a Community Note in one arm and the inert feature in the
other. The session shown is the one whose treatment effect is the median of
the five, not the best case.

Run: python3 fig_teaser.py   ->  fig_teaser.png (here) + paper/figures/fig_teaser.pdf
"""
from matplotlib.colors import LinearSegmentedColormap

from defuselab import (ARM_COLOR, VIOLET, MAGENTA, INK, INK2, GRID, SURFACE, FancyArrowPatch,
                       FancyBboxPatch, NOTE_ONSET_MIN, S, codes_for, msgs, plt, save,
                       show_session)

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


def strip(ax, cond, label, show_xlabel):
    """One session-arm on Day 1, one square per message, rows = participants."""
    code = codes_for(show_session, cond)
    order = sorted(code, key=lambda h: code[h])
    rows = {h: i for i, h in enumerate(order)}
    sel = [r for r in msgs if r["session"] == show_session and r["cond"] == cond and r["day"] == 1]
    for r in sel:
        ax.scatter(r["min"], rows[r["handle"]], s=11, marker="s",
                   color=TOX_RAMP(r["tox"] / 100), edgecolor=SURFACE, linewidth=0.35, zorder=3)
    ax.axvline(NOTE_ONSET_MIN, color=INK, lw=0.9, ls=(0, (4, 2)), zorder=2)
    ax.axvspan(0, NOTE_ONSET_MIN, color="#f3f2ee", zorder=0)
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels([code[h] for h in order], fontsize=6)
    ax.set_ylim(len(rows) - 0.4, -1.25 if cond == "EXPT" else -0.6)
    ax.set_xlim(-1, 61)
    ax.set_xticks([0, 15, 30, 35, 45, 60])
    ax.tick_params(axis="x", labelsize=6.2, length=2)
    ax.tick_params(axis="y", length=0)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.text(0.0, 1.02, label, transform=ax.transAxes, ha="left", va="bottom",
            fontsize=6.8, fontweight="bold", color=ARM_COLOR[cond])
    if show_xlabel:
        ax.set_xlabel("Minutes into the session", fontsize=7)
    else:
        ax.tick_params(axis="x", labelbottom=False)


def main():
    fig = plt.figure(figsize=(7.0, 2.75))
    gs = fig.add_gridspec(1, 2, width_ratios=[2.05, 1], wspace=0.18,
                          left=0.005, right=0.985, top=0.9, bottom=0.14)

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

    # ---- Panel B: one session, both arms, one square per message ------------
    gsb = gs[1].subgridspec(2, 1, hspace=0.55)
    axe = fig.add_subplot(gsb[0])
    axc = fig.add_subplot(gsb[1], sharex=axe)
    strip(axe, "EXPT", "Community Note arm", False)
    strip(axc, "CTRL", "Control arm", True)
    axe.text(NOTE_ONSET_MIN + 1.0, -0.75, "feature appears", ha="left", va="center",
             fontsize=5.8, color=INK2, style="italic")
    fig.text(0.665, 0.965, f"Session {show_session[1]}, Day 1 (A = ARMY, B = BLINK)",
             fontsize=7, fontweight="bold", ha="left", va="center")
    # colour key: three swatches instead of a colourbar, on the control strip's label row
    for k, (v, lab) in enumerate(((0.05, "calm"), (0.5, "heated"), (0.95, "toxic"))):
        x = 24 + k * 13
        axc.scatter(x, -0.95, s=11, marker="s", color=TOX_RAMP(v), edgecolor=SURFACE,
                    linewidth=0.35, clip_on=False, zorder=4)
        axc.text(x + 1.6, -0.95, lab, fontsize=6, color=INK2, va="center", ha="left")
    fig.text(0.655, 0.965, "B", fontsize=9, fontweight="bold", ha="right", va="center")

    save(fig, "fig_teaser")


if __name__ == "__main__":
    main()

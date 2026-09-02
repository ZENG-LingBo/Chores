#!/usr/bin/env python3
"""Figure 2: the escalation the note prevented, at the participant level.

Left: Day-1 toxicity before and after the feature in each arm. Bars are
message-level means (what the reported tests use); dots are individual
participants' means, connected across the two phases, so the reader sees both
the average and the people behind it. Right: each participant's change,
split into the platform-coded heavy poster of each session and everyone
else: in the note arm the periphery cooled while the core heated; in the
control arm both rose together.

Run: python3 fig_participants.py -> fig_participants.png + paper/figures/fig_participants.pdf
"""
import numpy as np

from defuselab import (ARMS, ARM_COLOR, ARM_LIGHT, ARM_NAME, INK, INK2, SURFACE, A, S,
                       clean_axes, per, plt, save)

RNG = np.random.default_rng(11)
XPOS = {"EXPT": (0.0, 1.0), "CTRL": (2.4, 3.4)}


def participants(cond):
    ps = [p for p in per.values() if p["cond"] == cond and p["pre"] and p["post"]]
    return [(np.mean(p["pre"]), np.mean(p["post"]), p["heavy"]) for p in ps]


def main():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.0, 3.0),
                                   gridspec_kw={"width_ratios": [1.45, 1]},
                                   constrained_layout=True)

    # ---- Left: arm x phase, bars = message means, dots = participants -------
    for c in ARMS:
        x_pre, x_post = XPOS[c]
        for x, ph, col in ((x_pre, "pre", ARM_LIGHT[c]), (x_post, "post", ARM_COLOR[c])):
            m = A[c][ph].mean()
            ax1.bar(x, m, width=0.62, color=col, edgecolor=SURFACE, linewidth=1.5, zorder=1)
            ax1.text(x, 2.5, f"{m:.1f}", ha="center", va="bottom", fontsize=7.5,
                     fontweight="bold", color=INK if ph == "pre" else SURFACE, zorder=5)
        pts = participants(c)
        xa = x_pre + RNG.uniform(-0.15, 0.15, len(pts))
        xb = x_post + RNG.uniform(-0.15, 0.15, len(pts))
        for (a, b, heavy), x0, x1 in zip(pts, xa, xb):
            ax1.plot([x0, x1], [a, b], color=INK if heavy else INK2,
                     lw=1.1 if heavy else 0.5, alpha=0.95 if heavy else 0.35, zorder=3)
        ax1.scatter(xa, [p[0] for p in pts], s=13, color=INK, zorder=4,
                    edgecolor=SURFACE, linewidth=0.6)
        ax1.scatter(xb, [p[1] for p in pts], s=13, color=INK, zorder=4,
                    edgecolor=SURFACE, linewidth=0.6)
        ax1.text((x_pre + x_post) / 2, -22, ARM_NAME[c] + " arm", ha="center", va="top",
                 fontsize=7.5, fontweight="bold", color=ARM_COLOR[c])
    ax1.set_xticks([XPOS[c][i] for c in ARMS for i in (0, 1)])
    ax1.set_xticklabels([f"before\n0–{S['noteOnsetMin']} min", f"after\n{S['noteOnsetMin']}–{S['sessionMinutes']} min"] * 2,
                        fontsize=7)
    ax1.set_xlim(-0.6, 4.0)
    ax1.set_ylim(0, 100)
    ax1.set_ylabel("Mean toxicity (0–100)", fontsize=7.5)
    clean_axes(ax1)
    ax1.set_title("Day 1: before and after the feature", fontsize=8, pad=4)
    ax1.text(0.5, 0.985,
             f"difference-in-differences over sessions: {S['didM']} points, "
             f"t({S['didDf']}) = {S['didT']}, p {S['didP']}",
             transform=ax1.transAxes, ha="center", va="top", fontsize=6.2, color=INK2)
    ax1.text(0.99, 0.87, "thick lines: the session's heaviest poster", transform=ax1.transAxes,
             ha="right", va="top", fontsize=6.2, color=INK2, style="italic")

    # ---- Right: change per participant, core vs periphery ------------------
    groups = []
    for c in ARMS:
        pts = participants(c)
        groups.append((c, "periphery", [b - a for a, b, h in pts if not h], False))
        groups.append((c, "heaviest\nposter", [b - a for a, b, h in pts if h], True))
    xs = [0, 1.3, 3.1, 4.4]
    for x, (c, lab, vals, heavy) in zip(xs, groups):
        m = np.mean(vals)
        ax2.bar(x, m, width=0.62, color=ARM_COLOR[c], edgecolor=SURFACE, linewidth=1.5,
                hatch="///" if heavy else None, zorder=1)
        ax2.scatter(x + RNG.uniform(-0.15, 0.15, len(vals)), vals, s=13, color=INK, zorder=4,
                    edgecolor=SURFACE, linewidth=0.6)
        # value label beside the bar, on the side away from its neighbour
        side = -1 if not heavy else 1
        ax2.text(x + side * 0.38, m, f"{m:+.1f}", ha="right" if side < 0 else "left",
                 va="center", fontsize=7.2, fontweight="bold", color=INK, zorder=5)
    ax2.axhline(0, color=INK2, lw=0.8)
    ax2.set_xticks(xs)
    ax2.set_xticklabels([f"{g[1]}\n(n = {len(g[2])})" for g in groups], fontsize=6.6)
    for c, x in zip(ARMS, (0.65, 3.75)):
        ax2.text(x, -84, ARM_NAME[c] + " arm", ha="center", va="top",
                 fontsize=7.5, fontweight="bold", color=ARM_COLOR[c])
    ax2.set_xlim(-1.0, 5.3)
    ax2.set_ylim(-52, 52)
    ax2.set_ylabel("Change in mean toxicity (after − before)", fontsize=7.5)
    clean_axes(ax2)
    ax2.set_title("Who changed", fontsize=8, pad=4)
    ax2.text(0.02, 0.985, f"note arm, core vs. periphery: Welch t({S['exptHeavyPeriDf']}) = "
             f"{S['exptHeavyPeriT']}, p {S['exptHeavyPeriP']}",
             transform=ax2.transAxes, ha="left", va="top", fontsize=6.2, color=INK2)

    save(fig, "fig_participants")


if __name__ == "__main__":
    main()

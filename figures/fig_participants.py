#!/usr/bin/env python3
"""Figure 3: the ceasefire at the participant level.

Bars are message-level means, the same quantities the reported tests use;
dots are individual participants' means, so the reader sees both the average
and the people behind it. Left: the whole free and note phases. Right: the
clearest contrast -- the peak window before the note against the quietest
window after it.

Run: python3 fig_participants.py -> fig_participants.png + paper/figures/fig_participants.pdf
"""
import numpy as np

from defuselab import (BLUE, ORANGE, INK, INK2, SURFACE, S, clean_axes, code, free_tox,
                       most_toxic, msgs, n_pre, note_tox, per, plt, save, win_edges,
                       win_labels, win_means)

RNG = np.random.default_rng(11)


def participant_means(lo, hi):
    """Per-participant mean toxicity for messages posted in [lo, hi)."""
    out = {}
    for h in per:
        v = [r["tox"] for r in msgs if r["handle"] == h and lo <= r["min"] < hi]
        if v:
            out[h] = np.mean(v)
    return out


def bar_with_dots(ax, i, bar_mean, dots, col):
    ax.bar(i, bar_mean, width=0.58, color=col, edgecolor=SURFACE, linewidth=1.5, zorder=1)
    ax.text(i, 0.018, f"{bar_mean:.3f}", ha="center", va="bottom",
            fontsize=7.5, fontweight="bold", color=SURFACE, zorder=5)
    xs = i + RNG.uniform(-0.14, 0.14, len(dots))
    ax.scatter(xs, dots, s=16, color=INK, zorder=4, edgecolor=SURFACE, linewidth=0.7)
    return xs


def finish(ax, labels, title, note):
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, fontsize=7, linespacing=1.15)
    ax.set_xlim(-0.75, 1.75)
    ax.set_ylim(0, 0.64)
    clean_axes(ax)
    ax.set_title(title, fontsize=8, pad=4)
    ax.text(0.5, 0.985, note, transform=ax.transAxes, ha="center", va="top",
            fontsize=6.6, color=INK2)


def main():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6.9, 2.9), sharey=True,
                                   constrained_layout=True)

    # ---- Left: whole phases --------------------------------------------------
    both = [h for h in per if per[h]["free"] and per[h]["note"]]
    fv = [np.mean(per[h]["free"]) for h in both]
    nv = [np.mean(per[h]["note"]) for h in both]
    x0 = bar_with_dots(ax1, 0, free_tox.mean(), fv, BLUE)
    x1 = bar_with_dots(ax1, 1, note_tox.mean(), nv, ORANGE)
    for a, b, xa, xb, h in zip(fv, nv, x0, x1, both):
        hot = h == most_toxic
        ax1.plot([xa, xb], [a, b], color=ORANGE if hot else INK2, lw=1.1 if hot else 0.6,
                 alpha=0.9 if hot else 0.45, zorder=3)
        if hot:
            ax1.annotate(f"{code[h]} (most toxic)", xy=(xb, b), xytext=(1.34, b),
                         fontsize=6.8, color=ORANGE, va="center")
    finish(ax1,
           [f"Free phase\n0–{S['noteOnsetMin']} min\n{S['nFreeMsgs']} messages",
            f"Note phase\n{S['noteOnsetMin']}–{S['sessionMinutes']} min\n{S['nNoteMsgs']} messages"],
           "Whole phases",
           f"messages: Welch t({S['msgWelchDf']}) = {S['msgWelchT']}, p = {S['msgWelchP']}\n"
           f"participants: paired t({len(both)-1}) = {S['pairedT']}, p = {S['pairedP']}")
    ax1.set_ylabel("Mean toxicity", fontsize=7.5)

    # ---- Right: peak window before vs quietest window after --------------------
    peak_i = int(np.argmax(win_means[:n_pre]))
    trough_i = n_pre + int(np.argmin(win_means[n_pre:]))
    pk = participant_means(win_edges[peak_i], win_edges[peak_i + 1])
    tr = participant_means(win_edges[trough_i], win_edges[trough_i + 1])
    bar_with_dots(ax2, 0, win_means[peak_i], list(pk.values()), BLUE)
    bar_with_dots(ax2, 1, win_means[trough_i], list(tr.values()), ORANGE)
    finish(ax2,
           [f"Peak before\n{win_labels[peak_i]} min\n{S['peakWinN']} msgs, {len(pk)} people",
            f"Quietest after\n{win_labels[trough_i]} min\n{S['troughWinN']} msgs, {len(tr)} people"],
           "Clearest contrast",
           f"messages: Welch t({S['peakTroughDf']}) = {S['peakTroughT']}, p = {S['peakTroughP']}")

    save(fig, "fig_participants")


if __name__ == "__main__":
    main()

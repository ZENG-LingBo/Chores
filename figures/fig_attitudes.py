#!/usr/bin/env python3
"""Figure: the ceasefire did not make them friends online, but offline is another matter.

Panel A: the feeling thermometer gap toward the rival fandom is intact.
Panel B: on the same battery, the item participants rate highest is whether a
rival-fandom member could be a friend in real life -- the one place where the
hostility does not reach.

Run: python3 fig_attitudes.py -> fig_attitudes.png + paper/figures/fig_attitudes.pdf
"""
import numpy as np

from defuselab import BLUE, ORANGE, INK, INK2, LIGHT_BLUE, SURFACE, S, clean_axes, plt, save, sv

# (survey column, label) on the shared 1-5 agreement scale, ordered as drawn
ITEMS = [
    ("s1_perc_intelligent", "Rival fans are intelligent"),
    ("s1_perc_moral", "Rival fans are moral"),
    ("s1_simil_values", "We share values"),
    ("s1_contact_share", "Would share their post"),
    ("s1_contact_discuss", "Would discuss K-pop with them"),
    ("s1_contact_work", "Would work with them"),
    ("s1_contact_friends", "Could be friends in real life"),
]


def main():
    fig, (axa, axb) = plt.subplots(
        1, 2, figsize=(7.0, 2.6), gridspec_kw={"width_ratios": [1, 2.35], "wspace": 0.08},
        constrained_layout=True)

    # ---- Panel A: the thermometer gap, on its own 0-100 scale ------------
    own = np.mean([float(r["s1_therm_own"]) for r in sv])
    rival = np.mean([float(r["s1_therm_rival"]) for r in sv])
    bars = axa.bar([0, 1], [own, rival], width=0.6, color=[LIGHT_BLUE, BLUE],
                   edgecolor=SURFACE, linewidth=1.5)
    for b, v in zip(bars, (own, rival)):
        axa.text(b.get_x() + b.get_width() / 2, v + 2, f"{v:.0f}", ha="center",
                 va="bottom", fontsize=8, fontweight="bold", color=INK)
    axa.annotate("", xy=(1, rival + 4), xytext=(1, own - 2),
                 arrowprops=dict(arrowstyle="<->", color=INK2, lw=1.0))
    axa.text(1.12, (own + rival) / 2, f"{own - rival:.0f}-point\ngap", fontsize=7,
             color=INK2, va="center", ha="left")
    axa.set_xticks([0, 1])
    axa.set_xticklabels(["Own\nfandom", "Rival\nfandom"], fontsize=7.5)
    axa.set_ylabel("Feeling thermometer (0–100)", fontsize=7.5)
    axa.set_ylim(0, 108)
    axa.set_xlim(-0.6, 2.0)
    clean_axes(axa)
    axa.set_title("Hostility is intact", fontsize=8, pad=4)

    # ---- Panel B: the agreement battery, on its own 1-5 scale ------------
    vals = [np.mean([float(r[k]) for r in sv if r[k]]) for k, _ in ITEMS]
    ys = np.arange(len(ITEMS))
    hot = len(ITEMS) - 1  # "could be friends in real life"
    cols = [ORANGE if i == hot else BLUE for i in range(len(ITEMS))]
    axb.barh(ys, vals, height=0.62, color=cols, edgecolor=SURFACE, linewidth=1.2)
    for y, v, i in zip(ys, vals, range(len(ITEMS))):
        axb.text(v + 0.06, y, f"{v:.2f}", va="center", fontsize=7.5, color=INK,
                 fontweight="bold" if i == hot else "normal")
    axb.axvline(3, color=INK, lw=0.9, ls=(0, (4, 2)))
    axb.set_ylim(len(ITEMS) - 0.45, -1.0)  # inverted; headroom for the midpoint label
    axb.text(3.04, -0.68, "scale midpoint", fontsize=6.5, color=INK2, va="center")
    axb.set_yticks(ys)
    axb.set_yticklabels([lab for _, lab in ITEMS], fontsize=7.5)
    axb.set_xlim(1, 5.25)
    axb.set_xticks([1, 2, 3, 4, 5])
    axb.set_xlabel("Mean agreement (1–5)", fontsize=7.5)
    for side in ("top", "right"):
        axb.spines[side].set_visible(False)
    axb.grid(axis="x", color="#e5e4e0", linewidth=0.6)
    axb.set_axisbelow(True)
    axb.set_title("…but it stops at the screen", fontsize=8, pad=4)

    axa.text(-0.62, 116, "A", fontsize=9, fontweight="bold")
    axb.text(0.86, -0.95, "B", fontsize=9, fontweight="bold")
    save(fig, "fig_attitudes")


if __name__ == "__main__":
    main()

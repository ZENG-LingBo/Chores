# Figures

Each figure's code sits next to the PNG it produces. Every script is runnable on
its own and reads the CSVs in `../data/`, so a figure can be tweaked and rebuilt
without touching anything else.

| Paper | Script | Image | What it shows |
|---|---|---|---|
| Fig. 1 (teaser) | `fig_teaser.py` | `fig_teaser.png` | The Community Notes mechanism in three stages, plus one Day-1 session drawn message by message in both arms |
| Fig. 2 | `fig_participants.py` | `fig_participants.png` | Day-1 toxicity before and after the feature by arm, with every participant; and who changed (periphery vs. heaviest poster) |
| Fig. 3 | `fig_histogram.py` | `fig_histogram.png` | Toxicity distributions before/after by arm: control shifts right as a block, the note arm splits |
| Fig. 4 | `fig_windows.py` | `fig_windows.png` | Five-minute windows on both days: the arms climb together, diverge at the feature, and resume at their Day-1 levels on Day 2 |
| Fig. 5 | `fig_days.py` | `fig_days.png` | Session-level means for Day 1 before/after and Day 2 by arm, with significance brackets |
| Fig. 6 | `fig_attitudes.py` | `fig_attitudes.png` | Pilot survey: hostility intact (thermometer gap) but confined to the screen (could be friends in real life) |

Shared code:

- `convert_all_data.py` — flattens the group's coded KFeed export
  (`../data/raw/all_data.xlsx`) into `../data/defuselab-all-messages.csv`. Needs
  `openpyxl`; run only when the workbook changes.
- `defuselab.py` — loads the message log and the pilot survey, computes **every
  statistic the paper reports** into the dict `S` (arm × phase means, the
  session-level difference-in-differences, the message-level interaction,
  participant-level paired tests, core vs. periphery, engagement, note-task and
  pronoun shares, five-minute windows, Day-2 tests, the robustness table), and
  holds the palette and plotting helpers. Figures and manuscript therefore print
  the same numbers.
- `make_all.py` — rebuilds all six figures and regenerates `../paper/stats.tex`,
  the macro file the manuscript's numbers come from.

## Rebuilding

```bash
pip install matplotlib numpy scipy

python3 make_all.py          # all six figures + paper/stats.tex
python3 fig_windows.py       # or just one figure
```

Each run writes two files: `<name>.png` here (300 dpi, for slides and talks) and
`../paper/figures/<name>.pdf` (vector, what LaTeX includes). After changing data
or a figure, run `make_all.py` and recompile the paper so text and figures stay
in sync:

```bash
cd ../paper && latexmk -pdf main.tex
```

Colors come from a validated colorblind-safe palette and always encode the arm:
orange is the Community Note arm, blue the control arm; the lighter tint of each
is the phase before the feature. Figure 2 also hatches the heaviest-poster bars
so that identity is never carried by color alone.

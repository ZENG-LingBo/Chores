# Figures

Each figure's code sits next to the PNG it produces. Every script is runnable on
its own and reads the CSVs in `../data/`, so a figure can be tweaked and rebuilt
without touching anything else.

| Paper | Script | Image | What it shows |
|---|---|---|---|
| Fig. 1 (teaser) | `fig_teaser.py` | `fig_teaser.png` | The Community Notes mechanism in three stages, plus the headline drop (0.329 → 0.220, −33%) |
| Fig. 2 | `fig_windows.py` | `fig_windows.png` | Mean toxicity in ten-minute windows; every post-note window is below every pre-note one |
| Fig. 3 | `fig_participants.py` | `fig_participants.png` | Paired per-participant slopes, free → note phase (4 of 5 declined) |
| Fig. 4 | `fig_histogram.py` | `fig_histogram.png` | Toxicity distribution before/after; the most toxic participant stays in the right tail |
| Fig. 5 | `fig_days.py` | `fig_days.png` | Day 1 phases versus Day 2 without the feature |

Shared code:

- `defuselab.py` — loads the three CSVs (deduping the concatenated message
  export), computes **every statistic the paper reports** into the dict `S`, and
  holds the palette and plotting helpers. Figures and manuscript therefore print
  the same numbers.
- `make_all.py` — rebuilds all five figures and regenerates `../paper/stats.tex`,
  the macro file the manuscript's numbers come from.

## Rebuilding

```bash
pip install matplotlib numpy scipy

python3 make_all.py          # all five figures + paper/stats.tex
python3 fig_windows.py       # or just one figure
```

Each run writes two files: `<name>.png` here (300 dpi, for slides and talks) and
`../paper/figures/<name>.pdf` (vector, what LaTeX includes). After changing data
or a figure, run `make_all.py` and recompile the paper so text and figures stay
in sync:

```bash
cd ../paper && latexmk -pdf main.tex
```

Colors come from a validated colorblind-safe palette; blue always means the
baseline/free phase, orange the intervention/note phase and the highlighted
participant. Figure 4 also hatches the highlighted series so identity is never
carried by color alone.

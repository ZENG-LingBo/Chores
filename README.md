# Chores

## DefuseLab paper: figures + LaTeX manuscript

CHI-style draft of the polarization-defusing (Community Notes) study, with all
figures, tables, and statistics computed from the DefuseLab data exports.

```
data/       DefuseLab exports (messages, per-participant sessions, surveys)
figures/    one script per figure, each next to the PNG it produces, plus
            defuselab.py (data + every statistic) and make_all.py
analysis/   analyze.py -- wrapper that runs the whole figures/ pipeline
paper/      main.tex (acmart manuscript, anonymous) + references.bib + build
            SUBMISSION.md -- CHI 2027 PCS keywords and paste-ready form fields
```

### Rebuild

```bash
pip install matplotlib numpy scipy
python3 analysis/analyze.py       # all figures + stats.tex (same as figures/make_all.py)
cd paper && latexmk -pdf main.tex # needs texlive-publishers (acmart) et al.
```

A single figure can be rebuilt on its own, e.g. `cd figures && python3 fig_windows.py`.
Each run writes `figures/<name>.png` (300 dpi) and `paper/figures/<name>.pdf` (vector,
what LaTeX includes). See `figures/README.md` for the figure-by-figure map.

All numbers in the manuscript come from `paper/stats.tex` (auto-generated), so
re-running the analysis after a data update flows straight into the PDF.
Remaining author TODOs are marked in orange in the compiled PDF (IRB details,
focus-group quote completions); bibliography entries are canonical best-effort
matches to the draft's citation hints and should be verified before submission.

# Chores

## DefuseLab paper: figures + LaTeX manuscript

CHI-style draft of the polarization-defusing (Community Notes) study, with all
figures, tables, and statistics computed from the DefuseLab data exports.

```
data/       DefuseLab exports (messages, per-participant sessions, surveys)
analysis/   analyze.py -- dedupes the message export, computes every statistic,
            renders paper/figures/*.pdf and writes paper/stats.tex macros
paper/      main.tex (acmart manuscript, anonymous) + references.bib + build
```

### Rebuild

```bash
pip install matplotlib numpy scipy
python3 analysis/analyze.py       # regenerates figures + stats.tex
cd paper && latexmk -pdf main.tex # needs texlive-publishers (acmart) et al.
```

All numbers in the manuscript come from `paper/stats.tex` (auto-generated), so
re-running the analysis after a data update flows straight into the PDF.
Remaining author TODOs are marked in orange in the compiled PDF (IRB details,
focus-group quote completions); bibliography entries are canonical best-effort
matches to the draft's citation hints and should be verified before submission.

#!/usr/bin/env python3
"""Rebuild the whole analysis: every figure plus paper/stats.tex.

The analysis itself lives in ../figures/, where each figure's code sits next to
the PNG it produces:
    figures/defuselab.py   data loading + every statistic the paper reports
    figures/fig_*.py       one script per figure (runnable on its own)
    figures/make_all.py    all five figures + paper/stats.tex

This wrapper just calls that pipeline so `python3 analysis/analyze.py` keeps
working from the repository root.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "figures"))

import make_all  # noqa: E402

if __name__ == "__main__":
    make_all.main()

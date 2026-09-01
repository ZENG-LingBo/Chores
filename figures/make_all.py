#!/usr/bin/env python3
"""Rebuild every figure and regenerate paper/stats.tex.

Run: python3 make_all.py
(Each figure can also be rebuilt on its own, e.g. python3 fig_windows.py)
"""
import json

import defuselab
import fig_days
import fig_histogram
import fig_participants
import fig_teaser
import fig_windows


def main():
    for module in (fig_teaser, fig_windows, fig_participants, fig_histogram, fig_days):
        module.main()
    path = defuselab.write_stats_tex()
    print("\nwrote", path)
    print(json.dumps(defuselab.S, indent=2))
    print("\nParticipant codes:",
          {defuselab.code[h]: h for h in defuselab.handles})


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Plot fixed-load and actual receiver-load comparisons with the scaling cost."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
evidence = ROOT / "doc/porting/evidence"
new = pd.read_csv(evidence / "sky_input2_candidate_nominal6.csv").sort_values("corner_mos")
old = pd.read_csv(evidence / "sky_tg2_feasible_ac.csv")
old = new[["corner_mos", "gcode"]].merge(old, on=["corner_mos", "gcode"], validate="one_to_one")
loaded = pd.read_csv(evidence / "input2_fanout6_matched.csv").sort_values(["fanout_input", "c_load"])
fig, axes = plt.subplots(1, 2, figsize=(12, 4), layout="constrained")
x = np.arange(5)
axes[0].bar(x-.18, old.bw_in2_ratio, .36, label="2 copies, 5.73 µm fixed loads")
axes[0].bar(x+.18, new.bw2_ratio_ihp, .36, label="6 copies, 1.41 µm fixed loads")
axes[0].set_xticks(x, new.corner_mos)
axes[0].set_title("100 fF per output, nominal MOS corners")
for copies, offset in [(2, -.18), (6, .18)]:
    rows = loaded[loaded.power_m == copies]
    axes[1].bar(np.arange(4)+offset, rows.bw2_ratio_ihp, .36, label=f"{copies} copies, identical receiver")
axes[1].set_xticks(np.arange(4), ["in1\n25 fF", "in1\n50 fF", "in2\n25 fF", "in2\n50 fF"])
axes[1].set_title("Slow corner, 1.41 µm loads in both variants")
axes[1].set_xlabel("Receiver input and wire capacitance per output")
for ax in axes:
    ax.axhline(1, color="black", linestyle=":")
    ax.set_ylabel("Input-2 bandwidth / matched IHP bandwidth")
    ax.grid(axis="y", alpha=.2)
    ax.legend(fontsize=8)
fig.suptitle("Six copies cost about 3× supply current and input capacitance versus two copies")
folder = ROOT / "doc/porting/figures"
fig.savefig(folder / "input2_improvement.png", dpi=180)
fig.savefig(folder / "input2_improvement.pdf")

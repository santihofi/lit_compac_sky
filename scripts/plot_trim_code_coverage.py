#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Plot nominal same-code gain, shape and bandwidth evidence."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
evidence = ROOT / "doc/porting/evidence"
dc = pd.read_csv(evidence / "sky_tg2_codes_nominal.csv")
ac = pd.read_csv(evidence / "sky_tg2_feasible_ac.csv")
fig, axes = plt.subplots(1, 3, figsize=(14, 4), layout="constrained")
for corner, rows in dc.groupby("corner_mos"):
    rows = rows.sort_values("gcode")
    line, = axes[0].plot(rows.gcode, rows.gain_error_percent, label=corner)
    axes[1].plot(rows.gcode, rows.compr, color=line.get_color())
    speed = ac[ac.corner_mos == corner].sort_values("gcode")
    axes[2].plot(speed.gcode, speed.bw_in2_ratio, "o-", color=line.get_color())
axes[0].axhspan(-1, 1, alpha=.15, color="green")
axes[1].axhspan(.96758, 1.03242, alpha=.15, color="green")
axes[2].axhline(1, color="black", linestyle=":")
for axis, title, ylabel in zip(axes,
    ["Gain error, provisional ±1% screen", "Diagonal shape", "Input-2 speed at DC-feasible codes"],
    ["K100 magnitude error (%)", "K100 / K10", "Bandwidth / matched IHP bandwidth"]):
    axis.set(title=title, xlabel="Gain code", ylabel=ylabel)
    axis.grid(alpha=.2)
axes[0].legend(title="SKY130 MOS corner")
fig.suptitle("Transmission-gate trim: 1.5 V, 27 °C, nominal passives, ideal bias")
folder = ROOT / "doc/porting/figures"
folder.mkdir(exist_ok=True)
fig.savefig(folder / "tg2_nominal_code_coverage.png", dpi=180)
fig.savefig(folder / "tg2_nominal_code_coverage.pdf")

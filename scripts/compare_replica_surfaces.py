#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Pair opposite raw skew labels before comparing the two PDK surface grids."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
evidence = ROOT/"doc/porting/evidence"
sky = pd.read_csv(evidence/"sky_replica_surface_corners.csv")
ihp = pd.read_csv(evidence/"ihp_surface_corners.csv")
sky["speed_case"] = sky.corner_mos.replace({"fs": "Nslow Pfast", "sf": "Nfast Pslow"})
ihp["speed_case"] = ihp.corner_mos.replace({"sf": "Nslow Pfast", "fs": "Nfast Pslow"})
metrics = ["fit_product_gain_per_v", "peak_residual_percent_fullscale",
           "rms_residual_percent_fullscale"]
keys = ["speed_case", "temp", "vdd", "vincm", "gcode"]
data = sky[keys+metrics].merge(ihp[keys+metrics], on=keys, suffixes=("_sky", "_ihp"),
                             validate="one_to_one")
if len(data) != 15:
    raise ValueError("Expected 15 matched semantic corners")
for metric in metrics[1:]:
    data[metric+"_ratio"] = data[metric+"_sky"]/data[metric+"_ihp"]
data.to_csv(evidence/"replica_ihp_matched_surfaces.csv", index=False)
fig, axes = plt.subplots(1, 2, figsize=(10, 4), constrained_layout=True)
for metric, ax, title in zip(metrics[1:], axes, ["Peak surface residual", "RMS surface residual"]):
    for name, frame in data.groupby("speed_case"):
        frame = frame.sort_values("temp")
        ax.plot(frame.temp, frame[metric+"_ratio"], "o-", label=name)
    ax.axhline(1, color="black", linewidth=.8)
    ax.set(xlabel="Temperature (C)", ylabel="SKY130 / IHP", title=title)
    ax.grid(True, alpha=.25)
axes[1].legend(title="Matched MOS speeds")
fig.suptitle("Replica candidate shape error at 1.5 V, CM 0.75 V and code 13\n"
             "Each surface normalized to its own fitted product gain")
for ext in ["png", "pdf"]:
    fig.savefig(ROOT/"doc/porting/figures"/("replica_ihp_matched_surfaces."+ext), dpi=180)
print(data[["speed_case", "temp"]+[m+"_ratio" for m in metrics[1:]]].to_string(index=False))

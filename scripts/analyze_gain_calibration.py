#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Audit laboratory-temperature code sweeps and select gain-10 settings."""
import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from check_chipify_results import audit

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument("--design", choices=["ihp", "sky"], required=True)
args = parser.parse_args()
project = ROOT / "verification/porting" / (
    "ihp_gain_trim" if args.design == "ihp" else "sky_replica_trim_range")
audits, frames = {}, []
for corner in ["ff", "fs", "sf", "ss", "tt"]:
    if args.design == "ihp":
        name = "steps_tt" if corner == "tt" else "lab_steps_" + corner
        folder = "steps" if corner == "tt" else "lab_steps"
    else:
        name, folder = "centered_steps_" + corner, "steps"
    sheet = project / "datasheets" / folder / (name + ".yaml")
    out = project / "out" / name
    audits[name] = audit(sheet, out, False)
    frame = pd.read_csv(out / "simulation_results.csv")
    if sorted(frame.gcode) != list(range(32)) or frame.corner_mos.unique().tolist() != [corner]:
        raise ValueError(f"Incomplete or duplicate code identities in {name}")
    if not ((frame.temp == 27).all() and (frame.vdd == 1.5).all()):
        raise ValueError("Calibration must use 27 C and 1.5 V")
    frame["datasheet"] = name
    frames.append(frame)
data = pd.concat(frames, ignore_index=True)
summary = []
for corner, group in data.groupby("corner_mos"):
    group = group.sort_values("gcode").copy()
    for metric in ["k100", "k10"]:
        magnitude = group[metric].abs()
        steps = np.diff(magnitude)
        closest = group.loc[(magnitude - 10).abs().idxmin()]
        shape = group[group.compr.between(.96758, 1.03242)]
        valid = None if shape.empty else shape.loc[(shape[metric].abs() - 10).abs().idxmin()]
        record = {
            "corner_mos": corner, "metric": metric,
            "minimum_gain": float(magnitude.min()), "maximum_gain": float(magnitude.max()),
            "brackets_target10": bool(magnitude.min() <= 10 <= magnitude.max()),
            "strictly_monotonic": bool(np.all(steps > 0)),
            "minimum_step_percent_of_10": float(steps.min() * 10),
            "maximum_step_percent_of_10": float(steps.max() * 10),
            "nearest_code": int(closest.gcode),
            "nearest_gain": float(abs(closest[metric])),
            "nearest_error_percent": float((abs(closest[metric]) / 10 - 1) * 100),
            "nearest_code_compression": float(closest.compr),
            "shape_qualified_codes": int(len(shape)),
            "nearest_shape_qualified_code": None if valid is None else int(valid.gcode),
            "nearest_shape_qualified_error_percent": None if valid is None else float(
                (abs(valid[metric]) / 10 - 1) * 100),
            "ibias_source_value": str(closest.ibias),
        }
        if "bw_in1_mhz" in group:
            record.update(bw_in1_mhz=float(closest.bw_in1_mhz),
                          bw_in2_mhz=float(closest.bw_in2_mhz))
        summary.append(record)
prefix = ROOT / "doc/porting/evidence" / (
    "ihp_gain_calibration" if args.design == "ihp" else "sky_centered_gain_calibration")
data.to_csv(str(prefix) + ".csv", index=False)
Path(str(prefix) + "_audit.json").write_text(json.dumps(audits, indent=2) + "\n")
Path(str(prefix) + "_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
print(pd.DataFrame(summary)[["corner_mos", "metric", "strictly_monotonic",
      "nearest_code", "nearest_error_percent", "nearest_code_compression",
      "nearest_shape_qualified_code"]].to_string(index=False))

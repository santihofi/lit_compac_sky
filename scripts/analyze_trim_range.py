#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Audit independent fixed/trim resistance controls and freeze their results."""
import argparse
import json
from pathlib import Path

import pandas as pd

from check_chipify_results import audit

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument("--group", choices=["initial", "centered"], default="initial")
args = parser.parse_args()
project = ROOT / "verification/porting/sky_replica_trim_range"
folder = project / "datasheets"
pattern = "range_*.yaml"
if args.group == "centered":
    folder /= "centered"
    pattern = "centered_*.yaml"
frames, audits = [], {}
for sheet in sorted(folder.glob(pattern)):
    out = project / "out" / sheet.stem
    audits[sheet.name] = audit(sheet, out, False)
    frame = pd.read_csv(out / "simulation_results.csv")
    frame["datasheet"] = sheet.name
    frames.append(frame)
expected = 2 if args.group == "initial" else 5
if len(frames) != expected:
    raise ValueError(f"Expected {expected} completed sheets")
data = pd.concat(frames, ignore_index=True)
keys = ["corner_mos", "temp", "vdd", "rbase_scale", "rtrim_scale"]
coverage = []
for key, group in data.groupby(keys):
    if sorted(group.gcode) != [0, 31]:
        raise ValueError("Expected one endpoint pair")
    record = dict(zip(keys, key))
    for metric in ["k100", "k10"]:
        values = group[metric].abs()
        record[metric + "_min"] = float(values.min())
        record[metric + "_max"] = float(values.max())
        record[metric + "_brackets10"] = bool(values.min() <= 10 <= values.max())
    record["all_endpoint_ratios_pass"] = bool(group.compr.between(.96758, 1.03242).all())
    coverage.append(record)
prefix = ROOT / "doc/porting/evidence" / ("sky_replica_trim_range_" + args.group)
data.to_csv(str(prefix) + ".csv", index=False)
Path(str(prefix) + "_audit.json").write_text(json.dumps(audits, indent=2) + "\n")
Path(str(prefix) + "_coverage.json").write_text(json.dumps(coverage, indent=2) + "\n")
print(pd.DataFrame(coverage).to_string(index=False))

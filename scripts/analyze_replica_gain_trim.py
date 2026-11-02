#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Audit endpoint coverage without claiming monotonicity or exact-code coverage."""
import json
from pathlib import Path

import pandas as pd

from check_chipify_results import audit

ROOT = Path(__file__).resolve().parents[1]
base = ROOT/"verification/porting"
evidence = ROOT/"doc/porting/evidence"
audits, frames = {}, []
sky = base/"sky_replica_gain_trim"
for sheet in sorted((sky/"datasheets/endpoints").glob("*.yaml")):
    out = sky/"out"/sheet.stem
    audits[sheet.name] = audit(sheet, out, False)
    frame = pd.read_csv(out/"simulation_results.csv")
    frame["datasheet"] = sheet.name
    frames.append(frame)
sky_data = pd.concat(frames, ignore_index=True)
sky_data.to_csv(evidence/"sky_replica_gain_trim.csv", index=False)
(evidence/"sky_replica_gain_trim_audit.json").write_text(json.dumps(audits,indent=2)+"\n")
ihp = base/"ihp_gain_trim"
ihp_audit = audit(ihp/"datasheets/endpoints.yaml", ihp/"out")
(evidence/"ihp_gain_trim_audit.json").write_text(json.dumps(ihp_audit,indent=2)+"\n")
ihp_data = pd.read_csv(ihp/"out/simulation_results.csv")
ihp_data.to_csv(evidence/"ihp_gain_trim.csv",index=False)
summary, rows = {}, []
keys = ["corner_mos", "temp", "vdd"]
for label, data in [
    ("SKY130 replica, VDD drive", sky_data),
    ("IHP, historical 1.5 V drive", ihp_data[ihp_data.gate_tracks_vdd == 0]),
    ("IHP, VDD drive", ihp_data[ihp_data.gate_tracks_vdd == 1]),
]:
    counts = {}
    for metric in ["k100", "k10"]:
        table = data.pivot(index=keys, columns="gcode", values=metric).abs()
        if len(table) != 45 or table.isna().any().any():
            raise ValueError("Missing endpoint pair")
        low, high = table.min(axis=1), table.max(axis=1)
        covered = (low <= 10) & (high >= 10)
        counts[metric] = int(covered.sum())
        for index, values in table.iterrows():
            rows.append(dict(design=label, corner_mos=index[0], temp=index[1], vdd=index[2],
                             metric=metric, magnitude_code0=values[0], magnitude_code31=values[31],
                             brackets_target10=bool(covered.loc[index])))
    summary[label] = counts
    print(label, counts)
coverage = pd.DataFrame(rows)
coverage.to_csv(evidence/"replica_ihp_gain_endpoint_coverage.csv",index=False)
keyed = ihp_data.set_index(keys+["gcode"])
fixed = keyed[keyed.gate_tracks_vdd == 0].drop(columns="gate_tracks_vdd")
tracking = keyed[keyed.gate_tracks_vdd == 1].drop(columns="gate_tracks_vdd")
differences = (tracking[["k100","k10","bw_in1_mhz","bw_in2_mhz"]] /
               fixed[["k100","k10","bw_in1_mhz","bw_in2_mhz"]] - 1).abs()
summary["ihp_maximum_relative_change_from_gate_rail"] = differences.max().to_dict()
(evidence/"replica_ihp_gain_endpoint_summary.json").write_text(json.dumps(summary,indent=2)+"\n")
print(summary["ihp_maximum_relative_change_from_gate_rail"])
print(coverage[(coverage.metric=="k100") & (~coverage.brackets_target10)]
      .groupby(["design","temp"]).size().to_string())

mid_out = ihp/"out/midcode"
mid_audit = audit(ihp/"datasheets/midcode/midcode.yaml", mid_out)
(evidence/"ihp_midcode_rails_audit.json").write_text(json.dumps(mid_audit,indent=2)+"\n")
mid = pd.read_csv(mid_out/"simulation_results.csv")
mid.to_csv(evidence/"ihp_midcode_rails.csv",index=False)
metrics = ["k100","k10","compr","bw_in1_mhz","bw_in2_mhz"]
ranges = {}
for mode in [0,1]:
    data = mid[mid.gate_tracks_vdd == mode]
    ranges[str(mode)] = {m: {"min": float(data[m].min()), "max": float(data[m].max())}
                         for m in metrics}
first = mid[mid.gate_tracks_vdd == 0].set_index(keys)
second = mid[mid.gate_tracks_vdd == 1].set_index(keys)
ranges["maximum_relative_change"] = (second[metrics]/first[metrics]-1).abs().max().to_dict()
(evidence/"ihp_midcode_rails_summary.json").write_text(json.dumps(ranges,indent=2)+"\n")

#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Audit global smaller-pair endpoints without treating span as calibrated coverage."""
import argparse
import json
from pathlib import Path
import numpy as np
import pandas as pd
import yaml
from check_chipify_results import audit

ROOT = Path(__file__).resolve().parents[1]
evidence = ROOT / "doc/porting/evidence"
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--trim-range", action="store_true")
args = parser.parse_args()
name = "sky_input2_pair_trim_range" if args.trim_range else "sky_input2_pair_endpoints"
project = ROOT / "verification/porting" / name
trim_factors = [1.4, 1.6, 1.65, 1.7] if args.trim_range else [1.4]
points = [(c, 27, 1.5, .9 if c == "ss" else 1.) for c in ["ff", "fs", "sf", "ss", "tt"]]
points += [("fs", 80, v, .9) for v in [1.45, 1.5, 1.65]]
points += [("ss", 80, 1.45, .9), ("tt", 0, 1.45, .85)]
expected = {(c, t, v, f, r, g) for c, t, v, f in points for r in trim_factors for g in [0, 31]}
frames, audits = [], {}
for sheet in sorted((project / "datasheets/endpoints").glob("*.yaml")):
    out = project / "out" / sheet.stem
    audits[sheet.name] = audit(sheet, out, False)
    data = pd.read_csv(out / "simulation_results.csv")
    for key, allowed in yaml.safe_load(sheet.read_text())["parameters"].items():
        if allowed == "range(1)":
            allowed = [0]
        assert isinstance(allowed, list) and set(data[key]) == set(allowed), (sheet, key)
    frames.append(data)
data = pd.concat(frames, ignore_index=True)
keys = ["corner_mos", "temp", "vdd", "bias_factor", "rtrim_scale", "gcode"]
assert len(data) == len(expected) and set(map(tuple, data[keys].to_numpy())) == expected
for key, value in {"pair_scale": 2/3, "power_m": 6, "rbase_scale": .8,
                   "trim_family": "2p85", "load_family": "1p41", "replica_tracks_signal": 0}.items():
    assert data[key].eq(value).all(), key
if args.trim_range:
    control_keys = [key for key in keys if key != "rtrim_scale"]
    prior = pd.read_csv(evidence / "sky_input2_pair_endpoints.csv").set_index(control_keys)
    control = data[data.rtrim_scale == 1.4]
    assert len(control) == 20
else:
    control_keys = ["gcode"]
    prior = pd.read_csv(evidence / "sky_input2_pair_calibration.csv").set_index(control_keys)
    control = data[(data.corner_mos == "ss") & (data.temp == 27) & (data.vdd == 1.5)]
    assert len(control) == 2
for _, row in control.iterrows():
    key = tuple(row[k] for k in control_keys) if len(control_keys) > 1 else row.gcode
    for metric in ["k100", "k10", "compr", "idd", "tail_gate_v", "tail_ratio"]:
        assert np.isclose(row[metric], prior.loc[key, metric], rtol=1e-5, atol=1e-12), (key, metric)
records = []
for key, group in data.groupby(keys[:-1]):
    low, high = group.k100.abs().min(), group.k100.abs().max()
    records.append(dict(zip(keys[:-1], key), gain_min=float(low), gain_max=float(high),
                        endpoint_span_brackets_target=bool(low <= 10 <= high),
                        endpoint_span_overlaps_gain_window=bool(low <= 10.1 and high >= 9.9)))
summary = {"audits": audits, "control_replay": "pass", "unchanged_controls": len(control),
           "endpoint_diagnostics": records, "full_spec_coverage": "unverified",
           "gain_tolerance_percent": 1, "gain_tolerance_status": "provisional",
           "scope": "ten-point endpoint diagnostic, each trim factor evaluated globally with the smaller pair"}
summary["target_brackets_by_trim_factor"] = {
    str(r): sum(x["endpoint_span_brackets_target"] for x in records if x["rtrim_scale"] == r)
    for r in trim_factors
}
stem = evidence / name
data.to_csv(stem.with_suffix(".csv"), index=False)
stem.with_name(stem.name + "_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
print(pd.DataFrame(records).to_string(index=False))

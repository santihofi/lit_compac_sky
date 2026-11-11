#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Audit refinement or resistor endpoints without treating endpoint span as coverage."""
import argparse
import itertools
import json
from pathlib import Path
import numpy as np
import pandas as pd
import yaml
from check_chipify_results import audit

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("study", choices=["refine", "range"])
args = parser.parse_args()
evidence = ROOT / "doc/porting/evidence"
project = ROOT / f"verification/porting/sky_input2_quiet_{args.study}"
folder = "refine" if args.study == "refine" else "endpoints"
bias = pd.read_csv(evidence / "sky_quiet_bias_sensitivity.csv")
baseline = pd.read_csv(evidence / "sky_quiet_codes_pvt.csv")
baseline["bias_factor"] = 1.0
controls = pd.concat([bias, baseline], ignore_index=True)
keys = ["corner_mos", "temp", "vdd", "gcode", "bias_factor", "rbase_scale", "rtrim_scale"]
if args.study == "refine":
    expected = set()
    for corner, temp, vdd, codes, factors in [
        ("fs", 27, 1.65, [25, 26, 27, 28], [0.8, 0.9]),
        ("tt", 0, 1.5, [0, 1], [0.83, 0.85, 0.87]),
    ]:
        expected.update((corner, temp, vdd, c, f, 1., 1.) for c, f in itertools.product(codes, factors))
else:
    points = [(c, 27, 1.5, 1.) for c in ["ff", "fs", "sf", "ss", "tt"]]
    points += [("fs", 80, v, .9) for v in [1.45, 1.5, 1.65]]
    points += [("ss", 80, 1.45, .9), ("tt", 0, 1.45, .9)]
    expected = {(c, t, v, g, f, rb, rt) for c, t, v, f in points
                for g, rb, rt in itertools.product([0, 31], [.8, .9, 1.], [1., 1.2, 1.4])}
frames, audits, replayed = [], {}, 0
for sheet in sorted((project / "datasheets" / folder).glob("*.yaml")):
    out = project / "out" / sheet.stem
    audits[sheet.name] = audit(sheet, out, False)
    frame = pd.read_csv(out / "simulation_results.csv")
    params = yaml.safe_load(sheet.read_text())["parameters"]
    for name, values in params.items():
        if values == "range(1)":
            values = [0]
        assert isinstance(values, list) and set(frame[name]) == set(values), (sheet, name)
    for _, row in frame.iterrows():
        match = pd.Series(True, index=controls.index)
        for key in keys:
            match &= controls[key].eq(row[key])
        prior = controls[match]
        if len(prior):
            for metric in ["k100", "k10", "compr", "idd", "tail_gate_v", "tail_ratio"]:
                assert np.allclose(prior[metric], row[metric], rtol=1e-5, atol=1e-12), (sheet, metric)
            replayed += 1
    frames.append(frame)
data = pd.concat(frames, ignore_index=True)
assert len(data) == len(expected) and set(map(tuple, data[keys].to_numpy())) == expected
assert replayed == (2 if args.study == "refine" else 20), replayed
data["gain_error_percent"] = 100 * (data.k100.abs() / 10 - 1)
data["dc_screen_pass"] = (data.gain_error_percent.abs().le(1) &
                         data.compr.between(.96758, 1.03242) &
                         data.tail_gate_v.between(0, data.vdd))
summary = {"audits": audits, "cases": len(data), "replayed_controls": replayed,
           "gain_tolerance_percent": 1, "gain_tolerance_status": "provisional",
           "full_spec_coverage": "unverified"}
if args.study == "range":
    records = []
    for key, group in data.groupby(["corner_mos", "temp", "vdd", "bias_factor", "rbase_scale", "rtrim_scale"]):
        low, high = group.k100.abs().min(), group.k100.abs().max()
        records.append(dict(zip(["corner_mos", "temp", "vdd", "bias_factor", "rbase_scale", "rtrim_scale"], key),
                            gain_min=float(low), gain_max=float(high),
                            endpoint_span_overlaps_gain_window=bool(low <= 10.1 and high >= 9.9),
                            endpoint_span_brackets_target=bool(low <= 10 and high >= 10)))
    summary["endpoint_diagnostics"] = records
    print(pd.DataFrame(records).groupby(["rbase_scale", "rtrim_scale"])[
        ["endpoint_span_overlaps_gain_window", "endpoint_span_brackets_target"]].sum().to_string())
else:
    summary["sampled_feasible_settings"] = data.loc[data.dc_screen_pass,
        keys + ["gain_error_percent", "compr"]].to_dict("records")
    print(json.dumps(summary["sampled_feasible_settings"], indent=2))
stem = evidence / f"sky_quiet_{args.study}"
data.to_csv(stem.with_suffix(".csv"), index=False)
stem.with_name(stem.name + "_summary.json").write_text(json.dumps(summary, indent=2) + "\n")

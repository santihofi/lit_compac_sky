#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Audit sparse bias sensitivity with an unchanged-current replay at every point."""
import json
from pathlib import Path
import numpy as np
import pandas as pd
import yaml
from check_chipify_results import audit

ROOT = Path(__file__).resolve().parents[1]
evidence = ROOT / "doc/porting/evidence"
project = ROOT / "verification/porting/sky_input2_quiet_bias"
baseline = pd.read_csv(evidence / "sky_quiet_codes_pvt.csv")
coverage = json.loads((evidence / "sky_quiet_codes_pvt_summary.json").read_text())["coverage"]
expected = {(x["corner_mos"], x["temp"], x["vdd"]) for x in coverage if not x["dc_covered"]}
expected_cases = {
    (x["corner_mos"], x["temp"], x["vdd"], code, factor)
    for x in coverage if not x["dc_covered"]
    for code in {0, x["nearest_gain_code"], 31}
    for factor in [0.8, 0.9, 1.0, 1.1, 1.2]
}
frames, audits = [], {}
for sheet in sorted((project / "datasheets/sensitivity").glob("*.yaml")):
    out = project / "out" / sheet.stem
    audits[sheet.name] = audit(sheet, out, False)
    frame = pd.read_csv(out / "simulation_results.csv")
    for name, values in yaml.safe_load(sheet.read_text())["parameters"].items():
        if values == "range(1)":
            values = [0]
        if not isinstance(values, list) or set(frame[name]) != set(values):
            raise ValueError(f"{sheet.name}: parameter mismatch {name}")
    if frame.duplicated(["corner_mos", "temp", "vdd", "gcode", "bias_factor"]).any():
        raise ValueError(f"{sheet.name}: duplicate cases")
    for _, row in frame[frame.bias_factor == 1].iterrows():
        control = baseline[(baseline.corner_mos == row.corner_mos) &
                           (baseline.temp == row.temp) & (baseline.vdd == row.vdd) &
                           (baseline.gcode == row.gcode)]
        assert len(control) == 1
        for metric in ["k100", "k10", "compr", "idd", "tail_gate_v", "tail_ratio"]:
            assert np.isclose(row[metric], control.iloc[0][metric], rtol=1e-5, atol=1e-12), (sheet, metric)
    frames.append(frame)
data = pd.concat(frames, ignore_index=True)
actual = set(map(tuple, data[["corner_mos", "temp", "vdd"]].drop_duplicates().to_numpy()))
assert actual == expected and len(frames) == len(expected)
case_columns = ["corner_mos", "temp", "vdd", "gcode", "bias_factor"]
assert set(map(tuple, data[case_columns].to_numpy())) == expected_cases
assert len(data) == len(expected_cases)
assert len(data[data.bias_factor == 1]) == sum(x[-1] == 1 for x in expected_cases)
data["gain_error_percent"] = 100 * (data.k100.abs() / 10 - 1)
data["dc_screen_pass"] = (data.gain_error_percent.abs().le(1) &
                         data.compr.between(.96758, 1.03242) &
                         data.tail_gate_v.between(0, data.vdd))
stem = evidence / "sky_quiet_bias_sensitivity"
data.to_csv(stem.with_suffix(".csv"), index=False)
report = {"audits": audits, "control_replay": "pass", "gain_tolerance_percent": 1,
          "gain_tolerance_status": "provisional", "scope": "sparse bias sensitivity, not exhaustive calibration",
          "cases": len(data), "sampled_feasible_settings": data.loc[data.dc_screen_pass,
              ["corner_mos", "temp", "vdd", "gcode", "bias_factor", "gain_error_percent", "compr"]].to_dict("records")}
stem.with_name(stem.name + "_summary.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report["sampled_feasible_settings"], indent=2))

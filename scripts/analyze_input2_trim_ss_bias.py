#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Audit all gain codes at sampled SS currents and preserve same-setting feasibility."""
import itertools
import json
from pathlib import Path
import numpy as np
import pandas as pd
import yaml
from check_chipify_results import audit

ROOT = Path(__file__).resolve().parents[1]
evidence = ROOT / "doc/porting/evidence"
project = ROOT / "verification/porting/sky_input2_trim_ss_bias"
sheet, out = project / "datasheets/ss_bias.yaml", project / "out"
report = audit(sheet, out, False)
data = pd.read_csv(out / "simulation_results.csv")
params = yaml.safe_load(sheet.read_text())["parameters"]
for key, allowed in params.items():
    if allowed == "range(1)":
        allowed = [0]
    assert isinstance(allowed, list) and set(data[key]) == set(allowed), key
expected = set(itertools.product(range(32), [.8, .9, 1., 1.1, 1.2]))
assert len(data) == 160 and set(map(tuple, data[["gcode", "bias_factor"]].to_numpy())) == expected
prior = pd.read_csv(evidence / "sky_quiet_trim_corners.csv")
prior = prior[(prior.corner_mos == "ss") & (prior.trim_family == "2p85")]
assert len(prior) == 2
for key in params:
    if key not in {"gcode", "bias_factor"}:
        assert data[key].eq(prior.iloc[0][key]).all(), key
for _, previous in prior.iterrows():
    control = data[(data.gcode == previous.gcode) & (data.bias_factor == 1.)]
    assert len(control) == 1
    for metric in ["k100", "k10", "compr", "idd", "tail_gate_v", "tail_ratio"]:
        assert np.isclose(control.iloc[0][metric], previous[metric], rtol=1e-5, atol=1e-12), metric
data["gain_error_percent"] = 100 * (data.k100.abs() / 10 - 1)
data["dc_screen_pass"] = (data.gain_error_percent.abs().le(1) &
                         data.compr.between(.96758, 1.03242) &
                         data.tail_gate_v.between(0, data.vdd))
coverage = []
for factor, group in data.groupby("bias_factor"):
    assert sorted(group.gcode) == list(range(32))
    coverage.append({"bias_factor": float(factor),
                     "dc_feasible_codes": sorted(map(int, group.loc[group.dc_screen_pass, "gcode"]))})
report.update(coverage=coverage, control_replay="pass", unchanged_controls=2,
              gain_tolerance_percent=1, gain_tolerance_status="provisional",
              full_spec_coverage="unverified",
              scope="SS 27 C 1.5 V, sampled ideal currents, gain/shape screen only")
stem = evidence / "sky_trim_ss_bias"
data.to_csv(stem.with_suffix(".csv"), index=False)
stem.with_name(stem.name + "_summary.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(coverage, indent=2))

#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Compare one in-simulator code sweep with 32 independent operating-point runs."""
import json
from pathlib import Path

import numpy as np
import pandas as pd

from check_chipify_results import audit

ROOT = Path(__file__).resolve().parents[1]
project = ROOT / "verification/porting/sky_gain_dc_sweep"
out = project / "out"
integrity = audit(project / "datasheets/control.yaml", out)
meta = json.loads(max((out / "history").glob("*.meta.json"),
                     key=lambda p: p.stat().st_mtime).read_text())
data = pd.read_csv(out / "simulation_results.csv", dtype={"run_id": str})
if len(data) != 1:
    raise ValueError("Expected the single typical-corner control")
row = data.iloc[0]
wave = pd.read_csv(out / meta["analysis_dirs"]["dc"] / ("run_" + row.run_id + "__code_curve.csv"))
if not np.array_equal(wave.sweep.to_numpy(), np.arange(32)):
    raise ValueError("Wrong code axis")
reference = pd.read_csv(ROOT / "doc/porting/evidence/sky_centered_gain_calibration.csv")
reference = reference[reference.corner_mos == "tt"].sort_values("gcode")
report = {"audit": integrity, "code_points": len(wave), "maximum_relative_differences": {}}
for metric, signal in [("k100", "dc8.k100_curve"), ("k10", "dc8.k10_curve"),
                       ("compr", "dc8.compr_curve")]:
    measured = wave[signal].to_numpy()
    expected = reference[metric].to_numpy()
    if not np.allclose(measured, expected, rtol=6e-6, atol=1e-6):
        raise ValueError(f"DC continuation differs from independent points for {metric}")
    report["maximum_relative_differences"][metric] = float(np.max(abs(measured/expected-1)))
    if metric != "compr":
        for index, suffix in [(0, "first"), (-1, "last")]:
            if not np.isclose(measured[index], row[metric + "_" + suffix], rtol=6e-6):
                raise ValueError("Endpoint scalar/capture mismatch")
evidence = ROOT / "doc/porting/evidence"
wave.to_csv(evidence / "sky_gain_dc_sweep_control.csv", index=False)
(evidence / "sky_gain_dc_sweep_control_audit.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report, indent=2))

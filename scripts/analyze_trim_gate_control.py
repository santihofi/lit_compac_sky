#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Audit the independent trim-rail control and its unchanged-rail anchors."""
import json
from pathlib import Path

import numpy as np
import pandas as pd

from check_chipify_results import audit
from check_core_ac_capture import check_curve

ROOT = Path(__file__).resolve().parents[1]
evidence = ROOT / "doc/porting/evidence"
for kind in ["dc", "ac"]:
    project = ROOT / "verification/porting" / ("sky_trim_gate_" + kind)
    out = project / "out"
    result = audit(project / "datasheets/control.yaml", out, False)
    data = pd.read_csv(out / "simulation_results.csv", dtype={"run_id": str})
    if len(data) != 6 or data.duplicated(["temp", "trim_high"]).any():
        raise ValueError("Expected six distinct gate-rail controls")
    if kind == "ac":
        meta = json.loads(max((out / "history").glob("*.meta.json"),
                             key=lambda p: p.stat().st_mtime).read_text())
        waves = {}
        for _, row in data.iterrows():
            wave = pd.read_csv(out / meta["analysis_dirs"]["ac"] / ("run_" + row.run_id + "__ac.csv"))
            for number in [1, 2]:
                check_curve(wave, f"ac{number}.gd", row[f"acgain_in{number}"],
                            row[f"bw_in{number}_mhz"])
            waves[row.run_id] = wave.to_numpy()
            waves["columns"] = wave.columns.to_numpy(dtype=str)
        np.savez_compressed(evidence / ("sky_trim_gate_ac_waveforms.npz"), **waves)
        result["anchored_curves"] = 2 * len(data)
    reference = pd.read_csv(evidence / ("sky_centered_" + kind + ".csv"))
    reference = reference[(reference.corner_mos == "sf") & (reference.vdd == 1.45)]
    fields = ["k100", "k10", "compr"] if kind == "dc" else ["bw_in1_mhz", "bw_in2_mhz"]
    maximum_anchor_error = 0.0
    for _, row in data[data.trim_high == 1.45].iterrows():
        original = reference[reference.temp == row.temp].iloc[0]
        relative_error = float(abs(row[fields].astype(float) / original[fields].astype(float) - 1).max())
        maximum_anchor_error = max(maximum_anchor_error, relative_error)
        if not np.allclose(row[fields].astype(float), original[fields].astype(float), rtol=1e-5):
            raise ValueError("The unchanged-rail control differs from calibrated PVT")
    result["unchanged_rail_cases_reproduced"] = 2
    result["maximum_unchanged_rail_relative_difference"] = maximum_anchor_error
    data.to_csv(evidence / ("sky_trim_gate_" + kind + ".csv"), index=False)
    (evidence / ("sky_trim_gate_" + kind + "_audit.json")).write_text(json.dumps(result, indent=2) + "\n")
    print(data[["temp", "trim_high"] + fields].sort_values(["temp", "trim_high"]).to_string(index=False))

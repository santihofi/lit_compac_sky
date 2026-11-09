#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Audit common-mode replica bias against unchanged bare and loaded controls."""
import json
from pathlib import Path
import numpy as np
import pandas as pd
from check_chipify_results import audit
from check_core_ac_capture import check_curve

ROOT = Path(__file__).resolve().parents[1]
evidence = ROOT / "doc/porting/evidence"
project = ROOT / "verification/porting/sky_input2_quiet_replica"
out = project / "out"
report = audit(project / "datasheets/quiet_fs.yaml", out, False)
data = pd.read_csv(out / "simulation_results.csv", dtype={"run_id": str}).copy()
if len(data) != 2 or set(data.replica_tracks_signal) != {0, 1}:
    raise ValueError("Expected signal-tracking and common-mode reference cases")
for key, value in {"corner_mos": "fs", "temp": 27, "vdd": 1.5, "power_m": 6, "gcode": 29}.items():
    if not data[key].eq(value).all():
        raise ValueError(f"Unexpected {key}")
meta = json.loads(max((out / "history").glob("*.meta.json"), key=lambda p: p.stat().st_mtime).read_text())
directory = Path(meta["analysis_dirs"]["ac"])
if not directory.is_absolute():
    directory = out / directory
waves = {}
for _, row in data.iterrows():
    for tb, prefix in [("ac", ""), ("fanout", "loaded_")]:
        wave = pd.read_csv(directory / f"run_{row.run_id}__{tb}.csv")
        for n in [1, 2]:
            check_curve(wave, f"ac{n}.gd", row[f"{prefix}acgain_in{n}"], row[f"{prefix}bw_in{n}_mhz"])
        waves[f"{tb}_{row.run_id}"] = wave.to_numpy()
        waves["columns"] = wave.columns.to_numpy(dtype=str)
control = data[data.replica_tracks_signal == 1].iloc[0]
bare = pd.read_csv(evidence / "sky_input2_candidate_nominal6.csv")
bare = bare[bare.corner_mos == "fs"].iloc[0]
loaded = pd.read_csv(evidence / "sky_input2_fanout6.csv")
loaded = loaded[(loaded.power_m == 6) & (loaded.fanout_input == 1) & (loaded.c_load == "25f")].iloc[0]
checks = {}
for previous, prefix, metrics in [
    (bare, "", ["k100", "compr", "idd", "bw_in1_mhz", "bw_in2_mhz", "cin1_per_pin_ff", "cin2_per_pin_ff"]),
    (loaded, "loaded_", ["bw_in1_mhz", "bw_in2_mhz", "acgain_in1", "acgain_in2"]),
]:
    for metric in metrics:
        actual = float(control[prefix + metric])
        if not np.isclose(actual, previous[metric], rtol=1e-5, atol=1e-12):
            raise ValueError(f"Unchanged replica control differs: {prefix}{metric}")
        checks[prefix + metric] = actual
ihp = pd.read_csv(evidence / "ihp_input2_fanout6.csv")
ihp = ihp[(ihp.fanout_input == 1) & (ihp.c_load == "25f")].iloc[0]
data["gain_error_percent"] = 100 * (data.k100.abs() / 10 - 1)
data["shape_pass"] = data.compr.between(.96758, 1.03242)
for n in [1, 2]:
    data[f"loaded_bw{n}_ratio_ihp"] = data[f"loaded_bw_in{n}_mhz"] / ihp[f"bw_in{n}_mhz"]
data["joint_dc_loaded_bw_screen"] = (
    data.gain_error_percent.abs().le(1) & data.shape_pass & data.tail_gate_v.between(0, 1.5)
    & data.loaded_bw1_ratio_ihp.ge(1) & data.loaded_bw2_ratio_ihp.ge(1))
report.update(anchored_curves=8, unchanged_controls=checks,
              gain_tolerance_percent=1, gain_tolerance_status="provisional",
              full_spec_coverage="unverified")
data.to_csv(evidence / "sky_input2_quiet_replica.csv", index=False)
np.savez_compressed(evidence / "sky_input2_quiet_replica_waveforms.npz", **waves)
(evidence / "sky_input2_quiet_replica_audit.json").write_text(json.dumps(report, indent=2) + "\n")
print(data[["replica_tracks_signal", "k100", "compr", "axis1", "axis2", "cin1_per_pin_ff",
            "bw_in2_mhz", "loaded_bw_in2_mhz", "loaded_bw2_ratio_ihp", "idd",
            "joint_dc_loaded_bw_screen"]].to_string(index=False))

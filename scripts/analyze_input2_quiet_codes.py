#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Choose an SS code by joint gain, shape and bandwidth, preserving the replay control."""
import json
from pathlib import Path
import numpy as np
import pandas as pd
from check_chipify_results import audit
from check_core_ac_capture import check_curve

ROOT = Path(__file__).resolve().parents[1]
evidence = ROOT / "doc/porting/evidence"
project = ROOT / "verification/porting/sky_input2_quiet_replica"
sheet = project / "datasheets/codes/quiet_ss_codes.yaml"
out = project / "out/quiet_ss_codes"
report = audit(sheet, out, False)
data = pd.read_csv(out / "simulation_results.csv", dtype={"run_id": str}).copy()
if len(data) != 3 or sorted(data.gcode) != [14, 15, 16]:
    raise ValueError("Expected SS codes 14, 15 and 16 exactly once")
for key, value in {"corner_mos": "ss", "temp": 27, "vdd": 1.5, "power_m": 6, "replica_tracks_signal": 0}.items():
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
parent = pd.read_csv(evidence / "input2_quiet_corners_matched.csv")
reference = parent[parent.corner_mos == "ss"].iloc[0]
control = data[data.gcode == 15].iloc[0]
for metric in ["k100", "compr", "idd", "bw_in1_mhz", "bw_in2_mhz",
               "loaded_bw_in1_mhz", "loaded_bw_in2_mhz"]:
    if not np.isclose(control[metric], reference[metric], rtol=1e-5, atol=1e-12):
        raise ValueError(f"SS code-15 replay differs: {metric}")
data["gain_error_percent"] = 100 * (data.k100.abs() / 10 - 1)
data["shape_pass"] = data.compr.between(.96758, 1.03242)
data["matched_corner"] = "ss"
for key in [c for c in parent.columns if c.startswith("ihp_")]:
    data[key] = reference[key]
speed_pass = pd.Series(True, index=data.index)
for n in [1, 2]:
    data[f"bare_bw{n}_ratio_ihp"] = data[f"bw_in{n}_mhz"] / data[f"ihp_bw_in{n}_mhz_bare"]
    data[f"loaded_bw{n}_ratio_ihp"] = data[f"loaded_bw_in{n}_mhz"] / data[f"ihp_bw_in{n}_mhz"]
    speed_pass &= data[f"bare_bw{n}_ratio_ihp"].ge(1) & data[f"loaded_bw{n}_ratio_ihp"].ge(1)
data["joint_dc_bare_loaded_bw_screen"] = (
    data.gain_error_percent.abs().le(1) & data.shape_pass
    & data.tail_gate_v.ge(0) & data.tail_gate_v.le(data.vdd) & speed_pass)
feasible = data[data.joint_dc_bare_loaded_bw_screen]
report.update(anchored_curves=12, unchanged_code15_control="pass",
              feasible_ss_codes=sorted(map(int, feasible.gcode)),
              gain_tolerance_percent=1, gain_tolerance_status="provisional",
              full_spec_coverage="unverified")
selection_path = evidence / "input2_quiet_selected_nominal.csv"
selection_path.unlink(missing_ok=True)
if len(feasible):
    selected = feasible.loc[feasible.gain_error_percent.abs().idxmin()]
    selected_set = pd.concat([parent[parent.corner_mos != "ss"], selected.to_frame().T], ignore_index=True)
    selected_set.to_csv(evidence / "input2_quiet_selected_nominal.csv", index=False)
    report["selected_ss_code"] = int(selected.gcode)
    report["joint_nominal_passes"] = int(selected_set.joint_dc_bare_loaded_bw_screen.sum())
data.to_csv(evidence / "sky_input2_quiet_ss_codes.csv", index=False)
np.savez_compressed(evidence / "sky_input2_quiet_ss_codes_waveforms.npz", **waves)
(evidence / "sky_input2_quiet_ss_codes_audit.json").write_text(json.dumps(report, indent=2) + "\n")
print(data[["gcode", "gain_error_percent", "compr", "bw_in2_mhz", "loaded_bw_in2_mhz",
            "loaded_bw2_ratio_ihp", "joint_dc_bare_loaded_bw_screen"]].sort_values("gcode").to_string(index=False))

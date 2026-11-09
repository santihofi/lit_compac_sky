#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Audit the input-2 sensitivity study, including replay of its unchanged control."""
import argparse
import json
from itertools import product
from pathlib import Path
import numpy as np
import pandas as pd
from check_chipify_results import audit
from check_core_ac_capture import check_curve

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--study", choices=["width", "loads", "parallel"], default="width")
args = parser.parse_args()
name, sheet = {
    "width": ("sky_input2_speed", "speed_fs.yaml"),
    "loads": ("sky_input2_load_resistors", "load_fs.yaml"),
    "parallel": ("sky_input2_parallel", "parallel_fs.yaml"),
}[args.study]
project = ROOT / "verification/porting" / name
out = project / "out"
evidence = ROOT / "doc/porting/evidence"
result = audit(project / "datasheets" / sheet, out, False)
data = pd.read_csv(out / "simulation_results.csv", dtype={"run_id": str})
if args.study == "width":
    if len(data) != 9 or data.duplicated(["quad_scale", "ibias"]).any():
        raise ValueError("Expected nine distinct width/current cases")
    if set(zip(data.quad_scale, data.ibias)) != set(product([.5, 1, 2], [27.5e-6, 35e-6, 45e-6])):
        raise ValueError("Unexpected width/current grid")
elif args.study == "loads":
    if len(data) != 3 or set(data.load_family) != {"5p73", "2p85", "1p41"}:
        raise ValueError("Expected all three load families")
    if not (data.quad_scale.eq(1) & data.ibias.eq(27.5e-6)).all():
        raise ValueError("Load study changed width or current")
else:
    if len(data) != 3 or set(data.power_m) != {2, 4, 6}:
        raise ValueError("Expected two, four and six copies")
    if not (data.quad_scale.eq(1) & data.ibias.eq(27.5e-6) & data.load_family.eq("1p41")).all():
        raise ValueError("Parallel study changed another sizing parameter")
for key, value in {"corner_mos": "fs", "temp": 27, "vdd": 1.5, "gcode": 29}.items():
    if not data[key].eq(value).all():
        raise ValueError(f"Unexpected {key}")
meta = json.loads(max((out / "history").glob("*.meta.json"), key=lambda p: p.stat().st_mtime).read_text())
folder = Path(meta["analysis_dirs"]["ac"])
if not folder.is_absolute():
    folder = out / folder
waves = {}
for _, row in data.iterrows():
    wave = pd.read_csv(folder / f"run_{row.run_id}__ac.csv")
    for number in [1, 2]:
        check_curve(wave, f"ac{number}.gd", row[f"acgain_in{number}"], row[f"bw_in{number}_mhz"])
    waves["run_" + row.run_id] = wave.to_numpy()
    waves["columns"] = wave.columns.to_numpy(dtype=str)
baseline = (data[(data.quad_scale == 1) & (data.ibias == 27.5e-6)]
            if args.study == "width" else
            data[data.load_family == "5p73"] if args.study == "loads" else
            data[data.power_m == 2]).iloc[0]
old_dc = pd.read_csv(evidence / "sky_tg2_codes_nominal.csv")
old_ac = pd.read_csv(evidence / "sky_tg2_feasible_ac.csv")
checks = {}
for previous, metrics in [(old_dc, ["k100", "compr", "idd"]),
                          (old_ac, ["bw_in1_mhz", "bw_in2_mhz", "cin2_per_pin_ff"])]:
    if args.study == "parallel":
        previous = pd.read_csv(evidence / "sky_input2_load_resistors.csv")
        reference = previous[previous.load_family == "1p41"].iloc[0]
    else:
        reference = previous[(previous.corner_mos == "fs") & (previous.gcode == 29)].iloc[0]
    for metric in metrics:
        if not np.isclose(baseline[metric], reference[metric], rtol=1e-5, atol=1e-12):
            raise ValueError(f"Unchanged-control replay failed: {metric}")
        checks[metric] = float(baseline[metric])
data["gain_error_percent"] = 100 * (data.k100.abs() / 10 - 1)
data["shape_pass"] = data.compr.between(.96758, 1.03242)
data["bw2_relative_to_control"] = data.bw_in2_mhz / baseline.bw_in2_mhz
data["current_relative_to_control"] = data.idd / baseline.idd
reference = pd.read_csv(evidence / "ihp_calibrated_pvt.csv")
reference = reference[(reference.corner_mos == "sf") & (reference.temp == 27) & (reference.vdd == 1.5)].iloc[0]
for number in [1, 2]:
    data[f"bw{number}_ratio_ihp"] = data[f"bw_in{number}_mhz"] / reference[f"bw_in{number}_mhz"]
data["joint_dc_bw_screen"] = (data.gain_error_percent.abs().le(1) & data.shape_pass
                             & data.tail_gate_v.between(0, 1.5)
                             & data.bw1_ratio_ihp.ge(1) & data.bw2_ratio_ihp.ge(1))
if args.study == "parallel":
    if not np.allclose(data.k100, baseline.k100, rtol=1e-5):
        raise ValueError("Parallel copies changed nominal DC gain")
    if not np.allclose(data.idd / baseline.idd, data.power_m / 2, rtol=1e-5):
        raise ValueError("Parallel current did not scale as expected")
data.to_csv(evidence / (name + ".csv"), index=False)
np.savez_compressed(evidence / (name + "_waveforms.npz"), **waves)
result.update(anchored_curves=2 * len(data), unchanged_control=checks,
              scope="Fixed-code sensitivity only, not gain-calibrated acceptance")
(evidence / (name + "_audit.json")).write_text(json.dumps(result, indent=2) + "\n")
axes = ["quad_scale", "ibias"] if args.study == "width" else ["load_family"] if args.study == "loads" else ["power_m"]
print(data[axes + ["k100", "compr", "axis1", "axis2", "bw_in1_mhz",
                  "bw_in2_mhz", "cin2_per_pin_ff", "idd", "shape_pass", "joint_dc_bw_screen"]].sort_values(axes).to_string(index=False))

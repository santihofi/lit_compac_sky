#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Audit release replay and five-corner joint DC/bandwidth coverage."""
import argparse
import importlib.metadata
import json
from pathlib import Path
import numpy as np
import pandas as pd
import yaml
from check_chipify_results import audit
from check_core_ac_capture import check_curve

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--control", action="store_true")
parser.add_argument("--copies", type=int, choices=[5, 6], default=6)
args = parser.parse_args()
project = ROOT / "verification/porting/sky_input2_candidate"
evidence = ROOT / "doc/porting/evidence"
phase = "control" if args.control else "nominal" if args.copies == 5 else "nominal6"
parts, audits, waves = [], {}, {}
for sheet in sorted((project / "datasheets" / phase).glob("*.yaml")):
    out = project / "out" / sheet.stem
    audits[sheet.stem] = audit(sheet, out, False)
    data = pd.read_csv(out / "simulation_results.csv", dtype={"run_id": str})
    params = yaml.safe_load(sheet.read_text())["parameters"]
    for key in ["corner_mos", "gcode", "power_m", "ibias", "temp", "vdd", "load_family"]:
        if set(data[key]) != set(params[key]):
            raise ValueError(f"Unexpected {key} in {sheet}")
    meta = json.loads(max((out / "history").glob("*.meta.json"), key=lambda p: p.stat().st_mtime).read_text())
    directory = Path(meta["analysis_dirs"]["ac"])
    if not directory.is_absolute():
        directory = out / directory
    for _, row in data.iterrows():
        wave = pd.read_csv(directory / f"run_{row.run_id}__ac.csv")
        for number in [1, 2]:
            check_curve(wave, f"ac{number}.gd", row[f"acgain_in{number}"], row[f"bw_in{number}_mhz"])
        waves[sheet.stem + "_" + row.run_id] = wave.to_numpy()
        waves["columns"] = wave.columns.to_numpy(dtype=str)
    parts.append(data)
data = pd.concat(parts, ignore_index=True)
report = {"audits": audits, "package_version": importlib.metadata.version("chipify")}
if args.control:
    if len(data) != 1:
        raise ValueError("Expected one release replay")
    previous = pd.read_csv(evidence / "sky_input2_load_resistors.csv")
    previous = previous[previous.load_family == "1p41"].iloc[0]
    checks = {}
    for metric in ["k100", "k10", "compr", "axis1", "axis2", "idd",
                   "bw_in1_mhz", "bw_in2_mhz", "cin1_per_pin_ff", "cin2_per_pin_ff"]:
        actual = float(data.iloc[0][metric])
        if not np.isclose(actual, previous[metric], rtol=1e-5, atol=1e-12):
            raise ValueError(f"Release replay differs: {metric}")
        checks[metric] = actual
    report["unchanged_release_control"] = checks
else:
    if len(data) != 5 or set(data.corner_mos) != {"tt", "ff", "fs", "sf", "ss"}:
        raise ValueError("Expected five distinct nominal MOS corners")
    reference = pd.read_csv(evidence / "ihp_calibrated_pvt.csv")
    reference = reference[(reference.temp == 27) & (reference.vdd == 1.5)].copy()
    reference["corner_mos"] = reference.corner_mos.replace({"fs": "sf", "sf": "fs"})
    data = data.merge(reference[["corner_mos", "bw_in1_mhz", "bw_in2_mhz"]],
                      on="corner_mos", validate="one_to_one", suffixes=("", "_ihp"))
    data["gain_error_percent"] = 100 * (data.k100.abs() / 10 - 1)
    data["shape_pass"] = data.compr.between(.96758, 1.03242)
    for number in [1, 2]:
        data[f"bw{number}_ratio_ihp"] = data[f"bw_in{number}_mhz"] / data[f"bw_in{number}_mhz_ihp"]
    data["joint_dc_bw_screen"] = (data.gain_error_percent.abs().le(1) & data.shape_pass
                                 & data.tail_gate_v.between(0, 1.5)
                                 & data.bw1_ratio_ihp.ge(1) & data.bw2_ratio_ihp.ge(1))
    report["joint_dc_bw_passes"] = int(data.joint_dc_bw_screen.sum())
    report["gain_tolerance_percent"] = 1
    report["gain_tolerance_status"] = "provisional"
    report["full_spec_coverage"] = "unverified"
    report["replica_finger_counts_integral"] = bool(np.allclose(
        12 * data.pair_scale * data.power_m / 8,
        np.round(12 * data.pair_scale * data.power_m / 8)))
    if not report["replica_finger_counts_integral"]:
        report["physical_candidate_status"] = "diagnostic only, replica finger truncation invalidates exact-copy geometry"
prefix = "sky_input2_candidate_" + ("control" if args.control else f"nominal{args.copies}")
data.to_csv(evidence / (prefix + ".csv"), index=False)
np.savez_compressed(evidence / (prefix + "_waveforms.npz"), **waves)
(evidence / (prefix + "_audit.json")).write_text(json.dumps(report, indent=2) + "\n")
columns = ["corner_mos", "gcode", "power_m", "k100", "compr", "bw_in1_mhz",
           "bw_in2_mhz", "cin1_per_pin_ff", "cin2_per_pin_ff", "idd"]
if not args.control:
    columns += ["bw2_ratio_ihp", "joint_dc_bw_screen"]
print(data[columns].to_string(index=False))

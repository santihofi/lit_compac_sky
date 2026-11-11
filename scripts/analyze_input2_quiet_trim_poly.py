#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Audit the trim-poly speed control against the unchanged widened-network cases."""
import argparse
import json
from pathlib import Path
import numpy as np
import pandas as pd
import yaml
from check_chipify_results import audit
from check_core_ac_capture import check_curve

ROOT = Path(__file__).resolve().parents[1]
evidence = ROOT / "doc/porting/evidence"
project = ROOT / "verification/porting/sky_input2_quiet_trim_poly"
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--corners", action="store_true")
args = parser.parse_args()
baseline = pd.read_csv(evidence / "sky_quiet_range14_ac.csv")
if not args.corners:
    baseline = baseline[baseline.corner_mos == "fs"]
expected = {(r.corner_mos, int(r.gcode), family) for _, r in baseline.iterrows()
            for family in ["5p73", "2p85"]}
baseline = baseline.set_index(["corner_mos", "gcode"], drop=False)
sheets = (sorted((project / "datasheets/corners").glob("*.yaml")) if args.corners
          else [project / "datasheets/trim_fs.yaml"])
frames, audits, waves = [], {}, {}
for sheet in sheets:
    out = project / "out" / sheet.stem if args.corners else project / "out"
    audits[sheet.name] = audit(sheet, out, False)
    frame = pd.read_csv(out / "simulation_results.csv", dtype={"run_id": str}).copy()
    params = yaml.safe_load(sheet.read_text())["parameters"]
    for key, allowed in params.items():
        if allowed == "range(1)":
            allowed = [0]
        assert isinstance(allowed, list) and set(frame[key]) == set(allowed), key
    meta = json.loads(max((out / "history").glob("*.meta.json"), key=lambda p: p.stat().st_mtime).read_text())
    directory = Path(meta["analysis_dirs"]["ac"])
    if not directory.is_absolute():
        directory = out / directory
    for _, row in frame.iterrows():
        prior = baseline.loc[(row.corner_mos, row.gcode)]
        for key in params:
            if key != "trim_family":
                assert row[key] == prior[key], key
        if row.trim_family == "5p73":
            for metric in ["k100", "k10", "compr", "idd", "tail_gate_v", "tail_ratio",
                           "bw_in1_mhz", "bw_in2_mhz", "loaded_bw_in1_mhz", "loaded_bw_in2_mhz",
                           "cin1_per_pin_ff", "cin2_per_pin_ff"]:
                assert np.isclose(row[metric], prior[metric], rtol=1e-5, atol=1e-12), (row.gcode, metric)
        for tb, prefix in [("ac", ""), ("fanout", "loaded_")]:
            wave = pd.read_csv(directory / f"run_{row.run_id}__{tb}.csv")
            for n in [1, 2]:
                check_curve(wave, f"ac{n}.gd", row[f"{prefix}acgain_in{n}"], row[f"{prefix}bw_in{n}_mhz"])
            waves[f"{sheet.stem}_{tb}_{row.run_id}"] = wave.to_numpy()
            waves["columns"] = wave.columns.to_numpy(dtype=str)
    frames.append(frame)
data = pd.concat(frames, ignore_index=True).copy()
assert len(data) == len(expected)
assert set(map(tuple, data[["corner_mos", "gcode", "trim_family"]].to_numpy())) == expected
refcols = ["corner_mos"] + [c for c in baseline if c.startswith("ihp_")]
refs = baseline[refcols].reset_index(drop=True).drop_duplicates()
assert refs.corner_mos.nunique() == len(refs)
data = data.merge(refs, on="corner_mos", validate="many_to_one").copy()
data["gain_error_percent"] = 100 * (data.k100.abs() / 10 - 1)
data["joint_dc_bare_loaded_bw_screen"] = (
    data.gain_error_percent.abs().le(1) & data.compr.between(.96758, 1.03242) &
    data.tail_gate_v.between(0, data.vdd))
for n in [1, 2]:
    data[f"bare_bw{n}_ratio_ihp"] = data[f"bw_in{n}_mhz"] / data[f"ihp_bw_in{n}_mhz_bare"]
    data[f"loaded_bw{n}_ratio_ihp"] = data[f"loaded_bw_in{n}_mhz"] / data[f"ihp_bw_in{n}_mhz"]
    data["joint_dc_bare_loaded_bw_screen"] &= data[f"bare_bw{n}_ratio_ihp"].ge(1) & data[f"loaded_bw{n}_ratio_ihp"].ge(1)
stem = evidence / ("sky_quiet_trim_corners" if args.corners else "sky_quiet_trim_poly")
data.to_csv(stem.with_suffix(".csv"), index=False)
np.savez_compressed(stem.with_name(stem.name + "_waveforms.npz"), **waves)
report = dict(audits=audits, anchored_curves=4*len(data), unchanged_controls=len(data)//2, control_replay="pass",
              gain_tolerance_percent=1, gain_tolerance_status="provisional", full_spec_coverage="unverified")
stem.with_name(stem.name + "_summary.json").write_text(json.dumps(report, indent=2) + "\n")
print(data[["corner_mos", "gcode", "trim_family", "gain_error_percent", "compr", "bw_in2_mhz",
            "loaded_bw_in2_mhz", "joint_dc_bare_loaded_bw_screen"]].to_string(index=False))

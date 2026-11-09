#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Intersect gain, shape, bare speed and receiver-loaded speed at five nominal points."""
import json
from pathlib import Path
import numpy as np
import pandas as pd
import yaml
from check_chipify_results import audit
from check_core_ac_capture import check_curve

ROOT = Path(__file__).resolve().parents[1]
evidence = ROOT / "doc/porting/evidence"
frames, audits = {}, {}
for design, name, tests in [
    ("sky", "sky_input2_quiet_replica", [("ac", ""), ("fanout", "loaded_")]),
    ("ihp", "ihp_input2_quiet_reference", [("ac", "")]),
]:
    project = ROOT / "verification/porting" / name
    parts, waves = [], {}
    audits[design] = {}
    for sheet in sorted((project / "datasheets/nominal").glob("*.yaml")):
        out = project / "out" / sheet.stem
        audits[design][sheet.stem] = audit(sheet, out, False)
        data = pd.read_csv(out / "simulation_results.csv", dtype={"run_id": str})
        params = yaml.safe_load(sheet.read_text())["parameters"]
        keys = ["corner_mos", "gcode", "temp", "vdd"]
        if design == "sky":
            keys += ["power_m", "replica_tracks_signal", "ibias", "load_family"]
        for key in keys:
            if set(data[key]) != set(params[key]):
                raise ValueError(f"Unexpected {key} in {sheet}")
        meta = json.loads(max((out / "history").glob("*.meta.json"), key=lambda p: p.stat().st_mtime).read_text())
        directory = Path(meta["analysis_dirs"]["ac"])
        if not directory.is_absolute():
            directory = out / directory
        for _, row in data.iterrows():
            for tb, prefix in tests:
                wave = pd.read_csv(directory / f"run_{row.run_id}__{tb}.csv")
                for n in [1, 2]:
                    check_curve(wave, f"ac{n}.gd", row[f"{prefix}acgain_in{n}"], row[f"{prefix}bw_in{n}_mhz"])
                waves[f"{sheet.stem}_{tb}_{row.run_id}"] = wave.to_numpy()
                waves["columns"] = wave.columns.to_numpy(dtype=str)
        parts.append(data)
    data = pd.concat(parts, ignore_index=True).copy()
    if len(data) != 5 or set(data.corner_mos) != {"tt", "ff", "fs", "sf", "ss"}:
        raise ValueError("Expected five distinct nominal MOS points")
    data.to_csv(evidence / (design + "_input2_quiet_corners.csv"), index=False)
    np.savez_compressed(evidence / (design + "_input2_quiet_corners_waveforms.npz"), **waves)
    frames[design] = data
sky = frames["sky"].copy()
sky["matched_corner"] = sky.corner_mos.replace({"fs": "sf", "sf": "fs"})
ihp = frames["ihp"].copy()
ihp["matched_corner"] = ihp.corner_mos
bare = pd.read_csv(evidence / "ihp_calibrated_pvt.csv")
bare = bare[(bare.temp == 27) & (bare.vdd == 1.5)].copy()
bare["matched_corner"] = bare.corner_mos
bare = bare[["matched_corner", "gcode", "bw_in1_mhz", "bw_in2_mhz"]]
ihp = ihp.merge(bare, on=["matched_corner", "gcode"], validate="one_to_one", suffixes=("", "_bare"))
if len(ihp) != 5:
    raise ValueError("IHP bare and loaded reference codes differ")
metrics = ["bw_in1_mhz", "bw_in2_mhz", "bw_in1_mhz_bare", "bw_in2_mhz_bare"]
references = ihp[["matched_corner", "gcode"] + metrics].rename(
    columns={"gcode": "ihp_gcode", **{m: "ihp_" + m for m in metrics}})
data = sky.merge(references, on="matched_corner", validate="one_to_one")
data["gain_error_percent"] = 100 * (data.k100.abs() / 10 - 1)
data["shape_pass"] = data.compr.between(.96758, 1.03242)
speed_pass = pd.Series(True, index=data.index)
for n in [1, 2]:
    data[f"bare_bw{n}_ratio_ihp"] = data[f"bw_in{n}_mhz"] / data[f"ihp_bw_in{n}_mhz_bare"]
    data[f"loaded_bw{n}_ratio_ihp"] = data[f"loaded_bw_in{n}_mhz"] / data[f"ihp_bw_in{n}_mhz"]
    speed_pass &= data[f"bare_bw{n}_ratio_ihp"].ge(1) & data[f"loaded_bw{n}_ratio_ihp"].ge(1)
data["joint_dc_bare_loaded_bw_screen"] = (
    data.gain_error_percent.abs().le(1) & data.shape_pass
    & data.tail_gate_v.ge(0) & data.tail_gate_v.le(data.vdd) & speed_pass)
data.to_csv(evidence / "input2_quiet_corners_matched.csv", index=False)
report = {"audits": audits, "gain_tolerance_percent": 1, "gain_tolerance_status": "provisional",
          "joint_nominal_passes": int(data.joint_dc_bare_loaded_bw_screen.sum()),
          "nominal_points": 5, "anchored_curves": 30,
          "loaded_scope": "Identical receiver input 1, 25 fF wire per output",
          "full_spec_coverage": "unverified",
          "remaining": ["voltage and temperature", "passive corners", "full transfer surfaces",
                        "noise", "loop stability", "real reference driver", "layout"]}
(evidence / "input2_quiet_corners_summary.json").write_text(json.dumps(report, indent=2) + "\n")
print(data[["corner_mos", "gcode", "gain_error_percent", "compr", "bw_in2_mhz",
            "loaded_bw_in2_mhz", "loaded_bw2_ratio_ihp", "cin1_per_pin_ff", "idd",
            "joint_dc_bare_loaded_bw_screen"]].sort_values("corner_mos").to_string(index=False))

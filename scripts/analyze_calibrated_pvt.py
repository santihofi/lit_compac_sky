#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Freeze fixed calibrated-code results and compare matched PVT conditions."""
import json
from pathlib import Path

import numpy as np
import pandas as pd

from check_chipify_results import audit
from check_core_ac_capture import check_curve

ROOT = Path(__file__).resolve().parents[1]
evidence = ROOT / "doc/porting/evidence"
frames = {}
for project in ["ihp_calibrated_pvt", "sky_centered_dc", "sky_centered_ac"]:
    directory = ROOT / "verification/porting" / project
    audits, parts, waves = {}, [], {}
    for sheet in sorted((directory / "datasheets/pvt").glob("*.yaml")):
        out = directory / "out" / sheet.stem
        result = audit(sheet, out, False)
        data = pd.read_csv(out / "simulation_results.csv", dtype={"run_id": str})
        if project == "sky_centered_ac":
            meta = json.loads(max((out / "history").glob("*.meta.json"),
                                 key=lambda p: p.stat().st_mtime).read_text())
            for _, row in data.iterrows():
                wave = pd.read_csv(out / meta["analysis_dirs"]["ac"] / ("run_" + row.run_id + "__ac.csv"))
                for number in [1, 2]:
                    check_curve(wave, f"ac{number}.gd", row[f"acgain_in{number}"],
                                row[f"bw_in{number}_mhz"])
                waves[sheet.stem + "_" + row.run_id] = wave.to_numpy()
                waves["columns"] = wave.columns.to_numpy(dtype=str)
            result["anchored_core_curves"] = 2 * len(data)
        audits[sheet.name] = result
        data["datasheet"] = sheet.name
        parts.append(data)
    data = pd.concat(parts, ignore_index=True)
    if len(data) != 45 or data.duplicated(["corner_mos","temp","vdd"]).any():
        raise ValueError("Expected 45 unique fixed-code conditions")
    data.to_csv(evidence / (project + ".csv"), index=False)
    (evidence / (project + "_audit.json")).write_text(json.dumps(audits, indent=2) + "\n")
    if waves:
        np.savez_compressed(evidence / (project + "_waveforms.npz"), **waves)
    frames[project] = data

summary = {}
for project, data in frames.items():
    fields = ["k100", "k10", "compr"] if "k100" in data else []
    fields += ["bw_in1_mhz", "bw_in2_mhz"] if "bw_in1_mhz" in data else []
    summary[project] = {m: {"min": float(data[m].min()), "max": float(data[m].max())} for m in fields}
    if "compr" in data:
        summary[project]["shape_passes"] = int(data.compr.between(.96758,1.03242).sum())
sky = frames["sky_centered_ac"].copy()
sky["matched_corner"] = sky.corner_mos.replace({"fs":"sf","sf":"fs"})
ihp = frames["ihp_calibrated_pvt"].copy()
ihp["matched_corner"] = ihp.corner_mos
keys = ["matched_corner", "temp", "vdd"]
matched = sky.merge(ihp, on=keys, suffixes=("_sky","_ihp"), validate="one_to_one")
for number in [1, 2]:
    metric = f"bw_in{number}_mhz"
    matched[metric + "_ratio"] = matched[metric + "_sky"] / matched[metric + "_ihp"]
    summary["input" + str(number) + "_bandwidth_comparison"] = {
        "sky_faster_cases": int((matched[metric + "_ratio"] > 1).sum()),
        "minimum_ratio": float(matched[metric + "_ratio"].min()),
        "maximum_ratio": float(matched[metric + "_ratio"].max())}
matched.to_csv(evidence / "calibrated_pvt_matched.csv", index=False)
(evidence / "calibrated_pvt_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
print(json.dumps(summary, indent=2))
failed = frames["sky_centered_dc"]
print(failed[~failed.compr.between(.96758,1.03242)][
    ["corner_mos","temp","vdd","gcode","k100","compr"]].to_string(index=False))

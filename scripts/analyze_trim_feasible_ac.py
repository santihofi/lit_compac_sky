#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Audit AC curves and intersect bandwidth coverage with measured DC feasibility."""
import json
from pathlib import Path
import numpy as np
import pandas as pd
from check_chipify_results import audit
from check_core_ac_capture import check_curve

ROOT = Path(__file__).resolve().parents[1]
evidence = ROOT / "doc/porting/evidence"
project = ROOT / "verification/porting/sky_trim_tg2_ac"
dc_summary = json.loads((evidence / "sky_tg2_codes_nominal_summary.json").read_text())
dc = pd.read_csv(evidence / "sky_tg2_codes_nominal.csv")
feasible = dc[dc.dc_screen_pass].copy()
audits, parts, waves = {}, [], {}
for sheet in sorted((project / "datasheets/feasible").glob("*.yaml")):
    out = project / "out" / sheet.stem
    result = audit(sheet, out, False)
    data = pd.read_csv(out / "simulation_results.csv", dtype={"run_id": str})
    meta = json.loads(max((out / "history").glob("*.meta.json"), key=lambda p: p.stat().st_mtime).read_text())
    folder = Path(meta["analysis_dirs"]["ac"])
    if not folder.is_absolute():
        folder = out / folder
    for _, row in data.iterrows():
        wave = pd.read_csv(folder / ("run_" + row.run_id + "__ac.csv"))
        for number in [1, 2]:
            check_curve(wave, f"ac{number}.gd", row[f"acgain_in{number}"], row[f"bw_in{number}_mhz"])
        waves[sheet.stem + "_" + row.run_id] = wave.to_numpy()
        waves["columns"] = wave.columns.to_numpy(dtype=str)
    result["anchored_core_curves"] = 2 * len(data)
    audits[sheet.name] = result
    parts.append(data)
data = pd.concat(parts, ignore_index=True)
keys = ["corner_mos", "temp", "vdd", "gcode"]
if set(map(tuple, data[keys].to_numpy())) != set(map(tuple, feasible[keys].to_numpy())):
    raise ValueError("AC and DC feasible-code coverage differ")
data = data.merge(feasible[keys + ["gain_error_percent", "compr"]], on=keys, validate="one_to_one")
ihp = pd.read_csv(evidence / "ihp_calibrated_pvt.csv")
ihp = ihp[(ihp.temp == 27) & (ihp.vdd == 1.5)].copy()
ihp["corner_mos"] = ihp.corner_mos.replace({"fs": "sf", "sf": "fs"})
data = data.merge(ihp[["corner_mos", "bw_in1_mhz", "bw_in2_mhz"]],
                  on="corner_mos", validate="many_to_one", suffixes=("", "_ihp"))
for n in [1, 2]:
    data[f"bw_in{n}_ratio"] = data[f"bw_in{n}_mhz"] / data[f"bw_in{n}_mhz_ihp"]
data["dc_and_matched_bw_pass"] = (data.bw_in1_ratio >= 1) & (data.bw_in2_ratio >= 1)
records = []
for corner, group in data.groupby("corner_mos"):
    records.append({
        "corner_mos": corner,
        "tested_codes": sorted(map(int, group.gcode)),
        "dc_and_matched_bw_codes": sorted(map(int, group[group.dc_and_matched_bw_pass].gcode)),
        "best_input2_ratio": float(group.bw_in2_ratio.max()),
        "full_spec_coverage": "unverified",
    })
data.to_csv(evidence / "sky_tg2_feasible_ac.csv", index=False)
np.savez_compressed(evidence / "sky_tg2_feasible_ac_waveforms.npz", **waves)
(evidence / "sky_tg2_feasible_ac_summary.json").write_text(json.dumps({
    "audits": audits, "coverage": records,
    "bandwidth_reference": "IHP nominal per-MOS nearest K100 code, VDD-tracking gate rail",
    "dc_gain_tolerance_percent": dc_summary["gain_tolerance_percent"],
    "missing": ["PVT coverage", "noise", "loop stability", "physical bias circuitry"],
}, indent=2) + "\n")
print(data[["corner_mos", "gcode", "gain_error_percent", "compr", "bw_in1_mhz",
            "bw_in2_mhz", "bw_in1_ratio", "bw_in2_ratio"]].to_string(index=False))
print(json.dumps(records, indent=2))

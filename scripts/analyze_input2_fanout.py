#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Compare audited driver bandwidth while scaling actual receiver loads too."""
import argparse
import json
from pathlib import Path
import numpy as np
import pandas as pd
from check_chipify_results import audit
from check_core_ac_capture import check_curve

ROOT = Path(__file__).resolve().parents[1]
evidence = ROOT / "doc/porting/evidence"
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--copies", type=int, choices=[5, 6], default=6)
args = parser.parse_args()
suffix = "6" if args.copies == 6 else ""
frames, audits = {}, {}
for design, corner, expected in [("sky", "fs", 8), ("ihp", "sf", 4)]:
    project = ROOT / "verification/porting" / (design + "_input2_fanout" + (suffix if design == "sky" else ""))
    out = project / "out"
    audits[design] = audit(project / f"datasheets/fanout_{corner}.yaml", out, False)
    data = pd.read_csv(out / "simulation_results.csv", dtype={"run_id": str})
    keys = ["fanout_input", "c_load"] + (["power_m"] if design == "sky" else [])
    if len(data) != expected or data.duplicated(keys).any():
        raise ValueError("Missing or repeated fanout cases")
    if not data.corner_mos.eq(corner).all() or not data.temp.eq(27).all() or not data.vdd.eq(1.5).all():
        raise ValueError("Wrong fanout operating condition")
    if set(data.c_load) != {"25f", "50f"} or set(data.fanout_input) != {1, 2}:
        raise ValueError("Wrong receiver-load grid")
    if design == "sky" and set(data.power_m) != {2, args.copies}:
        raise ValueError("Wrong copy-count grid")
    meta = json.loads(max((out / "history").glob("*.meta.json"), key=lambda p: p.stat().st_mtime).read_text())
    directory = Path(meta["analysis_dirs"]["ac"])
    if not directory.is_absolute():
        directory = out / directory
    waves = {}
    for _, row in data.iterrows():
        wave = pd.read_csv(directory / f"run_{row.run_id}__ac.csv")
        for number in [1, 2]:
            check_curve(wave, f"ac{number}.gd", row[f"acgain_in{number}"], row[f"bw_in{number}_mhz"])
        waves["run_" + row.run_id] = wave.to_numpy()
        waves["columns"] = wave.columns.to_numpy(dtype=str)
    np.savez_compressed(evidence / (design + "_input2_fanout" + suffix + "_waveforms.npz"), **waves)
    data.to_csv(evidence / (design + "_input2_fanout" + suffix + ".csv"), index=False)
    audits[design]["anchored_curves"] = 2 * len(data)
    frames[design] = data
keys = ["fanout_input", "c_load", "temp", "vdd"]
matched = frames["sky"].merge(frames["ihp"], on=keys, validate="many_to_one", suffixes=("_sky", "_ihp"))
for number in [1, 2]:
    metric = f"bw_in{number}_mhz"
    matched[f"bw{number}_ratio_ihp"] = matched[metric + "_sky"] / matched[metric + "_ihp"]
matched.to_csv(evidence / ("input2_fanout" + suffix + "_matched.csv"), index=False)
summary = {
    "audits": audits,
    "replica_finger_counts_integral": args.copies == 6,
    "scope": "Nominal slow-N fast-P driver plus identical receiver, 25/50 fF wire per output",
    "results": [],
}
for copies, group in matched.groupby("power_m"):
    summary["results"].append({
        "power_m": int(copies),
        "both_bandwidths_at_least_ihp": int((group.bw1_ratio_ihp.ge(1) & group.bw2_ratio_ihp.ge(1)).sum()),
        "cases": len(group),
        "input2_minimum_ratio_ihp": float(group.bw2_ratio_ihp.min()),
        "input2_maximum_ratio_ihp": float(group.bw2_ratio_ihp.max()),
    })
(evidence / ("input2_fanout" + suffix + "_summary.json")).write_text(json.dumps(summary, indent=2) + "\n")
print(matched[["power_m", "fanout_input", "c_load", "bw_in1_mhz_sky", "bw_in2_mhz_sky",
               "bw_in1_mhz_ihp", "bw_in2_mhz_ihp", "bw2_ratio_ihp"]].sort_values(
                   ["power_m", "fanout_input", "c_load"]).to_string(index=False))

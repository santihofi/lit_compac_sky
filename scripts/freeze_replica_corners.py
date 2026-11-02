#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Audit and retain the replica candidate's bandwidth and two feedback loops."""
import json
from pathlib import Path

import numpy as np
import pandas as pd

from check_chipify_results import audit
from check_core_ac_capture import check_curve
from check_loop_capture import check

ROOT = Path(__file__).resolve().parents[1]
evidence = ROOT / "doc/porting/evidence"
for project, folder, label in [
    ("sky_replica_ac", "pvt", "sky_replica_ac_pvt"),
    ("sky_replica_validation", "cmfb_pvt", "sky_replica_cmfb_pvt"),
    ("sky_replica_stability", "pvt", "sky_replica_bias_loop_pvt"),
]:
    p = ROOT / "verification/porting" / project
    audits, frames, archive = {}, [], {}
    for sheet in sorted((p / "datasheets" / folder).glob("*.yaml")):
        out = p / "out" / sheet.stem
        integrity = audit(sheet, out)
        frame = pd.read_csv(out / "simulation_results.csv", dtype={"run_id": str})
        if project == "sky_replica_ac":
            meta = json.loads(max((out / "history").glob("*.meta.json"),
                                 key=lambda f: f.stat().st_mtime).read_text())
            directory = Path(meta["analysis_dirs"]["ac"])
            if not directory.is_absolute():
                directory = out / directory
            for _, row in frame.iterrows():
                wave = pd.read_csv(directory / f"run_{row.run_id}__ac.csv")
                for number in [1, 2]:
                    check_curve(wave, f"ac{number}.gd", row[f"acgain_in{number}"],
                                row[f"bw_in{number}_mhz"])
                archive[sheet.stem + "_" + row.run_id] = wave.to_numpy()
                archive["columns"] = wave.columns.to_numpy(dtype=str)
            integrity["anchored_core_curves"] = 2 * len(frame)
        else:
            anchored, waves = check(sheet, out)
            integrity.update(anchored)
            archive.update({sheet.stem + "_" + k: v for k, v in waves.items()})
        audits[sheet.name] = integrity
        frame.insert(0, "datasheet", sheet.name)
        frames.append(frame)
    data = pd.concat(frames, ignore_index=True)
    data.to_csv(evidence / (label + ".csv"), index=False)
    (evidence / (label + "_audit.json")).write_text(json.dumps(audits, indent=2) + "\n")
    np.savez_compressed(evidence / (label + "_waveforms.npz"), **archive)
    metrics = (["bw_in1_mhz", "bw_in2_mhz", "cin1_per_pin_ff", "cin2_per_pin_ff", "idd"]
               if project == "sky_replica_ac" else ["pm", "gm_db", "fu", "ncross"])
    print(label)
    print(data.groupby("corner_mos")[metrics].agg(["min", "max"]).to_string())

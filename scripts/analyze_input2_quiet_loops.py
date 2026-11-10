#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Audit both captured loops at the selected nominal quiet-replica codes."""
import json
from pathlib import Path
import numpy as np
import pandas as pd
import yaml
from check_chipify_results import audit
from check_loop_capture import margins

ROOT = Path(__file__).resolve().parents[1]
project = ROOT / "verification/porting/sky_input2_quiet_loops"
evidence = ROOT / "doc/porting/evidence"
selection = pd.read_csv(evidence / "input2_quiet_selected_nominal.csv").set_index("corner_mos", drop=False)
assert len(selection) == 5 and set(selection.index) == {"ff", "fs", "sf", "ss", "tt"}
sheets = sorted((project / "datasheets/nominal").glob("*.yaml"))
assert {p.stem for p in sheets} == {"loops_" + c for c in selection.index}
frames, archive, audits = [], {}, {}
for sheet in sheets:
    out = project / "out" / sheet.stem
    integrity = audit(sheet, out)
    frame = pd.read_csv(out / "simulation_results.csv", dtype={"run_id": str})
    assert len(frame) == 1
    row = frame.iloc[0]
    expected = selection.loc[sheet.stem.removeprefix("loops_")]
    for key in yaml.safe_load(sheet.read_text())["parameters"]:
        if key in {"vd1", "vd2"}:
            assert row[key] == 0
        elif isinstance(expected[key], str):
            assert str(row[key]) == expected[key], key
        else:
            assert np.isclose(row[key], expected[key], rtol=1e-12, atol=0), key
    meta = json.loads(max((out / "history").glob("*.meta.json"), key=lambda p: p.stat().st_mtime).read_text())
    directory = Path(meta["analysis_dirs"]["ac"])
    if not directory.is_absolute():
        directory = out / directory
    for _, row in frame.iterrows():
        for loop in ["cmfb", "bias"]:
            wave = pd.read_csv(directory / f"run_{row.run_id}__{loop}.csv")
            for metric, value in margins(wave).items():
                assert np.isclose(value, row[f"{loop}_{metric}"], rtol=5e-5, atol=1e-4), (sheet, loop, metric)
            archive[f"{sheet.stem}_{loop}_{row.run_id}"] = wave.to_numpy()
            archive["columns"] = wave.columns.to_numpy(dtype=str)
    integrity["anchored_loop_curves"] = 2 * len(frame)
    audits[sheet.name] = integrity
    frames.append(frame)
data = pd.concat(frames, ignore_index=True)
data["both_loop_screens_pass"] = True
for loop in ["cmfb", "bias"]:
    data["both_loop_screens_pass"] &= (
        data[f"{loop}_pm"].between(45, 180) &
        (data[f"{loop}_gm_db"] >= 10) & (data[f"{loop}_ncross"] == 1))
stem = evidence / "sky_input2_quiet_loops"
data.to_csv(stem.with_suffix(".csv"), index=False)
stem.with_name(stem.name + "_audit.json").write_text(json.dumps(audits, indent=2) + "\n")
np.savez_compressed(stem.with_name(stem.name + "_waveforms.npz"), **archive)
print(data[["corner_mos", "gcode", "cmfb_pm", "cmfb_gm_db", "bias_pm", "bias_gm_db", "both_loop_screens_pass"]].to_string(index=False))

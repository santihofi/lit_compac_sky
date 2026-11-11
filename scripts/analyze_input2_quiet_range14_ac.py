#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Intersect nominal widened-network DC codes with bare and receiver-loaded speed."""
import json
from pathlib import Path
import numpy as np
import pandas as pd
import yaml
from check_chipify_results import audit
from check_core_ac_capture import check_curve

ROOT = Path(__file__).resolve().parents[1]
evidence = ROOT / "doc/porting/evidence"
project = ROOT / "verification/porting/sky_input2_quiet_range14_ac"
baseline = pd.read_csv(evidence / "sky_quiet_range14.csv")
nominal = baseline[(baseline.temp == 27) & (baseline.vdd == 1.5) & baseline.dc_screen_pass]
expected = set(map(tuple, nominal[["corner_mos", "gcode"]].to_numpy()))
frames, audits, waves = [], {}, {}
for sheet in sorted((project / "datasheets/nominal").glob("*.yaml")):
    out = project / "out" / sheet.stem
    audits[sheet.name] = audit(sheet, out, False)
    data = pd.read_csv(out / "simulation_results.csv", dtype={"run_id": str})
    for key, allowed in yaml.safe_load(sheet.read_text())["parameters"].items():
        if allowed == "range(1)":
            allowed = [0]
        assert isinstance(allowed, list) and set(data[key]) == set(allowed), (sheet, key)
    meta = json.loads(max((out / "history").glob("*.meta.json"), key=lambda p: p.stat().st_mtime).read_text())
    directory = Path(meta["analysis_dirs"]["ac"])
    if not directory.is_absolute():
        directory = out / directory
    for _, row in data.iterrows():
        prior = nominal[(nominal.corner_mos == row.corner_mos) & (nominal.gcode == row.gcode)]
        assert len(prior) == 1
        params = yaml.safe_load(sheet.read_text())["parameters"]
        for key in params:
            value = prior.iloc[0][key]
            assert row[key] == value, (sheet, key)
        for metric in ["k100", "k10", "compr", "idd", "tail_gate_v", "tail_ratio"]:
            assert np.isclose(row[metric], prior.iloc[0][metric], rtol=1e-5, atol=1e-12), (sheet, metric)
        for tb, prefix in [("ac", ""), ("fanout", "loaded_")]:
            wave = pd.read_csv(directory / f"run_{row.run_id}__{tb}.csv")
            for n in [1, 2]:
                check_curve(wave, f"ac{n}.gd", row[f"{prefix}acgain_in{n}"], row[f"{prefix}bw_in{n}_mhz"])
            waves[f"{sheet.stem}_{tb}_{row.run_id}"] = wave.to_numpy()
            waves["columns"] = wave.columns.to_numpy(dtype=str)
    frames.append(data)
data = pd.concat(frames, ignore_index=True)
assert len(data) == len(expected) and set(map(tuple, data[["corner_mos", "gcode"]].to_numpy())) == expected
references = pd.read_csv(evidence / "input2_quiet_corners_matched.csv")
columns = ["corner_mos", "matched_corner"] + [c for c in references if c.startswith("ihp_")]
references = references[columns]
assert len(references) == 5 and references.corner_mos.nunique() == 5
data = data.merge(references, on="corner_mos", validate="many_to_one")
data["gain_error_percent"] = 100 * (data.k100.abs() / 10 - 1)
data["joint_dc_bare_loaded_bw_screen"] = (
    data.gain_error_percent.abs().le(1) & data.compr.between(.96758, 1.03242) &
    data.tail_gate_v.between(0, data.vdd))
for n in [1, 2]:
    data[f"bare_bw{n}_ratio_ihp"] = data[f"bw_in{n}_mhz"] / data[f"ihp_bw_in{n}_mhz_bare"]
    data[f"loaded_bw{n}_ratio_ihp"] = data[f"loaded_bw_in{n}_mhz"] / data[f"ihp_bw_in{n}_mhz"]
    data["joint_dc_bare_loaded_bw_screen"] &= data[f"bare_bw{n}_ratio_ihp"].ge(1) & data[f"loaded_bw{n}_ratio_ihp"].ge(1)
coverage = [{"corner_mos": corner,
             "feasible_codes": sorted(map(int, group.loc[group.joint_dc_bare_loaded_bw_screen, "gcode"]))}
            for corner, group in data.groupby("corner_mos")]
summary = {"audits": audits, "coverage": coverage, "anchored_curves": 4 * len(data),
           "dc_replay": "pass", "gain_tolerance_percent": 1, "gain_tolerance_status": "provisional",
           "full_spec_coverage": "unverified", "scope": "nominal MOS corners, identical receiver input 1 with 25 fF wire"}
stem = evidence / "sky_quiet_range14_ac"
data.to_csv(stem.with_suffix(".csv"), index=False)
stem.with_name(stem.name + "_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
np.savez_compressed(stem.with_name(stem.name + "_waveforms.npz"), **waves)
print(data[["corner_mos", "gcode", "bw_in2_mhz", "loaded_bw_in2_mhz",
            "bare_bw2_ratio_ihp", "loaded_bw2_ratio_ihp", "joint_dc_bare_loaded_bw_screen"]].to_string(index=False))
print(json.dumps(coverage, indent=2))

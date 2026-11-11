#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Combine observed DC-feasible settings without mixing resistor variants or specifications."""
import json
from pathlib import Path
import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parents[1]
evidence = ROOT / "doc/porting/evidence"
sources = ["sky_quiet_codes_pvt", "sky_quiet_bias_sensitivity", "sky_quiet_refine"]
frames = []
for name in sources:
    data = pd.read_csv(evidence / f"{name}.csv")
    if "bias_factor" not in data:
        data["bias_factor"] = 1.
    for key, expected in {"power_m": 6, "rscale": 1.7, "rbase_scale": 1,
                          "rtrim_scale": 1, "load_family": "1p41",
                          "replica_tracks_signal": 0}.items():
        assert data[key].eq(expected).all(), (name, key)
    for corner, group in data.groupby("corner_mos"):
        sheet = ROOT / f"verification/porting/sky_input2_quiet_pvt/datasheets/codes_pvt/quiet_pvt_{corner}.yaml"
        for parameter, allowed in yaml.safe_load(sheet.read_text())["parameters"].items():
            if allowed == "range(1)":
                allowed = [0]
            assert isinstance(allowed, list)
            assert set(group[parameter]).issubset(set(allowed)), (name, corner, parameter)
    data["source"] = name
    frames.append(data)
all_data = pd.concat(frames, ignore_index=True)
all_data["dc_pass_recomputed"] = (all_data.k100.abs().between(9.9, 10.1) &
    all_data.compr.between(.96758, 1.03242) & all_data.tail_gate_v.between(0, all_data.vdd))
assert all_data.dc_pass_recomputed.eq(all_data.dc_screen_pass).all()
records = []
for key, group in all_data.groupby(["corner_mos", "temp", "vdd"]):
    good = group[group.dc_pass_recomputed]
    settings = good[["gcode", "ibias", "bias_factor", "source"]].drop_duplicates()
    records.append({"corner_mos": key[0], "temp": float(key[1]), "vdd": float(key[2]),
                    "dc_covered": bool(len(good)), "settings": settings.to_dict("records")})
assert len(records) == 45
summary = {"gain_tolerance_percent": 1, "gain_tolerance_status": "provisional",
           "scope": "observed DC gain/shape settings only, nominal passives and ideal references",
           "full_spec_coverage": "unverified", "covered_points": sum(x["dc_covered"] for x in records),
           "points": records}
(evidence / "sky_quiet_calibration_coverage.json").write_text(json.dumps(summary, indent=2) + "\n")
print("Covered DC points:", summary["covered_points"], "/45")
print("Unresolved:", [(x["corner_mos"], x["temp"], x["vdd"]) for x in records if not x["dc_covered"]])

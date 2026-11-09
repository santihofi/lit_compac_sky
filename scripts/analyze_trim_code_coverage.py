#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Report feasible DC codes per PVT without treating every code as a requirement."""
import argparse
import json
from pathlib import Path
import pandas as pd
from check_chipify_results import audit

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--grid", choices=["nominal", "pvt"], default="nominal")
parser.add_argument("--candidate", choices=["tg2", "wide"], default="tg2")
parser.add_argument("--gain-tolerance-percent", type=float, required=True,
                    help="Explicit screening tolerance, not an inferred specification")
args = parser.parse_args()
if not 0 <= args.gain_tolerance_percent < 100:
    parser.error("Gain tolerance must be in [0, 100)")
if args.candidate == "wide" and args.grid != "nominal":
    parser.error("The wider network has no exhaustive PVT code sweep yet")
project = ROOT / "verification/porting" / (
    "sky_trim_tg2" if args.candidate == "tg2" else "sky_replica_trim_range")
folder = "codes_" + args.grid if args.candidate == "tg2" else "steps"
frames, audits = [], {}
for sheet in sorted((project / "datasheets" / folder).glob("*.yaml")):
    out = project / "out" / sheet.stem
    audits[sheet.name] = audit(sheet, out, False)
    frame = pd.read_csv(out / "simulation_results.csv")
    import yaml
    parameters = yaml.safe_load(sheet.read_text())["parameters"]
    for name in ["corner_mos", "temp", "vdd", "gcode", "ibias", "rscale"]:
        if set(frame[name]) != set(parameters[name]):
            raise ValueError(f"Unexpected {name} values in {sheet.name}")
    frames.append(frame)
if len(frames) != 5:
    raise ValueError("Expected five MOS-corner sheets")
data = pd.concat(frames, ignore_index=True)
data["gain_error_percent"] = 100 * (data.k100.abs() / 10 - 1)
data["dc_screen_pass"] = (
    data.gain_error_percent.abs().le(args.gain_tolerance_percent)
    & data.compr.between(.96758, 1.03242)
    & data.tail_gate_v.ge(0) & data.tail_gate_v.le(data.vdd)
)
records = []
for key, group in data.groupby(["corner_mos", "temp", "vdd"]):
    if sorted(group.gcode) != list(range(32)):
        raise ValueError(f"Incomplete or duplicate code coverage: {key}")
    feasible = group[group.dc_screen_pass]
    best = group.loc[group.gain_error_percent.abs().idxmin()]
    records.append({
        "corner_mos": key[0], "temp": float(key[1]), "vdd": float(key[2]),
        "dc_feasible_codes": sorted(int(x) for x in feasible.gcode),
        "dc_covered": bool(len(feasible)),
        "nearest_gain_code": int(best.gcode),
        "nearest_gain_error_percent": float(best.gain_error_percent),
        "nearest_gain_shape": float(best.compr),
        "full_spec_coverage": "unverified",
    })
expected = 5 if args.grid == "nominal" else 45
if len(records) != expected:
    raise ValueError(f"Expected {expected} PVT points")
result = {
    "scope": "DC screening only, nominal passive models, ideal current and gate controls",
    "acceptance": "For every PVT point at least one single code must satisfy all applicable specs",
    "gain_tolerance_percent": args.gain_tolerance_percent,
    "gain_tolerance_status": "explicit sensitivity screen, not approved specification",
    "missing": ["bandwidth", "noise", "loop stability", "passive corners", "physical bias circuitry"],
    "audits": audits, "coverage": records,
}
prefix = ROOT / "doc/porting/evidence" / ("sky_" + args.candidate + "_codes_" + args.grid)
data.to_csv(str(prefix) + ".csv", index=False)
Path(str(prefix) + "_summary.json").write_text(json.dumps(result, indent=2) + "\n")
print(pd.DataFrame(records).to_string(index=False))

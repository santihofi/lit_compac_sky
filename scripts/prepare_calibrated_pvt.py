#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Hold each laboratory-selected code fixed across supply and temperature."""
import json
from pathlib import Path
import re

import yaml

ROOT = Path(__file__).resolve().parents[1]
base = ROOT / "verification/porting"
header = "# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer\n# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1\n"
source = base / "sky_replica_trim_range"
pattern = r"^\.subckt .*?^\.ends[^\n]*"
definitions = "\n".join(re.findall(pattern, (source / "tb/replica.spice").read_text(), re.M | re.S))
for design in ["sky", "ihp"]:
    filename = "sky_centered_gain_calibration" if design == "sky" else "ihp_gain_calibration"
    summary = json.loads((ROOT / "doc/porting/evidence" / (filename + "_summary.json")).read_text())
    selected = {r["corner_mos"]: r["nearest_code"] for r in summary if r["metric"] == "k100"}
    if len(selected) != 5:
        raise ValueError("Expected one gain-100mV code per MOS corner")
    if design == "sky":
        experiments = [
            ("sky_centered_dc", source / "tb/replica.spice", "replica",
             base / "sky_replica_tail/datasheets/calibration/trim_tt.yaml", 3),
            ("sky_centered_ac", base / "sky_replica_ac/tb/ac.spice", "ac",
             base / "sky_replica_ac/datasheets/ac.yaml", 3),
        ]
    else:
        experiments = [
            ("ihp_calibrated_pvt", base / "ihp_gain_trim/tb/core.spice", "core",
             base / "ihp_gain_trim/datasheets/endpoints.yaml", 2)]
    for name, deck_path, test, sheet_path, workers in experiments:
        target = base / name
        (target / "tb").mkdir(parents=True, exist_ok=True)
        (target / "datasheets/pvt").mkdir(parents=True, exist_ok=True)
        deck = deck_path.read_text()
        if design == "sky":
            deck = re.sub(pattern, "", deck, flags=re.M | re.S)
            deck = re.sub(r"^\.end\s*$", lambda _: definitions + "\n.end", deck, flags=re.M)
        (target / "tb" / (test + ".spice")).write_text(deck)
        for corner, code in selected.items():
            sheet = yaml.safe_load(sheet_path.read_text())
            if design == "sky":
                params = yaml.safe_load(
                    (base / "sky_replica_tail/datasheets/calibration" / ("trim_" + corner + ".yaml")).read_text()
                )["parameters"]
                sheet["parameters"] = params
                sheet["parameters"].update(rbase_scale=[.6], rtrim_scale=[2])
            else:
                sheet["parameters"]["gate_tracks_vdd"] = [1]
            sheet["parameters"].update(corner_mos=[corner], gcode=[code],
                                       temp=[0,27,80], vdd=[1.45,1.5,1.65])
            (target / "datasheets/pvt" / ("calibrated_" + corner + ".yaml")).write_text(
                header + yaml.safe_dump(sheet, sort_keys=False))
        (target / "settings.json").write_text(json.dumps(
            {"num_cores": workers, "sim_timeout_sec": 600}) + "\n")
        (target / "calibration.json").write_text(json.dumps({
            "target_metric": "k100", "target_magnitude_per_v": 10,
            "temperature_c": 27, "supply_v": 1.5, "gain_codes": selected,
            "source_evidence": filename + "_summary.json"}, indent=2) + "\n")
        (target / "README.md").write_text("""# Fixed-code calibrated PVT control

Each MOS corner uses its nearest measured K100 magnitude to 10 per volt at 27 C and 1.5 V.
The selected gain code then stays fixed over the supply and temperature grid.
The SKY130 design also retains its earlier fixed per-corner ideal current settings.
Nominal resistors are used throughout.
This is neither temperature compensation nor a real bias-DAC qualification.
scripts/prepare_calibrated_pvt.py generates the project from retained source decks and calibration evidence.
""")

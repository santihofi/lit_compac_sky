#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Prepare all gain codes only after a global trim factor passes endpoint screening."""
import argparse
import json
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--trim-factor", type=float, required=True)
args = parser.parse_args()
summary = json.loads((ROOT / "doc/porting/evidence/sky_input2_pair_trim_range_summary.json").read_text())
assert summary["control_replay"] == "pass"
assert summary["target_brackets_by_trim_factor"][str(args.trim_factor)] == 10
source = ROOT / "verification/porting/sky_input2_pair_trim_range"
target = ROOT / "verification/porting/sky_input2_pair_global_codes"
(target / "tb").mkdir(parents=True, exist_ok=True)
(target / "datasheets/codes").mkdir(parents=True, exist_ok=True)
(target / "tb/replica.spice").write_text((source / "tb/replica.spice").read_text())
header = "# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer\n# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1\n"
for path in sorted((source / "datasheets/endpoints").glob("*.yaml")):
    sheet = yaml.safe_load(path.read_text())
    sheet["parameters"].update(rtrim_scale=[args.trim_factor], gcode=list(range(32)))
    (target / "datasheets/codes" / path.name).write_text(header + yaml.safe_dump(sheet, sort_keys=False))
(target / "settings.json").write_text(json.dumps({"num_cores": 4, "sim_timeout_sec": 600}) + "\n")
(target / "README.md").write_text(f"""# Global smaller-pair gain-code screen

Use one trim factor {args.trim_factor}, fixed-load factor 0.8 and active-pair scale 2/3 at all ten operating points.
All 32 codes are swept, with twenty endpoints available as replay controls.
Nominal SS and hot points use bias factor 0.9, cold TT uses 0.85 and other nominal corners use 1.
These 320 cases test joint DC feasibility on a subset of PVT.
Same-setting AC, noise and stability remain necessary before a circuit acceptance verdict.
""")

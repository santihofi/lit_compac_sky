#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Prepare the minimum next integer-copy candidate and an unchanged release control."""
import json
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
base = ROOT / "verification/porting"
source = base / "sky_input2_parallel"
target = base / "sky_input2_candidate"
(target / "tb").mkdir(parents=True, exist_ok=True)
for folder in ["control", "nominal6"]:
    (target / "datasheets" / folder).mkdir(parents=True, exist_ok=True)
for name in ["replica", "ac"]:
    (target / f"tb/{name}.spice").write_text((source / f"tb/{name}.spice").read_text())
header = "# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer\n# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1\n"
control = yaml.safe_load((source / "datasheets/parallel_fs.yaml").read_text())
control["parameters"]["power_m"] = [2]
(target / "datasheets/control/release_fs.yaml").write_text(header + yaml.safe_dump(control, sort_keys=False))
summary = json.loads((ROOT / "doc/porting/evidence/sky_tg2_codes_nominal_summary.json").read_text())
for record in summary["coverage"]:
    corner = record["corner_mos"]
    sheet = yaml.safe_load((source / "datasheets/parallel_fs.yaml").read_text())
    sheet["parameters"] = yaml.safe_load((base / f"sky_trim_tg2/datasheets/codes_nominal/tg2_nominal_{corner}.yaml").read_text())["parameters"]
    sheet["parameters"].update(gcode=[record["nearest_gain_code"]], power_m=[6], load_family=["1p41"])
    replicas = 12 * sheet["parameters"]["pair_scale"][0] * sheet["parameters"]["power_m"][0] / 8
    if replicas != int(replicas):
        raise ValueError("Exact replica geometry needs an integer finger count")
    (target / f"datasheets/nominal6/candidate6_{corner}.yaml").write_text(header + yaml.safe_dump(sheet, sort_keys=False))
(target / "settings.json").write_text(json.dumps({"num_cores": 2, "sim_timeout_sec": 600}) + "\n")
(target / "README.md").write_text("""# Six-copy narrow-load candidate

Six copies are the smallest tested integer-finger option passing the slow-corner fixed-load bandwidth screen.
The fixed loads use resistance-matched 1.41 um precision poly.
Each MOS corner retains the earlier unit-current setting and nearest nominal gain code.
The release control is the previously measured two-copy fs point.
The earlier five-copy nominal folder is diagnostic only because its replica finger count was truncated.
This is a nominal gain, shape and fixed-load bandwidth screen, not complete schematic acceptance.
""")

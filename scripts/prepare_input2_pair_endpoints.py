#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Check global smaller-pair gain range before another exhaustive corner sweep."""
import json
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
base = ROOT / "verification/porting"
source = base / "sky_input2_quiet_range14"
target = base / "sky_input2_pair_endpoints"
(target / "tb").mkdir(parents=True, exist_ok=True)
(target / "datasheets/endpoints").mkdir(parents=True, exist_ok=True)
deck = (base / "sky_input2_pair_calibration/tb/replica.spice").read_text()
(target / "tb/replica.spice").write_text(deck)
header = "# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer\n# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1\n"
for path in sorted((source / "datasheets/codes").glob("range_*.yaml")):
    sheet = yaml.safe_load(path.read_text())
    sheet["parameters"].update(gcode=[0, 31], pair_scale=[2 / 3], trim_family=["2p85"])
    if path.stem == "range_ss_27C_1500mV":
        sheet["parameters"]["bias_factor"] = [.9]
    (target / "datasheets/endpoints" / path.name).write_text(header + yaml.safe_dump(sheet, sort_keys=False))
(target / "settings.json").write_text(json.dumps({"num_cores": 4, "sim_timeout_sec": 600}) + "\n")
(target / "README.md").write_text("""# Global smaller-pair endpoint screen

The smaller active-pair geometry and fixed dummy loading apply at every test point.
The five nominal MOS corners and five difficult PVT points are tested at gain-code endpoints.
Bias settings follow the preceding widened-network screen, except nominal SS uses its measured factor 0.9.
Nominal SS endpoints replay the completed smaller-pair 32-code sweep.
Endpoint span is a range diagnostic, not a joint code or full-PVT verdict.
Prior results from larger input pairs cannot establish coverage of this geometry.
""")

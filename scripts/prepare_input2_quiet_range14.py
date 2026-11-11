#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Sweep all gain codes for one globally fixed widened resistor network."""
import copy
import json
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
source = ROOT / "verification/porting/sky_input2_quiet_range"
target = ROOT / "verification/porting/sky_input2_quiet_range14"
(target / "tb").mkdir(parents=True, exist_ok=True)
(target / "datasheets/codes").mkdir(parents=True, exist_ok=True)
(target / "tb/replica.spice").write_text((source / "tb/replica.spice").read_text())
header = "# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer\n# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1\n"
for path in sorted((source / "datasheets/endpoints").glob("*.yaml")):
    sheet = yaml.safe_load(path.read_text())
    sheet["parameters"].update(rbase_scale=[0.8], rtrim_scale=[1.4])
    if path.stem == "range_tt_0C_1450mV":
        control = copy.deepcopy(sheet)
        (target / "datasheets/codes/control_tt_0C_1450mV.yaml").write_text(header + yaml.safe_dump(control, sort_keys=False))
        sheet["parameters"]["bias_factor"] = [0.85]
    sheet["parameters"]["gcode"] = list(range(32))
    (target / "datasheets/codes" / path.name).write_text(header + yaml.safe_dump(sheet, sort_keys=False))
(target / "settings.json").write_text(json.dumps({"num_cores": 4, "sim_timeout_sec": 600}) + "\n")
(target / "README.md").write_text("""# Fixed 0.8 / trim 1.4 global resistor candidate

This candidate applies one resistor network at all ten test points.
All 32 gain codes are tested at five nominal MOS corners and five previously unresolved PVT points.
Nominal bias factors remain 1, hot points use 0.9 and cold TT uses 0.85.
Two additional cold-TT endpoints at factor 0.9 replay the preceding range study.
The 322-case batch has twenty endpoint controls from that study.
These ten points are a screening subset, not all 45 PVT points.
DC-feasible codes still require same-code bandwidth, noise and stability checks.
Do not combine this variant's coverage with the original resistor network's 40/45 result.
""")

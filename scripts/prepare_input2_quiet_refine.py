#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Refine two bias/code gaps suggested by the sparse sensitivity data."""
import json
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
source = ROOT / "verification/porting/sky_input2_quiet_bias"
target = ROOT / "verification/porting/sky_input2_quiet_refine"
(target / "tb").mkdir(parents=True, exist_ok=True)
(target / "datasheets/refine").mkdir(parents=True, exist_ok=True)
(target / "tb/replica.spice").write_text((source / "tb/replica.spice").read_text())
header = "# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer\n# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1\n"
for name, codes, factors in [
    ("bias_fs_27C_1650mV", [25, 26, 27, 28], [0.8, 0.9]),
    ("bias_tt_0C_1500mV", [0, 1], [0.83, 0.85, 0.87]),
]:
    sheet = yaml.safe_load((source / f"datasheets/sensitivity/{name}.yaml").read_text())
    sheet["parameters"].update(gcode=codes, bias_factor=factors)
    (target / f"datasheets/refine/{name}.yaml").write_text(header + yaml.safe_dump(sheet, sort_keys=False))
(target / "settings.json").write_text(json.dumps({"num_cores": 4, "sim_timeout_sec": 600}) + "\n")

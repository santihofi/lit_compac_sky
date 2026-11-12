#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Recalibrate the smaller active-pair candidate before comparing matched-gain speed."""
import json
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
base = ROOT / "verification/porting"
source = base / "sky_input2_pair_width"
target = base / "sky_input2_pair_calibration"
(target / "tb").mkdir(parents=True, exist_ok=True)
(target / "datasheets").mkdir(exist_ok=True)
(target / "tb/replica.spice").write_text((source / "tb/replica.spice").read_text())
sheet = yaml.safe_load((source / "datasheets/pair_ss.yaml").read_text())
sheet["parameters"].update(gcode=list(range(32)), pair_scale=[2 / 3])
sheet["tests"] = {"replica": sheet["tests"]["replica"]}
header = "# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer\n# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1\n"
(target / "datasheets/calibrate_ss.yaml").write_text(header + yaml.safe_dump(sheet, sort_keys=False))
(target / "settings.json").write_text(json.dumps({"num_cores": 4, "sim_timeout_sec": 600}) + "\n")

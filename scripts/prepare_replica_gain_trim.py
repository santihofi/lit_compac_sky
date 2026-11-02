#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Check gain-trim endpoint coverage with the retained fixed current codes."""
import json
from pathlib import Path
import shutil

import yaml

ROOT = Path(__file__).resolve().parents[1]
source = ROOT/"verification/porting/sky_replica_tail"
target = ROOT/"verification/porting/sky_replica_gain_trim"
(target/"tb").mkdir(parents=True, exist_ok=True)
(target/"datasheets/endpoints").mkdir(parents=True, exist_ok=True)
shutil.copy2(source/"tb/replica.spice", target/"tb/replica.spice")
header = "# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer\n# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1\n"
for path in sorted((source/"datasheets/calibration").glob("*.yaml")):
    sheet = yaml.safe_load(path.read_text())
    sheet["parameters"]["gcode"] = [0, 31]
    (target/"datasheets/endpoints"/path.name).write_text(header+yaml.safe_dump(sheet, sort_keys=False))
(target/"settings.json").write_text(json.dumps({"num_cores": 3, "sim_timeout_sec": 600})+"\n")

#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Screen global trim factors with the smaller active pair and fixed base loads."""
import json
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
base = ROOT / "verification/porting"
source = base / "sky_input2_pair_endpoints"
target = base / "sky_input2_pair_trim_range"
(target / "tb").mkdir(parents=True, exist_ok=True)
(target / "datasheets/endpoints").mkdir(parents=True, exist_ok=True)
(target / "tb/replica.spice").write_text((source / "tb/replica.spice").read_text())
header = "# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer\n# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1\n"
for path in sorted((source / "datasheets/endpoints").glob("*.yaml")):
    sheet = yaml.safe_load(path.read_text())
    sheet["parameters"]["rtrim_scale"] = [1.4, 1.6, 1.65, 1.7]
    (target / "datasheets/endpoints" / path.name).write_text(header + yaml.safe_dump(sheet, sort_keys=False))
(target / "settings.json").write_text(json.dumps({"num_cores": 4, "sim_timeout_sec": 600}) + "\n")
(target / "README.md").write_text("""# Smaller-pair global trim-range controls

At fixed base-load factor 0.8, compare trim factors 1.4, 1.6, 1.65 and 1.7.
The smaller active pair, fixed four-finger dummy and 2.85 um trim family apply globally.
The same ten operating points and bias factors are retained.
Eighty endpoint cases include twenty factor-1.4 replay controls.
Any selected trim factor must be global, followed by gain/current calibration and same-setting AC.
Endpoint span alone does not establish a joint passing code.
""")

#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Search nominal SS gain/bias settings for the narrow trim-poly candidate."""
import json
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
base = ROOT / "verification/porting"
source = base / "sky_input2_quiet_trim_poly"
target = base / "sky_input2_trim_ss_bias"
(target / "tb").mkdir(parents=True, exist_ok=True)
(target / "datasheets").mkdir(exist_ok=True)
(target / "tb/replica.spice").write_text((source / "tb/replica.spice").read_text())
sheet = yaml.safe_load((source / "datasheets/corners/trim_ss.yaml").read_text())
sheet["parameters"].update(gcode=list(range(32)), bias_factor=[.8, .9, 1., 1.1, 1.2], trim_family=["2p85"])
sheet["tests"] = {"replica": sheet["tests"]["replica"]}
header = "# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer\n# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1\n"
(target / "datasheets/ss_bias.yaml").write_text(header + yaml.safe_dump(sheet, sort_keys=False))
(target / "settings.json").write_text(json.dumps({"num_cores": 4, "sim_timeout_sec": 600}) + "\n")
(target / "README.md").write_text("""# Nominal SS gain and bias search

The narrow trim-poly candidate keeps all geometry, reference voltage and resistor factors unchanged.
All 32 gain codes are evaluated at five ideal current factors from 0.8 to 1.2.
Both reference current sources scale together.
Codes 11 and 12 at factor 1 replay the preceding narrow-poly SS cases.
The DC-feasible set must subsequently be intersected with bare and receiver-loaded bandwidth at identical settings.
This discrete bias search does not exhaust arbitrary current values or physical DAC behavior.
""")

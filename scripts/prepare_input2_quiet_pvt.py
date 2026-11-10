#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Screen every gain code of the quiet replica at 45 nominal-passive PVT points."""
import json
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
source = ROOT / "verification/porting/sky_input2_quiet_replica"
target = ROOT / "verification/porting/sky_input2_quiet_pvt"
(target / "tb").mkdir(parents=True, exist_ok=True)
(target / "datasheets/codes_pvt").mkdir(parents=True, exist_ok=True)
(target / "tb/replica.spice").write_text((source / "tb/replica.spice").read_text())
header = "# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer\n# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1\n"
for corner in ["ff", "fs", "sf", "ss", "tt"]:
    sheet = yaml.safe_load((source / f"datasheets/nominal/quiet_{corner}.yaml").read_text())
    sheet["tests"] = {"replica": sheet["tests"]["replica"]}
    sheet["parameters"].update(gcode=list(range(32)), temp=[0, 27, 80], vdd=[1.45, 1.5, 1.65])
    (target / f"datasheets/codes_pvt/quiet_pvt_{corner}.yaml").write_text(header + yaml.safe_dump(sheet, sort_keys=False))
(target / "settings.json").write_text(json.dumps({"num_cores": 4, "sim_timeout_sec": 600}) + "\n")
(target / "README.md").write_text("""# Quiet-replica exhaustive gain-code PVT screen

This is the six-copy quiet-replica circuit with 1.41 um fixed loads.
All 32 gain codes are evaluated at five MOS corners, three temperatures and three supplies.
The earlier per-MOS ideal bias currents remain fixed across supply and temperature.
Passives are nominal, and gate and reference drivers are ideal.
The screen finds common gain and diagonal-shape codes, not full-spec coverage.
Alternative bias settings remain available when no gain code passes.
Use scripts/analyze_trim_code_coverage.py --candidate quiet --grid pvt --gain-tolerance-percent 1 after completion.
""")

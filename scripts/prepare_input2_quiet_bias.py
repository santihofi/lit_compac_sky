#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Probe bias sensitivity at uncovered PVT points before a broader code search."""
import json
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
source = ROOT / "verification/porting/sky_input2_quiet_pvt"
target = ROOT / "verification/porting/sky_input2_quiet_bias"
(target / "tb").mkdir(parents=True, exist_ok=True)
(target / "datasheets/sensitivity").mkdir(parents=True, exist_ok=True)
deck = (source / "tb/replica.spice").read_text()
assert deck.count("{{ibias*power_m}}") == 3
deck = deck.replace("{{ibias*power_m}}", "{{ibias*power_m*bias_factor}}")
(target / "tb/replica.spice").write_text(deck)
summary = json.loads((ROOT / "doc/porting/evidence/sky_quiet_codes_pvt_summary.json").read_text())
header = "# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer\n# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1\n"
count = 0
for point in summary["coverage"]:
    if point["dc_covered"]:
        continue
    corner = point["corner_mos"]
    sheet = yaml.safe_load((source / f"datasheets/codes_pvt/quiet_pvt_{corner}.yaml").read_text())
    codes = sorted({0, point["nearest_gain_code"], 31})
    sheet["parameters"].update(temp=[point["temp"]], vdd=[point["vdd"]],
                               gcode=codes, bias_factor=[0.8, 0.9, 1.0, 1.1, 1.2])
    name = f"bias_{corner}_{int(point['temp'])}C_{round(1000*point['vdd'])}mV"
    (target / f"datasheets/sensitivity/{name}.yaml").write_text(header + yaml.safe_dump(sheet, sort_keys=False))
    count += 5 * len(codes)
(target / "settings.json").write_text(json.dumps({"num_cores": 4, "sim_timeout_sec": 600}) + "\n")
(target / "README.md").write_text("""# Quiet-replica bias sensitivity at uncovered PVT points

At each uncovered point, test gain-code endpoints and the earlier nearest-gain code.
Scale both ideal unit-current sources by 0.8, 0.9, 1, 1.1 and 1.2.
The factor-one rows replay the prior exhaustive code sweep.
Other transistor, resistor, reference and trim settings remain unchanged.
This is a sparse sensitivity screen, not exhaustive bias or gain-code coverage.
Any promising bias setting still needs a complete gain-code search and same-code speed, noise and loop checks.
""")
print(f"Prepared {count} sensitivity cases")

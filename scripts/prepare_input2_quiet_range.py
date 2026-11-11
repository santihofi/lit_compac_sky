#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Screen fixed/trim resistor range at difficult PVT and all nominal MOS points."""
import json
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
source = ROOT / "verification/porting/sky_input2_quiet_bias"
pvt = ROOT / "verification/porting/sky_input2_quiet_pvt"
target = ROOT / "verification/porting/sky_input2_quiet_range"
(target / "tb").mkdir(parents=True, exist_ok=True)
(target / "datasheets/endpoints").mkdir(parents=True, exist_ok=True)
(target / "tb/replica.spice").write_text((source / "tb/replica.spice").read_text())
header = "# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer\n# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1\n"
points = [(c, 27, 1.5, 1.0) for c in ["ff", "fs", "sf", "ss", "tt"]]
points += [("fs", 80, v, 0.9) for v in [1.45, 1.5, 1.65]]
points += [("ss", 80, 1.45, 0.9), ("tt", 0, 1.45, 0.9)]
for corner, temp, vdd, bias in points:
    sheet = yaml.safe_load((pvt / f"datasheets/codes_pvt/quiet_pvt_{corner}.yaml").read_text())
    sheet["parameters"].update(temp=[temp], vdd=[vdd], bias_factor=[bias],
                               gcode=[0, 31], rbase_scale=[0.8, 0.9, 1.0],
                               rtrim_scale=[1.0, 1.2, 1.4])
    name = f"range_{corner}_{temp}C_{round(vdd*1000)}mV"
    (target / f"datasheets/endpoints/{name}.yaml").write_text(header + yaml.safe_dump(sheet, sort_keys=False))
(target / "settings.json").write_text(json.dumps({"num_cores": 4, "sim_timeout_sec": 600}) + "\n")
(target / "README.md").write_text("""# Quiet-replica resistor-range endpoint screen

Nine fixed-load and trim-resistance combinations are tested at five nominal MOS points and five difficult PVT points.
Fixed-load factors are 0.8, 0.9 and 1, while trim factors are 1, 1.2 and 1.4.
All use the existing quiet-replica geometry and 1.41 um fixed-load resistor family.
Nominal points retain the earlier ideal bias, while difficult points use the sampled factor 0.9.
Both code endpoints are measured, including the unchanged resistor-network control.
Endpoint gain coverage is only a range diagnostic.
It does not prove an intermediate code satisfying shape, speed, noise and stability.
A selected resistor combination must apply globally before repeating per-PVT calibration.
""")
print("Prepared 180 endpoint cases")

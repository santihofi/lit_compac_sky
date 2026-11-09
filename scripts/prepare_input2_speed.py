#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Screen quad width and bias current at the slow nominal input-2 corner."""
import json
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
base = ROOT / "verification/porting"
target = base / "sky_input2_speed"
(target / "tb").mkdir(parents=True, exist_ok=True)
(target / "datasheets").mkdir(exist_ok=True)
for name, source in [("replica", "sky_trim_tg2"), ("ac", "sky_trim_tg2_ac")]:
    (target / f"tb/{name}.spice").write_text((base / source / f"tb/{name}.spice").read_text())
dc = yaml.safe_load((base / "sky_trim_tg2/datasheets/codes_nominal/tg2_nominal_fs.yaml").read_text())
ac = yaml.safe_load((base / "sky_trim_tg2_ac/datasheets/feasible/tg2_ac_fs.yaml").read_text())
dc["parameters"].update(gcode=[29], quad_scale=[.5, 1, 2], ibias=[27.5e-6, 35e-6, 45e-6])
dc["tests"]["ac"] = ac["tests"]["ac"]
# Keep the quiescent DC current under a single measurement owner.
del dc["tests"]["ac"]["idd"]
header = "# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer\n# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1\n"
(target / "datasheets/speed_fs.yaml").write_text(header + yaml.safe_dump(dc, sort_keys=False))
(target / "settings.json").write_text(json.dumps({"num_cores": 2, "sim_timeout_sec": 600}) + "\n")
(target / "README.md").write_text("""# Input-2 speed sensitivity

This nine-case study retains the transmission-gate trim topology, nominal passives, 100 fF output loads, 1.5 V supply and 27 C.
At the slow nominal SKY130 fs corner it varies quad finger count and ideal unit bias current.
The quad uses two, four or eight 5 um fingers at 0.15 um length, with matching diffusion and dummy-device scaling inherited from the source deck.
Gain code 29 is held fixed for sensitivity measurement, so improved bandwidth is not yet matched-gain qualification.
Each case receives DC gain and shape plus both input AC responses.
The reference combination is quad_scale=1 and ibias=27.5 uA.
Physical bias circuitry, mismatch and loop stability are outside this screen.
""")

#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Check every nominal DC-feasible code of the widened network under both AC loads."""
import json
from pathlib import Path
import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parents[1]
base = ROOT / "verification/porting"
source = base / "sky_input2_quiet_replica"
target = base / "sky_input2_quiet_range14_ac"
(target / "tb").mkdir(parents=True, exist_ok=True)
(target / "datasheets/nominal").mkdir(parents=True, exist_ok=True)
for name in ["replica", "ac", "fanout"]:
    deck = (source / f"tb/{name}.spice").read_text()
    assert deck.count("{{ibias*power_m}}") >= 2
    deck = deck.replace("{{ibias*power_m}}", "{{ibias*power_m*bias_factor}}")
    (target / f"tb/{name}.spice").write_text(deck)
data = pd.read_csv(ROOT / "doc/porting/evidence/sky_quiet_range14.csv")
nominal = data[(data.temp == 27) & (data.vdd == 1.5) & data.dc_screen_pass]
assert set(nominal.corner_mos) == {"ff", "fs", "sf", "ss", "tt"}
header = "# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer\n# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1\n"
for corner, group in nominal.groupby("corner_mos"):
    sheet = yaml.safe_load((source / f"datasheets/nominal/quiet_{corner}.yaml").read_text())
    params = yaml.safe_load((base / f"sky_input2_quiet_range14/datasheets/codes/range_{corner}_27C_1500mV.yaml").read_text())["parameters"]
    params["gcode"] = sorted(map(int, group.gcode))
    sheet["parameters"] = params
    (target / f"datasheets/nominal/ac_{corner}.yaml").write_text(header + yaml.safe_dump(sheet, sort_keys=False))
(target / "settings.json").write_text(json.dumps({"num_cores": 4, "sim_timeout_sec": 600}) + "\n")

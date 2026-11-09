#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Check AC performance at every provisionally DC-feasible nominal TG code."""
import json
from pathlib import Path
import re
import yaml

ROOT = Path(__file__).resolve().parents[1]
base = ROOT / "verification/porting"
source = base / "sky_trim_tg2"
target = base / "sky_trim_tg2_ac"
summary = json.loads((ROOT / "doc/porting/evidence/sky_tg2_codes_nominal_summary.json").read_text())
pattern = r"^\.subckt .*?^\.ends[^\n]*"
definitions = "\n".join(re.findall(pattern, (source / "tb/replica.spice").read_text(), re.M | re.S))
assert len(re.findall(r"^\.subckt ", definitions, re.M)) == 3
deck = re.sub(pattern, "", (base / "sky_replica_ac/tb/ac.spice").read_text(), flags=re.M | re.S)
deck = re.sub(r"^\.end\s*$", lambda _: definitions + "\n.end", deck, flags=re.M)
(target / "tb").mkdir(parents=True, exist_ok=True)
(target / "datasheets/feasible").mkdir(parents=True, exist_ok=True)
(target / "tb/ac.spice").write_text(deck)
header = "# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer\n# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1\n"
for record in summary["coverage"]:
    corner = record["corner_mos"]
    sheet = yaml.safe_load((base / "sky_replica_ac/datasheets/ac.yaml").read_text())
    sheet["parameters"] = yaml.safe_load((source / f"datasheets/codes_nominal/tg2_nominal_{corner}.yaml").read_text())["parameters"]
    sheet["parameters"]["gcode"] = sorted(record["dc_feasible_codes"])
    if not sheet["parameters"]["gcode"]:
        raise ValueError(f"No feasible codes for {corner}")
    (target / f"datasheets/feasible/tg2_ac_{corner}.yaml").write_text(header + yaml.safe_dump(sheet, sort_keys=False))
(target / "settings.json").write_text(json.dumps({"num_cores": 2, "sim_timeout_sec": 600}) + "\n")
(target / "README.md").write_text("""# Transmission-gate feasible-code AC screen

The generator imports the exact three subcircuits from the nominal DC code study.
Every code passing its provisional gain, shape and gate-rail screen receives the same two-input AC and input-capacitance measurements.
Ideal reference currents, complementary gate controls and nominal passive models remain in use.
This experiment does not establish full PVT or physical calibration performance.
""")

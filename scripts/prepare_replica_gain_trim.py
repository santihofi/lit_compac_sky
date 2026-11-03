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

# Retain the historical 1.5 V trim drive and a supply-tracking control separately.
source = ROOT/"verification/porting/ihp_core_tradeoffs"
target = ROOT/"verification/porting/ihp_gain_trim"
(target/"tb").mkdir(parents=True, exist_ok=True)
(target/"datasheets").mkdir(exist_ok=True)
deck = (source/"tb/core.spice").read_text()
lines = []
count = 0
for line in deck.splitlines():
    if line.startswith("Egt"):
        if "1.5*" not in line:
            raise ValueError("Unexpected IHP trim drive")
        line = line.replace("1.5*", "{{'v(vdd)' if gate_tracks_vdd else '1.5'}}*", 1)
        count += 1
    lines.append(line)
if count != 5:
    raise ValueError("Expected five IHP trim drivers")
(target/"tb/core.spice").write_text("\n".join(lines)+"\n")
sheet = yaml.safe_load((source/"datasheets/corners.yaml").read_text())
sheet["parameters"].update(gcode=[0, 31], gate_tracks_vdd=[0, 1])
(target/"datasheets/endpoints.yaml").write_text(header+yaml.safe_dump(sheet,sort_keys=False))
(target/"settings.json").write_text(json.dumps({"num_cores": 2, "sim_timeout_sec": 600})+"\n")

# The code-13 control separates the historical bench rail from the PVT baseline.
midcode = yaml.safe_load((target/"datasheets/endpoints.yaml").read_text())
midcode["parameters"]["gcode"] = [13]
(target/"datasheets/midcode").mkdir(exist_ok=True)
(target/"datasheets/midcode/midcode.yaml").write_text(header+yaml.safe_dump(midcode,sort_keys=False))

for project, template in [
    ("sky_replica_gain_trim", ROOT/"verification/porting/sky_replica_tail/datasheets/nominal.yaml"),
    ("ihp_gain_trim", ROOT/"verification/porting/ihp_core_tradeoffs/datasheets/corners.yaml"),
]:
    p = ROOT/"verification/porting"/project
    sheet = yaml.safe_load(template.read_text())
    sheet["parameters"].update(temp=[27], vdd=[1.5], corner_mos=["tt"], gcode=list(range(32)))
    if project.startswith("ihp"):
        sheet["parameters"]["gate_tracks_vdd"] = [1]
    (p/"datasheets/steps").mkdir(exist_ok=True)
    (p/"datasheets/steps/steps_tt.yaml").write_text(header+yaml.safe_dump(sheet,sort_keys=False))

p = ROOT/"verification/porting/ihp_gain_trim"
lab = p/"datasheets/lab_steps"
lab.mkdir(exist_ok=True)
for corner in ["ff","fs","sf","ss"]:
    sheet=yaml.safe_load((p/"datasheets/steps/steps_tt.yaml").read_text())
    sheet["parameters"]["corner_mos"] = [corner]
    (lab/f"lab_steps_{corner}.yaml").write_text(header+yaml.safe_dump(sheet,sort_keys=False))

#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Separate fixed load resistance from the variable trim range."""
import json
from pathlib import Path
import re

import yaml

ROOT = Path(__file__).resolve().parents[1]
source = ROOT/"verification/porting/sky_replica_tail"
target = ROOT/"verification/porting/sky_replica_trim_range"
(target/"tb").mkdir(parents=True,exist_ok=True)
(target/"datasheets").mkdir(exist_ok=True)
deck = (source/"tb/replica.spice").read_text()
start = deck.index(".subckt gilbert_cell ")
end = deck.index(".ends",start)
core = deck[start:end]
count = 0
lines = []
for line in core.splitlines():
    if re.match(r"^X(?:R7|R5|RD1|RD2) ",line):
        if "*rscale-68.05" not in line:
            raise ValueError("Unexpected fixed load expression")
        line = line.replace("*rscale-68.05","*rscale*rbase_scale-68.05")
        count += 1
    lines.append(line)
if count != 4:
    raise ValueError("Expected two fixed load resistors and their dummies")
deck = deck[:start]+"\n".join(lines)+"\n"+deck[end:]
start = deck.index(".subckt gain_trim ")
end = deck.index(".ends",start)
trim = deck[start:end].replace("*rscale-68.05","*rscale*rtrim_scale-68.05")
deck = deck[:start]+trim+deck[end:]
(target/"tb/replica.spice").write_text(deck)
header="# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer\n# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1\n"
for corner in ["tt","fs"]:
    sheet=yaml.safe_load((source/f"datasheets/calibration/trim_{corner}.yaml").read_text())
    sheet["parameters"].update(temp=[27],vdd=[1.5],gcode=[0,31],
                               rbase_scale=[.8],rtrim_scale=[1,2,4])
    (target/f"datasheets/range_{corner}.yaml").write_text(header+yaml.safe_dump(sheet,sort_keys=False))
(target/"settings.json").write_text(json.dumps({"num_cores":3,"sim_timeout_sec":600})+"\n")

followup = target/"datasheets/centered"
followup.mkdir(exist_ok=True)
for corner in ["tt","ff","fs","sf","ss"]:
    sheet=yaml.safe_load((source/f"datasheets/calibration/trim_{corner}.yaml").read_text())
    sheet["parameters"].update(temp=[22,27],vdd=[1.5],gcode=[0,31],
                               rbase_scale=[.6],rtrim_scale=[2])
    (followup/f"centered_{corner}.yaml").write_text(header+yaml.safe_dump(sheet,sort_keys=False))

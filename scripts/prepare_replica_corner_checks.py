#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Apply the retained fixed current codes to independent replica validation decks."""
from pathlib import Path
import copy
import yaml

ROOT = Path(__file__).resolve().parents[1]
header = "# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer\n# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1\n"
calibration = ROOT / "verification/porting/sky_replica_tail/datasheets/calibration"
for project, nominal, target in [
    ("sky_replica_ac", "ac.yaml", "pvt"),
    ("sky_replica_validation", "stability.yaml", "cmfb_pvt"),
    ("sky_replica_stability", "nominal.yaml", "pvt"),
    ("sky_replica_validation", "transfer.yaml", "surface_corners"),
]:
    directory = ROOT / "verification/porting" / project
    base = yaml.safe_load((directory / "datasheets" / nominal).read_text())
    output = directory / "datasheets" / target
    output.mkdir(exist_ok=True)
    for path in sorted(calibration.glob("*.yaml")):
        current = yaml.safe_load(path.read_text())
        sheet = copy.deepcopy(base)
        sheet["parameters"] = current["parameters"]
        if target == "surface_corners":
            sheet["parameters"]["vdd"] = [1.5]
        name = "surface_" + path.name if target == "surface_corners" else path.name
        (output / name).write_text(header + yaml.safe_dump(sheet, sort_keys=False))

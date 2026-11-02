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

# Match the nominal-supply surface grid on the current IHP reference.
import json
import shutil

source = ROOT / "verification/porting/ihp_core_validation"
target = ROOT / "verification/porting/ihp_surface_corners"
(target / "tb").mkdir(parents=True, exist_ok=True)
(target / "datasheets/surface_corners").mkdir(parents=True, exist_ok=True)
shutil.copy2(source / "tb/transfer.spice", target / "tb/transfer.spice")
sheet = yaml.safe_load((source / "datasheets/transfer.yaml").read_text())
sheet["parameters"]["temp"] = [0, 27, 80]
for corner in ["tt", "ff", "fs", "sf", "ss"]:
    sheet["parameters"]["corner_mos"] = [corner]
    (target / "datasheets/surface_corners" / f"surface_{corner}.yaml").write_text(
        header + yaml.safe_dump(sheet, sort_keys=False))
(target / "settings.json").write_text(json.dumps(
    {"num_cores": 2, "sim_timeout_sec": 600}) + "\n")

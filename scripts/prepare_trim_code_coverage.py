#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Generate exhaustive gain-code screens with explicit per-PVT coverage."""
import argparse
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--grid", choices=["nominal", "pvt"], default="nominal")
args = parser.parse_args()
project = ROOT / "verification/porting/sky_trim_tg2"
header = "# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer\n# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1\n"
folder = project / "datasheets" / ("codes_" + args.grid)
folder.mkdir(parents=True, exist_ok=True)
for corner in ["tt", "ff", "fs", "sf", "ss"]:
    sheet = yaml.safe_load((project / f"datasheets/endpoints/tg2_{corner}.yaml").read_text())
    sheet["parameters"]["gcode"] = list(range(32))
    if args.grid == "pvt":
        sheet["parameters"].update(temp=[0, 27, 80], vdd=[1.45, 1.5, 1.65])
    (folder / f"tg2_{args.grid}_{corner}.yaml").write_text(header + yaml.safe_dump(sheet, sort_keys=False))
print(folder)

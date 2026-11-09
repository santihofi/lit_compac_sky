#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Extend quiet-replica screening to five MOS corners and matched IHP receiver loads."""
import json
from pathlib import Path
import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parents[1]
base = ROOT / "verification/porting"
header = "# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer\n# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1\n"
sky = base / "sky_input2_quiet_replica"
(sky / "datasheets/nominal").mkdir(exist_ok=True)
for corner in ["tt", "ff", "fs", "sf", "ss"]:
    sheet = yaml.safe_load((sky / "datasheets/quiet_fs.yaml").read_text())
    sheet["parameters"] = yaml.safe_load((base / f"sky_input2_candidate/datasheets/nominal6/candidate6_{corner}.yaml").read_text())["parameters"]
    sheet["parameters"]["replica_tracks_signal"] = [0]
    (sky / f"datasheets/nominal/quiet_{corner}.yaml").write_text(header + yaml.safe_dump(sheet, sort_keys=False))
ihp = base / "ihp_input2_quiet_reference"
(ihp / "tb").mkdir(parents=True, exist_ok=True)
(ihp / "datasheets/nominal").mkdir(parents=True, exist_ok=True)
(ihp / "tb/ac.spice").write_text((base / "ihp_input2_fanout/tb/ac.spice").read_text())
calibration = pd.read_csv(ROOT / "doc/porting/evidence/ihp_calibrated_pvt.csv")
for corner, group in calibration.groupby("corner_mos"):
    codes = group.gcode.unique()
    assert len(codes) == 1
    sheet = yaml.safe_load((base / "ihp_core_fanout/datasheets/ac.yaml").read_text())
    sheet["parameters"].update(corner_mos=[corner], gcode=[int(codes[0])], fanout_input=[1], c_load=["25f"])
    (ihp / f"datasheets/nominal/quiet_reference_{corner}.yaml").write_text(header + yaml.safe_dump(sheet, sort_keys=False))
(ihp / "settings.json").write_text(json.dumps({"num_cores": 2, "sim_timeout_sec": 600}) + "\n")
(ihp / "README.md").write_text("""# IHP receiver-load reference for quiet-replica comparison

Each nominal MOS corner uses its earlier nearest K100 code.
The driver feeds input 1 of an identical receiver, with 25 fF wire capacitance per output.
SKY130 fs/sf labels must be reversed when joining this reference.
""")

#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Measure output-load relief from parallel copies with narrow fixed loads."""
import json
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
base = ROOT / "verification/porting"
source = base / "sky_input2_load_resistors"
target = base / "sky_input2_parallel"
(target / "tb").mkdir(parents=True, exist_ok=True)
(target / "datasheets").mkdir(exist_ok=True)
for name in ["replica", "ac"]:
    (target / f"tb/{name}.spice").write_text((source / f"tb/{name}.spice").read_text())
sheet = yaml.safe_load((source / "datasheets/load_fs.yaml").read_text())
sheet["parameters"].update(load_family=["1p41"], power_m=[2, 4, 6])
header = "# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer\n# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1\n"
(target / "datasheets/parallel_fs.yaml").write_text(header + yaml.safe_dump(sheet, sort_keys=False))
(target / "settings.json").write_text(json.dumps({"num_cores": 2, "sim_timeout_sec": 600}) + "\n")
(target / "README.md").write_text("""# Parallel-copy input-2 speed control

This study varies two, four and six parallel circuit copies while retaining 100 fF per output.
All circuit MOS devices, resistor parallel multiplicities and both ideal reference currents scale together.
The fixed loads use the nominally resistance-matched 1.41 um precision-poly family.
The expected DC invariance is checked against the two-copy load-family study.
Increased speed must be reported with total supply current and input capacitance.
This is not a low-power optimization or physical-layout qualification.
""")

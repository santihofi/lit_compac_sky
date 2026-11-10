#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Test the remaining nominal SS code choices against loaded bandwidth."""
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
project = ROOT / "verification/porting/sky_input2_quiet_replica"
folder = project / "datasheets/codes"
folder.mkdir(exist_ok=True)
sheet = yaml.safe_load((project / "datasheets/nominal/quiet_ss.yaml").read_text())
sheet["parameters"]["gcode"] = [14, 15, 16]
header = "# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer\n# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1\n"
(folder / "quiet_ss_codes.yaml").write_text(header + yaml.safe_dump(sheet, sort_keys=False))

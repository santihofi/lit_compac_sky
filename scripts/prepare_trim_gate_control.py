#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Separate trim-switch gate drive from circuit supply as a causal control."""
import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
base = ROOT / "verification/porting"
header = "# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer\n# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1\n"
for suffix, bench in [("dc", "replica"), ("ac", "ac")]:
    source = base / ("sky_centered_" + suffix)
    target = base / ("sky_trim_gate_" + suffix)
    (target / "tb").mkdir(parents=True, exist_ok=True)
    (target / "datasheets").mkdir(exist_ok=True)
    lines, count = [], 0
    for line in (source / "tb" / (bench + ".spice")).read_text().splitlines():
        if line.startswith("Egt"):
            if "v(vdd)*" not in line:
                raise ValueError("Unexpected trim driver")
            line = line.replace("v(vdd)*", "{{trim_high}}*", 1)
            count += 1
        lines.append(line)
    if count != 5:
        raise ValueError("Expected five gate drivers")
    (target / "tb" / (bench + ".spice")).write_text("\n".join(lines) + "\n")
    sheet = yaml.safe_load((source / "datasheets/pvt/calibrated_sf.yaml").read_text())
    sheet["parameters"].update(vdd=[1.45], temp=[0,27], trim_high=[1.45,1.5,1.65])
    (target / "datasheets/control.yaml").write_text(header + yaml.safe_dump(sheet, sort_keys=False))
    (target / "settings.json").write_text(json.dumps({"num_cores": 2, "sim_timeout_sec": 600}) + "\n")
    (target / "README.md").write_text("""# Independent trim-drive diagnostic

This control holds the wider candidate at sf, 1.45 V and gain code 10, then varies only the ideal high rail of its five trim drivers.
The 1.45 V setting reproduces the circuit-supply-driven case.
The 1.5 V and 1.65 V settings deliberately separate switch drive from circuit supply.
Those over-rail settings diagnose sensitivity and are not proposed chip interfaces.
All transistor dimensions, loads and ideal bias currents stay fixed.
""")

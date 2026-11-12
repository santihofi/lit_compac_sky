#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Probe active input-pair loading with exact replica fingers and fixed dummy loading."""
import json
import math
from pathlib import Path
import re
import yaml

ROOT = Path(__file__).resolve().parents[1]
base = ROOT / "verification/porting"
source = base / "sky_input2_trim_ss_bias_ac"
target = base / "sky_input2_pair_width"
(target / "tb").mkdir(parents=True, exist_ok=True)
(target / "datasheets").mkdir(exist_ok=True)
scales = [2 / 3, 1.]
for scale in scales:
    for count in [12 * scale, 12 * scale * 6 / 8]:
        assert math.isclose(count, round(count), abs_tol=1e-12)
for name in ["replica", "ac", "fanout"]:
    deck = (source / f"tb/{name}.spice").read_text()
    # Retain the original four-finger dummy while scaling only active pair devices.
    deck, count = re.subn(r"(?m)^XMDP .+\n\+ .+",
                         lambda m: m[0].replace("pair_scale", "1"), deck)
    assert count == 1
    (target / f"tb/{name}.spice").write_text(deck)
sheet = yaml.safe_load((source / "datasheets/nominal/bias_0p9.yaml").read_text())
sheet["parameters"]["pair_scale"] = scales
header = "# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer\n# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1\n"
(target / "datasheets/pair_ss.yaml").write_text(header + yaml.safe_dump(sheet, sort_keys=False))
(target / "settings.json").write_text(json.dumps({"num_cores": 4, "sim_timeout_sec": 600}) + "\n")
(target / "README.md").write_text("""# Active input-pair width with fixed dummy loading

At SS, 27 C, 1.5 V and bias factor 0.9, compare pair scales 2/3 and 1 at codes 10 and 11.
The main pair has eight or twelve fingers and the one-eighth replica has six or nine fingers with six circuit copies.
XMDP retains its original four fingers and width, preventing fractional dummy geometry and keeping its absolute loading fixed.
The identical downstream receiver uses the same active-pair width.
All other geometry, current sources and resistor factors remain unchanged.
The scale-one cases must reproduce the preceding circuit.
This is fixed-code sensitivity, not matched-gain calibration or physical sign-off.
""")

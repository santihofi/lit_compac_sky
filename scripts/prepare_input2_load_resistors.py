#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Compare equal nominal resistance with smaller precision-poly load geometries."""
import hashlib
import json
from pathlib import Path
import re
import yaml

ROOT = Path(__file__).resolve().parents[1]
base = ROOT / "verification/porting"
target = base / "sky_input2_load_resistors"
(target / "tb").mkdir(parents=True, exist_ok=True)
(target / "datasheets").mkdir(exist_ok=True)
models = Path("/foss/pdks/sky130A/libs.ref/sky130_fd_pr/spice")
# At 27 C and zero resistor differential voltage, R = rcon + rsheet*L + A/L.
families = {
    "5p73": {"rcon": 68.05, "rsheet": 56.46, "a": 0.0},
    "2p85": {"rcon": 130.36, "rsheet": 113.56,
             "a": 130.36 * 1.425 * (1 - .00936 * (27-30)) *
                  (.0147 * -1.6 + .136 * (-1.6)**2 + .0529 * (-1.6)**3)},
    "1p41": {"rcon": 254.77, "rsheet": 230.05,
             "a": 254.77 * .705 * (1 - .00468 * (27-30)) *
                  (-.0762 * -1.4 + .198 * (-1.4)**2 + .0881 * (-1.4)**3)},
}
for family, values in families.items():
    model = models / f"sky130_fd_pr__res_high_po_{family}.model.spice"
    content = model.read_text()
    for key in ["rcon", "rsheet"]:
        found = float(re.search(rf"\b{key}\s*=\s*([0-9.]+)", content)[1])
        if found != values[key]:
            raise ValueError(f"Changed {family} {key}")
    values["model_sha256"] = hashlib.sha256(model.read_bytes()).hexdigest()
prefix = "{% set rc = " + repr({k:v["rcon"] for k,v in families.items()}) + "[load_family] %}\n"
prefix += "{% set rs = " + repr({k:v["rsheet"] for k,v in families.items()}) + "[load_family] %}\n"
prefix += "{% set aa = " + repr({k:v["a"] for k,v in families.items()}) + "[load_family] %}\n"
prefix += "{% set wanted_r = (68.05+56.46*13.035)*rscale*rbase_scale %}\n"
length = "((wanted_r-rc)+((wanted_r-rc)**2-4*rs*aa)**0.5)/(2*rs)"
for name, source in [("replica", "sky_trim_tg2"), ("ac", "sky_trim_tg2_ac")]:
    deck = (base / source / f"tb/{name}.spice").read_text()
    lines, changed = [], 0
    for line in deck.splitlines():
        if line.startswith(("XR7 ", "XR5 ", "XRD1 ", "XRD2 ")):
            line = line.replace("sky130_fd_pr__res_high_po_5p73",
                                "sky130_fd_pr__res_high_po_{{load_family}}")
            line = re.sub(r"L=\{\{.*?\}\}", "L={{" + length + "}}", line)
            changed += 1
        lines.append(line)
    assert changed == 4
    (target / f"tb/{name}.spice").write_text(prefix + "\n".join(lines) + "\n")
sheet = yaml.safe_load((base / "sky_input2_speed/datasheets/speed_fs.yaml").read_text())
sheet["parameters"].update(quad_scale=[1], ibias=[27.5e-6], load_family=list(families))
header = "# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer\n# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1\n"
(target / "datasheets/load_fs.yaml").write_text(header + yaml.safe_dump(sheet, sort_keys=False))
(target / "settings.json").write_text(json.dumps({"num_cores": 1, "sim_timeout_sec": 600}) + "\n")
(target / "mapping.json").write_text(json.dumps(families, indent=2) + "\n")
(target / "README.md").write_text("""# Equal-resistance load geometry screen

Only the two fixed core loads and their two dummy resistors change family.
Their target zero-voltage resistance is matched at 27 C using the installed model's end and body expressions.
The longer positive quadratic root is used for the two narrower families.
The trim segments and source resistors retain the 5.73 um family.
This is a nominal model-level geometry screen with continuous lengths, not layout or mismatch qualification.
A 5.73 um replay control must reproduce the earlier design.
The narrower families have different voltage coefficients and statistical behavior, so matching resistance does not imply interchangeable devices.
""")

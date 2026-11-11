#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Compare resistance-matched trim poly families on the widened-network FS codes."""
import hashlib
import json
from pathlib import Path
import re
import yaml

ROOT = Path(__file__).resolve().parents[1]
base = ROOT / "verification/porting"
source = base / "sky_input2_quiet_range14_ac"
target = base / "sky_input2_quiet_trim_poly"
(target / "tb").mkdir(parents=True, exist_ok=True)
(target / "datasheets").mkdir(parents=True, exist_ok=True)
mapping = json.loads((base / "sky_input2_load_resistors/mapping.json").read_text())
families = {key: mapping[key] for key in ["5p73", "2p85"]}
models = Path("/foss/pdks/sky130A/libs.ref/sky130_fd_pr/spice")
for family, values in families.items():
    model = models / f"sky130_fd_pr__res_high_po_{family}.model.spice"
    assert hashlib.sha256(model.read_bytes()).hexdigest() == values["model_sha256"]
prefix = ""
for variable, field in [("trc", "rcon"), ("trs", "rsheet"), ("taa", "a")]:
    prefix += "{% set " + variable + " = " + repr({k: v[field] for k, v in families.items()}) + "[trim_family] %}\n"
for name in ["replica", "ac", "fanout"]:
    deck = (source / f"tb/{name}.spice").read_text()
    start = deck.index(".subckt gain_trim ")
    end = deck.index(".ends", start)
    block = deck[start:end]
    count = 0
    for old_length in ["0.875", "10.76"]:
        before = "{{((68.05+56.46*" + old_length + ")*rscale*rtrim_scale-68.05)/56.46}}"
        wanted = "((68.05+56.46*" + old_length + ")*rscale*rtrim_scale)"
        after = "{{((" + wanted + "-trc)+((" + wanted + "-trc)**2-4*trs*taa)**0.5)/(2*trs)}}"
        count += block.count(before)
        block = block.replace(before, after)
    assert count == 35, count
    assert block.count("sky130_fd_pr__res_high_po_5p73") == 35
    block = block.replace("sky130_fd_pr__res_high_po_5p73", "sky130_fd_pr__res_high_po_{{trim_family}}")
    deck = prefix + deck[:start] + block + deck[end:]
    (target / f"tb/{name}.spice").write_text(deck)
sheet = yaml.safe_load((source / "datasheets/nominal/ac_fs.yaml").read_text())
sheet["parameters"]["trim_family"] = ["5p73", "2p85"]
header = "# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer\n# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1\n"
(target / "datasheets/trim_fs.yaml").write_text(header + yaml.safe_dump(sheet, sort_keys=False))
(target / "datasheets/corners").mkdir(exist_ok=True)
for path in sorted((source / "datasheets/nominal").glob("*.yaml")):
    corner_sheet = yaml.safe_load(path.read_text())
    corner_sheet["parameters"]["trim_family"] = ["5p73", "2p85"]
    name = "trim_" + corner_sheet["parameters"]["corner_mos"][0] + ".yaml"
    (target / "datasheets/corners" / name).write_text(header + yaml.safe_dump(corner_sheet, sort_keys=False))
(target / "settings.json").write_text(json.dumps({"num_cores": 4, "sim_timeout_sec": 600}) + "\n")
(target / "mapping.json").write_text(json.dumps(families, indent=2) + "\n")
(target / "README.md").write_text("""# Resistance-matched narrow trim poly control

Only the gain-trim subcircuit's 32 segment devices and three dummies change poly family.
Both widths match the target zero-voltage unit resistance at 27 C using the installed end-corrected model and longer positive quadratic root.
The widened trim unit is large enough for a positive 2.85 um family length.
The 1.41 um fixed core loads, source resistors, switches, transistor geometry, currents and codes remain unchanged.
Two 5.73 um cases replay the previous FS nominal codes.
The identical receiver uses the same candidate trim family.
These are continuous model lengths, not layout or mismatch qualification.
Resistance matching alone does not preserve voltage coefficient, temperature coefficient or shape.
""")

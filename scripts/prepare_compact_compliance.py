#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Isolate pair body effect and tail output conductance at PVT extremes."""
from pathlib import Path
import json
import re
import yaml

ROOT = Path(__file__).resolve().parents[1]
src = ROOT / "verification/porting/sky_compact_loads"
dst = ROOT / "verification/porting/sky_compact_compliance"
(dst / "tb").mkdir(parents=True, exist_ok=True)
(dst / "datasheets").mkdir(exist_ok=True)
deck = (src / "tb/loads.spice").read_text()
control = re.search(r"\.control\b(.*?)\.endc", deck, re.S)[1]
control = control[:control.index("set dc_k100=")]
control = control.replace("let idd=-i(vdd)",
    "let idd=-i(vdd)\nlet tail_current=abs(@m.x1.xm13.msky130_fd_pr__pfet_01v8_lvt[id])")
control += "let tail_current=op1.tail_current\nquit\n"
deck = re.sub(r"\.control\b.*?\.endc", lambda m: ".control" + control + ".endc", deck, flags=re.S)
start = deck.index(".subckt gilbert_cell ")
end = deck.index(".ends", start)

def change_device(match):
    line = match[0]
    name = line.split()[0]
    if name in {"XM13", "XM14", "XMDT"}:
        line = line.replace("L=0.65", "L={{0.65*tail_length_scale}}")
        line = line.replace("tail_width", "(tail_width*tail_length_scale)")
    if name in {"XM1", "XM2", "XMDP"}:
        source = {"XM1": "ps1", "XM2": "ps2", "XMDP": "vcm1"}[name]
        line = line.replace(" ntap sky130", " {{'" + source + "' if pair_body_tied else 'ntap'}} sky130", 1)
    return line

body = re.sub(r"^XM\S+ [^\n]+(?:\n\+[^\n]+)*", change_device, deck[start:end], flags=re.M)
deck = deck[:start] + body + deck[end:]
(dst / "tb/compliance.spice").write_text(deck)
sheet = yaml.safe_load((src / "datasheets/nominal.yaml").read_text())
metrics = yaml.safe_load((ROOT / "verification/porting/sky_pair_degenerated/datasheets/calibration_probe.yaml").read_text())["tests"]["curvature"]
sheet["tests"] = {"compliance": {**metrics, "tail_current": {}}}
sheet["parameters"].update(temp=[0, 80], vdd=[1.45, 1.65],
                           tail_length_scale=[1, 2], pair_body_tied=[0, 1])
header = "# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer\n# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1\n"
for corner, current in [("ss", 43.75e-6), ("sf", 38.75e-6)]:
    sheet["parameters"].update(corner_mos=[corner], ibias=[current])
    (dst / f"datasheets/{corner}.yaml").write_text(header + yaml.safe_dump(sheet, sort_keys=False))
(dst / "settings.json").write_text(json.dumps({"num_cores": 2, "sim_timeout_sec": 180}) + "\n")

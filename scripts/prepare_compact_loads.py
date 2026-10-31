#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Reduce PMOS load capacitance in the compact doubly degenerated candidate."""
from pathlib import Path
import json
import re
import yaml

ROOT = Path(__file__).resolve().parents[1]
src = ROOT / "verification/porting/sky_compact_pair"
dst = ROOT / "verification/porting/sky_compact_loads"
(dst / "tb").mkdir(parents=True, exist_ok=True)
(dst / "datasheets").mkdir(exist_ok=True)
deck = (src / "tb/compact.spice").read_text()
for subckt, names in [
    ("gilbert_cell", {"XM11", "XM12", "XMDL"}),
    ("ota", {"XM5", "XM6"}),
]:
    start = deck.index(".subckt " + subckt + " ")
    end = deck.index(".ends", start)

    def resize(match):
        line = match[0]
        if line.split()[0] not in names:
            return line
        width = float(re.search(r"\bW=(\S+)", line)[1])
        nf = int(re.search(r"\bnf=(\S+)", line)[1])
        finger = f"({width/nf}*pload_l)"
        params = {
            "L": "pload_l", "W": f"{width}*pload_l",
            "ad": f"{(nf+1)//2}*{finger}*0.29",
            "as": f"{(nf+2)//2}*{finger}*0.29",
            "pd": f"{2*((nf+1)//2)}*({finger}+0.29)",
            "ps": f"{2*((nf+2)//2)}*({finger}+0.29)",
            "nrd": f"0.29/({width}*pload_l)", "nrs": f"0.29/({width}*pload_l)",
        }
        for key, value in params.items():
            line = re.sub(r"\b" + key + r"=(?:{{.*?}}|\S+)",
                          key + "={{" + value + "}}", line)
        return line

    body = re.sub(r"^XM\S+ [^\n]+(?:\n\+[^\n]+)*", resize, deck[start:end], flags=re.M)
    deck = deck[:start] + body + deck[end:]
(dst / "tb/loads.spice").write_text(deck)
sheet = yaml.safe_load((src / "datasheets/sizing.yaml").read_text())
sheet["parameters"].update(
    mirror_l=[.25, .3], quad_scale=[1], rquad=[120], pload_l=[.35, .5, 1])
sheet["tests"] = {"loads": sheet["tests"]["compact"]}
header = "# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer\n# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1\n"
(dst / "datasheets/sizing.yaml").write_text(header + yaml.safe_dump(sheet, sort_keys=False))
(dst / "settings.json").write_text(json.dumps({"num_cores": 2, "sim_timeout_sec": 180}) + "\n")

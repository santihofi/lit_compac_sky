#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Quantize the selected replica geometry and retain every changed dimension."""
from decimal import Decimal, ROUND_HALF_UP
import json
from pathlib import Path
import re

import yaml

ROOT = Path(__file__).resolve().parents[1]
source = ROOT/"verification/porting/sky_replica_schematic"
target = ROOT/"verification/porting/sky_replica_grid"
(target/"tb").mkdir(parents=True, exist_ok=True)
(target/"datasheets").mkdir(exist_ok=True)
grid = Decimal("0.005")


def snap(value):
    return float((Decimal(str(value))/grid).quantize(Decimal(1), rounding=ROUND_HALF_UP)*grid)


changes = []
definitions = "\n".join(re.findall(r"^\.subckt .*?^\.ends[^\n]*",
                                  (source/"golden.spice").read_text(), re.M | re.S))
definitions = re.sub(r"\n\+\s*", " ", definitions)
lines = []
cell = ""
for line in definitions.splitlines():
    if line.startswith(".subckt"):
        cell = line.split()[1]
    if " sky130_fd_pr__" not in line:
        lines.append(line)
        continue
    tokens = line.split()
    index = next(i for i, token in enumerate(tokens) if token.startswith("sky130_fd_pr__"))
    model = tokens[index]
    props = dict(token.split("=", 1) for token in tokens[index+1:])
    before = dict(props)
    props["L"] = format(snap(props["L"]), ".12g")
    if "fet_" in model:
        nf = int(props["nf"])
        width = snap(float(props["W"])/nf)
        props["W"] = format(width*nf, ".12g")
        if float(props["W"]) != float(before["W"]):
            for key, val in dict(ad=((nf+1)//2)*width*.29,
                                 as_=((nf+2)//2)*width*.29,
                                 pd=2*((nf+1)//2)*(width+.29),
                                 ps=2*((nf+2)//2)*(width+.29),
                                 nrd=.29/(nf*width), nrs=.29/(nf*width)).items():
                props["as" if key == "as_" else key] = format(val, ".16g")
    modified = {k: {"before": before[k], "after": v} for k, v in props.items()
                if float(before[k]) != float(v)}
    if modified:
        changes.append({"cell": cell, "instance": tokens[0], "model": model,
                        "parameters": modified})
    lines.append(" ".join(tokens[:index+1])+" "+" ".join(f"{k}={v}" for k,v in props.items()))
definitions = "\n".join(lines)
(target/"geometry_changes.json").write_text(json.dumps(
    {"grid_um": float(grid), "changed_instances": len(changes), "changes": changes}, indent=2)+"\n")
header = "# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer\n# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1\n"
for project, sheet_name, name in [
    ("sky_replica_tail", "nominal", "replica"),
    ("sky_replica_ac", "ac", "ac"),
    ("sky_replica_validation", "noise", "noise"),
    ("sky_replica_validation", "transfer", "transfer"),
]:
    src = ROOT/"verification/porting"/project
    deck = (src/"tb"/(name+".spice")).read_text()
    deck = re.sub(r"^\.subckt .*?^\.ends[^\n]*", "", deck, flags=re.M | re.S)
    deck = re.sub(r"^\.end\s*$", lambda m: definitions+"\n.end", deck, flags=re.M)
    (target/"tb"/(name+".spice")).write_text(deck)
    sheet = yaml.safe_load((src/"datasheets"/(sheet_name+".yaml")).read_text())
    (target/"datasheets"/(name+".yaml")).write_text(header+yaml.safe_dump(sheet,sort_keys=False))
(target/"settings.json").write_text(json.dumps({"num_cores": 1, "sim_timeout_sec": 600})+"\n")
print("Quantized instances:", len(changes))

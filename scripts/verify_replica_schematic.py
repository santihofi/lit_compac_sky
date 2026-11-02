#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Netlist the drawn candidate, prove equivalence and prepare Chipify replays."""
import copy
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

import yaml
from jinja2 import Environment, StrictUndefined

from check_replica_schematic import circuits, compare

if os.environ.get("PDK") != "sky130A":
    raise SystemExit("Select sky130A with the project .designinit before netlisting")

ROOT = Path(__file__).resolve().parents[1]
project = ROOT / "verification/porting/sky_replica_schematic"
schematic = project / "schematic"
netlist = project / "netlist"
netlist.mkdir(exist_ok=True)
outputs = []
with tempfile.TemporaryDirectory(prefix="sky-replica-xschem-") as scratch:
    for name in ["gilbert_cell", "ota"]:
        command = ["xschem", "-n", "-q", "-x", "-r", "--rcfile", str(schematic/"xschemrc"),
                   "--tcl", "set top_is_subckt 1", "-o", scratch, str(schematic/(name+".sch"))]
        run = subprocess.run(command, cwd=schematic, text=True, capture_output=True, timeout=60)
        output = Path(scratch) / (name+".spice")
        if not output.is_file() or re.search(r"Error:|IS MISSING", run.stdout+run.stderr):
            raise ValueError("Xschem rejected " + name + "\n" + run.stdout + run.stderr)
        text = output.read_text()
        outputs.append(text)
        (netlist/(name+".spice")).write_text(text.replace(str(ROOT), "."))
drawn_text = "\n".join(outputs)
golden = circuits((project/"golden.spice").read_text())
drawn = circuits(drawn_text)
report = compare(golden, drawn)
# A wrong bulk and a wrong width must fail independently of the drawing.
for mutation in ["bulk", "width"]:
    changed = copy.deepcopy(drawn)
    nodes, model, props = changed["gilbert_cell"][1]["xm7"]
    if mutation == "bulk":
        nodes[3] = "outp"
    else:
        props["w"] = str(float(props["w"])*1.01)
    try:
        compare(golden, changed)
    except ValueError:
        pass
    else:
        raise ValueError("Equivalence checker accepted " + mutation + " mutant")
report["rejected_negative_controls"] = ["quad_bulk_short", "quad_width_plus_one_percent"]
(project/"equivalence.json").write_text(json.dumps(report, indent=2)+"\n")

# Preserve the drawn subcircuits in each independent measurement bench.
definitions = "\n".join(re.findall(r"^\.subckt .*?^\.ends[^\n]*", drawn_text, re.M | re.S))
replay = project/"replay"
(replay/"tb").mkdir(parents=True, exist_ok=True)
(replay/"datasheets").mkdir(exist_ok=True)
header = "# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer\n# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1\n"
for src, sheet_name, name in [
    ("sky_replica_tail", "nominal", "replica"),
    ("sky_replica_ac", "ac", "ac"),
    ("sky_replica_validation", "noise", "noise"),
    ("sky_replica_validation", "transfer", "transfer"),
    ("sky_replica_validation", "stability", "stability"),
]:
    source = ROOT/"verification/porting"/src
    sheet = yaml.safe_load((source/"datasheets"/(sheet_name+".yaml")).read_text())
    params = {k: v[0] if isinstance(v, list) else 0 if k == "seed" else v
              for k, v in sheet["parameters"].items()}
    deck = Environment(undefined=StrictUndefined).from_string(
        (source/"tb"/(name+".spice")).read_text()).render(**params)
    deck = re.sub(r"^\.subckt .*?^\.ends[^\n]*", "", deck, flags=re.M | re.S)
    deck = re.sub(r"^\.end\s*$", lambda m: definitions+"\n.end", deck, flags=re.M)
    (replay/"tb"/(name+".spice")).write_text(deck)
    (replay/"datasheets"/(name+".yaml")).write_text(header+yaml.safe_dump(sheet,sort_keys=False))
(replay/"settings.json").write_text(json.dumps({"num_cores": 1, "sim_timeout_sec": 600})+"\n")
print(json.dumps(report, indent=2))

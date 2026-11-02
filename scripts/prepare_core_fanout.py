#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Compare bare cores driving the actual input of a second identical core."""
import argparse
import json
from pathlib import Path
import re
import subprocess
import sys

import yaml

ROOT = Path(__file__).resolve().parents[1]
header = "# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer\n# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1\n"
parser = argparse.ArgumentParser()
parser.add_argument("--source", help="Generate only this source project")
args = parser.parse_args()
for src, sheet, name in [
    ("ihp_input_capacitance", "nominal.yaml", "ihp_core_fanout"),
    ("sky_compact_loads", "nominal.yaml", "sky_compact_fanout"),
    ("sky_replica_tail", "nominal.yaml", "sky_replica_fanout"),
]:
    if args.source and args.source != src:
        continue
    subprocess.run([sys.executable, str(ROOT / "scripts/prepare_core_ac.py"),
                    "--project", src, "--sheet", sheet, "--out", name], check=True)
    project = ROOT / "verification/porting" / name
    path = project / "tb/ac.spice"
    deck = path.read_text()
    core_ports = re.search(r"^\.subckt gilbert_cell (.+)$", deck, re.M)[1].split()
    ota_ports = re.search(r"^\.subckt ota (.+)$", deck, re.M)[1].split()
    core_nodes = {
        "vdd": "rvdd", "vbias": "rvbias", "outp": "routp", "outn": "routn",
        "vss": "GND", "ibias": "ribias", "ntap": "rvdd", "ptap": "GND",
        "vcm": "rvcm_sense", **{f"gt{i}": f"gt{i}" for i in range(5)},
    }
    for number in (1, 2):
        for sign in ("p", "n"):
            core_nodes[f"in{number}{sign}"] = (
                "{{'out" + sign + "' if fanout_input==" + str(number) +
                " else 'other" + sign + "'}}")
    ota_nodes = dict(vdd="rvdd", out="rvbias", inn="vref", inp="rvcm_sense",
                     vss="GND", ibias1="ribias_ota", ntap="rvdd", ptap="GND")
    bias = re.search(r"^I0 ibias GND (.+)$", deck, re.M)[1]
    extra = [
        "Vreceiver rvdd GND {{vdd}}",
        "Votherp otherp vcmi 0.05", "Vothern othern vcmi -0.05",
        f"Ireceiver ribias GND {bias}", f"Ireceiver_ota rvdd ribias_ota {bias}",
        "xreceiver " + " ".join(core_nodes[p] for p in core_ports) + " gilbert_cell",
        "xreceiver_cmfb " + " ".join(ota_nodes[p] for p in ota_ports) + " ota",
        "Creceiverp routp GND 100f", "Creceivern routn GND 100f",
    ]
    deck = deck.replace("\n.control", "\n" + "\n".join(extra) + "\n.control", 1)
    path.write_text(deck)
    sheet_path = project / "datasheets/ac.yaml"
    config = yaml.safe_load(sheet_path.read_text())
    config["parameters"].update(fanout_input=[1, 2], c_load=["25f", "50f"])
    sheet_path.write_text(header + yaml.safe_dump(config, sort_keys=False))
    (project / "settings.json").write_text(json.dumps({"num_cores": 1, "sim_timeout_sec": 180}) + "\n")

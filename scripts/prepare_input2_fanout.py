#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Compare slow-corner receiver-loaded bandwidth with matched nominal calibration."""
import json
from pathlib import Path
import re
import yaml

ROOT = Path(__file__).resolve().parents[1]
base = ROOT / "verification/porting"
header = "# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer\n# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1\n"
target = base / "sky_input2_fanout6"
(target / "tb").mkdir(parents=True, exist_ok=True)
(target / "datasheets").mkdir(exist_ok=True)
deck = (base / "sky_input2_candidate/tb/ac.spice").read_text()
core_ports = re.search(r"^\.subckt gilbert_cell (.+)$", deck, re.M)[1].split()
ota_ports = re.search(r"^\.subckt ota (.+)$", deck, re.M)[1].split()
nodes = {"vdd": "rvdd", "vbias": "rvbias", "outp": "routp", "outn": "routn",
         "vss": "GND", "ibias": "ribias", "ntap": "rvdd", "ptap": "GND",
         "vcm": "rvcm_sense", **{f"gt{i}": f"gt{i}" for i in range(5)}}
for number in [1, 2]:
    for sign in ["p", "n"]:
        nodes[f"in{number}{sign}"] = "{{'out" + sign + "' if fanout_input==" + str(number) + " else 'other" + sign + "'}}"
ota_nodes = dict(vdd="rvdd", out="rvbias", inn="vref", inp="rvcm_sense",
                 vss="GND", ibias1="ribias_ota", ntap="rvdd", ptap="GND")
bias = re.search(r"^I0 ibias GND (.+)$", deck, re.M)[1]
extra = [
    "Vreceiver rvdd GND {{vdd}}", "Votherp otherp vcmi 0.05", "Vothern othern vcmi -0.05",
    f"Ireceiver ribias GND {bias}", f"Ireceiver_ota rvdd ribias_ota {bias}",
    "xreceiver " + " ".join(nodes[p] for p in core_ports) + " gilbert_cell",
    "xreceiver_cmfb " + " ".join(ota_nodes[p] for p in ota_ports) + " ota",
    "Creceiverp routp GND 100f", "Creceivern routn GND 100f",
]
deck = deck.replace("\n.control", "\n" + "\n".join(extra) + "\n.control", 1)
(target / "tb/ac.spice").write_text(deck)
sheet = yaml.safe_load((base / "sky_input2_candidate/datasheets/nominal6/candidate6_fs.yaml").read_text())
sheet["tests"] = {"ac": sheet["tests"]["ac"]}
sheet["tests"]["ac"]["idd"] = {}
sheet["parameters"].update(power_m=[2, 6], fanout_input=[1, 2], c_load=["25f", "50f"])
(target / "datasheets/fanout_fs.yaml").write_text(header + yaml.safe_dump(sheet, sort_keys=False))
(target / "settings.json").write_text(json.dumps({"num_cores": 2, "sim_timeout_sec": 600}) + "\n")
(target / "README.md").write_text("""# Slow-corner receiver-loaded bandwidth

The driver feeds input 1 or input 2 of an identical core with its own ideal supplies and CMFB.
The unused receiver input has 100 mV differential bias.
Wire capacitance is 25 or 50 fF per driver output, and receiver outputs have 100 fF each.
Two-copy and six-copy SKY130 variants scale both driver and receiver together.
The IHP comparison uses raw sf, corresponding to raw SKY130 fs, and its nearest nominal gain code 12.
Driver current is measured separately from the receiver supply.
""")
target = base / "ihp_input2_fanout"
(target / "tb").mkdir(parents=True, exist_ok=True)
(target / "datasheets").mkdir(exist_ok=True)
(target / "tb/ac.spice").write_text((base / "ihp_core_fanout/tb/ac.spice").read_text())
sheet = yaml.safe_load((base / "ihp_core_fanout/datasheets/ac.yaml").read_text())
sheet["parameters"].update(corner_mos=["sf"], gcode=[12])
(target / "datasheets/fanout_sf.yaml").write_text(header + yaml.safe_dump(sheet, sort_keys=False))
(target / "settings.json").write_text(json.dumps({"num_cores": 2, "sim_timeout_sec": 600}) + "\n")
(target / "README.md").write_text("Matched IHP slow-N/fast-P receiver-loading control at nominal voltage and temperature.\n")

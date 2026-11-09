#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Test a common-mode-biased replica against signal tracking and receiver loading."""
import json
from pathlib import Path
import re
import yaml

ROOT = Path(__file__).resolve().parents[1]
base = ROOT / "verification/porting"
target = base / "sky_input2_quiet_replica"
(target / "tb").mkdir(parents=True, exist_ok=True)
(target / "datasheets").mkdir(exist_ok=True)
source = base / "sky_input2_candidate"
for name in ["replica", "ac"]:
    deck = (source / f"tb/{name}.spice").read_text()
    deck, ports = re.subn(r"(?m)^(\.subckt gilbert_cell .+)$", r"\1 replica_cm", deck)
    deck, instances = re.subn(r"(?m)^(x1 .+) gilbert_cell$", r"\1 vref gilbert_cell", deck)
    assert ports == instances == 1
    for number, gate in [(1, "in1n"), (2, "in1p")]:
        before = f"XMrep{number} ibias {gate} "
        after = f"XMrep{number} ibias {{{{'{gate}' if replica_tracks_signal else 'replica_cm'}}}} "
        assert deck.count(before) == 1
        deck = deck.replace(before, after)
    (target / f"tb/{name}.spice").write_text(deck)
deck = (target / "tb/ac.spice").read_text()
core_ports = re.search(r"^\.subckt gilbert_cell (.+)$", deck, re.M)[1].split()
ota_ports = re.search(r"^\.subckt ota (.+)$", deck, re.M)[1].split()
nodes = {"vdd": "rvdd", "vbias": "rvbias", "outp": "routp", "outn": "routn",
         "vss": "GND", "ibias": "ribias", "ntap": "rvdd", "ptap": "GND",
         "vcm": "rvcm_sense", "replica_cm": "vref",
         "in1p": "outp", "in1n": "outn", "in2p": "otherp", "in2n": "othern",
         **{f"gt{i}": f"gt{i}" for i in range(5)}}
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
deck = deck.replace("Cloadp outp GND {{c_load}}", "Cloadp outp GND 25f")
deck = deck.replace("Cloadn outn GND {{c_load}}", "Cloadn outn GND 25f")
sheet = yaml.safe_load((source / "datasheets/nominal6/candidate6_fs.yaml").read_text())
sheet["parameters"]["replica_tracks_signal"] = [1, 0]
ac_spec = sheet["tests"]["ac"]
fanout_spec = {}
for key, value in ac_spec.items():
    if key in {"source", "engine", "ac_signals"}:
        fanout_spec[key] = value
    else:
        fanout_spec["loaded_" + key] = value
        deck = re.sub(r"\b" + re.escape(key) + r"\b", "loaded_" + key, deck)
sheet["tests"]["fanout"] = fanout_spec
(target / "tb/fanout.spice").write_text(deck)
header = "# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer\n# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1\n"
(target / "datasheets/quiet_fs.yaml").write_text(header + yaml.safe_dump(sheet, sort_keys=False))
(target / "settings.json").write_text(json.dumps({"num_cores": 2, "sim_timeout_sec": 600}) + "\n")
(target / "README.md").write_text("""# Common-mode-biased replica control

The signal-tracking reference is compared with both replica gates tied to a new explicit replica_cm port.
The bench connects that port to its existing ideal vref source, also used by CMFB.
All transistor dimensions, currents, resistors and gain codes remain fixed.
Each case measures DC shape, bare-core AC and AC while driving an identical receiver input 1 with 25 fF wire per output.
This reference-bias change may alter curvature, common-mode sensitivity and noise.
It needs real reference-driver impedance, loop and PVT qualification before use in a port schematic.
""")

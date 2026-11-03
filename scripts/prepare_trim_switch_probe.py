#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Compare mid-rail NMOS, PMOS and transmission-gate conductance."""
import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
target = ROOT / "verification/porting/sky_trim_switch_probe"
(target / "tb").mkdir(parents=True, exist_ok=True)
(target / "datasheets").mkdir(exist_ok=True)
width, length = 7.365, .35
cases = {"n": (1,0), "p": (0,1), "p2": (0,2), "tg": (1,1), "tg2": (1,2)}
lines = ["Mid-rail trim-switch conductance",
         ".lib /foss/pdks/sky130A/libs.tech/ngspice/sky130.lib.spice {{corner_mos}}",
         ".temp {{temp}}", "Vdd vdd 0 1.5", "Vcm vcmi 0 0.75", "Vdiff vd 0 0.001"]
for name, (n_count, p_count) in cases.items():
    lines += [f"Ep_{name} d_{name} vcmi VOL='v(vd)/2'",
              f"En_{name} s_{name} vcmi VOL='-v(vd)/2'"]
    for kind, count in [("n",n_count),("p",p_count)]:
        if not count:
            continue
        gate, bulk = ("vdd","0") if kind == "n" else ("0","vdd")
        lines += [
            f"X{kind}_{name} d_{name} {gate} s_{name} {bulk} sky130_fd_pr__{kind}fet_01v8_lvt",
            f"+ l={length} w={width} nf=1 m={count} ad={width*.29} as={width*.29}",
            f"+ pd={2*(width+.29)} ps={2*(width+.29)} nrd={.29/width} nrs={.29/width} sa=0 sb=0 sd=0"]
lines += [".control", "save all", "dc Vdd 1.45 1.65 0.05", "let points=length(v(vdd))"]
test = {"source": "netlist", "engine": "ngspice", "points": {"min":5,"max":5}}
for name in cases:
    lines += [f"let ron_{name}=v(vd)/((i(En_{name})-i(Ep_{name}))/2)",
              f"let ron_{name}_150=ron_{name}[1]"]
    test[f"ron_{name}_150"] = {"min":0, "max":1e9}
test["dc_signals"] = ["ron_" + name for name in cases]
lines += ["quit", ".endc", ".end"]
(target / "tb/switches.spice").write_text("\n".join(lines) + "\n")
sheet = {"parameters": {"corner_mos": ["tt","ff","fs","sf","ss"], "temp":[27]},
         "tests": {"switches":test}}
header = "# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer\n# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1\n"
(target / "datasheets/probe.yaml").write_text(header + yaml.safe_dump(sheet,sort_keys=False))
(target / "settings.json").write_text(json.dumps({"num_cores":3,"sim_timeout_sec":600})+"\n")
(target / "README.md").write_text("""# Mid-rail trim-switch conductance

Five independent fixtures measure the differential conductance of a low-threshold NMOS, one or two parallel low-threshold PMOS devices, and their transmission-gate combinations.
Every unit is W=7.365 um, L=0.35 um, nf=1.
All switches are on, with NMOS gates at VDD and PMOS gates at zero.
Each source/drain pair stays centered at 0.75 V with 1 mV differential bias.
A native DC sweep varies VDD from 1.45 to 1.65 V.

The probe compares five MOS corners at 27 C.
It does not measure mismatch, switch capacitance, signal-amplitude distortion or the complete multiplier.
""")

length_target = ROOT/"verification/porting/sky_trim_switch_lengths"
(length_target/"tb").mkdir(parents=True,exist_ok=True)
(length_target/"datasheets").mkdir(exist_ok=True)
deck = (target/"tb/switches.spice").read_text()
device_lines = deck.splitlines()
for index, line in enumerate(device_lines):
    if line.startswith("Xn_"):
        if not device_lines[index+1].startswith("+ l=0.35 "):
            raise ValueError("Unexpected NMOS geometry")
        device_lines[index+1] = device_lines[index+1].replace("l=0.35", "l={{n_length}}", 1)
(length_target/"tb/switches.spice").write_text("\n".join(device_lines)+"\n")
sheet["parameters"]["n_length"] = [.15,.35,.5,1]
(length_target/"datasheets/probe.yaml").write_text(header+yaml.safe_dump(sheet,sort_keys=False))
(length_target/"settings.json").write_text(json.dumps({"num_cores":3,"sim_timeout_sec":600})+"\n")
(length_target/"README.md").write_text("""# Trim-switch NMOS length control

This extends sky_trim_switch_probe by changing only the NMOS channel length.
The PMOS-only fixtures remain unchanged as controls.
Lengths are 0.15, 0.35, 0.5 and 1 um, with all unit widths fixed at 7.365 um.
This measures on-resistance and supply sensitivity, not mismatch or circuit bandwidth.
""")

#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Add a scaled pair and source-resistor replica to the PMOS tail reference."""
from pathlib import Path
import json
import yaml

ROOT = Path(__file__).resolve().parents[1]
src = ROOT / "verification/porting/sky_compact_compliance"
dst = ROOT / "verification/porting/sky_replica_tail"
(dst / "tb").mkdir(parents=True, exist_ok=True)
(dst / "datasheets").mkdir(exist_ok=True)
deck = (src / "tb/compliance.spice").read_text()
assert "XM14 ibias ibias vdd" in deck
deck = deck.replace("XM14 ibias ibias vdd", "XM14 rvcm1 ibias vdd")
nf = "(12*pair_scale*power_m/8)"
width = "(74.625*pair_scale*power_m/8)"
lines = []
for number, gate in [(1, "in1n"), (2, "in1p")]:
    lines.append(
        f"XMrep{number} ibias {gate} rps{number} ntap sky130_fd_pr__pfet_01v8_lvt "
        "L={{pair_l}} W={{" + width + "}} nf={{" + nf + "|int}} "
        "ad={{((" + nf + "+1)/2)|int}}*6.21875*0.29")
    # Keep every arithmetic expression inside the Jinja braces.
    lines[-1] = lines[-1].split(" ad=")[0] + (
        " ad={{(((" + nf + "+1)/2)|int)*6.21875*0.29}}"
        " as={{(((" + nf + "+2)/2)|int)*6.21875*0.29}}"
        " pd={{2*(((" + nf + "+1)/2)|int)*(6.21875+0.29)}}"
        " ps={{2*(((" + nf + "+2)/2)|int)*(6.21875+0.29)}}"
        " nrd={{0.29/" + width + "}} nrs={{0.29/" + width + "}}"
        " sa=0 sb=0 sd=0 mult=1 m=1")
    for index in range(8):
        left = "rvcm1" if index == 0 else f"rp{number}_{index}"
        right = f"rps{number}" if index == 7 else f"rp{number}_{index+1}"
        lines.append(f"XRrep{number}_{index} {left} {right} ptap sky130_fd_pr__res_high_po_5p73 "
                     "L={{(rpair-68.05)/56.46}} mult={{power_m}} m={{power_m}}")
start = deck.index(".subckt gilbert_cell ")
end = deck.index(".ends", start)
deck = deck[:end] + "\n".join(lines) + "\n" + deck[end:]
extra = {
    "tail_gate_v": "v(ibias)", "tail_drop_v": "v(vdd)-v(x1.vcm1)",
    "replica_error_v": "v(x1.rvcm1)-v(x1.vcm1)",
}
deck = deck.replace("let idd=-i(vdd)", "let idd=-i(vdd)\n" +
                    "\n".join(f"let {name}={expr}" for name, expr in extra.items()))
deck = deck.replace("\nquit\n", "\n" +
                    "\n".join(f"let {name}=op1.{name}" for name in extra) +
                    "\nlet tail_ratio=tail_current/(8*{{ibias*power_m}})\nquit\n", 1)
(dst / "tb/replica.spice").write_text(deck)
sheet = yaml.safe_load((src / "datasheets/ss.yaml").read_text())
sheet["tests"] = {"replica": {**sheet["tests"]["compliance"], **{k: {} for k in extra},
                              "tail_ratio": {}}}
sheet["tests"]["replica"]["tail_gate_v"] = {"min": 0, "max": 1.45}
sheet["parameters"].update(temp=[27], vdd=[1.5], tail_length_scale=[1],
    pair_body_tied=[0], corner_mos=["tt", "ff", "ss", "fs", "sf"],
    ibias=[27.5e-6, 40e-6, 55e-6])
for pair in sheet["parameters"]["pair_scale"]:
    for power in sheet["parameters"]["power_m"]:
        fingers = 12*pair*power/8
        if fingers < 1 or int(fingers) != fingers:
            raise ValueError("Replica needs an integral finger count")
header = "# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer\n# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1\n"
(dst / "datasheets/bias.yaml").write_text(header + yaml.safe_dump(sheet, sort_keys=False))
(dst / "settings.json").write_text(json.dumps({"num_cores": 4, "sim_timeout_sec": 180}) + "\n")

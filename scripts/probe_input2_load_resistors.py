#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Measure resistance and driven-end capacitance of the proposed load geometries."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--kind", choices=["load", "trim"], default="load")
args = parser.parse_args()
project = "sky_input2_quiet_trim_poly" if args.kind == "trim" else "sky_input2_load_resistors"
mapping = json.loads((ROOT / f"verification/porting/{project}/mapping.json").read_text())
wanted = ((68.05 + 56.46 * .875) * 1.7 * 1.4 if args.kind == "trim"
          else (68.05 + 56.46 * 13.035) * 1.7)
lines = ["* Equal-resistance precision-poly load probe",
         ".lib /foss/pdks/sky130A/libs.tech/ngspice/sky130.lib.spice tt", ".temp 27"]
for family, v in mapping.items():
    model = Path("/foss/pdks/sky130A/libs.ref/sky130_fd_pr/spice") / f"sky130_fd_pr__res_high_po_{family}.model.spice"
    if hashlib.sha256(model.read_bytes()).hexdigest() != v["model_sha256"]:
        raise ValueError(f"Model changed since resistance mapping: {family}")
    length = ((wanted-v["rcon"]) + ((wanted-v["rcon"])**2-4*v["rsheet"]*v["a"])**.5)/(2*v["rsheet"])
    v["length_um"] = length
    v["minimum_model_resistance_ohm"] = v["rcon"] + 2*(v["rsheet"]*v["a"])**.5
    lines += [f"V{family} n{family} 0 dc .001 ac 1",
              f"X{family} n{family} 0 0 sky130_fd_pr__res_high_po_{family} l={length:.15g} m=1 mult=1"]
lines += [".control", "op"]
for family in mapping:
    lines += [f"let r_{family}=-v(n{family})/i(v{family})", f"print r_{family}"]
lines += ["ac lin 1 1meg 1meg"]
for family in mapping:
    lines += [f"let c_{family}=-imag(i(v{family}))/(6.28318530718*frequency)*1e15", f"print c_{family}"]
lines += ["quit", ".endc", ".end"]
with tempfile.TemporaryDirectory(prefix="input2_res_probe_") as directory:
    deck = Path(directory)/"probe.spice"
    deck.write_text("\n".join(lines)+"\n")
    result = subprocess.run([str(ROOT/"scripts/with_sky130_ngspice.sh"), "ngspice", "-b", str(deck)],
                            check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
for family, v in mapping.items():
    for prefix, key in [("r", "resistance_1mv_ohm"), ("c", "driven_end_capacitance_ff")]:
        match = re.search(rf"(?mi)^{prefix}_{family}\s*=\s*([-+0-9.eE]+)", result.stdout)
        if not match:
            raise ValueError(result.stdout)
        v[key] = float(match[1])
    if abs(v["resistance_1mv_ohm"]/wanted-1) > 1e-4:
        raise ValueError(f"Resistance mapping failed: {family}")
evidence = {"target_resistance_ohm": wanted, "temperature_c": 27,
            "voltage_v": .001, "ac_frequency_hz": 1e6, "models": mapping}
name = "sky_quiet_trim_resistor_probe.json" if args.kind == "trim" else "sky_input2_resistor_probe.json"
(ROOT/"doc/porting/evidence"/name).write_text(json.dumps(evidence, indent=2)+"\n")
print(json.dumps(evidence, indent=2))

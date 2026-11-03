#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Verify installed SKY130 deterministic passive corner selection."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument("--output", type=Path, required=True)
args = parser.parse_args()
if os.environ.get("PDK") != "sky130A":
    raise SystemExit("Select sky130A before running this probe")
pdk = Path(os.environ["PDKPATH"])
models = pdk / "libs.tech/ngspice"
wrapper = ROOT / "scripts/with_sky130_ngspice.sh"
bundles = ["res_typical__cap_typical", "res_low__cap_low", "res_low__cap_high",
           "res_high__cap_low", "res_high__cap_high"]
records = []
files = {models / "sky130.lib.spice", models / "corners/tt.spice",
         models / "corners/tt/specialized_cells.spice"}
for name in bundles:
    files.update(models / "r+c" / (name + suffix) for suffix in [".spice", "__lin.spice"])
with tempfile.TemporaryDirectory(prefix="sky-passive-corners-") as work:
    work = Path(work)
    for name in ["library_tt"] + bundles:
        if name == "library_tt":
            selection = f".lib {models}/sky130.lib.spice tt"
        else:
            selection = f""".param mc_mm_switch=0 mc_pr_switch=0
.include {models}/corners/tt.spice
.include {models}/r+c/{name}.spice
.include {models}/r+c/{name}__lin.spice
.include {models}/corners/tt/specialized_cells.spice"""
        deck = f"""SKY130 deterministic passive-corner control
{selection}
.temp 27
Vr1 r1 0 0.001
Vr10 r10 0 0.001
Xr1 r1 0 0 sky130_fd_pr__res_high_po_5p73 l=1 m=1 mult=1
Xr10 r10 0 0 sky130_fd_pr__res_high_po_5p73 l=10 m=1 mult=1
Vc c 0 dc 0.75 ac 1
Xc c 0 sky130_fd_pr__cap_mim_m3_1 w=5 l=5 mf=1
.control
save i(vr1) i(vr10) i(vc)
op
let r1_value=-0.001/i(vr1)
let r10_value=-0.001/i(vr10)
set r1_saved=$&r1_value
set r10_saved=$&r10_value
ac lin 1 1Meg 1Meg
let c_value=-imag(i(vc))/(2*PI*frequency)
echo PASSIVE_RESULT $r1_saved $r10_saved $&c_value
quit
.endc
.end
"""
        path = work / (name + ".spice")
        path.write_text(deck)
        run = subprocess.run([str(wrapper), "ngspice", "-b", str(path)], cwd=work,
                             text=True, capture_output=True, timeout=120)
        log = run.stdout + run.stderr
        match = re.search(r"^PASSIVE_RESULT\s+(\S+)\s+(\S+)\s+(\S+)", log, re.M)
        if run.returncode or not match or re.search(r"(?im)^error:", log):
            raise RuntimeError(f"{name}: invalid simulation\n{log[-2500:]}")
        r1, r10, capacitance = map(float, match.groups())
        if not (0 < r1 < r10 and capacitance > 0):
            raise ValueError("Nonphysical passive probe")
        records.append({"bundle": name, "r_l1_ohm": r1, "r_l10_ohm": r10,
                        "mim_5x5_f": capacitance})
nominal, explicit = records[:2]
for key in ["r_l1_ohm", "r_l10_ohm", "mim_5x5_f"]:
    if abs(explicit[key] / nominal[key] - 1) > 1e-6:
        raise ValueError("Explicit typical selection differs from library tt")
result = {
    "pdk": "sky130A", "temperature_c": 27,
    "resistor": "res_high_po_5p73, L=1/10 um, 1 mV bias, bulk=0",
    "capacitor": "cap_mim_m3_1, 5x5 um, 0.75 V, 1 MHz",
    "records": records,
    "selection_sha256": {str(p.relative_to(pdk)): hashlib.sha256(p.read_bytes()).hexdigest()
                         for p in sorted(files)},
}
args.output.parent.mkdir(parents=True, exist_ok=True)
args.output.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(records, indent=2))

#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Probe both closed replica-candidate loops with resolved current pulses."""
import json
from pathlib import Path
import re

import yaml

ROOT = Path(__file__).resolve().parents[1]
source = ROOT / "verification/porting/sky_replica_tail"
target = ROOT / "verification/porting/sky_replica_kick"
(target / "tb").mkdir(parents=True, exist_ok=True)
(target / "datasheets").mkdir(exist_ok=True)
deck = (source / "tb/replica.spice").read_text()
deck = deck.replace(".option method=gear", ".option method=trap reltol=1e-4")
assert "Iloopkick" not in deck
deck = deck.replace("**** begin user architecture code",
    "Iloopkick vdd {{kick_node}} PULSE(0 {{kick_current}} 100n 100p 100p 20n 2u)\n"
    "**** begin user architecture code", 1)
control = """.control
save v(outp) v(outn) v(vbias) v(ibias) v(x1.vcm1) v(x1.rvcm1) i(vdd)
op
let cm0=(v(outp)+v(outn))/2
let bias0=v(ibias)
let cmfb0=v(vbias)
tran {{maxstep}} 1u 0 {{maxstep}}
let end_time=time[length(time)-1]
if end_time > 0.999e-6
let cm=(v(outp)+v(outn))/2
let err=cm-op1.cm0
let bias_err=v(ibias)-op1.bias0
let cmfb_err=v(vbias)-op1.cmfb0
let abs_err=abs(err)
let abs_bias_err=abs(bias_err)
meas tran peak max abs_err from=100n to=900n
meas tran residual max abs_err from=900n to=1u
meas tran bias_residual max abs_bias_err from=900n to=1u
let peak_mv=peak*1000
let residual_mv=residual*1000
let bias_residual_mv=bias_residual*1000
end
quit
.endc"""
deck, count = re.subn(r"\.control\b.*?\.endc", lambda _: control, deck, flags=re.S)
assert count == 1
(target / "tb/kick.spice").write_text(deck)
sheet = yaml.safe_load((source / "datasheets/nominal.yaml").read_text())
sheet["parameters"].update(kick_node=["vbias", "ibias"],
    kick_current=[-40e-6, 40e-6], maxstep=["100p", "50p"])
sheet["tests"] = {"kick": {"source": "netlist", "engine": "ngspice",
    "end_time": {"min": .999e-6}, "peak_mv": {},
    "residual_mv": {"max": 1}, "bias_residual_mv": {"max": 1},
    "transient_signals": ["cm", "err", "bias_err", "cmfb_err",
                          "v(ibias)", "v(vbias)", "v(x1.vcm1)", "v(x1.rvcm1)"]}}
header = "# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer\n# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1\n"
(target / "datasheets/kick.yaml").write_text(header + yaml.safe_dump(sheet, sort_keys=False))
(target / "settings.json").write_text(json.dumps(
    {"num_cores": 2, "sim_timeout_sec": 600}) + "\n")
(target / "README.md").write_text("""# Replica loop current kicks

This bench uses the original replica candidate at tt, 27 C, 1.5 V and gain code 13.
It applies a 20 ns current pulse of either polarity to the CMFB load-gate node or the shared main/reference tail-gate node.
Pulse amplitude is 40 uA, compared with the two-copy circuit's 67.5 uA ideal reference.
Both loops remain closed.
Trapezoidal integration is repeated with maximum time steps of 100 ps and 50 ps.

The provisional residual limit is 1 mV on both output common mode and the tail gate at 900 to 1000 ns.
The initial DC point precedes each kick.
This is recovery about an established operating point, not power-up or physical bias-source qualification.
Use scripts/analyze_replica_kick.py to independently check waveform completion, scalar anchors and maximum-step sensitivity.
""")

#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Sweep gain code inside ngspice while Chipify sweeps process parameters."""
import json
from pathlib import Path
import re

import yaml

ROOT = Path(__file__).resolve().parents[1]
source = ROOT / "verification/porting/sky_replica_trim_range"
target = ROOT / "verification/porting/sky_gain_dc_sweep"
(target / "tb").mkdir(parents=True, exist_ok=True)
(target / "datasheets").mkdir(exist_ok=True)
deck = (source / "tb/replica.spice").read_text()
lines = [".control", "save v(outp) v(outn) v(gcode)", "destroy all"]
for amplitude in [.1, .01]:
    for sign1, sign2 in [(1, 1), (-1, 1), (-1, -1), (1, -1)]:
        lines += [f"alter vd1 dc={sign1*amplitude}",
                  f"alter vd2 dc={sign2*amplitude}",
                  "dc vgcode 0 31 1",
                  "let vo=v(outp)-v(outn)"]
lines += [
    "let k100_curve=(dc1.vo-dc2.vo+dc3.vo-dc4.vo)/0.04",
    "let k10_curve=(dc5.vo-dc6.vo+dc7.vo-dc8.vo)/0.0004",
    "let compr_curve=k100_curve/k10_curve",
    "let points=length(k100_curve)",
    "let k100_first=k100_curve[0]",
    "let k100_last=k100_curve[31]",
    "let k10_first=k10_curve[0]",
    "let k10_last=k10_curve[31]",
    "quit", ".endc"]
deck, count = re.subn(r"\.control\b.*?\.endc", lambda _: "\n".join(lines), deck, flags=re.S)
assert count == 1
(target / "tb/code_curve.spice").write_text(deck)
sheet = yaml.safe_load((source / "datasheets/centered/centered_tt.yaml").read_text())
sheet["parameters"].update(temp=[27], gcode=[0])
sheet["tests"] = {"code_curve": {
    "source": "netlist", "engine": "ngspice", "points": {"min": 32, "max": 32},
    "k100_first": {}, "k100_last": {}, "k10_first": {}, "k10_last": {},
    "dc_signals": ["dc8.k100_curve", "dc8.k10_curve", "dc8.compr_curve"]}}
header = "# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer\n# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1\n"
(target / "datasheets/control.yaml").write_text(header + yaml.safe_dump(sheet, sort_keys=False))
(target / "settings.json").write_text(json.dumps({"num_cores": 1, "sim_timeout_sec": 600}) + "\n")

#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Measure the local tail-replica loop with both main and reference gate loads."""
from pathlib import Path
import json
import re
import yaml

ROOT = Path(__file__).resolve().parents[1]
src = ROOT / "verification/porting/sky_replica_tail"
dst = ROOT / "verification/porting/sky_replica_stability"
(dst / "tb").mkdir(parents=True, exist_ok=True)
(dst / "datasheets").mkdir(exist_ok=True)
deck = (src / "tb/replica.spice").read_text()
deck = re.sub(r"^(x1 .+) gilbert_cell$", r"\1 tailgate gilbert_cell", deck, flags=re.M)
deck = re.sub(r"^(\.subckt gilbert_cell .+)$", r"\1 tailgate", deck, flags=re.M)
deck = deck.replace("XM13 vcm1 ibias vdd", "XM13 vcm1 tailgate vdd")
deck = deck.replace("XM14 rvcm1 ibias vdd", "XM14 rvcm1 tailgate vdd")
original = (ROOT / "verification/porting/sky_replica_validation/tb/stability.spice").read_text()
control = re.search(r"\.control\b.*?\.endc", original, re.S)[0]
control = control.replace("v(vbias_ota)", "v(ibias)").replace("v(vbias)", "v(tailgate)")
control = control.replace("vbias_dc", "bias_gate_v")
control = control.replace("* run 2: current injection, i(vstb) flows from vbias into the OTA output",
                          "* run 2: current injection across the shared tail-gate connection")
deck = re.sub(r"\.control\b.*?\.endc", lambda m: (
    "Vstb tailgate ibias dc 0 ac 0\nIstb GND tailgate dc 0 ac 0\n" + control),
    deck, flags=re.S)
(dst / "tb/stability.spice").write_text(deck)
sheet = yaml.safe_load((ROOT / "verification/porting/sky_replica_validation/datasheets/stability.yaml").read_text())
test = sheet["tests"]["stability"]
test["bias_gate_v"] = test.pop("vbias_dc")
header = "# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer\n# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1\n"
(dst / "datasheets/nominal.yaml").write_text(header + yaml.safe_dump(sheet, sort_keys=False))
(dst / "settings.json").write_text(json.dumps({"num_cores": 1, "sim_timeout_sec": 180}) + "\n")

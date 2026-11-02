#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Test a drain-voltage matched tail mirror with an ideal DC error amplifier."""
from pathlib import Path
import json
import yaml

ROOT = Path(__file__).resolve().parents[1]
src = ROOT / "verification/porting/sky_compact_compliance"
dst = ROOT / "verification/porting/sky_regulated_tail"
(dst / "tb").mkdir(parents=True, exist_ok=True)
(dst / "datasheets").mkdir(exist_ok=True)
deck = (src / "tb/compliance.spice").read_text()
assert "XM13 vcm1 ibias vdd" in deck
assert "XM14 ibias ibias vdd" in deck
deck = deck.replace("XM13 vcm1 ibias vdd", "XM13 vcm1 tail_gate vdd")
deck = deck.replace("XM14 ibias ibias vdd", "XM14 ibias tail_gate vdd")
start = deck.index(".subckt gilbert_cell ")
end = deck.index(".ends", start)
deck = deck[:end] + "Ereg tail_gate vss ibias vcm1 {{reg_gain}}\n" + deck[end:]
extra = {
    "tail_gate_v": "v(x1.tail_gate)",
    "tail_drop_v": "v(vdd)-v(x1.vcm1)",
    "reference_error_v": "v(ibias)-v(x1.vcm1)",
}
deck = deck.replace("let idd=-i(vdd)", "let idd=-i(vdd)\n" +
                    "\n".join(f"let {name}={expr}" for name, expr in extra.items()))
deck = deck.replace("\nquit\n", "\n" +
                    "\n".join(f"let {name}=op1.{name}" for name in extra) + "\nquit\n", 1)
(dst / "tb/regulated.spice").write_text(deck)
sheet = yaml.safe_load((src / "datasheets/ss.yaml").read_text())
sheet["tests"] = {"regulated": {**sheet["tests"]["compliance"], **{k: {} for k in extra}}}
sheet["tests"]["regulated"]["tail_gate_v"] = {"min": 0, "max": 1.45}
sheet["parameters"].update(temp=[27], vdd=[1.5], tail_length_scale=[1],
    pair_body_tied=[0], corner_mos=["tt", "ff", "ss", "fs", "sf"],
    ibias=[27.5e-6, 40e-6, 55e-6], reg_gain=[10000])
header = "# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer\n# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1\n"
(dst / "datasheets/bias.yaml").write_text(header + yaml.safe_dump(sheet, sort_keys=False))
(dst / "settings.json").write_text(json.dumps({"num_cores": 4, "sim_timeout_sec": 180}) + "\n")

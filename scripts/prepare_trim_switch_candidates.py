#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Screen PMOS and transmission-gate trim variants without widening segments."""
import json
from pathlib import Path
import re
import yaml

ROOT=Path(__file__).resolve().parents[1]
base=ROOT/"verification/porting"
source=(base/"sky_replica_trim_range/tb/replica.spice").read_text()
header="# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer\n# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1\n"
for mode,parallel in [("pmos4",4),("tg2",2)]:
    target=base/("sky_trim_"+mode)
    (target/"tb").mkdir(parents=True,exist_ok=True)
    (target/"datasheets/endpoints").mkdir(parents=True,exist_ok=True)
    deck=source.replace("ptap gain_trim","ptap ntap gain_trim",1)
    start=deck.index(".subckt gain_trim ")
    end=deck.index(".ends",start)
    trim=re.sub(r"\n\+\s*"," ",deck[start:end])
    lines=[]
    count=0
    for line in trim.splitlines():
        if line.startswith(".subckt gain_trim"):
            lines.append(line+" ntap")
            for bit in range(5):
                lines.append(f"Egp{bit} gp{bit} ptap VOL='v(ntap,ptap)-v(gt{bit},ptap)'")
            continue
        if line.startswith(("XMSW","XMDS")):
            if mode=="tg2":
                lines.append(line)
            tokens=line.split(maxsplit=5)
            name,drain,gate,source_node,bulk,rest=tokens
            assert bulk=="ptap"
            assert "sky130_fd_pr__nfet_01v8_lvt" in rest
            rest=rest.replace("sky130_fd_pr__nfet_01v8_lvt","sky130_fd_pr__pfet_01v8_lvt")
            rest=rest.replace("mult={{1.0*power_m}}",f"mult={{{{{parallel}*power_m}}}}")
            rest=rest.replace("m={{1*power_m}}",f"m={{{{{parallel}*power_m}}}}")
            pgate=gate.replace("gt","gp",1) if gate.startswith("gt") else gate
            lines.append(f"{name}_P {drain} {pgate} {source_node} ntap {rest}")
            count+=1
        else:
            lines.append(line)
    assert count==11
    deck=deck[:start]+"\n".join(lines)+"\n"+deck[end:]
    (target/"tb/replica.spice").write_text(deck)
    for corner in ["tt","ff","fs","sf","ss"]:
        sheet=yaml.safe_load((base/f"sky_replica_tail/datasheets/calibration/trim_{corner}.yaml").read_text())
        sheet["parameters"].update(temp=[27],vdd=[1.5],gcode=[0,31],
                                   rscale=[1.7],rbase_scale=[1],rtrim_scale=[1])
        (target/f"datasheets/endpoints/{mode}_{corner}.yaml").write_text(header+yaml.safe_dump(sheet,sort_keys=False))
    (target/"settings.json").write_text(json.dumps({"num_cores":2,"sim_timeout_sec":600})+"\n")
    (target/"README.md").write_text(f"""# {mode} trim-switch control

This retains the original replica transistors and current calibration.
Load and trim resistance scale together by 1.7, with no separate doubling of trim segments.
The {mode} variant uses {parallel} parallel PMOS copies per inherited switch unit.
PMOS wells connect to the core ntap supply.
Ideal complementary gate drivers preserve the original code polarity.
These drivers represent static control levels, not qualified physical inverters.
The retained NMOS switches in tg2 form transmission gates.
Endpoint bracketing is only a screen before matched-gain shape, speed and loop checks.
""")

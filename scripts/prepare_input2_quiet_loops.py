#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Generate double-injection loops from the selected quiet-replica circuit."""
import copy
import json
from pathlib import Path
import re
import yaml
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
base = ROOT / "verification/porting"
source = base / "sky_input2_quiet_replica"
target = base / "sky_input2_quiet_loops"
(target / "tb").mkdir(parents=True, exist_ok=True)
(target / "datasheets/nominal").mkdir(parents=True, exist_ok=True)
header = "# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer\n# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1\n"
original = (source / "tb/replica.spice").read_text()
tests = {}
for name, old_project, old_sheet in [
    ("cmfb", "sky_replica_validation", "stability.yaml"),
    ("bias", "sky_replica_stability", "nominal.yaml"),
]:
    old = base / old_project
    control = re.search(r"\.control\b.*?\.endc", (old / "tb/stability.spice").read_text(), re.S)[0]
    deck, count = re.subn(r"\.control\b.*?\.endc", lambda _: control, original, flags=re.S)
    assert count == 1
    if name == "cmfb":
        before = "x2 vdd vbias vref"
        assert deck.count(before) == 1
        deck = deck.replace(before, "x2 vdd vbias_ota vref")
        injection = "Vstb vbias vbias_ota dc 0 ac 0\nIstb GND vbias dc 0 ac 0\n"
    else:
        deck, count = re.subn(r"(?m)^(x1 .+) gilbert_cell$", r"\1 tailgate gilbert_cell", deck)
        assert count == 1
        deck, count = re.subn(r"(?m)^(\.subckt gilbert_cell .+)$", r"\1 tailgate", deck)
        assert count == 1
        for transistor, drain in [("XM13", "vcm1"), ("XM14", "rvcm1")]:
            before = f"{transistor} {drain} ibias vdd"
            assert deck.count(before) == 1
            deck = deck.replace(before, f"{transistor} {drain} tailgate vdd")
        injection = "Vstb tailgate ibias dc 0 ac 0\nIstb GND tailgate dc 0 ac 0\n"
    deck = deck.replace(".control", injection + ".control", 1)
    (target / f"tb/{name}.spice").write_text(deck)
    tests[name] = yaml.safe_load((old / "datasheets" / old_sheet).read_text())["tests"]["stability"]
    tests[name]["ncross"] = {"min": 1, "max": 1}
    # Prefix scalar names because both loop tests contribute to the same row.
    for metric in list(tests[name]):
        if metric in {"source", "engine", "ac_signals"}:
            continue
        deck = re.sub(r"\b" + re.escape(metric) + r"\b", name + "_" + metric, deck)
        tests[name][name + "_" + metric] = tests[name].pop(metric)
    (target / f"tb/{name}.spice").write_text(deck)
selection = pd.read_csv(ROOT / "doc/porting/evidence/input2_quiet_selected_nominal.csv")
assert len(selection) == 5 and set(selection.corner_mos) == {"ff", "fs", "sf", "ss", "tt"}
assert selection.joint_dc_bare_loaded_bw_screen.all()
for _, selected in selection.iterrows():
    corner, code = selected.corner_mos, int(selected.gcode)
    params = yaml.safe_load((source / f"datasheets/nominal/quiet_{corner}.yaml").read_text())["parameters"]
    params = copy.deepcopy(params)
    params.update(gcode=[code], vd1=[0], vd2=[0])
    sheet = {"parameters": params, "tests": tests}
    (target / f"datasheets/nominal/loops_{corner}.yaml").write_text(header + yaml.safe_dump(sheet, sort_keys=False))
(target / "settings.json").write_text(json.dumps({"num_cores": 3, "sim_timeout_sec": 600}) + "\n")

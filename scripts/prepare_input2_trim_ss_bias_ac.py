#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Check both AC loads at every DC-feasible sampled SS gain/current setting."""
import argparse
import copy
import json
from pathlib import Path
import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parents[1]
base = ROOT / "verification/porting"
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--pair-calibration", action="store_true")
args = parser.parse_args()
source = base / ("sky_input2_pair_width" if args.pair_calibration else "sky_input2_quiet_trim_poly")
target = base / ("sky_input2_pair_calibration_ac" if args.pair_calibration else "sky_input2_trim_ss_bias_ac")
(target / "tb").mkdir(parents=True, exist_ok=True)
(target / "datasheets/nominal").mkdir(parents=True, exist_ok=True)
for name in ["replica", "ac", "fanout"]:
    (target / f"tb/{name}.spice").write_text((source / f"tb/{name}.spice").read_text())
data = pd.read_csv(ROOT / "doc/porting/evidence" /
                   ("sky_input2_pair_calibration.csv" if args.pair_calibration else "sky_trim_ss_bias.csv"))
feasible = data[data.dc_screen_pass]
assert len(feasible) > 0
if not args.pair_calibration:
    assert len(feasible) == 4
template_path = "datasheets/pair_ss.yaml" if args.pair_calibration else "datasheets/corners/trim_ss.yaml"
template = yaml.safe_load((source / template_path).read_text())
param_path = ("sky_input2_pair_calibration/datasheets/calibrate_ss.yaml" if args.pair_calibration
              else "sky_input2_trim_ss_bias/datasheets/ss_bias.yaml")
params = yaml.safe_load((base / param_path).read_text())["parameters"]
header = "# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer\n# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1\n"
for factor, group in feasible.groupby("bias_factor"):
    sheet = copy.deepcopy(template)
    sheet["parameters"] = copy.deepcopy(params)
    sheet["parameters"].update(bias_factor=[float(factor)], gcode=sorted(map(int, group.gcode)))
    name = "bias_" + str(factor).replace(".", "p") + ".yaml"
    (target / "datasheets/nominal" / name).write_text(header + yaml.safe_dump(sheet, sort_keys=False))
(target / "settings.json").write_text(json.dumps({"num_cores": 4, "sim_timeout_sec": 600}) + "\n")

#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Record the minimum modeled channel lengths in the installed SKY130 TT bins."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument("--output", type=Path,
                    default=ROOT / "verification/controls/sky_mos_model_lengths.json")
args = parser.parse_args()
if os.environ.get("PDK") != "sky130A":
    raise SystemExit("Select sky130A before reading model limits")
pdk = Path(os.environ["PDKPATH"])
records = {}
for device in ["pfet_01v8_lvt", "pfet_01v8", "nfet_01v8_lvt", "nfet_01v8"]:
    path = pdk / "libs.ref/sky130_fd_pr/spice" / f"sky130_fd_pr__{device}__tt.pm3.spice"
    contents = path.read_bytes()
    bounds = [float(v) for v in re.findall(rb"\blmin\s*=\s*(\S+)", contents)]
    if not bounds:
        raise ValueError(f"No length bins in {path}")
    records[device] = {
        "minimum_length_um": min(bounds)*1e6,
        "model_path": str(path.relative_to(pdk)),
        "sha256": hashlib.sha256(contents).hexdigest(),
        "bins": len(bounds),
    }
args.output.parent.mkdir(parents=True, exist_ok=True)
args.output.write_text(json.dumps(records, indent=2) + "\n")
print(args.output)

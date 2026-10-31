#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Check the AC plot names after multiple operating-point analyses."""
import argparse
import json
from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument("--output", type=Path,
                    default=ROOT / "verification/controls/ngspice_plot_names.json")
args = parser.parse_args()
results = []
with tempfile.TemporaryDirectory(prefix="ngspice_plot_names_") as scratch:
    for count, clear in [(1, False), (2, False), (17, False), (17, True)]:
        source = Path(scratch) / f"op_{count}_clear_{int(clear)}.spice"
        commands = "op\n" * count + ("destroy all\n" if clear else "")
        source.write_text("AC plot naming control\n"
                          "v1 in 0 dc 1 ac 1\nr1 in out 1k\nc1 out 0 1p\n"
                          ".control\n" + commands +
                          "ac dec 10 1k 10g\nsetplot\nquit\n.endc\n.end\n")
        proc = subprocess.run(
            [str(ROOT / "scripts/with_sky130_ngspice.sh"), "ngspice", "-b", str(source)],
            capture_output=True, text=True, check=True)
        match = re.search(r"Current\s+(ac\d+)\s", proc.stdout)
        if not match:
            raise RuntimeError(proc.stdout + proc.stderr)
        expected = "ac1" if clear else f"ac{count}"
        if match[1] != expected:
            raise RuntimeError(f"Expected {expected}, observed {match[1]}")
        results.append({"op_analyses": count, "destroy_all": clear, "first_ac_plot": match[1]})
args.output.parent.mkdir(parents=True, exist_ok=True)
args.output.write_text(json.dumps({"status": "verified", "controls": results}, indent=2) + "\n")
print(args.output)

#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Detect an unconstrained sweep axis that never enters the circuit template."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument("--output", type=Path, required=True)
args = parser.parse_args()
with tempfile.TemporaryDirectory(prefix="chipify_unused_parameter_") as scratch:
    project = Path(scratch)
    (project / "tb").mkdir()
    (project / "datasheets").mkdir()
    (project / "settings.json").write_text('{"num_cores":1,"sim_timeout_sec":30}\n')
    (project / "tb/unused.spice").write_text("""Unused-axis control
V1 in 0 1
R1 in out 1k
R2 out 0 1k
.control
op
let output_v=v(out)
quit
.endc
.end
""")
    (project / "datasheets/control.yaml").write_text("""parameters:
  corner_res: [low, high]
tests:
  unused:
    source: netlist
    engine: ngspice
    output_v: {min: 0.499999, max: 0.500001}
""")
    run = subprocess.run(
        [str(ROOT / "scripts/with_sky130_ngspice.sh"), "chipify-cli", "-c", "control.yaml", "--json"],
        cwd=project, capture_output=True, text=True, timeout=90)
    if run.returncode:
        raise RuntimeError(run.stdout + run.stderr)
    frame = pd.read_csv(project / "out/simulation_results.csv")
    if sorted(frame.corner_res) != ["high", "low"] or not frame.global_pass.all():
        raise ValueError("Expected two valid labels from the unchanged resistor divider")
    if not (frame.output_v == .5).all():
        raise ValueError("Unexpected divider result")
    log = run.stdout + run.stderr
    result = {"cases": 2, "labels": frame.corner_res.tolist(),
              "output_v": frame.output_v.tolist(), "all_pass": True,
              "parameter_occurs_in_template": False,
              "unused_parameter_diagnostic_seen": any(
                  term in log.lower() for term in ["unused parameter", "unused sweep", "unconsumed parameter"]),
              "interpretation": "Two labelled cases do not demonstrate two resistor models"}
args.output.parent.mkdir(parents=True, exist_ok=True)
args.output.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))

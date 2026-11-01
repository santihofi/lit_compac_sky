#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Detect whether Chipify captures the intended first AC plot after repeated OP."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument("--output", type=Path,
                    default=ROOT / "verification/controls/chipify_ac_selection.json")
args = parser.parse_args()
with tempfile.TemporaryDirectory(prefix="chipify_ac_selection_") as scratch:
    project = Path(scratch)
    (project / "tb").mkdir()
    (project / "datasheets").mkdir()
    (project / "settings.json").write_text('{"num_cores":1,"sim_timeout_sec":30}\n')
    (project / "tb/selection.spice").write_text("""AC selection control
V1 in 0 dc 1 ac 1
R1 in out 1k
R2 out 0 1k
.control
{% for _ in range(op_count) %}op
{% endfor %}
ac dec 10 1k 1meg
let first_gain=real(v(out)[0])
set first_gain=$&first_gain
alter r2 3k
ac dec 10 1k 1meg
let first_gain=$first_gain
let last_gain=real(v(out)[0])
quit
.endc
.end
""")
    (project / "datasheets/control.yaml").write_text("""parameters:
  op_count: [1, 2]
tests:
  selection:
    source: netlist
    engine: ngspice
    first_gain: {min: 0.499999, max: 0.500001}
    last_gain: {min: 0.749999, max: 0.750001}
    ac_signals: [v(out)]
""")
    proc = subprocess.run(
        [str(ROOT / "scripts/with_sky130_ngspice.sh"), "chipify-cli",
         "-c", "control.yaml", "--json"],
        cwd=project, capture_output=True, text=True, timeout=90)
    if proc.returncode:
        raise RuntimeError(proc.stdout + proc.stderr)
    meta = max((project / "out/history").glob("*.meta.json"), key=lambda p: p.stat().st_mtime)
    info = json.loads(meta.read_text())
    frame = pd.read_csv(project / "out/simulation_results.csv", dtype={"run_id": str})
    if len(frame) != 2:
        raise RuntimeError("Expected both plot-selection controls")
    records = []
    for _, row in frame.iterrows():
        wave = pd.read_csv(project / "out" / info["analysis_dirs"]["ac"] /
                           f"run_{row.run_id}__selection.csv")
        captured = float(wave["v(out)_mag"].iloc[0])
        records.append({
            "op_count": int(row.op_count), "first_ac_gain": float(row.first_gain),
            "last_ac_gain": float(row.last_gain), "captured_gain": captured,
            "captures_first_ac": abs(captured - float(row.first_gain)) < 1e-6,
            "chipify_global_pass": bool(row.global_pass),
            "sim_error": None if pd.isna(row.sim_error) else str(row.sim_error),
        })
    records.sort(key=lambda r: r["op_count"])
    if not records[0]["captures_first_ac"]:
        raise RuntimeError("One-OP baseline did not capture its first AC plot")
    report = {
        "status": "correct_first_plot" if all(r["captures_first_ac"] for r in records)
                  else "wrong_plot_reproduced",
        "controls": records,
    }
args.output.parent.mkdir(parents=True, exist_ok=True)
args.output.write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report, indent=2))

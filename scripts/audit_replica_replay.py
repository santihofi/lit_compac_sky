#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Match nominal measurements from drawn views to the characterized source."""
import json
from pathlib import Path
import shutil

import numpy as np
import pandas as pd
import yaml

from analyze_corner_surfaces import fit_surface
from check_chipify_results import audit, RESERVED
from check_core_ac_capture import check_curve
from check_loop_capture import check

ROOT = Path(__file__).resolve().parents[1]
base = ROOT/"verification/porting"
replay = base/"sky_replica_schematic/replay"
report = {}
evidence = ROOT/"doc/porting/evidence"


def wave(out, kind, test, run):
    meta = json.loads(max((out/"history").glob("*.meta.json"),
                         key=lambda p:p.stat().st_mtime).read_text())
    directory = Path(meta["analysis_dirs"][kind])
    if not directory.is_absolute():
        directory = out/directory
    return pd.read_csv(directory/f"run_{run}__{test}.csv")


for name, project, sheet_name, result in [
    ("ac", "sky_replica_ac", "ac", "out"),
    ("noise", "sky_replica_validation", "noise", "out/noise"),
    ("replica", "sky_replica_tail", "calibration/trim_tt", "out/trim_tt"),
    ("stability", "sky_replica_validation", "stability", "out/stability"),
    ("transfer", "sky_replica_validation", "transfer", "out/transfer"),
]:
    source = base/project
    sheet = replay/"datasheets"/(name+".yaml")
    out = replay/"out"/name
    integrity = audit(sheet, out)
    audit(source/"datasheets"/(sheet_name+".yaml"), source/result)
    actual = pd.read_csv(out/"simulation_results.csv",dtype={"run_id":str}).iloc[0]
    reference_rows = pd.read_csv(source/result/"simulation_results.csv",dtype={"run_id":str})
    for key in ["temp", "vdd", "corner_mos", "gcode", "ibias"]:
        reference_rows = reference_rows[reference_rows[key] == actual[key]]
    if len(reference_rows) != 1:
        raise ValueError(f"{name}: no unique matching source case")
    expected = reference_rows.iloc[0]
    tests = yaml.safe_load(sheet.read_text())["tests"][name]
    errors = {}
    for metric in tests:
        if metric in RESERVED:
            continue
        a, b = float(actual[metric]), float(expected[metric])
        if not np.isclose(a, b, rtol=1e-5, atol=1e-8):
            raise ValueError(f"{name}/{metric}: drawn={a}, source={b}")
        errors[metric] = abs(a-b)
    if name == "ac":
        data = wave(out, "ac", name, actual.run_id)
        for number in [1, 2]:
            check_curve(data, f"ac{number}.gd", actual[f"acgain_in{number}"],
                        actual[f"bw_in{number}_mhz"])
    elif name == "stability":
        check(sheet, out)
    elif name == "transfer":
        data = wave(out, "dc", name, actual.run_id)
        reference = wave(source/result, "dc", name, expected.run_id)
        for column in ["v(vdin1)", "v(vdin2)", "outdiff", "vocm"]:
            if not np.allclose(data[column], reference[column], rtol=1e-5, atol=1e-8):
                raise ValueError("Drawn transfer differs: " + column)
        integrity["fit"] = fit_surface(data)
        data.to_csv(evidence/"sky_replica_schematic_transfer_surface.csv",index=False)
    report[name] = {"reference_project": project, "reference_datasheet": sheet_name,
                    "reference_run_id": expected.run_id, "audit": integrity, "maximum_absolute_scalar_differences": errors}
    shutil.copy2(out/"simulation_results.csv",evidence/f"sky_replica_schematic_{name}.csv")
(evidence/"sky_replica_schematic_replay_audit.json").write_text(json.dumps(report,indent=2)+"\n")
print(json.dumps({"status":"equivalent","tests":list(report),
                  "scalar_values":sum(v["audit"]["scalar_values"] for v in report.values()),
                  "waveform_files":sum(v["audit"]["waveform_files"] for v in report.values())}))

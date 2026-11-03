#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Audit pass-switch conductance and its parallel-device controls."""
import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from check_chipify_results import audit

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument("--project", default="sky_trim_switch_probe")
args = parser.parse_args()
project = ROOT / "verification/porting" / args.project
out = project / "out"
integrity = audit(project / "datasheets/probe.yaml", out)
meta = json.loads(max((out / "history").glob("*.meta.json"),
                     key=lambda p:p.stat().st_mtime).read_text())
data = pd.read_csv(out / "simulation_results.csv", dtype={"run_id":str})
frames, summary, archive = [], [], {}
for _, row in data.iterrows():
    wave = pd.read_csv(out / meta["analysis_dirs"]["dc"] / ("run_" + row.run_id + "__switches.csv"))
    if not np.allclose(wave.sweep, np.linspace(1.45,1.65,5), rtol=0, atol=1e-12):
        raise ValueError("Wrong supply axis")
    for name in ["n","p","p2","tg","tg2"]:
        if not np.isfinite(wave["ron_"+name]).all() or not (wave["ron_"+name] > 0).all():
            raise ValueError("Invalid on-resistance")
        if not np.isclose(wave["ron_"+name].iloc[1], row["ron_"+name+"_150"], rtol=6e-6):
            raise ValueError("Scalar/capture mismatch")
    for name, expected in [
        ("p2", wave.ron_p/2),
        ("tg", 1/(1/wave.ron_n+1/wave.ron_p)),
        ("tg2", 1/(1/wave.ron_n+1/wave.ron_p2)),
    ]:
        if not np.allclose(wave["ron_"+name], expected, rtol=1e-6):
            raise ValueError("Parallel-device conductance control failed")
    length = float(row.get("n_length", .35))
    record = {"corner_mos":row.corner_mos,"n_length_um":length}
    for name in ["n","p","p2","tg","tg2"]:
        values=wave["ron_"+name]
        record["ron_"+name+"_150"]=float(values.iloc[1])
        record["ron_"+name+"_165_over_145"]=float(values.iloc[-1]/values.iloc[0])
    summary.append(record)
    archive[row.run_id]=wave.to_numpy()
    archive["columns"]=wave.columns.to_numpy(dtype=str)
    wave["corner_mos"]=row.corner_mos
    wave["n_length_um"]=length
    frames.append(wave)
prefix=ROOT/"doc/porting/evidence"/args.project
data.to_csv(str(prefix)+".csv",index=False)
pd.concat(frames,ignore_index=True).to_csv(str(prefix)+"_curves.csv",index=False)
np.savez_compressed(str(prefix)+"_waveforms.npz",**archive)
Path(str(prefix)+"_summary.json").write_text(json.dumps(
    {"audit":integrity,"parallel_controls":"pass","cases":summary},indent=2)+"\n")
print(pd.DataFrame(summary)[["corner_mos","n_length_um","ron_n_150","ron_p_150",
                            "ron_n_165_over_145","ron_p_165_over_145"]].to_string(index=False))

#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Independently audit scalar values, specifications and declared waveform captures."""
import argparse,ast,csv,json,math
from pathlib import Path
import numpy as np
import yaml

RESERVED={"engine","source","measure","transient_signals","dc_signals","ac_signals"}
EMPTY={"","None","none"}
def count(value):
    if isinstance(value,list): return len(value)
    if not isinstance(value,str) or "(" not in value: return 1
    node=ast.parse(value,mode="eval").body
    if not isinstance(node,ast.Call) or not isinstance(node.func,ast.Name) or node.keywords:
        raise ValueError(f"Unsupported parameter sequence: {value}")
    funcs={"range":range,"linspace":np.linspace,"logspace":np.logspace}
    if node.func.id not in funcs: raise ValueError(value)
    args=[ast.literal_eval(a) for a in node.args]
    return len(funcs[node.func.id](*args))

def audit(sheet_path,out,enforce_limits=True):
    spec=yaml.safe_load(sheet_path.read_text())
    expected=math.prod(count(v) for v in spec["parameters"].values())
    result=out/"simulation_results.csv"
    with result.open(newline="") as f:
        reader=csv.DictReader(f);headers=reader.fieldnames;rows=list(reader)
    if len(rows)!=expected: raise ValueError(f"Expected {expected} rows, found {len(rows)}")
    if expected==0: raise ValueError("No parameter cases")
    if "sim_error" not in headers: raise ValueError("Missing simulator validity column")
    history=sorted((out/"history").glob("*.meta.json"),key=lambda p:p.stat().st_mtime)
    meta=json.loads(history[-1].read_text()) if history else {}
    if meta.get("yaml") not in [None,sheet_path.name]:
        raise ValueError("Latest results belong to a different datasheet")
    ids=[r["run_id"] for r in rows]
    if len(set(ids))!=expected: raise ValueError("Repeated run IDs")
    checked=waves=0
    failed_limits=[]
    for row in rows:
        rid=row["run_id"]
        for name,value in row.items():
            if name=="sim_error" or name.endswith("__error") or name.endswith("_capture"):
                if value not in EMPTY: raise ValueError(f"Case {rid}: {name}={value}")
        for tb,tests in spec["tests"].items():
            for key,limits in tests.items():
                if key in RESERVED: continue
                if key not in row: raise ValueError(f"Case {rid}: missing {key}")
                v=float(row[key])
                if not math.isfinite(v): raise ValueError(f"Case {rid}: nonfinite {key}")
                limits=limits or {}
                violation=None
                if limits.get("min") is not None and v<float(limits["min"]):
                    violation=f"Case {rid}: {key}={v} below {limits['min']}"
                if limits.get("max") is not None and v>float(limits["max"]):
                    violation=f"Case {rid}: {key}={v} above {limits['max']}"
                if violation:
                    failed_limits.append(violation)
                    if enforce_limits: raise ValueError(violation)
                checked+=1
            for kind,field in [("dc","dc_signals"),("tran","transient_signals"),("ac","ac_signals")]:
                signals=tests.get(field,[])
                if not signals: continue
                folder=meta.get("analysis_dirs",{}).get(kind)
                if not folder: raise ValueError(f"Missing {kind} capture directory")
                folder=Path(folder);folder=folder if folder.is_absolute() else out/folder
                wave=folder/f"run_{rid}__{tb}.csv"
                with wave.open(newline="") as f:
                    reader=csv.DictReader(f);cols=reader.fieldnames;data=list(reader)
                if len(data)<2: raise ValueError(f"Empty waveform: {wave}")
                for signal in signals:
                    want=[signal+"_mag",signal+"_phase"] if kind=="ac" else [signal]
                    for column in want:
                        if column not in cols: raise ValueError(f"Missing {column} in {wave}")
                        if any(not math.isfinite(float(d[column])) for d in data):
                            raise ValueError(f"Nonfinite {column} in {wave}")
                waves+=1
    return {"cases":expected,"scalar_values":checked,"waveform_files":waves,"status":"valid","specification_status":"fail" if failed_limits else "pass","failed_limits":failed_limits}
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("datasheet",type=Path);ap.add_argument("out",type=Path)
    ap.add_argument("--allow-spec-fail",action="store_true",help="Audit data integrity and report all failed limits without rejecting the run")
    args=ap.parse_args()
    print(json.dumps(audit(args.datasheet,args.out,not args.allow_spec_fail),sort_keys=True))
if __name__=="__main__": main()

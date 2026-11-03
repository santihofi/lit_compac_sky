#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Audit switch-candidate endpoint screens without claiming calibrated performance."""
import json
from pathlib import Path
import pandas as pd
from check_chipify_results import audit

ROOT=Path(__file__).resolve().parents[1]
evidence=ROOT/"doc/porting/evidence"
for mode in ["pmos4","tg2"]:
    project=ROOT/"verification/porting"/("sky_trim_"+mode)
    frames,checks=[],{}
    for sheet in sorted((project/"datasheets/endpoints").glob("*.yaml")):
        out=project/"out"/sheet.stem
        checks[sheet.name]=audit(sheet,out,False)
        frames.append(pd.read_csv(out/"simulation_results.csv"))
    data=pd.concat(frames,ignore_index=True)
    if len(data)!=10:
        raise ValueError("Expected ten endpoint cases")
    records=[]
    for corner,group in data.groupby("corner_mos"):
        if sorted(group.gcode)!=[0,31]:
            raise ValueError("Missing endpoint pair")
        record={"corner":corner}
        for metric in ["k100","k10"]:
            values=group[metric].abs()
            record[metric+"_min"]=float(values.min())
            record[metric+"_max"]=float(values.max())
            record[metric+"_brackets10"]=bool(values.min()<=10<=values.max())
        record["endpoint_shape_passes"]=int(group.compr.between(.96758,1.03242).sum())
        records.append(record)
    prefix=evidence/("sky_trim_"+mode+"_endpoints")
    data.to_csv(str(prefix)+".csv",index=False)
    Path(str(prefix)+"_summary.json").write_text(json.dumps({"audits":checks,"coverage":records},indent=2)+"\n")
    print(mode)
    print(pd.DataFrame(records).to_string(index=False))

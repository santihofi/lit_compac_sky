#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Measure nominal code monotonicity, step size and nearest target code."""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from check_chipify_results import audit

ROOT=Path(__file__).resolve().parents[1]
evidence=ROOT/"doc/porting/evidence"
report={}
fig,axes=plt.subplots(1,2,figsize=(10,4),constrained_layout=True)
for label,project in [("IHP","ihp_gain_trim"),("SKY130 replica","sky_replica_gain_trim")]:
    p=ROOT/"verification/porting"/project
    out=p/"out/steps_tt"
    result=audit(p/"datasheets/steps/steps_tt.yaml",out,False)
    data=pd.read_csv(out/"simulation_results.csv").sort_values("gcode")
    if data.gcode.tolist()!=list(range(32)):
        raise ValueError("Incomplete code sweep")
    data.to_csv(evidence/(project+"_nominal_steps.csv"),index=False)
    values={}
    for metric in ["k100","k10"]:
        magnitude=data[metric].abs().to_numpy()
        steps=np.diff(magnitude)
        best=int(np.argmin(abs(magnitude-10)))
        values[metric]=dict(minimum_gain=float(magnitude.min()),maximum_gain=float(magnitude.max()),
            strictly_monotonic=bool(np.all(steps>0)),minimum_step_per_v=float(steps.min()),
            maximum_step_per_v=float(steps.max()),nearest_code=best,
            nearest_gain=float(magnitude[best]),nearest_error_percent=float((magnitude[best]/10-1)*100))
    report[label]={"audit":result,"metrics":values}
    axes[0].plot(data.gcode,data.k100.abs(),"o-",label=label,markersize=3)
    axes[1].plot(range(1,32),np.diff(data.k100.abs())/10*100,"o-",label=label,markersize=3)
axes[0].axhline(10,color="black",linewidth=.8)
axes[0].set(xlabel="Gain code",ylabel="|K100| (1/V)")
axes[1].set(xlabel="Destination code",ylabel="Step (% of target gain 10)")
for ax in axes: ax.grid(True,alpha=.25)
axes[0].legend()
fig.suptitle("Nominal gain trim | tt, 27 C, 1.5 V, ideal fixed bias")
for ext in ["png","pdf"]:
    fig.savefig(ROOT/"doc/porting/figures"/("replica_ihp_gain_steps."+ext),dpi=180)
(evidence/"replica_ihp_gain_steps_summary.json").write_text(json.dumps(report,indent=2)+"\n")
print(json.dumps(report,indent=2))

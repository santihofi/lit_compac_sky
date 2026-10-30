#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Audit and retain current-kick traces, including a maximum-step comparison."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from check_chipify_results import audit
ROOT=Path(__file__).resolve().parents[1]
p=ROOT/'verification/porting/sky_cmfb_kick'
audit(p/'datasheets/kick.yaml',p/'out',False)
meta=json.loads(max((p/'out/history').glob('*.meta.json'),key=lambda f:f.stat().st_mtime).read_text())
directory=p/'out'/meta['analysis_dirs']['transient']
rows=pd.read_csv(p/'out/simulation_results.csv',dtype={'run_id':str})
report=[];arrays={}
fig,axes=plt.subplots(1,2,figsize=(10,4),layout='constrained')
for _,row in rows.iterrows():
    w=pd.read_csv(directory/('run_'+row.run_id+'__kick.csv'))
    t=w.iloc[:,0].to_numpy();e=w.err.to_numpy()
    if not (np.all(np.diff(t)>0) and abs(t[-1]-1e-6)<1e-12):
        raise ValueError('Incomplete or nonmonotonic transient')
    key=f"r{row.cmfb_rscale:g}_c{row.cmfb_cscale:g}_{row.maxstep}".replace('.','p')
    arrays[key]=np.column_stack([t,w.cm,e,w['v(vbias)']])
    outside=np.flatnonzero((t>=120.2e-9)&(abs(e)>1e-3))
    settle=None if len(outside) and outside[-1]==len(t)-1 else float((t[outside[-1]+1] if len(outside) else 120.2e-9)-120.2e-9)*1e9
    report.append({'case':key,'settle_1mv_after_pulse_ns':settle,'within_1mv_at_end':bool(abs(e[-1])<=1e-3)})
    if row.cmfb_rscale==1.5:
        label=f"C x{row.cmfb_cscale:g}, max step {row.maxstep}"
        for ax in axes:ax.plot(t*1e9,e*1e3,label=label,lw=1,ls='--' if row.maxstep=='50p' else '-')
for ax in axes:ax.set(xlabel='Time (ns)',ylabel='Common-mode error (mV)');ax.grid(alpha=.2)
axes[0].set(xlim=(80,350),title='80 uA, 20 ns load-gate current kick')
axes[1].set(xlim=(300,1000),ylim=(-5,5),title='Recovery at fast-loop R scale 1.5')
axes[1].axhline(1,color='grey',lw=.7);axes[1].axhline(-1,color='grey',lw=.7)
axes[0].legend(fontsize=8)
e=ROOT/'doc/porting/evidence'
np.savez_compressed(e/'sky_cmfb_kick_waveforms.npz',**arrays)
(e/'sky_cmfb_kick_settling.json').write_text(json.dumps(report,indent=2)+'\n')
for ext in ['png','pdf']:fig.savefig(ROOT/'doc/porting/figures'/('sky_cmfb_kick.'+ext),dpi=180)
print(json.dumps(report,indent=2))

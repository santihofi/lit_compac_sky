#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Compare corners by transistor skew, preserving original labels in CSV evidence."""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
e=ROOT/'doc/porting/evidence'
fig,axes=plt.subplots(2,3,figsize=(12,7),layout='constrained')
labels=['tt','ss','ff','N slow\nP fast','N fast\nP slow']
metrics=[('k100',-1,'|K100| (1/V)'),('compr',1,'K100/K10'),
         ('idd',1e3,'Supply current (mA)'),('bw_in1_mhz',1,'Input-1 bandwidth (MHz)'),
         ('bw_in2_mhz',1,'Input-2 bandwidth (MHz)'),('vocm',1e3,'Output common mode (mV)')]
for file,label,corners,dx,color in [
    ('ihp_core_corners.csv','IHP current core',['tt','ss','ff','sf','fs'],-.12,'#202020'),
    ('sky_degenerated_corners.csv','SKY130 degeneration candidate',['tt','ss','ff','fs','sf'],.12,'#007b95')]:
    d=pd.read_csv(e/file)
    for ax,(key,scale,title) in zip(axes.flat,metrics):
        means=[];low=[];high=[]
        for corner in corners:
            v=d.loc[d.corner_mos==corner,key]*scale
            means.append(v.mean());low.append(v.min());high.append(v.max())
        means=np.array(means)
        ax.errorbar(np.arange(5)+dx,means,yerr=[means-np.array(low),np.array(high)-means],fmt='o',capsize=4,color=color,label=label,ms=4)
        ax.set(xticks=range(5),xticklabels=labels,ylabel=title)
        ax.grid(axis='y',alpha=.2)
axes[0,1].axhline(1,color='grey',lw=.7)
for v in [.96758,1.03242]:axes[0,1].axhline(v,color='red',ls=':',lw=.7)
axes[0,0].legend(fontsize=8)
fig.suptitle('Matched transistor skews, schematic results at fixed gain code 13\nBars span 1.45/1.50/1.65 V and 0/27/80 C, 100 fF per output',fontsize=12)
for ext in ['png','pdf']:fig.savefig(ROOT/'doc/porting/figures'/('matched_corner_comparison.'+ext),dpi=180)

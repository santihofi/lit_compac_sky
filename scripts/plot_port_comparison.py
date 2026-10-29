#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Plot measured exploratory candidates without implying schematic qualification."""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
E=ROOT/'doc/porting/evidence'
OUT=ROOT/'doc/porting/figures'
OUT.mkdir(exist_ok=True)
fig,axes=plt.subplots(2,2,figsize=(11,8),layout='constrained')
series=[('Short mirrors','sky_core_short_mirror.csv','#7e57c2'),
        ('Long mirrors','sky_core_long_mirror.csv','#ef8a17'),
        ('Parallel copies','sky_core_parallel_scaling.csv','#00897b'),
        ('Native quad probes','sky_native_quad.csv','#1565c0')]
ref=pd.read_csv(E/'ihp_core_identical_load.csv').iloc[0]
for name,file,color in series:
 d=pd.read_csv(E/file)
 for ax,x,y in [(axes[0,0],-d.k100,d.compr),(axes[0,1],d.bw_in1_mhz,1000*d.mirror_margin),
                (axes[1,0],d.bw_in1_mhz,d.bw_in2_mhz),(axes[1,1],1000*d.idd,-d.k100)]:
  ax.scatter(x,y,color=color,label=name,s=27,alpha=.75)
for ax,x,y in [(axes[0,0],-ref.k100,ref.compr),(axes[0,1],ref.bw_in1_mhz,1000*ref.mirror_margin),
               (axes[1,0],ref.bw_in1_mhz,ref.bw_in2_mhz),(axes[1,1],1000*ref.idd,-ref.k100)]:
 ax.scatter([x],[y],marker='*',s=170,color='black',label='IHP reference',zorder=5)
 ax.grid(alpha=.2)
axes[0,0].axhline(1,color='grey',lw=.7)
axes[0,0].set(xlabel='|K100| (1/V)',ylabel='K100 / K10',title='Nominal gain and curvature')
axes[0,1].axhline(0,color='red',lw=.7)
axes[0,1].set(xlabel='Input 1 bandwidth (MHz)',ylabel='Mirror VDS − VDSAT (mV)',title='Speed and voltage margin')
axes[1,0].set(xlabel='Input 1 bandwidth (MHz)',ylabel='Input 2 bandwidth (MHz)',title='Both paths, 100 fF per output')
axes[1,1].set(xlabel='Supply current (mA)',ylabel='|K100| (1/V)',title='Gain and current cost')
axes[0,0].legend(fontsize=8,loc='lower left')
fig.suptitle('Schematic exploration at 1.5 V and 27 °C\nNo candidate is qualified across corners',fontsize=13)
for ext in ['png','pdf']:fig.savefig(OUT/('core_tradeoffs.'+ext),dpi=170)
plt.close(fig)
d=pd.read_csv(E/'sky_candidate_corners.csv')
fig,axes=plt.subplots(1,3,figsize=(12,3.8),layout='constrained')
for corner,g in d.groupby('corner_mos'):
 for ax,y in zip(axes,[g.compr,1000*g.mirror_margin,1000*g.tail_margin]):
  ax.scatter(g.temp,y,label=corner,s=30,alpha=.7)
for ax,title in zip(axes,['K100 / K10','Mirror margin (mV)','Tail margin (mV)']):
 ax.set(xlabel='Temperature (°C)',ylabel=title)
 ax.grid(alpha=.2)
for y in [.96758,1.03242]:axes[0].axhline(y,color='red',lw=.8)
for ax in axes[1:]:ax.axhline(0,color='red',lw=.8)
axes[0].legend(title='MOS corner',fontsize=8)
fig.suptitle('Rejected all-LVT candidate: 20/45 meet provisional checks\n1.45, 1.50 and 1.65 V, fixed gain code 13',fontsize=12)
for ext in ['png','pdf']:fig.savefig(OUT/('candidate_corners.'+ext),dpi=170)

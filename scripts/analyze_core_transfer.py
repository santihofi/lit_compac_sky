#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Freeze an audited two-input transfer sweep and fit its bilinear residual."""
from pathlib import Path
import argparse,json,shutil
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from check_chipify_results import audit

ROOT=Path(__file__).resolve().parents[1]
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--project',required=True)
    ap.add_argument('--label',required=True)
    args=ap.parse_args()
    p=ROOT/'verification/porting'/args.project
    result=audit(p/'datasheets/transfer.yaml',p/'out')
    meta=max((p/'out/history').glob('*.meta.json'),key=lambda f:f.stat().st_mtime)
    info=json.loads(meta.read_text())
    waves=list((p/'out'/info['analysis_dirs']['dc']).glob('*__transfer.csv'))
    if len(waves)!=1:raise ValueError('Expected exactly one nominal transfer surface')
    data=pd.read_csv(waves[0])
    x=data['v(vdin1)'].to_numpy();y=data['v(vdin2)'].to_numpy()
    z=data['outdiff'].to_numpy()
    if len(set(zip(x,y)))!=1681:raise ValueError('Repeated or missing input coordinates')
    if not np.allclose([x.min(),x.max(),y.min(),y.max()],[-.1,.1,-.1,.1]):raise ValueError('Wrong sweep bounds')
    a=np.column_stack([np.ones_like(x),x,y,x*y])
    coef=np.linalg.lstsq(a,z,rcond=None)[0]
    residual=z-a@coef
    fullscale=abs(coef[3]*.01)
    report={'audit':result,'fit_offset_v':coef[0],'fit_input1_feedthrough':coef[1],
            'fit_input2_feedthrough':coef[2],'fit_product_gain_per_v':coef[3],
            'peak_residual_v':float(abs(residual).max()),
            'rms_residual_v':float(np.sqrt(np.mean(residual**2))),
            'peak_residual_percent_fullscale':float(abs(residual).max()/fullscale*100),
            'rms_residual_percent_fullscale':float(np.sqrt(np.mean(residual**2))/fullscale*100)}
    dst=ROOT/'doc/porting/evidence'
    shutil.copy2(waves[0],dst/(args.label+'_transfer_surface.csv'))
    (dst/(args.label+'_transfer_fit.json')).write_text(json.dumps(report,indent=2)+'\n')
    fig,axes=plt.subplots(1,2,figsize=(9,3.6),constrained_layout=True)
    for ax,col,title in [(axes[0],z*1e3,'Differential output (mV)'),(axes[1],residual*1e3,'Residual after bilinear fit (mV)')]:
        grid=pd.DataFrame({'x':x*1e3,'y':y*1e3,'z':col}).pivot(index='y',columns='x',values='z')
        im=ax.imshow(grid,origin='lower',extent=[-100,100,-100,100],cmap='RdBu_r',aspect='equal')
        ax.set(xlabel='Input 1 differential (mV)',ylabel='Input 2 differential (mV)',title=title)
        fig.colorbar(im,ax=ax,shrink=.8)
    fig.suptitle(args.label.replace('_',' ')+' | tt, 27 C, 1.5 V, code 13')
    for ext in ['png','pdf']:fig.savefig(ROOT/'doc/porting/figures'/(args.label+'_transfer.'+ext),dpi=180)
    print(json.dumps(report,indent=2))
if __name__=='__main__':main()

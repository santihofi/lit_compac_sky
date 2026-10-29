#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Probe quad device and body options before deciding the physical implementation."""
from pathlib import Path
import json,re,yaml
ROOT=Path(__file__).resolve().parents[1]
src=ROOT/'verification/porting/sky_core_tradeoffs'
p=ROOT/'verification/porting/sky_quad_options'
(p/'tb').mkdir(exist_ok=True,parents=True)
(p/'datasheets').mkdir(exist_ok=True)
s=(src/'tb/core_scaled.spice').read_text()
start=s.index('.subckt gilbert_cell ');end=s.index('.ends',start)
core=s[start:end]
def quad(m):
    line=m.group()
    tokens=line.split()
    if tokens[0] in ['XM7','XM8','XM9','XM10','XMDQ1','XMDQ2']:
        line=line.replace(' sky130_fd_pr__nfet_01v8_lvt ',' sky130_fd_pr__{{quad_model}} ')
        body="{{'"+tokens[3]+"' if body_tied else 'ptap'}}"
        line=re.sub(r'^(\S+ \S+ \S+ \S+) ptap ',lambda m:m.group(1)+' '+body+' ',line)
        native={'W':'4*native_nf','nf':'native_nf',
                'ad':'(((native_nf+1)/2)|int)*4*0.29','as':'(((native_nf+2)/2)|int)*4*0.29',
                'pd':'2*(((native_nf+1)/2)|int)*4.29','ps':'2*(((native_nf+2)/2)|int)*4.29'}
        for key,expr in native.items():
            pattern=r'\b'+key+r'=(\{\{.*?\}\}|\S+)'
            match=re.search(pattern,line)
            old=match.group(1).strip('{}')
            val=key+"={{("+expr+") if quad_model=='nfet_03v3_nvt' else ("+old+")}}"
            line=line[:match.start()]+val+line[match.end():]
    return line
core=re.sub(r'^XM\S+ [^\n]+(?:\n\+[^\n]+)*',quad,core,flags=re.M)
s=s[:start]+core+s[end:]
s=s.replace('@m.x1.xm7.msky130_fd_pr__nfet_01v8_lvt','@m.x1.xm7.msky130_fd_pr__{{quad_model}}')
def access(m):
    line=m.group()
    match=re.search(r'\bW=(\{\{.*?\}\}|\S+)',line)
    if not match:return line
    w=match.group(1).strip('{}')
    for key in ['nrd','nrs']:
        line=re.sub(r'\b'+key+r'=\S+',key+'={{0.29/('+w+')}}',line)
    return line
s=re.sub(r'^XM\S+ [^\n]+(?:\n\+[^\n]+)*',access,s,flags=re.M)
(p/'tb/core_options.spice').write_text(s)
d=yaml.safe_load((src/'datasheets/power.yaml').read_text())
d['parameters'].update(mirror_scale=[4],mirror_l=[0.5],pair_scale=[0.75],quad_scale=[0.5,1],quad_l=[0.15,0.25,0.5],rscale=[1.14],power_m=[2],quad_model=['nfet_01v8_lvt'],body_tied=[0,1],native_nf=[1])
d['tests']={'core_options':d['tests']['core_scaled']}
header='# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer\n# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1\n'
(p/'datasheets/body.yaml').write_text(header+yaml.safe_dump(d,sort_keys=False))
d['parameters'].update(quad_model=['nfet_03v3_nvt'],body_tied=[0],quad_scale=[0.5],quad_l=[0.5],native_nf=[1,2,4,8])
(p/'datasheets/native.yaml').write_text(header+yaml.safe_dump(d,sort_keys=False))
(p/'settings.json').write_text(json.dumps({'num_cores':2,'sim_timeout_sec':180},indent=2)+'\n')

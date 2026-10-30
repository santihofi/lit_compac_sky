#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Explore quad source degeneration with ideal resistors before selecting PDK geometry."""
from pathlib import Path
import re,json,yaml
ROOT=Path(__file__).resolve().parents[1]
src=ROOT/'verification/porting/sky_quad_options'
p=ROOT/'verification/porting/sky_degenerated'
(p/'tb').mkdir(exist_ok=True,parents=True)
(p/'datasheets').mkdir(exist_ok=True)
s=(src/'tb/core_options.spice').read_text()
start=s.index('.subckt gilbert_cell ');end=s.index('.ends',start)
core=s[start:end]
add=[]
for n in [7,8,9,10]:
 pattern=r'^(XM'+str(n)+r' \S+ \S+) (qs[12]) '
 m=re.search(pattern,core,re.M)
 assert m
 node='qd'+str(n)
 core=core[:m.start()]+m.group(1)+' '+node+' '+core[m.end():]
 add.append('Rdegen'+str(n)+' '+node+' '+m.group(2)+" '{{rquad/power_m}}'")
core+='\n'+'\n'.join(add)+'\n'
s=s[:start]+core+s[end:]
s=s.replace('let quad_margin=(v(outp)-v(x1.qs1))','let quad_margin=(v(outp)-v(x1.qd7))')
(p/'tb/degenerated.spice').write_text(s)
d=yaml.safe_load((src/'datasheets/native_corners.yaml').read_text())
d['parameters'].update(quad_model=['nfet_01v8_lvt'],body_tied=[0],quad_scale=[1,2,4],quad_l=[0.15],rquad=[0.001,200,400,800],mirror_scale=[8],mirror_l=[0.5],pair_scale=[2],native_nf=[1],rscale=[1.4],power_m=[4],vdd=[1.5],temp=[27],corner_mos=['tt'])
d['tests']={'degenerated':d['tests']['core_options']}
for key in d['tests']['degenerated']:
 if key not in ['source','engine']:d['tests']['degenerated'][key]={}
header='# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer\n# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1\n'
(p/'datasheets/sizing.yaml').write_text(header+yaml.safe_dump(d,sort_keys=False))
(p/'settings.json').write_text(json.dumps({'num_cores':4,'sim_timeout_sec':180},indent=2)+'\n')

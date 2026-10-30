#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Increase fast-loop drive at constant device voltage and low-frequency loop gain."""
from pathlib import Path
import re,yaml,json
ROOT=Path(__file__).resolve().parents[1]
src=ROOT/'verification/porting/sky_cmfb_options'
p=ROOT/'verification/porting/sky_cmfb_drive'
(p/'tb').mkdir(parents=True,exist_ok=True);(p/'datasheets').mkdir(exist_ok=True)
s=(src/'tb/stability_sizing.spice').read_text()
s=s.replace('I1 vdd ibias_ota {{ibias*power_m}}','I1 vdd ibias_ota {{ibias*power_m*fast_scale}}')
start=s.index('.subckt ota ');end=s.index('.ends',start)
ota=s[start:end]
fast={'XM1','XM2','XM3A','XM3B','XM4','XM5','XM6','XMDA','XMDB','XMD3','XMD4','XMD5','XMD6'}
def scale(m):
 line=m[0]
 if line.split()[0] in fast or line.startswith('XRS'):
  line=line.replace('1.0*power_m','fast_scale*power_m').replace('1*power_m','fast_scale*power_m')
 return line
ota=re.sub(r'^X\S+ [^\n]+(?:\n\+[^\n]+)*',scale,ota,flags=re.M)
s=s[:start]+ota+s[end:]
s=s.replace('\nop\n','\nop\nlet idd_dc=-i(vdd)\n',1)
s=s.replace('\nquit\n','\nlet idd_dc=op1.idd_dc\nquit\n',1)
(p/'tb/stability_drive.spice').write_text(s)
d=yaml.safe_load((src/'datasheets/stability_sizing.yaml').read_text())
d['parameters'].update(cmfb_rscale=[1.5],cmfb_cscale=[4,16],fast_scale=[1,2,4],c_load=['100f'])
d['tests']={'stability_drive':d['tests']['stability_sizing']}
d['tests']['stability_drive']['idd_dc']={}
header='# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer\n# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1\n'
(p/'datasheets/sizing.yaml').write_text(header+yaml.safe_dump(d,sort_keys=False))
(p/'settings.json').write_text(json.dumps({'num_cores':2,'sim_timeout_sec':180})+'\n')

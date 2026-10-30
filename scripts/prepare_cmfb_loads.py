#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Test shorter mirror loads with constant W/L and recomputed parasitic geometry."""
from pathlib import Path
import re,yaml,json
ROOT=Path(__file__).resolve().parents[1]
src=ROOT/'verification/porting/sky_cmfb_options'
p=ROOT/'verification/porting/sky_cmfb_loads'
(p/'tb').mkdir(parents=True,exist_ok=True);(p/'datasheets').mkdir(exist_ok=True)
s=(src/'tb/stability_sizing.spice').read_text()
for subckt,names in [('gilbert_cell',{'XM11','XM12','XMDL'}),('ota',{'XM5','XM6'})]:
 start=s.index('.subckt '+subckt+' ');end=s.index('.ends',start)
 def resize(m):
  line=m[0]
  if line.split()[0] not in names:return line
  w=float(re.search(r'\bW=(\S+)',line)[1]);nf=int(re.search(r'\bnf=(\S+)',line)[1])
  wf=f'({w/nf}*pload_l)'
  updates={'L':'pload_l','W':f'{w}*pload_l','ad':f'{int((nf+1)/2)}*{wf}*0.29','as':f'{int((nf+2)/2)}*{wf}*0.29','pd':f'{2*int((nf+1)/2)}*({wf}+0.29)','ps':f'{2*int((nf+2)/2)}*({wf}+0.29)','nrd':f'0.29/({w}*pload_l)','nrs':f'0.29/({w}*pload_l)'}
  for key,val in updates.items():line=re.sub(r'\b'+key+r'=(?:{{.*?}}|\S+)',key+'={{'+val+'}}',line)
  return line
 part=re.sub(r'^XM\S+ [^\n]+(?:\n\+[^\n]+)*',resize,s[start:end],flags=re.M)
 s=s[:start]+part+s[end:]
s=s.replace('\nop\n','\nop\nlet idd_dc=-i(vdd)\n',1).replace('\nquit\n','\nlet idd_dc=op1.idd_dc\nquit\n',1)
(p/'tb/stability_loads.spice').write_text(s)
d=yaml.safe_load((src/'datasheets/stability_sizing.yaml').read_text())
d['parameters'].update(pload_l=[.35,.5,1],cmfb_rscale=[1,1.5],cmfb_cscale=[4],c_load=['100f'])
d['tests']={'stability_loads':d['tests']['stability_sizing']}
d['tests']['stability_loads']['idd_dc']={}
header='# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer\n# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1\n'
(p/'datasheets/sizing.yaml').write_text(header+yaml.safe_dump(d,sort_keys=False))
(p/'settings.json').write_text(json.dumps({'num_cores':2,'sim_timeout_sec':180})+'\n')

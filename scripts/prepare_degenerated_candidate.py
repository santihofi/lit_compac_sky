#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Prepare a corner candidate with wider tail devices and modeled degeneration."""
from pathlib import Path
import re,yaml
ROOT=Path(__file__).resolve().parents[1]
p=ROOT/'verification/porting/sky_degenerated'
s=(p/'tb/degenerated.spice').read_text()
start=s.index('.subckt gilbert_cell ');end=s.index('.ends',start)
core=s[start:end]
def resize(m):
    line=m.group()
    if line.split()[0] not in ['XM13','XM14','XMDT']:return line
    w=float(re.search(r'\bW=(\S+)',line).group(1))
    nf=int(re.search(r'\bnf=(\S+)',line).group(1))
    wf=w/nf
    updates={'W':f'{w}*tail_width','nf':f'({nf}*tail_width)|int',
             'ad':f'((({nf}*tail_width+1)/2)|int)*{wf}*0.29',
             'as':f'((({nf}*tail_width+2)/2)|int)*{wf}*0.29',
             'pd':f'2*((({nf}*tail_width+1)/2)|int)*({wf}+0.29)',
             'ps':f'2*((({nf}*tail_width+2)/2)|int)*({wf}+0.29)',
             'nrd':f'0.29/({w}*tail_width)','nrs':f'0.29/({w}*tail_width)'}
    for key,val in updates.items():
        line=re.sub(r'\b'+key+r'=\S+',key+'={{'+val+'}}',line)
    return line
core=re.sub(r'^XM\S+ [^\n]+(?:\n\+[^\n]+)*',resize,core,flags=re.M)
# Electrical and statistical copies both follow the circuit scale.
core=re.sub(r"^Rdegen(\d+) (\S+) (\S+) .*",
            r'XRdegen\1 \2 \3 ptap sky130_fd_pr__res_high_po_5p73 L={{(rquad-68.05)/56.46}} mult={{power_m}} m={{power_m}}',core,flags=re.M)
s=s[:start]+core+s[end:]
(p/'tb/candidate.spice').write_text(s)
d=yaml.safe_load((p/'datasheets/refine.yaml').read_text())
d['parameters'].update(quad_scale=[2],rquad=[240],mirror_scale=[6],rscale=[0.99],power_m=[4],tail_width=[2])
d['tests']={'candidate':d['tests']['degenerated']}
header='# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer\n# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1\n'
(p/'datasheets/candidate_nominal.yaml').write_text(header+yaml.safe_dump(d,sort_keys=False))
d['parameters'].update(vdd=[1.45,1.5,1.65],temp=[0,27,80],corner_mos=['tt','ss','ff','sf','fs'])
d['tests']['candidate']['compr']={'min':0.96758,'max':1.03242}
(p/'datasheets/candidate_corners.yaml').write_text(header+yaml.safe_dump(d,sort_keys=False))

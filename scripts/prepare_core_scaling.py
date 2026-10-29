#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Explore parallel circuit copies at constant voltage and unchanged external load."""
from pathlib import Path
import re,yaml
ROOT=Path(__file__).resolve().parents[1]
p=ROOT/'verification/porting/sky_core_tradeoffs'
s=(p/'tb/core.spice').read_text()
def scale(m):
    line=m.group()
    for key in ['mult','m']:
        match=re.search(r'\b'+key+r'=(\d+(?:\.\d+)?)\b',line)
        old=float(match.group(1)) if match else 1
        value=key+'={{'+str(old)+'*power_m}}'
        if match:line=line[:match.start()]+value+line[match.end():]
        else:line+=' '+value
    return line
s=re.sub(r'^X[MR]\S+ [^\n]+(?:\n\+[^\n]+)*',scale,s,flags=re.M)
s=s.replace('{{ibias}}','{{ibias*power_m}}')
(p/'tb/core_scaled.spice').write_text(s)
d=yaml.safe_load((p/'datasheets/long_mirror.yaml').read_text())
d['parameters'].update(mirror_scale=[4,6],mirror_l=[0.5],pair_scale=[0.75,1],quad_scale=[0.5],quad_l=[0.15,0.18],rscale=[1.1],power_m=[1,2,4],ibias=[40e-6])
d['tests']={'core_scaled':d['tests']['core']}
(p/'datasheets/power.yaml').write_text('# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer\n# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1\n'+yaml.safe_dump(d,sort_keys=False))

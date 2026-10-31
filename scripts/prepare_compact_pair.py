#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Measure the speed and curvature cost of reducing the doubly degenerated core."""
from pathlib import Path
import re,yaml,json
ROOT=Path(__file__).resolve().parents[1]
src=ROOT/'verification/porting/sky_pair_degenerated'
p=ROOT/'verification/porting/sky_compact_pair'
(p/'tb').mkdir(parents=True,exist_ok=True);(p/'datasheets').mkdir(exist_ok=True)
s=(src/'tb/curvature.spice').read_text()
ac=(ROOT/'verification/porting/sky_pair_ac/tb/ac.spice').read_text()
control=re.search(r'\.control\b(.*?)\.endc',ac,re.S)[1]
control=control[control.index('alter vd1 dc=0\n'):]
d=yaml.safe_load((src/'datasheets/calibration_probe.yaml').read_text())
metrics=[k for k in d['tests']['curvature'] if k not in ['engine','source']]
# ngspice names the first AC plot ac17 when seventeen OP plots remain.
# Preserve scalar values before clearing those plots for Chipify's ac1 capture.
control='\n'.join(f'set dc_{k}=$&{k}' for k in metrics)+'\ndestroy all\n'+control
control=control.replace('let idd=op1.idd\n','')
control=control.replace('\nquit\n','\n'+'\n'.join(f'let {k}=$dc_{k}' for k in metrics)+'\nquit\n')
s=s.replace('\nquit\n.endc','\n'+control+'.endc',1)
(p/'tb/compact.spice').write_text(s)
d['parameters'].update(corner_mos=['tt'],temp=[27],vdd=[1.5],mirror_scale=[4],mirror_l=[.15,.25,.3],quad_scale=[1,2],rquad=[120,180,240],pair_scale=[1],rpair=[120],rscale=[1.38],power_m=[2],tail_width=[4],ibias=[40e-6])
extra=yaml.safe_load((ROOT/'verification/porting/sky_pair_ac/datasheets/ac.yaml').read_text())['tests']['ac']
d['tests']={'compact':{**d['tests']['curvature'],**extra}}
header='# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer\n# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1\n'
(p/'datasheets/sizing.yaml').write_text(header+yaml.safe_dump(d,sort_keys=False))
(p/'settings.json').write_text(json.dumps({'num_cores':4,'sim_timeout_sec':180})+'\n')

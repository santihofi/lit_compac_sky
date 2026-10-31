#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Trade input-pair overdrive for modeled source degeneration and tail headroom."""
from pathlib import Path
import re,json,yaml
ROOT=Path(__file__).resolve().parents[1]
src=ROOT/'verification/porting/sky_curvature'
p=ROOT/'verification/porting/sky_pair_degenerated'
(p/'tb').mkdir(parents=True,exist_ok=True);(p/'datasheets').mkdir(exist_ok=True)
s=(src/'tb/curvature.spice').read_text()
start=s.index('.subckt gilbert_cell ');end=s.index('.ends',start)
core=s[start:end]
for n in [1,2]:
 core,count=re.subn(r'^(XM'+str(n)+r' \S+ \S+) vcm1 ',r'\1 ps'+str(n)+' ',core,flags=re.M)
 assert count==1
 core+=f'XRP{n} vcm1 ps{n} ptap sky130_fd_pr__res_high_po_5p73 L={{{{(rpair-68.05)/56.46}}}} mult={{{{power_m}}}} m={{{{power_m}}}}\n'
s=s[:start]+core+s[end:]
s=s.replace('let pair_margin=(v(x1.vcm1)-v(x1.net1))','let pair_margin=(v(x1.ps1)-v(x1.net1))')
(p/'tb/curvature.spice').write_text(s)
d=yaml.safe_load((src/'datasheets/calibration/trim_tt.yaml').read_text())
d['parameters'].update(ibias=[40e-6],pair_scale=[1,2],rpair=[120,180,240],quad_scale=[4],rquad=[180],rscale=[1.3])
header='# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer\n# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1\n'
for name,corner,vdd,temp in [('nominal','tt',1.5,27),('cold_ss','ss',1.45,0),('cold_sf','sf',1.45,0)]:
 d['parameters'].update(corner_mos=[corner],vdd=[vdd],temp=[temp])
 (p/'datasheets'/(name+'.yaml')).write_text(header+yaml.safe_dump(d,sort_keys=False))
(p/'settings.json').write_text(json.dumps({'num_cores':4,'sim_timeout_sec':180})+'\n')

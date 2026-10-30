#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Separate each input's curvature before optimizing the corner response."""
from pathlib import Path
import re,yaml,json
ROOT=Path(__file__).resolve().parents[1]
src=ROOT/'verification/porting/sky_degenerated'
p=ROOT/'verification/porting/sky_curvature'
(p/'tb').mkdir(parents=True,exist_ok=True)
(p/'datasheets').mkdir(exist_ok=True)
s=(src/'tb/candidate.spice').read_text()
c=re.search(r'\.control\b(.*?)\.endc',s,re.S)[1]
c=c[:c.index('alter vd1 dc=0\nalter vd2 dc=0.1\nalter @')]
extra=[]
for x,y in [(.1,.01),(-.1,.01),(-.1,-.01),(.1,-.01),(.01,.1),(-.01,.1),(-.01,-.1),(.01,-.1)]:
    extra += [f'alter vd1 dc={x}',f'alter vd2 dc={y}','op','let vo=v(outp)-v(outn)']
extra += ['let kaxis1=(op10.vo-op11.vo+op12.vo-op13.vo)/0.004',
          'let kaxis2=(op14.vo-op15.vo+op16.vo-op17.vo)/0.004',
          'let axis1=kaxis1/op9.k10','let axis2=kaxis2/op9.k10']
d=yaml.safe_load((src/'datasheets/candidate_nominal.yaml').read_text())
keys={k:v for k,v in d['tests']['candidate'].items() if k not in ['bw_in1_mhz','bw_in2_mhz','acgain_in1','acgain_in2']}
for k in keys:
    if k not in ['source','engine']:extra += [f'let {k}=op9.{k}']
extra += ['quit']
s=re.sub(r'\.control\b.*?\.endc',lambda m:'.control'+c+'\n'.join(extra)+'\n.endc',s,flags=re.S)
(p/'tb/curvature.spice').write_text(s)
keys.update(kaxis1={},kaxis2={},axis1={},axis2={})
d['tests']={'curvature':keys}
d['parameters'].update(corner_mos=['tt','ff','ss','fs','sf'],mirror_l=[0.3,0.4,0.5],mirror_scale=[4,8],rquad=[120,240],pair_scale=[1,2])
header='# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer\n# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1\n'
(p/'datasheets/sizing.yaml').write_text(header+yaml.safe_dump(d,sort_keys=False))
(p/'settings.json').write_text(json.dumps({'num_cores':4,'sim_timeout_sec':180})+'\n')

#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Compare DC solver settings on the identical rendered SKY130 core."""
from pathlib import Path
import re,time,subprocess,json
import numpy as np
import yaml,jinja2
ROOT=Path(__file__).resolve().parents[1]
src=ROOT/'verification/porting/sky_degenerated'
d=yaml.safe_load((src/'datasheets/candidate_nominal.yaml').read_text())
params={k:v[0] if isinstance(v,list) else v for k,v in d['parameters'].items()}
params['seed']=0
s=jinja2.Template((src/'tb/candidate.spice').read_text()).render(**params)
s=re.sub(r'^Vd2 .*$', 'Vd2 vdin2 GND 0.1',s,flags=re.M)
work=Path('/tmp/lit_sky_solver_probe')
work.mkdir(exist_ok=True)
records=[];baseline=None
for name,options in [
    ('default',''),
    ('klu','.option klu'),
    ('rshunt','.option rshunt=1e12'),
    ('nodeset_rshunt','.option rshunt=1e12\n.nodeset v(outp)=0.75 v(outn)=0.75 v(vbias)=0.67 v(x2.vref_int)=0.75'),
]:
    wave=work/(name+'.dat')
    c=f'.control\nsave v(vdin1) v(outp) v(outn)\ndc vd1 -0.1 0.1 0.02\nset wr_singlescale\nwrdata {wave} v(vdin1) v(outp) v(outn)\nquit\n.endc'
    deck=re.sub(r'\.control\b.*?\.endc',lambda m:options+'\n'+c,s,flags=re.S)
    path=work/(name+'.spice');path.write_text(deck)
    start=time.monotonic()
    with (work/(name+'.log')).open('w') as log:
        try:rc=subprocess.run([str(ROOT/'scripts/with_sky130_ngspice.sh'),'ngspice','-b',str(path)],stdout=log,stderr=subprocess.STDOUT,timeout=75).returncode
        except subprocess.TimeoutExpired:rc='timeout'
    log=(work/(name+'.log')).read_text()
    record={'setting':name,'return_code':rc,'seconds':time.monotonic()-start,'dynamic_gmin_starts':log.count('Starting dynamic gmin'),'data_rows':0}
    if wave.exists():
        data=np.loadtxt(wave)
        if data.shape==(11,4) and np.isfinite(data).all():
            record['data_rows']=len(data)
            if name=='default':baseline=data
            if baseline is not None:
                record['max_voltage_delta_v']=float(abs(data[:,2:]-baseline[:,2:]).max())
    records.append(record)
    print(record,flush=True)
(ROOT/'doc/porting/evidence/sky_dc_solver_probe.json').write_text(json.dumps(records,indent=2)+'\n')

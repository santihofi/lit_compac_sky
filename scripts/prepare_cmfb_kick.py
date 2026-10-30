#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Check compensation with a resolved current kick using trapezoidal integration."""
from pathlib import Path
import re,json,yaml
ROOT=Path(__file__).resolve().parents[1]
src=ROOT/'verification/porting/sky_cmfb_options'
p=ROOT/'verification/porting/sky_cmfb_kick'
(p/'tb').mkdir(parents=True,exist_ok=True);(p/'datasheets').mkdir(exist_ok=True)
s=(src/'tb/stability_sizing.spice').read_text()
s=s.replace('x2 vdd vbias_ota ', 'Icmkick vdd vbias PULSE(0 {{20e-6*power_m}} 100n 100p 100p 20n 2u)\nx2 vdd vbias_ota ')
s=s.replace('.option method=gear','.option method=trap reltol=1e-4\n.option rshunt=1e12\n.nodeset v(outp)=0.75 v(outn)=0.75 v(vbias)=0.67 v(x2.vref_int)=0.75')
c=""".control
save v(outp) v(outn) v(vbias)
op
let cm0=(v(outp)+v(outn))/2
tran {{maxstep}} 1u 0 {{maxstep}}
let end_time=time[length(time)-1]
if end_time > 0.999e-6
let cm=(v(outp)+v(outn))/2
let err=cm-op1.cm0
let abs_err=abs(err)
meas tran peak max abs_err from=100n to=900n
meas tran residual max abs_err from=900n to=1u
let peak_mv=peak*1000
let residual_mv=residual*1000
end
quit
.endc"""
s=re.sub(r'\.control\b.*?\.endc',lambda m:c,s,flags=re.S)
(p/'tb/kick.spice').write_text(s)
d=yaml.safe_load((src/'datasheets/stability_sizing.yaml').read_text())
d['parameters'].update(cmfb_rscale=[1.5,3],cmfb_cscale=[1,16],c_load=['100f'],maxstep=['100p','50p'])
d['tests']={'kick':{'source':'netlist','engine':'ngspice','end_time':{'min':.999e-6},'peak_mv':{},'residual_mv':{'max':1},'transient_signals':['cm','err','v(vbias)']}}
header='# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer\n# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1\n'
(p/'datasheets/kick.yaml').write_text(header+yaml.safe_dump(d,sort_keys=False))
(p/'settings.json').write_text(json.dumps({'num_cores':2,'sim_timeout_sec':600})+'\n')

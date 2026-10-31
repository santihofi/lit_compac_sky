#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Compare gain, bandwidth and differential input loading from one source circuit."""
from pathlib import Path
import argparse,re,json,yaml
ROOT=Path(__file__).resolve().parents[1]
ap=argparse.ArgumentParser()
ap.add_argument('--project',required=True);ap.add_argument('--sheet',required=True);ap.add_argument('--out',required=True)
args=ap.parse_args()
src=ROOT/'verification/porting'/args.project
d=yaml.safe_load((src/'datasheets'/args.sheet).read_text())
test=next(iter(d['tests']))
s=(src/'tb'/(test+'.spice')).read_text()
control=""".control
save all
op
let idd=-i(vdd)
alter vd1 dc=0
alter vd2 dc=0.1
alter @vd1[acmag]=1
alter @vd2[acmag]=0
ac dec 60 1k 10g
let gd=v(outp)-v(outn)
let gd_db=20*log10(mag(gd)/mag(gd[0]))
meas ac bw1 when gd_db=-3
set bw1=$&bw1
let ag1=mag(gd[0])
set ag1=$&ag1
let ci1=-imag(i(e1)[180]-i(e2)[180])/(6.28318530718*frequency[180])*1e15
set ci1=$&ci1
let ci1hf=-imag(i(e1)[300]-i(e2)[300])/(6.28318530718*frequency[300])*1e15
set ci1hf=$&ci1hf
alter vd1 dc=0.1
alter vd2 dc=0
alter @vd1[acmag]=0
alter @vd2[acmag]=1
ac dec 60 1k 10g
let gd=v(outp)-v(outn)
let gd_db=20*log10(mag(gd)/mag(gd[0]))
meas ac bw2 when gd_db=-3
let bw_in1_mhz=$bw1/1e6
let bw_in2_mhz=bw2/1e6
let acgain_in1=$ag1
let acgain_in2=mag(gd[0])
let cin1_per_pin_ff=$ci1
let cin1_100mhz_ff=$ci1hf
let cin2_per_pin_ff=-imag(i(e4)[180]-i(e5)[180])/(6.28318530718*frequency[180])*1e15
let cin2_100mhz_ff=-imag(i(e4)[300]-i(e5)[300])/(6.28318530718*frequency[300])*1e15
let idd=op1.idd
quit
.endc"""
s=re.sub(r'\.control\b.*?\.endc',lambda m:control,s,flags=re.S)
p=ROOT/'verification/porting'/args.out
(p/'tb').mkdir(parents=True,exist_ok=True);(p/'datasheets').mkdir(exist_ok=True)
(p/'tb/ac.spice').write_text(s)
d['parameters'].update(temp=[27],vdd=[1.5],corner_mos=['tt'])
d['tests']={'ac':{'source':'netlist','engine':'ngspice',**{k:{} for k in ['bw_in1_mhz','bw_in2_mhz','acgain_in1','acgain_in2','cin1_per_pin_ff','cin2_per_pin_ff','cin1_100mhz_ff','cin2_100mhz_ff','idd']},'ac_signals':['ac1.gd','ac2.gd']}}
header='# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer\n# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1\n'
(p/'datasheets/ac.yaml').write_text(header+yaml.safe_dump(d,sort_keys=False))
(p/'settings.json').write_text(json.dumps({'num_cores':2,'sim_timeout_sec':180})+'\n')

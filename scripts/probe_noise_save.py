#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Distinguish a selective save from save all before ngspice noise analysis."""
from pathlib import Path
import argparse,json,re,subprocess,tempfile
ROOT=Path(__file__).resolve().parents[1]
ap=argparse.ArgumentParser()
ap.add_argument('--output',type=Path,default=ROOT/'verification/controls/noise_save_controls.json')
args=ap.parse_args()
records=[]
with tempfile.TemporaryDirectory(prefix='noise-save-control-') as folder:
    for name,save in [('default',''),('all','save all'),('selected','save v(out)')]:
        deck=f"""* Noise capture control
V1 in 0 dc 0 ac 1
R1 in out 1k
R2 out 0 1k
.control
{save}
noise v(out) V1 dec 10 1k 1meg
setplot noise1
let n=onoise_spectrum[0]
print n
quit
.endc
.end
"""
        path=Path(folder)/(name+'.spice');path.write_text(deck)
        result=subprocess.run(['ngspice','-b',str(path)],capture_output=True,text=True,timeout=10)
        log=result.stdout+result.stderr
        match=re.search(r'^n = (\S+)',log,re.M)
        record={'mode':name,'return_code':result.returncode,'noise_v_per_rt_hz':float(match[1]) if match else None,'log':log}
        records.append(record)
assert records[0]['noise_v_per_rt_hz']==records[1]['noise_v_per_rt_hz'] and records[0]['noise_v_per_rt_hz']>0
assert records[2]['noise_v_per_rt_hz'] is None and 'no data saved for Noise analysis' in records[2]['log']
args.output.parent.mkdir(parents=True,exist_ok=True)
args.output.write_text(json.dumps(records,indent=2)+'\n')
print(json.dumps([{k:v for k,v in r.items() if k!='log'} for r in records],indent=2))

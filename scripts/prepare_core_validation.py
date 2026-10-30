#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Build matching loop and noise benches from the selected exploratory circuit."""
from pathlib import Path
import argparse,json,re,yaml
ROOT=Path(__file__).resolve().parents[1]
HEADER='# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer\n# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1\n'
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--project',required=True)
    ap.add_argument('--sheet',required=True)
    ap.add_argument('--out',required=True)
    args=ap.parse_args()
    src=ROOT/'verification/porting'/args.project
    d=yaml.safe_load((src/'datasheets'/args.sheet).read_text())
    test=next(iter(d['tests']))
    s=(src/'tb'/(test+'.spice')).read_text()
    p=ROOT/'verification/porting'/args.out
    (p/'tb').mkdir(parents=True,exist_ok=True);(p/'datasheets').mkdir(exist_ok=True)
    original=ROOT.parent/'lit_compac/macros/gilbert_cell/testbenches/xschem/tb_gilbert_cell_stb.sch'
    control=re.search(r'\.control\b.*?\.endc',original.read_text(),re.S).group()
    stb=s.replace('x2 vdd vbias ','x2 vdd vbias_ota ')
    stb=stb.replace('x2 vdd vbias_ota ', 'Vstb vbias vbias_ota dc 0 ac 0\nIstb GND vbias dc 0 ac 0\nx2 vdd vbias_ota ')
    stb=re.sub(r'\.control\b.*?\.endc',lambda m:control,stb,flags=re.S)
    (p/'tb/stability.spice').write_text(stb)
    keys={'pm':{'min':45,'max':180},'gm_db':{'min':10},'ncross':{'min':1},'fu':{},'f180':{},'t0_db':{},'vbias_dc':{},'voutcm_dc':{}}
    keys.update(ac_signals=['ac2.tloop'])
    sheet={'parameters':d['parameters'],'tests':{'stability':{'source':'netlist','engine':'ngspice',**keys}}}
    # Start with nominal conditions, retaining the selected geometry parameters.
    sheet['parameters'].update(corner_mos=['tt'],vdd=[1.5],temp=[27],c_load=['100f'],gcode=[13])
    (p/'datasheets/stability.yaml').write_text(HEADER+yaml.safe_dump(sheet,sort_keys=False))
    c=['.control','save all','alter vd1 dc=0','alter vd2 dc=0.1','alter @vd1[acmag]=1','noise v(outp,outn) vd1 dec 40 1k 100meg',
       'setplot noise1','let on1=onoise_spectrum[120]*1e9','let in1=inoise_spectrum[120]*1e9','let f1=frequency[120]',
       'setplot noise2','let no1=onoise_total*1e6','let ni1=inoise_total*1e6',
       'alter vd1 dc=0.1','alter vd2 dc=0','alter @vd2[acmag]=1','noise v(outp,outn) vd2 dec 40 1k 100meg',
       'setplot noise3','let on2=onoise_spectrum[120]*1e9','let in2=inoise_spectrum[120]*1e9',
       'setplot noise4','let no2=onoise_total*1e6','let ni2=inoise_total*1e6',
       'let onoise1_nv=noise1.on1','let inoise1_nv=noise1.in1','let frequency_hz=noise1.f1',
       'let onoise1_uv=noise2.no1','let inoise1_uv=noise2.ni1',
       'let onoise2_nv=noise3.on2','let inoise2_nv=noise3.in2','let onoise2_uv=no2','let inoise2_uv=ni2','quit','.endc']
    noise=re.sub(r'\.control\b.*?\.endc',lambda m:'\n'.join(c),s,flags=re.S)
    (p/'tb/noise.spice').write_text(noise)
    keys={k:{'min':0} for k in ['onoise1_nv','inoise1_nv','onoise1_uv','inoise1_uv','onoise2_nv','inoise2_nv','onoise2_uv','inoise2_uv']}
    keys['frequency_hz']={'min':999999,'max':1000001}
    sheet['tests']={'noise':{'source':'netlist','engine':'ngspice',**keys}}
    (p/'datasheets/noise.yaml').write_text(HEADER+yaml.safe_dump(sheet,sort_keys=False))
    c=['.control','save v(vdin1) v(vdin2) v(outp) v(outn)','dc vd1 -0.1 0.1 0.005 vd2 -0.1 0.1 0.005',
       'let outdiff=v(outp)-v(outn)','let vocm=(v(outp)+v(outn))/2',
       'let points=length(outdiff)','quit','.endc']
    transfer=re.sub(r'\.control\b.*?\.endc',lambda m:'\n'.join(c),s,flags=re.S)
    (p/'tb/transfer.spice').write_text(transfer)
    sheet['tests']={'transfer':{'source':'netlist','engine':'ngspice',
                    'points':{'min':1681,'max':1681},
                    'dc_signals':['v(vdin1)','v(vdin2)','outdiff','vocm']}}
    (p/'datasheets/transfer.yaml').write_text(HEADER+yaml.safe_dump(sheet,sort_keys=False))
    (p/'settings.json').write_text(json.dumps({'num_cores':2,'sim_timeout_sec':600},indent=2)+'\n')
if __name__=='__main__':main()

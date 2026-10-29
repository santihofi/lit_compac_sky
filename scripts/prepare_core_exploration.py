#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Create reproducible core sizing benches from the frozen Xschem reference templates."""
from pathlib import Path
import json,re,yaml
ROOT=Path(__file__).resolve().parents[1]
KEYS=['k100','k10','compr','vocm','idd','vos','tail_margin','pair_margin','mirror_margin','quad_margin','qs','sp','bw_in1_mhz','bw_in2_mhz','acgain_in1','acgain_in2']
GROUPS={**{n:('mirror_scale','mirror_l') for n in ['M3','M4','M5','M6','MDM']},
        **{n:('quad_scale','quad_l') for n in ['M7','M8','M9','M10','MDQ1','MDQ2']},
        **{n:('pair_scale','pair_l') for n in ['M1','M2','MDP']}}
def resize_core(text):
    start=text.index('.subckt gilbert_cell ');end=text.index('.ends',start)
    core=text[start:end]
    def resize(m):
        line=m.group();name=line.split()[0][1:]
        if name not in GROUPS:return line
        scale,length=GROUPS[name]
        w=float(re.search(r'\bW=(\S+)',line).group(1));nf=int(re.search(r'\bnf=(\S+)',line).group(1));wf=w/nf
        updates={'L':'{{'+length+'}}','W':f'{{{{{w}*{scale}}}}}','nf':f'{{{{({nf}*{scale})|int}}}}',
                 'ad':f'{{{{((({nf}*{scale}+1)/2)|int)*{wf}*0.29}}}}','as':f'{{{{((({nf}*{scale}+2)/2)|int)*{wf}*0.29}}}}',
                 'pd':f'{{{{2*((({nf}*{scale}+1)/2)|int)*({wf}+0.29)}}}}','ps':f'{{{{2*((({nf}*{scale}+2)/2)|int)*({wf}+0.29)}}}}'}
        for key,val in updates.items():line=re.sub(r'\b'+key+r'=\S+',key+'='+val,line)
        return line
    text=text[:start]+re.sub(r'^XM\S+ [^\n]+(?:\n\+[^\n]+)*',resize,core,flags=re.M)+text[end:]
    for cell in ['gilbert_cell','gain_trim']:
        start=text.index('.subckt '+cell+' ');end=text.index('.ends',start)
        core=text[start:end]
        def scale_res(m):
            line=m.group();length=float(re.search(r'\bL=(\S+)',line).group(1))
            val=f'{{{{((68.05+56.46*{length})*rscale-68.05)/56.46}}}}'
            return re.sub(r'\bL=\S+','L='+val,line)
        core=re.sub(r'^XR\S+ .*sky130_fd_pr__res_high_po_5p73[^\n]+',scale_res,core,flags=re.M)
        text=text[:start]+core+text[end:]
    return text
def control(pdk):
    c=['.control','save all','op','let vo=v(outp)-v(outn)','let cm=(v(outp)+v(outn))/2','let idd=-i(vdd)']
    for name,dev,volt in [('tail','13','v(vdd)-v(x1.vcm1)'),('pair','1','v(x1.vcm1)-v(x1.net1)'),('mirror','5','v(x1.qs1)'),('quad','7','v(outp)-v(x1.qs1)')]:
        if pdk=='sky':
            model='pfet' if name in ['tail','pair'] else 'nfet'
            expr=f'({volt})-abs(@m.x1.xm{dev}.msky130_fd_pr__{model}_01v8_lvt[vdsat])'
        else:
            model='pmos' if name in ['tail','pair'] else 'nmos'
            expr=f'@n.x1.xm{dev}.nsg13_lv_{model}[vsat]'
        c.append(f'let {name}_margin={expr}')
    c+=['let qs=v(x1.qs1)','let sp=v(x1.vcm1)']
    for a,b in [(0.1,0.1),(-0.1,0.1),(-0.1,-0.1),(0.1,-0.1),(0.01,0.01),(-0.01,0.01),(-0.01,-0.01),(0.01,-0.01)]:
        c += [f'alter vd1 dc={a}',f'alter vd2 dc={b}','op','let vo=v(outp)-v(outn)']
    c+=['let k100=(op2.vo-op3.vo+op4.vo-op5.vo)/0.04','let k10=(op6.vo-op7.vo+op8.vo-op9.vo)/0.0004','let compr=k100/k10',
        'let vocm=op1.cm','let idd=op1.idd','let vos=op1.vo']
    for key in KEYS[6:12]:c.append(f'let {key}=op1.{key}')
    c+=['alter vd1 dc=0','alter vd2 dc=0.1','alter @vd1[acmag]=1','alter @vd2[acmag]=0',
        'ac dec 60 1k 10g','let gd=mag(v(outp)-v(outn))','let gain0=gd[0]',
        'let gd_db=20*log10(gd/gain0)','meas ac bw1 when gd_db=-3',
        'set bw1=$&bw1','set ag1=$&gain0',
        'alter vd1 dc=0.1','alter vd2 dc=0','alter @vd1[acmag]=0','alter @vd2[acmag]=1',
        'ac dec 60 1k 10g','let gd=mag(v(outp)-v(outn))','let gain0=gd[0]',
        'let gd_db=20*log10(gd/gain0)','meas ac bw2 when gd_db=-3',
        'let bw_in1_mhz=$bw1/1e6','let bw_in2_mhz=bw2/1e6','let acgain_in1=$ag1','let acgain_in2=gain0']
    for key in KEYS[:12]:c.append(f'let {key}=op9.{key}')
    c+=['quit','.endc']
    return '\n'.join(c)
def prepare(pdk):
    e=ROOT/'doc/porting/evidence'
    source=e/('sky_initial_multiplier.template.spice' if pdk=='sky' else 'ihp_nominal_multiplier.template.spice')
    text=source.read_text()
    if pdk=='sky':text=resize_core(text)
    text=re.sub(r'\.control\b.*?\.endc',control(pdk),text,flags=re.S)
    p=ROOT/'verification/porting'/(pdk+'_core_tradeoffs')
    (p/'tb').mkdir(parents=True,exist_ok=True);(p/'datasheets').mkdir(exist_ok=True)
    (p/'tb/core.spice').write_text(text)
    d=yaml.safe_load((ROOT/'verification/porting/ihp_gilbert/datasheets/nominal_mult.yaml').read_text())
    if pdk=='sky':
        d['parameters'].update(mirror_scale=[2,4,8],mirror_l=[0.15,0.25],pair_scale=[0.5,1],pair_l=[0.35],quad_scale=[1],quad_l=[0.15,0.25],rscale=[1])
    d['tests']={'core':{'source':'netlist','engine':'ngspice',**{k:{} for k in KEYS}}}
    header='# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer\n# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1\n'
    (p/'datasheets/tradeoffs.yaml').write_text(header+yaml.safe_dump(d,sort_keys=False))
    if pdk=='sky':
        for key in ['mirror_scale','mirror_l','pair_scale','quad_l']:d['parameters'][key]=[d['parameters'][key][0]]
    (p/'datasheets/probe.yaml').write_text(header+yaml.safe_dump(d,sort_keys=False))
    (p/'settings.json').write_text(json.dumps({'num_cores':2,'sim_timeout_sec':180},indent=2)+'\n')
if __name__=='__main__':
    for pdk in ['ihp','sky']:prepare(pdk)

#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Santiago Hofwimmer
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
"""Generate an initial SKY130 core, not a qualified port, from the frozen IHP topology."""
import argparse,json,math,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
HEADER=re.compile(r"^C \{([^}]+)\} (-?[\d.]+) (-?[\d.]+) (\d) (\d) \{",re.M)
def components(text):
    for m in HEADER.finditer(text):
        depth,i=1,m.end()
        while depth and i<len(text):
            if text[i]=="\\":
                i+=2
                continue
            if text[i]=="{": depth+=1
            elif text[i]=="}": depth-=1
            i+=1
        if depth: raise ValueError("Unbalanced component")
        yield m,i,text[m.end():i-1]
def attr(a,key,default=None):
    m=re.search(r"(?:^|\s)"+re.escape(key)+r"=([^\s]+)",a)
    return m.group(1) if m else default
def um(s):
    return float(s[:-1]) if s.endswith("u") else float(s)*1e6
def point(x,y,rot,flip,dx,dy):
    if flip: dx=-dx
    for _ in range(rot): dx,dy=-dy,dx
    return x+dx,y+dy
def resistor_length(target,model):
    # Initial estimate from installed TT equations, 27 C and zero differential voltage.
    if model.endswith("5p73"):
        return round(((target-68.05)/56.46)/0.005)*0.005
    else:
        con,slope,vc,tc=254.77,230.05,(-0.0762,0.198,0.0881),-0.00468
    dt=-3
    b=slope  # The resistor reference temperature defaults to ngspice TNOM, 27 C.
    c=con*0.705*(vc[0]*(-1.4)*(1+tc*dt)+vc[1]*1.4**2+vc[2]*(-1.4)**3)
    disc=(target-con)**2-4*b*c
    if disc<0: raise ValueError(f"No initial resistor geometry for {target}")
    length=(target-con+math.sqrt(disc))/(2*b)
    if length<0.5: raise ValueError(f"Resistor too short: {length}")
    return round(length/0.005)*0.005
def convert(path,overrides,audit):
    text=path.read_text(); additions=[]
    for m,end,a in reversed(list(components(text))):
        sym,xs,ys,rs,fs=m.groups()
        x,y,rot,flip=float(xs),float(ys),int(rs),int(fs)
        name=attr(a,"name","");key=f"{path.stem}/{name}"
        override=overrides.get(key,{})
        old={"symbol":sym,"attributes":a}
        if sym.endswith(("sg13_lv_nmos.sym","sg13_lv_pmos.sym")):
            kind="nfet" if sym.endswith("nmos.sym") else "pfet"
            model=override.get("model",kind+"_01v8_lvt")
            l0,w0=um(attr(a,"l")),um(attr(a,"w"))
            l=override.get("L",max(l0,0.35 if kind=="pfet" else 0.15))
            w=override.get("W",w0*l/l0)
            nf=int(override.get("nf",attr(a,"ng","1")))
            mult=int(override.get("mult",attr(a,"m","1")))
            sym="sky130_fd_pr/"+model+".sym"
            a=f"name={name}\nL={l:.6g}\nW={w:.6g}\nnf={nf}\nmult={mult}\nmodel={model}\nspiceprefix=X\n"
        elif sym.endswith("/rppd.sym"):
            w,l=um(attr(a,"w")),um(attr(a,"l"))
            if float(attr(a,"b","0")): raise ValueError("Unmapped resistor bends")
            target=70/w+260*l/(w+0.006)
            model=override.get("model","res_high_po_5p73" if target<1800 else "res_high_po_1p41")
            length=override.get("L",resistor_length(target,model))
            mult=override.get("mult",int(attr(a,"m","1")))
            sym="sky130_fd_pr/"+model+".sym"
            a=f"name={name}\nL={length:.6g}\nmult={mult}\nmodel={model}\nspiceprefix=X\n"
            bx,by=point(x,y,rot,flip,-20,0)
            additions.append(f"C {{devices/lab_pin.sym}} {bx:g} {by:g} 0 0 {{name=body_{name} lab=ptap}}\n")
            audit[key+"_resistance"]={"ihp_nominal_ohm_per_copy":target,"parallel_copies":mult,"initial_sky_model":model,"initial_sky_length_um":length}
        elif sym.endswith(("/ptap1.sym","/ntap1.sym")):
            sym="devices/res.sym";a=f"name=Rtap_{name}\nvalue=1m\nlvs_ignore=short\n"
        elif sym.endswith("/annotate_fet_params.sym"):
            sym="sky130_fd_pr/annotate_fet_params.sym"
        elif sym.startswith("sg13g2_pr/"):
            raise ValueError(f"Unmapped primitive {sym} in {path}")
        else: continue
        audit[key]={"source":old,"target_symbol":sym,"target_attributes":a}
        text=text[:m.start()]+f"C {{{sym}}} {xs} {ys} {rs} {fs} {{{a}}}"+text[end:]
    return text.replace("lit_compac/macros/","lit_compac_sky/macros/")+"".join(additions)
def main():
    ap=argparse.ArgumentParser();ap.add_argument("--source",type=Path,default=ROOT.parent/"lit_compac")
    args=ap.parse_args();cfg=ROOT/"doc/porting/core_sizing.json"
    overrides=json.loads(cfg.read_text()) if cfg.exists() else {};audit={}
    for block in ["gilbert_cell","ota"]:
        dest=ROOT/"macros"/block/"schematic/xschem";dest.mkdir(parents=True,exist_ok=True)
        for path in (args.source/"macros"/block/"schematic/xschem").glob("*"):
            if path.suffix==".sch": (dest/path.name).write_text(convert(path,overrides,audit))
            elif path.suffix==".sym" and "_pex" not in path.stem:
                (dest/path.name).write_text(path.read_text().replace("lit_compac/macros/","lit_compac_sky/macros/"))
    (ROOT/"doc/porting/evidence/core_mapping.json").write_text(json.dumps(audit,indent=2)+"\n")
    print(f"Generated initial core and CMFB schematics, {len(audit)} mapping entries.")
if __name__=="__main__": main()

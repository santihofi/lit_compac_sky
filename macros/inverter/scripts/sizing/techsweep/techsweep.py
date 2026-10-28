#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Simon Dorrer and Harald Pretl
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
# Description: gm/ID techsweep of one sky130A MOSFET with ngspice, written as the pygmid lookup table.
#
# The sweep follows the Murmann techsweep as used for the IHP tables in the analog-circuit-design course
# (one device, the drain current read through a CCVS), split into two passes because every ngspice run of
# the sky130 library costs about 0.35 s regardless of its size:
#   1. the operating-point parameters come from one dc sweep of VDS per (L, VSB, VGS) point,
#   2. the noise (channel thermal and 1/f) comes from one-point noise analyses on a four times coarser
#      VGS and VDS grid and is interpolated onto the fine grid in the log domain.
# Every row carries its bias, so the converter sorts the rows into the grid by value, and a noise point the
# simulator dropped is filled from its neighbours. The table stores the arrays in the order L, VGS, VDS, VSB
# like the IHP tables.
#
# Usage inside the IIC-OSIC-TOOLS container (PDK_ROOT and PDK set, PDK=sky130A):
#   python3 techsweep.py nfet_01v8            # run both passes, convert to ../data/sky130_fd_pr__nfet_01v8.mat
#   python3 techsweep.py pfet_01v8 --convert  # convert the existing techsweep_<device>_{op,noise}.txt only
#   python3 techsweep.py --list

import argparse
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.normpath(os.path.join(HERE, "..", "data"))

# Finger width of the swept device in um. NFING stays 1, the tables scale with W.
W_FINGER = 5.0
# The noise grid is this many times coarser than the operating-point grid
NOISE_COARSE = 4

# The devices the sizing notebooks use: the 1.8 V core devices and the 5 V thick-oxide pair.
# l in um, voltages in V. The 5 V devices sweep to their rated 5 V with a coarser step.
DEVICES = {
    "nfet_01v8": dict(polarity=1, l=[0.15, 0.2, 0.3, 0.5, 1.0, 2.0, 5.0, 10.0], vmax=1.8, vstep=0.05, vsb=[0.0, 0.3, 0.6, 0.9]),
    "pfet_01v8": dict(polarity=-1, l=[0.15, 0.2, 0.3, 0.5, 1.0, 2.0, 5.0, 10.0], vmax=1.8, vstep=0.05, vsb=[0.0, 0.3, 0.6, 0.9]),
    "pfet_01v8_lvt": dict(polarity=-1, l=[0.35, 0.5, 1.0, 2.0, 5.0, 10.0], vmax=1.8, vstep=0.05, vsb=[0.0, 0.3, 0.6, 0.9]),
    "nfet_g5v0d10v5": dict(polarity=1, l=[0.5, 0.6, 0.8, 1.0, 2.0, 5.0, 10.0], vmax=5.0, vstep=0.1, vsb=[0.0, 1.0, 2.0, 3.0]),
    "pfet_g5v0d10v5": dict(polarity=-1, l=[0.5, 0.6, 0.8, 1.0, 2.0, 5.0, 10.0], vmax=5.0, vstep=0.1, vsb=[0.0, 1.0, 2.0, 3.0]),
}

# BSIM4 operating-point parameters saved per bias point (ngspice `show` names).
OP_PARAMS = ["id", "vth", "vdsat", "gm", "gmbs", "gds", "cgg", "cgs", "cgd", "cgb", "cdd", "css",
             "capbd", "capbs", "cgso", "cgdo", "cgbo", "vgs", "vds", "vbs"]


def model_name(device):
    return "sky130_fd_pr__" + device


def device_ref(device):
    """The ngspice name of the transistor inside the X1 wrapper."""
    return f"m.x1.m{model_name(device)}"


def fmt(v):
    """A plain decimal without a negative zero, which ngspice's compose does not take."""
    return f"{v + 0.0:.4f}".rstrip("0").rstrip(".") or "0"


def header(device, cfg, pdk_root, pdk, save_op=True):
    """The circuit. Every sweep vector stays positive (ngspice's compose reads `0 -0.3` as an expression),
    so the source polarities follow the device: gate and drain go negative for a PMOS, the bulk goes
    negative for an NMOS (positive VSB) and positive for a PMOS. The operating-point parameters are saved
    only in the dc pass, because a .save list would drop the noise vectors from the noise plot."""
    model = model_name(device)
    dev = device_ref(device)
    saves = "\n".join(f".save @{dev}[{par}]" for par in OP_PARAMS) if save_op else "* no .save, the noise plot keeps every vector"
    if cfg["polarity"] > 0:
        sources = "Vg g 0 0 ac 1\nVd d 0 0\nVb 0 b 0"
    else:
        sources = "Vg 0 g 0 ac 1\nVd 0 d 0\nVb b 0 0"
    return f"""* gm/ID techsweep of {model} (W = {W_FINGER} um, one finger)
.lib {pdk_root}/{pdk}/libs.tech/ngspice/sky130.lib.spice tt
.option sparse
.temp 27
.param wx={W_FINGER} lx={cfg['l'][0]}
X1 d g 0 b {model} W={{wx}} L={{lx}}
{sources}
* The CCVS turns the drain current into v(n), so the noise at n is the drain current noise in A/sqrt(Hz).
H1 n 0 Vd 1
{saves}
"""


def deck_op(device, cfg, pdk_root, pdk, out_txt):
    """Pass 1: one dc sweep of VDS per (L, VSB, VGS). The operating-point parameters land in dc1, l_tag
    marks the channel length of every row, the bias comes with the saved vgs, vds and vbs."""
    dev = device_ref(device)
    l_vec = " ".join(fmt(l) for l in cfg["l"])
    vb_vec = " ".join(fmt(v) for v in cfg["vsb"])
    # explicit values, a compose with start/stop/step loses the stop point to rounding
    vg_vec = " ".join(fmt(v) for v in grid_fine(cfg)[1])
    return header(device, cfg, pdk_root, pdk) + f""".control
set wr_singlescale
set wr_vecnames
option numdgt=6
compose l_vec values {l_vec}
compose vb_vec values {vb_vec}
compose vg_vec values {vg_vec}
foreach var1 $&l_vec
  alterparam lx=$var1
  reset
  foreach var2 $&vb_vec
    alter Vb $var2
    foreach var3 $&vg_vec
      alter Vg $var3
      dc Vd 0 {fmt(cfg['vmax'])} {fmt(cfg['vstep'])}
      let l_tag = @{dev}[vds]*0 + $var1
      wrdata {out_txt} dc1.all
      destroy all
      set appendwrite
      unset wr_vecnames
    end
  end
end
quit
.endc
.end
"""


def deck_noise(device, cfg, pdk_root, pdk, out_txt):
    """Pass 2: one-point noise analyses on the coarse (L, VSB, VGS, VDS) grid. The four tag vectors carry
    the bias of every row."""
    l_vec = " ".join(fmt(l) for l in cfg["l"])
    vb_vec = " ".join(fmt(v) for v in cfg["vsb"])
    v_vec = " ".join(fmt(v) for v in grid_coarse(cfg))
    return header(device, cfg, pdk_root, pdk, save_op=False) + f""".noise v(n) Vg lin 1 1 1 1
.control
set wr_singlescale
set wr_vecnames
option numdgt=6
compose l_vec values {l_vec}
compose vb_vec values {vb_vec}
compose vg_vec values {v_vec}
compose vd_vec values {v_vec}
foreach var1 $&l_vec
  alterparam lx=$var1
  reset
  foreach var2 $&vb_vec
    alter Vb $var2
    foreach var3 $&vg_vec
      alter Vg $var3
      foreach var4 $&vd_vec
        alter Vd $var4
        run
        setplot noise1
        let l_tag = $var1
        let vb_tag = $var2
        let vg_tag = $var3
        let vd_tag = $var4
        wrdata {out_txt} noise1.all
        destroy all
        set appendwrite
        unset wr_vecnames
      end
    end
  end
end
quit
.endc
.end
"""


def grid_fine(cfg):
    import numpy as np
    v = np.round(np.arange(0.0, cfg["vmax"] + cfg["vstep"] / 2, cfg["vstep"]), 3)
    return np.array(cfg["l"], dtype=float), v, v.copy(), np.array(cfg["vsb"], dtype=float)


def grid_coarse(cfg):
    import numpy as np
    step = cfg["vstep"] * NOISE_COARSE
    return np.round(np.arange(0.0, cfg["vmax"] + step / 2, step), 3)


def read_txt(path, columns):
    """The wanted columns as numbers, rows that lack one of them are dropped."""
    import pandas as pd
    df = pd.read_csv(path, sep=r"\s+")
    df = df.loc[:, ~df.columns.duplicated()][columns]
    return df.apply(pd.to_numeric, errors="coerce").dropna()


def place(df, keys, grids, columns):
    """Sort the rows into the (L, VGS, VDS, VSB) grid by their bias values. Returns one array per column
    with NaN where the simulator delivered no usable row."""
    import numpy as np
    idx = tuple(np.abs(np.asarray(k, dtype=float)[:, None] - g[None, :]).argmin(axis=1) for k, g in zip(keys, grids))
    out = {}
    for c in columns:
        a = np.full(tuple(len(g) for g in grids), np.nan)
        a[idx] = df[c].values
        out[c] = a
    return out


def fill_nan(a):
    """Replace NaN cells by the nearest valid cell along VDS, then VGS, then VSB, then L, without wrapping."""
    import numpy as np
    a = a.copy()
    for axis in (2, 1, 3, 0):
        for _ in range(a.shape[axis]):
            nan = np.isnan(a)
            if not nan.any():
                return a
            for shift in (1, -1):
                src = np.full_like(a, np.nan)
                lo, hi = [slice(None)] * a.ndim, [slice(None)] * a.ndim
                lo[axis], hi[axis] = slice(0, -1), slice(1, None)
                if shift > 0:
                    src[tuple(hi)] = a[tuple(lo)]
                else:
                    src[tuple(lo)] = a[tuple(hi)]
                take = nan & ~np.isnan(src)
                a[take] = src[take]
    return a


def convert(device, cfg, op_txt, noise_txt, mat_path):
    import numpy as np
    from scipy.interpolate import RegularGridInterpolator
    from scipy.io import savemat

    model = model_name(device)
    dev = device_ref(device)
    l, vgs, vds, vsb = grid_fine(cfg)
    vc = grid_coarse(cfg)
    nl, ng, nd, nb = len(l), len(vgs), len(vds), len(vsb)

    op_cols = [f"@{dev}[{par}]" for par in OP_PARAMS]
    df = read_txt(op_txt, ["l_tag"] + op_cols)
    op = place(df, (df["l_tag"], df[f"@{dev}[vgs]"].abs(), df[f"@{dev}[vds]"].abs(), df[f"@{dev}[vbs]"].abs()),
               (l, vgs, vds, vsb), op_cols)
    missing = int(np.isnan(op[op_cols[0]]).sum())
    if missing:
        sys.exit(f"[ERROR] {op_txt}: {missing} of {nl * ng * nd * nb} bias points missing.")

    noise_cols = [f"onoise.{dev}.id", f"onoise.{dev}.1overf"]
    df = read_txt(noise_txt, ["l_tag", "vg_tag", "vd_tag", "vb_tag"] + noise_cols)
    noise = place(df, (df["l_tag"], df["vg_tag"], df["vd_tag"], df["vb_tag"]), (l, vc, vc, vsb), noise_cols)
    missing = int(np.isnan(noise[noise_cols[0]]).sum())
    if missing:
        print(f"[WARNING] {noise_txt}: {missing} of {nl * len(vc) ** 2 * nb} noise points missing, filled from their neighbours.")
        noise = {c: fill_nan(a) for c, a in noise.items()}

    def col(name):
        return op[f"@{dev}[{name}]"]

    def noise_fine(kind):
        # the coarse (VGS, VDS) noise grid is interpolated onto the fine grid in the log domain, per L and VSB
        a = np.log10(np.maximum(noise[f"onoise.{dev}.{kind}"] ** 2, 1e-40))
        out = np.empty((nl, ng, nd, nb))
        gg, dd = np.meshgrid(vgs, vds, indexing="ij")
        pts = np.stack([gg.ravel(), dd.ravel()], axis=1)
        for i in range(nl):
            for k in range(nb):
                f = RegularGridInterpolator((vc, vc), a[i, :, :, k], bounds_error=False, fill_value=None)
                out[i, :, :, k] = f(pts).reshape(ng, nd)
        return 10.0 ** out

    # Currents and voltages are stored as magnitudes, so the PMOS table reads like the NMOS one. The
    # intrinsic gate capacitances come out negative from the model and are negated, the overlap and
    # junction terms are added on top, as in the IHP converter.
    table = {
        "INFO": f"SkyWater sky130A, 130nm CMOS, BSIM4 ({model})",
        "CORNER": "tt",
        "TEMP": 300.0,
        "VGS": vgs,
        "VDS": vds,
        "VSB": vsb,
        "L": l,
        "W": W_FINGER,
        "NFING": 1,
        "ID": np.abs(col("id")),
        "VTH": np.abs(col("vth")),
        "VDSS": np.abs(col("vdsat")),
        "GM": col("gm"),
        "GMB": col("gmbs"),
        "GDS": col("gds"),
        "CGG": col("cgg") + col("cgso") + col("cgdo") + col("cgbo"),
        "CGB": -col("cgb") + col("cgbo"),
        "CGD": -col("cgd") + col("cgdo"),
        "CGS": -col("cgs") + col("cgso"),
        "CDD": col("cdd") + col("capbd") + col("cgdo"),
        "CSS": col("css") + col("capbs") + col("cgso"),
        "STH": noise_fine("id"),
        "SFL": noise_fine("1overf"),
    }
    os.makedirs(os.path.dirname(mat_path), exist_ok=True)
    savemat(mat_path, {model: table})
    print(f"[INFO] wrote {mat_path} with the grid L x VGS x VDS x VSB = {[nl, ng, nd, nb]}")


def run_deck(name, text):
    deck = os.path.join(HERE, f"{name}.spice")
    with open(deck, "w") as f:
        f.write(text)
    log = os.path.join(HERE, f"{name}.log")
    print(f"[INFO] ngspice -b {os.path.basename(deck)} ...", flush=True)
    with open(log, "w") as f:
        subprocess.run(["ngspice", "-b", deck], check=True, cwd=HERE, stdout=f, stderr=subprocess.STDOUT)
    with open(log) as f:
        errors = [line for line in f if "rror" in line]
    if errors:
        sys.exit(f"[ERROR] ngspice reported errors, see {log}:\n" + "".join(errors[:10]))


def main():
    parser = argparse.ArgumentParser(description="gm/ID techsweep of a sky130A MOSFET")
    parser.add_argument("device", nargs="?", choices=sorted(DEVICES), help="device to sweep")
    parser.add_argument("--convert", action="store_true", help="only convert the existing sweep outputs")
    parser.add_argument("--list", action="store_true", help="list the devices and their grids")
    args = parser.parse_args()
    if args.list or not args.device:
        for name, cfg in DEVICES.items():
            print(f"{name}: L={cfg['l']} um, V=0..{cfg['vmax']} step {cfg['vstep']}, VSB={cfg['vsb']}")
        return 0
    cfg = DEVICES[args.device]
    op_txt = os.path.join(HERE, f"techsweep_{args.device}_op.txt")
    noise_txt = os.path.join(HERE, f"techsweep_{args.device}_noise.txt")
    mat = os.path.join(DATA_DIR, f"{model_name(args.device)}.mat")
    if not args.convert:
        pdk_root = os.environ.get("PDK_ROOT")
        pdk = os.environ.get("PDK", "sky130A")
        if not pdk_root:
            sys.exit("[ERROR] PDK_ROOT is not set, run this inside the IIC-OSIC-TOOLS container.")
        for path in (op_txt, noise_txt):
            if os.path.exists(path):
                os.remove(path)
        run_deck(f"techsweep_{args.device}_op", deck_op(args.device, cfg, pdk_root, pdk, op_txt))
        run_deck(f"techsweep_{args.device}_noise", deck_noise(args.device, cfg, pdk_root, pdk, noise_txt))
    convert(args.device, cfg, op_txt, noise_txt, mat)
    return 0


if __name__ == "__main__":
    sys.exit(main())

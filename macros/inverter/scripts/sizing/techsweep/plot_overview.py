#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Simon Dorrer and Harald Pretl
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
# Description: One overview page per device from the pygmid tables of techsweep.py, the four plots a gm/ID
# design starts from. Writes doc/sizing/techsweep_<model>_plots_overview.pdf.
#
# Usage inside the IIC-OSIC-TOOLS container, from this folder:
#   python3 plot_overview.py               # every device that has a table
#   python3 plot_overview.py nfet_01v8     # one device

import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from pygmid import Lookup as lk

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, "..", "data"))
OUT = os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "..", "doc", "sizing"))

# The VDS the curves are taken at, half the rated supply of the device family.
VDS = {"01v8": 0.9, "g5v0d10v5": 2.5}


def vds_of(model):
    for key, value in VDS.items():
        if key in model:
            return value
    return 0.9


def overview(model):
    table = lk(os.path.join(DATA, model + ".mat"))
    lengths = list(table["L"])
    vds = vds_of(model)
    fig, axes = plt.subplots(2, 2, figsize=(11, 8))
    fig.suptitle(f"{model}: gm/ID overview at VDS = {vds} V, VSB = 0 V, W = {float(table['W'])} um, tt, 27 C")

    for length in lengths:
        gm_id = table.lookup("GM_ID", L=length, VDS=vds, VSB=0)
        vgs = np.asarray(table["VGS"]).ravel()
        axes[0][0].plot(vgs, np.asarray(gm_id).ravel(), label=f"L = {length:g} um")
        axes[0][1].semilogy(np.asarray(gm_id).ravel(), np.asarray(table.lookup("ID_W", L=length, VDS=vds, VSB=0)).ravel() * 1e6)
        axes[1][0].plot(np.asarray(gm_id).ravel(), np.asarray(table.lookup("GM_GDS", L=length, VDS=vds, VSB=0)).ravel())
        axes[1][1].semilogy(np.asarray(gm_id).ravel(),
                            np.asarray(table.lookup("GM_CGG", L=length, VDS=vds, VSB=0)).ravel() / (2 * np.pi) * 1e-9)

    axes[0][0].set_xlabel("VGS (V)")
    axes[0][0].set_ylabel("gm/ID (1/V)")
    axes[0][1].set_xlabel("gm/ID (1/V)")
    axes[0][1].set_ylabel("ID/W (uA/um)")
    axes[1][0].set_xlabel("gm/ID (1/V)")
    axes[1][0].set_ylabel("gm/gds")
    axes[1][1].set_xlabel("gm/ID (1/V)")
    axes[1][1].set_ylabel("fT (GHz)")
    for ax in axes.ravel():
        ax.grid(True, which="both", alpha=0.3)
    axes[0][0].legend(fontsize=8, ncol=2)
    fig.tight_layout()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, f"techsweep_{model}_plots_overview.pdf")
    fig.savefig(path)
    plt.close(fig)
    print(f"[INFO] {path}")


def main():
    names = sys.argv[1:]
    models = [n if n.startswith("sky130_fd_pr__") else "sky130_fd_pr__" + n for n in names]
    if not models:
        models = sorted(f[:-4] for f in os.listdir(DATA) if f.endswith(".mat"))
    for model in models:
        overview(model)
    return 0


if __name__ == "__main__":
    sys.exit(main())

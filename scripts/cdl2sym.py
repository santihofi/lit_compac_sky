#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Simon Dorrer and Harald Pretl
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
# Description: Writes Xschem symbols for pad cells from the port order of their CDL subcircuits, so the LVS
# netlists and the transient testbench call the pads with the pin order of the layout. The PDK ships no
# Xschem symbols for sky130_ef_io.
#
# Usage:
#   python3 scripts/cdl2sym.py $PDK_ROOT/$PDK/libs.ref/sky130_fd_io/cdl/sky130_ef_io.cdl schematic/xschem/sky130_ef_io <subckt> [<subckt> ...]
#
# Pin sides: pad-side pins (PAD, P_PAD, *_PAD, PAD_A_*) on the left, supplies on top (power) and bottom
# (ground), every other pin on the right. Directions come from the sky130_ef_io.v port declarations of the
# GPIO pad, everything else is inout.

import argparse
import os
import re
import sys

INPUTS = {"OUT", "OE_N", "HLD_H_N", "ENABLE_H", "ENABLE_INP_H", "ENABLE_VDDA_H", "ENABLE_VSWITCH_H", "ENABLE_VDDIO",
          "INP_DIS", "IB_MODE_SEL", "VTRIP_SEL", "SLOW", "HLD_OVR", "ANALOG_EN", "ANALOG_SEL", "ANALOG_POL",
          "DM[0]", "DM[1]", "DM[2]"}
OUTPUTS = {"IN", "IN_H", "TIE_HI_ESD", "TIE_LO_ESD"}
PITCH = 20      # pin pitch on the Xschem grid
STUB = 20       # pin stub length
HEADER = "v {xschem version=3.4.8RC file_version=1.3}\n"


def subckt_ports(cdl_path, name):
    """The port list of one .SUBCKT, continuation lines joined."""
    with open(cdl_path) as f:
        lines = f.read().splitlines()
    for i, line in enumerate(lines):
        if re.match(rf"\.subckt\s+{re.escape(name)}\b", line, re.I):
            text = line
            j = i + 1
            while j < len(lines) and lines[j].startswith("+"):
                text += " " + lines[j][1:]
                j += 1
            return text.split()[2:]
    sys.exit(f"[ERROR] {cdl_path}: no subcircuit {name}")


def side_of(pin):
    if pin == "PAD" or pin == "P_PAD" or pin.endswith("_PAD") or pin.startswith("PAD_A_"):
        return "left"
    if pin.startswith("VSS"):
        return "bottom"
    if pin.startswith("V") or pin.startswith("AMUXBUS"):
        return "top"
    return "right"


def direction(pin):
    if pin in INPUTS:
        return "in"
    if pin in OUTPUTS:
        return "out"
    return "inout"


def write_symbol(name, ports, out_dir):
    sides = {"left": [], "right": [], "top": [], "bottom": []}
    for p in ports:
        sides[side_of(p)].append(p)
    # box size from the busiest sides, one pitch of margin
    width = max(4, max(len(sides["top"]), len(sides["bottom"])) + 1) * PITCH
    height = max(4, max(len(sides["left"]), len(sides["right"])) + 1) * PITCH
    x0, y0 = -width // 2, -height // 2
    x1, y1 = width // 2, height // 2
    # snap to the 10 unit grid
    x0, y0, x1, y1 = (v - v % 10 for v in (x0, y0, x1, y1))
    pin_pos = {}
    for i, p in enumerate(sides["left"]):
        pin_pos[p] = (x0 - STUB, y0 + PITCH * (i + 1), "left")
    for i, p in enumerate(sides["right"]):
        pin_pos[p] = (x1 + STUB, y0 + PITCH * (i + 1), "right")
    for i, p in enumerate(sides["top"]):
        pin_pos[p] = (x0 + PITCH * (i + 1), y0 - STUB, "top")
    for i, p in enumerate(sides["bottom"]):
        pin_pos[p] = (x0 + PITCH * (i + 1), y1 + STUB, "bottom")

    lines = [HEADER, "G {}\n",
             "K {type=primitive\n"
             "format=\"@name @pinlist @symname\"\n"
             "spectre_format=\"@name ( @pinlist ) @symname\"\n"
             f"template=\"name=x1\"\n"
             "}\n",
             "V {}\n", "S {}\n", "E {}\n"]
    # outline
    lines.append(f"L 4 {x0} {y0} {x1} {y0} {{}}\n")
    lines.append(f"L 4 {x1} {y0} {x1} {y1} {{}}\n")
    lines.append(f"L 4 {x1} {y1} {x0} {y1} {{}}\n")
    lines.append(f"L 4 {x0} {y1} {x0} {y0} {{}}\n")
    lines.append(f"T {{{name}}} {x0 + 10} {y0 - 40} 0 0 0.3 0.3 {{}}\n")
    lines.append(f"T {{@name}} {x0 + 10} {y1 + 25} 0 0 0.3 0.3 {{}}\n")
    # pins in CDL order, the order of the B records is the pinlist order
    for p in ports:
        x, y, side = pin_pos[p]
        lines.append(f"B 5 {x - 2.5} {y - 2.5} {x + 2.5} {y + 2.5} {{name={p} dir={direction(p)}}}\n")
        if side == "left":
            lines.append(f"L 4 {x} {y} {x + STUB} {y} {{}}\n")
            lines.append(f"T {{{p}}} {x + STUB + 5} {y - 4} 0 0 0.2 0.2 {{}}\n")
        elif side == "right":
            lines.append(f"L 4 {x - STUB} {y} {x} {y} {{}}\n")
            lines.append(f"T {{{p}}} {x - STUB - 5} {y - 4} 0 1 0.2 0.2 {{}}\n")
        elif side == "top":
            lines.append(f"L 4 {x} {y} {x} {y + STUB} {{}}\n")
            lines.append(f"T {{{p}}} {x + 4} {y + STUB + 5} 1 0 0.2 0.2 {{}}\n")
        else:
            lines.append(f"L 4 {x} {y - STUB} {x} {y} {{}}\n")
            lines.append(f"T {{{p}}} {x + 4} {y - STUB - 5} 3 0 0.2 0.2 {{}}\n")
    path = os.path.join(out_dir, name + ".sym")
    with open(path, "w") as f:
        f.writelines(lines)
    print(f"[INFO] {path}: {len(ports)} pins")


def main():
    parser = argparse.ArgumentParser(description="Xschem symbols from CDL subcircuit port lists.")
    parser.add_argument("cdl", help="CDL file with the subcircuits")
    parser.add_argument("out_dir", help="folder for the .sym files")
    parser.add_argument("subckts", nargs="+", help="subcircuit names")
    args = parser.parse_args()
    os.makedirs(args.out_dir, exist_ok=True)
    for name in args.subckts:
        write_symbol(name, subckt_ports(args.cdl, name), args.out_dir)
    return 0


if __name__ == "__main__":
    sys.exit(main())

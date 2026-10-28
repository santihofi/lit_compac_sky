#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Simon Dorrer and Harald Pretl
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
# Description: Adds DIRECTION and USE to the pins of a LEF that Magic wrote from a GDS. The GDS carries no
# port attributes, so Magic writes bare PIN blocks and OpenROAD then takes every pin for a signal input.
# Supply pins are found by name (VDD, VSS, IOVDD, IOVSS, VPWR, VGND and the like), the others by the
# --input and --output name patterns, the rest become INOUT.

import argparse
import fnmatch
import re
import sys

POWER = {"VDD", "IOVDD", "VPWR", "VCCD", "VDDIO", "VDDA", "VPB"}
GROUND = {"VSS", "IOVSS", "VGND", "VSSD", "VSSIO", "VSSA", "VNB"}


def main():
    parser = argparse.ArgumentParser(description="Add DIRECTION and USE to the pins of a Magic-written LEF.")
    parser.add_argument("lef", help="LEF file, rewritten in place")
    parser.add_argument("--input", action="append", default=[], help="glob of input pin names (repeatable)")
    parser.add_argument("--output", action="append", default=[], help="glob of output pin names (repeatable)")
    args = parser.parse_args()

    with open(args.lef) as f:
        lines = f.readlines()
    out = []
    added = {}
    i = 0
    while i < len(lines):
        line = lines[i]
        out.append(line)
        m = re.match(r"(\s*)PIN\s+(\S+)\s*$", line)
        if m:
            indent, name = m.group(1) + "  ", m.group(2)
            block = []
            j = i + 1
            while j < len(lines) and not re.match(r"\s*(PORT|END)\b", lines[j]):
                block.append(lines[j])
                j += 1
            has_direction = any(re.match(r"\s*DIRECTION\b", l) for l in block)
            has_use = any(re.match(r"\s*USE\b", l) for l in block)
            base = name.split("[")[0]
            if base in POWER:
                direction, use = "INOUT", "POWER"
            elif base in GROUND:
                direction, use = "INOUT", "GROUND"
            elif any(fnmatch.fnmatch(name, g) for g in args.input):
                direction, use = "INPUT", "SIGNAL"
            elif any(fnmatch.fnmatch(name, g) for g in args.output):
                direction, use = "OUTPUT", "SIGNAL"
            else:
                direction, use = "INOUT", "SIGNAL"
            if not has_direction:
                out.append(f"{indent}DIRECTION {direction} ;\n")
            if not has_use:
                out.append(f"{indent}USE {use} ;\n")
            added[name] = (direction, use)
        i += 1
    if not added:
        sys.exit(f"[ERROR] {args.lef}: no PIN found.")
    with open(args.lef, "w") as f:
        f.writelines(out)
    for name, (direction, use) in added.items():
        print(f"[INFO] {args.lef}: pin {name} DIRECTION {direction} USE {use}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

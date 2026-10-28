# SPDX-FileCopyrightText: 2026 Simon Dorrer and Harald Pretl
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1

"""Merges a second GDS (the metal fill pattern of generate_fill.py) into a design GDS.

The top cell of the second file is copied into the layout of the first one and placed once at the origin
inside the design's top cell, which keeps the design hierarchy untouched.

Expected KLayout -rd parameters:
    design: path to the design GDS (read)
    fill:   path to the GDS to merge in (read)
    out:    path of the merged GDS (written, .gds or .gds.gz)
"""

import pya

layout = pya.Layout()
layout.read(design)
top = layout.top_cell()

fill_layout = pya.Layout()
fill_layout.read(fill)
fill_top = fill_layout.top_cell()

merged = layout.create_cell(fill_top.name)
merged.copy_tree(fill_top)
top.insert(pya.CellInstArray(merged.cell_index(), pya.Trans()))

layout.write(out)
print(f"[INFO] {out}: {fill_top.name} from {fill} placed inside {top.name} of {design}.")

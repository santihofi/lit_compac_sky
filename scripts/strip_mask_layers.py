# SPDX-FileCopyrightText: 2026 Simon Dorrer and Harald Pretl
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1

"""Writes a copy of a GDS without the foundry mask prep layers, so Magic can read it.

The OpenRAM SRAM macro of sky130A carries cfom.maskAdd (22/21), cfom.maskDrop (22/22), cp1m.maskDrop
(33/42) and cp1m.maskAdd (33/43) in its bit cells. Those layers describe the mask bias the foundry applies
and hold no design geometry, but sky130A.tech does not define them, so Magic stops with "Unknown
layer/datatype in boundary" on every cell that has them. The tapeout GDS keeps them, only the copy the
Magic targets read is filtered.

Expected KLayout -rd parameters:
    input:  path of the GDS to read
    output: path of the GDS to write
    layers: layers to drop as a comma separated list of layer/datatype (default: the four above)
"""

import pya

try:
    drop = layers
except NameError:
    drop = "22/21,22/22,33/42,33/43"

layout = pya.Layout()
layout.read(input)

removed = []
for spec in drop.split(","):
    layer_num, datatype = (int(v) for v in spec.split("/"))
    index = layout.find_layer(layer_num, datatype)
    if index is None:
        continue
    shapes = sum(layout.cell(c).shapes(index).size() for c in layout.each_cell_top_down())
    layout.delete_layer(index)
    removed.append(f"{layer_num}/{datatype} ({shapes} shapes)")

layout.write(output)
print(f"[INFO] {output}: written without {', '.join(removed) if removed else 'anything, no such layer'}.")

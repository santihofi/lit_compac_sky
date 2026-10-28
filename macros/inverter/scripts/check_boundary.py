# SPDX-FileCopyrightText: 2026 Simon Dorrer and Harald Pretl
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
# Description: Check that the top cell of a layout carries the PR boundary box the chip flow needs.

import argparse
import sys

# GDS layer and datatype of prBoundary. sky130A defines it as prBoundary.boundary 235/4, and Magic maps
# exactly that datatype to its BOUND layer (cifin: calma BOUND 235 4), from which LibreLane's Magic.StreamOut
# derives the FIXED_BBOX of every macro it places. Other datatypes of layer 235 mean nothing to it.
BOUNDARY_LAYER = 235
BOUNDARY_DATATYPE = 4


def boundary_shapes(kdb, layout, cell, layer):
    """Return (datatype, count, bbox) for every datatype of the boundary layer drawn in the cell itself."""
    found = []
    for index in layout.layer_indexes():
        info = layout.get_info(index)
        if info.layer != layer:
            continue
        shapes = cell.shapes(index)
        if shapes.size():
            bbox = kdb.Box()
            for shape in shapes.each():
                bbox = bbox + shape.bbox()
            found.append((info.datatype, shapes.size(), bbox))
    return found


def main():
    parser = argparse.ArgumentParser(
        description="Check that the top cell of a layout carries the PR boundary box the chip flow needs."
    )
    parser.add_argument("layout", help="layout file (GDS or OASIS)")
    parser.add_argument("cell", help="name of the top cell")
    parser.add_argument("--layer", type=int, default=BOUNDARY_LAYER,
                        help=f"GDS layer of the PR boundary (default: {BOUNDARY_LAYER})")
    parser.add_argument("--datatype", type=int, default=BOUNDARY_DATATYPE,
                        help=f"GDS datatype of the PR boundary (default: {BOUNDARY_DATATYPE})")
    args = parser.parse_args()

    try:
        import klayout.db as kdb
    except ImportError:
        print("[ERROR] The klayout Python module is not available. Run this inside the "
              "IIC-OSIC-TOOLS container.", file=sys.stderr)
        return 2

    layout = kdb.Layout()
    layout.read(args.layout)
    cell = layout.cell(args.cell)
    if cell is None:
        print(f"[ERROR] {args.layout}: no cell '{args.cell}' found.", file=sys.stderr)
        return 1

    print(f"[INFO] Checking the PR boundary of {args.cell} in {args.layout} ...", flush=True)
    found = boundary_shapes(kdb, layout, cell, args.layer)
    dbu = layout.dbu
    boundary = None
    for datatype, count, bbox in found:
        print(f"[INFO] {count} shape(s) on layer {args.layer}/{datatype}, "
              f"{bbox.width() * dbu:.3f} um x {bbox.height() * dbu:.3f} um.")
        if datatype == args.datatype:
            boundary = bbox
        else:
            print(f"[WARNING] Layer {args.layer}/{datatype} is not the boundary datatype Magic reads "
                  f"({args.layer}/{args.datatype}), the chip flow ignores it.")
    if boundary is None:
        print(f"[ERROR] {args.layout}: cell '{args.cell}' draws no shape on the PR boundary layer "
              f"{args.layer}/{args.datatype}. The chip flow derives the macro bounding box from it and fails "
              f"without it ('Failed to extract PR boundary from GDSII view of macro'). Draw the boundary box "
              f"on prBoundary ({args.layer}/{args.datatype}) in the layout source and re-export the GDS.",
              file=sys.stderr)
        return 1
    if not cell.bbox().inside(boundary):
        print(f"[WARNING] The geometry of '{args.cell}' extends beyond the PR boundary box "
              f"({cell.bbox().width() * dbu:.3f} um x {cell.bbox().height() * dbu:.3f} um versus "
              f"{boundary.width() * dbu:.3f} um x {boundary.height() * dbu:.3f} um). The chip flow "
              f"places the macro by the boundary, so anything outside it may overlap a neighbor.")
    print("[INFO] PR boundary check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

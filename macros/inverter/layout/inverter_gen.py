#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Simon Dorrer and Harald Pretl
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
# Description: Generates the sky130A inverter layouts with KLayout, layout/inverter.gds (the unit cell) and
# layout/inverter_top.gds (four units inside a VDD/VSS ring on met3 and met4). The transistors and the guard
# rings come from the skywater130 PCell library the PDK ships, every wire, via, rail, pin and the PR boundary
# is drawn here. Run it inside the IIC-OSIC-TOOLS container, where that library is loaded at start:
#   klayout -z -nc -r inverter_gen.py
# Every dimension is derived from the few constants below and from the PCell geometry read back at run time,
# so a size change in the schematic is a change of NF, WN or WP here, followed by a rerun.

import os
import pya

HERE = os.path.dirname(os.path.abspath(__file__))
LIB = "skywater130"

# Device sizes, kept identical to schematic/xschem/inverter.sch
L = 1.0            # channel length in um
PFET = "sky130_fd_pr__pfet_01v8_lvt"   # the low-threshold pmos puts the switching point at mid-supply
NF = 20            # fingers of M1 (nfet) and M2 (pfet)
WN = 1.0           # nfet finger width, W = NF * WN = 20 um
WP = 2.0           # pfet finger width, W = NF * WP = 40 um
NF_DUMMY = 2       # fingers of the two dummies, same finger widths

# sky130 layers (GDS layer, datatype)
DIFF, TAP, NWELL = (65, 20), (65, 44), (64, 20)
NSDM, PSDM = (93, 44), (94, 20)
MET1, VIA1, MET2, VIA2, MET3, VIA3, MET4 = (68, 20), (68, 44), (69, 20), (69, 44), (70, 20), (70, 44), (71, 20)
PIN = {MET1: (68, 16), MET2: (69, 16), MET3: (70, 16), MET4: (71, 16)}
LBL = {MET1: (68, 5), MET2: (69, 5), MET3: (70, 5), MET4: (71, 5)}
PRBOUNDARY = (235, 4)

# Drawn rules (um), taken from the sky130 periphery rules with margin where it costs nothing
VIA1_SIZE, VIA1_PITCH, VIA1_PAD = 0.15, 0.32, 0.32     # met1 and met2 enclose a via by 0.085 on every side
VIA1_PAD2 = 0.66                                       # pad length that takes exactly two vias in a row
VIA2_SIZE, VIA2_PITCH, VIA2_PAD = 0.20, 0.40, 0.40     # met2 encloses via2 by 0.085, met3 by 0.065
VIA3_SIZE, VIA3_PITCH, VIA3_PAD = 0.20, 0.40, 0.40     # met3 encloses via3 by 0.09, met4 by 0.065
RING_W = 0.29                                          # guard ring tap and metal width of the PCell
RAIL_H = 1.5                                           # met1 supply rail height inside a row
BUS_H = 0.40                                           # met2 drain bus height and riser width
GAP_DUMMY = 0.7                                        # diffusion gap between a device and its dummy, the implants need 0.38

# The 0.005 um grid of the PDK
DBU = 0.005


def r3(v):
    return round(v, 3)


class Gen:
    def __init__(self):
        self.ly = pya.Layout()
        self.ly.dbu = DBU
        self.stats = {}

    def layer(self, ld):
        return self.ly.layer(pya.LayerInfo(ld[0], ld[1]))

    def rect(self, cell, ld, l, b, r, t):
        assert r > l and t > b, (ld, l, b, r, t)
        cell.shapes(self.layer(ld)).insert(pya.DBox(r3(l), r3(b), r3(r), r3(t)))

    def text(self, cell, ld, x, y, s):
        cell.shapes(self.layer(ld)).insert(pya.DText(s, pya.DTrans(r3(x), r3(y))))

    def pin(self, cell, metal, l, b, r, t, name):
        """Metal, pin purpose and label for one port."""
        self.rect(cell, metal, l, b, r, t)
        self.rect(cell, PIN[metal], l, b, r, t)
        self.text(cell, LBL[metal], (l + r) / 2, (b + t) / 2, name)

    def via_array(self, cell, via, l, b, r, t, size, pitch, enc=0.09):
        """Fill the box with as many vias as fit at the pitch while every via keeps `enc` to the box edges,
        centered. Returns the count."""
        nx = max(1, int((r - l - 2 * enc - size) / pitch) + 1)
        ny = max(1, int((t - b - 2 * enc - size) / pitch) + 1)
        ox = (l + r) / 2 - (nx - 1) * pitch / 2 - size / 2
        oy = (b + t) / 2 - (ny - 1) * pitch / 2 - size / 2
        for i in range(nx):
            for j in range(ny):
                self.rect(cell, via, ox + i * pitch, oy + j * pitch, ox + i * pitch + size, oy + j * pitch + size)
        self.stats[via] = self.stats.get(via, 0) + nx * ny
        return nx * ny

    def stack(self, cell, l, b, r, t, top):
        """A via stack from met1 up to `top` (MET2, MET3 or MET4) over the box, with the pads of every level."""
        self.rect(cell, MET1, l, b, r, t)
        self.via_array(cell, VIA1, l, b, r, t, VIA1_SIZE, VIA1_PITCH)
        self.rect(cell, MET2, l, b, r, t)
        if top == MET2:
            return
        self.via_array(cell, VIA2, l, b, r, t, VIA2_SIZE, VIA2_PITCH)
        self.rect(cell, MET3, l, b, r, t)
        if top == MET3:
            return
        self.via_array(cell, VIA3, l, b, r, t, VIA3_SIZE, VIA3_PITCH)
        self.rect(cell, MET4, l, b, r, t)

    # ------------------------------------------------------------------ devices
    def fet(self, cell, kind, model, w, nf, gate_pos, x, y):
        """Place one PCell FET with its diffusion origin at (x, y) and read its met1 columns and gate pads back."""
        params = {"type": model, "l": L, "w": w, "nf": nf, "bulk": "None", "gate_con_pos": gate_pos, "con_bet_fin": True}
        pc = self.ly.create_cell(kind, LIB, params)
        assert pc is not None, f"PCell {kind} of library {LIB} not found, run inside the container"
        cell.insert(pya.DCellInstArray(pc.cell_index(), pya.DTrans(pya.DVector(x, y))))
        cols, pads = [], []
        for shape in pc.shapes(self.layer(MET1)).each():
            b = shape.dbbox().moved(x, y)
            (cols if b.height() > 0.5 else pads).append(b)
        cols.sort(key=lambda b: b.left)
        diff = pya.Region(pc.begin_shapes_rec(self.layer(DIFF))).bbox().to_dtype(DBU).moved(x, y)
        assert len(cols) == nf + 1 and len(pads) == nf, (kind, len(cols), len(pads))
        return {"cols": cols, "pads": pads, "diff": diff, "w": w}

    def ring(self, cell, implant, l, b, r, t):
        """A guard ring whose inner opening is the box, ring metal on met1."""
        params = {"in_w": r3(r - l), "in_l": r3(t - b), "grw": RING_W, "con_lev": "metal1", "implant_type": implant}
        pc = self.ly.create_cell("guard_ring_gen", LIB, params)
        assert pc is not None, "guard_ring_gen PCell not found"
        cell.insert(pya.DCellInstArray(pc.cell_index(), pya.DTrans(pya.DVector(l, b))))

    # ------------------------------------------------------------------ the unit cell
    def unit(self):
        cell = self.ly.create_cell("inverter")
        x0 = 1.5                      # diffusion left edge of both devices
        yn = 2.6                      # nfet diffusion bottom
        yp = 9.6                      # pfet diffusion bottom
        m1 = self.fet(cell, "nfet", "sky130_fd_pr__nfet_01v8", WN, NF, "top", x0, yn)
        x_dummy = x0 + m1["diff"].width() + GAP_DUMMY
        d1 = self.fet(cell, "nfet", "sky130_fd_pr__nfet_01v8", WN, NF_DUMMY, "top", x_dummy, yn)
        m2 = self.fet(cell, "pfet", PFET, WP, NF, "bottom", x0, yp)
        d2 = self.fet(cell, "pfet", PFET, WP, NF_DUMMY, "bottom", x_dummy, yp)

        # Ring openings: 0.8 um beside the devices, the rails inside the rings below the nfet and above the pfet
        ring_l = x0 - 0.8
        ring_r = d1["diff"].right + 0.8
        n_ring_b, n_ring_t = yn - 2.2, yn + 3.0          # nfet: rail below, gate pads above
        p_ring_b, p_ring_t = yp - 1.9, yp + 5.2          # pfet: gate pads below, rail above
        self.ring(cell, "psdm", ring_l, n_ring_b, ring_r, n_ring_t)
        self.ring(cell, "nsdm", ring_l, p_ring_b, ring_r, p_ring_t)
        # nwell over the whole pfet row including its ring
        nwell = pya.DBox(ring_l - RING_W - 0.24, p_ring_b - RING_W - 0.24, ring_r + RING_W + 0.24, p_ring_t + RING_W + 0.24)
        self.rect(cell, NWELL, nwell.left, nwell.bottom, nwell.right, nwell.top)

        # Supply rails, merged with the ring metal they touch
        vss = pya.DBox(ring_l, n_ring_b, ring_r, n_ring_b + RAIL_H)
        vdd = pya.DBox(ring_l, p_ring_t - RAIL_H, ring_r, p_ring_t)
        self.pin(cell, MET1, vss.left, vss.bottom, vss.right, vss.top, "VSS")
        self.pin(cell, MET1, vdd.left, vdd.bottom, vdd.right, vdd.top, "VDD")

        # Gate buses: one met1 rectangle over all gate pads of a device
        def bus(pads, extend_to=None):
            b = pads[0]
            for p in pads[1:]:
                b = b + p
            if extend_to is not None:
                b = pya.DBox(b.left, b.bottom, extend_to, b.top)
            self.rect(cell, MET1, b.left, b.bottom, b.right, b.top)
            return b
        n_bus = bus(m1["pads"])
        p_bus = bus(m2["pads"])
        bus(d1["pads"], extend_to=ring_r)                # dummy gates onto the VSS ring
        bus(d2["pads"], extend_to=ring_r)                # dummy gates onto the VDD ring
        assert n_bus.right < d1["pads"][0].left - 0.5 and p_bus.right < d2["pads"][0].left - 0.5

        # Sources to the rails, drains onto a met2 bus. Even columns are sources, so both ends are sources.
        def wire_row(dev, rail, up, bus_y):
            n_drain_vias = 0
            drain_boxes = []
            for i, c in enumerate(dev["cols"]):
                if i % 2 == 0:
                    if up:
                        self.rect(cell, MET1, c.left, c.top - 0.1, c.right, rail.bottom + 0.3)
                    else:
                        self.rect(cell, MET1, c.left, rail.top - 0.3, c.right, c.bottom + 0.1)
                else:
                    cx = (c.left + c.right) / 2
                    pad = pya.DBox(cx - VIA1_PAD / 2, bus_y - VIA1_PAD2 / 2, cx + VIA1_PAD / 2, bus_y + VIA1_PAD2 / 2)
                    self.rect(cell, MET1, pad.left, pad.bottom, pad.right, pad.top)
                    self.rect(cell, MET2, pad.left, pad.bottom, pad.right, pad.top)
                    n_drain_vias += self.via_array(cell, VIA1, pad.left, pad.bottom, pad.right, pad.top, VIA1_SIZE, VIA1_PITCH)
                    drain_boxes.append(pad)
            return drain_boxes, n_drain_vias
        n_bus_y = yn + WN / 2
        p_bus_y = yp + WP / 2
        n_drains, nv = wire_row(m1, vss, False, n_bus_y)
        p_drains, pv = wire_row(m2, vdd, True, p_bus_y)
        for c in d1["cols"]:
            self.rect(cell, MET1, c.left, vss.top - 0.3, c.right, c.bottom + 0.1)
        for c in d2["cols"]:
            self.rect(cell, MET1, c.left, c.top - 0.1, c.right, vdd.bottom + 0.3)
        assert nv == 2 * (NF // 2) and pv == 2 * (NF // 2), (nv, pv)

        # Output riser on met2 between the devices and their dummies, drain buses reach it
        x_out = x0 + m1["diff"].width() + GAP_DUMMY / 2
        self.rect(cell, MET2, n_drains[0].left, n_bus_y - BUS_H / 2, x_out + BUS_H / 2, n_bus_y + BUS_H / 2)
        self.rect(cell, MET2, p_drains[0].left, p_bus_y - BUS_H / 2, x_out + BUS_H / 2, p_bus_y + BUS_H / 2)
        self.rect(cell, MET2, x_out - BUS_H / 2, n_bus_y - BUS_H / 2, x_out + BUS_H / 2, p_bus_y + BUS_H / 2)

        # Input riser on met2 at the left end of the gate buses, via pairs on both buses
        x_in = n_bus.left + VIA1_PAD / 2 + 0.05
        for b in (n_bus, p_bus):
            pad = pya.DBox(x_in - VIA1_PAD / 2, b.bottom + 0.05, x_in + VIA1_PAD / 2, b.top - 0.05)
            self.rect(cell, MET2, pad.left, pad.bottom, pad.right, pad.top)
            self.via_array(cell, VIA1, pad.left, pad.bottom, pad.right, pad.top, VIA1_SIZE, VIA1_PITCH)
        self.rect(cell, MET2, x_in - BUS_H / 2, n_bus.bottom + 0.05, x_in + BUS_H / 2, p_bus.top - 0.05)

        # Boundary and the two signal pins as met2 stubs in the channel between the rings
        width = r3(ring_r + RING_W + 0.24 + 0.4)
        height = r3(p_ring_t + RING_W + 0.24 + 0.4)
        y_ch = (n_ring_t + RING_W + p_ring_b - RING_W) / 2
        self.rect(cell, MET2, 0.0, y_ch - BUS_H / 2, x_in + BUS_H / 2, y_ch + BUS_H / 2)
        self.rect(cell, MET2, x_out - BUS_H / 2, y_ch - BUS_H / 2, width, y_ch + BUS_H / 2)
        self.pin(cell, MET2, 0.0, y_ch - BUS_H / 2, 0.6, y_ch + BUS_H / 2, "vin")
        self.pin(cell, MET2, width - 0.6, y_ch - BUS_H / 2, width, y_ch + BUS_H / 2, "vout")
        self.rect(cell, PRBOUNDARY, 0.0, 0.0, width, height)

        # The PCells are flattened into the cell, so the GDS carries plain geometry only
        cell.flatten(-1, True)
        self.unit_info = {"width": width, "height": height, "vss": vss, "vdd": vdd, "y_ch": y_ch}
        return cell

    # ------------------------------------------------------------------ the macro
    def top(self, unit):
        cell = self.ly.create_cell("inverter_top")
        u = self.unit_info
        ring_w, ring_gap, margin, unit_gap = 1.6, 0.6, 1.0, 1.0
        inner = ring_w + ring_gap                       # start of the inner (VDD) ring
        x_u = inner + ring_w + margin                   # unit column left edge
        pitch = u["height"] + unit_gap
        width = r3(x_u + u["width"] + margin + ring_w + ring_gap + ring_w)
        height = r3(2 * (inner + ring_w + margin) + 4 * u["height"] + 3 * unit_gap)
        y_u = [r3(inner + ring_w + margin + k * pitch) for k in range(4)]
        for k, y in enumerate(y_u):
            cell.insert(pya.DCellInstArray(unit.cell_index(), pya.DTrans(pya.DVector(x_u, y))))

        # Outer VSS ring and inner VDD ring: met3 top and bottom bars, met4 left and right bars, via3 corners
        def ring_bars(off, name):
            l, b, r, t = off, off, width - off, height - off
            self.pin(cell, MET3, l, b, r, b + ring_w, name)                    # bottom bar
            self.pin(cell, MET3, l, t - ring_w, r, t, name)                    # top bar
            self.pin(cell, MET4, l, b, l + ring_w, t, name)                    # left bar
            self.pin(cell, MET4, r - ring_w, b, r, t, name)                    # right bar
            for cx in (l, r - ring_w):
                for cy in (b, t - ring_w):
                    self.via_array(cell, VIA3, cx + 0.1, cy + 0.1, cx + ring_w - 0.1, cy + ring_w - 0.1, VIA3_SIZE, VIA3_PITCH)
            return l, r - ring_w
        vss_l, vss_r = ring_bars(0.0, "VSS")
        vdd_l, vdd_r = ring_bars(inner, "VDD")

        # Every unit rail reaches its ring bar on both sides through a via stack, VSS passes under the VDD bar on met1
        for y in y_u:
            for rail, xl, xr, top in ((u["vss"], vss_l, vss_r, MET4), (u["vdd"], vdd_l, vdd_r, MET4)):
                b, t = y + rail.bottom, y + rail.top
                self.rect(cell, MET1, xl + 0.1, b, x_u + rail.left + 0.2, t)
                self.rect(cell, MET1, x_u + rail.right - 0.2, b, xr + ring_w - 0.1, t)
                self.stack(cell, xl + 0.2, b + 0.1, xl + ring_w - 0.2, t - 0.1, top)
                self.stack(cell, xr + 0.2, b + 0.1, xr + ring_w - 0.2, t - 0.1, top)
            # signal stubs from the unit edge to the macro edge on met2, under the ring bars
            yc = y + u["y_ch"]
            k = y_u.index(y) + 1
            self.rect(cell, MET2, 0.0, yc - BUS_H / 2, x_u + 0.3, yc + BUS_H / 2)
            self.rect(cell, MET2, x_u + u["width"] - 0.3, yc - BUS_H / 2, width, yc + BUS_H / 2)
            self.pin(cell, MET2, 0.0, yc - BUS_H / 2, 0.8, yc + BUS_H / 2, f"vin{k}")
            self.pin(cell, MET2, width - 0.8, yc - BUS_H / 2, width, yc + BUS_H / 2, f"vout{k}")
        self.rect(cell, PRBOUNDARY, 0.0, 0.0, width, height)
        self.top_info = {"width": width, "height": height}
        return cell


def main():
    g = Gen()
    unit = g.unit()
    top = g.top(unit)
    # inverter.gds holds the unit cell alone, inverter_top.gds the macro with the unit as its subcell
    single = pya.Layout()
    single.dbu = DBU
    single.create_cell("inverter").copy_tree(unit)
    single.write(os.path.join(HERE, "inverter.gds"))
    opts = pya.SaveLayoutOptions()
    opts.select_cell(top.cell_index())
    opts.add_cell(top.cell_index())
    g.ly.write(os.path.join(HERE, "inverter_top.gds"), opts)
    print(f"[INFO] inverter: {g.unit_info['width']} um x {g.unit_info['height']} um")
    print(f"[INFO] inverter_top: {g.top_info['width']} um x {g.top_info['height']} um")
    print("[INFO] vias:", {f"{k[0]}/{k[1]}": v for k, v in g.stats.items()})


main()

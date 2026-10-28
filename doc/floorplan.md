# Floorplan

Die and core geometry of `chip_top`, where the hard macros sit and how the power reaches them. Every number here is in [flow/librelane/config.yaml](../flow/librelane/config.yaml), this file explains why.

## Die and core

| Item | Value |
| --- | --- |
| Die | 0 to 1600 um in x and y, 2.56 mm2 |
| Core | 300 to 1300 um in x and y, 1.0 mm2 |
| Pad depth | 198 um (`sky130_ef_io` cells are 197.965 um deep) |
| Corner cells | 200 um x 204 um |
| Margin between pad row and core | about 100 um, taken by the core ring and its clearance |
| Standard cell row | 2.72 um high, `unithd` site 0.46 um wide |
| Manufacturing grid | 0.005 um |

The core margin of 300 um is the pad depth plus room for the core ring. The same four numbers appear in [scripts/add_logo_fill.sh](../scripts/add_logo_fill.sh), which places the chip logo relative to the core corner. Change one, change both.

## Pad ring

Each side offers 1200 um between the two corner cells. The GPIO pads are 80 um wide, the supply and analog pads 75 um and the connect slices 20 um, and `OpenROAD.PadRing` centres the row and floors the gap between two cells to a multiple of `PAD_SPACING_MULTIPLE`.

| Side | Cells | Cell width sum | Fill | Gap | End spacing |
| --- | --- | --- | --- | --- | --- |
| West | 10 (8 pads, 2 connect slices) | 660 um | 540 um | 48 um | 54 um |
| North | 8 | 640 um | 560 um | 62 um | 63 um |
| South | 8 | 640 um | 560 um | 62 um | 63 um |
| East | 8 | 620 um | 580 um | 64 um | 66 um |

`PAD_SPACING_MULTIPLE` is 2 um. With the default of 1 um the west row ends on 49.5 um, which is not a multiple of the 1 um IO site, and the pad ring step stops with an error. The rule of thumb: pick the multiple so that the leftover at the two row ends lands on the site grid.

## Macro placement

Coordinates are the lower left corner of the macro in micrometres, as `MACROS` gives them.

| Instance | Position | Size | Orientation |
| --- | --- | --- | --- |
| `i_chip_core.sram_0` | 336.26, 336.26 | 479.78 x 397.50 | N |
| `i_chip_core.counter2` | 899.30, 703.80 | 200 x 100 | FS |
| `i_chip_core.counter1` | 899.30, 899.30 | 200 x 100 | N |
| `i_chip_core.inverter2` | 1219.92, 649.06 | 42.73 x 75.52 | N |
| `i_chip_core.inverter1` | 1219.92, 852.38 | 42.73 x 75.52 | N |
| `jku_logo` | 320, 1180 | 100 x 100 | N |
| `jku_names` | 1180, 1180 | 100 x 100 | N |

Two rules decide those positions.

**On the track grid.** Every macro origin is a multiple of 7.82 um, the common period of the `met1` track pitch (0.34 um) and the `met2` one (0.46 um). A macro placed off that grid puts its pins between the top-level tracks, and the detailed router then reports `DRT-0073 No access point` for them.

**On a power stripe.** The PDN runs `met4` stripes every 153.6 um. A macro narrower than that pitch can fall between two stripes, and then nothing connects its supply ring: the power grid analysis reports its shapes as unconnected and LVS reports its supply pins as separate nets. The two inverters are 42.73 um wide, so they are placed around the stripe pair at x = 1083.9 um and 1087.2 um. The counters at x = 899.3 um and the SRAM catch a stripe by their width alone.

## Power distribution

| Item | Layer | Value |
| --- | --- | --- |
| Standard cell rails | `met1` | 0.48 um wide, along every row |
| Vertical stripes | `met4` | 1.6 um wide, pitch 153.6 um, offset 16.32 um |
| Horizontal stripes | `met5` | 1.6 um wide, pitch 153.18 um, offset 16.65 um |
| Core ring | `met4` and `met5` | 10 um wide, 5 um spacing, 6 um from the core |
| Macro halo | - | 10 um in both directions |

The core ring connects to the pads through their `met3` supply tabs, which is what `PDN_CORE_RING_CONNECT_TO_PAD_LAYERS` names. The tab of the `VDD` pad alone carries 3000 via3 cuts into the ring.

Three macro grids are defined in [flow/librelane/pdn_cfg.tcl](../flow/librelane/pdn_cfg.tcl):

- the default grid for the two counters, which connects `met4` to `met5`,
- one for the two inverters and one for the SRAM, which add a `met3` to `met4` connection, because all three macros expose their supply ring on `met3` (horizontal) and `met4` (vertical).

`PDN_MACRO_CONNECTIONS` lists all five macros. The sky130A global connections only cover the `VPWR` and `VGND` pins of the standard cells, so a macro with `VDD` and `VSS` pins has to be named explicitly or it stays unconnected.

## Metal fill and logo

The metal fill is not inserted by the flow (`KLayout.Filler` is disabled). [scripts/add_logo_fill.sh](../scripts/add_logo_fill.sh) draws the chip logo on `met5` with ArtistIC and then runs the PDK fill generator `libs.tech/magic/generate_fill.py`, which fills tile by tile in 700 um squares and keeps its own distance to the drawn geometry. The result is `layout/chip_top_logo_fill.gds.gz`, which is the GDS every sign-off step reads.

## Where the geometry is written down

| File | What it holds |
| --- | --- |
| [flow/librelane/config.yaml](../flow/librelane/config.yaml) | `DIE_AREA`, `CORE_AREA`, the pad rows, the macro positions |
| [scripts/add_logo_fill.sh](../scripts/add_logo_fill.sh) | the same die and core box, for the logo placement |
| [packaging/config.yaml](../packaging/config.yaml) | the package and the pad to lead assignment |
| this file and [specifications.md](specifications.md) | the human readable copy |

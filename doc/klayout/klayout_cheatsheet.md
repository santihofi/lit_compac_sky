# KLayout cheatsheet for sky130A

Everything this template needs from KLayout with the sky130A PDK: how to start it, the PCells, the layers, and where the DRC and LVS menu entries write.

## Starting it

```sh
ke layout/lit_compac_top_logo_fill.gds.gz     # alias of klayout -e, edit mode, in the container
klayout -e layout/inverter.gds          # the same by hand
make open                               # the file browser of this repo, one button per file
```

The container sets `KLAYOUT_PATH` to the PDK technology folder, so KLayout starts with the `sky130A` technology, its layer properties and its macros. Check the technology in the title bar or with `Tools > Manage Technologies`. If it says `default`, `$PDK` is not `sky130A` in that shell.

## Shortcuts that matter

| Key | Action |
| --- | --- |
| `*` | show all hierarchy levels |
| `Shift+F2` | fit the layout in the window |
| `F2` | fit the selection |
| `Escape` | cancel the current operation |
| `l` | layer selection dialog |
| `s` | partial edit mode, moves edges and points |
| `r` | rectangle, `p` path, `i` instance |
| `Ctrl+Shift+F` | flatten the selected instance |
| `Shift+click` | add to the selection |
| `q` | properties of the selected object |
| `Ctrl+Shift+M` | marker browser, which reads the DRC and LVS databases |

## PCells

The PDK ships one KLayout library, `skywater130`, loaded by `libs.tech/klayout/pymacros/sky130_pcells.lym`. Its cells appear under `Instance > Library: skywater130`:

| PCell | Device |
| --- | --- |
| `nfet`, `pfet` | the MOSFET families, with the model as a parameter, plus fingers, guard ring and contact options |
| `res_poly`, `res_diff`, `res_metal` | the resistor families |
| `mim_cap`, `cap_var`, `cap_vpp` | MIM, varactor and vertical parallel plate capacitors |
| `n_diode`, `p_diode`, `photodiode` | diodes |
| `npn_bjt`, `pnp_bjt`, `rf_bjt` | bipolars |
| `rf_mosfet`, `rf_coils` | RF devices and inductors |
| `guard_ring_gen` | a guard ring of a given opening, implant and contact level |
| `vias_gen` | a via array between two layers |

The library needs the `gdsfactory` Python package, which the container has. In batch mode it is loaded with the technology:

```sh
klayout -z -nc -r layout/inverter_gen.py
```

[macros/inverter/layout/inverter_gen.py](../../macros/inverter/layout/inverter_gen.py) is the worked example: it places `nfet`, `pfet` and `guard_ring_gen` and draws everything else itself.

The PCell library is a Mabrains contribution and its README marks the device status. The three cells this template uses are listed as verified against DRC and LVS. The library has 18 PCells and none of them is a low threshold flavour of its own, which is why the inverter generator asks the `pfet` PCell for `sky130_fd_pr__pfet_01v8_lvt` through its `type` parameter.

## Layers

sky130 names a layer by purpose, and the layer properties file spells it out as `name.purpose - number/datatype`:

| Layer | GDS | Role |
| --- | --- | --- |
| `nwell.drawing` | 64/20 | n well |
| `diff.drawing` | 65/20 | diffusion |
| `tap.drawing` | 65/44 | well and substrate taps |
| `poly.drawing` | 66/20 | gate poly |
| `nsdm`, `psdm` | 93/44, 94/20 | n and p source drain implant |
| `lvtn`, `hvtp` | 125/44, 78/44 | low and high threshold implants |
| `licon1` | 66/44 | contact to diffusion, tap and poly |
| `li1.drawing` | 67/20 | local interconnect |
| `mcon` | 67/44 | via from `li1` to `met1` |
| `met1` to `met5` | 68/20, 69/20, 70/20, 71/20, 72/20 | metals |
| `via`, `via2`, `via3`, `via4` | 68/44, 69/44, 70/44, 71/44 | vias between them |
| `pad` | 76/20 | passivation opening, the bondpad |
| `prBoundary.boundary` | 235/4 | the place and route boundary |

Two purposes matter beside `drawing`: `pin` (`68/16` for `met1`) marks a connection point, and `label` (`68/5`) carries the net name. A pin without a label is invisible to LVS, a label without a pin is invisible to the router.

`prBoundary` is the only layer with datatype 4 in this list. Magic maps exactly `235/4` to its boundary layer, so a boundary drawn on another datatype is silently ignored by the chip flow. [macros/inverter/scripts/check_boundary.py](../../macros/inverter/scripts/check_boundary.py) checks it.

## DRC

Batch, through the repository targets:

```sh
make klayout-drc CELL=inverter DRC_LEVEL=macro     # in a macro folder
make klayout-drc-regular                           # the chip, all checks
```

`sak-drc.sh` runs the PDK deck `libs.tech/klayout/drc/sky130A_mr.drc` once per check group and writes one marker database per group directly into the report folder:

| File | Group |
| --- | --- |
| `<cell>.klayout.drc.feol.xml` | front end of line, including off grid at `macro` and `regular` |
| `<cell>.klayout.drc.beol.xml` | back end of line |
| `<cell>.klayout.drc.pincheck.xml` | pin and label checks |
| `<cell>.klayout.drc.zeroarea.xml` | zero area shapes |
| `<cell>.klayout.drc.density.xml` | metal density, only at `regular` |

That is different from the IHP templates, which get one `.lyrdb` in a run folder. Open a `.xml` with `Tools > Marker Browser`.

In the GUI: `Efabless sky130 > Run DRC (Custom)` runs the same deck on the open layout with the checks ticked in its dialog, and writes `sky130_drc.txt` next to the GDS. Despite the name that file is a marker database, open it in the marker browser. `layout/.gitignore` keeps it out of git.

## LVS

Batch:

```sh
make klayout-lvs CELL=inverter
```

`sak-lvs.sh` runs `libs.tech/klayout/lvs/sky130.lvs` and writes `<cell>.lvsdb` plus the extracted netlist. Two things about the schematic netlist it compares against:

- The netlist has to use `M` lines. The deck reads an `X` line as a subcircuit unless it is started with `convert_subckts=true`, so the Makefile exports the CDL with `set spiceprefix 0`.
- The lengths and widths on an `M` line are metres. The Xschem sky130 symbols write micrometres, for the ngspice `scale` option, so the Makefile appends `u` to every `L` and `W` after the export. Without that the compare fails with every net unmatched.

In the GUI: `Efabless sky130 > Run LVS` asks for the schematic netlist first. Its file dialog filters `.spice`, so type the name of the `.cdl` file. It writes `<cell>.lvsdb` and `<cell>_extracted.cir` next to the GDS, both ignored by git.

## Reading a marker database

`Tools > Marker Browser > File > Open` and pick the `.xml` or `.lvsdb`. The browser lists the rule names of the deck, and a click on a marker zooms to it. For LVS, the browser shows the netlist comparison as a tree, and the unmatched nets are the ones to start from.

## Other useful things

```sh
sak-render.py -t sky130A -w 2048 -s 4 -o render/img/chip layout/lit_compac_top.gds.gz
sak-render.py -t sky130A --list        # the layer names and groups the renderer knows
klayout -zz -r scripts/strip_mask_layers.py -rd input=a.gds -rd output=b.gds
```

The renderer takes the colours from the PDK layer properties, so a render looks like the layout does in the GUI.

# sky130A Open-PDK

sky130A ships no documentation folder, unlike the IHP PDKs, so this file is a link index plus the numbers this template measured in the installed PDK.

## Version

| Item | Value |
| --- | --- |
| open_pdks | `026824c7969ce6f4fc9678e6ca04b0a06a596c4b` (`$PDK_ROOT/sky130A/SOURCES`) |
| Magic tech file | `1.0.588-56-g026824c` (`version` in `libs.tech/magic/sky130A.tech`) |
| Container | IIC-OSIC-TOOLS 2026.08 |

Check the stamp before letting a number here decide a rule:

```sh
cat $PDK_ROOT/$PDK/SOURCES
grep -A1 '^version' $PDK_ROOT/$PDK/libs.tech/magic/sky130A.tech
```

## Documentation

The authoritative sky130 documentation is online, the PDK carries the decks instead of the prose.

| Topic | Where |
| --- | --- |
| Process and design rules | <https://skywater-pdk.readthedocs.io/en/main/rules.html> |
| Periphery rules (pads, seal ring) | <https://skywater-pdk.readthedocs.io/en/main/rules/periphery.html> |
| Layer table with GDS numbers | <https://skywater-pdk.readthedocs.io/en/main/rules/layers.html> |
| Device models and their parameters | <https://skywater-pdk.readthedocs.io/en/main/rules/device-details.html> |
| Standard cell library `sky130_fd_sc_hd` | <https://skywater-pdk.readthedocs.io/en/main/contents/libraries/sky130_fd_sc_hd.html> |
| IO library `sky130_fd_io` and the Efabless wrappers | <https://skywater-pdk.readthedocs.io/en/main/contents/libraries/sky130_fd_io.html> |
| OpenRAM SRAM macros | <https://github.com/VLSIDA/sky130_sram_macros> |
| open_pdks, which assembles the PDK for the tools | <https://github.com/RTimothyEdwards/open_pdks> |

## What the installed PDK holds

| Folder | Contents this template uses |
| --- | --- |
| `libs.tech/ngspice/` | `sky130.lib.spice` with the corner, mismatch and Monte Carlo sections, see [sky130A_ngspice_mc_mm_guide.md](sky130A_ngspice_mc_mm_guide.md) |
| `libs.tech/klayout/` | the DRC decks `sky130A_mr.drc` and the density and pin checks, the LVS deck `sky130.lvs`, the `skywater130` PCell library and the layer properties |
| `libs.tech/magic/` | `sky130A.tech`, `sky130A.magicrc`, the fill generator `generate_fill.py`, the seal ring generator |
| `libs.tech/netgen/` | `sky130A_setup.tcl`, the LVS setup this chip extends in [flow/librelane/netgen_setup.tcl](../../flow/librelane/netgen_setup.tcl) |
| `libs.tech/xschem/` | the device symbols, the `SKY130` menu and `sky130_save_fet_params` |
| `libs.tech/librelane/` | the LibreLane PDK configuration, including the pad site and liberty lists |
| `libs.ref/sky130_fd_sc_hd/` | the standard cells, the technology LEF this template reads its stack numbers from |
| `libs.ref/sky130_fd_io/` | the pad cells: LEF, GDS, Verilog, CDL, SPICE and liberty |
| `libs.ref/sky130_sram_macros/` | the OpenRAM SRAMs |
| `libs.ref/sky130_fd_pr/` | the device models, including the mismatch corner files |

## Deterministic passive models

[Passive corner selection and measured controls](passive-corners.md) explains the installed RC bundles and why MOS corners alone keep passives typical.

## Layout numbers

The metal stack, the via table and the current limits are in [../librelane/librelane_cheatsheet.md](../librelane/librelane_cheatsheet.md), read out of `sky130_fd_sc_hd__nom.tlef`. The two numbers that decide most layout work:

| Layer | Minimum width | Pitch |
| --- | --- | --- |
| `li1` | 0.17 um | 0.46 um |
| `met1` | 0.14 um | 0.34 um |
| `met2` | 0.14 um | 0.46 um |
| `met3` | 0.30 um | 0.68 um |
| `met4` | 0.30 um | 0.92 um |
| `met5` | 1.60 um | 3.40 um |

`met5` is the thick top metal: 1.6 um minimum width and space, which is why the chip PDN uses it for the horizontal stripes and why the logos are drawn on `met4`.

## Known limitations of this PDK for this flow

- **Magic cannot read the GDS of the OpenRAM SRAM macros.** The bit cells carry the foundry mask prep layers `cfom.maskAdd` (22/21), `cfom.maskDrop` (22/22), `cp1m.maskDrop` (33/42) and `cp1m.maskAdd` (33/43), which `sky130A.tech` does not define. Every Magic step that reads that GDS stops with `Unknown layer/datatype in boundary`. [scripts/strip_mask_layers.py](../../scripts/strip_mask_layers.py) writes the filtered copy the Magic targets read, the tapeout GDS keeps the layers.
- **The SRAM has one characterized corner**, `TT_1p8V_25C`. Every STA corner of this chip reads it.
- **The pad ring connects its supply buses by abutment.** Tools that follow wires and not net names, the OpenROAD power grid analysis and the DEF based Magic extraction, do not see those connections. What that costs and how this template handles it is in the comments of [flow/librelane/config.yaml](../../flow/librelane/config.yaml).
- **The PDK ships no Xschem symbols for the pad cells.** [scripts/cdl2sym.py](../../scripts/cdl2sym.py) generates them from the port lists of the PDK netlists into [schematic/xschem/sky130_ef_io/](../../schematic/xschem/sky130_ef_io/).

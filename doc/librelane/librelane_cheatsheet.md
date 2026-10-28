# LibreLane cheatsheet for sky130A

What the flow writes, how to read it, and the numbers of the sky130A metal stack that the configuration depends on. The tables are read out of the installed PDK, the commands to reproduce them are given.

## The `final/` folder

`make librelane` runs the flow with `--save-views-to flow/final/`, so the views of the last run land in one place:

| Folder | File | Used by |
| --- | --- | --- |
| `gds/` | `lit_compac_top.gds` | `copy-gds`, the logo and fill step, every sign-off run |
| `def/`, `odb/` | the placed and routed database | a rerun with `--last-run`, the OpenROAD and KLayout GUI targets |
| `nl/` | `lit_compac_top.nl.v` | gate-level simulation without power pins |
| `pnl/` | `lit_compac_top.pnl.v` | the netlist with power pins, the LVS reference |
| `spice/` | `lit_compac_top.spice` | `check-ports`, the netlist comparison |
| `lib/`, `sdf/` | timing views per corner | a parent design that instantiates this block |
| `spef/` | parasitics per corner | STA of a parent design |
| `json_h/` | the JSON header | a parent flow that needs the port list |

A macro build (`macros/counter`) writes the same set into its own `final/`, which is what the chip configuration reads through `MACROS`.

## Reading a run

```sh
ls flow/librelane/runs/                 # one folder per run, named by date
ls flow/librelane/runs/RUN_*/           # one folder per step, numbered in flow order
make librelane-openroad                 # open the last run in the OpenROAD GUI
make librelane-klayout                  # open the last run in KLayout
```

Every step folder holds its `config.json` (the variables as the step saw them), its log, and the views it wrote. `COMMANDS` is the command line that produced it, which is the fastest way to rerun one step by hand.

To rerun from the middle of a flow, for example after changing the LVS setup:

```sh
librelane flow/librelane/config.yaml --pdk $PDK --pdk-root $PDK_ROOT --manual-pdk \
  --last-run --from Netgen.LVS --to Checker.LVS
```

## Metal stack

Read out of `$PDK_ROOT/$PDK/libs.ref/sky130_fd_sc_hd/techlef/sky130_fd_sc_hd__nom.tlef`:

| Layer | Direction | Min width | Pitch | Min area | Sheet resistance | DC limit |
| --- | --- | --- | --- | --- | --- | --- |
| `li1` | vertical | 0.17 um | 0.46 um | 0.0561 um2 | 12.8 ohm/sq | - |
| `met1` | horizontal | 0.14 um | 0.34 um | 0.083 um2 | 0.125 ohm/sq | 2.8 mA/um |
| `met2` | vertical | 0.14 um | 0.46 um | 0.0676 um2 | 0.125 ohm/sq | 2.8 mA/um |
| `met3` | horizontal | 0.30 um | 0.68 um | 0.24 um2 | 0.047 ohm/sq | 6.8 mA/um |
| `met4` | vertical | 0.30 um | 0.92 um | 0.24 um2 | 0.047 ohm/sq | 6.8 mA/um |
| `met5` | horizontal | 1.60 um | 3.40 um | 4.0 um2 | 0.0285 ohm/sq | 10.17 mA/um |

`li1` is the local interconnect, one layer below `met1`, with a hundred times the sheet resistance of the metals. It carries the standard cell pins, not routing.

## Vias

| Cut | Size | Spacing | Resistance per cut | DC limit per cut |
| --- | --- | --- | --- | --- |
| `mcon` (`li1` to `met1`) | 0.17 um | 0.19 um | 9.30 ohm | 0.36 mA |
| `via` (`met1` to `met2`) | 0.15 um | 0.17 um | 4.50 ohm | 0.29 mA |
| `via2` (`met2` to `met3`) | 0.20 um | 0.20 um | 3.41 ohm | 0.48 mA |
| `via3` (`met3` to `met4`) | 0.20 um | 0.20 um | 3.41 ohm | 0.48 mA |
| `via4` (`met4` to `met5`) | 0.80 um | 0.80 um | 0.38 ohm | 2.49 mA |

The via rules the router uses are the `_PR` via definitions of the tech LEF:

```
L1M1_PR  M1M2_PR  M2M3_PR  M3M4_PR  M4M5_PR
```

each with the variants `_C`, `_M`, `_MR` and `_R`, which differ in the enclosure shape. A non-default rule names the base variants:

```yaml
NON_DEFAULT_RULES:
  NDR_analog:
    width:   [met1, "0.5", met2, "0.5", met3, "0.5", met4, "0.5"]
    spacing: [met1, "0.5", met2, "0.5", met3, "0.5", met4, "0.5"]
    via:     ["M1M2_PR", "M2M3_PR", "M3M4_PR"]
```

`met5` is not in that list: its minimum width is 1.6 um, which is wider than the rule, and it carries the power stripes.

Reproduce both tables:

```sh
python3 - <<'EOF'
import os, re
t = open(os.path.join(os.environ["PDK_ROOT"], os.environ["PDK"],
         "libs.ref/sky130_fd_sc_hd/techlef/sky130_fd_sc_hd__nom.tlef")).read()
for m in re.finditer(r"LAYER (\S+)\n(.*?)END \1", t, re.S):
    if "TYPE ROUTING" in m.group(2) or "TYPE CUT" in m.group(2):
        print(m.group(1), re.findall(r"^\s*(WIDTH|PITCH|AREA|RESISTANCE.*|DCCURRENTDENSITY.*)\s", m.group(2), re.M))
EOF
```

## Sites and grid

| Item | Value |
| --- | --- |
| Standard cell site `unithd` | 0.46 um x 2.72 um |
| Double height site `unithddbl` | 0.46 um x 5.44 um |
| Pad site `sky130_io` | 1.0 um x 200 um |
| Pad corner site `sky130_io_corner` | 200 um x 204 um |
| Manufacturing grid | 0.005 um |

A macro origin that is a multiple of 7.82 um sits on both the `met1` and the `met2` track grid (0.34 um and 0.46 um have 7.82 um as their common period). Off that grid the detailed router reports `DRT-0073 No access point` for the macro pins.

## Orientations

LEF and DEF name the eight orientations the same way, and `MACROS` in the configuration takes them:

| Name | Meaning |
| --- | --- |
| `N` | as drawn |
| `S` | rotated 180 degrees |
| `E` | rotated 270 degrees (clockwise 90) |
| `W` | rotated 90 degrees |
| `FN` | mirrored about the y axis |
| `FS` | mirrored about the x axis |
| `FE` | mirrored, then rotated 270 degrees |
| `FW` | mirrored, then rotated 90 degrees |

A macro row that alternates `N` and `FS` shares its supply rails between neighbours, which is why `counter2` is placed `FS`.

## Steps this chip switches off

| Step | Why |
| --- | --- |
| `KLayout.Filler` | the fill comes after the logo, from the PDK fill generator, see [scripts/add_logo_fill.sh](../../scripts/add_logo_fill.sh) |
| `Magic.StreamOut`, `KLayout.XOR`, `Checker.XOR` | Magic cannot read the OpenRAM SRAM GDS |
| `OpenROAD.IRDropReport`, `Checker.PowerGridViolations` | the pad ring connects its supply buses by abutment, which the analysis does not follow |
| `Checker.LVS` | four ring bus nets of the clock pad do not match for the same reason, the report is kept |
| `Checker.IllegalOverlap` | Magic reports overlaps of the pad cells that are by design |

Each one carries the full reason in [flow/librelane/config.yaml](../../flow/librelane/config.yaml). Read that file before switching one back on.

## Useful variables of this configuration

| Variable | Value here | Effect |
| --- | --- | --- |
| `PAD_SPACING_MULTIPLE` | 2 | the pad to pad gap is floored to this multiple, which decides whether the row ends on the site grid |
| `PAD_CFG` | `dir::pad_cfg.tcl` | a local copy of the pad ring script, here with terminal shapes on the supply bus pins |
| `PDN_CORE_RING_CONNECT_TO_PAD_LAYERS` | `[met3]` | the layer the core ring straps reach the pads on |
| `PDN_MACRO_CONNECTIONS` | five lines | every macro with `VDD` and `VSS` pins, the global connections only cover the standard cells |
| `MAGIC_GDS_FLATGLOB` | the OpenRAM subcells | flattens them for the Magic steps |
| `RSZ_DONT_TOUCH_LIST`, `DRT_ASSIGN_NDR` | the four analog nets | keeps the analog traces unbuffered and on the non-default rule |

# ngspice corners, mismatch and Monte Carlo in sky130A

What the model files of sky130A contain, which line selects what, and which runs are possible. Everything here was read out of the PDK of the IIC-OSIC-TOOLS 2026.08 image, open_pdks `026824c7`.

## One entry point

Every simulation pulls in one file and one section:

```spice
.lib $::SKYWATER_MODELS/sky130.lib.spice tt
```

`SKYWATER_MODELS` is set by the PDK `xschemrc` and points at `$PDK_ROOT/$PDK/libs.tech/combined`, the model tree open_pdks assembles. Outside Xschem, name the path:

```spice
.lib /foss/pdks/sky130A/libs.tech/ngspice/sky130.lib.spice tt
```

The two trees hold the same sections. `libs.tech/ngspice/` is the ngspice build, `libs.tech/combined/` is the one the Xschem variable points at.

`.option scale=1e-6` belongs with it in a hand-written deck: the sky130 device models take `W` and `L` in metres, and the Xschem symbols write them in micrometres.

## The sections

A section name has up to three parts: the MOS corner, the resistor and capacitor corner, and the mismatch flag.

| Part | Values | Meaning |
| --- | --- | --- |
| MOS corner | `tt`, `ss`, `ff`, `sf`, `fs` | typical, slow, fast, slow nmos with fast pmos, fast nmos with slow pmos |
| RC corner | omitted, `hh`, `hl`, `lh`, `ll` | resistance and capacitance high or low, in that order, omitted means typical |
| Mismatch | omitted or `_mm` | device to device mismatch off or on |

That gives the 52 sections the library defines, for example:

| Section | MOS | Resistors and capacitors | Mismatch |
| --- | --- | --- | --- |
| `tt` | typical | typical | off |
| `ss` | slow | typical | off |
| `tt_mm` | typical | typical | on |
| `ss_hh` | slow | high R, high C | off |
| `ff_ll_mm` | fast | low R, low C | on |
| `hh` | typical | high R, high C | off |
| `mc` | typical plus process variation | typical | off |

Unlike the IHP libraries, the RC corner is not a separate `.lib` line: it is part of the section name. One `.lib` line per simulation is all it takes, and a corner sweep is a sweep over section names.

List them all:

```sh
grep -o '^\.lib [a-z_0-9]*' $PDK_ROOT/$PDK/libs.tech/ngspice/sky130.lib.spice | sort -u
```

## What a section does

Every section sets two parameters and includes three groups of files:

```spice
.lib tt
.param mc_mm_switch=0
.param mc_pr_switch=0
.include "corners/tt.spice"                         MOSFETs
.include "r+c/res_typical__cap_typical.spice"       resistors and capacitors
.include "r+c/res_typical__cap_typical__lin.spice"
.include "corners/tt/specialized_cells.spice"       SRAM and flash cells
.endl tt
```

| Parameter | 0 | 1 | Set by |
| --- | --- | --- | --- |
| `mc_mm_switch` | no mismatch | mismatch on | the `_mm` sections |
| `mc_pr_switch` | no process variation | process variation on | the `mc` section |

Both are plain `.param` values, so a deck can override them after the `.lib` line. That is how this template runs its Monte Carlo, see below.

## Mismatch

The `_mm` sections switch on the mismatch models of the device families that have them. The models are in `libs.ref/sky130_fd_pr/spice/*__mismatch.corner.spice`, one file per device, and they are slopes on the BSIM parameters, for example for `nfet_01v8`:

```spice
.param sky130_fd_pr__nfet_01v8__toxe_slope=3.443e-03
.param sky130_fd_pr__nfet_01v8__lint_slope=0.0
.param sky130_fd_pr__nfet_01v8__nfactor_slope=0.0
.param sky130_fd_pr__nfet_01v8__voff_slope=0.007
.param sky130_fd_pr__nfet_01v8__vth0_slope=3.356e-03
```

The slope scales with the device area, so a wide, long device mismatches less. Which families have mismatch data:

```sh
ls $PDK_ROOT/$PDK/libs.ref/sky130_fd_pr/spice/ | grep mismatch
```

In the 2026.08 PDK that is 28 files: the 1.8 V core FETs and their low and high threshold flavours, the 5 V thick oxide FETs, the native FETs, the RF FETs and the flash and SRAM cells. Resistors, capacitors, diodes and bipolars have no mismatch model here, a mismatch run leaves them at their nominal value.

A mismatch run is a Monte Carlo over the mismatch models only, so it needs a repeated analysis:

```spice
.lib $::SKYWATER_MODELS/sky130.lib.spice tt_mm
.control
  let run = 0
  dowhile run < 200
    reset
    run
    ...
    let run = run + 1
  end
.endc
```

CACE does that repetition for you, see `ac_mm_params` in [macros/inverter/verification/cace/inverter.yaml](../../macros/inverter/verification/cace/inverter.yaml).

## Process variation

The `mc` section is different from the corner sections: it sets `mc_pr_switch=1` and includes `parameters/critical.spice` and `parameters/montecarlo.spice`, which redefine the process parameters as functions of a set of random variables. It does not include a MOS corner, so it cannot be stacked on top of one: reading `.lib ... mc` after `.lib ... tt` redefines the models.

The practical way to combine a corner with process variation is to keep the corner section and set the switch afterwards:

```spice
.lib $::SKYWATER_MODELS/sky130.lib.spice tt
.param mc_pr_switch=1
```

That is what the CACE datasheet of the inverter does, through its `mc_pr` condition. The parameter reaches the model equations, which scale the critical dimensions and the oxide thickness with it, and every `reset` draws a new set.

## Which run for which question

| Question | Section | Extra |
| --- | --- | --- |
| Does it work at the nominal corner? | `tt` | - |
| Does it work over process and RC corners? | `tt`, `ss`, `ff`, `sf`, `fs`, with `hh`, `hl`, `lh`, `ll` where the parasitics matter | sweep the section name |
| How much does device to device mismatch cost? | `tt_mm` | repeat the analysis, 100 to 1000 runs |
| How much does lot to lot process variation cost? | `tt` plus `.param mc_pr_switch=1` | repeat the analysis |
| Both at once? | `tt_mm` plus `.param mc_pr_switch=1` | repeat the analysis |

Temperature is not part of the section name, `.temp` is a separate statement, and supply variation is a parameter of the testbench.

## Differences from the IHP libraries

Readers coming from the sibling templates will notice:

| IHP SG13G2 | sky130A |
| --- | --- |
| one `.lib` line per device family (`cornerMOSlv.lib`, `cornerRES.lib`, `cornerCAP.lib`, ...) | one `.lib` line for everything |
| `mos_tt`, `res_typ`, `cap_typ` section names | `tt`, and the RC corner is part of the name |
| `mm_ok=1` on the device instance to enable its mismatch | no instance parameter, the `_mm` section switches every device that has data |
| `num_sigmas` on the instance | fixed slopes in the mismatch models |
| statistical corners in separate files | `mc` section and two switches |

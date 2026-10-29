# ngspice corners, mismatch and Monte Carlo in sky130A

What the model files of sky130A contain, which line selects what, and which runs are possible. The library structure was read in IIC-OSIC-TOOLS 2026.08, open_pdks `026824c7`.
The statistical selection and precision-poly mismatch were checked again with ngspice 47 in image 2026.10 on 2026-10-29.

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

The installed `all.spice` and `parameters/montecarlo.spice` set `.option scale=1.0u`.
The Xschem symbols therefore write `W` and `L` as numbers in micrometres.
A handwritten deck using the full library inherits this setting, so do not also add an SI suffix to those geometry values.

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
| `mc` | statistical process models | statistical process models | off |

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

In the 2026.08 PDK that is 28 files: the 1.8 V core FETs and their low and high threshold flavours, the 5 V thick oxide FETs, the native FETs, the RF FETs and the flash and SRAM cells. This filename list is not an inventory of all mismatch behavior.
Precision-poly resistor wrappers contain their own MC_MM_SWITCH-gated AGAUSS expressions, including body and end resistance mismatch.
The 1.41 um and 5.73 um high-poly families both varied in the measured control.
Inspect and probe other passive and bipolar families individually before claiming whether they have mismatch.

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

Selecting a corner and changing only the process switch does not load the statistical parameter definitions.
The measured `tt` plus `mc_pr_switch=1` control was identical to deterministic `tt` for all eight seeds.
Use the statistical section:

```spice
.lib $::SKYWATER_MODELS/sky130.lib.spice mc
```

For process variation together with local mismatch, select `mc` once and then set `.param mc_mm_switch=1`.
Do not stack a deterministic corner section with `mc`.
The inverter's `ac_mc_params` CACE test now selects `mc`.
Its previous `tt` selection with only the process switch enabled did not exercise process variation.

## Which run for which question

| Question | Section | Extra |
| --- | --- | --- |
| Does it work at the nominal corner? | `tt` | - |
| Does it work over process and RC corners? | `tt`, `ss`, `ff`, `sf`, `fs`, with `hh`, `hl`, `lh`, `ll` where the parasitics matter | sweep the section name |
| How much does device to device mismatch cost? | `tt_mm` | repeat the analysis, 100 to 1000 runs |
| How much does process variation cost? | `mc` | repeat the analysis |
| Both at once? | `mc` plus `.param mc_mm_switch=1` | repeat the analysis |

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

## Statistical activation controls

A 2026-10-29 control used two equal diode-connected low-threshold NMOS devices (W=20 um, L=0.5 um, nf=4, 80 uA each) and two equal L=10 um resistors from each high-poly family at 10 mV.
Each mode used eight independent seeds at 27 C.

| Selection | NMOS VGS sample standard deviation | Pair VGS difference sample standard deviation | 5.73 um resistor relative pair difference sample standard deviation |
| --- | ---: | ---: | ---: |
| `tt` | 0 | 0 | 0 |
| `tt` with process switch 1 | 0 | 0 | 0 |
| `tt_mm` | 1.905 mV | 2.160 mV | 0.4784% |
| `mc` | 6.542 mV | 0 | numerical roundoff |

The 1.41 um resistor pair difference had 0.8464% sample standard deviation with `tt_mm`.
These small controls establish model activation only, not a distribution, yield or foundry mismatch guarantee.

Both `mult` and `m` are present in the stock precision-poly Xschem symbol format.
For a 5.73 um resistor at L=1 um, `mult=2` alone measured the same 124.5 ohm as `mult=1`.
Using `mult=2 m=2` measured 62.26 ohm.
The wrapper's `mult` scales statistical area, while ngspice's instance `m` supplies electrical parallel copies.
Keep both when writing a netlist by hand.

## Inverter process Monte Carlo check

After changing the CACE selection to `mc`, all 200 schematic samples passed the existing limits of gain at least 0 dB and bandwidth at least 500 kHz.
At 1.8 V, input bias 0.9 V, 27 C and 10 pF load, gain spans 25.138 to 34.881 dB and bandwidth spans 689.573 kHz to 1.98538 MHz.
These are the corrected process-only results with ngspice 47 on 2026-10-29.
The generated samples are in [inverter_tb_ac.csv](../../macros/inverter/verification/cace/scripts/inverter_tb_ac.csv).

Reproduce with:

```sh
source .designinit
cd macros/inverter
../../scripts/with_sky130_ngspice.sh cace verification/cace/inverter.yaml -s schematic -p ac_mc_params -j 4
```

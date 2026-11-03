# SKY130 deterministic passive corners

The installed sky130.lib.spice sections tt, ff, ss, fs and sf all load res_typical__cap_typical.spice and its __lin companion.
Changing only the MOS section does not exercise resistor or capacitor extremes.
A datasheet parameter has no effect unless the netlist or an evaluation expression uses it.

The installed deterministic passive bundles are:

- res_typical__cap_typical
- res_low__cap_low
- res_low__cap_high
- res_high__cap_low
- res_high__cap_high

There is no supplied res_high__cap_typical or res_typical__cap_low file in this installation.
Use the supported complete bundles and record both names.
To choose a bundle independently of MOS speed, replace the aggregate .lib selection with its component includes, rather than loading both selections.

~~~spice
.param mc_mm_switch=0 mc_pr_switch=0
.include /foss/pdks/sky130A/libs.tech/ngspice/corners/tt.spice
.include /foss/pdks/sky130A/libs.tech/ngspice/r+c/res_high__cap_low.spice
.include /foss/pdks/sky130A/libs.tech/ngspice/r+c/res_high__cap_low__lin.spice
.include /foss/pdks/sky130A/libs.tech/ngspice/corners/tt/specialized_cells.spice
~~~

Select the same MOS name in both corners paths.
This is deterministic selection, not process or mismatch Monte Carlo.
The process and mismatch guide covers statistical activation separately.

## Measured control

After selecting sky130A, run:

~~~sh
python3 scripts/probe_sky_passive_corners.py --output verification/controls/sky_passive_corners.json
~~~

The script uses the committed ngspice runtime wrapper and verifies that explicit typical component includes reproduce the aggregate tt library.
It records the installed selection-file hashes.
Measured with ngspice 47 in IIC-OSIC-TOOLS 2026.10 at 27 C:

| Passive bundle | 5.73 um poly, L=1 um | 5.73 um poly, L=10 um | 5 by 5 um MIM |
|---|---:|---:|---:|
| typical/typical | 124.510 ohm | 632.650 ohm | 53.2822 fF |
| low/low | 93.138 ohm | 547.092 ohm | 45.4177 fF |
| low/high | 93.138 ohm | 547.092 ohm | 63.7270 fF |
| high/low | 155.882 ohm | 718.208 ohm | 43.4534 fF |
| high/high | 155.882 ohm | 718.208 ohm | 61.1145 fF |

The resistor is res_high_po_5p73 at 1 mV with its bulk grounded.
The capacitor is cap_mim_m3_1 at 0.75 V and 1 MHz.
The short resistor varies by about 25.2 percent, while the longer resistor varies by about 13.5 percent.
Do not represent every resistor geometry with one percentage scale.

The capacitor value also differs between resistor-low and resistor-high bundles with the same capacitor label.
Its model derives effective dimensions from m3_dw and tol_m3, so the complete RC bundle matters.
The listed capacitor extremes are not an independent change of one area-capacitance coefficient.

These controls validate model selection and primitive responses.
A circuit still needs its own passive-corner, statistical and extracted verification.

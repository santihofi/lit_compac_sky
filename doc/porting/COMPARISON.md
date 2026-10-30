# IHP SG13CMOS5L versus SKY130A

This report is incremental.
Initial SKY130 schematic results are measured below. No schematic equivalence or physical signoff is established yet.

## Comparison protocol

Use identical input amplitudes, common-mode references, loads and definitions, with the original 1.45 to 1.65 V supply range as the primary comparison.
Record a separate 1.8 V case if evaluated.
Separate deterministic corners, local mismatch and global process statistics.
Read simulator validity and waveform capture in addition to spec pass flags.
The reference design is pinned in evidence/provenance.json.

## Reproduced IHP reference

Measured with Chipify 0.2.3 from local source commit 1960c81 and the image's ngspice 47.
The current cell uses 59.7/0.28 um PMOS inputs, 20/0.5 um NMOS quad devices and an eightfold tail mirror.
The supplied bench's 40 uA reference therefore represents approximately 320 uA in the core tail.
Older results for a smaller 40 uA-tail cell must not be treated as this revision's bandwidth or mismatch results.

| Metric | IHP measured, schematic | SKY130 |
|---|---:|---:|
| Supply and temperature | 1.5 V, 27 C | 1.5 V, 27 C |
| Gain at four quadrant 100 mV inputs | -10.0387 V^-1 | -5.90626 V^-1 |
| Gain at four quadrant 10 mV inputs | -9.85739 V^-1 | -5.51704 V^-1 |
| Gain ratio, 100 mV / 10 mV | 1.01839 | 1.07055 |
| First-input-only gain ratio | 0.977262 | 1.03263 |
| Second-input-only gain ratio | 1.04751 | 1.04992 |
| Differential output at +100 mV, +100 mV | -100.387 mV | -59.0626 mV |
| Output common mode | 757.967 mV | 753.017 mV |
| Deterministic balanced output offset | -2.76e-13 V | Pending |

The nominal scalar table has no min/max limits, so its reported 100 percent yield means valid capture only.
It is not an equivalence or signoff verdict.
Full scalar values and the generated reference netlist template are retained under evidence/.

## Required remaining sections

Primitive mapping and model scope, resistor voltage/temperature coefficients, BJT choice, geometry and finger semantics, schematic sizing rationale, PVT and trim coverage, mismatch controls, loop stability, startup, noise, bandwidth, power, physical area, DRC/LVS, extraction and tree-level results remain to be measured.

## Current IHP schematic across corners

The 135-case reproduction sweeps five MOS corners, three resistor corners, supplies 1.45/1.5/1.65 V and temperatures 0/27/80 C.
All 135 rows, 1350 scalar values and 135 waveform files passed the independent data audit.
With gain code 13 fixed, K100 ranges from -12.4175 to -7.25745 V^-1, gain ratio from 1.00508 to 1.03242, and common mode from 756.207 to 763.491 mV.
These are measured ranges, not an all-corner K=10 guarantee.

The separately reproduced nominal bandgap gives 910.440 mV and 3.81681 uA per line.
The sixteen-channel bias distribution gives 749.512 mV common-mode reference, 800.159 mV output bias, 40.3056 uA cell reference and 40.2441 uA CMFB reference.
The nominal tile draws 1086.76 uA in its stated bench.
The current IHP mult_cell bandwidth bench reports 254.451 to 354.517 MHz across its four path/loading combinations, with code 14 giving K = 10.0243 V^-1.
These bandwidth figures replace the earlier small-cell bandwidth as the current comparison target.

## SKY130 primitive and headroom findings

For an isolated diode-connected 20/0.5 um NMOS with four fingers at 80 uA, VGS is 732.2 mV for the standard device and 620.2 mV for the low-threshold device.
For a 74.625/0.35 um PMOS with twelve fingers at 160 uA, |VGS| is 1.070 V standard and 474.3 mV low threshold.
These primitive probes have no extracted interconnect and are sizing measurements, not complete operating-range guarantees.

The first low-threshold mapping has -71.8 mV of NMOS folding-mirror saturation margin at balance.
Increasing VDD to 1.8 V while keeping the input common mode at 0.75 V does not solve this internal voltage budget.
The relevant voltage is available between ground and the quad source, which the input common mode and quad VGS determine.
A fourfold mirror width and twofold input-pair width restore nominal gain to -9.97492 V^-1 with ratio 0.988612, but leave only 7.0 mV of mirror margin.
That point is rejected as a qualified sizing choice.
A second sweep trades mirror length and width against headroom and linearity.
Even a nominal match is held from layout until PVT, bandwidth, noise and loop checks pass.

## Resistor and connectivity mapping

The IHP nominal trim segment is about 56.64 ohm after its two parallel copies.
A 5.73 um SKY130 precision-poly resistor measures 96.28 ohm at L=0.5 um and 124.51 ohm at L=1 um before parallel copies.
Its nominal low-voltage relation is approximately 68.05 + 56.46 L ohm, with L in um.
The 1.41 um family has a different end-voltage expression, including a shifted voltage argument.
Its short devices cannot be sized by sheet resistance alone.
These observations drove separate mappings for short trim segments and long reference resistors.

A netlist audit checked the terminal connectivity of 103 MOS and resistor instances across the core, trim ladder and CMFB.
Four resistor bulk connections change intentionally from the IHP n-well tie to the SKY130 substrate tie.
The audit does not establish layout connectivity or extracted performance.
Tap ties use a 1 milliohm simulation abstraction with LVS short semantics, since an ideal voltage source can form a forbidden loop when the parent already ties both tap ports together.

## Flow changes and publishing status

The SKY130 template runtime wrapper is committed as 8c39e53 on work-santi.
Its inverter DC result is unchanged at vgsp_at_vcm = 0.9071777 V.
The startup probe verifies that the intended SKY130 optimization setting becomes active even when Chipify launches ngspice from a scratch directory.
GitHub rejected the template push for lack of write access.
The destination design repository still needs a remote.

## Bandwidth and sizing tradeoffs at identical load

A separate bare-core comparison uses the same 100 fF load on each output, 1.5 V supply, 0.75 V input and output references, and one input fixed at 100 mV while the other receives the small-signal AC stimulus.
The IHP reference gives 426.673 MHz on input 1 and 836.155 MHz on input 2, with 718.416 uA supply current.
This is a different load from the current mult_cell bench's next-stage inputs and output buffer.

The first SKY130 speed sweep used folding mirrors of L=0.15 or 0.25 um.
Its 24 points were valid, but K100/K10 ranged from 0.836181 to 0.902001.
Bandwidth alone therefore cannot select the port.
A second 24-point sweep used 0.5 or 1.25 um folding mirrors and smaller quad devices.
One point, mirror W=80 um L=0.5 um, quad W=10 um L=0.15 um, pair W=74.625 um L=0.35 um, reaches K100=-9.45796, ratio 0.978145 and bandwidth 487.322/787.450 MHz.
Its 14.660 mV mirror margin remains too small to accept without corner checks.
Longer 1.25 um mirrors improve some curvature points but lower input-1 bandwidth to 149 to 254 MHz.
Parallel circuit scaling and resistor adjustment remain exploratory, with no accepted final sizing.

## Statistical model controls

Thirty-two primitive cases separate deterministic models, local mismatch and global process variation.
Eight seeds of tt with mc_pr_switch=1 gave exactly the same measured values as deterministic tt.
The mc section gave 6.542 mV sample standard deviation in the diode-connected LVT NMOS VGS, while the difference between equal devices stayed zero.
The tt_mm section gave 2.160 mV standard deviation in the pair difference.
Both precision-poly families have local mismatch in their wrapper models, contrary to the earlier template guide.
At L=10 um the eight-seed relative pair-difference standard deviations are 0.4784% for 5.73 um and 0.8464% for 1.41 um resistors.
These controls establish model activation, not reliable spread or yield estimates.

The template guide and inverter CACE process selection were corrected.
A 200-sample process-only inverter run using mc passed its existing limits, with gain 25.138 to 34.881 dB and bandwidth 689.573 kHz to 1.98538 MHz.
The primitive controls are also provided as a reusable Chipify project in testbenches/chipify/sky_statistics.

## Corner rejection and next device choice

Parallel copies at constant device voltage and inversely scaled resistance improve bandwidth under the fixed 100 fF external load.
At mirror scale 6, pair scale 0.75, 10/0.15 um LVT quad, resistor scale 1.1 and two parallel copies, the measured gain is -9.76893 V^-1, ratio 0.980359, bandwidth 459.448/1070.30 MHz and supply current 1.225 mA.
This is an exploratory nominal result.

![Nominal schematic tradeoffs](figures/core_tradeoffs.png)

The following 45-case check used resistor scale 1.14 and swept five MOS corners, three supplies and three temperatures.
All 720 scalar captures were valid.
Only 20 cases met the provisional checks: positive tail and mirror saturation margins and a gain ratio between 0.96758 and 1.03242.
This provisional ratio window uses the maximum magnitude of the reproduced IHP corner deviation from unity, and does not replace matched-corner or full transfer-surface comparisons.
The candidate is rejected.
At the fs corner, mirror margin reaches -35.66 mV and gain ratio reaches 1.19769.
At sf, tail margin reaches -52.98 mV.
The fixed-current all-LVT mapping therefore cannot be accepted from its nominal gain and bandwidth.

![All-LVT candidate corner rejection](figures/candidate_corners.png)

Tying the quad body to its source buys only about 10 to 20 mV in the tested points, before any well parasitics.
The native 3.3 V NMOS quad gives 353 to 523 mV nominal mirror margin in the first four valid geometry probes, but needs more width to recover gain.
These are schematic alternatives, not selected physical implementations.
The first native sweep failed because 5 um fingers fell outside all nine model bins.
The corrected probes use supported 4 um fingers at L=0.5 um, as described in [the geometry guide](../sky130A-Open-PDK/device-model-geometry.md).

## Skew-corner interpretation and native-quad rejection

The SKY130 device probes show sf means fast NMOS and slow PMOS in the installed models, while fs means slow NMOS and fast PMOS.
This reverses the IHP library's documented transistor order.
Semantic cross-process comparisons therefore map IHP mos_sf to SKY130 fs and IHP mos_fs to SKY130 sf.
Raw evidence keeps each PDK's own labels.

The 45-case IHP bare-core bandwidth sweep gives 379.086 to 456.491 MHz on input 1 and 800.967 to 864.774 MHz on input 2.
Its tail margin reaches -17.9 mV at a few low-supply points while the measured gain remains well behaved.
A zero-margin screen is therefore conservative and cannot serve as the sole equivalence criterion.
The saturation indicators also come from different compact models.

The native-quad candidate has positive folding-mirror margin, but its quad margin reaches -84.4 mV at the SKY130 sf corner.
A native transistor's gate and drain at the same common-mode voltage do not guarantee saturation.
Across the 45 cases its gain magnitude spans 2.3803 to 14.6000 V^-1.
The native substitution is rejected for equivalent transfer behavior, despite the large mirror margin.
The next candidate uses modeled source-degeneration resistors with wider LVT quad and tail devices.

## Source degeneration, noise and common-mode feedback

The four-copy source-degeneration candidate uses 60 ohm effective source resistors in each LVT quad arm, implemented by four parallel res_high_po_5p73 devices rather than ideal resistors.
Its unit dimensions are 120/0.5 um folding mirrors, 149.25/0.35 um input devices and 40/0.15 um quad devices.
Doubling the tail mirror width improves tail headroom.
At tt, 27 C, 1.5 V, code 13 and 100 fF per output, K100 is -9.99565 V^-1, K100/K10 is 1.01218, bandwidth is 474.822/1119.29 MHz and supply current is 2.611 mA.
The IHP bare core draws 0.718416 mA under the same bias and load definition.
The SKY130 candidate therefore costs about 3.63 times the bare-core current.

All 45 MOS/supply/temperature cases produce valid measurements.
Only 23 meet the provisional 0.96758 to 1.03242 gain-ratio window.
The ff and fs corners show expansion, with fs reaching 1.1123, while ss can compress to 0.9511.
The fs folding-mirror margin reaches -5.9 mV.
This candidate is not accepted as an equivalent port.

Matching nominal noise benches hold one input at 100 mV differential and measure noise referred to the other input.
Both integrate from 1 kHz to 100 MHz and use the same 100 fF output loads.

| Nominal schematic metric | Current IHP | SKY130 degeneration candidate |
|---|---:|---:|
| Input-1 noise at 1 MHz | 20.3362 nV/sqrt(Hz) | 7.79333 nV/sqrt(Hz) |
| Input-2 noise at 1 MHz | 20.3247 nV/sqrt(Hz) | 6.58537 nV/sqrt(Hz) |
| Input-1 integrated noise | 149.052 uVrms | 74.9687 uVrms |
| Input-2 integrated noise | 146.311 uVrms | 63.4849 uVrms |
| CMFB phase margin | 60.5671 degrees | 47.6232 degrees |
| CMFB gain margin | 18.0002 dB | 9.59422 dB |
| CMFB unity frequency | 14.4654 MHz | 18.3655 MHz |

These are schematic nominal measurements, not mismatch, PEX or loaded-tree results.
The noise source must have an AC magnitude of one or ngspice cannot compute the input-referred quantity.
The initial missing-AC bench was corrected before retaining these values.
The SKY130 common-mode loop fails the 10 dB minimum gain margin.
Increasing only the fast-loop degeneration resistance worsened phase margin, reaching 26.65 degrees at three times the mapped resistance and 100 fF load.
The next compensation experiment separates the slow integrating loop with a larger gate capacitor before tuning the fast-loop resistance.

Evidence: `evidence/ihp_core_noise.csv`, `evidence/ihp_core_stability.csv`, `evidence/sky_degenerated_noise.csv`, `evidence/sky_degenerated_stability.csv` and `evidence/sky_degenerated_corners.csv`.
The independent corner audit distinguishes valid data from failed specifications.

# IHP SG13CMOS5L versus SKY130A

This report is incremental.
The transistor-replica version of the compact two-copy candidate passes all 45 original-range diagonal-curvature cases with fixed per-corner current codes.
Its nominal full-surface error is below the IHP reference.
All 45 bandwidth captures and both sets of 45 feedback-loop captures pass the independent waveform audit.
The two feedback loops meet their provisional margin limits.
Fifteen full transfer surfaces at 1.5 V show lower peak error than IHP in every matched MOS/temperature case, with three RMS-error regressions.
No schematic equivalence or physical signoff is established.
The latest measured checkpoint is summarized first, with the earlier candidates retained below to explain the sizing decisions.

## Current transistor-replica checkpoint

The following nominal results use tt, 27 C, 1.5 V, common mode 0.75 V, gain code 13 and 100 fF per output.
IHP uses a 40 uA unit reference.
SKY130 uses two parallel circuit copies, 0.35 um PMOS loads, resistance scale 1.46 and 33.75 uA unit reference.
The full operating range remains 1.45/1.5/1.65 V and 0/27/80 C.

| Metric | Current IHP core | SKY130 transistor-replica candidate |
|---|---:|---:|
| Fitted product gain | -10.00640 V^-1 | -9.97783 V^-1 |
| Peak fitted transfer error | 1.38043% | 1.02346% |
| RMS fitted transfer error | 0.48130% | 0.39973% |
| Bare-core bandwidth, inputs 1/2 | 426.673/836.155 MHz | 592.706/845.691 MHz |
| Input capacitance per pin at 1 MHz, inputs 1/2 | 171.090/131.584 fF | 185.419/83.8715 fF |
| Input noise at 1 MHz, inputs 1/2 | 20.3362/20.3247 nV/sqrt(Hz) | 16.8151/14.2876 nV/sqrt(Hz) |
| Integrated input noise, 1 kHz to 100 MHz | 149.052/146.311 uVrms | 149.314/124.668 uVrms |
| CMFB phase margin | 60.5671 degrees | 101.600 degrees |
| CMFB gain margin | 18.0002 dB | 14.3740 dB |
| Supply current | 0.718416 mA | about 1.199 mA |

Noise uses the other differential input held at 100 mV.
The first-input integrated noise is essentially unchanged, and the CMFB gain margin remains lower.
The replica adds about 12.5 percent to input-1 capacitance relative to the preceding compact candidate.
Its local bias loop has nominal phase margin 85.9634 degrees and gain margin 33.0437 dB.
The loop bench breaks the shared gate connection so both the reference and main tail gate loads remain present.
The small nominal input-2 bandwidth advantage still needs extracted confirmation.
These measurements do not qualify mismatch, startup, actual bias circuitry or physical layout.

![Transistor-replica candidate transfer and fitted residual](figures/sky_replica_transfer.png)

## Replica feedback and bandwidth across PVT

All runs retain one fixed current code per raw SKY130 MOS corner, with supplies 1.45/1.5/1.65 V and temperatures 0/27/80 C.
The feedback-loop measurements use ideal input common-mode, output common-mode and bias references.
Their exported complex return ratios independently reproduce the scalar margins and crossing counts.

| Measurement | Minimum over 45 cases | Maximum over 45 cases |
|---|---:|---:|
| Input-1 bandwidth | 478.294 MHz | 655.962 MHz |
| Input-2 bandwidth | 693.129 MHz | 1077.460 MHz |
| Input-1 capacitance per pin | 146.738 fF | 223.750 fF |
| Input-2 capacitance per pin | 74.7499 fF | 94.0107 fF |
| CMFB phase margin | 81.6713 degrees | 111.164 degrees |
| CMFB gain margin | 14.1532 dB | 15.5771 dB |
| Replica-bias phase margin | 85.7102 degrees | 92.5843 degrees |
| Replica-bias gain margin | 32.5053 dB | 38.7649 dB |

Every loop capture has exactly one unity crossing.
The 90 core gain curves were checked against separately captured DC-frequency gain and 3 dB bandwidth.
The 90 loop curves were checked against phase margin, gain margin, unity frequency, phase-crossing frequency, DC gain and crossing count.
Frozen scalar tables, waveform archives and audits carry the sky_replica_ac_pvt, sky_replica_cmfb_pvt and sky_replica_bias_loop_pvt prefixes in evidence/.

The earlier IHP bare-core PVT bandwidth spans 379.086 to 456.491 MHz on input 1 and 800.967 to 864.774 MHz on input 2.
The SKY130 input-2 minimum remains below that IHP range.
This is not full-range performance equivalence.
The comparison also retains fixed gain code 13, so gain normalization and actual DAC/reference impedance remain separate checks.


## Replica receiver loading and corner surface shape

A driver feeds input 1 or input 2 of an identical receiver core with its own CMFB loop and bias.
The receiver's other differential input is held at 100 mV and its output load is 100 fF per pin.
The table gives driver bandwidth, with 25/50 fF added per driver output as a wire-capacitance proxy.
Both designs use nominal conditions and gain code 13.
The load excludes the offset DAC and tile output buffer.

| Receiver input | Wire load per output | IHP driver BW, inputs 1/2 | Replica driver BW, inputs 1/2 |
|---|---:|---:|---:|
| 1 | 25 fF | 331.819/511.728 MHz | 449.019/566.773 MHz |
| 2 | 25 fF | 373.239/612.754 MHz | 578.295/813.008 MHz |
| 1 | 50 fF | 315.648/463.835 MHz | 425.050/528.008 MHz |
| 2 | 50 fF | 352.942/548.314 MHz | 541.655/735.518 MHz |

All eight nominal bandwidth comparisons improve over IHP despite the replica's extra input-1 capacitance.
These are transistor receiver loads, not extracted tree interconnect.

The matched full-surface grid covers five MOS corners and 0/27/80 C at 1.5 V only.
Each case uses all 1681 input pairs from -100 to +100 mV in 5 mV steps.
A constant, two feedthrough terms and the product term are fitted independently, and shape error is normalized to that case's fitted full scale.
The SKY130 and IHP skew labels are reversed before matching N/P speed cases.

SKY130 peak residual spans 0.827867 to 1.530329 percent, versus IHP's 1.118381 to 1.587047 percent.
Every one of the fifteen matched cases has lower peak residual on SKY130.
RMS residual improves in twelve cases but worsens at all three temperatures of the N-fast/P-slow corner.
The worst RMS comparison is SKY130 sf at 0 C, 0.617139 percent versus IHP fs at 0 C, 0.540532 percent.
Thus lower peak error does not imply uniformly lower distortion over the full input square.
Supply-extreme full surfaces, gain-trim coverage, mismatch and real bias references remain open.

![Matched corner surface residual ratios](figures/replica_ihp_matched_surfaces.png)

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

| Metric | IHP measured, schematic | Initial SKY130 mapping |
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

## Remaining qualification

Core sizing and bias must first meet the original-range corner requirements.
Complete the real current DAC and voltage references, output stage, bandgap, mismatch qualification, startup and tree-level stability.
Python-generated layout, physical area, DRC/LVS and extracted performance follow schematic qualification.
The measurements below cover primitive mapping, candidate sizing, nominal noise and loop gain, input loading, transfer surfaces and several rejected PVT families.

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

## Full transfer surface and separate input curvature

The nominal transfer surfaces contain all 1681 combinations of input differentials from -100 to +100 mV in 5 mV steps.
A least-squares fit uses constant, input-1 feedthrough, input-2 feedthrough and product terms.
Residuals are normalized by the fitted product gain times 0.01 V^2, so gain error and shape error remain distinct.

| Nominal fitted metric | IHP current core | SKY130 degeneration candidate |
|---|---:|---:|
| Product gain | -10.0064 V^-1 | -10.0853 V^-1 |
| Peak residual | 1.38132 mV | 2.36880 mV |
| Peak residual / fitted full scale | 1.38043% | 2.34877% |
| RMS residual / fitted full scale | 0.48130% | 0.82899% |

![IHP full transfer surface](figures/ihp_core_transfer.png)

![SKY130 candidate full transfer surface](figures/sky_degenerated_transfer.png)

The SKY130 candidate's combined gain ratio of 1.01218 hides opposing errors on its two axes.
Holding input 2 at 10 mV, increasing input 1 from 10 to 100 mV changes normalized gain from -9.87541 to -9.47623 V^-1.
Holding input 1 at 10 mV, increasing input 2 to 100 mV instead gives -10.74152 V^-1.
A further 120-case sizing sweep therefore measures each axis separately.
No configuration in that sweep keeps combined gain curvature within the provisional corner window, even at fixed 27 C and 1.5 V.
Its best worst-corner deviation is 4.936%.
The next experiment widens the quad further while reducing input-pair transconductance.

## Loop compensation and DC convergence controls

Increasing the slow-loop MOS capacitor to sixteen times its mapped multiplicity, with fast-loop resistance scaled by 1.5, gives 71.5876 degrees phase margin and 10.5120 dB gain margin at 100 fF.
The nominal 30 fF result is 70.7993 degrees and 10.3237 dB.
This is a compensation experiment, with additional area and settling cost still to evaluate.
A current-kick bench uses trapezoidal integration and checks both 100 ps and 50 ps maximum steps.

The original dense SKY130 DC surface timed out after 600 seconds.
An eleven-point control compared unchanged circuit outputs with alternate solver settings.
Adding 1e12 ohm shunts alone changed output voltages by at most 45 nV but did not remove repeated gmin recovery.
Adding initial guesses on the two outputs, load-gate bias and integrator node removed recovery in that control, with at most 49 nV difference from the original result.
The full 1681-point surface then completed in 58.27 seconds.
These numerical aids are explicit in the generated transfer bench.
They are initial guesses and weak conductances, not forced node voltages.

KLU aborted the same control with no DC data despite returning exit code zero.
It is not selected for these benches.
The audit checks waveform completeness and finite values independently of the simulator exit code.
Evidence and the reproducible control are `evidence/sky_dc_solver_probe.json` and `scripts/probe_sky_dc_solver.py`.

## Matched-skew corner comparison

![Matched transistor-skew comparison](figures/matched_corner_comparison.png)

Each bar spans the nine combinations of supply and temperature for one transistor skew.
IHP and SKY130 skew corners are paired by NMOS/PMOS behavior, not by the literal sf/fs strings.
The SKY130 candidate improves nominal noise and some bandwidth values, but uses more current and has larger transfer error.
It remains a rejected schematic candidate.

## Compensation cost and large-signal recovery

An 80 uA, 20 ns current pulse into the load-gate bias drives the candidate close to the supply rail in common mode.
At fast-loop resistance scale 1.5, the original integrating capacitor settles within 1 mV about 199.9 ns after the pulse ends.
The sixteenfold capacitor does not settle within 1 mV before the 1 us simulation ends.
Its maximum error between 900 ns and 1 us is 1.65098 mV.
Repeating with 50 ps instead of 100 ps maximum steps gives 1.65090 mV.
This is a settling penalty rather than evidence that the larger capacitor is a complete fix.

![Common-mode current-kick recovery](figures/sky_cmfb_kick.png)

Scaling the entire fast OTA by four, with reciprocal resistor scaling and the slow loop unchanged, improves nominal margins to 83.1195 degrees and 14.7666 dB with capacitor scale four.
Supply current rises from 2.611 to 3.319 mA.
Shortening both PMOS load and mirror-master devices to 0.35 um while preserving their W/L gives 118.826 degrees and 14.9866 dB at resistance scale one, with current 2.608 mA.
That geometry change requires new transfer, mismatch and corner checks.
It is not included in the previously reported transfer or noise candidate.

The transient audit was corrected to use Chipify's transient metadata key and legacy tran_dir fallback.
All eight traces are finite and reach 1 us.
Missing-waveform and nonfinite-sample controls are rejected.
The complete traces are retained in evidence/sky_cmfb_kick_waveforms.npz.

## Bias calibration experiment at the original supply

A wider quad improves voltage margin but does not remove process-dependent curvature at a single fixed bias.
A fifteen-case current sweep shows that bias can tune curvature substantially.
The following nominal experiment keeps 1.5 V and 0.75 V common mode, uses a 4x quad-width scale, 0.5x input-pair scale, 0.3 um folding mirrors, four circuit copies and 180 ohm unit degeneration resistors.
The effective source resistance is one quarter of the unit value.
Load resistance scale is 1.3.

The ideal reference currents are quantized to (21 + code) times 1.25 uA per circuit copy.
The codes for ff, fs, sf, ss and tt are respectively 3, 11, 12, 30 and 12.
This retains a five-bit code but changes the current-DAC unit from the IHP schematic's approximately 0.95 uA, before the fourfold circuit scaling.
No SKY130 DAC implementation is claimed by this ideal-source experiment.

| SKY130 corner at 27 C | Unit reference current | K100 | K100/K10 |
|---|---:|---:|---:|
| ff | 30.00 uA | -8.98496 V^-1 | 1.02141 |
| fs | 40.00 uA | -9.48636 V^-1 | 1.01437 |
| sf | 41.25 uA | -8.81761 V^-1 | 1.02346 |
| ss | 63.75 uA | -9.93479 V^-1 | 1.02076 |
| tt | 41.25 uA | -9.74103 V^-1 | 1.01800 |

All five pass the provisional diagonal ratio window.
Input-axis curvature, full surfaces, current-source temperature dependence, trim coverage, real bias circuitry and loaded bandwidth still determine acceptance.
The completed original-range sweep and its failures are reported below.

## Separate 1.8 V and 0.9 V common-mode alternative

Raising both supply and signal common mode enables a less aggressive undegenerated LVT core.
One two-copy nominal point uses 40/0.5 um folding mirrors, 20/0.5 um quad devices and the initial mapped input pair.
At load-resistance scale one it gives K100=-9.74012, ratio 0.983951, bandwidth 720.638/1008.690 MHz and supply current 1.379 mA.

With resistor scale 1.03, nominal gain becomes -9.99626 V^-1.
Eleven of fifteen MOS/temperature cases at 1.8 V meet the provisional ratio window.
The worst ratio is 0.932630 at sf and 0 C, so the higher common mode alone does not complete the port.
This experiment changes supply and common mode and is not mixed into equal-supply conclusions.

Differential AC admittance at 1 MHz gives nominal effective capacitance per input pin of 170.400/231.979 fF for this alternative.
The matching IHP measurement gives 171.090/131.584 fF.
The second input therefore loads a preceding stage more heavily even though the fixed-100-fF bare-core bandwidth is higher.
The next-stage transistor load must be included before accepting tree bandwidth.

## Calibrated-candidate follow-up on 2026-10-31

The nominal calibrated 1.5 V candidate gives a fitted product gain of -9.78082 V^-1.
Its full 1681-point transfer surface has 1.02711 percent peak residual and 0.39345 percent RMS residual, both below the IHP nominal values of 1.38043 and 0.48130 percent.
This is an improvement in nominal shape error, with gain still requiring trim.

The fixed per-corner bias settings pass 33 of 45 combinations of 1.45/1.5/1.65 V and 0/27/80 C.
The ss ratio spans 0.955037 to 1.06920 and sf spans 0.947973 to 1.06481.
At 1.45 V and 0 C, tail saturation indicators are -62.65 mV at ss and -41.48 mV at sf.
At 1.65 V they become positive and the same fixed currents produce expansion.
These results identify tail compliance as a remaining supply-sensitivity mechanism.
Nominal bias calibration is insufficient.

The follow-up experiment enlarges the PMOS input pair and adds modeled source resistors.
It recovers tail voltage but imposes the loading and bandwidth costs reported below.
It has not been promoted into the drawn prototype.

The separate higher-common-mode mirror sweep produces 30 valid cases, with 23 inside the provisional ratio window.
At mirror length 0.3 um the ratio spans 0.979283 to 1.04059.
It also remains unqualified.


## Pair-source degeneration trades compliance for input loading

The four-copy follow-up uses pair scale two, quad scale four, folding mirrors at scale eight and length 0.3 um, tail width scale four, load resistance scale 1.38 and unit pair/quad source resistances 240/180 ohm.
Actual source resistances are 60/45 ohm after parallel scaling.
Five-bit bias codes ff=0, fs=8, sf=5, ss=17 and tt=8 use the same ideal (21 + code) times 1.25 uA unit-current experiment.
The fixed currents pass 42 of 45 MOS/supply/temperature cases.

| SKY130 corner | Minimum K100/K10 | Maximum K100/K10 | Minimum tail indicator |
|---|---:|---:|---:|
| ff | 0.999810 | 1.03158 | 242.244 mV |
| fs | 1.00366 | 1.02525 | 237.206 mV |
| sf | 0.974835 | 1.04296 | 45.462 mV |
| ss | 0.980761 | 1.03454 | 36.359 mV |
| tt | 0.994579 | 1.03031 | 134.451 mV |

Every tail indicator is positive, yet three cases still fail the provisional curvature screen.
This separates the remaining temperature dependence from the earlier loss of tail compliance.
It does not establish full-surface accuracy across corners or a physical bias implementation.

The nominal input capacitances are 502.672/619.235 fF per pin at 1 MHz under symmetric differential drive, compared with IHP 171.090/131.584 fF.
The fixed-100-fF bandwidths are 366.019/624.410 MHz, compared with IHP 426.673/836.155 MHz.
Supply current is 2.31553 mA against IHP 0.718416 mA.
The large geometry therefore fails the speed comparison even before its heavier load is applied to a preceding stage.
Scaling circuit current and all device sizes together cannot remove intrinsic cascade loading.
The retained data are evidence/sky_pair_degenerated_pvt.csv, evidence/sky_pair_degenerated_ac.csv and the independent PVT audit.

## AC capture after repeated operating points

The initial compact sizing run produced finite scalar metrics but no requested AC traces in all eighteen cases.
Ngspice 47 names the first AC plot ac17 after seventeen retained operating-point plots.
Chipify 1960c81 injects setplot ac1 and cannot capture that run as declared.
The independent auditor rejected the output despite scalar pass flags.
The rejection record is evidence/sky_compact_capture_rejection.json.

The compact bench now saves scalar values as control variables and clears the old plots before AC.
This restores ac1/ac2 without changing the circuit.
scripts/probe_ngspice_plot_names.py reproduces the plot-name behavior in a PDK-independent RC circuit using the same runtime wrapper.

## Compact candidate speed recovery

After the capture correction, eighteen sizing cases and their AC traces pass the data-integrity audit.
Nine meet the diagonal curvature screen.
A follow-up shortens the core PMOS loads and the fast-OTA mirror devices at constant W/L.
All six nominal combinations of mirror length 0.25/0.3 um and PMOS load length 0.35/0.5/1 um produce valid data and meet that screen.

At mirror length 0.3 um and PMOS load length 0.35 um, the two-copy circuit gives K100=-9.51697 V^-1, ratio 1.01034, bandwidths 609.274/884.406 MHz, input capacitances 161.882/83.8877 fF and current 1.21753 mA.
These measurements use pair scale one, quad scale one, mirror scale four, tail width scale four, pair and quad unit resistors 120 ohm, load-resistance scale 1.38 and 40 uA unit bias.
This recovers nominal speed with input capacitance below the matched IHP values.
Gain, full transfer shape, corner coverage, feedback margins, noise and actual cascaded loading still require qualification.
The retained sweeps are evidence/sky_compact_pair_sizing.csv and evidence/sky_compact_load_sizing.csv.


## Compact candidate across supply and temperature

Five ideal fixed current codes ff=3, fs=2, sf=10, ss=14 and tt=11 use (21 + code) times 1.25 uA per copy.
All 45 cases and their 90 AC curves pass data-integrity and gain/bandwidth identity checks.
Thirty-six cases meet the provisional diagonal-ratio screen.
The sf range is 0.955138 to 1.04897, and ss is 0.959437 to 1.04788.
At the worst low-supply cold point, sf retains only 6.578 mV tail margin.
At fs the folding-mirror indicator reaches -0.111 mV and input-2 bandwidth falls to 690.072 MHz.
Positive tail indicators in the remaining failures show that nominal saturation alone does not establish supply-independent bias.
The results reject this candidate as a completed port.

The exported curves are independently checked against each run's scalar low-frequency gain and 3 dB crossing by scripts/check_core_ac_capture.py.
This catches wrong-plot capture even when every sample is finite.
The retained PVT audit covers all cases, and evidence/sky_compact_pvt_ac_anchors.json records the waveform identity checks.

## Nominal bandwidth with an actual next-core input

Each driver now feeds input 1 or input 2 of a second identical core, with that receiver's other differential input held at 100 mV.
The receiver includes its own CMFB and 100 fF per output.
The driver also sees the stated wire capacitance on each output.
These are core-to-core benches, with tile output stages and offset DACs still to be added.

| Receiver input | Wire capacitance per output | IHP driver bandwidth, inputs 1/2 | SKY130 driver bandwidth, inputs 1/2 |
|---|---:|---:|---:|
| 1 | 25 fF | 331.819/511.728 MHz | 471.907/607.915 MHz |
| 2 | 25 fF | 373.239/612.754 MHz | 575.346/811.244 MHz |
| 1 | 50 fF | 315.648/463.835 MHz | 445.801/563.500 MHz |
| 2 | 50 fF | 352.942/548.314 MHz | 539.004/733.938 MHz |

The compact candidate improves all eight nominal path/load combinations.
This validates the nominal loading benefit beyond a fixed-capacitor bench, while its PVT failures remain unresolved.
The source builder is scripts/prepare_core_fanout.py.
The matched evidence tables are evidence/ihp_core_fanout.csv and evidence/sky_compact_fanout.csv.

## Wrong finite AC curve control

A separate resistor-divider test confirms that a failed managed plot selection can export a complete but incorrect curve.
After two operating points and two AC analyses, Chipify 1960c81 exports the second gain of 0.75 instead of the intended first gain of 0.5.
Scalar metrics, finite samples and global pass flags all look valid.
The reusable control is scripts/probe_chipify_ac_selection.py.
The core AC auditor now compares every captured curve with its corresponding scalar gain and bandwidth.

## Tail-compliance and mirror follow-up

At sf and 0 C, the unmodified compact tail current rises from 334 uA at 1.45 V to 462 uA at 1.65 V, although its external reference remains fixed.
The corresponding diagonal ratio changes from 0.955138 to 1.02049.
A source-tied input pair improves cold low-supply margin by about 10.6 mV, but its high-supply hot ratio grows to 1.05460.
Doubling tail length from 0.65 to 1.3 um while preserving W/L raises current and does not remove the voltage dependence.
That change multiplies tail gate area by four, from 1664 to 6656 um2 for M13 alone in this two-copy candidate.
These are geometric gate areas, not routed macro areas.
Only eleven of the 32 combined well-tie and length cases pass the provisional ratio window.

The twelve-case wider folding-mirror follow-up recovers a small nominal fs margin but reduces input-1 bandwidth.
Its best fs margin in this set is 7.638 mV, still insufficient to establish a robust voltage budget.
The next diagnostic matches the tail-reference drain voltage to the core tail drain, first with an ideal error amplifier.
That ideal amplifier is a causal control, not a qualified implementation.
A separate scaled input-pair replica tests a transistor implementation of the same voltage matching.

The low-threshold PMOS input pair is already at its installed 0.35 um minimum length.
The TT model-bin scan and KLayout PCell coercion both confirm that limit.
A shorter low-threshold pair cannot be used to recover headroom with this PDK.

## Tail-reference voltage matching controls

The active-matching diagnostic moves the tail-reference transistor's gate off its drain and uses an ideal gain-10000 error amplifier to equalize reference and output drain voltages.
Fourteen nominal bias/corner points regulate tail current near the intended eightfold reference ratio.
One tt, 55 uA point converges to a nonphysical -213.825 V gate solution.
The gate-voltage limit rejects that case, so the result is not treated as physical feasibility evidence.
Ideal dependent-source experiments require explicit voltage-domain checks.

The transistor replica uses a one-eighth copy of each input-pair branch and eight series source-resistor units in the reference path.
Its two branch gates follow the corresponding real inputs.
With two circuit copies, each replica PMOS has three full-size fingers, preserving integer physical geometry.
The original reference current flows through this replica and sets the shared tail gate without an ideal error amplifier.

At nominal conditions its tail current is 3.30 to 9.39 percent above the ideal eightfold value over the tested currents and MOS corners.
The replica's source differs from the real pair source by 6.53 to 129.10 mV, so it is not an exact drain-voltage copy.
The pair-drain operating voltages differ between the replica and signal path.
Per-corner current trim must therefore be repeated.
The current sweep places useful shape settings near 26.25 to 33.75 uA, and the fixed-code supply/temperature sweep is the next acceptance check.
Both the active and transistor-replica results are retained as experiments.


![Nominal return ratios of both replica-candidate loops](figures/sky_replica_loops.png)

## First complete fixed-code curvature screen

The transistor-replica codes ff=1, fs=1, sf=0, ss=4 and tt=6 correspond to unit currents 27.5/27.5/26.25/31.25/33.75 uA.
Each code stays fixed over the three supplies and three temperatures.
All 45 cases meet the provisional ratio limits, with an overall range 0.995562 to 1.02830.
The reference current sources are still ideal, so real DAC and bandgap qualification remains required.

| SKY130 corner | Minimum ratio | Maximum ratio | Minimum tail voltage |
|---|---:|---:|---:|
| ff | 1.00452 | 1.02341 | 270.134 mV |
| fs | 1.00641 | 1.02737 | 306.080 mV |
| sf | 1.00117 | 1.02767 | 56.900 mV |
| ss | 0.995562 | 1.02830 | 81.173 mV |
| tt | 1.01324 | 1.02347 | 163.579 mV |

This is a pass of the diagonal shape screen, not a claim that every electrical requirement is met.
Tail-current ratio still reaches 1.26308 at fs, showing that exact mirror tracking is not what passed.
The observed transfer and the separate noise, bandwidth, feedback and transient tests determine acceptance.
The calibrated nominal surface, AC, noise and both loop data are retained under evidence/sky_replica_*.

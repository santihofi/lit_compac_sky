# IHP SG13CMOS5L versus SKY130A

This report is incremental.
No SKY130 circuit performance or physical signoff is claimed yet.

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
| Supply and temperature | 1.5 V, 27 C | Pending |
| Gain at four quadrant 100 mV inputs | -10.0387 V^-1 | Pending |
| Gain at four quadrant 10 mV inputs | -9.85739 V^-1 | Pending |
| Gain ratio, 100 mV / 10 mV | 1.01839 | Pending |
| First-input-only gain ratio | 0.977262 | Pending |
| Second-input-only gain ratio | 1.04751 | Pending |
| Differential output at +100 mV, +100 mV | -100.387 mV | Pending |
| Output common mode | 757.967 mV | Pending |
| Deterministic balanced output offset | -2.76e-13 V | Pending |

The nominal scalar table has no min/max limits, so its reported 100 percent yield means valid capture only.
It is not an equivalence or signoff verdict.
Full scalar values and the generated reference netlist template are retained under evidence/.

## Required remaining sections

Primitive mapping and model scope, resistor voltage/temperature coefficients, BJT choice, geometry and finger semantics, schematic sizing rationale, PVT and trim coverage, mismatch controls, loop stability, startup, noise, bandwidth, power, physical area, DRC/LVS, extraction and tree-level results remain to be measured.

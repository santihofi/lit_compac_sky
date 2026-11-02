# Reproducing the schematic exploration

All commands run inside iic-osic-tools.
The container mounts this repository at /foss/designs/lit_compac_sky and the IHP reference at /foss/designs/lit_compac.
The reference revision is 3764a02 and the measured tool image reports 2026.10.
Chipify is the local master revision 1960c81, version 0.2.3.
It predates strict verdict exit codes and resume support.

These are exploratory source decks and datasheets.
The drawn SKY130 prototype is still the initial mapping, not the rejected candidates or a qualified final schematic.
The inherited counter, inverter and chip-top template views do not represent a completed multiplier port.

## Run one SKY130 experiment

~~~sh
source /foss/designs/lit_compac_sky/.designinit
cd /foss/designs/lit_compac_sky/verification/porting/sky_curvature
/foss/designs/lit_compac_sky/scripts/with_sky130_ngspice.sh chipify-cli -c quad_sizing.yaml --json
python3 /foss/designs/lit_compac_sky/scripts/check_chipify_results.py datasheets/quad_sizing.yaml out
~~~

Use chipify-cli for headless work.
The chipify command starts the Qt application.
Do not run concurrent Chipify jobs in the same project directory.
The project shares its scratch area and latest output, even for different datasheets.
Independent projects can run concurrently within the container's CPU and memory limits.

The auditor verifies the latest sidecar's datasheet identity, case count, scalar validity and requested waveforms.
Use its allow-spec-fail option when retaining a valid failed candidate, then read specification_status separately.
A 100 percent yield from an unconstrained exploratory datasheet is only a data-validity result.

For IHP projects, source /foss/designs/lit_compac/.designinit and invoke chipify-cli directly.
Do not use the SKY130 wrapper with IHP models.
No clean target is needed.

## Experiment map

| Project under verification/porting | Purpose |
|---|---|
| ihp_core_tradeoffs | Current IHP bare core, matched 100 fF load and MOS/PVT baseline |
| ihp_core_validation | Current IHP nominal noise, CMFB loop gain and full transfer surface |
| sky_core_tradeoffs | Initial width and length exploration |
| sky_quad_options | LVT body connection and native-quad alternatives |
| sky_degenerated | Quad-source degeneration and modeled-resistor corner candidate |
| sky_curvature | Separate input-axis curvature, quad sizing and bias-current sensitivity |
| sky_core_validation | Degenerated candidate noise, loop gain and full transfer surface |
| sky_cmfb_options | Fast-loop resistance and slow-loop capacitor sweep |
| sky_cmfb_kick | Trapezoidal current-kick transients at two maximum time steps |
| sky_cmfb_drive | Fast-loop drive scaling at constant device voltage |
| sky_cmfb_loads | Shorter PMOS loads and mirror-master devices |
| sky_pair_degenerated | Added PMOS source resistors, bias sweep and fixed-code PVT |
| sky_pair_ac | Large pair candidate bandwidth and differential input loading |
| sky_compact_pair | Smaller pair/quad devices with curvature and AC capture |
| sky_compact_loads | Compact candidate with shorter PMOS loads, bias trim and PVT |
| sky_compact_compliance | Input-pair well ties and tail-length controls |
| sky_regulated_tail | Ideal error-amplifier diagnostic with explicit gate-voltage limits |
| sky_replica_tail | Transistor input-pair replica for the tail reference |
| sky_compact_validation | Compact nominal noise, CMFB and full transfer surface |
| ihp_core_fanout and sky_compact_fanout | Matched transistor receiver loads and 25/50 fF wire load |
| sky_higher_cm | Separate 1.8 V supply and 0.9 V common-mode alternative |

The prepare_core_exploration, prepare_core_scaling, prepare_quad_options, prepare_core_degeneration and prepare_degenerated_candidate scripts form the initial dependency chain.
Later prepare scripts consume those retained source decks.
Datasheets retain the explicit parameter selections for each measured sweep.
Rerunning a preparation script can restore its default datasheets, so inspect the diff before rerunning an accepted or historical configuration.

Full transfer captures are frozen by scripts/analyze_core_transfer.py.
It checks all 1681 input pairs, fits constant, feedthrough and product terms, and writes residual metrics and figures.
For batch output, pass the results option with out/transfer relative to the project.
scripts/check_core_ac_capture.py takes the datasheet and output directory and verifies captured core curves against scalar gain and bandwidth, in addition to the general integrity audit.
scripts/analyze_cmfb_kick.py audits transient captures, checks their final time, freezes a compressed waveform archive and plots recovery.
scripts/probe_sky_dc_solver.py runs direct ngspice controls on an unchanged rendered circuit to isolate solver behavior.

## Evidence interpretation

The comparison report identifies each candidate and its operating conditions.
CSV files preserve the raw PDK corner names.
Matched-skew plots reverse fs and sf between IHP and SKY130 according to the measured transistor controls.
The 1.8 V alternative is not an equal-supply replacement for the 1.5 V reference.

Bandwidth figures with 100 fF per output are bare-core measurements.
Input capacitance, actual next-stage loading, bias circuitry, PVT, mismatch, startup, extraction and layout remain separate acceptance checks.
No port candidate has reached physical signoff.

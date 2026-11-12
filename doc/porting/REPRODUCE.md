# Reproducing the schematic exploration

All commands run inside iic-osic-tools.
The container mounts this repository at /foss/designs/lit_compac_sky and the IHP reference at /foss/designs/lit_compac.
The frozen electrical reference is 3764a02 and the measured tool image reports 2026.10.
The system architecture was updated to reference 93ff956 on 2026-11-02, with the three measured core schematic blobs unchanged.
Chipify is the local master revision 1960c81, version 0.2.3.
It predates strict verdict exit codes and resume support.

These are exploratory source decks and datasheets.
The main macro schematic folders still contain the initial mapping.
A separate drawn replica candidate and its nominal replay are under verification/porting/sky_replica_schematic, with no claim of final schematic qualification.
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
| sky_replica_ac | Replica bare-core bandwidth and input capacitance |
| sky_replica_validation | Replica noise, CMFB and transfer surfaces |
| sky_replica_stability | Replica local bias-loop return ratio |
| sky_replica_fanout | Replica core driving an identical receiver |
| ihp_surface_corners | Matched IHP transfer surfaces at 1.5 V and three temperatures |
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

## Replica corner capture

Run the pvt batch folder in sky_replica_ac and sky_replica_stability, and the cmfb_pvt folder in sky_replica_validation.
After those complete, scripts/freeze_replica_corners.py independently checks all scalar values and anchors every exported core or loop curve before writing the evidence files.
scripts/check_loop_capture.py also accepts one datasheet and output directory for an individual feedback-loop audit.

Run the surface_corners batch in sky_replica_validation only after its CMFB batch finishes.
Use the same batch folder in ihp_surface_corners with the IHP environment.
scripts/analyze_corner_surfaces.py accepts project and label options, checks each complete 41 by 41 grid and freezes fitted shape metrics plus the raw waveforms.
The initial surface grid is five MOS corners by three temperatures at 1.5 V, not the full supply grid.
Raw fs/sf labels have opposite N/P speed meanings between the PDKs.

Batch output directories use datasheet basenames, irrespective of the input subfolder.
Surface datasheets therefore have a surface_ prefix to avoid overwriting the CMFB trim_* result directories.
Use distinct basenames when retaining separate sweeps in one Chipify project.

## Drawn replica and geometry grid

scripts/draw_replica_candidate.py writes the experimental core, OTA and gain-trim sheets.
scripts/verify_replica_schematic.py uses fresh Xschem netlists, checks all 132 instances against the rendered source and prepares frozen nominal replay decks.
The replay project README gives the exact Chipify commands.
scripts/audit_replica_replay.py compares measurements and captures against the original experiments.

scripts/prepare_replica_grid.py prepares a separate nominal control after rounding lengths and per-finger widths to 0.005 um.
It recalculates diffusion areas, perimeters and source/drain squares when a finger width changes, and retains every changed parameter in geometry_changes.json.
The exploratory source candidate and its earlier measurements remain intact.

## Gain-code coverage and resolution

scripts/prepare_replica_gain_trim.py prepares the endpoint, code-13 rail-control and nominal 32-code projects.
Run each project's endpoint configuration before its separate steps batch.
scripts/analyze_replica_gain_trim.py freezes the endpoint and rail-control data.
scripts/analyze_gain_steps.py verifies all 32 code identities, measures monotonicity and computes the nearest-code residual.

scripts/prepare_replica_trim_range.py prepares independent fixed-load and trim-segment resistance controls.
Its root datasheets test fixed-load scale 0.8 and trim scales 1/2/4 at tt/fs.
Its centered batch tests fixed-load scale 0.6 and trim scale 2 at all five MOS corners, 22/27 C and 1.5 V.
Use scripts/analyze_trim_range.py with group initial or centered to audit and freeze the corresponding results.
The minimum and maximum gains are endpoint brackets, not a guarantee of an acceptable intermediate code.

## Laboratory calibration and replica recovery

scripts/analyze_gain_calibration.py with design ihp or sky audits all five 32-code sweeps at 27 C and 1.5 V.
Its source summaries are required by scripts/prepare_calibrated_pvt.py.
That builder selects the nearest K100 code per corner and prepares separate SKY130 DC and AC projects plus the IHP comparison, with each code fixed over supply and temperature.

scripts/prepare_replica_kick.py builds the original replica's closed-loop current-kick project.
Run its kick.yaml with the SKY130 wrapper, then scripts/analyze_replica_kick.py.
The auditor checks waveform completion and scalar anchors, freezes every trace and compares the 100 ps and 50 ps time steps.
This recovery bench does not exercise power-up.

scripts/analyze_calibrated_pvt.py freezes the three completed calibrated PVT projects and anchors all 90 SKY130 AC curves.
scripts/prepare_trim_gate_control.py prepares a separate ideal trim-rail diagnostic, and scripts/analyze_trim_gate_control.py checks both its waveform anchors and its unchanged-rail controls.

scripts/prepare_gain_dc_sweep.py builds the separate in-simulator code sweep.
After its control.yaml run, scripts/audit_gain_dc_sweep.py compares all 32 waveform points with the independent code runs.
A one-row waveform sweep is not a replacement for per-code specification checks.

## Mid-rail switch controls

scripts/prepare_trim_switch_probe.py generates the type comparison and the separate NMOS length sweep.
Run probe.yaml in sky_trim_switch_probe or sky_trim_switch_lengths.
scripts/analyze_trim_switch_probe.py accepts the project name, checks the supply axis and scalar anchors, and verifies the PMOS multiplicity and parallel transmission-gate conductance identities.
The saved curves retain all five supply values for each process and length condition.

scripts/prepare_trim_switch_candidates.py generates the PMOS-only and transmission-gate endpoint projects.
Run each endpoints batch, then scripts/analyze_trim_switch_candidates.py to audit all twenty cases and freeze their coverage.
The two projects use different output directories and may run concurrently.

## Per-corner gain-code coverage

Run scripts/prepare_trim_code_coverage.py with --grid nominal for all 32 codes at five MOS corners, 27 C and 1.5 V.
Run with --grid pvt for all 32 codes at five MOS corners, three temperatures and three supplies.
Inside verification/porting/sky_trim_tg2, use the SKY130 ngspice wrapper with chipify-cli --batch datasheets/codes_nominal --json or datasheets/codes_pvt.
Then run scripts/analyze_trim_code_coverage.py with the matching --grid and an explicit --gain-tolerance-percent.
The tolerance is a sensitivity screen until a gain specification is confirmed.
The report groups codes by PVT and requires gain, diagonal shape and gate-rail bounds at the same code.
Every point must contain all 32 codes, with no duplicates, before the report is written.
This DC screen cannot assert complete specification coverage because AC, noise, loops and passive corners remain separate requirements.

Run scripts/prepare_trim_feasible_ac.py after freezing nominal code coverage.
Inside verification/porting/sky_trim_tg2_ac, run the SKY130 ngspice wrapper with chipify-cli --batch datasheets/feasible --json.
Run scripts/analyze_trim_feasible_ac.py to check every captured AC curve and join the results to exactly the DC-feasible code set.
Run scripts/plot_trim_code_coverage.py to regenerate the comparison figure.
The bandwidth reference is the nominal per-MOS IHP calibration with the trim gate rail tracking VDD.

## Input-2 speed controls

Run scripts/prepare_input2_speed.py, scripts/prepare_input2_load_resistors.py and scripts/prepare_input2_parallel.py in that order.
The generated projects are verification/porting/sky_input2_speed, sky_input2_load_resistors and sky_input2_parallel.
From each project directory, run the SKY130 ngspice wrapper with chipify-cli -c speed_fs.yaml, load_fs.yaml or parallel_fs.yaml respectively.
Freeze the first two studies with scripts/analyze_input2_speed.py and its --study loads option.
Use --study parallel after the third run.
Run scripts/probe_input2_load_resistors.py for the independent resistance and capacitance controls.
All scripts use the installed SKY130 models, and the resistor mapping records model hashes.

## Chipify release transition on 2026-11-09

The installed 0.2.3 release is source revision e318888764770c3f5d55751580679df1054e7cac.
Installed CLI, analysis and abort-module hashes match the corresponding local release files.
The old batch used /headless/.local/bin/chipify-cli, which was removed during the package upgrade.
Its ff, fs and sf PVT datasheets completed with 288 valid cases each.
Its ss sweep stalled when replacement workers could not reopen the old executable path, and tt had not started.
The stale process tree was stopped before restarting work.
The new release executable is /usr/local/bin/chipify-cli.
An unchanged two-copy narrow-load fs control reproduces ten prior scalar values and both independently anchored AC curves.

To repeat only the unfinished corners, use chipify-cli -c codes_pvt/tg2_pvt_ss.yaml --out out/tg2_pvt_ss --cores 4 --json and then the corresponding tt command from verification/porting/sky_trim_tg2 with the SKY130 ngspice wrapper.
Do not use --resume for the old build's interrupted work because it did not write the new run journal.
The released CLI supports --cores and --out directly, so worker and result-directory changes no longer require editing project settings.
Keep completed corner provenance separate from release-replay evidence.

## Quiet-replica selected codes and qualification

Run python scripts/analyze_input2_quiet_corners.py and python scripts/analyze_input2_quiet_codes.py to reconstruct the nominal joint selection from completed batches.
The latter replaces the selected-code evidence only when an SS code is feasible.

Run python scripts/prepare_input2_quiet_loops.py, then run the wrapper with chipify-cli --batch datasheets/nominal --cores 3 --json from verification/porting/sky_input2_quiet_loops.
After completion run python scripts/analyze_input2_quiet_loops.py from the repository root.
The loop auditor requires all five selected parameter tuples and reconstructs the captured return-ratio margins.

Run python scripts/prepare_input2_quiet_pvt.py to create a separate exhaustive DC project.
From verification/porting/sky_input2_quiet_pvt run the wrapper with chipify-cli --batch datasheets/codes_pvt --cores 4 --json.
After all five sheets complete, run python scripts/analyze_trim_code_coverage.py --candidate quiet --grid pvt --gain-tolerance-percent 1 from the repository root.
This is 1440 gain-code cases at retained bias currents, with nominal passives and ideal references.
Bandwidth, noise and stability must subsequently be checked at the same feasible settings.

## Bias sensitivity at the uncovered quiet-replica PVT points

After the exhaustive quiet PVT audit, run python scripts/prepare_input2_quiet_bias.py.
Run the wrapper with chipify-cli --batch datasheets/sensitivity --cores 4 --json from verification/porting/sky_input2_quiet_bias.
After all thirteen sheets finish, run python scripts/analyze_input2_quiet_bias.py from the repository root.
The analyzer requires the intended 150 parameter tuples, including thirty unchanged-current controls, and checks six control metrics against the original sweep.
A lack of passing sampled codes does not reject untested gain or bias codes.

## Fine calibration and resistor-range controls

Run python scripts/prepare_input2_quiet_refine.py and python scripts/prepare_input2_quiet_range.py.
Their separate projects are verification/porting/sky_input2_quiet_refine and verification/porting/sky_input2_quiet_range.
Run the wrapper with chipify-cli --batch datasheets/refine --cores 4 --json in the refinement project, and use datasheets/endpoints in the range project.
After each batch completes, run python scripts/analyze_input2_quiet_followups.py refine or range from the repository root.
Run python scripts/summarize_input2_quiet_calibration.py after the refinement audit to combine observed DC settings for the unchanged resistor network.
It explicitly excludes resistor-range variants.

## Global widened-network code screen

Run python scripts/prepare_input2_quiet_range14.py after the endpoint study.
From verification/porting/sky_input2_quiet_range14 run the wrapper with chipify-cli --batch datasheets/codes --cores 4 --json.
After completion, run python scripts/analyze_input2_quiet_followups.py range14.
The analyzer requires all 322 tuples, reproduces twenty prior endpoints and excludes the two replay-only rows from the ten-point all-code verdict.
This study uses one global resistor network and cannot be merged into the previous network's calibration coverage.

## Widened-network nominal speed checks

Run python scripts/prepare_input2_quiet_range14_ac.py after the all-code subset audit.
From verification/porting/sky_input2_quiet_range14_ac run the wrapper with chipify-cli --batch datasheets/nominal --cores 4 --json.
After completion run python scripts/analyze_input2_quiet_range14_ac.py from the repository root.
Every nominal DC-feasible code is checked, with exact parameter matching, six DC replay metrics and four independently anchored AC curves.
The matched IHP bare and loaded references are reused from the preceding comparison with the fs/sf mapping preserved.

## Resistance-matched trim-poly controls

Run python scripts/prepare_input2_quiet_trim_poly.py and python scripts/probe_input2_load_resistors.py --kind trim.
From verification/porting/sky_input2_quiet_trim_poly run the wrapper with chipify-cli -c trim_fs.yaml --cores 4 --json for the four-case FS control.
Use --batch datasheets/corners for the sixteen-case comparison across all nominal DC-feasible codes.
Run python scripts/analyze_input2_quiet_trim_poly.py for the FS audit, or add --corners for the five-corner audit.
The wider-family control must reproduce prior DC and AC metrics, while every captured curve is independently anchored.

## SS calibration search with narrow trim poly

Run python scripts/prepare_input2_trim_ss_bias.py.
From verification/porting/sky_input2_trim_ss_bias run the wrapper with chipify-cli -c ss_bias.yaml --cores 4 --json.
After completion run python scripts/analyze_input2_trim_ss_bias.py.
The auditor requires all 160 gain/current tuples and replays two preceding SS controls.
It reports DC-feasible codes per sampled current, not bandwidth coverage.

# SKY130 ngspice runtime

The installed SKY130 library directory contains spinit, while ngspice's user initialization lookup expects .spiceinit.
With the template's original SPICE_USERINIT_DIR, the tested image selected hsa compatibility through its other startup files but did not enable skywaterpdk.
The process-local scripts/with_sky130_ngspice.sh wrapper selects the committed scripts/ngspice/.spiceinit before model parsing and limits solver threads to one.
It works when a characterization tool changes the simulator working directory.

Run source .designinit, then scripts/with_sky130_ngspice.sh chipify-cli with the desired arguments from a characterization project.
Use the wrapper's absolute path when launching outside the project root.
The template's batch ngspice Make targets use this wrapper automatically.
The wrapper rejects an unset or different PDK, and changes only its child process environment.

Verified on IIC-OSIC-TOOLS 2026.10 with ngspice 47.
A startup probe reported SKY130_OPT=0 through the original environment and SKY130_OPT=1 through the wrapper.
Do not use only a Chipify return code as an electrical pass criterion.
Read the expected case count, finite measurements, sim_error and waveform capture results.

The existing inverter DC bench produced vgsp_at_vcm = 0.9071777 V with both the original environment and the wrapper.
The wrong-PDK guard returned 2 and bash -n passed.
The image does not provide ShellCheck or REUSE executables, so those checks were not run locally.
The template's existing license-check CI remains the REUSE gate.

## Dense analog DC sweeps

Inspect the simulator log when a DC sweep repeatedly times out.
Repeated dynamic gmin recovery can dominate a run even when every recovered point eventually converges.
Keep convergence aids in the affected bench so their electrical effect can be compared with an unchanged reference.

In a measured SKY130 analog example, initial guesses on the outputs and common-mode control nodes plus rshunt=1e12 reduced a 1681-point sweep from a 600-second timeout to 58.27 seconds.
An eleven-point control differed from the original result by at most 49 nV on the two outputs.
That result does not establish suitable guesses or shunt values for another circuit.
A nodeset supplies a starting guess, while a shunt adds conductance and must be included in the accuracy check.

KLU aborted that example without DC vectors even though ngspice returned zero.
Require the expected point count, sweep endpoints and finite requested vectors.
The runtime wrapper deliberately leaves solver selection and convergence aids to each bench.

## Noise analysis and save selection

On ngspice 47, save all before noise preserves the noise spectra.
A selective voltage save, such as save v(out), suppresses the noise result and produces a no-data diagnostic even when the simulator returns zero.
A two-resistor control gives 2.878894 nV/sqrt(Hz) with either no save command or save all, and no noise result with the selective save.
Run python3 scripts/probe_noise_save.py to reproduce all three controls.
The output is verification/controls/noise_save_controls.json.
Use the output option to retain it elsewhere.

## AC plot names after repeated operating points

Ngspice 47 names the first AC plot ac2 after two retained op plots, and ac17 after seventeen.
Do not assume that the first AC command always creates ac1.
Chipify 1960c81 hard-codes ac1 for managed AC capture.
Keep AC in a separate testbench, or save any needed scalars as control variables and run destroy all before AC.
The latter clears the previous vectors, so copy them before clearing.
Run python3 scripts/probe_ngspice_plot_names.py to reproduce one, two and seventeen operating points, plus the clear-before-AC control.

A second control demonstrates a more subtle capture error on Chipify 1960c81.
A divider has first-AC gain 0.5 and second-AC gain 0.75.
After one op, managed capture exports the intended first AC curve.
After two op commands, its failed setplot ac1 leaves the second AC current and exports gain 0.75, while all scalar and pass fields remain valid.
Finite waveform data alone cannot establish analysis identity.
Run python3 scripts/probe_chipify_ac_selection.py and compare the captured gain with the explicit first-AC scalar.

## Unused sweep parameters

A parameter listed in a datasheet does not change the circuit unless the template or an evaluation expression consumes it.
Chipify 1960c81 accepts a two-label resistor-corner sweep of an unchanged resistor divider, reports both cases as passing and emits no unused-parameter diagnostic.
Run python3 scripts/probe_chipify_unused_parameter.py with an output path to reproduce that control.
Inspect the selected model entry points as well as the result labels.
The separate [passive-corner control](passive-corners.md) verifies the installed SKY130 model responses.

## Chipify 0.2.3 run controls and environment changes

Release e318888 provides --cores N and --out DIR for per-run worker and output-directory selection.
Use the SKY130 ngspice wrapper with these options so simulator initialization stays the same in scratch directories.
The --resume option continues a compatible interrupted run from its saved journal.
An interrupted older build without that journal must be rerun, while completed datasheets can be retained separately.
The --strict option classifies individual row failures in the exit status.
When unused calibration codes may fail, evaluate the existence of a jointly passing code per operating condition separately from row yield.

Keep the executing CLI path and installed package stable during a multiprocessing run.
In a measured update from an older installation, removing its CLI executable left replacement workers repeatedly failing to reopen that path.
The completed datasheets survived, but the active datasheet required recovery.
After an environment change, check the installed path and source-file hashes and replay an unchanged control before combining new measurements with earlier results.
The released 0.2.3 installation reproduced ten analog scalar values and two independently anchored AC curves in that control.

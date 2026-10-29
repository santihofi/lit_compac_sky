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

# Replica gain-trim range control

This experiment separates the fixed core load resistance from the bypassed trim segments.
scripts/prepare_replica_trim_range.py generates the source deck and datasheets from sky_replica_tail.
All MOS geometry and per-corner ideal reference currents are unchanged.

Source the design .designinit and run Chipify through scripts/with_sky130_ngspice.sh.
The initial range_tt.yaml and range_fs.yaml sweeps each contain six cases.
The centered batch contains five sheets of four cases each.
Do not run two Chipify jobs concurrently in this folder.
Run scripts/analyze_trim_range.py after each complete group to audit its metadata and scalar results before freezing evidence.

The initial experiment has valid data in all twelve cases and several shape failures.
The centered configurations are follow-up experiments.
No configuration here is accepted geometry or a calibrated physical DAC.

# Transistor-replica tail experiment

This is a candidate source circuit for the SKY130A port.
It has not been promoted into the drawn prototype or released to layout.

scripts/prepare_replica_tail.py starts from the compact source-degenerated candidate.
M14 drives a one-eighth replica of the two PMOS input branches and their source resistors.
The replica branch drains connect to the shared tail gate, while their gates follow the corresponding input.
At pair_scale=1 and power_m=2, each replica transistor uses three 6.21875 um fingers.
Eight series copies of each source-resistor unit provide the eightfold effective resistance.

The fixed-code PVT sheets cover five MOS corners, supplies 1.45/1.5/1.65 V and temperatures 0/27/80 C.
The five ideal reference-current settings are a proxy for per-die bias calibration, not a demonstrated SKY130 DAC.
Run them through chipify-cli with the repository's ngspice wrapper.
The general result auditor rejects missing and nonfinite data independently of electrical limits.

The separate sky_replica_ac, sky_replica_validation and sky_replica_stability projects measure differential AC, noise, full transfer, CMFB and the local replica feedback loop.
Keep one active Chipify job per project.
A batch writes outputs under the datasheet stem, so use distinct stems when different folders contain different tests.

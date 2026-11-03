# Replica loop current kicks

This bench uses the original replica candidate at tt, 27 C, 1.5 V and gain code 13.
It applies a 20 ns current pulse of either polarity to the CMFB load-gate node or the shared main/reference tail-gate node.
Pulse amplitude is 40 uA, compared with the two-copy circuit's 67.5 uA ideal reference.
Both loops remain closed.
Trapezoidal integration is repeated with maximum time steps of 100 ps and 50 ps.

The provisional residual limit is 1 mV on both output common mode and the tail gate at 900 to 1000 ns.
The initial DC point precedes each kick.
This is recovery about an established operating point, not power-up or physical bias-source qualification.
Use scripts/analyze_replica_kick.py to independently check waveform completion, scalar anchors and maximum-step sensitivity.

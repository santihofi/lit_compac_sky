# Common-mode-biased replica control

The signal-tracking reference is compared with both replica gates tied to a new explicit replica_cm port.
The bench connects that port to its existing ideal vref source, also used by CMFB.
All transistor dimensions, currents, resistors and gain codes remain fixed.
Each case measures DC shape, bare-core AC and AC while driving an identical receiver input 1 with 25 fF wire per output.
This reference-bias change may alter curvature, common-mode sensitivity and noise.
It needs real reference-driver impedance, loop and PVT qualification before use in a port schematic.

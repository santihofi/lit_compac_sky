# Slow-corner receiver-loaded bandwidth

The driver feeds input 1 or input 2 of an identical core with its own ideal supplies and CMFB.
The unused receiver input has 100 mV differential bias.
Wire capacitance is 25 or 50 fF per driver output, and receiver outputs have 100 fF each.
Two-copy and five-copy SKY130 variants scale both driver and receiver together.
The IHP comparison uses raw sf, corresponding to raw SKY130 fs, and its nearest nominal gain code 12.
Driver current is measured separately from the receiver supply.

This five-copy experiment is diagnostic only because the inherited replica expression truncates 7.5 fingers to seven while retaining diffusion parameters for the original finger width.
Use sky_input2_fanout6 for the integer-finger follow-up.

# Slow-corner receiver-loaded bandwidth

The driver feeds input 1 or input 2 of an identical core with its own ideal supplies and CMFB.
The unused receiver input has 100 mV differential bias.
Wire capacitance is 25 or 50 fF per driver output, and receiver outputs have 100 fF each.
Two-copy and six-copy SKY130 variants scale both driver and receiver together.
The IHP comparison uses raw sf, corresponding to raw SKY130 fs, and its nearest nominal gain code 12.
Driver current is measured separately from the receiver supply.

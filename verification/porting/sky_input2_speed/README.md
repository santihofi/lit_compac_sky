# Input-2 speed sensitivity

This nine-case study retains the transmission-gate trim topology, nominal passives, 100 fF output loads, 1.5 V supply and 27 C.
At the slow nominal SKY130 fs corner it varies quad finger count and ideal unit bias current.
The quad uses two, four or eight 5 um fingers at 0.15 um length, with matching diffusion and dummy-device scaling inherited from the source deck.
Gain code 29 is held fixed for sensitivity measurement, so improved bandwidth is not yet matched-gain qualification.
Each case receives DC gain and shape plus both input AC responses.
The reference combination is quad_scale=1 and ibias=27.5 uA.
Physical bias circuitry, mismatch and loop stability are outside this screen.

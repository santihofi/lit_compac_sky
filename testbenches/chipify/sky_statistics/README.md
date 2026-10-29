# SKY130 statistical activation controls

Run inside IIC-OSIC-TOOLS after selecting sky130A.
Chipify 0.2.3 is required.

```sh
source ../../../.designinit
../../../scripts/with_sky130_ngspice.sh chipify-cli --batch datasheets --json
```

The four individual-mode statistical cases use eight independent seeds each.
The combined process and mismatch case uses four seeds.
Compare `out/<datasheet>/simulation_results.csv` after checking simulator errors and finite values.
The `off` and `process_on_tt` results should be equal across seeds.
The `mismatch` case should give unequal paired devices.
The `process_mc` case should vary across seeds while equal device pairs stay equal.
The combined case should show both variation across seeds and unequal paired devices.
The multiplicity case distinguishes a resistor wrapper's statistical area parameter from electrical parallel copies.
These are activation controls, not estimates of production spread or yield.
The model path assumes the container's /foss/pdks/sky130A installation.

See [the model guide](../../../doc/sky130A-Open-PDK/sky130A_ngspice_mc_mm_guide.md) for measured control results and model-selection rules.

# SKY130 device controls

Run in IIC-OSIC-TOOLS with Chipify 0.2.3 from this folder:

```sh
source ../../../.designinit
../../../scripts/with_sky130_ngspice.sh chipify-cli -c corner_identity.yaml --json
```

The probe measures diode-connected standard and low-threshold MOS gate voltages at fixed currents and low-voltage precision-poly resistance.
The corner sweep checks all five MOS labels.
Every scalar is unconstrained, so inspect simulator errors and finite values before interpreting the table.
The measured values describe the bench conditions, not an operating-range guarantee.
See [the model guide](../../../doc/sky130A-Open-PDK/sky130A_ngspice_mc_mm_guide.md) for the skew-corner interpretation.

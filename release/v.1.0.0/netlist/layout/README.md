# Extracted Layout Netlists

Layout netlists of `chip_top`, extracted from the GDS during LVS.

They are written by `make klayout-lvs` (`chip_top_klayout.cir`) and by `make magic-lvs` (`chip_top_magic.ext.spc`), which move the extracted netlist here out of the LVS run folder in `verification/lvs/`.

The LVS that signs this chip off is the one inside the LibreLane flow, whose report is [verification/reports/lvs.netgen.rpt](https://github.com/iic-jku/sky130A-ams-chip-template/blob/main/verification/reports/lvs.netgen.rpt). The two targets above run the same comparison outside the flow and write here. See [Layout Versus Schematic (LVS)](https://github.com/iic-jku/sky130A-ams-chip-template/blob/main/README.md#layout-versus-schematic-lvs) in the top-level README.

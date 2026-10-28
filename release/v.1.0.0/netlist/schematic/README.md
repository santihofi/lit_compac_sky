# Schematic Netlists

Schematic netlists of `chip_top` for LVS, exported from Xschem.

They are written by `make klayout-lvs-netlist` (CDL, `chip_top_klayout.cdl`) and by `make magic-lvs-netlist` (SPICE, `chip_top_magic.spice`). Both targets also run as the first step of `make klayout-lvs` and `make magic-lvs`.

The CDL export sets `spiceprefix 0` and appends a `u` to every `L` and `W`, because the KLayout deck reads an `X` line as a subcircuit and takes the numbers on an `M` line as metres. See [Layout Versus Schematic (LVS)](https://github.com/iic-jku/sky130A-ams-chip-template/blob/main/README.md#layout-versus-schematic-lvs) in the top-level README.

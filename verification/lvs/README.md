# Top-Level LVS Reports

Per-cell LVS run folders of `chip_top`, written by `make klayout-lvs` (`chip_top.klayout.lvs/`) and by `make magic-lvs` (`chip_top.magic.lvs/`). Both folders are wiped at the start of each run, so they always reflect the latest run only.

The LVS that signs this chip off runs inside the LibreLane flow and writes [../reports/lvs.netgen.rpt](../reports/lvs.netgen.rpt). It ends with four unmatched nets, the `VDDIO_Q`, `VSSIO_Q`, `VDDA` and `VSSA` ring buses of the clock pad, which the pad ring connects by abutment and the extraction therefore does not follow. `Checker.LVS` is off for that reason, see the comment in [flow/librelane/config.yaml](../../flow/librelane/config.yaml). See [Layout Versus Schematic (LVS)](https://github.com/iic-jku/sky130A-ams-chip-template/blob/main/README.md#layout-versus-schematic-lvs) in the top-level README.

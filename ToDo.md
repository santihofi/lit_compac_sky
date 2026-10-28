# ToDo List

The port of this template from [ihp-sg13g2-ams-chip-template](https://github.com/iic-jku/ihp-sg13g2-ams-chip-template) to sky130A ran on 2026-09-18 and 2026-09-19, one commit per step. The step-by-step plan it followed, with the ten decisions and a "Done" line per step recording what was measured, is the version of this file at commit `603ba9f`. What is left is below.

- [ ] Zenodo release and DOI: into the badge row and the BibTeX of [README.md](README.md) and into the `identifiers` entry of [CITATION.cff](CITATION.cff). The `## PDKs` section of the two IHP templates links this repository since 2026-09-20.
- [ ] Repeat the record run on the IIC-OSIC-TOOLS `2026.09` image once it is released: `make clean-all && make all`, then the targets `all` does not cover whose outputs are tracked (the plot scripts, PEX modes 1 and 2 per macro, CACE, `make bondplan`). Everything in this repository was measured on `2026.08`, which was `latest` during the port while the templates ask for `2026.09`.
- [ ] Top-level `klayout-drc-regular` on a bigger machine. `magic-pex` is done, it took two hours and fifteen minutes and its netlist is in `netlist/pex/`.
- [ ] Top-level `make sim-gl-xschem` on the extracted netlist, its plotted data in `testbenches/xschem/plot_simulations/`, and the five tutorial figures that show it. Two things make this more than a long run. The netlist is 48 MB of flat transistors, and the flat extraction merges every supply of the pad ring into `VDD` and `VSS`, so the pads see the core rail instead of 3.3 V. Decide whether the figures come from this netlist or from a testbench that drives the merged rail on purpose.
- [ ] Three tutorial figures need the container desktop, they have no batch export: the KLayout DRC and LVS output windows and the 2.5D view of `inverter_top`. They were dropped rather than copied from the IHP template, whose screenshots show IHP content.
- [ ] Top-level LVS: four nets do not match, the `VDDIO_Q`, `VSSIO_Q`, `VDDA` and `VSSA` ring buses of the clock pad, because the pad ring connects its supply buses by abutment and the extraction reads the DEF, where abutment is a net name and not a wire. Fix that and switch `Checker.LVS` back on in [flow/librelane/config.yaml](flow/librelane/config.yaml).
- [ ] IR drop and power grid analysis that follows an abutted pad ring. `check_power_grid` starts its search at a pad bus stub and never leaves the ring, so `OpenROAD.IRDropReport` and `Checker.PowerGridViolations` are off. With the pad instances removed from a copy of the database the same check reports 24 unconnected shapes of 12618, all inside the two inverter macros.
- [ ] Magic reading the OpenRAM SRAM GDS. Its bit cells carry `cfom.maskAdd` (22/21), `cfom.maskDrop` (22/22), `cp1m.maskDrop` (33/42) and `cp1m.maskAdd` (33/43), which `sky130A.tech` does not define. With that fixed, `Magic.StreamOut`, `KLayout.XOR` and `Checker.XOR` go back on and [scripts/strip_mask_layers.py](scripts/strip_mask_layers.py) retires.
- [ ] A custom LibreLane step for the logo and the fill, replacing [scripts/add_logo_fill.sh](scripts/add_logo_fill.sh).
- [ ] Blender renders for [render/blender/](render/blender/).
- [ ] VACASK testbenches for the inverter macro, and gate-level ones for the counter macro.
- [ ] Ngspice and Verilog RTL co-simulation in Xschem: https://www.youtube.com/watch?v=PPd7jkcHOgA
- [ ] Save a Markdown report of the CACE run next to its plots.
- [ ] Exercise solutions for the tutorial.
- [ ] Custom LibreLane step for power estimation, for the counter macro and the top level.
- [ ] YouTube tutorial.

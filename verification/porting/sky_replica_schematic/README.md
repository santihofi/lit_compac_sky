# Drawn replica candidate

This is an experimental schematic view of the characterized compact replica candidate.
The main macro folders still contain the initial port mapping.
This view has not been accepted for layout or integrated into the chip top.

The wired multiplier adds modeled degeneration resistors to both input stages and a one-eighth input-pair replica in the tail reference.
The gain-trim and OTA sheets retain their wired topology with the selected SKY130 dimensions.
The symbols preserve port order and carry Spectre format attributes, but the measured replay uses ngspice only.

From the repository root inside the container:

~~~sh
source .designinit
python3 scripts/draw_replica_candidate.py
python3 scripts/verify_replica_schematic.py
cd verification/porting/sky_replica_schematic/replay
/foss/designs/lit_compac_sky/scripts/with_sky130_ngspice.sh chipify-cli --batch datasheets --json
cd /foss/designs/lit_compac_sky
python3 scripts/audit_replica_replay.py
~~~

The drawing generator consumes the frozen source topology and selected nominal parameter set.
Regenerate the drawings through that script.
The verification script creates fresh Xschem netlists, rejects netlist errors and compares all 132 instances, their ordered terminals, port lists and numerical parameters against the reference deck.
Its node mapping must be bijective.
It rejects independent wrong-bulk and wrong-width controls.
Xschem's omitted unity m attribute is normalized to its default of one.

The five replay decks are frozen nominal snapshots, not general parameter-sweep templates.
Their YAML parameters describe those snapshots.
Regenerate from the source when changing conditions or geometry.
AC, noise, diagonal DC, CMFB and full transfer replay match 48 scalar values and the three declared waveform captures.
The full transfer capture contains 1681 input pairs.

Dimensions still include off-grid values from continuous electrical exploration.
The separate sky_replica_grid experiment rounds channel lengths, per-finger widths and resistor lengths to 0.005 um, and recalculates changed diffusion geometry.
That quantized candidate needs its own corner, mismatch, transient and physical checks.
Neither view proves a complete port or physical signoff.

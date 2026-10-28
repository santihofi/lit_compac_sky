# Specifications

Top-level specification of `lit_compac_top`, an analog mixed-signal chip in SkyWater sky130A.

## Technology

| Item | Value | Source |
| --- | --- | --- |
| Process | SkyWater sky130, 130 nm CMOS, five metal layers | PDK |
| PDK | sky130A, open_pdks `026824c7` | `$PDK_ROOT/sky130A/SOURCES` |
| Standard cells | `sky130_fd_sc_hd`, 2.72 um row height, 0.46 um site | `sky130_fd_sc_hd__nom.tlef` |
| Routing layers | `li1` to `met5`, the flow routes `met1` to `met5` | [flow/librelane/config.yaml](../flow/librelane/config.yaml) |
| Pad library | `sky130_ef_io`, 80 um GPIO pads and 75 um supply and analog pads on a 200 um deep ring | `sky130_ef_io.lef` |
| Die | 1600 um x 1600 um | [floorplan.md](floorplan.md) |

## Supplies

| Net | Voltage | Domain | Pad cell |
| --- | --- | --- | --- |
| `VDD` | 1.8 V | digital core, analog macros | `sky130_ef_io__vccd_lvc_clamped_pad` |
| `VSS` | 0 V | core ground | `sky130_ef_io__vssd_lvc_clamped_pad` |
| `IOVDD` | 3.3 V | pad ring | `sky130_ef_io__vddio_hvc_clamped_pad` |
| `IOVSS` | 0 V | pad ring ground | `sky130_ef_io__vssio_hvc_clamped_pad` |

The sky130 pads carry twelve ring buses. Every pad instance in [rtl/lit_compac_top.sv](../rtl/lit_compac_top.sv) ties them to those four supplies: `VCCD` and `VCCHIB` to `VDD`, `VSSD` to `VSS`, `VDDIO`, `VDDIO_Q`, `VDDA` and `VSWITCH` to `IOVDD`, and `VSSIO`, `VSSIO_Q` and `VSSA` to `IOVSS`. Two connect slices short the same buses inside the ring, so the ring is one node per supply even where a pad does not drive it. `AMUXBUS_A` and `AMUXBUS_B` stay unconnected, this chip has no analog mux.

## Clock and reset

| Item | Value |
| --- | --- |
| Clock port | `clk_PAD`, through `clk_pad.pad_cell/IN` into the core |
| Clock period | 25 ns, 40 MHz |
| Reset | `rst_n_PAD`, active low, asynchronous to the counters |
| IO delay constraint | 20 percent of the clock period, in and out |

The IHP templates of this family run at 50 MHz. The sky130 GPIO pad is slower: at a 20 ns period the slow corner misses the setup of the pad paths by 3.4 ns, at 25 ns every corner closes. The cocotb testbench and the transient testbench use the same 40 MHz.

## Corners

Three nominal parasitic corners, each with its standard cell and pad liberty files:

| Corner | Process | Voltage | Temperature |
| --- | --- | --- | --- |
| `nom_tt_025C_1v80` (default) | typical | 1.80 V | 25 C |
| `nom_ss_100C_1v60` | slow | 1.60 V | 100 C |
| `nom_ff_n40C_1v95` | fast | 1.95 V | -40 C |

The OpenRAM SRAM macro is characterized for one corner only, `TT_1p8V_25C`, so every STA corner reads that library. This is the same stand-in situation the IHP SRAM has above 1.32 V and it makes the SRAM timing optimistic in the slow corner and pessimistic in the fast one.

## Macro inventory

| Instance | Macro | Size | Role |
| --- | --- | --- | --- |
| `i_lit_compac_core.counter1` | `counter_top` | 200 um x 100 um | 8 bit counter, low nibble to `output_PAD[3:0]`, high nibble to the four bidirectional pads |
| `i_lit_compac_core.counter2` | `counter_top` | 200 um x 100 um | 8 bit counter, all eight bits to `output_PAD[11:4]` |
| `i_lit_compac_core.inverter1` | `inverter_top` | 42.73 um x 75.52 um | four inverters used as digital inverters, inputs from the bidirectional pads, outputs to `output_PAD[15:12]` |
| `i_lit_compac_core.inverter2` | `inverter_top` | 42.73 um x 75.52 um | two inverters as analog amplifiers between the analog pads, the other two tied off |
| `i_lit_compac_core.sram_0` | `sky130_sram_1kbyte_1rw1r_32x256_8` | 479.78 um x 397.5 um | 256 words of 32 bit, port 0 reads address 0 every clock, port 1 deselected, the parity of the word goes to `output_PAD[16]` |
| `jku_logo` | `sky130_ip__jku` | 100 um x 100 um | logo on `met4` |
| `jku_names` | `sky130_ip__jku_names` | 100 um x 100 um | names on `met4` |

## Functional behaviour

- `input_PAD[0]` is the enable. High lets both counters count and switches the four bidirectional pads to output, low freezes the counters and turns the bidirectional pads into inputs, which then drive the inputs of `inverter1`.
- The two counters run from the same clock and reset, so they count in lock step. `counter1` shows its low nibble on four dedicated output pads and its high nibble on the bidirectional pads, `counter2` shows all eight bits.
- `inverter1` is a digital inverter chain: each of its four channels inverts one bidirectional pad onto one output pad.
- `inverter2` is the analog channel: two inputs behind the ESD diodes of their pads, two outputs on bare pads, with the other two channels tied to `VSS`. At 0.9 V common mode the inverter has 29.5 dB of open-loop gain and a 1.25 MHz corner into 10 pF, see [macros/inverter/README.md](../macros/inverter/README.md).
- The SRAM reads address 0 on every clock and the core reduces the 32 bit word to its parity, so one pad shows whether the word has an odd number of ones. Nothing writes the SRAM, its content is whatever the array powers up with.

## Verification state

| Check | Tool | Result |
| --- | --- | --- |
| RTL lint | Verilator | clean, with and without the power pins |
| RTL simulation | cocotb with Icarus | 6 of 6 tests pass |
| Gate-level simulation | cocotb with Icarus on `netlist/pnl/lit_compac_top.pnl.v` | 6 of 6 tests pass |
| Chip DRC | Magic, on `lit_compac_top` and `lit_compac_top_logo_fill` | 0 violations each |
| Chip DRC | KLayout `sky130A_mr.drc` | run outside the flow, see the README |
| Chip LVS | Netgen, 313 devices on each side | 4 unmatched nets, the `VDDIO_Q`, `VSSIO_Q`, `VDDA` and `VSSA` ring buses of the clock pad, see [flow/librelane/config.yaml](../flow/librelane/config.yaml) |
| Antenna | OpenROAD | passed, no net listed |
| Timing | OpenROAD STA, three corners | closed at 40 MHz, see below |
| Packaging | `run_bondplan.py` | 32 wires, no warning |
| Macro sign-off | KLayout and Magic DRC, LVS, PEX | clean, see the macro READMEs |

### Timing

Post-route static timing analysis, worst slack per corner in nanoseconds. No path violates setup or hold, and the total negative slack is zero everywhere.

| Corner | Worst setup slack | Worst hold slack |
| --- | --- | --- |
| `nom_tt_025C_1v80` | 10.244 | 0.360 |
| `nom_ss_100C_1v60` | 8.890 | 0.956 |
| `nom_ff_n40C_1v95` | 10.826 | 0.144 |

The 130 maximum capacitance and 48 maximum slew messages in the same report are on the pad ring nets, which the tool sees without their package load.

### Packaging

| Quantity | Value |
| --- | --- |
| Bondwires | 32, one per pad |
| Wire length | 1253 to 1613 um |
| Minimum wire to wire gap | 86 um |
| Maximum landing skew | 2.2 deg |
| Pad pitch and opening | 142 um and 70.0 um |

The full table is in [packaging/result.md](../packaging/result.md).

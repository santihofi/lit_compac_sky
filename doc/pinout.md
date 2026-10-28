# Pinout

The 32 bondpads of `lit_compac_top`, the pad cell behind each one and the role it carries inside `lit_compac_core`.

The pad order per side is the one of `PAD_WEST`, `PAD_NORTH`, `PAD_SOUTH` and `PAD_EAST` in [flow/librelane/config.yaml](../flow/librelane/config.yaml), which OpenROAD places bottom to top on the vertical sides and left to right on the horizontal ones. The package pin numbers come from `PINOUT` in [packaging/config.yaml](../packaging/config.yaml), where pin 1 is the top left lead of the QFN32 and the numbering runs counter-clockwise.

Two cells of the west row are not bondpads: the ring bus connect slices, 20 um wide each. They short `VCCHIB` to `VCCD`, `VSWITCH` to `VDDIO`, `VDDA` to `VDDIO` and `VSSA` to `VSSIO` inside the ring.

## West, bottom to top (package pins 8 to 1)

| Pin | Port | Pad cell | Role in `lit_compac_core` |
| --- | --- | --- | --- |
| 8 | `output_PAD[16]` | `gpiov2_pad`, output | parity of the SRAM word at address 0 |
| 7 | `VSS` | `vssd_lvc_clamped_pad` | core ground |
| 6 | `VDD` | `vccd_lvc_clamped_pad` | 1.8 V core supply |
| - | - | `connect_vcchib_vccd_and_vswitch_vddio_slice_20um` | ring bus short, no bondpad |
| 5 | `IOVSS` | `vssio_hvc_clamped_pad` | 3.3 V pad ring ground |
| 4 | `IOVDD` | `vddio_hvc_clamped_pad` | 3.3 V pad ring supply |
| - | - | `connect_vdda_vddio_and_vssa_vssio_slice_20um` | ring bus short, no bondpad |
| 3 | `input_PAD[0]` | `gpiov2_pad`, input | enable of both counters and output enable of the bidirectional pads |
| 2 | `rst_n_PAD` | `gpiov2_pad`, input | reset, active low |
| 1 | `clk_PAD` | `gpiov2_pad`, input | 40 MHz clock |

## North, left to right (package pins 32 to 25)

| Pin | Port | Pad cell | Role in `lit_compac_core` |
| --- | --- | --- | --- |
| 32 | `output_PAD[0]` | `gpiov2_pad`, output | `counter1` bit 0 |
| 31 | `output_PAD[1]` | `gpiov2_pad`, output | `counter1` bit 1 |
| 30 | `output_PAD[2]` | `gpiov2_pad`, output | `counter1` bit 2 |
| 29 | `output_PAD[3]` | `gpiov2_pad`, output | `counter1` bit 3 |
| 28 | `bidir_PAD[0]` | `gpiov2_pad`, bidirectional | `counter1` bit 4 when enabled, otherwise input of `inverter1` channel 1 |
| 27 | `bidir_PAD[1]` | `gpiov2_pad`, bidirectional | `counter1` bit 5 when enabled, otherwise input of `inverter1` channel 2 |
| 26 | `bidir_PAD[2]` | `gpiov2_pad`, bidirectional | `counter1` bit 6 when enabled, otherwise input of `inverter1` channel 3 |
| 25 | `bidir_PAD[3]` | `gpiov2_pad`, bidirectional | `counter1` bit 7 when enabled, otherwise input of `inverter1` channel 4 |

## South, left to right (package pins 9 to 16)

| Pin | Port | Pad cell | Role in `lit_compac_core` |
| --- | --- | --- | --- |
| 9 | `output_PAD[4]` | `gpiov2_pad`, output | `counter2` bit 0 |
| 10 | `output_PAD[5]` | `gpiov2_pad`, output | `counter2` bit 1 |
| 11 | `output_PAD[6]` | `gpiov2_pad`, output | `counter2` bit 2 |
| 12 | `output_PAD[7]` | `gpiov2_pad`, output | `counter2` bit 3 |
| 13 | `output_PAD[8]` | `gpiov2_pad`, output | `counter2` bit 4 |
| 14 | `output_PAD[9]` | `gpiov2_pad`, output | `counter2` bit 5 |
| 15 | `output_PAD[10]` | `gpiov2_pad`, output | `counter2` bit 6 |
| 16 | `output_PAD[11]` | `gpiov2_pad`, output | `counter2` bit 7 |

## East, bottom to top (package pins 17 to 24)

| Pin | Port | Pad cell | Role in `lit_compac_core` |
| --- | --- | --- | --- |
| 17 | `analog_PAD[0]` | `analog_esd_pad` | input of `inverter2` channel 1, behind the ESD diodes of the pad |
| 18 | `analog_PAD[1]` | `analog_esd_pad` | input of `inverter2` channel 2, behind the ESD diodes of the pad |
| 19 | `analog_PAD[2]` | `analog_noesd_pad` | output of `inverter2` channel 1, bare pad |
| 20 | `analog_PAD[3]` | `analog_noesd_pad` | output of `inverter2` channel 2, bare pad |
| 21 | `output_PAD[12]` | `gpiov2_pad`, output | `inverter1` channel 1 output |
| 22 | `output_PAD[13]` | `gpiov2_pad`, output | `inverter1` channel 2 output |
| 23 | `output_PAD[14]` | `gpiov2_pad`, output | `inverter1` channel 3 output |
| 24 | `output_PAD[15]` | `gpiov2_pad`, output | `inverter1` channel 4 output |

## Pad cells and their settings

Every digital pad is a `sky130_ef_io__gpiov2_pad` inside one of the three wrappers of [rtl/lit_compac_top.sv](../rtl/lit_compac_top.sv). The wrappers differ in two pins only:

| Wrapper | `DM[2:0]` | `OE_N` | `INP_DIS` | Use |
| --- | --- | --- | --- | --- |
| `chip_pad_in` | `3'b001` | 1 | 0 | driver off, input buffer on |
| `chip_pad_out` | `3'b110` | 0 | 1 | strong push-pull driver, input buffer off |
| `chip_pad_bidir` | `3'b110` | `~c2p_en` | 0 | driver switched by the enable, input buffer on |

The static controls are the same in all three: `HLD_H_N`, `ENABLE_H` and `ENABLE_VDDA_H` from the pad's own `TIE_HI_ESD` output, `ENABLE_INP_H` and `ENABLE_VSWITCH_H` from `TIE_LO_ESD`, `ENABLE_VDDIO` high, and `IB_MODE_SEL`, `VTRIP_SEL`, `SLOW`, `HLD_OVR`, `ANALOG_EN`, `ANALOG_SEL` and `ANALOG_POL` low. That is CMOS input levels referenced to `VDDIO`, fast slew, no hold mode and no analog mux.

The analog pads have no controls. `analog_esd_pad` puts its ESD diodes between `P_PAD` and the supplies and brings `P_CORE` inside, `analog_noesd_pad` is the same cell without the diodes, for outputs whose macro carries its own protection. In the layout both are `SPECIAL` nets that the detailed router does not touch, they are routed with the `NDR_analog` non-default rule.

## Bonding

The die has 32 bondpads and the QFN32 has 32 leads, eight per side, so every pad is bonded to the lead facing it, one to one, with no downbonds to the exposed pad. The bond table with the wire lengths and the gaps is [packaging/result.md](../packaging/result.md), the drawing is in [packaging/render/](../packaging/render/).

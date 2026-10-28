// SPDX-FileCopyrightText: 2026 Simon Dorrer and Harald Pretl
// SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
// Description: Top-level chip wrapper.
// Instantiates the padframe, the chip core and custom logos.
// The padframe with I/O cells, power ring, corners and fillers is handled by LibreLane.
// The specifications can be found in doc/specifications.md.
// The pinout mapping can be found in doc/pinout.md.
// The floorplan can be found in doc/floorplan.md.
//
// The sky130 pads share twelve ring buses. Under USE_POWER_PINS every pad here ties them to the four chip
// supplies: VCCD and VCCHIB to VDD, VSSD to VSS, VDDIO, VDDIO_Q, VDDA and VSWITCH to IOVDD, VSSIO, VSSIO_Q
// and VSSA to IOVSS. Two connect slices short the VDDA, VSSA, VSWITCH and VCCHIB buses to their partners
// in the ring. The AMUXBUS_A and AMUXBUS_B buses stay unconnected. Without USE_POWER_PINS the supply
// pins are left open, which is how LibreLane synthesizes the design, the power connections are made by
// the flow afterwards. The pad models need the supplies to simulate, so the simulations define
// USE_POWER_PINS and drive the four rails.

`default_nettype none

// ==========================================================================
// GPIO pad wrappers, one per pad role
// ==========================================================================
// The static controls of sky130_ef_io__gpiov2_pad are tied from the pad's own TIE_HI_ESD and TIE_LO_ESD
// outputs (the levels of the 3.3 V domain) or from core-level constants, the same way the Caravel padframe
// does it:
//   HLD_H_N, ENABLE_H, ENABLE_VDDA_H = TIE_HI_ESD   normal operation, no hold, 3.3 V domain enabled
//   ENABLE_INP_H, ENABLE_VSWITCH_H  = TIE_LO_ESD   input buffer follows INP_DIS, no VSWITCH supply
//   ENABLE_VDDIO = 1                              1.8 V domain enabled
//   IB_MODE_SEL = 0, VTRIP_SEL = 0                CMOS input levels referenced to VDDIO
//   SLOW = 0, HLD_OVR = 0, ANALOG_* = 0           fast slew, no hold override, no analog mux
// DM[2:0] selects the driver: 3'b110 is the strong push-pull output, 3'b001 the input (driver off).

// Input pad: driver off, input buffer on
module chip_pad_in (
    `ifdef USE_POWER_PINS
    inout  wire VDD,
    inout  wire VSS,
    inout  wire IOVDD,
    inout  wire IOVSS,
    `endif
    inout  wire pad,
    output wire p2c
);
    wire tie_hi;
    wire tie_lo;

    sky130_ef_io__gpiov2_pad pad_cell (
        `ifdef USE_POWER_PINS
        .VCCD             (VDD),
        .VCCHIB           (VDD),
        .VSSD             (VSS),
        .VDDIO            (IOVDD),
        .VDDIO_Q          (IOVDD),
        .VDDA             (IOVDD),
        .VSWITCH          (IOVDD),
        .VSSIO            (IOVSS),
        .VSSIO_Q          (IOVSS),
        .VSSA             (IOVSS),
        `endif
        .PAD              (pad),
        .IN               (p2c),
        .IN_H             (),
        .OUT              (1'b0),
        .OE_N             (1'b1),
        .DM               (3'b001),
        .INP_DIS          (1'b0),
        .IB_MODE_SEL      (1'b0),
        .VTRIP_SEL        (1'b0),
        .SLOW             (1'b0),
        .HLD_OVR          (1'b0),
        .HLD_H_N          (tie_hi),
        .ENABLE_H         (tie_hi),
        .ENABLE_VDDA_H    (tie_hi),
        .ENABLE_INP_H     (tie_lo),
        .ENABLE_VSWITCH_H (tie_lo),
        .ENABLE_VDDIO     (1'b1),
        .ANALOG_EN        (1'b0),
        .ANALOG_SEL       (1'b0),
        .ANALOG_POL       (1'b0),
        .TIE_HI_ESD       (tie_hi),
        .TIE_LO_ESD       (tie_lo),
        .PAD_A_NOESD_H    (),
        .PAD_A_ESD_0_H    (),
        .PAD_A_ESD_1_H    (),
        .AMUXBUS_A        (),
        .AMUXBUS_B        ()
    );
endmodule

// Output pad: strong driver always on, input buffer off
module chip_pad_out (
    `ifdef USE_POWER_PINS
    inout  wire VDD,
    inout  wire VSS,
    inout  wire IOVDD,
    inout  wire IOVSS,
    `endif
    inout  wire pad,
    input  wire c2p
);
    wire tie_hi;
    wire tie_lo;

    sky130_ef_io__gpiov2_pad pad_cell (
        `ifdef USE_POWER_PINS
        .VCCD             (VDD),
        .VCCHIB           (VDD),
        .VSSD             (VSS),
        .VDDIO            (IOVDD),
        .VDDIO_Q          (IOVDD),
        .VDDA             (IOVDD),
        .VSWITCH          (IOVDD),
        .VSSIO            (IOVSS),
        .VSSIO_Q          (IOVSS),
        .VSSA             (IOVSS),
        `endif
        .PAD              (pad),
        .IN               (),
        .IN_H             (),
        .OUT              (c2p),
        .OE_N             (1'b0),
        .DM               (3'b110),
        .INP_DIS          (1'b1),
        .IB_MODE_SEL      (1'b0),
        .VTRIP_SEL        (1'b0),
        .SLOW             (1'b0),
        .HLD_OVR          (1'b0),
        .HLD_H_N          (tie_hi),
        .ENABLE_H         (tie_hi),
        .ENABLE_VDDA_H    (tie_hi),
        .ENABLE_INP_H     (tie_lo),
        .ENABLE_VSWITCH_H (tie_lo),
        .ENABLE_VDDIO     (1'b1),
        .ANALOG_EN        (1'b0),
        .ANALOG_SEL       (1'b0),
        .ANALOG_POL       (1'b0),
        .TIE_HI_ESD       (tie_hi),
        .TIE_LO_ESD       (tie_lo),
        .PAD_A_NOESD_H    (),
        .PAD_A_ESD_0_H    (),
        .PAD_A_ESD_1_H    (),
        .AMUXBUS_A        (),
        .AMUXBUS_B        ()
    );
endmodule

// Bidirectional pad: strong driver enabled by c2p_en, input buffer always on
module chip_pad_bidir (
    `ifdef USE_POWER_PINS
    inout  wire VDD,
    inout  wire VSS,
    inout  wire IOVDD,
    inout  wire IOVSS,
    `endif
    inout  wire pad,
    input  wire c2p,
    input  wire c2p_en,
    output wire p2c
);
    wire tie_hi;
    wire tie_lo;

    sky130_ef_io__gpiov2_pad pad_cell (
        `ifdef USE_POWER_PINS
        .VCCD             (VDD),
        .VCCHIB           (VDD),
        .VSSD             (VSS),
        .VDDIO            (IOVDD),
        .VDDIO_Q          (IOVDD),
        .VDDA             (IOVDD),
        .VSWITCH          (IOVDD),
        .VSSIO            (IOVSS),
        .VSSIO_Q          (IOVSS),
        .VSSA             (IOVSS),
        `endif
        .PAD              (pad),
        .IN               (p2c),
        .IN_H             (),
        .OUT              (c2p),
        .OE_N             (~c2p_en),
        .DM               (3'b110),
        .INP_DIS          (1'b0),
        .IB_MODE_SEL      (1'b0),
        .VTRIP_SEL        (1'b0),
        .SLOW             (1'b0),
        .HLD_OVR          (1'b0),
        .HLD_H_N          (tie_hi),
        .ENABLE_H         (tie_hi),
        .ENABLE_VDDA_H    (tie_hi),
        .ENABLE_INP_H     (tie_lo),
        .ENABLE_VSWITCH_H (tie_lo),
        .ENABLE_VDDIO     (1'b1),
        .ANALOG_EN        (1'b0),
        .ANALOG_SEL       (1'b0),
        .ANALOG_POL       (1'b0),
        .TIE_HI_ESD       (tie_hi),
        .TIE_LO_ESD       (tie_lo),
        .PAD_A_NOESD_H    (),
        .PAD_A_ESD_0_H    (),
        .PAD_A_ESD_1_H    (),
        .AMUXBUS_A        (),
        .AMUXBUS_B        ()
    );
endmodule

// ==========================================================================
// Chip top
// ==========================================================================
module lit_compac_top #(
    // Power / ground pads for digital core / analog front-end
    parameter int unsigned NUM_VDD_PADS    = 1,
    parameter int unsigned NUM_VSS_PADS    = 1,

    // Power / ground pads for I/O
    parameter int unsigned NUM_IOVDD_PADS  = 1,
    parameter int unsigned NUM_IOVSS_PADS  = 1,

    // Signal pads
    parameter int unsigned NUM_INPUT_PADS  = 1,  // excluding clock and reset pads
    parameter int unsigned NUM_OUTPUT_PADS = 17,
    parameter int unsigned NUM_BIDIR_PADS  = 4,
    parameter int unsigned NUM_ANALOG_PADS = 4   // the lower half with ESD protection (inputs), the upper half bare (outputs)
) (
    `ifdef USE_POWER_PINS
    inout wire IOVDD,
    inout wire IOVSS,
    inout wire VDD,
    inout wire VSS,
    `endif
    inout wire                       clk_PAD,
    inout wire                       rst_n_PAD,
    inout wire [NUM_INPUT_PADS-1 :0] input_PAD,
    inout wire [NUM_OUTPUT_PADS-1:0] output_PAD,
    inout wire [NUM_BIDIR_PADS-1 :0] bidir_PAD,
    inout wire [NUM_ANALOG_PADS-1:0] analog_PAD
);

    // ======================================================
    // Internal nets
    // ======================================================
    // Clock
    logic                       clk_PAD2CORE;

    // Reset
    logic                       rst_n_PAD2CORE;

    // Inputs
    logic [NUM_INPUT_PADS-1 :0] input_PAD2CORE;

    // Outputs
    logic [NUM_OUTPUT_PADS-1:0] output_CORE2PAD;

    // Bidirectionals
    logic [NUM_BIDIR_PADS-1 :0] bidir_PAD2CORE;
    logic [NUM_BIDIR_PADS-1 :0] bidir_CORE2PAD;
    logic [NUM_BIDIR_PADS-1 :0] bidir_CORE2PAD_OE;

    // Analog (must remain wire: connected to inout pad/macro ports)
    wire  [NUM_ANALOG_PADS-1:0] analog_PADESD;
    wire  [NUM_ANALOG_PADS-1:0] analog_PADBARE;
    // ======================================================

    // ======================================================
    // VDD - PAD INSTANCES
    // ======================================================
    generate
        for (genvar i = 0; i < NUM_VDD_PADS; i++) begin : g_vdd_pads
            (* keep *)
            sky130_ef_io__vccd_lvc_clamped_pad vdd_pad (
                `ifdef USE_POWER_PINS
                .VCCD_PAD  (VDD),
                .VCCD      (VDD),
                .VCCHIB    (VDD),
                .VSSD      (VSS),
                .VDDIO     (IOVDD),
                .VDDIO_Q   (IOVDD),
                .VDDA      (IOVDD),
                .VSWITCH   (IOVDD),
                .VSSIO     (IOVSS),
                .VSSIO_Q   (IOVSS),
                .VSSA      (IOVSS),
                `endif
                .AMUXBUS_A (),
                .AMUXBUS_B ()
            );
        end
    endgenerate
    // ======================================================

    // ======================================================
    // VSS - PAD INSTANCES
    // ======================================================
    generate
        for (genvar i = 0; i < NUM_VSS_PADS; i++) begin : g_vss_pads
            (* keep *)
            sky130_ef_io__vssd_lvc_clamped_pad vss_pad (
                `ifdef USE_POWER_PINS
                .VSSD_PAD  (VSS),
                .VCCD      (VDD),
                .VCCHIB    (VDD),
                .VSSD      (VSS),
                .VDDIO     (IOVDD),
                .VDDIO_Q   (IOVDD),
                .VDDA      (IOVDD),
                .VSWITCH   (IOVDD),
                .VSSIO     (IOVSS),
                .VSSIO_Q   (IOVSS),
                .VSSA      (IOVSS),
                `endif
                .AMUXBUS_A (),
                .AMUXBUS_B ()
            );
        end
    endgenerate
    // ======================================================

    // ======================================================
    // IOVDD - PAD INSTANCES
    // ======================================================
    generate
        for (genvar i = 0; i < NUM_IOVDD_PADS; i++) begin : g_iovdd_pads
            (* keep *)
            sky130_ef_io__vddio_hvc_clamped_pad iovdd_pad (
                `ifdef USE_POWER_PINS
                .VDDIO_PAD (IOVDD),
                .VCCD      (VDD),
                .VCCHIB    (VDD),
                .VSSD      (VSS),
                .VDDIO     (IOVDD),
                .VDDIO_Q   (IOVDD),
                .VDDA      (IOVDD),
                .VSWITCH   (IOVDD),
                .VSSIO     (IOVSS),
                .VSSIO_Q   (IOVSS),
                .VSSA      (IOVSS),
                `endif
                .AMUXBUS_A (),
                .AMUXBUS_B ()
            );
        end
    endgenerate
    // ======================================================

    // ======================================================
    // IOVSS - PAD INSTANCES
    // ======================================================
    generate
        for (genvar i = 0; i < NUM_IOVSS_PADS; i++) begin : g_iovss_pads
            (* keep *)
            sky130_ef_io__vssio_hvc_clamped_pad iovss_pad (
                `ifdef USE_POWER_PINS
                .VSSIO_PAD (IOVSS),
                .VCCD      (VDD),
                .VCCHIB    (VDD),
                .VSSD      (VSS),
                .VDDIO     (IOVDD),
                .VDDIO_Q   (IOVDD),
                .VDDA      (IOVDD),
                .VSWITCH   (IOVDD),
                .VSSIO     (IOVSS),
                .VSSIO_Q   (IOVSS),
                .VSSA      (IOVSS),
                `endif
                .AMUXBUS_A (),
                .AMUXBUS_B ()
            );
        end
    endgenerate
    // ======================================================

    // ======================================================
    // RING BUS CONNECT SLICES
    // ======================================================
    // VCCHIB to VCCD and VSWITCH to VDDIO
    (* keep *)
    sky130_ef_io__connect_vcchib_vccd_and_vswitch_vddio_slice_20um connect_vcchib_vswitch (
        `ifdef USE_POWER_PINS
        .VCCHIB  (VDD),
        .VCCD    (VDD),
        .VSWITCH (IOVDD),
        .VDDIO   (IOVDD)
        `endif
    );

    // VDDA to VDDIO and VSSA to VSSIO
    (* keep *)
    sky130_ef_io__connect_vdda_vddio_and_vssa_vssio_slice_20um connect_vdda_vssa (
        `ifdef USE_POWER_PINS
        .VDDA  (IOVDD),
        .VDDIO (IOVDD),
        .VSSA  (IOVSS),
        .VSSIO (IOVSS)
        `endif
    );
    // ======================================================

    // ======================================================
    // CLOCK - PAD INSTANCE
    // ======================================================
    chip_pad_in clk_pad (
        `ifdef USE_POWER_PINS
        .VDD   (VDD),
        .VSS   (VSS),
        .IOVDD (IOVDD),
        .IOVSS (IOVSS),
        `endif
        .p2c   (clk_PAD2CORE),
        .pad   (clk_PAD)
    );
    // ======================================================

    // ======================================================
    // RESET - PAD INSTANCE (active low)
    // ======================================================
    chip_pad_in rst_n_pad (
        `ifdef USE_POWER_PINS
        .VDD   (VDD),
        .VSS   (VSS),
        .IOVDD (IOVDD),
        .IOVSS (IOVSS),
        `endif
        .p2c   (rst_n_PAD2CORE),
        .pad   (rst_n_PAD)
    );
    // ======================================================

    // ======================================================
    // SIGNAL INPUTS - PAD INSTANCES
    // ======================================================
    generate
        for (genvar i = 0; i < NUM_INPUT_PADS; i++) begin : g_inputs
            chip_pad_in input_pad (
                `ifdef USE_POWER_PINS
                .VDD   (VDD),
                .VSS   (VSS),
                .IOVDD (IOVDD),
                .IOVSS (IOVSS),
                `endif
                .p2c   (input_PAD2CORE[i]),
                .pad   (input_PAD[i])
            );
        end
    endgenerate
    // ======================================================

    // ======================================================
    // SIGNAL OUTPUTS - PAD INSTANCES
    // ======================================================
    generate
        for (genvar i = 0; i < NUM_OUTPUT_PADS; i++) begin : g_outputs
            chip_pad_out output_pad (
                `ifdef USE_POWER_PINS
                .VDD   (VDD),
                .VSS   (VSS),
                .IOVDD (IOVDD),
                .IOVSS (IOVSS),
                `endif
                .c2p   (output_CORE2PAD[i]),
                .pad   (output_PAD[i])
            );
        end
    endgenerate
    // ======================================================

    // ======================================================
    // SIGNAL BIDIRECTIONALS - PAD INSTANCES
    // ======================================================
    generate
        for (genvar i = 0; i < NUM_BIDIR_PADS; i++) begin : g_bidirs
            chip_pad_bidir bidir_pad (
                `ifdef USE_POWER_PINS
                .VDD    (VDD),
                .VSS    (VSS),
                .IOVDD  (IOVDD),
                .IOVSS  (IOVSS),
                `endif
                .c2p    (bidir_CORE2PAD[i]),
                .c2p_en (bidir_CORE2PAD_OE[i]),
                .p2c    (bidir_PAD2CORE[i]),
                .pad    (bidir_PAD[i])
            );
        end
    endgenerate
    // ======================================================

    // ======================================================
    // SIGNAL ANALOG - PAD INSTANCES
    // ======================================================
    // The lower half are analog inputs behind the pad's ESD diodes, the upper half are bare pads for the
    // analog outputs, whose macro carries its own protection.
    generate
        for (genvar i = 0; i < NUM_ANALOG_PADS; i++) begin : g_analogs
            if (i < NUM_ANALOG_PADS / 2) begin : g_esd
                (* keep *)
                sky130_ef_io__analog_esd_pad analog_pad (
                    `ifdef USE_POWER_PINS
                    .VCCD      (VDD),
                    .VCCHIB    (VDD),
                    .VSSD      (VSS),
                    .VDDIO     (IOVDD),
                    .VDDIO_Q   (IOVDD),
                    .VDDA      (IOVDD),
                    .VSWITCH   (IOVDD),
                    .VSSIO     (IOVSS),
                    .VSSIO_Q   (IOVSS),
                    .VSSA      (IOVSS),
                    `endif
                    // SPECIAL net in OpenROAD; ignored during detailed routing -> analog_PADESD.
                    .P_PAD     (analog_PAD[i]),
                    .P_CORE    (analog_PADESD[i]),
                    .AMUXBUS_A (),
                    .AMUXBUS_B ()
                );
            end else begin : g_noesd
                (* keep *)
                sky130_ef_io__analog_noesd_pad analog_pad (
                    `ifdef USE_POWER_PINS
                    .VCCD      (VDD),
                    .VCCHIB    (VDD),
                    .VSSD      (VSS),
                    .VDDIO     (IOVDD),
                    .VDDIO_Q   (IOVDD),
                    .VDDA      (IOVDD),
                    .VSWITCH   (IOVDD),
                    .VSSIO     (IOVSS),
                    .VSSIO_Q   (IOVSS),
                    .VSSA      (IOVSS),
                    `endif
                    // SPECIAL net in OpenROAD; ignored during detailed routing -> analog_PADBARE.
                    .P_PAD     (analog_PAD[i]),
                    .P_CORE    (analog_PADBARE[i]),
                    .AMUXBUS_A (),
                    .AMUXBUS_B ()
                );
            end
        end
    endgenerate
    // ======================================================

    // ======================================================
    // CORE DESIGN
    // ======================================================
    lit_compac_core #(
        .NUM_INPUT_PADS  (NUM_INPUT_PADS),
        .NUM_OUTPUT_PADS (NUM_OUTPUT_PADS),
        .NUM_BIDIR_PADS  (NUM_BIDIR_PADS),
        .NUM_ANALOG_PADS (NUM_ANALOG_PADS)
    ) i_lit_compac_core (
        `ifdef USE_POWER_PINS
        .VDD            (VDD),
        .VSS            (VSS),
        `endif

        .clk            (clk_PAD2CORE),
        .rst_n          (rst_n_PAD2CORE),

        .input_in       (input_PAD2CORE),

        .output_out     (output_CORE2PAD),
        .bidir_in       (bidir_PAD2CORE),
        .bidir_out      (bidir_CORE2PAD),
        .bidir_oe       (bidir_CORE2PAD_OE),

        .analog_padesd  (analog_PADESD),
        .analog_padbare (analog_PADBARE)
    );
    // ======================================================

    // ======================================================
    // LOGOS
    // ======================================================
    // JKU logo
    (* keep *)
    sky130_ip__jku jku_logo ();

    // JKU names
    (* keep *)
    sky130_ip__jku_names jku_names ();
    // ======================================================

endmodule

`default_nettype wire

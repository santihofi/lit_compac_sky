// SPDX-FileCopyrightText: 2026 Simon Dorrer and Harald Pretl
// SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
// Description: Top-level chip core.
// Instantiates and connects the digital and analog macros.

`default_nettype none

module lit_compac_core #(
    parameter int unsigned NUM_INPUT_PADS,
    parameter int unsigned NUM_OUTPUT_PADS,
    parameter int unsigned NUM_BIDIR_PADS,
    parameter int unsigned NUM_ANALOG_PADS
)(
    `ifdef USE_POWER_PINS
    inout  wire VDD,
    inout  wire VSS,
    `endif

    input  logic clk,       // clock
    input  logic rst_n,     // reset (active low)

    input  logic [NUM_INPUT_PADS-1 :0] input_in,        // Input value
    output logic [NUM_OUTPUT_PADS-1:0] output_out,      // Output value
    input  logic [NUM_BIDIR_PADS-1 :0] bidir_in,        // Bidir input value
    output logic [NUM_BIDIR_PADS-1 :0] bidir_out,       // Bidir output value
    output logic [NUM_BIDIR_PADS-1 :0] bidir_oe,        // Bidir output enable

    inout  wire  [NUM_ANALOG_PADS-1:0] analog_padesd,   // Analog (behind the ESD diodes of the pad, the lower half)
    inout  wire  [NUM_ANALOG_PADS-1:0] analog_padbare   // Analog (bare pad connection, the upper half)
);

    // ======================================================
    // Input Assignments
    // ======================================================
    logic enable;
    assign enable = input_in[0];

    // Inverter 1 (vin* are inout ports on inverter_top -> must be wire)
    wire inv1_din1 = bidir_in[0];
    wire inv1_din2 = bidir_in[1];
    wire inv1_din3 = bidir_in[2];
    wire inv1_din4 = bidir_in[3];

    // Inverter 2 (analog inputs tapped from the pad ring)
    wire inv2_vin1 = analog_padesd[0];
    wire inv2_vin2 = analog_padesd[1];
    // ======================================================

    // ======================================================
    // Counter 1 (digital macro)
    // ======================================================
    logic [7:0] counter1_value;

    counter_top counter1 (
        `ifdef USE_POWER_PINS
        .VDD(VDD),
        .VSS(VSS),
        `endif
        .clock_i        (clk),
        .reset_n_i      (rst_n),
        .enable_i       (enable),
        .counter_value_o(counter1_value)
    );
    // ======================================================

    // ======================================================
    // Counter 2 (digital macro)
    // ======================================================
    logic [7:0] counter2_value;

    counter_top counter2 (
        `ifdef USE_POWER_PINS
        .VDD(VDD),
        .VSS(VSS),
        `endif
        .clock_i        (clk),
        .reset_n_i      (rst_n),
        .enable_i       (enable),
        .counter_value_o(counter2_value)
    );
    // ======================================================

    // ======================================================
    // Inverter 1 (analog macro, used as digital inverter)
    // ======================================================
    wire inv1_dout1;
    wire inv1_dout2;
    wire inv1_dout3;
    wire inv1_dout4;

    inverter_top inverter1 (
        `ifdef USE_POWER_PINS
        .VDD  (VDD),
        .VSS  (VSS),
        `endif
        .vin1 (inv1_din1),
        .vin2 (inv1_din2),
        .vin3 (inv1_din3),
        .vin4 (inv1_din4),
        .vout1(inv1_dout1),
        .vout2(inv1_dout2),
        .vout3(inv1_dout3),
        .vout4(inv1_dout4)
    );
    // ======================================================

    // ======================================================
    // Inverter 2 (analog macro)
    // ======================================================
    `ifdef USE_POWER_PINS
    wire vss_tie = VSS;
    `else
    wire vss_tie = 1'b0;
    `endif

    wire inv2_vout1;
    wire inv2_vout2;

    inverter_top inverter2 (
        `ifdef USE_POWER_PINS
        .VDD  (VDD),
        .VSS  (VSS),
        `endif
        .vin1 (inv2_vin1),
        .vin2 (inv2_vin2),
        .vin3 (vss_tie),
        .vin4 (vss_tie),
        .vout1(inv2_vout1),
        .vout2(inv2_vout2),
        .vout3(vss_tie),
        .vout4(vss_tie)
    );
    // ======================================================

    // ======================================================
    // 256 x 32 SRAM (digital macro, OpenRAM sky130_sram_1kbyte_1rw1r_32x256_8)
    // ======================================================
    // Port 0 reads address 0 on every clock, port 1 is deselected.
    logic [31:0] sram_0_out;

    sky130_sram_1kbyte_1rw1r_32x256_8 sram_0 (
        `ifdef USE_POWER_PINS
        .vccd1 (VDD),
        .vssd1 (VSS),
        `endif
        // Port 0: read/write
        .clk0   (clk),
        .csb0   (1'b0),       // chip select, active low
        .web0   (1'b1),       // write enable, active low: read only
        .wmask0 ('0),
        .addr0  ('0),
        .din0   ('0),
        .dout0  (sram_0_out),
        // Port 1: read, unused
        .clk1   (clk),
        .csb1   (1'b1),
        .addr1  ('0),
        .dout1  ()
    );
    // ======================================================

    // ======================================================
    // Output Assignments
    // ======================================================
    // Digital outputs
    // Counter 1
    assign output_out[0]  = counter1_value[0];
    assign output_out[1]  = counter1_value[1];
    assign output_out[2]  = counter1_value[2];
    assign output_out[3]  = counter1_value[3];

    // Counter 2
    assign output_out[4]  = counter2_value[0];
    assign output_out[5]  = counter2_value[1];
    assign output_out[6]  = counter2_value[2];
    assign output_out[7]  = counter2_value[3];
    assign output_out[8]  = counter2_value[4];
    assign output_out[9]  = counter2_value[5];
    assign output_out[10] = counter2_value[6];
    assign output_out[11] = counter2_value[7];

    // Inverter 1
    assign output_out[12] = inv1_dout1;
    assign output_out[13] = inv1_dout2;
    assign output_out[14] = inv1_dout3;
    assign output_out[15] = inv1_dout4;

    // SRAM
    // Reduce the 32-bit SRAM output to a single bit by computing the parity.
    // sram_parity = 1 when an odd number of bits in sram_0_out are 1.
    // sram_parity = 0 when an even number of bits in sram_0_out are 1.
    // The read data of the OpenRAM macro changes on the falling clock edge, so the parity is registered
    // before it leaves the chip: the combinational path from the macro to the pad would otherwise have
    // half a clock period for the XOR tree and the pad driver, which the slow corner does not meet.
    logic sram_parity;

    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            sram_parity <= 1'b0;
        end else begin
            sram_parity <= ^sram_0_out;
        end
    end

    assign output_out[16] = sram_parity;

    // Digital bidirectionals (output side)
    // Bidir output enable: drive when `enable` is high (counter visible),
    // float as input when low (so external stimuli can drive inverter1).
    assign bidir_out[0] = counter1_value[4];
    assign bidir_oe[0]  = enable;

    assign bidir_out[1] = counter1_value[5];
    assign bidir_oe[1]  = enable;

    assign bidir_out[2] = counter1_value[6];
    assign bidir_oe[2]  = enable;

    assign bidir_out[3] = counter1_value[7];
    assign bidir_oe[3]  = enable;

    // Analog outputs
    assign analog_padbare[2] = inv2_vout1;
    assign analog_padbare[3] = inv2_vout2;
    // ======================================================
endmodule

`default_nettype wire

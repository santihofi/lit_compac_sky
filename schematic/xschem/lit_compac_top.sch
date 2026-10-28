v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {lit_compac_top: padframe and core assembly} 0 -60 0 0 0.8 0.8 {}
T {Every pin carries a label instead of a wire. The SRAM macro is left out, its OpenRAM SPICE model is a transistor netlist the top-level transient testbench does not need.} 0 -30 0 0 0.4 0.4 {}
C {chip_pad_in.sym} 400 -400 0 0 {name=clk_pad}
C {lab_pin.sym} 310 -480 0 0 {name=l1 lab=VDD}
C {lab_pin.sym} 340 -480 0 0 {name=l2 lab=VSS}
C {lab_pin.sym} 370 -480 0 0 {name=l3 lab=IOVDD}
C {lab_pin.sym} 400 -480 0 0 {name=l4 lab=IOVSS}
C {lab_pin.sym} 310 -320 0 0 {name=l5 lab=clk_PAD}
C {lab_pin.sym} 540 -440 2 0 {name=l6 lab=clk_PAD2CORE}
C {chip_pad_in.sym} 400 -660 0 0 {name=rst_n_pad}
C {lab_pin.sym} 310 -740 0 0 {name=l7 lab=VDD}
C {lab_pin.sym} 340 -740 0 0 {name=l8 lab=VSS}
C {lab_pin.sym} 370 -740 0 0 {name=l9 lab=IOVDD}
C {lab_pin.sym} 400 -740 0 0 {name=l10 lab=IOVSS}
C {lab_pin.sym} 310 -580 0 0 {name=l11 lab=rst_n_PAD}
C {lab_pin.sym} 540 -700 2 0 {name=l12 lab=rst_n_PAD2CORE}
C {chip_pad_in.sym} 400 -920 0 0 {name=input_pad0}
C {lab_pin.sym} 310 -1000 0 0 {name=l13 lab=VDD}
C {lab_pin.sym} 340 -1000 0 0 {name=l14 lab=VSS}
C {lab_pin.sym} 370 -1000 0 0 {name=l15 lab=IOVDD}
C {lab_pin.sym} 400 -1000 0 0 {name=l16 lab=IOVSS}
C {lab_pin.sym} 310 -840 0 0 {name=l17 lab=input_PAD[0]}
C {lab_pin.sym} 540 -960 2 0 {name=l18 lab=input_PAD2CORE[0]}
C {chip_pad_out.sym} 400 -1180 0 0 {name=output_pad0}
C {lab_pin.sym} 310 -1260 0 0 {name=l19 lab=VDD}
C {lab_pin.sym} 340 -1260 0 0 {name=l20 lab=VSS}
C {lab_pin.sym} 370 -1260 0 0 {name=l21 lab=IOVDD}
C {lab_pin.sym} 400 -1260 0 0 {name=l22 lab=IOVSS}
C {lab_pin.sym} 310 -1100 0 0 {name=l23 lab=output_PAD[0]}
C {lab_pin.sym} 260 -1220 0 0 {name=l24 lab=output_CORE2PAD[0]}
C {chip_pad_out.sym} 400 -1440 0 0 {name=output_pad1}
C {lab_pin.sym} 310 -1520 0 0 {name=l25 lab=VDD}
C {lab_pin.sym} 340 -1520 0 0 {name=l26 lab=VSS}
C {lab_pin.sym} 370 -1520 0 0 {name=l27 lab=IOVDD}
C {lab_pin.sym} 400 -1520 0 0 {name=l28 lab=IOVSS}
C {lab_pin.sym} 310 -1360 0 0 {name=l29 lab=output_PAD[1]}
C {lab_pin.sym} 260 -1480 0 0 {name=l30 lab=output_CORE2PAD[1]}
C {chip_pad_out.sym} 400 -1700 0 0 {name=output_pad2}
C {lab_pin.sym} 310 -1780 0 0 {name=l31 lab=VDD}
C {lab_pin.sym} 340 -1780 0 0 {name=l32 lab=VSS}
C {lab_pin.sym} 370 -1780 0 0 {name=l33 lab=IOVDD}
C {lab_pin.sym} 400 -1780 0 0 {name=l34 lab=IOVSS}
C {lab_pin.sym} 310 -1620 0 0 {name=l35 lab=output_PAD[2]}
C {lab_pin.sym} 260 -1740 0 0 {name=l36 lab=output_CORE2PAD[2]}
C {chip_pad_out.sym} 400 -1960 0 0 {name=output_pad3}
C {lab_pin.sym} 310 -2040 0 0 {name=l37 lab=VDD}
C {lab_pin.sym} 340 -2040 0 0 {name=l38 lab=VSS}
C {lab_pin.sym} 370 -2040 0 0 {name=l39 lab=IOVDD}
C {lab_pin.sym} 400 -2040 0 0 {name=l40 lab=IOVSS}
C {lab_pin.sym} 310 -1880 0 0 {name=l41 lab=output_PAD[3]}
C {lab_pin.sym} 260 -2000 0 0 {name=l42 lab=output_CORE2PAD[3]}
C {chip_pad_out.sym} 400 -2220 0 0 {name=output_pad4}
C {lab_pin.sym} 310 -2300 0 0 {name=l43 lab=VDD}
C {lab_pin.sym} 340 -2300 0 0 {name=l44 lab=VSS}
C {lab_pin.sym} 370 -2300 0 0 {name=l45 lab=IOVDD}
C {lab_pin.sym} 400 -2300 0 0 {name=l46 lab=IOVSS}
C {lab_pin.sym} 310 -2140 0 0 {name=l47 lab=output_PAD[4]}
C {lab_pin.sym} 260 -2260 0 0 {name=l48 lab=output_CORE2PAD[4]}
C {chip_pad_out.sym} 1100 -400 0 0 {name=output_pad5}
C {lab_pin.sym} 1010 -480 0 0 {name=l49 lab=VDD}
C {lab_pin.sym} 1040 -480 0 0 {name=l50 lab=VSS}
C {lab_pin.sym} 1070 -480 0 0 {name=l51 lab=IOVDD}
C {lab_pin.sym} 1100 -480 0 0 {name=l52 lab=IOVSS}
C {lab_pin.sym} 1010 -320 0 0 {name=l53 lab=output_PAD[5]}
C {lab_pin.sym} 960 -440 0 0 {name=l54 lab=output_CORE2PAD[5]}
C {chip_pad_out.sym} 1100 -660 0 0 {name=output_pad6}
C {lab_pin.sym} 1010 -740 0 0 {name=l55 lab=VDD}
C {lab_pin.sym} 1040 -740 0 0 {name=l56 lab=VSS}
C {lab_pin.sym} 1070 -740 0 0 {name=l57 lab=IOVDD}
C {lab_pin.sym} 1100 -740 0 0 {name=l58 lab=IOVSS}
C {lab_pin.sym} 1010 -580 0 0 {name=l59 lab=output_PAD[6]}
C {lab_pin.sym} 960 -700 0 0 {name=l60 lab=output_CORE2PAD[6]}
C {chip_pad_out.sym} 1100 -920 0 0 {name=output_pad7}
C {lab_pin.sym} 1010 -1000 0 0 {name=l61 lab=VDD}
C {lab_pin.sym} 1040 -1000 0 0 {name=l62 lab=VSS}
C {lab_pin.sym} 1070 -1000 0 0 {name=l63 lab=IOVDD}
C {lab_pin.sym} 1100 -1000 0 0 {name=l64 lab=IOVSS}
C {lab_pin.sym} 1010 -840 0 0 {name=l65 lab=output_PAD[7]}
C {lab_pin.sym} 960 -960 0 0 {name=l66 lab=output_CORE2PAD[7]}
C {chip_pad_out.sym} 1100 -1180 0 0 {name=output_pad8}
C {lab_pin.sym} 1010 -1260 0 0 {name=l67 lab=VDD}
C {lab_pin.sym} 1040 -1260 0 0 {name=l68 lab=VSS}
C {lab_pin.sym} 1070 -1260 0 0 {name=l69 lab=IOVDD}
C {lab_pin.sym} 1100 -1260 0 0 {name=l70 lab=IOVSS}
C {lab_pin.sym} 1010 -1100 0 0 {name=l71 lab=output_PAD[8]}
C {lab_pin.sym} 960 -1220 0 0 {name=l72 lab=output_CORE2PAD[8]}
C {chip_pad_out.sym} 1100 -1440 0 0 {name=output_pad9}
C {lab_pin.sym} 1010 -1520 0 0 {name=l73 lab=VDD}
C {lab_pin.sym} 1040 -1520 0 0 {name=l74 lab=VSS}
C {lab_pin.sym} 1070 -1520 0 0 {name=l75 lab=IOVDD}
C {lab_pin.sym} 1100 -1520 0 0 {name=l76 lab=IOVSS}
C {lab_pin.sym} 1010 -1360 0 0 {name=l77 lab=output_PAD[9]}
C {lab_pin.sym} 960 -1480 0 0 {name=l78 lab=output_CORE2PAD[9]}
C {chip_pad_out.sym} 1100 -1700 0 0 {name=output_pad10}
C {lab_pin.sym} 1010 -1780 0 0 {name=l79 lab=VDD}
C {lab_pin.sym} 1040 -1780 0 0 {name=l80 lab=VSS}
C {lab_pin.sym} 1070 -1780 0 0 {name=l81 lab=IOVDD}
C {lab_pin.sym} 1100 -1780 0 0 {name=l82 lab=IOVSS}
C {lab_pin.sym} 1010 -1620 0 0 {name=l83 lab=output_PAD[10]}
C {lab_pin.sym} 960 -1740 0 0 {name=l84 lab=output_CORE2PAD[10]}
C {chip_pad_out.sym} 1100 -1960 0 0 {name=output_pad11}
C {lab_pin.sym} 1010 -2040 0 0 {name=l85 lab=VDD}
C {lab_pin.sym} 1040 -2040 0 0 {name=l86 lab=VSS}
C {lab_pin.sym} 1070 -2040 0 0 {name=l87 lab=IOVDD}
C {lab_pin.sym} 1100 -2040 0 0 {name=l88 lab=IOVSS}
C {lab_pin.sym} 1010 -1880 0 0 {name=l89 lab=output_PAD[11]}
C {lab_pin.sym} 960 -2000 0 0 {name=l90 lab=output_CORE2PAD[11]}
C {chip_pad_out.sym} 1100 -2220 0 0 {name=output_pad12}
C {lab_pin.sym} 1010 -2300 0 0 {name=l91 lab=VDD}
C {lab_pin.sym} 1040 -2300 0 0 {name=l92 lab=VSS}
C {lab_pin.sym} 1070 -2300 0 0 {name=l93 lab=IOVDD}
C {lab_pin.sym} 1100 -2300 0 0 {name=l94 lab=IOVSS}
C {lab_pin.sym} 1010 -2140 0 0 {name=l95 lab=output_PAD[12]}
C {lab_pin.sym} 960 -2260 0 0 {name=l96 lab=output_CORE2PAD[12]}
C {chip_pad_out.sym} 1800 -400 0 0 {name=output_pad13}
C {lab_pin.sym} 1710 -480 0 0 {name=l97 lab=VDD}
C {lab_pin.sym} 1740 -480 0 0 {name=l98 lab=VSS}
C {lab_pin.sym} 1770 -480 0 0 {name=l99 lab=IOVDD}
C {lab_pin.sym} 1800 -480 0 0 {name=l100 lab=IOVSS}
C {lab_pin.sym} 1710 -320 0 0 {name=l101 lab=output_PAD[13]}
C {lab_pin.sym} 1660 -440 0 0 {name=l102 lab=output_CORE2PAD[13]}
C {chip_pad_out.sym} 1800 -660 0 0 {name=output_pad14}
C {lab_pin.sym} 1710 -740 0 0 {name=l103 lab=VDD}
C {lab_pin.sym} 1740 -740 0 0 {name=l104 lab=VSS}
C {lab_pin.sym} 1770 -740 0 0 {name=l105 lab=IOVDD}
C {lab_pin.sym} 1800 -740 0 0 {name=l106 lab=IOVSS}
C {lab_pin.sym} 1710 -580 0 0 {name=l107 lab=output_PAD[14]}
C {lab_pin.sym} 1660 -700 0 0 {name=l108 lab=output_CORE2PAD[14]}
C {chip_pad_out.sym} 1800 -920 0 0 {name=output_pad15}
C {lab_pin.sym} 1710 -1000 0 0 {name=l109 lab=VDD}
C {lab_pin.sym} 1740 -1000 0 0 {name=l110 lab=VSS}
C {lab_pin.sym} 1770 -1000 0 0 {name=l111 lab=IOVDD}
C {lab_pin.sym} 1800 -1000 0 0 {name=l112 lab=IOVSS}
C {lab_pin.sym} 1710 -840 0 0 {name=l113 lab=output_PAD[15]}
C {lab_pin.sym} 1660 -960 0 0 {name=l114 lab=output_CORE2PAD[15]}
C {chip_pad_out.sym} 1800 -1180 0 0 {name=output_pad16}
C {lab_pin.sym} 1710 -1260 0 0 {name=l115 lab=VDD}
C {lab_pin.sym} 1740 -1260 0 0 {name=l116 lab=VSS}
C {lab_pin.sym} 1770 -1260 0 0 {name=l117 lab=IOVDD}
C {lab_pin.sym} 1800 -1260 0 0 {name=l118 lab=IOVSS}
C {lab_pin.sym} 1710 -1100 0 0 {name=l119 lab=output_PAD[16]}
C {lab_pin.sym} 1660 -1220 0 0 {name=l120 lab=output_CORE2PAD[16]}
C {chip_pad_bidir.sym} 1800 -1440 0 0 {name=bidir_pad0}
C {lab_pin.sym} 1710 -1520 0 0 {name=l121 lab=VDD}
C {lab_pin.sym} 1740 -1520 0 0 {name=l122 lab=VSS}
C {lab_pin.sym} 1770 -1520 0 0 {name=l123 lab=IOVDD}
C {lab_pin.sym} 1800 -1520 0 0 {name=l124 lab=IOVSS}
C {lab_pin.sym} 1710 -1360 0 0 {name=l125 lab=bidir_PAD[0]}
C {lab_pin.sym} 1660 -1480 0 0 {name=l126 lab=bidir_CORE2PAD[0]}
C {lab_pin.sym} 1660 -1460 0 0 {name=l127 lab=input_PAD2CORE[0]}
C {lab_pin.sym} 1940 -1480 2 0 {name=l128 lab=bidir_PAD2CORE[0]}
C {chip_pad_bidir.sym} 1800 -1700 0 0 {name=bidir_pad1}
C {lab_pin.sym} 1710 -1780 0 0 {name=l129 lab=VDD}
C {lab_pin.sym} 1740 -1780 0 0 {name=l130 lab=VSS}
C {lab_pin.sym} 1770 -1780 0 0 {name=l131 lab=IOVDD}
C {lab_pin.sym} 1800 -1780 0 0 {name=l132 lab=IOVSS}
C {lab_pin.sym} 1710 -1620 0 0 {name=l133 lab=bidir_PAD[1]}
C {lab_pin.sym} 1660 -1740 0 0 {name=l134 lab=bidir_CORE2PAD[1]}
C {lab_pin.sym} 1660 -1720 0 0 {name=l135 lab=input_PAD2CORE[0]}
C {lab_pin.sym} 1940 -1740 2 0 {name=l136 lab=bidir_PAD2CORE[1]}
C {chip_pad_bidir.sym} 1800 -1960 0 0 {name=bidir_pad2}
C {lab_pin.sym} 1710 -2040 0 0 {name=l137 lab=VDD}
C {lab_pin.sym} 1740 -2040 0 0 {name=l138 lab=VSS}
C {lab_pin.sym} 1770 -2040 0 0 {name=l139 lab=IOVDD}
C {lab_pin.sym} 1800 -2040 0 0 {name=l140 lab=IOVSS}
C {lab_pin.sym} 1710 -1880 0 0 {name=l141 lab=bidir_PAD[2]}
C {lab_pin.sym} 1660 -2000 0 0 {name=l142 lab=bidir_CORE2PAD[2]}
C {lab_pin.sym} 1660 -1980 0 0 {name=l143 lab=input_PAD2CORE[0]}
C {lab_pin.sym} 1940 -2000 2 0 {name=l144 lab=bidir_PAD2CORE[2]}
C {chip_pad_bidir.sym} 1800 -2220 0 0 {name=bidir_pad3}
C {lab_pin.sym} 1710 -2300 0 0 {name=l145 lab=VDD}
C {lab_pin.sym} 1740 -2300 0 0 {name=l146 lab=VSS}
C {lab_pin.sym} 1770 -2300 0 0 {name=l147 lab=IOVDD}
C {lab_pin.sym} 1800 -2300 0 0 {name=l148 lab=IOVSS}
C {lab_pin.sym} 1710 -2140 0 0 {name=l149 lab=bidir_PAD[3]}
C {lab_pin.sym} 1660 -2260 0 0 {name=l150 lab=bidir_CORE2PAD[3]}
C {lab_pin.sym} 1660 -2240 0 0 {name=l151 lab=input_PAD2CORE[0]}
C {lab_pin.sym} 1940 -2260 2 0 {name=l152 lab=bidir_PAD2CORE[3]}
C {sky130_ef_io/sky130_ef_io__analog_esd_pad.sym} 2500 -400 0 0 {name=analog_pad0}
C {lab_pin.sym} 2610 -420 2 0 {name=l153 lab=analog_PADESD[0]}
C {lab_pin.sym} 2430 -340 0 0 {name=l154 lab=IOVSS}
C {lab_pin.sym} 2450 -340 0 0 {name=l155 lab=VSS}
C {lab_pin.sym} 2430 -460 0 0 {name=l156 lab=AMUXBUS_B}
C {lab_pin.sym} 2450 -460 0 0 {name=l157 lab=AMUXBUS_A}
C {lab_pin.sym} 2470 -460 0 0 {name=l158 lab=IOVDD}
C {lab_pin.sym} 2490 -460 0 0 {name=l159 lab=IOVDD}
C {lab_pin.sym} 2510 -460 2 0 {name=l160 lab=IOVDD}
C {lab_pin.sym} 2470 -340 0 0 {name=l161 lab=IOVSS}
C {lab_pin.sym} 2530 -460 2 0 {name=l162 lab=IOVDD}
C {lab_pin.sym} 2550 -460 2 0 {name=l163 lab=VDD}
C {lab_pin.sym} 2570 -460 2 0 {name=l164 lab=VDD}
C {lab_pin.sym} 2490 -340 0 0 {name=l165 lab=IOVSS}
C {lab_pin.sym} 2390 -420 0 0 {name=l166 lab=analog_PAD[0]}
C {sky130_ef_io/sky130_ef_io__analog_esd_pad.sym} 2500 -660 0 0 {name=analog_pad1}
C {lab_pin.sym} 2610 -680 2 0 {name=l167 lab=analog_PADESD[1]}
C {lab_pin.sym} 2430 -600 0 0 {name=l168 lab=IOVSS}
C {lab_pin.sym} 2450 -600 0 0 {name=l169 lab=VSS}
C {lab_pin.sym} 2430 -720 0 0 {name=l170 lab=AMUXBUS_B}
C {lab_pin.sym} 2450 -720 0 0 {name=l171 lab=AMUXBUS_A}
C {lab_pin.sym} 2470 -720 0 0 {name=l172 lab=IOVDD}
C {lab_pin.sym} 2490 -720 0 0 {name=l173 lab=IOVDD}
C {lab_pin.sym} 2510 -720 2 0 {name=l174 lab=IOVDD}
C {lab_pin.sym} 2470 -600 0 0 {name=l175 lab=IOVSS}
C {lab_pin.sym} 2530 -720 2 0 {name=l176 lab=IOVDD}
C {lab_pin.sym} 2550 -720 2 0 {name=l177 lab=VDD}
C {lab_pin.sym} 2570 -720 2 0 {name=l178 lab=VDD}
C {lab_pin.sym} 2490 -600 0 0 {name=l179 lab=IOVSS}
C {lab_pin.sym} 2390 -680 0 0 {name=l180 lab=analog_PAD[1]}
C {sky130_ef_io/sky130_ef_io__analog_noesd_pad.sym} 2500 -920 0 0 {name=analog_pad2}
C {lab_pin.sym} 2610 -940 2 0 {name=l181 lab=analog_PADBARE[2]}
C {lab_pin.sym} 2430 -860 0 0 {name=l182 lab=IOVSS}
C {lab_pin.sym} 2450 -860 0 0 {name=l183 lab=VSS}
C {lab_pin.sym} 2430 -980 0 0 {name=l184 lab=AMUXBUS_B}
C {lab_pin.sym} 2450 -980 0 0 {name=l185 lab=AMUXBUS_A}
C {lab_pin.sym} 2470 -980 0 0 {name=l186 lab=IOVDD}
C {lab_pin.sym} 2490 -980 0 0 {name=l187 lab=IOVDD}
C {lab_pin.sym} 2510 -980 2 0 {name=l188 lab=IOVDD}
C {lab_pin.sym} 2470 -860 0 0 {name=l189 lab=IOVSS}
C {lab_pin.sym} 2530 -980 2 0 {name=l190 lab=IOVDD}
C {lab_pin.sym} 2550 -980 2 0 {name=l191 lab=VDD}
C {lab_pin.sym} 2570 -980 2 0 {name=l192 lab=VDD}
C {lab_pin.sym} 2490 -860 0 0 {name=l193 lab=IOVSS}
C {lab_pin.sym} 2390 -940 0 0 {name=l194 lab=analog_PAD[2]}
C {sky130_ef_io/sky130_ef_io__analog_noesd_pad.sym} 2500 -1180 0 0 {name=analog_pad3}
C {lab_pin.sym} 2610 -1200 2 0 {name=l195 lab=analog_PADBARE[3]}
C {lab_pin.sym} 2430 -1120 0 0 {name=l196 lab=IOVSS}
C {lab_pin.sym} 2450 -1120 0 0 {name=l197 lab=VSS}
C {lab_pin.sym} 2430 -1240 0 0 {name=l198 lab=AMUXBUS_B}
C {lab_pin.sym} 2450 -1240 0 0 {name=l199 lab=AMUXBUS_A}
C {lab_pin.sym} 2470 -1240 0 0 {name=l200 lab=IOVDD}
C {lab_pin.sym} 2490 -1240 0 0 {name=l201 lab=IOVDD}
C {lab_pin.sym} 2510 -1240 2 0 {name=l202 lab=IOVDD}
C {lab_pin.sym} 2470 -1120 0 0 {name=l203 lab=IOVSS}
C {lab_pin.sym} 2530 -1240 2 0 {name=l204 lab=IOVDD}
C {lab_pin.sym} 2550 -1240 2 0 {name=l205 lab=VDD}
C {lab_pin.sym} 2570 -1240 2 0 {name=l206 lab=VDD}
C {lab_pin.sym} 2490 -1120 0 0 {name=l207 lab=IOVSS}
C {lab_pin.sym} 2390 -1200 0 0 {name=l208 lab=analog_PAD[3]}
C {sky130_ef_io/sky130_ef_io__vccd_lvc_clamped_pad.sym} 2500 -1440 0 0 {name=vdd_pad}
C {lab_pin.sym} 2430 -1500 0 0 {name=l209 lab=AMUXBUS_A}
C {lab_pin.sym} 2450 -1500 0 0 {name=l210 lab=AMUXBUS_B}
C {lab_pin.sym} 2390 -1460 0 0 {name=l211 lab=VDD}
C {lab_pin.sym} 2430 -1380 0 0 {name=l212 lab=IOVSS}
C {lab_pin.sym} 2470 -1500 0 0 {name=l213 lab=IOVDD}
C {lab_pin.sym} 2490 -1500 0 0 {name=l214 lab=IOVDD}
C {lab_pin.sym} 2510 -1500 2 0 {name=l215 lab=IOVDD}
C {lab_pin.sym} 2530 -1500 2 0 {name=l216 lab=VDD}
C {lab_pin.sym} 2550 -1500 2 0 {name=l217 lab=IOVDD}
C {lab_pin.sym} 2570 -1500 2 0 {name=l218 lab=VDD}
C {lab_pin.sym} 2450 -1380 0 0 {name=l219 lab=IOVSS}
C {lab_pin.sym} 2470 -1380 0 0 {name=l220 lab=VSS}
C {lab_pin.sym} 2490 -1380 0 0 {name=l221 lab=IOVSS}
C {sky130_ef_io/sky130_ef_io__vssd_lvc_clamped_pad.sym} 2500 -1700 0 0 {name=vss_pad}
C {lab_pin.sym} 2430 -1760 0 0 {name=l222 lab=AMUXBUS_A}
C {lab_pin.sym} 2450 -1760 0 0 {name=l223 lab=AMUXBUS_B}
C {lab_pin.sym} 2390 -1720 0 0 {name=l224 lab=VSS}
C {lab_pin.sym} 2430 -1640 0 0 {name=l225 lab=IOVSS}
C {lab_pin.sym} 2470 -1760 0 0 {name=l226 lab=IOVDD}
C {lab_pin.sym} 2490 -1760 0 0 {name=l227 lab=IOVDD}
C {lab_pin.sym} 2510 -1760 2 0 {name=l228 lab=IOVDD}
C {lab_pin.sym} 2530 -1760 2 0 {name=l229 lab=VDD}
C {lab_pin.sym} 2550 -1760 2 0 {name=l230 lab=IOVDD}
C {lab_pin.sym} 2570 -1760 2 0 {name=l231 lab=VDD}
C {lab_pin.sym} 2450 -1640 0 0 {name=l232 lab=IOVSS}
C {lab_pin.sym} 2470 -1640 0 0 {name=l233 lab=VSS}
C {lab_pin.sym} 2490 -1640 0 0 {name=l234 lab=IOVSS}
C {sky130_ef_io/sky130_ef_io__vddio_hvc_clamped_pad.sym} 2500 -1960 0 0 {name=iovdd_pad}
C {lab_pin.sym} 2430 -2020 0 0 {name=l235 lab=AMUXBUS_A}
C {lab_pin.sym} 2450 -2020 0 0 {name=l236 lab=AMUXBUS_B}
C {lab_pin.sym} 2390 -1980 0 0 {name=l237 lab=IOVDD}
C {lab_pin.sym} 2430 -1900 0 0 {name=l238 lab=IOVSS}
C {lab_pin.sym} 2470 -2020 0 0 {name=l239 lab=IOVDD}
C {lab_pin.sym} 2490 -2020 0 0 {name=l240 lab=IOVDD}
C {lab_pin.sym} 2510 -2020 2 0 {name=l241 lab=IOVDD}
C {lab_pin.sym} 2530 -2020 2 0 {name=l242 lab=VDD}
C {lab_pin.sym} 2550 -2020 2 0 {name=l243 lab=IOVDD}
C {lab_pin.sym} 2570 -2020 2 0 {name=l244 lab=VDD}
C {lab_pin.sym} 2450 -1900 0 0 {name=l245 lab=IOVSS}
C {lab_pin.sym} 2470 -1900 0 0 {name=l246 lab=VSS}
C {lab_pin.sym} 2490 -1900 0 0 {name=l247 lab=IOVSS}
C {sky130_ef_io/sky130_ef_io__vssio_hvc_clamped_pad.sym} 2500 -2220 0 0 {name=iovss_pad}
C {lab_pin.sym} 2430 -2280 0 0 {name=l248 lab=AMUXBUS_A}
C {lab_pin.sym} 2450 -2280 0 0 {name=l249 lab=AMUXBUS_B}
C {lab_pin.sym} 2390 -2240 0 0 {name=l250 lab=IOVSS}
C {lab_pin.sym} 2430 -2160 0 0 {name=l251 lab=IOVSS}
C {lab_pin.sym} 2470 -2280 0 0 {name=l252 lab=IOVDD}
C {lab_pin.sym} 2490 -2280 0 0 {name=l253 lab=IOVDD}
C {lab_pin.sym} 2510 -2280 2 0 {name=l254 lab=IOVDD}
C {lab_pin.sym} 2530 -2280 2 0 {name=l255 lab=VDD}
C {lab_pin.sym} 2550 -2280 2 0 {name=l256 lab=IOVDD}
C {lab_pin.sym} 2570 -2280 2 0 {name=l257 lab=VDD}
C {lab_pin.sym} 2450 -2160 0 0 {name=l258 lab=IOVSS}
C {lab_pin.sym} 2470 -2160 0 0 {name=l259 lab=VSS}
C {lab_pin.sym} 2490 -2160 0 0 {name=l260 lab=IOVSS}
C {sky130_ef_io/sky130_ef_io__connect_vcchib_vccd_and_vswitch_vddio_slice_20um.sym} 3200 -400 0 0 {name=connect_vcchib_vswitch}
C {lab_pin.sym} 3150 -460 0 0 {name=l261 lab=AMUXBUS_A}
C {lab_pin.sym} 3170 -460 0 0 {name=l262 lab=AMUXBUS_B}
C {lab_pin.sym} 3150 -340 0 0 {name=l263 lab=IOVSS}
C {lab_pin.sym} 3190 -460 0 0 {name=l264 lab=IOVDD}
C {lab_pin.sym} 3210 -460 2 0 {name=l265 lab=IOVDD}
C {lab_pin.sym} 3230 -460 2 0 {name=l266 lab=IOVDD}
C {lab_pin.sym} 3250 -460 2 0 {name=l267 lab=VDD}
C {lab_pin.sym} 3170 -340 0 0 {name=l268 lab=IOVSS}
C {lab_pin.sym} 3190 -340 0 0 {name=l269 lab=VSS}
C {lab_pin.sym} 3210 -340 2 0 {name=l270 lab=IOVSS}
C {sky130_ef_io/sky130_ef_io__connect_vdda_vddio_and_vssa_vssio_slice_20um.sym} 3200 -660 0 0 {name=connect_vdda_vssa}
C {lab_pin.sym} 3150 -720 0 0 {name=l271 lab=AMUXBUS_A}
C {lab_pin.sym} 3170 -720 0 0 {name=l272 lab=AMUXBUS_B}
C {lab_pin.sym} 3150 -600 0 0 {name=l273 lab=IOVSS}
C {lab_pin.sym} 3190 -720 0 0 {name=l274 lab=IOVDD}
C {lab_pin.sym} 3210 -720 2 0 {name=l275 lab=IOVDD}
C {lab_pin.sym} 3230 -720 2 0 {name=l276 lab=IOVDD}
C {lab_pin.sym} 3250 -720 2 0 {name=l277 lab=VDD}
C {lab_pin.sym} 3170 -600 0 0 {name=l278 lab=IOVSS}
C {lab_pin.sym} 3190 -600 0 0 {name=l279 lab=VSS}
C {lab_pin.sym} 3210 -600 2 0 {name=l280 lab=IOVSS}
C {counter_top.sym} 3200 -920 0 0 {name=counter1}
C {lab_pin.sym} 3200 -1020 0 0 {name=l281 lab=VDD}
C {lab_pin.sym} 3200 -820 0 0 {name=l282 lab=VSS}
C {lab_pin.sym} 3100 -980 0 0 {name=l283 lab=clk_PAD2CORE}
C {lab_pin.sym} 3100 -860 0 0 {name=l284 lab=rst_n_PAD2CORE}
C {lab_pin.sym} 3100 -920 0 0 {name=l285 lab=input_PAD2CORE[0]}
C {lab_pin.sym} 3300 -920 2 0 {name=l286 lab=output_CORE2PAD[0],output_CORE2PAD[1],output_CORE2PAD[2],output_CORE2PAD[3],bidir_CORE2PAD[0],bidir_CORE2PAD[1],bidir_CORE2PAD[2],bidir_CORE2PAD[3]}
C {counter_top.sym} 3200 -1180 0 0 {name=counter2}
C {lab_pin.sym} 3200 -1280 0 0 {name=l287 lab=VDD}
C {lab_pin.sym} 3200 -1080 0 0 {name=l288 lab=VSS}
C {lab_pin.sym} 3100 -1240 0 0 {name=l289 lab=clk_PAD2CORE}
C {lab_pin.sym} 3100 -1120 0 0 {name=l290 lab=rst_n_PAD2CORE}
C {lab_pin.sym} 3100 -1180 0 0 {name=l291 lab=input_PAD2CORE[0]}
C {lab_pin.sym} 3300 -1180 2 0 {name=l292 lab=output_CORE2PAD[4],output_CORE2PAD[5],output_CORE2PAD[6],output_CORE2PAD[7],output_CORE2PAD[8],output_CORE2PAD[9],output_CORE2PAD[10],output_CORE2PAD[11]}
C {inverter_top.sym} 3200 -1440 0 0 {name=inverter1}
C {lab_pin.sym} 3200 -1580 0 0 {name=l293 lab=VDD}
C {lab_pin.sym} 3080 -1500 0 0 {name=l294 lab=bidir_PAD2CORE[3]}
C {lab_pin.sym} 3320 -1500 2 0 {name=l295 lab=output_CORE2PAD[15]}
C {lab_pin.sym} 3200 -1300 0 0 {name=l296 lab=VSS}
C {lab_pin.sym} 3080 -1460 0 0 {name=l297 lab=bidir_PAD2CORE[2]}
C {lab_pin.sym} 3320 -1460 2 0 {name=l298 lab=output_CORE2PAD[14]}
C {lab_pin.sym} 3080 -1420 0 0 {name=l299 lab=bidir_PAD2CORE[1]}
C {lab_pin.sym} 3320 -1420 2 0 {name=l300 lab=output_CORE2PAD[13]}
C {lab_pin.sym} 3320 -1380 2 0 {name=l301 lab=output_CORE2PAD[12]}
C {lab_pin.sym} 3080 -1380 0 0 {name=l302 lab=bidir_PAD2CORE[0]}
C {inverter_top.sym} 3200 -1700 0 0 {name=inverter2}
C {lab_pin.sym} 3200 -1840 0 0 {name=l303 lab=VDD}
C {lab_pin.sym} 3080 -1760 0 0 {name=l304 lab=VSS}
C {lab_pin.sym} 3320 -1760 2 0 {name=l305 lab=VSS}
C {lab_pin.sym} 3200 -1560 0 0 {name=l306 lab=VSS}
C {lab_pin.sym} 3080 -1720 0 0 {name=l307 lab=VSS}
C {lab_pin.sym} 3320 -1720 2 0 {name=l308 lab=VSS}
C {lab_pin.sym} 3080 -1680 0 0 {name=l309 lab=analog_PADESD[1]}
C {lab_pin.sym} 3320 -1680 2 0 {name=l310 lab=analog_PADBARE[3]}
C {lab_pin.sym} 3320 -1640 2 0 {name=l311 lab=analog_PADBARE[2]}
C {lab_pin.sym} 3080 -1640 0 0 {name=l312 lab=analog_PADESD[0]}
T {output_CORE2PAD[16] carries the SRAM parity in rtl/lit_compac_core.sv. The SRAM macro is not} 100 -350 0 0 0.4 0.4 {}
T {in this schematic, so that pad has no driver here.} 100 -320 0 0 0.4 0.4 {}
C {devices/iopin.sym} -100 -300 0 0 {name=p313 lab=clk_PAD}
C {devices/iopin.sym} -100 -330 0 0 {name=p314 lab=rst_n_PAD}
C {devices/iopin.sym} -100 -360 0 0 {name=p315 lab=input_PAD[0]}
C {devices/iopin.sym} -100 -390 0 0 {name=p316 lab=output_PAD[0]}
C {devices/iopin.sym} -100 -420 0 0 {name=p317 lab=output_PAD[1]}
C {devices/iopin.sym} -100 -450 0 0 {name=p318 lab=output_PAD[2]}
C {devices/iopin.sym} -100 -480 0 0 {name=p319 lab=output_PAD[3]}
C {devices/iopin.sym} -100 -510 0 0 {name=p320 lab=output_PAD[4]}
C {devices/iopin.sym} -100 -540 0 0 {name=p321 lab=output_PAD[5]}
C {devices/iopin.sym} -100 -570 0 0 {name=p322 lab=output_PAD[6]}
C {devices/iopin.sym} -100 -600 0 0 {name=p323 lab=output_PAD[7]}
C {devices/iopin.sym} -100 -630 0 0 {name=p324 lab=output_PAD[8]}
C {devices/iopin.sym} -100 -660 0 0 {name=p325 lab=output_PAD[9]}
C {devices/iopin.sym} -100 -690 0 0 {name=p326 lab=output_PAD[10]}
C {devices/iopin.sym} -100 -720 0 0 {name=p327 lab=output_PAD[11]}
C {devices/iopin.sym} -100 -750 0 0 {name=p328 lab=output_PAD[12]}
C {devices/iopin.sym} -100 -780 0 0 {name=p329 lab=output_PAD[13]}
C {devices/iopin.sym} -100 -810 0 0 {name=p330 lab=output_PAD[14]}
C {devices/iopin.sym} -100 -840 0 0 {name=p331 lab=output_PAD[15]}
C {devices/iopin.sym} -100 -870 0 0 {name=p332 lab=output_PAD[16]}
C {devices/iopin.sym} -100 -900 0 0 {name=p333 lab=bidir_PAD[0]}
C {devices/iopin.sym} -100 -930 0 0 {name=p334 lab=bidir_PAD[1]}
C {devices/iopin.sym} -100 -960 0 0 {name=p335 lab=bidir_PAD[2]}
C {devices/iopin.sym} -100 -990 0 0 {name=p336 lab=bidir_PAD[3]}
C {devices/iopin.sym} -100 -1020 0 0 {name=p337 lab=analog_PAD[0]}
C {devices/iopin.sym} -100 -1050 0 0 {name=p338 lab=analog_PAD[1]}
C {devices/iopin.sym} -100 -1080 0 0 {name=p339 lab=analog_PAD[2]}
C {devices/iopin.sym} -100 -1110 0 0 {name=p340 lab=analog_PAD[3]}
C {devices/iopin.sym} -100 -1140 0 0 {name=p341 lab=VDD}
C {devices/iopin.sym} -100 -1170 0 0 {name=p342 lab=VSS}
C {devices/iopin.sym} -100 -1200 0 0 {name=p343 lab=IOVDD}
C {devices/iopin.sym} -100 -1230 0 0 {name=p344 lab=IOVSS}

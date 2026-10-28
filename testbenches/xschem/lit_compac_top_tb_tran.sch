v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {lit_compac_top transient testbench: the extracted chip with its pad ring} 200 -1300 0 0 0.8 0.8 {}
T {The chip pins carry labels, the pad ring and the macros come from the PEX netlist.} 200 -1270 0 0 0.4 0.4 {}
C {lit_compac_top_pex.sym} 1400 -700 0 0 {name=x1}
C {devices/lab_wire.sym} 1260 -860 0 0 {name=p1 sig_type=std_logic lab=clock}
C {devices/lab_wire.sym} 1260 -840 0 0 {name=p2 sig_type=std_logic lab=reset_n}
C {devices/lab_wire.sym} 1260 -820 0 0 {name=p3 sig_type=std_logic lab=enable}
C {devices/lab_wire.sym} 1260 -800 0 0 {name=p4 sig_type=std_logic lab=counter1_value0}
C {devices/lab_wire.sym} 1260 -780 0 0 {name=p5 sig_type=std_logic lab=counter1_value1}
C {devices/lab_wire.sym} 1260 -760 0 0 {name=p6 sig_type=std_logic lab=counter1_value2}
C {devices/lab_wire.sym} 1260 -740 0 0 {name=p7 sig_type=std_logic lab=counter1_value3}
C {devices/lab_wire.sym} 1260 -720 0 0 {name=p8 sig_type=std_logic lab=counter2_value0}
C {devices/lab_wire.sym} 1260 -700 0 0 {name=p9 sig_type=std_logic lab=counter2_value1}
C {devices/lab_wire.sym} 1260 -680 0 0 {name=p10 sig_type=std_logic lab=counter2_value2}
C {devices/lab_wire.sym} 1260 -660 0 0 {name=p11 sig_type=std_logic lab=counter2_value3}
C {devices/lab_wire.sym} 1260 -640 0 0 {name=p12 sig_type=std_logic lab=counter2_value4}
C {devices/lab_wire.sym} 1260 -620 0 0 {name=p13 sig_type=std_logic lab=counter2_value5}
C {devices/lab_wire.sym} 1260 -600 0 0 {name=p14 sig_type=std_logic lab=counter2_value6}
C {devices/lab_wire.sym} 1260 -580 0 0 {name=p15 sig_type=std_logic lab=counter2_value7}
C {devices/lab_wire.sym} 1540 -860 2 0 {name=p16 sig_type=std_logic lab=inv1_dout1}
C {devices/lab_wire.sym} 1540 -840 2 0 {name=p17 sig_type=std_logic lab=inv1_dout2}
C {devices/lab_wire.sym} 1540 -820 2 0 {name=p18 sig_type=std_logic lab=inv1_dout3}
C {devices/lab_wire.sym} 1540 -800 2 0 {name=p19 sig_type=std_logic lab=inv1_dout4}
C {devices/lab_wire.sym} 1540 -780 2 0 {name=p20 sig_type=std_logic lab=sram_0_out}
C {devices/lab_wire.sym} 1540 -760 2 0 {name=p21 sig_type=std_logic lab=counter1_value4_inv1_din1}
C {devices/lab_wire.sym} 1540 -740 2 0 {name=p22 sig_type=std_logic lab=counter1_value5_inv1_din2}
C {devices/lab_wire.sym} 1540 -720 2 0 {name=p23 sig_type=std_logic lab=counter1_value6_inv1_din3}
C {devices/lab_wire.sym} 1540 -700 2 0 {name=p24 sig_type=std_logic lab=counter1_value7_inv1_din4}
C {devices/lab_wire.sym} 1540 -680 2 0 {name=p25 sig_type=std_logic lab=inv2_vin1}
C {devices/lab_wire.sym} 1540 -660 2 0 {name=p26 sig_type=std_logic lab=inv2_vin2}
C {devices/lab_wire.sym} 1540 -640 2 0 {name=p27 sig_type=std_logic lab=inv2_vout1}
C {devices/lab_wire.sym} 1540 -620 2 0 {name=p28 sig_type=std_logic lab=inv2_vout2}
C {devices/lab_wire.sym} 1540 -600 2 0 {name=p29 sig_type=std_logic lab=VDD}
C {devices/lab_wire.sym} 1540 -580 2 0 {name=p30 sig_type=std_logic lab=GND}
C {devices/lab_wire.sym} 1540 -560 2 0 {name=p31 sig_type=std_logic lab=VIO}
C {devices/vsource.sym} 200 -400 0 0 {name=VDD value={VDD}}
C {devices/lab_wire.sym} 200 -440 0 0 {name=nVDD sig_type=std_logic lab=VDD}
N 200 -440 200 -430 {lab=VDD}
C {devices/gnd.sym} 200 -340 0 0 {name=gVDD lab=GND}
N 200 -370 200 -340 {lab=GND}
C {devices/vsource.sym} 350 -400 0 0 {name=VIO value={IOVDD}}
C {devices/lab_wire.sym} 350 -440 0 0 {name=nVIO sig_type=std_logic lab=VIO}
N 350 -440 350 -430 {lab=VIO}
C {devices/gnd.sym} 350 -340 0 0 {name=gVIO lab=GND}
N 350 -370 350 -340 {lab=GND}
C {devices/vsource.sym} 500 -400 0 0 {name=vclk value="pulse(0 \{IOVDD\} 0 100p 100p \{0.5/fclk\} \{1/fclk\})"}
C {devices/lab_wire.sym} 500 -440 0 0 {name=nvclk sig_type=std_logic lab=clock}
N 500 -440 500 -430 {lab=clock}
C {devices/gnd.sym} 500 -340 0 0 {name=gvclk lab=GND}
N 500 -370 500 -340 {lab=GND}
C {devices/vsource.sym} 650 -400 0 0 {name=vrst value="pulse(\{IOVDD\} 0 \{2/fclk\} 100p 100p \{2/fclk\} 1 1)"}
C {devices/lab_wire.sym} 650 -440 0 0 {name=nvrst sig_type=std_logic lab=reset_n}
N 650 -440 650 -430 {lab=reset_n}
C {devices/gnd.sym} 650 -340 0 0 {name=gvrst lab=GND}
N 650 -370 650 -340 {lab=GND}
C {devices/vsource.sym} 800 -400 0 0 {name=Venable value="pulse(\{IOVDD\} 0 \{100/fclk\} 100p 100p \{100/fclk\} 1 1)"}
C {devices/lab_wire.sym} 800 -440 0 0 {name=nVenable sig_type=std_logic lab=enable}
N 800 -440 800 -430 {lab=enable}
C {devices/gnd.sym} 800 -340 0 0 {name=gVenable lab=GND}
N 800 -370 800 -340 {lab=GND}
C {devices/vsource.sym} 950 -400 0 0 {name=vsine1 value="sin(\{Vcm\} 10m 200k)"}
C {devices/lab_wire.sym} 950 -440 0 0 {name=nvsine1 sig_type=std_logic lab=inv2_vin1}
N 950 -440 950 -430 {lab=inv2_vin1}
C {devices/gnd.sym} 950 -340 0 0 {name=gvsine1 lab=GND}
N 950 -370 950 -340 {lab=GND}
C {devices/vsource.sym} 1100 -400 0 0 {name=vsine2 value="sin(\{Vcm\} 10m 400k)"}
C {devices/lab_wire.sym} 1100 -440 0 0 {name=nvsine2 sig_type=std_logic lab=inv2_vin2}
N 1100 -440 1100 -430 {lab=inv2_vin2}
C {devices/gnd.sym} 1100 -340 0 0 {name=gvsine2 lab=GND}
N 1100 -370 1100 -340 {lab=GND}
C {devices/code.sym} 200 -1100 0 0 {name=NGSPICE
only_toplevel=true 
value="
.include ../../../netlist/pex/lit_compac_top_magic_pex_1.spice
.include ../../../macros/counter/netlist/xspice/counter_top.xspice
.param IOVDD=3.3
.param VDD=1.8
.param Vcm=0.9
.temp 27
.param fclk=40e6
.csparam fclk=fclk
.options klu method=gear reltol=3e-3 vntol=1e-5 abstol=1e-11 chgtol=1e-11 cshunt=100f rshunt=1e15
.control

save all

* User Constants
let tstart = 0
let tstop = 10u
let tstep = 100n

* Transient Operating Point Analysis
op
remzerovec
write @schname\\.raw
set appendwrite

* Transient Analysis
tran $&tstep $&tstop $&tstart
write @schname\\.raw

* Plotting
plot clock reset_n enable sram_0_out
plot inv2_vin1 inv2_vout1 inv2_vin2 inv2_vout2
plot inv1_dout1 inv1_dout2 inv1_dout3 inv1_dout4
plot counter2_value0 counter2_value1 counter2_value2 counter2_value3 counter2_value4 counter2_value5 counter2_value6 counter2_value7
plot counter1_value4_inv1_din1 counter1_value5_inv1_din2

* Write Data
unset appendwrite
set wr_vecnames
set wr_singlescale
wrdata ../plot_simulations/data/lit_compac_top_tb_tran.txt
+ v(clock) v(reset_n) v(enable) v(sram_0_out)
+ v(inv2_vin1) v(inv2_vout1) v(inv2_vin2) v(inv2_vout2)
+ v(inv1_dout1) v(inv1_dout2) v(inv1_dout3) v(inv1_dout4)
+ v(counter2_value0) v(counter2_value1) v(counter2_value2) v(counter2_value3)
+ v(counter2_value4) v(counter2_value5) v(counter2_value6) v(counter2_value7)
+ v(counter1_value4_inv1_din1) v(counter1_value5_inv1_din2)

*quit
*rusage all
.endc
"}
C {devices/code_shown.sym} 800 -1100 0 0 {name=MODEL only_toplevel=true
format="tcleval( @value )"
value="
.lib $::SKYWATER_MODELS/sky130.lib.spice tt
"}
C {devices/launcher.sym} 200 -1180 0 0 {name=h2
descr="Simulate" 
tclcommand="xschem save; xschem netlist; file mkdir $netlist_dir; write_data [save_params] $netlist_dir/[file rootname [file tail [xschem get current_name]]].save; xschem simulate"
}
C {devices/launcher.sym} 400 -1180 0 0 {name=h1
descr="Annotate OP" 
tclcommand="set show_hidden_texts 1; xschem annotate_op"
}
C {devices/launcher.sym} 600 -1180 0 0 {name=h3
descr="Load waves" 
tclcommand="xschem raw_read $netlist_dir/[file rootname [file tail [xschem get current_name]]].raw tran"
}

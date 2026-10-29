v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {Multiplier DC characterization, vout = K * v1 * v2 (K in 1/V)
-) Input CM vcmi and CMFB reference vref are separate sources, as in the multiplier chain
-) k100: four-quadrant K at +-100 mV on both inputs, k10: the same at +-10 mV, compr = k100/k10
-) k_in1big / k_in2big: K with only in1 / only in2 at 100 mV, to see which input compresses
-) vos_out: output offset at zero input, vos1_eq / vos2_eq: feedthrough of in2 / in1 referred to the other input
-) The CMFB amplifier bias I1 tracks ibias 1:1 (needed by the diode-load CMFB)} 100 -1060 0 0 0.3 0.3 {}
N 100 -330 100 -350 {lab=vdd}
N 100 -270 100 -250 {lab=GND}
N 200 -330 200 -350 {lab=vcmi}
N 200 -270 200 -250 {lab=GND}
N 300 -330 300 -350 {lab=vref}
N 300 -270 300 -250 {lab=GND}
N 400 -330 400 -350 {lab=ibias}
N 400 -270 400 -250 {lab=GND}
N 500 -330 500 -350 {lab=vdd}
N 500 -270 500 -250 {lab=ibias_ota}
N 100 -130 100 -150 {lab=vdin1}
N 100 -70 100 -50 {lab=GND}
N 200 -130 200 -150 {lab=in1p}
N 200 -70 200 -50 {lab=vcmi}
N 300 -130 300 -150 {lab=in1n}
N 300 -70 300 -50 {lab=vcmi}
N 440 -130 440 -150 {lab=vdin2}
N 440 -70 440 -50 {lab=GND}
N 540 -130 540 -150 {lab=in2p}
N 540 -70 540 -50 {lab=vcmi}
N 640 -130 640 -150 {lab=in2n}
N 640 -70 640 -50 {lab=vcmi}
N 1000 -500 1000 -540 {lab=vdd}
N 1040 -500 1040 -560 {lab=ibias}
N 1060 -500 1060 -520 {lab=vdd}
N 1060 -520 1100 -520 {lab=vdd}
N 900 -440 860 -440 {lab=in1p}
N 900 -420 860 -420 {lab=in1n}
N 900 -380 860 -380 {lab=in2p}
N 900 -360 860 -360 {lab=in2n}
N 1000 -300 1000 -260 {lab=GND}
N 1060 -300 1060 -260 {lab=GND}
N 1100 -420 1180 -420 {lab=outp}
N 1180 -420 1340 -420 {lab=outp}
N 1100 -380 1180 -380 {lab=outn}
N 1180 -380 1240 -380 {lab=outn}
N 1340 -360 1340 -340 {lab=GND}
N 1240 -320 1240 -300 {lab=GND}
N 1100 -450 1150 -450 {lab=vcm_sense}
N 1150 -450 1150 -600 {lab=vcm_sense}
N 1150 -600 1150 -770 {lab=vcm_sense}
N 1150 -830 1200 -830 {lab=vref}
N 1060 -900 1060 -940 {lab=vdd}
N 1030 -900 1030 -940 {lab=ibias_ota}
N 1110 -900 1110 -940 {lab=vdd}
N 1060 -700 1060 -660 {lab=GND}
N 1110 -700 1110 -660 {lab=GND}
N 960 -800 960 -650 {lab=vbias}
N 960 -650 960 -500 {lab=vbias}
N 940 -300 940 -260 {lab=gt0}
N 960 -300 960 -260 {lab=gt1}
N 980 -300 980 -260 {lab=gt2}
N 1020 -300 1020 -260 {lab=gt3}
N 1040 -300 1040 -260 {lab=gt4}
N 100 -1310 100 -1330 {lab=gcode}
N 100 -1250 100 -1230 {lab=GND}
N 200 -1310 200 -1330 {lab=gt0}
N 200 -1250 200 -1230 {lab=GND}
N 300 -1310 300 -1330 {lab=gt1}
N 300 -1250 300 -1230 {lab=GND}
N 400 -1310 400 -1330 {lab=gt2}
N 400 -1250 400 -1230 {lab=GND}
N 500 -1310 500 -1330 {lab=gt3}
N 500 -1250 500 -1230 {lab=GND}
N 600 -1310 600 -1330 {lab=gt4}
N 600 -1250 600 -1230 {lab=GND}
C {devices/code_shown.sym} 1500 -1060 0 0 {name=NGSPICE only_toplevel=true
value="
.temp \{\{ temp \}\}
.option SEED = \{\{ (seed|int) + 1 \}\}
.option method=gear

.control
save all
* op1..op21: (vd1, vd2) points; every op plot gets vout = v(outp)-v(outn)
op
let vout = v(outp)-v(outn)
let vocm = (v(outp)+v(outn))/2
alter vd1 dc=0.1
alter vd2 dc=0.1
op
let vout = v(outp)-v(outn)
alter vd1 dc=-0.1
op
let vout = v(outp)-v(outn)
alter vd2 dc=-0.1
op
let vout = v(outp)-v(outn)
alter vd1 dc=0.1
op
let vout = v(outp)-v(outn)
* feedthrough points: one input at +-100 mV, the other at 0
alter vd2 dc=0
op
let vout = v(outp)-v(outn)
alter vd1 dc=-0.1
op
let vout = v(outp)-v(outn)
alter vd1 dc=0
alter vd2 dc=0.1
op
let vout = v(outp)-v(outn)
alter vd2 dc=-0.1
op
let vout = v(outp)-v(outn)
* small-signal four-quadrant at +-10 mV (op10..op13)
alter vd1 dc=0.01
alter vd2 dc=0.01
op
let vout = v(outp)-v(outn)
alter vd1 dc=-0.01
op
let vout = v(outp)-v(outn)
alter vd2 dc=-0.01
op
let vout = v(outp)-v(outn)
alter vd1 dc=0.01
op
let vout = v(outp)-v(outn)
* in1 at +-100 mV, in2 at +-10 mV (op14..op17)
alter vd1 dc=0.1
alter vd2 dc=0.01
op
let vout = v(outp)-v(outn)
alter vd1 dc=-0.1
op
let vout = v(outp)-v(outn)
alter vd2 dc=-0.01
op
let vout = v(outp)-v(outn)
alter vd1 dc=0.1
op
let vout = v(outp)-v(outn)
* in1 at +-10 mV, in2 at +-100 mV (op18..op21)
alter vd1 dc=0.01
alter vd2 dc=0.1
op
let vout = v(outp)-v(outn)
alter vd1 dc=-0.01
op
let vout = v(outp)-v(outn)
alter vd2 dc=-0.1
op
let vout = v(outp)-v(outn)
alter vd1 dc=0.01
op
let vout = v(outp)-v(outn)
* transfer curves: vs vd1 at vd2 = +100 mV (dc1), vs vd2 at vd1 = +100 mV (dc2)
alter vd2 dc=0.1
dc vd1 -0.2 0.2 0.005
let vout_v1 = v(outp)-v(outn)
alter vd1 dc=0.1
dc vd2 -0.2 0.2 0.005
let vout_v2 = v(outp)-v(outn)
* scalars, K = vout/(v1*v2) from four-quadrant differences (offsets and feedthrough cancel)
let k100 = (op2.vout - op3.vout - op5.vout + op4.vout)/(4*0.1*0.1)
let k10 = (op10.vout - op11.vout - op13.vout + op12.vout)/(4*0.01*0.01)
let k_in1big = (op14.vout - op15.vout - op17.vout + op16.vout)/(4*0.1*0.01)
let k_in2big = (op18.vout - op19.vout - op21.vout + op20.vout)/(4*0.01*0.1)
let compr = k100/k10
let compr1 = k_in1big/k10
let compr2 = k_in2big/k10
let vout_pp = op2.vout
let vos_out = op1.vout
let vocm = op1.vocm
* feedthrough of one input, referred to the other input as an equivalent offset
let vos2_eq = (op6.vout - op7.vout)/(2*k10*0.1)
let vos1_eq = (op8.vout - op9.vout)/(2*k10*0.1)
quit
.endc
"}
C {simulator_commands_shown.sym} 100 -720 0 0 {
name=Libs_Ngspice
simulator=ngspice
only_toplevel=false
value="
.lib /foss/pdks/sky130A/libs.tech/ngspice/sky130.lib.spice \{\{ corner_mos \}\}
"
      }
C {devices/title.sym} 100 100 0 0 {name=l100 author="Santiago Hofwimmer | JKU IICQC"}
C {devices/vsource.sym} 100 -300 0 0 {name=Vdd value=\{\{vdd\}\} savecurrent=true}
C {devices/lab_pin.sym} 100 -350 3 1 {name=p1 sig_type=std_logic lab=vdd}
C {devices/gnd.sym} 100 -250 0 0 {name=l1 lab=GND}
C {devices/vsource.sym} 200 -300 0 0 {name=Vcmi value=\{\{vincm\}\} savecurrent=false}
C {devices/lab_pin.sym} 200 -350 3 1 {name=p2 sig_type=std_logic lab=vcmi}
C {devices/gnd.sym} 200 -250 0 0 {name=l2 lab=GND}
C {devices/vsource.sym} 300 -300 0 0 {name=Vref value=\{\{vref\}\} savecurrent=false}
C {devices/lab_pin.sym} 300 -350 3 1 {name=p3 sig_type=std_logic lab=vref}
C {devices/gnd.sym} 300 -250 0 0 {name=l3 lab=GND}
C {devices/isource.sym} 400 -300 0 0 {name=I0 value=\{\{ibias\}\}}
C {devices/lab_pin.sym} 400 -350 3 1 {name=p4 sig_type=std_logic lab=ibias}
C {devices/gnd.sym} 400 -250 0 0 {name=l4 lab=GND}
C {devices/isource.sym} 500 -300 0 0 {name=I1 value=\{\{ibias\}\}}
C {devices/lab_pin.sym} 500 -350 3 1 {name=p5 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 500 -250 3 0 {name=p6 sig_type=std_logic lab=ibias_ota}
C {devices/vsource.sym} 100 -100 0 0 {name=Vd1 value=\{\{vd1\}\} savecurrent=false}
C {devices/lab_pin.sym} 100 -150 3 1 {name=p7 sig_type=std_logic lab=vdin1}
C {devices/gnd.sym} 100 -50 0 0 {name=l5 lab=GND}
C {devices/vsource_arith.sym} 200 -100 0 0 {name=E1 VOL=v(vdin1)/2}
C {devices/lab_pin.sym} 200 -150 3 1 {name=p8 sig_type=std_logic lab=in1p}
C {devices/lab_pin.sym} 200 -50 3 0 {name=p9 sig_type=std_logic lab=vcmi}
C {devices/vsource_arith.sym} 300 -100 0 0 {name=E2 VOL=-v(vdin1)/2}
C {devices/lab_pin.sym} 300 -150 3 1 {name=p10 sig_type=std_logic lab=in1n}
C {devices/lab_pin.sym} 300 -50 3 0 {name=p11 sig_type=std_logic lab=vcmi}
C {devices/vsource.sym} 440 -100 0 0 {name=Vd2 value=\{\{vd2\}\} savecurrent=false}
C {devices/lab_pin.sym} 440 -150 3 1 {name=p12 sig_type=std_logic lab=vdin2}
C {devices/gnd.sym} 440 -50 0 0 {name=l6 lab=GND}
C {devices/vsource_arith.sym} 540 -100 0 0 {name=E4 VOL=v(vdin2)/2}
C {devices/lab_pin.sym} 540 -150 3 1 {name=p13 sig_type=std_logic lab=in2p}
C {devices/lab_pin.sym} 540 -50 3 0 {name=p14 sig_type=std_logic lab=vcmi}
C {devices/vsource_arith.sym} 640 -100 0 0 {name=E5 VOL=-v(vdin2)/2}
C {devices/lab_pin.sym} 640 -150 3 1 {name=p15 sig_type=std_logic lab=in2n}
C {devices/lab_pin.sym} 640 -50 3 0 {name=p16 sig_type=std_logic lab=vcmi}
C {lit_compac_sky/macros/gilbert_cell/schematic/xschem/gilbert_cell.sym} 1000 -400 0 0 {name=x1}
C {devices/lab_pin.sym} 1000 -540 3 1 {name=p17 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 1040 -560 3 1 {name=p18 sig_type=std_logic lab=ibias}
C {devices/lab_pin.sym} 1100 -520 2 0 {name=p19 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 860 -440 2 1 {name=p20 sig_type=std_logic lab=in1p}
C {devices/lab_pin.sym} 860 -420 2 1 {name=p21 sig_type=std_logic lab=in1n}
C {devices/lab_pin.sym} 860 -380 2 1 {name=p22 sig_type=std_logic lab=in2p}
C {devices/lab_pin.sym} 860 -360 2 1 {name=p23 sig_type=std_logic lab=in2n}
C {devices/gnd.sym} 1000 -260 0 0 {name=l7 lab=GND}
C {devices/gnd.sym} 1060 -260 0 0 {name=l8 lab=GND}
C {devices/lab_wire.sym} 1180 -420 0 0 {name=p24 sig_type=std_logic lab=outp}
C {devices/lab_wire.sym} 1180 -380 0 0 {name=p25 sig_type=std_logic lab=outn}
C {devices/capa.sym} 1340 -390 0 0 {name=Cloadp
m=1
value=\{\{c_load\}\}}
C {devices/gnd.sym} 1340 -340 0 0 {name=l9 lab=GND}
C {devices/capa.sym} 1240 -350 0 0 {name=Cloadn
m=1
value=\{\{c_load\}\}}
C {devices/gnd.sym} 1240 -300 0 0 {name=l10 lab=GND}
C {lit_compac_sky/macros/ota/schematic/xschem/ota.sym} 1060 -800 0 1 {name=x2}
C {devices/lab_wire.sym} 1150 -600 3 0 {name=p26 sig_type=std_logic lab=vcm_sense}
C {devices/lab_pin.sym} 1200 -830 2 0 {name=p27 sig_type=std_logic lab=vref}
C {devices/lab_pin.sym} 1060 -940 3 1 {name=p28 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} 1030 -940 3 1 {name=p29 sig_type=std_logic lab=ibias_ota}
C {devices/lab_pin.sym} 1110 -940 3 1 {name=p30 sig_type=std_logic lab=vdd}
C {devices/gnd.sym} 1060 -660 0 0 {name=l11 lab=GND}
C {devices/gnd.sym} 1110 -660 0 0 {name=l12 lab=GND}
C {devices/lab_wire.sym} 960 -650 3 0 {name=p31 sig_type=std_logic lab=vbias}
C {devices/lab_pin.sym} 940 -260 3 0 {name=lgt0 sig_type=std_logic lab=gt0}
C {devices/lab_pin.sym} 960 -260 3 0 {name=lgt1 sig_type=std_logic lab=gt1}
C {devices/lab_pin.sym} 980 -260 3 0 {name=lgt2 sig_type=std_logic lab=gt2}
C {devices/lab_pin.sym} 1020 -260 3 0 {name=lgt3 sig_type=std_logic lab=gt3}
C {devices/lab_pin.sym} 1040 -260 3 0 {name=lgt4 sig_type=std_logic lab=gt4}
T {gain trim: gcode 0..31 with K up for a higher code, gt<k> = 1.5 V bypasses segment k, so gt<k> = 1.5 x (1 - bit k)} 100 -1390 0 0 0.3 0.3 {}
C {devices/vsource.sym} 100 -1280 0 0 {name=Vgcode value=\{\{gcode\}\} savecurrent=false}
C {devices/lab_pin.sym} 100 -1330 3 1 {name=lgcode sig_type=std_logic lab=gcode}
C {devices/gnd.sym} 100 -1230 0 0 {name=lgcg lab=GND}
C {devices/vsource_arith.sym} 200 -1280 0 0 {name=Egt0 VOL=v(vdd)*(1-(floor((v(gcode)+0.5)/1)-2*floor((v(gcode)+0.5)/2)))}
C {devices/lab_pin.sym} 200 -1330 3 1 {name=lgtd0 sig_type=std_logic lab=gt0}
C {devices/gnd.sym} 200 -1230 0 0 {name=lgtg0 lab=GND}
C {devices/vsource_arith.sym} 300 -1280 0 0 {name=Egt1 VOL=v(vdd)*(1-(floor((v(gcode)+0.5)/2)-2*floor((v(gcode)+0.5)/4)))}
C {devices/lab_pin.sym} 300 -1330 3 1 {name=lgtd1 sig_type=std_logic lab=gt1}
C {devices/gnd.sym} 300 -1230 0 0 {name=lgtg1 lab=GND}
C {devices/vsource_arith.sym} 400 -1280 0 0 {name=Egt2 VOL=v(vdd)*(1-(floor((v(gcode)+0.5)/4)-2*floor((v(gcode)+0.5)/8)))}
C {devices/lab_pin.sym} 400 -1330 3 1 {name=lgtd2 sig_type=std_logic lab=gt2}
C {devices/gnd.sym} 400 -1230 0 0 {name=lgtg2 lab=GND}
C {devices/vsource_arith.sym} 500 -1280 0 0 {name=Egt3 VOL=v(vdd)*(1-(floor((v(gcode)+0.5)/8)-2*floor((v(gcode)+0.5)/16)))}
C {devices/lab_pin.sym} 500 -1330 3 1 {name=lgtd3 sig_type=std_logic lab=gt3}
C {devices/gnd.sym} 500 -1230 0 0 {name=lgtg3 lab=GND}
C {devices/vsource_arith.sym} 600 -1280 0 0 {name=Egt4 VOL=v(vdd)*(1-(floor((v(gcode)+0.5)/16)-2*floor((v(gcode)+0.5)/32)))}
C {devices/lab_pin.sym} 600 -1330 3 1 {name=lgtd4 sig_type=std_logic lab=gt4}
C {devices/gnd.sym} 600 -1230 0 0 {name=lgtg4 lab=GND}

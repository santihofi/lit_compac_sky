v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}


T {slow loop (integrator)} -680 -460 0 0 0.4 0.4 {}
T {fast loop (diode-load CMFB)} -40 -460 0 0 0.4 0.4 {}
T {n bulk
contact} 540 -340 0 0 0.3 0.3 {}
T {p bulk
contact} 540 150 0 0 0.3 0.3 {}
N 40 -420 40 -350 {lab=vdd}
N 300 -420 300 -350 {lab=vdd}
N 0 -320 40 -320 {lab=ntap}
N 300 -320 340 -320 {lab=ntap}
N 80 -320 110 -320 {lab=vd_m5}
N 110 -320 110 -250 {lab=vd_m5}
N 40 -250 110 -250 {lab=vd_m5}
N 40 -290 40 -250 {lab=vd_m5}
N 40 -250 40 -30 {lab=vd_m5}
N 230 -320 260 -320 {lab=out}
N 230 -320 230 -250 {lab=out}
N 230 -250 300 -250 {lab=out}
N 300 -290 300 -250 {lab=out}
N 300 -250 300 -200 {lab=out}
N 300 -200 300 -30 {lab=out}
N 300 -200 400 -200 {lab=out}
N -40 0 0 0 {lab=inp}
N 40 0 80 0 {lab=ptap}
N 340 0 380 0 {lab=vref_int}
N 260 0 300 0 {lab=ptap}
N 40 30 40 80 {lab=sa}
N 40 80 40 120 {lab=sa}
N 40 80 140 80 {lab=sa}
N 300 30 300 80 {lab=sb}
N 300 80 300 120 {lab=sb}
N 200 80 300 80 {lab=sb}
N 40 180 40 260 {lab=vss}
N 300 180 300 260 {lab=vss}
N -120 180 -120 260 {lab=vss}
N 40 150 80 150 {lab=ptap}
N 260 150 300 150 {lab=ptap}
N -160 150 -120 150 {lab=ptap}
N 340 150 380 150 {lab=ibias1}
N -80 150 -60 150 {lab=ibias1}
N -60 150 0 150 {lab=ibias1}
N -120 100 -120 120 {lab=ibias1}
N -120 100 -60 100 {lab=ibias1}
N -60 100 -60 150 {lab=ibias1}
N -120 60 -120 100 {lab=ibias1}
N -580 -420 -580 -350 {lab=vdd}
N -320 -420 -320 -350 {lab=vdd}
N -620 -320 -580 -320 {lab=ntap}
N -320 -320 -280 -320 {lab=ntap}
N -540 -320 -510 -320 {lab=vd_m10}
N -510 -320 -360 -320 {lab=vd_m10}
N -510 -320 -510 -260 {lab=vd_m10}
N -580 -260 -510 -260 {lab=vd_m10}
N -580 -290 -580 -260 {lab=vd_m10}
N -580 -260 -580 -90 {lab=vd_m10}
N -320 -290 -320 -150 {lab=vref_int}
N -320 -150 -320 -90 {lab=vref_int}
N -320 -150 -200 -150 {lab=vref_int}
N -660 -60 -620 -60 {lab=inn}
N -580 -60 -540 -60 {lab=ptap}
N -280 -60 -240 -60 {lab=inp}
N -370 -60 -320 -60 {lab=ptap}
N -580 -30 -580 20 {lab=vtail_slow}
N -580 20 -450 20 {lab=vtail_slow}
N -320 -30 -320 20 {lab=vtail_slow}
N -450 20 -320 20 {lab=vtail_slow}
N -450 20 -450 50 {lab=vtail_slow}
N -530 80 -490 80 {lab=ibias1}
N -450 110 -450 260 {lab=vss}
N -450 80 -410 80 {lab=ptap}
N -160 -200 -160 -180 {lab=vss}
N -160 -120 -160 -100 {lab=vss}
N -160 -150 -120 -150 {lab=ptap}
N 500 -420 500 -350 {lab=vdd}
N 500 -290 500 -270 {lab=ntap}
N 500 190 500 260 {lab=vss}
N 500 90 500 130 {lab=ptap}
N -700 -420 -580 -420 {lab=vdd}
N -580 -420 -320 -420 {lab=vdd}
N -320 -420 40 -420 {lab=vdd}
N 40 -420 300 -420 {lab=vdd}
N 300 -420 500 -420 {lab=vdd}
N -700 260 -450 260 {lab=vss}
N -450 260 -120 260 {lab=vss}
N -120 260 40 260 {lab=vss}
N 40 260 300 260 {lab=vss}
N 300 260 500 260 {lab=vss}
C {title.sym} -700 380 0 0 {name=l1 author="Santiago Hofwimmer | JKU IICQC"}
C {sky130_fd_pr/pfet_01v8_lvt.sym} 60 -320 0 1 {name=M5
L=0.35
W=1.54
nf=2
ad=0.2233
as=0.4466
pd=2.12
ps=4.24
nrd=0.1883116883116883
nrs=0.1883116883116883
sa=0
sb=0
sd=0
mult=2.0
model=pfet_01v8_lvt
spiceprefix=X
}
C {sky130_fd_pr/pfet_01v8_lvt.sym} 280 -320 0 0 {name=M6
L=0.35
W=1.54
nf=2
ad=0.2233
as=0.4466
pd=2.12
ps=4.24
nrd=0.1883116883116883
nrs=0.1883116883116883
sa=0
sb=0
sd=0
mult=2.0
model=pfet_01v8_lvt
spiceprefix=X
}
C {lab_pin.sym} 0 -320 2 1 {name=p20 sig_type=std_logic lab=ntap}
C {lab_pin.sym} 340 -320 2 0 {name=p21 sig_type=std_logic lab=ntap}
C {lab_wire.sym} 40 -140 3 0 {name=p22 sig_type=std_logic lab=vd_m5}
C {opin.sym} 400 -200 0 0 {name=p5 lab=out}
C {sky130_fd_pr/nfet_01v8_lvt.sym} 20 0 0 0 {name=M1
L=1
W=16
nf=4
ad=2.32
as=3.48
pd=17.16
ps=25.74
nrd=0.018125
nrs=0.018125
sa=0
sb=0
sd=0
mult=2.0
model=nfet_01v8_lvt
spiceprefix=X
}
C {sky130_fd_pr/nfet_01v8_lvt.sym} 320 0 0 1 {name=M2
L=1
W=16
nf=4
ad=2.32
as=3.48
pd=17.16
ps=25.74
nrd=0.018125
nrs=0.018125
sa=0
sb=0
sd=0
mult=2.0
model=nfet_01v8_lvt
spiceprefix=X
}
C {ipin.sym} -40 0 0 0 {name=p2 lab=inp}
C {lab_pin.sym} 80 0 2 0 {name=p23 sig_type=std_logic lab=ptap}
C {lab_pin.sym} 380 0 2 0 {name=p24 sig_type=std_logic lab=vref_int}
C {lab_pin.sym} 260 0 2 1 {name=p25 sig_type=std_logic lab=ptap}
C {sky130_fd_pr/res_high_po_1p41.sym} 800 80 3 0 {name=RS1
L=22.705
mult=2.0
model=res_high_po_1p41
spiceprefix=X
}


C {sky130_fd_pr/res_high_po_1p41.sym} 900 80 3 0 {name=RS2
L=22.705
mult=2.0
model=res_high_po_1p41
spiceprefix=X
}


C {sky130_fd_pr/res_high_po_1p41.sym} 1000 80 3 0 {name=RS3
L=22.705
mult=2.0
model=res_high_po_1p41
spiceprefix=X
}


C {sky130_fd_pr/res_high_po_1p41.sym} 1100 80 3 0 {name=RS4
L=22.705
mult=2.0
model=res_high_po_1p41
spiceprefix=X
}


C {sky130_fd_pr/res_high_po_1p41.sym} 1200 80 3 0 {name=RS5
L=22.705
mult=2.0
model=res_high_po_1p41
spiceprefix=X
}


C {sky130_fd_pr/res_high_po_1p41.sym} 1300 80 3 0 {name=RS6
L=22.705
mult=2.0
model=res_high_po_1p41
spiceprefix=X
}


C {sky130_fd_pr/res_high_po_1p41.sym} 1400 80 3 0 {name=RS7
L=22.705
mult=2.0
model=res_high_po_1p41
spiceprefix=X
}


C {sky130_fd_pr/res_high_po_1p41.sym} 1500 80 3 0 {name=RS8
L=22.705
mult=2.0
model=res_high_po_1p41
spiceprefix=X
}


C {sky130_fd_pr/res_high_po_1p41.sym} 1600 80 3 0 {name=RS9
L=22.705
mult=2.0
model=res_high_po_1p41
spiceprefix=X
}


C {sky130_fd_pr/res_high_po_1p41.sym} 1700 80 3 0 {name=RS10
L=22.705
mult=2.0
model=res_high_po_1p41
spiceprefix=X
}


C {sky130_fd_pr/res_high_po_1p41.sym} 1800 80 3 0 {name=RS11
L=22.705
mult=2.0
model=res_high_po_1p41
spiceprefix=X
}


C {sky130_fd_pr/res_high_po_1p41.sym} 1900 80 3 0 {name=RS12
L=22.705
mult=2.0
model=res_high_po_1p41
spiceprefix=X
}


C {lab_wire.sym} 90 80 0 0 {name=p26 sig_type=std_logic lab=sa}
C {lab_wire.sym} 250 80 0 0 {name=p27 sig_type=std_logic lab=sb}
C {sky130_fd_pr/nfet_01v8_lvt.sym} 20 150 0 0 {name=M3
L=2
W=16
nf=4
ad=2.32
as=3.48
pd=17.16
ps=25.74
nrd=0.018125
nrs=0.018125
sa=0
sb=0
sd=0
mult=2.0
model=nfet_01v8_lvt
spiceprefix=X
}
C {sky130_fd_pr/nfet_01v8_lvt.sym} 320 150 0 1 {name=M3B
L=2
W=16
nf=4
ad=2.32
as=3.48
pd=17.16
ps=25.74
nrd=0.018125
nrs=0.018125
sa=0
sb=0
sd=0
mult=2.0
model=nfet_01v8_lvt
spiceprefix=X
}
C {sky130_fd_pr/nfet_01v8_lvt.sym} -100 150 0 1 {name=M4
L=2
W=32
nf=8
ad=4.64
as=5.8
pd=34.32
ps=42.9
nrd=0.0090625
nrs=0.0090625
sa=0
sb=0
sd=0
mult=2.0
model=nfet_01v8_lvt
spiceprefix=X
}
C {lab_pin.sym} 80 150 2 0 {name=p28 sig_type=std_logic lab=ptap}
C {lab_pin.sym} 260 150 2 1 {name=p29 sig_type=std_logic lab=ptap}
C {lab_pin.sym} -160 150 2 1 {name=p30 sig_type=std_logic lab=ptap}
C {lab_pin.sym} 380 150 2 0 {name=p31 sig_type=std_logic lab=ibias1}
C {ipin.sym} -120 60 1 0 {name=p1 lab=ibias1}
C {sky130_fd_pr/pfet_01v8_lvt.sym} -560 -320 0 1 {name=M10
L=4
W=1
nf=1
ad=0.29
as=0.29
pd=2.58
ps=2.58
nrd=0.29
nrs=0.29
sa=0
sb=0
sd=0
mult=2.0
model=pfet_01v8_lvt
spiceprefix=X
}
C {sky130_fd_pr/pfet_01v8_lvt.sym} -340 -320 0 0 {name=M11
L=4
W=1
nf=1
ad=0.29
as=0.29
pd=2.58
ps=2.58
nrd=0.29
nrs=0.29
sa=0
sb=0
sd=0
mult=2.0
model=pfet_01v8_lvt
spiceprefix=X
}
C {lab_pin.sym} -620 -320 2 1 {name=p32 sig_type=std_logic lab=ntap}
C {lab_pin.sym} -280 -320 2 0 {name=p33 sig_type=std_logic lab=ntap}
C {lab_wire.sym} -580 -180 3 0 {name=p34 sig_type=std_logic lab=vd_m10}
C {lab_wire.sym} -260 -150 0 0 {name=p35 sig_type=std_logic lab=vref_int}
C {sky130_fd_pr/nfet_01v8_lvt.sym} -600 -60 0 0 {name=M7
L=2
W=2
nf=2
ad=0.29
as=0.58
pd=2.58
ps=5.16
nrd=0.145
nrs=0.145
sa=0
sb=0
sd=0
mult=2.0
model=nfet_01v8_lvt
spiceprefix=X
}
C {sky130_fd_pr/nfet_01v8_lvt.sym} -300 -60 0 1 {name=M8
L=2
W=2
nf=2
ad=0.29
as=0.58
pd=2.58
ps=5.16
nrd=0.145
nrs=0.145
sa=0
sb=0
sd=0
mult=2.0
model=nfet_01v8_lvt
spiceprefix=X
}
C {ipin.sym} -660 -60 0 0 {name=p3 lab=inn}
C {lab_pin.sym} -540 -60 2 0 {name=p36 sig_type=std_logic lab=ptap}
C {lab_pin.sym} -240 -60 2 0 {name=p37 sig_type=std_logic lab=inp}
C {lab_pin.sym} -370 -60 2 1 {name=p38 sig_type=std_logic lab=ptap}
C {lab_wire.sym} -520 20 0 0 {name=p39 sig_type=std_logic lab=vtail_slow}
C {sky130_fd_pr/nfet_01v8_lvt.sym} -470 80 0 0 {name=M9
L=5
W=1
nf=1
ad=0.29
as=0.29
pd=2.58
ps=2.58
nrd=0.29
nrs=0.29
sa=0
sb=0
sd=0
mult=2.0
model=nfet_01v8_lvt
spiceprefix=X
}
C {lab_pin.sym} -530 80 2 1 {name=p40 sig_type=std_logic lab=ibias1}
C {lab_pin.sym} -410 80 2 0 {name=p41 sig_type=std_logic lab=ptap}
C {sky130_fd_pr/nfet_01v8_lvt.sym} -180 -150 0 0 {name=MC
L=6
W=6
nf=1
ad=1.74
as=1.74
pd=12.58
ps=12.58
nrd=0.04833333333333333
nrs=0.04833333333333333
sa=0
sb=0
sd=0
mult=2.0
model=nfet_01v8_lvt
spiceprefix=X
}
C {lab_pin.sym} -160 -200 3 1 {name=p42 sig_type=std_logic lab=vss}
C {lab_pin.sym} -160 -100 3 0 {name=p43 sig_type=std_logic lab=vss}
C {lab_pin.sym} -120 -150 2 0 {name=p44 sig_type=std_logic lab=ptap}
C {devices/res.sym} 500 -320 0 0 {name=Rtap_R2
value=1m
m=1
}
C {iopin.sym} 500 -270 3 1 {name=p18 lab=ntap}
C {devices/res.sym} 500 160 2 0 {name=Rtap_R7
value=1m
m=1
}
C {iopin.sym} 500 90 1 1 {name=p19 lab=ptap}
C {iopin.sym} -700 -420 0 1 {name=p4 lab=vdd}
C {iopin.sym} -700 260 0 1 {name=p6 lab=vss}




C {sky130_fd_pr/nfet_01v8_lvt.sym} -640 640 0 0 {name=MDA
L=1
W=16
nf=4
ad=2.32
as=3.48
pd=17.16
ps=25.74
nrd=0.018125
nrs=0.018125
sa=0
sb=0
sd=0
mult=2.0
model=nfet_01v8_lvt
spiceprefix=X
}
N -620 610 -620 580 {lab=sa}
C {lab_pin.sym} -620 580 1 0 {name=pdm1 sig_type=std_logic lab=sa}
N -620 670 -620 700 {lab=sa}
C {lab_pin.sym} -620 700 3 0 {name=pdm2 sig_type=std_logic lab=sa}
N -660 640 -700 640 {lab=sa}
C {lab_pin.sym} -700 640 0 0 {name=pdm3 sig_type=std_logic lab=sa}
N -620 640 -580 640 {lab=ptap}
C {lab_pin.sym} -580 640 2 0 {name=pdm4 sig_type=std_logic lab=ptap}
C {sky130_fd_pr/nfet_01v8_lvt.sym} -400 640 0 0 {name=MDB
L=1
W=16
nf=4
ad=2.32
as=3.48
pd=17.16
ps=25.74
nrd=0.018125
nrs=0.018125
sa=0
sb=0
sd=0
mult=2.0
model=nfet_01v8_lvt
spiceprefix=X
}
N -380 610 -380 580 {lab=sb}
C {lab_pin.sym} -380 580 1 0 {name=pdm5 sig_type=std_logic lab=sb}
N -380 670 -380 700 {lab=sb}
C {lab_pin.sym} -380 700 3 0 {name=pdm6 sig_type=std_logic lab=sb}
N -420 640 -460 640 {lab=sb}
C {lab_pin.sym} -460 640 0 0 {name=pdm7 sig_type=std_logic lab=sb}
N -380 640 -340 640 {lab=ptap}
C {lab_pin.sym} -340 640 2 0 {name=pdm8 sig_type=std_logic lab=ptap}
C {sky130_fd_pr/nfet_01v8_lvt.sym} -160 640 0 0 {name=MD3
L=2
W=16
nf=4
ad=2.32
as=3.48
pd=17.16
ps=25.74
nrd=0.018125
nrs=0.018125
sa=0
sb=0
sd=0
mult=2.0
model=nfet_01v8_lvt
spiceprefix=X
}
N -140 610 -140 580 {lab=vss}
C {lab_pin.sym} -140 580 1 0 {name=pdm9 sig_type=std_logic lab=vss}
N -140 670 -140 700 {lab=vss}
C {lab_pin.sym} -140 700 3 0 {name=pdm10 sig_type=std_logic lab=vss}
N -180 640 -220 640 {lab=vss}
C {lab_pin.sym} -220 640 0 0 {name=pdm11 sig_type=std_logic lab=vss}
N -140 640 -100 640 {lab=ptap}
C {lab_pin.sym} -100 640 2 0 {name=pdm12 sig_type=std_logic lab=ptap}
C {sky130_fd_pr/pfet_01v8_lvt.sym} 80 640 0 0 {name=MD5
L=1
W=4.4
nf=2
ad=0.638
as=1.276
pd=4.98
ps=9.96
nrd=0.0659090909090909
nrs=0.0659090909090909
sa=0
sb=0
sd=0
mult=2.0
model=pfet_01v8_lvt
spiceprefix=X
}
N 100 610 100 580 {lab=vd_m5}
C {lab_pin.sym} 100 580 1 0 {name=pdm13 sig_type=std_logic lab=vd_m5}
N 100 670 100 700 {lab=vd_m5}
C {lab_pin.sym} 100 700 3 0 {name=pdm14 sig_type=std_logic lab=vd_m5}
N 60 640 20 640 {lab=vdd}
C {lab_pin.sym} 20 640 0 0 {name=pdm15 sig_type=std_logic lab=vdd}
N 100 640 140 640 {lab=ntap}
C {lab_pin.sym} 140 640 2 0 {name=pdm16 sig_type=std_logic lab=ntap}
C {sky130_fd_pr/nfet_01v8_lvt.sym} 320 640 0 0 {name=MD7
L=2
W=2
nf=2
ad=0.29
as=0.58
pd=2.58
ps=5.16
nrd=0.145
nrs=0.145
sa=0
sb=0
sd=0
mult=2.0
model=nfet_01v8_lvt
spiceprefix=X
}
N 340 610 340 580 {lab=vd_m10}
C {lab_pin.sym} 340 580 1 0 {name=pdm17 sig_type=std_logic lab=vd_m10}
N 340 670 340 700 {lab=vd_m10}
C {lab_pin.sym} 340 700 3 0 {name=pdm18 sig_type=std_logic lab=vd_m10}
N 300 640 260 640 {lab=vd_m10}
C {lab_pin.sym} 260 640 0 0 {name=pdm19 sig_type=std_logic lab=vd_m10}
N 340 640 380 640 {lab=ptap}
C {lab_pin.sym} 380 640 2 0 {name=pdm20 sig_type=std_logic lab=ptap}
C {sky130_fd_pr/pfet_01v8_lvt.sym} 560 640 0 0 {name=MD10
L=4
W=1
nf=1
ad=0.29
as=0.29
pd=2.58
ps=2.58
nrd=0.29
nrs=0.29
sa=0
sb=0
sd=0
mult=2.0
model=pfet_01v8_lvt
spiceprefix=X
}
N 580 610 580 580 {lab=vd_m10}
C {lab_pin.sym} 580 580 1 0 {name=pdm21 sig_type=std_logic lab=vd_m10}
N 580 670 580 700 {lab=vd_m10}
C {lab_pin.sym} 580 700 3 0 {name=pdm22 sig_type=std_logic lab=vd_m10}
N 540 640 500 640 {lab=vdd}
C {lab_pin.sym} 500 640 0 0 {name=pdm23 sig_type=std_logic lab=vdd}
N 580 640 620 640 {lab=ntap}
C {lab_pin.sym} 620 640 2 0 {name=pdm24 sig_type=std_logic lab=ntap}
C {sky130_fd_pr/pfet_01v8_lvt.sym} 800 640 0 0 {name=MD11
L=4
W=1
nf=1
ad=0.29
as=0.29
pd=2.58
ps=2.58
nrd=0.29
nrs=0.29
sa=0
sb=0
sd=0
mult=2.0
model=pfet_01v8_lvt
spiceprefix=X
}
N 820 610 820 580 {lab=vref_int}
C {lab_pin.sym} 820 580 1 0 {name=pdm25 sig_type=std_logic lab=vref_int}
N 820 670 820 700 {lab=vref_int}
C {lab_pin.sym} 820 700 3 0 {name=pdm26 sig_type=std_logic lab=vref_int}
N 780 640 740 640 {lab=vdd}
C {lab_pin.sym} 740 640 0 0 {name=pdm27 sig_type=std_logic lab=vdd}
N 820 640 860 640 {lab=ntap}
C {lab_pin.sym} 860 640 2 0 {name=pdm28 sig_type=std_logic lab=ntap}
C {sky130_fd_pr/nfet_01v8_lvt.sym} 1040 640 0 0 {name=MD8
L=2
W=2
nf=2
ad=0.29
as=0.58
pd=2.58
ps=5.16
nrd=0.145
nrs=0.145
sa=0
sb=0
sd=0
mult=2.0
model=nfet_01v8_lvt
spiceprefix=X
}
N 1060 610 1060 580 {lab=vref_int}
C {lab_pin.sym} 1060 580 1 0 {name=pdm29 sig_type=std_logic lab=vref_int}
N 1060 670 1060 700 {lab=vref_int}
C {lab_pin.sym} 1060 700 3 0 {name=pdm30 sig_type=std_logic lab=vref_int}
N 1020 640 980 640 {lab=vss}
C {lab_pin.sym} 980 640 0 0 {name=pdm31 sig_type=std_logic lab=vss}
N 1060 640 1100 640 {lab=ptap}
C {lab_pin.sym} 1100 640 2 0 {name=pdm32 sig_type=std_logic lab=ptap}













N 800 100 800 140 {}
N 830 80 870 80 {}
C {devices/lab_pin.sym} 850 80 1 0 {name=candidate_label53 sig_type=std_logic lab=rs1}
N 900 100 900 140 {}
N 930 80 970 80 {}
C {devices/lab_pin.sym} 950 80 1 0 {name=candidate_label54 sig_type=std_logic lab=rs2}
N 1000 100 1000 140 {}
N 1030 80 1070 80 {}
C {devices/lab_pin.sym} 1050 80 1 0 {name=candidate_label55 sig_type=std_logic lab=rs3}
N 1100 100 1100 140 {}
N 1130 80 1170 80 {}
C {devices/lab_pin.sym} 1150 80 1 0 {name=candidate_label56 sig_type=std_logic lab=rs4}
N 1200 100 1200 140 {}
N 1230 80 1270 80 {}
C {devices/lab_pin.sym} 1250 80 1 0 {name=candidate_label57 sig_type=std_logic lab=rs5}
N 1300 100 1300 140 {}
N 1330 80 1370 80 {}
C {devices/lab_pin.sym} 1350 80 1 0 {name=candidate_label58 sig_type=std_logic lab=rs6}
N 1400 100 1400 140 {}
N 1430 80 1470 80 {}
C {devices/lab_pin.sym} 1450 80 1 0 {name=candidate_label59 sig_type=std_logic lab=rs7}
N 1500 100 1500 140 {}
N 1530 80 1570 80 {}
C {devices/lab_pin.sym} 1550 80 1 0 {name=candidate_label60 sig_type=std_logic lab=rs8}
N 1600 100 1600 140 {}
N 1630 80 1670 80 {}
C {devices/lab_pin.sym} 1650 80 1 0 {name=candidate_label61 sig_type=std_logic lab=rs9}
N 1700 100 1700 140 {}
N 1730 80 1770 80 {}
C {devices/lab_pin.sym} 1750 80 1 0 {name=candidate_label62 sig_type=std_logic lab=rs10}
N 1800 100 1800 140 {}
N 1830 80 1870 80 {}
C {devices/lab_pin.sym} 1850 80 1 0 {name=candidate_label63 sig_type=std_logic lab=rs11}
N 1900 100 1900 140 {}
N 800 140 1900 140 {}
C {devices/lab_pin.sym} 800 140 0 0 {name=candidate_label64 sig_type=std_logic lab=ptap}
N 730 80 770 80 {}
C {devices/lab_pin.sym} 730 80 0 0 {name=candidate_label65 sig_type=std_logic lab=sa}
N 1930 80 1970 80 {}
C {devices/lab_pin.sym} 1970 80 0 1 {name=candidate_label66 sig_type=std_logic lab=sb}
T {Fast-loop degeneration, twelve series resistor units} 760 -180 0 0 0.4 0.4 {}

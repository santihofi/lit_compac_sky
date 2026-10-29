v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
L 4 -40 -620 -40 -460 {}
L 4 -660 -460 -40 -460 {}
L 4 -660 -620 -660 -460 {}
L 4 -660 -620 -40 -620 {}
L 4 60 -660 60 -530 {}
L 4 60 -530 850 -530 {}
L 4 850 -660 850 -530 {}
L 4 60 -660 850 -660 {}
L 4 -320 -440 -320 -290 {}
L 4 -320 -290 0 -290 {}
L 4 -320 -440 0 -440 {}
L 4 -0 -440 0 -290 {}
L 4 -340 -20 680 -20 {}
L 4 -340 -150 -340 -20 {}
L 4 -340 -150 680 -150 {}
L 4 680 -150 680 -20 {}
L 4 90 -410 90 -210 {}
L 4 90 -210 810 -210 {}
L 4 810 -410 810 -210 {}
L 4 90 -410 810 -410 {}
T {p bulk
contact} 1250 -260 0 0 0.4 0.4 {}
T {tail_mirror} -430 -580 0 0 0.4 0.4 {}
T {active_load} 400 -620 0 0 0.4 0.4 {}
T {diff_pair_1} -210 -420 0 0 0.4 0.4 {}
T {cascode_mirror} 90 -90 0 0 0.4 0.4 {}
T {diff_pair_2} 390 -360 0 0 0.4 0.4 {}
T {gain_trim} 1150 -680 0 0 0.4 0.4 {}
N 150 -260 150 -240 {lab=#net1}
N 750 -260 750 -240 {lab=#net2}
N 450 -290 510 -290 {lab=in2p}
N 110 -290 110 -230 {lab=in2n}
N 110 -230 790 -230 {lab=in2n}
N 790 -290 790 -230 {lab=in2n}
N 150 -370 150 -320 {lab=outp}
N 550 -370 550 -320 {lab=outp}
N 150 -370 550 -370 {lab=outp}
N 350 -390 350 -320 {lab=outn}
N 350 -390 750 -390 {lab=outn}
N 450 -290 450 -190 {lab=in2p}
N 390 -290 450 -290 {lab=in2p}
N 550 -40 550 0 {lab=vss}
N 350 -40 350 0 {lab=vss}
N 350 -180 350 -100 {lab=#net1}
N 550 -160 550 -100 {lab=#net2}
N 250 -290 350 -290 {lab=ptap}
N 750 -780 750 -620 {lab=vdd}
N 150 -700 150 -640 {lab=vdd}
N 90 -610 90 -560 {lab=vbias}
N 90 -610 110 -610 {lab=vbias}
N 90 -560 710 -560 {lab=vbias}
N 710 -590 710 -560 {lab=vbias}
N 150 -440 150 -370 {lab=outp}
N 350 0 550 -0 {lab=vss}
N -60 -40 -60 0 {lab=vss}
N -260 -40 -260 0 {lab=vss}
N -260 0 -60 0 {lab=vss}
N -320 -70 -300 -70 {lab=#net3}
N -120 -70 -100 -70 {lab=#net4}
N -160 -700 -160 -580 {lab=vdd}
N -160 -700 150 -700 {lab=vdd}
N -260 -420 -260 -370 {lab=vcm1}
N -60 -420 -60 -370 {lab=vcm1}
N -160 -520 -160 -420 {lab=vcm1}
N -590 -700 -590 -570 {lab=vdd}
N -590 -700 -160 -700 {lab=vdd}
N -320 -130 -260 -130 {lab=#net3}
N -160 -340 -60 -340 {lab=ntap}
N 150 -780 150 -700 {lab=vdd}
N 510 -130 510 -70 {lab=#net3}
N -260 -130 510 -130 {lab=#net3}
N 310 -110 310 -70 {lab=#net4}
N 750 -440 750 -390 {lab=outn}
N 750 -390 750 -320 {lab=outn}
N -160 -550 -100 -550 {lab=ntap}
N -590 -490 -590 -430 {lab=ibias}
N -630 -540 -630 -490 {lab=ibias}
N -220 -550 -220 -490 {lab=ibias}
N -220 -550 -200 -550 {lab=ibias}
N -590 -490 -220 -490 {lab=ibias}
N -590 -510 -590 -490 {lab=ibias}
N -630 -490 -590 -490 {lab=ibias}
N -590 -540 -530 -540 {lab=ntap}
N -160 -350 -160 -340 {lab=ntap}
N -260 -340 -160 -340 {lab=ntap}
N 150 -780 750 -780 {lab=vdd}
N -260 -70 -210 -70 {lab=ptap}
N -60 -70 -10 -70 {lab=ptap}
N 550 -70 600 -70 {lab=ptap}
N 350 -70 400 -70 {lab=ptap}
N 650 -290 750 -290 {lab=ptap}
N 650 -310 650 -290 {lab=ptap}
N 250 -310 250 -290 {lab=ptap}
N 150 -290 250 -290 {lab=ptap}
N 550 -290 650 -290 {lab=ptap}
N 1290 -150 1290 -110 {lab=ptap}
N -660 -700 -590 -700 {lab=vdd}
N 1290 -50 1290 0 {lab=vss}
N -520 0 -260 -0 {lab=vss}
N -260 -130 -260 -100 {lab=#net3}
N -60 -110 -60 -100 {lab=#net4}
N 150 -440 180 -440 {lab=outp}
N 750 -440 780 -440 {lab=outn}
N 750 -590 790 -590 {lab=ntap}
N 150 -610 190 -610 {lab=ntap}
N -330 -340 -300 -340 {lab=in1n}
N -20 -340 10 -340 {lab=in1p}
N 70 -290 110 -290 {lab=in2n}
N -160 -420 -60 -420 {lab=vcm1}
N -260 -420 -160 -420 {lab=vcm1}
N 150 -240 250 -240 {lab=#net1}
N 250 -240 350 -240 {lab=#net1}
N 350 -260 350 -240 {lab=#net1}
N 550 -260 550 -240 {lab=#net2}
N 550 -240 650 -240 {lab=#net2}
N 650 -240 750 -240 {lab=#net2}
N 250 -180 350 -180 {lab=#net1}
N 250 -240 250 -180 {lab=#net1}
N 650 -240 650 -160 {lab=#net2}
N 550 -160 650 -160 {lab=#net2}
N -60 0 350 0 {lab=vss}
N 40 -560 90 -560 {lab=vbias}
N 150 -470 150 -440 {lab=outp}
N 150 -470 230 -470 {lab=outp}
N 150 -580 150 -470 {lab=outp}
N 750 -470 750 -440 {lab=outn}
N 550 -0 1290 -0 {lab=vss}
N 560 -470 750 -470 {lab=outn}
N 750 -560 750 -470 {lab=outn}
N -260 -310 -260 -130 {lab=#net3}
N -320 -130 -320 -70 {lab=#net3}
N -60 -110 310 -110 {lab=#net4}
N -60 -310 -60 -110 {lab=#net4}
N -120 -110 -60 -110 {lab=#net4}
N -120 -110 -120 -70 {lab=#net4}
N 750 -780 950 -780 {lab=vdd}
N 950 -780 950 -730 {lab=vdd}
N 950 -670 950 -650 {lab=ntap}
N 290 -470 320 -470 {lab=t4p}
N 500 -470 470 -470 {lab=t4n}
N 1050 -520 1130 -520 {lab=gt0}
N 1050 -540 1130 -540 {lab=gt1}
N 1050 -560 1130 -560 {lab=gt2}
N 1050 -580 1130 -580 {lab=gt3}
N 1050 -600 1130 -600 {lab=gt4}
N 1330 -600 1370 -600 {lab=t4p}
N 1330 -560 1370 -560 {lab=vcm}
N 1330 -520 1370 -520 {lab=t4n}
N 1230 -460 1230 -440 {lab=ptap}
C {devices/title.sym} -410 90 0 0 {name=l5 author="Santiago Hofwimmer | JKU IICQC"}
C {sky130_fd_pr/nfet_01v8_lvt.sym} 330 -70 0 0 {name=M5
L=1.25
W=20
nf=4
mult=1
model=nfet_01v8_lvt
spiceprefix=X
}
C {sky130_fd_pr/nfet_01v8_lvt.sym} 530 -70 0 0 {name=M6
L=1.25
W=20
nf=4
mult=1
model=nfet_01v8_lvt
spiceprefix=X
}
C {sky130_fd_pr/nfet_01v8_lvt.sym} 130 -290 0 0 {name=M7
L=0.5
W=20
nf=4
mult=1
model=nfet_01v8_lvt
spiceprefix=X
}
C {sky130_fd_pr/nfet_01v8_lvt.sym} 530 -290 0 0 {name=M9
L=0.5
W=20
nf=4
mult=1
model=nfet_01v8_lvt
spiceprefix=X
}
C {sky130_fd_pr/nfet_01v8_lvt.sym} 770 -290 0 1 {name=M10
L=0.5
W=20
nf=4
mult=1
model=nfet_01v8_lvt
spiceprefix=X
}
C {sky130_fd_pr/nfet_01v8_lvt.sym} 370 -290 0 1 {name=M8
L=0.5
W=20
nf=4
mult=1
model=nfet_01v8_lvt
spiceprefix=X
}
C {sky130_fd_pr/pfet_01v8_lvt.sym} 130 -610 0 0 {name=M11
L=1
W=32
nf=8
mult=1
model=pfet_01v8_lvt
spiceprefix=X
}
C {sky130_fd_pr/pfet_01v8_lvt.sym} 730 -590 0 0 {name=M12
L=1
W=32
nf=8
mult=1
model=pfet_01v8_lvt
spiceprefix=X
}
C {iopin.sym} -660 -700 2 0 {name=p3 lab=vdd}
C {ipin.sym} -330 -340 0 0 {name=p4 lab=in1n}
C {opin.sym} 180 -440 0 0 {name=p5 lab=outp}
C {opin.sym} 780 -440 0 0 {name=p7 lab=outn}
C {iopin.sym} -520 0 2 0 {name=p9 lab=vss}
C {ipin.sym} 10 -340 0 1 {name=p10 lab=in1p}
C {ipin.sym} 70 -290 0 0 {name=p6 lab=in2n}
C {ipin.sym} 450 -190 2 0 {name=p8 lab=in2p}
C {ipin.sym} 40 -560 2 1 {name=p2 lab=vbias}
C {sky130_fd_pr/pfet_01v8_lvt.sym} -280 -340 0 0 {name=M1
L=0.35
W=74.625
nf=12
mult=1
model=pfet_01v8_lvt
spiceprefix=X
}
C {sky130_fd_pr/pfet_01v8_lvt.sym} -180 -550 0 0 {name=M13
L=0.65
W=40
nf=4
mult=8
model=pfet_01v8_lvt
spiceprefix=X
}
C {sky130_fd_pr/nfet_01v8_lvt.sym} -280 -70 0 0 {name=M3
L=1.25
W=20
nf=4
mult=1
model=nfet_01v8_lvt
spiceprefix=X
}
C {sky130_fd_pr/nfet_01v8_lvt.sym} -80 -70 0 0 {name=M4
L=1.25
W=20
nf=4
mult=1
model=nfet_01v8_lvt
spiceprefix=X
}
C {sky130_fd_pr/pfet_01v8_lvt.sym} -40 -340 0 1 {name=M2
L=0.35
W=74.625
nf=12
mult=1
model=pfet_01v8_lvt
spiceprefix=X
}
C {sky130_fd_pr/pfet_01v8_lvt.sym} -610 -540 0 0 {name=M14
L=0.65
W=40
nf=4
mult=1
model=pfet_01v8_lvt
spiceprefix=X
}
C {ipin.sym} -590 -430 3 0 {name=p11 lab=ibias}
C {lab_pin.sym} -530 -540 2 0 {name=p13 sig_type=std_logic lab=ntap}
C {lab_pin.sym} -100 -550 2 0 {name=p14 sig_type=std_logic lab=ntap}
C {lab_pin.sym} 190 -610 2 0 {name=p15 sig_type=std_logic lab=ntap}
C {lab_pin.sym} 790 -590 2 0 {name=p16 sig_type=std_logic lab=ntap}
C {lab_pin.sym} -160 -350 1 0 {name=p17 sig_type=std_logic lab=ntap}
C {lab_pin.sym} -210 -70 2 0 {name=p21 sig_type=std_logic lab=ptap}
C {lab_pin.sym} -10 -70 2 0 {name=p22 sig_type=std_logic lab=ptap}
C {lab_pin.sym} 400 -70 2 0 {name=p23 sig_type=std_logic lab=ptap}
C {lab_pin.sym} 600 -70 2 0 {name=p24 sig_type=std_logic lab=ptap}
C {lab_pin.sym} 650 -310 1 0 {name=p25 sig_type=std_logic lab=ptap}
C {lab_pin.sym} 250 -310 1 0 {name=p26 sig_type=std_logic lab=ptap}
C {devices/res.sym} 1290 -80 2 0 {name=Rtap_R1
value=1m
lvs_ignore=short
}
C {lab_pin.sym} 1290 -110 2 1 {name=p29 sig_type=std_logic lab=ptap}
C {sky130_fd_pr/annotate_fet_params.sym} -200 -850 0 0 {name=annot1 ref=M7
}
C {sky130_fd_pr/annotate_fet_params.sym} -630 -850 0 0 {name=annot2 ref=M14

}
C {sky130_fd_pr/annotate_fet_params.sym} 620 10 0 0 {name=annot3 ref=M10}
C {sky130_fd_pr/annotate_fet_params.sym} -430 -150 0 0 {name=annot4 ref=M3}
C {sky130_fd_pr/annotate_fet_params.sym} 40 -850 0 0 {name=annot5 ref=M1
}
C {sky130_fd_pr/annotate_fet_params.sym} 820 -410 0 0 {name=annot6 ref=M8}
C {sky130_fd_pr/annotate_fet_params.sym} -370 -290 0 0 {name=annot7 ref=M6}
C {sky130_fd_pr/res_high_po_5p73.sym} 260 -470 3 0 {name=R7
L=13.035
mult=1
model=res_high_po_5p73
spiceprefix=X
}
C {iopin.sym} 1290 -150 3 0 {name=p31 lab=ptap}
C {sky130_fd_pr/res_high_po_5p73.sym} 530 -470 3 0 {name=R5
L=13.035
mult=1
model=res_high_po_5p73
spiceprefix=X
}
C {opin.sym} 400 -430 0 0 {name=p33 lab=vcm}
C {isource.sym} -590 -140 0 0 {name=I0 value=5u
spice_ignore=true}
C {lab_pin.sym} -260 -420 0 0 {name=p1 sig_type=std_logic lab=vcm1}
C {devices/res.sym} 950 -700 0 0 {name=Rtap_R2
value=1m
lvs_ignore=short
}
C {iopin.sym} 950 -650 1 0 {name=p12 lab=ntap}
C {lab_pin.sym} 320 -470 2 0 {name=lt1 sig_type=std_logic lab=t4p}
C {lab_pin.sym} 470 -470 0 0 {name=lt2 sig_type=std_logic lab=t4n}
C {lit_compac_sky/macros/gilbert_cell/schematic/xschem/gain_trim.sym} 1150 -480 0 0 {name=xtrim}
C {ipin.sym} 1050 -520 0 0 {name=pgt0 lab=gt0}
C {ipin.sym} 1050 -540 0 0 {name=pgt1 lab=gt1}
C {ipin.sym} 1050 -560 0 0 {name=pgt2 lab=gt2}
C {ipin.sym} 1050 -580 0 0 {name=pgt3 lab=gt3}
C {ipin.sym} 1050 -600 0 0 {name=pgt4 lab=gt4}
C {lab_pin.sym} 1370 -600 2 0 {name=lt3 sig_type=std_logic lab=t4p}
C {lab_pin.sym} 1370 -560 2 0 {name=lt4 sig_type=std_logic lab=vcm}
C {lab_pin.sym} 1370 -520 2 0 {name=lt5 sig_type=std_logic lab=t4n}
C {lab_pin.sym} 1230 -440 3 0 {name=lt6 sig_type=std_logic lab=ptap}
C {lab_pin.sym} 250 -180 3 0 {name=pdm1 sig_type=std_logic lab=qs1}
C {lab_pin.sym} 650 -160 3 0 {name=pdm2 sig_type=std_logic lab=qs2}
C {sky130_fd_pr/pfet_01v8_lvt.sym} -560 420 0 0 {name=MDP
L=0.35
W=24.875
nf=4
mult=1
model=pfet_01v8_lvt
spiceprefix=X
}
N -540 390 -540 360 {lab=vcm1}
C {lab_pin.sym} -540 360 1 0 {name=pdm3 sig_type=std_logic lab=vcm1}
N -540 450 -540 480 {lab=vcm1}
C {lab_pin.sym} -540 480 3 0 {name=pdm4 sig_type=std_logic lab=vcm1}
N -580 420 -620 420 {lab=vcm1}
C {lab_pin.sym} -620 420 0 0 {name=pdm5 sig_type=std_logic lab=vcm1}
N -540 420 -500 420 {lab=ntap}
C {lab_pin.sym} -500 420 2 0 {name=pdm6 sig_type=std_logic lab=ntap}
C {sky130_fd_pr/nfet_01v8_lvt.sym} -300 420 0 0 {name=MDM
L=1.25
W=10
nf=2
mult=1
model=nfet_01v8_lvt
spiceprefix=X
}
N -280 390 -280 360 {lab=vss}
C {lab_pin.sym} -280 360 1 0 {name=pdm7 sig_type=std_logic lab=vss}
N -280 450 -280 480 {lab=vss}
C {lab_pin.sym} -280 480 3 0 {name=pdm8 sig_type=std_logic lab=vss}
N -320 420 -360 420 {lab=vss}
C {lab_pin.sym} -360 420 0 0 {name=pdm9 sig_type=std_logic lab=vss}
N -280 420 -240 420 {lab=ptap}
C {lab_pin.sym} -240 420 2 0 {name=pdm10 sig_type=std_logic lab=ptap}
C {sky130_fd_pr/nfet_01v8_lvt.sym} -40 420 0 0 {name=MDQ1
L=0.5
W=20
nf=4
mult=1
model=nfet_01v8_lvt
spiceprefix=X
}
N -20 390 -20 360 {lab=qs1}
C {lab_pin.sym} -20 360 1 0 {name=pdm11 sig_type=std_logic lab=qs1}
N -20 450 -20 480 {lab=qs1}
C {lab_pin.sym} -20 480 3 0 {name=pdm12 sig_type=std_logic lab=qs1}
N -60 420 -100 420 {lab=qs1}
C {lab_pin.sym} -100 420 0 0 {name=pdm13 sig_type=std_logic lab=qs1}
N -20 420 20 420 {lab=ptap}
C {lab_pin.sym} 20 420 2 0 {name=pdm14 sig_type=std_logic lab=ptap}
C {sky130_fd_pr/nfet_01v8_lvt.sym} 220 420 0 0 {name=MDQ2
L=0.5
W=20
nf=4
mult=1
model=nfet_01v8_lvt
spiceprefix=X
}
N 240 390 240 360 {lab=qs2}
C {lab_pin.sym} 240 360 1 0 {name=pdm15 sig_type=std_logic lab=qs2}
N 240 450 240 480 {lab=qs2}
C {lab_pin.sym} 240 480 3 0 {name=pdm16 sig_type=std_logic lab=qs2}
N 200 420 160 420 {lab=qs2}
C {lab_pin.sym} 160 420 0 0 {name=pdm17 sig_type=std_logic lab=qs2}
N 240 420 280 420 {lab=ptap}
C {lab_pin.sym} 280 420 2 0 {name=pdm18 sig_type=std_logic lab=ptap}
C {sky130_fd_pr/pfet_01v8_lvt.sym} 480 420 0 0 {name=MDL
L=1
W=16
nf=4
mult=1
model=pfet_01v8_lvt
spiceprefix=X
}
N 500 390 500 360 {lab=vdd}
C {lab_pin.sym} 500 360 1 0 {name=pdm19 sig_type=std_logic lab=vdd}
N 500 450 500 480 {lab=vdd}
C {lab_pin.sym} 500 480 3 0 {name=pdm20 sig_type=std_logic lab=vdd}
N 460 420 420 420 {lab=vdd}
C {lab_pin.sym} 420 420 0 0 {name=pdm21 sig_type=std_logic lab=vdd}
N 500 420 540 420 {lab=ntap}
C {lab_pin.sym} 540 420 2 0 {name=pdm22 sig_type=std_logic lab=ntap}
C {sky130_fd_pr/pfet_01v8_lvt.sym} 740 420 0 0 {name=MDT
L=0.65
W=20
nf=2
mult=1
model=pfet_01v8_lvt
spiceprefix=X
}
N 760 390 760 360 {lab=vdd}
C {lab_pin.sym} 760 360 1 0 {name=pdm23 sig_type=std_logic lab=vdd}
N 760 450 760 480 {lab=vdd}
C {lab_pin.sym} 760 480 3 0 {name=pdm24 sig_type=std_logic lab=vdd}
N 720 420 680 420 {lab=vdd}
C {lab_pin.sym} 680 420 0 0 {name=pdm25 sig_type=std_logic lab=vdd}
N 760 420 800 420 {lab=ntap}
C {lab_pin.sym} 800 420 2 0 {name=pdm26 sig_type=std_logic lab=ntap}
T {dummies: one finger at each row end, source and drain on the node that ends the row; gate on the rail, or for the
pair (MDP) and quad (MDQ1/MDQ2) dummies on that node too (all terminals one net, off at Vgs = 0).
R1/R2 tap devices: lvs_ignore=open, the tap rings are the ntap/ptap nets themselves (LVS with tap extraction off).} -600 300 0 0 0.3 0.3 {}
T {Layout plan. Every matched device has an even finger count, fingers paired around a drain, sources at the row ends,
so half the fingers of each device conduct one way and half the other (anisotropy cancels). Fingers at most 10 um.
-) M1/M2 59.7/0.28, 12 fingers of 4.975 um each: two rows ABBAAB over BAABBA in groups of 2 (2D common centroid), vcm1 at the row ends, dummies MDP (4)
-) M3..M6 20/1.25, 4 fingers each: one row M3 M6 M4 M5 M5 M4 M6 M3 in groups of 2 (mirror partners side by side), vss at the ends, dummies MDM
-) M7..M10 20/0.5, 4 fingers each: two rows, M7 M8 + M10 M9 over M9 M10 + M8 M7, sub-rows end on qs1 or qs2, dummies MDQ1/MDQ2
-) M11/M12 32/1, 8 fingers of 4 um each: two rows ABBA over BAAB in groups of 2 (2D common centroid), vdd at the row ends, dummies MDL (4)
-) M13/M14 from 40/0.65 um units of four 10 um fingers, M13 = 8 units, M14 = 1 unit: one row AAAA B AAAA, dummies MDT
   (320 um, not 640: the larger tail coupled input-CM steps into the output CM and the tree rang 0.13;
   L 0.65 um: at 1 um the tail had too little headroom and 20 mV supply kicks rang the tree's output CM, at 0.5 um
   its higher output conductance let an input-CM step ring the cell at tt, at 0.7 um a supply drop still rang ss 80 C)
-) tail 320 uA = 8 x ibias, R7/R5 rppd 3/9.01 um plus the gain trim ladder, about 1.43 kOhm per half at code 13 for K = 10 at tt} -600 560 0 0 0.3 0.3 {}
C {sky130_fd_pr/res_high_po_5p73.sym} -560 900 0 0 {name=RD1
L=13.035
mult=1
model=res_high_po_5p73
spiceprefix=X
}
N -560 870 -560 840 {lab=ntap}
C {lab_pin.sym} -560 840 1 0 {name=pdm101 sig_type=std_logic lab=ntap}
N -560 930 -560 960 {lab=ntap}
C {lab_pin.sym} -560 960 3 0 {name=pdm102 sig_type=std_logic lab=ntap}
C {sky130_fd_pr/res_high_po_5p73.sym} -420 900 0 0 {name=RD2
L=13.035
mult=1
model=res_high_po_5p73
spiceprefix=X
}
N -420 870 -420 840 {lab=ntap}
C {lab_pin.sym} -420 840 1 0 {name=pdm103 sig_type=std_logic lab=ntap}
N -420 930 -420 960 {lab=ntap}
C {lab_pin.sym} -420 960 3 0 {name=pdm104 sig_type=std_logic lab=ntap}
T {RD1/RD2: rppd dummies (3 x 9.01 um) at both sides of R7/R5, in the PMOS ring's NWell with them: heads and body on ntap} -600 800 0 0 0.3 0.3 {}
C {devices/lab_pin.sym} -440 900 0 0 {name=body_RD2 lab=ptap}
C {devices/lab_pin.sym} -580 900 0 0 {name=body_RD1 lab=ptap}
C {devices/lab_pin.sym} 530 -450 0 0 {name=body_R5 lab=ptap}
C {devices/lab_pin.sym} 260 -450 0 0 {name=body_R7 lab=ptap}

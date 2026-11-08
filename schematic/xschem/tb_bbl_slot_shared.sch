v {xschem version=3.4.5 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {tb_bbl_slot_shared: slot with harness bus switch, bus line and LED amplifier input per bus} -700 -700 0 0 0.6 0.6 {}
T {dig_in in the code block (N0 tuning code 1 here); vbias open (on-chip pull-up: full coupling)} -700 -650 0 0 0.3 0.3 {}
T {LED amplifier: ultra-high-impedance input modelled as 1 Tohm || 5 pF; Cb = bus line + pad (+ external)} -700 -620 0 0 0.3 0.3 {}
N -130 -490 -100 -490 {lab=vdd_3v3}
N -130 -470 -100 -470 {lab=vss_3v3}
N -130 -450 -100 -450 {lab=vdd_1v2}
N -130 -430 -100 -430 {lab=vss_1v2}
N -130 -410 -100 -410 {lab=enable}
N -130 -390 -100 -390 {lab=clk}
N -130 -370 -100 -370 {lab=reset}
N -130 -350 -100 -350 {lab=dig_in[0]}
N -130 -330 -100 -330 {lab=dig_in[1]}
N -130 -310 -100 -310 {lab=dig_in[2]}
N -130 -290 -100 -290 {lab=dig_in[3]}
N -130 -270 -100 -270 {lab=dig_in[4]}
N -130 -250 -100 -250 {lab=dig_in[5]}
N -130 -230 -100 -230 {lab=dig_in[6]}
N -130 -210 -100 -210 {lab=dig_in[7]}
N -130 -190 -100 -190 {lab=dig_in[8]}
N -130 -170 -100 -170 {lab=dig_in[9]}
N -130 -150 -100 -150 {lab=dig_in[10]}
N -130 -130 -100 -130 {lab=dig_in[11]}
N -130 -110 -100 -110 {lab=dig_in[12]}
N -130 -90 -100 -90 {lab=dig_in[13]}
N -130 -70 -100 -70 {lab=dig_in[14]}
N -130 -50 -100 -50 {lab=dig_in[15]}
N -130 -30 -100 -30 {lab=dig_in[16]}
N -130 -10 -100 -10 {lab=dig_in[17]}
N -130 10 -100 10 {lab=dig_in[18]}
N -130 30 -100 30 {lab=dig_in[19]}
N -130 50 -100 50 {lab=dig_in[20]}
N -130 70 -100 70 {lab=dig_in[21]}
N -130 90 -100 90 {lab=dig_in[22]}
N -130 110 -100 110 {lab=dig_in[23]}
N -130 130 -100 130 {lab=dig_out[0]}
N -130 150 -100 150 {lab=dig_out[1]}
N -130 170 -100 170 {lab=dig_out[2]}
N -130 190 -100 190 {lab=dig_out[3]}
N -130 210 -100 210 {lab=dig_out[4]}
N -130 230 -100 230 {lab=dig_out[5]}
N -130 250 -100 250 {lab=dig_out[6]}
N -130 270 -100 270 {lab=dig_out[7]}
N -130 290 -100 290 {lab=dig_out[8]}
N -130 310 -100 310 {lab=dig_out[9]}
N -130 330 -100 330 {lab=dig_out[10]}
N -130 350 -100 350 {lab=dig_out[11]}
N -130 370 -100 370 {lab=analog_bus0}
N -130 390 -100 390 {lab=analog_bus1}
N -130 410 -100 410 {lab=analog_bus2}
N -130 430 -100 430 {lab=analog_bus3}
N -130 450 -100 450 {lab=vbias}
N -130 470 -100 470 {lab=ibias0}
N -130 490 -100 490 {lab=ibias1}
N -700 730 200 730 {lab=0}
N -600 670 -600 640 {lab=vdd_3v3}
N -440 670 -440 640 {lab=vdd_1v2}
N -280 670 -280 640 {lab=enable}
N -120 670 -120 640 {lab=vss_3v3}
N 40 670 40 640 {lab=vss_1v2}
N 640 -300 700 -300 {lab=analog_bus0}
N 760 -300 940 -300 {lab=busx0}
N 790 -300 790 -260 {lab=busx0}
N 850 -300 850 -260 {lab=busx0}
N 910 -300 910 -260 {lab=busx0}
N 640 -100 700 -100 {lab=analog_bus1}
N 760 -100 940 -100 {lab=busx1}
N 790 -100 790 -60 {lab=busx1}
N 850 -100 850 -60 {lab=busx1}
N 910 -100 910 -60 {lab=busx1}
N 640 100 700 100 {lab=analog_bus2}
N 760 100 940 100 {lab=busx2}
N 790 100 790 140 {lab=busx2}
N 850 100 850 140 {lab=busx2}
N 910 100 910 140 {lab=busx2}
N 640 300 700 300 {lab=analog_bus3}
N 760 300 940 300 {lab=busx3}
N 790 300 790 340 {lab=busx3}
N 850 300 850 340 {lab=busx3}
N 910 300 910 340 {lab=busx3}
C {bbl_slot_shared.sym} 0 0 0 0 {name=x1}
C {lab_pin.sym} -130 -490 0 0 {name=l1 sig_type=std_logic lab=vdd_3v3}
C {lab_pin.sym} -130 -470 0 0 {name=l2 sig_type=std_logic lab=vss_3v3}
C {lab_pin.sym} -130 -450 0 0 {name=l3 sig_type=std_logic lab=vdd_1v2}
C {lab_pin.sym} -130 -430 0 0 {name=l4 sig_type=std_logic lab=vss_1v2}
C {lab_pin.sym} -130 -410 0 0 {name=l5 sig_type=std_logic lab=enable}
C {lab_pin.sym} -130 -390 0 0 {name=l6 sig_type=std_logic lab=clk}
C {lab_pin.sym} -130 -370 0 0 {name=l7 sig_type=std_logic lab=reset}
C {lab_pin.sym} -130 -350 0 0 {name=l8 sig_type=std_logic lab=dig_in[0]}
C {lab_pin.sym} -130 -330 0 0 {name=l9 sig_type=std_logic lab=dig_in[1]}
C {lab_pin.sym} -130 -310 0 0 {name=l10 sig_type=std_logic lab=dig_in[2]}
C {lab_pin.sym} -130 -290 0 0 {name=l11 sig_type=std_logic lab=dig_in[3]}
C {lab_pin.sym} -130 -270 0 0 {name=l12 sig_type=std_logic lab=dig_in[4]}
C {lab_pin.sym} -130 -250 0 0 {name=l13 sig_type=std_logic lab=dig_in[5]}
C {lab_pin.sym} -130 -230 0 0 {name=l14 sig_type=std_logic lab=dig_in[6]}
C {lab_pin.sym} -130 -210 0 0 {name=l15 sig_type=std_logic lab=dig_in[7]}
C {lab_pin.sym} -130 -190 0 0 {name=l16 sig_type=std_logic lab=dig_in[8]}
C {lab_pin.sym} -130 -170 0 0 {name=l17 sig_type=std_logic lab=dig_in[9]}
C {lab_pin.sym} -130 -150 0 0 {name=l18 sig_type=std_logic lab=dig_in[10]}
C {lab_pin.sym} -130 -130 0 0 {name=l19 sig_type=std_logic lab=dig_in[11]}
C {lab_pin.sym} -130 -110 0 0 {name=l20 sig_type=std_logic lab=dig_in[12]}
C {lab_pin.sym} -130 -90 0 0 {name=l21 sig_type=std_logic lab=dig_in[13]}
C {lab_pin.sym} -130 -70 0 0 {name=l22 sig_type=std_logic lab=dig_in[14]}
C {lab_pin.sym} -130 -50 0 0 {name=l23 sig_type=std_logic lab=dig_in[15]}
C {lab_pin.sym} -130 -30 0 0 {name=l24 sig_type=std_logic lab=dig_in[16]}
C {lab_pin.sym} -130 -10 0 0 {name=l25 sig_type=std_logic lab=dig_in[17]}
C {lab_pin.sym} -130 10 0 0 {name=l26 sig_type=std_logic lab=dig_in[18]}
C {lab_pin.sym} -130 30 0 0 {name=l27 sig_type=std_logic lab=dig_in[19]}
C {lab_pin.sym} -130 50 0 0 {name=l28 sig_type=std_logic lab=dig_in[20]}
C {lab_pin.sym} -130 70 0 0 {name=l29 sig_type=std_logic lab=dig_in[21]}
C {lab_pin.sym} -130 90 0 0 {name=l30 sig_type=std_logic lab=dig_in[22]}
C {lab_pin.sym} -130 110 0 0 {name=l31 sig_type=std_logic lab=dig_in[23]}
C {lab_pin.sym} -130 130 0 0 {name=l32 sig_type=std_logic lab=dig_out[0]}
C {lab_pin.sym} -130 150 0 0 {name=l33 sig_type=std_logic lab=dig_out[1]}
C {lab_pin.sym} -130 170 0 0 {name=l34 sig_type=std_logic lab=dig_out[2]}
C {lab_pin.sym} -130 190 0 0 {name=l35 sig_type=std_logic lab=dig_out[3]}
C {lab_pin.sym} -130 210 0 0 {name=l36 sig_type=std_logic lab=dig_out[4]}
C {lab_pin.sym} -130 230 0 0 {name=l37 sig_type=std_logic lab=dig_out[5]}
C {lab_pin.sym} -130 250 0 0 {name=l38 sig_type=std_logic lab=dig_out[6]}
C {lab_pin.sym} -130 270 0 0 {name=l39 sig_type=std_logic lab=dig_out[7]}
C {lab_pin.sym} -130 290 0 0 {name=l40 sig_type=std_logic lab=dig_out[8]}
C {lab_pin.sym} -130 310 0 0 {name=l41 sig_type=std_logic lab=dig_out[9]}
C {lab_pin.sym} -130 330 0 0 {name=l42 sig_type=std_logic lab=dig_out[10]}
C {lab_pin.sym} -130 350 0 0 {name=l43 sig_type=std_logic lab=dig_out[11]}
C {lab_pin.sym} -130 370 0 0 {name=l44 sig_type=std_logic lab=analog_bus0}
C {lab_pin.sym} -130 390 0 0 {name=l45 sig_type=std_logic lab=analog_bus1}
C {lab_pin.sym} -130 410 0 0 {name=l46 sig_type=std_logic lab=analog_bus2}
C {lab_pin.sym} -130 430 0 0 {name=l47 sig_type=std_logic lab=analog_bus3}
C {lab_pin.sym} -130 450 0 0 {name=l48 sig_type=std_logic lab=vbias}
C {lab_pin.sym} -130 470 0 0 {name=l49 sig_type=std_logic lab=ibias0}
C {lab_pin.sym} -130 490 0 0 {name=l50 sig_type=std_logic lab=ibias1}
C {gnd.sym} -700 730 0 0 {name=l0 lab=0}
C {vsource.sym} -600 700 0 0 {name=Vdd33 value="pwl 0 0 100u 3.3" savecurrent=false}
C {lab_pin.sym} -600 640 0 1 {name=l53 sig_type=std_logic lab=vdd_3v3}
C {vsource.sym} -440 700 0 0 {name=Vdd12 value="pwl 0 0 100u 1.2" savecurrent=false}
C {lab_pin.sym} -440 640 0 1 {name=l55 sig_type=std_logic lab=vdd_1v2}
C {vsource.sym} -280 700 0 0 {name=Vena value="pwl 0 0 100u 0 200u 1.2" savecurrent=false}
C {lab_pin.sym} -280 640 0 1 {name=l57 sig_type=std_logic lab=enable}
C {vsource.sym} -120 700 0 0 {name=Vss33 value="0" savecurrent=false}
C {lab_pin.sym} -120 640 0 1 {name=l59 sig_type=std_logic lab=vss_3v3}
C {vsource.sym} 40 700 0 0 {name=Vss12 value="0" savecurrent=false}
C {lab_pin.sym} 40 640 0 1 {name=l61 sig_type=std_logic lab=vss_1v2}
C {lab_pin.sym} 640 -300 0 0 {name=l62 sig_type=std_logic lab=analog_bus0}
C {res.sym} 730 -300 1 0 {name=Rsw0 value=2k m=1}
C {lab_pin.sym} 940 -300 0 1 {name=l64 sig_type=std_logic lab=busx0}
C {capa.sym} 790 -230 0 0 {name=Cb0 value=3p m=1}
C {gnd.sym} 790 -200 0 0 {name=g00 lab=0}
C {res.sym} 850 -230 0 0 {name=Ramp0 value=1T m=1}
C {gnd.sym} 850 -200 0 0 {name=g01 lab=0}
C {capa.sym} 910 -230 0 0 {name=Camp0 value=5p m=1}
C {gnd.sym} 910 -200 0 0 {name=g02 lab=0}
C {lab_pin.sym} 640 -100 0 0 {name=l71 sig_type=std_logic lab=analog_bus1}
C {res.sym} 730 -100 1 0 {name=Rsw1 value=2k m=1}
C {lab_pin.sym} 940 -100 0 1 {name=l73 sig_type=std_logic lab=busx1}
C {capa.sym} 790 -30 0 0 {name=Cb1 value=3p m=1}
C {gnd.sym} 790 0 0 0 {name=g10 lab=0}
C {res.sym} 850 -30 0 0 {name=Ramp1 value=1T m=1}
C {gnd.sym} 850 0 0 0 {name=g11 lab=0}
C {capa.sym} 910 -30 0 0 {name=Camp1 value=5p m=1}
C {gnd.sym} 910 0 0 0 {name=g12 lab=0}
C {lab_pin.sym} 640 100 0 0 {name=l80 sig_type=std_logic lab=analog_bus2}
C {res.sym} 730 100 1 0 {name=Rsw2 value=2k m=1}
C {lab_pin.sym} 940 100 0 1 {name=l82 sig_type=std_logic lab=busx2}
C {capa.sym} 790 170 0 0 {name=Cb2 value=3p m=1}
C {gnd.sym} 790 200 0 0 {name=g20 lab=0}
C {res.sym} 850 170 0 0 {name=Ramp2 value=1T m=1}
C {gnd.sym} 850 200 0 0 {name=g21 lab=0}
C {capa.sym} 910 170 0 0 {name=Camp2 value=5p m=1}
C {gnd.sym} 910 200 0 0 {name=g22 lab=0}
C {lab_pin.sym} 640 300 0 0 {name=l89 sig_type=std_logic lab=analog_bus3}
C {res.sym} 730 300 1 0 {name=Rsw3 value=2k m=1}
C {lab_pin.sym} 940 300 0 1 {name=l91 sig_type=std_logic lab=busx3}
C {capa.sym} 790 370 0 0 {name=Cb3 value=3p m=1}
C {gnd.sym} 790 400 0 0 {name=g30 lab=0}
C {res.sym} 850 370 0 0 {name=Ramp3 value=1T m=1}
C {gnd.sym} 850 400 0 0 {name=g31 lab=0}
C {capa.sym} 910 370 0 0 {name=Camp3 value=5p m=1}
C {gnd.sym} 910 400 0 0 {name=g32 lab=0}
C {code_shown.sym} -700 900 0 0 {name=s1 only_toplevel=false value=".lib cornerMOShv.lib mos_tt
.lib cornerMOSlv.lib mos_tt
.lib cornerRES.lib res_typ
.option gmin=1e-15 reltol=1e-3 abstol=1e-14 method=gear
Vd0 dig_in[0] 0 1.2
Vd1 dig_in[1] 0 0
Vd2 dig_in[2] 0 0
Vd3 dig_in[3] 0 0
Vd4 dig_in[4] 0 0
Vd5 dig_in[5] 0 0
Vd6 dig_in[6] 0 0
Vd7 dig_in[7] 0 0
Vd8 dig_in[8] 0 0
Vd9 dig_in[9] 0 0
Vd10 dig_in[10] 0 0
Vd11 dig_in[11] 0 0
Vd12 dig_in[12] 0 0
Vd13 dig_in[13] 0 0
Vd14 dig_in[14] 0 0
Vd15 dig_in[15] 0 0
Vd16 dig_in[16] 0 0
Vd17 dig_in[17] 0 0
Vd18 dig_in[18] 0 0
Vd19 dig_in[19] 0 0
Vd20 dig_in[20] 0 0
Vd21 dig_in[21] 0 0
Vd22 dig_in[22] 0 0
Vd23 dig_in[23] 0 0
.control
tran 10u 2.5
wrdata tb_bbl_slot_shared.dat v(analog_bus0) v(analog_bus1) v(analog_bus2) v(analog_bus3)
.endc
"}

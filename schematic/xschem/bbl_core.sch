v {xschem version=3.4.5 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {bbl_core: four neurons, synapses, gap junctions, bus coupling} -600 -560 0 0 0.6 0.6 {}
T {N0, N1: LED drivers XL0 / XL1 on analog_bus0 / 1; synapses XS01 / XS10; gap junction XG01} -600 -510 0 0 0.3 0.3 {}
T {N2, N3: membranes on analog_bus2 / 3 through XMP2 / XMP3 (gate vcplb); XG32 couples N3 to bus2} -600 -480 0 0 0.3 0.3 {}
N -290 -390 -290 -360 {lab=vdd}
N -290 -240 -290 -210 {lab=vss}
N -250 -390 -250 -360 {lab=vddl}
N -250 -240 -250 -210 {lab=vssl}
N -380 -320 -350 -320 {lab=ena}
N -150 -320 -120 -320 {lab=vbnl}
N -150 -300 -120 -300 {lab=vcpla}
N -150 -280 -120 -280 {lab=vcplb}
N 110 -460 110 -430 {lab=vdd}
N 110 -270 110 -240 {lab=vss}
N 250 -390 280 -390 {lab=vm0}
N 250 -370 280 -370 {lab=out0}
N 20 -390 50 -390 {lab=vbnl}
N 20 -370 50 -370 {lab=d0}
N 20 -350 50 -350 {lab=d1}
N 20 -330 50 -330 {lab=d2}
N 20 -310 50 -310 {lab=d3}
N 110 -160 110 -130 {lab=vdd}
N 110 30 110 60 {lab=vss}
N 250 -90 280 -90 {lab=vm1}
N 250 -70 280 -70 {lab=out1}
N 20 -90 50 -90 {lab=vbnl}
N 20 -70 50 -70 {lab=d4}
N 20 -50 50 -50 {lab=d5}
N 20 -30 50 -30 {lab=d6}
N 20 -10 50 -10 {lab=d7}
N 110 140 110 170 {lab=vdd}
N 110 330 110 360 {lab=vss}
N 250 210 280 210 {lab=vm2}
N 250 230 280 230 {lab=out2}
N 20 210 50 210 {lab=vbnl}
N 20 230 50 230 {lab=d8}
N 20 250 50 250 {lab=d9}
N 20 270 50 270 {lab=d10}
N 20 290 50 290 {lab=d11}
N 110 440 110 470 {lab=vdd}
N 110 630 110 660 {lab=vss}
N 250 510 280 510 {lab=vm3}
N 250 530 280 530 {lab=out3}
N 20 510 50 510 {lab=vbnl}
N 20 530 50 530 {lab=d12}
N 20 550 50 550 {lab=d13}
N 20 570 50 570 {lab=d14}
N 20 590 50 590 {lab=d15}
N 610 -530 610 -500 {lab=vdd}
N 610 -400 610 -370 {lab=vss}
N 520 -460 550 -460 {lab=out0}
N 750 -460 780 -460 {lab=bus0}
N 610 -280 610 -250 {lab=vdd}
N 610 -150 610 -120 {lab=vss}
N 520 -210 550 -210 {lab=out1}
N 750 -210 780 -210 {lab=bus1}
N 1010 -530 1010 -500 {lab=vdd}
N 1010 -400 1010 -370 {lab=vss}
N 920 -460 950 -460 {lab=out0}
N 1150 -460 1180 -460 {lab=spk0}
N 1010 -280 1010 -250 {lab=vdd}
N 1010 -150 1010 -120 {lab=vss}
N 920 -210 950 -210 {lab=out1}
N 1150 -210 1180 -210 {lab=spk1}
N 610 -40 610 -10 {lab=vdd}
N 610 110 610 140 {lab=vss}
N 520 30 550 30 {lab=spk0}
N 750 30 780 30 {lab=vm1}
N 520 50 550 50 {lab=d16}
N 520 70 550 70 {lab=d17}
N 610 160 610 190 {lab=vdd}
N 610 310 610 340 {lab=vss}
N 520 230 550 230 {lab=spk1}
N 750 230 780 230 {lab=vm0}
N 520 250 550 250 {lab=d18}
N 520 270 550 270 {lab=d19}
N 610 520 610 550 {lab=vss}
N 520 420 550 420 {lab=vm0}
N 750 420 780 420 {lab=vm1}
N 520 440 550 440 {lab=vcpla}
N 520 460 550 460 {lab=d20}
N 520 480 550 480 {lab=d21}
N 610 720 610 750 {lab=vss}
N 520 620 550 620 {lab=bus2}
N 750 620 780 620 {lab=vm3}
N 520 640 550 640 {lab=vcplb}
N 520 660 550 660 {lab=d22}
N 520 680 550 680 {lab=d23}
N 1070 240 1070 270 {lab=bus2}
N 1000 300 1030 300 {lab=vcplb}
N 1070 330 1070 360 {lab=vm2}
N 1070 300 1100 300 {lab=vss}
N 1070 440 1070 470 {lab=bus3}
N 1000 500 1030 500 {lab=vcplb}
N 1070 530 1070 560 {lab=vm3}
N 1070 500 1100 500 {lab=vss}
N -600 -400 -560 -400 {lab=vdd}
N -600 -375 -560 -375 {lab=vss}
N -600 -350 -560 -350 {lab=vddl}
N -600 -325 -560 -325 {lab=vssl}
N -600 -300 -560 -300 {lab=ena}
N -600 -275 -560 -275 {lab=d0}
N -600 -250 -560 -250 {lab=d1}
N -600 -225 -560 -225 {lab=d2}
N -600 -200 -560 -200 {lab=d3}
N -600 -175 -560 -175 {lab=d4}
N -600 -150 -560 -150 {lab=d5}
N -600 -125 -560 -125 {lab=d6}
N -600 -100 -560 -100 {lab=d7}
N -600 -75 -560 -75 {lab=d8}
N -600 -50 -560 -50 {lab=d9}
N -600 -25 -560 -25 {lab=d10}
N -600 0 -560 0 {lab=d11}
N -600 25 -560 25 {lab=d12}
N -600 50 -560 50 {lab=d13}
N -600 75 -560 75 {lab=d14}
N -600 100 -560 100 {lab=d15}
N -600 125 -560 125 {lab=d16}
N -600 150 -560 150 {lab=d17}
N -600 175 -560 175 {lab=d18}
N -600 200 -560 200 {lab=d19}
N -600 225 -560 225 {lab=d20}
N -600 250 -560 250 {lab=d21}
N -600 275 -560 275 {lab=d22}
N -600 300 -560 300 {lab=d23}
N -600 325 -560 325 {lab=bus0}
N -600 350 -560 350 {lab=bus1}
N -600 375 -560 375 {lab=bus2}
N -600 400 -560 400 {lab=bus3}
N -600 425 -560 425 {lab=vcpla}
N -600 450 -560 450 {lab=vcplb}
C {bbl_bias.sym} -250 -300 0 0 {name=XB}
C {lab_pin.sym} -290 -390 0 1 {name=l1 sig_type=std_logic lab=vdd}
C {lab_pin.sym} -290 -210 0 1 {name=l2 sig_type=std_logic lab=vss}
C {lab_pin.sym} -250 -390 0 1 {name=l3 sig_type=std_logic lab=vddl}
C {lab_pin.sym} -250 -210 0 1 {name=l4 sig_type=std_logic lab=vssl}
C {lab_pin.sym} -380 -320 0 0 {name=l5 sig_type=std_logic lab=ena}
C {lab_pin.sym} -120 -320 0 1 {name=l6 sig_type=std_logic lab=vbnl}
C {lab_pin.sym} -120 -300 0 1 {name=l7 sig_type=std_logic lab=vcpla}
C {lab_pin.sym} -120 -280 0 1 {name=l8 sig_type=std_logic lab=vcplb}
C {bbl_unit.sym} 150 -350 0 0 {name=XU0}
C {lab_pin.sym} 110 -460 0 1 {name=l10 sig_type=std_logic lab=vdd}
C {lab_pin.sym} 110 -240 0 1 {name=l11 sig_type=std_logic lab=vss}
C {lab_pin.sym} 280 -390 0 1 {name=l12 sig_type=std_logic lab=vm0}
C {lab_pin.sym} 280 -370 0 1 {name=l13 sig_type=std_logic lab=out0}
C {lab_pin.sym} 20 -390 0 0 {name=l14 sig_type=std_logic lab=vbnl}
C {lab_pin.sym} 20 -370 0 0 {name=l15 sig_type=std_logic lab=d0}
C {lab_pin.sym} 20 -350 0 0 {name=l16 sig_type=std_logic lab=d1}
C {lab_pin.sym} 20 -330 0 0 {name=l17 sig_type=std_logic lab=d2}
C {lab_pin.sym} 20 -310 0 0 {name=l18 sig_type=std_logic lab=d3}
C {bbl_unit.sym} 150 -50 0 0 {name=XU1}
C {lab_pin.sym} 110 -160 0 1 {name=l20 sig_type=std_logic lab=vdd}
C {lab_pin.sym} 110 60 0 1 {name=l21 sig_type=std_logic lab=vss}
C {lab_pin.sym} 280 -90 0 1 {name=l22 sig_type=std_logic lab=vm1}
C {lab_pin.sym} 280 -70 0 1 {name=l23 sig_type=std_logic lab=out1}
C {lab_pin.sym} 20 -90 0 0 {name=l24 sig_type=std_logic lab=vbnl}
C {lab_pin.sym} 20 -70 0 0 {name=l25 sig_type=std_logic lab=d4}
C {lab_pin.sym} 20 -50 0 0 {name=l26 sig_type=std_logic lab=d5}
C {lab_pin.sym} 20 -30 0 0 {name=l27 sig_type=std_logic lab=d6}
C {lab_pin.sym} 20 -10 0 0 {name=l28 sig_type=std_logic lab=d7}
C {bbl_unit.sym} 150 250 0 0 {name=XU2}
C {lab_pin.sym} 110 140 0 1 {name=l30 sig_type=std_logic lab=vdd}
C {lab_pin.sym} 110 360 0 1 {name=l31 sig_type=std_logic lab=vss}
C {lab_pin.sym} 280 210 0 1 {name=l32 sig_type=std_logic lab=vm2}
C {lab_pin.sym} 280 230 0 1 {name=l33 sig_type=std_logic lab=out2}
C {lab_pin.sym} 20 210 0 0 {name=l34 sig_type=std_logic lab=vbnl}
C {lab_pin.sym} 20 230 0 0 {name=l35 sig_type=std_logic lab=d8}
C {lab_pin.sym} 20 250 0 0 {name=l36 sig_type=std_logic lab=d9}
C {lab_pin.sym} 20 270 0 0 {name=l37 sig_type=std_logic lab=d10}
C {lab_pin.sym} 20 290 0 0 {name=l38 sig_type=std_logic lab=d11}
C {bbl_unit.sym} 150 550 0 0 {name=XU3}
C {lab_pin.sym} 110 440 0 1 {name=l40 sig_type=std_logic lab=vdd}
C {lab_pin.sym} 110 660 0 1 {name=l41 sig_type=std_logic lab=vss}
C {lab_pin.sym} 280 510 0 1 {name=l42 sig_type=std_logic lab=vm3}
C {lab_pin.sym} 280 530 0 1 {name=l43 sig_type=std_logic lab=out3}
C {lab_pin.sym} 20 510 0 0 {name=l44 sig_type=std_logic lab=vbnl}
C {lab_pin.sym} 20 530 0 0 {name=l45 sig_type=std_logic lab=d12}
C {lab_pin.sym} 20 550 0 0 {name=l46 sig_type=std_logic lab=d13}
C {lab_pin.sym} 20 570 0 0 {name=l47 sig_type=std_logic lab=d14}
C {lab_pin.sym} 20 590 0 0 {name=l48 sig_type=std_logic lab=d15}
C {bbl_inv.sym} 650 -450 0 0 {name=XL0}
C {lab_pin.sym} 610 -530 0 1 {name=l50 sig_type=std_logic lab=vdd}
C {lab_pin.sym} 610 -370 0 1 {name=l51 sig_type=std_logic lab=vss}
C {lab_pin.sym} 520 -460 0 0 {name=l52 sig_type=std_logic lab=out0}
C {lab_pin.sym} 780 -460 0 1 {name=l53 sig_type=std_logic lab=bus0}
C {bbl_inv.sym} 650 -200 0 0 {name=XL1}
C {lab_pin.sym} 610 -280 0 1 {name=l55 sig_type=std_logic lab=vdd}
C {lab_pin.sym} 610 -120 0 1 {name=l56 sig_type=std_logic lab=vss}
C {lab_pin.sym} 520 -210 0 0 {name=l57 sig_type=std_logic lab=out1}
C {lab_pin.sym} 780 -210 0 1 {name=l58 sig_type=std_logic lab=bus1}
C {bbl_inv.sym} 1050 -450 0 0 {name=XI0}
C {lab_pin.sym} 1010 -530 0 1 {name=l60 sig_type=std_logic lab=vdd}
C {lab_pin.sym} 1010 -370 0 1 {name=l61 sig_type=std_logic lab=vss}
C {lab_pin.sym} 920 -460 0 0 {name=l62 sig_type=std_logic lab=out0}
C {lab_pin.sym} 1180 -460 0 1 {name=l63 sig_type=std_logic lab=spk0}
C {bbl_inv.sym} 1050 -200 0 0 {name=XI1}
C {lab_pin.sym} 1010 -280 0 1 {name=l65 sig_type=std_logic lab=vdd}
C {lab_pin.sym} 1010 -120 0 1 {name=l66 sig_type=std_logic lab=vss}
C {lab_pin.sym} 920 -210 0 0 {name=l67 sig_type=std_logic lab=out1}
C {lab_pin.sym} 1180 -210 0 1 {name=l68 sig_type=std_logic lab=spk1}
C {bbl_syn.sym} 650 50 0 0 {name=XS01}
C {lab_pin.sym} 610 -40 0 1 {name=l70 sig_type=std_logic lab=vdd}
C {lab_pin.sym} 610 140 0 1 {name=l71 sig_type=std_logic lab=vss}
C {lab_pin.sym} 520 30 0 0 {name=l72 sig_type=std_logic lab=spk0}
C {lab_pin.sym} 780 30 0 1 {name=l73 sig_type=std_logic lab=vm1}
C {lab_pin.sym} 520 50 0 0 {name=l74 sig_type=std_logic lab=d16}
C {lab_pin.sym} 520 70 0 0 {name=l75 sig_type=std_logic lab=d17}
C {bbl_syn.sym} 650 250 0 0 {name=XS10}
C {lab_pin.sym} 610 160 0 1 {name=l77 sig_type=std_logic lab=vdd}
C {lab_pin.sym} 610 340 0 1 {name=l78 sig_type=std_logic lab=vss}
C {lab_pin.sym} 520 230 0 0 {name=l79 sig_type=std_logic lab=spk1}
C {lab_pin.sym} 780 230 0 1 {name=l80 sig_type=std_logic lab=vm0}
C {lab_pin.sym} 520 250 0 0 {name=l81 sig_type=std_logic lab=d18}
C {lab_pin.sym} 520 270 0 0 {name=l82 sig_type=std_logic lab=d19}
C {bbl_gap.sym} 650 450 0 0 {name=XG01}
C {lab_pin.sym} 610 550 0 1 {name=l84 sig_type=std_logic lab=vss}
C {lab_pin.sym} 520 420 0 0 {name=l85 sig_type=std_logic lab=vm0}
C {lab_pin.sym} 780 420 0 1 {name=l86 sig_type=std_logic lab=vm1}
C {lab_pin.sym} 520 440 0 0 {name=l87 sig_type=std_logic lab=vcpla}
C {lab_pin.sym} 520 460 0 0 {name=l88 sig_type=std_logic lab=d20}
C {lab_pin.sym} 520 480 0 0 {name=l89 sig_type=std_logic lab=d21}
C {bbl_gap.sym} 650 650 0 0 {name=XG32}
C {lab_pin.sym} 610 750 0 1 {name=l91 sig_type=std_logic lab=vss}
C {lab_pin.sym} 520 620 0 0 {name=l92 sig_type=std_logic lab=bus2}
C {lab_pin.sym} 780 620 0 1 {name=l93 sig_type=std_logic lab=vm3}
C {lab_pin.sym} 520 640 0 0 {name=l94 sig_type=std_logic lab=vcplb}
C {lab_pin.sym} 520 660 0 0 {name=l95 sig_type=std_logic lab=d22}
C {lab_pin.sym} 520 680 0 0 {name=l96 sig_type=std_logic lab=d23}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1050 300 0 0 {name=MP2 l=0.45u w=1u ng=1 m=1 mm_ok=1 model=sg13_hv_nmos spiceprefix=X}
C {lab_pin.sym} 1070 240 0 1 {name=l98 sig_type=std_logic lab=bus2}
C {lab_pin.sym} 1000 300 0 0 {name=l99 sig_type=std_logic lab=vcplb}
C {lab_pin.sym} 1070 360 0 1 {name=l100 sig_type=std_logic lab=vm2}
C {lab_pin.sym} 1100 300 0 1 {name=l101 sig_type=std_logic lab=vss}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1050 500 0 0 {name=MP3 l=0.45u w=1u ng=1 m=1 mm_ok=1 model=sg13_hv_nmos spiceprefix=X}
C {lab_pin.sym} 1070 440 0 1 {name=l103 sig_type=std_logic lab=bus3}
C {lab_pin.sym} 1000 500 0 0 {name=l104 sig_type=std_logic lab=vcplb}
C {lab_pin.sym} 1070 560 0 1 {name=l105 sig_type=std_logic lab=vm3}
C {lab_pin.sym} 1100 500 0 1 {name=l106 sig_type=std_logic lab=vss}
C {iopin.sym} -600 -400 0 0 {name=p107 lab=vdd}
C {lab_pin.sym} -560 -400 0 1 {name=l108 sig_type=std_logic lab=vdd}
C {iopin.sym} -600 -375 0 0 {name=p109 lab=vss}
C {lab_pin.sym} -560 -375 0 1 {name=l110 sig_type=std_logic lab=vss}
C {iopin.sym} -600 -350 0 0 {name=p111 lab=vddl}
C {lab_pin.sym} -560 -350 0 1 {name=l112 sig_type=std_logic lab=vddl}
C {iopin.sym} -600 -325 0 0 {name=p113 lab=vssl}
C {lab_pin.sym} -560 -325 0 1 {name=l114 sig_type=std_logic lab=vssl}
C {iopin.sym} -600 -300 0 0 {name=p115 lab=ena}
C {lab_pin.sym} -560 -300 0 1 {name=l116 sig_type=std_logic lab=ena}
C {iopin.sym} -600 -275 0 0 {name=p117 lab=d0}
C {lab_pin.sym} -560 -275 0 1 {name=l118 sig_type=std_logic lab=d0}
C {iopin.sym} -600 -250 0 0 {name=p119 lab=d1}
C {lab_pin.sym} -560 -250 0 1 {name=l120 sig_type=std_logic lab=d1}
C {iopin.sym} -600 -225 0 0 {name=p121 lab=d2}
C {lab_pin.sym} -560 -225 0 1 {name=l122 sig_type=std_logic lab=d2}
C {iopin.sym} -600 -200 0 0 {name=p123 lab=d3}
C {lab_pin.sym} -560 -200 0 1 {name=l124 sig_type=std_logic lab=d3}
C {iopin.sym} -600 -175 0 0 {name=p125 lab=d4}
C {lab_pin.sym} -560 -175 0 1 {name=l126 sig_type=std_logic lab=d4}
C {iopin.sym} -600 -150 0 0 {name=p127 lab=d5}
C {lab_pin.sym} -560 -150 0 1 {name=l128 sig_type=std_logic lab=d5}
C {iopin.sym} -600 -125 0 0 {name=p129 lab=d6}
C {lab_pin.sym} -560 -125 0 1 {name=l130 sig_type=std_logic lab=d6}
C {iopin.sym} -600 -100 0 0 {name=p131 lab=d7}
C {lab_pin.sym} -560 -100 0 1 {name=l132 sig_type=std_logic lab=d7}
C {iopin.sym} -600 -75 0 0 {name=p133 lab=d8}
C {lab_pin.sym} -560 -75 0 1 {name=l134 sig_type=std_logic lab=d8}
C {iopin.sym} -600 -50 0 0 {name=p135 lab=d9}
C {lab_pin.sym} -560 -50 0 1 {name=l136 sig_type=std_logic lab=d9}
C {iopin.sym} -600 -25 0 0 {name=p137 lab=d10}
C {lab_pin.sym} -560 -25 0 1 {name=l138 sig_type=std_logic lab=d10}
C {iopin.sym} -600 0 0 0 {name=p139 lab=d11}
C {lab_pin.sym} -560 0 0 1 {name=l140 sig_type=std_logic lab=d11}
C {iopin.sym} -600 25 0 0 {name=p141 lab=d12}
C {lab_pin.sym} -560 25 0 1 {name=l142 sig_type=std_logic lab=d12}
C {iopin.sym} -600 50 0 0 {name=p143 lab=d13}
C {lab_pin.sym} -560 50 0 1 {name=l144 sig_type=std_logic lab=d13}
C {iopin.sym} -600 75 0 0 {name=p145 lab=d14}
C {lab_pin.sym} -560 75 0 1 {name=l146 sig_type=std_logic lab=d14}
C {iopin.sym} -600 100 0 0 {name=p147 lab=d15}
C {lab_pin.sym} -560 100 0 1 {name=l148 sig_type=std_logic lab=d15}
C {iopin.sym} -600 125 0 0 {name=p149 lab=d16}
C {lab_pin.sym} -560 125 0 1 {name=l150 sig_type=std_logic lab=d16}
C {iopin.sym} -600 150 0 0 {name=p151 lab=d17}
C {lab_pin.sym} -560 150 0 1 {name=l152 sig_type=std_logic lab=d17}
C {iopin.sym} -600 175 0 0 {name=p153 lab=d18}
C {lab_pin.sym} -560 175 0 1 {name=l154 sig_type=std_logic lab=d18}
C {iopin.sym} -600 200 0 0 {name=p155 lab=d19}
C {lab_pin.sym} -560 200 0 1 {name=l156 sig_type=std_logic lab=d19}
C {iopin.sym} -600 225 0 0 {name=p157 lab=d20}
C {lab_pin.sym} -560 225 0 1 {name=l158 sig_type=std_logic lab=d20}
C {iopin.sym} -600 250 0 0 {name=p159 lab=d21}
C {lab_pin.sym} -560 250 0 1 {name=l160 sig_type=std_logic lab=d21}
C {iopin.sym} -600 275 0 0 {name=p161 lab=d22}
C {lab_pin.sym} -560 275 0 1 {name=l162 sig_type=std_logic lab=d22}
C {iopin.sym} -600 300 0 0 {name=p163 lab=d23}
C {lab_pin.sym} -560 300 0 1 {name=l164 sig_type=std_logic lab=d23}
C {iopin.sym} -600 325 0 0 {name=p165 lab=bus0}
C {lab_pin.sym} -560 325 0 1 {name=l166 sig_type=std_logic lab=bus0}
C {iopin.sym} -600 350 0 0 {name=p167 lab=bus1}
C {lab_pin.sym} -560 350 0 1 {name=l168 sig_type=std_logic lab=bus1}
C {iopin.sym} -600 375 0 0 {name=p169 lab=bus2}
C {lab_pin.sym} -560 375 0 1 {name=l170 sig_type=std_logic lab=bus2}
C {iopin.sym} -600 400 0 0 {name=p171 lab=bus3}
C {lab_pin.sym} -560 400 0 1 {name=l172 sig_type=std_logic lab=bus3}
C {iopin.sym} -600 425 0 0 {name=p173 lab=vcpla}
C {lab_pin.sym} -560 425 0 1 {name=l174 sig_type=std_logic lab=vcpla}
C {iopin.sym} -600 450 0 0 {name=p175 lab=vcplb}
C {lab_pin.sym} -560 450 0 1 {name=l176 sig_type=std_logic lab=vcplb}

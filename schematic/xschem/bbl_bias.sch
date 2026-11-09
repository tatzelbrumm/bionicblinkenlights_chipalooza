v {xschem version=3.4.5 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {bbl_bias: self-biased subthreshold beta multiplier (K = 8, rhigh), enable, pull-ups} -120 -570 0 0 0.6 0.6 {}
T {about 45 nA per branch; start-up by the Vgs = 0 leakage of XMSU} -120 -500 0 0 0.3 0.3 {}
T {vbnl: about 2.5 nA reference of the tuning DACs; vcpla / vcplb pulled up by about 1 nA} -120 -470 0 0 0.3 0.3 {}
N -120 -380 1220 -380 {lab=vdd}
N -120 510 1220 510 {lab=vss}
N 340 250 340 320 {lab=sa}
N 480 250 480 320 {lab=rs}
N 480 320 460 320 {lab=rs}
N 140 -220 170 -220 {lab=vddl}
N 280 -220 300 -220 {lab=vdd}
N 300 -220 300 -380 {lab=vdd}
N 280 -250 280 -380 {lab=vdd}
N 420 -220 440 -220 {lab=vdd}
N 440 -220 440 -380 {lab=vdd}
N 420 -250 420 -380 {lab=vdd}
N 560 -220 580 -220 {lab=vdd}
N 580 -220 580 -380 {lab=vdd}
N 560 -250 560 -380 {lab=vdd}
N 700 -220 720 -220 {lab=vdd}
N 720 -220 720 -380 {lab=vdd}
N 700 -250 700 -380 {lab=vdd}
N 840 -220 860 -220 {lab=vdd}
N 860 -220 860 -380 {lab=vdd}
N 840 -250 840 -380 {lab=vdd}
N 980 -220 1000 -220 {lab=vdd}
N 1000 -220 1000 -380 {lab=vdd}
N 980 -250 980 -380 {lab=vdd}
N 200 220 220 220 {lab=vss}
N 220 220 220 510 {lab=vss}
N 340 220 360 220 {lab=vss}
N 360 220 360 510 {lab=vss}
N 480 220 500 220 {lab=vss}
N 500 220 500 510 {lab=vss}
N 620 220 640 220 {lab=vss}
N 640 220 640 510 {lab=vss}
N 620 250 650 250 {lab=vss}
N 650 250 650 510 {lab=vss}
N 760 220 780 220 {lab=vss}
N 780 220 780 510 {lab=vss}
N 760 250 790 250 {lab=vss}
N 790 250 790 510 {lab=vss}
N 900 220 920 220 {lab=vss}
N 920 220 920 510 {lab=vss}
N 900 190 930 190 {lab=vss}
N 930 190 930 510 {lab=vss}
N 900 250 930 250 {lab=vss}
N 930 250 930 510 {lab=vss}
N 1040 220 1060 220 {lab=vss}
N 1060 220 1060 510 {lab=vss}
N 1040 190 1070 190 {lab=vss}
N 1070 190 1070 510 {lab=vss}
N 1040 250 1070 250 {lab=vss}
N 1070 250 1070 510 {lab=vss}
N 340 350 360 350 {lab=vss}
N 360 350 360 510 {lab=vss}
N 340 380 340 510 {lab=vss}
N 620 350 640 350 {lab=vss}
N 640 350 640 510 {lab=vss}
N 620 380 620 510 {lab=vss}
N 100 -220 100 20 {lab=ena}
N 140 -190 140 -40 {lab=enab}
N 240 -220 240 -140 {lab=vbp}
N 280 -190 280 40 {lab=vbn}
N 380 -220 380 -140 {lab=vbp}
N 420 -190 420 -140 {lab=vbp}
N 520 -220 520 -100 {lab=vdd}
N 560 -190 560 40 {lab=vbn}
N 660 -220 660 -140 {lab=vbp}
N 700 -190 700 -20 {lab=vbnl}
N 800 -220 800 -140 {lab=vbp}
N 840 -190 840 -80 {lab=vcpla}
N 940 -220 940 -140 {lab=vbp}
N 980 -190 980 -60 {lab=vcplb}
N 160 220 160 20 {lab=ena}
N 200 190 200 -40 {lab=enab}
N 300 220 300 40 {lab=vbn}
N 340 190 340 40 {lab=vbn}
N 440 220 440 40 {lab=vbn}
N 480 190 480 -140 {lab=vbp}
N 580 220 580 -40 {lab=enab}
N 620 190 620 40 {lab=vbn}
N 720 220 720 -20 {lab=vbnl}
N 760 190 760 -20 {lab=vbnl}
N 860 220 860 -80 {lab=vcpla}
N 1000 220 1000 -60 {lab=vcplb}
N 140 -250 170 -250 {lab=vddl}
N 170 -250 170 -120 {lab=vddl}
N 200 250 230 250 {lab=vssl}
N 230 250 230 0 {lab=vssl}
N 300 350 310 350 {lab=ena}
N 310 350 310 20 {lab=ena}
N 460 380 510 380 {lab=sb}
N 510 380 510 60 {lab=sb}
N 580 350 590 350 {lab=ena}
N 590 350 590 20 {lab=ena}
N 620 320 660 320 {lab=sb}
N 660 320 660 60 {lab=sb}
N 240 -140 940 -140 {lab=vbp}
N -120 -120 170 -120 {lab=vddl}
N 520 -100 1180 -100 {lab=vdd}
N 1180 -100 1180 -380 {lab=vdd}
N -120 -80 860 -80 {lab=vcpla}
N -120 -60 1000 -60 {lab=vcplb}
N 140 -40 580 -40 {lab=enab}
N -120 -20 760 -20 {lab=vbnl}
N -120 0 230 0 {lab=vssl}
N -120 20 590 20 {lab=ena}
N 280 40 620 40 {lab=vbn}
N 510 60 660 60 {lab=sb}
C {lab_pin.sym} 340 320 0 1 {name=l0 sig_type=std_logic lab=sa}
C {lab_pin.sym} 480 320 0 1 {name=l1 sig_type=std_logic lab=rs}
C {sg13cmos5l_pr/sg13_lv_pmos.sym} 120 -220 0 0 {name=MIP l=0.5u w=0.3u ng=1 m=1 mm_ok=1 model=sg13_lv_pmos spiceprefix=X}
C {lab_pin.sym} 170 -220 0 1 {name=l3 sig_type=std_logic lab=vddl}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 260 -220 0 0 {name=MPA l=2u w=2u ng=1 m=1 mm_ok=1 model=sg13_hv_pmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 400 -220 0 0 {name=MPB l=2u w=2u ng=1 m=1 mm_ok=1 model=sg13_hv_pmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 540 -220 0 0 {name=MSU l=0.45u w=4u ng=1 m=1 mm_ok=1 model=sg13_hv_pmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 680 -220 0 0 {name=MLP l=8u w=0.3u ng=1 m=1 mm_ok=1 model=sg13_hv_pmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 820 -220 0 0 {name=MCA l=22u w=0.3u ng=1 m=1 mm_ok=1 model=sg13_hv_pmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 960 -220 0 0 {name=MCB l=22u w=0.3u ng=1 m=1 mm_ok=1 model=sg13_hv_pmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_lv_nmos.sym} 180 220 0 0 {name=MIN l=0.5u w=0.3u ng=1 m=1 mm_ok=1 model=sg13_lv_nmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 320 220 0 0 {name=MNA l=2u w=2u ng=1 m=1 mm_ok=1 model=sg13_hv_nmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 460 220 0 0 {name=MNB l=2u w=16u ng=8 m=1 mm_ok=1 model=sg13_hv_nmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 600 220 0 0 {name=MCL l=0.45u w=1u ng=1 m=1 mm_ok=1 model=sg13_hv_nmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 740 220 0 0 {name=MLD l=2u w=2u ng=1 m=1 mm_ok=1 model=sg13_hv_nmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 880 220 0 0 {name=CA l=10u w=50u ng=5 m=1 mm_ok=1 model=sg13_hv_nmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1020 220 0 0 {name=CB l=10u w=50u ng=5 m=1 mm_ok=1 model=sg13_hv_nmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 320 350 0 0 {name=MEA l=0.45u w=1u ng=1 m=1 mm_ok=1 model=sg13_hv_nmos spiceprefix=X}
C {sg13cmos5l_pr/rhigh.sym} 460 350 0 0 {name=R1 w=0.5e-6 l=41.055e-6 model=rhigh body=vss spiceprefix=X b=9 m=1 mm_ok=1}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 600 350 0 0 {name=MEB l=0.45u w=1u ng=1 m=1 mm_ok=1 model=sg13_hv_nmos spiceprefix=X}
C {lab_pin.sym} 240 -140 0 0 {name=l20 sig_type=std_logic lab=vbp}
C {lab_pin.sym} 140 -40 0 0 {name=l21 sig_type=std_logic lab=enab}
C {lab_pin.sym} 280 40 0 0 {name=l22 sig_type=std_logic lab=vbn}
C {lab_pin.sym} 510 60 0 0 {name=l23 sig_type=std_logic lab=sb}
C {iopin.sym} -120 -380 0 0 {name=p24 lab=vdd}
C {iopin.sym} -120 510 0 0 {name=p25 lab=vss}
C {iopin.sym} -120 -120 0 0 {name=p26 lab=vddl}
C {iopin.sym} -120 0 0 0 {name=p27 lab=vssl}
C {iopin.sym} -120 20 0 0 {name=p28 lab=ena}
C {iopin.sym} -120 -20 0 0 {name=p29 lab=vbnl}
C {iopin.sym} -120 -80 0 0 {name=p30 lab=vcpla}
C {iopin.sym} -120 -60 0 0 {name=p31 lab=vcplb}

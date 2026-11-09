v {xschem version=3.4.5 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {bbl_bias: self-biased subthreshold beta multiplier (K = 8, rhigh), enable, pull-ups} 0 -680 0 0 0.6 0.6 {}
T {about 45 nA per branch; start-up by the Vgs = 0 leakage of XMSU} 0 -620 0 0 0.3 0.3 {}
T {vbnl: about 2.5 nA reference of the tuning DACs; vcpla / vcplb pulled up by about 1 nA} 0 -590 0 0 0.3 0.3 {}
T {LV inverter (vddl / vssl)} 60 -530 0 0 0.35 0.35 {layer=8}
T {start-up, clamp} 340 -530 0 0 0.35 0.35 {layer=8}
T {beta multiplier} 580 -530 0 0 0.35 0.35 {layer=8}
T {vbnl, vcpla, vcplb} 1140 -530 0 0 0.35 0.35 {layer=8}
N 0 -290 200 -290 {lab=vddl}
N 200 -260 200 -290 {lab=vddl}
N 0 -30 200 -30 {lab=vssl}
N 200 -60 300 -60 {lab=vss}
N 300 -60 300 200 {lab=vss}
N 160 -260 160 -60 {lab=ena}
N 0 -160 160 -160 {lab=ena}
N 200 -230 200 -90 {lab=enab}
N 360 -380 340 -380 {lab=vdd}
N 340 -380 340 -480 {lab=vdd}
N 400 -380 400 -480 {lab=vdd}
N 400 -350 400 -190 {lab=vbn}
N 400 -160 400 200 {lab=vss}
N 200 -160 360 -160 {lab=enab}
N 400 -300 640 -300 {lab=vbn}
N 640 -380 640 -480 {lab=vdd}
N 880 -380 880 -480 {lab=vdd}
N 680 -380 840 -380 {lab=vbp}
N 820 -380 820 -320 {lab=vbp}
N 820 -320 880 -320 {lab=vbp}
N 680 -160 840 -160 {lab=vbn}
N 700 -160 700 -230 {lab=vbn}
N 700 -230 640 -230 {lab=vbn}
N 640 -350 640 -190 {lab=vbn}
N 880 -350 880 -190 {lab=vbp}
N 640 -160 540 -160 {lab=vss}
N 540 -160 540 200 {lab=vss}
N 880 -160 1060 -160 {lab=vss}
N 1060 -160 1060 200 {lab=vss}
N 640 -130 640 50 {lab=sa}
N 880 -130 880 -70 {lab=rs}
N 880 -10 880 50 {lab=sb}
N 640 80 640 200 {lab=vss}
N 880 80 880 200 {lab=vss}
N 680 80 840 80 {lab=ena}
N 760 80 760 130 {lab=ena}
N 1200 -380 1200 -480 {lab=vdd}
N 1420 -380 1420 -480 {lab=vdd}
N 1640 -380 1640 -480 {lab=vdd}
N 880 -280 1600 -280 {lab=vbp}
N 1160 -280 1160 -380 {lab=vbp}
N 1380 -280 1380 -380 {lab=vbp}
N 1600 -280 1600 -380 {lab=vbp}
N 1200 -350 1200 -50 {lab=vbnl}
N 1240 -20 1240 -80 {lab=vbnl}
N 1240 -80 1200 -80 {lab=vbnl}
N 1200 -20 1200 200 {lab=vss}
N 1420 -350 1420 -100 {lab=vcpla}
N 1460 -130 1460 200 {lab=vss}
N 1640 -350 1640 -220 {lab=vcplb}
N 1680 -250 1680 200 {lab=vss}
N 1240 -20 1840 -20 {lab=vbnl}
N 1420 -160 1840 -160 {lab=vcpla}
N 1640 -270 1840 -270 {lab=vcplb}
N 0 -480 1640 -480 {lab=vdd}
N 0 200 1680 200 {lab=vss}
C {sg13cmos5l_pr/sg13_lv_pmos.sym} 180 -260 0 0 {name=MIP l=0.5u w=0.3u ng=1 m=1 mm_ok=1 model=sg13_lv_pmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_lv_nmos.sym} 180 -60 0 0 {name=MIN l=0.5u w=0.3u ng=1 m=1 mm_ok=1 model=sg13_lv_nmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 380 -380 0 0 {name=MSU l=0.45u w=4u ng=1 m=1 mm_ok=1 model=sg13_hv_pmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 380 -160 0 0 {name=MCL l=0.45u w=1u ng=1 m=1 mm_ok=1 model=sg13_hv_nmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 660 -380 0 1 {name=MPA l=2u w=2u ng=1 m=1 mm_ok=1 model=sg13_hv_pmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 860 -380 0 0 {name=MPB l=2u w=2u ng=1 m=1 mm_ok=1 model=sg13_hv_pmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 660 -160 0 1 {name=MNA l=2u w=2u ng=1 m=1 mm_ok=1 model=sg13_hv_nmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 860 -160 0 0 {name=MNB l=2u w=16u ng=8 m=1 mm_ok=1 model=sg13_hv_nmos spiceprefix=X}
C {sg13cmos5l_pr/rhigh.sym} 880 -40 0 0 {name=R1 w=0.5e-6 l=41.055e-6 model=rhigh body=vss spiceprefix=X b=9 m=1 mm_ok=1}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 660 80 0 1 {name=MEA l=0.45u w=1u ng=1 m=1 mm_ok=1 model=sg13_hv_nmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 860 80 0 0 {name=MEB l=0.45u w=1u ng=1 m=1 mm_ok=1 model=sg13_hv_nmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1180 -380 0 0 {name=MLP l=7u w=0.3u ng=1 m=1 mm_ok=1 model=sg13_hv_pmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1220 -20 0 1 {name=MLD l=2u w=2u ng=1 m=1 mm_ok=1 model=sg13_hv_nmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1400 -380 0 0 {name=MCA l=22u w=0.3u ng=1 m=1 mm_ok=1 model=sg13_hv_pmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1440 -100 0 0 {name=CA l=10u w=50u ng=5 m=1 mm_ok=1 model=sg13_hv_nmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1620 -380 0 0 {name=MCB l=22u w=0.3u ng=1 m=1 mm_ok=1 model=sg13_hv_pmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1660 -220 0 0 {name=CB l=10u w=50u ng=5 m=1 mm_ok=1 model=sg13_hv_nmos spiceprefix=X}
C {lab_pin.sym} 760 130 0 1 {name=l1 sig_type=std_logic lab=ena}
C {lab_wire.sym} 240 -160 0 1 {name=l2 sig_type=std_logic lab=enab}
C {lab_wire.sym} 460 -300 0 1 {name=l3 sig_type=std_logic lab=vbn}
C {lab_wire.sym} 960 -280 0 1 {name=l4 sig_type=std_logic lab=vbp}
C {lab_wire.sym} 640 -20 0 0 {name=l5 sig_type=std_logic lab=sa}
C {lab_wire.sym} 880 -100 0 0 {name=l6 sig_type=std_logic lab=rs}
C {lab_wire.sym} 880 20 0 0 {name=l7 sig_type=std_logic lab=sb}
C {iopin.sym} 0 -480 0 1 {name=p24 lab=vdd}
C {iopin.sym} 0 200 0 1 {name=p25 lab=vss}
C {iopin.sym} 0 -290 0 1 {name=p26 lab=vddl}
C {iopin.sym} 0 -30 0 1 {name=p27 lab=vssl}
C {iopin.sym} 0 -160 0 1 {name=p28 lab=ena}
C {iopin.sym} 1840 -20 0 0 {name=p29 lab=vbnl}
C {iopin.sym} 1840 -160 0 0 {name=p30 lab=vcpla}
C {iopin.sym} 1840 -270 0 0 {name=p31 lab=vcplb}

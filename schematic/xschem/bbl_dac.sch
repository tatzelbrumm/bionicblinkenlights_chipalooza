v {xschem version=3.4.5 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {1 unit} 631 106 0 0 0.3 0.3 {layer=8}
T {2 units} 871 106 0 0 0.3 0.3 {layer=8}
T {4 units} 1111 106 0 0 0.3 0.3 {layer=8}
T {8 units} 1351 106 0 0 0.3 0.3 {layer=8}
T {base leg} 371 -14 0 0 0.3 0.3 {layer=8}
T {(always on)} 371 6 0 0 0.3 0.3 {layer=8}
T {bbl_dac: tuning DAC, diode XMD carries (base + code) x unit, code = b3..b0} 0 -590 0 0 0.6 0.6 {}
T {b0..b3 are 1.2 V logic (dig_in) on the switches XMS0..XMS3; the base leg XMH is always on, so code 0 still blinks} 0 -520 0 0 0.3 0.3 {}
N 200 -300 200 -400 {lab=vdd}
N 200 -270 200 -200 {lab=vin}
N 160 -300 160 -200 {lab=vin}
N 160 -200 1480 -200 {lab=vin}
N 360 -90 360 -200 {lab=vin}
N 360 -60 360 200 {lab=vss}
N 0 -140 1280 -140 {lab=vbnl}
N 320 -140 320 -60 {lab=vbnl}
N 600 -90 600 -200 {lab=vin}
N 560 -140 560 -60 {lab=vbnl}
N 600 -30 600 30 {lab=s0}
N 600 -60 700 -60 {lab=vss}
N 700 -60 700 200 {lab=vss}
N 600 60 600 200 {lab=vss}
N 530 60 560 60 {lab=b0}
N 840 -90 840 -200 {lab=vin}
N 800 -140 800 -60 {lab=vbnl}
N 840 -30 840 30 {lab=s1}
N 840 -60 940 -60 {lab=vss}
N 940 -60 940 200 {lab=vss}
N 840 60 840 200 {lab=vss}
N 770 60 800 60 {lab=b1}
N 1080 -90 1080 -200 {lab=vin}
N 1040 -140 1040 -60 {lab=vbnl}
N 1080 -30 1080 30 {lab=s2}
N 1080 -60 1180 -60 {lab=vss}
N 1180 -60 1180 200 {lab=vss}
N 1080 60 1080 200 {lab=vss}
N 1010 60 1040 60 {lab=b2}
N 1320 -90 1320 -200 {lab=vin}
N 1280 -140 1280 -60 {lab=vbnl}
N 1320 -30 1320 30 {lab=s3}
N 1320 -60 1420 -60 {lab=vss}
N 1420 -60 1420 200 {lab=vss}
N 1320 60 1320 200 {lab=vss}
N 1250 60 1280 60 {lab=b3}
N 0 -400 200 -400 {lab=vdd}
N 0 200 1420 200 {lab=vss}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 180 -300 0 0 {name=MD l=3u w=3u ng=1 m=1 mm_ok=1 model=sg13_hv_pmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 340 -60 0 0 {name=MH l=3.2u w=0.3u ng=1 m=1 mm_ok=1 model=sg13_hv_nmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 580 -60 0 0 {name=MU0 l=2u w=0.3u ng=1 m=1 mm_ok=1 model=sg13_hv_nmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 580 60 0 0 {name=MS0 l=0.45u w=0.3u ng=1 m=1 mm_ok=1 model=sg13_hv_nmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 820 -60 0 0 {name=MU1 l=2u w=0.6u ng=2 m=1 mm_ok=1 model=sg13_hv_nmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 820 60 0 0 {name=MS1 l=0.45u w=0.6u ng=2 m=1 mm_ok=1 model=sg13_hv_nmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1060 -60 0 0 {name=MU2 l=2u w=1.2u ng=4 m=1 mm_ok=1 model=sg13_hv_nmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1060 60 0 0 {name=MS2 l=0.45u w=1.2u ng=4 m=1 mm_ok=1 model=sg13_hv_nmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1300 -60 0 0 {name=MU3 l=2u w=2.4u ng=8 m=1 mm_ok=1 model=sg13_hv_nmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1300 60 0 0 {name=MS3 l=0.45u w=2.4u ng=8 m=1 mm_ok=1 model=sg13_hv_nmos spiceprefix=X}
C {lab_pin.sym} 530 60 0 0 {name=l1 sig_type=std_logic lab=b0}
C {lab_wire.sym} 600 0 0 0 {name=l2 sig_type=std_logic lab=s0}
C {lab_pin.sym} 770 60 0 0 {name=l3 sig_type=std_logic lab=b1}
C {lab_wire.sym} 840 0 0 0 {name=l4 sig_type=std_logic lab=s1}
C {lab_pin.sym} 1010 60 0 0 {name=l5 sig_type=std_logic lab=b2}
C {lab_wire.sym} 1080 0 0 0 {name=l6 sig_type=std_logic lab=s2}
C {lab_pin.sym} 1250 60 0 0 {name=l7 sig_type=std_logic lab=b3}
C {lab_wire.sym} 1320 0 0 0 {name=l8 sig_type=std_logic lab=s3}
C {iopin.sym} 0 -400 0 1 {name=p14 lab=vdd}
C {iopin.sym} 0 200 0 1 {name=p15 lab=vss}
C {iopin.sym} 1480 -200 0 0 {name=p16 lab=vin}
C {iopin.sym} 0 -140 0 1 {name=p17 lab=vbnl}
C {iopin.sym} 0 20 0 1 {name=p18 lab=b0}
C {iopin.sym} 0 50 0 1 {name=p19 lab=b1}
C {iopin.sym} 0 80 0 1 {name=p20 lab=b2}
C {iopin.sym} 0 110 0 1 {name=p21 lab=b3}

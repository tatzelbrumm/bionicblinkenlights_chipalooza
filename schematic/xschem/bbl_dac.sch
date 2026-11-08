v {xschem version=3.4.5 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {bbl_dac: tuning DAC, diode XMD carries (0.5 + code) x unit, code = b3..b0} -120 -520 0 0 0.6 0.6 {}
T {b0..b3 are 1.2 V logic (dig_in); the half-unit leg XMH is always on} -120 -470 0 0 0.3 0.3 {}
N -120 -360 940 -360 {lab=vdd}
N -120 490 940 490 {lab=vss}
N 340 230 340 300 {lab=s0}
N 480 230 480 300 {lab=s1}
N 620 230 620 300 {lab=s2}
N 760 230 760 300 {lab=s3}
N 140 -200 160 -200 {lab=vdd}
N 160 -200 160 -360 {lab=vdd}
N 140 -230 140 -360 {lab=vdd}
N 200 200 220 200 {lab=vss}
N 220 200 220 490 {lab=vss}
N 200 230 230 230 {lab=vss}
N 230 230 230 490 {lab=vss}
N 340 200 360 200 {lab=vss}
N 360 200 360 490 {lab=vss}
N 480 200 500 200 {lab=vss}
N 500 200 500 490 {lab=vss}
N 620 200 640 200 {lab=vss}
N 640 200 640 490 {lab=vss}
N 760 200 780 200 {lab=vss}
N 780 200 780 490 {lab=vss}
N 340 330 360 330 {lab=vss}
N 360 330 360 490 {lab=vss}
N 340 360 340 490 {lab=vss}
N 480 330 500 330 {lab=vss}
N 500 330 500 490 {lab=vss}
N 480 360 480 490 {lab=vss}
N 620 330 640 330 {lab=vss}
N 640 330 640 490 {lab=vss}
N 620 360 620 490 {lab=vss}
N 760 330 780 330 {lab=vss}
N 780 330 780 490 {lab=vss}
N 760 360 760 490 {lab=vss}
N 100 -200 100 -40 {lab=vin}
N 140 -170 140 -40 {lab=vin}
N 160 200 160 -20 {lab=vbnl}
N 200 170 200 -40 {lab=vin}
N 300 200 300 -20 {lab=vbnl}
N 340 170 340 -40 {lab=vin}
N 440 200 440 -20 {lab=vbnl}
N 480 170 480 -40 {lab=vin}
N 580 200 580 -20 {lab=vbnl}
N 620 170 620 -40 {lab=vin}
N 720 200 720 -20 {lab=vbnl}
N 760 170 760 -40 {lab=vin}
N 300 330 310 330 {lab=b0}
N 310 330 310 -120 {lab=b0}
N 440 330 450 330 {lab=b1}
N 450 330 450 -100 {lab=b1}
N 580 330 590 330 {lab=b2}
N 590 330 590 -80 {lab=b2}
N 720 330 730 330 {lab=b3}
N 730 330 730 -60 {lab=b3}
N -120 -120 310 -120 {lab=b0}
N -120 -100 450 -100 {lab=b1}
N -120 -80 590 -80 {lab=b2}
N -120 -60 730 -60 {lab=b3}
N -120 -40 760 -40 {lab=vin}
N -120 -20 720 -20 {lab=vbnl}
C {lab_pin.sym} 340 300 0 1 {name=l0 sig_type=std_logic lab=s0}
C {lab_pin.sym} 480 300 0 1 {name=l1 sig_type=std_logic lab=s1}
C {lab_pin.sym} 620 300 0 1 {name=l2 sig_type=std_logic lab=s2}
C {lab_pin.sym} 760 300 0 1 {name=l3 sig_type=std_logic lab=s3}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 120 -200 0 0 {name=MD l=3u w=3u ng=1 m=1 mm_ok=1 model=sg13_hv_pmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 180 200 0 0 {name=MH l=9u w=0.3u ng=1 m=1 mm_ok=1 model=sg13_hv_nmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 320 200 0 0 {name=MU0 l=2u w=0.3u ng=1 m=1 mm_ok=1 model=sg13_hv_nmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 460 200 0 0 {name=MU1 l=2u w=0.6u ng=2 m=1 mm_ok=1 model=sg13_hv_nmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 600 200 0 0 {name=MU2 l=2u w=1.2u ng=4 m=1 mm_ok=1 model=sg13_hv_nmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 740 200 0 0 {name=MU3 l=2u w=2.4u ng=8 m=1 mm_ok=1 model=sg13_hv_nmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 320 330 0 0 {name=MS0 l=0.45u w=0.3u ng=1 m=1 mm_ok=1 model=sg13_hv_nmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 460 330 0 0 {name=MS1 l=0.45u w=0.6u ng=2 m=1 mm_ok=1 model=sg13_hv_nmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 600 330 0 0 {name=MS2 l=0.45u w=1.2u ng=4 m=1 mm_ok=1 model=sg13_hv_nmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 740 330 0 0 {name=MS3 l=0.45u w=2.4u ng=8 m=1 mm_ok=1 model=sg13_hv_nmos spiceprefix=X}
C {iopin.sym} -120 -360 0 0 {name=p14 lab=vdd}
C {iopin.sym} -120 490 0 0 {name=p15 lab=vss}
C {iopin.sym} -120 -40 0 0 {name=p16 lab=vin}
C {iopin.sym} -120 -20 0 0 {name=p17 lab=vbnl}
C {iopin.sym} -120 -120 0 0 {name=p18 lab=b0}
C {iopin.sym} -120 -100 0 0 {name=p19 lab=b1}
C {iopin.sym} -120 -80 0 0 {name=p20 lab=b2}
C {iopin.sym} -120 -60 0 0 {name=p21 lab=b3}

v {xschem version=3.4.5 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {bbl_tielo: dig_out[11:0] held low (1.2 V NMOS)} -120 -550 0 0 0.6 0.6 {}
N -120 -390 1920 -390 {lab=vddl}
N -120 390 1920 390 {lab=vss}
N 200 230 220 230 {lab=vss}
N 220 230 220 390 {lab=vss}
N 340 230 360 230 {lab=vss}
N 360 230 360 390 {lab=vss}
N 480 230 500 230 {lab=vss}
N 500 230 500 390 {lab=vss}
N 620 230 640 230 {lab=vss}
N 640 230 640 390 {lab=vss}
N 760 230 780 230 {lab=vss}
N 780 230 780 390 {lab=vss}
N 900 230 920 230 {lab=vss}
N 920 230 920 390 {lab=vss}
N 1040 230 1060 230 {lab=vss}
N 1060 230 1060 390 {lab=vss}
N 1180 230 1200 230 {lab=vss}
N 1200 230 1200 390 {lab=vss}
N 1320 230 1340 230 {lab=vss}
N 1340 230 1340 390 {lab=vss}
N 1460 230 1480 230 {lab=vss}
N 1480 230 1480 390 {lab=vss}
N 1600 230 1620 230 {lab=vss}
N 1620 230 1620 390 {lab=vss}
N 1740 230 1760 230 {lab=vss}
N 1760 230 1760 390 {lab=vss}
N 160 230 160 90 {lab=vddl}
N 200 200 200 -150 {lab=q0}
N 300 230 300 90 {lab=vddl}
N 340 200 340 -130 {lab=q1}
N 440 230 440 90 {lab=vddl}
N 480 200 480 -110 {lab=q2}
N 580 230 580 90 {lab=vddl}
N 620 200 620 -90 {lab=q3}
N 720 230 720 90 {lab=vddl}
N 760 200 760 -70 {lab=q4}
N 860 230 860 90 {lab=vddl}
N 900 200 900 -50 {lab=q5}
N 1000 230 1000 90 {lab=vddl}
N 1040 200 1040 -30 {lab=q6}
N 1140 230 1140 90 {lab=vddl}
N 1180 200 1180 -10 {lab=q7}
N 1280 230 1280 90 {lab=vddl}
N 1320 200 1320 10 {lab=q8}
N 1420 230 1420 90 {lab=vddl}
N 1460 200 1460 30 {lab=q9}
N 1560 230 1560 90 {lab=vddl}
N 1600 200 1600 50 {lab=q10}
N 1700 230 1700 90 {lab=vddl}
N 1740 200 1740 70 {lab=q11}
N 200 260 230 260 {lab=vssl}
N 230 260 230 110 {lab=vssl}
N 340 260 370 260 {lab=vssl}
N 370 260 370 110 {lab=vssl}
N 480 260 510 260 {lab=vssl}
N 510 260 510 110 {lab=vssl}
N 620 260 650 260 {lab=vssl}
N 650 260 650 110 {lab=vssl}
N 760 260 790 260 {lab=vssl}
N 790 260 790 110 {lab=vssl}
N 900 260 930 260 {lab=vssl}
N 930 260 930 110 {lab=vssl}
N 1040 260 1070 260 {lab=vssl}
N 1070 260 1070 110 {lab=vssl}
N 1180 260 1210 260 {lab=vssl}
N 1210 260 1210 110 {lab=vssl}
N 1320 260 1350 260 {lab=vssl}
N 1350 260 1350 110 {lab=vssl}
N 1460 260 1490 260 {lab=vssl}
N 1490 260 1490 110 {lab=vssl}
N 1600 260 1630 260 {lab=vssl}
N 1630 260 1630 110 {lab=vssl}
N 1740 260 1770 260 {lab=vssl}
N 1770 260 1770 110 {lab=vssl}
N -120 -150 200 -150 {lab=q0}
N -120 -130 340 -130 {lab=q1}
N -120 -110 480 -110 {lab=q2}
N -120 -90 620 -90 {lab=q3}
N -120 -70 760 -70 {lab=q4}
N -120 -50 900 -50 {lab=q5}
N -120 -30 1040 -30 {lab=q6}
N -120 -10 1180 -10 {lab=q7}
N -120 10 1320 10 {lab=q8}
N -120 30 1460 30 {lab=q9}
N -120 50 1600 50 {lab=q10}
N -120 70 1740 70 {lab=q11}
N 160 90 1880 90 {lab=vddl}
N 1880 90 1880 -390 {lab=vddl}
N -120 110 1770 110 {lab=vssl}
C {sg13cmos5l_pr/sg13_lv_nmos.sym} 180 230 0 0 {name=MT0 l=0.5u w=0.3u ng=1 m=1 mm_ok=1 model=sg13_lv_nmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_lv_nmos.sym} 320 230 0 0 {name=MT1 l=0.5u w=0.3u ng=1 m=1 mm_ok=1 model=sg13_lv_nmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_lv_nmos.sym} 460 230 0 0 {name=MT2 l=0.5u w=0.3u ng=1 m=1 mm_ok=1 model=sg13_lv_nmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_lv_nmos.sym} 600 230 0 0 {name=MT3 l=0.5u w=0.3u ng=1 m=1 mm_ok=1 model=sg13_lv_nmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_lv_nmos.sym} 740 230 0 0 {name=MT4 l=0.5u w=0.3u ng=1 m=1 mm_ok=1 model=sg13_lv_nmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_lv_nmos.sym} 880 230 0 0 {name=MT5 l=0.5u w=0.3u ng=1 m=1 mm_ok=1 model=sg13_lv_nmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_lv_nmos.sym} 1020 230 0 0 {name=MT6 l=0.5u w=0.3u ng=1 m=1 mm_ok=1 model=sg13_lv_nmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_lv_nmos.sym} 1160 230 0 0 {name=MT7 l=0.5u w=0.3u ng=1 m=1 mm_ok=1 model=sg13_lv_nmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_lv_nmos.sym} 1300 230 0 0 {name=MT8 l=0.5u w=0.3u ng=1 m=1 mm_ok=1 model=sg13_lv_nmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_lv_nmos.sym} 1440 230 0 0 {name=MT9 l=0.5u w=0.3u ng=1 m=1 mm_ok=1 model=sg13_lv_nmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_lv_nmos.sym} 1580 230 0 0 {name=MT10 l=0.5u w=0.3u ng=1 m=1 mm_ok=1 model=sg13_lv_nmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_lv_nmos.sym} 1720 230 0 0 {name=MT11 l=0.5u w=0.3u ng=1 m=1 mm_ok=1 model=sg13_lv_nmos spiceprefix=X}
C {iopin.sym} -120 -390 0 0 {name=p12 lab=vddl}
C {iopin.sym} -120 110 0 0 {name=p13 lab=vssl}
C {iopin.sym} -120 390 0 0 {name=p14 lab=vss}
C {iopin.sym} -120 -150 0 0 {name=p15 lab=q0}
C {iopin.sym} -120 -130 0 0 {name=p16 lab=q1}
C {iopin.sym} -120 -110 0 0 {name=p17 lab=q2}
C {iopin.sym} -120 -90 0 0 {name=p18 lab=q3}
C {iopin.sym} -120 -70 0 0 {name=p19 lab=q4}
C {iopin.sym} -120 -50 0 0 {name=p20 lab=q5}
C {iopin.sym} -120 -30 0 0 {name=p21 lab=q6}
C {iopin.sym} -120 -10 0 0 {name=p22 lab=q7}
C {iopin.sym} -120 10 0 0 {name=p23 lab=q8}
C {iopin.sym} -120 30 0 0 {name=p24 lab=q9}
C {iopin.sym} -120 50 0 0 {name=p25 lab=q10}
C {iopin.sym} -120 70 0 0 {name=p26 lab=q11}

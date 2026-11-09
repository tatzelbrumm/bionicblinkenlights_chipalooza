v {xschem version=3.4.5 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {bbl_gap: gap junction (electrical synapse) a <-> b} -120 -480 0 0 0.6 0.6 {}
T {pass gates at the analog coupling voltage vc in series with 1.2 V enables} -120 -410 0 0 0.3 0.3 {}
N -120 -320 520 -320 {lab=vdd}
N -120 450 520 450 {lab=vss}
N 200 190 200 260 {lab=gw}
N 340 190 340 260 {lab=gs}
N 200 160 220 160 {lab=vss}
N 220 160 220 450 {lab=vss}
N 340 160 360 160 {lab=vss}
N 360 160 360 450 {lab=vss}
N 200 290 220 290 {lab=vss}
N 220 290 220 450 {lab=vss}
N 340 290 360 290 {lab=vss}
N 360 290 360 450 {lab=vss}
N 160 160 160 -40 {lab=vc}
N 200 130 200 -20 {lab=a}
N 300 160 300 -40 {lab=vc}
N 340 130 340 -20 {lab=a}
N 160 290 170 290 {lab=enw}
N 170 290 170 -80 {lab=enw}
N 200 320 250 320 {lab=b}
N 250 320 250 0 {lab=b}
N 300 290 310 290 {lab=ens}
N 310 290 310 -60 {lab=ens}
N 340 320 390 320 {lab=b}
N 390 320 390 0 {lab=b}
N -120 -80 170 -80 {lab=enw}
N -120 -60 310 -60 {lab=ens}
N -120 -40 300 -40 {lab=vc}
N -120 -20 340 -20 {lab=a}
N -120 0 390 0 {lab=b}
C {lab_pin.sym} 200 260 0 1 {name=l0 sig_type=std_logic lab=gw}
C {lab_pin.sym} 340 260 0 1 {name=l1 sig_type=std_logic lab=gs}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 180 160 0 0 {name=MGW l=10u w=0.3u ng=1 m=1 mm_ok=1 model=sg13_hv_nmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 320 160 0 0 {name=MGS l=0.45u w=1u ng=1 m=1 mm_ok=1 model=sg13_hv_nmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 180 290 0 0 {name=MTW l=0.45u w=0.3u ng=1 m=1 mm_ok=1 model=sg13_hv_nmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 320 290 0 0 {name=MTS l=0.45u w=1u ng=1 m=1 mm_ok=1 model=sg13_hv_nmos spiceprefix=X}
C {iopin.sym} -120 450 0 0 {name=p6 lab=vss}
C {iopin.sym} -120 -20 0 0 {name=p7 lab=a}
C {iopin.sym} -120 0 0 0 {name=p8 lab=b}
C {iopin.sym} -120 -40 0 0 {name=p9 lab=vc}
C {iopin.sym} -120 -80 0 0 {name=p10 lab=enw}
C {iopin.sym} -120 -60 0 0 {name=p11 lab=ens}

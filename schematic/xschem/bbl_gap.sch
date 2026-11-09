v {xschem version=3.4.5 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {bbl_gap: gap junction (electrical synapse) a <-> b} 0 -440 0 0 0.6 0.6 {}
T {pass gates at the analog coupling voltage vc in series with 1.2 V enables} 0 -370 0 0 0.3 0.3 {}
T {weak leg} 140 -300 0 0 0.35 0.35 {layer=8}
T {strong leg} 400 -300 0 0 0.35 0.35 {layer=8}
N 200 -130 200 -240 {lab=a}
N 200 -70 200 10 {lab=gw}
N 200 70 200 140 {lab=b}
N 200 -100 300 -100 {lab=vss}
N 300 -100 300 220 {lab=vss}
N 200 40 300 40 {lab=vss}
N 160 -180 160 -100 {lab=vc}
N 460 -130 460 -240 {lab=a}
N 460 -70 460 10 {lab=gs}
N 460 70 460 140 {lab=b}
N 460 -100 560 -100 {lab=vss}
N 560 -100 560 220 {lab=vss}
N 460 40 560 40 {lab=vss}
N 420 -180 420 -100 {lab=vc}
N 0 -240 460 -240 {lab=a}
N 0 -180 420 -180 {lab=vc}
N 0 40 160 40 {lab=enw}
N 390 40 420 40 {lab=ens}
N 0 140 460 140 {lab=b}
N 0 220 560 220 {lab=vss}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 180 -100 0 0 {name=MGW l=10u w=0.3u ng=1 m=1 mm_ok=1 model=sg13_hv_nmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 180 40 0 0 {name=MTW l=0.45u w=0.3u ng=1 m=1 mm_ok=1 model=sg13_hv_nmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 440 -100 0 0 {name=MGS l=0.45u w=1u ng=1 m=1 mm_ok=1 model=sg13_hv_nmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 440 40 0 0 {name=MTS l=0.45u w=1u ng=1 m=1 mm_ok=1 model=sg13_hv_nmos spiceprefix=X}
C {lab_wire.sym} 200 -30 0 0 {name=l1 sig_type=std_logic lab=gw}
C {lab_wire.sym} 460 -30 0 0 {name=l2 sig_type=std_logic lab=gs}
C {lab_pin.sym} 390 40 0 0 {name=l3 sig_type=std_logic lab=ens}
C {iopin.sym} 0 220 0 1 {name=p6 lab=vss}
C {iopin.sym} 0 -240 0 1 {name=p7 lab=a}
C {iopin.sym} 0 140 0 1 {name=p8 lab=b}
C {iopin.sym} 0 -180 0 1 {name=p9 lab=vc}
C {iopin.sym} 0 40 0 1 {name=p10 lab=enw}
C {iopin.sym} 0 90 0 1 {name=p11 lab=ens}

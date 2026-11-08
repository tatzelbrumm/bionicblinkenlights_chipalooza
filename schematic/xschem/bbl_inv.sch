v {xschem version=3.4.5 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {bbl_inv: 3.3 V inverter (LED bus driver, spike output)} -120 -440 0 0 0.6 0.6 {}
N -120 -280 380 -280 {lab=vdd}
N -120 280 380 280 {lab=vss}
N 140 -120 160 -120 {lab=vdd}
N 160 -120 160 -280 {lab=vdd}
N 140 -150 140 -280 {lab=vdd}
N 200 120 220 120 {lab=vss}
N 220 120 220 280 {lab=vss}
N 200 150 200 280 {lab=vss}
N 100 -120 100 -40 {lab=a}
N 140 -90 140 -20 {lab=y}
N 160 120 160 -40 {lab=a}
N 200 90 200 -20 {lab=y}
N -120 -40 160 -40 {lab=a}
N -120 -20 200 -20 {lab=y}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 120 -120 0 0 {name=MP l=0.45u w=1u ng=1 m=1 mm_ok=1 model=sg13_hv_pmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 180 120 0 0 {name=MN l=0.45u w=1u ng=1 m=1 mm_ok=1 model=sg13_hv_nmos spiceprefix=X}
C {iopin.sym} -120 -280 0 0 {name=p2 lab=vdd}
C {iopin.sym} -120 280 0 0 {name=p3 lab=vss}
C {iopin.sym} -120 -40 0 0 {name=p4 lab=a}
C {iopin.sym} -120 -20 0 0 {name=p5 lab=y}

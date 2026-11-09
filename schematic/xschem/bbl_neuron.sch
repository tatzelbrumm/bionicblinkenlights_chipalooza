v {xschem version=3.4.5 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {bbl_neuron: Bionic Blinkenlight integrate-and-fire neuron (CMOS translation)} -120 -470 0 0 0.6 0.6 {}
T {Q1..Q4 of the discrete circuit = XM1..XM4; resistors = XMR1..XMR5 (R4 merged into XM3)} -120 -420 0 0 0.3 0.3 {}
T {XC1 membrane capacitor 10 pF (PMOS gate cap), XC2 slow-node capacitor 1.8 pF} -120 -390 0 0 0.3 0.3 {}
T {self-biased: gates of XMR1, XMR5 on vss, XMR2 on vdd; only XMR3 (vin) is biased} -120 -360 0 0 0.3 0.3 {}
N -120 -310 1020 -310 {lab=vdd}
N -120 310 1020 310 {lab=vss}
N 140 -150 160 -150 {lab=vdd}
N 160 -150 160 -310 {lab=vdd}
N 140 -180 140 -310 {lab=vdd}
N 280 -150 300 -150 {lab=vdd}
N 300 -150 300 -310 {lab=vdd}
N 280 -180 280 -310 {lab=vdd}
N 280 -120 310 -120 {lab=vdd}
N 310 -120 310 -310 {lab=vdd}
N 420 -150 440 -150 {lab=vdd}
N 440 -150 440 -310 {lab=vdd}
N 420 -180 420 -310 {lab=vdd}
N 560 -150 580 -150 {lab=vdd}
N 580 -150 580 -310 {lab=vdd}
N 560 -180 560 -310 {lab=vdd}
N 700 -150 720 -150 {lab=vdd}
N 720 -150 720 -310 {lab=vdd}
N 700 -180 700 -310 {lab=vdd}
N 840 -150 860 -150 {lab=vdd}
N 860 -150 860 -310 {lab=vdd}
N 200 150 220 150 {lab=vss}
N 220 150 220 310 {lab=vss}
N 200 180 200 310 {lab=vss}
N 340 150 360 150 {lab=vss}
N 360 150 360 310 {lab=vss}
N 340 180 340 310 {lab=vss}
N 480 150 500 150 {lab=vss}
N 500 150 500 310 {lab=vss}
N 480 180 480 310 {lab=vss}
N 620 150 640 150 {lab=vss}
N 640 150 640 310 {lab=vss}
N 620 120 650 120 {lab=vss}
N 650 120 650 310 {lab=vss}
N 620 180 620 310 {lab=vss}
N 100 -150 100 -30 {lab=vin}
N 140 -120 140 -10 {lab=vm}
N 240 -150 240 -10 {lab=vm}
N 380 -150 380 -70 {lab=out}
N 420 -120 420 -10 {lab=vm}
N 520 -150 520 -50 {lab=vss}
N 560 -120 560 -70 {lab=out}
N 660 -150 660 10 {lab=slow}
N 700 -120 700 30 {lab=rst}
N 800 -150 800 -50 {lab=vss}
N 840 -120 840 10 {lab=slow}
N 160 150 160 30 {lab=rst}
N 200 120 200 -10 {lab=vm}
N 300 150 300 -10 {lab=vm}
N 340 120 340 -70 {lab=out}
N 440 150 440 50 {lab=vdd}
N 480 120 480 30 {lab=rst}
N 580 150 580 10 {lab=slow}
N 840 -180 870 -180 {lab=out}
N 870 -180 870 -70 {lab=out}
N -120 -70 870 -70 {lab=out}
N 520 -50 1000 -50 {lab=vss}
N 1000 -50 1000 310 {lab=vss}
N -120 -30 100 -30 {lab=vin}
N -120 -10 420 -10 {lab=vm}
N 580 10 840 10 {lab=slow}
N 160 30 700 30 {lab=rst}
N 440 50 980 50 {lab=vdd}
N 980 50 980 -310 {lab=vdd}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 120 -150 0 0 {name=MR3 l=30u w=0.3u ng=1 m=1 mm_ok=1 model=sg13_hv_pmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 260 -150 0 0 {name=C1 l=10u w=225u ng=18 m=1 mm_ok=1 model=sg13_hv_pmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 400 -150 0 0 {name=M3 l=4u w=0.3u ng=1 m=1 mm_ok=1 model=sg13_hv_pmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 540 -150 0 0 {name=MR1 l=20u w=0.3u ng=1 m=1 mm_ok=1 model=sg13_hv_pmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 680 -150 0 0 {name=M4 l=0.45u w=1u ng=1 m=1 mm_ok=1 model=sg13_hv_pmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 820 -150 0 0 {name=MR5 l=100u w=0.3u ng=1 m=1 mm_ok=1 model=sg13_hv_pmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 180 150 0 0 {name=M2 l=0.45u w=2u ng=1 m=1 mm_ok=1 model=sg13_hv_nmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 320 150 0 0 {name=M1 l=1u w=1u ng=1 m=1 mm_ok=1 model=sg13_hv_nmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 460 150 0 0 {name=MR2 l=20u w=0.3u ng=1 m=1 mm_ok=1 model=sg13_hv_nmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 600 150 0 0 {name=C2 l=10u w=60u ng=6 m=1 mm_ok=1 model=sg13_hv_nmos spiceprefix=X}
C {lab_pin.sym} 580 10 0 0 {name=l10 sig_type=std_logic lab=slow}
C {lab_pin.sym} 160 30 0 0 {name=l11 sig_type=std_logic lab=rst}
C {iopin.sym} -120 -310 0 0 {name=p12 lab=vdd}
C {iopin.sym} -120 310 0 0 {name=p13 lab=vss}
C {iopin.sym} -120 -10 0 0 {name=p14 lab=vm}
C {iopin.sym} -120 -70 0 0 {name=p15 lab=out}
C {iopin.sym} -120 -30 0 0 {name=p16 lab=vin}

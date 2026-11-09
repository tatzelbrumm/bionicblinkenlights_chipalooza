v {xschem version=3.4.5 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {R3} 211 -334 0 0 0.3 0.3 {layer=8}
T {C1} 361 -334 0 0 0.3 0.3 {layer=8}
T {Q2} 409 126 0 1 0.3 0.3 {layer=8}
T {Q3 + R4} 509 -174 0 1 0.3 0.3 {layer=8}
T {R1} 691 -334 0 0 0.3 0.3 {layer=8}
T {Q1} 691 6 0 0 0.3 0.3 {layer=8}
T {R5b} 889 -334 0 1 0.3 0.3 {layer=8}
T {C2} 951 6 0 0 0.3 0.3 {layer=8}
T {Q4} 1071 -174 0 0 0.3 0.3 {layer=8}
T {R2} 1049 216 0 1 0.3 0.3 {layer=8}
T {R5a} 776 -246 0 1 0.3 0.3 {layer=8}
T {bbl_neuron_hi: the neuron of N3, robust against bus leakage (generated from bbl_neuron.sch)} 0 -710 0 0 0.6 0.6 {}
T {Q1..Q4, R1..R5, C1, C2 of the discrete circuit (spike1.asc) are marked under each device; R4 = the length of XM3} 0 -650 0 0 0.3 0.3 {}
T {XC1 membrane capacitor 10 pF (PMOS gate cap), XC2 slow-node capacitor 2.6 pF} 0 -620 0 0 0.3 0.3 {}
T {self-biased: XMR1 gate on vss, XMR2 and XMR5A gates on vdd; XMR3 and XMR5B on the DAC bias vin} 0 -590 0 0 0.3 0.3 {}
T {XMR3 mirrors 16 x the DAC current (5.6 .. 174 nA): audio rates on chip, blinking with about 10 nF on the bus; XM2, XM4, XMR5B resized; XMR5A: slow to vss, gate outb} 0 -530 0 0 0.3 0.3 {}
T {Schmitt comparator (right): inverter XMIP / XMIN (out -> outb, switches at about 2.3 V) and pull-up XMQ on out (gate outb)} 0 -500 0 0 0.3 0.3 {}
T {R5 = XMR5A (fast discharge of slow) + XMR5B (slow recharge: refractory time, complete reset)} 0 -560 0 0 0.3 0.3 {}
N 0 -480 1180 -480 {lab=vdd}
N 0 250 1060 250 {lab=vss}
N 200 -380 200 -480 {lab=vdd}
N 680 -380 680 -480 {lab=vdd}
N 1060 -220 1060 -480 {lab=vdd}
N 900 -380 900 -480 {lab=vdd}
N 520 -220 520 -480 {lab=vdd}
N 350 -350 350 -480 {lab=vdd}
N 420 80 420 250 {lab=vss}
N 680 -40 680 250 {lab=vss}
N 1060 170 1060 250 {lab=vss}
N 940 -70 940 250 {lab=vss}
N 790 -180 790 40 {lab=vss}
N 790 40 940 40 {lab=vss}
N 0 -380 160 -380 {lab=vin}
N 200 -350 200 -40 {lab=vm}
N 310 -380 310 -40 {lab=vm}
N 0 -40 640 -40 {lab=vm}
N 420 50 420 -40 {lab=vm}
N 520 -190 520 -40 {lab=vm}
N 680 -350 680 -70 {lab=out}
N 560 -220 680 -220 {lab=out}
N 740 -180 760 -180 {lab=vss}
C {lab_pin.sym} 740 -180 0 0 {name=l24 sig_type=std_logic lab=vss}
N 610 -380 640 -380 {lab=vss}
N 790 -220 790 -260 {lab=outb}
C {lab_pin.sym} 790 -260 0 1 {name=l25 sig_type=std_logic lab=outb}
N 820 -180 900 -180 {lab=slow}
N 900 -350 900 -40 {lab=slow}
N 900 -220 1020 -220 {lab=slow}
N 940 -380 970 -380 {lab=vin}
N 1060 -190 1060 140 {lab=rst}
N 460 80 1060 80 {lab=rst}
N 1100 170 1180 170 {lab=vdd}
N 1180 170 1180 -480 {lab=vdd}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 180 -380 0 0 {name=MR3 l=3u w=48u ng=8 m=1 mm_ok=1 model=sg13_hv_pmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 330 -380 0 0 {name=C1 l=10u w=225u ng=18 m=1 mm_ok=1 model=sg13_hv_pmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 440 80 0 1 {name=M2 l=0.45u w=40u ng=8 m=1 mm_ok=1 model=sg13_hv_nmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 540 -220 0 1 {name=M3 l=4u w=0.3u ng=1 m=1 mm_ok=1 model=sg13_hv_pmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 660 -380 0 0 {name=MR1 l=20u w=0.3u ng=1 m=1 mm_ok=1 model=sg13_hv_pmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 660 -40 0 0 {name=M1 l=1u w=1u ng=1 m=1 mm_ok=1 model=sg13_hv_nmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 790 -200 1 0 {name=MR5A l=0.45u w=3u ng=1 m=1 mm_ok=1 model=sg13_hv_nmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 920 -380 0 1 {name=MR5B l=0.45u w=10u ng=2 m=1 mm_ok=1 model=sg13_hv_pmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 920 -40 0 0 {name=C2 l=10u w=60u ng=6 m=1 mm_ok=1 model=sg13_hv_nmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1040 -220 0 0 {name=M4 l=0.45u w=10u ng=2 m=1 mm_ok=1 model=sg13_hv_pmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1080 170 0 1 {name=MR2 l=20u w=0.3u ng=1 m=1 mm_ok=1 model=sg13_hv_nmos spiceprefix=X}
C {lab_pin.sym} 610 -380 0 0 {name=l1 sig_type=std_logic lab=vss}
C {lab_pin.sym} 970 -380 0 1 {name=l2 sig_type=std_logic lab=vin}
C {lab_wire.sym} 600 -220 0 1 {name=l3 sig_type=std_logic lab=out}
C {lab_wire.sym} 950 -220 0 1 {name=l4 sig_type=std_logic lab=slow}
C {lab_wire.sym} 560 80 0 1 {name=l5 sig_type=std_logic lab=rst}
C {iopin.sym} 0 -480 0 1 {name=p13 lab=vdd}
C {iopin.sym} 0 250 0 1 {name=p14 lab=vss}
C {iopin.sym} 0 -40 0 1 {name=p15 lab=vm}
C {iopin.sym} 0 -220 0 1 {name=p16 lab=out}
C {iopin.sym} 0 -380 0 1 {name=p17 lab=vin}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1300 -380 0 0 {name=MQ l=3u w=0.3u ng=1 m=1 mm_ok=1 model=sg13_hv_pmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1440 -380 0 0 {name=MIP l=0.45u w=3u ng=1 m=1 mm_ok=1 model=sg13_hv_pmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 1440 -60 0 0 {name=MIN l=4u w=0.3u ng=1 m=1 mm_ok=1 model=sg13_hv_nmos spiceprefix=X}
N 1180 -480 1460 -480 {lab=vdd}
N 1060 250 1460 250 {lab=vss}
N 1320 -380 1320 -480 {lab=vdd}
N 1460 -380 1460 -480 {lab=vdd}
N 1460 -60 1460 250 {lab=vss}
N 1320 -350 1320 -320 {lab=out}
C {lab_pin.sym} 1320 -320 0 1 {name=l20 sig_type=std_logic lab=out}
N 1260 -380 1280 -380 {lab=outb}
C {lab_pin.sym} 1260 -380 0 0 {name=l21 sig_type=std_logic lab=outb}
N 1460 -350 1460 -90 {lab=outb}
N 1460 -220 1500 -220 {lab=outb}
C {lab_pin.sym} 1500 -220 0 1 {name=l22 sig_type=std_logic lab=outb}
N 1420 -380 1420 -60 {lab=out}
N 1400 -220 1420 -220 {lab=out}
C {lab_pin.sym} 1400 -220 0 0 {name=l23 sig_type=std_logic lab=out}

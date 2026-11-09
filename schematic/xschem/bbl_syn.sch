v {xschem version=3.4.5 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {bbl_syn: pulse synapse (stand-in for the photoresistor of the demos)} 0 -600 0 0 0.6 0.6 {}
T {g = NAND(spk, en): XMN/XMB stack, pull-ups XMP (spk) and XMR (self-biased, en)} 0 -540 0 0 0.3 0.3 {}
T {XMSW weak leg (0.3/100), XMSS strong leg (0.3/20) into the postsynaptic membrane} 0 -510 0 0 0.3 0.3 {}
T {weak leg: gw = NAND(spk, enw)} 100 -450 0 0 0.35 0.35 {layer=8}
T {strong leg: gs = NAND(spk, ens)} 660 -450 0 0 0.35 0.35 {layer=8}
N 180 -300 180 -400 {lab=vdd}
N 400 -300 400 -400 {lab=vdd}
N 540 -300 540 -400 {lab=vdd}
N 180 40 180 180 {lab=vss}
N 180 -80 280 -80 {lab=vss}
N 280 -80 280 180 {lab=vss}
N 180 -270 180 -110 {lab=gw}
N 400 -270 400 -200 {lab=gw}
N 180 -200 500 -200 {lab=gw}
N 500 -200 500 -300 {lab=gw}
N 180 -50 180 10 {lab=bw}
N 140 -300 100 -300 {lab=spk}
N 100 -300 100 40 {lab=spk}
N 0 40 140 40 {lab=spk}
N 0 -80 140 -80 {lab=enw}
N 330 -300 360 -300 {lab=vss}
N 540 -270 540 120 {lab=post}
N 740 -300 740 -400 {lab=vdd}
N 960 -300 960 -400 {lab=vdd}
N 1100 -300 1100 -400 {lab=vdd}
N 740 40 740 180 {lab=vss}
N 740 -80 840 -80 {lab=vss}
N 840 -80 840 180 {lab=vss}
N 740 -270 740 -110 {lab=gs}
N 960 -270 960 -200 {lab=gs}
N 740 -200 1060 -200 {lab=gs}
N 1060 -200 1060 -300 {lab=gs}
N 740 -50 740 10 {lab=bs}
N 700 -300 660 -300 {lab=spk}
N 660 -300 660 40 {lab=spk}
N 630 40 700 40 {lab=spk}
N 630 -80 700 -80 {lab=ens}
N 890 -300 920 -300 {lab=vss}
N 1100 -270 1100 120 {lab=post}
N 0 -400 1100 -400 {lab=vdd}
N 0 180 840 180 {lab=vss}
N 540 120 1160 120 {lab=post}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 160 -300 0 0 {name=MPW l=0.45u w=0.3u ng=1 m=1 mm_ok=1 model=sg13_hv_pmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 160 -80 0 0 {name=MNW l=0.45u w=0.3u ng=1 m=1 mm_ok=1 model=sg13_hv_nmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 160 40 0 0 {name=MBW l=0.45u w=0.3u ng=1 m=1 mm_ok=1 model=sg13_hv_nmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 380 -300 0 0 {name=MRW l=20u w=0.3u ng=1 m=1 mm_ok=1 model=sg13_hv_pmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 520 -300 0 0 {name=MSW l=100u w=0.3u ng=1 m=1 mm_ok=1 model=sg13_hv_pmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 720 -300 0 0 {name=MPS l=0.45u w=0.3u ng=1 m=1 mm_ok=1 model=sg13_hv_pmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 720 -80 0 0 {name=MNS l=0.45u w=0.3u ng=1 m=1 mm_ok=1 model=sg13_hv_nmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 720 40 0 0 {name=MBS l=0.45u w=0.3u ng=1 m=1 mm_ok=1 model=sg13_hv_nmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 940 -300 0 0 {name=MRS l=20u w=0.3u ng=1 m=1 mm_ok=1 model=sg13_hv_pmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 1080 -300 0 0 {name=MSS l=20u w=0.3u ng=1 m=1 mm_ok=1 model=sg13_hv_pmos spiceprefix=X}
C {lab_pin.sym} 330 -300 0 0 {name=l1 sig_type=std_logic lab=vss}
C {lab_wire.sym} 420 -200 0 1 {name=l2 sig_type=std_logic lab=gw}
C {lab_wire.sym} 180 -20 0 0 {name=l3 sig_type=std_logic lab=bw}
C {lab_pin.sym} 890 -300 0 0 {name=l4 sig_type=std_logic lab=vss}
C {lab_wire.sym} 980 -200 0 1 {name=l5 sig_type=std_logic lab=gs}
C {lab_wire.sym} 740 -20 0 0 {name=l6 sig_type=std_logic lab=bs}
C {lab_pin.sym} 630 40 0 0 {name=l7 sig_type=std_logic lab=spk}
C {lab_pin.sym} 630 -80 0 0 {name=l8 sig_type=std_logic lab=ens}
C {iopin.sym} 0 -400 0 1 {name=p14 lab=vdd}
C {iopin.sym} 0 180 0 1 {name=p15 lab=vss}
C {iopin.sym} 0 40 0 1 {name=p16 lab=spk}
C {iopin.sym} 1160 120 0 0 {name=p17 lab=post}
C {iopin.sym} 0 -80 0 1 {name=p18 lab=enw}
C {iopin.sym} 0 -20 0 1 {name=p19 lab=ens}

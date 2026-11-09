v {xschem version=3.4.5 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {bbl_syn: pulse synapse (stand-in for the photoresistor of the demos)} -120 -530 0 0 0.6 0.6 {}
T {g = NAND(spk, en): XMN/XMB stack, pull-ups XMP (spk) and XMR (self-biased, en)} -120 -460 0 0 0.3 0.3 {}
T {XMSW weak leg (0.3/100), XMSS strong leg (0.3/20) into the postsynaptic membrane} -120 -430 0 0 0.3 0.3 {}
N -120 -340 1020 -340 {lab=vdd}
N -120 470 1020 470 {lab=vss}
N 200 210 200 280 {lab=bw}
N 340 210 340 280 {lab=bs}
N 140 -180 160 -180 {lab=vdd}
N 160 -180 160 -340 {lab=vdd}
N 140 -210 140 -340 {lab=vdd}
N 280 -180 300 -180 {lab=vdd}
N 300 -180 300 -340 {lab=vdd}
N 280 -210 280 -340 {lab=vdd}
N 420 -180 440 -180 {lab=vdd}
N 440 -180 440 -340 {lab=vdd}
N 420 -210 420 -340 {lab=vdd}
N 560 -180 580 -180 {lab=vdd}
N 580 -180 580 -340 {lab=vdd}
N 560 -210 560 -340 {lab=vdd}
N 700 -180 720 -180 {lab=vdd}
N 720 -180 720 -340 {lab=vdd}
N 700 -210 700 -340 {lab=vdd}
N 840 -180 860 -180 {lab=vdd}
N 860 -180 860 -340 {lab=vdd}
N 840 -210 840 -340 {lab=vdd}
N 200 180 220 180 {lab=vss}
N 220 180 220 470 {lab=vss}
N 340 180 360 180 {lab=vss}
N 360 180 360 470 {lab=vss}
N 200 310 220 310 {lab=vss}
N 220 310 220 470 {lab=vss}
N 200 340 200 470 {lab=vss}
N 340 310 360 310 {lab=vss}
N 360 310 360 470 {lab=vss}
N 340 340 340 470 {lab=vss}
N 100 -180 100 -20 {lab=spk}
N 140 -150 140 -100 {lab=gw}
N 240 -180 240 -80 {lab=vss}
N 280 -150 280 -100 {lab=gw}
N 380 -180 380 -100 {lab=gw}
N 420 -150 420 -60 {lab=post}
N 520 -180 520 -20 {lab=spk}
N 560 -150 560 -40 {lab=gs}
N 660 -180 660 -80 {lab=vss}
N 700 -150 700 -40 {lab=gs}
N 800 -180 800 -40 {lab=gs}
N 840 -150 840 -60 {lab=post}
N 160 180 160 0 {lab=enw}
N 200 150 200 -100 {lab=gw}
N 300 180 300 20 {lab=ens}
N 340 150 340 -40 {lab=gs}
N 160 310 170 310 {lab=spk}
N 170 310 170 -20 {lab=spk}
N 300 310 310 310 {lab=spk}
N 310 310 310 -20 {lab=spk}
N 140 -100 380 -100 {lab=gw}
N 240 -80 1000 -80 {lab=vss}
N 1000 -80 1000 470 {lab=vss}
N -120 -60 840 -60 {lab=post}
N 340 -40 800 -40 {lab=gs}
N -120 -20 520 -20 {lab=spk}
N -120 0 160 0 {lab=enw}
N -120 20 300 20 {lab=ens}
C {lab_pin.sym} 200 280 0 1 {name=l0 sig_type=std_logic lab=bw}
C {lab_pin.sym} 340 280 0 1 {name=l1 sig_type=std_logic lab=bs}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 120 -180 0 0 {name=MPW l=0.45u w=0.3u ng=1 m=1 mm_ok=1 model=sg13_hv_pmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 260 -180 0 0 {name=MRW l=20u w=0.3u ng=1 m=1 mm_ok=1 model=sg13_hv_pmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 400 -180 0 0 {name=MSW l=100u w=0.3u ng=1 m=1 mm_ok=1 model=sg13_hv_pmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 540 -180 0 0 {name=MPS l=0.45u w=0.3u ng=1 m=1 mm_ok=1 model=sg13_hv_pmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 680 -180 0 0 {name=MRS l=20u w=0.3u ng=1 m=1 mm_ok=1 model=sg13_hv_pmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_pmos.sym} 820 -180 0 0 {name=MSS l=20u w=0.3u ng=1 m=1 mm_ok=1 model=sg13_hv_pmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 180 180 0 0 {name=MNW l=0.45u w=0.3u ng=1 m=1 mm_ok=1 model=sg13_hv_nmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 320 180 0 0 {name=MNS l=0.45u w=0.3u ng=1 m=1 mm_ok=1 model=sg13_hv_nmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 180 310 0 0 {name=MBW l=0.45u w=0.3u ng=1 m=1 mm_ok=1 model=sg13_hv_nmos spiceprefix=X}
C {sg13cmos5l_pr/sg13_hv_nmos.sym} 320 310 0 0 {name=MBS l=0.45u w=0.3u ng=1 m=1 mm_ok=1 model=sg13_hv_nmos spiceprefix=X}
C {lab_pin.sym} 140 -100 0 0 {name=l12 sig_type=std_logic lab=gw}
C {lab_pin.sym} 340 -40 0 0 {name=l13 sig_type=std_logic lab=gs}
C {iopin.sym} -120 -340 0 0 {name=p14 lab=vdd}
C {iopin.sym} -120 470 0 0 {name=p15 lab=vss}
C {iopin.sym} -120 -20 0 0 {name=p16 lab=spk}
C {iopin.sym} -120 -60 0 0 {name=p17 lab=post}
C {iopin.sym} -120 0 0 0 {name=p18 lab=enw}
C {iopin.sym} -120 20 0 0 {name=p19 lab=ens}

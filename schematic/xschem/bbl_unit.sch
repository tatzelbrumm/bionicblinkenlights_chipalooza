v {xschem version=3.4.5 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {bbl_unit: one neuron with its tuning DAC} -600 -560 0 0 0.6 0.6 {}
N 260 -80 260 -50 {lab=vdd}
N 260 50 260 80 {lab=vss}
N 400 -10 430 -10 {lab=vm}
N 400 10 430 10 {lab=out}
N 170 -10 200 -10 {lab=vin}
N -140 -110 -140 -80 {lab=vdd}
N -140 80 -140 110 {lab=vss}
N 0 -40 30 -40 {lab=vin}
N -230 -40 -200 -40 {lab=vbnl}
N -230 -20 -200 -20 {lab=b0}
N -230 0 -200 0 {lab=b1}
N -230 20 -200 20 {lab=b2}
N -230 40 -200 40 {lab=b3}
N -600 -400 -560 -400 {lab=vdd}
N -600 -375 -560 -375 {lab=vss}
N -600 -350 -560 -350 {lab=vm}
N -600 -325 -560 -325 {lab=out}
N -600 -300 -560 -300 {lab=vbnl}
N -600 -275 -560 -275 {lab=b0}
N -600 -250 -560 -250 {lab=b1}
N -600 -225 -560 -225 {lab=b2}
N -600 -200 -560 -200 {lab=b3}
C {bbl_neuron.sym} 300 0 0 0 {name=XN}
C {lab_pin.sym} 260 -80 0 1 {name=l1 sig_type=std_logic lab=vdd}
C {lab_pin.sym} 260 80 0 1 {name=l2 sig_type=std_logic lab=vss}
C {lab_pin.sym} 430 -10 0 1 {name=l3 sig_type=std_logic lab=vm}
C {lab_pin.sym} 430 10 0 1 {name=l4 sig_type=std_logic lab=out}
C {lab_pin.sym} 170 -10 0 0 {name=l5 sig_type=std_logic lab=vin}
C {bbl_dac.sym} -100 0 0 0 {name=XD}
C {lab_pin.sym} -140 -110 0 1 {name=l7 sig_type=std_logic lab=vdd}
C {lab_pin.sym} -140 110 0 1 {name=l8 sig_type=std_logic lab=vss}
C {lab_pin.sym} 30 -40 0 1 {name=l9 sig_type=std_logic lab=vin}
C {lab_pin.sym} -230 -40 0 0 {name=l10 sig_type=std_logic lab=vbnl}
C {lab_pin.sym} -230 -20 0 0 {name=l11 sig_type=std_logic lab=b0}
C {lab_pin.sym} -230 0 0 0 {name=l12 sig_type=std_logic lab=b1}
C {lab_pin.sym} -230 20 0 0 {name=l13 sig_type=std_logic lab=b2}
C {lab_pin.sym} -230 40 0 0 {name=l14 sig_type=std_logic lab=b3}
C {iopin.sym} -600 -400 0 0 {name=p15 lab=vdd}
C {lab_pin.sym} -560 -400 0 1 {name=l16 sig_type=std_logic lab=vdd}
C {iopin.sym} -600 -375 0 0 {name=p17 lab=vss}
C {lab_pin.sym} -560 -375 0 1 {name=l18 sig_type=std_logic lab=vss}
C {iopin.sym} -600 -350 0 0 {name=p19 lab=vm}
C {lab_pin.sym} -560 -350 0 1 {name=l20 sig_type=std_logic lab=vm}
C {iopin.sym} -600 -325 0 0 {name=p21 lab=out}
C {lab_pin.sym} -560 -325 0 1 {name=l22 sig_type=std_logic lab=out}
C {iopin.sym} -600 -300 0 0 {name=p23 lab=vbnl}
C {lab_pin.sym} -560 -300 0 1 {name=l24 sig_type=std_logic lab=vbnl}
C {iopin.sym} -600 -275 0 0 {name=p25 lab=b0}
C {lab_pin.sym} -560 -275 0 1 {name=l26 sig_type=std_logic lab=b0}
C {iopin.sym} -600 -250 0 0 {name=p27 lab=b1}
C {lab_pin.sym} -560 -250 0 1 {name=l28 sig_type=std_logic lab=b1}
C {iopin.sym} -600 -225 0 0 {name=p29 lab=b2}
C {lab_pin.sym} -560 -225 0 1 {name=l30 sig_type=std_logic lab=b2}
C {iopin.sym} -600 -200 0 0 {name=p31 lab=b3}
C {lab_pin.sym} -560 -200 0 1 {name=l32 sig_type=std_logic lab=b3}

import sys
from bbltb import *
case=sys.argv[1]
src=open(SRC).read()
body={'T1':"XB vdd 0 vddl 0 ena vbn vcpla vcplb bbl_bias\nXU0 vdd 0 vm0 out0 vbn d0 d1 d2 d3 bbl_unit\n",
      'T2':"XB vdd 0 vddl 0 ena vbn vcpla vcplb bbl_bias\nXU0 vdd 0 vm0 out0 vbn d0 d1 d2 d3 bbl_unit\nXL0 vdd 0 out0 bus0 bbl_inv\nCb bus0 0 1p\n",
      'T3':"Ib vdd vbn 45n\nXMB vbn vbn 0 0 sg13_hv_nmos w=2u l=2u ng=1 m=1\nXU0 vdd 0 vm0 out0 vbn d0 d1 d2 d3 bbl_unit\n",
      'T4':"Ib vdd vbn 45n\nXMB vbn vbn 0 0 sg13_hv_nmos w=2u l=2u ng=1 m=1\nXN vdd 0 vm0 out0 vin bbl_neuron\nId vin 0 9n\nXMD vin vin vdd vdd sg13_hv_pmos w=3u l=3u ng=1 m=1\n"}[case]
net=f"""* bisect {case}
{corner_libs()}
.option gmin=1e-15 reltol=1e-3 abstol=1e-14 method=gear
.include {SRC}
Vdd vdd 0 pwl 0 0 100u 3.3
Vddl vddl 0 pwl 0 0 100u 1.2
Vena ena 0 pwl 0 0 100u 0 200u 1.2
Vd0 d0 0 pwl 0 0 100u 1.2
Vd1 d1 0 pwl 0 0 100u 1.2
Vd2 d2 0 pwl 0 0 100u 1.2
Vd3 d3 0 pwl 0 0 100u 1.2
{body}"""
try:
    d=run(net,'bis_'+case,tstop=0.6,tstep='0.1m',vecs=['v(out0)','v(vm0)','i(vdd)'])
    print(case,'OK', len(spikes(d['time'],d['vout0'])),'spikes')
except Exception as e: print(case,'FAIL',e)

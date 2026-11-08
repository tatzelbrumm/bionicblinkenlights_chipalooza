# effect of rshunt=1e12 on one neuron: N0 alone at codes 0 and 15, all coupling off, with and without rshunt
from bbltb import *
import sys
code=int(sys.argv[1]); sh=sys.argv[2]
net=netlist(dig=code)
net=net.replace("rshunt=1e12", "" if sh=='no' else "rshunt=1e12").replace("method=gear","")
d=run(net,f'shck_{code}_{sh}',tstop=3 if code==0 else 0.6, tstep='0.1m')
s=summary(d,t0=0.05)
print(code, sh, 'f0=%.4f'%s[0]['f'])

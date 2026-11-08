import sys
from bbltb import *
opt=sys.argv[1]; tag=sys.argv[2]; ts=sys.argv[3]
inc=os.path.join(OUT,'bis2_C1.spice')
net=netlist(dig=15|(15<<4)|(10<<8)|(15<<12),include=inc).replace(".option gmin=1e-15 reltol=1e-3 abstol=1e-14 method=gear",opt)
try:
    d=run(net,'bis3_'+tag,tstop=0.6,tstep=ts); s=summary(d,t0=0.1); print(tag,'OK',{k:round(v['f'],2) for k,v in s.items()})
except Exception as e: print(tag,'FAIL',e)

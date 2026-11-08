import sys
from bbltb import *
opt=sys.argv[1]; tag=sys.argv[2]; ts=sys.argv[3]
net=netlist(dig=1|(2<<4)|(4<<8)|(8<<12)).replace(".option gmin=1e-15 reltol=1e-3 abstol=1e-14 method=gear", opt)
import time; t=time.time()
try:
    d=run(net,'opt3_'+tag,tstop=1.5,tstep=ts); s=summary(d,t0=0.2); print(tag,'OK',{k:round(v['f'],2) for k,v in s.items()},'%.0fs'%(time.time()-t))
except Exception as e: print(tag,'FAIL',e,'%.0fs'%(time.time()-t))

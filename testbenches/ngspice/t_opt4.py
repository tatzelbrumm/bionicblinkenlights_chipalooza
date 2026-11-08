import sys
from bbltb import *
opt=sys.argv[1]; tag=sys.argv[2]
net=netlist(dig=15|(15<<4)|(10<<8)|(15<<12)).replace(".option gmin=1e-15 reltol=1e-3 abstol=1e-14 method=gear", opt)
import time; t=time.time()
try:
    d=run(net,'opt4_'+tag,tstop=0.6,tstep='0.1m'); s=summary(d,t0=0.1); print(tag,'OK',{k:round(v['f'],2) for k,v in s.items()},'%.0fs'%(time.time()-t))
except Exception as e: print(tag,'FAIL',e,'%.0fs'%(time.time()-t))

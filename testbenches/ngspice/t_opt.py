import sys, bbltb
from bbltb import *
opt=sys.argv[1]
net=netlist(dig=0|(5<<4)|(10<<8)|(15<<12)).replace(".option gmin=1e-15 reltol=1e-3 abstol=1e-14 vntol=1e-6 method=gear maxord=2 rshunt=1e15", opt)
import time; t=time.time()
try:
    d=run(net,'opt_'+sys.argv[2],tstop=1.5); s=summary(d,t0=0.2); print(sys.argv[2],'OK',{k:round(v['f'],2) for k,v in s.items()},'%.0fs'%(time.time()-t))
except Exception as e: print(sys.argv[2],'FAIL',e,'%.0fs'%(time.time()-t))

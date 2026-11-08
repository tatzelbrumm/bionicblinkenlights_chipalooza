import sys
from bbltb import *
import simleak
tag=sys.argv[1]; cp=sys.argv[2] if sys.argv[2]!='-' else None; lk=sys.argv[3]=='1'; ts=sys.argv[4]; extra=sys.argv[5] if len(sys.argv)>5 else ''
inc=simleak.make(SRC, os.path.join(OUT,f'x_{tag}.spice'), None if lk else [], cpar=cp)
net=netlist(dig=0|(5<<4)|(10<<8)|(15<<12),include=inc).replace("method=gear","method=gear "+extra)
import time; t=time.time()
try:
    d=run(net,'x_'+tag,tstop=3,tstep=ts); s=summary(d); print(tag,'OK',{k:round(v['f'],3) for k,v in s.items()},'%.0fs'%(time.time()-t))
except Exception as e: print(tag,'FAIL',e,'%.0fs'%(time.time()-t))

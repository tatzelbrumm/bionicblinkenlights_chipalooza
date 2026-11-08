import sys
from bbltb import *
import simleak
g=sys.argv[1]
groups=None if g=='all' else [g]
inc=simleak.make(SRC, os.path.join(OUT,f'leak_{g}.spice'), groups)
try:
    d=run(netlist(dig=0|(5<<4)|(10<<8)|(15<<12),include=inc),'leak_'+g,tstop=3)
    s=summary(d); print(g,'OK',{k:round(v['f'],3) for k,v in s.items()})
except Exception as e: print(g,'FAIL',e)

import sys
from bbltb import *
case=sys.argv[1]
src=open(SRC).read()
if case=='nosyn':
    src='\n'.join(l for l in src.splitlines() if not l.startswith(('XS01','XS10')))
if case=='nogap':
    src='\n'.join(l for l in src.splitlines() if not l.startswith(('XG01','XG32')))
if case=='nocpl':
    src='\n'.join(l for l in src.splitlines() if not l.startswith(('XS01','XS10','XG01','XG32')))
if case=='noinv':
    src='\n'.join(l for l in src.splitlines() if not l.startswith(('XL0','XL1')))
inc=os.path.join(OUT,'dbg_'+case+'.spice'); open(inc,'w').write(src)
cb=(1e-15,)*4 if case=='nocap' else (3e-12,)*4
net=netlist(dig=0|(5<<4)|(10<<8)|(15<<12),cbus=cb,include=inc).replace(".option gmin=1e-15 reltol=1e-3 abstol=1e-14 vntol=1e-6 method=gear maxord=2 rshunt=1e15",".option gmin=1e-15 reltol=1e-3 abstol=1e-14")
try:
    d=run(net,'dbg_'+case,tstop=0.8); s=summary(d,t0=0.1); print(case,'OK',{k:round(v['f'],2) for k,v in s.items()})
except Exception as e: print(case,'FAIL',e)

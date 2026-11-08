import sys
from bbltb import *
case=sys.argv[1]
drop={'C0':('XS01','XS10','XG01','XG32','XMP2','XMP3'),'C1':('XG01','XG32','XMP2','XMP3'),'CA':(),
      'C2':('XS01','XS10','XG32','XMP2','XMP3'),'C3':('XS01','XS10','XG01')}[case]
src=open(SRC).read()
src='\n'.join(l for l in src.splitlines() if not l.startswith(drop))
inc=os.path.join(OUT,'bis2_'+case+'.spice'); open(inc,'w').write(src)
net=netlist(dig=15|(15<<4)|(10<<8)|(15<<12),include=inc)
try:
    d=run(net,'bis2_'+case,tstop=0.6,tstep='0.1m'); s=summary(d,t0=0.1); print(case,'OK',{k:round(v['f'],2) for k,v in s.items()})
except Exception as e: print(case,'FAIL',e)

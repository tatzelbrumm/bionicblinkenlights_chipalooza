# tuning sweep: N0..N3 at codes (0,5,10,15) in one run, buses at 3 pF
from bbltb import *
import sys
codes=[int(c) for c in sys.argv[1:5]] if len(sys.argv)>4 else [0,5,10,15]
dig=sum(c<<(4*k) for k,c in enumerate(codes))
d=run(netlist(dig=dig), 'tune_'+'_'.join(map(str,codes)), tstop=float(sys.argv[5]) if len(sys.argv)>5 else 3)
s=summary(d)
print(codes, {k:round(v['f'],3) for k,v in s.items()}, "Iavg=%.3g"%iavg(d))

from bbltb import *
import time
t=time.time()
d=run(netlist(dig=0), 'first', tstop=4)
s=summary(d)
print({k:round(v['f'],3) for k,v in s.items()}, "Iavg=%.3g"%(-np.mean(d['ivdd'][d['time']>0.5])), "t=%.0fs"%(time.time()-t))

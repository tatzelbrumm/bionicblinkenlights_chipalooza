from bbltb import *
import bbltb
inc=os.path.join(OUT,'dbg_nogap.spice')
net=netlist(dig=0|(5<<4)|(10<<8)|(15<<12),include=inc).replace(".option gmin=1e-15 reltol=1e-3 abstol=1e-14 vntol=1e-6 method=gear maxord=2 rshunt=1e15",".option gmin=1e-15 reltol=1e-3 abstol=1e-14")
vecs=bbltb.VECS+['v(x1.xs10.sw)','v(x1.xs10.ss)','v(x1.xs01.sw)','v(x1.xs01.ss)','v(x1.xu0.xn.rst)','v(x1.xu0.xn.slow)','v(x1.xu1.xn.rst)']
d=run(net,'dbg2',tstop=0.14,vecs=vecs)
t=d['time']; k=spikes(t,d['vx1out1'])[0]; print('k',k)
m=(t>k-3e-6)&(t<k+15e-6)
import numpy as np
np.set_printoptions(linewidth=250,precision=3,suppress=True)
names=['vx1out1','vx1vm1','vx1xs10sw','vx1xs10ss','vx1vm0','vx1out0','vx1xu0xnrst','vx1xs01ss']
print(names)
for i in np.where(m)[0][::max(1,np.sum(m)//40)]:
    print('%.3f'%((t[i]-k)*1e6), [round(float(d[n][i]),3) for n in names])

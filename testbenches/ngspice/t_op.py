from bbltb import *
net=netlist(dig=0)
ctl=".control\nop\nshow all\n.endc\n.end\n"
open("out/op.sp","w").write(net.replace(f".include {SRC}",f".include {SRC}")+ctl)
r=subprocess.run(['ngspice','-b','op.sp'],cwd=OUT,env=ENV,capture_output=True,text=True)
txt=r.stdout
# parse device blocks: device names and ids
blocks=re.split(r"\n\s*\n",txt)
import collections
cur={}
for line in txt.splitlines():
    pass
# simpler: use print of all voltages, then currents via savecurrents

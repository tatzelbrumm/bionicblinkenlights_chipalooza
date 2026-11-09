# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""DC I-V of the PDK analog pad (sg13cmos5l_IOPadAnalog) seen from the pad node, 27 and 60 C, typical;
writes padleak_<T>C.inc, a behavioural replacement (leakage table + 0.21 pF) for transients: the pad's
antenna diode models are "designed for reverse direction" and stop the transient solver when a bus dips
below ground at a neuron reset. usage: python3 padiv.py <outdir> (with a .spiceinit there, see buscap.py)"""
import os, subprocess, sys
outdir = sys.argv[1]
os.makedirs(outdir, exist_ok=True)
env = dict(os.environ, PDK_ROOT='/foss/pdks', PDK='ihp-sg13cmos5l')
for temp in (27, 60):
    net = f"""* pad I-V
.lib cornerMOShv.lib mos_tt
.lib cornerMOSlv.lib mos_tt
.lib cornerRES.lib res_typ
.lib cornerDIO.lib dio_tt
.include /foss/pdks/ihp-sg13cmos5l/libs.ref/sg13cmos5l_io/spice/sg13cmos5l_io.spice
.option gmin=1e-15 abstol=1e-16 reltol=1e-4
.temp {temp}
Vavdd avdd 0 3.3
Vdvdd dvdd 0 1.2
X1 x padres dvdd 0 avdd 0 sg13cmos5l_IOPadAnalog
Vx x 0 dc 0
.control
dc Vx 0 3.3 0.1
let ileak = -i(Vx)
wrdata padiv_{temp}C.dat ileak
.endc
.end
"""
    open(os.path.join(outdir, f'padiv_{temp}C.sp'), 'w').write(net)
    subprocess.run(['ngspice', '-b', f'padiv_{temp}C.sp'], cwd=outdir, env=env, capture_output=True, text=True)
    rows = [tuple(map(float, l.split()[:2])) for l in open(os.path.join(outdir, f'padiv_{temp}C.dat'))
            if l.strip() and not l.lstrip()[0].isalpha()]
    print(f'{temp} C: ' + ', '.join(f'{v:.1f} V {i * 1e12:.0f} pA' for v, i in rows[::3]))
    tab = ', '.join(f'{v:.2f}, {i:.4e}' for v, i in rows)
    open(os.path.join(outdir, f'padleak_{temp}C.inc'), 'w').write(
        f"* leakage of the PDK analog pad at {temp} C (from padiv.py): current from the node to ground\n"
        f".subckt padleak x\nBleak x 0 I = pwl(V(x), -0.5, -1e-6, {tab})\nCpad x 0 0.21p\n.ends\n")

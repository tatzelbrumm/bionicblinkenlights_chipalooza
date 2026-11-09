# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Capacitance and leakage of what a slot's analog bus sees in the harness: the harness's own extracted
bus switch (analog_switch_med, from the harness repository's netlist/layout/chipalooza_frame.spice, read
only) and the PDK analog pad (sg13cmos5l_IOPadAnalog).

usage: python3 buscap.py <harness>/netlist/layout/chipalooza_frame.spice <outdir> [case ...]

Per node: C = Im(I) / (2 pi f) at 1 kHz with 1 V AC, at DC bias 0.3 / 0.8 / 1.5 V; leakage = DC current
from the node into the device under test (positive: the device pulls the node down; negative: it pushes
current into the node), at 27 and 60 C. Typical corner.

Topology (harness verilog/rtl/chipalooza_frame.v): each slot's analog_bus<k> pin goes through its own
analog_switch_med to user_analog_shared[k], which is the chip's analog pin k; 18 slots share it."""
import os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
harness_net, outdir = sys.argv[1], sys.argv[2]
os.makedirs(outdir, exist_ok=True)
PDK = '/foss/pdks/ihp-sg13cmos5l'
text = open(harness_net).read()
subs = {m.group(1): m.group(0) for m in re.finditer(r'(?ms)^\.subckt (\S+).*?^\.ends', text)}

def deps(name, seen):
    if name in seen or name not in subs:
        return
    seen.append(name)
    for line in re.sub(r'\n\+', ' ', subs[name]).splitlines():
        if line.startswith('X'):
            toks = [t for t in line.split() if '=' not in t]
            deps(toks[-1], seen)

sw = []
deps('analog_switch_med', sw)
open(os.path.join(outdir, 'switch.spice'), 'w').write('\n\n'.join(subs[n] for n in reversed(sw)) + '\n')
open(os.path.join(outdir, '.spiceinit'), 'w').write(open(os.path.join(HERE, '..', 'ngspice', '.spiceinit')).read())

HEAD = """* harness bus node: {title}
.lib cornerMOShv.lib mos_tt
.lib cornerMOSlv.lib mos_tt
.lib cornerRES.lib res_typ
.lib cornerDIO.lib dio_tt
.include switch.spice
.include {pdk}/libs.ref/sg13cmos5l_io/spice/sg13cmos5l_io.spice
.option gmin=1e-15 abstol=1e-16 reltol=1e-4
.temp {temp}
Vavdd avdd 0 3.3
Vdvdd dvdd 0 1.2
Venable enable 0 {ena}
Vin in 0 dc {vin}
"""
CASES = {
    # node under test is 'x'
    'switch_out_off': ('X1 in enable avdd x 0 dvdd 0 analog_switch_med', 0.0, 'slot side of an open switch'),
    'switch_in_off': ('X1 x enable avdd out 0 dvdd 0 analog_switch_med\nVout out 0 dc 0.8', 0.0,
                      'shared side of an open switch (other slot side at 0.8 V)'),
    'switch_on': ('X1 x enable avdd out 0 dvdd 0 analog_switch_med', 1.2,
                  'closed switch, both sides (other side floating on it)'),
    'pad': ('X1 x padres dvdd 0 avdd 0 sg13cmos5l_IOPadAnalog', 0.0, 'analog pad (ESD clamps and diodes)'),
    'pad_clamps': ('XI0 avdd 0 x sg13cmos5l_Clamp_P20N0D\nXI4 0 x sg13cmos5l_Clamp_N20N0D', 0.0,
                   'the two clamp transistors of the analog pad only'),
}
if len(sys.argv) > 3:
    CASES = {k: CASES[k] for k in sys.argv[3:]}

env = dict(os.environ, PDK_ROOT='/foss/pdks', PDK='ihp-sg13cmos5l')
for name, (dut, ena, title) in CASES.items():
    for temp in (27, 60):
        for v in (0.3, 0.8, 1.5):
            tag = f'{name}_{temp}C_{v}'
            net = HEAD.format(title=title, pdk=PDK, temp=temp, ena=ena, vin=0.8) + dut + \
                f"\nVx x 0 dc {v} ac 1\n.control\nop\nlet ileak = -i(Vx)\nprint ileak\nac lin 1 1k 1k\n" \
                f"let c = imag(-i(Vx)) / (2 * pi * 1k)\nprint c\n.endc\n.end\n"
            open(os.path.join(outdir, tag + '.sp'), 'w').write(net)
            r = subprocess.run(['ngspice', '-b', tag + '.sp'], cwd=outdir, env=env, capture_output=True, text=True)
            open(os.path.join(outdir, tag + '.log'), 'w').write(r.stdout + r.stderr)
            il = re.search(r'ileak = ([-\d.e+]+)', r.stdout)
            c = re.search(r'^c = ([-\d.e+]+)', r.stdout, re.M)
            print(f'{name:16s} {temp:3d} C  V = {v:.1f}  C = {float(c.group(1)) * 1e12 if c else float("nan"):7.3f} pF'
                  f'  I_leak = {float(il.group(1)) * 1e12 if il else float("nan"):10.3f} pA', flush=True)

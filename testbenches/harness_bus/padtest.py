# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""N2, N3 with the PDK analog pad's leakage (table from padiv.py, the model as it is) and capacitance on
their buses, i.e. with the harness bus switch closed; schematic netlist, 2.5 s each.

usage: python3 padtest.py <padiv outdir> <out.json> [case ...]"""
import os, sys, json
from multiprocessing import Pool
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ngspice'))
import bbltb

INC = os.path.join(os.path.abspath(sys.argv[1]), 'padleak_{t}C.inc')

def dig(t0=0, t1=0, t2=0, t3=0):
    return t0 | (t1 << 4) | (t2 << 8) | (t3 << 12)

# (name, N2/N3 code, bus capacitance, pad leakage, temperature)
CASES = [('leak_c6_3p', 6, 3e-12, True, 27), ('leak_c10_3p', 10, 3e-12, True, 27),
         ('leak_c15_3p', 15, 3e-12, True, 27), ('leak_c15_10p', 15, 10e-12, True, 27),
         ('leak_c15_10p_ref', 15, 10e-12, False, 27), ('leak_c15_3p_60C', 15, 3e-12, True, 60)]

def one(c):
    name, code, cb, leak, temp = c
    extra = (f".include {INC.format(t=temp)}\nXl2 busx2 padleak\nXl3 busx3 padleak\n") if leak else ''
    net = bbltb.netlist(dig=dig(6, 6, code, code), cbus=(3e-12, 3e-12, cb, cb), temp=temp, extra=extra)
    try:
        d = bbltb.run(net, name, tstop=2.5)
    except RuntimeError as e:
        print(json.dumps({'case': name, 'error': str(e)}), flush=True)
        return {'case': name, 'error': str(e)}
    t = d['time']
    out = {'case': name, 'code': code, 'cbus': cb, 'leak': leak, 'temp': temp}
    for k in (2, 3):
        sp = bbltb.spikes(t, d[f'vx1out{k}'])
        vm = d[f'vx1vm{k}'][t > 0.5]
        out[f'N{k}'] = dict(rate=bbltb.rate(sp, 0.5), n_spikes=int(len(sp)), vm_min=float(vm.min()),
                           vm_max=float(vm.max()), vm_end=float(vm[-1]))
    print(json.dumps(out), flush=True)
    return out

if __name__ == '__main__':
    if len(sys.argv) > 3:
        CASES = [c for c in CASES if c[0] in sys.argv[3:]]
    with Pool(len(CASES)) as p:
        res = p.map(one, CASES)
    json.dump(res, open(sys.argv[2], 'w'), indent=1)

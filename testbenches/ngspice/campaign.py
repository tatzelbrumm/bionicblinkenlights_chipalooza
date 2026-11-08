# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Simulation campaign for the Bionic Blinkenlights core (schematic or extracted netlist).

usage: python3 campaign.py [--include <netlist>] [--tag <name>] [--jobs N] [case ...]
Each case is one transient of the whole core (four neurons); results go to out/<tag>/<case>.json
and the waveforms to out/<tag>/<case>.dat. plots.py draws the figures from them.

dig_in bits: N0 tune 3:0, N1 7:4, N2 11:8, N3 15:12; synapse N0->N1 16 (weak) 17 (strong),
N1->N0 18, 19; gap junction N0<->N1 20, 21; N3 -> analog_bus2 22, 23.
"""
import os, sys, json, argparse
from multiprocessing import Pool
import numpy as np
import bbltb
from bbltb import netlist, run, summary, phase_locking, iavg, SRC

def dig(t0=0, t1=0, t2=0, t3=0, bits=()):
    return t0 | (t1 << 4) | (t2 << 8) | (t3 << 12) | sum(1 << b for b in bits)

C3 = 3e-12        # analog bus line on chip + pad, no external load (estimate, see README)
CASES = {}
# 1. tuning: all four neurons, four codes per run (N2, N3 on their 3 pF buses)
for codes in [(0, 1, 2, 3), (4, 5, 6, 7), (8, 9, 10, 11), (12, 13, 14, 15)]:
    CASES['tune_' + '_'.join(map(str, codes))] = dict(dig=dig(*codes), tstop=2.5)
# 2. bus load: N2 and N3 at code 6, external load added to analog_bus2 / analog_bus3
for c in [0, 10e-12, 30e-12, 100e-12]:
    CASES[f'busload_{int(round(c * 1e12))}p'] = dict(dig=dig(6, 6, 6, 6), cbus=(C3, C3, C3 + c, C3 + c), tstop=2.5)
# 3. analog coupling to the bus: vcplb swept with 30 pF on the buses
for v in [0.0, 0.8, 1.2, 3.3]:
    CASES[f'vcplb_{v:.1f}'] = dict(dig=dig(6, 6, 6, 6), cbus=(C3, C3, C3 + 30e-12, C3 + 30e-12), vcplb=v, tstop=2.5)
# 4. demo img11: N0 fast, N1 slow, excitatory synapse N0 -> N1 at four weights
for name, bits in [('none', ()), ('weak', (16,)), ('strong', (17,)), ('both', (16, 17))]:
    CASES[f'syn01_{name}'] = dict(dig=dig(9, 1, 0, 0, bits), tstop=2.5)
# 5. demo img12: mutual excitation, N0 and N1 slow and detuned
for name, bits in [('none', ()), ('mutual_weak', (16, 18)), ('mutual_strong', (17, 19))]:
    CASES[f'mutual_{name}'] = dict(dig=dig(3, 1, 0, 0, bits), tstop=4.0)
# 6. gap junction N0 <-> N1: detuned pair (codes 5 and 7), digital legs and analog vcpla
for name, bits, v in [('off', (), None), ('weak', (20,), None), ('strong', (21,), None), ('both', (20, 21), None),
                      ('both_v0.6', (20, 21), 0.6), ('both_v0.9', (20, 21), 0.9)]:
    CASES[f'gap_{name}'] = dict(dig=dig(5, 7, 0, 0, bits), vcpla=v, tstop=2.5)
# 7. N2 and N3 coupled through analog_bus2 (detuned, codes 5 and 7), with and without bus load
for name, bits, c in [('off', (), 0), ('weak', (22,), 0), ('strong', (23,), 0), ('strong_30p', (23,), 30e-12)]:
    CASES[f'bus23_{name}'] = dict(dig=dig(0, 0, 5, 7, bits), cbus=(C3, C3, C3 + c, C3), tstop=2.5)


def one(args):
    name, case, include, tag = args
    outdir = os.path.join(bbltb.OUT, tag)
    os.makedirs(outdir, exist_ok=True)
    kw = {k: v for k, v in case.items() if k in ('dig', 'cbus', 'vcpla', 'vcplb')}
    net = netlist(include=include, **kw)
    res = dict(case=name, **{k: (list(v) if isinstance(v, tuple) else v) for k, v in case.items()})
    try:
        d = run(net, os.path.join(tag, name), tstop=case['tstop'])
        s = summary(d, t0=0.3)
        res['f'] = [float(s[k]['f']) for k in range(4)]
        res['spikes'] = [list(map(float, s[k]['spikes'])) for k in range(4)]
        res['iavg'] = float(iavg(d, 0.3))
        p01 = phase_locking(s[0]['spikes'], s[1]['spikes'], 0.3)
        p23 = phase_locking(s[2]['spikes'], s[3]['spikes'], 0.3)
        res['lock01'] = dict(ratio=float(p01['ratio']), vs=float(p01['vs']))
        res['lock23'] = dict(ratio=float(p23['ratio']), vs=float(p23['vs']))
        res['ok'] = True
    except Exception as e:
        res['ok'] = False
        res['error'] = str(e)
    json.dump(res, open(os.path.join(outdir, name + '.json'), 'w'), indent=1)
    print(name, 'ok' if res['ok'] else 'FAIL', res.get('f'), res.get('error', ''), flush=True)
    return res


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--include', default=SRC)
    ap.add_argument('--tag', default='sch')
    ap.add_argument('--jobs', type=int, default=3)
    ap.add_argument('cases', nargs='*')
    a = ap.parse_args()
    names = a.cases or list(CASES)
    with Pool(a.jobs) as p:
        p.map(one, [(n, CASES[n], a.include, a.tag) for n in names], chunksize=1)

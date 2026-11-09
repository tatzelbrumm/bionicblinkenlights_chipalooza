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
CB3 = 10e-9       # N3 (bbl_neuron_hi, nA) in the system cases: 10 nF on analog_bus3 = blinking mode
CBUS = (C3, C3, C3, CB3)
PAD = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'harness_bus', 'padleak_27C.inc')
CASES = {}
# 1. tuning: all four neurons, four codes per run (N2 on its 3 pF bus, N3 on 10 nF)
for codes in [(0, 1, 2, 3), (4, 5, 6, 7), (8, 9, 10, 11), (12, 13, 14, 15)]:
    CASES['tune_' + '_'.join(map(str, codes))] = dict(dig=dig(*codes), cbus=CBUS, tstop=2.5)
CASES['tune_low'] = dict(dig=dig(0, 0, 0, 0), cbus=CBUS, tstop=5.0)
# 2. bus load: N2 at code 6, external load added to analog_bus2 (N3: cases n3_busload_*)
for c in [0, 10e-12, 30e-12, 100e-12]:
    CASES[f'busload_{int(round(c * 1e12))}p'] = dict(dig=dig(6, 6, 6, 6), cbus=(C3, C3, C3 + c, CB3), tstop=2.5)
# 3. analog coupling to the bus: vcplb swept with 30 pF on analog_bus2 (N3 at code 0, 10 nF: with vcplb
#    low it runs on its own membrane at about 0.5 kHz)
for v in [0.0, 0.8, 1.2, 3.3]:
    CASES[f'vcplb_{v:.1f}'] = dict(dig=dig(6, 6, 6, 0), cbus=(C3, C3, C3 + 30e-12, CB3), vcplb=v, tstop=2.5)
# 4. demo img11: N0 fast, N1 slow, excitatory synapse N0 -> N1 at four weights
for name, bits in [('none', ()), ('weak', (16,)), ('strong', (17,)), ('both', (16, 17))]:
    CASES[f'syn01_{name}'] = dict(dig=dig(9, 1, 0, 0, bits), cbus=CBUS, tstop=2.5)
# 5. demo img12: mutual excitation, N0 and N1 slow and detuned
for name, bits in [('none', ()), ('mutual_weak', (16, 18)), ('mutual_strong', (17, 19))]:
    CASES[f'mutual_{name}'] = dict(dig=dig(3, 1, 0, 0, bits), cbus=CBUS, tstop=4.0)
# 6. gap junction N0 <-> N1: detuned pair (codes 5 and 7), digital legs and analog vcpla
for name, bits, v in [('off', (), None), ('weak', (20,), None), ('strong', (21,), None), ('both', (20, 21), None),
                      ('both_v0.3', (20, 21), 0.3), ('both_v0.4', (20, 21), 0.4), ('both_v0.5', (20, 21), 0.5),
                      ('both_v0.6', (20, 21), 0.6), ('both_v0.9', (20, 21), 0.9)]:
    CASES[f'gap_{name}'] = dict(dig=dig(5, 7, 0, 0, bits), cbus=CBUS, vcpla=v, tstop=2.5)
# 7. N3 (blinking, 10 nF) coupled to analog_bus2 and through it N2, with and without load on bus2
for name, bits, c in [('off', (), 0), ('weak', (22,), 0), ('strong', (23,), 0), ('strong_30p', (23,), 30e-12)]:
    CASES[f'bus23_{name}'] = dict(dig=dig(0, 0, 5, 7, bits), cbus=(C3, C3, C3 + c, CB3), tstop=2.5)
# 8. N3 alone (bbl_neuron_hi): audio rates on the bare bus, blinking with an external capacitor, leakage.
#    Short runs; t0 = start of the analysis.
for code in (0, 3, 6, 9, 12, 15):
    CASES[f'n3_tune_{code}'] = dict(dig=dig(6, 6, 6, code), tstop=0.02, tstep='1u', t0=0.004)
for c, tstop, tstep, t0 in [(0, 0.02, '1u', 0.004), (10e-12, 0.02, '1u', 0.004), (30e-12, 0.02, '1u', 0.004),
                            (100e-12, 0.03, '1u', 0.005), (1e-9, 0.3, '10u', 0.05), (10e-9, 2.0, '10u', 0.3),
                            (100e-9, 12.0, '50u', 2.0)]:
    lab = f'{c * 1e12:g}p' if c < 1e-9 else f'{c * 1e9:g}n'
    CASES[f'n3_busload_{lab}'] = dict(dig=dig(6, 6, 6, 6), cbus=(C3, C3, C3, C3 + c), tstop=tstop, tstep=tstep, t0=t0)
for code, tstop, tstep in [(0, 6.0, '20u'), (15, 1.0, '10u')]:
    CASES[f'n3_blink_{code}'] = dict(dig=dig(6, 6, 6, code), cbus=CBUS, tstop=tstop, tstep=tstep, t0=0.3)
for code in (0, 15):     # the PDK pad model's leakage on analog_bus3 (20 pF: bus switch closed, see harness_bus)
    CASES[f'n3_pad_{code}'] = dict(dig=dig(6, 6, 6, code), cbus=(C3, C3, C3, 20e-12), pad=True, tstop=0.02,
                                   tstep='1u', t0=0.004)
CASES['n3_pad_blink_6'] = dict(dig=dig(6, 6, 6, 6), cbus=CBUS, pad=True, tstop=2.0, t0=0.3)


# post-layout subset (extracted netlist), run with --tstop 1.5 (applies to the system cases only)
PEX_CASES = ['tune_0_1_2_3', 'tune_4_5_6_7', 'tune_8_9_10_11', 'tune_12_13_14_15', 'busload_0p', 'busload_10p',
             'busload_30p', 'busload_100p', 'syn01_both', 'gap_off', 'gap_both', 'bus23_off', 'bus23_strong',
             'n3_tune_0', 'n3_tune_6', 'n3_tune_15', 'n3_busload_0p', 'n3_busload_100p', 'n3_busload_1n',
             'n3_blink_15', 'n3_pad_0']


def one(args):
    name, case, include, tag, reuse = args
    outdir = os.path.join(bbltb.OUT, tag)
    os.makedirs(outdir, exist_ok=True)
    kw = {k: v for k, v in case.items() if k in ('dig', 'cbus', 'vcpla', 'vcplb')}
    pex = include.endswith('.pex.spice')
    if pex:
        cell = os.path.basename(include).split('.')[0]
        kw['dut'] = bbltb.slot_dut(include, cell)
    if case.get('pad'):
        kw['extra'] = f".include {PAD}\nXl3 busx3 padleak\n"
    net = netlist(include=include, **kw)
    res = dict(case=name, **{k: (list(v) if isinstance(v, tuple) else v) for k, v in case.items()})
    t0 = case.get('t0', 0.3)
    try:
        if reuse:    # --reanalyze: the saved waveforms of an earlier run
            d = np.genfromtxt(os.path.join(outdir, name + '.dat'), names=True)
        else:
            d = run(net, os.path.join(tag, name), tstop=case['tstop'], tstep=case.get('tstep', '10u'),
                    vecs=bbltb.BUSVECS if pex else bbltb.VECS + ['v(busx0)'])
        s = bbltb.summary_bus(d, t0=t0) if pex else summary(d, t0=t0)
        sb = bbltb.summary_bus(d, t0=t0)
        res['f_bus'] = [float(sb[k]['f']) for k in range(4)]
        res['f'] = [float(s[k]['f']) for k in range(4)]
        res['spikes'] = [list(map(float, s[k]['spikes'])) for k in range(4)]
        res['iavg'] = float(iavg(d, t0))
        res['bus3_range'] = [float(d['vbus3'][d['time'] > t0].min()), float(d['vbus3'][d['time'] > t0].max())]
        p01 = phase_locking(s[0]['spikes'], s[1]['spikes'], t0)
        p23 = phase_locking(s[2]['spikes'], s[3]['spikes'], t0)
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
    ap.add_argument('--tstop', type=float, default=None)
    ap.add_argument('--reanalyze', action='store_true',
                    help='recompute the results from the saved waveforms out/<tag>/<case>.dat, no simulation')
    a = ap.parse_args()
    names = a.cases or list(CASES)
    if a.tstop:      # shortens or lengthens the system cases; the n3_* cases keep their own
        for n in names:
            if not n.startswith('n3_'):
                CASES[n] = dict(CASES[n], tstop=a.tstop)
    with Pool(a.jobs) as p:
        p.map(one, [(n, CASES[n], a.include, a.tag, a.reanalyze) for n in names], chunksize=1)

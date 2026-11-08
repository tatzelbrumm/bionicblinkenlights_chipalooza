# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Round-trip check of the xschem sheets: netlist every sheet with xschem as a .subckt and compare it
device by device with the source netlist (model, terminal nets in order, w/l/ng/m, port order).
usage: python3 check_sheets.py [sheet ...]     exit status = number of mismatching sheets"""
import os, re, subprocess, sys, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from gen_sheets import parse_netlist, subs

def xschem_netlist(cell, outdir):
    os.makedirs(outdir, exist_ok=True)
    out = os.path.join(outdir, cell + '.spice')
    if os.path.exists(out):
        os.remove(out)
    env = dict(os.environ, PWD=HERE, PDK_ROOT=os.environ.get('PDK_ROOT', '/foss/pdks'), PDK='ihp-sg13cmos5l')
    r = subprocess.run(['xschem', '--rcfile', os.path.join(HERE, 'xschemrc'), '-n', '-s', '-q', '-x', '--no_x',
                        '--tcl', 'set top_is_subckt 1', '-o', outdir, os.path.join(HERE, cell + '.sch')],
                       cwd=HERE, env=env, capture_output=True, text=True, timeout=120)
    return out, r.returncode, (r.stdout + r.stderr)

def norm(v):
    m = re.match(r'^([0-9.eE+-]+)\s*([munpf]?)u?$', v)
    if not m:
        return v
    mult = dict(m=1e-3, u=1e-6, n=1e-9, p=1e-12, f=1e-15).get(m.group(2), 1.0)
    x = float(m.group(1)) * mult
    if v.endswith('u') and not m.group(2):
        x *= 1e-6
    return f'{x:.6g}'

def compare(cell, path):
    if not os.path.exists(path):
        return [f'{cell}: no netlist written']
    txt = open(path).read()
    errs = []
    if 'IS MISSING' in txt:
        errs.append(f'{cell}: missing symbol(s)')
    got = parse_netlist([path]).get(cell)
    if got is None:
        return errs + [f'{cell}: no .subckt {cell} in the xschem netlist']
    ref = subs[cell]
    if got['ports'] != ref['ports']:
        errs.append(f"{cell}: port order {got['ports']} != {ref['ports']}")
    g = {i['name'].upper(): i for i in got['insts']}
    r = {i['name'].upper(): i for i in ref['insts']}
    for n in sorted(set(g) | set(r)):
        if n not in g:
            errs.append(f'{cell}: {n} missing in the sheet'); continue
        if n not in r:
            errs.append(f'{cell}: {n} only in the sheet'); continue
        a, b = g[n], r[n]
        if a['model'] != b['model']:
            errs.append(f"{cell}: {n} model {a['model']} != {b['model']}")
        if [x.lower() for x in a['nodes']] != [x.lower() for x in b['nodes']]:
            errs.append(f"{cell}: {n} nodes {a['nodes']} != {b['nodes']}")
        for k in ('w', 'l', 'ng', 'm', 'b'):
            if k in b['params'] and norm(a['params'].get(k, '1' if k in ('ng', 'm') else '?')) != norm(b['params'][k]):
                errs.append(f"{cell}: {n} {k}={a['params'].get(k)} != {b['params'][k]}")
    return errs

if __name__ == '__main__':
    cells = sys.argv[1:] or ['bbl_neuron', 'bbl_dac', 'bbl_unit', 'bbl_inv', 'bbl_syn', 'bbl_gap', 'bbl_bias',
                             'bbl_core', 'bbl_tielo', 'bbl_slot_shared', 'bbl_slot_pads']
    outdir = os.path.join(HERE, 'netlist_check')
    bad = 0
    for c in cells:
        p, rc, log = xschem_netlist(c, outdir)
        e = compare(c, p)
        print(f"{c}: {'OK' if not e else 'MISMATCH'} ({len(subs[c]['insts'])} devices/instances, xschem exit {rc})")
        for x in e[:12]:
            print('   ', x)
        bad += bool(e)
    print('sheets with mismatches:', bad)
    sys.exit(bad)

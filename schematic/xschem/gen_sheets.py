# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Generate the xschem sheets (.sch) and symbols (.sym) of Bionic Blinkenlights from the source netlist.

Style (skill xschem-analog-schematic, Christoph Maier's conventions): supply and ground are wires across
the top and the bottom; PMOS row under vdd, NMOS row(s) over vss, every source and bulk on a rail is
wired to it; every other net is a horizontal track in the channel between the rows with vertical drops
from its pins; ports in one column on the left at the height of their track. Hierarchical sheets place
symbols and connect them with short label stubs.  The netlist is the source of truth: check_sheets.py
netlists every sheet with xschem and compares it device by device with netlist/source/*.spice.
usage: python3 gen_sheets.py
"""
import os, re
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..'))
PDKSYM = '/foss/pdks/ihp-sg13cmos5l/libs.tech/xschem/sg13cmos5l_pr'

# --------------------------------------------------------------------------------------------- netlist
def parse_netlist(paths):
    subs, cur = {}, None
    for p in paths:
        lines = []
        for raw in open(p):
            raw = raw.rstrip('\n')
            if raw.startswith('+') and lines:
                lines[-1] += ' ' + raw[1:]
            else:
                lines.append(raw)
        for l in lines:
            t = l.split()
            if not t or t[0].startswith('*'):
                continue
            if t[0].lower() == '.subckt':
                cur = dict(name=t[1], ports=t[2:], insts=[])
                subs[t[1]] = cur
            elif t[0].lower() == '.ends':
                cur = None
            elif cur is not None and t[0][0] in 'Xx':
                params = dict(w.split('=', 1) for w in t[1:] if '=' in w)
                nodes = [w for w in t[1:] if '=' not in w]
                cur['insts'].append(dict(name=t[0], nodes=nodes[:-1], model=nodes[-1], params=params))
    return subs

# ------------------------------------------------------------------------------------------ geometry
MOSPINS = {'nmos': dict(D=(20, -30), G=(-20, 0), S=(20, 30), B=(20, 0)),
           'pmos': dict(S=(20, -30), G=(-20, 0), D=(20, 30), B=(20, 0))}
RESPINS = dict(P=(0, -30), M=(0, 30))
MODEL_SYM = {'sg13_hv_nmos': ('sg13cmos5l_pr/sg13_hv_nmos.sym', 'nmos'),
             'sg13_hv_pmos': ('sg13cmos5l_pr/sg13_hv_pmos.sym', 'pmos'),
             'sg13_lv_nmos': ('sg13cmos5l_pr/sg13_lv_nmos.sym', 'nmos'),
             'sg13_lv_pmos': ('sg13cmos5l_pr/sg13_lv_pmos.sym', 'pmos')}


class Sheet:
    def __init__(self, name, title):
        self.name, self.title = name, title
        self.lines = []
        self.wires = []
        self.texts = []

    def C(self, sym, x, y, rot=0, flip=0, props=''):
        self.lines.append(f'C {{{sym}}} {x} {y} {rot} {flip} {{{props}}}')

    def N(self, x1, y1, x2, y2, lab=''):
        if (x1, y1) == (x2, y2):
            return
        self.wires.append((x1, y1, x2, y2, lab))

    def vfree(self, x, y0, y1, net):
        a, b = min(y0, y1), max(y0, y1)
        for (x1, y1_, x2, y2, l) in self.wires:
            if l == net:
                continue
            if x1 == x2 == x and not (max(y1_, y2) < a or min(y1_, y2) > b):
                return False
            # a horizontal wire of another net whose end lies on this vertical
            if y1_ == y2 and a <= y1_ <= b and x in (x1, x2):
                return False
        return True

    def vroute(self, net, px, py, y_to, x0, step=10):
        """Vertical from pin (px, py) to y_to: straight down/up if free, else a short jog to the first free
        x to the right of x0."""
        if x0 == px and self.vfree(px, py, y_to, net):
            self.N(px, py, px, y_to, net)
            return px
        x = max(x0, px + 10)
        while not self.vfree(x, py, y_to, net) or not self.hfree(px, x, py, net):
            x += step
        self.N(px, py, x, py, net)
        self.N(x, py, x, y_to, net)
        return x

    def hfree(self, xa, xb, y, net):
        a, b = min(xa, xb), max(xa, xb)
        for (x1, y1_, x2, y2, l) in self.wires:
            if l == net:
                continue
            if x1 == x2 and a <= x1 <= b and min(y1_, y2) <= y <= max(y1_, y2) and (x1 in (a, b) or y in (y1_, y2)):
                return False
            if y1_ == y2 == y and not (max(x1, x2) < a or min(x1, x2) > b):
                return False
        return True

    def lab(self, x, y, net, flip=0):
        self.C('lab_pin.sym', x, y, 0, flip, f'name=l{len(self.lines)} sig_type=std_logic lab={net}')

    def port(self, kind, x, y, net):
        self.C(f'{kind}.sym', x, y, 0, 0, f'name=p{len(self.lines)} lab={net}')

    def text(self, x, y, s, size=0.4):
        self.texts.append(f'T {{{s}}} {x} {y} 0 0 {size} {size} {{}}')

    def save(self, path):
        out = ['v {xschem version=3.4.5 file_version=1.2}', 'G {}', 'K {}', 'V {}', 'S {}', 'E {}']
        out += self.texts
        out += [f'N {a} {b} {c} {d} {{lab={l}}}' for a, b, c, d, l in self.wires]
        out += self.lines
        open(path, 'w').write('\n'.join(out) + '\n')


def mos_pins(kind, x, y, flip=0):
    return {k: (x + (-dx if flip else dx), y + dy) for k, (dx, dy) in MOSPINS[kind].items()}


def leaf_sheet(sub, rows, title, rails=('vdd', 'vss'), pitch=140, notes=()):
    """Draw a transistor-level sheet. rows: list of lists of instance names; rows[0] is the PMOS row
    (under vdd), the last row(s) NMOS (over vss); devices listed per row left to right."""
    S = Sheet(sub['name'], title)
    vdd, vss = rails
    inst = {i['name']: i for i in sub['insts']}
    ports = sub['ports']
    XP = -120                         # port column
    YV, YS = -420, 420                # rails
    nn = len({n for i in sub['insts'] for n in i['nodes']}) + 2
    half = max(120, 10 * nn + 60)
    rowy = {0: -half}
    nrows = len(rows)
    for r in range(1, nrows):
        rowy[r] = half + 130 * (r - 1)
    YV = rowy[0] - 160
    YS = rowy[nrows - 1] + 160
    placed = {}
    col_of = {}
    for r, names in enumerate(rows):
        x = 120 + (60 if r > 0 else 0)
        for nm in names:
            if nm is not None:
                i = inst[nm]
                sym, kind = MODEL_SYM.get(i['model'], (None, None))
                placed[nm] = ('res' if sym is None else kind, x, rowy[r], i, r)
                col_of[(r, x)] = nm
            x += pitch
    xmax = max(p[1] for p in placed.values()) + 120
    S.N(XP, YV, xmax + 80, YV, vdd)
    S.N(XP, YS, xmax + 80, YS, vss)
    pend = []          # (net, x, y_pin, direction)

    def pins_of(nm):
        kind, x, y, i, r = placed[nm]
        if kind == 'res':
            return {'top': (x, y - 30), 'bot': (x, y + 30)}, {'top': i['nodes'][0], 'bot': i['nodes'][1]}
        pins = mos_pins(kind, x, y)
        D, G, Sn, B = i['nodes']
        if kind == 'pmos':
            return {'top': pins['S'], 'bot': pins['D']}, {'top': Sn, 'bot': D}
        return {'top': pins['D'], 'bot': pins['S']}, {'top': D, 'bot': Sn}

    stacked_top = set()     # lower devices whose top pin is wired straight to the device above
    stacked_bot = set()     # upper devices whose bottom pin is wired straight to the device below
    for nm, (kind, x, y, i, r) in placed.items():
        if r >= 2 and (r - 1, x) in col_of:
            up = col_of[(r - 1, x)]
            upins, unets = pins_of(up)
            lpins, lnets = pins_of(nm)
            if unets['bot'] == lnets['top'] and unets['bot'] not in (vdd, vss):
                (ux, uy), (lx, ly) = upins['bot'], lpins['top']
                S.N(ux, uy, ux, ly, lnets['top'])
                S.N(ux, ly, lx, ly, lnets['top'])
                S.lab(ux, ly, lnets['top'], 1)
                stacked_top.add(nm)
                # the net still reaches the channel through the upper device's bottom pin if it has
                # other connections
                others = [1 for j in sub['insts'] if lnets['top'] in j['nodes'] and j['name'] not in (nm, up)]
                if not others and lnets['top'] not in ports:
                    stacked_bot.add(up)
    for nm, (kind, x, y, i, r) in placed.items():
        low = r >= 2
        pins_tb, nets_tb = pins_of(nm)
        if kind == 'res':
            S.C('sg13cmos5l_pr/rhigh.sym', x, y, 0, 0,
                f"name={i['name'][1:]} w={i['params']['w']} l={i['params']['l']} model=rhigh body={i['nodes'][2]} "
                f"spiceprefix=X b={i['params'].get('b', 0)} m={i['params'].get('m', 1)} mm_ok=1")
        else:
            p = i['params']
            S.C(MODEL_SYM[i['model']][0], x, y, 0, 0,
                f"name={i['name'][1:]} l={p['l']} w={p['w']} ng={p.get('ng', 1)} m={p.get('m', 1)} "
                f"mm_ok=1 model={i['model']} spiceprefix=X")
            pins = mos_pins(kind, x, y)
            B = i['nodes'][3]
            bx, by = pins['B']
            rail_b = YV if (kind == 'pmos' and B == vdd) else (YS if (kind == 'nmos' and B == vss) else None)
            if rail_b is not None:
                S.N(bx, by, bx + 20, by, B)
                S.N(bx + 20, by, bx + 20, rail_b, B)
            else:
                S.N(bx, by, bx + 30, by, B)
                S.lab(bx + 30, by, B, 1)
            gx, gy = pins['G']
            pend.append((i['nodes'][1], gx, gy, 'down' if kind == 'pmos' else 'up', gx if not low else gx + 10))
        for side in ('top', 'bot'):
            tx, ty = pins_tb[side]
            n = nets_tb[side]
            if (side == 'top' and nm in stacked_top) or (side == 'bot' and nm in stacked_bot):
                continue
            last = r == nrows - 1
            if kind == 'pmos':
                if side == 'top' and n == vdd:
                    S.N(tx, ty, tx, YV, n)
                elif n == vdd:
                    S.N(tx, ty, tx + 30, ty, n); S.N(tx + 30, ty, tx + 30, YV, n)
                elif side == 'top':
                    pend.append((n, tx, ty, 'down', tx + 30))
                else:
                    pend.append((n, tx, ty, 'down', tx))
            else:   # nmos and resistor rows
                if side == 'bot' and n == vss and last:
                    S.N(tx, ty, tx, YS, n)
                elif n == vss:
                    off = 30 if not low else 50
                    S.N(tx, ty, tx + off, ty, n); S.N(tx + off, ty, tx + off, YS, n)
                elif side == 'top' and not low:
                    pend.append((n, tx, ty, 'up', tx))
                elif side == 'top':
                    pend.append((n, tx, ty, 'up', tx + 40))
                else:
                    pend.append((n, tx, ty, 'up', tx + (30 if not low else 50)))
    # channel tracks between the PMOS row and the first NMOS row
    nets = []
    for n, *_r in pend:
        if n not in nets:
            nets.append(n)
    ytop, ybot = rowy[0] + 60, rowy[1] - 60
    step = 20
    slots = list(range(ytop + 20, ybot - 10, step))
    if len(nets) > len(slots):
        step = 10
        slots = list(range(ytop + 10, ybot - 5, step))
    assert len(nets) <= len(slots), (sub['name'], len(nets), len(slots))
    # PMOS-side nets near the top, NMOS-side nets near the bottom
    def side(n):
        ds = [d for (m, _, _, d, _) in pend if m == n]
        return sum(1 for d in ds if d == 'down') - sum(1 for d in ds if d == 'up')
    nets.sort(key=lambda n: -side(n))
    ty = {n: slots[k] for k, n in enumerate(nets)}
    xs = {n: [] for n in nets}
    # straight drops first, then the jogged ones
    for n, x, y, d, x0 in sorted(pend, key=lambda p: p[4] != p[1]):
        xs[n].append(S.vroute(n, x, y, ty[n], x0))
    for n in nets:
        lo, hi = min(xs[n]), max(xs[n])
        if n in ports and n not in (vdd, vss):
            lo = XP
        if n in (vdd, vss):
            # link the track to its rail at the right end
            hi2 = xmax + (40 if n == vdd else 60)
            S.N(lo, ty[n], hi2, ty[n], n)
            S.N(hi2, ty[n], hi2, YV if n == vdd else YS, n)
        else:
            S.N(lo, ty[n], hi, ty[n], n)
            if n not in ports:
                S.lab(lo, ty[n], n, 0)
    # ports
    for n in ports:
        if n == vdd:
            S.port('iopin', XP, YV, n)
        elif n == vss:
            S.port('iopin', XP, YS, n)
        elif n in ty:
            S.port('iopin', XP, ty[n], n)
    S.text(XP, YV - 80 - 30 * len(notes) - 50, title, 0.6)  # title above the notes
    for k, s in enumerate(notes):
        S.text(XP, YV - 60 - 30 * (len(notes) - k), s, 0.3)
    return S


def symbol(sub, path, left=None, right=None, top=None, bot=None, label=None):
    """Box symbol, pins in .subckt order (sim_pinnumber)."""
    ports = sub['ports']
    left = left or [p for p in ports if p not in (right or []) + (top or []) + (bot or [])]
    right = right or []
    top = top or []
    bot = bot or []
    h = max(len(left), len(right), 2) * 20 + 20
    w = max(160, 40 * max(len(top), len(bot), 1) + 40)
    out = ['v {xschem version=3.4.5 file_version=1.2}',
           'G {}', 'K {type=subcircuit\nformat="@name @pinlist @symname"\ntemplate="name=x1"\n}', 'V {}', 'S {}', 'E {}',
           f'L 4 {-w//2} {-h//2} {w//2} {-h//2} {{}}', f'L 4 {w//2} {-h//2} {w//2} {h//2} {{}}',
           f'L 4 {w//2} {h//2} {-w//2} {h//2} {{}}', f'L 4 {-w//2} {h//2} {-w//2} {-h//2} {{}}',
           f'T {{@symname}} {-w//2 + 5} {-h//2 - 25} 0 0 0.3 0.3 {{}}',
           f'T {{@name}} {-w//2 + 5} {h//2 + 5} 0 0 0.3 0.3 {{}}']
    if label:
        out.append(f'T {{{label}}} {-w//2 + 10} {-10} 0 0 0.25 0.25 {{}}')
    pos = {}
    for k, p in enumerate(left):
        pos[p] = (-w // 2 - 20, -h // 2 + 20 + 20 * k, 'L')
    for k, p in enumerate(right):
        pos[p] = (w // 2 + 20, -h // 2 + 20 + 20 * k, 'R')
    for k, p in enumerate(top):
        pos[p] = (-w // 2 + 40 + 40 * k, -h // 2 - 20, 'T')
    for k, p in enumerate(bot):
        pos[p] = (-w // 2 + 40 + 40 * k, h // 2 + 20, 'B')
    for n, p in enumerate(ports):
        x, y, s = pos[p]
        out.append(f'B 5 {x - 2.5} {y - 2.5} {x + 2.5} {y + 2.5} {{name={p} dir=inout sim_pinnumber={n + 1}}}')
        if s == 'L':
            out.append(f'L 4 {x} {y} {x + 20} {y} {{}}')
            out.append(f'T {{{p}}} {x + 25} {y - 6} 0 0 0.2 0.2 {{}}')
        elif s == 'R':
            out.append(f'L 4 {x - 20} {y} {x} {y} {{}}')
            out.append(f'T {{{p}}} {x - 25} {y - 6} 0 1 0.2 0.2 {{}}')
        elif s == 'T':
            out.append(f'L 4 {x} {y} {x} {y + 20} {{}}')
            out.append(f'T {{{p}}} {x - 6} {y + 25} 1 0 0.2 0.2 {{}}')
        else:
            out.append(f'L 4 {x} {y - 20} {x} {y} {{}}')
            out.append(f'T {{{p}}} {x - 6} {y - 25} 3 0 0.2 0.2 {{}}')
    open(path, 'w').write('\n'.join(out) + '\n')
    return {p: pos[p] for p in ports}


def hier_sheet(sub, title, placement, symbols, notes=()):
    """Sheet of subcircuit instances: placement {inst: (x, y)}; every pin gets a short label stub."""
    S = Sheet(sub['name'], title)
    for i in sub['insts']:
        if i['model'] in MODEL_SYM:
            continue
        x, y = placement[i['name']]
        S.C(f"{i['model']}.sym", x, y, 0, 0, f"name={i['name']}")
        pins = symbols[i['model']]
        for p, n in zip(subs[i['model']]['ports'], i['nodes']):
            px, py, side = pins[p]
            ax, ay = x + px, y + py
            if side == 'L':
                S.N(ax - 30, ay, ax, ay, n); S.lab(ax - 30, ay, n, 0)
            elif side == 'R':
                S.N(ax, ay, ax + 30, ay, n); S.lab(ax + 30, ay, n, 1)
            elif side == 'T':
                S.N(ax, ay - 30, ax, ay, n); S.lab(ax, ay - 30, n, 1)
            else:
                S.N(ax, ay, ax, ay + 30, n); S.lab(ax, ay + 30, n, 1)
    # MOSFETs at hierarchical level (bus pass gates of bbl_core): with label stubs
    for i in sub['insts']:
        if i['model'] not in MODEL_SYM:
            continue
        x, y = placement[i['name']]
        p = i['params']
        kind = MODEL_SYM[i['model']][1]
        S.C(MODEL_SYM[i['model']][0], x, y, 0, 0,
            f"name={i['name'][1:]} l={p['l']} w={p['w']} ng={p.get('ng', 1)} m={p.get('m', 1)} mm_ok=1 "
            f"model={i['model']} spiceprefix=X")
        pins = mos_pins(kind, x, y)
        for t, n in zip(('D', 'G', 'S', 'B'), i['nodes']):
            px, py = pins[t]
            if t == 'G':
                S.N(px - 30, py, px, py, n); S.lab(px - 30, py, n, 0)
            elif t == 'B':
                S.N(px, py, px + 30, py, n); S.lab(px + 30, py, n, 1)
            elif py < y:
                S.N(px, py - 30, px, py, n); S.lab(px, py - 30, n, 1)
            else:
                S.N(px, py, px, py + 30, n); S.lab(px, py + 30, n, 1)
    # ports: a column on the left
    for k, n in enumerate(sub['ports']):
        S.port('iopin', -600, -400 + 25 * k, n)
        S.N(-600, -400 + 25 * k, -440, -400 + 25 * k, n)
        S.lab(-440, -400 + 25 * k, n, 1)
    S.text(-600, -560, title, 0.6)
    for k, s in enumerate(notes):
        S.text(-600, -510 + 30 * k, s, 0.3)
    return S


subs = parse_netlist([os.path.join(ROOT, 'netlist', 'source', 'bbl.spice'),
                      os.path.join(ROOT, 'netlist', 'source', 'bbl_slot.spice')])

if __name__ == '__main__':
    out = HERE
    I = lambda sub: [i['name'] for i in subs[sub]['insts']]
    sheets = {
        'bbl_neuron': ([['XMR3', 'XC1', 'XM3', 'XMR1', 'XM4', 'XMR5B'], ['XM2', 'XM1', 'XMR2', 'XMR5A', 'XC2']],
                       'bbl_neuron: Bionic Blinkenlight integrate-and-fire neuron (CMOS translation)',
                       ['Q1..Q4 of the discrete circuit = XM1..XM4; resistors = XMR1..XMR5B (R4 = the length of XM3)',
                        'XC1 membrane capacitor 10 pF (PMOS gate cap), XC2 slow-node capacitor 2.6 pF',
                        'self-biased: XMR1 gate on vss, XMR2 and XMR5A gates on vdd; XMR3 and XMR5B on the DAC bias vin',
                        'R5 = XMR5A (fast discharge of slow) + XMR5B (slow recharge: refractory time, complete reset)']),
        'bbl_dac': ([['XMD'], ['XMH', 'XMU0', 'XMU1', 'XMU2', 'XMU3'], [None, 'XMS0', 'XMS1', 'XMS2', 'XMS3']],
                    'bbl_dac: tuning DAC, diode XMD carries (0.5 + code) x unit, code = b3..b0',
                    ['b0..b3 are 1.2 V logic (dig_in); the half-unit leg XMH is always on']),
        'bbl_inv': ([['XMP'], ['XMN']], 'bbl_inv: 3.3 V inverter (LED bus driver, spike output)', []),
        'bbl_syn': ([['XMPW', 'XMRW', 'XMSW', 'XMPS', 'XMRS', 'XMSS'], ['XMNW', 'XMNS'], ['XMBW', 'XMBS']],
                    'bbl_syn: pulse synapse (stand-in for the photoresistor of the demos)',
                    ['g = NAND(spk, en): XMN/XMB stack, pull-ups XMP (spk) and XMR (self-biased, en)',
                     'XMSW weak leg (0.3/100), XMSS strong leg (0.3/20) into the postsynaptic membrane']),
        'bbl_gap': ([[], ['XMGW', 'XMGS'], ['XMTW', 'XMTS']], 'bbl_gap: gap junction (electrical synapse) a <-> b',
                    ['pass gates at the analog coupling voltage vc in series with 1.2 V enables']),
        'bbl_bias': ([['XMIP', 'XMPA', 'XMPB', 'XMSU', 'XMLP', 'XMCA', 'XMCB'],
                      ['XMIN', 'XMNA', 'XMNB', 'XMCL', 'XMLD', 'XCA', 'XCB'], [None, 'XMEA', 'XR1', 'XMEB']],
                     'bbl_bias: self-biased subthreshold beta multiplier (K = 8, rhigh), enable, pull-ups',
                     ['about 45 nA per branch; start-up by the Vgs = 0 leakage of XMSU',
                      'vbnl: about 2.5 nA reference of the tuning DACs; vcpla / vcplb pulled up by about 1 nA']),
        'bbl_tielo': ([[], ['XMT%d' % k for k in range(12)]], 'bbl_tielo: dig_out[11:0] held low (1.2 V NMOS)', []),
    }
    for nm, (rows, title, notes) in sheets.items():
        rails = ('vdd', 'vss')
        if nm == 'bbl_tielo':
            rails = ('vddl', 'vss')
        if rows[0] == []:
            rows = [[]] + rows[1:]
        sh = leaf_sheet(subs[nm], rows, title, rails=rails, notes=notes)
        sh.save(os.path.join(out, nm + '.sch'))
    # symbols
    syms = {}
    syms['bbl_neuron'] = symbol(subs['bbl_neuron'], os.path.join(out, 'bbl_neuron.sym'),
                                left=['vin'], right=['vm', 'out'], top=['vdd'], bot=['vss'], label='neuron')
    syms['bbl_dac'] = symbol(subs['bbl_dac'], os.path.join(out, 'bbl_dac.sym'),
                             left=['vbnl', 'b0', 'b1', 'b2', 'b3'], right=['vin'], top=['vdd'], bot=['vss'], label='DAC')
    syms['bbl_unit'] = symbol(subs['bbl_unit'], os.path.join(out, 'bbl_unit.sym'),
                              left=['vbnl', 'b0', 'b1', 'b2', 'b3'], right=['vm', 'out'], top=['vdd'], bot=['vss'],
                              label='neuron + DAC')
    syms['bbl_inv'] = symbol(subs['bbl_inv'], os.path.join(out, 'bbl_inv.sym'), left=['a'], right=['y'],
                             top=['vdd'], bot=['vss'])
    syms['bbl_syn'] = symbol(subs['bbl_syn'], os.path.join(out, 'bbl_syn.sym'), left=['spk', 'enw', 'ens'],
                             right=['post'], top=['vdd'], bot=['vss'], label='pulse synapse')
    syms['bbl_gap'] = symbol(subs['bbl_gap'], os.path.join(out, 'bbl_gap.sym'), left=['a', 'vc', 'enw', 'ens'],
                             right=['b'], bot=['vss'], label='gap junction')
    syms['bbl_bias'] = symbol(subs['bbl_bias'], os.path.join(out, 'bbl_bias.sym'), left=['ena'],
                              right=['vbnl', 'vcpla', 'vcplb'], top=['vdd', 'vddl'], bot=['vss', 'vssl'],
                              label='reference')
    syms['bbl_tielo'] = symbol(subs['bbl_tielo'], os.path.join(out, 'bbl_tielo.sym'),
                               left=['vddl', 'vssl', 'vss'], right=['q%d' % k for k in range(12)])
    core_ports = subs['bbl_core']['ports']
    syms['bbl_core'] = symbol(subs['bbl_core'], os.path.join(out, 'bbl_core.sym'),
                              left=['ena'] + ['d%d' % k for k in range(24)], right=['bus0', 'bus1', 'bus2', 'bus3', 'vcpla', 'vcplb'],
                              top=['vdd', 'vddl'], bot=['vss', 'vssl'], label='Bionic Blinkenlights core')
    # hierarchical sheets
    sh = hier_sheet(subs['bbl_unit'], 'bbl_unit: one neuron with its tuning DAC',
                    {'XN': (300, 0), 'XD': (-100, 0)}, syms)
    sh.save(os.path.join(out, 'bbl_unit.sch'))
    pl = {'XB': (-250, -300), 'XU0': (150, -350), 'XU1': (150, -50), 'XU2': (150, 250), 'XU3': (150, 550),
          'XL0': (650, -450), 'XL1': (650, -200), 'XI0': (1050, -450), 'XI1': (1050, -200),
          'XS01': (650, 50), 'XS10': (650, 250), 'XG01': (650, 450), 'XG32': (650, 650),
          'XMP2': (1050, 300), 'XMP3': (1050, 500)}
    sh = hier_sheet(subs['bbl_core'], 'bbl_core: four neurons, synapses, gap junctions, bus coupling', pl, syms,
                    ['N0, N1: LED drivers XL0 / XL1 on analog_bus0 / 1; synapses XS01 / XS10; gap junction XG01',
                     'N2, N3: membranes on analog_bus2 / 3 through XMP2 / XMP3 (gate vcplb); XG32 couples N3 to bus2'])
    sh.save(os.path.join(out, 'bbl_core.sch'))
    for v in ('bbl_slot_shared', 'bbl_slot_pads'):
        sp = subs[v]['ports']
        syms[v] = symbol(subs[v], os.path.join(out, v + '.sym'), label=v)
        sh = hier_sheet(subs[v], f'{v}: harness slot top', {'XC': (0, 0), 'XT': (0, 700)}, syms,
                        ['port names = harness slot wrapper pins'])
        sh.save(os.path.join(out, v + '.sch'))
    open(os.path.join(out, 'xschemrc'), 'w').write(
        '# SPDX-FileCopyrightText: 2026 Christoph Maier\n# SPDX-License-Identifier: Apache-2.0\n'
        'source $env(PDK_ROOT)/$env(PDK)/libs.tech/xschem/xschemrc\n'
        'append XSCHEM_LIBRARY_PATH :[file dirname [info script]]\n')
    print('sheets written to', out)


def tb_sheet(path, dut='bbl_slot_shared'):
    """Testbench: the slot with its supplies (sources in one row at the bottom on a GND bus), the
    harness bus switch (on-resistance) and bus line plus LED amplifier input on each analog bus, and
    a code block with the models, the dig_in settings and the transient."""
    S = Sheet('tb_' + dut, 'testbench')
    syms = {}
    syms[dut] = {p: v for p, v in symbol(subs[dut], os.path.join(HERE, dut + '.sym'), label=dut).items()}
    x0, y0 = 0, 0
    S.C(f'{dut}.sym', x0, y0, 0, 0, 'name=x1')
    pins = syms[dut]
    for p in subs[dut]['ports']:
        px, py, side = pins[p]
        ax, ay = x0 + px, y0 + py
        S.N(ax - 30, ay, ax, ay, p); S.lab(ax - 30, ay, p, 0)
    # supplies and enable: one row at the bottom, minus on the GND bus
    yb = 700
    S.N(-700, yb + 30, 200, yb + 30, '0')
    S.C('gnd.sym', -700, yb + 30, 0, 0, 'name=l0 lab=0')
    for k, (name, net, val) in enumerate([('Vdd33', 'vdd_3v3', 'pwl 0 0 100u 3.3'), ('Vdd12', 'vdd_1v2', 'pwl 0 0 100u 1.2'),
                                          ('Vena', 'enable', 'pwl 0 0 100u 0 200u 1.2'), ('Vss33', 'vss_3v3', '0'),
                                          ('Vss12', 'vss_1v2', '0')]):
        x = -600 + 160 * k
        S.C('vsource.sym', x, yb, 0, 0, f'name={name} value="{val}" savecurrent=false')
        S.N(x, yb - 30, x, yb - 60, net); S.lab(x, yb - 60, net, 1)
    # analog buses: harness switch (2 kOhm), bus line + pad + external load (Cbus), LED amplifier input
    for k in range(4):
        y = -300 + 200 * k
        x = 700
        S.N(x - 60, y, x, y, f'analog_bus{k}'); S.lab(x - 60, y, f'analog_bus{k}', 0)
        S.C('res.sym', x + 30, y, 1, 0, f'name=Rsw{k} value=2k m=1')     # rot 1: pins left/right
        S.N(x + 60, y, x + 240, y, f'busx{k}')
        S.lab(x + 240, y, f'busx{k}', 1)
        for j, (sym, nm, val) in enumerate([('capa.sym', f'Cb{k}', '3p'), ('res.sym', f'Ramp{k}', '1T'),
                                            ('capa.sym', f'Camp{k}', '5p')]):
            cx = x + 90 + 60 * j
            S.N(cx, y, cx, y + 40, f'busx{k}') if j else S.N(cx, y, cx, y + 40, f'busx{k}')
            S.C(sym, cx, y + 70, 0, 0, f'name={nm} value={val} m=1')
            S.C('gnd.sym', cx, y + 100, 0, 0, f'name=g{k}{j} lab=0')
    code = ('.lib cornerMOShv.lib mos_tt\n.lib cornerMOSlv.lib mos_tt\n.lib cornerRES.lib res_typ\n'
            '.option gmin=1e-15 reltol=1e-3 abstol=1e-14 method=gear\n'
            + ''.join(f'Vd{k} dig_in[{k}] 0 {v}\n' for k, v in enumerate(['1.2', '0', '0', '0'] + ['0'] * 20))
            + '.control\ntran 10u 2.5\nwrdata tb_' + dut + '.dat v(analog_bus0) v(analog_bus1) v(analog_bus2) v(analog_bus3)\n.endc\n')
    S.C('code_shown.sym', -700, 900, 0, 0, f'name=s1 only_toplevel=false value="{code}"')
    S.text(-700, -700, f'tb_{dut}: slot with harness bus switch, bus line and LED amplifier input per bus', 0.6)
    S.text(-700, -650, 'dig_in in the code block (N0 tuning code 1 here); vbias open (on-chip pull-up: full coupling)', 0.3)
    S.text(-700, -620, 'LED amplifier: ultra-high-impedance input modelled as 1 Tohm || 5 pF; Cb = bus line + pad (+ external)', 0.3)
    S.save(path)


if __name__ == '__main__':
    tb_sheet(os.path.join(HERE, 'tb_bbl_slot_shared.sch'))
    print('testbench written')

# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Assemble the Bionic Blinkenlights slot layouts (KLayout, IHP sg13cmos5l).

usage: python3 build_slot.py <harness>/gds/slot1_wrapper.gds <outdir>

Writes <outdir>/bbl_slot_shared.gds and <outdir>/bbl_slot_pads.gds (top cells of the same names).
Floorplan: the four neuron units stacked on the left half, the bias, synapses and small cells along
the bottom, a Metal3 trunk band between them (y 40..92 um). Every connection of a cell port is a
Metal4 vertical in its own column from the port's Metal3 track to the net's trunk; supplies go up or
down to TopMetal1 straps fed by the frame's supply pins.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pdk import db, L, TECHNAME
from lay import um, box, snap
import build

W, H = 537.15, 273.0
COL = 0.5                    # Metal4 column pitch
BAND = (40.5, 92.0)          # trunk band (Metal3), pin nets below PINLIM
PINLIM = 71.5

# instance name -> (cell, x, y, {cell net: global net})
def placement(variant):
    P = {}
    for k in range(4):
        P[f'U{k}'] = ('bbl_unit', 45.0, 96.0 + 43.0 * k,
                      dict(vdd='vdd', vss='vss', vm=f'vm{k}', out=f'out{k}', vbnl='vbnl',
                           b0=f'd{4*k}', b1=f'd{4*k+1}', b2=f'd{4*k+2}', b3=f'd{4*k+3}'))
    P['B'] = ('bbl_biasc', 45.0, 4.0, dict(vdd='vdd', vss='vss', vbnl='vbnl', vcpla='vcpla', vcplb='vcplb',
                                          ena='ena', enab='enab', rs='rs', sb='sb'))
    P['R'] = ('bbl_rhigh', 522.0, 95.0, dict(rs='rs', sb='sb'))
    P['S01'] = ('bbl_syn', 200.0, 4.0, dict(vdd='vdd', vss='vss', spk='spk0', post='vm1', enw='d16', ens='d17'))
    P['S10'] = ('bbl_syn', 200.0, 21.0, dict(vdd='vdd', vss='vss', spk='spk1', post='vm0', enw='d18', ens='d19'))
    for i, (nm, a, y) in enumerate([('XL0', 'out0', 'bus0'), ('XL1', 'out1', 'bus1'),
                                     ('XI0', 'out0', 'spk0'), ('XI1', 'out1', 'spk1')]):
        P[nm] = ('bbl_inv', 380.0 + 9.0 * i, 4.0, dict(vdd='vdd', vss='vss', a=a, y=y))
    P['G01'] = ('bbl_gap', 417.0, 4.0, dict(vss='vss', a='vm0', b='vm1', vc='vcpla', enw='d20', ens='d21'))
    P['G32'] = ('bbl_gap', 441.0, 4.0, dict(vss='vss', a='bus2', b='vm3', vc='vcplb', enw='d22', ens='d23'))
    P['PS'] = ('bbl_pass', 465.0, 4.0, dict(vss='vss', vm2='vm2', bus2='bus2', vm3='vm3', bus3='bus3', vcplb='vcplb'))
    P['LV'] = ('bbl_lvinv', 476.0, 4.0, dict(vddl='vddl', vssl='vssl', vss='vss', ena='ena', enab='enab'))
    P['TL'] = ('bbl_tielo', 486.0, 4.0, dict(dict(vddl='vddl', vssl='vssl', vss='vss'),
                                              **{f'q{k}': f'q{k}' for k in range(12)}))
    return P

SUPPLY_STRAPS = {'vss': [(116.0, 120.0), (137.0, 141.0)],
                 'vdd': [(153.0, 157.0), (196.0, 200.0), (239.0, 243.0)],
                 'vddl': [(36.0, 40.0)],
                 'vssl': [(67.0, 71.0)]}
SUPPLY_PIN = {'vss': 'vss_3v3', 'vdd': 'vdd_3v3', 'vddl': 'vdd_1v2', 'vssl': 'vss_1v2'}


class Router:
    def __init__(self, top, li):
        self.top, self.li = top, li
        self.occ = {}              # column -> list of (y0, y1)
        self.trunk_pts = {}        # net -> list of x
        self.trunk_y = {}

    def rect(self, layer, x0, y0, x1, y1):
        self.top.shapes(self.li[layer]).insert(box(x0, y0, x1, y1))

    def via(self, layer, x, y, s=0.19):
        self.rect(layer, x - s / 2, y - s / 2, x + s / 2, y + s / 2)

    def free(self, c, y0, y1):
        return all(y1 < a or y0 > b for a, b in self.occ.get(c, []))

    def take(self, c, y0, y1):
        self.occ.setdefault(c, []).append((y0, y1))

    def pick(self, lo, hi, y0, y1, wide=None):
        """Leftmost free column in [lo, hi] for a vertical from y0 to y1; wide = (ya, yb) range where
        the neighbouring columns must also be free (TopVia1 pad)."""
        c0, c1 = int((lo + 0.25) / COL) + 1, int((hi - 0.25) / COL)
        for c in range(c0, c1 + 1):
            if not self.free(c, y0 - 0.6, y1 + 0.6):
                continue
            if wide and not all(self.free(cc, wide[0], wide[1]) for cc in (c - 1, c + 1)):
                continue
            return c
        raise RuntimeError(f'no free Metal4 column in x {lo:.2f}..{hi:.2f} for y {y0:.2f}..{y1:.2f}')

    def vertical(self, c, y0, y1):
        x = c * COL
        ya, yb = min(y0, y1), max(y0, y1)
        self.rect('Metal4', x - 0.1, ya - 0.145, x + 0.1, yb + 0.145)
        self.take(c, ya, yb)
        return x


def build_variant(frame_gds, variant, outdir, slot=None):
    ly = db.Layout()
    ly.dbu = 0.001
    ly.technology_name = TECHNAME
    cells = {b.cell.name: b for b in build.cells(ly)}
    topname = f'slot_{slot}' if slot else f'bbl_slot_{variant}'
    top = ly.create_cell(topname)
    li = {k: ly.layer(*v) for k, v in L.items()}
    R = Router(top, li)

    # frame: shapes of the harness slot wrapper (pins, labels, boundary); the shared variant drops the
    # dedicated pad pins on the right edge
    fl = db.Layout()
    fl.read(frame_gds)
    ft = fl.top_cell()
    frame_pins = {}
    for fli in fl.layer_indexes():
        info = fl.get_info(fli)
        tli = ly.layer(info.layer, info.datatype)
        for sh in ft.shapes(fli).each():
            bb = sh.dbbox()
            right = bb.left > 530.0
            if variant == 'shared' and right:
                continue
            if sh.is_text():
                top.shapes(tli).insert(db.Text(sh.text_string, db.Trans(um(sh.text_dpos.x), um(sh.text_dpos.y))))
                frame_pins.setdefault(sh.text_string, []).append((info.layer, sh.text_dpos.x, sh.text_dpos.y))
            else:
                top.shapes(tli).insert(sh.polygon.to_dtype(fl.dbu).to_itype(ly.dbu) if sh.is_polygon()
                                       else box(bb.left, bb.bottom, bb.right, bb.top))

    # pin rectangles (Metal3 drawing under each Metal3 label)
    m3 = [s.dbbox() for s in ft.shapes(fl.find_layer(30, 0)).each()]

    def pin_rect(name):
        layer, x, y = [p for p in frame_pins[name] if p[0] == 30][0]
        cand = [b for b in m3 if b.left - 1e-3 <= x <= b.right + 1e-3 and b.bottom - 1e-3 <= y <= b.top + 1e-3]
        return min(cand, key=lambda b: b.width() * b.height())

    # instances
    P = placement(variant)
    ports = {}       # global net -> list of (inst, x_lo, x_hi, y_track)
    for inst, (cname, x, y, conn) in P.items():
        b = cells[cname]
        top.insert(db.CellInstArray(b.cell.cell_index(), db.Trans(um(x), um(y))))
        for cnet, gnet in conn.items():
            lo, hi = b.spans[cnet]
            ports.setdefault(gnet, []).append((inst, x + lo, x + hi, y + b.ty[cnet]))

    # signal nets: pins on the left edge (Metal3) and the dedicated pads on the right
    pin_of = {f'd{k}': f'dig_in[{k}]' for k in range(24)}
    pin_of.update({f'q{k}': f'dig_out[{k}]' for k in range(12)})
    pin_of.update({'ena': 'enable', 'bus0': 'analog_bus0', 'bus1': 'analog_bus1', 'bus2': 'analog_bus2',
                   'bus3': 'analog_bus3'})
    if variant == 'shared':
        pin_of['vcpla'] = 'vbias'
    else:
        pin_of['vcpla'] = f's{slot or 1}_an_0_esd'
        pin_of['vcplb'] = f's{slot or 1}_an[1]'

    # trunk assignment: pin nets first (they must stay below PINLIM), then the rest
    signal_nets = sorted(n for n in ports if n not in SUPPLY_STRAPS)
    order = [n for n in signal_nets if n in pin_of and pin_of[n] in frame_pins and pin_rect(pin_of[n]).left < 5] + \
            [n for n in signal_nets if not (n in pin_of and pin_of[n] in frame_pins and pin_rect(pin_of[n]).left < 5)]
    for i, n in enumerate(order):
        R.trunk_y[n] = BAND[0] + i * 0.5
    assert max(R.trunk_y.values()) < BAND[1]
    nleft = sum(1 for n in order if n in pin_of and pin_of[n] in frame_pins and pin_rect(pin_of[n]).left < 5)
    assert BAND[0] + (nleft - 1) * 0.5 < PINLIM, 'too many pin trunks for the space below the pin band'

    # supply landings first (wide TopVia1 pads)
    for net, straps in SUPPLY_STRAPS.items():
        for (inst, lo, hi, yt) in ports.get(net, []):
            ys0, ys1 = min(straps, key=lambda s: abs((s[0] + s[1]) / 2 - yt))
            ys = (ys0 + ys1) / 2
            c = R.pick(lo, hi, min(yt, ys), max(yt, ys), wide=(ys - 0.8, ys + 0.8))
            x = R.vertical(c, yt, ys)
            R.via('Via3', x, yt)
            R.rect('Metal4', x - 0.31, ys - 0.31, x + 0.31, ys + 0.31)
            R.via('TopVia1', x, ys, 0.42)
            for cc in (c - 1, c + 1):
                R.take(cc, ys - 0.8, ys + 0.8)
    # TopMetal1 straps from the supply pins
    for net, straps in SUPPLY_STRAPS.items():
        for ys0, ys1 in straps:
            R.rect('TopMetal1', 0.0, ys0, 518.0, ys1)
    # second supply pins of the frame on Metal2 (slots 3 and 12: a vss_3v3 strip on the right edge, the same
    # port as the TopMetal1 pin on the left): Via2 + Via3 near the top of the strip, Metal4 up to the nearest
    # strap of that supply, TopVia1, and the strap extended east over it
    m2 = [s.dbbox() for s in ft.shapes(fl.find_layer(10, 0)).each()] if fl.find_layer(10, 0) is not None else []
    for net, pin in SUPPLY_PIN.items():
        for layer, px, py in frame_pins.get(pin, []):
            if layer != 10:
                continue
            pr = [b for b in m2 if b.left <= px <= b.right and b.bottom <= py <= b.top][0]
            ys0, ys1 = min(SUPPLY_STRAPS[net], key=lambda s: abs((s[0] + s[1]) / 2 - py))
            ys, yl = (ys0 + ys1) / 2, pr.top - 1.0
            c = R.pick(pr.left + 0.3, pr.right - 0.3, yl, ys, wide=(ys - 0.8, ys + 0.8))
            x = R.vertical(c, yl, ys)
            R.rect('Metal3', x - 0.3, yl - 0.3, x + 0.3, yl + 0.3)
            R.via('Via2', x, yl)
            R.via('Via3', x, yl)
            R.rect('Metal4', x - 0.31, ys - 0.31, x + 0.31, ys + 0.31)
            R.via('TopVia1', x, ys, 0.42)
            R.rect('TopMetal1', 517.0, ys0, x + 1.0, ys1)
            for cc in (c - 1, c + 1):
                R.take(cc, ys - 0.8, ys + 0.8)

    # signal landings
    for net in order:
        ty = R.trunk_y[net]
        for (inst, lo, hi, yt) in ports[net]:
            c = R.pick(lo, hi, min(yt, ty), max(yt, ty))
            x = R.vertical(c, yt, ty)
            R.via('Via3', x, yt)
            R.via('Via3', x, ty)
            R.trunk_pts.setdefault(net, []).append(x)
    # pins
    xl_next = [3.0]
    for net in order:
        if net not in pin_of or pin_of[net] not in frame_pins:
            continue
        pr = pin_rect(pin_of[net])
        ty = R.trunk_y[net]
        yc = (pr.bottom + pr.top) / 2
        hh = min(pr.height(), 0.4) / 2 if pr.height() > 0.3 else pr.height() / 2
        if pr.left < 5:            # left edge: Metal3 east to a column in x 3..40
            c = R.pick(xl_next[0], 40.0, min(yc, ty), max(yc, ty))
            x = R.vertical(c, yc, ty)
            R.rect('Metal3', pr.right - 0.05, yc - hh, x + 0.145, yc + hh)
            xl_next[0] = x + 0.05
        else:                      # right edge pad: Metal3 west to a column in x 528..534
            c = R.pick(528.0, pr.left - 0.4, min(yc, ty), max(yc, ty))
            x = R.vertical(c, yc, ty)
            R.rect('Metal3', x - 0.145, yc - hh, pr.left + 0.05, yc + hh)
        R.via('Via3', x, yc)
        R.via('Via3', x, ty)
        R.trunk_pts.setdefault(net, []).append(x)
    # trunks
    for net, xs in R.trunk_pts.items():
        ty = R.trunk_y[net]
        lo, hi = min(xs) - 0.145, max(xs) + 0.145
        if hi - lo < 0.8:
            lo, hi = (lo + hi) / 2 - 0.4, (lo + hi) / 2 + 0.4
        R.rect('Metal3', lo, ty - 0.1, hi, ty + 0.1)

    os.makedirs(outdir, exist_ok=True)
    opt = db.SaveLayoutOptions()
    opt.write_context_info = False
    out = os.path.join(outdir, topname + '.gds')
    # keep only the cells under this top
    keep = set([top.cell_index()]) | set(top.called_cells())
    for ci in [c.cell_index() for c in ly.each_cell()]:
        if ci not in keep:
            ly.delete_cell(ci)
    ly.write(out, opt)
    print(out, top.dbbox(), 'trunks', len(R.trunk_y), 'columns', len(R.occ))
    return out


def pad_types(config, n):
    """Pad types of slot n's dedicated pads, from the harness config.txt ("s<n>_an[k]: <type> <name>")."""
    types = {}
    for line in open(config):
        f = line.split()
        if f and f[0].startswith(f's{n}_an['):
            types[int(f[0][len(f's{n}_an['):-2])] = f[1]
    return types


if __name__ == '__main__':
    # build_slot.py <harness>/gds <outdir>                    the two generic variants (slot 1 frame)
    # build_slot.py <harness>/gds <outdir> <N> shared|pads    slot_<N>.gds for the harness, top cell slot_<N>
    hdir = sys.argv[1]
    outdir = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(__file__), '..', 'gds')
    if len(sys.argv) > 4:
        n, v = int(sys.argv[3]), sys.argv[4]
        # the pads variant takes vcpla from s<N>_an_0_esd and vcplb from s<N>_an[1]: both pads have to be
        # analog pads (config.txt of the harness; in the 2026-11 config: slots 1, 2, 3, 5, 9, 10, 12, 14, 16, 18)
        t = pad_types(os.path.join(hdir, '..', 'config.txt'), n)
        if v == 'pads' and not (t.get(0) == t.get(1) == 'sg13cmos5l_IOPadAnalog'):
            sys.exit(f'slot {n}: dedicated pads {t}; the pads variant needs s{n}_an[0] and s{n}_an[1] '
                     f'to be sg13cmos5l_IOPadAnalog; use the shared variant')
        build_variant(os.path.join(hdir, f'slot{n}_wrapper.gds'), v, outdir, slot=n)
    else:
        for v in ('shared', 'pads'):
            build_variant(os.path.join(hdir, 'slot1_wrapper.gds'), v, outdir)

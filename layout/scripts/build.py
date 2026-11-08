# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Build the Bionic Blinkenlights layout (cells and slot tops) from the source netlist's devices.

Usage:  python3 build.py [outdir]
Writes <outdir>/bbl_cells.gds (all cells) -- the slot tops are added by build_slot.py.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pdk import db, TECHNAME
from lay import Builder

GAP = 0.80          # horizontal gap between devices in a row (um)


def row(b, devs, x0, yref, side, avoid=None):
    """Place devices left to right. devs: list of (name, kind, w, l, ng, S, D, G).
    side 'up' = NMOS row below the channel, aligned by the active's top edge at yref;
    side 'down' = PMOS row above the channel, aligned by the active's bottom edge at yref.
    avoid: Metal2 stub x positions of the other row (pins of other nets must keep 0.45 um)."""
    x = x0
    for dv in devs:
        (name, kind, w, l, ng, S, D, G) = dv[:8]
        model = dv[8] if len(dv) > 8 else None
        wf = w / ng
        y = yref - wf if side == 'up' else yref
        if avoid is not None:
            # nudge right until no stub of this device comes closer than 0.45 um to a foreign stub
            while True:
                sx = [x + 0.15 + i * (l + 0.38) for i in range(ng + 1)]
                gx = [x + 0.34 + l / 2 + i * (l + 0.38) for i in range(ng)]
                mine = [(S if i % 2 == 0 else D, p) for i, p in enumerate(sx)] + [(G, gx[len(gx) // 2])]
                bad = any(abs(p - q) < 0.45 and n != m for n, p in mine for (m, q) in avoid)
                if not bad:
                    break
                x += 0.05
        width = b.mos(name, kind, w, l, ng, x, y, side, S, D, G, model=model)
        x += width + GAP
    return x


def stubs_of(b, start):
    return [(n, x) for (n, x, y) in b.pins[start:]]


def make_cell(ly, name, pdev, ndev, pnet='vdd', nnet='vss', tgo=True, lv=False, xpad=1.5, ports=()):
    """Generic cell: optional PMOS row (side 'down') over a channel over an optional NMOS row.
    Tap rails: ptap (net nnet) under the NMOS row, ntap (net pnet) over the PMOS row."""
    b = Builder(ly, name)
    model = 'lv' if lv else None
    nets = set()
    for d in pdev + ndev:
        nets |= {d[5], d[6], d[7]}
    nets |= ({nnet} if ndev else set()) | ({pnet} if pdev else set())
    ntr = len(nets) + 2
    chan = (ntr - 1) * 0.5 + 1.6 + 2 * (0.48 + 0.3)
    xl, ybot = 0.0, 0.0
    hn = max([d[2] / d[4] for d in ndev], default=0.0)
    hp = max([d[2] / d[4] for d in pdev], default=0.0)
    yn_top = ybot + (0.78 + 1.2 + hn if ndev else 0.0)
    yp_bot = yn_top + chan
    ytop = yp_bot + (hp + 1.2 + 0.78 if pdev else 0.0)
    pstubs = []
    xr_p = xr_n = xl + xpad
    if pdev:
        xr_p = row(b, [d + (model,) for d in pdev], xl + xpad, yp_bot, 'down')
        pstubs = stubs_of(b, 0)
    if ndev:
        xr_n = row(b, [d + (model,) for d in ndev], xl + xpad, yn_top, 'up', avoid=pstubs)
    xr = max(xr_p, xr_n) + 0.7
    if ndev:
        b.tap('p', xl, ybot, xr, nnet)
        b.pins.append((nnet, xl + 0.3, ybot + 0.39))
        b.via('Via1', xl + 0.3, ybot + 0.39)
    if pdev:
        b.tap('n', xl, ytop - 0.78, xr, pnet)
        b.pins.append((pnet, xl + 0.9, ytop - 0.39))
        b.via('Via1', xl + 0.9, ytop - 0.39)
        b.rect('NWell', xl - 0.62, yp_bot - 1.2, xr + 0.62, ytop + 0.62)
    if tgo:
        b.rect('ThickGateOx', xl - 0.7, ybot - 0.7, xr + 0.7, ytop + 0.7)
    b.ty, b.ntr = b.channel(yn_top + 0.48 + 0.3, yp_bot - 0.48 - 0.3,
                            ext={p: (xl + 0.2, xr - 0.2) for p in ports})
    b.rect('prBoundary', xl - 1.0, ybot - 1.0, xr + 1.0, ytop + 1.0)
    b.bbox = (xl - 1.0, ybot - 1.0, xr + 1.0, ytop + 1.0)
    return b


def rhigh_cell(ly, name, w, l, nb, A, B):
    """rhigh meander (no ThickGateOx) with its two terminals routed up to a two-track channel."""
    from pdk import pcell
    b = Builder(ly, name)
    ci = pcell(ly, 'rhigh', w=f'{w}u', l=f'{l}u', b=nb)
    x0, y0 = 1.0, 1.5
    b.inst(ci, x0, y0)
    bb = ly.cell(ci).dbbox()
    pins = []
    for sh in ly.cell(ci).shapes(ly.layer(8, 2)).each():
        c = sh.dbbox().center()
        pins.append((c.x + x0, c.y + y0))
    pins.sort()
    for net, (x, y) in zip((A, B), pins):
        b.rect('Metal1', x - 0.23, y - 0.145, x + 0.23, y + 0.145)
        b.via('Via1', x, y)
        b.pins.append((net, x, y))
    ytop = y0 + bb.top
    b.ty, b.ntr = b.channel(ytop + 0.5, ytop + 0.5 + 0.5 + 1.6 + 0.5,
                            ext={A: (0.3, x0 + bb.right + 0.7), B: (0.3, x0 + bb.right + 0.7)})
    b.rect('prBoundary', 0.0, 0.0, x0 + bb.right + 1.0, ytop + 4.1)
    b.bbox = (0.0, 0.0, x0 + bb.right + 1.0, ytop + 4.1)
    return b


def unit(ly):
    """bbl_unit: neuron (8 transistors, C1, C2) plus tuning DAC."""
    pdev = [('XMD', 'p', 3, 3, 1, 'vdd', 'vin', 'vin'),
            ('XMR3', 'p', 0.3, 30, 1, 'vdd', 'vm', 'vin'),
            ('XC1', 'p', 225, 10, 18, 'vdd', 'vdd', 'vm'),
            ('XM3', 'p', 1, 0.45, 1, 'vdd', 'vm', 'out'),
            ('XMR1', 'p', 0.3, 20, 1, 'vdd', 'out', 'vss'),
            ('XM4', 'p', 1, 0.45, 1, 'vdd', 'rst', 'slow'),
            ('XMR5', 'p', 0.3, 100, 1, 'out', 'slow', 'vss')]
    ndev = [('XM1', 'n', 1, 1, 1, 'vss', 'out', 'vm'),
            ('XM2', 'n', 2, 0.45, 1, 'vss', 'vm', 'rst'),
            ('XMR2', 'n', 0.3, 20, 1, 'vss', 'rst', 'vdd'),
            ('XC2', 'n', 40, 10, 4, 'vss', 'vss', 'slow'),
            ('XMH', 'n', 0.3, 4.5, 1, 'vss', 'vin', 'vbnl'),
            ('XMU0', 'n', 0.3, 2, 1, 's0', 'vin', 'vbnl'),
            ('XMS0', 'n', 0.3, 0.45, 1, 'vss', 's0', 'b0'),
            ('XMU1', 'n', 0.6, 2, 2, 's1', 'vin', 'vbnl'),
            ('XMS1', 'n', 0.6, 0.45, 2, 'vss', 's1', 'b1'),
            ('XMU2', 'n', 1.2, 2, 4, 's2', 'vin', 'vbnl'),
            ('XMS2', 'n', 1.2, 0.45, 4, 'vss', 's2', 'b2'),
            ('XMU3', 'n', 2.4, 2, 8, 's3', 'vin', 'vbnl'),
            ('XMS3', 'n', 2.4, 0.45, 8, 'vss', 's3', 'b3')]
    return make_cell(ly, 'bbl_unit', pdev, ndev, ports=('vdd', 'vss', 'vm', 'out', 'vbnl', 'b0', 'b1', 'b2', 'b3'))


def cells(ly):
    out = [unit(ly)]
    out.append(make_cell(ly, 'bbl_inv', [('XMP', 'p', 1, 0.45, 1, 'vdd', 'y', 'a')],
                         [('XMN', 'n', 1, 0.45, 1, 'vss', 'y', 'a')], ports=('vdd', 'vss', 'a', 'y')))
    out.append(make_cell(ly, 'bbl_syn',
        [('XMPW', 'p', 0.3, 0.45, 1, 'vdd', 'gw', 'spk'), ('XMRW', 'p', 0.3, 20, 1, 'vdd', 'gw', 'vss'),
         ('XMSW', 'p', 0.3, 100, 1, 'vdd', 'post', 'gw'), ('XMPS', 'p', 0.3, 0.45, 1, 'vdd', 'gs', 'spk'),
         ('XMRS', 'p', 0.3, 20, 1, 'vdd', 'gs', 'vss'), ('XMSS', 'p', 0.3, 20, 1, 'vdd', 'post', 'gs')],
        [('XMNW', 'n', 0.3, 0.45, 1, 'bw', 'gw', 'enw'), ('XMBW', 'n', 0.3, 0.45, 1, 'vss', 'bw', 'spk'),
         ('XMNS', 'n', 0.3, 0.45, 1, 'bs', 'gs', 'ens'), ('XMBS', 'n', 0.3, 0.45, 1, 'vss', 'bs', 'spk')],
        ports=('vdd', 'vss', 'spk', 'post', 'enw', 'ens')))
    out.append(make_cell(ly, 'bbl_gap', [],
        [('XMGW', 'n', 0.3, 10, 1, 'gw', 'a', 'vc'), ('XMTW', 'n', 0.3, 0.45, 1, 'b', 'gw', 'enw'),
         ('XMGS', 'n', 1, 0.45, 1, 'gs', 'a', 'vc'), ('XMTS', 'n', 1, 0.45, 1, 'b', 'gs', 'ens')],
        ports=('vss', 'a', 'b', 'vc', 'enw', 'ens')))
    out.append(make_cell(ly, 'bbl_pass', [],
        [('XMP2', 'n', 1, 0.45, 1, 'vm2', 'bus2', 'vcplb'), ('XMP3', 'n', 1, 0.45, 1, 'vm3', 'bus3', 'vcplb')],
        ports=('vss', 'vm2', 'bus2', 'vm3', 'bus3', 'vcplb')))
    out.append(make_cell(ly, 'bbl_biasc',
        [('XMPA', 'p', 2, 2, 1, 'vdd', 'vbn', 'vbp'), ('XMPB', 'p', 2, 2, 1, 'vdd', 'vbp', 'vbp'),
         ('XMSU', 'p', 4, 0.45, 1, 'vdd', 'vbn', 'vdd'), ('XMLP', 'p', 0.3, 8, 1, 'vdd', 'vbnl', 'vbp'),
         ('XMCA', 'p', 0.3, 22, 1, 'vdd', 'vcpla', 'vbp'), ('XMCB', 'p', 0.3, 22, 1, 'vdd', 'vcplb', 'vbp')],
        [('XMNA', 'n', 2, 2, 1, 'sa', 'vbn', 'vbn'), ('XMNB', 'n', 16, 2, 8, 'rs', 'vbp', 'vbn'),
         ('XMEA', 'n', 1, 0.45, 1, 'vss', 'sa', 'ena'), ('XMEB', 'n', 1, 0.45, 1, 'vss', 'sb', 'ena'),
         ('XMCL', 'n', 1, 0.45, 1, 'vss', 'vbn', 'enab'), ('XMLD', 'n', 2, 2, 1, 'vss', 'vbnl', 'vbnl'),
         ('XCA', 'n', 50, 10, 5, 'vss', 'vss', 'vcpla'), ('XCB', 'n', 50, 10, 5, 'vss', 'vss', 'vcplb')],
        ports=('vdd', 'vss', 'vbnl', 'vcpla', 'vcplb', 'ena', 'enab', 'rs', 'sb')))
    out.append(rhigh_cell(ly, 'bbl_rhigh', 0.5, 40, 9, 'rs', 'sb'))
    out.append(make_cell(ly, 'bbl_lvinv', [('XMIP', 'p', 0.3, 0.5, 1, 'vddl', 'enab', 'ena')],
                         [('XMIN', 'n', 0.3, 0.5, 1, 'vssl', 'enab', 'ena')], pnet='vddl', tgo=False, lv=True,
                         ports=('vddl', 'vssl', 'vss', 'ena', 'enab')))
    out.append(make_cell(ly, 'bbl_tielo', [],
        [(f'XMT{k}', 'n', 0.3, 0.5, 1, 'vssl', f'q{k}', 'vddl') for k in range(12)], tgo=False, lv=True,
        ports=tuple(['vddl', 'vssl', 'vss'] + [f'q{k}' for k in range(12)])))
    return out


def main(outdir):
    ly = db.Layout()
    ly.dbu = 0.001
    ly.technology_name = TECHNAME
    for b in cells(ly):
        print(b.cell.name, b.cell.dbbox(), 'tracks', b.ntr)
    os.makedirs(outdir, exist_ok=True)
    opt = db.SaveLayoutOptions()
    opt.write_context_info = False
    ly.write(os.path.join(outdir, 'bbl_cells.gds'), opt)


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), '..', 'gds'))

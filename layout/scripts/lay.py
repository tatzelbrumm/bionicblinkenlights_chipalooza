# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Row-and-channel layout builder for the Bionic Blinkenlights cells (IHP sg13cmos5l, KLayout).

A cell is a PMOS row above a routing channel and an NMOS row below it. Devices are PDK PCells
(nmosHV, pmosHV, rhigh, ...). Every source/drain strip and every gate gets its own vertical Metal2
stub into the channel, where each net has its own horizontal Metal3 track (left-edge interval
packing). Nothing else uses Metal2/Metal3 inside a cell, so stubs and tracks cannot short as long
as stubs keep the Metal2 pitch, which the device geometry guarantees (L >= 0.45 um).
Metal4 and TopMetal1 are left free for the top level.
"""
import math
from pdk import db, L, pcell, LIB, TECHNAME

DBU = 0.001
M2W, M3W = 0.20, 0.20          # stub / track width
TRK = 0.50                     # Metal3 track pitch
V = 0.19                       # via size (Via1..Via3)


def um(x):
    return int(round(x / DBU))


def snap(x):
    return round(x / 0.005) * 0.005


def box(x0, y0, x1, y1):
    return db.Box(um(min(x0, x1)), um(min(y0, y1)), um(max(x0, x1)), um(max(y0, y1)))


class Builder:
    def __init__(self, layout, name):
        self.ly = layout
        self.cell = layout.create_cell(name)
        self.li = {k: layout.layer(*v) for k, v in L.items()}
        self.pins = []        # (net, x, y, layer) layer 'M1' for S/D/gate pads
        self.devices = []     # (name, kind, params, bbox)
        self.ports = set()

    # -- primitives ---------------------------------------------------------------------------
    def rect(self, layer, x0, y0, x1, y1):
        self.cell.shapes(self.li[layer]).insert(box(x0, y0, x1, y1))

    def via(self, layer, x, y):
        h = V / 2
        self.rect(layer, x - h, y - h, x + h, y + h)

    def label(self, layer, text, x, y):
        self.cell.shapes(self.li[layer]).insert(db.Text(text, db.Trans(um(x), um(y))))

    def inst(self, ci, x, y, mirror=False):
        t = db.Trans(db.Trans.M0 if mirror else db.Trans.R0, um(snap(x)), um(snap(y)))
        self.cell.insert(db.CellInstArray(ci, t))

    # -- MOS ------------------------------------------------------------------------------------
    def mos(self, name, kind, w, l, ng, x, y, side, S, D, G, model=None):
        """Place a MOSFET with its active area's lower-left corner at (x, y).
        side = 'up': the routing channel is above the device (NMOS row);
        side = 'down': the channel is below (PMOS row).
        Strips alternate S, D, S, ... from the left; gates are tied by a poly bar on the channel side.
        Returns the device width (um)."""
        pc = 'nmosHV' if kind == 'n' else 'pmosHV'
        if model == 'lv':
            pc = 'nmos' if kind == 'n' else 'pmos'
        wf = w / ng
        ci = pcell(self.ly, pc, w=f'{w:.3f}u', l=f'{l:.3f}u', ng=ng)
        # The PCell's active area starts at (0, 0) and is wf tall; mirror for 'down' so that the
        # poly end cap at the channel side is the one we extend.
        if side == 'up':
            self.inst(ci, x, y)
            ya, yb = y, y + wf          # active bottom / top
        else:
            self.inst(ci, x, y + wf, mirror=True)
            ya, yb = y, y + wf
        # measured from the PCell: strip i at 0.07 + i (l + 0.38) .. + 0.16, gate i at 0.34 + i (l + 0.38)
        sx = [0.15 + i * (l + 0.38) for i in range(ng + 1)]
        gx = [0.34 + l / 2 + i * (l + 0.38) for i in range(ng)]
        # strips: via pads on the channel side
        for i, cx in enumerate(sx):
            net = S if i % 2 == 0 else D
            if wf >= 0.69:
                vy = (yb - 0.245) if side == 'up' else (ya + 0.245)
            else:
                vy = (ya + yb) / 2
            if side == 'up':
                self.rect('Metal1', x + cx - 0.105, vy + 0.145 - 0.45, x + cx + 0.105, vy + 0.145)
            else:
                self.rect('Metal1', x + cx - 0.105, vy - 0.145, x + cx + 0.105, vy - 0.145 + 0.45)
            self.via('Via1', x + cx, vy)
            self.pins.append((net, x + cx, vy))
        # gate poly bar and contact(s) on the channel side
        gl, gr = x + gx[0] - l / 2, x + gx[-1] + l / 2
        if side == 'up':
            py0, py1 = yb + 0.07, yb + 0.48
            cy = yb + 0.33
        else:
            py0, py1 = ya - 0.48, ya - 0.07
            cy = ya - 0.33
        self.rect('GatPoly', gl, py0, gr, py1)
        gcx = x + gx[len(gx) // 2]
        self.rect('Cont', gcx - 0.08, cy - 0.08, gcx + 0.08, cy + 0.08)
        if side == 'up':
            self.rect('Metal1', gcx - 0.145, cy - 0.13, gcx + 0.145, cy + 0.19)
        else:
            self.rect('Metal1', gcx - 0.145, cy - 0.19, gcx + 0.145, cy + 0.13)
        self.via('Via1', gcx, cy)
        self.pins.append((G, gcx, cy))
        width = sx[-1] + 0.23
        self.devices.append((name, pc, dict(w=w, l=l, ng=ng), (x, ya, x + width, yb)))
        return width

    def tap(self, kind, x0, y0, x1, net):
        """Substrate (ptap) or NWell (ntap) tie strip from x0 to x1 at y0 (0.78 um tall), with a
        Metal1 rail on top; the rail is the tie's terminal."""
        n = max(1, int((x1 - x0 - 0.78) // 4.0) + 1)
        step = round((x1 - x0 - 0.78) / max(n - 1, 1) / 0.005 - 0.5) * 0.005
        ci = pcell(self.ly, 'ptap1' if kind == 'p' else 'ntap1', w='0.78u', l='0.78u')
        for i in range(n):
            self.inst(ci, snap(x0 + i * step), snap(y0))
        self.rect('Metal1', x0, y0 + 0.14, x1, y0 + 0.64)
        return (net, x0, x1, y0 + 0.39)

    # -- routing ----------------------------------------------------------------------------------
    def channel(self, ylo, yhi, order=None, ext=None):
        """Route all registered pins in a channel between ylo (top of the NMOS row's gate pads)
        and yhi (bottom of the PMOS row's gate pads). Returns {net: track y}.
        ext: {net: (x_left, x_right)} to extend tracks (cell ports)."""
        nets = {}
        for net, x, y in self.pins:
            nets.setdefault(net, []).append((x, y))
        ext = ext or {}
        spans = {}
        for net, pts in nets.items():
            xs = [p[0] for p in pts]
            lo, hi = min(xs) - 0.15, max(xs) + 0.15
            if hi - lo < 0.8:
                c = (lo + hi) / 2
                lo, hi = c - 0.4, c + 0.4
            if net in ext:
                lo, hi = min(lo, ext[net][0]), max(hi, ext[net][1])
            spans[net] = (lo, hi)
        # left-edge packing
        order = order or sorted(spans, key=lambda n: spans[n][0])
        tracks = []           # list of lists of (lo, hi)
        assign = {}
        for net in order:
            lo, hi = spans[net]
            for ti, occ in enumerate(tracks):
                if all(hi + 0.6 < a or lo - 0.6 > b for a, b in occ):
                    occ.append((lo, hi)); assign[net] = ti; break
            else:
                tracks.append([(lo, hi)]); assign[net] = len(tracks) - 1
        ntr = len(tracks)
        need = (ntr - 1) * TRK + 2 * 0.8
        if yhi - ylo < need:
            raise ValueError(f'channel {yhi - ylo:.2f} um < {need:.2f} um for {ntr} tracks')
        y0 = (ylo + yhi) / 2 - (ntr - 1) * TRK / 2
        ty = {net: y0 + assign[net] * TRK for net in spans}
        for net, (lo, hi) in spans.items():
            y = ty[net]
            self.rect('Metal3', lo, y - M3W / 2, hi, y + M3W / 2)
            # net label and pin shape at the left end of the track
            self.rect('Metal3pin', lo, y - M3W / 2, lo + 0.4, y + M3W / 2)
            self.label('Metal3txt', net, lo + 0.2, y)
        self.spans = spans
        for net, x, y in self.pins:
            t = ty[net]
            self.rect('Metal2', x - M2W / 2, min(y, t) - 0.145, x + M2W / 2, max(y, t) + 0.145)
            self.via('Via2', x, t)
        return ty, ntr

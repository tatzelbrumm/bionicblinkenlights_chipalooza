# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Render a GDS top cell to PNG (matplotlib, selected layers).  usage: render.py in.gds out.png [cell]"""
import sys
import klayout.db as db
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
ly = db.Layout(); ly.read(sys.argv[1])
top = ly.cell(sys.argv[3]) if len(sys.argv) > 3 else ly.top_cell()
layers = [((31, 0), '#e8e0c0', 0.5), ((1, 0), '#40a040', 0.6), ((5, 0), '#d04040', 0.6), ((128, 0), '#a040a0', 0.7),
          ((8, 0), '#4060c0', 0.35), ((10, 0), '#c08020', 0.45), ((30, 0), '#20a0a0', 0.5),
          ((50, 0), '#a0a020', 0.5), ((126, 0), '#808080', 0.25)]
fig, ax = plt.subplots(figsize=(18, 9.5))
for (l, d), col, a in layers:
    li = ly.find_layer(l, d)
    if li is None:
        continue
    reg = db.Region(top.begin_shapes_rec(li)).merged()
    for p in reg.each():
        b = p.bbox()
        if p.is_box():
            ax.add_patch(Rectangle((b.left * ly.dbu, b.bottom * ly.dbu), b.width() * ly.dbu, b.height() * ly.dbu,
                                   color=col, alpha=a, lw=0))
        else:
            pts = [(pt.x * ly.dbu, pt.y * ly.dbu) for pt in p.to_simple_polygon().each_point()]
            ax.add_patch(plt.Polygon(pts, color=col, alpha=a, lw=0))
bb = top.dbbox()
ax.set_xlim(bb.left, bb.right); ax.set_ylim(bb.bottom, bb.top); ax.set_aspect('equal')
ax.set_title(f'{top.name}: NWell, Activ, GatPoly, PolyRes, Metal1..Metal4, TopMetal1')
plt.savefig(sys.argv[2], dpi=110, bbox_inches='tight')

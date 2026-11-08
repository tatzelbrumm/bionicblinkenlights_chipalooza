# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Load the IHP sg13cmos5l PyCell library into the standalone KLayout Python module."""
import os, sys, types
PDK_ROOT = os.environ.get('PDK_ROOT', '/foss/pdks')
TECH = os.path.join(PDK_ROOT, 'ihp-sg13cmos5l', 'libs.tech', 'klayout')
os.environ.setdefault('KLAYOUT_PATH', TECH)
_B = os.path.join(TECH, 'python')
for p in (os.path.join(_B, 'pycell4klayout-api', 'source', 'python'), _B):
    if p not in sys.path:
        sys.path.insert(0, p)
import klayout.db as db
import klayout.tl as tl
if 'pya' not in sys.modules:
    pya = types.ModuleType('pya')
    for m in (db, tl):
        for k in dir(m):
            if not k.startswith('__'):
                setattr(pya, k, getattr(m, k))
    sys.modules['pya'] = pya
import sg13cmos5l_pycell_lib  # noqa: F401  (registers library SG13_dev)
LIB = 'SG13_dev'
TECHNAME = 'sg13cmos5l'

# GDS layers (layer, datatype)
L = dict(Activ=(1, 0), GatPoly=(5, 0), Cont=(6, 0), nSD=(7, 0), Metal1=(8, 0), pSD=(14, 0),
         Via1=(19, 0), Metal2=(10, 0), Via2=(29, 0), Metal3=(30, 0), Via3=(49, 0), Metal4=(50, 0),
         Via4=(66, 0), Metal5=(67, 0), TopVia1=(125, 0), TopMetal1=(126, 0), NWell=(31, 0),
         ThickGateOx=(44, 0), prBoundary=(189, 4),
         Metal1pin=(8, 2), Metal2pin=(10, 2), Metal3pin=(30, 2), Metal4pin=(50, 2), Metal5pin=(67, 2),
         TopMetal1pin=(126, 2), Metal1txt=(8, 25), Metal2txt=(10, 25), Metal3txt=(30, 25),
         Metal4txt=(50, 25), Metal5txt=(67, 25), TopMetal1txt=(126, 25))

def pcell(layout, name, **params):
    """Instantiate a PDK PCell variant; returns the cell index."""
    c = layout.create_cell(name, LIB, params)
    if c is None:
        raise RuntimeError(f"PCell {name} {params} not created")
    return c.cell_index()

# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Simulation-only copy of the source netlist with 1 Tohm leak resistors on internal nodes that can be
left floating between two off transistors (switch stacks). They make the transient solver converge;
they are not part of the design and do not touch the membrane nodes (at most 3 pA at 3.3 V)."""
import re
LEAKS = {'bbl_dac': ['s0', 's1', 's2', 's3'], 'bbl_syn': ['bw', 'bs'], 'bbl_gap': ['gw', 'gs']}
def make(src, dst, groups=None, r='1e12', cpar=None):
    s = open(src).read()
    for sub, nodes in LEAKS.items():
        if groups is not None and sub not in groups:
            continue
        lines = ''.join(f"RLEAK_{n} {n} vss {r}\n" for n in nodes)
        s = s.replace(f".ends {sub}", lines + f".ends {sub}")
    if cpar:
        # wiring parasitics of the fast internal nodes (the layout adds more than this)
        s = s.replace('.ends bbl_neuron', ''.join(f'CPAR_{n} {n} vss {cpar}\n' for n in ('out', 'rst', 'slow')) + '.ends bbl_neuron')
        s = s.replace('.ends bbl_inv', f'CPAR_y y vss {cpar}\n.ends bbl_inv')
        s = s.replace('.ends bbl_syn', ''.join(f'CPAR_{n} {n} vss {cpar}\n' for n in ('gw', 'gs')) + '.ends bbl_syn')
    open(dst, 'w').write(s)
    return dst

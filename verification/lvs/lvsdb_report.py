# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Print the mismatches of a KLayout .lvsdb (circuits, pins, nets, devices that do not match)."""
import sys
import klayout.db as db

lvs = db.LayoutVsSchematic()
lvs.read(sys.argv[1])
xref = lvs.xref()
bad = 0
for cp in xref.each_circuit_pair():
    a, b = cp.first(), cp.second()
    name = (a.name if a else '-') + ' / ' + (b.name if b else '-')
    st = cp.status()
    if st == db.NetlistCrossReference.Match:
        print(f'circuit {name}: match')
        continue
    print(f'circuit {name}: {st}')
    for pp in xref.each_pin_pair(cp):
        if pp.status() != db.NetlistCrossReference.Match:
            print('  pin', pp.first().name() if pp.first() else '-', '/', pp.second().name() if pp.second() else '-', pp.status())
            bad += 1
    for npair in xref.each_net_pair(cp):
        if npair.status() != db.NetlistCrossReference.Match:
            print('  net', npair.first().expanded_name() if npair.first() else '-', '/',
                  npair.second().expanded_name() if npair.second() else '-', npair.status())
            bad += 1
    for dp in xref.each_device_pair(cp):
        if dp.status() != db.NetlistCrossReference.Match:
            f, s = dp.first(), dp.second()
            def dd(d):
                if not d:
                    return '-'
                return f"{d.expanded_name()} {d.device_class().name} " + ' '.join(
                    f"{t.name}={d.net_for_terminal(t.id()).expanded_name() if d.net_for_terminal(t.id()) else '?'}"
                    for t in d.device_class().terminal_definitions())
            print('  dev', dd(f), '|', dd(s), dp.status())
            bad += 1
    for sp in xref.each_subcircuit_pair(cp):
        if sp.status() != db.NetlistCrossReference.Match:
            print('  sub', sp.first().expanded_name() if sp.first() else '-', '/', sp.second().expanded_name() if sp.second() else '-', sp.status())
            bad += 1
print('mismatched items:', bad)

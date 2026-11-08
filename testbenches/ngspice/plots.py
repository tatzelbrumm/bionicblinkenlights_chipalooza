# SPDX-FileCopyrightText: 2026 Christoph Maier
# SPDX-License-Identifier: Apache-2.0
"""Figures and a results table from the campaign JSON files.
usage: python3 plots.py <tag> [<tag2>]   (tag2: post-layout results drawn next to tag)"""
import os, sys, json, glob
import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, 'results')
COL = ['#2a6fdb', '#d9822b', '#2f9e5b', '#c23b3b']


def load(tag):
    out = {}
    for f in glob.glob(os.path.join(HERE, 'out', tag, '*.json')):
        r = json.load(open(f))
        out[r['case']] = r
    return out


def tuning(R, ax, label, marker='o'):
    pts = []
    for name, r in R.items():
        if name.startswith('tune_') and r.get('ok'):
            codes = list(map(int, name.split('_')[1:]))
            for k in range(4):
                pts.append((codes[k], r['f'][k], k))
    for k in range(4):
        p = sorted((c, f) for c, f, kk in pts if kk == k)
        if p:
            ax.plot(*zip(*p), marker=marker, color=COL[k], label=f'{label} N{k}' + (' (bus)' if k >= 2 else ''))
    ax.set_xlabel('tuning code (dig_in)'); ax.set_ylabel('firing rate (Hz)'); ax.grid(alpha=0.3)


def raster(ax, r, title, t1=2.5):
    for k in range(4):
        sp = np.array(r['spikes'][k])
        ax.vlines(sp, k + 0.6, k + 1.4, color=COL[k])
    ax.set_yticks([1, 2, 3, 4]); ax.set_yticklabels(['N0', 'N1', 'N2', 'N3'])
    ax.set_xlim(0, t1); ax.set_title(title, fontsize=9); ax.set_xlabel('t (s)')


def main():
    tags = sys.argv[1:] or ['sch']
    os.makedirs(RES, exist_ok=True)
    R = {t: load(t) for t in tags}
    # 1. tuning
    fig, ax = plt.subplots(figsize=(7, 4.5))
    for t, m in zip(tags, ['o', 's']):
        tuning(R[t], ax, t, m)
    ax.legend(fontsize=7, ncol=2); ax.set_title('Tuning: firing rate vs. 4-bit code (N2, N3 on 3 pF buses)')
    fig.tight_layout(); fig.savefig(os.path.join(RES, 'tuning.png'), dpi=120)
    # 2. bus load and vcplb
    fig, axs = plt.subplots(1, 2, figsize=(11, 4.2))
    for t, m in zip(tags, ['o', 's']):
        pts = sorted((float(n.split('_')[1][:-1]), r['f']) for n, r in R[t].items() if n.startswith('busload_') and r.get('ok'))
        if pts:
            c = [p[0] for p in pts]
            for k in range(4):
                axs[0].plot(c, [p[1][k] for p in pts], marker=m, color=COL[k], label=f'{t} N{k}')
        pts = sorted((float(n.split('_')[1]), r['f']) for n, r in R[t].items() if n.startswith('vcplb_') and r.get('ok'))
        if pts:
            v = [p[0] for p in pts]
            for k in (2, 3):
                axs[1].plot(v, [p[1][k] for p in pts], marker=m, color=COL[k], label=f'{t} N{k}')
    axs[0].set_xscale('symlog', linthresh=10); axs[0].set_xlabel('external load on analog_bus2/3 (pF)')
    axs[0].set_ylabel('firing rate (Hz)'); axs[0].set_title('Bus load: N2, N3 slow down, N0, N1 (buffered) do not', fontsize=9)
    axs[1].set_xlabel('vcplb (V)'); axs[1].set_title('Analog bus coupling (30 pF on the buses)', fontsize=9)
    for a in axs:
        a.grid(alpha=0.3); a.legend(fontsize=7)
    fig.tight_layout(); fig.savefig(os.path.join(RES, 'busload.png'), dpi=120)
    # 3. rasters of the coupling cases
    for group, names in [('syn01', ['syn01_none', 'syn01_weak', 'syn01_strong', 'syn01_both']),
                         ('mutual', ['mutual_none', 'mutual_mutual_weak', 'mutual_mutual_strong']),
                         ('gap', ['gap_off', 'gap_weak', 'gap_strong', 'gap_both', 'gap_both_v0.6', 'gap_both_v0.9']),
                         ('bus23', ['bus23_off', 'bus23_weak', 'bus23_strong', 'bus23_strong_30p'])]:
        for t in tags:
            rs = [(n, R[t][n]) for n in names if n in R[t] and R[t][n].get('ok')]
            if not rs:
                continue
            fig, axs = plt.subplots(len(rs), 1, figsize=(10, 1.6 * len(rs) + 0.6), sharex=True)
            axs = np.atleast_1d(axs)
            for a, (n, r) in zip(axs, rs):
                lk = r['lock01'] if group != 'bus23' else r['lock23']
                raster(a, r, f"{t} {n}: f = " + ', '.join(f'{x:.2f}' for x in r['f']) +
                       f" Hz;  ratio {lk['ratio']:.2f}, vector strength {lk['vs']:.2f}", r.get('tstop', 2.5))
            fig.tight_layout(); fig.savefig(os.path.join(RES, f'{group}_{t}.png'), dpi=110)
    # table
    with open(os.path.join(RES, 'results.md'), 'w') as f:
        f.write('| case | tag | f N0 | f N1 | f N2 | f N3 (Hz) | N0:N1 ratio | VS01 | N2:N3 ratio | VS23 | I(vdd) avg |\n')
        f.write('|---|---|---|---|---|---|---|---|---|---|---|\n')
        for t in tags:
            for n in sorted(R[t]):
                r = R[t][n]
                if not r.get('ok'):
                    f.write(f"| {n} | {t} | failed: {r.get('error', '')[:60]} | | | | | | | | |\n")
                    continue
                fN = ' | '.join(f'{x:.2f}' for x in r['f'])
                f.write(f"| {n} | {t} | {fN} | {r['lock01']['ratio']:.2f} | {r['lock01']['vs']:.2f} | "
                        f"{r['lock23']['ratio']:.2f} | {r['lock23']['vs']:.2f} | {r['iavg'] * 1e9:.0f} nA |\n")
    print('figures and results.md in', RES)


if __name__ == '__main__':
    main()

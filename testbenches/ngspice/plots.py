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


def fmed(r, k):
    """Rate of a free-running neuron: 1 / median spike interval after t0. Unlike the mean rate (r['f']) it
    ignores the rare spurious early spike of the transient solver (one each in 4 of about 70 runs, e.g.
    post-layout busload_0p: N0 and N1 together at 1.2953 s, 76 ms into a 110 ms ramp)."""
    sp = np.array(r['spikes'][k])
    sp = sp[sp > r.get('t0', 0.3)]
    return 1.0 / np.median(np.diff(sp)) if len(sp) >= 4 else r['f'][k]


def tuning(R, ax, label, marker='o'):
    pts = {}
    # tune_low (all codes 0, 5 s) last, so its longer run sets the code-0 points
    for name in sorted((n for n in R if n.startswith('tune_')), key=lambda n: n == 'tune_low'):
        r = R[name]
        if not r.get('ok'):
            continue
        codes = [0, 0, 0, 0] if name == 'tune_low' else list(map(int, name.split('_')[1:]))
        for k in range(4):
            if r['f'][k] > 0:              # 0: fewer than two spikes in the run, no rate
                pts[(k, codes[k])] = fmed(r, k)
    for k in range(4):
        p = sorted((c, f) for (kk, c), f in pts.items() if kk == k)
        if p:
            ax.plot(*zip(*p), marker=marker, color=COL[k],
                    label=f'{label} N{k}' + {2: ' (3 pF bus)', 3: ' (10 nF on the bus)'}.get(k, ''))
    ax.set_xlabel('tuning code (dig_in)'); ax.set_ylabel('firing rate (Hz)'); ax.grid(alpha=0.3)


def tuning_n3(R, ax, label, marker='o', ls='-'):
    """N3 alone on the bare bus (3 pF): audio rates."""
    p = sorted((int(n.split('_')[2]), fmed(r, 3)) for n, r in R.items() if n.startswith('n3_tune_') and r.get('ok'))
    if p:
        ax.plot(*zip(*p), marker=marker, color=COL[3], ls=ls, ms=8 if ls == 'none' else 5,
                label=f'{label} N3 (3 pF bus)')
    ax.set_yscale('log'); ax.set_xlabel('tuning code (dig_in)'); ax.set_ylabel('firing rate (Hz)'); ax.grid(alpha=0.3)


C1, C3 = 10.0, 3.0      # pF: membrane capacitor XC1; analog bus line on chip + pad (estimate, as in campaign.py)


def cval(lab):
    """'10p' / '1n' -> pF"""
    return float(lab[:-1]) * (1e3 if lab.endswith('n') else 1.0)


def busload(R, tags, ax):
    """Firing rate vs bus capacitance (log-log) of N2 (pA, busload_*) and N3 (nA, n3_busload_*), with the 1/C
    prediction from the unloaded point; returns the sensitivity rows."""
    rows = []
    for t, m in zip(tags, ['o', 's']):
        for k, prefix in [(2, 'busload_'), (3, 'n3_busload_')]:
            pts = sorted((cval(n[len(prefix):]), fmed(r, k) if r['f'][k] > 0 else 0.0) for n, r in R[t].items()
                         if n.startswith(prefix) and r.get('ok'))
            if not pts:
                continue
            cbus = np.array([C3 + p[0] for p in pts])
            f = np.array([p[1] if p[1] > 0 else np.nan for p in pts])
            # post-layout: markers only (fewer points; a line between them would suggest values in between)
            ax.plot(cbus, f, marker=m, color=COL[k], ls='-' if t == tags[0] else 'none', ms=5 if t == tags[0] else 8,
                    label=f'{t} N{k}' + (' (pA neuron)' if k == 2 else ' (nA neuron)'))
            ok = np.isfinite(f)
            fit = ok & (cbus <= 2e4)       # up to 10 nF: at 100 nF N3's reset is incomplete (README)
            if fit.sum() >= 2:
                expo = np.polyfit(np.log(C1 + cbus[fit]), np.log(f[fit]), 1)[0]
                rows.append((t, k, list(zip(cbus[ok], f[ok])), expo))
            if t == tags[0] and pts[0][0] == 0 and pts[0][1] > 0:
                cc = np.geomspace(cbus.min(), cbus.max(), 50)
                ax.plot(cc, pts[0][1] * (C1 + C3) / (C1 + cc), color=COL[k], lw=0.8, ls=':',
                        label=f'N{k}: f(3 pF) x 13 pF / (10 pF + C_bus)')
    ax.axhspan(1, 20, color='#f2e6a0', alpha=0.4, lw=0)
    ax.set_xscale('log'); ax.set_yscale('log')
    ax.set_xlabel('capacitance on analog_bus2/3: 3 pF line + external load (pF)')
    ax.set_ylabel('firing rate (Hz)')
    ax.set_title('Bus capacitance sets the rate (code 6); shaded: 1 .. 20 Hz', fontsize=9)
    return rows


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
    # 1. tuning: all four (N3 blinking on 10 nF) and N3 alone at audio rates
    fig, axs = plt.subplots(1, 2, figsize=(11, 4.5))
    for t, m in zip(tags, ['o', 's']):
        tuning(R[t], axs[0], t, m)
        tuning_n3(R[t], axs[1], t, m, '-' if t == tags[0] else 'none')
    axs[0].legend(fontsize=7, ncol=2); axs[0].set_title('Tuning: firing rate vs. 4-bit code (N3 with 10 nF on its bus)', fontsize=9)
    axs[1].legend(fontsize=7); axs[1].set_title('N3 (nA neuron) on the bare bus: audio rates', fontsize=9)
    fig.tight_layout(); fig.savefig(os.path.join(RES, 'tuning.png'), dpi=120)
    # 2. bus load and vcplb
    fig, axs = plt.subplots(1, 2, figsize=(11, 4.2))
    sens = busload(R, tags, axs[0])
    for t, m in zip(tags, ['o', 's']):
        pts = sorted((float(n.split('_')[1]), r['f']) for n, r in R[t].items() if n.startswith('vcplb_') and r.get('ok'))
        if pts:
            v = [p[0] for p in pts]
            axs[1].plot(v, [p[1][2] if p[1][2] > 0 else np.nan for p in pts], marker=m, color=COL[2], label=f'{t} N2')
            axs[1].plot(v, [p[1][3] if p[1][3] > 0 else np.nan for p in pts], marker=m, color=COL[3],
                        label=f'{t} N3 (code 0, 10 nF on bus3)')
    axs[1].set_yscale('log'); axs[1].set_ylabel('firing rate (Hz)')
    axs[1].set_xlabel('vcplb (V)'); axs[1].set_title('Bus pass gates (vcplb): N2 with 30 pF on bus2, N3 with 10 nF on bus3',
                                                    fontsize=9)
    for a in axs:
        a.grid(alpha=0.3); a.legend(fontsize=7)
    fig.tight_layout(); fig.savefig(os.path.join(RES, 'busload.png'), dpi=120)
    # 3. rasters of the coupling cases
    for group, names in [('syn01', ['syn01_none', 'syn01_weak', 'syn01_strong', 'syn01_both']),
                         ('mutual', ['mutual_none', 'mutual_mutual_weak', 'mutual_mutual_strong']),
                         ('gap', ['gap_off', 'gap_weak', 'gap_strong', 'gap_both', 'gap_both_v0.3', 'gap_both_v0.4',
                                  'gap_both_v0.5', 'gap_both_v0.6', 'gap_both_v0.9']),
                         ('bus23', ['bus23_off', 'bus23_weak', 'bus23_strong', 'bus23_strong_30p'])]:
        for t in tags:
            rs = [(n, R[t][n]) for n in names if n in R[t] and R[t][n].get('ok')]
            if not rs:
                continue
            fig, axs = plt.subplots(len(rs), 1, figsize=(10, 1.6 * len(rs) + 0.6), sharex=True)
            axs = np.atleast_1d(axs)
            for a, (n, r) in zip(axs, rs):
                lk = r['lock01'] if group != 'bus23' else r['lock23']
                raster(a, r, f"{t} {n}: f = " + ', '.join(f'{x:.2f}' if x > 0 else '-' for x in r['f']) +
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
                fN = ' | '.join(f'{x:.2f}' if x > 0 else f'< 2 spikes in {r.get("tstop", 2.5):g} s' for x in r['f'])
                f.write(f"| {n} | {t} | {fN} | {r['lock01']['ratio']:.2f} | {r['lock01']['vs']:.2f} | "
                        f"{r['lock23']['ratio']:.2f} | {r['lock23']['vs']:.2f} | {r['iavg'] * 1e9:.0f} nA |\n")
        f.write('\nRates in the table above: spikes after t0 / time (mean rate). Below and in tuning.png / busload.png: '
                '1 / median interval, which ignores the rare spurious early spike of the transient solver.\n')
        f.write('\nBus-capacitance sensitivity (code 6; C_bus = 3 pF line + external load). N2: pA neuron, '
                'N3: nA neuron (bbl_neuron_hi). Exponent: slope of ln f vs ln(10 pF + C_bus), fitted up to 10 nF '
                '(at 100 nF N3 does not reset its bus completely); -1 means f is inversely proportional to the '
                'membrane capacitance including the bus.\n\n')
        f.write('| tag | neuron | f (Hz) at C_bus (pF) | exponent |\n|---|---|---|---|\n')
        for t, k, pts, expo in sens:
            f.write(f"| {t} | N{k} | " + ', '.join(f'{fv:.4g} @ {c:g}' for c, fv in pts) + f" | {expo:.2f} |\n")
        f.write('\nN3 alone (n3_* cases): rate (1 / median interval), swing of analog_bus3 after t0, supply current '
                'of the slot.\n\n')
        f.write('| case | tag | code | C on bus3 | pad leakage | f N3 (Hz) | bus3 min .. max (V) | I(vdd) avg |\n'
                '|---|---|---|---|---|---|---|---|\n')
        for t in tags:
            for n in sorted(x for x in R[t] if x.startswith('n3_')):
                r = R[t][n]
                if not r.get('ok'):
                    f.write(f"| {n} | {t} | failed: {r.get('error', '')[:60]} | | | | | |\n")
                    continue
                b = r.get('bus3_range', [np.nan, np.nan])
                f.write(f"| {n} | {t} | {(r['dig'] >> 12) & 15} | {r.get('cbus', [C3 * 1e-12] * 4)[3] * 1e12:g} pF | {'yes' if r.get('pad') else ''} "
                        f"| {fmed(r, 3):.4g} | {b[0]:.2f} .. {b[1]:.2f} | {r['iavg'] * 1e9:.0f} nA |\n")
    print('figures and results.md in', RES)


if __name__ == '__main__':
    main()

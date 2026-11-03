"""Assign every Okapi symbol, local label and text to a named region of its sheet,
and verify that no wire crosses a region boundary.

usage: pages_regions.py <KiCAD-10import dir> <out regions.json> [--dump]

A region is a rectangle on one sheet (sheet mm, x right, y down). The regions
are the rigid blocks that a re-paging may move as a group. The script reports,
for each sheet, every wire whose two ends fall in different regions (a cut wire)
and every symbol with a pin in a region other than its anchor's (a cut through
a symbol body, which the wire test alone misses: R18 on Okapi_3 at y=175.26
with pins at 170.18 and 180.34 straddled the first y=176 cut). --dump prints every symbol with its
region, sorted, so that finer cuts can be chosen.
"""
import sys, json, os
sys.path.insert(0, '/home/awickert/Dropbox/NorthernWidget/github/NW-Tests/kicad')
from sexp import parse, kids, kid
from sch_walk import Sheet

INF = 1e9
# name: (sheet, x0, x1, y0, y1) or a list of them; half-open on the upper bound
REGIONS = {
    # Okapi_1 (power): three columns, the middle and right columns each cut once
    'S1L_T':  ('Okapi_1', -INF, 170, -INF, 95),    # LOGO1, U39 MIC94094, U1 TLV61220 boost (5V_LP)
    'S1L_B':  ('Okapi_1', -INF, 170, 95, INF),     # U2 TPS6282 (3V3_AUX), U3 TPS61032 (5V_AUX), U13, Q7
    'S1M_T':  ('Okapi_1', 170, 295, -INF, 100),    # S5 start button, U5 BQ2980 + Q1, Q2
    'S1M_B':  [('Okapi_1', 170, 295, 100, INF),    # U4 LT3652 solar charger, Q8
               ('Okapi_1', 148, 170, 116, 128)],   # + the solar input strip D1, R74 (R74 straddled x=170)
    'S1R_T':  ('Okapi_1', 295, INF, -INF, 135),    # U37, U6, U7 + Q5, U9, Q6
    'S1R_B':  ('Okapi_1', 295, INF, 135, INF),     # Q3, U8 TPL5111 + JP8, U10
    # Okapi_2: switched sensor power (left) and USB (right), each cut once
    'S2L_T':  ('Okapi_2', -INF, 190, -INF, 160),   # S1, S2, U11, U12, U14, U15, U17-U20, JP1-JP4
    'S2L_B':  ('Okapi_2', -INF, 172, 160, INF),    # U16, U21, U22
    'S2R_T':  ('Okapi_2', 190, INF, -INF, 150),    # J10 USB-C, F1, U23 FT231X, D4
    'S2R_B':  ('Okapi_2', 172, INF, 150, INF),     # U40 XOR (pins at 182.88, its labels at 177.8), U$1, U$2 VDIV-JP
    # Okapi_3: processor
    'S3UL':   ('Okapi_3', -INF, 222, -INF, 176),   # J9 B-series module, S6, S7, USB2, F2, U35 FRAM
    'S3LAD':  ('Okapi_3', 222, INF, -INF, 190),    # U45 PCA9634 + D10-D18 ladder (R18 reaches y=180.34)
    'S3SD':   ('Okapi_3', -INF, 105, 176, 240),    # SD1
    'S3TERM': ('Okapi_3', -INF, 105, 240, INF),    # J1-J4 screw terminals
    'S3MID':  ('Okapi_3', 105, 205, 176, INF),     # JP5, ICSP (ISP1), MS1 FeatherWing, H1-H3, Q4
    'S3LR_T': ('Okapi_3', 205, INF, 176, 245),     # J5-J8 power terminals (battery, solar, V_PRIME)
    'S3LR_B': ('Okapi_3', 205, INF, 245, INF),     # S3 LOG_INT button, D5 indicator LED
    'S4':     ('Okapi_4', -INF, INF, -INF, INF),
    'S5':     ('Okapi_5', -INF, INF, -INF, INF),
    'S6':     ('Okapi_6', -INF, INF, -INF, INF),
}
ORDER = ['S1M_B'] + [k for k in REGIONS if k != 'S1M_B']   # the strip is tested before S1L
RECTS = {k: (v if isinstance(v, list) else [v]) for k, v in REGIONS.items()}
# coarse blocks, as unions of the fine ones (the baseline proposal's cuts)
COARSE = {
    'S1L': ['S1L_T', 'S1L_B'],
    'S1M': ['S1M_T', 'S1M_B'], 'S1R': ['S1R_T', 'S1R_B'], 'S2L': ['S2L_T', 'S2L_B'],
    'S2R': ['S2R_T', 'S2R_B'], 'S3LOW': ['S3TERM', 'S3MID', 'S3LR_T', 'S3LR_B'], 'S3LR': ['S3LR_T', 'S3LR_B'],
}

def region_of(sheet, p):
    x, y = p
    for name in ORDER:
        for s, x0, x1, y0, y1 in RECTS[name]:
            if s == sheet and x0 <= x < x1 and y0 <= y < y1:
                return name
    return None

def crossings(sh, axis, c, lo, hi):
    """Wires of Sheet sh that cross the line axis=c between lo and hi (other axis)."""
    out = []
    i = 0 if axis == 'x' else 1
    j = 1 - i
    for a, b in sh.wires:
        if (a[i] - c) * (b[i] - c) < 0:
            t = (c - a[i]) / (b[i] - a[i])
            o = a[j] + t * (b[j] - a[j])
            if lo <= o < hi:
                out.append((a, b))
    return out

def main():
    if sys.argv[2] == '--cut':
        # pages_regions.py <dir> --cut <sheet> <x|y> <c> <lo> <hi>
        sh = Sheet(os.path.join(sys.argv[1], sys.argv[3] + '.kicad_sch'))
        w = crossings(sh, sys.argv[4], float(sys.argv[5]), float(sys.argv[6]), float(sys.argv[7]))
        print(sys.argv[3:], 'wires crossing:', len(w), w[:6])
        return
    d, out = sys.argv[1], sys.argv[2]
    dump = '--dump' in sys.argv
    res = {'regions': {k: [list(r) for r in v] for k, v in RECTS.items()}, 'syms': {}, 'labels': {}, 'texts': {}, 'cut_wires': [], 'sym_pos': {}}
    for n in range(1, 7):
        name = f'Okapi_{n}'
        sh = Sheet(os.path.join(d, name + '.kicad_sch'))
        for ref, (lib, x, y, rot, mir) in sh.syms.items():
            r = region_of(name, (x, y))
            # a symbol belongs where its pins are; a pin in another region means the
            # cut line passes through the symbol body (the wire test cannot see that)
            pin_regs = {region_of(name, p[3]) for p in sh.pins if p[0] == ref}
            if pin_regs and pin_regs != {r}:
                print('STRADDLE', name, ref, lib, (x, y), 'anchor', r, 'pins', sorted(pin_regs))
                res.setdefault('straddles', []).append([name, ref, r, sorted(pin_regs)])
            res['syms'][ref] = r
            res['sym_pos'][ref] = [x, y, lib]
        for k, lab, at in sh.labels:
            if k == 'label':
                res['labels'].setdefault(lab + '@' + name, []).append([region_of(name, at), at[0], at[1]])
        for t in kids(sh.t, 'text'):
            at = kid(t, 'at')
            p = (float(at[1]), float(at[2]))
            r0 = region_of(name, p)
            res['texts'].setdefault(r0, []).append([t[1], p[0], p[1]])
            # estimated extent: KiCad's stroke font is about one size-width per
            # character; the anchor is the left end unless justified right, and the
            # text runs along +x at rotation 0 and up the sheet at 90
            eff = kid(t, 'effects')
            font = kid(eff, 'font') if eff else None
            size = float(kid(font, 'size')[1]) if font and kid(font, 'size') else 1.27
            just = kid(eff, 'justify') if eff else None
            rot = float(at[3]) if len(at) > 3 else 0.0
            longest = max(len(line) for line in t[1].split('\\n'))
            L = longest * size
            if rot in (0.0, 180.0):
                ends = [(p[0] + L, p[1])] if not (just and 'right' in just) else [(p[0] - L, p[1])]
            else:
                ends = [(p[0], p[1] - L)]
            for e in ends:
                r1 = region_of(name, e)
                if r1 != r0:
                    print(f'TEXT STRADDLE {name} {t[1][:40]!r} at ({p[0]:.1f},{p[1]:.1f}) anchor {r0}, estimated far end ({e[0]:.1f},{e[1]:.1f}) in {r1}')
                    res.setdefault('text_straddles', []).append([name, t[1], r0, r1])
        for a, b in sh.wires:
            ra, rb = region_of(name, a), region_of(name, b)
            if ra != rb:
                res['cut_wires'].append([name, ra, rb, a, b])
        for j in sh.juncs:
            # a junction exactly on a cut line would be ambiguous
            pass
        if dump:
            print('--', name)
            for ref, (lib, x, y, rot, mir) in sorted(sh.syms.items(), key=lambda kv: (kv[1][1], kv[1][2])):
                print(f'  {region_of(name,(x,y)):6s} {ref:6s} ({x:6.1f},{y:6.1f}) {lib}')
    print('symbols', len(res['syms']), 'cut wires', len(res['cut_wires']), 'straddling symbols', len(res.get('straddles', [])))
    for w in res['cut_wires']:
        print('  CUT', w)
    from collections import Counter
    print('symbols per region', dict(Counter(res['syms'].values())))
    for k, v in sorted(res['labels'].items()):
        regs = {x[0] for x in v}
        print(f'  local label {k}: {len(v)} instances in {sorted(regs)}' + ('  SPLIT' if len(regs) > 1 else ''))
    json.dump(res, open(out, 'w'), indent=1)

if __name__ == '__main__':
    main()

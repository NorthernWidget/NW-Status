"""Rigid-growth scenarios for Margay v4. For each: which footprints translate (whole, with the edge),
the new outline (rectangle, corner radii ignored), which nets are stretched by the move (pads on both a
moved and a fixed footprint; the added length is at least the move distance per net, a lower bound),
and free top/bottom area near the places the v4 parts need. Nothing is saved: the board is read only.
Occupancy follows margay-room31/occ.py (conservative mode): courtyard bbox, else pads+body bbox;
0.15 mm spacing; 0.4 mm edge; through-hole pads block both sides; hole keepout 5.56 mm circle (H1, H2).
Board-level silkscreen is NOT counted here (occ.py counts it). Parts removed by #66/#70 are left out:
U9 U10 R17 R18 C11 C20."""
import pcbnew, numpy as np, math, collections, json, sys
RES = 0.1; MARGIN = 0.15; EDGE = 0.4; HOLE_D = 5.56
REMOVE = {'U9','U10','R17','R18','C11','C20'}
FIXED_ALWAYS = {'H1','H2','U$1','LOGO1'}  # holes keep the mount pattern; U$1 is a drawing, LOGO1 movable art
b = pcbnew.LoadBoard('Margay.kicad_pcb')
X0, X1, Y0, Y1 = 123.4286, 173.5736, 89.8016, 120.2056
fps = {}
for f in b.GetFootprints():
    r = f.GetReference()
    side = 'B' if f.IsFlipped() else 'F'
    cy = f.GetCourtyard(pcbnew.B_CrtYd if f.IsFlipped() else pcbnew.F_CrtYd)
    bb = cy.BBox() if cy.OutlineCount() else f.GetBoundingBox(False)
    box = [pcbnew.ToMM(v) for v in (bb.GetX(), bb.GetY(), bb.GetRight(), bb.GetBottom())]
    pads = []
    for p in f.Pads():
        pb = p.GetBoundingBox(); q = p.GetPosition()
        pads.append(dict(num=p.GetNumber(), net=p.GetNetname(), x=pcbnew.ToMM(q.x), y=pcbnew.ToMM(q.y),
                         box=[pcbnew.ToMM(v) for v in (pb.GetX(), pb.GetY(), pb.GetRight(), pb.GetBottom())],
                         th=p.GetAttribute() in (pcbnew.PAD_ATTRIB_PTH, pcbnew.PAD_ATTRIB_NPTH)))
    p0 = f.GetPosition()
    fps[r] = dict(side=side, box=box, pads=pads, x=pcbnew.ToMM(p0.x), y=pcbnew.ToMM(p0.y))
TRACK = collections.defaultdict(float)
for t in b.GetTracks():
    if t.GetClass() != 'PCB_VIA': TRACK[t.GetNetname()] += pcbnew.ToMM(t.GetLength())

def scenario(name, moves, edges):
    """moves: dict ref -> (dx, dy); edges: (x0, y0, x1, y1) new outline."""
    ex0, ey0, ex1, ey1 = edges
    W, H = ex1 - ex0, ey1 - ey0
    nx, ny = int(W / RES) + 1, int(H / RES) + 1
    top = np.zeros((ny, nx), bool); bot = np.zeros((ny, nx), bool)
    def mark(g, xa, ya, xb, yb, m=MARGIN):
        i0 = max(0, int((xa - m - ex0) / RES)); i1 = min(nx, int((xb + m - ex0) / RES) + 1)
        j0 = max(0, int((ya - m - ey0) / RES)); j1 = min(ny, int((yb + m - ey0) / RES) + 1)
        if i1 > i0 and j1 > j0: g[j0:j1, i0:i1] = True
    yy, xx = np.mgrid[0:ny, 0:nx]; XX = ex0 + (xx + 0.5) * RES; YY = ey0 + (yy + 0.5) * RES
    placed = {}
    for r, f in fps.items():
        if r in REMOVE or r in ('U$1', 'LOGO1'): continue
        dx, dy = moves.get(r, (0, 0))
        if r in ('H1', 'H2'):
            k = (XX - (f['x'] + dx))**2 + (YY - (f['y'] + dy))**2 <= (HOLE_D / 2)**2
            top |= k; bot |= k; placed[r] = (f['x'] + dx, f['y'] + dy); continue
        bx = [f['box'][0] + dx, f['box'][1] + dy, f['box'][2] + dx, f['box'][3] + dy]
        mark(bot if f['side'] == 'B' else top, *bx)
        for p in f['pads']:
            if p['th']:
                pb = p['box']; mark(top if f['side'] == 'B' else bot, pb[0] + dx, pb[1] + dy, pb[2] + dx, pb[3] + dy)
        placed[r] = bx
    e = int(round(EDGE / RES))
    for g in (top, bot):
        g[:e, :] = True; g[-e:, :] = True; g[:, :e] = True; g[:, -e:] = True
    # overlap check: moved footprints against fixed ones (same side), and against hole keepouts
    clash = []
    for r, bx in placed.items():
        if r in ('H1', 'H2') or r not in moves: continue
        for h in ('H1', 'H2'):
            hx, hy = placed[h]
            cx = min(max(hx, bx[0]), bx[2]); cy_ = min(max(hy, bx[1]), bx[3])
            if math.hypot(cx - hx, cy_ - hy) < HOLE_D / 2: clash.append(f'{r} on {h} keepout')
        for s, bs in placed.items():
            if s in moves or s in ('H1', 'H2') or fps[s]['side'] != fps[r]['side']: continue
            if bx[0] < bs[2] and bs[0] < bx[2] and bx[1] < bs[3] and bs[1] < bx[3]: clash.append(f'{r} on {s}')
        if bx[0] < ex0 + EDGE or bx[2] > ex1 - EDGE or bx[1] < ey0 - 1.5 or bx[3] > ey1 - EDGE:
            clash.append(f'{r} past edge')
    # stretched nets
    side_of = collections.defaultdict(set)
    for r, f in fps.items():
        if r in REMOVE: continue
        for p in f['pads']:
            if p['net']: side_of[p['net']].add(moves.get(r, (0, 0)))
    stretched = []
    for n, s in side_of.items():
        if len(s) > 1 and n != 'GND':
            dmax = max(abs(a[0] - c[0]) + abs(a[1] - c[1]) for a in s for c in s)
            stretched.append((n, dmax, TRACK[n]))
    stretched.sort(key=lambda t: -t[2])
    # pad positions after the move, for the "need" regions
    P = collections.defaultdict(list)
    for r, f in fps.items():
        if r in REMOVE: continue
        dx, dy = moves.get(r, (0, 0))
        for p in f['pads']: P[(r, p['num'])].append((p['x'] + dx, p['y'] + dy)); P[('net', p['net'])].append((p['x'] + dx, p['y'] + dy)); P[(r, '*')].append((p['x'] + dx, p['y'] + dy))
    def near(pts, rad):
        k = np.zeros_like(top)
        for (px, py) in pts: k |= (XX - px)**2 + (YY - py)**2 <= rad**2
        return k
    NEED = {
      'J2 pins, 8 mm (J2 ESD and series R)': near(P[('J2', '*')], 8),
      'U1 pins 7, 8 (crystal), 5 mm': near(P[('U1', '7')] + P[('U1', '8')], 5),
      'U1 center, 10 mm': near([(fps['U1']['x'] + moves.get('U1', (0, 0))[0], fps['U1']['y'] + moves.get('U1', (0, 0))[1])], 10),
      'power nets VUSB/VBAT+/VMAIN pads, 6 mm (#66)': near(P[('net', 'VUSB')] + P[('net', 'VBAT+')] + P[('net', '/Power_Sensors/VMAIN')], 6),
      'J3 pins, 6 mm (J3 ESD)': near(P[('J3', '*')], 6),
      'J4 pins, 6 mm (USB ESD)': near([q for (k, v) in P.items() if k[0] == 'J4' and k[1] != '*' for q in v], 6),
      'RTC1, 6 mm (clock)': near(P[('RTC1', '*')], 6),
    }
    inside = (XX >= ex0) & (XX <= ex1) & (YY >= ey0) & (YY <= ey1)
    A = RES * RES
    out = dict(name=name, outline=f'{W:.3f} x {H:.3f}', moved=sorted(moves), clash=clash,
               free_top=round(float((~top).sum() * A), 1), free_bot=round(float((~bot).sum() * A), 1),
               stretched=[(n, round(d, 2), round(t, 1)) for n, d, t in stretched],
               stretch_sum=round(sum(d for _, d, _ in stretched), 1),
               need={k: (round(float((~top & v).sum() * A), 1), round(float((~bot & v).sum() * A), 1)) for k, v in NEED.items()})
    np.save(f'occ_{name}_top.npy', top); np.save(f'occ_{name}_bot.npy', bot)
    return out

def sel(rule):
    return [r for r, f in fps.items() if r not in FIXED_ALWAYS and r not in REMOVE and rule(f)]
DY_T = 40.64 - 30.404; DX_T = 50.8 - 50.145      # 50.8 x 40.64
DX_L = 68.58 - 50.145                           # 68.58 x 30.404
DX_B, DY_B = 58.42 - 50.145, 35.56 - 30.404     # 58.42 x 35.56
S = []
S.append(scenario('S0_today', {}, (X0, Y0, X1, Y1)))
S.append(scenario('A0_taller_strip', {}, (X0, Y0, X1 + DX_T, Y1 + DY_T)))
lower = sel(lambda f: f['box'][1] >= 109.0 and f['side'] == 'F') + ['J3', 'JP2']
S.append(scenario('A1_taller_lower_row_down', {r: (0, DY_T) for r in set(lower)}, (X0, Y0, X1 + DX_T, Y1 + DY_T)))
right = sel(lambda f: f['box'][0] >= 166.0)
S.append(scenario('B1_longer_right_column_out', {r: (DX_L, 0) for r in right}, (X0, Y0, X1 + DX_L, Y1)))
S.append(scenario('B2_longer_J2_out_left', {'J2': (-DX_L, 0)}, (X0 - DX_L, Y0, X1, Y1)))
mid = sel(lambda f: f['x'] > 157.9 and f['side'] == 'F') + ['JP2']
S.append(scenario('B3_longer_split_x157.9', {r: (DX_L, 0) for r in set(mid)}, (X0, Y0, X1 + DX_L, Y1)))
both = {r: (0, DY_B) for r in set(sel(lambda f: f['box'][1] >= 109.0 and f['side'] == 'F') + ['J3', 'JP2'])}
for r in sel(lambda f: f['box'][0] >= 166.0):
    both[r] = (DX_B, both.get(r, (0, 0))[1])
S.append(scenario('C1_both_lower_row_down_right_column_out', both, (X0, Y0, X1 + DX_B, Y1 + DY_B)))
json.dump(S, open('scenarios.json', 'w'), indent=1)
for s in S:
    print('=' * 100); print(s['name'], 'outline', s['outline'], 'mm')
    print('  moved:', ' '.join(s['moved']) or '(none)')
    print('  clashes:', s['clash'] or 'none')
    print(f"  free top {s['free_top']} mm2, free bottom {s['free_bot']} mm2 (removed parts excluded; silkscreen not counted)")
    print(f"  stretched nets (excl. GND): {len(s['stretched'])}, sum of minimum added length {s['stretch_sum']} mm")
    for n, d, t in s['stretched']: print(f"     {n:32s} +{d:5.2f} mm  (routed today {t} mm)")
    print('  free area near needs (top, bottom) mm2:')
    for k, v in s['need'].items(): print(f"     {k:48s} {v[0]:7.1f} {v[1]:7.1f}")

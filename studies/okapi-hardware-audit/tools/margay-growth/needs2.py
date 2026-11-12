"""Follow-ups on scenarios.py occupancy grids:
(1) #59: free top area in the band under U1 where the crystal and its caps would move (x 134-146, y 104.4-115).
(2) #57: best free top spot for a BME280 courtyard (3.2 x 2.6 mm, LGA 2.5 x 2.5 plus courtyard; ESTIMATE from today's
    U12 box 3.21 x 2.62), maximizing the smaller of its center distances to U2 (FT231X) and U6 (TPS797 LDO);
    also reported: distance to U7 (3V3_AUX LDO) and to the nearest SCL pad.
(3) free bottom area outside J1, split above/below J1's pad row and right of J1."""
import numpy as np, json, math
S = json.load(open('scenarios.json')); F = {d['ref']: d for d in json.load(open('fps.json'))}
from scenarios import fps, DY_T, DX_T, DX_L, DX_B, DY_B  # noqa: re-runs scenarios (read only)
EDGES = {'S0_today': (123.4286, 89.8016), 'A0_taller_strip': (123.4286, 89.8016), 'A1_taller_lower_row_down': (123.4286, 89.8016),
         'B1_longer_right_column_out': (123.4286, 89.8016), 'B2_longer_J2_out_left': (123.4286 - DX_L, 89.8016),
         'B3_longer_split_x157.9': (123.4286, 89.8016), 'C1_both_lower_row_down_right_column_out': (123.4286, 89.8016)}
RES = 0.1
def moves_of(s):
    import scenarios as sc
    return None
for s in S:
    n = s['name']; top = np.load(f'occ_{n}_top.npy'); bot = np.load(f'occ_{n}_bot.npy'); ex0, ey0 = EDGES[n]
    ny, nx = top.shape
    def sub(g, xa, ya, xb, yb):
        i0 = max(0, int((xa - ex0) / RES)); i1 = min(nx, int((xb - ex0) / RES)); j0 = max(0, int((ya - ey0) / RES)); j1 = min(ny, int((yb - ey0) / RES))
        return g[j0:j1, i0:i1]
    A = RES * RES
    xtal = round(float((~sub(top, 134, 104.4, 146, 115)).sum() * A), 1)
    # moved positions of heat sources
    mv = set(s['moved'])
    def pos(r):
        f = F[r]; dx = dy = 0
        if r in mv:
            if n.startswith('A1'): dy = DY_T
            elif n.startswith('B1') or n.startswith('B3'): dx = DX_L
            elif n.startswith('B2'): dx = -DX_L
            elif n.startswith('C1'):
                dy = DY_B if f['bbox'][1] >= 109.0 or r in ('J3', 'JP2') else 0
                dx = DX_B if f['bbox'][0] >= 166.0 else 0
        return f['x'] + dx, f['y'] + dy
    U2, U6, U7 = pos('U2'), pos('U6'), pos('U7')
    scl = [(p['x'] + (pos(r)[0] - F[r]['x']), p['y'] + (pos(r)[1] - F[r]['y'])) for r, f in fps.items() for p in f['pads'] if p['net'] == 'SCL']
    w, h = 32, 26  # cells
    best = None
    free = ~top
    # integral image for box-free test
    I = np.pad(top.astype(np.int32).cumsum(0).cumsum(1), ((1, 0), (1, 0)))
    for j in range(0, ny - h, 2):
        for i in range(0, nx - w, 2):
            if I[j + h, i + w] - I[j, i + w] - I[j + h, i] + I[j, i]: continue
            cx, cy = ex0 + (i + w / 2) * RES, ey0 + (j + h / 2) * RES
            d = min(math.dist((cx, cy), U2), math.dist((cx, cy), U6))
            if not best or d > best[0]: best = (d, cx, cy)
    d, cx, cy = best
    dscl = min(math.dist((cx, cy), q) for q in scl)
    b_tot = round(float((~bot).sum() * A), 1)
    print(f"{n:42s} #59 free top under U1 {xtal:6.1f} mm2 | #57 best BME spot ({cx:6.1f},{cy:6.1f}) to U2 {math.dist((cx,cy),U2):5.1f} U6 {math.dist((cx,cy),U6):5.1f} U7 {math.dist((cx,cy),U7):5.1f} nearest SCL pad {dscl:5.1f} mm | free bottom {b_tot}")
print('today U12 at', (F['U12']['x'], F['U12']['y']), 'to U2', round(math.dist((F['U12']['x'], F['U12']['y']), (F['U2']['x'], F['U2']['y'])), 2), 'U6', round(math.dist((F['U12']['x'], F['U12']['y']), (F['U6']['x'], F['U6']['y'])), 2))

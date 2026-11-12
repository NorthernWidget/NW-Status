"""How many 2.54 mm screw-terminal positions fit along each edge, per option.
Body length for n positions = (n-1)*2.54 + 3.25 mm, the end allowance measured on today's blocks
(J2: 26.11 mm for 10, J3: 15.95 mm for 6, from fps.txt bboxes: 26.11-22.86 = 3.25, 15.95-12.70 = 3.25).
Depth 6.75 mm (both blocks). Spacing to a keepout or another courtyard 0.15 mm (this study's proposal).
Edge inset 0.4 mm is NOT applied along the wire-entry edge: today's J2 bbox already starts at the edge."""
import math
P = 2.54; END = 3.25; GAP = 0.15
def n_for(length):
    return max(0, math.floor((length - END) / P + 1e-6) + 1)
H1_Y, H_R = 118.047, 5.56 / 2          # H1 center y, keepout radius
H2_Y = 92.012
TOP = 89.8016; J4_BOT = 96.81           # J4 courtyard bottom (fps.txt)
rows = []
def edge(label, a, b, note):
    L = b - a; rows.append((label, round(a, 2), round(b, 2), round(L, 2), n_for(L), note))
for name, H, right_edge_clear in (('today 50.145 x 30.404', 30.404, False), ('taller 50.8 x 40.64', 40.64, False),
                                  ('longer 68.58 x 30.404 (right column out)', 30.404, True), ('both 58.42 x 35.56 (right column out)', 35.56, True)):
    bot = TOP + H - 0.4
    # left edge, J2 column, holes kept: above H1 and (if room) below H1
    edge(f'{name}: left edge above H1', 89.75, 115.86, 'calibrated: today\'s J2 body, which overlaps the H1 screw-head circle by 0.59 mm')
    if bot - (H1_Y + H_R + GAP) > 0:
        edge(f'{name}: left edge below H1', H1_Y + H_R + GAP, bot, 'second block, holes kept')
    # right edge, J3 column
    start = TOP + 0.4 if right_edge_clear else J4_BOT + GAP
    edge(f'{name}: right edge', start, bot, 'J4 and H2 no longer on this edge' if right_edge_clear else 'below J4 courtyard (H2 keepout ends 94.79)')
    # left edge if H1 were moved to the new bottom-left corner (breaks the hole pair)
    if H > 30.5:
        h1n = TOP + H - 2.159
        edge(f'{name}: left edge, H1 moved to the new corner', 89.75, h1n - H_R + 0.59, 'breaks the diagonal pair; same 0.59 mm overlap as today')
for r in rows: print(f"{r[0]:62s} y {r[1]:7.2f}-{r[2]:7.2f}  {r[3]:5.2f} mm -> {r[4]:2d} positions  ({r[5]})")
# long edges
print()
print('bottom long edge, taller: strip under H1 keepout to the J3 column: x 123.83-166.21 ->', n_for(166.21 - 123.83), 'positions (uses 6.75 mm of the 10.24 mm added height)')
print('bottom long edge, longer (right column out 18.435): new band x 166.21-185.05 ->', n_for(185.05 - 166.21), 'positions')
print('top long edge, longer: band right of H2 keepout x 174.36-185.05 ->', n_for(185.05 - 174.36), 'positions')
print('bottom long edge, both (right column out 8.275): x 166.21-176.89 ->', n_for(176.89 - 166.21), 'positions')

"""Does each outline fit on the WH-02 lid plate (MargayMount_WH02_lid.STL), with the diagonal hole pair on its two
standoffs? Plate 54.41 x 78.74 mm, standoffs at (4.28, 13.33) and (50.13, 39.37) mm: numbers from the
convenient-sizes agent report F3 (measured there from the STL; not re-measured here). Board frame: Eagle's, origin at
today's lower-left corner, y up; H1 (2.159, 2.159), H2 (48.006, 28.194). The board may sit either way round (0 or 180
degrees), since the hole pair maps onto itself under a half turn; it cannot be mirrored. Overhang of the plate edge is
reported, not judged: whether the lid cavity allows it is UNVERIFIED (no Polycase drawing read)."""
PW, PH = 54.41, 78.74; S1 = (4.28, 13.33); S2 = (50.13, 39.37); H1 = (2.159, 2.159); H2 = (48.006, 28.194)
def place(x0, y0, x1, y1):
    res = []
    for rot in (0, 180):
        if rot == 0:
            ox, oy = S1[0] - H1[0], S1[1] - H1[1]; X = (x0 + ox, x1 + ox); Y = (y0 + oy, y1 + oy)
        else:
            ox, oy = S2[0] + H1[0], S2[1] + H1[1]; X = (ox - x1, ox - x0); Y = (oy - y1, oy - y0)
        m = min(X[0], PW - X[1], Y[0], PH - Y[1])
        res.append((rot, round(X[0], 2), round(X[1], 2), round(Y[0], 2), round(Y[1], 2), round(m, 2)))
    return res
C = {
 'today 50.145 x 30.404': (0, 0, 50.145, 30.404),
 'taller 50.8 x 40.64 (bottom edge down 10.236, right edge out 0.655)': (0, -10.236, 50.8, 30.404),
 'taller limit: 50.8 x 41.57': (0, -11.17, 50.8, 30.404),
 'longer 68.58 x 30.404, right edge out': (0, 0, 68.58, 30.404),
 'longer 68.58 x 30.404, left edge out (J2 moves)': (-18.435, 0, 50.145, 30.404),
 'both 58.42 x 35.56 (bottom down 5.156, right out 8.275)': (0, -5.156, 58.42, 30.404),
 'both, within the plate: 52.29 x 41.57': (0, -11.17, 52.29, 30.404),
}
for k, v in C.items():
    for rot, xa, xb, ya, yb, m in place(*v):
        print(f"{k:70s} rot {rot:3d}: plate x {xa:6.2f}-{xb:6.2f} y {ya:6.2f}-{yb:6.2f}  smallest margin {m:6.2f} mm {'FITS' if m >= 0 else 'OVERHANGS'}")

"""Measure the printed ink of each region from the rasterized schematic.

usage: pages_ink.py <regions.json> <png dir> <out ink.json> [--rewrap]

The PNGs come from
  kicad-cli sch export pdf -e -n --black-and-white -o okapi.pdf Okapi.kicad_sch
  pdftoppm -r 100 -png okapi.pdf pg
so page N of the PDF is pg-N.png, pages 2..7 are Okapi_1..Okapi_6, and one
pixel is 0.254 mm (100 dpi) measured from the page's top-left corner, which is
the sheet origin. Ink is any pixel darker than 200. A region's ink is the
bounding box of dark pixels inside the region's rectangle, in mm; because no
wire crosses a region boundary (pages_regions.py), that box is the block's
printed extent, apart from a text item straddling the line.
"""
import sys, json
import numpy as np

# Free text whose printed extent crosses a region boundary is clipped by the
# region rectangle, so its measured extent (raster, same PNGs) is added to the
# block that it belongs to. "Select address" is anchored at x=205.7 in S3UL but
# names the PCA9634 address resistors, so it travels with the ladder. --rewrap
# models the 86-character SDA note re-wrapped onto three lines (text edit) by
# dropping its extension to the right of the S3MID rectangle.
TEXT_EXTENTS = {
    'S1L_B':  ('Okapi_1', 152.8, 206.4, 167.0, 172.1),   # 'Remove LBI pullup??'
    'S3MID':  ('Okapi_3', 157.5, 262.3, 195.8, 199.6),   # 'Jump SDA channels together, ...'
    'S3LAD':  ('Okapi_3', 205.8, 241.9, 136.5, 141.1),   # 'Select address'
}
from PIL import Image

PX = 25.4 / 100.0
PAGE = {'Okapi_1': 2, 'Okapi_2': 3, 'Okapi_3': 4, 'Okapi_4': 5, 'Okapi_5': 6, 'Okapi_6': 7}

def main():
    reg = json.load(open(sys.argv[1]))['regions']
    d = sys.argv[2]
    imgs = {}
    for sh, n in PAGE.items():
        a = np.asarray(Image.open(f'{d}/pg-{n}.png').convert('L'))
        imgs[sh] = a < 200
    out = {}
    def box(sh, x0, x1, y0, y1):
        m = imgs[sh]
        H, W = m.shape
        c0, c1 = max(0, int(x0 / PX)), min(W, int(np.ceil(x1 / PX)))
        r0, r1 = max(0, int(y0 / PX)), min(H, int(np.ceil(y1 / PX)))
        sub = m[r0:r1, c0:c1]
        ys, xs = np.nonzero(sub)
        if len(xs) == 0:
            return None
        X0, X1 = (c0 + xs.min()) * PX, (c0 + xs.max() + 1) * PX
        Y0, Y1 = (r0 + ys.min()) * PX, (r0 + ys.max() + 1) * PX
        return dict(x0=round(X0, 1), x1=round(X1, 1), y0=round(Y0, 1), y1=round(Y1, 1), w=round(X1 - X0, 1), h=round(Y1 - Y0, 1), dark=int(len(xs)))
    for sh in PAGE:
        out['sheet:' + sh] = box(sh, 0, 1e9, 0, 1e9)
    for name, rects in reg.items():
        bs = [b for b in (box(sh, max(0, x0), min(1e8, x1), max(0, y0), min(1e8, y1)) for sh, x0, x1, y0, y1 in rects) if b]
        b = dict(x0=min(q['x0'] for q in bs), x1=max(q['x1'] for q in bs), y0=min(q['y0'] for q in bs), y1=max(q['y1'] for q in bs), dark=sum(q['dark'] for q in bs))
        if name in TEXT_EXTENTS and not ('--rewrap' in sys.argv and name == 'S3MID'):
            _, tx0, tx1, ty0, ty1 = TEXT_EXTENTS[name]
            b = dict(x0=min(b['x0'], tx0), x1=max(b['x1'], tx1), y0=min(b['y0'], ty0), y1=max(b['y1'], ty1), dark=b['dark'])
        b['w'] = round(b['x1'] - b['x0'], 1)
        b['h'] = round(b['y1'] - b['y0'], 1)
        out[name] = b
    for k, v in out.items():
        print(f'{k:14s} {v["w"]:6.1f} x {v["h"]:6.1f} mm   x {v["x0"]:6.1f}..{v["x1"]:6.1f}  y {v["y0"]:6.1f}..{v["y1"]:6.1f}   dark px {v["dark"]}')
    json.dump(out, open(sys.argv[3], 'w'), indent=1)

if __name__ == '__main__':
    main()

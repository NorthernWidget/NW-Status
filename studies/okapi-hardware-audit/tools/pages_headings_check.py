#!/usr/bin/env python3
"""Check every page heading by printed ink, not by anchor.

    pages_headings_check.py <project dir> <scratch dir>

Renders the schematic twice without the drawing sheet (as it is, and with
every heading removed; a heading is a text of Bobby's 5.08 x 4.318 size),
rasterizes both at 100 dpi, and for each heading reports the box its ink
occupies, how many pixels of other ink fall inside that box (overlap), and
the gap from the heading's bottom to the first ink below it within its
width (the block it labels).
"""
import os, re, shutil, subprocess, sys
import numpy as np
from PIL import Image

DPI = 100
K = DPI / 25.4

def render(proj, out):
    subprocess.run(['kicad-cli', 'sch', 'export', 'pdf', '-e', '-n', '--black-and-white', '-o', out, os.path.join(proj, 'Okapi.kicad_sch')], capture_output=True)
    base = out[:-4]
    for f in os.listdir(os.path.dirname(out)):
        if f.startswith(os.path.basename(base) + '-'):
            os.remove(os.path.join(os.path.dirname(out), f))
    subprocess.run(['pdftoppm', '-r', str(DPI), '-png', out, base], capture_output=True)
    pages = sorted([f for f in os.listdir(os.path.dirname(out)) if f.startswith(os.path.basename(base) + '-')], key=lambda s: int(s.rsplit('-', 1)[1][:-4]))
    return [np.asarray(Image.open(os.path.join(os.path.dirname(out), f)).convert('L')) < 200 for f in pages]

def main():
    proj, scratch = sys.argv[1:3]
    a = os.path.join(scratch, 'with'); b = os.path.join(scratch, 'without')
    for d in (a, b):
        shutil.rmtree(d, ignore_errors=True); shutil.copytree(proj, d)
    heads = {}   # sheet uuid order is the page order: read the root's sheet list
    root = open(os.path.join(proj, 'Okapi.kicad_sch')).read()
    # page order is the (page "n") of each sheet symbol, not the file order (KiCad re-sorts sheets on save)
    order = [f for n, f in sorted((int(re.search(r'\(page "(\d+)"', blk).group(1)), re.search(r'\(property "Sheetfile" "([^"]*)"', blk).group(1))
                                   for blk in re.findall(r'\t\(sheet\n(?:.*\n)*?\t\)\n', root))]
    for f in order:
        t = open(os.path.join(b, f)).read()
        hs = re.findall(r'\t\(text "([^"]*)"\n\t\t\(exclude_from_sim no\)\n\t\t\(at ([-\d.]+) ([-\d.]+) 0\)\n\t\t\(effects\n\t\t\t\(font\n\t\t\t\t\(size 5\.08 4\.318\)', t)
        heads[f] = [(h, float(x), float(y)) for h, x, y in hs]
        t2 = re.sub(r'\t\(text "[^"]*"\n\t\t\(exclude_from_sim no\)\n\t\t\(at [-\d.]+ [-\d.]+ 0\)\n\t\t\(effects\n\t\t\t\(font\n\t\t\t\t\(size 5\.08 4\.318\)\n(?:.*\n)*?\t\)\n', '', t)
        open(os.path.join(b, f), 'w').write(t2)
    A = render(a, os.path.join(scratch, 'with.pdf')); B = render(b, os.path.join(scratch, 'without.pdf'))
    for i, f in enumerate(order):
        pa, pb = A[i + 1], B[i + 1]
        mask = pa & ~pb
        for h, x, y in heads[f]:
            y0, y1 = int((y - 7) * K), int((y + 2) * K)
            # this heading's own ink: columns from its anchor rightwards until 5 mm of empty columns
            cols = mask[y0:y1, int(x * K):].any(axis=0)
            last = None; empty = 0
            for c, v in enumerate(cols):
                if v: last = c; empty = 0
                else:
                    empty += 1
                    if last is not None and empty > 5 * K: break
            if last is None:
                print('%-16s %-28s NOT FOUND in the render' % (f[:-10], h)); continue
            sub = mask[y0:y1, int(x * K):int(x * K) + last + 1]
            ys, xs = np.where(sub)
            bx0, bx1 = int(x * K) + xs.min(), int(x * K) + xs.max(); by0, by1 = y0 + ys.min(), y0 + ys.max()
            pad = int(1 * K)
            overlap = pb[by0 - pad:by1 + pad, bx0 - pad:bx1 + pad].sum()
            below = pb[by1:, bx0:bx1 + 1]
            rows = np.where(below.any(axis=1))[0]
            gap = (rows[0] / K) if len(rows) else None
            print('%-16s %-28s ink x %5.1f..%5.1f y %5.1f..%5.1f  overlap px %4d  gap to ink below %s' % (f[:-10], h, bx0 / K, bx1 / K, by0 / K, by1 / K, overlap, '%.1f mm' % gap if gap is not None else 'none'))

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Every annotation on every page that prints over something else.

    pages_collisions.py <project dir> <scratch dir> [--json out.json]

For each page, renders it four ways without the drawing sheet at 100 dpi:
(A) as it is, (B) without its labels and free texts, (C) without its wires,
(N) without its labels. Annotation ink = A and not B, taken as connected
components; a component that has B-ink inside its box (padded 0.3 mm)
collides with a part, a wire or another annotation's remains, and is named
by the nearest label or text anchor. A note (N and not B) with label ink
(A and not N) inside its padded box collides with that label and is reported
under the note (kind t), so the fixer moves the note. Wires over symbol bodies: wire ink = A and not C, flagged where it
runs through a symbol's box away from the box's edge (pin ends sit on the
edge). Prints one line per collision and a count per page.
"""
import json, os, re, shutil, subprocess, sys
import numpy as np
from PIL import Image
from scipy import ndimage

DPI = 100
K = DPI / 25.4

def strip(t, kinds):
    for k in kinds:
        t = re.sub(r'^\t\(%s(?: "[^"]*")?\n(?:.*\n)*?\t\)\n' % k, '', t, flags=re.M)
    return t

def render(proj, sheet, out_png):
    tmp = os.path.join(os.path.dirname(out_png), 'tmp_' + os.path.basename(out_png)[:-4])
    shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
    open(os.path.join(tmp, 'p.kicad_sch'), 'w').write(sheet)
    for f in ('fp-lib-table', 'sym-lib-table'):
        if os.path.exists(os.path.join(proj, f)): shutil.copy(os.path.join(proj, f), tmp)
    subprocess.run(['kicad-cli', 'sch', 'export', 'pdf', '-e', '-n', '--black-and-white', '-o', os.path.join(tmp, 'p.pdf'), os.path.join(tmp, 'p.kicad_sch')], capture_output=True)
    subprocess.run(['pdftoppm', '-r', str(DPI), '-png', '-singlefile', os.path.join(tmp, 'p.pdf'), out_png[:-4]], capture_output=True)
    return np.asarray(Image.open(out_png).convert('L')) < 200

def anchors(t):
    out = []
    for m in re.finditer(r'^\t\((global_label|label|hierarchical_label|text) "([^"]*)"\n(?:\t\t\(shape \w+\)\n)?(?:\t\t\(exclude_from_sim no\)\n)?\t\t\(at ([-\d.]+) ([-\d.]+)', t, re.M):
        out.append((m.group(1)[:1], m.group(2)[:24], float(m.group(3)), float(m.group(4))))
    return out

def main():
    proj, scratch = sys.argv[1:3]
    os.makedirs(scratch, exist_ok=True)
    root = open(os.path.join(proj, 'Okapi.kicad_sch')).read()
    order = [f for n, f in sorted((int(re.search(r'\(page "(\d+)"', b).group(1)), re.search(r'\(property "Sheetfile" "([^"]*)"', b).group(1)) for b in re.findall(r'\t\(sheet\n(?:.*\n)*?\t\)\n', root))]
    total = {}
    report = {}
    for f in order:
        t = open(os.path.join(proj, f)).read()
        A = render(proj, t, os.path.join(scratch, f[:-10] + '_A.png'))
        B = render(proj, strip(t, ['global_label', 'label', 'hierarchical_label', 'text']), os.path.join(scratch, f[:-10] + '_B.png'))
        C = render(proj, strip(t, ['wire', 'bus', 'junction']), os.path.join(scratch, f[:-10] + '_C.png'))
        ann = A & ~B
        lab, n = ndimage.label(ann)
        boxes = ndimage.find_objects(lab)
        an = anchors(t)
        hits = []
        pad = int(0.3 * K)
        for i, sl in enumerate(boxes):
            if sl is None: continue
            ys, xs = sl
            if (ys.stop - ys.start) < 2 or (xs.stop - xs.start) < 2: continue
            under = B[max(0, ys.start - pad):ys.stop + pad, max(0, xs.start - pad):xs.stop + pad]
            if under.sum() == 0: continue
            cx, cy = (xs.start + xs.stop) / 2 / K, (ys.start + ys.stop) / 2 / K
            near = min(an, key=lambda a: (a[2] - cx) ** 2 + (a[3] - cy) ** 2) if an else ('?', '?', 0, 0)
            hits.append((near[0], near[1], round(cx, 1), round(cy, 1), int(under.sum())))
        # notes against labels
        N = render(proj, strip(t, ['global_label', 'label', 'hierarchical_label']), os.path.join(scratch, f[:-10] + '_N.png'))
        notes = N & ~B; labels_ink = A & ~N
        nlab, nn = ndimage.label(notes)
        tan = [a for a in an if a[0] == 't']
        for sl in ndimage.find_objects(nlab):
            if sl is None: continue
            ys, xs = sl
            if (ys.stop - ys.start) < 2 or (xs.stop - xs.start) < 2: continue
            under = labels_ink[max(0, ys.start - pad):ys.stop + pad, max(0, xs.start - pad):xs.stop + pad]
            if under.sum() == 0 or not tan: continue
            cx, cy = (xs.start + xs.stop) / 2 / K, (ys.start + ys.stop) / 2 / K
            near = min(tan, key=lambda a: (a[2] - cx) ** 2 + (a[3] - cy) ** 2)
            hits.append(('t', near[1], round(cx, 1), round(cy, 1), int(under.sum())))
        # merge hits on the same annotation
        merged = {}
        for k, name, cx, cy, px in hits:
            key = (k, name, round(cx / 10), round(cy / 10))
            merged[key] = merged.get(key, 0) + px
        # wires over symbol bodies: wire ink inside a symbol component's box, away from its edge
        # fields (Reference and Value texts) over wires or parts: render with every field hidden
        th = re.sub(r'(\t\t\(property "(?:Reference|Value)" "[^"]*"\n\t\t\t\(at [^)]*\)\n)(?!\t\t\t\(hide yes\))', r'\1\t\t\t(hide yes)\n', t)
        D = render(proj, th, os.path.join(scratch, f[:-10] + '_D.png'))
        fld = A & ~D & ~ann
        flab, fn = ndimage.label(fld)
        fhits = 0
        for sl in ndimage.find_objects(flab):
            if sl is None: continue
            ys, xs = sl
            if (ys.stop - ys.start) < 2 or (xs.stop - xs.start) < 2: continue
            under = D[max(0, ys.start - pad):ys.stop + pad, max(0, xs.start - pad):xs.stop + pad]
            if under.sum() >= 8: fhits += 1
        wires = A & ~C
        symb = C & ~(A & ~B)       # parts: no labels, no wires (texts are gone from C? no: C keeps texts) -> use B minus wires
        parts = B & C              # ink that is neither annotation nor wire
        plab, pn = ndimage.label(ndimage.binary_dilation(parts, iterations=2))
        pboxes = ndimage.find_objects(plab)
        wover = 0
        for sl in pboxes:
            if sl is None: continue
            ys, xs = sl
            if (ys.stop - ys.start) < 4 * K or (xs.stop - xs.start) < 4 * K: continue   # a body, not a stub
            inner = wires[ys.start + int(K):ys.stop - int(K), xs.start + int(K):xs.stop - int(K)]
            if inner.size and inner.sum() > 2 * K:
                wover += 1
        name = f[:-10]
        report[name] = [list(k) + [v] for k, v in merged.items()]
        big = sum(1 for v in merged.values() if v >= 30)
        total[name] = (big, fhits, wover)
        print('%-20s labels/notes colliding (>=30 px): %3d   fields over wires or parts: %3d   symbol boxes with a wire through them: %2d' % (name, big, fhits, wover))
        for (k, nm, _, _), v in sorted(merged.items(), key=lambda x: -x[1])[:6]:
            print('      %s %-24s %5d px' % (k, nm, v))
    print('TOTAL labels/notes %d, fields %d, wire-over-symbol boxes %d' % (sum(v[0] for v in total.values()), sum(v[1] for v in total.values()), sum(v[2] for v in total.values())))
    if '--json' in sys.argv:
        json.dump(report, open(sys.argv[sys.argv.index('--json') + 1], 'w'), indent=1)

if __name__ == '__main__':
    main()

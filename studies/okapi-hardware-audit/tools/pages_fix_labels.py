#!/usr/bin/env python3
"""Turn or slide every global label whose flag prints over a wire or a part.

    pages_fix_labels.py <project dir> <scratch dir> <collisions.json> [--min PX]

For each colliding global label (from pages_collisions.py, >= PX, default 30)
the candidates are its anchor and the far end of the wire it sits on, each at
the four angles (0 and 90 with justify left, 180 and 270 with justify right),
and the anchor pushed two or four ticks further out along that wire with the
wire lengthened to meet it (a label that sits on a pin whose name prints
outside the body has nowhere else to go). Each candidate is rendered over the
page without that one annotation (every other label, note and field kept)
and the one with the least ink under its flag wins; ties keep the current placement, then the shorter wire. A candidate
whose flag leaves the printable area (4 mm inside the border) is dropped. A
label is moved only along its own wire, so no net changes. A colliding note
(kind t) is nudged instead: up to eight ticks along either axis, least ink
then shortest move. Every touched sheet is re-saved through kicad-cli; run
the gate afterwards.
"""
import json, os, re, shutil, subprocess, sys
import numpy as np
from PIL import Image
from scipy import ndimage

DPI = 100
K = DPI / 25.4

def fmt(v):
    s = ('%.6f' % v).rstrip('0').rstrip('.')
    return '0' if s in ('-0', '') else s

def render(proj, sheet, tmpdir, tag):
    os.makedirs(tmpdir, exist_ok=True)
    open(os.path.join(tmpdir, 'p.kicad_sch'), 'w').write(sheet)
    for f in ('fp-lib-table', 'sym-lib-table'):
        if os.path.exists(os.path.join(proj, f)) and not os.path.exists(os.path.join(tmpdir, f)): shutil.copy(os.path.join(proj, f), tmpdir)
    subprocess.run(['kicad-cli', 'sch', 'export', 'pdf', '-e', '-n', '--black-and-white', '-o', os.path.join(tmpdir, tag + '.pdf'), os.path.join(tmpdir, 'p.kicad_sch')], capture_output=True)
    subprocess.run(['pdftoppm', '-r', str(DPI), '-png', '-singlefile', os.path.join(tmpdir, tag + '.pdf'), os.path.join(tmpdir, tag)], capture_output=True)
    return np.asarray(Image.open(os.path.join(tmpdir, tag + '.png')).convert('L')) < 200

LAB = re.compile(r'^\t\((global_label|label) "([^"]*)"\n(\t\t\(shape \w+\)\n)?\t\t\(at ([-\d.]+) ([-\d.]+) (\d+)\)\n((?:.*\n)*?)\t\)\n', re.M)

def set_label(block, x, y, ang):
    block = re.sub(r'\(at [-\d.]+ [-\d.]+ \d+\)', '(at %s %s %d)' % (fmt(x), fmt(y), ang), block, count=1)
    block = re.sub(r'(\t\t\t\(justify )(left|right)', lambda m: m.group(1) + ('left' if ang in (0, 90) else 'right'), block, count=1)
    return block

def ink_under(A, B):
    """pixels of the base render within 0.3 mm of the candidate's own ink; None when that ink leaves the printable area"""
    ink = A & ~B
    lab, n = ndimage.label(ink)
    px = 0
    for sl in ndimage.find_objects(lab):
        if sl is None: continue
        ys, xs = sl; pad = int(0.3 * K)
        if xs.start / K < 8.5 or xs.stop / K > 272.9 or ys.start / K < 8.5 or ys.stop / K > 209.4: return None
        px += int(B[max(0, ys.start - pad):ys.stop + pad, max(0, xs.start - pad):xs.stop + pad].sum())
    return px

WIRE = r'\t\(wire\n\t\t\(pts\n\t\t\t\(xy ([-\d.]+) ([-\d.]+)\) \(xy ([-\d.]+) ([-\d.]+)\)\n(?:.*\n)*?\t\)\n'

def add_wire(t, a, b):
    """a new wire from a to b, appended before the closing paren: the old wire end stays where it was, because a
    label's anchor can also be a pin end (C42 on the ATmega page lost its net when the end itself was moved)"""
    import uuid
    seg = '\t(wire\n\t\t(pts\n\t\t\t(xy %s %s) (xy %s %s)\n\t\t)\n\t\t(stroke\n\t\t\t(width 0)\n\t\t\t(type default)\n\t\t)\n\t\t(uuid "%s")\n\t)\n' % (
        fmt(a[0]), fmt(a[1]), fmt(b[0]), fmt(b[1]), uuid.uuid5(uuid.NAMESPACE_URL, 'https://github.com/NorthernWidget/Project-Okapi/kicad/stub/%s/%s' % (fmt(a[0]) + ',' + fmt(a[1]), fmt(b[0]) + ',' + fmt(b[1]))))
    return t[:-2] + seg + ')\n'

TEXT = re.compile(r'^\t\(text "([^"]*)"\n(\t\t\(exclude_from_sim \w+\)\n)?\t\t\(at ([-\d.]+) ([-\d.]+) (\d+)\)\n((?:.*\n)*?)\t\)\n', re.M)

def main():
    a = sys.argv[1:]
    minpx = 30
    if '--min' in a:
        i = a.index('--min'); minpx = int(a[i + 1]); del a[i:i + 2]
    proj, scratch, colf = a
    col = json.load(open(colf))
    for page, hits in col.items():
        want = [(h[0], h[1], h[2], h[3]) for h in hits if (h[0] == 'g' and h[4] >= minpx) or (h[0] == 't' and h[4] >= 5)]   # a note crossed by one body line is few pixels and still wrong
        if not want: continue
        path = os.path.join(proj, page + '.kicad_sch'); t = open(path).read()
        tmp = os.path.join(scratch, 'fix_' + page); shutil.rmtree(tmp, ignore_errors=True)
        # each annotation is judged against the whole page without itself: parts, wires, fields, the other labels and the notes
        moved = 0
        for kind, name, cx, cy in want:
            if kind == 't':
                cands = [(m, (float(m.group(3)) - cx) ** 2 + (float(m.group(4)) - cy) ** 2) for m in TEXT.finditer(t) if m.group(1) == name]
                if not cands: continue
                m = min(cands, key=lambda c: c[1])[0]
                x, y = float(m.group(3)), float(m.group(4)); block = m.group(0)
                base_t = t.replace(block, '', 1); B_t = render(proj, base_t, tmp, 'Bt')
                best = None
                for dx, dy in [(0, 0)] + [(k * 1.27, 0) for k in range(-8, 9) if k] + [(0, k * 1.27) for k in range(-8, 9) if k]:
                    cand = re.sub(r'\(at [-\d.]+ [-\d.]+ (\d+)\)', lambda q: '(at %s %s %s)' % (fmt(x + dx), fmt(y + dy), q.group(1)), block, count=1)
                    px = ink_under(render(proj, base_t[:-2] + cand + ')\n', tmp, 'c'), B_t)
                    if px is None: continue
                    key = (px, abs(dx) + abs(dy))
                    if best is None or key < best[0]: best = (key, (dx, dy), cand)
                (px, _), (dx, dy), cand = best
                if (dx, dy) != (0, 0):
                    t = t.replace(block, cand, 1); moved += 1
                    print('  %s: note %r (%g,%g) -> (%g,%g), %d px under it' % (page, name, x, y, x + dx, y + dy, px))
                else:
                    print('  %s: note %r stays (%g,%g), best %d px' % (page, name, x, y, px))
                continue
            # the colliding label: the one of that name nearest the collision's center
            cands = [(m, (float(m.group(4)) - cx) ** 2 + (float(m.group(5)) - cy) ** 2) for m in LAB.finditer(t) if m.group(2) == name]
            if not cands: continue
            m = min(cands, key=lambda c: c[1])[0]
            x, y, ang = float(m.group(4)), float(m.group(5)), int(m.group(6)); block = m.group(0)
            base = t.replace(block, '', 1); B = render(proj, base, tmp, 'B')
            wires = [((float(x1), float(y1)), (float(x2), float(y2))) for x1, y1, x2, y2 in re.findall(r'\t\(wire\n\t\t\(pts\n\t\t\t\(xy ([-\d.]+) ([-\d.]+)\) \(xy ([-\d.]+) ([-\d.]+)\)', t)]
            ends = [((x, y), 'anchor', 0)]
            for p1, p2 in wires:
                far = p2 if abs(p1[0] - x) < 1e-6 and abs(p1[1] - y) < 1e-6 else (p1 if abs(p2[0] - x) < 1e-6 and abs(p2[1] - y) < 1e-6 else None)
                if far is None: continue
                ends.append((far, 'far', 0))
                if abs(far[0] - x) < 1e-6 or abs(far[1] - y) < 1e-6:   # an axis-aligned wire: push the anchor out along it
                    ux = 0 if abs(far[0] - x) < 1e-6 else (1 if x > far[0] else -1)
                    uy = 0 if abs(far[1] - y) < 1e-6 else (1 if y > far[1] else -1)
                    for k in (2, 4):
                        ends.append(((x + ux * k * 1.27, y + uy * k * 1.27), 'extend', k))
            best = None
            for (ex, ey), how, k in ends:
                page_t = base if how != 'extend' else add_wire(base, (x, y), (ex, ey))
                Bk = B if how != 'extend' else render(proj, page_t, tmp, 'Bk')
                for ca in (0, 90, 180, 270):
                    cand = set_label(block, ex, ey, ca)
                    px = ink_under(render(proj, page_t[:-2] + cand + ')\n', tmp, 'c'), Bk)   # the page without annotations plus this one label
                    if px is None: continue
                    key = (px, 0 if (ex, ey, ca) == (x, y, ang) else 1, k)
                    if best is None or key < best[0]: best = (key, (ex, ey, ca), how, cand)
            (px, _, k), (ex, ey, ca), how, cand = best
            if (ex, ey, ca) != (x, y, ang):
                t = t.replace(block, cand, 1); moved += 1
                if how == 'far':   # the label slid to the far end of its wire: that wire is a bare stub now and goes
                    for wm in re.finditer(WIRE, t):
                        pts = {(float(wm.group(1)), float(wm.group(2))), (float(wm.group(3)), float(wm.group(4)))}
                        if pts == {(x, y), (ex, ey)}:
                            t = t.replace(wm.group(0), '', 1); break
                elif how == 'extend':
                    t = add_wire(t, (x, y), (ex, ey))
                print('  %s: %s (%g,%g,%d) -> (%g,%g,%d) %s, %d px under it' % (page, name, x, y, ang, ex, ey, ca, how, px))
            else:
                print('  %s: %s stays (%g,%g,%d), best %d px' % (page, name, x, y, ang, px))
        open(path, 'w').write(t)
        subprocess.run(['kicad-cli', 'sch', 'upgrade', '--force', path], capture_output=True)
        print('%s: %d of %d labels moved' % (page, moved, len(want)))

if __name__ == '__main__':
    main()

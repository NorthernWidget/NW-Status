#!/usr/bin/env python3
"""Trim or delete the wire tails ERC reports as unconnected endpoints, from ERC's own report.

    erc_stubs.py <erc.json> <project dir> <NW-Tests/kicad dir> [--dry-run]

For each unconnected_wire_endpoint item, the wire with an end at the reported
point is found and both ends are walked with sch_walk. An end is bare when
nothing but the wire itself is there. The Eagle import leaves two shapes: a
wire that runs past the label or junction it serves to a bare end (the tail
is trimmed back to the last thing on the segment), and a wire to nothing (it
is deleted when its other end is bare too, or when the other end still has
something else to connect to; a wire that is a pin's only connection is
kept and reported, since removing it would change a net). An
endpoint_off_grid item whose wire end carries a label is snapped to the
grid with the label (the Eagle import's 0.1 mm placements). Every touched
sheet is re-saved through kicad-cli; run the gate afterwards.
"""
import json, os, re, subprocess, sys

def fmt(v):
    s = ('%.6f' % v).rstrip('0').rstrip('.')
    return '0' if s in ('-0', '') else s

WIRE = r'\t\(wire\n\t\t\(pts\n\t\t\t\(xy ([-\d.]+) ([-\d.]+)\) \(xy ([-\d.]+) ([-\d.]+)\)\n(?:.*\n)*?\t\)\n'

def main():
    a = sys.argv[1:]
    dry = '--dry-run' in a
    if dry: a.remove('--dry-run')
    ercf, proj, tools = a
    sys.path.insert(0, tools)
    from sch_walk import Sheet, on_seg, near
    ends = {}
    for s in json.load(open(ercf))['sheets']:
        for v in s['violations']:
            if v['type'] != 'unconnected_wire_endpoint': continue
            p = v['items'][0]['pos']; ends.setdefault(s['path'].strip('/'), []).append((p['x'], p['y']))
    files = [f for f in os.listdir(proj) if f.endswith('.kicad_sch')]
    # a wire end off the 1.27 mm grid with a label anchored on it: both snap to the nearest grid point
    offg = {}
    for s in json.load(open(ercf))['sheets']:
        for v in s['violations']:
            if v['type'] != 'endpoint_off_grid' or not v['items'][0]['description'].endswith('Wire') and 'Wire' not in v['items'][0]['description']: continue
            p = v['items'][0]['pos']; offg.setdefault(s['path'].strip('/'), []).append((p['x'], p['y']))
    def snap(v): return round(v / 1.27) * 1.27
    for name, pts in sorted(offg.items()):
        cands = [os.path.join(proj, name + '.kicad_sch')] if name else [os.path.join(proj, f) for f in files]
        for path in cands:
            t = open(path).read(); changed = 0
            for x, y in pts:
                for wm in re.finditer(WIRE, t):
                    p1 = (float(wm.group(1)), float(wm.group(2))); p2 = (float(wm.group(3)), float(wm.group(4)))
                    if not (near(p1, (x, y)) or near(p2, (x, y))): continue
                    for g in (1, 3):
                        ex, ey = float(wm.group(g)), float(wm.group(g + 1))
                        if near((ex, ey), (snap(ex), snap(ey))): continue
                        nx, ny = snap(ex), snap(ey)
                        lm = re.search(r'(\t\((?:global_label|label|hierarchical_label) "[^"]*"\n(?:\t\t\(shape \w+\)\n)?\t\t\(at )%s %s( \d+\))' % (re.escape(fmt(ex)), re.escape(fmt(ey))), t)
                        print('%s: wire end (%s, %s) %s to (%s, %s)%s%s' % (os.path.basename(path), fmt(ex), fmt(ey), 'would snap' if dry else 'snapped', fmt(nx), fmt(ny), ' with its label' if lm else ', no label there', ' (dry run)' if dry else ''))
                        if dry: continue
                        blk = wm.group(0).replace('(xy %s %s)' % (wm.group(g), wm.group(g + 1)), '(xy %s %s)' % (fmt(nx), fmt(ny)), 1)
                        t = t.replace(wm.group(0), blk, 1); changed += 1
                        if lm:
                            t = t.replace(lm.group(0), lm.group(1) + '%s %s' % (fmt(nx), fmt(ny)) + lm.group(2), 1)
                            # the hidden Intersheetrefs field keeps its offset from the anchor
                            blk2 = re.search(r'\t\((?:global_label|label|hierarchical_label) "[^"]*"\n(?:\t\t\(shape \w+\)\n)?\t\t\(at %s %s \d+\)\n(?:.*\n)*?\t\)\n' % (re.escape(fmt(nx)), re.escape(fmt(ny))), t)
                            if blk2:
                                b2 = re.sub(r'(\(property "Intersheetrefs" "[^"]*"\n\t\t\t\(at )([-\d.]+) ([-\d.]+)', lambda q: q.group(1) + '%s %s' % (fmt(float(q.group(2)) + nx - ex), fmt(float(q.group(3)) + ny - ey)), blk2.group(0), count=1)
                                t = t.replace(blk2.group(0), b2, 1)
                    # no break: another wire may share the reported point and carry the off-grid end
            if changed:
                open(path, 'w').write(t); subprocess.run(['kicad-cli', 'sch', 'upgrade', '--force', path], capture_output=True)
    for name, pts in sorted(ends.items()):
        cands = [os.path.join(proj, name + '.kicad_sch')] if name else [os.path.join(proj, f) for f in files]
        for path in cands:
            t = open(path).read(); changed = 0
            for x, y in pts:
                for wm in re.finditer(WIRE, t):
                    p1 = (float(wm.group(1)), float(wm.group(2))); p2 = (float(wm.group(3)), float(wm.group(4)))
                    if not (near(p1, (x, y)) or near(p2, (x, y))): continue
                    sh = Sheet(path)
                    def bare(pt):
                        k = sh.at_point(pt); return sum(1 for e in k if e[0] == 'wire') <= 1 and all(e[0] == 'wire' for e in k)
                    b1, b2 = bare(p1), bare(p2)
                    # things on the segment's interior: label anchors, junctions, other wires' ends
                    inner = [l[2] for l in sh.labels if on_seg(l[2], p1, p2) and not near(l[2], p1) and not near(l[2], p2)]
                    inner += [j for j in sh.juncs if on_seg(j, p1, p2) and not near(j, p1) and not near(j, p2)]
                    inner += [e for w in sh.wires for e in w if w != (p1, p2) and on_seg(e, p1, p2) and not near(e, p1) and not near(e, p2)]
                    tag = '%s: wire (%s, %s)-(%s, %s)' % (os.path.basename(path), fmt(p1[0]), fmt(p1[1]), fmt(p2[0]), fmt(p2[1]))
                    if inner and (b1 or b2):
                        keep, bare_end = (p2, p1) if b1 else (p1, p2)
                        new = min(inner, key=lambda q: (q[0] - bare_end[0]) ** 2 + (q[1] - bare_end[1]) ** 2)
                        print('%s: tail past (%s, %s) trimmed%s' % (tag, fmt(new[0]), fmt(new[1]), '' if not dry else ' (dry run)'))
                        if not dry:
                            blk = wm.group(0).replace('(xy %s %s)' % (wm.group(1 if b1 else 3), wm.group(2 if b1 else 4)), '(xy %s %s)' % (fmt(new[0]), fmt(new[1])), 1)
                            t = t.replace(wm.group(0), blk, 1); changed += 1
                    elif b1 and b2:
                        print('%s: both ends bare, deleted%s' % (tag, ' (dry run)' if dry else ''))
                        if not dry: t = t.replace(wm.group(0), '', 1); changed += 1
                    elif b1 or b2:
                        other = sh.at_point(p2 if b1 else p1)
                        kinds = sorted(set(e[0] for e in other))
                        if kinds == ['pin', 'wire'] and sum(1 for e in other if e[0] == 'wire') == 1:
                            print("%s: a pin's only wire, to nothing: kept (%s)" % (tag, ' '.join(e[1] for e in other if e[0] == 'pin')))
                        else:
                            print('%s: a stub off %s, deleted%s' % (tag, ' '.join(kinds), ' (dry run)' if dry else ''))
                            if not dry: t = t.replace(wm.group(0), '', 1); changed += 1
                    else:
                        continue   # another wire shares this point; the dangling one is the next match
                    break
            if changed:
                open(path, 'w').write(t); subprocess.run(['kicad-cli', 'sch', 'upgrade', '--force', path], capture_output=True)

if __name__ == '__main__':
    main()

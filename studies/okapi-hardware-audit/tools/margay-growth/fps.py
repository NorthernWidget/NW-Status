"""Dump every footprint: ref, value, side, center, bbox (courtyard if any, else pads+graphics), and its nets."""
import pcbnew, json
b = pcbnew.LoadBoard('Margay.kicad_pcb')
out = []
for f in b.GetFootprints():
    side = 'B' if f.IsFlipped() else 'F'
    lay = pcbnew.B_CrtYd if f.IsFlipped() else pcbnew.F_CrtYd
    c = f.GetCourtyard(lay)
    if c.OutlineCount():
        bb = c.BBox(); src = 'crtyd'
    else:
        bb = f.GetBoundingBox(False); src = 'bbox'
    x0, y0, x1, y1 = [pcbnew.ToMM(v) for v in (bb.GetX(), bb.GetY(), bb.GetRight(), bb.GetBottom())]
    p = f.GetPosition()
    nets = sorted({pd.GetNetname() for pd in f.Pads() if pd.GetNetname()})
    out.append(dict(ref=f.GetReference(), val=f.GetValue(), fp=str(f.GetFPID().GetLibItemName()), side=side,
                    x=round(pcbnew.ToMM(p.x), 2), y=round(pcbnew.ToMM(p.y), 2),
                    bbox=[round(v, 2) for v in (x0, y0, x1, y1)], src=src, nets=nets))
out.sort(key=lambda d: d['ref'])
json.dump(out, open('fps.json', 'w'), indent=1)
for d in out:
    print(f"{d['ref']:7s} {d['side']} {d['x']:7.2f} {d['y']:7.2f}  bbox {d['bbox']} {d['src']:5s} {d['val'][:14]:14s} {','.join(d['nets'])[:90]}")

import pcbnew, collections
b=pcbnew.LoadBoard('Margay.kicad_pcb')
bb=b.GetBoardEdgesBoundingBox()
print('outline mm', bb.GetX()/1e6, bb.GetY()/1e6, bb.GetWidth()/1e6, bb.GetHeight()/1e6)
print('layers', b.GetCopperLayerCount())
for ref in ['J2','J3','J4','J1','H1','H2']:
    f=b.FindFootprintByReference(ref)
    if not f: print(ref,'none'); continue
    p=f.GetPosition()
    print(ref, f.GetValue(), f.GetFPIDAsString(), 'side', 'B' if f.IsFlipped() else 'F', 'pos', p.x/1e6, p.y/1e6, 'rot', f.GetOrientationDegrees())
    for pad in sorted(f.Pads(), key=lambda q: q.GetNumber()):
        pp=pad.GetPosition()
        print('   pad', pad.GetNumber(), pad.GetNetname(), round(pp.x/1e6,2), round(pp.y/1e6,2), pad.GetAttribute())
# netnet: for each net on these connectors list pads
nets=set()
for ref in ['J2','J3','J4']:
    for pad in b.FindFootprintByReference(ref).Pads(): nets.add(pad.GetNetname())
idx=collections.defaultdict(list)
for f in b.GetFootprints():
    for pad in f.Pads(): idx[pad.GetNetname()].append(f"{f.GetReference()}.{pad.GetNumber()}({f.GetValue()})")
for n in sorted(nets):
    print('NET',n, ' '.join(sorted(idx[n])) if n not in ('GND','/GND') else f'{len(idx[n])} pads')
print('ZONES')
for z in b.Zones():
    print(' ', z.GetNetname(), z.GetLayerName(), 'area mm2', round(z.GetFilledArea()/1e12,1) if z.IsFilled() else 'unfilled', z.GetIsRuleArea())

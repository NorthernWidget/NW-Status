"""Per-net routed track length (sum of segment and arc lengths, both layers), via count,
and the pad locations of each net, for the nets that cross the board."""
import pcbnew, collections, math, sys
b = pcbnew.LoadBoard('Margay.kicad_pcb')
L = collections.defaultdict(float); V = collections.Counter()
for t in b.GetTracks():
    n = t.GetNetname()
    if t.GetClass() == 'PCB_VIA':
        V[n] += 1
    else:
        L[n] += pcbnew.ToMM(t.GetLength())
pads = collections.defaultdict(list)
for f in b.GetFootprints():
    for p in f.Pads():
        if p.GetNetname():
            q = p.GetPosition()
            pads[p.GetNetname()].append((f.GetReference()+'.'+p.GetNumber(), round(pcbnew.ToMM(q.x),2), round(pcbnew.ToMM(q.y),2)))
print('net, track length mm, vias, pad count, pad bbox dx x dy mm')
for n in sorted(L, key=lambda k: -L[k]):
    ps = pads[n]
    if ps:
        xs=[p[1] for p in ps]; ys=[p[2] for p in ps]
        span=f"{max(xs)-min(xs):5.1f} x {max(ys)-min(ys):5.1f}"
    else: span='-'
    print(f"{n:34s} {L[n]:7.1f} {V[n]:3d} {len(ps):3d}  {span}")
print('\nPads of selected nets')
for n in sys.argv[1:]:
    print(n, pads[n], f"track {L[n]:.1f} mm, {V[n]} vias")

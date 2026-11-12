import pcbnew, collections
b=pcbnew.LoadBoard('Margay.kicad_pcb')
L=collections.Counter(); W=collections.Counter(); vias=0
for t in b.GetTracks():
    if t.GetNetname()!='GND': continue
    if t.GetClass()=='PCB_VIA': vias+=1; continue
    L[t.GetLayerName()]+=t.GetLength()/1e6
    W[(t.GetLayerName(),round(t.GetWidth()/1e6,3))]+=t.GetLength()/1e6
print('GND track length by layer mm', dict(L)); print('by width', dict(W)); print('GND vias', vias)
tot=collections.Counter()
for t in b.GetTracks():
    if t.GetClass()!='PCB_VIA': tot[t.GetLayerName()]+=t.GetLength()/1e6
print('all track length', dict(tot))
# per GND pad of connectors: tracks touching
for ref,pn in [('J2','1'),('J2','7'),('J3','1'),('J4','A1B12'),('J4','B1A12'),('J4','S1')]:
    f=b.FindFootprintByReference(ref)
    for pad in f.Pads():
        if pad.GetNumber()!=pn: continue
        pp=pad.GetPosition(); n=0; ws=[]
        for t in b.GetTracks():
            if t.GetNetname()!='GND' or t.GetClass()=='PCB_VIA': continue
            for e in (t.GetStart(),t.GetEnd()):
                if pad.HitTest(e): n+=1; ws.append((t.GetLayerName(),round(t.GetWidth()/1e6,3),round(t.GetLength()/1e6,2)))
        print(ref,pn,round(pp.x/1e6,2),round(pp.y/1e6,2),'tracks',n,ws)
ds=b.GetDesignSettings()
print('netclasses'); 
for name,nc in b.GetAllNetClasses().items(): print(' ',name, nc.GetTrackWidth()/1e6, nc.GetClearance()/1e6)

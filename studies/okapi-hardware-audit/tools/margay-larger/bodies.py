# For parts without a courtyard: pads+0.25 bbox vs body-graphics bbox (graphics on silk/fab, plus pads, no text)
import pcbnew, json
b=pcbnew.LoadBoard('Margay.kicad_pcb'); mm=pcbnew.ToMM
out={}
for f in b.GetFootprints():
    fl=f.IsFlipped(); cy=f.GetCourtyard(pcbnew.B_CrtYd if fl else pcbnew.F_CrtYd)
    if cy.OutlineCount() or not f.Pads(): continue
    layers={}
    for g in f.GraphicalItems():
        if g.Type()==pcbnew.PCB_FIELD_T or g.Type()==pcbnew.PCB_TEXT_T: continue
        ln=b.GetLayerName(g.GetLayer()); bb=g.GetBoundingBox()
        layers.setdefault(ln,[]).append([mm(bb.GetX()),mm(bb.GetY()),mm(bb.GetRight()),mm(bb.GetBottom())])
    pb=None
    for p in f.Pads():
        q=p.GetBoundingBox()
        if pb is None: pb=q
        else: pb.Merge(q)
    P=[mm(pb.GetX()),mm(pb.GetY()),mm(pb.GetRight()),mm(pb.GetBottom())]
    allb=list(P)
    for ln,bs in layers.items():
        for r in bs:
            allb=[min(allb[0],r[0]),min(allb[1],r[1]),max(allb[2],r[2]),max(allb[3],r[3])]
    w=lambda r:(r[2]-r[0],r[3]-r[1])
    pw,ph=w(P); bw,bh=w(allb)
    out[f.GetReference()]=dict(pads_plus=[round(pw+0.5,2),round(ph+0.5,2),round((pw+0.5)*(ph+0.5),2)],body=[round(bw,2),round(bh,2),round(bw*bh,2)],layers=sorted(layers),pads_bbox=[round(v,2) for v in P],body_bbox=[round(v,2) for v in allb])
    print('%-6s pads+0.25 %5.2f x %5.2f = %6.2f | body+pads %5.2f x %5.2f = %6.2f | layers %s'%(f.GetReference(),pw+0.5,ph+0.5,(pw+0.5)*(ph+0.5),bw,bh,bw*bh,','.join(sorted(layers))))
json.dump(out,open('bodies.json','w'),indent=1)

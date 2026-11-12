# Inventory of Margay's footprints: side, courtyard source, area; outline, holes.
import pcbnew, sys, json
b=pcbnew.LoadBoard(sys.argv[1] if len(sys.argv)>1 else 'Margay.kicad_pcb')
bb=b.GetBoardEdgesBoundingBox()
mm=pcbnew.ToMM
print('outline bbox x %.3f-%.3f y %.3f-%.3f  W %.3f H %.3f'%(mm(bb.GetX()),mm(bb.GetRight()),mm(bb.GetY()),mm(bb.GetBottom()),mm(bb.GetWidth()),mm(bb.GetHeight())))
rows=[]
for f in b.GetFootprints():
    ref=f.GetReference(); fl=f.IsFlipped()
    cy=f.GetCourtyard(pcbnew.B_CrtYd if fl else pcbnew.F_CrtYd)
    if cy.OutlineCount():
        src='courtyard'; area=cy.Area()/1e12; c=cy.BBox(); bw,bh=mm(c.GetWidth()),mm(c.GetHeight())
    else:
        src='pads+0.25'; cb=None
        for p in f.Pads():
            pb=p.GetBoundingBox()
            if cb is None: cb=pb
            else: cb.Merge(pb)
        if cb is None: src='nopads'; bw=bh=area=0
        else:
            cb.Inflate(pcbnew.FromMM(0.25)); bw,bh=mm(cb.GetWidth()),mm(cb.GetHeight()); area=bw*bh
    p=f.GetPosition(); th=sum(1 for q in f.Pads() if q.GetAttribute() in (pcbnew.PAD_ATTRIB_PTH,pcbnew.PAD_ATTRIB_NPTH))
    rows.append(dict(ref=ref,fp=str(f.GetFPID().GetLibItemName()),side='B' if fl else 'F',src=src,area=round(area,3),w=round(bw,3),h=round(bh,3),x=round(mm(p.x),3),y=round(mm(p.y),3),npads=len(f.Pads()),th=th,value=f.GetValue()))
rows.sort(key=lambda r:(r['side'],r['ref']))
for r in rows: print('%-8s %-24s %s %-10s %8.3f mm2 %6.2f x %6.2f at %7.2f %7.2f pads %2d th %d %s'%(r['ref'],r['fp'],r['side'],r['src'],r['area'],r['w'],r['h'],r['x'],r['y'],r['npads'],r['th'],r['value']))
json.dump(rows,open('inventory.json','w'),indent=1)

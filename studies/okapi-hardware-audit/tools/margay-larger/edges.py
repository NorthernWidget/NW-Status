import pcbnew
b=pcbnew.LoadBoard('Margay.kicad_pcb'); mm=pcbnew.ToMM
for d in b.GetDrawings():
    if d.GetLayer()==pcbnew.Edge_Cuts:
        print(d.ShowShape(), 'w',mm(d.GetWidth()), [ (round(mm(p.x),3),round(mm(p.y),3)) for p in (d.GetStart(),d.GetEnd())])
for f in b.GetFootprints():
    for g in f.GraphicalItems():
        if g.GetLayer()==pcbnew.Edge_Cuts: print('fp edge',f.GetReference())
ps=pcbnew.SHAPE_POLY_SET()
ok=b.GetBoardPolygonOutlines(ps,False)
print('outline ok',ok,'area mm2',round(ps.Area()/1e12,3),'outlines',ps.OutlineCount())
for r in ('H1','H2'):
    f=b.FindFootprintByReference(r)
    for p in f.Pads(): print(r,'pad',p.GetAttribute(),'drill',mm(p.GetDrillSizeX()),'size',mm(p.GetSizeX()),'at',mm(p.GetPosition().x),mm(p.GetPosition().y))
    cy=f.GetCourtyard(pcbnew.F_CrtYd); print(r,'crt bbox',mm(cy.BBox().GetWidth()),'area',cy.Area()/1e12, 'holes', cy.HoleCount(0) if cy.OutlineCount() else None)
    for g in f.GraphicalItems(): print('  ',r,b.GetLayerName(g.GetLayer()),g.ShowShape(), round(mm(g.GetBoundingBox().GetWidth()),2))

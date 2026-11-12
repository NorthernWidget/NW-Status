import pcbnew; b=pcbnew.LoadBoard('Margay.kicad_pcb'); mm=pcbnew.ToMM
for r in ('J4','J1','BT1','U1','U12','XTAL1','U2','U6'):
    f=b.FindFootprintByReference(r)
    cyp=f.GetCourtyard(pcbnew.B_CrtYd if f.IsFlipped() else pcbnew.F_CrtYd)
    if cyp.OutlineCount():
        cy=cyp.BBox(); print(r,'crt bbox x %.2f-%.2f y %.2f-%.2f'%(mm(cy.GetX()),mm(cy.GetRight()),mm(cy.GetY()),mm(cy.GetBottom())), 'rot',f.GetOrientationDegrees())
    xs=[];ys=[]
    for p in f.Pads():
        q=p.GetBoundingBox(); xs+= [mm(q.GetX()),mm(q.GetRight())]; ys+=[mm(q.GetY()),mm(q.GetBottom())]
    print('   %s pads x %.2f-%.2f y %.2f-%.2f center %.2f %.2f'%(r,min(xs),max(xs),min(ys),max(ys),mm(f.GetPosition().x),mm(f.GetPosition().y)))

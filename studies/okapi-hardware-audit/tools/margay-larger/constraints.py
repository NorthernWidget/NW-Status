import pcbnew, math; b=pcbnew.LoadBoard('Margay.kicad_pcb'); mm=pcbnew.ToMM
pos=lambda r:(mm(b.FindFootprintByReference(r).GetPosition().x),mm(b.FindFootprintByReference(r).GetPosition().y))
for a,c in (('U12','U2'),('U12','U6'),('U12','U7'),('U12','U9')):
    (x1,y1),(x2,y2)=pos(a),pos(c); print('%s-%s center distance %.2f mm'%(a,c,math.hypot(x2-x1,y2-y1)))
u1=b.FindFootprintByReference('U1')
for p in u1.Pads():
    if p.GetNetname() and 'XTAL' in p.GetNetname().upper() or p.GetNumber() in ('7','8'):
        print('U1 pad',p.GetNumber(),p.GetNetname(),round(mm(p.GetPosition().x),2),round(mm(p.GetPosition().y),2))
x=b.FindFootprintByReference('XTAL1')
for p in x.Pads(): print('XTAL1 pad',p.GetNumber(),p.GetNetname(),round(mm(p.GetPosition().x),2),round(mm(p.GetPosition().y),2))
for r in ('C2','C3'): print(r,pos(r))

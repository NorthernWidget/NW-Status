# v0.8.0 question: a rectangular outline, and the M.2 socket (J9) moved toward the interior.
# For a shift dx (mm, negative = toward the board's left/center), list the footprints the B-SoM's
# envelope (J9's F.Fab card outline, and separately its pads, each + 0.25 mm) would land on. MS1 (the Feather
# footprint, an alternative to the B-SoM) is ignored: its header holes sit unpopulated under the card.
import pcbnew, sys
b=pcbnew.LoadBoard('Okapi.kicad_pcb')
j=b.FindFootprintByReference('J9')
def env(items):
    xs=[];ys=[]
    for bb in items: xs+=[pcbnew.ToMM(bb.GetX()),pcbnew.ToMM(bb.GetRight())]; ys+=[pcbnew.ToMM(bb.GetY()),pcbnew.ToMM(bb.GetBottom())]
    return (min(xs)-0.25,min(ys)-0.25,max(xs)+0.25,max(ys)+0.25)
CARD=env([d.GetBoundingBox() for d in j.GraphicalItems() if d.GetLayerName()=='F.Fab'])
PADS=env([p.GetBoundingBox() for p in j.Pads()])
for n,E in (('card outline (F.Fab)',CARD),('socket and standoff pads',PADS)): print('%s +0.25 mm: x %.2f-%.2f, y %.2f-%.2f'%(n,E[0],E[2],E[1],E[3]))
boxes=[]
for f in b.GetFootprints():
    r=f.GetReference()
    if r in ('J9','MS1') or f.IsFlipped(): continue
    cy=f.GetCourtyard(pcbnew.F_CrtYd); c=cy.BBox() if cy.OutlineCount() else f.GetBoundingBox(False)
    boxes.append((r,[pcbnew.ToMM(v) for v in (c.GetX(),c.GetY(),c.GetRight(),c.GetBottom())]))
bb=b.GetBoardEdgesBoundingBox(); BX0=pcbnew.ToMM(bb.GetX())
for dx in [0,-3,-5,-7,-10,-12.2,-15,-20,-25]:
    hit=set()
    for E in (CARD,PADS):
        e=(E[0]+dx,E[1],E[2]+dx,E[3])
        hit|={r for r,a in boxes if a[0]<e[2] and a[2]>e[0] and a[1]<e[3] and a[3]>e[1]}
    hit=sorted(hit)
    print('dx %6.1f  card x %6.2f-%6.2f  lands on %2d: %s'%(dx,CARD[0]+dx,CARD[2]+dx,len(hit),' '.join(hit)) + ('  (past the left edge)' if CARD[0]+dx<BX0 else ''))

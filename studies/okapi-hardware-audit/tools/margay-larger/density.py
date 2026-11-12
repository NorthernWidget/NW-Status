# Packing density of Margay's top side.
# Usable top area: board outline (Edge.Cuts polygon) inset 0.4 mm, minus mounting-hole keepouts
# (circle of diameter HOLE_D around each H* pad: the 5.56 mm User.Comments circle in 4_40_CLOSE, i.e. the screw-head keepout).
# Part area per top footprint: courtyard polygon area where the footprint has one; otherwise
#   PROXY=pads  -> pads bbox + 0.25 mm per side (the study's stated rule)
#   PROXY=body  -> the larger of pads+0.25 and the body-graphics+pads bbox (counts the screw-terminal bodies)
# Excluded from the part sum: H1, H2 (counted as keepouts), U$1 (B.Fab drawing, no pads), LOGO1.
import pcbnew, numpy as np, json, os, sys
mm=pcbnew.ToMM
HOLE_D=float(os.environ.get('HOLE_D','5.56')); INSET=0.4; RES=0.05
b=pcbnew.LoadBoard(sys.argv[1] if len(sys.argv)>1 else 'Margay.kicad_pcb')
ps=pcbnew.SHAPE_POLY_SET(); b.GetBoardPolygonOutlines(ps,False)
outline_area=ps.Area()/1e12
ins=pcbnew.SHAPE_POLY_SET(ps); ins.Deflate(pcbnew.FromMM(INSET),pcbnew.CORNER_STRATEGY_ROUND_ALL_CORNERS,pcbnew.FromMM(0.005))
inset_area=ins.Area()/1e12
bb=ps.BBox(); x0,y0=mm(bb.GetX()),mm(bb.GetY()); nx,ny=int(mm(bb.GetWidth())/RES)+2,int(mm(bb.GetHeight())/RES)+2
X,Y=np.meshgrid(x0+(np.arange(nx)+0.5)*RES,y0+(np.arange(ny)+0.5)*RES)
inside=np.zeros((ny,nx),bool)
for j in range(ny):
    for i in range(nx):
        inside[j,i]=ins.Contains(pcbnew.VECTOR2I(pcbnew.FromMM(float(X[j,i])),pcbnew.FromMM(float(Y[j,i]))))
holes=[]
for f in b.GetFootprints():
    if f.GetReference().startswith('H'):
        p=f.GetPosition(); hx,hy=mm(p.x),mm(p.y); holes.append((f.GetReference(),hx,hy))
        inside&=~(((X-hx)**2+(Y-hy)**2)<=(HOLE_D/2)**2)
usable=inside.sum()*RES*RES
bodies=json.load(open('bodies.json'))
proxy=os.environ.get('PROXY','pads')
rows=[]; total=0
for f in b.GetFootprints():
    ref=f.GetReference()
    if f.IsFlipped() or ref.startswith('H') or ref in ('U$1',) or ref.startswith('LOGO'): continue
    cy=f.GetCourtyard(pcbnew.F_CrtYd)
    if cy.OutlineCount(): a=cy.Area()/1e12; src='courtyard'
    else:
        a=bodies[ref]['pads_plus'][2]; src='pads+0.25'
        if proxy=='body' and bodies[ref]['body'][2]>a: a=bodies[ref]['body'][2]; src='body bbox'
    rows.append((ref,src,round(a,3))); total+=a
print('PROXY=%s HOLE_D=%.2f INSET=%.2f RES=%.2f'%(proxy,HOLE_D,INSET,RES))
print('outline area %.1f mm2; inset outline %.1f mm2; holes %s; usable top area %.1f mm2'%(outline_area,inset_area,holes,usable))
print('top parts counted %d; sum of areas %.1f mm2; density %.3f'%(len(rows),total,total/usable))
for r in sorted(rows,key=lambda r:-r[2]): print('  %-6s %-10s %8.3f'%r)
json.dump(dict(proxy=proxy,usable=usable,outline=outline_area,sum=total,density=total/usable,rows=rows),open('density_%s.json'%proxy,'w'),indent=1)

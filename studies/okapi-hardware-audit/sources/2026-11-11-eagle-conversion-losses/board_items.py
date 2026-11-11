"""Board-level items outside packages: outline (Eagle layer 20 against Edge.Cuts), plain items on fab/rule layers, dimensions.
usage: python3 board_items.py <eagle.brd> <board.kicad_pcb> <dx> <dy>"""
import sys,math,collections
import xml.etree.ElementTree as ET
import pcbnew
brd,kp,dx,dy=sys.argv[1],sys.argv[2],float(sys.argv[3]),float(sys.argv[4])
r=ET.parse(brd).getroot(); b=pcbnew.LoadBoard(kp)
def k2e(p): return (round(pcbnew.ToMM(p.x)-dx,3),round(-pcbnew.ToMM(p.y)-dy,3))
E=[]
for w in r.find('.//plain'):
    if w.tag=='wire' and w.get('layer')=='20':
        a=(round(float(w.get('x1')),3),round(float(w.get('y1')),3)); c=(round(float(w.get('x2')),3),round(float(w.get('y2')),3))
        E.append((frozenset([a,c]),float(w.get('curve') or 0)))
K=[]
for d in b.GetDrawings():
    if d.GetLayer()==pcbnew.Edge_Cuts:
        K.append((frozenset([k2e(d.GetStart()),k2e(d.GetEnd())]),d.GetShapeStr()))
print('outline: Eagle layer-20 wires %d (curved %d); KiCad Edge.Cuts %d %s'%(len(E),sum(1 for e in E if e[1]),len(K),dict(collections.Counter(s for _,s in K))))
ke=set(k for k,_ in K)
miss=[e for e in E if not any(all(min(math.hypot(p[0]-q[0],p[1]-q[1]) for q in kk)<0.002 for p in e[0]) for kk in ke)]
print('  Eagle outline segments with no Edge.Cuts item of the same end points:',len(miss),miss[:5])
print('plain items by tag and layer:',dict(collections.Counter((c.tag,c.get('layer')) for c in r.find('.//plain'))))
print('KiCad drawings by class and layer:',dict(collections.Counter((d.GetClass(),b.GetLayerName(d.GetLayer())) for d in b.GetDrawings())))
ra=[z for z in b.Zones() if z.GetIsRuleArea()]
print('KiCad board-level rule areas: %d, footprint rule areas: %d'%(len(ra),sum(len(list(fp.Zones())) for fp in b.GetFootprints())))
for z in ra: print('   ',[pcbnew.BOARD.GetStandardLayerName(l) for l in z.GetLayerSet().Seq()],k2e(z.Outline().CVertex(0)))
for c in r.find('.//plain'):
    if c.tag=='polygon' and c.get('layer') in('41','42','43'): print('  Eagle plain restrict polygon layer',c.get('layer'),[(q.get('x'),q.get('y')) for q in c.findall('vertex')][:3],'...')
    if c.tag=='dimension': print('  Eagle dimension layer',c.get('layer'),c.get('dtype'),c.get('x1'),c.get('y1'),c.get('x2'),c.get('y2'))
for d in b.GetDrawings():
    if 'DIM' in d.GetClass(): print('  KiCad dimension',b.GetLayerName(d.GetLayer()),k2e(d.GetStart()),k2e(d.GetEnd()))
# arc check: the Eagle arc's midpoint (from its curve angle) against the KiCad arc's
def emid(x1,y1,x2,y2,curve):
    a=math.radians(curve); c=math.hypot(x2-x1,y2-y1); R=c/2/math.sin(abs(a)/2); mx,my=(x1+x2)/2,(y1+y2)/2
    sag=R-math.sqrt(max(R*R-c*c/4,0)) if abs(curve)<=180 else R+math.sqrt(max(R*R-c*c/4,0))
    nx,ny=(y2-y1)/c,-(x2-x1)/c   # right-hand normal; a counterclockwise (positive) arc bulges to the right of the chord
    s=1 if curve>0 else -1
    return (mx+s*nx*sag,my+s*ny*sag)
km=[k2e(d.GetArcMid()) for d in b.GetDrawings() if d.GetLayer()==pcbnew.Edge_Cuts and d.GetShapeStr()=='Arc']
worst=0
for w in r.find('.//plain'):
    if w.tag=='wire' and w.get('layer')=='20' and w.get('curve'):
        m=emid(*[float(w.get(k)) for k in('x1','y1','x2','y2')],float(w.get('curve')))
        worst=max(worst,min(math.hypot(m[0]-q[0],m[1]-q[1]) for q in km))
print('outline arcs: worst distance from an Eagle arc midpoint to the nearest KiCad arc midpoint %.4f mm'%worst)

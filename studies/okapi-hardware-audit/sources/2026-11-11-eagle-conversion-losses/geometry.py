"""Area and extent, per Eagle layer, of every package's graphics on the fab and rule layers, against the KiCad library footprint's
layer that the importer maps it to. Eagle shapes are built with shapely (wire: buffered line, round caps; circle width 0: disc,
else a ring of that width; rectangle: rotated about its center; polygon: outline buffered by width/2); KiCad shapes with
pcbnew's own TransformShapeToPolygon, keepouts from the zone outline.
usage: python3 geometry.py <eagle.brd> <inventory.json> <lib.pretty> [layers]"""
import sys,json,math,collections
import xml.etree.ElementTree as ET
import shapely
from shapely.geometry import Polygon,Point,LineString
from shapely.ops import unary_union
from shapely import affinity
import pcbnew
brd,inv,pretty=sys.argv[1:4]
LAYERS=[int(x) for x in sys.argv[4].split(',')] if len(sys.argv)>4 else [1,16,20,29,30,31,32,35,39,40,41,42,43,46,21]
KMAP={1:'F.Cu',16:'B.Cu',20:'Edge.Cuts',29:'F.Mask',30:'B.Mask',31:'F.Paste',32:'B.Paste',35:'F.Adhes',39:'F.CrtYd',40:'B.CrtYd',21:'F.SilkS'}
root=ET.parse(brd).getroot(); r=json.load(open(inv))
pk={(l.get('name'),p.get('name')):p for l in root.find('.//board/libraries') for p in l.iter('package')}
def arcline(x1,y1,x2,y2,curve,n=32):
    if not curve: return LineString([(x1,y1),(x2,y2)])
    a=math.radians(curve); c=math.hypot(x2-x1,y2-y1); R=c/2/math.sin(a/2)
    mx,my=(x1+x2)/2,(y1+y2)/2; d=math.sqrt(max(R*R-c*c/4,0)); ux,uy=-(y2-y1)/c,(x2-x1)/c
    s=1 if a>0 else -1
    cx,cy=mx+s*ux*d*(1 if abs(curve)<180 else -1),my+s*uy*d*(1 if abs(curve)<180 else -1)
    t1=math.atan2(y1-cy,x1-cx)
    return LineString([(cx+abs(R)*math.cos(t1+a*k/n),cy+abs(R)*math.sin(t1+a*k/n)) for k in range(n+1)])
def eshape(c):
    t=c.tag; w=float(c.get('width') or 0)
    if t=='wire':
        return arcline(*[float(c.get(k)) for k in('x1','y1','x2','y2')],float(c.get('curve') or 0)).buffer(w/2)
    if t=='circle':
        x,y,R=float(c.get('x')),float(c.get('y')),float(c.get('radius'))
        return Point(x,y).buffer(R,64) if w==0 else Point(x,y).buffer(R+w/2,64).difference(Point(x,y).buffer(max(R-w/2,0),64))
    if t=='rectangle':
        x1,y1,x2,y2=[float(c.get(k)) for k in('x1','y1','x2','y2')]
        g=Polygon([(x1,y1),(x2,y1),(x2,y2),(x1,y2)]); rot=float((c.get('rot') or 'R0').lstrip('R'))
        return affinity.rotate(g,rot,origin='centroid')
    if t=='polygon':
        vs=c.findall('vertex'); pts=[]
        for i,q in enumerate(vs):   # a vertex's curve is the arc from it to the next vertex
            n=vs[(i+1)%len(vs)]; x1,y1,x2,y2=float(q.get('x')),float(q.get('y')),float(n.get('x')),float(n.get('y'))
            pts+=list(arcline(x1,y1,x2,y2,float(q.get('curve') or 0)).coords)[:-1]
        g=Polygon(pts).buffer(0); return g.buffer(w/2) if w else g
    return None
def kpoly(ps):
    out=[]
    for i in range(ps.OutlineCount()):
        o=ps.Outline(i); pts=[(pcbnew.ToMM(o.CPoint(j).x),-pcbnew.ToMM(o.CPoint(j).y)) for j in range(o.PointCount())]
        g=Polygon(pts)
        for h in range(ps.HoleCount(i)):
            hh=ps.Hole(i,h); g=g.difference(Polygon([(pcbnew.ToMM(hh.CPoint(j).x),-pcbnew.ToMM(hh.CPoint(j).y)) for j in range(hh.PointCount())]))
        out.append(g)
    return unary_union(out) if out else Polygon()
def kshapes(fp,layer):
    gs=[]
    for it in fp.GraphicalItems():
        if it.GetLayer()!=layer or not hasattr(it,'TransformShapeToPolygon'): continue
        ps=pcbnew.SHAPE_POLY_SET(); it.TransformShapeToPolygon(ps,layer,0,pcbnew.FromMM(0.002),pcbnew.ERROR_INSIDE); gs.append(kpoly(ps))
    return unary_union(gs) if gs else Polygon()
def kzones(fp):
    d=collections.defaultdict(list)
    for z in fp.Zones():
        for l in z.GetLayerSet().Seq(): d[pcbnew.BOARD.GetStandardLayerName(l)].append(kpoly(z.Outline()))
    return {k:unary_union(v) for k,v in d.items()}
def desc(g):
    if g.is_empty: return 'none'
    b=g.bounds; return 'area %.4f mm2, extent (%.3f,%.3f)-(%.3f,%.3f)'%(g.area,*b)
ndiff=0; nchk=0
for k,v in r.items():
    p=pk[(v['lib'],v['package'])]; fp=pcbnew.FootprintLoad(pretty,v['fp']) if v['fp'] else None
    if fp is None: continue
    zs=kzones(fp); lines=[]
    for L in LAYERS:
        es=[eshape(c) for c in p if c.get('layer')==str(L) and c.tag in('wire','circle','rectangle','polygon')]
        es=[g for g in es if g is not None]
        if not es: continue
        eg=unary_union(es); nchk+=1
        if L in KMAP: kg=kshapes(fp,getattr(pcbnew,KMAP[L].replace('.','_')))
        elif L in(41,42,43): kg=unary_union(list(zs.values())) if zs else Polygon()
        else: kg=Polygon()
        sd=eg.symmetric_difference(kg).area
        ok=sd<=max(0.002,0.01*eg.area)
        if not ok: ndiff+=1
        if not ok or L in(41,42,43): lines.append('   layer %d %s: eagle %s | kicad %s | sym. diff %.4f mm2 %s'%(L,KMAP.get(L,'keepout zones '+','.join(sorted(zs)) if L in (41,42,43) else 'no KiCad layer'),desc(eg),desc(kg),sd,'' if ok else 'DIFFERS'))
    if lines: print('==',k,v['fp'],','.join(v['refs'][:5])); print('\n'.join(lines))
print('layer comparisons %d, differing %d'%(nchk,ndiff))

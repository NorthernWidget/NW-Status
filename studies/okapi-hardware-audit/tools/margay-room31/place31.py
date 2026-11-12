# v3.1 room study: where the parts of #70, #71/#73, #48, #52, #53 and #72 fit on the current board.
# Board: Margay.kicad_pcb from Project-Margay HEAD (see SOURCE_COMMIT). Courtyard spacing 0.15 mm, 0.3 mm edge keepout.
# mode cu: new pads also clear existing tracks, vias and pads by 0.15 mm (fits with no reroute)
# mode crt: courtyards only (fits if Andy reroutes the tracks under it)
import pcbnew, numpy as np, json, sys, math
from occ import occupancy
LIB='/home/awickert/Dropbox/NorthernWidget/github/nw-cold-silicon/nw-cold-silicon.pretty'
CU_CLR=0.15
REMOVE={'C20'}
b=pcbnew.LoadBoard('Margay.kicad_pcb')
top,bot,(x0,y0,res),_=occupancy(b,remove=REMOVE)
ny,nx=top.shape
def mark(g,xa,ya,xb,yb,m):
    i0=max(0,int((xa-m-x0)/res)); i1=min(nx,int((xb+m-x0)/res)+1)
    j0=max(0,int((ya-m-y0)/res)); j1=min(ny,int((yb+m-y0)/res)+1)
    g[j0:j1,i0:i1]=True
cuT=np.zeros_like(top); cuB=np.zeros_like(top)
padT=np.zeros_like(top); padB=np.zeros_like(top)
for t in b.GetTracks():
    if t.GetNetname()=='Net-(BT1-+)' and False: continue
    if t.GetClass()=='PCB_VIA':
        p=t.GetPosition(); x,y=pcbnew.ToMM(p.x),pcbnew.ToMM(p.y); r=pcbnew.ToMM(t.GetWidth(pcbnew.F_Cu))/2
        for g in (cuT,cuB): mark(g,x-r,y-r,x+r,y+r,CU_CLR)
        continue
    w=pcbnew.ToMM(t.GetWidth())/2
    g=cuT if t.GetLayer()==pcbnew.F_Cu else cuB
    s,e=t.GetStart(),t.GetEnd(); xs,ys,xe,ye=[pcbnew.ToMM(v) for v in (s.x,s.y,e.x,e.y)]
    L=max(math.hypot(xe-xs,ye-ys),1e-6); n=int(L/0.05)+1
    for k in range(n+1):
        x=xs+(xe-xs)*k/n; y=ys+(ye-ys)*k/n; mark(g,x-w,y-w,x+w,y+w,CU_CLR)
for f in b.GetFootprints():
    if f.GetReference() in REMOVE: continue
    for p in f.Pads():
        bb=p.GetBoundingBox(); r=[pcbnew.ToMM(v) for v in (bb.GetX(),bb.GetY(),bb.GetRight(),bb.GetBottom())]
        th=p.GetAttribute() in (pcbnew.PAD_ATTRIB_PTH,pcbnew.PAD_ATTRIB_NPTH)
        if th or p.IsOnLayer(pcbnew.F_Cu): mark(cuT,*r,CU_CLR); mark(padT,*r,CU_CLR)
        if th or p.IsOnLayer(pcbnew.B_Cu): mark(cuB,*r,CU_CLR); mark(padB,*r,CU_CLR)
# existing pads can never be rerouted: they block in every mode
top|=padT; bot|=padB
_io=pcbnew.PCB_IO_KICAD_SEXPR()
def fpgeom(name,rot):
    f=_io.FootprintLoad(LIB if not name.startswith(('RARRAY','USON10','DFN1006')) else 'scratch.pretty',name); f.SetOrientationDegrees(rot)
    cy=f.GetCourtyard(pcbnew.F_CrtYd)
    c=cy.BBox() if cy.OutlineCount() else f.GetBoundingBox(False)
    body=[pcbnew.ToMM(v) for v in (c.GetX(),c.GetY(),c.GetRight(),c.GetBottom())]
    pads=[[pcbnew.ToMM(v) for v in (q.GetX(),q.GetY(),q.GetRight(),q.GetBottom())] for q in (p.GetBoundingBox() for p in f.Pads())]
    return body,pads,bool(cy.OutlineCount())
def fits(g,rect,dx,dy,m=0.0):
    xa,ya,xb,yb=rect
    i0=int((xa+dx-m-x0)/res); i1=int((xb+dx+m-x0)/res)+1; j0=int((ya+dy-m-y0)/res); j1=int((yb+dy+m-y0)/res)+1
    if i0<0 or j0<0 or i1>nx or j1>ny: return False
    return not g[j0:j1,i0:i1].any()
def search(name,target,side,radius,need_cu):
    tx,ty=target; best=None
    crt=top if side=='F' else bot; cu=cuT if side=='F' else cuB
    for rot in (0,90):
        body,pads,hascy=fpgeom(name,rot)
        if side=='B':
            body=[body[0],-body[3],body[2],-body[1]]; pads=[[p[0],-p[3],p[2],-p[1]] for p in pads]
        for dx in np.arange(tx-radius,tx+radius,0.1):
            for dy in np.arange(ty-radius,ty+radius,0.1):
                d=math.hypot(dx-tx,dy-ty)
                if d>radius or (best and d>=best[0]): continue
                if not fits(crt,body,dx,dy,0.15): continue
                if need_cu and not all(fits(cu,p,dx,dy) for p in pads): continue
                best=(d,side,rot,round(dx,2),round(dy,2),body,pads)
    return best
def commit(best):
    d,side,rot,dx,dy,body,pads=best
    crt=top if side=='F' else bot; cu=cuT if side=='F' else cuB
    mark(crt,body[0]+dx,body[1]+dy,body[2]+dx,body[3]+dy,0)
    for p in pads: mark(cu,p[0]+dx,p[1]+dy,p[2]+dx,p[3]+dy,CU_CLR)
PARTS=json.load(open(__import__('os').environ.get('PARTS','parts.json')))
if __name__=='__main__':
    mode=sys.argv[1]; sides=sys.argv[2]
    out=[]
    for issue,ref,fp,tgt,r,why in PARTS:
        best=None
        for s in sides:
            best=search(fp,tgt,s,r,mode=='cu')
            if best: break
        if not best:
            print(f'{issue:6} {ref:8} {fp:16} NO PLACE within {r} mm | {why}'); out.append([issue,ref,fp,None,None,None,None,None,why]); continue
        commit(best)
        print(f'{issue:6} {ref:8} {fp:16} side {best[1]} rot {best[2]:3} at {best[3]:7.2f} {best[4]:7.2f} dist {best[0]:4.2f} | {why}')
        out.append([issue,ref,fp,best[1],best[2],best[3],best[4],round(best[0],2),why])
    json.dump(out,open(f'placed_{mode}_{sides}.json','w'),indent=1)

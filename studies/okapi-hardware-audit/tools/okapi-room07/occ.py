import pcbnew, numpy as np, sys, os
REMOVE=set()
def load(path):
    return pcbnew.LoadBoard(path)
def occupancy(b, remove=REMOVE, res=0.1, margin=0.15):
    bb=b.GetBoardEdgesBoundingBox()
    x0,y0=pcbnew.ToMM(bb.GetX()),pcbnew.ToMM(bb.GetY()); W,H=pcbnew.ToMM(bb.GetWidth()),pcbnew.ToMM(bb.GetHeight())
    nx,ny=int(W/res)+1,int(H/res)+1
    top=np.zeros((ny,nx),bool); bot=np.zeros((ny,nx),bool)
    def mark(g,xa,ya,xb,yb):
        i0=max(0,int((xa-margin-x0)/res)); i1=min(nx,int((xb+margin-x0)/res)+1)
        j0=max(0,int((ya-margin-y0)/res)); j1=min(ny,int((yb+margin-y0)/res)+1)
        g[j0:j1,i0:i1]=True
    boxes=[]
    for f in b.GetFootprints():
        ref=f.GetReference()
        if ref in remove: continue
        flipped=f.IsFlipped()
        cy=f.GetCourtyard(pcbnew.B_CrtYd if flipped else pcbnew.F_CrtYd)
        if cy.OutlineCount():
            cb=cy.BBox()
        elif os.environ.get('LENIENT') and (ref[0] in 'UQDLCR' or ref.startswith('RTC')):
            cb=None
            for p in f.Pads():
                pb=p.GetBoundingBox()
                if cb is None: cb=pb
                else: cb.Merge(pb)
            if cb is None: cb=f.GetBoundingBox(False)   # no pads (artwork): body outline
            else: cb.Inflate(pcbnew.FromMM(0.25))   # IPC-7351 nominal courtyard excess, an ESTIMATE for parts imported without a courtyard
        else:
            cb=f.GetBoundingBox(False)   # body graphics + pads, no text
        xa,ya,xb,yb=[pcbnew.ToMM(v) for v in (cb.GetX(),cb.GetY(),cb.GetRight(),cb.GetBottom())]
        g=bot if flipped else top
        if ref.startswith('LOGO'): pass
        mark(g,xa,ya,xb,yb); boxes.append((ref,'B' if flipped else 'F',xa,ya,xb,yb))
        # through-hole pads also block the other side
        for p in f.Pads():
            if p.GetAttribute() in (pcbnew.PAD_ATTRIB_PTH,pcbnew.PAD_ATTRIB_NPTH):
                pb=p.GetBoundingBox()
                mark(top if flipped else bot,*[pcbnew.ToMM(v) for v in (pb.GetX(),pb.GetY(),pb.GetRight(),pb.GetBottom())])
    # board-level silkscreen (terminal labels, jumper notes, the credit block) also blocks parts on its side
    for d in b.GetDrawings():
        ln=d.GetLayer()
        if ln not in (pcbnew.F_SilkS,pcbnew.B_SilkS): continue
        if os.environ.get('MOVE_CREDIT') and hasattr(d,'GetText') and d.GetText().startswith('Project Margay'): continue
        bb=d.GetBoundingBox()
        mark(top if ln==pcbnew.F_SilkS else bot,*[pcbnew.ToMM(v) for v in (bb.GetX(),bb.GetY(),bb.GetRight(),bb.GetBottom())])
    # board-edge keepout 0.3 mm
    e=int(round(0.4/res))   # 0.4 mm: the board setup asks 0.381 mm copper to edge
    for g in (top,bot):
        g[:e,:]=True; g[-e:,:]=True; g[:,:e]=True; g[:,-e:]=True
    return top,bot,(x0,y0,res),boxes
def max_rect(g):
    # largest all-free axis-aligned rectangle (histogram method)
    ny,nx=g.shape; h=np.zeros(nx,int); best=(0,None)
    for j in range(ny):
        h=np.where(g[j],0,h+1)
        st=[]
        for i in range(nx+1):
            cur=h[i] if i<nx else 0
            start=i
            while st and st[-1][1]>=cur:
                s,hh=st.pop(); a=hh*(i-s)
                if a>best[0]: best=(a,(s,j-hh+1,i-1,j))
                start=s
            st.append((start,cur))
    return best
if __name__=='__main__':
    b=load(sys.argv[1]); top,bot,(x0,y0,res),boxes=occupancy(b)
    print('board',x0,y0)
    for name,g in (('top',top),('bottom',bot)):
        print(name,'free area mm2 (0.15 mm margin around parts, 0.3 mm edge):',round((~g).sum()*res*res,1),'of',round(g.size*res*res,1))
    regions={'power (J4/J3 to U6/U7): x150-174, y88-121':(150,88,174,121),'clock/BT1: x128-156, y104-121':(128,104,156,121)}
    for rn,(xa,ya,xb,yb) in regions.items():
        for name,g in (('top',top),('bottom',bot)):
            xa=max(xa,x0); ya=max(ya,y0); i0,i1=int((xa-x0)/res),min(g.shape[1],int((xb-x0)/res)); j0,j1=int((ya-y0)/res),min(g.shape[0],int((yb-y0)/res))
            sub=g[j0:j1,i0:i1]
            a,r=max_rect(sub)
            print(rn,name,'free',round((~sub).sum()*res*res,1),'mm2; largest free rectangle',
                  None if not r else (round((r[2]-r[0]+1)*res,2),'x',round((r[3]-r[1]+1)*res,2),'at x',round(xa+r[0]*res,2),'-',round(xa+(r[2]+1)*res,2),'y',round(ya+r[1]*res,2),'-',round(ya+(r[3]+1)*res,2)))
    np.save('top.npy',top); np.save('bot.npy',bot)

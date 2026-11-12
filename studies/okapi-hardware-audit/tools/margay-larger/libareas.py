# Courtyard area of library footprints (nw-cold-silicon; scratch.pretty estimates marked). No courtyard -> pads bbox + 0.25 mm per side.
import pcbnew, json
LIB='/home/awickert/Dropbox/NorthernWidget/github/nw-cold-silicon/nw-cold-silicon.pretty'
io=pcbnew.PCB_IO_KICAD_SEXPR(); mm=pcbnew.ToMM
names=['C0402','R0402','C0603','R0603','C0805','C1206','SOD323-R','SOT143B','DRV0006A','DCK_R-PDSO-G6','DBV_R-PDSO-G6','SC-70_6','SOT23-6L','RARRAY4_0402','USON10_2.5X1','DFN1006_TVS']
out={}
for n in names:
    lib='scratch.pretty' if n in ('RARRAY4_0402','USON10_2.5X1','DFN1006_TVS') else LIB
    try: f=io.FootprintLoad(lib,n)
    except Exception as e: print(n,'LOAD FAIL',e); continue
    if f is None: print(n,'not found'); continue
    cy=f.GetCourtyard(pcbnew.F_CrtYd)
    if cy.OutlineCount():
        c=cy.BBox(); a=cy.Area()/1e12; src='courtyard'; w,h=mm(c.GetWidth()),mm(c.GetHeight())
    else:
        xs=[];ys=[]
        for p in f.Pads():
            q=p.GetBoundingBox(); xs+=[mm(q.GetX()),mm(q.GetRight())]; ys+=[mm(q.GetY()),mm(q.GetBottom())]
        w,h=max(xs)-min(xs)+0.5,max(ys)-min(ys)+0.5; a=w*h; src='pads+0.25'
    if lib=='scratch.pretty': src+=' (scratch ESTIMATE footprint)'
    out[n]=dict(area=round(a,3),w=round(w,2),h=round(h,2),src=src)
    print('%-16s %-40s %5.2f x %5.2f  %7.3f mm2'%(n,src,w,h,a))
json.dump(out,open('libareas.json','w'),indent=1)

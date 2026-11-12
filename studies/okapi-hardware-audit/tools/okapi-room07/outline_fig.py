# Figure: v0.8.0 options. Today's outline, the notch a rectangle fills, and the B-SoM (J9) today and centered.
import pcbnew, sys, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt, matplotlib.patches as pa
b=pcbnew.LoadBoard('Okapi.kicad_pcb'); out=sys.argv[1]
fig,ax=plt.subplots(figsize=(7.5,13))
BLOCK={'D7','F2','Q3','Q4','R19','R20','R54','R81','R82','R83','R86','R87','S6','S7','U10','U8','USB2'}
for f in b.GetFootprints():
    r=f.GetReference()
    if r in ('J9','MS1') or f.IsFlipped(): continue
    cy=f.GetCourtyard(pcbnew.F_CrtYd); c=cy.BBox() if cy.OutlineCount() else f.GetBoundingBox(False)
    x0,y0,x1,y1=[pcbnew.ToMM(v) for v in (c.GetX(),c.GetY(),c.GetRight(),c.GetBottom())]
    col='#c0392b' if r in BLOCK else ('#555555' if r.startswith('H') else '#bbbbbb')
    ax.add_patch(pa.Rectangle((x0,y0),x1-x0,y1-y0,fc=col if r in BLOCK or r.startswith('H') else '#dddddd',ec=col,lw=0.4,alpha=0.8))
    if r in BLOCK or r.startswith('H'): ax.text(x1+0.3,y0+1,r,fontsize=6,color=col)
for d in b.GetDrawings():
    if d.GetLayerName()!='Edge.Cuts': continue
    s,e=d.GetStart(),d.GetEnd(); ax.plot([pcbnew.ToMM(s.x),pcbnew.ToMM(e.x)],[pcbnew.ToMM(s.y),pcbnew.ToMM(e.y)],'k',lw=1.5)
ax.add_patch(pa.Rectangle((116.126,37.504),25.0,35.0,fc='#2e86c1',alpha=0.15,ec='#2e86c1',ls='--',lw=1))
ax.text(128.6,55,'rectangle adds\n25 x 35 mm\n(875 mm²)',ha='center',va='center',color='#2e86c1',fontsize=9)
for dx,ls,lab in ((0,'-','B-SoM today'),(-12.2,'--','B-SoM centered (dx -12.2 mm)')):
    ax.add_patch(pa.Rectangle((145.39+dx,43.83),30.63,42.63,fc='none',ec='#7d3c98',ls=ls,lw=1.6))
    ax.add_patch(pa.Rectangle((149.87+dx,81.0),22.4,9.9,fc='#7d3c98',alpha=0.25 if dx==0 else 0.1,ec='#7d3c98',ls=ls,lw=0.8))
    ax.text(160.7+dx,46.5 if dx==0 else 50.5,lab,ha='center',color='#7d3c98',fontsize=8)
ax.set_xlim(114,183); ax.set_ylim(175,35); ax.set_aspect('equal')
ax.set_title('Okapi top side: red = B-SoM support parts that move with J9;\ngray = mounting holes; blue = what a rectangular outline adds',fontsize=9)
ax.set_xlabel('x (mm)'); ax.set_ylabel('y (mm)')
fig.savefig(out,dpi=200,bbox_inches='tight')

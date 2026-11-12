# Figure: the v0.7.0 placement plan on the top side. python3 render.py <plan board> <out.png>
# The board is plotted by kicad-cli (F.Cu, F.Silkscreen, Edge.Cuts); new parts are boxed: green = fits as routed,
# orange = needs tracks moved (from KiCad's DRC on the plan board, drc.json beside it).
import subprocess, json, sys, os, pcbnew
pcb,out=sys.argv[1],sys.argv[2]; S=os.path.dirname(os.path.abspath(out))
NEW=json.load(open('placed_mix_F.json'))
drc=json.load(open(os.path.join(os.path.dirname(pcb),'drc.json')))
bad={w for v in drc['violations'] for i in v['items'] for w in [p[1] for p in NEW] if ('of '+w) in i['description'] or i['description']=='Footprint '+w}
svg=out[:-4]+'.svg'
subprocess.run(['kicad-cli','pcb','export','svg','--mode-single','--fit-page-to-board','--exclude-drawing-sheet','-l','F.Cu,F.Silkscreen,Edge.Cuts','-o',svg,pcb],check=True,capture_output=True)
subprocess.run(['inkscape',svg,'--export-type=png','--export-dpi=600','--export-background=white','--export-filename='+out],check=True,capture_output=True)
b=pcbnew.LoadBoard(pcb); bb=b.GetBoardEdgesBoundingBox()
X0,Y0,W=pcbnew.ToMM(bb.GetX()),pcbnew.ToMM(bb.GetY()),pcbnew.ToMM(bb.GetWidth())
w=int(subprocess.check_output(['identify','-format','%w',out])); s=w/W
draw=[]
for issue,ref,fp,side,rot,x,y,d,why in NEW:
    if side is None: continue
    f=b.FindFootprintByReference(ref); c=f.GetBoundingBox(False)
    xa,ya,xb,yb=[(pcbnew.ToMM(v)-o)*s for v,o in ((c.GetX(),X0),(c.GetY(),Y0),(c.GetRight(),X0),(c.GetBottom(),Y0))]
    col='#e07000' if ref in bad else '#00a050'
    draw+=['-stroke',col,'-strokewidth','6','-fill','none','-draw','rectangle %d,%d %d,%d'%(xa-6,ya-6,xb+6,yb+6),
           '-stroke','none','-fill',col,'-pointsize','40','-draw','text %d,%d "%s"'%(xb+10,ya+20,issue)]
subprocess.run(['convert',out]+draw+['-gravity','north','-background','white','-splice','0x90','-pointsize','46','-fill','black','-annotate','+0+12',
                'Okapi v0.7.0, top side: green fits as routed, orange needs tracks moved',out],check=True)

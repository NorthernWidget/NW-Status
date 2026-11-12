import subprocess, json, pcbnew
P=json.load(open('res_PARTS_parts2.json_crt.json'))
NEW={p[1]:p[0] for p in P if p[3]}
def run(c): subprocess.run(c,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
def rend(pcb,side,png):
    L='F.Cu,F.SilkS,F.Fab,Edge.Cuts' if side=='F' else 'B.Cu,B.SilkS,B.Fab,Edge.Cuts'
    svg=png[:-4]+'.svg'
    c=['kicad-cli','pcb','export','svg','--mode-single','--fit-page-to-board','--exclude-drawing-sheet','-l',L,'-o',svg,pcb]
    if side=='B': c.insert(-3,'--mirror')
    run(c); run(['inkscape',svg,'--export-type=png','--export-dpi=1000','--export-background=white','--export-filename='+png])
b=pcbnew.LoadBoard('KiCAD/Margay_room.kicad_pcb')
bb=b.GetBoardEdgesBoundingBox(); X0,Y0,W=pcbnew.ToMM(bb.GetX()),pcbnew.ToMM(bb.GetY()),pcbnew.ToMM(bb.GetWidth())
items=[]
for f in b.GetFootprints():
    if f.GetReference() in NEW:
        c=f.GetBoundingBox(False); items.append((f.GetReference(),NEW[f.GetReference()],'B' if f.IsFlipped() else 'F',[pcbnew.ToMM(v) for v in (c.GetX(),c.GetY(),c.GetRight(),c.GetBottom())]))
c20=b.FindFootprintByReference('C20')
for side,tag,title in (('F','top','Top: blue = proposed parts (placement only, tracks not rerouted); orange = C20, removed by #70'),('B','bot','Bottom, viewed from below (mirrored): blue = proposed parts')):
    png=f'r/{tag}.png'; rend('KiCAD/Margay_room.kicad_pcb',side,png)
    w=int(subprocess.check_output(['identify','-format','%w',png])); s=w/W
    draw=[]
    boxes=[(r,i,sd,bx,'blue') for r,i,sd,bx in items]
    if side=='F': boxes.append(('C20','#70','F',[150.79,109.97,153.83,112.03],'orange'))
    for ref,iss,sd,(xa,ya,xb,yb),col in boxes:
        if sd!=side: continue
        if side=='B': xa,xb=X0+W-(xb-X0),X0+W-(xa-X0)
        px=[(xa-X0)*s,(ya-Y0)*s,(xb-X0)*s,(yb-Y0)*s]
        draw+=['-stroke',col,'-strokewidth','6','-fill','none','-draw','rectangle %d,%d %d,%d'%tuple(px),
               '-stroke','none','-fill',col,'-pointsize','34','-draw','text %d,%d "%s %s"'%(px[0],max(30,px[1]-8),iss,ref)]
    run(['convert',png]+draw+['-gravity','north','-background','white','-splice','0x70','-fill','black','-pointsize','40','-annotate','+0+12',title,f'r/{tag}_l.png'])
run(['convert','r/top_l.png','r/bot_l.png','-background','white','-splice','0x30','-append','+repage','-resize','50%','room31.png'])

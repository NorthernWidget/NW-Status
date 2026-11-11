"""Are vias open in the solder mask? Counts mask-Gerber flashes at every via of a board.
usage: python3 gerber_vias.py eagle <board.brd> <mask.gbr> | kicad <board.kicad_pcb> <mask.gbr>
Eagle Gerbers are in the .brd's own coordinates; a KiCad Gerber export (no origin option) is in the board's page coordinates,
y down, which the Gerber writes negated."""
import sys,re,collections
import xml.etree.ElementTree as ET
def flashes(path):
    t=open(path).read(); fs=re.search(r'%FSLAX(\d)(\d)Y',t); dec=10**int(fs.group(2))
    ap={m.group(1):m.group(2) for m in re.finditer(r'%ADD(\d+)([^*]*)\*%',t)}
    cur=None; x=y=0; out=[]
    for m in re.finditer(r'(?:G\d+)?(?:X(-?\d+))?(?:Y(-?\d+))?D(\d+)\*',t):
        if m.group(3) and int(m.group(3))>=10 and not m.group(1) and not m.group(2): cur=m.group(3); continue
        if m.group(1): x=int(m.group(1))/dec
        if m.group(2): y=int(m.group(2))/dec
        if m.group(3) in('03','3'): out.append((x,y,ap.get(cur)))
    return out
kind,b,g=sys.argv[1:4]
if kind=='eagle':
    r=ET.parse(b).getroot(); vias=[(float(v.get('x')),float(v.get('y')),v.get('drill')) for s in r.iter('signal') for v in s.findall('via')]
else:
    import pcbnew; bd=pcbnew.LoadBoard(b)
    vias=[(pcbnew.ToMM(t.GetPosition().x),-pcbnew.ToMM(t.GetPosition().y),'%.3f'%pcbnew.ToMM(t.GetDrill())) for t in bd.GetTracks() if t.GetClass()=='PCB_VIA']
F=flashes(g); idx=collections.defaultdict(list)
for x,y,a in F: idx[(round(x,1),round(y,1))].append((x,y,a))
hit=collections.Counter(); miss=collections.Counter(); aps=collections.Counter()
for x,y,d in vias:
    found=[f for dx in(-0.1,0,0.1) for dy in(-0.1,0,0.1) for f in idx[(round(x+dx,1),round(y+dy,1))] if abs(f[0]-x)<0.005 and abs(f[1]-y)<0.005]
    (hit if found else miss)[d]+=1
    for f in found[:1]: aps[(d,f[2])]+=1
print(g); print('  mask flashes',len(F),'vias',len(vias)); print('  vias with a mask opening, by drill:',dict(hit)); print('  vias without:',dict(miss)); print('  opening aperture by drill:',dict(aps))

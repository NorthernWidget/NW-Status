"""Per-package inventory: Eagle package (from the .brd <libraries>) against the KiCad library footprint and board instances.

usage: python3 inventory.py <eagle.brd> <board.kicad_pcb> <lib.pretty> <out.json> [EagleRef=KiCadRef ...]
Prints, for every package used by an element: Eagle items per layer, KiCad library items per layer, KiCad board-instance
items per layer (first instance, side normalized to front), and pad-by-pad differences. Read-only.
"""
import sys,json,math,collections,os
import xml.etree.ElementTree as ET
import pcbnew
brd,kpcb,pretty,out=sys.argv[1:5]
ALIAS=dict(a.split('=') for a in sys.argv[5:])   # Eagle ref=KiCad ref, for a part renamed in KiCad (U$4=LOGO1)
root=ET.parse(brd).getroot()
LN={l.get('number'):l.get('name') for l in root.iter('layer')}
def line_of(path,needle):
    with open(path) as f:
        for i,l in enumerate(f,1):
            if needle in l: return i
pkgs={}
for lib in root.find('.//board/libraries'):
    for p in lib.iter('package'): pkgs[(lib.get('name'),p.get('name'))]=p
elements=collections.defaultdict(list)
for e in root.iter('element'): elements[(e.get('library'),e.get('package'))].append(e.get('name'))
def rot(s):
    s=s or 'R0'; m='M' in s; return float(s.replace('M','').replace('S','').lstrip('R') or 0),m
def eagle_inv(p):
    L=collections.Counter(); pads=[]
    for c in p:
        if c.tag in('description',): continue
        if c.tag=='pad':
            r,_=rot(c.get('rot'))
            pads.append(dict(kind='th',name=c.get('name'),x=float(c.get('x')),y=float(c.get('y')),drill=float(c.get('drill')),dia=float(c.get('diameter') or 0),
                 shape=c.get('shape','round'),rot=r,stop=c.get('stop','yes'),thermals=c.get('thermals','yes'),first=c.get('first','no')))
            L['17 Pads']+=1
        elif c.tag=='smd':
            r,_=rot(c.get('rot'))
            pads.append(dict(kind='smd',name=c.get('name'),x=float(c.get('x')),y=float(c.get('y')),dx=float(c.get('dx')),dy=float(c.get('dy')),layer=c.get('layer'),
                 roundness=int(c.get('roundness') or 0),rot=r,stop=c.get('stop','yes'),cream=c.get('cream','yes'),thermals=c.get('thermals','yes')))
            L['%s %s smd'%(c.get('layer'),LN.get(c.get('layer')))]+=1
        elif c.tag=='hole':
            pads.append(dict(kind='hole',name='',x=float(c.get('x')),y=float(c.get('y')),drill=float(c.get('drill'))))
            L['45 Holes']+=1
        else:
            k=c.get('layer'); L['%s %s %s%s'%(k,LN.get(k),c.tag,' curve' if c.get('curve') else '')]+=1
    return L,pads
def klayer(fp,item_layer):
    n=fp.GetBoard().GetLayerName(item_layer) if fp.GetBoard() else pcbnew.LayerName(item_layer)
    return n
SWAP={'F.':'B.','B.':'F.'}
def kinv(fp,flip):
    L=collections.Counter(); pads=[]
    def nm(l):
        n=pcbnew.BOARD.GetStandardLayerName(l)
        if flip and n[:2] in SWAP: n=SWAP[n[:2]]+n[2:]
        return n
    for it in fp.GraphicalItems():
        cls=it.GetClass().replace('PCB_','').replace('FP_','')
        if hasattr(it,'GetShapeStr'): cls+=' '+it.GetShapeStr()
        L['%s %s'%(nm(it.GetLayer()),cls)]+=1
    for z in fp.Zones():
        ls=[nm(l) for l in z.GetLayerSet().Seq()]
        ko=z.GetIsRuleArea()
        desc='zone' if not ko else 'keepout[%s%s%s%s%s]'%('T' if z.GetDoNotAllowTracks() else 't','V' if z.GetDoNotAllowVias() else 'v','P' if z.GetDoNotAllowPads() else 'p','Z' if z.GetDoNotAllowZoneFills() else 'z','F' if z.GetDoNotAllowFootprints() else 'f')
        L['%s %s'%('+'.join(ls),desc)]+=1
    for p in fp.Pads():
        a=p.GetAttribute()
        kind={pcbnew.PAD_ATTRIB_PTH:'th',pcbnew.PAD_ATTRIB_SMD:'smd',pcbnew.PAD_ATTRIB_NPTH:'hole',pcbnew.PAD_ATTRIB_CONN:'conn'}[a]
        pos=p.GetFPRelativePosition()
        sh=p.GetShape(pcbnew.F_Cu) if hasattr(pcbnew,'F_Cu') else p.GetShape()
        lay=sorted(nm(l) for l in p.GetLayerSet().Seq())
        d=dict(kind=kind,name=p.GetNumber(),x=pcbnew.ToMM(pos.x),y=-pcbnew.ToMM(pos.y),sx=pcbnew.ToMM(p.GetSize(pcbnew.F_Cu).x),sy=pcbnew.ToMM(p.GetSize(pcbnew.F_Cu).y),
               rot=p.GetFPRelativeOrientation().AsDegrees(),shape=p.ShowPadShape(pcbnew.F_Cu),layers=lay,
               drill=pcbnew.ToMM(p.GetDrillSize().x),drilly=pcbnew.ToMM(p.GetDrillSize().y),
               rr=p.GetRoundRectRadiusRatio(pcbnew.F_Cu),zc=int(p.GetLocalZoneConnection()) if hasattr(p,'GetLocalZoneConnection') else None,
               off=(pcbnew.ToMM(p.GetOffset(pcbnew.F_Cu).x),pcbnew.ToMM(p.GetOffset(pcbnew.F_Cu).y)),
               mm=p.GetLocalSolderMaskMargin(), pm=p.GetLocalSolderPasteMargin())
        for k in ('mm','pm'):
            v=d[k]; d[k]=None if v is None else (pcbnew.ToMM(v) if not hasattr(v,'has_value') else (pcbnew.ToMM(v.value()) if v.has_value() else None))
        pads.append(d); L['pad '+kind]+=1
    return L,pads
board=pcbnew.LoadBoard(kpcb)
byref={fp.GetReference():fp for fp in board.GetFootprints()}
res={}
for (lib,pk),refs in sorted(elements.items(),key=lambda kv:kv[0][1]):
    p=pkgs[(lib,pk)]
    EL,EP=eagle_inv(p)
    refs=[ALIAS.get(r,r) for r in refs]
    insts=[byref[r] for r in refs if r in byref]
    missing=[r for r in refs if r not in byref]
    fpn=insts[0].GetFPID().GetLibItemName().wx_str() if insts else pk   # no instance (part removed in KiCad): the library footprint of the package's name
    libfp=None
    if fpn and os.path.exists(os.path.join(pretty,fpn+'.kicad_mod')):
        libfp=pcbnew.FootprintLoad(pretty,fpn)
    LL,LP=kinv(libfp,False) if libfp else (None,None)
    IL=[]
    for fp in insts:
        il,ip=kinv(fp,fp.IsFlipped()); IL.append((fp.GetReference()+'['+fp.GetFPID().GetLibItemName().wx_str()+']',fp.IsFlipped(),dict(il),ip))
    res['%s/%s'%(lib,pk)]=dict(lib=lib,package=pk,refs=refs,missing=missing,fp=fpn,line=line_of(brd,'<package name="%s"'%pk),
        eagle_layers=dict(EL),eagle_pads=EP,lib_layers=dict(LL) if LL else None,lib_pads=LP,instances=IL)
json.dump(res,open(out,'w'),indent=1)
print(brd,'packages used:',len(res),'elements:',sum(len(v['refs']) for v in res.values()),'missing on KiCad board:',sum(len(v['missing']) for v in res.values()))

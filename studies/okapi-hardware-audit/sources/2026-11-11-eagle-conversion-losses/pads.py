"""Pad-by-pad comparison of each Eagle package (from the .brd) with its KiCad library footprint, matched by position.
usage: python3 pads.py <inventory.json>
Effective Eagle through-hole size: max(diameter, drill + 2 x clamp(0.25 x drill, 5 mil, 20 mil)) (the DRU of both boards:
rvPadTop 0.25, rlMinPadTop 5mil, rlMaxPadTop 20mil); a long or offset pad is that by twice it (psElongation 100).
Eagle SMD roundness r % is KiCad roundrect ratio r/200. Prints only differences, and a count per package."""
import json,sys,math
r=json.load(open(sys.argv[1]))
TOL=0.0011
def eff(d,dr): return max(d,dr+2*min(max(0.25*dr,0.127),0.508))
def norm(sx,sy,rot):
    q=round(rot)%180
    if q==90: return sy,sx
    if q==0: return sx,sy
    return None
tot=0; npk=0
for k,v in r.items():
    if not v['lib_pads'] and not v['eagle_pads']: continue
    npk+=1
    E=v['eagle_pads']; K=list(v['lib_pads'] or []); out=[]
    if len(E)!=len(K): out.append('pad count eagle %d kicad %d'%(len(E),len(K)))
    used=set()
    for e in E:
        best=min(((math.hypot(p['x']-e['x'],p['y']-e['y']),i) for i,p in enumerate(K) if i not in used),default=(9,None))
        if best[0]>0.01: out.append('%s %s at (%g,%g): no KiCad pad at that position (nearest %.3f mm)'%(e['kind'],e['name'],e['x'],e['y'],best[0])); continue
        i=best[1]; used.add(i); p=K[i]; d=[]
        if p['kind']!=e['kind']: d.append('kind %s->%s'%(e['kind'],p['kind']))
        ml=[l for l in p['layers'] if 'Mask' in l]; pl=[l for l in p['layers'] if 'Paste' in l]
        if e['kind']=='smd':
            want=(e['dx'],e['dy']); got=(p['sx'],p['sy'])
            if (e['rot']-p['rot'])%180>0.01:
                n1=norm(e['dx'],e['dy'],e['rot']); n2=norm(p['sx'],p['sy'],p['rot'])
                if n1 is None or n2 is None: d.append('rot %g vs %g (not orthogonal)'%(e['rot'],p['rot']))
                else: want,got=n1,n2
            if abs(want[0]-got[0])>TOL or abs(want[1]-got[1])>TOL: d.append('size %gx%g -> %gx%g'%(want+got))
            wr=e['roundness']/200.
            if e['roundness']==0 and p['shape']!='Rectangle': d.append('shape rect -> %s'%p['shape'])
            if e['roundness']>0 and not (p['shape'] in ('Roundrect','Round rect','Rounded rectangle') or 'ound' in p['shape']): d.append('roundness %d -> %s'%(e['roundness'],p['shape']))
            if e['roundness']>0 and abs(p['rr']-wr)>0.01 and p['shape']!='Oval': d.append('roundness %d (ratio %.3f) -> ratio %.3f'%(e['roundness'],wr,p['rr']))
            if (e['stop']=='no')!=(not ml): d.append('stop=%s, KiCad mask layers %s'%(e['stop'],ml))
            if (e['cream']=='no')!=(not pl): d.append('cream=%s, KiCad paste layers %s'%(e['cream'],pl))
            if e['thermals']=='no': d.append('thermals=no, KiCad zone connection %s'%p['zc'])
        elif e['kind']=='th':
            if abs(e['drill']-p['drill'])>TOL: d.append('drill %g -> %g'%(e['drill'],p['drill']))
            if abs(p['drill']-p['drilly'])>TOL: d.append('KiCad oblong drill %gx%g'%(p['drill'],p['drilly']))
            w=eff(e['dia'],e['drill']); sh=e['shape']
            want={'round':(w,w),'square':(w,w),'octagon':(w,w),'long':(2*w,w),'offset':(2*w,w)}[sh]
            n2=norm(p['sx'],p['sy'],p['rot']); n1=norm(want[0],want[1],e['rot'])
            if n1 and n2 and (abs(n1[0]-n2[0])>TOL or abs(n1[1]-n2[1])>TOL): d.append('size %s dia %g drill %g: Eagle fabricates %.4gx%.4g, KiCad %.4gx%.4g'%(sh,e['dia'],e['drill'],n1[0],n1[1],n2[0],n2[1]))
            kshape={'round':'Circle','square':'Rectangle','octagon':'Chamfered rect','long':'Oval','offset':'Oval'}[sh]
            if p['shape']!=kshape: d.append('shape %s -> %s'%(sh,p['shape']))
            if sh=='offset' and abs(p['off'][0])+abs(p['off'][1])<TOL: d.append('offset pad without drill offset')
            if e['stop']=='no' and ml: d.append('stop=no but KiCad mask %s'%ml)
            if e['stop']!='no' and len(ml)<2: d.append('KiCad mask layers %s'%ml)
            if e['thermals']=='no': d.append('thermals=no, KiCad zone connection %s'%p['zc'])
            if e['first']=='yes': d.append('first=yes')
        else:
            if abs(e['drill']-p['drill'])>TOL: d.append('hole drill %g -> %g'%(e['drill'],p['drill']))
            if abs(p['sx']-p['drill'])>TOL: d.append('NPTH pad size %g vs drill %g'%(p['sx'],p['drill']))
            if len(ml)<2: d.append('hole mask layers %s'%ml)
        if p['mm'] is not None or p['pm'] is not None: d.append('local margins mask %s paste %s'%(p['mm'],p['pm']))
        if d: out.append('%s %s -> %s: %s'%(e['kind'],e['name'],p['name'],'; '.join(d)))
    for i,p in enumerate(K):
        if i not in used: out.append('KiCad pad %s %s at (%g,%g) has no Eagle pad'%(p['kind'],p['name'],p['x'],p['y']))
    print('== %s fp %s refs %s: %d differences'%(k,v['fp'],','.join(v['refs'][:6])+('...' if len(v['refs'])>6 else ''),len(out)))
    for o in out: print('   ',o)
    tot+=len(out)
print('packages compared %d, differences %d'%(npk,tot))

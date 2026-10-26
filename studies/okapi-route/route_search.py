import xml.etree.ElementTree as ET, math, sys, collections
import numpy as np
from PIL import Image, ImageDraw
RES=0.05
import os
TW=float(os.environ.get("TW","0.1524"))
CL=float(os.environ.get("CL","0.1524"))
VIA_D=float(os.environ.get("VIA","0.6")); VIA_DRILL=0.3
r=ET.parse('Okapi.brd').getroot()
els={e.get('name'):e for e in r.iter('element')}
# board outline
xs=[];ys=[]
for pl in r.iter('plain'):
    for w in pl.iter('wire'):
        if w.get('layer')=='20': xs+=[float(w.get('x1')),float(w.get('x2'))]; ys+=[float(w.get('y1')),float(w.get('y2'))]
X0,X1,Y0,Y1=min(xs),max(xs),min(ys),max(ys)
W=int((X1-X0)/RES)+1; H=int((Y1-Y0)/RES)+1
def px(x,y): return ((x-X0)/RES, (Y1-y)/RES)
# packages
pkgs={}
for l in r.iter('library'):
    for p in l.iter('package'): pkgs[(l.get('name'),p.get('name'))]=p
def rot_of(s):
    if not s: return 0.0,False
    m=s.startswith('M'); a=float(s.lstrip('MSR') or 0); return a,m
def xform(ex,ey,ang,mir,x,y):
    if mir: x=-x
    a=math.radians(ang); return ex+x*math.cos(a)-y*math.sin(a), ey+x*math.sin(a)+y*math.cos(a)
# images: value 255 = blocked. per layer, keyed 1 (top) and 16 (bottom). Also own-net masks.
img={1:Image.new('L',(W,H),0),16:Image.new('L',(W,H),0)}
drw={k:ImageDraw.Draw(v) for k,v in img.items()}
own={1:Image.new('L',(W,H),0),16:Image.new('L',(W,H),0)}
odr={k:ImageDraw.Draw(v) for k,v in own.items()}
NET='MPPT_SHDN'; TARGET=('U41','17')
# target pad given
print('target pad',TARGET)
target_poly=None
def line(d,x1,y1,x2,y2,w):
    a=px(x1,y1); b=px(x2,y2); rad=w/2/RES
    d.line([a,b],fill=255,width=max(1,int(round(2*rad))))
    d.ellipse([a[0]-rad,a[1]-rad,a[0]+rad,a[1]+rad],fill=255); d.ellipse([b[0]-rad,b[1]-rad,b[0]+rad,b[1]+rad],fill=255)
def disc(d,x,y,dia):
    c=px(x,y); rad=dia/2/RES; d.ellipse([c[0]-rad,c[1]-rad,c[0]+rad,c[1]+rad],fill=255)
def poly(d,pts): d.polygon([px(x,y) for x,y in pts],fill=255)
def smd_corners(ex,ey,ang,mir,sx,sy,dx,dy,srot):
    a,_=rot_of(srot)
    cs=[]
    for cx,cy in [(-dx/2,-dy/2),(dx/2,-dy/2),(dx/2,dy/2),(-dx/2,dy/2)]:
        ra=math.radians(a); px_=sx+cx*math.cos(ra)-cy*math.sin(ra); py_=sy+cx*math.sin(ra)+cy*math.cos(ra)
        cs.append(xform(ex,ey,ang,mir,px_,py_))
    return cs
grow=CL+TW/2   # obstacle growth so the path centre stays clear
# net copper membership by (element,pad)
netpads={}
for s in r.iter('signal'):
    for c in s.iter('contactref'): netpads[(c.get('element'),c.get('pad'))]=s.get('name')
for name,e in els.items():
    ex,ey=float(e.get('x')),float(e.get('y')); ang,mir=rot_of(e.get('rot'))
    p=pkgs[(e.get('library'),e.get('package'))]
    for s in p.iter('smd'):
        lay=int(s.get('layer')); 
        if mir: lay=16 if lay==1 else 1
        cs=smd_corners(ex,ey,ang,mir,float(s.get('x')),float(s.get('y')),float(s.get('dx')),float(s.get('dy')),s.get('rot'))
        n=netpads.get((name,s.get('name')))
        if n==NET: poly(odr[lay],cs)
        elif (name,s.get('name'))==TARGET: target_poly=(lay,cs); poly(odr[lay],cs)
        else:
            # grow by drawing the polygon and a thick outline
            poly(drw[lay],cs); d=drw[lay]
            pts=[px(x,y) for x,y in cs]+[px(*cs[0])]
            d.line(pts,fill=255,width=int(round(2*grow/RES)),joint='curve')
            for pt in pts: d.ellipse([pt[0]-grow/RES,pt[1]-grow/RES,pt[0]+grow/RES,pt[1]+grow/RES],fill=255)
    for pd in p.iter('pad'):
        x,y=xform(ex,ey,ang,mir,float(pd.get('x')),float(pd.get('y'))); dia=float(pd.get('diameter') or 0) or float(pd.get('drill'))*2
        n=netpads.get((name,pd.get('name')))
        for lay in (1,16):
            if n==NET: disc(odr[lay],x,y,dia)
            else: disc(drw[lay],x,y,dia+2*grow)
    for h in p.iter('hole'):
        x,y=xform(ex,ey,ang,mir,float(h.get('x')),float(h.get('y')))
        for lay in (1,16): disc(drw[lay],x,y,float(h.get('drill'))+2*grow)
    for w in p.iter('wire'):
        lay=int(w.get('layer'))
        if lay in (1,16):
            if mir: lay=16 if lay==1 else 1
            a=xform(ex,ey,ang,mir,float(w.get('x1')),float(w.get('y1'))); b=xform(ex,ey,ang,mir,float(w.get('x2')),float(w.get('y2')))
            line(drw[lay],*a,*b,float(w.get('width'))+2*grow)
    for c in p.iter('circle'):
        lay=int(c.get('layer'))
        if lay in (1,16):
            x,y=xform(ex,ey,ang,mir,float(c.get('x')),float(c.get('y'))); disc(drw[lay],x,y,2*float(c.get('radius'))+float(c.get('width'))+2*grow)
for s in r.iter('signal'):
    n=s.get('name')
    for w in s.iter('wire'):
        lay=int(w.get('layer'))
        if lay not in (1,16): continue
        if n==NET: line(odr[lay],float(w.get('x1')),float(w.get('y1')),float(w.get('x2')),float(w.get('y2')),float(w.get('width')))
        else: line(drw[lay],float(w.get('x1')),float(w.get('y1')),float(w.get('x2')),float(w.get('y2')),float(w.get('width'))+2*grow)
    for v in s.iter('via'):
        x,y=float(v.get('x')),float(v.get('y')); dia=float(v.get('diameter') or 0) or float(v.get('drill'))+0.3
        for lay in (1,16):
            if n==NET: disc(odr[lay],x,y,dia)
            else: disc(drw[lay],x,y,dia+2*grow)
# board edge keep-in
edge=np.zeros((H,W),bool); m=int(0.5/RES); edge[:m,:]=edge[-m:,:]=True; edge[:,:m]=edge[:,-m:]=True
blocked={k:(np.array(img[k])>0)|edge for k in (1,16)}
ownm={k:np.array(own[k])>0 for k in (1,16)}
free={k:(~blocked[k])|ownm[k] for k in (1,16)}
# via feasibility: both layers free in a disc of radius VIA_D/2+CL
vr=int(math.ceil((VIA_D/2+CL)/RES))
from scipy.ndimage import binary_erosion
disk=np.zeros((2*vr+1,2*vr+1),bool); yy,xx=np.ogrid[-vr:vr+1,-vr:vr+1]; disk[xx*xx+yy*yy<=vr*vr]=True
viaok=binary_erosion(free[1]&free[16],disk)
print('free fraction top %.2f bottom %.2f via-ok %.3f'%(free[1].mean(),free[16].mean(),viaok.mean()))
# BFS from own-net copper (either layer) to target pad
start=np.zeros((2,H,W),bool); start[0]=ownm[1]; start[1]=ownm[16]
tl,cs=target_poly; timg=Image.new('L',(W,H),0); ImageDraw.Draw(timg).polygon([px(x,y) for x,y in cs],fill=255); tmask=np.array(timg)>0
goal=np.zeros((2,H,W),bool); goal[0 if tl==1 else 1]=tmask
# exclude the target pad from the start set
start[0]&=~tmask; start[1]&=~tmask
LAY=[free[1],free[16]]
dist=np.full((2,H,W),-1,np.int32); prev=np.full((2,H,W),-1,np.int64)
q=collections.deque()
for l in range(2):
    for (y,x) in zip(*np.nonzero(start[l])): dist[l,y,x]=0; q.append((l,y,x))
print('start cells',len(q))
found=None
VIA_COST=0  # BFS: vias free; we count them after
while q:
    l,y,x=q.popleft()
    if goal[l,y,x]: found=(l,y,x); break
    d=dist[l,y,x]+1
    for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
        ny,nx=y+dy,x+dx
        if 0<=ny<H and 0<=nx<W and LAY[l][ny,nx] and dist[l,ny,nx]<0:
            dist[l,ny,nx]=d; prev[l,ny,nx]=(l*H+y)*W+x; q.append((l,ny,nx))
    ol=1-l
    if viaok[y,x] and dist[ol,y,x]<0:
        dist[ol,y,x]=d; prev[ol,y,x]=(l*H+y)*W+x; q.append((ol,y,x))
if not found: print('NO ROUTE at this clearance'); sys.exit(0)
# trace back
path=[]; cur=found
while cur is not None:
    path.append(cur); p_=prev[cur]; 
    if p_<0: break
    cur=(p_//(H*W),(p_//W)%H,p_%W)
path.reverse()
vias=sum(1 for a,b in zip(path,path[1:]) if a[0]!=b[0])
length=sum(RES for a,b in zip(path,path[1:]) if a[0]==b[0])
top=sum(1 for a,b in zip(path,path[1:]) if a[0]==b[0]==0)*RES; bot=sum(1 for a,b in zip(path,path[1:]) if a[0]==b[0]==1)*RES
print('ROUTE FOUND: length %.1f mm (top %.1f, bottom %.1f), vias %d, from (%.1f,%.1f) to (%.1f,%.1f)'%(length,top,bot,vias,X0+path[0][2]*RES,Y1-path[0][1]*RES,X0+path[-1][2]*RES,Y1-path[-1][1]*RES))
# render
out=Image.new('RGB',(W,H),(20,20,20))
a1=np.array(img[1])>0; a16=np.array(img[16])>0
arr=np.array(out); arr[a16]=(60,60,120); arr[a1]=(120,60,60); arr[a1&a16]=(110,60,110)
arr[ownm[1]|ownm[16]]=(255,200,0); arr[tmask]=(0,255,0)
for l,y,x in path:
    arr[max(0,y-2):y+3,max(0,x-2):x+3]=(0,255,255) if l==0 else (255,0,255)
for a,b in zip(path,path[1:]):
    if a[0]!=b[0]: y,x=a[1],a[2]; arr[max(0,y-6):y+7,max(0,x-6):x+7]=(255,255,255)
Image.fromarray(arr).save('route_%s.png' % os.environ.get("CL","x"))
# zoomed crop around the path
ys_=[p[1] for p in path]; xs_=[p[2] for p in path]
crop=Image.fromarray(arr).crop((max(0,min(xs_)-80),max(0,min(ys_)-80),min(W,max(xs_)+80),min(H,max(ys_)+80)))
crop.save('crop_%s.png' % os.environ.get("CL","x")); print('images written')

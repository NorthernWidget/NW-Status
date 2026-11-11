"""Render an Eagle fab Gerber and the KiCad export of the same layer in one window (gerbv) and report the pixels that differ.
usage: python3 render_diff.py <eagle.brd> <eagle.gbr> <kicad.gbr> <dx> <dy> <out prefix> [dpi]
dx, dy: KiCad Gerber coordinates minus Eagle coordinates, in mm (from the element positions: KiCad x - Eagle x, -KiCad y - Eagle y).
Writes <prefix>_eagle.png, <prefix>_kicad.png, <prefix>_diff.png (red: only Eagle, blue: only KiCad) and prints the connected
regions of difference larger than 0.05 mm2 with their center in Eagle coordinates."""
import sys,subprocess,numpy as np
import xml.etree.ElementTree as ET
from PIL import Image
brd,eg,kg,dx,dy,pre=sys.argv[1:7]; dx,dy=float(dx),float(dy); dpi=int(sys.argv[7]) if len(sys.argv)>7 else 1000
r=ET.parse(brd).getroot()
xs=[];ys=[]
for w in r.find('.//plain'):
    if w.tag=='wire' and w.get('layer')=='20': xs+=[float(w.get('x1')),float(w.get('x2'))]; ys+=[float(w.get('y1')),float(w.get('y2'))]
import math
pkgs={(l.get('name'),p.get('name')):p for l in r.find('.//board/libraries') for p in l.iter('package')}
PADS=[]   # every pad, smd and hole of every element, in board coordinates
for e in r.iter('element'):
    ex,ey=float(e.get('x')),float(e.get('y')); s=e.get('rot') or 'R0'; mir='M' in s; a=math.radians(float(s.replace('M','').replace('S','').lstrip('R') or 0))
    for c in pkgs[(e.get('library'),e.get('package'))]:
        if c.tag in('pad','smd','hole'):
            x,y=float(c.get('x')),float(c.get('y'))
            if mir: x=-x
            PADS.append((ex+x*math.cos(a)-y*math.sin(a),ey+x*math.sin(a)+y*math.cos(a),e.get('name')+'.'+(c.get('name') or 'hole')+('(back)' if mir else '')))
for s in r.iter('signal'):
    for v in s.findall('via'): PADS.append((float(v.get('x')),float(v.get('y')),'via '+s.get('name')))
def nearest(x,y): return min((math.hypot(px-x,py-y),n) for px,py,n in PADS)
def near(x,y):
    d,n=nearest(x,y); return '%s (%.2f mm)'%(n,d)
SKIPVIA='--skip-vias' in sys.argv   # count regions centered on an Eagle via (within 0.05 mm) and do not list them
x0,y0=min(xs)-2,min(ys)-2; W,H=max(xs)-min(xs)+4,max(ys)-min(ys)+4
def render(g,ox,oy,out):
    subprocess.run(['gerbv','-x','png','-B','0','-D',str(dpi),'-O','%f;%f'%(ox/25.4,oy/25.4),'-W','%fx%f'%(W/25.4,H/25.4),'-b','#000000','-f','#FFFFFFFF','-o',out,g],check=True,capture_output=True)
    return np.array(Image.open(out).convert('L'))>127
a=render(eg,x0,y0,pre+'_eagle.png'); b=render(kg,x0+dx,y0+dy,pre+'_kicad.png')
h=min(a.shape[0],b.shape[0]); w=min(a.shape[1],b.shape[1]); a=a[:h,:w]; b=b[:h,:w]
px=25.4/dpi
img=np.zeros((h,w,3),np.uint8); img[a&b]=(90,90,90); img[a&~b]=(255,0,0); img[b&~a]=(0,128,255); Image.fromarray(img).save(pre+'_diff.png')
print(eg,'vs',kg); print('  copper area eagle %.2f mm2, kicad %.2f mm2, only eagle %.2f, only kicad %.2f'%(a.sum()*px*px,b.sum()*px*px,(a&~b).sum()*px*px,(b&~a).sum()*px*px))
from scipy import ndimage
for name,m in (('only in Eagle',a&~b),('only in KiCad',b&~a)):
    m=ndimage.binary_opening(m,iterations=2)   # drop the one-pixel rims that rasterizing two writers' arcs leaves
    lab,n=ndimage.label(m); sizes=ndimage.sum(m,lab,range(1,n+1))*px*px
    big=[(s,i+1) for i,s in enumerate(sizes) if s>0.05]
    if SKIPVIA:
        keep=[]; nv=0
        for s,i in big:
            yy,xx=np.where(lab==i); d,n=nearest(x0+xx.mean()*px,y0+H-yy.mean()*px)
            if n.startswith('via') and d<0.05: nv+=1
            else: keep.append((s,i))
        print('  %s: %d regions centered on an Eagle via, not listed'%(name,nv)); big=keep
    print('  %s: %d regions over 0.05 mm2 after a 2-pixel opening'%(name,len(big)))
    for s,i in sorted(big,reverse=True)[:int(sys.argv[8]) if len(sys.argv)>8 and sys.argv[8].isdigit() else 25]:
        yy,xx=np.where(lab==i); cx=x0+xx.mean()*px; cy=y0+H-yy.mean()*px
        print('     %.3f mm2 at Eagle (%.2f, %.2f), extent %.2f x %.2f mm, nearest %s'%(s,cx,cy,(xx.max()-xx.min()+1)*px,(yy.max()-yy.min()+1)*px,near(cx,cy)))

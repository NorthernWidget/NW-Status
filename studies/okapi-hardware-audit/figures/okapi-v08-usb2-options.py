"""USB2 placement options for Okapi v0.8 (Andy, 2026-11-11): (A) move the M.2 socket J9 left, USB2 horizontal at
the right edge; (B) fill the notch, USB2 horizontal at the new left edge. Geometry from Okapi.kicad_pcb (courtyards,
pads), Project-Okapi 28a74ae. Usage: python3 okapi-v08-usb2-options.py <dir holding board300.png> <out.png>"""
import sys
from PIL import Image, ImageDraw, ImageFont
S,OUT=sys.argv[1:3]
X0,Y0=116.1261,37.5036; YMAX=100.0
src=Image.open(f'{S}/board300.png').convert('RGB'); k0=src.size[0]/64.75
src=src.crop((0,0,src.size[0],int((YMAX-Y0)*k0)))
SC=1.5; src=src.resize((int(src.size[0]*SC),int(src.size[1]*SC))); k=k0*SC
src=Image.blend(src,Image.new('RGB',src.size,'white'),0.5)
F=lambda s,b=False: ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans%s.ttf'%('-Bold' if b else ''),s)
BLUE=(20,70,200); GREEN=(0,140,60); RED=(200,30,30); GRAY=(110,110,110); ORANGE=(230,110,0)
# USB-C (Andy's footprint) courtyard: 10.14 wide, 8.43 deep from the board edge
CW,CD=10.14,8.43
def panel(title,draw):
    pad=40; top=90; ext=8.43*k+20   # room to the left for a grown board
    cv=Image.new('RGB',(int(src.size[0]+ext+2*pad),src.size[1]+2*pad+top),'white'); ox=pad+ext
    cv.paste(src,(int(ox),pad+top)); d=ImageDraw.Draw(cv)
    Q=lambda x,y:(ox+(x-X0)*k,pad+top+(y-Y0)*k)
    def box(x0,y0,x1,y1,c,w=5,dash=False):
        if not dash: d.rectangle([Q(x0,y0),Q(x1,y1)],outline=c,width=w); return
        for (a,b) in (((x0,y0),(x1,y0)),((x1,y0),(x1,y1)),((x1,y1),(x0,y1)),((x0,y1),(x0,y0))):
            n=40
            for i in range(0,n,2):
                p=(a[0]+(b[0]-a[0])*i/n,a[1]+(b[1]-a[1])*i/n); q=(a[0]+(b[0]-a[0])*(i+1)/n,a[1]+(b[1]-a[1])*(i+1)/n)
                d.line([Q(*p),Q(*q)],fill=c,width=w)
    def tag(x,y,t,c,s=26): d.text(Q(x,y),t,font=F(s,True),fill=c,stroke_width=4,stroke_fill='white')
    d.text((pad,25),title,font=F(34,True),fill='black')
    draw(d,Q,box,tag)
    return cv
def common(d,Q,box,tag):
    box(127.31,73.38,178.42,96.55,GRAY,3); tag(128,97.0-2.6,'MS1 Feather socket',GRAY,22)
    a=Q(167.57,89.88); d.ellipse([a[0]-9,a[1]-9,a[0]+9,a[1]+9],fill=GREEN)
def A(d,Q,box,tag):
    common(d,Q,box,tag)
    box(145.45,40.89,175.96,91.42,BLUE,3,dash=True); tag(150,43,'J9 today',BLUE,22)
    s=3.81; box(145.45-s,40.89,175.96-s,91.42,BLUE,6); tag(147,52,'J9 moved 3.81 mm left',BLUE)
    for r,(x0,x1,y0,y1) in {'S6':(141.39,144.71,46.08,51.28),'R87':(141.53,144.57,51.45,52.51),'R86':(141.53,144.57,58.18,59.24),
        'S7':(141.39,144.71,59.54,64.74),'F2':(142.41,144.7,67.31,72.21),'U10':(138.89,142.64,73.25,76.79),'R54':(142.27,143.32,77.0,80.04),
        'U8':(138.49,142.02,82.08,85.88),'R20':(142.55,145.58,84.1,86.16),'D7':(141.99,146.39,86.71,89.64)}.items():
        box(x0,y0,x1,y1,RED,4)
    tag(128.5,50,'10 parts\nto move',RED)
    box(180.8761-CD,63.0,180.8761,63.0+CW,GREEN,6); tag(166,62,'USB2',GREEN)
    box(116.1261,37.5036,141.1261,72.5036,ORANGE,4,dash=True); tag(118,40,'notch\nfilled',ORANGE,22)
def B(d,Q,box,tag):
    common(d,Q,box,tag)
    box(145.45,40.89,175.96,91.42,BLUE,4); tag(150,43,'J9 stays',BLUE,22)
    box(116.1261,37.5036,141.1261,72.5036,ORANGE,4,dash=True); tag(118,40,'notch\nfilled',ORANGE,22)
    box(116.1261,50.0,116.1261+CD,50.0+CW,GREEN,6); tag(118,62,'USB2',GREEN)
    a=Q(167.57,89.88); b=Q(116.1261+CD,55.07); d.line([a,b],fill=GREEN,width=5)
    import math; tag(128,70,'%.0f mm straight\nfrom J9 USB pads'%math.hypot(167.57-(116.1261+CD),89.88-55.07),GREEN,22)
pa=panel('A: move the M.2 socket left',A); pb=panel('B: fill the notch, USB2 at the left',B)
W=pa.size[0]+pb.size[0]+20; H=max(pa.size[1],pb.size[1])
out=Image.new('RGB',(W,H),'white'); out.paste(pa,(0,0)); out.paste(pb,(pa.size[0]+20,0)); out.save(OUT); print(out.size)

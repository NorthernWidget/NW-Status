"""Compare an Eagle Excellon drill file with a KiCad one: every hit and slot, matched by position (KiCad shifted by dx, dy).
usage: python3 drills.py <eagle.xln> <kicad.drl> <dx> <dy> [eagle.brd]
Prints hits by diameter on each side and every hit or slot without a partner of the same diameter within 0.01 mm."""
import sys,re,collections,math
def parse(path):
    t=open(path).read().splitlines(); tools={}; cur=None; out=[]; metric=True; tz=False; fmt=None
    for l in t:
        m=re.match(r'^T(\d+)C([\d.]+)',l)
        if m: tools[m.group(1).lstrip('0')]=float(m.group(2)); continue
        if l.startswith('METRIC') or l.startswith('INCH'): metric=l.startswith('METRIC'); fmt=l
        m=re.match(r'^T(\d+)$',l)
        if m: cur=tools.get(m.group(1).lstrip('0')); continue
        m=re.match(r'^X(-?[\d.]+)Y(-?[\d.]+)(?:G85X(-?[\d.]+)Y(-?[\d.]+))?$',l)
        if m:
            def num(s):
                if '.' in s: return float(s)
                return int(s)/1000.0   # Eagle METRIC,TZ,000.000: three decimals implied
            x,y=num(m.group(1)),num(m.group(2))
            if not metric: x,y=x*25.4,y*25.4
            if m.group(3): x2,y2=num(m.group(3)),num(m.group(4)); out.append((cur,x,y,x2,y2))
            else: out.append((cur,x,y,None,None))
    return out
E=parse(sys.argv[1]); K=parse(sys.argv[2]); dx,dy=float(sys.argv[3]),float(sys.argv[4])
K=[(d,x-dx,y-dy,(x2-dx) if x2 is not None else None,(y2-dy) if y2 is not None else None) for d,x,y,x2,y2 in K]   # a KiCad Excellon file is y-up, as the Gerbers
print('Eagle hits by diameter:',sorted(collections.Counter((d,'slot' if x2 is not None else 'hole') for d,x,y,x2,y2 in E).items()))
print('KiCad hits by diameter:',sorted(collections.Counter((d,'slot' if x2 is not None else 'hole') for d,x,y,x2,y2 in K).items()))
def unmatched(A,B):
    out=[]
    for a in A:
        if not any(abs(a[0]-b[0])<0.011 and math.hypot(a[1]-b[1],a[2]-b[2])<0.01 for b in B): out.append(a)
    return out
for name,A,B in(('only in Eagle',E,K),('only in KiCad',K,E)):
    u=unmatched(A,B); print(name,len(u))
    for a in u: print('   ',a)

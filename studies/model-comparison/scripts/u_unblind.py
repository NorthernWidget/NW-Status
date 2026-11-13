# Unblind the judged CSVs (run only after all judges marked COMPLETE). Duplicate ids (the same human turn present in
# both session files, which overlap 10-20 to 10-22) are counted once, first judgment kept.
import csv,json,os,collections,math
S=os.path.dirname(os.path.abspath(__file__))
def read(fn):
    rows={}
    for line in open(os.path.join(S,fn)):
        if line.startswith('#') or line.startswith('id,'): continue
        p=line.rstrip('\n').split(',',3)
        if len(p)>=2 and p[0] not in rows: rows[p[0]]=p
    return rows
def wilson(k,n,z=1.96):
    if n==0: return (0,0)
    p=k/n; d=1+z*z/n; c=p+z*z/(2*n); h=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))
    return ((c-h)/d*100,(c+h)/d*100)
T=json.load(open(os.path.join(S,'turns.json')))
uu=collections.Counter(t['uuid'] for t in T); print('duplicate human-turn uuids in turns.json',sum(1 for v in uu.values() if v>1))
key=json.load(open(os.path.join(S,'turns_key.json')))
J={**read('turns_judged_1.csv'),**read('turns_judged_2.csv')}
print('turn judgments',len(J),'keyed',len(key))
c=collections.defaultdict(collections.Counter); ty=collections.defaultdict(collections.Counter)
for h,p in J.items():
    m=key[h]['model']; c[m][p[1]]+=1
    if p[1]=='CORRECTION': ty[m][p[2]]+=1
for m in sorted(c):
    n=sum(c[m].values()); k=c[m]['CORRECTION']; u=c[m]['UNCLEAR']
    lo,hi=wilson(k,n); lo2,hi2=wilson(k+u,n)
    print(m,'n',n,dict(c[m]),'correction %.1f%% [%.1f-%.1f]'%(100*k/n,lo,hi),'incl unclear %.1f%% [%.1f-%.1f]'%(100*(k+u)/n,lo2,hi2),'types',dict(ty[m]))
# touches
tk=json.load(open(os.path.join(S,'touch_key.json'))); TJ=read('touch_judged.csv')
tc=collections.defaultdict(collections.Counter)
for h,p in TJ.items(): tc[tk[h]['author'].split('-')[0]][p[1]]+=1; tc[tk[h]['author']][p[1]]+=1
for m in sorted(tc): print('touch',m,dict(tc[m]))
# fixword vs judged
fw=collections.Counter((tk[h]['fixword'],p[1]) for h,p in TJ.items()); print('fixword x judged',dict(fw))

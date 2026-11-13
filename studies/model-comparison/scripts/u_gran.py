# Unblind the granularity judgments: share MULTI and mean message quality, by model and by model x kind.
import json,os,collections,statistics
S=os.path.dirname(os.path.abspath(__file__))
key=json.load(open(os.path.join(S,'gran_key.json'))); J={}
for l in open(os.path.join(S,'gran_judged.csv')):
    if l.startswith('#') or l.startswith('id,'): continue
    p=l.rstrip('\n').split(',',3)
    if p[0] in key and p[0] not in J: J[p[0]]=p
print('judged',len(J))
for grp in (lambda k:k['model'], lambda k:(k['model'],k['kind'])):
    g=collections.defaultdict(list)
    for h,p in J.items(): g[grp(key[h])].append(p)
    for k in sorted(g):
        v=g[k]; c=collections.Counter(p[1] for p in v); q=[int(p[2]) for p in v if p[2].isdigit()]
        print(k,'n',len(v),dict(c),'MULTI %.1f%%'%(100*c['MULTI']/len(v)),'quality %.2f'%statistics.mean(q))

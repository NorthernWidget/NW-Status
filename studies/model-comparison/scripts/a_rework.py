# Summaries of rework.json. Windows: a commit counts toward a W-day touch rate only if W full days have elapsed
# since it (now = 2026-11-10T21:00Z), so recent Opus 5.5 commits are not credited with an unobserved quiet period.
import json,collections,statistics,os,sys,datetime,subprocess
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from common import *
R=json.load(open(os.path.join(S,'rework.json')))
NOW=datetime.datetime(2026,11,10,21,0,tzinfo=datetime.timezone.utc)
for r in R:
    r['dt']=datetime.datetime.fromisoformat(r['date'])
    for t in r['touches']:
        t['dt']=datetime.datetime.fromisoformat(git(r['repo'],'log','-1','--format=%aI',t['sha']).strip())
        t['lag_h']=(t['dt']-r['dt']).total_seconds()/3600
def per(rows,label):
    rows=[r for r in rows if r['added']>0]
    if not rows: return
    n=len(rows)
    lw_head=sum(r['surv_head'] for r in rows)/sum(r['added'] for r in rows)
    med_head=statistics.median(r['surv_head']/r['added'] for r in rows)
    s3=[r for r in rows if r['surv3'] is not None and (NOW-r['dt']).days>=3]
    lw3=sum(r['surv3'] for r in s3)/max(1,sum(r['added'] for r in s3)); med3=statistics.median(r['surv3']/r['added'] for r in s3) if s3 else float('nan')
    out=[label,'n',n,'HEAD lw %.3f med %.3f'%(lw_head,med_head),'| 3d n',len(s3),'lw %.3f med %.3f'%(lw3,med3)]
    for W in (2,7):
        el=[r for r in rows if (NOW-r['dt']).total_seconds()>=W*86400]
        if not el: out+=['| %dd n 0'%W]; continue
        anyt=sum(1 for r in el if any(t['lag_h']<=24*W for t in r['touches']))
        fixt=sum(1 for r in el if any(t['lag_h']<=24*W and t['fixword'] for t in r['touches']))
        out+=['| %dd n %d touched %.1f%% fixword %.1f%%'%(W,len(el),100*anyt/len(el),100*fixt/len(el))]
    print(*out)
def group(key,title):
    print('##',title); g=collections.defaultdict(list)
    for r in R: g[key(r)].append(r)
    for k in sorted(g): per(g[k],str(k))
group(lambda r:fam(r['model']),'family')
group(lambda r:r['model'],'model')
group(lambda r:(r['kind'],fam(r['model'])),'kind x family')
group(lambda r:(r['kind'],r['date'][:7],r['model']),'kind x month x model')
# who did the fix-word touches
c=collections.Counter()
for r in R:
    for t in r['touches']:
        if t['fixword'] and t['lag_h']<=168: c[(r['model'],t['by'])]+=1
print('## fix-word touches within 7d: (author model, toucher)',dict(c))
json.dump([{k:v for k,v in r.items() if k!='dt'} | {'touches':[{k:v for k,v in t.items() if k!='dt'} for t in r['touches']]} for r in R],open(os.path.join(S,'rework_enriched.json'),'w'),indent=1)

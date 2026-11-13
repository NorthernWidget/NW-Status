# Summary-form compliance (reply >300 words ends with ---/**Summary.**) before and after Andy's explicit requests
# to resume summaries: Fable 2026-11-04T18:17Z; Opus 5.5 2026-11-08T06:47Z and 2026-11-10T03:57Z. Window: 48 h after each ask, same model only.
import json,re,os,datetime
S=os.path.dirname(os.path.abspath(__file__))
T=json.load(open(os.path.join(S,'turns.json')))
def comp(m,lo,hi):
    n=k=0
    for t in T:
        if t['model']==m and lo<t['ts']<=hi and len(t['prev'].split())>300:
            n+=1; k+=bool(re.search(r'\n---\s*\n+\*\*Summary\.\*\*',t['prev'][-2500:]))
    return k,n
for m,ask in [('claude-fable-5-1','2026-11-04T18:17'),('claude-opus-5-5','2026-11-08T06:47'),('claude-opus-5-5','2026-11-10T03:57')]:
    a=datetime.datetime.fromisoformat(ask)
    print(m,ask,'48h before',comp(m,(a-datetime.timedelta(hours=48)).isoformat(),ask),'0-12h after',comp(m,ask,(a+datetime.timedelta(hours=12)).isoformat()),'12-48h after',comp(m,(a+datetime.timedelta(hours=12)).isoformat(),(a+datetime.timedelta(hours=48)).isoformat()))

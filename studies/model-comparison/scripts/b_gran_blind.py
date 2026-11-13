# Blinded granularity sample: 45 commits per model (Fable 5.1, Opus 5, Opus 5.5), stratified across kinds
# by round-robin; message (trailers and model names stripped) + stat + first 70 diff lines.
import json,random,hashlib,re,os,sys,collections
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from common import *
d=json.load(open(os.path.join(S,'compliance.json')))
random.seed(5)
items=[];key={}
def clean(s):
    s='\n'.join(l for l in s.splitlines() if not re.match(r'^(Co-Authored-By|Claude-Session|Signed-off-by):',l,re.I))
    return re.sub(r'(?i)\b(claude|fable|opus|sonnet)\b(\s*[0-9.]+)?','[MODEL]',s).strip()
for m in ['fable-5.1','opus-5','opus-5.5']:
    byk=collections.defaultdict(list)
    for r in d:
        if r['model']==m: byk[r['kind']].append(r)
    for v in byk.values(): random.shuffle(v)
    pick=[]; ks=sorted(byk)
    while len(pick)<45 and any(byk.values()):
        for k in ks:
            if byk[k] and len(pick)<45: pick.append(byk[k].pop())
    for r in pick:
        h=hashlib.sha1(r['sha'].encode()).hexdigest()[:8]
        msg=clean(git(r['repo'],'log','-1','--format=%B',r['sha']))[:1500]
        st=git(r['repo'],'show','--stat=100','--format=',r['sha'])[:800]
        df='\n'.join(l[:160] for l in git(r['repo'],'show','--format=','-U1',r['sha']).splitlines()[:50])
        df=re.sub(r'(?i)\b(fable|opus)\b','[MODEL]',df)
        items.append((h,f"=== ITEM {h} repo={r['repo']}\n--- MESSAGE ---\n{msg}\n--- STAT ---\n{st}\n--- DIFF (first 70 lines) ---\n{df}\n"))
        key[h]=dict(model=m,kind=r['kind'],repo=r['repo'],sha=r['sha'],month=r['date'][:7])
items.sort()
open(os.path.join(S,'gran_blind.txt'),'w').write('\n'.join(x for _,x in items))
json.dump(key,open(os.path.join(S,'gran_key.json'),'w'),indent=1)
print(len(items))

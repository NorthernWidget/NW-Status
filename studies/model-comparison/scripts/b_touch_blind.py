# Blinded packet of 7-day touches (a later commit that deletes/modifies lines a sampled commit added).
# Model names, trailers and dates stripped; items ordered by a hash; key kept in a separate file not read until judging is done.
import json,random,hashlib,re,os,sys,collections
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from common import *
R=json.load(open(os.path.join(S,'rework_enriched.json')))
pairs=[]
for r in R:
    for t in r['touches']:
        if t['lag_h']<=168: pairs.append((r,t))
random.seed(7)
by=collections.defaultdict(list)
for p in pairs: by[fam(p[0]['model'])].append(p)
print({k:len(v) for k,v in by.items()})
pick=[]
for k,v in by.items(): pick+=random.sample(v,min(50,len(v)))
def clean(s):
    s='\n'.join(l for l in s.splitlines() if not re.match(r'^(Co-Authored-By|Claude-Session|Signed-off-by):',l,re.I))
    s=re.sub(r'(?i)\b(claude|fable|opus|sonnet)\b(\s*[0-9.]+)?','[MODEL]',s)
    s=re.sub(r'https://claude\.ai/\S+','[URL]',s)
    return s.strip()
items=[];key={}
for r,t in pick:
    h=hashlib.sha1((r['sha']+t['sha']).encode()).hexdigest()[:8]
    orig=clean(git(r['repo'],'log','-1','--format=%B',r['sha']))[:1200]
    later=clean(git(r['repo'],'log','-1','--format=%B',t['sha']))[:1500]
    diff=git(r['repo'],'show','--format=','-U0','--stat',t['sha'])[:600]
    items.append((h,f"=== ITEM {h}  repo={r['repo']}  lag_hours={t['lag_h']:.0f}  lines_of_original_touched={t['lines']}\n--- ORIGINAL ---\n{orig}\n--- LATER ---\n{later}\n--- LATER STAT ---\n{diff}\n"))
    key[h]=dict(author=r['model'],toucher=t['by'],kind=r['kind'],month=r['date'][:7],orig=r['sha'],later=t['sha'],repo=r['repo'],fixword=t['fixword'])
items.sort()
open(os.path.join(S,'touch_blind.txt'),'w').write('\n'.join(x for _,x in items))
json.dump(key,open(os.path.join(S,'touch_key.json'),'w'),indent=1)
print(len(items))

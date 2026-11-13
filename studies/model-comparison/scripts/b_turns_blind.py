# Blinded sample of human turns: 120 per model (Opus 5, Fable 5.1, Opus 5.5), seeded; model names scrubbed;
# no timestamps; items ordered by hash and split into two packets. Key in turns_key.json.
import json,random,hashlib,re,os,collections
S=os.path.dirname(os.path.abspath(__file__))
T=json.load(open(os.path.join(S,'turns.json')))
random.seed(11)
by=collections.defaultdict(list)
for t in T:
    if t['model'] in('claude-opus-5','claude-fable-5-1','claude-opus-5-5'): by[t['model']].append(t)
def scrub(s):
    s=re.sub(r'(?i)\b(claude[- ]?)?(fable|opus|sonnet)([- ]?[0-9.\-]+)?\b','[MODEL]',s)
    s=re.sub(r'https?://claude\.ai/\S+','[URL]',s)
    s=re.sub(r'20\d\d-\d\d-\d\d','[DATE]',s)
    return s
items=[]; key={}
for m,v in by.items():
    for t in random.sample(v,min(120,len(v))):
        h=hashlib.sha1(t['uuid'].encode()).hexdigest()[:8]
        prev=scrub(t['prev'].strip()); prev=('...'+prev[-700:]) if len(prev)>700 else prev
        u=scrub(t['user'].strip()); u=u[:900]+('...' if len(u)>900 else '')
        items.append((h,f"=== ITEM {h}\n--- ASSISTANT (end of previous reply) ---\n{prev}\n--- USER ---\n{u}\n"))
        key[h]=dict(model=m,ts=t['ts'],sid=t['sid'])
items.sort()
half=len(items)//2
open(os.path.join(S,'turns_blind_1.txt'),'w').write('\n'.join(x for _,x in items[:half]))
open(os.path.join(S,'turns_blind_2.txt'),'w').write('\n'.join(x for _,x in items[half:]))
json.dump(key,open(os.path.join(S,'turns_key.json'),'w'),indent=1)
print(len(items),half)

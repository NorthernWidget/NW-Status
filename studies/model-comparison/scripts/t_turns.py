# Extract Andy's human turns from the main-thread NW transcripts and attribute each to the model of the
# assistant reply episode that preceded it. Assistant "turn" = one reply episode: all main-thread assistant
# messages between two human turns. Human turn = type 'user', not sidechain, not meta, content is a string or has a
# text block, and is not a tool_result, a task-notification, a slash-command echo or a system/hook injection.
import json,os,re,collections,sys
P=os.path.expanduser('~/.claude/projects/-home-awickert-Dropbox-NorthernWidget-github/')
SESS=['30dafa30-bbc0-47e8-a62c-69dba3d468d7','cf0342fa-36e3-4818-be1e-2b4b31cc1756']
S=os.path.dirname(os.path.abspath(__file__))
def text_of(c):
    if isinstance(c,str): return c
    if isinstance(c,list):
        if any(isinstance(b,dict) and b.get('type')=='tool_result' for b in c): return None
        return '\n'.join(b.get('text','') for b in c if isinstance(b,dict) and b.get('type')=='text')
    return None
SKIP=re.compile(r'^\s*(<task-notification>|<command-name>|<command-message>|<local-command|<system-reminder>|Caveat:|\[SYSTEM NOTIFICATION|This session is being continued)',re.S)
out=[]; episodes=collections.Counter(); asst_msgs=collections.Counter()
STOP=os.environ.get('STOP','2026-11-10T20:50')  # exclude the turn that launched this analysis
for sid in SESS:
    last_model=None; last_text=''; in_episode=False; ep_model=None
    with open(P+sid+'.jsonl') as fh:
        for line in fh:
            try: d=json.loads(line)
            except: continue
            if d.get('isSidechain'): continue
            ts=d.get('timestamp','')
            if ts>=STOP: break
            if d.get('type')=='assistant':
                m=d['message'].get('model')
                if m=='<synthetic>': continue
                asst_msgs[m]+=1; last_model=m
                t=text_of(d['message'].get('content'))
                if t and t.strip(): last_text=t
                if not in_episode: episodes[m]+=1; in_episode=True
            elif d.get('type')=='user' and not d.get('isMeta'):
                t=text_of(d['message'].get('content'))
                if t is None or not t.strip() or SKIP.match(t): continue
                interrupted=t.startswith('[Request interrupted')
                if last_model is None: continue
                out.append(dict(sid=sid[:8],ts=ts,model=last_model,user=t,prev=last_text,interrupt=interrupted,uuid=d.get('uuid')))
                in_episode=False
seen=set(); ded=[]
for o in out:
    if o['uuid'] in seen: continue
    seen.add(o['uuid']); ded.append(o)
print('deduplicated by uuid: removed',len(out)-len(ded))
out=ded
json.dump(out,open(os.path.join(S,'turns.json'),'w'))
c=collections.Counter(o['model'] for o in out); ci=collections.Counter(o['model'] for o in out if o['interrupt'])
print('human turns by preceding model',dict(c)); print('interrupts',dict(ci)); print('assistant episodes',dict(episodes)); print('assistant messages',dict(asst_msgs))
mm=collections.defaultdict(collections.Counter)
for o in out: mm[o['model']][o['ts'][:10]]+=1
for k,v in mm.items(): print(k,sorted(v.items()))

import json,collections,os,sys
P=os.path.expanduser('~/.claude/projects/-home-awickert-Dropbox-NorthernWidget-github/')
for sid in ['30dafa30-bbc0-47e8-a62c-69dba3d468d7','cf0342fa-36e3-4818-be1e-2b4b31cc1756']:
    day=collections.defaultdict(collections.Counter)
    with open(P+sid+'.jsonl') as fh:
        for line in fh:
            try: d=json.loads(line)
            except: continue
            if d.get('type')=='assistant' and not d.get('isSidechain'):
                m=d['message'].get('model'); day[d['timestamp'][:10]][m]+=1
    print(sid)
    for k in sorted(day): print(' ',k,dict(day[k]))

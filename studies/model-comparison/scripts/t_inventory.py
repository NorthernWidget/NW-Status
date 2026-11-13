import json,sys,glob,collections,os
files=glob.glob(os.path.expanduser('~/.claude/projects/-home-awickert-Dropbox-NorthernWidget-github*/**/*.jsonl'),recursive=True)
for f in sorted(files):
    models=collections.Counter(); types=collections.Counter(); t0=t1=None
    with open(f) as fh:
        for line in fh:
            try: d=json.loads(line)
            except: continue
            types[d.get('type')]+=1
            ts=d.get('timestamp')
            if ts:
                t0=t0 or ts; t1=ts
            if d.get('type')=='assistant':
                models[d.get('message',{}).get('model')]+=1
    print(os.path.relpath(f,os.path.expanduser('~/.claude/projects')), os.path.getsize(f)//1000000,'MB', t0,t1, dict(models), dict(types))

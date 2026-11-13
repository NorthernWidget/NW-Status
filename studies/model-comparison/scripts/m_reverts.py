# Commits (any author) that revert or explicitly correct a specific earlier Claude commit: the message names the
# earlier commit by hash (7-40 hex, resolved in the same repository) and either is a git revert ("This reverts commit")
# or carries a correction word (fix|correct|revert|wrong|restore|undo|mistake|error|broke). Attributed to the earlier commit's model.
import sys,os,re,json,collections,glob,subprocess
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from common import *
rows=load_commits()
ai={(r['repo'],r['sha']):r['model'] for r in rows}
bysha=collections.defaultdict(dict)
for (repo,sha),m in ai.items(): bysha[repo][sha]=m
CW=re.compile(r'\b(fix\w*|correct\w*|revert\w*|wrong|restor\w*|undo\w*|mistake\w*|error\w*|broke\w*)\b',re.I)
repos=sorted(set(r['repo'] for r in rows))
hits=[]
for repo in repos:
    log=git(repo,'log','--all','--format=%x01%H%x02%aI%x02%B')
    for ch in log.split('\x01')[1:]:
        sha,date,body=ch.split('\x02',2)
        isrev='This reverts commit' in body
        if not (isrev or CW.search(body)): continue
        for tok in set(re.findall(r'\b[0-9a-f]{7,40}\b',body)):
            if tok==sha[:len(tok)]: continue
            full=[s for s in bysha[repo] if s.startswith(tok)]
            if len(full)!=1: continue
            mm=re.search(r'Co-Authored-By:\s*Claude\s+([A-Za-z]+)\s*([0-9.]*)',body,re.I)
            by=(mm.group(1).lower()+'-'+mm.group(2)) if mm else 'none'
            subj=body.splitlines()[0]
            hits.append(dict(repo=repo,sha=sha,date=date,by=by,target=full[0],target_model=bysha[repo][full[0]],revert=isrev,subject=subj[:110]))
json.dump(hits,open(os.path.join(S,'reverts.json'),'w'),indent=1)
n=collections.Counter(r['model'] for r in rows)
c=collections.Counter(h['target_model'] for h in hits); cr=collections.Counter(h['target_model'] for h in hits if h['revert'])
for m in sorted(n): print(m,'commits',n[m],'referenced-by-correction',c[m],'(%.2f per 100)'%(100*c[m]/n[m]),'git reverts',cr[m])
print(len(hits))
for h in hits: print(h['target_model'],'<-',h['by'],h['repo'],h['sha'][:8],h['subject'][:90])

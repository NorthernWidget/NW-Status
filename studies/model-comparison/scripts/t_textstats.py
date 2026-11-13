# Objective text measures on main-thread assistant replies (final text of each reply episode, i.e. the text Andy reads
# before his next turn) in the two NW sessions: em-dashes per 1k words; flattery/agreement openers
# (first 80 chars match good question|great question|you're right|you are right|exactly|great|excellent|good catch|good point);
# for replies >300 words, whether the last block is '---' + '**Summary.**' paragraph (the CLAUDE.md fixed form).
import json,os,re,collections
S=os.path.dirname(os.path.abspath(__file__))
T=json.load(open(os.path.join(S,'turns.json')))
OPEN=re.compile(r"^\W*(good question|great question|you'?re right|you are right|exactly|great|excellent|good catch|good point|that'?s right|perfect)\b",re.I)
def period(t):
    return t['model']
agg=collections.defaultdict(lambda: collections.Counter())
for t in T:
    p=t['prev']; m=t['model']; w=len(p.split())
    a=agg[(m,)]; a2=agg[(m,t['ts'][:7])]
    for x in (a,a2):
        x['replies']+=1; x['words']+=w; x['em']+=p.count('—'); x['flatter']+=bool(OPEN.match(p.strip()))
        if w>300:
            x['long']+=1
            x['summary']+=bool(re.search(r'\n---\s*\n+\*\*Summary\.\*\*[^\n]+\s*$',p.strip()+'\n') or re.search(r'\n---\s*\n+\*\*Summary\.\*\*',p[-2500:]))
for k in sorted(agg):
    x=agg[k]
    print(k,'replies',x['replies'],'em/1k words %.2f'%(1000*x['em']/max(1,x['words'])),'flattery-opener %.1f%%'%(100*x['flatter']/x['replies']),'long',x['long'],'Summary-form %.1f%%'%(100*x['summary']/max(1,x['long'])))

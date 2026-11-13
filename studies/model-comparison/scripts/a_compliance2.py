# kind x month x model table for granularity and test-number measures; and the spelling split at the rule date 2026-10-27
import json,collections,statistics,os
S=os.path.dirname(os.path.abspath(__file__))
d=json.load(open(os.path.join(S,'compliance.json')))
g=collections.defaultdict(list)
for r in d: g[(r['kind'],r['date'][:7],r['model'])].append(r)
print('kind month model n files_median pct_files>5 pct_testnum')
for k in sorted(g):
    v=g[k]; n=len(v)
    print(*k,n,statistics.median(r['files'] for r in v),round(100*sum(r['files']>5 for r in v)/n,1),round(100*sum(r['testnum'] for r in v)/n,1))
print('\nspelling and em-dash per 10k clean words, split at 2026-10-27 (spelling_check.py created) ')
h=collections.defaultdict(list)
for r in d: h[(r['model'],'pre-10-27' if r['date'][:10]<'2026-10-27' else 'post-10-27')].append(r)
for k in sorted(h):
    v=h[k]; w=sum(r['prose_words']+r['msg_words']+r['code_words'] for r in v); pm=sum(r['prose_words']+r['msg_words'] for r in v)
    print(*k,'n',len(v),'words',w,'brit/10k',round(1e4*sum(r['prose_brit']+r['msg_brit']+r['code_brit'] for r in v)/max(1,w),2),'commits_with_brit',sum(1 for r in v if r['prose_brit']+r['msg_brit']+r['code_brit']),'em/10k prose+msg',round(1e4*sum(r['prose_em']+r['msg_em'] for r in v)/max(1,pm),2),'msg_em_commits',sum(1 for r in v if r['msg_em']))

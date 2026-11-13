import json,collections,statistics,os,sys
S=os.path.dirname(os.path.abspath(__file__))
d=json.load(open(os.path.join(S,'compliance.json')))
def agg(rows):
    n=len(rows)
    if not n: return None
    files=[r['files'] for r in rows]
    pw=sum(r['prose_words'] for r in rows); mw=sum(r['msg_words'] for r in rows); cw=sum(r['code_words'] for r in rows)
    return dict(n=n,files_med=statistics.median(files),files_gt5=round(100*sum(f>5 for f in files)/n,1),
      session=round(100*sum(r['session'] for r in rows)/n,1),testnum=round(100*sum(r['testnum'] for r in rows)/n,1),
      brit_per10k=round(1e4*sum(r['msg_brit']+r['prose_brit']+r['code_brit'] for r in rows)/max(1,pw+mw+cw),2),
      em_per10k_prose_msg=round(1e4*sum(r['msg_em']+r['prose_em'] for r in rows)/max(1,pw+mw),2),
      em_per10k_code=round(1e4*sum(r['code_em'] for r in rows)/max(1,cw),2),
      words=pw+mw+cw)
def period(r):
    m=r['model']; d=r['date'][:10]
    return m+' '+r['date'][:7]
def show(title,key):
    print('##',title)
    g=collections.defaultdict(list)
    for r in d: g[key(r)].append(r)
    for k in sorted(g): print(k, agg(g[k]))
show('model',lambda r:r['model'])
show('model x month',lambda r:(r['model'],r['date'][:7]))
show('model x kind',lambda r:(r['kind'],r['model']))
show('overlap days 09-24,10-20,11-04,11-06',lambda r:(r['date'][:10],r['model']) if r['date'][:10] in('2026-09-24','2026-10-20','2026-11-04','2026-11-06') else ('zz',))

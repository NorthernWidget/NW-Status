# Rework measures for a stratified sample of Fable 5.1 and Opus (5, 5.5) commits.
# (1) survival of added lines to HEAD and at a fixed 3-day horizon (git blame, .git-blame-ignore-revs honored);
# (2) later commits within 7 days on HEAD's history that delete or modify lines the sampled commit added
#     (blame of the later commit's parent over its removed ranges), with their subjects for classification.
import sys,random,json,datetime,collections,re,os
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from common import *
random.seed(20261110)
CAP=int(sys.argv[1]) if len(sys.argv)>1 else 60
heads={}
def head(repo):
    if repo not in heads: heads[repo]=git(repo,'rev-parse','HEAD').strip()
    return heads[repo]
def files_of(repo,sha):
    out=git(repo,'show','--numstat','--format=','--no-renames',sha)
    res=[]
    for l in out.splitlines():
        p=l.split('\t')
        if len(p)==3 and p[0].isdigit(): res.append((p[2],int(p[0]),int(p[1])))
    return res
bcache={}
def blame_counts(repo,rev,path):
    k=(repo,rev,path)
    if k in bcache: return bcache[k]
    args=['blame','--porcelain']
    ign=os.path.join(repo_path(repo),'.git-blame-ignore-revs')
    if os.path.exists(ign): args+=['--ignore-revs-file',ign]
    out=git(repo,*args,rev,'--',path)
    c=collections.Counter()
    for l in out.splitlines():
        m=re.match(r'^([0-9a-f]{40}) \d+ \d+',l)
        if m: c[m.group(1)]+=1
    bcache[k]=c; return c
def rev_before(repo,when):
    return git(repo,'rev-list','-1','--before='+when.isoformat(),'HEAD').strip()
FIXRE=re.compile(r'\b(fix|fixes|fixed|correct|corrects|corrected|correction|revert|reverts|wrong|restore|restores|restored)\b',re.I)
def touches(repo,sha,date,paths):
    end=date+datetime.timedelta(days=7)
    out=git(repo,'rev-list','--no-merges','--since='+date.isoformat(),'--until='+end.isoformat(),'HEAD','--',*paths)
    res=[]
    for L in out.split():
        if L==sha: continue
        if subprocess.run(['git','-C',repo_path(repo),'merge-base','--is-ancestor',sha,L]).returncode!=0: continue
        diff=git(repo,'diff','-U0','--no-renames',L+'^',L,'--',*paths)
        ranges=collections.defaultdict(list); cur=None
        for l in diff.splitlines():
            if l.startswith('--- '): cur=l[6:] if l.startswith('--- a/') else None
            m=re.match(r'^@@ -(\d+)(?:,(\d+))? ',l)
            if m and cur:
                s=int(m.group(1)); n=int(m.group(2)) if m.group(2) is not None else 1
                if n>0: ranges[cur].append((s,s+n-1))
        hit=0
        for p,rs in ranges.items():
            args=['blame','--porcelain']
            for a,b in rs: args+=['-L',f'{a},{b}']
            o=git(repo,*args,L+'^','--',p)
            hit+=sum(1 for l in o.splitlines() if l.startswith(sha+' '))
        if hit:
            subj=git(repo,'log','-1','--format=%s',L).strip()
            body=git(repo,'log','-1','--format=%B',L)
            mm=re.search(r'Co-Authored-By:\s*Claude\s+([A-Za-z]+)\s*([0-9.]*)',body,re.I)
            res.append({'sha':L,'lines':hit,'subject':subj,'fixword':bool(FIXRE.search(subj)),'by':(mm.group(1).lower()+'-'+mm.group(2)) if mm else 'human/none'})
    return res
def analyze(r):
    repo,sha=r['repo'],r['sha']
    date=datetime.datetime.fromisoformat(r['date'])
    fl=files_of(repo,sha)
    paths=[f for f,a,d in fl if a>0]
    added=sum(a for f,a,d in fl)
    if not paths: return None
    hd=head(repo)
    surv_head=sum(min(a,blame_counts(repo,hd,f)[sha]) for f,a,d in fl if a>0)
    h3=rev_before(repo,date+datetime.timedelta(days=3))
    surv3=sum(min(a,blame_counts(repo,h3,f)[sha]) for f,a,d in fl if a>0) if h3 else None
    t=touches(repo,sha,date,paths)
    return dict(repo=repo,sha=sha,date=r['date'],model=r['model'],kind=r['kind'],files=len(fl),added=added,
                surv_head=surv_head,surv3=surv3,age_days=(datetime.datetime.now(datetime.timezone.utc)-date).days,
                touches=t,subject=r['subject'])
def main():
    rows=load_commits()
    elig=[]
    for r in rows:
        if subprocess.run(['git','-C',repo_path(r['repo']),'merge-base','--is-ancestor',r['sha'],'HEAD']).returncode!=0: continue
        fl=files_of(r['repo'],r['sha'])
        r['kind']=kind(r['repo'],[f for f,a,d in fl]); elig.append(r)
    json.dump([{k:r[k] for k in('repo','sha','date','model','kind')} for r in elig],open(os.path.join(S,'eligible.json'),'w'))
    strata=collections.defaultdict(list)
    for r in elig: strata[(fam(r['model']),r['kind'])].append(r)
    sample=[]
    for k,v in sorted(strata.items()):
        # stratify inside each (model,kind) by month so every era is represented
        bym=collections.defaultdict(list)
        for r in v: bym[r['date'][:7]].append(r)
        per=max(1,CAP//len(bym)); pick=[]
        for m,lst in sorted(bym.items()): pick+=random.sample(lst,min(per,len(lst)))
        rest=[r for r in v if r not in pick]; random.shuffle(rest)
        pick+=rest[:max(0,CAP-len(pick))]
        sample+=pick
        print(k,'eligible',len(v),'sampled',len(pick),flush=True)
    with ThreadPoolExecutor(8) as ex:
        res=[x for x in ex.map(analyze,sample) if x]
    json.dump(res,open(os.path.join(S,'rework.json'),'w'),indent=1)
    print('done',len(res))
main()

# Process compliance from git, for every Fable 5.1 / Opus 5 / Opus 5.5 commit (deduplicated by sha, backups excluded).
# Per commit: files touched; added lines; Claude-Session trailer present; a test/check count in the message;
# British spellings (wickert-voice spelling_check.scan, hard hits only) and em-dashes (U+2014) in
# (a) the commit message minus trailers and (b) added lines of prose files (.md .txt .tex .rst .html .cff) and code comments are NOT separated (code files counted separately).
import sys,os,re,json,tempfile,collections,importlib.util
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from common import *
spec=importlib.util.spec_from_file_location('sc',os.path.expanduser('~/misc/wickert-voice/tools/spelling_check.py'))
sc=importlib.util.module_from_spec(spec); spec.loader.exec_module(sc)
PROSE=('.md','.txt','.tex','.rst','.html','.cff')
CODE=('.ino','.cpp','.h','.c','.py','.sh')
TESTRE=re.compile(r'\b\d+\s*(?:/\s*\d+\s*)?(?:tests?|checks?|passed|pass|passes|cases|assertions|ok|green|fail(?:ed|s|ures)?|transcripts?|scenarios?)\b|\b\d+\s*/\s*\d+\b',re.I)
def brit(text):
    with tempfile.NamedTemporaryFile('w',suffix='.md',delete=False) as f: f.write(text); p=f.name
    n=sum(1 for h in sc.scan(p) if not h[3]); os.unlink(p); return n
def words(t): return len(re.findall(r"[A-Za-z]{2,}",t))
rows=load_commits(); out=[]
for r in rows:
    repo,sha=r['repo'],r['sha']
    body=git(repo,'log','-1','--format=%B',sha)
    msg='\n'.join(l for l in body.splitlines() if not re.match(r'^(Co-Authored-By|Claude-Session|Signed-off-by):',l,re.I))
    diff=git(repo,'show','--format=','--no-renames','-U0',sha)
    cur=None; prose=[]; code=[]; perfile=collections.Counter()
    for l in diff.splitlines():
        if l.startswith('+++ '): cur=l[6:] if l.startswith('+++ b/') else None; continue
        if l.startswith('+') and cur: perfile[cur]+=1
    # 'clean' prose: written by the agent, not imported or generated. Excluded: paths under corpus/ or reports/
    # (Andy's own corpus, scan dumps), any file receiving >1500 added lines in the commit (generated or imported),
    # .html, and Markdown table rows (lines starting with '|': generated status tables use an em-dash for an empty cell).
    cur=None
    for l in diff.splitlines():
        if l.startswith('+++ '): cur=l[6:] if l.startswith('+++ b/') else None; continue
        if l.startswith('+') and cur and perfile[cur]<=1500 and not re.search(r'(^|/)(corpus|reports)/',cur):
            low=cur.lower()
            if low.endswith(PROSE) and not low.endswith('.html'):
                if not l[1:].lstrip().startswith('|') and len(l)<=600: prose.append(l[1:])  # lines >600 chars are embedded data
            elif low.endswith(CODE): code.append(l[1:])
    P='\n'.join(prose); C='\n'.join(code)
    fl=git(repo,'show','--numstat','--format=','--no-renames',sha).strip().splitlines()
    out.append(dict(repo=repo,sha=sha,date=r['date'],model=r['model'],files=len(fl),added=int(r['added']),
        session=int(r['session_trailer']),testnum=bool(TESTRE.search(msg)),
        msg_words=words(msg),msg_brit=brit(msg),msg_em=msg.count('—'),
        prose_words=words(P),prose_brit=brit(P) if P else 0,prose_em=P.count('—'),
        code_words=words(C),code_brit=brit(C) if C else 0,code_em=C.count('—'),
        kind=kind(repo,[x.split('\t')[-1] for x in fl])))
json.dump(out,open(os.path.join(S,'compliance.json'),'w'))
print(len(out))

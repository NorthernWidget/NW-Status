import csv,subprocess,os,re,collections
W='/home/awickert/Dropbox/NorthernWidget/github'
S=os.path.dirname(os.path.abspath(__file__))
def repo_path(repo):
    if repo in('claude-kicad-text','wickert-voice'): return os.path.expanduser('~/misc/'+repo)
    return os.path.join(W,repo)
def git(repo,*a,check=False):
    r=subprocess.run(['git','-C',repo_path(repo)]+list(a),capture_output=True,text=True,errors='replace')
    return r.stdout if (r.returncode==0 or not check) else None
def fam(m): return m.split('-')[0]
HW_EXT=('.kicad_sch','.kicad_pcb','.kicad_pro','.kicad_sym','.kicad_mod','.kicad_wks','.sch','.brd','.lbr','.kicad_prl','.kicad_dru')
FW_EXT=('.ino','.cpp','.h','.c','.hpp')
SIMTEST_REPOS={'NW-Sim','NW-Tests','NW-Provision','NW-Build','claude-kicad-text'}
DOC_REPOS={'NW-Status','NW-Device-Specification','NW-Registry','wickert-voice','Inclinometer-Selection','Deployments'}
def kind(repo,files):
    """Repository kind, decided per commit: repo name first for sim/tests and docs; otherwise by touched-file extensions."""
    if repo in SIMTEST_REPOS: return 'sim/tests'
    if repo in DOC_REPOS: return 'docs/status'
    if repo=='nw-cold-silicon': return 'hardware'
    hw=sum(1 for f in files if f.lower().endswith(HW_EXT))
    fw=sum(1 for f in files if f.lower().endswith(FW_EXT))
    if hw and hw>=fw: return 'hardware'
    if fw: return 'firmware'
    if repo.startswith('Project-'): return 'hardware'
    return 'firmware'  # library repos: README/metadata-only commits stay with their repo kind
EXCLUDE_REPO=re.compile(r'\.backup$|Archive')
def load_commits():
    rows=list(csv.DictReader(open(os.path.join(S,'commits.csv'))))
    seen=set(); out=[]
    for r in rows:
        if fam(r['model']) not in('fable','opus') or r['model']=='opus-4.8': continue
        if EXCLUDE_REPO.search(r['repo']): continue
        if r['sha'] in seen: continue
        seen.add(r['sha']); out.append(r)
    return out

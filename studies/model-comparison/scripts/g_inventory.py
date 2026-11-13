# Inventory: every commit in every git repo under the workspace (+ ~/misc tools) with a Claude co-author trailer.
import subprocess,os,re,csv,sys,glob
ROOTS=sorted(glob.glob('/home/awickert/Dropbox/NorthernWidget/github/*/.git'))+[os.path.expanduser('~/misc/claude-kicad-text/.git'),os.path.expanduser('~/misc/wickert-voice/.git')]
out=csv.writer(open(sys.argv[1],'w'))
out.writerow(['repo','sha','date','model','session_trailer','files','added','deleted','subject'])
seen=set()
for g in ROOTS:
    r=os.path.dirname(g)
    if not os.path.isdir(g): continue
    try:
        log=subprocess.run(['git','-C',r,'log','--all','--format=%x01%H%x02%aI%x02%B%x03','--numstat'],capture_output=True,text=True,errors='replace',timeout=300).stdout
    except Exception as e:
        print('ERR',r,e); continue
    for chunk in log.split('\x01')[1:]:
        head,_,stat=chunk.partition('\x03')
        sha,date,body=head.split('\x02',2)
        m=re.findall(r'Co-Authored-By:\s*Claude\s+([A-Za-z]+)\s*([0-9.]*)',body,re.I)
        if not m: continue
        fam=m[0][0].lower(); ver=m[0][1]
        model=fam+('-'+ver if ver else '')
        key=(os.path.basename(r),sha)
        if key in seen: continue
        seen.add(key)
        files=add=dele=0
        for l in stat.strip().splitlines():
            p=l.split('\t')
            if len(p)==3:
                files+=1
                if p[0].isdigit(): add+=int(p[0]); dele+=int(p[1])
        sess=1 if re.search(r'Claude-Session:',body) else 0
        out.writerow([os.path.basename(r),sha,date,model,sess,files,add,dele,body.splitlines()[0][:120]])

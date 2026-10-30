import json,re,collections
S='/tmp/claude-1000/-home-awickert-Dropbox-NorthernWidget-github/cf0342fa-36e3-4818-be1e-2b4b31cc1756/scratchpad/kicad/'
E=json.load(open(S+'eagle.json')); K=json.load(open(S+'knet.json'))
def norm_k(n):
    m=re.match(r'^/Okapi_(\d)/(.*)$',n)
    local=None
    if m: local=m.group(1); n=m.group(2)
    n=re.sub(r'~\{([^}]*)\}',r'!\1',n)
    return n,local
# Eagle pin sets by (ref,pad)
epins={}  # net -> set
for n,lst in E['nets'].items():
    s=set((p,pad) for p,g,pin,pad in lst if pad is not None)
    epins[n]=s
kpins={}; kmeta={}
for n,lst in K['nets'].items():
    nn,local=norm_k(n)
    kpins[n]=set((r,p) for r,p,f in lst); kmeta[n]=(nn,local)
# local-label fragments: same normalized name across different KiCad nets
byname=collections.defaultdict(list)
for n,(nn,local) in kmeta.items(): byname[nn].append(n)
print('== KiCad nets whose normalized name appears more than once (local-label splits):')
for nn,l in sorted(byname.items()):
    if len(l)>1: print('  ',nn,'->',l, [len(kpins[x]) for x in l])
# pin -> knet
k_of=collections.defaultdict(list)
for n,s in kpins.items():
    for pp in s: k_of[pp].append(n)
dup=[(pp,l) for pp,l in k_of.items() if len(l)>1]
print('KiCad pins in >1 net:',dup[:10])
e_of={}
for n,s in epins.items():
    for pp in s: e_of[pp]=n
# named net name diff
en_named={n for n in epins if not n.startswith('N$')}
kn_named={kmeta[n][0] for n in kpins if not (n.startswith('Net-(') or n.startswith('unconnected-('))}
print('\n== Named nets in Eagle not in KiCad (after normalization):',sorted(en_named-kn_named))
print('== Named nets in KiCad not in Eagle:',sorted(kn_named-en_named))
# connectivity: for each Eagle net, which KiCad nets cover its pins
diffs=[]
exact=0
for n,s in sorted(epins.items()):
    cover=collections.Counter(k_of[pp][0] if k_of[pp] else None for pp in s)
    knets=[k for k in cover if k]
    missing=[pp for pp in s if not k_of[pp]]
    extra=set()
    for k in knets: extra|= (kpins[k]-s)
    if len(knets)==1 and not missing and not extra:
        exact+=1; continue
    diffs.append((n,len(s),dict(cover),missing,sorted(extra)))
print('\n== Eagle nets:',len(epins),' exactly reproduced in one KiCad net:',exact,' with differences:',len(diffs))
for d in diffs:
    print('  EAGLE',d[0],'(%d pins)'%d[1],'-> KiCad cover',d[2],'| eagle pins missing from KiCad:',d[3],'| extra pins in those KiCad nets:',d[4])
# KiCad pins not in any Eagle net
allk=set(pp for s in kpins.values() for pp in s if not pp[0] in('H1','H2','H3','U$1','U$2'))
alle=set(e_of)
print('\nKiCad connected pins not in Eagle nets (excluding unconnected-*):')
kc=set(pp for n,s in kpins.items() if not n.startswith('unconnected-') for pp in s)
print(sorted(kc-alle))
print('Eagle-connected pins missing from KiCad entirely:',sorted(alle-allk))
# unconnected comparison
kunc=set(pp for n,s in kpins.items() if n.startswith('unconnected-') for pp in s)
eunc=set((p,pad) for p,pl in E['partpins'].items() for g,pn,pad,d in pl if pad and (p,pad) not in alle)
print('\nEagle unconnected pads:',len(eunc),' KiCad unconnected-* pins:',len(kunc))
print('KiCad unconnected but Eagle connected:',sorted(kunc&alle))
print('Eagle unconnected but KiCad connected:',sorted(eunc&kc))
print('Eagle unconnected, absent from KiCad netlist altogether:',sorted(eunc-kunc-kc))

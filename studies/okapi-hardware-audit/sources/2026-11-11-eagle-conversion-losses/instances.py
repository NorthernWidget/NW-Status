"""Each board instance's pads against its library footprint's: kind, number, size, drill, shape, roundrect ratio, layer set
(back side mirrored to front), local margins, zone connection. Prints differences and the footprint each instance names.
usage: python3 instances.py <inventory.json>"""
import json,sys,collections
r=json.load(open(sys.argv[1])); n=0; bad=0; names=collections.Counter()
def key(p): return (p['kind'],p['name'],round(p['sx'],4),round(p['sy'],4),round(p['drill'],4),p['shape'],round(p['rr'],3),tuple(p['layers']),p['mm'],p['pm'],p['zc'])
for k,v in r.items():
    lib=sorted(map(key,v['lib_pads'] or []))
    for ref,flip,il,ip in v['instances']:
        n+=1; got=sorted(map(key,ip))
        if got!=lib:
            bad+=1; print(k,ref,'back' if flip else 'front','differs from library',v['fp']); print('   only instance:',sorted(set(got)-set(lib))[:4]); print('   only library:',sorted(set(lib)-set(got))[:4])
print('instances',n,'differing',bad)

"""Print each package's items per layer: Eagle package, KiCad library footprint, and whether every board instance has the library's counts.
usage: python3 layers.py <inventory.json>"""
import json,sys,collections
r=json.load(open(sys.argv[1]))
for k,v in r.items():
    print('==',k,'refs',len(v['refs']),'fp',v['fp'],'brd line',v['line'])
    print('   eagle:',', '.join('%s:%d'%kv for kv in sorted(v['eagle_layers'].items(),key=lambda kv:int(kv[0].split()[0]))))
    print('   lib  :',', '.join('%s:%d'%kv for kv in sorted((v['lib_layers'] or {}).items())))
    for ref,flip,il,ip in v['instances']:
        if il!=v['lib_layers']:
            print('   inst %s%s differs:'%(ref,' (back)' if flip else ''),{x:(il.get(x,0),(v['lib_layers'] or {}).get(x,0)) for x in set(il)|set(v['lib_layers'] or {}) if il.get(x,0)!=(v['lib_layers'] or {}).get(x,0)})

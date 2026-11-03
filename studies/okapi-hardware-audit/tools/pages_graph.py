"""Build the net graph between regions from the KiCad XML netlist.

usage: pages_graph.py <okapi.xml> <regions.json> <out nets.json>

For every net: its (ref, pin) members and the set of regions they fall in
(regions.json from pages_regions.py). Prints the region-pair matrix of shared
nets, all nets and then signal nets only (RAILS excluded, listed below), and
for each region the nets that leave it. Power symbols (#GND, #P+) are not in
the netlist, so GND and the rails count only through real pins.
"""
import sys, json, collections
import xml.etree.ElementTree as ET

RAILS = {'GND', '3V3_AUX', '3V3_CORE', '3V3_CORE_ISO', '3V3_FEATHER', '5V_AUX',
         'V_PRIME', 'V_PRIME-', 'V_BETA', 'V_LI', 'V_HP', 'VBUS_PRIME', 'VBUS_SEC',
         'VUSB_POWER', 'V_SOLAR', 'V_SOLAR_IN', 'FEATHER_BAT', 'LI+', 'LI-'}

def main():
    r = ET.parse(sys.argv[1]).getroot()
    reg = json.load(open(sys.argv[2]))
    sym = reg['syms']
    nets = {}
    for n in r.find('nets').findall('net'):
        mem = sorted({(nd.get('ref'), nd.get('pin')) for nd in n.findall('node')})
        regs = sorted({sym[ref] for ref, _ in mem if ref in sym})
        missing = sorted({ref for ref, _ in mem if ref not in sym})
        if missing:
            print('WARNING ref not in any region:', missing)
        nets[n.get('name')] = dict(members=mem, regions=regs)
    json.dump(dict(nets=nets, rails=sorted(RAILS)), open(sys.argv[3], 'w'), indent=1)
    names = list(nets)
    print('nets', len(names), 'rails present', sorted(RAILS & set(names)), 'rails absent', sorted(RAILS - set(names)))
    print('global-label nets not classed as rails:', sorted(n for n in names if not n.startswith('/') and not n.startswith('Net-') and n not in RAILS))
    regions = list(reg['regions'])
    for title, keep in (('ALL NETS', lambda n: True), ('SIGNAL NETS (rails excluded)', lambda n: n not in RAILS)):
        pair = collections.Counter()
        for n, v in nets.items():
            if not keep(n):
                continue
            rs = v['regions']
            for i in range(len(rs)):
                for j in range(i + 1, len(rs)):
                    pair[(rs[i], rs[j])] += 1
        print('\n==', title, ': shared nets per region pair (ranked)')
        for (a, b), c in pair.most_common():
            print(f'  {c:3d}  {a} -- {b}')
        print('\n==', title, ': nets leaving each region')
        for R in regions:
            out = [n for n, v in nets.items() if keep(n) and R in v['regions'] and len(v['regions']) > 1]
            inside = [n for n, v in nets.items() if keep(n) and v['regions'] == [R]]
            print(f'  {R:7s} leaving {len(out):3d}  internal {len(inside):3d}')
    print('\n== signal nets by region set (which blocks each signal joins)')
    for n, v in sorted(nets.items(), key=lambda kv: (len(kv[1]['regions']), kv[0])):
        if n in RAILS or len(v['regions']) < 2:
            continue
        print(f'  {n:22s} {" ".join(v["regions"])}')

if __name__ == '__main__':
    main()

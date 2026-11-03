#!/usr/bin/env python3
"""A no-connect flag on every pin ERC reports open, from ERC's own report.

    erc_noconnects.py <erc.json> <project dir> [--labels NAME,NAME]

Each pin_not_connected item names its sheet and the pin's connection point; a
no_connect goes there. --labels names local labels that sit alone on a pin
(ERC's isolated_pin_label): each is deleted and a no_connect takes its place.
uuids are uuid5 of sheet and point, so a rerun writes the same file. Every
touched sheet is re-saved through kicad-cli; run the gate afterwards, and
rename_nets.py on the board for the pads whose net name changes.
"""
import json, os, re, subprocess, sys, uuid

def fmt(v):
    s = ('%.6f' % v).rstrip('0').rstrip('.')
    return '0' if s in ('-0', '') else s

def main():
    a = sys.argv[1:]
    labels = []
    if '--labels' in a:
        i = a.index('--labels'); labels = a[i + 1].split(','); del a[i:i + 2]
    ercf, proj = a
    erc = json.load(open(ercf))
    flags = {}   # sheet file -> [(x, y, why)]
    for s in erc['sheets']:
        name = s['path'].strip('/')
        if not name: continue   # the root carries no parts
        f = os.path.join(proj, name + '.kicad_sch')
        for v in s['violations']:
            if v['type'] == 'pin_not_connected':
                it = v['items'][0]
                flags.setdefault(f, []).append((it['pos']['x'], it['pos']['y'], it['description']))
    # labels alone on a pin: the label's position is the pin end
    for f in sorted(os.listdir(proj)):
        if not f.endswith('.kicad_sch'): continue
        path = os.path.join(proj, f); t = open(path).read(); n = 0
        for name in labels:
            m = re.search(r'\t\(label "%s"\n\t\t\(at ([-\d.]+) ([-\d.]+) \d+\)\n(?:.*\n)*?\t\)\n' % re.escape(name), t)
            if not m: continue
            flags.setdefault(path, []).append((float(m.group(1)), float(m.group(2)), 'label ' + name))
            t = t.replace(m.group(0), '', 1); n += 1
        if n: open(path, 'w').write(t); print('%s: %d labels deleted' % (f, n))
    for path, pts in sorted(flags.items()):
        t = open(path).read()
        items = ''
        for x, y, why in pts:
            if re.search(r'\(no_connect\n\t\t\(at %s %s\)' % (re.escape(fmt(x)), re.escape(fmt(y))), t): continue
            u = uuid.uuid5(uuid.NAMESPACE_URL, 'https://github.com/NorthernWidget/Project-Okapi/kicad/no_connect/%s/%s,%s' % (os.path.basename(path), fmt(x), fmt(y)))
            items += '\t(no_connect\n\t\t(at %s %s)\n\t\t(uuid "%s")\n\t)\n' % (fmt(x), fmt(y), u)
        t = t[:-2] + items + ')\n'
        open(path, 'w').write(t)
        subprocess.run(['kicad-cli', 'sch', 'upgrade', '--force', path], capture_output=True)
        print('%s: %d no-connects' % (os.path.basename(path), len(pts)))

if __name__ == '__main__':
    main()

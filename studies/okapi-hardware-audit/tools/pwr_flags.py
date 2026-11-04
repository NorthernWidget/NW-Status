#!/usr/bin/env python3
"""A PWR_FLAG on every power pin ERC reports undriven, from ERC's own report;
the project's name comes from its .kicad_pro.

    pwr_flags.py <erc.json> <project dir> <lib.kicad_sym> [--skip PIN,PIN]

Each power_pin_not_driven item names its sheet and the pin's connection point,
which is where a rail enters the schematic from a connector, a battery, a
passive part or a power symbol; a PWR_FLAG's pin lands on that point, which
joins the net with no new wire. One flag per net. --skip names pins to leave
alone (SW: a converter's switch node is not a rail). The library's PWR_FLAG
definition is copied into the sheet's lib_symbols when it is not there.
References are #FLG01 upward. uuids are uuid5 of sheet and point, so a rerun
writes the same file. Every touched sheet is re-saved through kicad-cli; run
the gate afterwards.
"""
import json, os, re, subprocess, sys, uuid

NICK = 'nw-cold-silicon'

def fmt(v):
    s = ('%.6f' % v).rstrip('0').rstrip('.')
    return '0' if s in ('-0', '') else s

def lib_block(lib):
    t = open(lib).read()
    i = t.index('\n\t(symbol "PWR_FLAG"'); j = t.index('\n\t(symbol "', i + 10)
    return t[i + 1:j + 1]

def prop(name, value, x, y, hide):
    return ('\t\t(property "%s" "%s"\n\t\t\t(at %s %s 0)\n%s\t\t\t(show_name no)\n\t\t\t(do_not_autoplace no)\n\t\t\t(effects\n\t\t\t\t(font\n\t\t\t\t\t(size 1.27 1.27)\n\t\t\t\t)\n\t\t\t)\n\t\t)\n'
            % (name, value, fmt(x), fmt(y), '\t\t\t(hide yes)\n' if hide else ''))

def instance(x, y, ref, u, sheet_path, project):
    return ('\t(symbol\n\t\t(lib_id "%s:PWR_FLAG")\n\t\t(at %s %s 0)\n\t\t(unit 1)\n\t\t(body_style 1)\n\t\t(exclude_from_sim no)\n\t\t(in_bom yes)\n\t\t(on_board yes)\n\t\t(in_pos_files yes)\n\t\t(dnp no)\n\t\t(uuid "%s")\n'
            % (NICK, fmt(x), fmt(y), u)
            + prop('Reference', ref, x, y - 1.905, True) + prop('Value', 'PWR_FLAG', x, y - 3.81, False)
            + prop('Footprint', '', x, y, True) + prop('Datasheet', '', x, y, True) + prop('Description', '', x, y, True)
            + '\t\t(pin "1"\n\t\t\t(uuid "%s")\n\t\t)\n' % uuid.uuid5(uuid.NAMESPACE_URL, u + '/pin1')
            + '\t\t(instances\n\t\t\t(project "%s"\n\t\t\t\t(path "%s"\n\t\t\t\t\t(reference "%s")\n\t\t\t\t\t(unit 1)\n\t\t\t\t)\n\t\t\t)\n\t\t)\n\t)\n' % (project, sheet_path, ref))

def main():
    a = sys.argv[1:]
    skip = set()
    if '--skip' in a:
        i = a.index('--skip'); skip = set(a[i + 1].split(',')); del a[i:i + 2]
    ercf, proj, lib = a
    project = [f[:-10] for f in os.listdir(proj) if f.endswith('.kicad_pro')][0]   # the project's name: the root sheet, the instances block, the uuid namespace
    root = open(os.path.join(proj, project + '.kicad_sch')).read()
    root_uuid = re.findall(r'\(uuid "([^"]*)"\)', root)[0]
    sheet_uuid = {re.findall(r'\(property "Sheetname" "([^"]*)"', b)[0]: re.findall(r'\(uuid "([^"]*)"\)', b)[0]
                  for b in re.findall(r'\t\(sheet\n(?:.*\n)*?\t\)\n', root)}
    files = [f for f in os.listdir(proj) if f.endswith('.kicad_sch')]
    nflag = sum(open(os.path.join(proj, f)).read().count('"#FLG') for f in files)
    block = lib_block(lib).replace('(symbol "PWR_FLAG"', '(symbol "%s:PWR_FLAG"' % NICK, 1)
    seen = set(); placed = {}
    for s in json.load(open(ercf))['sheets']:
        name = s['path'].strip('/')
        if not name: continue
        for v in s['violations']:
            if v['type'] != 'power_pin_not_driven': continue
            it = v['items'][0]
            m = re.match(r'Symbol (\S+) Pin (\S+) \[([^,]*),', it['description'])
            if not m: continue
            ref, pin, pname = m.groups()
            if pname in skip: print('%s: %s.%s (%s) skipped' % (name, ref, pin, pname)); continue
            x, y = it['pos']['x'], it['pos']['y']
            if (name, x, y) in seen: continue
            seen.add((name, x, y)); placed.setdefault(name, []).append((x, y, '%s.%s %s' % (ref, pin, pname)))
    for name, pts in sorted(placed.items()):
        path = os.path.join(proj, name + '.kicad_sch'); t = open(path).read()
        if '(symbol "%s:PWR_FLAG"' % NICK not in t:
            t = t.replace('\t(lib_symbols\n', '\t(lib_symbols\n' + block, 1)
        items = ''
        for x, y, why in pts:
            nflag += 1; ref = '#FLG%02d' % nflag
            u = str(uuid.uuid5(uuid.NAMESPACE_URL, 'https://github.com/NorthernWidget/Project-%s/kicad/pwr_flag/%s/%s,%s' % (project, name, fmt(x), fmt(y))))
            items += instance(x, y, ref, u, '/%s/%s' % (root_uuid, sheet_uuid[name]), project)
            print('%s: %s at (%s, %s) on %s' % (name, ref, fmt(x), fmt(y), why))
        t = t[:-2] + items + ')\n'
        open(path, 'w').write(t)
        subprocess.run(['kicad-cli', 'sch', 'upgrade', '--force', path], capture_output=True)

if __name__ == '__main__':
    main()

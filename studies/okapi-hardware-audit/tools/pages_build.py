#!/usr/bin/env python3
"""Build layout H (pages.md, 2026-11-03): Okapi's six imported sheets onto ten US Letter pages.

    pages_build.py <project dir> <NW-Tests/kicad dir> <ink_rewrap.json> [--only PAGE]

Runs, in order: the two note edits on Okapi_3, RST_TRIG to a global label, the
block lifts page by page (sheet_lift.py, translations rounded to 1.27 mm), the
renames of the three sheets that stay whole, the root's sheet list
(root_sheets.py), and kicad-cli's re-save of every sheet. Checks are run by
the caller. With --only PAGE it stops after that page's lifts (for a commit
per page); run again with the next page, the lifts already done are skipped
because their blocks are gone from the source sheets. --only prep does the
note edits and RST_TRIG alone; --only rename the three whole-sheet renames
and the root alone.
"""
import json, os, re, subprocess, sys, uuid

INF = 1e9
# the nineteen blocks of pages.md, rectangles in sheet mm (x0, x1, y0, y1)
BLOCKS = {
    'S1L_T': ('Okapi_1', [(-INF, 170, -INF, 95)]),
    'S1L_B': ('Okapi_1', [(-INF, 170, 95, INF)]),
    'S1M_T': ('Okapi_1', [(170, 295, -INF, 100)]),
    'S1M_B': ('Okapi_1', [(170, 295, 100, INF), (148, 170, 116, 128)]),
    'S1R_T': ('Okapi_1', [(295, INF, -INF, 135)]),
    'S1R_B': ('Okapi_1', [(295, INF, 135, INF)]),
    'S2L_T': ('Okapi_2', [(-INF, 190, -INF, 160)]),
    'S2L_B': ('Okapi_2', [(-INF, 172, 160, INF)]),
    'S2R_T': ('Okapi_2', [(190, INF, -INF, 150)]),
    'S2R_B': ('Okapi_2', [(172, INF, 150, INF)]),
    'S3UL':  ('Okapi_3', [(-INF, 222, -INF, 176)]),
    'S3LAD': ('Okapi_3', [(222, INF, -INF, 190), (204, 222, 138, 141)]),   # + the "Select address" note
    'S3SD':  ('Okapi_3', [(-INF, 105, 176, 240)]),
    'S3TERM': ('Okapi_3', [(-INF, 105, 240, INF)]),
    'S3MID': ('Okapi_3', [(105, 205, 176, INF)]),
    'S3LR_T': ('Okapi_3', [(205, 222, 176, 245), (222, INF, 190, 245)]),   # not the strip x>=222, y<190: R18's wire and ~{LED_EN} belong to the ladder
    'S3LR_B': ('Okapi_3', [(205, INF, 245, INF)]),
}
# layout H: page name, [(block, ink offset x, ink offset y)] from the packing in pages.md
PAGES = [
    ('Power_Input',     [('S1M_T', 0, 0), ('S3LR_T', 108, 0), ('S1M_B', 0, 70)]),
    ('Core_Supply',     [('S1L_T', 0, 0), ('S1R_T', 0, 78)]),
    ('Aux_Rails',       [('S2R_B', 0, 0), ('S2L_B', 122, 0), ('S1L_B', 0, 52)]),
    ('Microcontroller', 'Okapi_6'),
    ('Indicators',      [('S3LAD', 0, 0), ('S3LR_B', 140, 0)]),
    ('Cell_Module',     [('S3UL', 0, 0), ('S3SD', 207, 0)]),
    ('Level_Shifters',  'Okapi_4'),
    ('Sensors',         'Okapi_5'),
    ('Sensor_Ports',    [('S2L_T', 0, 0), ('S3TERM', 165, 0)]),
    ('USB_ISP_Feather', [('S2R_T', 0, 0), ('S3MID', 175, 0), ('S1R_B', 0, 104)]),
]
ORIGIN = (10.16, 10.16)        # where a page's ink begins; the sheet border is at 2.5 mm, the inner line at 4.5
ORIGIN_X = {'Cell_Module': 8.89}            # one tick left: its ink is 267.7 mm wide
SHIFT = {'Microcontroller': (-11.43, 0), 'Sensors': (-6.35, 0)}   # whole sheets moved onto the Letter page, in ticks of 1.27
TICK = 1.27
DATE, REV = '2024-11-02', '1.0'

def page_uuid(name):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, 'https://github.com/NorthernWidget/Project-Okapi/kicad/page/' + name))

def tick(v):
    return round(v / TICK) * TICK

def run(*cmd):
    print('$', ' '.join(cmd))
    r = subprocess.run(cmd, capture_output=True, text=True)
    sys.stdout.write(r.stdout)
    if r.returncode:
        sys.stdout.write(r.stderr)
        raise SystemExit(r.returncode)

def main():
    a = sys.argv[1:]
    only = None
    if '--only' in a:
        i = a.index('--only')
        only = a[i + 1]
        del a[i:i + 2]
    proj, tools, inkf = a
    ink = json.load(open(inkf))
    sh = lambda n: os.path.join(proj, n + '.kicad_sch')
    # 1. the notes and RST_TRIG on Okapi_3 (once; harmless if already done)
    p3 = sh('Okapi_3')
    if os.path.exists(p3):
        t = open(p3).read()
        t = t.replace('(text "Jump SDA channels together, prevents using occupied addresses on the external I2C port"',
                      '(text "Jump SDA channels together,\\nprevents using occupied addresses\\non the external I2C port"')
        def to_global(m):
            x, y, ang = m.group(1), m.group(2), m.group(3)
            return ('\t(global_label "RST_TRIG"\n\t\t(shape bidirectional)\n\t\t(at %s %s %s)\n\t\t(fields_autoplaced yes)\n'
                    '\t\t(effects\n\t\t\t(font\n\t\t\t\t(size 1.2446 1.2446)\n\t\t\t)\n\t\t\t(justify left)\n\t\t)\n'
                    '\t\t(uuid "%s")\n'
                    '\t\t(property "Intersheetrefs" "${INTERSHEET_REFS}"\n\t\t\t(at %s %s 0)\n\t\t\t(hide yes)\n\t\t\t(show_name no)\n\t\t\t(do_not_autoplace no)\n'
                    '\t\t\t(effects\n\t\t\t\t(font\n\t\t\t\t\t(size 1.27 1.27)\n\t\t\t\t)\n\t\t\t\t(justify left)\n\t\t\t)\n\t\t)\n\t)\n'
                    % (x, y, ang, m.group(4), '%g' % (float(x) + 12.608), y))
        t, n = re.subn(r'\t\(label "RST_TRIG"\n\t\t\(at (-?[\d.]+) (-?[\d.]+) (\d+)\)\n\t\t\(effects\n(?:.*\n)*?\t\t\)\n\t\t\(uuid "([^"]*)"\)\n\t\)\n', to_global, t)
        if n:
            print('RST_TRIG: %d local labels made global' % n)
        open(p3, 'w').write(t)
    if only == 'prep':
        return
    # 2. lifts, page by page
    for name, spec in PAGES:
        if isinstance(spec, str) or only == 'rename':
            continue
        dst = sh(name)
        for block, ox, oy in spec:
            src_name, rects = BLOCKS[block]
            src = sh(src_name)
            if not os.path.exists(src):
                continue      # its sheet is gone: already lifted
            b = ink[block]
            dx, dy = tick(ORIGIN_X.get(name, ORIGIN[0]) + ox - b['x0']), tick(ORIGIN[1] + oy - b['y0'])
            cmd = ['python3', os.path.join(tools, 'sheet_lift.py'), src, dst]
            for x0, x1, y0, y1 in rects:
                cmd += ['--rect', str(x0), str(x1), str(y0), str(y1)]
            cmd += ['--translate', '%g' % dx, '%g' % dy]
            if not os.path.exists(dst):
                cmd += ['--new', '--uuid', page_uuid(name), '--paper', 'USLetter', '--date', DATE, '--rev', REV]
            run(*cmd)
        if only == name:
            break
    # 3. empty source sheets go; the three whole sheets are renamed
    for old in ('Okapi_1', 'Okapi_2', 'Okapi_3'):
        p = sh(old)
        if os.path.exists(p):
            t = open(p).read()
            left = re.findall(r'^\t\((symbol|wire|label|global_label|junction|text|polyline|no_connect)\n', t, re.M)
            if not left:
                os.remove(p)
                print('%s: empty, removed' % old)
            else:
                print('%s: still holds %d items' % (old, len(left)))
    for name, spec in PAGES:
        if isinstance(spec, str) and os.path.exists(sh(spec)):
            os.rename(sh(spec), sh(name))
            print('%s -> %s' % (spec, name))
            if name in SHIFT:
                run('python3', os.path.join(tools, 'sheet_page.py'), sh(name), '--paper', 'USLetter', '--translate', '%g' % SHIFT[name][0], '%g' % SHIFT[name][1])
            else:
                run('python3', os.path.join(tools, 'sheet_page.py'), sh(name), '--paper', 'USLetter')
    # 4. the root
    root = sh('Okapi')
    rt = open(root).read()
    plan = []
    for name, spec in PAGES:
        f = name + '.kicad_sch'
        if not os.path.exists(sh(name)):
            continue
        if isinstance(spec, str):
            u = re.search(r'\(uuid "([^"]*)"\)', open(sh(name)).read()).group(1)
        else:
            u = page_uuid(name)
        plan.append({'name': name, 'file': f, 'uuid': u})
    # sheets not yet split keep their symbols
    for old in ('Okapi_1', 'Okapi_2', 'Okapi_3'):
        if os.path.exists(sh(old)):
            u = re.search(r'\(uuid "([^"]*)"\)', open(sh(old)).read()).group(1)
            plan.append({'name': old, 'file': old + '.kicad_sch', 'uuid': u})
    json.dump(plan, open(os.path.join(proj, 'sheets.json'), 'w'), indent=1)
    run('python3', os.path.join(tools, 'root_sheets.py'), root, os.path.join(proj, 'sheets.json'), '--paper', 'USLetter')
    os.remove(os.path.join(proj, 'sheets.json'))
    # 5. KiCad orders every file
    for f in sorted(os.listdir(proj)):
        if f.endswith('.kicad_sch'):
            run('kicad-cli', 'sch', 'upgrade', '--force', os.path.join(proj, f))

if __name__ == '__main__':
    main()

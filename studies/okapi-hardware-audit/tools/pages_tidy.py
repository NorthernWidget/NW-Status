#!/usr/bin/env python3
"""Organize Okapi's ten pages the way Bobby organized Margay's: a bold heading per
theme, a divider between themes, blocks spaced evenly, notes beside their parts.

    pages_tidy.py <project dir> <NW-Tests/kicad dir> [--only PAGE]

Everything moves by whole grid ticks (1.27 mm). Heading and divider forms are
Bobby's on Margay's Power_Sensors sheet (5.08 x 4.318 bold text, 0.1524 mm
line). Run kicad-cli sch upgrade on every touched sheet afterwards, then the
checks. uuids are uuid5 of the page and item, so a rerun reproduces the files.
"""
import os, re, subprocess, sys, uuid

T = 1.27
def tk(n): return n * T

# per page: shift of the whole sheet (ticks), then block moves (rect in current mm, ticks),
# headings (text, x, y), dividers ((x1,y1),(x2,y2)), notes to move in (text, from page, x, y, angle),
# notes to move within (text, x, y, angle), symbols to move (ref, ticks dx, ticks dy)
PLAN = {
 'Power_Input': dict(shift=(0, 10),
    blocks=[((116, 195, 5, 79), (56, 0))],                        # the terminals to the right column (the charger starts at y 80)
    headings=[('Battery Protection & Solar Charger', 12.7, 15.24), ('Terminals', 190.5, 15.24)],
    dividers=[((177.8, 5.08), (177.8, 175.26))],          # dividers right of x 175.3 stop above the title block
    notes_in=[('To Battery Connectors', 'Core_Supply', 190.5, 110.49, 0)]),
 'Core_Supply': dict(shift=(0, 8),
    headings=[('Core Supply', 12.7, 15.24)],
    notes_out=['Remove PG pullup?', 'To Battery Connectors']),
 'Aux_Rails': dict(shift=(0, 8),
    blocks=[((5, 200, 60, 175), (0, 8))],                         # the rails block down another eight ticks, under its heading
    headings=[('V_HP Source Select', 12.7, 15.24), ('3V3_AUX & 5V_AUX Rails', 12.7, 78.74)],
    dividers=[((5.08, 72.39), (275.59, 72.39))],
    notes_in=[('Remove PG pullup?', 'Core_Supply', 160.02, 90.17, 0)]),
 'Microcontroller': dict(shift=(0, 0), headings=[('Microcontroller & GPIO Expander', 12.7, 15.24)]),
 'Indicators': dict(shift=(0, 8),
    headings=[('Indicator LEDs', 12.7, 15.24), ('Status LED & Log Button', 152.4, 15.24)],
    dividers=[((149.86, 5.08), (149.86, 110.49))]),
 'Cell_Module': dict(shift=(0, 6),
    headings=[('Cellular Module', 12.7, 15.24), ('SD Card', 217.17, 15.24)]),
 'Level_Shifters': dict(shift=(0, 0), headings=[('Level Shifters', 12.7, 15.24)]),
 'Sensors': dict(shift=(0, 0), headings=[('On-Board Sensors', 12.7, 15.24)]),
 'Sensor_Ports': dict(shift=(0, 8),
    blocks=[((173, 245, 5, 100), (10, 0))],                       # the terminals ten ticks right
    headings=[('Switched Port Power', 12.7, 15.24), ('Sensor Terminals', 189.23, 15.24)],
    dividers=[((181.61, 5.08), (181.61, 175.26))]),
 'USB_ISP_Feather': dict(shift=(0, 6),
    blocks=[((183, 270, 5, 170), (4, 0)), ((5, 120, 112, 195), (0, 6))],   # ISP/Feather right; the timer down
    headings=[('USB', 12.7, 15.24), ('ISP & Feather', 193.04, 15.24), ('Feather Power Timer', 12.7, 128.27)],
    dividers=[((187.96, 5.08), (187.96, 175.26)), ((5.08, 121.92), (187.96, 121.92))],
    symbols=[('H1', -68, 44), ('H2', -68, 44), ('H3', -68, 44)]),
}
# stage 2 (2026-11-04), after pages_headings_check.py measured every heading's ink: two headings
# touched their dividers, two sat far above the ink they label
STAGE2 = {
 'Aux_Rails': dict(blocks=[((5, 200, 80, 195), (0, 2))], move_texts=[('3V3_AUX & 5V_AUX Rails', 12.7, 81.28)]),
 'USB_ISP_Feather': dict(blocks=[((5, 120, 125, 210), (0, 2))], move_texts=[('Feather Power Timer', 12.7, 130.81)]),
 'Microcontroller': dict(shift=(0, -20), move_texts=[('Microcontroller & GPIO Expander', 12.7, 15.24)]),   # the shift carries the heading too
 'Cell_Module': dict(move_texts=[('Cellular Module', 101.6, 15.24)]),
}
ORDER = ['Core_Supply', 'Power_Input', 'Aux_Rails', 'Microcontroller', 'Indicators', 'Cell_Module',
         'Level_Shifters', 'Sensors', 'Sensor_Ports', 'USB_ISP_Feather']   # Core_Supply first: it gives notes away

HEADING = '\t(text "{text}"\n\t\t(exclude_from_sim no)\n\t\t(at {x} {y} 0)\n\t\t(effects\n\t\t\t(font\n\t\t\t\t(size 5.08 4.318)\n\t\t\t\t(thickness 0.8636)\n\t\t\t\t(bold yes)\n\t\t\t)\n\t\t\t(justify left bottom)\n\t\t)\n\t\t(uuid "{u}")\n\t)\n'
DIVIDER = '\t(polyline\n\t\t(pts\n\t\t\t(xy {x1} {y1}) (xy {x2} {y2})\n\t\t)\n\t\t(stroke\n\t\t\t(width 0.1524)\n\t\t\t(type solid)\n\t\t)\n\t\t(uuid "{u}")\n\t)\n'

def fmt(v):
    s = ('%.6f' % v).rstrip('0').rstrip('.')
    return '0' if s in ('-0', '') else s

def u5(*parts):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, 'https://github.com/NorthernWidget/Project-Okapi/kicad/tidy/' + '/'.join(map(str, parts))))

def run(*cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    sys.stdout.write(r.stdout)
    if r.returncode:
        sys.stdout.write(r.stderr)
        raise SystemExit(r.returncode)

def text_block(t, text):
    m = re.search(r'^\t\(text "' + re.escape(text) + r'"\n(?:.*\n)*?\t\)\n', t, re.M)
    assert m, 'no text %r' % text
    return m

def append_items(path, items):
    t = open(path).read()
    i = t.rstrip().rfind('\n)')      # before the file's closing paren
    t = t[:i + 1] + ''.join(items) + t[i + 1:]
    open(path, 'w').write(t)

def main():
    a = sys.argv[1:]
    only = None
    if '--only' in a:
        i = a.index('--only'); only = a[i + 1]; del a[i:i + 2]
    stage = 1
    if '--stage' in a:
        i = a.index('--stage'); stage = int(a[i + 1]); del a[i:i + 2]
    proj, tools = a
    sh = lambda n: os.path.join(proj, n + '.kicad_sch')
    if stage == 2:
        for name, p in STAGE2.items():
            path = sh(name)
            sx, sy = p.get('shift', (0, 0))
            if sx or sy:
                run('python3', os.path.join(tools, 'sheet_page.py'), path, '--translate', fmt(tk(sx)), fmt(tk(sy)))
            for (x0, x1, y0, y1), (bx, by) in p.get('blocks', []):
                run('python3', os.path.join(tools, 'sheet_lift.py'), path, path, '--rect', str(x0), str(x1), str(y0), str(y1), '--translate', fmt(tk(bx)), fmt(tk(by)))
            t = open(path).read()
            for text, x, y in p.get('move_texts', []):
                m = text_block(t, text); blk = m.group(0)
                blk = re.sub(r'\(at -?[\d.]+ -?[\d.]+ (\d+)\)', lambda q: '(at %s %s %s)' % (fmt(x), fmt(y), q.group(1)), blk, count=1)
                t = t[:m.start()] + blk + t[m.end():]
            open(path, 'w').write(t)
            run('kicad-cli', 'sch', 'upgrade', '--force', path)
            print('%s: stage 2, shift %s, %d block moves, %d texts moved' % (name, p.get('shift', (0, 0)), len(p.get('blocks', [])), len(p.get('move_texts', []))))
        return
    held = {}   # notes lifted out of a page, by text
    for name in ORDER:
        p = PLAN[name]
        if only and name != only and name != 'Core_Supply':
            continue
        path = sh(name)
        # notes leaving this page are cut first (kept in memory with their text block)
        for text in p.get('notes_out', []):
            t = open(path).read(); m = text_block(t, text)
            held[text] = m.group(0); open(path, 'w').write(t[:m.start()] + t[m.end():])
        if only and name != only:
            continue
        sx, sy = p['shift']
        if sx or sy:
            run('python3', os.path.join(tools, 'sheet_page.py'), path, '--translate', fmt(tk(sx)), fmt(tk(sy)))
        for (x0, x1, y0, y1), (bx, by) in p.get('blocks', []):
            run('python3', os.path.join(tools, 'sheet_lift.py'), path, path, '--rect', str(x0), str(x1), str(y0 + tk(sy)), str(y1 + tk(sy)), '--translate', fmt(tk(bx)), fmt(tk(by)))
        items = []
        for i, (text, x, y) in enumerate(p.get('headings', [])):
            items.append(HEADING.format(text=text, x=fmt(x), y=fmt(y), u=u5(name, 'heading', i)))
        for i, ((x1, y1), (x2, y2)) in enumerate(p.get('dividers', [])):
            items.append(DIVIDER.format(x1=fmt(x1), y1=fmt(y1), x2=fmt(x2), y2=fmt(y2), u=u5(name, 'divider', i)))
        for text, src, x, y, ang in p.get('notes_in', []):
            blk = held.pop(text)
            blk = re.sub(r'\(at -?[\d.]+ -?[\d.]+ \d+\)', '(at %s %s %s)' % (fmt(x), fmt(y), ang), blk, count=1)
            items.append(blk)
        if items:
            append_items(path, items)
        if p.get('symbols'):
            sys.path.insert(0, tools)
            from sch_edit import Editor
            e = Editor(path)
            for ref, dx, dy in p['symbols']:
                e.move_symbol(ref, tk(dx), tk(dy))
            e.save()
        run('kicad-cli', 'sch', 'upgrade', '--force', path)
        print('%s: shift %s ticks, %d block moves, %d headings, %d dividers, %d notes in, %d symbols moved' % (
            name, p['shift'], len(p.get('blocks', [])), len(p.get('headings', [])), len(p.get('dividers', [])), len(p.get('notes_in', [])), len(p.get('symbols', []))))
    assert not held, 'notes left over: %s' % list(held)
    run('kicad-cli', 'sch', 'upgrade', '--force', sh('Core_Supply'))

if __name__ == '__main__':
    main()

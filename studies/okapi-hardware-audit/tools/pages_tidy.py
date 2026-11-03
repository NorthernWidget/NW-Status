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
# stage 3 (2026-11-04): Andy's page notes (NW-Status/MORNING-2026-11-04.md item 3c), page by page.
# ops: props (ref, field, x, y): a Reference/Value text anchor; labels (kind, name, (x, y), new x, y, angle):
# a label moved and turned (0 and 90 take justify left, 180 and 270 right); texts (text, x, y);
# blocks and symbols as in the stages above; wires [(a, b, old end, new end)]
STAGE3 = {
 'Power_Input': dict(
    labels=[('global_label', 'V_LI_SENSE', (92.71, 43.18), 92.71, 43.18, 90),        # the flag lay over R72
            ('global_label', 'V_SOLAR_SENSE', (25.4, 105.41), 25.4, 105.41, 90),     # over R74
            ('global_label', 'V_PRIME_SENSE', (220.98, 58.42), 223.52, 58.42, 90)],  # over J5
    props=[('D1', 'Reference', 12.7, 102.87), ('D1', 'Value', 12.7, 109.22),
           ('R74', 'Reference', 33.02, 102.87), ('R74', 'Value', 33.02, 109.22),
           ('R73', 'Reference', 228.6, 55.372), ('R73', 'Value', 228.6, 61.722),
           ('D2', 'Reference', 100.33, 113.03), ('D2', 'Value', 100.33, 115.57)],
    texts=[('Reverse Polarity Protection', 10.16, 96.52)]),
 'Core_Supply': dict(
    labels=[('global_label', 'V_PRIME', (31.75, 114.3), 31.75, 114.3, 180)]),           # pointed into U37's IN-
 'Aux_Rails': dict(
    labels=[('global_label', 'POWER_EN', (58.42, 147.32), 58.42, 147.32, 90)],         # lay over L2 and R2
    blocks=[((84, 152, 166, 195), (64, -20))]),
 'Microcontroller': dict(
    blocks=[((41, 135, 18, 140), (6, 0), 'stretch'),    # IC1 with its pin notes (anchored at x 120.65) right; the leads from the left cluster stretch
            ((136, 275, 18, 130), (-10, 34))],           # then U41 with its left-side labels at x 139.7, R68, the "ADD:" notes and the pull-up ladder it is wired to: down and a little left
    labels=[('global_label', 'DTR', (11.43, 43.18), 11.43, 43.18, 90),          # lay over C39
            ('global_label', '3V3_CORE', (34.29, 40.64), 34.29, 40.64, 90),     # pointed into VCC
            ('global_label', 'RST', (39.37, 53.34), 39.37, 53.34, 90),          # lay over R52
            ('global_label', '3V3_CORE', (34.29, 68.58), 34.29, 68.58, 180)],   # pointed into AVCC
    props=[('R52', 'Value', 32.0, 52.07)]),
 'Indicators': dict(
    blocks=[((69, 150, 18, 80), (6, 0), 'stretch'),      # the resistor and LED row with its bus wires right; the leads from U45's pin ends at x 68.58 stretch
            ((55, 75, 85, 110), (0, 8)),                 # R18 down
            ((148, 152, 0, 115), (8, 0)),                # the divider, since the row now reaches x 152
            ((156, 245, 18, 80), (8, 0))]),              # the status LED and log button right of it
 'Level_Shifters': dict(                                 # the columns share a label column at x 106.68 (a chip's right-hand labels and its
    # neighbor's left-hand labels on the same points), so a chip cannot leave its row without rewiring; what can move safely:
    blocks=[((185, 260, 75, 112), (0, -30)),             # U29, alone on the right, up to row 1 beside U28
            ((106, 185, 163, 190), (54, -64))]),         # U36 from the foot of column 2 to column 3, row 2 (U26's lowest label row, 162.56, stays)
 'Sensors': dict(                                        # grouped: column 1 the environment and motion sensors, column 2 reference, DAC and clock, column 3 power monitor and ADC
    blocks=[((115, 170, 95, 125), (-76, -40)),           # BME280 (its right lead reaches x 166.37) to the top of column 1
            ((115, 185, 125, 162), (-10, 0)),            # RTC1, BT1 and C32 (its lead starts at x 118.11) under the DAC
            ((10, 105, 150, 185), (-2, 0)),              # MLX90393 onto the column's x
            ],
    labels=[('global_label', '3V3_AUX', (113.03, 137.16), 113.03, 137.16, 180),   # pointed into RTC1
            ('global_label', 'RTC_INT', (113.03, 139.7), 113.03, 139.7, 180)],
    props=[('R51', 'Reference', 210.82, 48.26), ('R51', 'Value', 210.82, 53.34),
           ('R50', 'Reference', 262.89, 113.03), ('R50', 'Value', 262.89, 120.65)]),   # R50's texts off the page edge; the part stays
 'Sensor_Ports': dict(
    blocks=[((5, 170, 85, 160), (0, 34)),                # the primary channel with R25's 3V3_AUX supply at y 86.36, down
            ((5, 170, 18, 85), (0, 10)),                 # the secondary channel under its title
            ((195, 236, 49, 100), (0, 16)),              # J2 with its label bundle (diagonal leads up to y 50.8) down
            ((236, 276, 45, 85), (0, 10))],              # J4 down
    subheads=[('Secondary port', 12.7, 29.21), ('Primary port', 12.7, 128.27)]),
 'USB_ISP_Feather': dict(
    pre_delete_wires=[((72.39, 186.69), (77.47, 186.69))],   # V_LI's lead into VIN: the label moves onto the pin end (its old place lands on U8's wire)
    blocks=[((74, 120, 178, 210), (0, -26), 'stretch'),  # U10 up, so ON meets DRVN
            ((190, 276, 25, 50), (0, -8)),               # JP5 and its note up
            ((190, 276, 60, 85), (0, -10))],             # the ICSP header up (Q4 and R54 stay: no clear spot in the column without overlapping the socket's labels; Andy to say where)
    delete_wires=[((74.93, 166.37), (74.93, 166.37))],   # the lead between DRVN and ON, now of zero length
    labels=[('global_label', 'V_LI', (72.39, 186.69), 77.47, 153.67, 90)]),
 'Cell_Module': dict(
    blocks=[((95, 150, 18, 65), (90, 84)),               # the mode and reset buttons to the right column, under the SD card
            ((55, 100, 70, 100), (-26, -24))]),          # the micro-USB to the top of the left column
}
# values that are Eagle package names, never set by Bobby: they print nothing a reader needs and sat on
# the labels he circled; hidden on every page (the Footprint field carries the package)
HIDE_VALUES = ('R-EU_R0402', 'R-EU_R0805', 'DIODEDO-214AC', 'DIODESOD-323', 'JUMPER-SMT_2_NO_SILK')
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
    if stage == 3:
        sys.path.insert(0, tools)
        from sch_edit import Editor, fmt as efmt
        if only in (None, 'hide_values'):
            for f in sorted(os.listdir(proj)):
                if not f.endswith('.kicad_sch'): continue
                path = os.path.join(proj, f); t = open(path).read(); n = 0
                for v in HIDE_VALUES:
                    t, k = re.subn(r'(\t\t\(property "Value" "%s"\n\t\t\t\(at [^)]*\)\n)(?!\t\t\t\(hide yes\))' % re.escape(v), r'\1\t\t\t(hide yes)\n', t); n += k
                if n:
                    open(path, 'w').write(t); run('kicad-cli', 'sch', 'upgrade', '--force', path); print('%s: %d package-name values hidden' % (f, n))
            if only == 'hide_values':
                return
        for name, p in STAGE3.items():
            if only and name != only:
                continue
            path = sh(name)
            sx, sy = p.get('shift', (0, 0))
            if sx or sy:
                run('python3', os.path.join(tools, 'sheet_page.py'), path, '--translate', fmt(tk(sx)), fmt(tk(sy)))
            if p.get('pre_delete_wires'):
                e0 = Editor(path)
                for a_, b_ in p['pre_delete_wires']:
                    e0.delete_wire(a_, b_)
                e0.save()
            for blk in p.get('blocks', []):
                (x0, x1, y0, y1), (bx, by) = blk[0], blk[1]
                extra = ['--stretch'] if len(blk) > 2 and blk[2] == 'stretch' else []
                run('python3', os.path.join(tools, 'sheet_lift.py'), path, path, '--rect', str(x0), str(x1), str(y0), str(y1), '--translate', fmt(tk(bx)), fmt(tk(by)), *extra)
            e = Editor(path)
            for ref, dx, dy in p.get('symbols', []):
                e.move_symbol(ref, tk(dx), tk(dy))
            for ref, field, x, y in p.get('props', []):
                # the field's anchor inside this symbol's block (sch_edit.set_property keys on the Reference text only)
                m = [m for m in re.finditer(r'\t\(symbol\n(?:.*\n)*?\t\)\n', e.s) if '(property "Reference" "%s"' % ref in m.group(0)]
                assert len(m) == 1, (ref, len(m)); blk = m[0].group(0)
                blk2, n = re.subn(r'(\(property "%s" "[^"]*"\n\t\t\t\(at )-?[\d.]+ -?[\d.]+( -?[\d.]+\))' % field, lambda q: q.group(1) + efmt(x) + ' ' + efmt(y) + q.group(2), blk, count=1)
                assert n == 1, (ref, field); e.s = e.s[:m[0].start()] + blk2 + e.s[m[0].end():]
            for a_, b_, old, new in p.get('wires', []):
                e.move_wire_end(a_, b_, old, new)
            for a_, b_ in p.get('delete_wires', []):
                e.delete_wire(a_, b_)
            e.save()
            t = open(path).read()
            for kind, lname, (ox, oy), x, y, ang in p.get('labels', []):
                pat = r'(\t\(%s "%s"\n(?:\t\t\(shape \w+\)\n)?\t\t)\(at %s %s \d+\)\n((?:.*\n)*?\t\t\t\(justify )(left|right)' % (kind, re.escape(lname), re.escape(efmt(ox)), re.escape(efmt(oy)))
                t, n = re.subn(pat, lambda m: '%s(at %s %s %d)\n%s%s' % (m.group(1), fmt(x), fmt(y), ang, m.group(2), 'left' if ang in (0, 90) else 'right'), t, count=1)
                assert n == 1, 'label %s at (%s, %s) not found once' % (lname, ox, oy)
            for text, x, y in p.get('texts', []):
                m = text_block(t, text); blk = m.group(0)
                blk = re.sub(r'\(at -?[\d.]+ -?[\d.]+ (\d+)\)', lambda q: '(at %s %s %s)' % (fmt(x), fmt(y), q.group(1)), blk, count=1)
                t = t[:m.start()] + blk + t[m.end():]
            open(path, 'w').write(t)
            subs = [HEADING.replace('(size 5.08 4.318)', '(size 3.048 2.54)').replace('(thickness 0.8636)', '(thickness 0.508)').format(text=text, x=fmt(x), y=fmt(y), u=u5(name, 'subhead', i)) for i, (text, x, y) in enumerate(p.get('subheads', []))]
            if subs:
                append_items(path, subs)
            run('kicad-cli', 'sch', 'upgrade', '--force', path)
            print('%s: stage 3 applied' % name)
        return
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

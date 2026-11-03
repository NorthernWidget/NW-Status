#!/usr/bin/env python3
"""Organize Okapi's ten pages the way Bobby organized Margay's: a bold heading per
theme, a divider between themes, blocks spaced evenly, notes beside their parts.

    pages_tidy.py <project dir> <NW-Tests/kicad dir> [--only PAGE]

Everything moves by whole grid ticks (1.27 mm). Heading and divider forms are
Bobby's on Margay's Power_Sensors sheet (5.08 x 4.318 bold text, 0.1524 mm
line). Run kicad-cli sch upgrade on every touched sheet afterwards, then the
checks. uuids are uuid5 of the page and item, so a rerun reproduces the files.
"""
import json, os, re, subprocess, sys, uuid

T = 1.27
DATE, REV = '2024-11-02', '1.0'

def page_uuid(name):   # the same deterministic uuid as pages_build.py, so a page's uuid never depends on when it was made
    return str(uuid.uuid5(uuid.NAMESPACE_URL, 'https://github.com/NorthernWidget/Project-Okapi/kicad/page/' + name))
def tk(n): return n * T
ORDER_STAGE16 = ['Power_Input', 'Core_Supply', 'Core_Power_Path', 'Aux_Rails', 'Microcontroller', 'GPIO_Expander', 'Indicators',
                 'Cell_Module', 'Feather_ISP', 'Level_Shifters', 'Level_Shifters_Ports', 'Sensors', 'Analog_Clock_Power', 'Sensor_Ports',
                 'Sensor_Terminals', 'USB_ISP_Feather']   # stages 5 to 16: the order of the split, then Feather_ISP after Cell_Module
ORDER16 = ['Power_Input', 'Core_Power_Path', 'Core_Supply', 'Aux_Rails',                  # power: in, which source feeds the core, the core rails, the aux rails
           'Microcontroller', 'GPIO_Expander', 'USB_ISP_Feather',                         # the brain and its programming and serial port
           'Indicators', 'Analog_Clock_Power', 'Sensors',                                 # on-board peripherals
           'Cell_Module', 'Feather_ISP',                                                  # the two Particle hosts
           'Level_Shifters', 'Level_Shifters_Ports', 'Sensor_Ports', 'Sensor_Terminals']  # out to the sensor ports: core side, port side, switched power, terminals
           # stage 17 (Andy, 2026-11-04: "other ideas of page ordering by relevance"); the shared-net counts between neighbors sum to 45 against 42 before

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
HIDE_VALUES = ('R-EU_R0402', 'R-EU_R0805', 'DIODEDO-214AC', 'DIODESOD-323', 'JUMPER-SMT_2_NO_SILK',
               'CONN_022.54_SCREW', 'CONN_42.54_SCREW', 'CONN_82.54_SCREW', 'CONN_102.54_SCREW')   # the screw terminals' package names (stage 13)
# stage 6 (Andy, second round): a small label for each circuit, headings for the new pages, room used
STAGE6 = {
 'Power_Input': dict(above=[('U5', 'Battery protection', -50, -4), ('U4', 'Solar charger', -40, -4), ('J5', 'V_PRIME', -10, -4), ('J6', 'Battery', -10, -4), ('J7', 'Solar', -10, -4)]),
 'Core_Supply': dict(blocks=[((5, 165, 97, 162), (0, 16))],   # D8, U37 (wired to U6's EN below it), the selector and LDO rows move down together
    above=[('U39', 'Core switch', -30, -4), ('U1', '5V_LP boost', -30, -4), ('U37', 'V_CORE select', -30, -4), ('U9', '3V3_CORE LDO', -20, -4)]),
 'Core_Power_Path': dict(headings=[('Core Power Path', 12.7, 15.24)], blocks=[((95, 140, 60, 110), (60, 0)), ((5, 95, 18, 110), (0, 12))],   # D9's row is wired to Q5 below it: the whole ideal-diode block moves down under the heading   # Q6 with its labels at x 102.87 first, then the ideal-diode block down
    props=[('D9', 'Reference', 55.88, 21.59)],
    above=[('U7', 'Ideal diode', -30, -4), ('D9', 'Battery / USB sense', -30, -4), ('Q6', 'Battery switch', -20, -4)]),
 'Aux_Rails': dict(above=[('U2', '3V3_AUX buck', -40, -4), ('U3', '5V_AUX boost', -40, -4), ('U13', 'POWER_EN logic', -30, -4), ('U40', 'C0/C1 decode', -20, -4), ('U21', 'V_HP switches', -60, -4)]),
 'Microcontroller': dict(rename_texts=[('Microcontroller & GPIO Expander', 'Microcontroller')], above=[('IC1', 'ATmega1284', -30, -4), ('S4', 'Reset', -5, -8), ('XTAL1', 'Clock', -8, -14)]),
 'GPIO_Expander': dict(headings=[('GPIO Expander', 12.7, 15.24)], above=[('U41', 'MCP23018', -20, -4), ('R58', 'Pull-ups', -10, -8)]),
 'Indicators': dict(blocks=[((190, 245, 30, 62), (0, 40))],   # the log button only, down; the status LED stays
    above=[('U45', 'PCA9634 LED driver', -20, -4), ('D5', 'Status LED', -10, -8), ('S3', 'Log button', -10, -8)]),
 'Cell_Module': dict(above=[('J9', 'B-series module', -20, -4), ('USB2', 'Module USB', -10, -4), ('D7', 'RGB LED', -10, -8), ('U35', 'FRAM', -10, -4), ('S6', 'Mode / reset buttons', -30, -8)]),
 'Level_Shifters': dict(rename_texts=[('Level Shifters', 'Level Shifters: Core Side')],
    above=[('U34', 'Feather UART (TXS0102)', -20, -4), ('U24', 'SDA select (mux)', -20, -4), ('U25', 'SPI buffer', -20, -4), ('U26', 'TXS0102', -20, -4)]),
 'Level_Shifters_Ports': dict(headings=[('Level Shifters: Port Side', 12.7, 15.24)], blocks=[((105, 200, 18, 150), (24, 0))],   # column 3 with its left-hand labels at x 110.49
    above=[('U27', 'TXS0104', -20, -4), ('U42', 'TXS0104', -20, -4), ('U29', 'TXS0104', -20, -4), ('U28', 'TCA9406 I2C', -20, -4), ('U36', 'TCA9406 I2C', -20, -4)]),
 'Sensors': dict(blocks=[((5, 110, 118, 152), (96, -64)), ((5, 110, 152, 190), (96, -56))],
    above=[('U31', 'BME280 environment', -20, -4), ('U44', 'VEML6030 light', -20, -4), ('U43', 'BMA456 accelerometer', -20, -4), ('U38', 'MLX90393 magnetometer', -20, -4)]),
 'Analog_Clock_Power': dict(headings=[('Analog, Clock & Power Monitor', 12.7, 15.24)],
    above=[('U30', 'DAC & reference', -30, -4), ('RTC1', 'Real-time clock', -20, -4), ('U32', 'PAC1934 power monitor', -20, -4), ('U33', 'ADS1115 ADC', -20, -4)]),
 'Sensor_Terminals': dict(blocks=[((65, 120, 50, 100), (92, -34)), ((65, 120, 15, 50), (52, 0)), ((15, 65, 60, 130), (44, -24))],
    above=[('J1', 'J1', -10, -4), ('J2', 'J2', -10, -4), ('J3', 'J3', -10, -4), ('J4', 'J4', -10, -4)]),
 'USB_ISP_Feather': dict(above=[('J10', 'USB-C', -5, -8), ('U23', 'FT231X USB serial', -20, -4)]),
 'Feather_ISP': dict(above=[('JP5', 'SDA jumper', -5, -8), ('ISP1', 'ICSP header', -10, -4), ('MS1', 'Feather socket', -10, -4), ('Q4', 'Feather enable', -20, -8)]),
}
ORDER = ['Core_Supply', 'Power_Input', 'Aux_Rails', 'Microcontroller', 'Indicators', 'Cell_Module',
         'Level_Shifters', 'Sensors', 'Sensor_Ports', 'USB_ISP_Feather']   # Core_Supply first: it gives notes away

LABRE = re.compile(r'^\t\((global_label|label) "([^"]*)"\n(\t\t\(shape \w+\)\n)?\t\t\(at ([-\d.]+) ([-\d.]+) (\d+)\)\n((?:.*\n)*?)\t\)\n', re.M)
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

def relist(proj, tools, sh, order, stage):
    """the root sheet rewritten to list the pages in this order (sheet uuids kept, so the board's paths hold)"""
    plan = [{'name': name, 'file': name + '.kicad_sch', 'uuid': re.search(r'\(uuid "([^"]*)"\)', open(sh(name)).read()).group(1)} for name in order]
    json.dump(plan, open(os.path.join(proj, 'sheets.json'), 'w'), indent=1)
    run('python3', os.path.join(tools, 'root_sheets.py'), sh('Okapi'), os.path.join(proj, 'sheets.json'), '--paper', 'USLetter')
    os.remove(os.path.join(proj, 'sheets.json'))
    run('kicad-cli', 'sch', 'upgrade', '--force', sh('Okapi'))
    print('stage %d: root re-listed, %s' % (stage, ', '.join(order)))

def trim_dividers(proj):
    """every page divider clipped to the printable area: x 10.16-269.24, y from 17.78 (below the heading band; 10.16
    until stage 15, when the Terminals heading was found sitting on its divider) to 205.74, or 172.72 beside the title block"""
    XL, XR, YT, YB, CX, CY = 10.16, 269.24, 17.78, 205.74, 172.72, 172.72
    ndiv = [0]
    for f in sorted(os.listdir(proj)):
        if not f.endswith('.kicad_sch'): continue
        path = os.path.join(proj, f); t = open(path).read()
        def trim(m):
            x1, y1, x2, y2 = map(float, m.groups())
            nx1, nx2 = (min(max(x, XL), XR) for x in (x1, x2))
            yb = CY if max(nx1, nx2) > CX else YB
            ny1, ny2 = (min(max(y, YT), yb) for y in (y1, y2))
            if (nx1, ny1, nx2, ny2) != (x1, y1, x2, y2): ndiv[0] += 1
            return '\t(polyline\n\t\t(pts\n\t\t\t(xy %s %s) (xy %s %s)' % (fmt(nx1), fmt(ny1), fmt(nx2), fmt(ny2))
        t2 = re.sub(r'^\t\(polyline\n\t\t\(pts\n\t\t\t\(xy ([-\d.]+) ([-\d.]+)\) \(xy ([-\d.]+) ([-\d.]+)\)', trim, t, flags=re.M)
        if t2 != t: open(path, 'w').write(t2)
    print('dividers trimmed: %d' % ndiv[0])

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
    if stage == 17:
        # the pages by relevance: power in to the aux rails, the brain with its USB port, the on-board peripherals,
        # the two Particle hosts, then the chain out to the sensor terminals
        relist(proj, tools, sh, ORDER16, 17)
        return
    if stage == 16:
        # the root re-listed so that ISP & Feather (the Boron's socket) follows Cellular Module (the B-series socket)
        relist(proj, tools, sh, ORDER_STAGE16, 16)
        return
    if stage == 15:
        # after the block moves: dividers kept out of the heading band, and every circuit label re-seated with two
        # ticks of air (pages_headings_check found five resting on the ink below them)
        trim_dividers(proj)
        for name in STAGE6:
            run('kicad-cli', 'sch', 'upgrade', '--force', sh(name))
        reseat_only = True; stage = 7
    if stage == 14:
        # Andy, 2026-11-04 evening: "uniform spacing, not crowding, grouping by function", then "execute the list".
        # Whole blocks by ticks, from the measured ink boxes: blocks that touched get a gap, stacks that left
        # half a page empty become two columns or a row, a stranded part goes back beside its chip.
        MOVES = [   # (page, rects x0 x1 y0 y1 in current mm, ticks dx dy, stretch); on one page a later rect must not
                    # cover where an earlier move has just put things, so the order below is the order that holds
            ('Power_Input', [(5, 170, 90, 205)], (0, 8), False),             # the solar charger block 10 mm down from the battery protection block it touched
            ('Core_Supply', [(5, 170, 115, 185)], (0, 12), False),           # V_CORE select and the LDO down first ...
            ('Core_Supply', [(25, 135, 52.5, 112)], (0, 8), False),          # ... then 5V_LP boost down from the core switch it touched
            ('Core_Power_Path', [(150, 215, 50, 100)], (-32, 0), False),     # the battery switch beside the ideal diode
            ('Microcontroller', [(5, 100, 18, 140), (100, 190, 15, 140)], (24, 0), False),   # the ATmega block, its labels and the Add: note 30 mm right
            ('Microcontroller', [(30, 76, 36, 90)], (-8, 0), True),          # then clock and reset 10 mm back out from the chip
            ('Level_Shifters', [(10, 100, 88, 113)], (100, -52), False),     # SDA select (mux) to a right column, top
            ('Level_Shifters', [(10, 100, 145, 175)], (100, -40), False),    # TXS0102 to the right column, bottom
            ('Level_Shifters', [(10, 100, 117, 142)], (0, -16), False),      # SPI buffer up under the Feather UART
            ('Level_Shifters_Ports', [(5, 50, 163, 195)], (80, -24), False), # C44 back beside the third TXS0104
            ('Sensors', [(15, 115, 78, 115)], (0, 28), False),               # VEML6030 to a second row
            ('Sensors', [(120, 245, 72, 120)], (0, 32), False),              # MLX90393 with C47, C48 to the second row
            ('Analog_Clock_Power', [(10, 131, 55, 110)], (0, -32), False),   # DAC up into the empty cell
            ('Analog_Clock_Power', [(25, 126, 120, 172)], (0, -20), False),  # the RTC up after it
            ('Sensor_Terminals', [(168, 215, 12, 56)], (35, 0), False),      # J1 to J4 in one row at a 66 mm pitch, rightmost first
            ('Sensor_Terminals', [(118, 165, 14, 52)], (23, 0), False),
            ('Sensor_Terminals', [(65, 118, 50, 102)], (11, -28), False),
            ('Sensor_Terminals', [(5, 270, 12, 110)], (0, 8), False),       # the whole row 10 mm down, so J4's label has a band above it
            ('Feather_ISP', [(10, 90, 50, 82)], (104, 70), False),           # the ICSP header under the power timer
            ('Feather_ISP', [(5, 115, 82, 190)], (0, -24), False),           # the Feather socket up under the SDA jumper
        ]
        for name, rects, (dx, dy), stretch in MOVES:
            cmd = ['python3', os.path.join(tools, 'sheet_lift.py'), sh(name), sh(name)]
            for x0, x1, y0, y1 in rects:
                cmd += ['--rect', str(x0), str(x1), str(y0), str(y1)]
            cmd += ['--translate', fmt(tk(dx)), fmt(tk(dy))]
            if stretch: cmd.append('--stretch')
            run(*cmd)
        path = sh('USB_ISP_Feather'); t = open(path).read()
        m = text_block(t, 'USB & ISP'); t = t[:m.start()] + t[m.end():]; open(path, 'w').write(t)   # Bobby's block label, under the page heading now
        for name in sorted({m_[0] for m_ in MOVES} | {'USB_ISP_Feather'}):
            run('kicad-cli', 'sch', 'upgrade', '--force', sh(name))
        print('stage 14: %d block moves' % len(MOVES))
        only = 'Sensor_Terminals'; reseat_only = True; stage = 7   # then the four connector labels re-seated on the moved row
    HAND = {'Indicators': ['PCA9634 LED driver', 'Status LED'],                              # circuit labels set by hand in stages 9 and 10; the search leaves them
            'Level_Shifters_Ports': [a[1] for a in STAGE6['Level_Shifters_Ports']['above']],   # replaced by one label per column in stage 10
            'Power_Input': ['V_PRIME', 'Battery', 'Solar'],                                    # beside their connectors (stage 13)
            'Aux_Rails': ['3V3_AUX buck']}                                                     # the fullest page: a 7 mm band sent it over the mid-page heading (stage 15), so it keeps its stage-13 seat
    if stage == 13:
        # Andy's third round, the general causes behind "Battery / USB sense has nothing under it" and the
        # garbled text at D9: (1) every BOM field that prints (D9's DIGIKEY, MF and MPN, all at one point) and
        # the screw terminals' package-name values are hidden; (2) each circuit label is centered over its part
        # instead of sitting at a typed offset, then re-seated by the stage-7 band search from there.
        # the pull-up ladder six more ticks down, so its label has a band above the rail labels and under U41's notes
        run('python3', os.path.join(tools, 'sheet_lift.py'), sh('GPIO_Expander'), sh('GPIO_Expander'), '--rect', '5', '150', '100', '150', '--translate', '0', fmt(tk(6)), '--stretch')
        # the SPI buffer and the TXS0102 under it six ticks down, so the buffer's label has a band between it and the mux
        run('python3', os.path.join(tools, 'sheet_lift.py'), sh('Level_Shifters'), sh('Level_Shifters'), '--rect', '5', '100', '110', '200', '--translate', '0', fmt(tk(6)), '--stretch')
        # the three terminal labels stand beside their connectors (a column of connectors leaves no band between them)
        BESIDE = {'Power_Input': [('J5', 'V_PRIME'), ('J6', 'Battery'), ('J7', 'Solar')]}
        for name, pairs in BESIDE.items():
            path = sh(name); t = open(path).read()
            longest = max(len(text) for ref, text in pairs)   # one x for the group, so the labels line up, 14 mm clear of the connectors' pin stubs (bold text runs wider than 2.2 mm a character)
            for ref, text in pairs:
                sm = [s for s in re.finditer(r'\t\(symbol\n(?:.*\n)*?\t\)\n', t) if '(property "Reference" "%s"' % ref in s.group(0)]
                px, py = (float(v) for v in re.search(r'\t\t\(at ([-\d.]+) ([-\d.]+)', sm[0].group(0)).groups())
                m = text_block(t, text)
                blk = re.sub(r'\(at [-\d.]+ [-\d.]+ (\d+)\)', lambda q: '(at %s %s %s)' % (fmt(round((px - 2.2 * longest - 14) / T) * T), fmt(py), q.group(1)), m.group(0), count=1)
                t = t[:m.start()] + blk + t[m.end():]
            open(path, 'w').write(t); print('%s: %d labels set beside their connectors' % (name, len(pairs)))
        for f in sorted(os.listdir(proj)):
            if not f.endswith('.kicad_sch'): continue
            path = os.path.join(proj, f); t = open(path).read(); n = 0
            t, k = re.subn(r'(\t\t\(property "(?!Reference|Value|Footprint|Datasheet|Description|Sheetname|Sheetfile)[^"]*" "[^"]+"\n\t\t\t\(at [^)]*\)\n)(?!\t\t\t\(hide yes\))', r'\1\t\t\t(hide yes)\n', t); n += k
            for v in HIDE_VALUES:
                t, k = re.subn(r'(\t\t\(property "Value" "%s"\n\t\t\t\(at [^)]*\)\n)(?!\t\t\t\(hide yes\))' % re.escape(v), r'\1\t\t\t(hide yes)\n', t); n += k
            if n:
                open(path, 'w').write(t); print('%s: %d fields hidden' % (f, n))
        for name, p in STAGE6.items():
            if only and name != only: continue
            labels = [(a[0], a[1]) for a in p.get('above', []) if a[1] not in HAND.get(name, [])]
            if not labels: continue
            path = sh(name); t = open(path).read(); n = 0
            for ref, text in labels:
                m = text_block(t, text); blk = m.group(0)
                sm = [s for s in re.finditer(r'\t\(symbol\n(?:.*\n)*?\t\)\n', t) if '(property "Reference" "%s"' % ref in s.group(0)]
                if not sm: print('  %s: no part %s for %r' % (name, ref, text)); continue
                px = float(re.search(r'\t\t\(at ([-\d.]+) ', sm[0].group(0)).group(1))
                w = 2.2 * len(text) + 1                                   # measured: 19 characters of 3.048 bold print 43 mm wide
                x = round((px - w / 2) / T) * T
                blk2 = re.sub(r'\(at [-\d.]+ ([-\d.]+) (\d+)\)', lambda q: '(at %s %s %s)' % (fmt(x), q.group(1), q.group(2)), blk, count=1)
                if blk2 != blk: t = t[:m.start()] + blk2 + t[m.end():]; n += 1
            open(path, 'w').write(t); print('%s: %d circuit labels centered on their parts' % (name, n))
        reseat_only = True   # then the band search from the new x, without stage 7's one-off nudges
        stage = 7
    if stage == 12:
        # The edge rule as a general fix (Andy, third round: "seek to solve general problems instead of tweaking
        # locally"): every page divider is trimmed to the printable area, the two blocks that hang past the right
        # border move in by whole ticks, and then every page is shifted by the whole ticks its own rendered ink needs
        # to sit inside x 8.5-272.9 mm and y 8.5-209.4 mm, with nothing over the title block (x > 172.3, y > 174.8).
        trim_dividers(proj)
        run('python3', os.path.join(tools, 'sheet_lift.py'), sh('Power_Input'), sh('Power_Input'), '--rect', '186', '280', '5', '120', '--translate', fmt(tk(-16)), '0')   # the terminals block, with its heading, centered in its column
        run('python3', os.path.join(tools, 'sheet_lift.py'), sh('Feather_ISP'), sh('Feather_ISP'), '--rect', '145', '280', '5', '120', '--translate', fmt(tk(-8)), '0')     # the TPL5111 timer block, with its heading
        # every page's ink, from KiCad's own print, decides its shift
        pdf = os.path.join(proj, 'edge_fit.pdf')
        run('kicad-cli', 'sch', 'export', 'pdf', '-e', '-n', '--black-and-white', '-o', pdf, sh('Okapi'))
        run('pdftoppm', '-r', '50', '-png', pdf, pdf[:-4]); os.remove(pdf)
        from PIL import Image
        import numpy as np, math, glob
        k = 25.4 / 50
        pngs = sorted(glob.glob(pdf[:-4] + '-*.png')); assert len(pngs) == 1 + len(ORDER_STAGE16), pngs
        for name, png in zip(ORDER_STAGE16, pngs[1:]):
            a = np.asarray(Image.open(png).convert('L')) < 200; ys, xs = np.where(a)
            x0, x1, y0, y1 = xs.min() * k, xs.max() * k, ys.min() * k, ys.max() * k
            dx = max(0, math.ceil((8.5 - x0) / T)); dy = max(0, math.ceil((8.5 - y0) / T))
            assert x1 + dx * T <= 272.9 and y1 + dy * T <= 209.4, (name, x0, x1, y0, y1, dx, dy)
            if dx or dy:
                run('python3', os.path.join(tools, 'sheet_page.py'), sh(name), '--translate', fmt(tk(dx)), fmt(tk(dy)))
            print('%-22s ink x %.1f-%.1f y %.1f-%.1f  shift %d,%d ticks' % (name, x0, x1, y0, y1, dx, dy))
            os.remove(png)
        os.remove(pngs[0])
        for f in sorted(os.listdir(proj)):
            if f.endswith('.kicad_sch'): run('kicad-cli', 'sch', 'upgrade', '--force', os.path.join(proj, f))
        return
    if stage == 11:
        # Andy's third round: the SD card off the page edge, C32 out from under the RTC's labels, the pull-up ladder
        # clear of U41, J2's diagonal leads straightened; the edge rule is now 4 mm inside the border (gate.sh)
        sys.path.insert(0, tools)
        from sch_edit import Editor, fmt as efmt
        run('python3', os.path.join(tools, 'sheet_lift.py'), sh('Cell_Module'), sh('Cell_Module'), '--rect', '200', '280', '5', '75', '--translate', fmt(tk(-5)), '0')
        run('python3', os.path.join(tools, 'sheet_lift.py'), sh('Analog_Clock_Power'), sh('Analog_Clock_Power'), '--rect', '40', '54', '135', '160', '--translate', fmt(tk(-8)), '0', '--stretch')
        run('python3', os.path.join(tools, 'sheet_lift.py'), sh('GPIO_Expander'), sh('GPIO_Expander'), '--rect', '5', '150', '100', '190', '--translate', '0', fmt(tk(8)), '--stretch')   # the whole ladder, R55 at y 109 to R58 at 130
        # J2: each diagonal lead becomes a horizontal stub of four ticks with its label at the far end, pointing left
        path = sh('Sensor_Terminals'); t = open(path).read()
        wires = [(m, (float(m.group(1)), float(m.group(2))), (float(m.group(3)), float(m.group(4)))) for m in re.finditer(r'\t\(wire\n\t\t\(pts\n\t\t\t\(xy ([-\d.]+) ([-\d.]+)\) \(xy ([-\d.]+) ([-\d.]+)\)\n(?:.*\n)*?\t\)\n', t)]
        labels = {(float(m.group(4)), float(m.group(5))): m for m in LABRE.finditer(t)}
        n = 0
        for m, a_, b_ in wires:
            if abs(a_[0] - b_[0]) < 1e-6 or abs(a_[1] - b_[1]) < 1e-6: continue   # straight
            lab, pin = (a_, b_) if a_ in labels else ((b_, a_) if b_ in labels else (None, None))
            if lab is None: continue
            nx, ny = pin[0] - 5.08, pin[1]
            t = t.replace(m.group(0), m.group(0).replace('(xy %s %s)' % (efmt(lab[0]), efmt(lab[1])), '(xy %s %s)' % (efmt(nx), efmt(ny)), 1), 1)
            lm = labels[lab]
            t = t.replace(lm.group(0), re.sub(r'\(at [-\d.]+ [-\d.]+ \d+\)', '(at %s %s 180)' % (efmt(nx), efmt(ny)), lm.group(0), count=1).replace('(justify left)', '(justify right)'), 1)
            n += 1
        open(path, 'w').write(t); print('Sensor_Terminals: %d diagonal leads straightened' % n)
        for name in ('Cell_Module', 'Analog_Clock_Power', 'GPIO_Expander', 'Sensor_Terminals'):
            run('kicad-cli', 'sch', 'upgrade', '--force', sh(name))
        return
    if stage == 10:
        # the ports page: one label per column at the top instead of one beside each chip (the chips' Value
        # fields already print their part numbers and the columns are 15 mm apart); Indicators: two last nudges
        path = sh('Level_Shifters_Ports'); t = open(path).read()
        for text in ('TXS0104 (U28)', 'TXS0104 (U27)', 'TXS0104 (U42)', 'TCA9406 (U29)', 'TCA9406 (U36)'):
            m = text_block(t, text); t = t[:m.start()] + t[m.end():]
        open(path, 'w').write(t)
        subs = [('4-bit shifters, TXS0104', 38.1, 33.02), ('I2C shifters, TCA9406', 139.7, 33.02)]
        append_items(path, [HEADING.replace('(size 5.08 4.318)', '(size 3.048 2.54)').replace('(thickness 0.8636)', '(thickness 0.508)').format(text=a_, x=fmt(x), y=fmt(y), u=u5('Level_Shifters_Ports', 'column', i)) for i, (a_, x, y) in enumerate(subs)])
        run('kicad-cli', 'sch', 'upgrade', '--force', path); print('Level_Shifters_Ports: a label per column')
        path = sh('Indicators')
        run('python3', os.path.join(tools, 'sheet_lift.py'), path, path, '--rect', '155', '190', '17', '96', '--translate', '0', fmt(tk(2)))
        t = open(path).read()
        m = text_block(t, 'PCA9634 LED driver'); blk = re.sub(r'\(at -?[\d.]+ -?[\d.]+ (\d+)\)', lambda q: '(at 12.7 43.18 %s)' % q.group(1), m.group(0), count=1); t = t[:m.start()] + blk + t[m.end():]
        open(path, 'w').write(t)
        run('kicad-cli', 'sch', 'upgrade', '--force', path); print('Indicators: nudged')
        return
    if stage == 9:
        # the six labels the raster search could not seat: stacked columns on the ports page (labels set beside
        # each chip instead), and the Indicators status block, nudged down with its label and the driver's label set by hand
        sys.path.insert(0, tools)
        path = sh('Level_Shifters_Ports'); t = open(path).read()
        for text in ('TXS0104', 'TXS0104', 'TXS0104', 'TCA9406 I2C', 'TCA9406 I2C'):
            m = text_block(t, text); t = t[:m.start()] + t[m.end():]
        open(path, 'w').write(t)
        subs = [('TXS0104 (U28)', 118.11, 57.15), ('TXS0104 (U27)', 118.11, 96.52), ('TXS0104 (U42)', 118.11, 139.7), ('TCA9406 (U29)', 200.66, 57.15), ('TCA9406 (U36)', 200.66, 96.52)]
        append_items(path, [HEADING.replace('(size 5.08 4.318)', '(size 3.048 2.54)').replace('(thickness 0.8636)', '(thickness 0.508)').format(text=a_, x=fmt(x), y=fmt(y), u=u5('Level_Shifters_Ports', 'beside', i)) for i, (a_, x, y) in enumerate(subs)])
        run('kicad-cli', 'sch', 'upgrade', '--force', path); print('Level_Shifters_Ports: five labels set beside their chips')
        path = sh('Indicators')
        run('python3', os.path.join(tools, 'sheet_lift.py'), path, path, '--rect', '155', '190', '17', '86', '--translate', '0', fmt(tk(6)))
        t = open(path).read()
        for text, x, y in (('PCA9634 LED driver', 12.7, 45.72), ('Status LED', 160.02, 22.86)):
            m = text_block(t, text); blk = re.sub(r'\(at -?[\d.]+ -?[\d.]+ (\d+)\)', lambda q: '(at %s %s %s)' % (fmt(x), fmt(y), q.group(1)), m.group(0), count=1); t = t[:m.start()] + blk + t[m.end():]
        open(path, 'w').write(t)
        run('kicad-cli', 'sch', 'upgrade', '--force', path); print('Indicators: status block down six ticks, two labels set')
        return
    if stage == 8:
        # pages whose top block sat against the heading band, so a circuit label found no room: down six ticks
        for name in ('Core_Supply', 'Core_Power_Path', 'Aux_Rails', 'Indicators', 'Level_Shifters', 'Level_Shifters_Ports',
                     'Analog_Clock_Power', 'Sensor_Terminals', 'Feather_ISP'):
            if only and name != only: continue
            t = open(sh(name)).read()
            # everything but the 5.08 mm page headings moves (sheet_page.py would move those too)
            i = t.find('(lib_symbols'); d = 0; j = i
            while True:
                if t[j] == '(': d += 1
                elif t[j] == ')':
                    d -= 1
                    if d == 0: break
                j += 1
            head, lib, body = t[:i], t[i:j + 1], t[j + 1:]
            heads = re.findall(r'\t\(text "[^"]*"\n\t\t\(exclude_from_sim no\)\n\t\t\(at [^)]*\)\n\t\t\(effects\n\t\t\t\(font\n\t\t\t\t\(size 5\.08 4\.318\)\n(?:.*\n)*?\t\)\n', body)
            for h in heads: body = body.replace(h, '', 1)
            body = re.sub(r'\((at|xy|start|end|center|mid) (-?[\d.]+) (-?[\d.]+)', lambda m: '(%s %s %s' % (m.group(1), fmt(float(m.group(2))), fmt(float(m.group(3)) + tk(6))), body)
            open(sh(name), 'w').write(head + lib + ''.join(heads) + body)
            run('kicad-cli', 'sch', 'upgrade', '--force', sh(name))
            print('%s: moved down six ticks under its heading' % name)
        return
    if stage == 7:
        # the circuit labels of stage 6 were set just above each part's Reference text, which on these
        # imported symbols sits on the body; here each is moved up to the first clear band in its own
        # column, found on a raster of the page without its labels (1.9 mm per character, 6 mm band)
        import shutil
        from PIL import Image
        import numpy as np
        K_ = 100 / 25.4
        NUDGE = {'Indicators': [((155, 190, 17, 70), (0, 4))]}        # the status LED block (the LED row's bus reaches x 152.4), from under its heading
        MOVE_TEXTS = {'Aux_Rails': [('3V3_AUX & 5V_AUX Rails', 12.7, 88.9)]}   # the mid-page heading follows its block down
        if 'reseat_only' not in dir(): reseat_only = False
        for name, p in STAGE6.items():
            if only and name != only: continue
            path = sh(name)
            for (x0, x1, y0, y1), (bx, by) in ([] if reseat_only else NUDGE.get(name, [])):
                run('python3', os.path.join(tools, 'sheet_lift.py'), path, path, '--rect', str(x0), str(x1), str(y0), str(y1), '--translate', fmt(tk(bx)), fmt(tk(by)))
            if MOVE_TEXTS.get(name) and not reseat_only:
                t = open(path).read()
                for text, x, y in MOVE_TEXTS[name]:
                    m = text_block(t, text); blk = re.sub(r'\(at -?[\d.]+ -?[\d.]+ (\d+)\)', lambda q: '(at %s %s %s)' % (fmt(x), fmt(y), q.group(1)), m.group(0), count=1); t = t[:m.start()] + blk + t[m.end():]
                open(path, 'w').write(t)
            labels = [a[1] for a in p.get('above', []) if a[1] not in HAND.get(name, [])]
            if not labels: continue
            t = open(path).read()
            # a page copy without the circuit labels, rendered alone
            tmp = os.path.join(proj, '_probe'); shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
            t2 = t
            for text in labels:
                m = text_block(t2, text); t2 = t2[:m.start()] + t2[m.end():]
            open(os.path.join(tmp, 'probe.kicad_sch'), 'w').write(t2)
            for f in ('fp-lib-table', 'sym-lib-table'):
                if os.path.exists(os.path.join(proj, f)): shutil.copy(os.path.join(proj, f), tmp)
            subprocess.run(['kicad-cli', 'sch', 'export', 'pdf', '-e', '-n', '--black-and-white', '-o', os.path.join(tmp, 'p.pdf'), os.path.join(tmp, 'probe.kicad_sch')], capture_output=True)
            subprocess.run(['pdftoppm', '-r', '100', '-png', '-singlefile', os.path.join(tmp, 'p.pdf'), os.path.join(tmp, 'p')], capture_output=True)
            ink = np.asarray(Image.open(os.path.join(tmp, 'p.png')).convert('L')) < 200
            moved = []
            refs = {a[1]: a[0] for a in p.get('above', [])}
            for text in labels:
                m = text_block(t, text); blk = m.group(0)
                at = re.search(r'\(at ([-\d.]+) ([-\d.]+) (\d+)\)', blk); x = float(at.group(1))
                # the search starts at the part's Reference text, not at wherever the label sits now
                sm = [s for s in re.finditer(r'\t\(symbol\n(?:.*\n)*?\t\)\n', t) if '(property "Reference" "%s"' % refs[text] in s.group(0)]
                r = re.search(r'\(property "Reference" "[^"]*"\n\t\t\t\(at ([-\d.]+) ([-\d.]+)', sm[0].group(0)); y = float(r.group(2))
                w = 2.2 * len(text) + 1
                def seat(xx):            # the band for a column starting at xx, or None
                    cx0, cx1 = int(xx * K_), int((xx + w) * K_)
                    def clear(yy):
                        band = ink[int((yy - 7) * K_):int(yy * K_), cx0:cx1]; return band.size and not band.any()   # 7 mm: the label box with two ticks of air under it
                    def ink_below(yy):       # distance from a band's bottom to the first ink under it in the column
                        col = ink[int(yy * K_):, cx0:cx1].any(axis=1); rows = np.where(col)[0]
                        return rows[0] / K_ if len(rows) else 99
                    yy = y
                    while yy >= 24:          # a band above the part, no further from the part's ink than 8 mm
                        if clear(yy) and ink_below(yy) <= 8: return yy
                        yy -= 1.27
                    yy = y + 7.62            # else a band below it, within 8 mm of the ink above
                    while yy <= 205:
                        if clear(yy):
                            col = ink[:int((yy - 7) * K_), cx0:cx1].any(axis=1); rows = np.where(col)[0]
                            if len(rows) and (yy - 7) - rows[-1] / K_ <= 8: return yy
                        yy += 1.27
                    return None
                # the column slides by whole ticks either side of where the label starts (centered on its part since
                # stage 13; a vertical wire above the part blocks one column and not the next); nearest seat wins
                best = None
                for k in sorted(range(-20, 21), key=abs):
                    xx = x + k * 1.27
                    if xx < 8.5 or xx + w > 272.9: continue
                    yy = seat(xx)
                    if yy is None: continue
                    key = (0 if yy < y else 1, abs(yy - y) + 3 * abs(k) * 1.27)   # above the part before below it; then the nearest seat, a slid column costing three times its slide
                    if best is None or key < best[0]: best = (key, xx, yy)
                if best is None:
                    print('  %s: no clear band near the part for %r, left at y %.2f' % (name, text, float(at.group(2)))); continue
                _, x, ny = best
                cx0, cx1 = int(x * K_), int((x + w) * K_)
                ny = round((ny - 2.54) / 1.27) * 1.27      # two ticks of air under the label (one left five labels resting on ink, stage 15)
                ink[int((ny - 4.5) * K_):int((ny + 0.5) * K_), cx0:cx1] = True   # this label's box is taken now
                if (fmt(x), fmt(ny)) != (at.group(1), at.group(2)):
                    blk2 = blk.replace(at.group(0), '(at %s %s %s)' % (fmt(x), fmt(ny), at.group(3)), 1)
                    t = t[:m.start()] + blk2 + t[m.end():]; moved.append((text, y, ny))
            open(path, 'w').write(t)
            shutil.rmtree(tmp, ignore_errors=True)
            run('kicad-cli', 'sch', 'upgrade', '--force', path)
            print('%s: %d circuit labels raised' % (name, len(moved)))
        return
    if stage == 5:
        # Andy, second round: "this is usually the time to expand and produce more pages". Six pages give a
        # block each to a new page (sheet_lift.py with --new), the stale dividers and two orphaned notes go,
        # and the root lists sixteen pages in reading order.
        SPLITS = [   # (source page, new page, rects in source mm, translate in ticks)
            ('Core_Supply', 'Core_Power_Path', [(5, 180, 148, 215)], (0, -97)),                      # LTC4412 ideal diode, D9, Q5, Q6
            ('Microcontroller', 'GPIO_Expander', [(129, 275, 60, 172)], (-88, -28)),                  # MCP23018, its notes and pull-up ladder
            ('Level_Shifters', 'Level_Shifters_Ports', [(103, 280, 18, 200)], (-67, 0)),   # the TXS0104s and TCA9406s with their caps (the labels at x 106.68 are the caps' rails)
            ('Sensors', 'Analog_Clock_Power', [(75, 110, 55, 91), (100, 110, 130, 160), (110, 280, 18, 200)], (-45, 0)),    # DAC and reference, RTC, PAC1934, ADS1115
            ('Sensor_Ports', 'Sensor_Terminals', [(183, 280, 5, 200)], (-130, 0)),                   # J1 to J4 with their heading
            ('USB_ISP_Feather', 'Feather_ISP', [(190, 280, 5, 200)], (-140, 0)),                     # JP5, ICSP, the Feather socket, Q4, with the heading
            ('USB_ISP_Feather', 'Feather_ISP', [(5, 186, 123, 198)], (112, -77)),                    # the TPL5111 timer with its heading, to the new page's right half
        ]
        DELETE_POLYLINES = {'Sensor_Ports': [((181.61, 5.08), (181.61, 175.26))],
                            'USB_ISP_Feather': [((187.96, 5.08), (187.96, 175.26)), ((5.08, 121.92), (187.96, 121.92))]}
        DELETE_TEXTS = {'Power_Input': ['To Battery Connectors'],      # Bobby's pointer to wires that now sit beside the terminals they went to
                        'Indicators': ['Indicators']}                 # his small block label, now under the page heading and over 3V3_CORE
        # a local label whose instances would land on two pages becomes one net on each: make it global first
        t = open(sh('Microcontroller')).read()
        t, n = re.subn(r'\t\(label "GLOBAL_INT"\n\t\t\(at (-?[\d.]+) (-?[\d.]+) (\d+)\)\n\t\t\(effects\n(?:.*\n)*?\t\t\)\n\t\t\(uuid "([^"]*)"\)\n\t\)\n',
                      lambda m: ('\t(global_label "GLOBAL_INT"\n\t\t(shape bidirectional)\n\t\t(at %s %s %s)\n\t\t(fields_autoplaced yes)\n'
                                 '\t\t(effects\n\t\t\t(font\n\t\t\t\t(size 1.27 1.27)\n\t\t\t)\n\t\t\t(justify %s)\n\t\t)\n\t\t(uuid "%s")\n'
                                 '\t\t(property "Intersheetrefs" "${INTERSHEET_REFS}"\n\t\t\t(at %s %s 0)\n\t\t\t(hide yes)\n\t\t\t(show_name no)\n\t\t\t(do_not_autoplace no)\n'
                                 '\t\t\t(effects\n\t\t\t\t(font\n\t\t\t\t\t(size 1.27 1.27)\n\t\t\t\t)\n\t\t\t\t(justify left)\n\t\t\t)\n\t\t)\n\t)\n')
                                % (m.group(1), m.group(2), m.group(3), 'left' if int(m.group(3)) in (0, 90) else 'right', m.group(4), '%g' % (float(m.group(1)) + 12.608), m.group(2)), t)
        open(sh('Microcontroller'), 'w').write(t); print('GLOBAL_INT: %d local labels made global' % n)
        for src, dst, rects, (dx, dy) in SPLITS:
            cmd = ['python3', os.path.join(tools, 'sheet_lift.py'), sh(src), sh(dst)]
            for x0, x1, y0, y1 in rects:
                cmd += ['--rect', str(x0), str(x1), str(y0), str(y1)]
            cmd += ['--translate', fmt(tk(dx)), fmt(tk(dy))]
            if not os.path.exists(sh(dst)):
                cmd += ['--new', '--uuid', page_uuid(dst), '--paper', 'USLetter', '--date', DATE, '--rev', REV]
            run(*cmd)
        # pages whose leftward labels grew past the left border: moved in by whole ticks
        for name, (ex, ey) in {'Power_Input': (5, 0), 'Sensors': (5, 0), 'Feather_ISP': (4, 0)}.items():
            run('python3', os.path.join(tools, 'sheet_page.py'), sh(name), '--translate', fmt(tk(ex)), fmt(tk(ey)))
        run('python3', os.path.join(tools, 'sheet_lift.py'), sh('Cell_Module'), sh('Cell_Module'), '--rect', '5', '60', '95', '125', '--translate', fmt(tk(8)), '0')   # the RGB LED block
        for name, lines in DELETE_POLYLINES.items():
            t = open(sh(name)).read()
            for (x1, y1), (x2, y2) in lines:
                t, n = re.subn(r'\t\(polyline\n\t\t\(pts\n\t\t\t\(xy %s %s\) \(xy %s %s\)\n(?:.*\n)*?\t\)\n' % (re.escape(fmt(x1)), re.escape(fmt(y1)), re.escape(fmt(x2)), re.escape(fmt(y2))), '', t, count=1)
                assert n == 1, ('polyline', name, x1, y1)
            open(sh(name), 'w').write(t)
        for name, texts in DELETE_TEXTS.items():
            t = open(sh(name)).read()
            for text in texts:
                m = text_block(t, text); t = t[:m.start()] + t[m.end():]
            open(sh(name), 'w').write(t)
        plan = []
        for name in ORDER_STAGE16:
            u = page_uuid(name) if name in [s[1] for s in SPLITS] else re.search(r'\(uuid "([^"]*)"\)', open(sh(name)).read()).group(1)
            plan.append({'name': name, 'file': name + '.kicad_sch', 'uuid': u})
        json.dump(plan, open(os.path.join(proj, 'sheets.json'), 'w'), indent=1)
        run('python3', os.path.join(tools, 'root_sheets.py'), sh('Okapi'), os.path.join(proj, 'sheets.json'), '--paper', 'USLetter')
        os.remove(os.path.join(proj, 'sheets.json'))
        for f in sorted(os.listdir(proj)):
            if f.endswith('.kicad_sch'):
                run('kicad-cli', 'sch', 'upgrade', '--force', os.path.join(proj, f))
        print('stage 5: %d lifts, root with %d pages' % (len(SPLITS), len(ORDER_STAGE16)))
        return
    if stage == 4:
        # Andy, second round (okapi_2026-11-03_v2-AW.pdf): "hold all font sizes constant". One size per kind:
        # labels 1.27 mm (KiCad's default; Bobby's larger ones were 1.2446, the importer's 0.569 to 1.016),
        # notes 1.778 (Bobby's pin notes and most of his remarks), Reference and Value fields 1.27; headings
        # (5.08) and circuit labels (3.048) untouched.
        for f in sorted(os.listdir(proj)):
            if not f.endswith('.kicad_sch') or f == 'Okapi.kicad_sch': continue
            path = os.path.join(proj, f); t = open(path).read()
            i = t.find('(lib_symbols'); d = 0; j = i
            while True:
                if t[j] == '(': d += 1
                elif t[j] == ')':
                    d -= 1
                    if d == 0: break
                j += 1
            head, lib, body = t[:i], t[i:j + 1], t[j + 1:]
            n = [0, 0, 0]
            def lab(m):
                n[0] += 1; return m.group(1) + '(size 1.27 1.27)'
            body = re.sub(r'(\t\((?:global_label|label|hierarchical_label) "[^"]*"\n(?:\t\t\(shape \w+\)\n)?\t\t\(at [^)]*\)\n(?:\t\t\(fields_autoplaced yes\)\n)?\t\t\(effects\n\t\t\t\(font\n\t\t\t\t)\(size [\d.]+ [\d.]+\)', lab, body)
            def txt(m):
                if m.group(2) in ('5.08', '3.048'): return m.group(0)
                n[1] += 1; return m.group(1) + '(size 1.778 1.778)'
            body = re.sub(r'(\t\(text "[^"]*"\n\t\t\(exclude_from_sim no\)\n\t\t\(at [^)]*\)\n\t\t\(effects\n\t\t\t\(font\n\t\t\t\t)\(size ([\d.]+) [\d.]+\)', txt, body)
            def fld(m):
                n[2] += 1; return m.group(1) + '(size 1.27 1.27)'
            body = re.sub(r'(\t\t\(property "(?:Reference|Value)" "[^"]*"\n\t\t\t\(at [^)]*\)\n(?:\t\t\t\((?!effects)[^\n]*\n)*?\t\t\t\(effects\n\t\t\t\t\(font\n\t\t\t\t\t)\(size [\d.]+ [\d.]+\)', fld, body)
            open(path, 'w').write(head + lib + body)
            run('kicad-cli', 'sch', 'upgrade', '--force', path)
            print('%s: %d labels, %d notes, %d fields resized' % (f, n[0], n[1], n[2]))
        return
    if stage in (3, 6):
        sys.path.insert(0, tools)
        from sch_edit import Editor, fmt as efmt
        PLAN_N = {3: STAGE3, 6: STAGE6}[stage]
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
        for name, p in PLAN_N.items():
            if only and name != only:
                continue
            path = sh(name)
            if p.get('rename_texts') or p.get('headings'):
                t = open(path).read()
                for a_, b_ in p.get('rename_texts', []):
                    m = text_block(t, a_); t = t[:m.start()] + m.group(0).replace('(text "%s"' % a_, '(text "%s"' % b_, 1) + t[m.end():]
                open(path, 'w').write(t)
                if p.get('headings'):
                    append_items(path, [HEADING.format(text=text, x=fmt(x), y=fmt(y), u=u5(name, 'heading6', i)) for i, (text, x, y) in enumerate(p['headings'])])
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
            for i, (ref, text, ox, oy) in enumerate(p.get('above', [])):   # a circuit label above a part: at its Reference text, offset (ox, oy) mm
                m = [m for m in re.finditer(r'\t\(symbol\n(?:.*\n)*?\t\)\n', t) if '(property "Reference" "%s"' % ref in m.group(0)]
                assert len(m) == 1, (name, ref, len(m))
                r = re.search(r'\(property "Reference" "[^"]*"\n\t\t\t\(at ([-\d.]+) ([-\d.]+)', m[0].group(0))
                subs.append(HEADING.replace('(size 5.08 4.318)', '(size 3.048 2.54)').replace('(thickness 0.8636)', '(thickness 0.508)').format(text=text, x=fmt(float(r.group(1)) + ox), y=fmt(float(r.group(2)) + oy), u=u5(name, 'above', i)))
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

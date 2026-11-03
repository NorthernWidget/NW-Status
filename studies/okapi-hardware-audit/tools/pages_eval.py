"""Evaluate candidate page groupings of the Okapi schematic for US Letter.

usage: pages_eval.py <regions.json> <ink.json> <nets.json> [candidate ...]

Inputs come from pages_regions.py, pages_ink.py and pages_graph.py. Each
candidate is a list of pages, each page a list of rigid blocks (regions). For
every page the script reports the parts on it, the packed ink size and whether
it fits the US Letter drawing area clear of the title block, the local labels
that the grouping splits, and the nets that leave the page (all nets, then
signal nets with the rails of pages_graph.RAILS excluded). The totals count
every net that spans two or more pages.

Packing: blocks keep their measured ink boxes (pages_ink.py) and are placed by
a bottom-left heuristic over every ordering with GAP between blocks, on a
PAGE_W x PAGE_H area whose lower-right TB_W x TB_H corner (the title block) is
blocked. A page "fits" when some ordering places every block. The heuristic
can miss a feasible packing, never report an infeasible one, so "no fit" for a
page with several blocks is a strong hint and not a proof.
"""
import sys, json, itertools, re

PAGE_W, PAGE_H = 274.0, 211.0         # US Letter drawing area inside the 2.5 mm margins
TB_W, TB_H = 101.6, 35.56             # title block, lower right
GAP = 2.54                            # two grid ticks between ink boxes
EPS = 1e-6

def fits_corner(x, y, w, h):
    return not (x + w > PAGE_W - TB_W + EPS and y + h > PAGE_H - TB_H + EPS)

def overlap(a, b):
    (x, y, w, h), (x2, y2, w2, h2) = a, b
    return not (x + w + GAP <= x2 + EPS or x2 + w2 + GAP <= x + EPS or
                y + h + GAP <= y2 + EPS or y2 + h2 + GAP <= y + EPS)

def pack(blocks):
    """blocks: [(name, w, h)]. Returns (W, H, placed) of the smallest-area packing, or None."""
    best = None
    for perm in itertools.permutations(blocks):
        placed = []
        ok = True
        for name, w, h in perm:
            cands = {(0.0, 0.0)}
            for _, x2, y2, w2, h2 in placed:
                cands |= {(x2 + w2 + GAP, y2), (x2, y2 + h2 + GAP), (x2 + w2 + GAP, 0.0), (0.0, y2 + h2 + GAP)}
            pos = None
            for x, y in sorted(cands, key=lambda c: (c[1], c[0])):
                if x + w > PAGE_W + EPS or y + h > PAGE_H + EPS or not fits_corner(x, y, w, h):
                    continue
                if any(overlap((x, y, w, h), (x2, y2, w2, h2)) for _, x2, y2, w2, h2 in placed):
                    continue
                pos = (x, y)
                break
            if pos is None:
                ok = False
                break
            placed.append((name, pos[0], pos[1], w, h))
        if ok:
            W = max(x + w for _, x, y, w, h in placed)
            H = max(y + h for _, x, y, w, h in placed)
            if best is None or W * H < best[0] * best[1] - EPS:
                best = (W, H, placed)
    return best

def natural(ref):
    m = re.match(r'([^\d]*)(\d*)', ref)
    return (m.group(1), int(m.group(2) or 0))

# ---------------------------------------------------------------- candidates
# page: (title, [blocks], one-line thematic verdict)
CANDIDATES = {
 'A_baseline': ('The ten-page proposal on the table (regions as its cuts, with the three straddling symbols assigned by pin)', [
    ('Power_Input',     ['S1M_T', 'S1M_B', 'S1R_T', 'S1R_B'], 'battery protection, charger, V_PRIME selection and core LDO, plus the Feather sleep timer: two themes and a stray'),
    ('Power_Rails',     ['S1L_T', 'S1L_B'],                   'the 5V_LP, 3V3_AUX, 5V_AUX regulators and the POWER_EN gate: one theme (5V_LP feeds the other page)'),
    ('Processor',       ['S3UL', 'S3SD'],                     'B-series cellular SoM with its USB, buttons, FRAM, SD card: coherent, but the ATmega1284 is the processor and sits elsewhere'),
    ('IO_Expansion',    ['S6', 'S3LAD'],                      'misnamed: this is the ATmega1284 MCU page, with the MCP23018 and the PCA9634 LED driver'),
    ('Level_Shifters',  ['S4'],                               'one theme'),
    ('Sensors',         ['S5'],                               'one theme (on-board I2C sensors, RTC, DAC, ADC)'),
    ('Sensor_Power',    ['S2L_T', 'S2L_B'],                   'port power switches and the V_HP/V_BETA switches; their XOR gate is on another page'),
    ('Connectors',      ['S3TERM', 'S3MID', 'S3LR_T', 'S3LR_B'], 'a leftover: field terminals, Feather socket, ICSP, battery and solar terminals, log button, status LED'),
    ('USB_Programming', ['S2R_T', 'S2R_B'],                   'USB-C and FT231X, plus the U40 XOR and VDIV jumpers that belong to the power switches'),
 ]),
 'B_corrected': ('Baseline with four blocks re-homed and two pages renamed; cuts unchanged', [
    ('Power_Input',     ['S3LR_T', 'S1M_T', 'S1M_B', 'S1R_T', 'S1R_B'], 'battery and solar terminals join their protection and charger; still carries the selector and the timer'),
    ('Power_Rails',     ['S1L_T', 'S1L_B'],                   'one theme'),
    ('Cell_Module',     ['S3UL', 'S3SD'],                     'B-series SoM and SD card'),
    ('Microcontroller', ['S6', 'S3LAD', 'S3LR_B'],            'ATmega1284, MCP23018, LED driver, status LED and log button: the MCU and what it drives'),
    ('Level_Shifters',  ['S4'],                               'one theme'),
    ('Sensors',         ['S5'],                               'one theme'),
    ('Sensor_Power',    ['S2L_T', 'S2L_B', 'S2R_B'],          'port and rail switches with their enable logic: one theme'),
    ('Connectors',      ['S3TERM', 'S3MID'],                  'field terminals, Feather socket, ICSP: headers'),
    ('USB_Programming', ['S2R_T'],                            'USB-C and FT231X alone: coherent but 173 x 101 mm on a page'),
 ]),
 'C_thematic': ('Signal-path order, every page one function; the Feather timer with the selector column', [
    ('Power_Input',     ['S3LR_T', 'S1M_T', 'S1M_B'],         'battery and solar terminals, start button, BQ2980 protection, LT3652 charger: everything from the terminals to V_LI'),
    ('Power_Select',    ['S1R_T', 'S1R_B'],                   'V_PRIME selection (TLV3691, TPS2105, LTC4412), TPS797 core LDO; the TPL5111 Feather timer rides along'),
    ('Power_Rails',     ['S1L_T', 'S1L_B'],                   '5V_LP, 3V3_AUX, 5V_AUX regulators and POWER_EN'),
    ('Microcontroller', ['S6', 'S3LAD', 'S3LR_B'],            'ATmega1284, MCP23018, PCA9634 ladder, status LED, log button'),
    ('Cell_Module',     ['S3UL', 'S3SD'],                     'B-series SoM, its USB, buttons, FRAM; SD card on the shared buffered SPI'),
    ('Level_Shifters',  ['S4'],                               'one theme'),
    ('Sensors',         ['S5'],                               'one theme'),
    ('Sensor_Ports',    ['S2L_T', 'S2L_B', 'S2R_B', 'S3TERM'], 'the field ports: MIC2544 switched power, V_HP/V_BETA switches and their logic, and the screw terminals they feed'),
    ('USB_ISP',         ['S2R_T', 'S3MID'],                   'Bobby\'s own heading "USB & ISP": USB-C, FT231X, ICSP header, Feather socket, I2C jumper'),
 ]),
 'D_nine': ('C with the selector merged into Power_Input and the Feather timer beside the Feather socket (nine pages)', [
    ('Power_Input',     ['S3LR_T', 'S1M_T', 'S1M_B', 'S1R_T'], 'terminals, protection, charger, V_PRIME selection, core LDO: the whole input chain'),
    ('Power_Rails',     ['S1L_T', 'S1L_B'],                   '5V_LP, 3V3_AUX, 5V_AUX regulators and POWER_EN'),
    ('Microcontroller', ['S6', 'S3LAD', 'S3LR_B'],            'ATmega1284, MCP23018, PCA9634 ladder, status LED, log button'),
    ('Cell_Module',     ['S3UL', 'S3SD'],                     'B-series SoM and SD card'),
    ('Level_Shifters',  ['S4'],                               'one theme'),
    ('Sensors',         ['S5'],                               'one theme'),
    ('Sensor_Ports',    ['S2L_T', 'S2L_B', 'S2R_B', 'S3TERM'], 'switched port power and the screw terminals'),
    ('USB_ISP_Feather', ['S2R_T', 'S3MID', 'S1R_B'],          'USB-C, FT231X, ICSP, Feather socket and the TPL5111 timer that gates FEATHER_BAT'),
 ]),
 'E_core_supply': ('C with the rails column split so the 5V_LP boost sits with the selector that it feeds (no local label split on Okapi_1)', [
    ('Power_Input',     ['S3LR_T', 'S1M_T', 'S1M_B'],         'terminals, start button, protection, charger'),
    ('Core_Supply',     ['S1L_T', 'S1R_T'],                   'MIC94094, TLV61220 5V_LP boost, TLV3691/TPS2105 V_CORE switch, LTC4412 ideal diode, TPS797 LDO: the 3V3_CORE chain'),
    ('Aux_Rails',       ['S1L_B', 'S2L_B', 'S2R_B'],          'TPS6282 3V3_AUX, TPS61032 5V_AUX, POWER_EN gate, and the V_HP/V_BETA TPS22917 switches with their C0/C1 logic'),
    ('Microcontroller', ['S6', 'S3LAD', 'S3LR_B'],            'ATmega1284, MCP23018, PCA9634 ladder, status LED, log button'),
    ('Cell_Module',     ['S3UL', 'S3SD'],                     'B-series SoM and SD card'),
    ('Level_Shifters',  ['S4'],                               'one theme'),
    ('Sensors',         ['S5'],                               'one theme'),
    ('Sensor_Ports',    ['S2L_T', 'S3TERM'],                  'MIC2544 switched port power and the screw terminals'),
    ('USB_ISP_Feather', ['S2R_T', 'S3MID', 'S1R_B'],          'USB-C, FT231X, ICSP, Feather socket and its timer'),
 ]),
 'G_indicators': ('C with an eleventh page for the indicators, so that the MCU page holds the MCU and nothing is a stray', [
    ('Power_Input',     ['S3LR_T', 'S1M_T', 'S1M_B'],         'terminals, start button, protection, charger'),
    ('Power_Select',    ['S1R_T', 'S1R_B'],                   'V_PRIME selection and core LDO; the Feather timer rides along'),
    ('Power_Rails',     ['S1L_T', 'S1L_B'],                   '5V_LP, 3V3_AUX, 5V_AUX regulators and POWER_EN'),
    ('Microcontroller', ['S6'],                               'ATmega1284 and MCP23018, as Okapi_6 is today'),
    ('Indicators',      ['S3LAD', 'S3LR_B'],                  'Bobby\'s heading "Indicators": PCA9634 ladder, D5 status LED, S3 log button; a small page'),
    ('Cell_Module',     ['S3UL', 'S3SD'],                     'B-series SoM and SD card'),
    ('Level_Shifters',  ['S4'],                               'one theme'),
    ('Sensors',         ['S5'],                               'one theme'),
    ('Sensor_Ports',    ['S2L_T', 'S2L_B', 'S2R_B', 'S3TERM'], 'switched port power, rail switches and logic, screw terminals'),
    ('USB_ISP',         ['S2R_T', 'S3MID'],                   'USB-C, FT231X, ICSP, Feather socket, I2C jumper'),
 ]),
 'H_core_indicators': ('E (rails column split) with the Indicators page and the Feather timer beside its socket', [
    ('Power_Input',     ['S3LR_T', 'S1M_T', 'S1M_B'],         'terminals, start button, protection, charger'),
    ('Core_Supply',     ['S1L_T', 'S1R_T'],                   'MIC94094, 5V_LP boost, V_CORE switch, ideal diode, TPS797: the 3V3_CORE chain'),
    ('Aux_Rails',       ['S1L_B', 'S2L_B', 'S2R_B'],          '3V3_AUX, 5V_AUX, POWER_EN, and the V_HP/V_BETA switches with their logic'),
    ('Microcontroller', ['S6'],                               'ATmega1284 and MCP23018'),
    ('Indicators',      ['S3LAD', 'S3LR_B'],                  'PCA9634 ladder, D5 status LED, S3 log button'),
    ('Cell_Module',     ['S3UL', 'S3SD'],                     'B-series SoM and SD card'),
    ('Level_Shifters',  ['S4'],                               'one theme'),
    ('Sensors',         ['S5'],                               'one theme'),
    ('Sensor_Ports',    ['S2L_T', 'S3TERM'],                  'MIC2544 switched port power and the screw terminals'),
    ('USB_ISP_Feather', ['S2R_T', 'S3MID', 'S1R_B'],          'USB-C, FT231X, ICSP, Feather socket and its timer'),
 ]),
 'C2_stray_on_usb': ('C with the MCU page as the baseline has it (MCU + ladder) and the status LED and log button on the USB/ISP page', [
    ('Power_Input',     ['S3LR_T', 'S1M_T', 'S1M_B'],         'terminals, start button, protection, charger'),
    ('Power_Select',    ['S1R_T', 'S1R_B'],                   'V_PRIME selection and core LDO; the Feather timer rides along'),
    ('Power_Rails',     ['S1L_T', 'S1L_B'],                   '5V_LP, 3V3_AUX, 5V_AUX regulators and POWER_EN'),
    ('Microcontroller', ['S6', 'S3LAD'],                      'ATmega1284, MCP23018, PCA9634 ladder'),
    ('Cell_Module',     ['S3UL', 'S3SD'],                     'B-series SoM and SD card'),
    ('Level_Shifters',  ['S4'],                               'one theme'),
    ('Sensors',         ['S5'],                               'one theme'),
    ('Sensor_Ports',    ['S2L_T', 'S2L_B', 'S2R_B', 'S3TERM'], 'switched port power, rail switches and logic, screw terminals'),
    ('USB_ISP',         ['S2R_T', 'S3MID', 'S3LR_B'],         'USB-C, FT231X, ICSP, Feather socket, and a stray status LED and log button'),
 ]),
 'I_nine_fit': ('D with the ladder on the MCU page and the status LED and log button beside the Feather socket: the nine-page layout that fits', [
    ('Power_Input',     ['S3LR_T', 'S1M_T', 'S1M_B', 'S1R_T'], 'terminals, protection, charger, V_PRIME selection, core LDO: the whole input chain'),
    ('Power_Rails',     ['S1L_T', 'S1L_B'],                   '5V_LP, 3V3_AUX, 5V_AUX regulators and POWER_EN'),
    ('Microcontroller', ['S6', 'S3LAD'],                      'ATmega1284, MCP23018, PCA9634 ladder'),
    ('Cell_Module',     ['S3UL', 'S3SD'],                     'B-series SoM and SD card'),
    ('Level_Shifters',  ['S4'],                               'one theme'),
    ('Sensors',         ['S5'],                               'one theme'),
    ('Sensor_Ports',    ['S2L_T', 'S2L_B', 'S2R_B', 'S3TERM'], 'switched port power, rail switches and logic, screw terminals'),
    ('USB_ISP_Feather', ['S2R_T', 'S3MID', 'S1R_B', 'S3LR_B'], 'USB-C, FT231X, ICSP, Feather socket and timer, plus a stray status LED and log button'),
 ]),
 'J_ten_indicators': ('D with an Indicators page: ten pages, every block on a page named for what it does', [
    ('Power_Input',     ['S3LR_T', 'S1M_T', 'S1M_B', 'S1R_T'], 'terminals, start button, BQ2980 protection, LT3652 charger, V_PRIME selection, TPS797 core LDO'),
    ('Power_Rails',     ['S1L_T', 'S1L_B'],                   '5V_LP, 3V3_AUX, 5V_AUX regulators and POWER_EN'),
    ('Microcontroller', ['S6'],                               'ATmega1284 and MCP23018'),
    ('Indicators',      ['S3LAD', 'S3LR_B'],                  'PCA9634 ladder, D5 status LED, S3 log button'),
    ('Cell_Module',     ['S3UL', 'S3SD'],                     'B-series SoM, its USB, buttons, FRAM; SD card'),
    ('Level_Shifters',  ['S4'],                               'one theme'),
    ('Sensors',         ['S5'],                               'one theme'),
    ('Sensor_Ports',    ['S2L_T', 'S2L_B', 'S2R_B', 'S3TERM'], 'switched port power, rail switches and logic, screw terminals'),
    ('USB_ISP_Feather', ['S2R_T', 'S3MID', 'S1R_B'],          'USB-C, FT231X, ICSP, Feather socket and the timer that gates FEATHER_BAT'),
 ]),
 'F_eight': ('Fewest pages tried: E with Aux_Rails pushed into Sensor_Ports and the ladder moved to the Cell_Module page', [
    ('Power_Input',     ['S3LR_T', 'S1M_T', 'S1M_B'],         'terminals, start button, protection, charger'),
    ('Core_Supply',     ['S1L_T', 'S1R_T'],                   'the 3V3_CORE chain'),
    ('Microcontroller', ['S6', 'S3LR_B'],                     'ATmega1284, MCP23018, status LED, log button'),
    ('Cell_Module',     ['S3UL', 'S3SD', 'S3LAD'],            'B-series SoM, SD card, and a PCA9634 ladder that has nothing to do with it'),
    ('Level_Shifters',  ['S4'],                               'one theme'),
    ('Sensors',         ['S5'],                               'one theme'),
    ('Rails_and_Ports', ['S1L_B', 'S2L_T', 'S2L_B', 'S2R_B', 'S3TERM'], 'aux regulators, every power switch, and the terminals: too much'),
    ('USB_ISP_Feather', ['S2R_T', 'S3MID', 'S1R_B'],          'USB-C, FT231X, ICSP, Feather socket and its timer'),
 ]),
}

def main():
    reg = json.load(open(sys.argv[1]))
    ink = json.load(open(sys.argv[2]))
    netd = json.load(open(sys.argv[3]))
    nets, rails = netd['nets'], set(netd['rails'])
    want = sys.argv[4:] or list(CANDIDATES)
    syms, pos = reg['syms'], reg['sym_pos']
    by_region = {}
    for ref, r in syms.items():
        by_region.setdefault(r, []).append(ref)
    summary = []
    for cname in want:
        desc, pages = CANDIDATES[cname]
        print(f'\n### {cname}\n\n{desc}. Page 1 is the root sheet (178 x 80 mm) in every candidate.\n')
        print('| # | Page | Blocks | Parts | Ink, packed (mm) | Fit | Local labels split | Nets out all / signal | Verdict |')
        print('|---|---|---|---|---|---|---|---|---|')
        page_of = {}
        for i, (title, blocks, verdict) in enumerate(pages, start=2):
            for b in blocks:
                page_of[b] = title
        unplaced = sorted(set(syms.values()) - set(page_of))
        if unplaced:
            print('UNPLACED REGIONS', unplaced, file=sys.stderr)
            raise SystemExit(1)
        nets_pages = {n: sorted({page_of[r] for r in v['regions']}) for n, v in nets.items()}
        split_labels = {}
        for lab, inst in reg['labels'].items():
            pg = {page_of[x[0]] for x in inst}
            if len(pg) > 1:
                split_labels[lab] = sorted(pg)
        tot_all = sum(1 for n, p in nets_pages.items() if len(p) > 1)
        tot_sig = sum(1 for n, p in nets_pages.items() if len(p) > 1 and n not in rails)
        rows = []
        nofit = 0
        for i, (title, blocks, verdict) in enumerate(pages, start=2):
            refs = sorted((r for b in blocks for r in by_region.get(b, []) if not r.startswith('#')), key=natural)
            ics = [r for r in refs if not r[0] in 'RC' or r.startswith('RTC')]
            nR = sum(1 for r in refs if r[0] == 'R' and not r.startswith('RTC'))
            nC = sum(1 for r in refs if r[0] == 'C')
            parts = ' '.join(ics) + f' + {nR} R, {nC} C'
            bl = [(b, ink[b]['w'], ink[b]['h']) for b in blocks]
            if len(blocks) == 1 and blocks[0] in ('S4', 'S5', 'S6'):
                bl = [(blocks[0], ink['sheet:Okapi_' + blocks[0][1]]['w'], ink['sheet:Okapi_' + blocks[0][1]]['h'])]
            p = pack(bl)
            if p:
                W, H, placed = p
                fit = 'yes'
                size = f'{W:.0f} x {H:.0f}, slack {PAGE_W - W:.0f} x {PAGE_H - H:.0f}'
                if len(blocks) > 1:
                    size += ' (' + '; '.join(f'{n} at {x:.0f},{y:.0f}' for n, x, y, w, h in placed) + ')'
            else:
                nofit += 1
                fit = 'NO'
                rw = sum(w for _, w, h in bl) + GAP * (len(bl) - 1)
                ch = sum(h for _, w, h in bl) + GAP * (len(bl) - 1)
                size = f'row {rw:.0f} x {max(h for _, w, h in bl):.0f}, column {max(w for _, w, h in bl):.0f} x {ch:.0f}'
            out_all = [n for n, pg in nets_pages.items() if title in pg and len(pg) > 1]
            out_sig = [n for n in out_all if n not in rails]
            labs = [l.split('@')[0] for l, pg in split_labels.items() if title in pg]
            rows.append(dict(title=title, blocks=blocks, out_sig=out_sig))
            print(f'| {i} | {title} | {" ".join(blocks)} | {parts} | {size} | {fit} | {", ".join(labs) or "–"} | {len(out_all)} / {len(out_sig)} | {verdict} |')
        print(f'\nTotals: {len(pages) + 1} pages; nets spanning two or more pages {tot_all} (all) / {tot_sig} (signal); '
              f'local labels split {len(split_labels)} ({", ".join(sorted(split_labels)) or "none"}); pages that do not fit {nofit}; wires cut 0 (every block boundary is wire-clean and pin-clean by pages_regions.py).')
        summary.append((cname, len(pages) + 1, tot_all, tot_sig, len(split_labels), nofit))
        if '--nets' in sys.argv or True:
            for r in rows:
                print(f'  - {r["title"]} signal nets out: {", ".join(sorted(r["out_sig"])) or "none"}')
    print('\n### Comparison\n')
    print('| Candidate | Pages | Spanning nets, all | Spanning nets, signal | Local labels split | Pages that do not fit |')
    print('|---|---|---|---|---|---|')
    for c, np_, a, s, l, f in summary:
        print(f'| {c} | {np_} | {a} | {s} | {l} | {f} |')

if __name__ == '__main__':
    main()

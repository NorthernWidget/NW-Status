STATUS: COMPLETE

# Margay: placed symbols moved from Margay-eagle-import onto nw-cold-silicon

Started 2026-11-03. Same program as Okapi (Project-Okapi 11776ab, f5ae35d, d8d6c7e;
nw-cold-silicon 3b2d109). Every number below is pasted from the command above it.
Project: Project-Margay/Hardware/KiCAD (root Margay.kicad_sch; sheets Margay_1,
Margay_2, Margay_3). Tools: NW-Tests/kicad.

## Placed symbols at the start (git: Project-Margay 00cdab0)

```
grep -o '(lib_id "[^:]*:[^"]*"' Project-Margay/Hardware/KiCAD/*.kicad_sch | sed 's/.*lib_id //' | sort | uniq -c | sort -rn
```
         26 "Margay-eagle-import:GND"
         22 "Margay-eagle-import:R-EU_R0402"
         15 "Margay-eagle-import:C-EUC0402"
          8 "Margay-eagle-import:SparkFun-PowerSymbols_GND"
          6 "Margay-eagle-import:FRAME_A_L"
          4 "Margay-eagle-import:R-EU_R0603"
          3 "Margay-eagle-import:C-EUC0603"
          2 "Margay-eagle-import:MOUNTING_HOLE4_NP_CLOSE"
          2 "Margay-eagle-import:DIODESOD-323"
          2 "Margay-eagle-import:CLVBA-FKA"
          2 "Margay-eagle-import:C-EUC0805"
          2 "Margay-eagle-import:BUTTON4.2X3.2"
          1 "nw-cold-silicon:NWLOGO_MED"
          1 "Margay-eagle-import:VDIV_MARGAYFULL-VDIV"
          1 "Margay-eagle-import:USB_C"
          1 "Margay-eagle-import:TPS7A05DBV"
          1 "Margay-eagle-import:TPS797"
          1 "Margay-eagle-import:TPS22916YFP"
          1 "Margay-eagle-import:TPS210"
          1 "Margay-eagle-import:TPL5010DDC"
          1 "Margay-eagle-import:TLV3691DPF"
          1 "Margay-eagle-import:SN74LVC1G3157SC70"
          1 "Margay-eagle-import:SN74AUP3G34DCU"
          1 "Margay-eagle-import:SDMMCWR-CRD"
          1 "Margay-eagle-import:MOSFET_PCH-FDN360P"
          1 "Margay-eagle-import:MOSFET-NCH-DMG3404L"
          1 "Margay-eagle-import:MOSFET-NCH-2N7002PW"
          1 "Margay-eagle-import:MIC9409C6"
          1 "Margay-eagle-import:MCP342"
          1 "Margay-eagle-import:MAX6070AAUT"
          1 "Margay-eagle-import:JUMPER-SMT_3_1-NC_PASTE_SILK"
          1 "Margay-eagle-import:JUMPER-SMT_2_NO_SILK"
          1 "Margay-eagle-import:JUMPER-SMT_2_NC_PASTE_SILK"
          1 "Margay-eagle-import:FT231X-Q"
          1 "Margay-eagle-import:DS3231M"
          1 "Margay-eagle-import:CRYSTAL5X3.2"
          1 "Margay-eagle-import:CONN_6SCREW_2.54"
          1 "Margay-eagle-import:CONN_102.54_SCREW"
          1 "Margay-eagle-import:BME280"
          1 "Margay-eagle-import:BATTERY_COIN12MM"
          1 "Margay-eagle-import:AVRISP-6"
          1 "Margay-eagle-import:ATMEGA1284M"

123 placed symbols name Margay-eagle-import (Margay_1 44, Margay_2 26, Margay_3 53; root 0), 1 names nw-cold-silicon (LOGO1).

## Baselines (Project-Margay 00cdab0, measured 2026-11-03, NW-Tests/kicad)

```
./check_conversion.sh $M/Margay.kicad_sch ../../Project-Margay/Hardware/Margay.sch 'LOGO1'
== Eagle nets: 75  exactly reproduced in one KiCad net: 72  with differences: 3
KiCad unconnected but Eagle connected: []
./erc_counts.sh $M/Margay.kicad_sch erc.json
unconnected_wire_endpoint 8  endpoint_off_grid 12  total 76
./roundtrip.sh $M/Margay.kicad_sch
Margay.kicad_sch Margay_1 Margay_2 Margay_3: identical (exit 0)
./roundtrip_pcb.sh $M/Margay.kicad_pcb
Margay.kicad_pcb  identical
```

ERC tally at the start (erc.json from the command above):
```
24 unresolved_variable
16 pin_not_connected
12 endpoint_off_grid
10 power_pin_not_driven
8 unconnected_wire_endpoint
3 isolated_pin_label
2 lib_symbol_mismatch   (JUMPER-SMT_2_NO_SILK, JUMPER-SMT_2_NC_PASTE_SILK "doesn't match copy in library Margay-eagle-import")
1 pin_to_pin
```
Netlist baseline: `kicad-cli sch export netlist --format kicadxml` + `kicad_nets.py`:
`KiCad netlist: comps 84 nets 91 nodes 323`; net GND has 70 nodes.

## The map (symbol_map.py, Project-Margay 00cdab0)

```
python3 symbol_map.py $M/Margay.kicad_sch ../../nw-cold-silicon/nw-cold-silicon.kicad_sym Margay-eagle-import --strip bschulz_passives_,bschulz_,awickert_,SparkFun-Jumpers_,supply1_371_,supply2_372_
placed from Margay-eagle-import: 123 {'same pins and geometry': 80, 'same numbers and geometry, names differ': 2, 'power symbol': 40, 'no library symbol': 1}
== names differ
   FT231X-Q (GND@13, GND@3, GND@21 -> GND); ATMEGA1284M (VCC@1, VCC@2 -> VCC; GND@1, GND@2 -> GND)
== no library symbol
   SDMMCWR-CRD (1; embedded in Margay_1 only, not in Margay-eagle-import.kicad_sym: a lift from the sheet)
== power symbol (classed by the # reference)
   GND 26, SparkFun-PowerSymbols_GND 8, FRAME_A_L 6 (the Eagle page frame, two units, not a power symbol)
```

Power-symbol geometry, every sheet's embedded definition against the library's GND
(getsym.py dump of each): GND and SparkFun-PowerSymbols_GND on Margay_1, _2, _3 all
have `(pin power_in line (at 0 2.54 270) (length 2.54))`, the same as the library's GND.
Every placed GND and SparkFun-PowerSymbols_GND instance already carries Value "GND"
(40 instances listed; net GND 70 nodes). No rewire is needed for the rails.
SparkFun-PowerSymbols_GND maps onto the library's GND with the strip prefix
`SparkFun-PowerSymbols_`.

FRAME_A_L: the library's unit 1 (the border) draws the same as the embedded one
(diff is polyline order only; rendered Margay_1 before/after a trial swap on a
scratch copy, identical border). The library's unit 2 (the title block) lacks the
eight `${...}` text placeholders of the import's (${CURRENT_DATE}, ${PROJECTNAME},
${PROJECT}, ${DESIGNER}, ${#}/${##}, ${REV}): 8 texts x 3 unit-2 instances = the 24
ERC unresolved_variable warnings. A swap removes those 24 warnings and the title
block's printed "Project: Margay / Designer: Bobby Schulz / TITLE: Margay / REV 2.2 /
Date / Sheet 4/4" with them (the values stay as the instances' hidden DESIGNER,
PROJECT, REV properties). DECISION: swap in batch B (so the import library can
retire) and flag for Andy: the KiCad-native place for those values is each sheet's
title_block, which is empty; proposal, not done.

## Batch A: 82 placed symbols, 37 names (Project-Margay fc9e682)

swap_symbols.py per sheet with --only the 37 library names (identical + names-differ):
Margay_1 27 (10 names), Margay_2 19 (11 names), Margay_3 36 (22 names); then
kicad-cli sch upgrade --force on all four sheets. Diff outside lib_symbols: lib_id
lines only (54, 38, 72). Checks (check_all.sh A):
```
== Eagle nets: 75  exactly reproduced in one KiCad net: 72  with differences: 3
KiCad unconnected but Eagle connected: []
unconnected_wire_endpoint 8  endpoint_off_grid 12  total 68
   tally: unresolved_variable=18 pin_not_connected=16 endpoint_off_grid=12 power_pin_not_driven=10 unconnected_wire_endpoint=8 isolated_pin_label=3 pin_to_pin=1
roundtrip: Margay, Margay_1, Margay_2, Margay_3 identical; board identical
KiCad netlist: comps 84 nets 91 nodes 323; (ref,pin) sets per net identical: True
pin names changed: U1 17/38 VCC@n->VCC, U1 18/28/39 GND@n->GND, U2 3/13/EP GND@n->GND
lib_ids: 41 Margay-eagle-import, 83 nw-cold-silicon
```
ERC 76 -> 68: ${DISP} texts 1 (Margay_2) + 5 (Margay_3) -> 0; lib_symbol_mismatch 2 -> 0.

## Library: SDMMCWR-CRD lifted (nw-cold-silicon 775096a, 668ce0d)

The first `python3 tools/build.py` raised FileNotFoundError on
Project-Okapi/Hardware/KiCAD-10import/Okapi-eagle-import.kicad_sym: the file left
Project-Okapi at f5ae35d (`git log --oneline -- <file>`: f5ae35d, 74f8c91, 6b6530f;
`git cat-file -e f5ae35d:<file>` false) and SCHEMATIC_LIFT/POWER_LIFT read it from the
working tree, so the library has not been buildable since Okapi's batch B. At 11776ab
the file holds GND and the six parts and the sheets embed 3V3_AUX and 3V3_CORE
(counted per name with git show). Fix (775096a): a lift source is `Repo@commit:path`,
read with `git show`; the embedded fallback reads the sheets at that commit with
`git ls-tree`. Okapi pinned at 11776ab, Margay at fc9e682 (Margay_1 there still
embeds SDMMCWR-CRD). SDMMCWR-CRD: Eagle part J1 library="bschulz" deviceset="SDMMC"
device="WR-CRD"; the committed Cold-Silicon/bschulz.lbr SDMMC deviceset has devices
SCDA, 18650, 06132 only (library symbols SDMMC06132, SDMMC18650, SDMMCSCDA exist).
```
python3 tools/build.py   (1m43s each run)
847 footprints, 1402 symbols; second pass: 0 fp changed, sym identical; collisions 1764
git diff nw-cold-silicon.kicad_sym: removed lines 0, added 414; symbols added: SDMMCWR-CRD
PROVENANCE.md: 1401 -> 1402 symbols
kicad-cli sym upgrade --force on a copy: upgrade diff lines: 0
```

## Batch B: 41 placed symbols (Project-Margay f4ecd20)

swap_symbols.py per sheet, --only GND,FRAME_A_L,SDMMCWR-CRD with SparkFun-PowerSymbols_
added to --strip: Margay_1 17 (4 names), Margay_2 7 (3 names), Margay_3 17 (3 names).
Diff outside lib_symbols: lib_id lines only (34, 14, 34). Placed Value "GND" count
37 = 34 instances + 3 library copies. No rewire: every GND variant's pin at (0, 2.54),
as the library's. Checks (check_all.sh B):
```
== Eagle nets: 75  exactly reproduced in one KiCad net: 72  with differences: 3
KiCad unconnected but Eagle connected: []
unconnected_wire_endpoint 8  endpoint_off_grid 12  total 50
   tally: pin_not_connected=16 endpoint_off_grid=12 power_pin_not_driven=10 unconnected_wire_endpoint=8 isolated_pin_label=3 pin_to_pin=1
roundtrip: all four sheets identical; board identical
KiCad netlist: comps 84 nets 91 nodes 323; (ref,pin) sets per net identical: True
lib_ids: 124 nw-cold-silicon, 0 Margay-eagle-import; embedded Margay-eagle-import definitions left: 0
```
ERC 68 -> 50: the 18 unresolved_variable warnings were the frames' title-block texts.
FLAGGED for Andy: the pages no longer print Project/Designer/TITLE/REV/Date/Sheet in the
Eagle frame; the values survive as the frames' hidden DESIGNER, PROJECT, REV properties
(e.g. "Bobby Schulz", "Margay", "2.2"); each sheet's KiCad title_block is empty and is the
native place for them. Proposal, not done.

## Retirement (Project-Margay efb5fae, 86c2bff)

efb5fae: Margay-eagle-import line out of sym-lib-table, `git rm` of the .kicad_sym
(no embedded definition remained, swap_symbols pruned them as it went), README sentence
reframed. check_all.sh R: same numbers as batch B. 86c2bff: `grep -c '"Margay:'
Hardware/KiCAD/*` is 0 in every file and fp-lib-table had no Margay line, so the 37
files of Margay.pretty removed; board identical, DRC unchanged (below).

## Final (Project-Margay 86c2bff; nw-cold-silicon 668ce0d)

```
check_all.sh F: Eagle nets 75, exact 72, differences 3; KiCad unconnected but Eagle connected: []
ERC: unconnected_wire_endpoint 8  endpoint_off_grid 12  total 50
   tally: pin_not_connected=16 endpoint_off_grid=12 power_pin_not_driven=10 unconnected_wire_endpoint=8 isolated_pin_label=3 pin_to_pin=1
roundtrip: Margay, Margay_1, Margay_2, Margay_3 identical; roundtrip_pcb: Margay.kicad_pcb identical
kicad-cli pcb drc --severity-all --schematic-parity: violations 399 unconnected_items 3 schematic_parity 4
   parity: MPN R7, R9 (RC0603FR-07330RL vs RC0402FR-071KL), MPN R23 (CRT0603-BY-1002ELF vs ...ELFCT), DIGIKEY U13 (MAX6070AAUT18+TCT-ND vs MAX6070BAUT18+...)  = Project-Margay#62
   top types: silk_over_copper 199, text_height 75, text_thickness 67, silk_overlap 34, silk_edge_clearance 11, hole_clearance 4, track_dangling 4, clearance 2
kicad-cli sch export netlist: components 84 nets 91 libraries ['nw-cold-silicon'] libparts 39 from ['nw-cold-silicon']
kicad-cli sch export bom: 83 rows (excluding header)
kicad-cli sch export pdf: Pages 4
```

| check | before (00cdab0) | after (86c2bff) |
|---|---|---|
| Eagle nets exact / total / differences | 72 / 75 / 3 | 72 / 75 / 3 |
| KiCad unconnected but Eagle connected | [] | [] |
| ERC total | 76 | 50 |
| ERC unconnected_wire_endpoint / endpoint_off_grid | 8 / 12 | 8 / 12 |
| ERC unresolved_variable / lib_symbol_mismatch | 24 / 2 | 0 / 0 |
| round trip, 4 sheets | identical | identical |
| round trip, board | identical | identical |
| netlist comps / nets / nodes | 84 / 91 / 323 | 84 / 91 / 323 (pin sets per net identical) |
| placed symbols on Margay-eagle-import / nw-cold-silicon | 123 / 1 | 0 / 124 |
| DRC violations / unconnected / parity | 399 / 3 / 4 | 399 / 3 / 4 |
| BOM rows | – | 83 |
| PDF pages | – | 4 |

Commits: Project-Margay fc9e682 (batch A, 82), f4ecd20 (batch B, 41), efb5fae (symbol
library retired), 86c2bff (Margay.pretty retired); nw-cold-silicon 775096a (lift sources
are git objects), 668ce0d (SDMMCWR-CRD lifted).

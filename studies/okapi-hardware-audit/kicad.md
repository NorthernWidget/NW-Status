STATUS: COMPLETE

# Okapi Eagle-to-KiCad conversion audit

Started 2026-10-30. Question: is `Project-Okapi/Hardware/KiCAD-10import/` a sound base for the
open hardware issues, now that Eagle 9.6.2 no longer runs here?

Tooling: `kicad-cli` 10.0.7 at `/usr/bin/kicad-cli` (also `/usr/bin/kicad`). Scratch directory:
`/tmp/claude-1000/-home-awickert-Dropbox-NorthernWidget-github/cf0342fa-36e3-4818-be1e-2b4b31cc1756/scratchpad/kicad/`.

Eagle originals last changed in commit b4032d4 (2024-11-02, "v1.0 updates"). KiCad import files
dated 2026-06-03 (schematic sheets edited 06:34–06:56 after the 06:15 import), project file
2026-06-18. Three commits: 6b6530f, faaf72e, fb54477. `Okapi.kicad_dru` holds only `(version 1)`
(11 bytes): no custom rules.

## 1. Inventory

Method: Python `xml.etree` over `Okapi.sch` (parts, library `connects` to map gate+pin to pad,
`pinref`s on all sheets); `kicad-cli sch export netlist --format kicadxml` for KiCad, plus regex
counts over the six `.kicad_sch` files.

| | Eagle `Okapi.sch` | KiCad (6 sheets) |
|---|---|---|
| Sheets | 6 | 6 (root + Okapi_2..6) |
| Parts (refdes) | 376, of which 246 have pads; 130 are supply symbols (105 GND, 9 SUPPLY, 11 P+), 3 holes H, 2 logos U$ | 376 symbol instances; 251 in the netlist (the 246 real parts + H1–H3, U$1, U$2) |
| Nets | 209 (82 anonymous `N$`) | 335 in the netlist: 214 real nets (87 anonymous `Net-(…)`) + 121 single-pin `unconnected-(…)` |
| Pin connections | 1048 pinrefs; 993 connected pads | 1043 nodes, 922 on real nets + 121 unconnected |
| Symbol pins (all) | 1168 (incl. supply symbols) | 1168 across sheets |
| Labels | – | 43 local, 325 global, 0 hierarchical, 7 no-connect flags (all on Okapi_3) |

Refdes present in one and not the other: none among parts with pads. KiCad's netlist carries
H1–H3, U$1 and U$2 (mounting holes and logos; pad-less in Eagle) as components.

Net-name normalization: KiCad local labels carry a sheet prefix (`/Okapi_2/D+`), stripped; KiCad
overbar `~{RST}` mapped to Eagle `!RST`; Eagle `N$nn` and KiCad `Net-(…)`/`unconnected-(…)`
matched by pin content, not by name. After normalization, every named Eagle net exists in KiCad and
vice versa (0 missing either way). Note that 24 Eagle-global nets became *local* labels in KiCad
(5V_LP, MPPT_SHDN, MPPT_VIN_REG, V_CORE, V_CORE_SW, 3V3_FTDI, CC1, CC2, D+, D-, SBU1, SBU2, VUSB,
BLUE, GREEN, RED, BSOM_VUSB, PD+, PD-, RST_TRIG, !MODE, !RST, SENSOR_INT, GLOBAL_INT); none of
them is used on more than one sheet, so no connectivity is lost by that today, but any future edit
that reuses one of those names on another sheet will silently not connect.

## 2. Connectivity

Method: KiCad netlist (kicad-cli, i.e. KiCad's own connectivity engine) against Eagle pinrefs,
compared as sets of (refdes, pad). Eagle pins that map to several pads (`connect pad="3 7 10"`)
were split to one entry per pad.

**168 of 209 Eagle nets are reproduced exactly** (same pins, one KiCad net). The 41 others:

*(a) Nets split into pieces (real connectivity loss between parts that stay connected to something):*

| Eagle net | KiCad pieces |
|---|---|
| 3V3_CORE (45 pins) | 3V3_CORE 33 + `Net-(R53-Pad2)` 8 + four unconnected (U45-20, U45-3, R18-2, U35-8) |
| GND (216 pins) | GND 202 + `Net-(J9-GND@3)` 6 + eight unconnected (J9-15/49/56/76, MS1-4, U45-19/14, J2-10) |
| FEATHER_BAT (7) | `Net-(J9-VCC@2)` 4 + FEATHER_BAT 2 + MS1-28 unconnected; and U21-5, U22-5 **added** (not in Eagle's net; Eagle has them unconnected) |
| LOG_INT (4) | `Net-(S3-3)` 3 + LOG_INT 1 |
| V_PRIME_SENSE (3) | `Net-(J5-2)` 2 + V_PRIME_SENSE 1 |

*(b) Nets merged:* Eagle N$59 (D5 pin 1, R44 pin 2) and N$60 (D5 pin 4, R43 pin 2) are one KiCad
net `Net-(D5-GREEN_CATH)`; at the same time R44-1 (LED1) and R42-1 (LED2) are unconnected. The
D5 RGB-LED/R42–R44 region is wrong in KiCad.

*(c) Pins connected in Eagle and dangling in KiCad (54 pins, 34 nets):* F2-2 (5V_AUX), ISP1-5
(RST), Q4-3 (RST), J1-2/5/7, J2-3/6/7/10, J4-2/3/4/7/8 (the sensor-bus connectors), J6-P1/P2,
J7-P2, J8-1 (battery and solar inputs: LI+, LI-, V_SOLAR), J9-15/22/36/49/50/52/56/76 (B-Series
socket: GND, SDA, TX, MISO, MOSI), MS1-4/8/10/11/12/14/15/18/19/20/26/28 (Feather socket: GND,
WD_DONE, GPIO, SCK, MOSI, RX, TX, SCL, 5V_AUX, VBAT), R18-2, R41-2, R42-1, R44-1, R73-2, R86-2,
SD1-4 (3V3_AUX), U35-5/6/8 (SDA_OB, SCL, VDD), U45-3/14/17/19/20 (PCA9634 address pins and SDA).

*(d) Pins unconnected in Eagle and connected in KiCad:* U21-5, U22-5 (into FEATHER_BAT), USB2
P$1–P$6 (shell pads, into their own net).

In total: 922 KiCad pin-on-net nodes against 993 Eagle connected pads; 54 connections lost, 8
gained, 5 nets fragmented, 2 merged.

**Where the damage came from (verified by exporting the netlist at each commit):**

| Commit | Nets exact / 209 | Lost connections | Notes |
|---|---|---|---|
| 6b6530f (raw import) | 205 | 0 | 15 pins mislabeled `VCC` (importer gives every P+/SUPPLY symbol the net VCC); D5 merge |
| faaf72e (power-net fix) | 206 | 0 | VCC fixed correctly; adds V_CORE label; only D5 merge and the U21/U22 `QOD` gain remain |
| fb54477 (no-connect) | 168 | 54 | deleted 62 global labels from Okapi_3, of which only SIM_VCC and UB_VBUS were stray; the other 60 (GND ×9, 3V3_CORE ×5, SDA_OB, RX, RST, MOSI_BUF, MISO, LI-, FEATHER_BAT, 5V_AUX, 3V3_AUX ×2 each, and 38 singles) carried real connections |

The Eagle board itself holds J9-67
on SIM_VCC and J9-74 on UB_VBUS, and U21-5/U22-5 on a board-only net `QOD` (two unrouted airwires
in Eagle: V_SOLAR_IN and QOD), so the Eagle schematic and board were themselves out of step on those
four pads.

**D5 merge (b), mechanism:** in Eagle, the N$59 wire runs from the RED_CATH pin end (198.12, 40.64)
to the GREEN_CATH pin end, and N$60 begins at that same RED point; Eagle stores net membership
explicitly and kept them apart, KiCad connects by geometry and joins them. The Eagle board's pad nets confirm the intended wiring (D5-4 with R43-2; D5-1 with R44-2).

**Board as the reference:** the KiCad PCB's 972 pad-net assignments equal the Eagle board's 972
one for one (only `!X` → `~{X}` spelling differs), and the Eagle board agrees with the Eagle
schematic on all 968 pads the schematic connects. The PCB, not the KiCad schematic, is currently
the trustworthy copy of the connectivity.

## 3. Symbols and footprints

All 376 symbol instances come from the single generated library `Okapi-eagle-import` (468 symbols,
5 of them power symbols); no KiCad standard-library part is used. Two power symbols (3V3_AUX,
3V3_CORE) exist only embedded in the sheets, not in the library (ERC `lib_symbol_issues` ×13).

Pin numbers and names survived. Checked by comparing every (pin name, pad number) pair from the
Eagle library `connects` with the KiCad library symbol: U4 LT3652 (13/13), U6 TPS2105 (5/5), U32
PAC1934 (17/17 incl. EP), U41 MCP23018 (25/25), U45 PCA9634 (21/21), IC1 ATmega1284P (45/45), J9
B-Series M.2 (70/70). The only differences are Eagle `!NAME` rendered as KiCad `~{NAME}`.

Footprints: 251 schematic symbols ↔ 252 PCB footprints; the extra is `U$4` (NWLOGO_MED, a logo
with no schematic symbol). Every symbol's Footprint field reads `Okapi:<name>`, but there is no
`fp-lib-table` and no `Okapi.pretty` anywhere: the footprints exist only embedded in
`Okapi.kicad_pcb` (ERC `footprint_link_issues` ×251). Eight jumpers (JP1–JP8) carry a `_528`
suffix on the board and not in the schematic. No footprint carries a `(path …)` link to its symbol,
so the DRC parity check reports 172 "extra footprints" and 90 mismatches that are link failures,
not wrong parts: a first "Update PCB from Schematic" must use re-link by reference.

## 4. Board

| Object | Eagle `Okapi.brd` | KiCad `Okapi.kicad_pcb` |
|---|---|---|
| Elements / footprints | 252 (244 top, 8 bottom) | 252 (244 F.Cu, 8 B.Cu) |
| Signal wires / track segments | 2797 Top + 1100 Bottom | 2797 F.Cu + 1100 B.Cu (0 arcs) |
| Vias | 345 | 345 |
| Polygons / zones | 16 (net-bound, 14 Top, 2 Bottom) | 16, same nets and layers, **unfilled** |
| bRestrict polygons | 2 | 0 (not carried; no keepout zone) |
| Dimension (20) wires | 12 | Edge.Cuts: 6 lines + 6 arcs |
| tDocu (51) wires / texts | 32 / 18 | F.Fab: 16 lines + 16 arcs / 18 texts |
| bDocu (52) wires / texts | 6 / 60 | B.Fab: 2 lines + 4 arcs / 60 texts |
| tNames (25) texts | 2 | F.SilkS: 2 |
| Pads with a net | 972 contactrefs | 972 |
| Unrouted airwires | 2 (V_SOLAR_IN, QOD) | 1 after refill (QOD) |

Layer mapping is the expected one: tPlace → F.SilkS (813 lines, 291 polygons, 42 circles inside
footprints), tDocu → F.Fab, Dimension → Edge.Cuts, tKeepout → F.CrtYd (548 lines), tGlue →
F.Adhes, tCream → F.Paste. The 2 bRestrict polygons are the one loss.

Design rules: Eagle used the `jlcpcb-2layer` set (5 mil wire-wire, 6 mil pad-via, 5 mil width,
0.2 mm drill). `Okapi.kicad_dru` is empty (`(version 1)`). The project file carries
min_clearance 0.127 and min_track_width 0.1524 in board setup but the Default netclass keeps
KiCad's 0.2 mm clearance, and the board has no stackup.

DRC as committed (zones unfilled, 0.2 mm netclass): 1296 violations – 499 clearance (every one
between 0.127 and 0.2 mm), 199 each of silk-over-copper, text height and text thickness, 125 silk
overlap, 20 hole clearance, 18 mask bridge, 9 shorting items, 9 annular width, 8 silk-edge, 6
dangling vias, 3 dangling tracks, 2 hole-to-hole; plus 18 unconnected items and 361 parity items.
On a scratch copy with zones refilled and the netclass clearance set to 0.127 mm: 796 violations,
of which the errors are 18 mask bridge, 16 hole clearance, 9 clearance, 9 shorting, 9 annular
width; 1 unconnected item (QOD). Every clearance, shorting and mask-bridge error is inside the
USB2 footprint (its six `P$n` shell pads overlap each other and their own copper, with no net),
the hole-clearance errors are USB2 plus the J10 USB-C NPTH posts, and the annular-width errors are
the nine thermal vias under U3's PAD. These are footprint questions, not conversion damage. The 597 text warnings are the Eagle 0.5–0.7 mm silk text against KiCad's 0.8 mm default.

## 5. ERC

622 violations at HEAD against 483 at the raw import. Errors: pin_not_connected 115 (66 at
import; the increase is the fb54477 damage, concentrated on J9 ×32 and MS1 ×24), power_pin_not_driven
53 (every Eagle-import pin is typed "power input" and no symbol has a "power output": needs
PWR_FLAG symbols on each rail or pin-type edits), unresolved_variable 22 (`${DISP}` text in U-symbol fields, cosmetic), pin_not_driven 13. Warnings: 251 footprint-library
links (section 3), 112 unconnected wire endpoints (60 at import: Eagle wire stubs plus the cut
labels), 27 off-grid endpoints (Eagle's 0.1-inch grid against KiCad's), 16 isolated labels (13 of
them the cut Okapi_3 partners), 13 library-symbol issues. The 7 no-connect flags sit on J9's SIM
and UB pins on Okapi_3 and are correct; U$1, U$2, H1–H3 are in the BOM as if they were parts.

## 6. Verdict

**The raw import was sound; the current HEAD is not, and it is cheap to make sound.** The board
is a complete, object-for-object copy of the Eagle board with its original connectivity intact. The
schematic reproduced 205 of 209 nets at import, 206 after the power-net fix, and lost 54
connections in the last commit. Re-importing with a newer KiCad gains nothing (the one importer merge, D5, is an Eagle drawing
ambiguity) and redrawing is not warranted.

Repairs, in order:

1. **Restore the 60 global labels on Okapi_3** from faaf72e, keep the 7 no-connect flags, delete
   only SIM_VCC and UB_VBUS. Acceptance: netlist export gives 206/209 nets exact and 0 lost
   connections against the Eagle pinrefs (the scripts in the scratch directory do this). About an
   hour, mostly verification.
2. **Redraw the two D5 wires** so N$59 reaches GREEN_CATH without passing through the RED_CATH pin
   end. Acceptance: 208/209 (U21/U22 `QOD` is an Eagle-side discrepancy to decide, not a conversion
   fault). Minutes.
3. **Give the footprints a library**: export the 252 embedded footprints to `Okapi.pretty`, add a
   project `fp-lib-table`, resolve the eight `_528` jumper names, then run Update PCB from
   Schematic with re-link by reference so every footprint gets a `(path …)`. Acceptance: DRC
   parity 0; ERC footprint links 0. Half a day.
4. **Carry the design rules**: Default netclass clearance 0.127 mm, track 0.127 mm, via drill 0.2
   mm, from the Eagle `jlcpcb-2layer` set; add a 2-layer stackup; refill zones and save. Acceptance:
   clearance errors 499 → 9 (all USB2). An hour.
5. **Recreate the two bRestrict keepouts** on B.Cu by eye from the Eagle board (the only lost
   geometry). An hour.
6. **ERC hygiene**: PWR_FLAG per rail, add the two embedded power symbols to the library, clear
   the `${DISP}` fields, decide whether the 24 local labels should be global (they are the Eagle
   global names), exclude U$1/U$2/H1–H3 from the BOM. Half a day, no connectivity risk.
7. **Decide the Eagle-origin discrepancies**: J9-67/74 (SIM_VCC, UB_VBUS) and U21-5/U22-5 (`QOD`)
   are connected on the board and not in the schematic; the V_SOLAR_IN airwire was never routed.

What a reviewer must do by eye in KiCad, because the files cannot show it: open each sheet and look
for wires that cross a pin end they should not touch (the D5 pattern; KiCad's geometric
connectivity will join any such crossing, and Eagle's explicit netlist would not have) – the 112
dangling wire endpoints and 27 off-grid endpoints are where to look first; confirm the USB2 shell
pads are meant to overlap; check the silkscreen reads after the 0.8 mm text rule is relaxed; and
walk the refilled GND pours against the Eagle rendering for islands (one isolated B.Cu GND island
after refill).

## Sources and commands

- `which kicad-cli` → /usr/bin/kicad-cli; `kicad-cli version` → 10.0.7
- `git log --oneline -- Hardware/KiCAD-10import` (3 commits); `git log -1 -- Hardware/Okapi.sch` → b4032d4 2024-11-02
- `xxd Okapi.kicad_dru` → `(version 1)` only
- `cat sym-lib-table` → one library, `Okapi-eagle-import`
- Headers: Okapi.sch / Okapi.brd are Eagle 9.6.2 XML; kicad_sch version 20260306, kicad_pcb version 20260206
- Scripts: scratchpad/kicad/parse_eagle.py, parse_knet.py, compare.py (outputs eagle.json, knet.json, compare2.out)
- `kicad-cli sch export netlist --format kicadxml -o okapi.xml Okapi.kicad_sch` (exit 0)
- `kicad-cli sch erc --format json --severity-all` (622 violations); `kicad-cli pcb drc --format json --severity-all --all-track-errors --schematic-parity` (1296 + 18 unconnected + 361 parity)
- `kicad-cli pcb export svg -l F.Cu,B.Cu,Edge.Cuts,F.SilkS,F.Fab` → board.svg (exit 0)
- Scripts (all in the scratch directory): sexp.py (s-expression reader), pcb_stats.py, compare_orig.py, compare_mid.py; outputs orig/ (6b6530f sheets, netlist, erc.json, compare.out), mid/ (faaf72e), drc2/ (refilled, 0.127 mm netclass DRC)
- `git show 6b6530f:…` and `git show faaf72e:…` for each sheet; `git show fb54477 -- Okapi_3.kicad_sch | grep '^-\t(global_label'` → 62 removed, 0 added, 7 no_connect added
- `kicad-cli pcb drc --refill-zones` on drc2/Okapi.kicad_pcb (board not saved; repository untouched)
- Eagle board parse: `Okapi.brd` plain wires/texts/polygons by layer, signals (wires, vias, polygons, contactrefs), designrules `jlcpcb-2layer`
- Dead ends: first Eagle parser treated multi-pad `connect pad="3 7 10"` as one pad (fixed, rerun); first PCB regex assumed `(net N "name")` numeric form, the 20260206 format uses `(net "name")` (replaced by the s-expression parser)
- `${DISP}` appears in all six sheets and 24 times in the library; ERC flags 22 symbols on the root sheet
- Untracked: `Okapi-backups/Okapi-2026-06-17_182008.zip` (git status)

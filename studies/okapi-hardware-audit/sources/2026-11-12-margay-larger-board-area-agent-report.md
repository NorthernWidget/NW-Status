COMPLETE

# Margay larger board: required area and shape (agent report, 2026-11-12)

Question: how much board area a larger Margay (v4.0.0) needs if every part goes on the top side except the bottom's SD holder, its solder jumpers and parts that are easy to hand-solder after reflow (0603 or larger passives; SOD, SOT-23, SOT-143, SC-70 at most; never leadless).

Board: Project-Margay `Hardware/KiCAD/Margay.kicad_pcb` at ca24e31, copied to `tools/margay-larger/Margay.kicad_pcb` (sha1 d82cf620e445de7cf0c491074fadc09e178d4003, identical to the source). Nothing in Project-Margay or nw-cold-silicon was modified. All scripts and their outputs are in `tools/margay-larger/`; every number below is pasted from the named output file.

## Result in brief

- **Today's top density**: 0.645 (courtyards, and pads + 0.25 mm for footprints without one) or 0.802 (the same, but the screw terminals, RTC1, ISP1 and a few others counted by their body outline, the larger of the two). Usable top area 1423.6 mm².
- **Added on top** (v3.1 issues plus #66, all new parts on top): 27 parts, 141.8 mm²; removed 29.2 mm² (C20, U9, U10, R17, R18, C11). Undecided items from #66, #51 and #57 add 8 parts, 25.4 mm².
- **Required usable top area**: 1564-1598 mm² at today's density (x1.10-1.12), 1738-1776 mm² at 90 % of it (x1.22-1.25), 1955-1998 mm² at 80 % (x1.37-1.40). The range within each pair is the two proxies.
- **Fixed dimensions**: the top edge is fully spoken for (J2's pads, the SD card's entry, USB-C and H2), so 50.1 mm is already the minimum length with today's edge assignment; the left edge is J2's 26.1 mm body plus H1, so 30.4 mm is the minimum height. Every larger board grows from 50.1 x 30.4, it does not reshape it.
- **Shapes** (same corner radii and hole offsets): at today's density 50.1 x 33.9, 56.0 x 30.4, or 53.0 x 32.1; at 90 % of today 50.1 x 37.5, 62.0 x 30.4, or 55.8 x 33.8 (pads proxy, the larger of the two).
- **Bottom-side rule**: three base parts fail it: the TVS0500 (WSON-6), the 4-line clamp if it is the USON-10, and the 4 x 0402 resistor array; and every 0402 passive fails it by size. These are all on top in the main case. If the leaded parts that pass the rule (90.3 mm² of the 141.8) went on the bottom, the top need falls to x1.02 at today's density.

## 1. Parts on the larger board that are not on today's top

Footprint areas are measured from nw-cold-silicon (`libareas.py` -> `libareas.txt`): the courtyard polygon where the footprint has one, otherwise the pads' bounding box plus 0.25 mm per side (stated as "pads+0.25"). Three footprints come from `scratch.pretty` (copied from `margay-room31`) and are ESTIMATES: the resistor array, the USON-10 clamp and the DFN1006 TVS. The part list, values and issues come from `margay-room31/parts4D.json` (v3.1) and the #66 comments and `margay-power-path-decision.md` §4, §8 (v4.0.0). Command: `python3 required.py` -> `required.txt`.

Side: "top" in the main case, which puts every new part on top. "Bottom rule" says whether the part could go on the bottom under the hand-solder rule.

| Issue | Part | Function | Footprint | Area mm² | Area source | Bottom rule |
|---|---|---|---|---|---|---|
| #53 | C_SDHF | 0.1 µF at J1 VDD | C0402 | 2.807 | courtyard | no: 0402 |
| #70 | C_VBAT | 100 µF on VBAT | C1206 | 9.655 | courtyard | yes |
| #70 | D_BT | BAT43WS, coin cell to VBAT | SOD323-R | 3.630 | pads+0.25 | yes |
| #70 | R_BT | 1 k, coin cell series | R0402 | 2.807 | courtyard | no: 0402 |
| #71 | R_EN | 10 k, PC6 to U7 EN | R0402 | 2.807 | courtyard | no: 0402 |
| #71 | C_EN | 0.1 µF, U7 EN to GND | C0402 | 2.807 | courtyard | no: 0402 |
| #73 | R_PD | 100 k, U7 EN to GND | R0402 | 2.807 | courtyard | no: 0402 |
| #48 | R_INT | 10 k pull-up, RTC_INT (on 3V3) | R0402 | 2.807 | courtyard | no: 0402 |
| #52 | C_ADC | 0.1 µF at U14 VDD | C0402 | 2.807 | courtyard | no: 0402 |
| #53 | C_SD | 4.7 µF at J1 VDD | C0603 | 5.743 | courtyard | yes |
| #72-1 | U_USB | SP0503BAHTG, USB D+ D- VBUS | SOT143B | 7.500 | pads+0.25 | yes |
| #72-2 | U_TVS | TVS0500, VBAT+ | DRV0006A | 6.090 | pads+0.25 | **no: WSON-6, leadless** |
| #72-3 | RN_J2 | 4 x 330 Ω array, TX RX ADC GPIO | RARRAY4_0402 | 4.517 | ESTIMATE footprint | no: 0402-size array |
| #72-3 | R_SDA | 330 Ω, SDA_EXT | R0402 | 2.807 | courtyard | no: 0402 |
| #72-3 | R_SCL | 330 Ω, SCL | R0402 | 2.807 | courtyard | no: 0402 |
| #72-4 | U_CL2 | clamp, SDA SCL | DCK_R-PDSO-G6 | 7.920 | pads+0.25 | yes: SC-70-6 |
| #72-4 | U_CL3 | clamp, AX VREF at J3 | DCK_R-PDSO-G6 | 7.920 | pads+0.25 | yes: SC-70-6 |
| #72-4 | U_CL1 | 4-line clamp, TX RX ADC GPIO | USON10_2.5X1 | 4.455 | ESTIMATE footprint | **no: USON-10, leadless** (the SC-70-6 option passes, +3.5 mm²) |
| #66 | U_A | LM66100, USB | DCK_R-PDSO-G6 | 7.920 | pads+0.25 | yes: SC-70-6 |
| #66 | U_B | LM66100, battery | DCK_R-PDSO-G6 | 7.920 | pads+0.25 | yes: SC-70-6 |
| #66 | U_SS | TPS22917 soft-start | DBV_R-PDSO-G6 | 12.750 | pads+0.25 | yes: SOT-23-6 |
| #66 | C_CT | 0.1 µF, U_SS CT | C0402 | 2.807 | courtyard | no: 0402 |
| #66 | R_CEA | 10 k, U_A CE | R0402 | 2.807 | courtyard | no: 0402 |
| #66 | R_CEB | 10 k, U_B CE | R0402 | 2.807 | courtyard | no: 0402 |
| #66 | R_PU | 10 k, U_A ST pull-up | R0402 | 2.807 | courtyard | no: 0402 |
| #66 | C_VSYS1 | 100 µF, VSYS bulk | C1206 | 9.655 | courtyard | yes |
| #66 | C_VSYS2 | 100 µF, VSYS bulk | C1206 | 9.655 | courtyard | yes |
| **Base total** | 27 parts | | | **141.8** | | 90.3 mm² pass the rule |
| #66 open | C_3V3OUT | FT231X 3V3OUT's own capacitor (0.1 µF assumed) | C0402 | 2.807 | courtyard | no: 0402 |
| #66 open | C_FTVCC1 | FT231X VCC 100 nF (FTDI reference) | C0402 | 2.807 | courtyard | no: 0402 |
| #66 open | C_FTVCC2 | FT231X VCC 4.7 µF (0603 assumed) | C0603 | 5.743 | courtyard | yes |
| #51 | FB_AVCC | ferrite bead 3V3 to AVCC | R0402 size | 2.807 | courtyard | no: 0402 |
| #51 | C_AVCC | 10 µF at AVCC | C0402 | 2.807 | courtyard | no: 0402 |
| #51 | R_AREF | 100 Ω AVCC to AREF | R0402 | 2.807 | courtyard | no: 0402 |
| #51 | C_AREF | 1 µF at AREF | C0402 | 2.807 | courtyard | no: 0402 |
| #57 | R_SDO | 1 MΩ SDO pull-down (the issue's item 3) | R0402 | 2.807 | courtyard | no: 0402 |
| **Options total** | 8 parts | | | **25.4** | | |

Moved, no area change: C19 moves along the top to RTC1's VBAT (#70). Nothing moves from today's bottom to the top: J1, JP1 and JP2 stay on the bottom.

Removed (from `density_pads.json`, the same proxies as today's parts): C20 5.74 (#70), U9 12.39, U10 2.61, R17 2.81, R18 2.81, C11 2.81 (#66). Total 29.2 mm².

Not counted, with the reason:
- #55 (TVS on J3 and J2) is the same protection #72 adds (TVS0500 on VBAT+, the SC-70-6 clamps at J3 and on SDA/SCL, the 4-line clamp on the J2 signal lines). No extra parts.
- #50: its option A removes Q2 (11.2 mm², pads+0.25) and adds an optional 0402 bead; #66 instead keeps Q2 for VCCIO and RESET#. Undecided, so Q2 stays in the count.
- #66 asks C6 to drop from 10 µF to 4.7 µF; the footprint is not specified, so C6 stays at its present C0805.
- #29 (silkscreen) and #9 (PG cutoff, now firmware) add no parts.
- All values in the options rows are the issues' proposals, not decisions.

Package changes the bottom rule implies (only if Andy wants these parts on the bottom; in the main case they are on top and need nothing):
- **TVS0500 (WSON-6, DRV)**: no leaded version of this part; a bottom VBAT+ TVS would need a different part in SOD-323 or SOD-123 (none checked here).
- **4-line clamp**: USON-10 fails; the SC-70-6 option (`placed_parts4E.json`) passes.
- **Resistor array (4 x 0402)**: fails by size; four 0603 resistors would pass (4 x 5.743 = 23.0 mm² against 4.5 mm²).
- **Every 0402 passive** (19 in base and options): 0603 would pass.
- Already passing: the 1206 capacitors, BAT43WS (SOD-323), SP0503BAHTG (SOT-143), the SC-70-6 clamps, both LM66100 (SC-70-6) and the TPS22917 (SOT-23-6).

## 2. Today's top packing density

Definition (`density.py`):
- **Usable top area**: the Edge.Cuts polygon inset 0.4 mm (the board asks 0.381 mm copper to edge), minus a 5.56 mm circle at H1 and H2 (the screw-head circle on User.Comments in `4_40_CLOSE`; the courtyard circle is 4.65 mm). Rasterized at 0.05 mm.
- **Part area**: the sum (not the union) of each top footprint's area: courtyard polygon where it has one; otherwise pads + 0.25 mm per side (proxy `pads`, the stated rule), or the larger of that and the body-graphics + pads bounding box (proxy `body`). H1, H2 (counted as keepouts), U$1 (a B.Fab drawing with no pads) and LOGO1 are excluded. 77 top footprints counted.
- **Density** = part area / usable area.

Commands: `PROXY=pads python3 density.py` -> `density_pads.txt`, `PROXY=body python3 density.py` -> `density_body.txt`.

| | Value |
|---|---|
| Outline (polygon area) | 1521.8 mm² (bbox of the cut lines 50.145 x 30.404 mm; corner radius 2 mm on three corners, the J2 corner square) |
| Inset outline | 1458.9 mm² |
| Usable top area | 1423.6 mm² |
| Sum of top parts, proxy `pads` | 918.5 mm², density **0.645** |
| Sum of top parts, proxy `body` | 1141.0 mm², density **0.802** |

The two differ mostly at the screw terminals: J2 is 50.4 mm² by its pads and 176.4 mm² by its body (6.75 x 26.11 mm), J3 29.8 against 107.8 mm² (`bodies.txt`). The `body` proxy is closer to what the top physically holds; the `pads` proxy is the rule the study was given. 34 footprints have no courtyard (`inventory.txt`, "pads+0.25" rows); all of them use a proxy here.

## 3. Required top area

`required.py` -> `required.txt`. Required usable area = (today's top sum - removed + added) / density. The new parts are counted with the same definitions as today's.

| Case | Sum, `pads` / `body` mm² | Today's density | 90 % of today | 80 % of today |
|---|---|---|---|---|
| A: base, all new parts on top | 1031.1 / 1253.7 | 1598 / 1564 (x1.12 / x1.10) | 1776 / 1738 (x1.25 / x1.22) | 1998 / 1955 (x1.40 / x1.37) |
| B: base + options, all on top | 1056.5 / 1279.1 | 1638 / 1596 (x1.15 / x1.12) | 1819 / 1773 (x1.28 / x1.25) | 2047 / 1995 (x1.44 / x1.40) |
| C: base, rule-passing parts on the bottom | 940.9 / 1163.4 | 1458 / 1452 (x1.02 / x1.02) | 1620 / 1613 (x1.14 / x1.13) | 1823 / 1814 (x1.28 / x1.27) |

Values are usable top area in mm² with the ratio to today's 1423.6 mm².

**The relaxed densities are a proposal, not a measurement.** Today's density is what a nearly full board reached: the v3.1 room study placed its 19 parts only by moving tracks under most of them. I chose 90 % and 80 % of today as two steps of relief for routing the new power path (every power net changes over once, and the J2 protection must sit in line between J2 and U1); the right figure is Andy's call. Case C also assumes the bottom has room outside J1 for 90 mm² of parts; today the bottom outside J1 is a 16 mm strip at the J3 end and a 3.5 mm strip along the long edge (room study), and a taller board adds to both.

## 4. Shape constraints

Measured on the board (`keyparts.py`, `bodies.txt`, `edges.py`); board coordinates, x along the 50.1 mm length, y along the 30.4 mm height, top edge y 89.80, bottom edge y 120.21, left edge x 123.43, right edge x 173.57.

| Part | Side | Where | Size |
|---|---|---|---|
| J2, 10-position screw terminal | top, THT | along the left (short) edge, from the top edge down | body 6.75 x 26.11 mm (x 123.40-130.16, y 89.75-115.86); pads span y 90.61-115.00 |
| J3, 6-position screw terminal | top, THT | along the right (short) edge, lower part | body 6.75 x 15.95 mm (x 166.36-173.11, y 102.45-118.40) |
| J1, full-size SD holder | bottom | card enters at the top edge (courtyard overhangs it by 0.67 mm; confirmed in the README photo `Margay_v30_back_with_quarter_20250206.jpg`) | courtyard 29.39 x 26.84 mm (x 128.29-157.68, y 89.13-115.97); pad row at y 115.62 |
| J4, USB-C | top | top edge, overhanging it (courtyard to y 88.29) | courtyard 10.23 x 8.52 mm (x 158.57-168.80) |
| BT1, 12 mm coin cell holder | top | lower edge, over J1 | pads+0.25 18.28 x 10.66 mm (x 132.45-150.23, y 109.54-119.70) |
| H1 | – | bottom-left corner, 125.59, 118.05 | 5.56 mm keepout (2.95 mm drill) |
| H2 | – | top-right corner, 171.43, 92.01 | 5.56 mm keepout |

What these fix:
- **Minimum length about 50.1 mm.** Along the top edge, from the left: edge to J1's courtyard 4.86 mm (J2's pads end at x 127.49, 0.8 mm clear of J1), J1 29.39, gap 0.89, J4 10.23, J4 to the right edge 4.77 (H2's keepout begins at x 168.65, 0.15 mm inside J4's courtyard). Sum 50.14 mm, today's length. Keeping the SD entry and USB-C on the same edge as today, the length cannot shrink and only grows if a part moves off the top edge or the board widens.
- **Minimum height about 30.4 mm.** Along the left edge J2's body runs from the top edge to y 115.86, and H1's keepout from y 115.27 to the bottom edge (0.6 mm overlap with J2's body bbox, as today). J1 alone needs 26.2 mm from the top edge (26.84 less its 0.67 mm overhang), plus whatever the bottom holds below it.
- **J3 and H2** share the right edge: J3 needs 15.95 mm, H2's keepout 4.6 mm from the top edge; 30.4 mm leaves 9.6 mm of the right edge free, between them.
- **USB-C** sits between the SD entry and H2; neither a taller nor a longer board moves it.

Candidate shapes (`shapes.py` -> `shapes.txt`; usable area = (W-0.8)(H-0.8) - 1.9 - 35.3 mm², calibrated to reproduce today's 1423.6 mm², with three 2 mm corner radii and the holes at today's corner offsets):

| Target (case A) | Same 50.1 length, taller | Same 30.4 height, longer | Both, same proportion |
|---|---|---|---|
| Today's density (usable 1564-1598) | 50.1 x 33.2-33.9 | 54.9-56.0 x 30.4 | 52.5-53.0 x 31.8-32.1 |
| 90 % of today (1738-1776) | 50.1 x 36.8-37.5 | 60.8-62.0 x 30.4 | 55.2-55.8 x 33.4-33.8 |
| 80 % of today (1955-1998) | 50.1 x 41.2-42.0 | 68.1-69.5 x 30.4 | 58.4-59.0 x 35.4-35.7 |

Spot candidates (same file): 50.1 x 34 holds 1600 mm² usable (x1.124); 50.1 x 36, 1698 (x1.193); 50.1 x 38, 1797 (x1.262); 55 x 35, 1816 (x1.276); 60 x 30.4, 1715 (x1.205); 60 x 35, 1987 (x1.396).

Which direction suits the circuit (interpretation, a hypothesis): growing the height adds a strip along the bottom long edge, below BT1 and ISP1, and lengthens the right edge where J3 and the power cluster sit; growing the length adds a band at one short edge, which moves J2 or J3 away from the circuit they serve. The power path (#66) and the J3 protection gather at the right end, between J4 and J3.

## Placement constraints (#57, #59), recorded

- **#57, BME280 away from heat.** The BME280 on the board is **U12**, not U10 as the issue says (U10 is the TLV3691, which #66 removes). Center distances (`constraints.py` -> `constraints.txt`): U12 to U2 (FT231X) 10.12 mm, to U6 (TPS797) 15.24 mm, to U7 11.51 mm, to U9 12.82 mm. It sits over J1 near the board's middle. The issue asks for a corner far from U2 and U6; on a taller board, the new strip's left end (near H1, away from U2 at the top and the regulators at the right) is a candidate.
- **#59, crystal closer to the ATmega.** The crystal is **XTAL1** on the board (the issue says Y1). Pad-center distances: U1 pin 8 (XTAL1) to XTAL1's OSC1 3.88 mm; U1 pin 7 (XTAL2) to OSC2 3.87 mm. The crystal's pads begin 1.98 mm below U1's pad row (y 106.18 against 104.20). C2 and C3 (136.13 and 143.75, 107.51) sit outboard of the crystal, not between it and U1, which the issue asks for.

Neither adds area; both want room near U1 and at a corner that the density figures above do not reserve.

## 5. Placement test

Skipped. A test that keeps today's layout and drops the new parts into an added strip would test an add-on strip, not the re-laid-out board that the density figure assumes, and the v3.1 study's target radii (parts within 4-14 mm of their pins) would mostly fail on a strip at the far edge, which would read as "does not fit" for the wrong reason. A fair test needs Andy's placement of the power path first.

## Sources and runs

- `cp Project-Margay/Hardware/KiCAD/Margay.kicad_pcb tools/margay-larger/` (ca24e31; sha1 match checked).
- `python3 inventory.py` -> `inventory.txt`, `inventory.json`: every footprint, side, courtyard or proxy.
- `python3 edges.py`: Edge.Cuts (lines and three r = 2 mm arcs; outline polygon 1521.762 mm²), H1/H2 (2.9464 mm drill, 4.65 mm courtyard circle, 5.56 mm User.Comments circle). Note: `GetCourtyard().Area()` for H1/H2 reports 4.2 mm², the area of a stroked circle, not a disk; holes are handled as keepouts instead.
- `python3 bodies.py` -> `bodies.txt`, `bodies.json`: pads+0.25 against body bbox for the 34 footprints without a courtyard.
- `python3 libareas.py` -> `libareas.txt`, `libareas.json`.
- `PROXY=pads|body python3 density.py` -> `density_*.txt`, `density_*.json`.
- `python3 required.py` -> `required.txt` (inputs `parts_v4.json`, `removed_v4.json`).
- `python3 shapes.py` -> `shapes.txt`.
- `python3 keyparts.py`, `python3 constraints.py` -> `constraints.txt`.
- Documents read: `margay-v3.1-room-study.md`; `margay-room31/occ.py`, `place31.py`, `parts4D.json`; `margay-power-path-lm66100.md`; `margay-power-path-decision.md`; `sources/2026-11-11-margay-room-study-agent-report.md` (the #66 parts and the earlier 75 mm² estimate); `sources/2026-11-11-margay-sd-holder-agent-report.md` (J1 is the Würth 693063010911, full-size SD); README photo of the back.
- GitHub, read only: `gh issue list -R NorthernWidget/Project-Margay --milestone v4.0.0` (open: #66, #59, #57, #55, #51, #50, #29, #9); `gh issue view N --comments` for each.
- Dead ends: `GetShapeTypeName` does not exist in this pcbnew (used `ShowShape`); `GetBoardPolygonOutlines` needs a second argument in KiCad 10; merging pad boxes with an `or` idiom crashed pcbnew (malloc abort), replaced by coordinate lists.

# Margay v3.1.0 room study for #66 and #70 (agent report, 2026-11-11)

Status: COMPLETE

Scratch copy: /tmp/claude-1000/-home-awickert-Dropbox-NorthernWidget-github/cf0342fa-36e3-4818-be1e-2b4b31cc1756/scratchpad/roomstudy/KiCAD (Project-Margay untouched).

## Method

- Occupancy grids at 0.1 mm per side (`occ.py`, `place.py` in the scratch directory). A kept part blocks its courtyard where it has one, otherwise its body graphics and pads (silkscreen outline included, text excluded), plus 0.15 mm. Through-hole pads block both sides. Board edge keepout 0.3 mm. U$1 is excluded: it is a B.Fab drawing with no pads.
- Removed before measuring: U9, U10, R17, R18, C11, C20. Tracks of the nets that disappear with them (Net-(U10-IN-), Net-(U10-OUT), VMAIN, which becomes VSYS) are not counted as copper.
- Copper grid per side: every other track, via and pad, grown by 0.15 mm. Margay has no zones.
- Footprints: LM66100 on `DCK_R-PDSO-G6` (pads 0.4 x 0.9 mm at 0.65 mm pitch, rows 2.2 mm apart: the footprint U4, a TI DCK part, already uses; the Microchip-style `SC-70_6` has 0.47 x 1.0 pads at 1.8 mm rows). TPS22917 on `DBV_R-PDSO-G6`, the footprint the library's TPS22917DBV symbol names. 100 uF on `C1206`, 0402 passives on `C0402`/`R0402`, BAT43WS on `SOD323-R`.
- Placement search: every position at 0.1 mm and every 90-degree rotation within 9 mm of a target point beside what the part connects to; nearest wins, the bottom carries a 2 mm penalty. Two tests: (a) courtyards only, routing to be redone; (b) courtyards and pads clear of existing copper, no rerouting.

## Free area (0.15 mm margin around parts, 0.3 mm edge)

| Region | Top free | Top largest free rectangle | Bottom free | Bottom largest free rectangle |
|---|---|---|---|---|
| Whole board (1531 mm2) | 271 mm2 | – | 545 mm2 | – |
| Power, x 150-174, y 89.8-121 | 133 mm2 | 6.0 x 3.1 mm at x 154.6-160.6, y 101.2-104.3 (the old U9/U10 spot) | 372 mm2 | 15.5 x 6.5 mm at x 158.0-173.5, y 96.6-103.1 |
| Clock and BT1, x 128-156, y 104-121 | 89 mm2 | 1.8 x 7.9 mm at x 154.2-156.0, y 112.2-120.1 | 112 mm2 | 28.0 x 3.9 mm at x 128.0-156.0, y 116.2-120.1 (below the SD holder) |

The new parts need roughly 75 mm2 of footprint (three 1206 at about 10 mm2 each, TPS22917 about 12, two LM66100 about 8 each, six 0402 at about 3 each, SOD323 about 4). The six removed parts free about 30 mm2 on top.

Board-level silkscreen also blocks parts on its side: the terminal labels (REF, Ax, B+, B-, Vs, GND, TX, RX and the rest), the jumper notes (SDA OB, SDA EXT, AUX, J0), and the bottom credit block "Project Margay v3.0 / Northern Widget & University of Minnesota" (x 160.5-173.0, y 93.5-98.0). With these counted the bottom power-region figures above drop to 270 mm2 free, largest rectangle 14.7 x 4.8 mm at x 158.8-173.5, y 98.3-103.1. All numbers below are with the silkscreen counted.

## Result: the parts fit, but only with nine of the twelve on the bottom

Top alone does not hold them. Courtyards only (routing ignored), top only: U_A takes U9's place, then neither the second LM66100, the TPS22917 nor any of the three 100 uF capacitors finds a spot within 9 mm of its target. With 0805 bulk capacitors in place of 1206 the top result is the same: no 0805 fits either.

Placed with both sides (scratch board `KiCAD/Margay_C.kicad_pcb`, plan `plan_C.json`; center coordinates in board mm, rotation as KiCad reports it):

| Part | Footprint | Side | Center x, y | Rotation | Joins |
|---|---|---|---|---|---|
| U_A, LM66100 (USB) | DCK_R-PDSO-G6 | bottom | 160.6, 100.6 | 180 | VUSB_SS to VSYS |
| U_B, LM66100 (battery) | DCK_R-PDSO-G6 | bottom | 163.6, 100.6 | 180 | VBAT_SW to VSYS |
| U_SS, TPS22917 | DBV_R-PDSO-G6 | bottom | 167.2, 100.6 | 180 | VUSB to VUSB_SS |
| C_CT, 0.1 uF | C0402 | bottom | 170.9, 100.6 | 180 | U_SS CT |
| R_CEA, 10 k | R0402 | bottom | 170.9, 102.3 | 180 | U_A CE |
| R_PU, 10 k | R0402 | bottom | 166.9, 103.5 | 180 | U_A ST pull-up |
| R_CEB, 10 k | R0402 | bottom | 159.5, 107.7 | 90 | U_B CE |
| C_VSYS1, 100 uF | C1206 | top | 157.8, 103.0 | 0 | VSYS, in U9's place |
| C_VSYS2, 100 uF | C1206 | bottom | 162.6, 103.8 | 180 | VSYS |
| C_VBAT, 100 uF | C1206 | bottom | 152.0, 117.5 | 180 | RTC VBAT (#70), below the SD holder |
| D_BT, BAT43WS | SOD323-R | top | 155.1, 114.5 | 90 | coin cell series diode (#70) |
| R_BT, 1 k | R0402 | top | 152.1, 111.1 | 0 | coin cell series resistor (#70), in C20's place |

Checks on the placed board:
- Body or courtyard gaps under 0.15 mm between a new part and any kept part, any through-hole pad on the other side, or any board-level silkscreen item: none (two DBV-adjacent 0402s first came out 0.19 mm into U_SS because the DBV body is asymmetric and flips differently than the search assumed; both moved 0.4 mm in x).
- Distance from the board edge, smallest: C_CT and R_CEA 1.18 mm, C_VBAT 1.70 mm; every 1206 at least 1.7 mm in.
- `kicad-cli pcb drc` reports courtyards_overlap 0, but that check is weak here: DCK_R-PDSO-G6, DBV_R-PDSO-G6, SOD323-R and most of Margay's own parts carry no courtyard in the library, so the grid check above is the one that counts. (The scratch copy also reports lib_footprint_issues, because its fp-lib-table path does not resolve from the scratch directory.)
- DRC items involving the new parts, all expected for a placement without routing: shorting_items 53, solder_mask_bridge 79, clearance 13, hole_clearance 10. They are new pads landing on existing tracks and vias.

**VBUS ESD spot (#72):** with the plan above in place, a SOD-323 fits on top at 160.7, 98.6 (rotation 90), in the place R17 and R18 leave, about 2.7 mm from J4's VBUS pad B4A9. No SOT-23-3 fits within 5 mm of J4's VBUS pins on either side.

## Routing, rough judgment (not attempted)

Tracks and vias the new parts land on, which would have to move:

| Area | Track segments by net | Vias |
|---|---|---|
| Bottom power cluster, x 159.4-172.4, y 98.7-104.9 | 3V3 6, VREF 6, SCL 6, VUSB 4, 3V3_AUX 3, SDA_OB 3, GND 1 | VUSB, GND, 3V3, SDA_OB, SCL 1 each; 3V3_AUX 2 |
| C_VSYS1, top | VUSB 6, GND 7 (old U9 fan-out, rerouted anyway) | – |
| C_VBAT, bottom | SCK 3, MISO 2, GND 2 | – |
| R_BT, top | GND 4, Net-(BT1-+) 3 (C20's old tracks) | – |
| D_BT, top | MISO 1 | – |

Tight spots:
1. **The bottom strip under J4, y 98.3-104.9**, between the credit block above and the Northern Widget logo below. About ten bottom tracks (SCL, SDA_OB, VREF, 3V3, 3V3_AUX, VUSB) cross it on their way to J3 and the jumpers, and the cluster sits on them. They need a new path: through the 0.5 mm gap between C_VSYS2 and the logo (y 104.8-105.3), around through the top, or by moving the credit block or the logo. Moving the credit block frees the strip up to y 96.6 (largest bottom rectangle then 14.7 x 6.5 mm).
2. **Every power net changes sides once:** VUSB from J4's top pads down to U_SS, VBAT_SW from U8 (top) to U_B, VSYS from the cluster up to U6 and U7 (top) and C_VSYS1. Each needs one or two vias in an area where the top is already dense around U8, Q2 and Q3.
3. **C_VBAT** sits on SCK and MISO below the SD holder; those two tracks would move a little toward the board edge (1.7 mm of room).
4. The cluster covers the U$1 drawing (the jumper glyph "1V8 / REF / Ax / front JP" on B.Fab). It does not print today; if #80 brings it back to the silkscreen, it needs another place.

**Assembly note:** Margay already has a bottom-side SMT part (J1, the SD holder), so nine more bottom parts add parts to an existing second side, not a new side.

**Fallbacks if the bottom is not acceptable:** none of the obvious ones works on top alone. 0805 bulk capacitors do not fit on top either. What would free top space: a smaller soft-start switch than the SOT-23-6 TPS22917 (none checked), or dropping C_VSYS2 to a single bulk capacitor (#66's sizing needs about 47 uF effective; one GRM31 gives about 23.7 uF worst case, so not without re-deciding the handover margin).

## Renders

- Top before and after: `/tmp/claude-1000/-home-awickert-Dropbox-NorthernWidget-github/cf0342fa-36e3-4818-be1e-2b4b31cc1756/scratchpad/roomstudy/r/top_pair.png`
- Bottom before and after (viewed from below, mirrored): `/tmp/claude-1000/-home-awickert-Dropbox-NorthernWidget-github/cf0342fa-36e3-4818-be1e-2b4b31cc1756/scratchpad/roomstudy/r/bot_pair.png`

Orange boxes mark the removed parts, blue boxes the new parts.

## Reproduce

```sh
cd /tmp/claude-1000/-home-awickert-Dropbox-NorthernWidget-github/cf0342fa-36e3-4818-be1e-2b4b31cc1756/scratchpad/roomstudy
python3 occ.py KiCAD/Margay.kicad_pcb            # free areas
python3 place.py crt F                           # top only, courtyards
BULK=C0805 python3 place.py crt F                # top only, 0805 bulk
python3 planC.py plan_C.json; python3 build_scratch.py plan_C.json KiCAD/Margay_C.kicad_pcb
kicad-cli pcb drc --severity-all --format json -o drc_C.json KiCAD/Margay_C.kicad_pcb
python3 render.py
```

COMPLETE

# Margay v4.0.0: along which dimension should the board grow?

Agent report, 2026-11-12. Results are appended as they are confirmed.

Board: Project-Margay `Hardware/KiCAD/Margay.kicad_pcb` at ca24e31, copied to `tools/margay-growth/Margay.kicad_pcb` (sha1 d82cf620e445de7cf0c491074fadc09e178d4003, identical to the source, the same file the two earlier reports used). Board coordinates: x along the 50.1 mm length (left edge 123.43, right edge 173.57), y along the 30.4 mm height, increasing downward (top edge 89.80, bottom edge 120.21).

## Findings (appended as confirmed)

### G1. Today's functional blocks (`python3 fps.py` -> `fps.txt`, `fps.json`)

Bounding boxes are courtyards where the footprint has one, otherwise pads plus body graphics (`fps.txt` column "src"). Block boxes are the union of the members' boxes.

| Block (members) | x (mm) | y (mm) |
|---|---|---|
| J2, 10-position terminal | 123.40-130.16 | 89.75-115.86 |
| MCU: U1, C4, XTAL1, C2, C3, S1, S2, R14, R22, R23, U5, D3, R11-R13 | 130.40-145.29 | 90.17-110.61 |
| USB/FT231X: J4, U2, R3, R4, R7-R9, C1, C5-C9, D1, D2, R5, R6, R31, R32, Q2, Q3, R19, R21, U10 | 143.25-173.10 | 88.29-104.13 |
| Power: U6, U7, U8, U9, R17, R18, C10-C15, R20, Q1, U11, JP2 | 153.51-168.11 | 96.97-115.71 |
| Clock: RTC1, BT1, C19, C20, D4 | 132.07-153.83 | 103.22-119.70 |
| ADC/reference: U14, U13, C16-C18, R24, JP3 | 160.66-173.11 | 98.24-109.42 |
| I2C switch: U4, R15, R16, JP1 | 148.81-158.56 | 99.13-106.29 |
| BME280 U12 | 144.01-147.22 | 103.02-105.64 |
| Watchdog/reset: U3, R10, R2 | 150.88-166.22 | 114.68-120.07 |
| ISP1 | 156.51-161.72 | 112.27-120.02 |
| SD: J1 (bottom), R1 | 128.13-157.68 | 89.13-119.34 |
| J3, 6-position terminal | 166.36-173.11 | 102.45-118.40 |

Command: `python3 blocks.py` -> `blocks.txt`. The grouping is this study's proposal. H1 (125.59, 118.05) and H2 (171.43, 92.01) are the holes.

Read as a map: the left third is J2 and the MCU over the SD card; the top band from x 143 to the right edge is USB and the FT231X; the power cluster and the ADC fill the right half below it; the clock (RTC1, and BT1 along the lower edge) sits between U1 and the power cluster. BT1 (17.8 x 10.2 mm) lies directly under U1 and the crystal, 5.3 mm below U1's pad row (BT1 box top 109.54, U1 box bottom 104.20).

### G2. Routed length of the nets that cross the board (`python3 nets.py ...` -> `nets.txt`)

Sum of track segments on both layers, per net, at ca24e31:

| Net | Routed (mm) | Vias | Pad spread dx x dy (mm) | Ends |
|---|---|---|---|---|
| 3V3_AUX | 178.4 | 9 | 41.2 x 24.9 | J2.2, J2.8 at the left edge to U7 (center right), U13, U14, J1, JP2 |
| 3V3 | 128.6 | 12 | 30.5 x 28.2 | |
| SCL | 77.9 | 3 | 38.8 x 14.7 | J2.10 (126.73, 114.24) to U1, RTC1, U12, R16, U14 (165.5, 104.78) |
| VUSB | 55.4 | 4 | 17.2 x 9.8 | |
| VREF | 52.9 | 1 | 35.3 x 6.1 | U13 and J3.6 at the right to U1 pin 34 (AREF) |
| SDA_EXT | 45.0 | 3 | 30.7 x 10.8 | J2.9 to U4 and JP1 |
| TX_EXT | 27.4 | 2 | 15.8 x 6.6 | J2.3 to U1 pin 12 (142.5, 103.02) |
| RX_EXT | 23.3 | 2 | 15.0 x 4.8 | J2.4 to U1 pin 11 (141.68, 103.85) |
| VBAT+ | 21.0 | 2 | 12.6 x 9.4 | |
| Net-(BT1-+) (VBAT) | 19.9 | 0 | 18.5 x 15.0 | |
| ADC_EXT_A0 | 10.0 | 0 | 9.1 x 2.0 | J2.5 to U1 pin 37 |
| GPIO_EXT_D0 | 9.8 | 0 | 9.1 x 1.6 | J2.6 to U1 pin 43 |

TX_EXT and RX_EXT run about 1.2 times the Manhattan distance between their pads (27.4 against 22.4 mm, 23.3 against 19.8 mm, computed) because U1 pins 11 and 12 sit on the far (lower right) corner of the TQFP from J2; no outline change shortens them, only a pin or package rotation. The long nets (3V3_AUX, SCL, VREF, SDA_EXT) are long because their ends sit at opposite short edges: J2 at the left, U13/U14/J3 at the right.

### G3. Rigid-growth scenarios (`python3 scenarios.py` -> `scenarios.txt`, `scenarios.json`)

Method: footprints translate whole (never part by part), with their edge; nothing is saved. Occupancy follows `margay-room31/occ.py` conservative mode (courtyard box, else pads plus body; 0.15 mm spacing; 0.4 mm edge; through-hole pads block both sides; H1 and H2 as 5.56 mm discs), except that board-level silkscreen is not counted. The six parts #66 and #70 remove (U9, U10, R17, R18, C11, C20) are left out in every case, today's included. "Stretched" nets have pads on both a moved and a fixed footprint; the added length is at least the move per net, a lower bound. GND is excluded (pour). The outlines are rectangles (corner radii ignored). Sizes: 50.8 x 40.64 (taller), 68.58 x 30.404 (longer, 2.7 in, usable 1969 mm² by the earlier report's formula, computed), 58.42 x 35.56 (both, 2.3 x 1.4 in, usable 1966 mm², computed). All three sit in the 80 % band (1955-1998 mm²).

| Scenario | What moves | Free top / bottom (mm²) | Nets stretched, sum of minimum added length |
|---|---|---|---|
| S0 today | – | 261.4 / 546.1 | – |
| A0 taller, bottom edge down 10.236 mm, nothing moves | – | 778.8 / 1069.2 | 0 |
| A1 taller, the lower-edge row moves down 10.236 mm | BT1 C12 C19 D4 ISP1 J3 JP2 Q1 R1 R10 R2 U11 U3 U6 (top parts whose box starts below y 109.0, plus J3, JP2) | 772.4 / 1065.8 | 15 nets, 153.5 mm |
| B1 longer, right edge out 18.435 mm with the right column | C16 C17 C18 C5 C6 J3 U13 | 801.4 / 1088.6 | 7 nets, 129.0 mm (3V3_AUX, VUSB, VREF, VBAT+, AX, VSWITCH, VBAT-) |
| B2 longer, left edge out 18.435 mm with J2 | J2 | 803.1 / 1088.9 | 7 nets, 129.0 mm (every J2 signal, 3V3_AUX, SCL) |
| B3 longer, board split at x 157.9 | 27 parts right of the split (J4, the power and ADC blocks, J3) | 802.7 / 1085.7 | 19 nets, 350.3 mm |
| C1 both, bottom down 5.156, right column out 8.275 | union of A1 and B1 sets | 782.3 / 1077.6 | 18 nets, 135.3 mm |

The scripts flag "past edge" for ISP1, U3, J2 and J4; these are today's overhangs (J2 and J4 by design, ISP1 and U3 by their silk/fab boxes), not new clashes. No moved footprint lands on a fixed one or on a hole keepout.

Free top / bottom area (mm²) within reach of what the v4 parts need (same run). The radii are this study's proposal:

| Need | S0 | A0 | A1 | B1 | B2 | B3 | C1 |
|---|---|---|---|---|---|---|---|
| J2 pins, 8 mm (J2 series R and clamps) | 42.5 / 91.2 | 55.2 / 103.9 | 78.6 / 103.9 | 42.5 / 91.2 | 150.6 / 280.5 | 42.5 / 91.2 | 69.3 / 103.9 |
| U1 pins 7, 8, 5 mm (crystal) | 17.9 / 0 | 17.9 / 0 | 17.9 / 0 | 17.9 / 0 | 16.9 / 0 | 17.9 / 0 | 17.9 / 0 |
| U1 center, 10 mm | 100.4 / 0 | 100.4 / 0 | 108.2 / 0 | 100.4 / 0 | 105.8 / 0 | 100.4 / 0 | 108.2 / 0 |
| VUSB, VBAT+, VMAIN pads, 6 mm (#66) | 90.7 / 355.9 | 104.0 / 372.0 | 204.8 / 460.5 | 248.7 / 492.0 | 90.7 / 355.2 | 250.9 / 516.6 | 313.7 / 544.6 |
| J3 pins, 6 mm (J3 ESD) | 10.7 / 163.9 | 40.5 / 196.3 | 67.4 / 175.5 | 54.1 / 172.1 | 11.0 / 162.7 | 11.0 / 162.7 | 79.5 / 173.9 |
| J4 pins, 6 mm (USB ESD) | 27.2 / 137.9 | 29.1 / 140.2 | 29.1 / 140.2 | 59.2 / 140.7 | 27.3 / 138.3 | 76.8 / 190.6 | 59.2 / 140.7 |
| RTC1, 6 mm (clock) | 82.3 / 0.6 | 82.3 / 0.6 | 124.3 / 0.6 | 82.3 / 0.6 | 80.9 / 0.7 | 83.3 / 0.6 | 120.5 / 0.6 |

### G4. Crystal, BME280 and the bottom (`python3 needs2.py` -> `needs2.txt`)

- **#59**: free top area in the band under U1 where the crystal and C2/C3 would be rearranged (x 134-146, y 104.4-115, this study's window): 21.0 mm² today, 21.0 in A0, B1 and B3, 20.5 in B2, **87.0 in A1** and 82.2 in C1. Only the options that move BT1 off U1's lower side open this band. A strip added at an edge does not.
- **#57**: the free top spot for a 3.2 x 2.6 mm BME280 box that maximizes the smaller distance to U2 (FT231X) and U6 (TPS797). Today's U12 is 10.12 mm from U2 and 15.24 mm from U6 (same run; agrees with the earlier report's `constraints.txt`). Best spots: A0 and A1 at (125.4, 128.7), the new bottom-left corner below H1: 41.5 mm from U2, 39.0 (A0) or 35.4 (A1) from U6, 14.5 mm from the nearest SCL pad (J2.10). B1 at (190.0, 91.5), the new top-right corner: 40.8 from U2, 35.6 from U6, but 27.9 mm from the nearest SCL pad. B2 at (107.0, 118.5): 48.5 and 53.5 mm, 4.5 mm from SCL, but outboard of J2 on the cable side. C1 at (125.4, 123.7): 37.5 and 35.4 mm.
- **Bottom outside J1** (free bottom area, same runs): 546.1 mm² today; 1069.2 (A0), 1088.6 (B1), 1077.6 (C1). The amounts match because the added area matches; the place differs. Taller adds a full-width strip below J1's pad row (J1 pads end at y 116.37, the new bottom edge is at 130.44), directly under J1's VDD pin (142.36, 115.62), BT1 and the J2 I2C pins. Longer adds a block at one end only, beside J3 and the power cluster (B1) or between J2 and J1 (B2).

### G5. Terminal positions (`python3 terminals.py` -> `terminals.txt`)

Body length for n positions is (n-1) x 2.54 + 3.25 mm, the end allowance measured on J2 (26.11 mm for 10) and J3 (15.95 mm for 6); depth 6.75 mm; 0.15 mm to a keepout (proposal). The left edge is calibrated to today's J2, which overlaps H1's 5.56 mm screw-head circle by 0.59 mm.

| Edge | Today 50.1 x 30.4 | Taller 50.8 x 40.64 | Longer 68.58 x 30.4, right column out | Both 58.42 x 35.56 |
|---|---|---|---|---|
| Left (J2), holes kept | 10 | 10 above H1, plus 3 below it | 10 | 10, plus 1 below H1 |
| Left, H1 moved to the new corner (breaks the pair) | – | 14 | – | 12 |
| Right (J3) | 8 (6 used) | 12 | 11 (J4 and H2 no longer on this edge) | 13 |
| Bottom long edge | – (BT1, ISP1) | 16, in the added strip | 7, in the new band | 3, in the new band |
| Top long edge | – (SD, USB-C, H2) | – | 3, right of H2 | – |

A 12-position J3 on the taller board runs from below J4 to the new corner, which displaces U13 and C16-C18 from the column above today's J3. A bottom-edge block on the taller board takes 6.75 mm of the 10.24 mm the board gains, which is most of the relief.

### G6. WH-02 lid plate (`python3 wh02.py` -> `wh02.txt`)

Plate 54.41 x 78.74 mm, standoffs at (4.28, 13.33) and (50.13, 39.37), from the convenient-sizes report F3 (not re-measured here). The board may sit either way round on the two standoffs (a half turn maps the diagonal pair onto itself).

| Outline | 0° | 180° |
|---|---|---|
| Today | fits, 2.12 mm margin | fits, 2.12 |
| Taller 50.8 x 40.64 | fits, 0.93 mm margin (bottom edge) | fits, 1.49 (side); 26.97 mm spare in height |
| Taller, largest at 0° | 50.8 x 41.57, 0.00 mm | – |
| Longer 68.58 x 30.4, either end | overhangs by 16.29-16.31 mm | overhangs by 16.29-16.31 |
| Both 58.42 x 35.56 | overhangs by 6.13 mm | overhangs by 6.13 |
| Both, largest that fits | 52.29 x 41.57 (in effect the taller option) | |

Whether a board may overhang the plate inside the lid is UNVERIFIED (lid cavity not measured). WH-10 and WQ-48 locate by the hole pair with free room around it (convenient-sizes report F3), so every option that keeps the pair keeps those two.

### G7. The three options, block by block

**Taller only (50.8 x 40.64 mm).** The top edge stays: J1's card entry, J4, H2 and J2's first pin. The bottom edge moves down 10.236 mm and the right edge out 0.655 mm. H1 and H2 stay where they are, so H1 ends 12.39 mm above the new bottom edge, inside the J2 column. Blocks that stay: J2, MCU, USB/FT231X, I2C switch, ADC/reference, U12 (until #57 moves it), J1. Blocks that can move rigidly with the bottom edge, at Andy's choice: BT1 with C19 and D4; ISP1; U3, R10 and R2; J3 with Q1, U11, C12; U6. The new area is a 10.2 mm strip across the whole board (A0), or, with the lower row moved down (A1), a band at y 109-120 directly under U1, the crystal, RTC1 and the power cluster. A1 is the only case that changes the room at the crystal (21.0 to 87.0 mm²) and it more than doubles the room at the #66 nets (90.7 to 204.8 mm² top). ESD: J2's clamps and resistors gain room right of J2's lower pins (42.5 to 78.6 mm² top within 8 mm of J2), where BT1's left end was; J3's clamp gains 10.7 to 67.4 mm² top; J4's stays at about 29 mm² top and 140 mm² bottom (the room study already placed the USB array on the bottom behind J4).

**Longer only (68.58 x 30.404 mm).** Height stays at J2's 26.1 mm plus H1. One short edge moves 18.4 mm. At the right (B1), J3 and the column with U13, C16-C18, C5 and C6 move out; H2 stays and becomes an interior hole at the top, between J4 and the new corner. The band opens between the power cluster and J3, which is the best case here for #66 (248.7 mm² top) and the USB ESD (59.2), but it adds nothing at J2, U1 or the crystal, and it stretches VBAT+, VUSB, VREF, AX and 3V3_AUX, the nets #66 and the ADC care about. At the left (B2), J2 moves out and every J2 signal grows 18.4 mm; the band then holds J2's protection (150.6 mm² top within 8 mm of J2's pins) but nothing else that needs room. Splitting the board in the middle (B3) stretches 19 nets by 350.3 mm in total. Every longer variant overhangs the WH-02 lid plate by about 16.3 mm.

**Both (58.42 x 35.56 mm).** The bottom edge moves down 5.156 mm and the right edge out 8.275 mm. It gives the most room at the #66 nets (313.7 mm² top) and at J3 (79.5), nearly A1's room at the crystal (82.2), and 13 positions on the right edge. It overhangs the WH-02 lid plate by 6.13 mm; the largest "both" that fits the plate is 52.29 x 41.57 mm, which is the taller option.

### G8. Placement test: skipped

A greedy placement of the 27 parts into a rigidly moved board would test today's layout with a band in it, not the relaid v4 board that the 80 % density figure assumes, and the targets for the #66 parts depend on where Andy puts the power path. The free-area-within-reach table (G3) measures the same question, room beside the pins that need it, without pretending to be a layout. The earlier area report skipped it for the same reason.

### G9. Andy's two hypotheses, tested

These were offered as "not necessarily good ideas" and are treated as hypotheses.

**(1) Grow the long axis only, to get more screw terminals. Mostly wrong.** Terminals live on the short edges (J2 left, J3 right), and long-axis growth does not lengthen either one. What it does do is move the right edge away from J4 and H2, which frees the whole right edge: 11 positions there against 8 possible today (G5). It also opens 7 positions on the bottom long edge and 3 on the top, inside the new band, where they compete with the parts the band was meant for. Short-axis growth adds positions more directly: the right edge takes 12, the left edge 10 plus a 3-position block below H1 (holes kept) or 14 in one block (H1 moved), and the bottom long edge 16. The part of the hypothesis that holds: if the goal is one long, uninterrupted terminal row on a short edge with no USB-C or hole in the way, the longer board's right edge gives it (11). The price is the WH-02 lid plate (16.3 mm overhang, G6), 7 stretched nets (G3), and no new room at U1.

**(2) Grow the short axis only, keeping the mounting holes. Right.** H2 costs nothing: the top edge does not move, so H2 stays in its corner (2.8 mm from the right edge instead of 2.14). H1 is the cost. It stays at (125.59, 118.05), 12.39 mm above the new bottom edge, in the J2 column. Its 5.56 mm screw-head disc (24.3 mm², computed) blocks a continuous J2 extension (10 + 3 rather than 14 positions), splits the new strip's left end, and makes the J2 lines that run down into the strip (SDA_EXT at J2.9, SCL at J2.10) pass right of x 128.4. That is a small and local cost: the corner that H1 vacates was unusable anyway, and the disc's area is the same as today. What it buys: the WH-02 lid plate still fits (0.93 mm margin at 0°, 1.49 mm at 180°), and the WH-10 and WQ-48 plates still locate the board. No longer or "both" option keeps the WH-02 lid. Every option needs a new `StencilMount_Margay` pocket.

## Recommendation

**Grow taller only: 50.8 x 40.64 mm (2.0 x 1.6 in). The bottom edge moves down 10.236 mm and the right edge out 0.655 mm; the top edge, J1's card entry, J4, H2 and both holes stay.** In the v4 layout, move BT1 (with C19 and D4) down into the new strip, and slide J3 (with Q1, U11, C12) down the lengthened right edge.

Reasons, in order:
1. It is the only direction that puts new room next to the crowded U1/J2 region: once BT1 leaves U1's lower side, the band under U1 grows from 21.0 to 87.0 mm² (#59), the room by J2's pins from 42.5 to 78.6 mm² (J2 ESD), and the room at RTC1 from 82.3 to 124.3 mm². Longer boards leave all three unchanged.
2. It still more than doubles the room at the #66 power nets (90.7 to 204.8 mm² top) and gives J3's clamp 67.4 mm² against 10.7.
3. It stretches nothing until Andy chooses to move a block (A0: 0 nets), and the rigid version (A1) adds at least 10.24 mm to 15 nets, against 18.4 mm on 7-19 nets for the longer variants. No option shortens today's long nets by itself: they are long because their ends sit at opposite short edges (G2), and only the longer options pull those edges farther apart.
4. #57 gets a corner 41.5 mm from U2 and 35-39 mm from U6 (today 10.12 and 15.24), 14.5 mm from J2's SCL pin.
5. The bottom gains a full-width strip under J1's pad row, beside J1's VDD pin and below BT1, for the iron-friendly parts.
6. It keeps the diagonal hole pair and every mount, including the WH-02 lid plate, and the right edge can carry up to 12 terminal positions.

**The case against it.**
- The new area arrives at the bottom edge, not at U1. The gain at U1, the crystal and J2 is real only if BT1 moves; if the coin cell has to stay where it is, A0's numbers apply and the crystal band is unchanged (21.0 mm²).
- The power cluster gains less than on a longer board with its band at the right (204.8 against 248.7 mm² top) or the "both" shape (313.7), and USB ESD at J4 gains nothing (29 mm² top either way; the bottom behind J4 has about 140 mm² in every option).
- Moving the lower row stretches 3V3, 3V3_AUX, RST, VREF and the ISP lines by at least 10 mm each (A1), unless ISP1 stays put.
- H1 becomes an interior hole in J2's column and caps a continuous J2 at 10 positions.
- The WH-02 lid margin at 0° shrinks from 2.12 to 0.93 mm, and whether the lid cavity takes the board is UNVERIFIED.
- The aspect ratio moves from 1.65 to 1.25 (computed), farther from the Feather-like strip some users may expect.

**What Andy has to decide.**
1. Whether BT1 moves to the new strip, which is the move the recommendation rests on.
2. Whether J3 slides down, grows (up to 12 positions, displacing U13 and C16-C18 from above it), or stays and leaves the right edge free for the power path.
3. Whether more terminal positions are wanted at all, and where: the right edge (cheap), a 3-position block below H1, or a bottom-edge row (which uses most of the relief).
4. Whether 0.93 mm on the WH-02 lid plate is enough, or the board should be mounted at 180° (1.49 mm, with 27 mm of spare height).
5. The exact height: 40.64 mm (0.1 in grid, 1955 mm² usable) or anything up to 41.57 mm, the WH-02 plate's limit at 0°.

## Sources and runs

- `cp Project-Margay/Hardware/KiCAD/Margay.kicad_pcb tools/margay-growth/` (ca24e31; sha1 d82cf620e445de7cf0c491074fadc09e178d4003 on both, checked). Nothing in Project-Margay or nw-cold-silicon was modified; the copy was only read, never saved.
- `python3 fps.py` -> `fps.txt`, `fps.json`: every footprint's side, position, box and nets.
- `python3 blocks.py` -> `blocks.txt`.
- `python3 nets.py TX_EXT RX_EXT ... GND` -> `nets.txt`: per-net routed length and vias.
- `python3 scenarios.py` -> `scenarios.txt`, `scenarios.json`, `occ_*_top.npy`, `occ_*_bot.npy`.
- `python3 needs2.py` -> `needs2.txt` (it re-runs `scenarios.py` on import, so `needs2.txt` repeats that output before its own lines).
- `python3 terminals.py` -> `terminals.txt`. First version gave 9 positions for today's left edge against J2's 10 (a guessed overlap allowance); recalibrated to today's J2 body and re-run.
- `python3 wh02.py` -> `wh02.txt`.
- Documents read: `margay-v4-board-size.md`, `margay-v3.1-room-study.md`, `sources/2026-11-12-margay-larger-board-area-agent-report.md`, `sources/2026-11-12-margay-convenient-sizes-agent-report.md`, `tools/margay-room31/occ.py`, `place31.py`, `tools/margay-larger/parts_v4.json`.
- GitHub, read only: `gh issue list -R NorthernWidget/Project-Margay --milestone v4.0.0`; `gh issue view 57|59|66 --json body,comments`. Plain `gh issue view N --comments` printed nothing in this shell (dead end); the JSON form worked.
- Not done: the optional placement test (G8). ESD parts were located by room only, not designed.

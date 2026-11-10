# Passive parts on Okapi and Margay: the numbers, the slips, and what could merge

2026-11-05. Sources: Okapi, the partlist inside `Hardware/Okapi_2024-11-02.zip`
(`CAMOutputs/Assembly/Okapi.txt`, Bobby's export of 2024-11-02, 117 of 122 rows
with a manufacturer number) read against `Hardware/Okapi.sch`'s nets; Margay,
`Production/Margay_BoM_3v0_-_2026-11-04.csv`. Every number below is pasted from
those files. A merge is a proposal; nothing here is changed.

## Both boards from the KiCad export (2026-11-10): the current lines

Read from fresh `kicad-cli sch export netlist` runs on Project-Okapi 3a981d2
(`Hardware/KiCAD-10import`) and Project-Margay 5b5d358 (`Hardware/KiCAD`, v3.1).
These supersede the resistor tables below, which are kept as the record of how
the lines got here. Every position carries a part number.

| | Okapi | Margay | Both boards |
|---|---|---|---|
| Resistor positions | 87 | 26 | 113 |
| Resistor part numbers | 26 | 6 | 26 (Margay's six are all on Okapi's list) |
| Resistor values | 23 | 5 | 23 |
| Capacitor positions | 50 | 20 | 70 |
| Capacitor part numbers | 9 | 5 | 10 |
| Capacitor values | 8 | 4 | 9 |

The 23 resistor values are 19 standard values, 0 Ω and three shunts; #46 retires
143 kΩ in v0.8.0, leaving 18 standard values. The export counts 24 values across
both boards only because Margay spells 5.1 kΩ "5.1K" and Okapi "5.1k"; it is one
part number. Capacitors go to 14 part numbers with every proposal in
`capacitors.md` and to 12 with the merges filed (Okapi #49, #50; Margay #68).

Resistors, one row per part number and package. "0402 0603" is the dual land
(nw-cold-silicon R0402_0603); the fitted part is the primary's size. The shunts
(R10, R72 to R75) and R22 have no secondary yet (C10: the shunts' land check; R22
retires with #46).

| Value | Package | Okapi | Margay | Primary | Digi-Key | Secondary | Digi-Key |
|---|---|---|---|---|---|---|---|
| 0 | 0402 | R51 | – | ERJ-2GE0R00X (Panasonic) | P0.0JCT-ND | RC0402JR-070RP (Yageo) | YAG1279CT-ND |
| 3m | 0805 | R10 | – | PMR10EZPFV3L00 (Rohm) | RHM.003AJCT-ND | – | – |
| 20m | 0805 | R72, R73, R75 | – | ERJ-6BWFR020V (Panasonic) | P.02AQCT-ND | – | – |
| 50m | 0805 | R74 | – | ERJ-6BWFR050V (Panasonic) | P17581CT-ND | – | – |
| 5.1K | 0402 | – | R31, R32 | RC0402FR-075K1L (Yageo) | 311-5.10KLRCT-ND | ERJ-2RKF5101X (Panasonic) | P5.10KLCT-ND |
| 27 | 0402 | R11, R34, R35 | R3, R4 | RC0402FR-0727RL (Yageo) | YAG3086CT-ND | ERJ-2RKF27R0X (Panasonic) | P27.0LCT-ND |
| 100R | 0402 | R14 | – | RC0402FR-07100RL (Yageo) | 311-100LRCT-ND | RMCF0402FT100R (Stackpole) | RMCF0402FT100RCT-ND |
| 220R | 0402 | R9, R53, R60, R64, R76 to R80 | – | CRGCQ0402F220R (TE) | A129619CT-ND | RC0402FR-07220RL (Yageo) | 311-220LRCT-ND |
| 232 | 0402 | R26 to R29 | – | RC0402FR-07232RL (Yageo) | YAG3063CT-ND | RMCF0402FT232R (Stackpole) | RMCF0402FT232RCT-ND |
| 330 | 0402 | R36 to R40, R42 to R44 | R5 to R9, R11 to R13 | RC0402FR-07330RL (Yageo) | 311-330LRCT-ND | ERJ-2RKF3300X (Panasonic) | P330LCT-ND |
| 464 | 0402 | R30 to R33 | – | RC0402FR-07464RL (Yageo) | 311-464LRCT-ND | ERJ-2RKF4640X (Panasonic) | P464LCT-ND |
| 1k | 0402 | R12, R15 | – | RC0402FR-071KL (Yageo) | 311-1.00KLRCT-ND | ERJ-2RKF1001X (Panasonic) | P1.00KLCT-ND |
| 1k | 0402 0603 | R48 | – | RC0402FR-071KL (Yageo) | 311-1.00KLRCT-ND | ERJ-2RKF1001X (Panasonic) | P1.00KLCT-ND |
| 5.1k | 0402 | R81 to R85 | – | RC0402FR-075K1L (Yageo) | 311-5.10KLRCT-ND | ERJ-2RKF5101X (Panasonic) | P5.10KLCT-ND |
| 10k | 0402 | R24, R25, R41, R45 to R47, R52, R54, R67, R86, R87 | R1, R2, R14 to R21 | RC0402FR-0710KL (Yageo) | 311-10.0KLRCT-ND | ERJ-2RKF1002X (Panasonic) | P10.0KLCT-ND |
| 10k | 0603 | R49, R50 | R22 to R24 | CRT0603-BY-1002ELF (Bourns) | CRT0603-BY-1002ELFCT-ND | RG1608P-103-B-T5 (Susumu) | RG16P10.0KBCT-ND |
| 91k | 0603 | R16 | – | ERJ-3EKF9102V (Panasonic) | P91.0KHCT-ND | RC0603FR-0791KL (Yageo) | 311-91.0KHRCT-ND |
| 100k | 0402 | R18, R19, R23, R57, R58, R61, R63 | – | RC0402FR-07100KL (Yageo) | 311-100KLRCT-ND | ERJ-2RKF1003X (Panasonic) | P100KLCT-ND |
| 100k | 0402 0603 | R69 | – | RC0402FR-07100KL (Yageo) | 311-100KLRCT-ND | ERJ-2RKF1003X (Panasonic) | P100KLCT-ND |
| 130k | 0603 | R20 | R10 | ERJ-3EKF1303V (Panasonic) | P130KHCT-ND | RMCF0603FT130K (Stackpole) | RMCF0603FT130KCT-ND |
| 143k | 0402 0603 | R22 | – | RC0603FR-07143KL (Yageo) | 311-143KHRCT-ND | – | – |
| 180k | 0402 | R5, R7, R65, R66 | – | RC0402FR-07180KL (Yageo) | 311-180KLRCT-ND | ERJ-2RKF1803X (Panasonic) | P180KLCT-ND |
| 180k | 0603 | R1, R8, R13 | – | ERJ-3EKF1803V (Panasonic) | P180KHCT-ND | RMCF0603FT180K (Stackpole) | RMCF0603FT180KCT-ND |
| 200k | 0402 0603 | R70 | – | ERJ-2RKF2003X (Panasonic) | P200KLCT-ND | RC0402FR-07200KL (Yageo) | 311-200KLRCT-ND |
| 330k | 0603 | R3, R17, R62 | – | ERJ-3EKF3303V (Panasonic) | P330KHCT-ND | RMCF0603FT330K (Stackpole) | RMCF0603FT330KCT-ND |
| 820k | 0603 | R6 | – | RC0603FR-07820KL (Yageo) | 311-820KHRCT-ND | ERJ-3EKF8203V (Panasonic) | P820KHCT-ND |
| 1M | 0402 | R55, R56, R59, R68 | – | RC0402FR-071ML (Yageo) | 311-1.00MLRCT-ND | ERJ-2RKF1004X (Panasonic) | P1.00MLCT-ND |
| 1M | 0402 0603 | R71 | – | RC0402FR-071ML (Yageo) | 311-1.00MLRCT-ND | ERJ-2RKF1004X (Panasonic) | P1.00MLCT-ND |
| 1M | 0603 | R21 | – | ERJ-3EKF1004V (Panasonic) | P1.00MHCT-ND | RC0603FR-071ML (Yageo) | 311-1.00MHRCT-ND |
| 1.62M | 0603 | R2, R4 | – | CRCW06031M62FKEA (Vishay) | 541-1.62MHCT-ND | RC0603FR-071M62L (Yageo) | 13-RC0603FR-071M62LCT-ND |

## Okapi resistors: value against the number ordered

*Superseded by the 2026-11-10 export table above; kept as the record.*

The 2024 build ordered what the number says, not what the schematic says, as
Margay's R7/R9 and R19 did. Rows where the two differ:

| Refs | Schematic | Ordered | What it is |
|---|---|---|---|
| R26, R27, R28, R29 | 287R | RC0402FR-07232RL, 232 Ω | ILIM resistors of U17 to U20 (the port power switches), one per switch, to GND |
| R30, R31, R32, R33 | 287R | RC0402FR-07453RL, 453 Ω | the second ILIM resistor of each, in parallel through JP1 to JP4 |
| R36, R37, R38, R39, R40, R42, R43, R44 | 330, 0402 | RC0603FR-07330RL, an 0603 part | LED series (D4, D5) and the FT231X UART series (R38, R40); Margay's R7/R9 slip |
| R54 | no value | RC0402FR-0710KL, 10 k | RST_TRIG pull-down (Q4's gate) |
| R84, R85 | no value | RC0402FR-075K1L, 5.1 k | USB-C CC pull-downs |
| R86, R87 | no value | RC0402FR-0710KL, 10 k | Feather !RST and !MODE pull-ups |
| R51 | no value | no number | PAC1934 ADDR_SEL to GND |
| R72, R73, R74, R75 | no value | no number | PAC1934 sense shunts, 0805 (Project-Okapi #21) |

Only the 287R rows are a question of which value is right; the rest are a
value field to fill from the number, or a number to choose (R51, R72 to R75).

## Okapi resistors: the lines, and what could merge

*Superseded by the 2026-11-10 export table above; kept as the record.*

Thirty-five lines on the 2024 partlist. Grouped by value, with the package and
the role from the nets:

| Value | Lines | Refs and roles | Could merge? |
|---|---|---|---|
| 10 k | 0402 Yageo ×8 (two Digi-Key codes), 0603 ERA-3AEB103V ×2 | pull-ups and pull-downs; R49, R50 are 0.1 % parts to GND behind JP6, JP7 | R49/R50 to the 0402 line unless the 0.1 % is meant (a divider option) |
| 100 k | 0402 ×6, 0603 ×1 (R69) | pull-ups; R69 with R22 143 k is the LT3652 VIN_REG divider | R69 to 0402: a footprint change |
| 180 k | 0402 ×2 (R65, R66), 0603 Panasonic ×4 (R1, R5, R7, R8) | R65/R66 VBUS pull-downs; R1/R8 pull-ups to 5V_AUX; R5/R7 feedback dividers of U1 and U2 | one line in one package: four or two footprint changes; all are 1 % |
| 1 M | 0402 ×4, 0603 Panasonic ×1 (R71) | pull-ups; R71 with R70 200 k on the LT3652 SHDN | R71 to 0402: a footprint change |
| 330 | 0402 ×8 (+R9 0402 on its own line by its 0402 number), 0603 ×1 (R48, 5V_AUX to VREF) | LED/UART series; R9 filters U5's VDD; R48 biases the reference | one 0402 line of 10 once the eight take the 0402 number; R48 to 0402 is a footprint change |
| 287R / 232 / 453 | 0402 ×4 + ×4 | ILIM of the four port switches | a value decision first (below) |
| 120 k | 0402 ×1 (R19) | FEATHER_EN pull-up to 3V3_CORE | could be 100 k: one line fewer, no cost |
| 130 k, 330 k | 0603 ×1 each (R20, R62) | TPL5111 DELAY: R20 fixed, R62 the JP8 alternative, above the part's 170 k maximum (DECISIONS Okapi 3) | R62 to 130 k (one line fewer) or to a second in-range interval |
| 220R | 0402 TE ×8 | PCA9634 LED anodes | fine |
| 5.6 k | 0402 ×3 | Feather RGB | fine |
| 27 | 0402 ×2 | USB D+/D− | fixed by the FT231X |
| 20, 100R, 1 k, 2 k, 3 m | 0402, 0805 | the BQ charger U5's network (R11, R14, R12, R15, R10) | fixed by the datasheet |
| 91 k, 182 k, 360 k, 820 k, 1.62 M ×2, 143 k, 200 k, 470 k | 0603 | regulator and MPPT dividers (U1, U2, U3, U4) | fixed by the designs; a review item (#22) says the regulator dividers are too high-impedance |
| no value | R51, R72 to R75 | PAC1934 | #21 |

The arithmetic: 35 lines today; the eight 0402 330 Ω taking their 0402 number
removes none (they join R9's line only if R9's line is the same number, which
it is); the package merges (R69, R71, R48, R1/R5/R7/R8 or R65/R66, R49/R50)
remove five lines at the cost of footprint changes on the board; R19 to 100 k
and R62 to 130 k remove two more for nothing. Floor about 27 lines without
touching the dividers.

## Okapi resistors, planned for v0.7.0 (2026-11-06)

*Superseded by the 2026-11-10 export table above; kept as the record.*

The 2024 partlist with every decision through A5 applied (DECISIONS A2 to A4,
#20, #32 to #35). Pending items are marked; everything else is a B1 field edit
or a filed footprint change. Counts are parts; a value in two packages is two
lines.

| Value | Package | Count | Number | Refs | Change from 2024 |
|---|---|---|---|---|---|
| 0 Ω | 0402 | 1 | RC0402JR-070RL | R51 | new value: PAC1934 address 0x10 (A3) |
| 20 mΩ, 0.5 W | 0805 | 3 | ERJ-6BWFR020V | R72, R73, R75 | new value: PAC1934 shunts (A3) |
| 50 mΩ, 0.5 W | 0805 | 2 | ERJ-6BWFR050V | R74, and the restored charger sense resistor of #32 (new designator) | new value (A3); #32 names ERJ-L06KF50MV and needs the 0.5 W part instead |
| 3 mΩ | 0805 | 1 | PMR10EZPFV3L00 | R10 | BQ2980 sense; the number was in Eagle all along (B1 export, 2026-11-06) |
| 20 Ω | 0402 | 1 | RC0402FR-0720RL | R11 | – |
| 27 Ω | 0402 | 2 | RC0402FR-0727RL | R34, R35 | – |
| 100 Ω | 0402 | 1 | RC0402FR-07100RL | R14 | – |
| 220 Ω | 0402 | 8 | CRGCQ0402F220R (TE) | R53, R60, R64, R76 to R80 | the number was in Eagle all along (B1 export, 2026-11-06) |
| 232 Ω | 0402 | 4 | RC0402FR-07232RL | R26 to R29 | value field from 287R (A2) |
| 330 Ω | 0402 | 9 | RC0402FR-07330RL | R9, R36 to R40, R42 to R44 | eight take the 0402 number; one line instead of three |
| 464 Ω | 0402 | 4 | RC0402FR-07464RL | R30 to R33 | value field from 287R; 464 Ω in place of the 2024 files' 453 Ω so that 232 ∥ 464 = 154.7 Ω is inside the MIC2544's 154 Ω floor (A2, 2026-11-06); Digi-Key 311-464LRCT-ND |
| 1 kΩ | 0402 | 2 | RC0402FR-071KL | R12, R48 | R48 from 330 Ω 0603 (A4, 2026-11-06); its pads take 0603 or 0402 so a user can fit 330 Ω for more reference current |
| 2 kΩ | 0402 | 1 | RC0402FR-072KL | R15 | – |
| 5.1 kΩ | 0402 | 2 | RC0402FR-075K1L | R84, R85 | value field from the number (B1) |
| 5.6 kΩ | 0402 | 3 | RC0402FR-075K6L | R81 to R83 | – |
| 10 kΩ | 0402 | 11 | RC0402FR-0710KL | R24, R25, R41, R45 to R47, R52, R54, R67, R86, R87 | R54, R86, R87 value fields from the number (B1); one Digi-Key code, not two |
| 10 kΩ, 0.1 % | 0603 | 2 | ERA-3AEB103V | R49, R50 | stays (#33) |
| 91 kΩ | 0603 | 1 | ERJ-3EKF9102V | R16 | – |
| 100 kΩ | 0402 | 7 | RC0402FR-07100KL | R18, R19, R23, R57, R58, R61, R63 | R19 from 120 kΩ (A4); the 120 kΩ line is gone |
| 100 kΩ | 0603 | 1 | RC0603FR-07100KL | R69 | stays 0603: MPPT pair, user-swappable (#20) |
| 130 kΩ | 0603 | 2 | RC0603FR-07130KL | R20, and the TPL5010 DELAY resistor of #35 | #35's value decided 2026-11-06: 130 kΩ, 66 min, as Margay's R10 |
| 143 kΩ | 0603 | 1 | RC0603FR-07143KL | R22 | stays 0603: MPPT pair (#20) |
| 180 kΩ | 0402 | 4 | RC0402FR-07180KL | R1, R8, R65, R66 | R1, R8 from 0603 (#33) |
| 180 kΩ | 0402 | (2 more, on the line above) | RC0402FR-07180KL | R5, R7 | decided and done 2026-11-06 (Andy: no downside): 0402, Project-Okapi 9fc83f9 |
| 182 kΩ | 0603 | 1 | ERJ-3EKF1823V | R13 | – |
| 200 kΩ | 0603 | 1 | RC0603FR-07200KL | R70 | – |
| 330 kΩ | 0603 | 1 | ERJ-3EKF3303V | R17 | R62 removed with JP8 (#34) |
| 360 kΩ | 0603 | 1 | RC0603FR-07360KL | R3 | – |
| 470 kΩ | 0603 | 1 | RC0603JR-07470KL | R21 | – |
| 820 kΩ | 0603 | 1 | RC0603FR-07820KL | R6 | 5 % to 1 % for 3V3_AUX (Andy, 2026-11-06; d7504ee) |
| 1 MΩ | 0402 | 5 | RC0402FR-071ML | R55, R56, R59, R68, R71 | R71 from 0603 (#33) |
| 1.62 MΩ | 0603 | 2 | RMCF0603FT1M62CT-ND | R2, R4 | – |

Totals: 88 resistors (77 valued in 2024, plus the ten that had no value, plus
#32's, plus #35's, minus R62) on 31 lines against 34, with R5/R7
pending; merged to 0402 they make 30. Lines
removed: the 0603 330 Ω eight, R48's 330 Ω 0603, R71's 1 MΩ 0603,
the 120 kΩ. Lines added: 0 Ω, 5.1 kΩ, 20 mΩ, 50 mΩ. The 5.1 kΩ and 10 kΩ
additions were always on the board; they were missing from the 2024 export
because their value fields were empty.

## Okapi capacitors

Thirteen lines on the 2024 partlist.

| Value | Package | Refs | Number | Note |
|---|---|---|---|---|
| 0.1 µF | 0402 | 17 parts | GCM155R71C104KA55D | Murata X7R 16 V; the same part Margay uses |
| 0.22 µF | 0402 | C15, C16 | GRT155R61E224KE01D | |
| 12 pF | 0402 | C23, C24 | CGA2B2C0G1H120J050BA | TDK 0402 C0G |
| 12 pF | 0402 | C40, C41 | CL10C120JB8NNNC | **a Samsung 0603 number on 0402 pads** (CL10 = 0603); merge into C23/C24's line |
| 1 µF | 0402 | C42 | CL10B105MO8NNWC | **an 0603 number on an 0402 pad** (#28's "C42 mismatch"); an 0402 1 µF part, or the pad to 0603 |
| 1 µF | 0603 | C11, C13 | TMK107B7105KA-T | Taiyo Yuden, Margay's part |
| 4.7 µF | 0603 | C18 | GRM188R61C475KAAJD | |
| 4.7 µF | 0805 | C1 | C0805C475K4RACTU | two packages for one value: C1 to 0603 is a footprint change |
| 10 µF | 0805 | C3, C4, C14, C22, C30 | GRM21BR61C106KE15K | Margay's part |
| 22 µF | 0805 | 7 parts | GRM219R61C226ME15L | |
| 68 pF | 0402 | C6 | 885012005060 | Würth |
| 100 µF | 1206 tantalum | C43 | TL8A0107M010D | |
| 220 µF | 2917 tantalum | C5 | TPSY227K010R0100 | |

Two slips to fix (C40/C41, C42), one merge for free (the 12 pF lines), one
package merge (4.7 µF) at a footprint change. Thirteen lines to ten.

## Margay capacitors

Five lines, no two of one value, every number the right package. Nothing to
merge. The only thing that could move is the pair of crystal values, 12 pF
(C7, C8) and 18 pF (C2, C3), if #54's check of the crystal's CL changes one of
them.

## Margay resistors

*Superseded by the 2026-11-10 export table above; kept as the record.*

Done 2026-11-04: six lines, floor five (DECISIONS Margay 13).

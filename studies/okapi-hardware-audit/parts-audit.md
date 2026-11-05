# Passive parts on Okapi and Margay: the numbers, the slips, and what could merge

2026-11-05. Sources: Okapi, the partlist inside `Hardware/Okapi_2024-11-02.zip`
(`CAMOutputs/Assembly/Okapi.txt`, Bobby's export of 2024-11-02, 117 of 122 rows
with a manufacturer number) read against `Hardware/Okapi.sch`'s nets; Margay,
`Production/Margay_BoM_3v0_-_2026-11-04.csv`. Every number below is pasted from
those files. A merge is a proposal; nothing here is changed.

## Okapi resistors: value against the number ordered

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

Done 2026-11-04: six lines, floor five (DECISIONS Margay 13).

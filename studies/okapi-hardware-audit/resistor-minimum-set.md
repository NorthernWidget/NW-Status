# Resistors across Okapi (v0.8.0 plan) and Margay (KiCad v3.1): a minimum set of values

2026-11-09. Andy's question: the smallest set of resistor values that keeps every chip on both
boards running as well as possible, without favoring a value because it is already fitted.
Method: one constraint per position (a range, or a divider equation with a tolerance), each
marked D (datasheet) or P (proposal, Andy to review); an integer program (pulp/CBC) over the
E24 and E96 values picks the fewest distinct values, E24 preferred on ties. The constraints are
in `tools/resistor_minimum_set.py`; the first run's output is
`sources/2026-11-09-resistor-minimum-set-run1.txt`.

Held outside the set (fixed by function): 0 Ω (R51), the shunts 3 mΩ (R10), 20 mΩ (R72, R73,
R75), 50 mΩ (R74, #32), and the 0.1 % 10 kΩ (Okapi R49/R50, Margay R22-R24; one part to choose
for both). R48 is 1 kΩ by Andy's decision; 1 kΩ is in the set. (Superseded: run 1's script listed R48 but never
constrained it, and 1 kΩ came into the set on its own. Run 2 holds it.)

## Run 1: 10 values, optimal

24 Ω, 220 Ω, 560 Ω, 1 kΩ, 5.6 kΩ, 68 kΩ, 124 kΩ (E96), 169 kΩ (E96), 300 kΩ, 620 kΩ.
Checked by hand:
- TLV61220 620k/68k: 5.06 V. TPS62822 300k/68k: 3.25 V. LT3652 float 169k/620k: 4.200 V, with
  R13 = 124k making R13 + R16||R17 = 257 k. ILIM 220 Ω: 1.05 A; with 560 Ω in parallel, 158 Ω,
  1.46 A. SHDN 620k/124k: 7.2 V. LBI 620k/124k: 3.0 V (edge of the range). MPPT 169k/124k:
  6.38 V (below the P106's 6.5 V Vmp).

Couplings the table does not model, which run 1 breaks or strains:
1. **C6, the TPS62822's feed-forward capacitor, depends on R7** (12 µs / R2: 68 pF at 180 k).
   With R7 = 68 k it wants about 180 pF, a new capacitor line.
2. **USB-C Rd 5.6 kΩ** sits at +9.8 % of 5.1 kΩ under my ±10 % assumption; the USB-C
   tolerance is unverified, and with 1 % parts it may fall outside. Likely fix: hold Rd at 5.1 k.
3. **The timer at 124 kΩ** shortens the 66-minute interval by an amount not yet computed from
   the TPL5111/TPL5010 equation (Andy chose 66 min, "at least for now").
4. **MPPT 6.38 V** is below the P106's maximum-power point; LBI at 3.0 V is at the edge.
5. **Status LEDs at 220 or 560 Ω** change brightness on both boards.
6. Almost every resistor on both boards changes value, Margay's included.

## Run 2: the trade between values and changed positions

`tools/resistor_minimum_set_run2.py` models every position with its current value, read from
the KiCad netlists (101 positions: 78 on Okapi, 23 on Margay; the shunts, 0 Ω, the 0.1 % parts and R62,
which leaves with JP8 in #34, are excluded). It holds what run 1 broke: Rd at 5.1 kΩ; R7 at 180 kΩ, which keeps C6 at 68 pF; the
timer at 130 kΩ, which TPL5010 Equation 1 (set 5) puts at 3943 s, 65.7 min (124 kΩ gives 59.0
min); MPPT at 6.4-6.7 V; and R48 at 1 kΩ. For each cap on the number of values, it finds the
fewest changed positions. Outputs: `sources/2026-11-09-resistor-minimum-set-run2-float4200.txt`
and `-float4210.txt`.

The floor is still 10 values, at 70 changed positions on both boards. The check: with the float
window opened to 4.210 V, the as-built boards satisfy every constraint and the solver returns
22 values with 0 changes. The as-built float, 3.3(1 + 91k/330k), is 4.210 V, outside the
4.178-4.200 V window I proposed; holding 4.200 V costs one change, R16 91k to 88.7k (4.187 V).

| Values | Changed (float 4.210 V) | Changed (float 4.200 V) |
|---|---|---|
| 10 | 70 | 70 |
| 11 | 47 | 47 |
| 12 | 31 | 31 |
| 13 | 23 | 23 |
| 14 | 16 | 16 |
| 15 | 12 | 12 |
| 16 | 8 | 9 |
| 17 | 6 | 7 |
| 18 | 4 | 5 |
| 19 | 3 | 4 |
| 20 | 2 | 3 |
| 22 | 0 | 1 |

From 16 values up, every change is on Okapi and none touches a pull-up's current. With the float
as built, the 16-value option changes eight positions, each checked by hand:
- R21 470k to 1M: the LTC4412 STAT pull-up still meets R ≥ 420 k.
- R13 182k to 180k: R13 + R16||R17 = 251.3 k against 253.3 k now.
- R15 2k to 1k: BQ298000 RPACK ≤ 2 kΩ; this is proposal D.
- R14 100 to 220: BQ298000 RCTR, 100 Ω typical; 220 Ω is inside my proposed 47-220 Ω.
- R22/R69 143k/100k to 130k/91k: MPPT 6.557 V against 6.561 V now.
- R71/R70 1M/200k to 1.62M/330k: SHDN start 7.09 V against 7.20 V now.

That leaves 27, 220, 232*, 330, 464*, 1k, 5.1k, 10k, 91k, 100k, 130k, 180k, 330k, 820k, 1M, and
1.62M* (* = E96). Below 16 the changes reach the weak pull-ups (R55, R56, R59, R68 from 1 MΩ to
100-180 kΩ), the LBI threshold, and the float divider, and from 12 down the status-LED
brightness on both boards.

Not modeled: static current. The 10-100 kΩ range for logic pull-ups treats a 10 kΩ pull-up on
a held-low line (FEATHER_EN, ~LED_EN) as free, at 330 µA. Every option of 16 values or more
leaves those positions alone, but a cut below 16 needs that constraint first.

For Andy: (1) whether 4.210 V float stands or R16 goes to 88.7k; (2) which point on the table;
(3) R14 at 220 Ω and R15 at 1 kΩ, which ride with the 18-value option and below.

## Run 3 and Andy's review of the 16-value option (2026-11-09)

Run 3 widened every LED position to 100 Ω-10 kΩ (`ledwide`): with the float at 4.200 V the
changed-position count is identical to run 2 at every cap from 10 to 22
(`sources/2026-11-09-resistor-minimum-set-run3-ledwide-float4200.txt`), so LED brightness was
never what set the minimum. Andy: the LEDs must be visible outdoors. The rule going forward
(proposal): each LED position keeps its current value or goes lower, never dimmer.

Andy on the 16-value option:
- R21 470k to 1M: approved.
- R13 182k to 180k: approved.
- R15 2k to 1k: uncertain, leaning no; held at 2k and kept open (proposal D).
- R22/R69 (MPPT) and R71/R70 (SHDN start): set from the solar panels Okapi is likely to use,
  not from the value count. An agent surveys the panels:
  `sources/2026-11-09-solar-panels-agent-report.md`.

## Run 4: with Andy's decisions held

Holds R21 at 1 MΩ, R13 at 180 kΩ and R15 at 2 kΩ; MPPT and SHDN as built (143k/100k, 1M/200k)
until the panel survey; every LED at its current value or lower. The floor rises to 15 values.
Outputs: `sources/2026-11-09-resistor-minimum-set-run4-*.txt`.

| Values | Changed (float 4.210 V) | Changed (float 4.200 V) | What the last value removed costs |
|---|---|---|---|
| 20 | 2 | 3 | R21 and R13, both approved (and R16 88.7k for 4.200 V) |
| 19 | 3 | 4 | R14 100 to 220 Ω |
| 18 | 6 | 6 | R3, R16, R17: LBI 2.72 V (2.67 V at 4.200), float 4.204 V (4.182 V) |
| 17 | 14 | 14 | ILIM 232/464 to 220/560: 1.045 A, 1.456 A on the jumper |
| 16 | 30 | 30 | status LEDs 330 to 220 Ω and UART series on both boards |
| 15 | 51 | 51 | 10 kΩ pull-ups to 100 kΩ on both boards |

The approved changes alone take the boards from 22 values to 20. The 18-value step undoes the
LBI threshold set this morning (R3 330k, 2.95 V).

## v0.8.0 charger dividers (Andy, 2026-11-09)

MPPT R22/R69 = 1M/200k (16.2 V) and start R71/R70 = 1M/100k (13.2 V), for 10-20 W 12 V
panels (DECISIONS.md, Okapi design item 5). Against run 4's 20 values, 143k leaves the board
(R22 was its only position) and 200k and 100k trade places, so the v0.8.0 set is 19 values
with five changed positions: R21, R13, R22, R69, R70.

## Run 5: run 4 with the #46 dividers held

Confirms 19 values for five changes (R21, R13, R22, R69, R70) with the float as built; holding
4.200 V adds R16 88.7k for six. Outputs: `sources/2026-11-09-resistor-minimum-set-run5-*.txt`.

| Values | Changed (4.210 V) | The next value removed costs |
|---|---|---|
| 19 | 5 | – |
| 18 | 6 | R14 100 to 220 Ω |
| 17 | 9 | R3 330k to 374k, R16/R17 to 100k/374k: LBI 2.95 to 2.67 V, float 4.182 V |
| 16 | 17 | ILIM 232/464 to 220/560 Ω: 0.99 to 1.045 A, jumper 1.49 to 1.46 A |
| 15 | 33 | status LEDs 330 to 220 Ω and UART series, on both boards |

## Andy, 2026-11-09 (evening): R15, STAT, R51, the precision 10 kΩ

- **R51 (0 Ω) stays.** Proposal F, a copper tie, is declined.
- **Precision 10 kΩ for both boards: Panasonic ERA-3AEB103V** (0.1 %, ±25 ppm/°C, 0603 thin
  film, AEC-Q200), picked for the broadest sourcing. The Bourns CRT0603-BY-1002ELF has the same
  tolerance and TCR (B = 0.1 %, Y = ±25 ppm/°C). FindChips, 2026-11-09: ERA-3AEB103V on
  Newark (605,000 and 259,246 on two lines), RS, TME, Rutronik, LCSC and others, 6.29 M on
  all rows including brokers; CRT0603-BY-1002ELF at 150,302 on all rows (Newark 48,745 the
  largest). Digi-Key US shows ERA-3AEB103V at 0 with a 55-week factory lead time on the same
  day, so the Digi-Key code on the BoM should carry an alternate. Changes Margay R22-R24 at
  the Okapi/Margay merge; Okapi R49/R50 already carry it.
- **R15 and STAT:** discussed below; R15 held at 2 kΩ, STAT kept.

**R15 (BQ298000 RPACK, PACK pin on V_LI).** Table 8-1: maximum 2 kΩ, no minimum, "to protect
the PACK pin from a reverse charging current condition". It forms a divider with the internal
RPACK-VSS (100-550 kΩ, typical 300 kΩ), so PACK reads low by 15-82 mV at 4.2 V with 2 kΩ and
8-42 mV with 1 kΩ. The detection thresholds it feeds are 100 mV (charger removed), 400 mV (load)
and 700 mV (charger attached): neither value crosses one. 1 kΩ halves the offset and doubles the
current a reverse-voltage fault on PACK could drive; on Okapi PACK sits on V_LI beside an
on-board charger, so that fault takes a reversed cell. No measurable performance change either
way; held at 2 kΩ (Andy, leaning no), which keeps 2k as a value of its own.

**STAT (LTC4412, U7).** U7 drives Q5, the ideal diode from V_LI to V_BETA; USB reaches V_BETA
through D9. STAT sinks 10 µA (6-17 µA) when V_BETA is above V_LI by 20 mV, that is, when USB
rather than the cell carries the load. Today nothing reads it: R21 pulls it to V_BETA, and the
pin costs about 10 µA at 470 kΩ, 4.6 µA at 1 MΩ, only while on USB. Against keeping it: R68
already tells U41 (GPA0) that USB is present, and with D9 dropping 0.3-0.5 V USB wins over a
full cell nearly always, so STAT mostly repeats R68; the PAC1934's V_LI and V_BETA channels
show which source is supplying, when the PAC is read. For keeping it: STAT is the one signal
that says the cell is not supplying without powering and reading the PAC (a missing, dead or
disconnected cell while on USB), it is free in current off USB, and U41's GPA2 is unconnected.
To read it, STAT routes to GPA2 and R21 stays on V_BETA: the MCP23018's GPIO pins are rated
-0.6 to 5.5 V whatever its supply (absolute maximum ratings), which is how R68 already brings
VUSB_POWER into GPA0. (Superseded: an earlier line here moved R21 to 3V3_CORE; not needed.) At
1 MΩ the 10 µA sink pulls the pin fully low. Andy expects to
want it: Proposal A (remove R21) is withdrawn, and the read is a v0.8.0 candidate.

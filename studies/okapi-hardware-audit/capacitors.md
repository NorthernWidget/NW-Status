# Okapi capacitors: acceptable bounds per position

Started 2026-11-08. Goal (Andy): for every capacitor on Okapi, the bounds its circuit
accepts, read the way each datasheet states them, and our part's effective value at
its own voltage. Correct circuits first; merge lines only where a circuit is flexible.

## How datasheets state a capacitor requirement

1. **An explicit effective minimum** (newer datasheets, LDOs especially): the value
   must remain after DC bias, temperature, tolerance and aging. Example: TPS62822,
   "a minimum effective output capacitance of 5µF". Read: derate the chosen part with
   its maker's curve and compare. ADI AN-1099: worst case = DC-bias derating x
   temperature change x tolerance. TI SSZT654: DC bias "may reduce capacitance values
   by as much as 90%".
2. **A bare value, often with a reference part** ("at least 10 µF recommended",
   "10 µF ceramic required"): set by a design built and tested with particular parts,
   so their derating is baked in. Read: our part must deliver at least what the
   reference part delivers at the same voltage; with no reference part, the nominal
   value with ordinary margin. Example: TLV61220's design example uses a 10 µF 6.3 V
   0603 X5R (GRM188R60J106ME84D) at 3.3 V.
3. **An equation** (ripple, stability, hold-up): physics, so the effective value goes
   in. Examples: LT3652 C_IN(BULK) = I_CHG(MAX) (V_BAT/V_IN) / ΔV_IN; TLV61220
   C_OUT >= L/2 for L > 4.7 µH.
Maximums follow the same reading.

## Murata DC-bias data, 25 °C (effective µF)

From Murata's own characteristic data (the numeric curves behind pim.murata.com),
collected 2026-11-07; 3.3, 4.2 and 5.0 V linearly interpolated on a 0.08 V grid.

| Part | AC level | 0 V | 3.3 V | 4.2 V | 5.0 V | 8 V | 12 V | 16 V |
|---|---|---|---|---|---|---|---|---|
| GRM21BR61C106KE15 (10 µF 16 V X5R 0805) | 0.5 Vrms | 10.955 | 7.149 | 6.042 | 5.219 | 3.179 | 1.872 | 1.260 |
| GRM219R61C226ME15 (22 µF 16 V X5R 0805) | 0.5 Vrms | 20.276 | 11.489 | 9.136 | 7.577 | 4.472 | 2.839 | 2.104 |
| GRM188Z71C475KE21 (4.7 µF 16 V X7R 0603) | 1 Vrms | 4.700 | 3.574 | 3.084 | 2.695 | 1.701 | 1.091 | 0.786 |

Temperature at 0 V: GRM21B -3.5 % at -40 °C, -6.3 % at +85 °C; GRM219 -6.6 % and
-13.8 % (measured at 0.15 Vrms); GRM188Z7: no curve published.

Solar-input candidates (rating at least 35 V): TDK CNA6P1X7R1H106K250AE and
CNC6P1X7R1H106K250AE (10 µF 50 V X7R 1210, AEC-Q200, soft termination; 445-180367-1-ND
13,196 and 445-181655-1-ND 21,000 on Digi-Key 2026-11-07): about 9.06 µF at 8 V,
7.89 at 12 V, 5.67 at 20 V, 3.46 at 32 V, interpolated between TDK's published points
(0, 4, 6.3, 10, 16, 25, 35, 50 V). No 22 µF part at 35 V or more was both in stock and
published with data. Murata X7S 1210s hold more at 32 V (4.2 to 4.8 µF) but 59 or 0
were in stock. Not reachable: Samsung's data pages (server error) and Taiyo Yuden's
(a terms dialog not accepted without Andy's OK).

## Findings that change the design (2026-11-08, verified against the netlist and the datasheet text)

1. **C33, 0.1 µF on the DAC output (U30 MCP4726 VOUT, DAC_OUT to J1 pin 7).** The
   datasheet: "The VOUT pin can drive up to 100 pF of capacitive load"; its electrical
   specifications assume CL = 100 pF; larger loads want a series RISO, sized on the
   bench (DS22272C §4.4.6). Its own Fig 8-2 draws an optional 0.1 µF there, so the
   document disagrees with itself. As built: 1000 times the stated load, no RISO.
2. **U37 (TLV3691 comparator) has no supply capacitor.** Its VCC net (Net-(D8-C), fed
   through D8) holds no capacitor at all; the datasheet asks 0.1 µF at VCC (SBOS694A §10.1).
3. **R9, 330 Ω, exceeds the BQ298000's R_VDD maximum of 300 Ω** (SLUSCS3M Table 8-1:
   R_VDD max 300 Ω; C_VDD typ 0.1 µF, max 1 µF). C11 is 1 µF, at the maximum.
4. **BQ298000 CTR (configured "CTR" in this variant): high opens the FETs or shuts the
   part down for storage (§7.1).** R12 (1 kΩ) and C12 (0.1 µF) hold it low; it is driven
   through R14 (100 Ω) from expander GPA1, an open-drain output, so it can never be
   driven high, and Okapi_Library never uses it. Harmless as built; the intended
   firmware disconnect cannot work. Andy's question: what was CTR meant to do.
5. **U21 (TPS22917) VIN has C16 0.22 µF**; the datasheet calls 1 µF "sufficient in most
   situations" (SLVSDW8B §11), a recommendation.
6. **Supply pins with no capacitor within 3 mm** (3 mm is a threshold of mine, a
   proposal): sources/2026-11-08-supply-pins-nearest-capacitor.txt. Datasheets that ask
   for one: the AUP/AHC logic gates (0.1 µF), TPL5111 (0.1 µF X7R), DS3231M (0.1 to 1.0
   µF), the MIC2544s at IN (0.1 to 1 µF), the TPS22917s at VIN (1 µF), the TXS0102/0104
   and TCA9406 B sides (0.1 µF), ADS1115 ("at least 0.1 µF", C36 at 3.3 mm), the ATmega
   (AN2519). Datasheets silent: MCP23018, PCA9634, MB85RC512T, SN74AUP3G34,
   SN74LVC1G3157, MIC94094. The SD card specification was not obtained (terms page).

## Decided 2026-11-08 (Andy)

- C33 (DAC output) 68 pF, Würth 885012005060 (Project-Okapi 33d3041).
- R9 (BQ298000 VDD) 220 Ω, TE CRGCQ0402F220R (cff1189).
- C15, C16 1 µF, Samsung CL05A105KA5NQNC; the 0.22 µF line retired (73477d8).
- **C10 (solar input): two TDK CNA6P1X7R1H106K250AE in parallel** (10 µF 50 V X7R
  1210, AEC-Q200; 445-180367-1-ND), the second with a new designator; a copper change
  for B8. Bounds: rated 50 V for the 32 V input; C_eff(V_IN) >= 84/V_IN µF (LT3652
  rev D: C_IN(BULK) = I_CHG (V_BAT/V_IN)/ΔV_IN, 2 A, 4.2 V, 0.1 V), so 12.8 µF at the
  P106's 6.56 V operating point, holding at +85 °C and -10 % tolerance (two parts: 15.8
  µF; one part: 9.45 µF at 25 °C); about 1 A RMS ripple shared. No datasheet upper
  bound. Before placing: check Linear AN88 (ceramic-only inputs ringing at plug-in on
  long leads toward 2 x V_panel against the LT3652's 40 V absolute maximum), which may
  add a damped bulk capacitor.
- **Missing decouplers on v0.8.0 (Andy): Project-Okapi #41**, with the table (28 pins
  whose datasheets ask for a capacitor, 7 where they are silent, 4 near the line). U37's
  capacitor is in it. The ATmega's VCC pins stay with #17 on v0.7.0.
- **C3, C4, C14 to 22 µF** (Andy; Project-Okapi 26d9ddc).
- **V_LI bulk: Project-Okapi #42 on v0.8.0** (Andy: add the part): 100 µF low-ESR
  non-ceramic beside C14 per the LT3652's "VBAT Output Decoupling" (battery
  disconnected under a system load: the BQ2980 opening its FETs; long cell leads).
  Proposed KEMET T520B107M010ATE070 (100 µF 10 V polymer, 70 mΩ, B case, -55 to
  +105 °C, 20,065 stocked 2026-11-08).
- **C43 (V_CORE, Vishay TL8A0107M010D) is obsolete** (Digi-Key, 2026-11-08; 7 Ω
  ESR): **replaced on v0.7.0 by the KEMET T520B107M010ATE070 (Andy: the same part as #42,
  for an easier migration): Project-Okapi #43.** The B case (CT3528) does not fit in place
  (DRC 5 to 23: mask bridges and clearances to V_CORE, 3V3_CORE and C16), so it needs
  a nearby site and rerouting; the in-place attempt is a stash in Project-Okapi.
- Still pending: C17 (TPS2105 output, 0.1 µF; TI: "bypassing the output with a 1-µF
  ceramic capacitor improves the immunity of the device to short-circuit transients").

## C43 (V_CORE hold-up): leakage and a ceramic alternative (2026-11-08)

Leakage, rated maximum at 25 °C after 5 min at rated voltage: the old Vishay TL8A0107M010
(MICROTAN, MnO2) 100 µA (Vishay 40156, Standard Ratings); KEMET T520A107M006ATE070 63 µA,
T520B107M010ATE070 100 µA (KEMET spec sheets). Vishay's typical leakage-factor curve (40156
p4, read off the plot) at +25 °C: about 0.12 at 50 % of rated voltage, 0.3 at 67 %, 0.5 at
79 %, 0.65 at 86 %; about 3 times higher at +55 °C. Upper-bound estimates on V_CORE (5.0 V):
old part and T520B about 12 µA, T520A 32 to 41 µA; README's backup sleep figure is 4 µA.

Hold-up need, from TPS2105 Figure 11 (IN2 to IN1, read off the plot): 0.4 V droop at about
6 mA with 10 µF and about 30 mA with 47 µF, so a gap of about 0.65 ms;
C_eff >= I x 0.65 ms / ΔV. The TPS797 downstream needs about 3.45 V, so with the backup pack
low (3.6 V) the droop allowed is about 0.15 V: 87 µF effective at 20 mA, 217 µF at 50 mA;
at 0.3 V, 43 and 108 µF.

Ceramic 1210 candidates, 100 µF 10 V X5R, manufacturer data read in Chrome (2026-11-08):
- TDK C3225X5R1A107M250AC (Production): 100, 95.5, 81.4, 62.7 (3.2 V), 53.1 (4 V),
  43.7 (5 V), 34.8 µF (6.3 V); temperature at 0 V: 86.8 % at -55 °C, 87.5 % at +85 °C.
  Digi-Key: 0 in stock, 500 expected 2027-03-04.
- Murata GRM32ER61A107ME20L: 59.9 µF (3.6 V), 55.4 (4 V), 45.6 (5 V), 42.3 (5.4 V)
  (25 °C, 0.5 Vrms, Murata's characteristic data); temperature at 0 V: -2.0 % at -40 °C,
  -8.7 % at +85 °C. Digi-Key 490-9969-1-ND: 0 in stock, 1,000 expected 2026-11-25,
  17-week lead, $0.82.
Leakage: insulation resistance, nanoamps.

**Decided (Andy, 2026-11-08): C43 becomes the Murata GRM32ER61A107ME20L** (one; a second
if the first board shows the core above about 20 mA awake), recorded on #43, whose title
now says so. The 1210 footprint is copper work, with the other board edits. #42 keeps a
non-ceramic part (the LT3652 asks for one) and gained a leakage note.

**Smaller and better-stocked alternatives (Andy: "not necessarily that part"), read in
Chrome 2026-11-08.** Effective µF at 25 °C, 3.6 V / 4 V / 5 V:
- Murata GRM31CR60J107MEA8 (100 µF 6.3 V X5R 1206): 50.6 / 45.2 / 34.8; Digi-Key 0, expected
  2027-09-08.
- TDK C3216X5R0J107M160AB (100 µF 6.3 V X5R 1206): about 42.9 (interpolated) / 37.8 / 28.8;
  -11 % at -40 °C (interpolated), -9 % at +85 °C; Digi-Key 38.
- Taiyo Yuden JMK316ABJ107ML-T (100 µF 6.3 V X5R 1206): Digi-Key 330,856, $0.52; its own
  curve sits behind TY-COMPAS's terms dialog (not accepted), so Murata's and TDK's 1206 curves
  bracket it (an assumption).
- Samsung CL31A107MQHNNNE (same spec): Digi-Key 0.
- Murata GRM32ER60J107ME20 (100 µF 6.3 V 1210): 56.9 / 52.6 / 43.2. Taiyo Yuden
  LMK325ABJ107MM-T (100 µF 10 V 1210): Digi-Key 59.
- Murata 47 µF 1206 (GRM31CR61A476ME15): 25.8 / 23.5 / 18.7, too little.
A 1206 keeps about 85 % (Murata) or 72 to 75 % (TDK) of the 1210's effective capacitance.

**Rated 10 V or more, in stock (Andy's ask; Digi-Key and Murata in Chrome, 2026-11-08):**
- **Murata GRM31CR61A107MEA8L, 100 µF 10 V X5R 1206: 873,508 in stock, $0.55.** Murata's
  data: 50.6 µF at 3.6 V, 45.2 at 4 V, 34.8 at 5 V, 31.6 at 5.4 V (25 °C, 0.5 Vrms);
  -6.7 % at -40 °C, -13.3 % at +85 °C (0 V, 0.2 Vrms). The DC-bias numbers are identical to
  the 6.3 V GRM31CR60J107MEA8's, which suggests one construction rated two ways (an
  inference). At V_CORE's 5.0 to 5.4 V it runs at 50 to 54 % of rating.
- 1206 at 16 V: none in stock.
- 1210 at 10 V in stock: Murata GRM32ER61A107ME20K (the K-reel version of the earlier plan)
  23,692, $0.82; Taiyo Yuden LMK325ABJ107MM-P 95,115, LMK325BJ107MM-T 79,108 (about $1.36 to
  $1.40); TDK C3225X7T1A107M250AC (X7T) 1,507, $2.06.
- Not stocked: TDK C3216X5R1A107M160AC (0, expected 2027-01-18), Samsung CL32A107MPVNNNE (0).

**Done 2026-11-08 (Andy: "Great plan"): C43 is the Murata GRM31CR61A107MEA8L on its existing
C1206_TANT pads** (Project-Okapi d630f34; #43 updated). Left for the copper work: a 1206 ceramic
land and a non-polarized symbol. To measure on the first board: backup-pack sleep current, and
the core's awake current (a second part only if the core exceeds about 10 to 20 mA awake).

## Copper plan (2026-11-08)

Check of every R and C: the part number's size against its footprint. One mismatch, R48
(0402 on 0603 pads), which is Andy's intended user-adjustable part; #36's dual 0603/0402
land completes it. C43 is the one real inconsistency (a ceramic on a tantalum land and
symbol). Steps, least copper first, each one commit with a render shown first: (1) R1, R8 to
0402 (#33); (2) C43 ceramic 1206 land and a plain capacitor symbol; (3) R48 dual pads (#36,
footprint drawn in nw-cold-silicon first); (4) JP8, R62 out (#34); (5) #37's SLOW pull-up;
(6) C10 as two 50 V 1210s (milestone to confirm; AN88 check first); (7) #32's sense
resistor; (8) #35's TPL5010; (9) #17's three IC1 decouplers: **a top-side reroute (Andy),
not yet: placement around IC1 to be thought through first**. Open: R71 staying 0603; C10's
milestone; AREF.
Decided 2026-11-08 (Andy): **R70 and R71 lands at least 0603** whatever resistor is fitted
(they set the charger's start voltage, 7.2 V, per panel); R71 can take an 0402 1 MΩ on dual
0603/0402 pads to join the 1 MΩ 0402 line; R70 stays an 0603 part (recorded on #33). The
logger core (3V3_CORE) is typically 10 mA or less awake (Andy), so one C43 ceramic suffices
(worst case about 9 mA through 0.15 V of droop with the backup at 3.6 V, 17 mA through 0.3 V).
Decided 2026-11-08 (Andy): **C10's 50 V upgrade is #44 on v0.8.0**; the README now limits the
panel to 4.95 to 16 V open-circuit on v0.7.0 (Project-Okapi 30adefc). **#43 moved to v0.8.0**
for the ceramic land and plain symbol (v0.7.0 carries the stocked Murata part). **R69 on dual
0603/0402 pads with an 0402 100 kΩ** (on #33). **#45 (enhancement, v0.8.0): a second C43** if
the first board shows thin hold-up margin.

## Positions

All 70 positions on Okapi and Margay, one row each (net and voltage, governing pin, the
requirement quoted with its type, bounds, rating, dielectric, land, effective value, verdict,
source): `sources/2026-11-09-capacitor-constraints-agent-report.md` (agent, 2026-11-09).
Checked against the netlist: Margay C19 (0.1 µF) and C20 (1 µF) both sit on the DS3231M's
VBAT with BT1 and D4; D4 (BAT43WS) runs from 3V3 to BT1+ (Andy b82f7d8, a backup feed for
the RTC, whose VCC is on the switched 3V3_AUX); Margay U9 is a TPS2104DBVT.

Fails: Okapi C10 (#44); Margay C10, 0.1 µF on the TPS2104's IN1 against "require 0.22 µF";
Margay C19 + C20, 1.1 µF on VBAT against the DS3231M's 0.1-1.0 µF. Merge candidates: (A) 10
µF 0805 into 22 µF 0805, no copper, blocked by Margay's VUSB 10 µF limit and the TPS7A05's 22
µF maximum read nominally; (B) 4.7 µF 0603 into 1 µF 0603, blocked by FTDI's 4.7 µF at Okapi
C22; (C) the two 1 µF lines, copper either way.

## Decided 2026-11-09 (Andy), from the two-board constraint table

- **Margay C10 1 µF 0402** (CL05A105KA5NQNC), for the TPS2104's 0.22 µF on IN1 (Project-Margay
  01cb15f). C11 (IN2, on VUSB) stays 0.1 µF: VUSB already holds 10.2 µF against USB's 10 µF.
- **Okapi C30 22 µF** (GRM219R61C226ME15L), 7.6 µF effective at 5 V against the MCP4726's
  10 µF tantalum (Project-Okapi 3a981d2). Okapi no longer uses the 10 µF line; Margay does.
- **C43: both parts on v0.8.0**, fitted by default (#45, retitled, with the reasoning).
- **CTR (C12, R12, R14): Project-Okapi #47**, a firmware battery disconnect to revisit.
- **The 1 µF positions onto 0402**, on dual 0402/0603 lands where the land is 0603 now: Okapi
  C11 (v0.8.0), Margay C13, C14, C20 (v3.1). Margay C13 meets at the line (0.51 µF effective at
  5.5 V against the TPS7A05's 1 µF nominal, which TI says assumes about 50 %). Okapi C13
  (LT3652 BOOST, "1µF or greater", no upper bound) takes a higher-capacitance part instead:
  proposed a 2.2 µF 0603 X7R on its present land, to be picked with the Digi-Key pass. The
  Taiyo TMK107B7105KA line then retires and a 2.2 µF line arrives: the count stays 10.
- **Margay C19 + C20** stay as they are until the RTC conversation (QUEUE, "ON ANDY'S DESK"
  14): Andy added C20 to keep the clock's time through power drops.

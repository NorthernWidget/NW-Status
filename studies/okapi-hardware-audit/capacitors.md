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

## Positions

(to be filled: ref, net and voltage, the datasheet and its type, lower and upper bound,
our part, its effective value, verdict)

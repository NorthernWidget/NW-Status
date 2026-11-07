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

## Positions

(to be filled: ref, net and voltage, the datasheet and its type, lower and upper bound,
our part, its effective value, verdict)

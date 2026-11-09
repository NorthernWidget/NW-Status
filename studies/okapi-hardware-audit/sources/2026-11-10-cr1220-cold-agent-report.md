COMPLETE

# CR1220 in the cold at real-time-clock loads, and a 1 kOhm + Schottky + 100 uF buffer

Agent report, 2026-11-10. Every number carries a source URL, or is marked UNVERIFIED or ESTIMATE with its arithmetic.

## 1. Clock load (DS3231M datasheet 19-5312 Rev 5, 7/13; local text copy)

Source: /tmp/claude-1000/-home-awickert-Dropbox-NorthernWidget-github/cf0342fa-36e3-4818-be1e-2b4b31cc1756/scratchpad/icreq/txt/ds3231m.txt

- VBAT operating range 2.3 V min, 3.0 V typ, 5.5 V max (Recommended operating conditions, line 82).
- IBATT timekeeping, VBAT = 3.63 V, EN32KHZ = 0: typ 2 uA, max 3.0 uA; "Note 4: Includes the temperature conversion current (averaged)."
- IBATTC temperature-conversion current, VBAT = 3.63 V: 575 uA (max); 650 uA at VBATMAX.
- tCONV temperature conversion time: 10 ms.
- Period on battery: "When VBAT is the presently selected power source, temperature conversions are executed once every 10s." (On VCC: once per second.)
- Operating temperature: "-45 C to +85 C".

## 2. Sources log (all checked, dead ends included)

Derived from the clock figures (ESTIMATE): average conversion current = 575 uA x 10 ms / 10 s = 0.575 uA, which is already inside the 2 uA IBATT typical. Charge per conversion = 575 uA x 10 ms = 5.75 uC.

### S1. Panasonic CR1220 datasheet (As of February 2026), FETCHED, graphs read from rendered page
URL: https://energy.panasonic.com/dam/master/pdf/en/datasheet/lithium/CR1220_Datasheet_EN.pdf
- "Nominal capacity 35mAh"; "Continuous drain 0.1mA"; "Operating temperature -30 C to +85 C". (Older distributor copies said -30 to +60 C; not fetched.)
- "Excellent low-temperature performance enhanced by manganese-dioxide positive pole".
- Graph "Discharge temperature characteristics", "Load: 30kOhm (95uA)": plateau read by eye at about 2.9 V at 20 C, about 3.0 V at 60 C, and about 2.70 V at -10 C (dipping to about 2.65 V in the first 50 h), lasting about 380 h at -10 C against about 400 h at 20 C. No curve below -10 C.
- Graph "Operating voltage vs. load resistance (voltage at 50% discharge depth)", 20 C only, read by eye: about 2.9 V at 100 kOhm (0.03 mA), 2.8 V at 10 kOhm (0.28 mA), about 2.65 V at 3 kOhm (about 0.9 mA), 2.4 V at 1 kOhm (about 2.4 mA). These are continuous-drain voltages, not 10 ms pulse voltages.
- Graph "Capacity vs. load resistance" (20 C, cutoff 2.0 V): about 18 mAh at 1 kOhm, about 35 mAh at 4 kOhm, about 38 mAh at 20 kOhm and above.

### S2. Panasonic BR1225A datasheet (As of February 2026), FETCHED
URL: https://energy.panasonic.com/dam/master/pdf/en/datasheet/lithium/BR1225A_Datasheet_EN_240701.pdf
- "Nominal capacity 48mAh"; "Continuous drain 0.03mA"; "Operating temperature -40 C to +125 C". Chemistry: "poly-carbonmonofluoride".
- Graph "Discharge temperature characteristics", "Load: 30kOhm" (about 90 uA), read by eye: 20 C plateau about 2.72 V; 60 C about 2.83 V; 100 C about 2.93 V; 125 C about 3.05 V; -10 C starts at about 2.30 V, rises to about 2.48 V by 50 h, holds about 2.45 V to 370 h, then falls to 1.9 V at about 450 h. No curve below -10 C.
- Reading: at the same ~90 uA, the BR1225A at -10 C sits about 0.2 V BELOW the Panasonic CR1220 at -10 C (2.48 against 2.70 V), and its initial dip (2.30 V) touches the DS3231M's 2.3 V floor.

### S3. Renata CR1220 Technical Data Sheet, Rev. CR1220.04 10/01, FETCHED (distributor copy)
URL: https://www.100y.com.tw/pdf_file/Renata_CR1220.pdf
- "Chemical System Li / MnO2"; "Rated Capacity 38 mAh"; "Standard Discharge Current 0,05 mA"; "Max. Cont. Discharge Current 1,0 mA"; "Temperature Range -30 - +70 C"; "Self Discharge at 23 C < 1% / year".
- Graph "Temperature performance Load 27kOhm" (about 107 uA at 2.9 V), read by eye from a 400 dpi render: first-hours voltage about 2.95 V at all four temperatures (-20, 0, 23, 70 C); -20 C curve falls slowly from about 2.9 V at 100 h to about 2.7 V at 200-230 h and reaches 2.0 V at about 340 h; 0 C reaches 2.0 V at about 340 h; 23 C at about 350 h; 70 C at about 360 h. That is, at about 0.1 mA continuous the Renata CR1220 delivers over 90% of its 23 C life at -20 C, at about 2.85-2.9 V for the first 100 h.
- Graph "Cell capacity at various loads" (to 2.0 V), read by eye: at -20 C, about 18.5 mAh at 8 kOhm (about 0.35 mA), about 21 mAh at 10 kOhm, about 30 mAh at 20 kOhm, about 35 mAh at 50 kOhm, about 38 mAh at 100 kOhm (full rating). At 0 C: about 19 mAh at 5 kOhm (about 0.55 mA). The -20 C curve is not drawn below 8 kOhm.

### S4. Panasonic "Lithium Batteries Handbook", December 1998, coin-cell section (third-party mirror), FETCHED
URL: https://extranet.mandieselturbo.com/electronics/datasheets/Panasonic/BR-CR_Series/Old/Lithium-BR-CR-coin_1998.pdf
- Handbook p. 25: "Panasonic coin type lithium batteries are mostly operable over the temperature range from -40 C to 85 C." and "Organic solvents are used for the electrolyte in lithium batteries. Therefore, the solidifying point of this electrolyte is much lower than that of the aqueous solution type electrolyte ... enabling the use of lithium batteries in low-temperature regions."
- p. 25: "an annual deterioration rate as low as about 1.0% at room temperature".
- p. 26 spec table: CR1220 "3 V, 35 mAh, 0.10 mA standard continuous drain"; BR1220 "3 V, 35 mAh, 0.03 mA"; footnote "Nominal capacity ... based on standard drain and cut off voltage down to 2.0 V at 20 C".
- p. 37 CR1220 sheet: identical curves to S1 (30 kOhm, 95 uA, -10/20/60 C). No CR1220 data below -10 C in either edition.
- p. 30 BR1220 sheet, "Operating voltage vs. load resistance" at uA loads, three temperatures, read by eye from a 400 dpi render:
  | Load | Current (axis) | 60 C | 20 C | -10 C |
  |---|---|---|---|---|
  | 10 MOhm | 0.3 uA | 3.03 V | 2.90 V | 2.77 V |
  | 1 MOhm | about 3 uA | 2.92 V | 2.77 V | 2.65 V |
  | 0.15 MOhm | about 17 uA | 2.80 V | 2.64 V | 2.51 V |
  The curve is logarithmic in current (about 0.12-0.13 V per decade), not ohmic.
- p. 30 BR1220 "Discharge temperature characteristics", Load 30 kOhm (90 uA): 20 C about 2.72 V, -10 C about 2.52 V, life about 290 h at -10 C against about 370 h at 20 C.
- p. 30 BR1220 "Capacity vs. load resistance" (2.0 V cutoff): -10 C about 23 mAh at 2 kOhm (about 1.3 mA), about 30 mAh at 20 kOhm, about 33 mAh at 100 kOhm; 20 C about 36 mAh at 100 kOhm.
- p. 46 BR1225A (then "Under Development"), 30 kOhm: same family as S2; -10 C about 2.5 V plateau, ends near 410 h.
- p. 44 CR2477 (1000 mAh, 24.5 x 7.7 mm) "Operating voltage vs. load resistance", read by eye from a 400 dpi render: the -40 C curve runs from about 2.75 V at 0.09 MOhm (about 0.03 mA) to about 2.96 V at about 3 MOhm (about 0.001 mA); -10 C runs from about 2.60 V at about 0.7 mA to 2.90 V at 0.06 mA; 20 C about 2.82 V at about 0.7 mA. Different and much larger cell; used only as evidence that Li-MnO2 delivers about 2.75-2.95 V at -40 C at uA-to-30 uA loads. ESTIMATE of scaling to the CR1220: face area ratio (12.5/24.5)^2 = 0.26, so 30 uA in a CR2477 is about the current density of 8 uA in a CR1220, and 575 uA in a CR1220 is about the current density of 2.2 mA in a CR2477, which is off the -40 C curve's range.

### S5. Maxell CR1220 Data Sheet (rev. mark "20.06"), FETCHED (retailer-hosted copy of the Maxell sheet)
URL: https://cdn.shopify.com/s/files/1/0645/4932/3005/files/Maxell-CR1220-Data-Sheet.pdf
(The maxell.com.tw copy https://www.maxell.com.tw/images/uploads/2014/10/CR1220_DataSheet_e.pdf returned a 654-byte HTML page, not the PDF: dead end.)
- "Nominal Capacity (mAh)* 36"; "Nominal Discharge Current (mA) 0.1"; "Operating Temperature Range (deg. C)** -20 to +85"; "** When using these batteries at temperatures outside the range of 0 to +40 deg. C, please consult Maxell in advance for conditions of use."
- Graph "Temperature Characteristics, Discharge load: 30kOhm" (about 95 uA), read by eye from a 400 dpi render: plateau about 2.88 V at 20 C, about 2.70 V at 0 C, about 2.50-2.55 V at -10 C (starting at 2.65 V). Life to 2.0 V: about 395 h at 20 C, about 375 h at 0 C, about 345 h at -10 C. Maxell's cold voltage is about 0.15-0.2 V lower than Panasonic's and Renata's at the same load.
- Graph "Pulse Discharge Characteristics", 20 C, 1 MOhm continuous with "300 Ohm 5sec" pulses: loaded voltage about 2.60 V at the start (about 8.7 mA, so (3.0 - 2.6) V / 8.7 mA = about 46 Ohm effective; ESTIMATE), 2.5 V at about 20 mAh, 2.0 V at about 30 mAh.
- Graph "Relationship between Discharge Current and Discharge Capacity", final voltage 2.0 V, read by eye: at -20 C, about 29.8 mAh at 10 uA, about 28.5 mAh at 100 uA, about 25 mAh at 400 uA, about 20 mAh at 700 uA (the curve stops there). At -10 C: about 33 mAh at 10 uA, 31.5 mAh at 100 uA, 27 mAh at 700 uA, 23.5 mAh at 1.1 mA. At 20 C: 38 mAh at 10-100 uA, 30.5 mAh at 1.1 mA.
- Reading: even at 10 uA, about 20% of the 20 C capacity (38 to 29.8 mAh) is not available above 2.0 V at -20 C. The cell's end-of-life knee moves earlier in the cold. A half-used cell has less margin in the cold than a fresh one.

### S6. Energizer CR1220 Product Datasheet, Form No. EBC-4113I, FETCHED (distributor mirror)
URL: https://files.batteryjunction.com/frontend/files/CR1220.pdf
- "Typical Capacity: 40 mAh (to 2.0 volts) (Rated at 45K ohms at 21 C)"; "Max Rev Charge: 1 microampere".
- No operating-temperature range or cold data on this sheet.
- "Internal Resistance Characteristics, Pulse Test at 21 C": "Bkgnd Drain: Continuous 62K ohms 0.046 mA @2.85V"; "Pulse Drain: 2 seconds X 12 times/day 1K ohms 2.8 mA @2.65V". Graph read by eye: background CCV about 2.92 V; pulse CCV about 2.72 V fresh; "IR, ohms" about 45 Ohm fresh, about 55 Ohm at 10 mAh, about 80 Ohm at 20 mAh, about 105 Ohm at 25 mAh, about 150 Ohm at 33 mAh, rising past 280 Ohm at about 36 mAh.
- ESTIMATE from those curves: (2.92 - 2.72) V / (2.8 - 0.046) mA = 73 Ohm effective over a 2 s pulse, fresh, at 21 C.

### S7. Jauch CR 1220 Technical Data Sheet, 10/2022, FETCHED
URL: https://www.jauch.com/downloadfile/5ef1edcfcf4cefed1b72b21a8a69c1430/cr1220_jauch.pdf
- "Nominal Capacity 40 mAh"; "Standard Load 62 kOhm"; "Max. Continuous Current < 0.1 mA"; "Max. Pulse Current 4 mA"; "Operating Temperature -30 C to +85 C*".
- Graph "Temperature Characteristics, EPV 2.0V, Load 68kOhm" (about 42 uA), read by eye: 23 C about 2.9 V; -20 C about 2.65 V plateau, ending near 950 h against about 1100 h at 23 C.
- Graph "Load vs. Capacity": -20 C about 43 mAh at 30 kOhm rising to about 46 mAh at 100 kOhm (23 C about 46 mAh). Optimistic beside Maxell's.

### S8. VARTA CR 1220 (Type 6220), catalog page "Primary Lithium Cells p. 15", FETCHED (distributor copy)
URL: https://www.electrokit.com/upload/quick/42/f2/fad6_41003323-CR1220_Varta.pdf
- "Typical Capacity C 35 mAh (Load 39 kOhm, at 20 C down to 2 V)"; "Temperature Ranges ... Discharge -20 C 70 C" with "Contact VARTA if the application is intended to be outside the range of -20 C to +70 C."; "Storage -55 C".
- Its temperature, voltage-vs-load and capacity-vs-load graphs are the Panasonic graphs of S1 reproduced (same 30 kOhm/95 uA, -10/20/60 C curves). Not independent data.

### S9. Energizer "Primary Lithium Coin Handbook and Application Manual" (PDF dated May 2026), FETCHED
URL: https://data.energizer.com/wp-content/uploads/2026/05/Lithium-Coin-app-manual-0526.pdf
(The older URL https://data.energizer.com/pdfs/lithiumcoin_appman.pdf returned an HTML page, not a PDF: dead end.)
- Temperature: "Cold temperatures cause the electrochemical reactions that take place within the battery to slow down and will reduce ion mobility in the electrolyte." Side note: "Lithium coin cells temporarily lose capacity in extreme cold due to increased internal resistance, but this effect is reversible. Once the battery warms back to normal operating conditions, voltage and capacity recover". (Its only temperature graph is a 2032 at 1 mA, 0/21/40 C; no sub-zero CR1220 data.)
- Internal resistance: "the starting IR of a 2032 battery is near 10 ohms"; dual-pulse method example, fresh 2032, 1000 kOhm background, 50 ms 25 Ohm pulse: "(3.279V - 2.429V) / (.097A - .000003A) = 9 Ohm. The drain rate and pulse duration can impact the IR calculation."
- "The battery IR will typically increase during discharge due to the impact of the reaction by-products". "Not all drains are the same ... very low uA drain rates can cause a significant rise in the battery IR early in the discharge." Graph "2032 BATTERY 3 uA DISCHARGE", read by eye: IR about 20 Ohm at about 25 mAh, about 30 Ohm at 50 mAh, about 55 Ohm at 75 mAh, about 100 Ohm at about 90 mAh (out of about 230 mAh). That is, IR rises several-fold under a uA drain long before half the capacity is used.
- Passivation: "After years of storage, lithium coin cells can develop a perceptible poor conducting passivation layer ... can contribute to a slightly higher initial internal resistance and subsequently an increased voltage drop when the battery is first put into use. Once a load is placed on the battery, the passivation layer will become thinner, and internal resistance typically returns to normal."
- Shelf: "lose approximately 1% of their capacity per year".

### S10. TI white paper SWRA349 "Coin cells and peak current draw" (M. Jensen), FETCHED (not a cell manufacturer; included for the capacitor-buffer method)
URL: https://www.ti.com/lit/wp/swra349/swra349.pdf
- "adding a capacitor in parallel with a CR2032 coin cell is the most effective choice a designer can make to maximize battery capacity utilization in low power RF applications (more than 40% improvement with poor quality CR2032s)".
- Figure 6: calculated CR2032 IR rises from a few Ohm to about 45 Ohm as capacity is used; "Since the IR increases rapidly as capacity is used, the circuit must be able to manage a very high IR".
- "For our testing we dimensioned for an IR of 1kohm which resulted in a capacitor of approximately 100uF."
- "Note: At low temperatures it probably becomes even more important to use a capacitor since the internal resistance increases with lowering temperatures." (No cold data in the paper; all tests at room temperature.)

### Dead ends and partial sources (cells)
- Renata FAQ "Frequently Asked Questions" (mirrors manualsdir.com and manualmachine.com). manualsdir.com fetched page gave only the OCV and Ri text: "a fresh lithium cell will typically show an OCV ... between 3.10-3.40 V"; "the OCV values depend on the temperature of the measurement"; "Ri = ( OCV - CCV ) x R1 / CCV". manualmachine.com returned HTTP 403. The sentence "Below -30 C the pulse current performance of the cells is significantly reduced, due to the increased internal resistance" appears only in a search-engine summary of the manualmachine mirror: UNVERIFIED verbatim.
- Renata Designer's Guide 2011 (https://www.mouser.com/datasheet/2/346/DesignersGuide_2011_Coin_Cells-1518723.pdf): curl returned nothing; WebFetch timed out. Search snippet only: "CR1220 MFR 40 0.10 1.00 -30/+70". UNVERIFIED (snippet).
- Panasonic Lithium Handbook 2025 (https://energy.panasonic.com/dam/master/pdf/eu/material/Panasonic_Lithium_Handbook_2025.pdf): HTTP 404 / 700-byte HTML. Dead end.
- Murata CR1220: murata.com lineup page lists no CR1220 datasheet (only UN38.3 summary and SDS); page states the micro primary battery business transferred to Maxell, Ltd. effective March 1, 2026. DigiKey page: "no longer available". A search summary gave Murata CR1220 "-30 C to 70 C": UNVERIFIED (not fetched). Dead end for curves.
- Maxell Taiwan CR1220 sheet URL: 654-byte HTML, dead end (Maxell sheet obtained from S5 instead).
- Energizer old handbook data.energizer.com/pdfs/lithiumcoin_appman.pdf: HTML, dead end (2026 edition used, S9).
- EEVblog thread "Coin cell performance in low temperatures" (https://www.eevblog.com/forum/projects/coin-cell-performance-in-low-temperatures/): forum, no manufacturer cold numbers; one poster reports Renata supplied a lifetime-vs-temperature analysis for a supplied load profile. Not used for numbers.
- No manufacturer document found giving CR1220 internal resistance or pulse voltage as a function of temperature below -10 C (Panasonic, Varta) or -20 C (Renata, Maxell, Jauch). The cold pulse figures below are therefore ESTIMATES built from the continuous-load curves.

### S11. Panasonic BR1220 datasheet (As of February 2026), FETCHED
URL: https://energy.panasonic.com/dam/master/pdf/en/datasheet/lithium/BR1220_Datasheet_EN.pdf
- "Nominal capacity 35mAh"; "Continuous drain 0.03mA"; "Operating temperature*2 -40 C to +85 C".
- Footnote *2: "It has been confirmed that the initial battery meets the following conditions: (i) it operated with a 300kOhm discharge load at -40 C, and (ii) It can discharge for more than 240 hours with a cutoff voltage of 2.0V." That is, the -40 C rating is set at about 9 uA (ESTIMATE: 2.6 V / 300 kOhm = 8.7 uA) and a 2.0 V cutoff, which is below the DS3231M's 2.3 V floor.
- Curves identical to the 1998 handbook (S4): 30 kOhm (90 uA): 20 C about 2.72 V, -10 C about 2.52 V; voltage-vs-load at 0.3-20 uA for -10/20/60 C.
- (The README's "BR1220 to -30 C" matches the older sheet generation; the 2026 sheet says -40 C at the 300 kOhm condition above.)

### S12. Diodes Inc. BAT42WS/BAT43WS datasheet DS30100 Rev. 15-2, August 2022, FETCHED
URL: https://www.diodes.com/assets/Datasheets/ds30100.pdf
- "Forward Voltage Drop ... BAT43WS 0.26 (min) 0.33 (max) V, IF = 2.0mA"; "0.45 V max, IF = 15mA" (at 25 C).
- "Reverse Current ... 500 nA, VR = 25V"; "100 uA, VR = 25V, TJ = 100 C". "Operating and Storage Temperature Range -55 to +125 C".
- Fig. 1 "Typical Forward Characteristics", read by eye from a 300 dpi render, lowest plotted current 0.1 mA: 25 C about 210 mV at 0.1 mA and about 285 mV at 1 mA; -25 C about 315 mV at 0.1 mA and about 350 mV at 1 mA; 75 C about 120 mV at 0.1 mA. Nothing plotted below 0.1 mA.
- Fig. 2 "Typical Reverse Characteristics", 25 C: about 0.04-0.06 uA at 0-5 V reverse.
- ESTIMATE of VF at uA currents (extrapolated below the plotted range): temperature coefficient at 0.1 mA = (315 - 210) mV / 50 C = 2.1 mV/C; slope below 0.1 mA taken as the ideal-diode value n x 2.303 kT/q with n = 1.05 (ASSUMED, not from the datasheet), 62 mV/decade at 25 C, 49 mV/decade at -40 C. VF(I) = VF(0.1 mA, T) - log10(0.1 mA / I) x slope(T):
  | T (C) | VF at 0.1 mA (mV) | VF at 2.5 uA (mV) | VF at 8.5 uA (mV) |
  |---|---|---|---|
  | 20 | 220 | 123 | 155 |
  | 0 | 262 | 171 | 202 |
  | -10 | 284 | 196 | 225 |
  | -20 | 304 | 220 | 248 |
  | -30 | 326 | 244 | 271 |
  | -40 | 346 | 269 | 294 |
  (8.5 uA = 2.5 uA clock + 6 uA worst-case capacitor leakage, see S13.)

### S13. Murata MLCC insulation resistance and X5R class
- Murata FAQ "leakage current of MLCCs", FETCHED: https://www.murata.com/support/faqs/products/capacitor/mlcc/char/0039 : "Leakage current specification values are not prescribed for DC, and are instead specified by the insulation resistance value." Example GRM188R60J106ME47: "50 Ohm F or more", "Insulation resistance = 5 MOhm", "I (leakage current) = 1.26 uA or less" at 6.3 V. Test conditions at normal temperature; no temperature dependence given.
- GRM31CR61A107MEA8L's own I.R. row: NOT FETCHED (murata.com product page redirected to pim.murata.com, which returned empty; search.murata.co.jp spec URL returned HTML). A search snippet for the sibling GRM31CR60J226KE19 gives "More than 50 Ohm F": UNVERIFIED for the 107 part.
- ESTIMATE, if the 107 part is also specified at 50 Ohm F: IR >= 50 Ohm F / 100 uF = 0.5 MOhm, so leakage <= 3.0 V / 0.5 MOhm = 6 uA guaranteed maximum at room temperature. This is a guaranteed bound, not a typical value; typical MLCC leakage is far lower (UNVERIFIED, no Murata typical figure found). Leakage in ceramics falls in the cold (thermally activated; general behavior, UNVERIFIED for this part).
- X5R class: Murata datasheets (search result for Murata KRM31 sheet https://pim.murata.com/asset/pim4/ceramicCapacitorSMD/KRM31_E_PDF_CERAMICCAPACITORSMD; snippet, NOT FETCHED) give X5R as within +/-15 % over -55 to 85 C. The 50 uF effective near 3 V is the caller's figure; ESTIMATE worst-case cold capacitance 0.85 x 50 uF = 42.5 uF (assumes the DC-bias loss and the temperature change multiply; not verified).

## 3. Analysis (all ESTIMATES; method, inputs and arithmetic shown)

The table in 3.3 was computed by a short Python script (output kept at /tmp/claude-1000/-home-awickert-Dropbox-NorthernWidget-github/cf0342fa-36e3-4818-be1e-2b4b31cc1756/scratchpad/cr1220dl/est.txt, a temporary location); every formula and input it used is stated in 3.2 and the S12 table, so it can be rebuilt from this file.

### 3.1 What no manufacturer gives
No manufacturer document found states a CR1220's (or BR1220's) internal resistance, pulse voltage, or impedance as a function of temperature. Panasonic and Varta stop at -10 C; Renata, Maxell and Jauch stop at -20 C; all cold curves are continuous loads of 42-107 uA. The cold pulse voltage must therefore be built from those curves.

### 3.2 Method
- V100(T): the cell's closed-circuit voltage at about 0.1 mA continuous, early-plateau, read from the graphs (S1, S3, S5, S7, S11). Values marked "x" are extrapolated linearly from the two coldest data points.
- Polarization multiplier k(T) = (OCV - V100(T)) / (OCV - V100(20 C)), with OCV = 3.2 V (inside Renata's "3.10-3.40 V" for a fresh cell; ASSUMED single value).
- Unbuffered pulse, two bounds:
  - "continuous" (pessimistic): V575 = V100 - 0.15 V x k. The 0.15 V is the Panasonic 20 C continuous-load difference between 30 kOhm (about 0.1 mA, 2.87 V) and about 5 kOhm (about 0.575 mA, 2.72 V), read from S1's voltage-vs-load graph.
  - "ohmic" (optimistic): V575 = V100 - 0.475 mA x 75 Ohm x k. The 75 Ohm is the fresh-cell 2 s pulse resistance at 21 C (S6, (2.92 - 2.72) V / 2.75 mA = 73 Ohm; Maxell's 5 s pulse gives about 46 Ohm, S5).
  A 10 ms pulse sits between the bounds: shorter than the 2-5 s pulses behind the ohmic figure, and far shorter than the continuous discharge behind the other.
- Cell voltage at the clock's average draw: Vu = V100 + 0.10 V/decade x log10(100/2.5) x k. The 0.10 V/decade is S1's 20 C slope between 0.03 and 0.28 mA. Check: S4's CR2477 -40 C curve reaches about 2.96 V at about 1 uA, which supports Vu near 2.85-2.95 V at -40 C at uA current densities.
- Buffered VBAT minimum = Vu - VF(2.5 uA, T) (S12 table) - 2.5 uA x 1 kOhm (2.5 mV) - droop. Droop = 5.75 uC / C, with C falling linearly from 50 uF at 20 C to 42.5 uF at -40 C (0.115 V to 0.135 V). This ignores the cell's own contribution through 1 kOhm during the pulse, which can only reduce the droop.

### 3.3 Results, fresh cells
| Cell | T (C) | V100 (V) | k | Unbuffered V575, continuous bound (V) | Unbuffered V575, ohmic bound (V) | Vu at 2.5 uA (V) | Diode VF (V) | Droop (V) | Buffered VBAT min (V) |
|---|---|---|---|---|---|---|---|---|---|
| CR1220, Panasonic/Varta/Renata/Jauch-type | 20 | 2.90 | 1.00 | 2.75 | 2.86 | 3.06 | 0.123 | 0.115 | 2.82 |
| | 0 | 2.80 (interp.) | 1.33 | 2.60 | 2.75 | 3.01 | 0.171 | 0.121 | 2.72 |
| | -10 | 2.70 | 1.67 | 2.45 | 2.64 | 2.97 | 0.196 | 0.124 | 2.64 |
| | -20 | 2.63 (Jauch 2.65 at 42 uA) | 1.90 | 2.35 | 2.56 | 2.93 | 0.220 | 0.128 | 2.58 |
| | -30 | 2.57 x | 2.10 | 2.25 | 2.50 | 2.91 | 0.244 | 0.131 | 2.53 |
| | -40 | 2.50 x | 2.33 | 2.15 | 2.42 | 2.87 | 0.269 | 0.135 | 2.47 |
| CR1220, Maxell | 20 | 2.88 | 1.07 | 2.72 | 2.84 | 3.05 | 0.123 | 0.115 | 2.81 |
| | 0 | 2.70 | 1.67 | 2.45 | 2.64 | 2.97 | 0.171 | 0.121 | 2.67 |
| | -10 | 2.52 | 2.27 | 2.18 | 2.44 | 2.88 | 0.196 | 0.124 | 2.56 |
| | -20 | 2.34 x | 2.87 | 1.91 | 2.24 | 2.80 | 0.220 | 0.128 | 2.45 |
| | -30 | 2.16 x | 3.47 | 1.64 | 2.04 | 2.72 | 0.244 | 0.131 | 2.34 |
| | -40 | 1.98 x | 4.07 | 1.37 | 1.84 | 2.63 | 0.269 | 0.135 | 2.23 |
| BR1220 (Panasonic) | 20 | 2.72 | 1.60 | 2.48 | 2.66 | 2.78 (S4 graph) | 0.123 | 0.115 | 2.54 |
| | 0 | 2.59 x | 2.03 | 2.29 | 2.52 | 2.70 x | 0.171 | 0.121 | 2.41 |
| | -10 | 2.52 | 2.27 | 2.18 | 2.44 | 2.66 (S4 graph) | 0.196 | 0.124 | 2.34 |
| | -20 | 2.45 x | 2.50 | 2.08 | 2.36 | 2.62 x | 0.220 | 0.128 | 2.27 |
| | -30 | 2.38 x | 2.73 | 1.97 | 2.28 | 2.58 x | 0.244 | 0.131 | 2.20 |
| | -40 | 2.31 x | 2.97 | 1.87 | 2.20 | 2.54 x | 0.269 | 0.135 | 2.13 |
The BR1225A tracks the BR1220 within about 0.04 V (S2: 2.72 V at 20 C and 2.48 V at -10 C at 30 kOhm, against 2.72 and 2.52 V), so its rows are the BR1220 rows less up to 0.04 V. Its -10 C start-up dip to about 2.30 V (S2) sits on the 2.3 V floor even at 90 uA.

### 3.4 Lowest temperature at which VBAT stays >= 2.3 V (fresh cell; linear interpolation in the table)
| Cell | Unbuffered, continuous bound | Unbuffered, ohmic bound | Buffered (1 kOhm + BAT43WS + 100 uF) |
|---|---|---|---|
| CR1220, Panasonic-type | about -25 C | below -40 C (2.42 V at -40) | below -40 C (2.47 V at -40) |
| CR1220, Maxell | about -5 C | about -17 C | about -34 C |
| BR1220 | about 0 C | about -28 C | about -14 C |
| BR1225A | about 0 C or warmer | about -25 C | about -12 C |

Reading (hypothesis, not measurement): the field failures near -20 C (or near 0 C in the field emails) and the cure by warming fit the continuous-bound column for a Maxell-like or part-used cell, and do not fit the ohmic column for a fresh Panasonic-type cell.

### 3.5 Refill, and the cell's voltage during it (question 3a)
- Average refill current is the clock's own conversion charge: 5.75 uC / 10 s = 0.575 uA, on top of the 2-3 uA timekeeping draw.
- Peak refill current: the 1 kOhm and the diode share the droop. At -20 C, with 50 uA flowing the resistor drops 50 mV and the diode rises by about 22.9 mV x ln(50/2.5) = 69 mV above its 2.5 uA value (n kT/q = 22.9 mV at 253 K, n = 1.05 ASSUMED); 50 + 69 = 119 mV, about the 0.128 V droop. ESTIMATE: peak refill about 50 uA, well under the 0.1 mA ceiling.
- Cell voltage during refill (50 uA) against during an unbuffered 575 uA pulse: the log-law gap is 0.10 V/decade x log10(575/50) x k = 0.106 x k V, that is 0.11 V at 20 C, 0.20 V at -20 C (Panasonic-type) and 0.30 V at -20 C (Maxell-type, k = 2.87); under the continuous bound the gap is larger, (V575 continuous) against Vu less about 0.13 x k V.
- Recovery time: the diode's small-signal resistance at 2.5 uA is 22.9 mV / 2.5 uA = 9.2 kOhm at -20 C; tau = 9.2 kOhm x 46 uF = 0.42 s. Ten seconds between conversions is about 24 tau, so the capacitor is full before the next pulse.

### 3.6 Capacitor in the cold (question 3c)
- Capacitance: X5R stays within +/-15 % from -55 to 85 C (S13), so the droop grows from 0.115 V to at most 0.135 V (5.75 uC / 42.5 uF). Not a limiting term.
- Leakage: the only guaranteed figure is the insulation-resistance floor. If 50 Ohm F applies to this part (UNVERIFIED), worst-case leakage is 6 uA at room temperature, two to three times the clock's 2-3 uA. At that bound: (1) backup life on a 35 mAh cell falls from 35 mAh / 2.5 uA = 14,000 h (1.6 years) to 35 mAh / 8.5 uA = 4,100 h (0.47 years), and (2) the diode drop rises by about 30 mV (S12 table, 2.5 against 8.5 uA). Leakage falls in the cold, so it costs life in warm storage rather than margin at -40 C. Typical parts leak far less than the bound; measuring one board's VBAT current with main power off would settle it.

### 3.7 Aged cells
- IR rises with depth of discharge: Energizer CR1220 pulse IR about 45 Ohm fresh, about 80 Ohm at 20 mAh, about 150 Ohm at 33 mAh of 40 (S6); a 2032 under a 3 uA drain rises several-fold well before half capacity (S9); TI measured the same rise on six CR2032 brands (S10).
- Unbuffered, ohmic bound at -20 C, Panasonic-type, with 150 Ohm instead of 75 Ohm: V575 = 2.63 - 0.475 mA x 150 Ohm x 1.90 = 2.49 V (against 2.56 V fresh); with 300 Ohm: 2.36 V. The pulse margin shrinks by 0.07-0.2 V as the cell ages.
- Buffered: the cell carries 2.5 uA average and about 50 uA peak, so an extra 225 Ohm costs 2.5 uA x 225 Ohm = 0.6 mV at the average and about 11 mV at the refill peak. The buffer makes the clock almost blind to IR growth.
- Capacity at end of life still limits both: Maxell gives only about 29.8 mAh (of 38) above 2.0 V at -20 C even at 10 uA (S5); the share above 2.3 V is lower and not published.

## 4. Other limits in the cold at this duty cycle (question 4)
- Passivation and voltage delay: Energizer describes a passivation layer after years of storage that gives "a slightly higher initial internal resistance" and clears under load (S9). Li-MnO2 shows little delay in the curves found: the Panasonic CR1220 -10 C trace starts near 2.75 V and dips about 0.1 V in its first 50 h (S1). The CFx cells show the larger start-up dip: BR1225A -10 C starts at about 2.30 V and takes about 50 h to reach 2.48 V (S2); BR1220 -10 C starts about 2.4 V (S4). A backup cell that has idled for years behind a 3.3 V rail, then is asked for 575 uA at -20 C, meets the passivated, cold case at once. No figure for this combined case was found.
- Recovery after a pulse: no manufacturer number for recovery time after a 10 ms pulse. Energizer says cold-induced loss "is reversible" on warming (S9). With the buffer, recovery of the capacitor (tau about 0.4 s, section 3.5) governs instead of the cell.
- Capacity loss in the cold: Maxell -20 C, 10 uA: 29.8 mAh of 38 mAh to 2.0 V (S5); Renata -20 C, 100 kOhm: about 38 mAh, the full rating (S3); Jauch -20 C, 100 kOhm: about 46 mAh (S7). The makers disagree by about 25 %. Self-discharge about 1 % per year at room temperature (S3, S4, S9).
- Holder contact: no manufacturer data found on coin-cell holder contact resistance or spring force in the cold. Not quantified (UNVERIFIED). At 575 uA, even 1 Ohm of contact resistance costs only 0.6 mV, so the holder matters only if contact is lost outright (thermal contraction, frost or condensation, vibration).
- Reverse charge: Energizer specifies "Max Rev Charge: 1 microampere" (S6). The series Schottky's reverse leakage (about 0.05 uA at 25 C, S12) keeps the 3.3 V rail from charging the cell; the diode on the cell is therefore needed while a rail diode also feeds VBAT.

## 5. Design note (a proposal, not checked against the schematic)
The cell-side Schottky costs 0.12-0.27 V (S12 estimate), which in the Panasonic-type rows is about as much as the buffer saves under the ohmic bound. The DS3231M already switches between VCC and VBAT internally (datasheet, section 1). If the second Schottky from the 3.3 V rail onto VBAT were removed, the cell could feed the capacitor through the 1 kOhm alone, with no diode drop and no reverse-charge path. That would raise every buffered VBAT figure above by the diode column (0.12 V at 20 C to 0.27 V at -40 C). The cost: the capacitor's leakage would then draw on the cell even while main power is present. Whether that trade is worth it depends on the measured leakage (section 3.6).

## 6. Summary
A fresh CR1220 holds about 2.9-3.06 V at the clock's 2-3 uA average from 20 C down to at least -20 C (data) and probably -40 C (estimate). The background load is not the problem; the 575 uA, 10 ms conversion every 10 s is. Unbuffered, a fresh cell's pulse voltage reaches the 2.3 V floor at about -25 C for Panasonic-type cells and about -5 C for Maxell's under the continuous-load bound; under the optimistic ohmic bound those limits are below -40 C and about -17 C. Aging lowers them further. With the 1 kOhm + BAT43WS + 100 uF buffer, the cell supplies at most about 50 uA. VBAT then stays at or above 2.3 V to below -40 C (Panasonic-type) or about -34 C (Maxell), and it is almost blind to IR growth. Against the continuous bound the gain is about 15-30 C; against the ohmic bound it is small, because the Schottky gives back 0.12-0.27 V. The BR1220 and BR1225A are worse here, not better: about 0.2 V lower than a CR1220 at the same load, about 0 C unbuffered and about -12 to -14 C buffered. Their -40 C rating is set at a 300 kOhm load and a 2.0 V cutoff.


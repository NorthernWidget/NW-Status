# COMPLETE

# Okapi solar panels, LT3652 VIN_REG and SHDN dividers (agent report, 2026-11-09)

## Source log (every source checked, dead ends included)

- analog.com LT3652 PDF (https://www.analog.com/media/en/technical-documentation/data-sheets/3652fe.pdf): WebFetch timed out at 60 s; curl (no custom headers) returned no bytes in 110 s. Also tried .../LT3652.pdf and .../3652hvfb.pdf by curl: no bytes. DEAD END.
- mouser.com mirror (https://www.mouser.com/datasheet/2/609/3652fe-1270201.pdf, guessed path): no bytes. DEAD END.
- cdn-shop.adafruit.com/datasheets/LT3652.pdf, sparkfun.com/datasheets/Prototyping/LT3652.pdf, cdn.sparkfun.com/datasheets/Prototyping/3652fe.pdf: all 404. DEAD END.
- es.datasheetq.com LT3652 page: HTTP 403. DEAD END.
- radiolocman.com viewer (https://www.radiolocman.com/datasheet/pdf.html?di=150119): page images only, but links the file below.
- USED: https://www.rlocman.ru/i/File/2017/09/30/3652fe.pdf (533,710 bytes, 26 pages, title "LT3652 - Power Tracking 2A Battery Charger for Solar Power", footer revision "3652fe", PDF created 2015-12-14 by Linear Technology). This is a mirror of the Linear Technology rev E datasheet, not analog.com itself.

- Voltaic: https://voltaicsystems.com/6-watt-panel/ (WebFetch and curl): now 301 to /p105 (the P105 5 W page). https://voltaicsystems.com/P106 -> /6-watt-panel/ -> /p105. https://voltaicsystems.com/P106C: 404. https://voltaicsystems.com/P109 -> /9-watt-panel/ -> P110 page.
- Voltaic Wayback: CDX list https://web.archive.org/cdx/search/cdx?url=voltaicsystems.com/6-watt-panel/ ; snapshots 20240416145752 and 20251215144022 read (SKU P106C, 7.7 V / 6.5 V / 930 mA / 6.0 W; EOL notice in the 2025-12-15 snapshot).
- Voltaic datasheets: https://voltaicsystems.com/content/P105_ds.pdf and P126_ds.pdf (Aug 2026, with revision tables): USED. P106_ds, P106C_ds, P108_ds, P109_ds, P110_ds, P120_ds .pdf: 404 (guessed paths). DEAD END.
- Voltaic collection table https://voltaicsystems.com/solar-panels/ (WebFetch summary): USED for Isc of P110, P120, P124, P108, P152; its Vmp/Voc for P110 and P120 (6.2 / 7.3 V) disagree with the product pages (5.71 / 6.94 V and 5.21 / 6.61 V).
- Voltaic product pages (curl): /5-watt-panel-etfe/, /10-watt-panel-etfe/, /9-watt-18v-panel-etfe/, /20-watt-6-volt-solar-panel-etfe/, /P126/, /1-watt-6-volt-solar-panel-etfe/: USED. None publishes a temperature coefficient.
- Temperature coefficient for Voltaic panels: no Voltaic source publishes one. USED instead: SunPower Maxeon Gen III cell sheet, https://midsummerwholesale.co.uk/pdfs/sunpower-back-contact-gen3-solar-cell-ds-en-a4-m3.pdf : "Temp. Coefficients in SunPower Panels: Voltage: -1.74 mV/C, Power: -0.30 %/C"; typical cell Voc 0.72-0.73 V. Derived -1.74/730 = -0.238 %/C. Voltaic P105/P126 datasheets name SunPower Maxeon Gen III and Gen V cells. The Gen V coefficient was not found; applying the Gen III value to Gen V revisions is an ASSUMPTION. https://mikrocontroller.net/attachment/238825/sunpower_c60_bin.pdf returned HTML, DEAD END. https://voltaicsystems.com/content/Voltaic%20Systems%20P123%20R1G.pdf: drawing only, no coefficient.
- Voltaic P106C reseller: https://dasenic.com/product/voltaic-systems-p106-c-6790470 (WebFetch): 6.22 W, Voc 7.67 V, Vmp 6.5 V, Imp 960 mA, Isc 1.02 A, "Active". The prior note's "6.0 V / 7.0 V" reseller figure for the P106C was NOT reproduced anywhere I looked.
- Adafruit (curl): https://www.adafruit.com/product/200 , 500, 1525, 2747, 3809, 5366, 5367, 5368, 5369, 5856: USED. 200/500/1525/2747 "No longer stocked", 3809 out of stock; current stock is Voltaic ETFE (P105, P110, P124, P126, P123), relabeled "5V" except P126.
- SparkFun (curl): https://www.sparkfun.com/products/13781, 13783, 16837, 13780, 13779, 13778, 9241, 7840, 16834, 18730: 404. 13782 and 16835 (10 W USB charger), 18723, 18724, 18725, 18726: all "retired". Category https://www.sparkfun.com/components/power/solar.html lists only those retired Voltaic ETFE panels, the 10 W USB charger and the Sunny Buddy. No current SparkFun 6 V panel above 1.2 W was found.
- Campbell Scientific: https://s.campbellsci.com/documents/us/manuals/sp10-10r-20-20r.pdf and https://www.campbellsci.com/sp10 , /sp20: USED. No Voc or Isc published.
- Renogy: https://www.mygenerator.com.au/assets/files/RNG-10D-SS-Product-Card.pdf , RNG-30D-SS, RNG-50D-SS: USED. RNG-20D-SS / RNG-20D card URLs: 404. https://solartown.com/content/renogy/batteries/10D-SS-Datasheet.pdf: 403. DEAD END.
- Ameresco: https://www.mrsolar.com/content/pdf/Ameresco/Ameresco-Solar-20J-V-2024.pdf and Ameresco-Solar-10M-V-2024.pdf: USED. A 10J sheet was not found.
- Okapi netlist (read-only): kicad-cli sch export netlist of /home/awickert/Dropbox/NorthernWidget/github/Project-Okapi/Hardware/KiCAD-10import/Okapi.kicad_sch into the session scratchpad. U4 = LT3652EDD#PBF; R22 143k, R69 100k, R71 1M, R70 200k; R70's bottom goes to Q8 (2N7002) drain, Q8 gate on MPPT_CHRG (pulled to 3V3_CORE by R55 1M); BOOST through D2 from V_LI (no separate BOOST supply); TIMER (pin 6) on GND; NTC (pin 8) unconnected; SENSE (pin 10) and BAT (pin 9) both on V_LI (no sense resistor; already filed as #32 per DECISIONS.md).

## LT3652 datasheet values

Source for every number in this section: LT3652 datasheet rev E (3652fe), mirror https://www.rlocman.ru/i/File/2017/09/30/3652fe.pdf, Electrical Characteristics (p. 3), Pin Functions (p. 6), Applications Information (pp. 9, 15, 16).

| Symbol | Parameter | Min | Typ | Max | Note |
|---|---|---|---|---|---|
| VIN_REG(TH) | Input regulation reference | 2.65 V | 2.7 V | 2.75 V | over full temperature range |
| IIN_REG | VIN_REG bias current | | 35 nA | 100 nA | over full temperature range |
| VSHDN | Shutdown threshold, rising | 1.15 V | 1.2 V | 1.25 V | over full temperature range |
| VSHDN(HYST) | Shutdown hysteresis | | 120 mV | | 25 C typical only |
| ISHDN | SHDN input bias current | | -10 nA | | typical only; pin text: "Typical SHDN pin input bias current is 10nA" |
| VIN | Operating range | 4.95 V | | 32 V | VBAT = 4.2 V |
| | VIN start voltage | 7.5 V | | | VBAT = 4.2 V; Note 4: start = VBAT(FLT) + 3.3 V |
| VIN(OVLO) | OVLO threshold, rising | 32 V | 35 V | 40 V | 1 V hysteresis |
| VIN(UVLO) | UVLO threshold, rising | | 4.6 V | 4.95 V | 0.2 V hysteresis |
| | Absolute maximum VIN, SW | | | 40 V | VIN_REG, SHDN: VIN + 0.5 V, 40 V |

Quoted behavior (p. 6, VIN_REG pin): "Maximum charge current is reduced when this pin is below 2.7V ... The LT3652 servos the maximum charge current required to maintain the programmed operational VIN voltage, through maintaining the voltage on VIN_REG at or above 2.7V."

Quoted behavior (p. 16): "If an input supply cannot provide enough power to satisfy the requirements of an LT3652 charger, the supply voltage will collapse. A minimum operating supply voltage can thus be programmed by monitoring the supply through a resistor divider, such that the desired minimum voltage corresponds to 2.7V at the VIN_REG pin." Divider: RIN1/RIN2 = (VIN(MIN)/2.7) - 1.

Quoted (p. 16, MPPT temperature compensation): Voc temperature coefficient is "similar to a common p-n diode, or about -2mV/C" per cell, and "the temperature coefficient for the peak power point is similar to that of VOC" (Vmp approximated as a fixed offset below Voc). Worked example: 36-cell panel, Voc 21.7 V, Vmp 17.6 V, TC -78 mV/C, LM234 compensation network.

Quoted (p. 9, start-up): "If there is no BOOST supply available, the internal switch requires (VIN - VSW) >= 3.3V to reliably operate ... When an LT3652 charger is not switching, the SW pin is at the same potential as the battery ... for reliable start-up, the VIN supply must be at least 3.3V above VBAT(FLT). Once switching begins and the BOOST supply capacitor gets charged such that (VBOOST - VSW) > 2V, the VIN requirement no longer applies." Pin text (p. 6): "(VIN - VBAT(FLT)) >= 0.75V is the minimum operating voltage, provided (VBOOST - VSW) >= 2V."

Consequences for the dividers (my arithmetic, from the values above):
- VIN_REG tolerance from the reference alone: 2.65/2.7 = -1.85 %, 2.75/2.7 = +1.85 %. At 6.56 V that is 6.44 to 6.68 V before resistor tolerance.
- SHDN: falling threshold is about 1.2 - 0.12 = 1.08 V at the pin, so a divider that starts at 7.2 V stops at about 7.2 x 1.08/1.2 = 6.48 V (typical hysteresis, 25 C only).
- Bias error: 100 nA max into the VIN_REG divider's Thevenin resistance (R22 || R69 = 143k || 100k = 58.8k today) is 5.9 mV at the pin, 14 mV at VIN. 10 nA typical SHDN bias into 1M || 200k = 167k is 1.7 mV at the pin. Both are small against the 1.85 % / 4 % reference tolerances. The dividers could go to roughly 3x higher resistance before bias error rivals 1 % resistor tolerance.
- The 7.5 V start requirement (with a full 4.2 V cell and no BOOST supply) is the reason the charging-start voltage matters: a SHDN threshold below VBAT + 3.3 V can enable the IC before it can reliably switch. With a partly discharged cell (3.7 V) the requirement is 7.0 V.

## Panel rows (appended as confirmed)

| Panel | Vmp (V) | Voc (V) | Imp (A) | Isc (A) | P (W) | TC Voc | TC Vmp | Source |
|---|---|---|---|---|---|---|---|---|
| Voltaic P106C, 6 W 6 V (END OF LIFE) | 6.5 | 7.7 | 0.93 | not listed | 6.0 | not published | not published | Wayback snapshot https://web.archive.org/web/20240416145752/https://voltaicsystems.com/6-watt-panel/ (SKU P106C); EOL text in https://web.archive.org/web/20251215144022/https://voltaicsystems.com/6-watt-panel/ : "This product is End of Life. We suggest the P105 as an alternative." Live URL https://voltaicsystems.com/6-watt-panel/ now 301-redirects to /p105 (curl -I, 2026-11-09); https://voltaicsystems.com/P106C returns 404 |
| Voltaic P105 R9C, 5 W 6 V ETFE (nominal) | 6.23 | 7.28 | 0.95 | 1.00 | 5.89 | not published | not published | https://voltaicsystems.com/content/P105_ds.pdf (Aug 2026); page https://voltaicsystems.com/5-watt-panel-etfe/ says Peak Current 1000mA |
| Voltaic P105 R9C ("Expected", after real-world losses) | 6.01 | 7.07 | 0.83 | 0.93 | 4.98 | | | same datasheet |
| Voltaic P105 R7D/R7E (produced to 2025-05/06) | 5.21 | 6.61 | 1.06-1.07 | 0.95-0.96 | 5.51-5.55 | | | P105_ds.pdf revision table |
| Voltaic P105 R7C/R6M (to 2024-11) | 6.07 | 7.09 | 0.90 | 0.99 | 5.49 | | | P105_ds.pdf revision table |
| Voltaic P105 R5A (to 2021-08) | 5.71 | 6.94 | 0.86 | 0.90 | 4.91 | | | P105_ds.pdf revision table |
| Voltaic P126, 2 W 6 V ETFE R3C (nominal) | 7.48 | 8.74 | 0.35 | 0.37 | 2.62 | not published | not published | https://voltaicsystems.com/content/P126_ds.pdf ; Expected 7.21 / 8.48 V; earlier revisions Vmp 7.09-7.33, Voc 8.51-8.76 |
| Voltaic P124, 1.2 W 6 V ETFE | 6.23 | 7.28 | 0.22 | 0.23 (listing) | 1.35 | not published | not published | https://voltaicsystems.com/1-watt-6-volt-solar-panel-etfe/ ; Isc from https://voltaicsystems.com/solar-panels/ table |
| Voltaic P110, 10 W 6 V ETFE (product page) | 5.71 | 6.94 | 1.67 | 1.99 (listing) | 9.54 | not published | not published | https://voltaicsystems.com/10-watt-panel-etfe/ ; collection table https://voltaicsystems.com/solar-panels/ instead says 6.2 / 7.3 V, 1.89 A, 11.8 W (newer revision, UNVERIFIED which ships) |
| Voltaic P109, 9 W 6 V | | | | | | | | https://voltaicsystems.com/P109 -> /9-watt-panel/ -> now redirects to P110 page (curl); search summary says "not in production", P110 suggested. Specs not retrieved. |
| Voltaic P120, 20 W 6 V ETFE (product page) | 5.21 | 6.61 | 4.46 | 4.17 (listing) | 23.21 | not published | not published | https://voltaicsystems.com/20-watt-6-volt-solar-panel-etfe/ ; collection table says 6.2 / 7.3 V, 3.96 A, 24.7 W (UNVERIFIED which ships) |
| Voltaic P108, 9 W 18 V ETFE (product page) | 17.34 | 20.45 | 0.57 | 0.60 (listing) | 9.92 | not published | not published | https://voltaicsystems.com/9-watt-18v-panel-etfe/ ; collection table says 19.2 / 22.1 V, 0.57 A, 10.9 W |
| Voltaic P152, 25 W 18 V | 17.9 | 20.7 | 1.60 | 1.67 | 28.7 | not published | not published | https://voltaicsystems.com/solar-panels/ table (product page not fetched) |
| Adafruit 5367, "5V 5W ETFE [Voltaic P105]" (in stock) | 6.12 | 7.13 | 0.94 | not listed | 5.75 | not published | not published | https://www.adafruit.com/product/5367 (older P105 revision figures; Voltaic now says 6.23 / 7.28) |
| Adafruit 5369, "5V 10W ETFE [Voltaic P110]" (in stock) | 5.71 | 6.94 | 1.67 | not listed | 9.54 | not published | not published | https://www.adafruit.com/product/5369 |
| Adafruit 5366, "6V 2W ETFE [Voltaic P126]" (in stock) | 7.28 | 8.51 | 0.33 | not listed | 2.37 | not published | not published | https://www.adafruit.com/product/5366 |
| Adafruit 5368, "5V 1.2W ETFE [Voltaic P124]" (in stock) | 6.07 | 7.09 | 0.20 | not listed | 1.22 | not published | not published | https://www.adafruit.com/product/5368 |
| Adafruit 2747, Colossal 6V 9W (No longer stocked) | 6.5 | 7.7 | 1.42 | not listed | 9.2 | not published | not published | https://www.adafruit.com/product/2747 |
| Adafruit 3809, Small 6V 1W (Out of stock) | 6.5 | 7.7 | 0.18 | not listed | 1.2 | not published | not published | https://www.adafruit.com/product/3809 |
| Adafruit 200 / 500 / 1525, Medium 2W / Large 3.5W / Huge 6W 6V (all "No longer stocked"; Adafruit points to P126 / P105 / P110) | not extracted | | | | 2 / 3.5 / 6 | | | https://www.adafruit.com/product/200 , /500 , /1525 |
| SparkFun PRT-18726, 1.2 W 6 V ETFE (Voltaic P124; RETIRED) | 6.07 | 7.09 | 0.20 | not listed | 1.22 | not published | not published | https://www.sparkfun.com/products/18726 ("This product has been retired from our catalog") |
| SparkFun PRT-18725, 0.6 W 6 V ETFE (Voltaic P123; RETIRED) | 6.07 | 7.09 | 0.11 | not listed | 0.64 | not published | not published | https://www.sparkfun.com/products/18725 |
| SparkFun PRT-16835, Solar Panel Charger 10W (USB 5 V output; RETIRED) | "around 6V" | not listed | 1.7 | not listed | 10 | | | https://www.sparkfun.com/products/16835 ; has a 5 V USB regulator, not a raw panel; not suited to the LT3652 MPPT |
| Campbell Scientific SP10, 10 W 12 V-nominal (logger-industry panel) | 16.8 | not published | 0.59 | not published | 10 | -0.37 %/C (Voc) | not published | https://s.campbellsci.com/documents/us/manuals/sp10-10r-20-20r.pdf ; https://www.campbellsci.com/sp10 |
| Campbell Scientific SP20, 20 W 12 V-nominal | 16.8 | not published | 1.19 | not published | 20 (18 guaranteed min) | -0.38 %/C (Voc) | not published | same manual; https://www.campbellsci.com/sp20 |
| Renogy RNG-10D-SS, 10 W 12 V (32 cells) | 18 | 21.6 | 0.56 | 0.61 | 10 | -0.33 %/C (Voc) | not published (Pmax -0.23 %/C) | https://www.mygenerator.com.au/assets/files/RNG-10D-SS-Product-Card.pdf (Renogy product card, reseller-hosted) |
| Renogy RNG-30D-SS, 30 W 12 V (32 cells; above the 5-20 W brief, included as the nearest Renogy size retrieved) | 18.0 | 21.6 | 1.67 | 1.82 | 30 | -0.28 %/C (Voc) | not published (Pmax -0.37 %/C) | https://www.mygenerator.com.au/assets/files/RNG-30D-SS-Product-Card.pdf |
| Renogy RNG-20D-SS, 20 W 12 V | not retrieved | | | | 20 | | | product card URL pattern 404; search found only a multi-model sheet with unlabeled columns. UNVERIFIED |
| Ameresco Solar 20J, 20 W 12 V (36 cells), STC | 18.2 | 22.2 | 1.10 | 1.20 | 20 | -0.360 %/C (Voc) | not published (Pmax -0.45 %/C) | https://www.mrsolar.com/content/pdf/Ameresco/Ameresco-Solar-20J-V-2024.pdf |
| Ameresco Solar 20J at NMOT (800 W/m2, module 47 C) | 16.3 | 19.9 | 0.88 | 0.98 | 14.4 | | | same datasheet, second column |
| Ameresco Solar 10M, 10 W 12 V (36 cells), STC | 18.1 | 21.8 | 0.55 | 0.62 | 10 | -0.360 %/C (Voc) | not published | https://www.mrsolar.com/content/pdf/Ameresco/Ameresco-Solar-10M-V-2024.pdf ; NMOT: 16.2 V Vmp, 19.7 V Voc, 7.2 W |

Note on the part grade: Okapi's U4 is LT3652EDD#PBF (netlist). Datasheet Note 2: the E grade "is guaranteed to meet performance specifications from 0C to 125C junction temperature"; -40C to 125C is "assured by design, characterization, and correlation". The I grade (LT3652IDD) is guaranteed over -40C to 125C.

## Task 2: Voc at -40 C, and fit against v0.7.0 (16 V) and v0.8.0 (32 V)

Script: scratchpad calc/voc_cold.py (session scratchpad, not committed). Voc(-40) = Voc(25) x (1 + TC x (-65 C)). TC column: "pub" is the panel's own datasheet; "SPW" is -0.238 %/C derived from the SunPower Gen III cell sheet (Voltaic publishes none); "ASM" is ASSUMED -0.30 %/C. The -0.30 %/C column is given for every row for comparison. Hot and cold Vmp use the same V/C as Voc, which is the LT3652 datasheet's own approximation (p. 16). This is a cold-sky worst case: it assumes full irradiance on a -40 C module.

| Panel | Vmp 25C | Voc 25C | TC %/C | TC source | Voc at -40C | Voc at -40C, -0.30 %/C | v0.7.0 16 V | v0.8.0 32 V | Voc at 60C | Vmp at 60C | Vmp at -10C |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Voltaic P105 R9C nominal | 6.23 | 7.28 | -0.238 | SPW | 8.41 | 8.70 | ok | ok | 6.67 | 5.62 | 6.84 |
| Voltaic P105 R9C expected | 6.01 | 7.07 | -0.238 | SPW | 8.17 | 8.45 | ok | ok | 6.48 | 5.42 | 6.60 |
| Voltaic P105 R7D/R7E | 5.21 | 6.61 | -0.238 | SPW | 7.63 | 7.90 | ok | ok | 6.06 | 4.66 | 5.76 |
| Voltaic P110 (product page) | 5.71 | 6.94 | -0.238 | SPW | 8.02 | 8.29 | ok | ok | 6.36 | 5.13 | 6.29 |
| Voltaic P110 / P120 (collection table) | 6.20 | 7.30 | -0.238 | SPW | 8.43 | 8.72 | ok | ok | 6.69 | 5.59 | 6.81 |
| Voltaic P120 (product page) | 5.21 | 6.61 | -0.238 | SPW | 7.63 | 7.90 | ok | ok | 6.06 | 4.66 | 5.76 |
| Voltaic P124 | 6.23 | 7.28 | -0.238 | SPW | 8.41 | 8.70 | ok | ok | 6.67 | 5.62 | 6.84 |
| Voltaic P126 nominal | 7.48 | 8.74 | -0.238 | SPW | 10.09 | 10.44 | ok | ok | 8.01 | 6.75 | 8.21 |
| Voltaic P126 expected | 7.21 | 8.48 | -0.238 | SPW | 9.79 | 10.13 | ok | ok | 7.77 | 6.50 | 7.92 |
| Voltaic P106C (EOL) | 6.50 | 7.70 | -0.30 | ASM | 9.20 | 9.20 | ok | ok | 6.89 | 5.69 | 7.31 |
| Adafruit 2747 / 3809 (legacy) | 6.50 | 7.70 | -0.30 | ASM | 9.20 | 9.20 | ok | ok | 6.89 | 5.69 | 7.31 |
| Voltaic P108 (product page) | 17.34 | 20.45 | -0.238 | SPW | 23.62 | 24.44 | NO | ok | 18.74 | 15.63 | 19.05 |
| Voltaic P108 (collection table) | 19.20 | 22.10 | -0.238 | SPW | 25.52 | 26.41 | NO | ok | 20.26 | 17.36 | 21.04 |
| Voltaic P152 | 17.90 | 20.70 | -0.238 | SPW | 23.91 | 24.74 | NO | ok | 18.97 | 16.17 | 19.63 |
| Renogy RNG-10D-SS | 18.00 | 21.60 | -0.33 | pub | 26.23 | 25.81 | NO | ok | 19.11 | 15.51 | 20.49 |
| Renogy RNG-30D-SS | 18.00 | 21.60 | -0.28 | pub | 25.53 | 25.81 | NO | ok | 19.48 | 15.88 | 20.12 |
| Ameresco 20J | 18.20 | 22.20 | -0.36 | pub | 27.39 | 26.53 | NO | ok | 19.40 | 15.40 | 21.00 |
| Ameresco 10M | 18.10 | 21.80 | -0.36 | pub | 26.90 | 26.05 | NO | ok | 19.05 | 15.35 | 20.85 |
| Campbell SP10 (Voc ASSUMED 21.7) | 16.80 | 21.7 | -0.37 | pub TC, Voc ASSUMED | 26.92 | 25.93 | NO | ok | 18.89 | 13.99 | 19.61 |
| Campbell SP20 (Voc ASSUMED 21.7) | 16.80 | 21.7 | -0.38 | pub TC, Voc ASSUMED | 27.06 | 25.93 | NO | ok | 18.81 | 13.91 | 19.69 |

The Campbell Voc of 21.7 V is ASSUMED: it is the LT3652 datasheet's "common 36-cell" example, and Campbell publishes no Voc. Every 12 V-nominal panel fails v0.7.0's 16 V even at 25 C (Voc 20.45-22.2 V). Every panel fits v0.8.0's 32 V at -40 C (largest 27.39 V, Ameresco 20J), which also stays below the LT3652's minimum OVLO threshold of 32 V.

## Task 3: proposed set points and divider pairs, by panel class

Formulas: VIN_REG = 2.7 V x (1 + R22/R69); VSTART = 1.2 V x (1 + R71/R70). Script: scratchpad calc/pairs.py. All 0603, 1 %. Every value below is computed, not measured.

Two facts from the netlist and the datasheet shape the start voltage:
1. Okapi has no separate BOOST supply (D2 from V_LI), so the datasheet start-up rule applies: VIN - VBAT >= 3.3 V, i.e. 7.5 V with the cell at 4.2 V and 7.0 V with the cell at 3.7 V.
2. R70 returns through Q8, gated by !CHRG. Once charging current exceeds C/10, !CHRG goes low, Q8 opens, and SHDN is pulled to V_SOLAR_IN through R71. Charging then continues down to VIN_REG (or UVLO). When current falls below C/10 (dim light, or VIN_REG throttling), !CHRG releases, the divider reconnects, and the falling threshold is about 0.9 x VSTART (1.08 V / 1.2 V, typical hysteresis). If VIN_REG is below 0.9 x VSTART, a cloudy spell shuts the charger off and it needs Voc >= VSTART to restart.

| Class | Panels | Proposed VIN_REG | R22 / R69 | Computed | Proposed start | R71 / R70 | Computed |
|---|---|---|---|---|---|---|---|
| A: 10-cell "5 V / 6 V" ETFE | Voltaic P105, P110, P120, P124; Adafruit 5367, 5368, 5369 | about 5.9 V | 143k (kept) / 120k (E24) | 5.917 V | about 7.0 V | 1M (kept) / 205k (E96) | 7.054 V |
| A, alternative (favors hot summer, old R7 revisions) | same | about 5.67 V | 100k / 91k (preferred set) | 5.667 V | | 1.62M / 330k (preferred set) | 7.091 V |
| B: 12-cell and legacy urethane 6 V | Voltaic P126 (Adafruit 5366), P106C (EOL), Adafruit 2747 / 3809 (legacy) | about 6.5 V | 130k / 91k (preferred set), or today's 143k / 100k | 6.557 V (6.561 V) | 7.5 V | 1.05M (E96) / 200k (kept) | 7.500 V |
| B, P126 only, winter-weighted | Voltaic P126 | about 7.0 V | 160k / 100k (E24) | 7.020 V | 7.5 V, or 7.87 V | 1M / 180k (preferred set) | 7.867 V |
| C: 36-cell 12 V-nominal, v0.8.0 only | Campbell SP10, SP20; Renogy RNG-10D-SS; Ameresco 10M, 20J; Voltaic P108, P152 | about 16.2 V | 1M / 200k (E24) | 16.200 V | about 13 V | 1M (kept) / 100k (preferred set) | 13.200 V |
| C, preferred-set only | same | | 1.62M / 330k | 15.955 V | | | |
| C, winter-weighted | same | about 17.5 V | 1M / 180k (preferred set) | 17.700 V | | | |

Reasoning per class (the set points are proposals for Andy to decide):
- Class A. Vmp at 25 C spans 5.21-6.23 V across shipped revisions (P105 datasheet revision table; P110 and P120 product pages). 5.9 V is near Vmp for an R9C P105 at about 45 C module temperature and close to the 25 C Vmp of the current revisions. It keeps R22 and changes only R69 (issue #20 already proposed R69 = 120k). The floor is set by the buck: duty cycle max 90 % (datasheet p. 4) and the 4.95 V maximum UVLO rising threshold mean VIN_REG much below about 5.2 V leaves no headroom for a 4.2 V float. The start voltage of 7.0 V matches VBAT + 3.3 V for a cell at 3.7 V, which is the state in which charging matters; it is 0.5 V below the datasheet's full-cell figure, so a nearly full cell may not restart. That is a proposal, not a datasheet guarantee.
- Class B. 6.56 V is today's value and sits within 1 % of the 25 C Vmp of the P106C and Adafruit legacy panels (6.5 V). The P126's Vmp is higher (7.21-7.48 V), so it gives up some power at 6.56 V in winter. 7.5 V start is the datasheet's full-cell figure, and class B Voc (7.7-8.74 V at 25 C) reaches it except on hot days for the 7.7 V panels.
- Class C. 16.2 V sits between STC Vmp (16.8-18.2 V) and the Ameresco NMOT Vmp (16.2-16.3 V at 800 W/m2, 47 C module). The divider current is 16.2 V / 1.2M = 13.5 uA. The start voltage has headroom to spare: any value above 7.5 V satisfies the start rule, and 13.2 V keeps R71 at 1M and sits below hot Voc (about 19 V at 60 C).

Tolerance per set point (worst case, computed): VIN_REG reference +/-1.85 %, plus 1 % resistors contributing up to about 2 % x R22/(R22+R69). Class A 5.92 V: about +/-3.0 % (5.74-6.10 V). Class C 16.2 V: about +/-3.5 % (15.6-16.8 V). SHDN reference +/-4.2 % (1.15-1.25 V), so today's 7.2 V start is 6.90-7.50 V before resistor tolerance. Bias error: 100 nA max into 166.7k (1M || 200k) is 16.7 mV at VIN_REG, 0.1 V at VIN for class C, 0.6 %.

## Task 4: how Vmp moves, and whether erring high is safe

What the datasheet says (rev E, pp. 6 and 16): the VIN_REG loop servos charge current down to hold VIN_REG at or above 2.7 V. It is a minimum-input-voltage loop and does not seek the peak. "If an input supply cannot provide enough power ... the supply voltage will collapse" is the case WITHOUT the divider. With the divider at any set point, the charger throttles instead of collapsing the panel. The datasheet does not claim that a high set point is safer than a low one.

The claim in our earlier note ("erring high is safe: the charger throttles rather than collapsing the panel") is therefore half right. It is true that the panel never collapses, whichever way the set point errs. It is not true that erring high costs nothing. When the panel is power-limited the operating point IS the set point, and the I-V curve falls steeply above Vmp. When hot Voc drops below the set point, charge current goes to zero.

Model (ASSUMED; scratchpad calc/ivmodel.py): ideal-diode I-V, no series resistance, curvature fitted to each panel's published Vmp and Voc, Voc shifted by the temperature coefficient and by a ln(G) for irradiance. It exaggerates the drop of Vmp at low irradiance, so read it for shape, not for exact percentages. Fraction of the available maximum power delivered at each set point:

| Panel | Module T, irradiance | Model Vmp | 5.67 V | 5.94 V | 6.21 V | 6.56 V |
|---|---|---|---|---|---|---|
| P105 R9C | -20 C, 1.0 sun | 7.08 | 0.83 | 0.87 | 0.91 | 0.96 |
| P105 R9C | 0 C, 0.2 sun | 6.19 | 0.95 | 0.99 | 1.00 | 0.95 |
| P105 R9C | 25 C, 1.0 sun | 6.23 | 0.95 | 0.98 | 1.00 | 0.96 |
| P105 R9C | 45 C, 1.0 sun | 5.86 | 0.99 | 1.00 | 0.96 | 0.74 |
| P105 R9C | 65 C, 1.0 sun | 5.49 | 0.99 | 0.92 | 0.73 | 0.09 |
| P105 R7D | 25 C, 1.0 sun | 5.21 | 0.95 | 0.84 | 0.63 | 0.11 |
| P105 R7D | 45 C, 1.0 sun | 4.88 | 0.80 | 0.57 | 0.17 | 0.00 |

| Panel | Module T, irradiance | Model Vmp | 14.97 V | 15.95 V | 16.20 V | 17.13 V | 17.70 V |
|---|---|---|---|---|---|---|---|
| Ameresco 20J | -20 C, 1.0 sun | 21.96 | 0.72 | 0.77 | 0.78 | 0.83 | 0.85 |
| Ameresco 20J | 25 C, 1.0 sun | 18.20 | 0.88 | 0.93 | 0.95 | 0.98 | 1.00 |
| Ameresco 20J | 45 C, 1.0 sun | 16.58 | 0.96 | 0.99 | 1.00 | 0.99 | 0.97 |
| Ameresco 20J | 65 C, 1.0 sun | 14.99 | 1.00 | 0.97 | 0.96 | 0.83 | 0.68 |

How Vmp moves: temperature lowers Vmp at roughly the Voc coefficient in V/C (datasheet p. 16): about -17 mV/C for a 10-cell Voltaic panel and about -80 mV/C for the Ameresco 20J, so a 60 C summer module sits 0.6 V (class A) or 2.8 V (class C) below its 25 C Vmp, and a -10 C winter module sits the same amount above. Irradiance moves Vmp less, roughly logarithmically, and in the same direction as cold-to-hot (dimmer is lower). The implication: erring low costs power roughly in proportion to (Vmp - set point)/Vmp, which is gentle. Erring high costs power steeply and goes to zero once hot Voc passes the set point (P105 R7D at 6.56 V: 11 % at 25 C, none at 45 C). The case for erring a little high is Minnesota winter, when energy is scarce and modules are cold (Vmp above STC). The case against is summer heat and the low-Vmp revisions Voltaic has shipped under the same SKU. The floor for erring low is the buck's headroom (about 5.2 V for a 4.2 V float, from the 90 % maximum duty cycle) and the 4.95 V UVLO.

## Surprises

1. The README's recommended panel no longer exists. https://voltaicsystems.com/6-watt-panel/ now 301-redirects to the P105 (5 W). The P106C was marked End of Life by Voltaic (archived 2025-12-15, "We suggest the P105 as an alternative"). The README link therefore now recommends a 5 W panel with Voc 7.28 V nominal and 7.07 V "expected".
2. Today's 7.2 V start voltage is at or above the 25 C Voc of every class A panel Voltaic sells (6.61-7.30 V nominal; 7.07 V expected for the P105 R9C). On a warm day such a panel cannot start the charger at all, and the SHDN tolerance (6.90-7.50 V) makes it a coin toss even at 25 C. The 7.2 V is also below the datasheet's 7.5 V full-cell start rule. A 10-cell panel cannot satisfy both: this is a mismatch between 10-cell panels and an LT3652 charging a 4.2 V cell without a separate BOOST supply, not a resistor problem.
3. Voltaic has changed the P105's electrical spec under one SKU: Vmp 5.21 V (R7D, R7E, to mid-2025) to 6.23 V (R9C). The same spread shows between Voltaic's own product pages and collection table for the P110 and P120. A user cannot know Vmp from the SKU alone.
4. Voltaic sells no 9 V or 12 V class panels now: only 2 V, 4 V, 6 V and 18 V. The P109 (9 W 6 V) redirects to the P110.
5. Adafruit's and SparkFun's own 6 V urethane panels are discontinued or retired. Adafruit now resells Voltaic ETFE, relabeled "5V". SparkFun lists no 6 V panel above 1.2 W.
6. The prior note's "P106C at 6.0 V / 7.0 V from resellers" was not reproduced. Voltaic's archived page gives 6.5 / 7.7 V, and the one reseller checked gives 6.5 / 7.67 V.
7. Voltaic publishes no temperature coefficient for any panel. The -0.238 %/C used here is derived from SunPower's Gen III cell sheet.
8. In the netlist, NTC is unconnected, which disables the 0-40 C battery-temperature window, so the charger will charge a Li-ion cell below 0 C in a Minnesota winter. Outside this brief, but it bears on the winter-weighted set points.

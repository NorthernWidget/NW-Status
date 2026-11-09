# COMPLETE

# Fresh AA and D cell voltages: sourced figures (agent report, 2026-11-09)

Question: how a Margay logger should choose between USB power (4.75-5.25 V at the port) and a 3xAA pack (board accepts 3.3-5.5 V). Recollection to check: fresh alkaline AA is about 1.7 V per cell. Earlier figure from memory: about 1.6 V per cell (4.8 V per pack).

## Sources checked (log, dead ends included)

- https://data.energizer.com/pdfs/alkaline_appman.pdf : OK (PDF, 2018, "Alkaline Manganese Dioxide Handbook and Application Manual", Energizer Brands). Used.
- https://data.energizer.com/pdfs/lithiuml91l92_appman.pdf : OK (PDF, 2017, "Cylindrical Primary Lithium Handbook and Application Manual", Form No. 12004-A). Used.
- https://data.energizer.com/pdfs/typical_characteristics.pdf : OK (PDF, "Principal Dry Battery Systems, Typical Characteristics"). Nominal voltages and operating ranges only; no OCV.
- https://data.energizer.com/pdfs/E91.pdf : DEAD (404, HTML page).
- https://data.energizer.com/pdfs/L91.pdf : DEAD (404, HTML page).
- https://data.energizer.com/pdfs/E91_Max_NA.pdf : DEAD (404, HTML page).
- https://data.energizer.com/pdfs/alk-power-aa.pdf : DEAD (404).
- https://data.energizer.com/pdfs/ep91_ap.pdf : DEAD (404). Energizer's /pdfs/ product sheets appear to have moved; the handbooks still resolve.
- https://courses.egr.uh.edu/ECE/ECE2100/Archive/Spring%202024%20Honors/E91.pdf : OK. Mirror of Energizer E91 product datasheet, Form No. EBC-1102Q (PDF created 2015, modified 2016). Manufacturer document, third-party host. Used. No OCV stated.
- https://files.batteryjunction.com/frontend/files/L91.pdf : OK. Mirror of Energizer L91 product datasheet, Form No. EBC-4201M (PDF dated 2007). Manufacturer document, third-party host. Used. No OCV stated.
- https://www.ece.ucsb.edu/~ilan/Classes/ECE2A_F2010/Labs/Datasheets/Duracell%20AA%20MN1500%20LR6.pdf : OK. Mirror of Duracell MN1500 Coppertop datasheet "MN1500_US_CT", dated 6/08. Used.
- https://www.ee.columbia.edu/sites/default/files/content/docs/Duracell%20AA%20battery.pdf : OK. Mirror of Duracell MN1500 Coppertop datasheet MN15CTUS0413. Used (curves only; no OCV).
- https://www.webstaurantstore.com/documents/specsheets/mn15usct0122-a.pdf : OK. Duracell MN15USCT0122. Nominal 1.5 V, impedance 80 mOhm at 1 kHz, operating -20 C to 54 C. No OCV.
- Scope update from the owner (mid-task): alkaline AA and alkaline D are the standard packs and the priority. D cells added below.
- https://files.batteryjunction.com/frontend/files/energizer/datasheet/ENERGIZER-E95-UpdatedDataSheet.pdf : OK. Mirror of Energizer E95 datasheet, Form No. E95NA0323. Used.
- https://www.bto.pl/pdf/05306/e95.pdf : OK. Older Energizer E95 datasheet, Form No. EBC-1105-P. Same headline figures.
- https://data.energizer.com/pdfs/ep95.pdf : DEAD (404).
- https://www.farnell.com/datasheets/3550005.pdf : DEAD for this session (curl timed out at 60 s, no bytes).
- https://images.toolsid.com/duracell/items/pdf/mn1300b2-information.pdf : OK. Mirror of Duracell MN1300 Coppertop D datasheet, MN13CTUS0413. Used.
- https://static.rapidonline.com/pdf/658023_da_en_01.pdf : OK. Generic "PRODUCT SPECIFICATION, Alkaline battery, 1.5 volts, LR6", sold by Rapid Electronics; maker not named on the sheet. Not a major brand. Used, labeled as such.
- https://cdn-shop.adafruit.com/product-files/3349/AA_LR6_1.5V.pdf : OK. Generic Chinese maker's LR6 specification hosted by Adafruit (company address "Meitai Technology Park"). Not a major brand. Used, labeled as such.
- https://pdf.directindustry.com/pdf/panasonic-industry-europe-gmbh/batteries-panasonic-alkaline-handbook-professionals/15208-945022.html : DEAD (403 to WebFetch). A search-engine summary claimed this Panasonic handbook gives alkaline OCV "between about 1.55 V and 1.65 V"; NOT verified, because the document could not be read.
- https://eu.industrial.panasonic.com/sites/default/pidseu/files/downloads/files/id_alkaline_1203_e.pdf : DEAD (returns an HTML/JavaScript page, not the PDF).
- https://energy.panasonic.cn/dam/master/pdf/jp/material/dry/Overview_of_dry_batteries_20240701.pdf : DEAD (404).
- https://static6.arrow.com/.../nasonic-batteries-alkaline-for-professionals_interactive.pdf : DEAD for this session (HTTP/2 stream error, then a timeout over HTTP/1.1).
- https://img.pcbx.com/erp/file/part/spec/LR6XWA%20B-Panasonic.pdf : OK. Mirror of Panasonic Industrial LR6XWA datasheet, Form AAInd PEC-2.2009, (c)2009 Panasonic Energy Corporation of America. Used (curves; no OCV).
- https://www.akkuman.de/shop/mediafiles/PDF/Panasonic/Batterien/4501.pdf : OK. Mirror of Panasonic Energy Europe LR20EPS (D) datasheet, April 2020. Used (no OCV; lightest load 2.2 ohm).
- https://media.elv.com/file/111947_ls14500_data.pdf : OK. Mirror of Saft LS14500 datasheet, Doc. No 31064-2-0408, April 2008. Used.
- https://www.peak-system.com/produktcd/Tools/PCAN-Diag%20FD/Documentation/Addendum%20Batteries/Panasonic_Cell%20Type%20BK-3MCC.pdf : OK. Panasonic BK-3MCC (eneloop AA) specification sheet, undated. Used.
- https://lygte-info.dk/review/batteries2012/Duracell%20Plus%20Power%20AA%20UK.html and .../Energizer%20Ultimate%20Lithium%20AA%20UK.html : read via WebFetch; no measured OCV in text (curves are images). Secondary; only "the unloaded voltage for lithium batteries is 1.8 volt" (general statement).
- https://powerstream.com/AA-tests.htm : read via WebFetch; lightest load 100 mA, no OCV in text. Dead end.
- Alkaline OCV temperature coefficient: a web-search summary of a student lab report (https://www.slideshare.net/RashidAlsuwaidi/exp3-battery) gave about -0.12 mV/K (1.5959 V at 27.5 C, 1.5978 V at 11.8 C). Page NOT opened; UNVERIFIED and not a manufacturer figure. No manufacturer document found that states OCV versus temperature for alkaline, LiFeS2 or NiMH.

## Sourced figures

### Alkaline AA (Energizer alkaline handbook, 2018)

Source: https://data.energizer.com/pdfs/alkaline_appman.pdf

- A1. Operating voltage window, per cell: "Most devices are designed to operate within a voltage range (for example from 1.6 volts to 0.9 volts per cell) to accommodate this sloping discharge characteristic." (p. 3)
- A2. OCV 1.6 V, in a worked example (not a specification): "Example: A 1 Amp drain is placed on a battery with a Ri of 0.1 Ohms. ... Open circuit voltage = 1.6 Volts ... 1.6 Volts - 0.1 Volts = 1.5 Volts (expected closed circuit voltage)" (p. 9)
- A3. Light-load voltage, fresh, in the dual-pulse example: "if a 5 mA stabilization load is used in combination with a 505 mA pulse ... If the voltage changes from 1.485 to 1.378 ..." (p. 7). That is 1.485 V per cell under 5 mA. Fig. 9's y-axis runs 1.35-1.55 V. Whether the example cell is fresh is not stated in the sentence, but the next paragraph gives "typical effective resistance of fresh Energizer alkaline cylindrical batteries" as "approximately 150 to 300 milliohms" by the same method.
- A4. Fresh CCV under about 10 ohm (about 150 mA): "In the case of a single cylindrical 1.5 volt alkaline battery, the load would be approximately 10 ohms. A fresh (unused) battery will typically test at about 1.5 volts CCV. A battery that tests at 1.1 volts CCV has approximately 20% service remaining." (p. 13)
- A5. Temperature: "The recommended operating temperature range for alkaline batteries is -18 C to 55 C." and "The Alkaline-Manganese Dioxide cell can operate at temperatures as low as -20 C however this performance will be significantly lower (fig. 5)." (p. 4). Fig. 5 (250 mA, -20/0/20 C) y-axis 0.8-1.6 V. No OCV-versus-temperature figure in this handbook.

- A6. Early discharge at a light load, read by eye from Fig. 10 ("AA/LR6 Alkaline Battery, 50mA Discharge Ri Test (10mA / 500mA Pulse) at 21C", p. 9; rendered at 250 dpi from the PDF). These are graph readings, uncertain by about +/-0.02 V: start about 1.60 V at t = 0; about 1.46 V at 2 h; about 1.40 V at 5 h; about 1.36 V at 10 h; about 1.30 V at 20 h; end of curve about 0.85 V at about 54 h. Taking 54 h as full life, 5 % of capacity is about 2.7 h (about 1.45 V) and 10 % is about 5.4 h (about 1.40 V). The steepest fall is in the first hour or two: the first 0.15 V is gone by about 4 % of life.
- A7. Same handbook, p. 9, text under Fig. 10: "Cold temperatures ... will reduce ion mobility in the electrolyte. Subsequently, effective resistance will rise as ambient temperatures drops." Again resistance, not OCV.
- A8. Energizer E91 product datasheet (Form EBC-1102Q, mirror at https://courses.egr.uh.edu/ECE/ECE2100/Archive/Spring%202024%20Honors/E91.pdf): "Nominal Voltage: 1.5 volts", "Nominal IR: 150 to 300 milliohms (fresh)", "Operating Temp: -18 C to 55 C". No OCV. Page 2, "RADIO/CLOCK 43 ohm 4 hrs/day" (about 35 mA), read by eye: CCV starts at 1.50 V, about 1.45 V at 5 h, about 1.41 V at 10 h, 0.8 V at about 100 h. So about 1.45 V at 5 % and 1.41 V at 10 % of life. (Intermittent test, 4 h/day.)
- A9. Energizer L91 product datasheet (Form EBC-4201M, mirror at https://files.batteryjunction.com/frontend/files/L91.pdf), page 2, "Low Drain Performance 50mA Continuous (21 C)", gray "AA Alkaline" curve, read by eye: starts about 1.52 V, about 1.47 V at 2.5 h, about 1.40 V at 5 h, about 1.30 V at 15 h, 0.8 V at about 48 h. So about 1.47 V at 5 % and 1.40 V at 10 % of life.
- A10. Duracell MN1500 Coppertop datasheet (MN1500_US_CT, 6/08, mirror at https://www.ece.ucsb.edu/~ilan/Classes/ECE2A_F2010/Labs/Datasheets/Duracell%20AA%20MN1500%20LR6.pdf): "Nominal Voltage: 1.5 V", "Operating Voltage 1.6 - 0.75V", "Impedance: 120 m-ohm @ 1kHz", "Operating Temperature Range: -20 C to 54 C". No OCV. "Typical discharge characteristics at 21 C", 43 ohm curve, read by eye: starts at 1.50 V, about 1.42 V at 5 h, about 1.40 V at 8 h, about 1.37 V at 20 h, 0.8 V at about 112 h. So about 1.43 V at 5 % and 1.40 V at 10 % of life.
- A11. Duracell MN15CTUS0413 (mirror at https://www.ee.columbia.edu/sites/default/files/content/docs/Duracell%20AA%20battery.pdf), page 2, "Coppertop AA Constant Temperature at 100 mA": at t = 0 both 21 C and 0 C curves start near 1.58-1.60 V; the 0 C curve falls faster (about 1.30 V at 3 h versus about 1.36 V at 21 C). Read by eye; uncertain.
- A12. OCV acceptance limits for a fresh LR6, from two non-major-brand manufacturer specifications (secondary in brand, primary in kind):
  - Rapid Electronics LR6 specification (https://static.rapidonline.com/pdf/658023_da_en_01.pdf), section 10: "(Test environment: 20 +/-2, 60%+/-15% R.H) (Load resistance: 3.9ohms, Measure time: 0.3S) ... OCV (V) Initial >=1.59 ... After 12 months storage >=1.57"; CCV at 3.9 ohm "Initial >=1.45".
  - Adafruit-hosted LR6 specification (https://cdn-shop.adafruit.com/product-files/3349/AA_LR6_1.5V.pdf): "Initial 1.56<=OCV<=1.65", "After 12 months >=1.56", "OCV measurment: The inner resistance of Voltage Metre is above 1MOhm" (verbatim quotation; spelling is the source's).
  - The 1.65 V ceiling in the second sheet matches the upper bound a search summary attributed to the Panasonic handbook (unread; see log). An IEC 60086 maximum OCV for LR6 is UNVERIFIED (standard not consulted).
- A13. Panasonic LR6XWA datasheet (mirror above), page 2, "IEC/ANSI Standard Tests @ 20 C", "Radio (43ohm 4hpd)", read by eye from a 300 dpi render: CCV starts at 1.60 V, about 1.55 V at 5 h, about 1.49 V at 10 h, about 1.34 V at 20 h, 0.8 V at about 94 h. So about 1.55 V at 5 % and 1.49 V at 10 % of life. This curve is visibly smoothed (a drawn line, not raw data) and starts 0.10 V above the Energizer and Duracell 43 ohm curves (A8, A10); treat its early points as less reliable. Page 2 also has "Typical Temperature Characteristics 0.9 Volts Cutoff Voltage" (service hours versus load at 45, 20, 0, -10 C); no voltage-versus-temperature.

### Alkaline D

- D1. Energizer E95 datasheet (Form E95NA0323, mirror at https://files.batteryjunction.com/frontend/files/energizer/datasheet/ENERGIZER-E95-UpdatedDataSheet.pdf): "Nominal Voltage: 1.5 volts", "Nominal IR: 150 to 300 milliohms (fresh)", "Operating Temp: -18 C to 55 C (0 F to 130 F)", "Shelf Life: 10 years at 21 C". No OCV. Capacity bars, continuous to 0.8 V at 21 C, read by eye: about 17,000 mAh at 25 mA, about 15,000 at 100 mA, about 12,500 at 250 mA, about 9,000 at 500 mA.
- D2. E95, "Radio 10 ohm 4 hrs/day" (about 140 mA; the lightest curve given), read by eye from a 300 dpi render: CCV starts at 1.50 V, about 1.43 V at 4 h, about 1.41 V at 6.6 h (5 % of about 132 h), about 1.37 V at 13 h (10 %), about 1.30 V at 30 h.
- D3. Duracell MN1300 Coppertop D datasheet (MN13CTUS0413, mirror at https://images.toolsid.com/duracell/items/pdf/mn1300b2-information.pdf): "Nominal voltage 1.5 V", "Impedance 136 m-ohm @ 1 kHz", "Operating temperature range -20 C to 54 C". No OCV. Page 2, "Coppertop D Constant Resistance", 10 ohm curve, read by eye: starts about 1.55 V, about 1.42 V at 6.5 h (5 % of about 131 h), about 1.37 V at 13 h (10 %), about 1.32 V at 25 h.
- D4. MN1300, "Coppertop D Constant Temperature at 250 mA", read by eye: at t = 0, 21 C starts about 1.55 V and 0 C about 1.47 V; at 5 h, about 1.36 V (21 C) against about 1.28 V (0 C). This is the only D-cell temperature figure found, and it is closed-circuit at 250 mA, not OCV.
- D5. Panasonic LR20EPS (D) datasheet, April 2020 (mirror at https://www.akkuman.de/shop/mediafiles/PDF/Panasonic/Batterien/4501.pdf): "Nominal Voltage 1,5 Volt", "Operating temp. range -20 C (-4 F) ~ +55 C (131 F)", "Average Impedance +/- 100 m-Ohm @ 1kHz fresh", "IEC 60086-1, IEC 60086-2, IEC 60086-5". Curves only at 2.2 ohm and 600 mA (all start at about 1.49-1.50 V); no light-load curve and no OCV.
- D6. Light-load D curves (a few mA) were not found in any manufacturer document. D and AA share the same chemistry and the same OCV (chemistry sets OCV, not size); at a given current, a D cell sees about one-sixth of the AA's fractional drain (about 17,000 against about 2,800 mAh), so its early fall at a few mA is expected to be slower than the AA's at the same current. That last statement is inference, not a sourced figure.

### Lithium iron disulfide AA (Energizer lithium handbook, 2017)

Source: https://data.energizer.com/pdfs/lithiuml91l92_appman.pdf

- L1. Fresh OCV and spread: "the chemical reaction with lithium results in an open circuit voltage (OCV) of 1.8 volts." and "device designers should take into consideration that the OCV of fresh batteries can range from 1.79 to 1.83V." (p. 3)
- L2. OCV as a state-of-charge indicator: "A 'good' battery will generally have an OCV >1.74 volts. Any battery with an OCV <1.70 (after it has been allowed to recover) is completely discharged. Although an alkaline battery may read 'good' at 1.6 volts, this reading on a LiFeS2 battery indicates the product has been discharged." (p. 3). This is also a second Energizer statement placing a good alkaline cell at about 1.6 V OCV.
- L3. Temperature: "The recommended operating temperature range is -40 C to +60 C" and "LiFeS2 batteries can deliver approximately full rated capacity at -40 C if they are discharged at 25 mA." (p. 4). "Cold temperatures also lower the operating voltage" (p. 5, Fig. 3, 250 mA, -40 to 60 C, y-axis 0.8-2.0 V).
- L4. Two-step discharge visible at light loads: "Typically the two step discharge can be seen at low drain rates of approximately ten milliamps or less" (p. 4).
- L5. Lithium Fig. 3 (p. 5, 250 mA continuous), read by eye: at 21 C the curve runs flat at about 1.47-1.48 V for most of the 14 h life (after a brief start near 1.8 V at t = 0); at -40 C it starts about 1.33 V. A load of 250 mA is about ten times the Margay's range and is not the light-load figure.
- L6. Energizer L91 product datasheet (Form EBC-4201M, mirror above): "Nominal Voltage: 1.5 Volts", "Typical IR: 90 to 150 milliohms*", "Recommended Lithium Operating/Storage Temperature: -40 C to 60 C". No OCV. Page 2, 50 mA continuous at 21 C, read by eye from a 300 dpi render: a brief start near 1.58 V at t = 0, about 1.53 V by 0.5 h, about 1.52 V at 3 h (5 % of about 62 h), about 1.51 V at 6 h (10 %), about 1.48 V at 30 h, about 1.40 V at 52 h, then a cliff at about 62 h. The 43 ohm "RADIO" curve (about 35 mA) sits near 1.48-1.50 V at its start.


### NiMH AA (brief)

- N1. Panasonic BK-3MCC (eneloop) specification (mirror at https://www.peak-system.com/produktcd/Tools/PCAN-Diag%20FD/Documentation/Addendum%20Batteries/Panasonic_Cell%20Type%20BK-3MCC.pdf): "Nominal Voltage 1.2V", "Internal Impedance Approx. 25m Ohm (at 1000Hz)", "Discharge Condition 0 C - 50 C". No OCV. Discharge figure ("Charge: 2000mA (-dV=10mV), Rest: 1h, Discharge: 400,1000,2000,4000,6000mA, Ambient Temp.: 25 C"), 400 mA curve, read by eye: starts about 1.42 V, plateau about 1.25-1.27 V from about 10 % to 80 % of capacity. No curve lighter than 400 mA.

### Lithium thionyl chloride AA-size (brief; must not go into this logger)

- S1. Saft LS14500 datasheet (Doc. No 31064-2-0408, April 2008; mirror at https://media.elv.com/file/111947_ls14500_data.pdf): "Open circuit voltage (at + 20 C) 3.67 V", "Nominal voltage (at 0.2 mA + 20 C) 3.6 V". Three in series is about 11 V, twice the board's 5.5 V maximum.

## Three-cell pack against USB (4.75, 5.00, 5.25 V)

Pack = 3 x per-cell figure, computed with python from the per-cell values above. Margins are pack minus USB; positive means the pack is higher. Per-cell curve readings are by eye and uncertain by about +/-0.02 V per cell (+/-0.06 V per pack). Loaded figures are at the currents stated, which are heavier than a Margay's average draw.

| Case (source items) | V per cell | Pack (V) | vs 4.75 | vs 5.00 | vs 5.25 |
|---|---|---|---|---|---|
| Alkaline OCV, spec limits, fresh (A12) | 1.56-1.65 | 4.68-4.95 | -0.07 to +0.20 | -0.32 to -0.05 | -0.57 to -0.30 |
| Alkaline OCV, typical fresh (A2, L2, A10) | 1.60 | 4.80 | +0.05 | -0.20 | -0.45 |
| Alkaline AA under 5 mA, fresh (A3) | 1.485 | 4.46 | -0.29 | -0.54 | -0.79 |
| Alkaline AA at 35-50 mA, start (A8, A9, A10, A13) | 1.50-1.60 | 4.50-4.80 | -0.25 to +0.05 | -0.50 to -0.20 | -0.75 to -0.45 |
| Alkaline AA at 35-50 mA, 5 % used (A6, A8, A9, A10; A13 high) | 1.43-1.55 | 4.29-4.65 | -0.46 to -0.10 | -0.71 to -0.35 | -0.96 to -0.60 |
| Alkaline AA at 35-50 mA, 10 % used (same) | 1.40-1.49 | 4.20-4.47 | -0.55 to -0.28 | -0.80 to -0.53 | -1.05 to -0.78 |
| Alkaline D OCV (same chemistry as AA; no D-specific OCV found) | 1.56-1.65 | 4.68-4.95 | -0.07 to +0.20 | -0.32 to -0.05 | -0.57 to -0.30 |
| Alkaline D at 10 ohm (about 140 mA), start (D2, D3) | 1.50-1.55 | 4.50-4.65 | -0.25 to -0.10 | -0.50 to -0.35 | -0.75 to -0.60 |
| Alkaline D at 10 ohm, 5-10 % used (D2, D3) | 1.37-1.42 | 4.11-4.26 | -0.64 to -0.49 | -0.89 to -0.74 | -1.14 to -0.99 |
| LiFeS2 OCV, fresh (L1) | 1.79-1.83 | 5.37-5.49 | +0.62 to +0.74 | +0.37 to +0.49 | +0.12 to +0.24 |
| LiFeS2 at 50 mA, early (L6) | 1.53 | 4.59 | -0.16 | -0.41 | -0.66 |
| LiFeS2 at 50 mA, 5-10 % used (L6) | 1.51-1.52 | 4.53-4.56 | -0.22 to -0.19 | -0.47 to -0.44 | -0.72 to -0.69 |
| NiMH at 400 mA, start (N1) | 1.42 | 4.26 | -0.49 | -0.74 | -0.99 |
| NiMH plateau at 400 mA (N1) | 1.25-1.27 | 3.75-3.81 | -1.00 to -0.94 | -1.25 to -1.19 | -1.50 to -1.44 |
| LiSOCl2 OCV (S1) | 3.67 | 11.01 | +6.26 | +6.01 | +5.76 |

Measured facts from the table (interpretation left to the owner):

1. A fresh alkaline pack at open circuit (4.68-4.95 V) overlaps the bottom of the USB band (4.75 V) and never reaches 5.00 V.
2. Under any load in these documents, from 5 mA upward, a fresh alkaline pack sits at or below 4.80 V, and below 4.75 V in every Energizer and Duracell curve; by 5-10 % of capacity it is 4.20-4.65 V.
3. A fresh LiFeS2 pack at open circuit (5.37-5.49 V) is above the USB maximum of 5.25 V and within 0.01-0.13 V of the board's 5.5 V limit. Under 50 mA it falls to about 4.6 V.
4. A LiSOCl2 pack is about 11 V and exceeds the board's limit by a factor of two.

## Temperature (all chemistries)

- No manufacturer document consulted states OCV versus temperature. The figures found are closed-circuit: alkaline AA at 250 mA (A5, Fig. 5, -20/0/20 C), alkaline D at 250 mA (D4: start about 1.55 V at 21 C, about 1.47 V at 0 C), LiFeS2 AA at 250 mA (L5: about 1.47 V at 21 C, about 1.33 V at -40 C).
- Rated operating ranges: alkaline AA and D, -18 C to 55 C (Energizer, A5, A8, D1) or -20 C to 54-55 C (Duracell, Panasonic); LiFeS2, -40 C to 60 C (L3); eneloop discharge 0-50 C (N1). Alkaline is not rated to -40 C by any of the three makers.
- Alkaline OCV temperature coefficient of about -0.12 mV/K is UNVERIFIED (student lab report, page not opened). If correct, -40 C would raise alkaline OCV by about 8 mV per cell relative to 25 C, which is negligible beside the loaded-voltage drop.

## Does "about 1.7 V per fresh alkaline cell" hold?

No. Every alkaline source places fresh OCV at about 1.6 V: Energizer's handbook example ("Open circuit voltage = 1.6 Volts", A2) and lithium handbook ("an alkaline battery may read 'good' at 1.6 volts", L2), Duracell's "Operating Voltage 1.6 - 0.75V" (A10), and two maker specifications with limits of >=1.59 V and 1.56-1.65 V (A12). No alkaline source reaches 1.7 V; the highest stated ceiling is 1.65 V. The 1.7-1.8 V range is lithium iron disulfide (1.79-1.83 V fresh, L1). The earlier figure of about 1.6 V per cell (4.8 V per pack) is supported, at open circuit only.

# Margay cold sweep: passives (C1–C20, R1–R32)

Status: COMPLETE

Agent report, 2026-11-11. Input: `2026-11-11-margay-bom-export.csv` (KiCad schematic export, 11 lines read: 5 C lines, 6 R lines). Rule checked: every field-board part rated to −40 °C, AEC-Q200 grade where Digi-Key has one, no obsolete parts. Configuration resistors stay 0603 or larger; no part is proposed smaller.

## Results table

Verdicts apply the rule as written, clause by clause. PASS: rated to −40 °C or colder, AEC-Q200, active. FAIL: one clause is not met. No line fails the −40 °C clause and no line is obsolete; every FAIL below is the AEC-Q200 clause (Digi-Key carries an AEC-Q200 part in the same size and value, and the BoM's primary is not it). CHECK: could not be settled from sources. "ALT" rows are the ALT_MF/ALT_MPN/ALT_DIGIKEY second sources in the export. Stock and price are Digi-Key, read 2026-11-11 through WebFetch of the keyword-search page; the "at 100" price is cut tape.

| Ref | MPN | Maker | Dielectric/type | Op. temp | AEC-Q200? | Lifecycle | DK stock | Field issues | Verdict | Source URL |
|---|---|---|---|---|---|---|---|---|---|---|
| C1, C4, C5, C9, C11, C12, C16–C19 (0.1 µF, x10) | GCM155R71C104KA55D | Murata | MLCC X7R (−55 to +125 °C), 16 V | −55 to +125 °C | Yes (GCM is Murata's automotive line; DK lists AEC-Q200) | Active | 5,182,724; $0.01960 at 100 | None: MF Murata correct; 490-4759-1-ND maps to this MPN; 0.1 µF matches "104"; GCM15 = 0402 matches C0402 | PASS | https://www.digikey.com/en/products/result?keywords=490-4759-1-ND |
| C2, C3, C7, C8 (12 pF, x4) | CGA2B2C0G1H120J050BA | TDK | MLCC C0G/NP0 (EIA C0G: 0 ±30 ppm/K, so about 0.2 % change at −40 °C), 50 V | −55 to +125 °C | Yes (CGA is TDK's automotive line; DK lists AEC-Q200) | Active | 134,830; $0.03120 at 100 | None: MF TDK correct; 445-5585-1-ND maps to this MPN; 12 pF matches "120"; CGA2 = 0402 (1005) matches C0402 | PASS | https://www.digikey.com/en/products/result?keywords=445-5585-1-ND |
| C6, C15 (10 µF, x2) | GRM21BR61C106KE15K | Murata | MLCC X5R (−55 to +85 °C), 16 V | −55 to +85 °C (Murata datasheet, "In Production", last updated 9/8/2026) | No (GRM is the consumer/industrial line); an automotive 0805 10 µF exists, see options section | Active, in production | 0 in stock (695 due 28-Dec-2026, 9,305 due 19-Feb-2027); $0.04140 at 100 | None: MF Murata correct; 490-6473-1-ND maps to this MPN; 10 µF matches "106"; GRM21 = 0805 matches C0805 | FAIL (AEC-Q200 clause only; meets −40 °C; also zero DK stock today) | https://www.digikey.com/en/products/result?keywords=490-6473-1-ND ; Murata data sheet copy https://extranet.mandieselturbo.com/electronics/datasheets/muRata/GRMxx%20Series/GRM21BR61C106KE15.pdf |
| C10 (1 µF, x1) | CL05A105KA5NQNC | Samsung Electro-Mechanics | MLCC X5R (−55 to +85 °C), 25 V | −55 to +85 °C (Samsung page: "X5R(-55 ~ +85)", status "Mass Production") | No (general-standard line); AEC-Q200 0402 1 µF options exist, see options section | Active; maker "Mass Production" | 1,961,997; $0.06750 at 100 | None: MF Samsung correct; 1276-1445-1-ND maps to this MPN; 1 µF matches "105"; CL05 = 0402 matches C0402 | FAIL (AEC-Q200 clause only; meets −40 °C) | https://www.digikey.com/en/products/result?keywords=1276-1445-1-ND ; https://product.samsungsem.com/mlcc/CL05A105KA5NQN.do |
| C13, C14, C20 (1 µF, x3) | TMK107B7105KA-T | Taiyo Yuden | MLCC X7R (−55 to +125 °C), 25 V | −55 to +125 °C (Taiyo Yuden TY-COMPAS) | No (successor part is the "General Purpose" category); Murata GCM188R71E105KA64D is an automotive drop-in, see options section | Maker has RENAMED it: TY-COMPAS says "TMK107B7105KA-T is renamed" to MSAST168SB7105KTNA01 (General Purpose, "Mass Production (Preferred)") or MLAST168SB7105KTNA01 (Medical, "Mass Production (Previous Category)"). DK still lists the old MPN as Active | Old MPN: 0 (4,000 due 16-Nov-2026), $0.03010 at 100. New MPN MSAST168SB7105KTNA01: 9 in stock, 587-MSAST168SB7105KTNA01CT-ND, $0.03920 at 100 | MF Taiyo Yuden correct; 587-2984-1-ND maps to this MPN; 1 µF matches "105"; TMK107 = 0603 matches C0603. Issue: MPN superseded by a renamed part number | FAIL (AEC-Q200 clause; meets −40 °C; MPN renamed by maker; near-zero DK stock on old and new numbers) | https://ds.yuden.co.jp/TYCOMPAS/ut/detail?pn=TMK107B7105KA-T&u=M ; https://www.digikey.com/en/products/result?keywords=587-2984-1-ND ; https://www.digikey.com/en/products/result?keywords=MSAST168SB7105KTNA01 |
| R1, R2, R14–R21 (10k, x10) | RC0402FR-0710KL | Yageo | Thick film, 1 %, ±100 ppm/K, 1/16 W | −55 to +155 °C (Yageo RC_L spec, Table 2; DK) | No (RC_L is general purpose; DK lists no AEC-Q200) | Active | 6,509,272; $0.01080 at 100 | None: 311-10.0KLRCT-ND maps to this MPN; "10K" matches 10k; RC0402 = 0402 matches R0402 | FAIL (AEC-Q200 clause only; the listed ALT is AEC-Q200) | https://www.digikey.com/en/products/result?keywords=RC0402FR-0710KL ; https://www.digikey.co.uk/en/resources/datasheets/yageo/rc-series-l-suffix-datasheet |
| R1, R2, R14–R21 ALT | ERJ-2RKF1002X | Panasonic | Thick film, 1 %, ±100 ppm/K, 1/10 W | −55 to +155 °C (Panasonic datasheet, 29-May-25) | Yes, AEC-Q200 Grade 0 (Panasonic datasheet; DK "Automotive AEC-Q200") | Active; ERJ2RK is not marked NRFND (NRFND applies to ERJ8EN and larger) | 772,011; $0.01550 at 100 | None: P10.0KLCT-ND maps to this MPN; "1002" = 10k; ERJ-2 = 0402 matches R0402 | PASS | https://www.digikey.com/en/products/result?keywords=ERJ-2RKF1002X ; https://industrial.panasonic.com/cdbs/www-data/pdf/RDA0000/AOA0000C304.pdf |
| R3, R4 (27, x2) | RC0402FR-0727RL | Yageo | Thick film, 1 %, ±100 ppm/K, 1/16 W | −55 to +155 °C | No | Active | 459,607; $0.01080 at 100 | None: YAG3086CT-ND maps to this MPN (DK lists YAG3086TR/CT/DKR for it); "27R" matches 27; 0402 matches R0402 | FAIL (AEC-Q200 clause only; ALT is AEC-Q200) | https://www.digikey.com/en/products/result?keywords=YAG3086CT-ND |
| R3, R4 ALT | ERJ-2RKF27R0X | Panasonic | Thick film, 1 %, ±100 ppm/K, 1/10 W | −55 to +155 °C | Yes, Grade 0 | Active | 371,675 (DK buy box; DK substitutes table shows 531,675); $0.01640 at 100 | None: P27.0LCT-ND maps to this MPN; "27R0" = 27; 0402 | PASS | https://www.digikey.com/en/products/result?keywords=ERJ-2RKF27R0X ; https://industrial.panasonic.com/cdbs/www-data/pdf/RDA0000/AOA0000C304.pdf |
| R5–R9, R11–R13 (330, x8) | RC0402FR-07330RL | Yageo | Thick film, 1 %, ±100 ppm/K, 1/16 W | −55 to +155 °C | No | Active | 2,769,037; $0.01080 at 100 | None: 311-330LRCT-ND maps to this MPN; "330R" matches 330; 0402 matches R0402 | FAIL (AEC-Q200 clause only; ALT is AEC-Q200) | https://www.digikey.com/en/products/result?keywords=RC0402FR-07330RL |
| R5–R9, R11–R13 ALT | ERJ-2RKF3300X | Panasonic | Thick film, 1 %, ±100 ppm/K, 1/10 W | −55 to +155 °C | Yes, Grade 0 | Active | 326,441; $0.01550 at 100 | None: P330LCT-ND maps to this MPN; "3300" = 330; 0402 | PASS | https://www.digikey.com/en/products/result?keywords=ERJ-2RKF3300X ; https://industrial.panasonic.com/cdbs/www-data/pdf/RDA0000/AOA0000C304.pdf |
| R10 (130k, x1; U3 DELAY, configuration resistor, stays 0603) | ERJ-3EKF1303V | Panasonic | Thick film, 1 %, ±100 ppm/K, 1/10 W | −55 to +155 °C | Yes, Grade 0 | Active; ERJ3EK not NRFND | 49,857; $0.01950 at 100 | None: P130KHCT-ND maps to this MPN; "1303" = 130k; ERJ-3 = 0603 matches R0603 | PASS | https://www.digikey.com/en/products/result?keywords=ERJ-3EKF1303V ; https://industrial.panasonic.com/cdbs/www-data/pdf/RDA0000/AOA0000C304.pdf |
| R10 ALT | RMCF0603FT130K | Stackpole | Thick film, 1 %, ±100 ppm/K, 1/10 W | −55 to +155 °C (DK; Stackpole PDF returned 403, UNVERIFIED at maker) | Yes (DK "Automotive AEC-Q200") | Active | 79,761; $0.00960 at 100 | None: RMCF0603FT130KCT-ND maps to this MPN; 130K; 0603 matches R0603 | PASS | https://www.digikey.com/en/products/result?keywords=RMCF0603FT130K |
| R22–R24 (10k 0.1 %, x3; BAT_SENSE divider and AX) | CRT0603-BY-1002ELF | Bourns | Thin film, 0.1 %, ±25 ppm/K, 1/10 W | −55 to +155 °C (Bourns CRT datasheet) | No (Bourns CRT datasheet lists no AEC-Q200; DK lists none) | Active | 66,734; $0.06440 at 100 | None: CRT0603-BY-1002ELFCT-ND maps to this MPN; "1002" = 10k, B = ±0.1 %, Y = ±25 ppm; CRT0603 = 0603 matches R0603 | FAIL (AEC-Q200 clause only; ALT is AEC-Q200 with the same tolerance and TCR) | https://www.bourns.com/docs/Product-Datasheets/CRT.pdf ; https://www.digikey.com/en/products/result?keywords=CRT0603-BY-1002ELF |
| R22–R24 ALT | RG1608P-103-B-T5 | Susumu | Thin film, 0.1 %, ±25 ppm/K, 1/10 W, anti-sulfur | −55 to +155 °C (DK; Susumu RG datasheet not retrieved, UNVERIFIED at maker) | Yes (DK "Anti-Sulfur, Automotive AEC-Q200") | Active | 551,979; $0.06390 at 100 | None: RG16P10.0KBCT-ND maps to this MPN; "103" = 10k, B = 0.1 %; RG1608 = 0603 matches R0603 | PASS | https://www.digikey.com/en/products/detail/susumu/RG1608P-103-B-T5/1240450 |
| R31, R32 (5.1k, x2; USB CC1/CC2 pull-downs) | RC0402FR-075K1L | Yageo | Thick film, 1 %, ±100 ppm/K, 1/16 W | −55 to +155 °C | No | Active | 417,255; $0.01080 at 100 | None: 311-5.10KLRCT-ND maps to this MPN; "5K1" matches 5.1K; 0402 matches R0402 | FAIL (AEC-Q200 clause only; ALT is AEC-Q200) | https://www.digikey.com/en/products/result?keywords=RC0402FR-075K1L |
| R31, R32 ALT | ERJ-2RKF5101X | Panasonic | Thick film, 1 %, ±100 ppm/K, 1/10 W | −55 to +155 °C | Yes, Grade 0 | Active | 810,122; $0.01640 at 100 | None: P5.10KLCT-ND maps to this MPN; "5101" = 5.1k; 0402 | PASS | https://www.digikey.com/en/products/result?keywords=ERJ-2RKF5101X ; https://industrial.panasonic.com/cdbs/www-data/pdf/RDA0000/AOA0000C304.pdf |

## Capacitance at −40 °C and DC bias

Applied DC bias per capacitor, from the KiCad netlist (`kicad-cli sch export netlist` on `Project-Margay/Hardware/KiCAD/Margay.kicad_sch`, read 2026-11-11) and the input range in `Project-Margay/README.md` ("3.5–5.5 V for regulated operation, 6.0 V absolute maximum; three alkaline AA or D cells"):

| Ref | Net | Bias used below |
|---|---|---|
| C6 | VUSB | 5.0 V |
| C15 | 3V3_AUX | 3.3 V |
| C10 | /Power_Sensors/VBAT_SW | 4.8 V (three fresh alkaline cells, 1.6 V each, UNVERIFIED nominal) and 5.5 V (top of regulated range) |
| C13 | /Power_Sensors/VMAIN | 5.0–5.5 V (VMAIN voltage UNVERIFIED; assumed to follow the battery or USB input) |
| C14 | 3V3 | 3.3 V |
| C20 | Net-(BT1-+) (coin cell) | 3.0 V |

Each number below is read from the maker's own characteristic data, at room temperature for the DC-bias curve and at 0 V DC for the temperature curve. The maker publishes no combined (−40 °C and DC bias) curve for these parts; adding the two percentages is an approximation, marked as such.

**C6, C15: Murata GRM21BR61C106KE15 (10 µF X5R 16 V 0805).** Source: Murata "Product Search Data Sheet", last updated 9/8/2026, copy at https://extranet.mandieselturbo.com/electronics/datasheets/muRata/GRMxx%20Series/GRM21BR61C106KE15.pdf (Murata's own pim.murata.com page is JavaScript-only and would not fetch). The curves are vector graphics; the values were digitized from the PDF path coordinates against the plot gridlines (`pdftocairo -svg`, then linear interpolation), not read by eye.
- C–Temp. (DC 0 V, AC 0.5 Vrms): −3.5 % at −40 °C; −7.1 % at −55 °C.
- C–DC bias (25 °C, AC 0.5 Vrms): −34.7 % at 3.3 V (C15); −52.4 % at 5.0 V (C6); −56.4 % at 5.5 V.
- Effective at −40 °C, approximate sum: C15 about 6.2 µF; C6 about 4.4 µF of the nominal 10 µF. The DC bias, not the cold, is the dominant loss.

**C10: Samsung CL05A105KA5NQN (1 µF X5R 25 V 0402).** Source: the characteristic data embedded in https://product.samsungsem.com/mlcc/CL05A105KA5NQN.do (JSON `datasheetData`, parsed and interpolated).
- TCC (0 V DC, 1 kHz): −1.8 % at −40 °C; −2.4 % at −55 °C.
- DC bias (25 °C, 1 kHz): −27.1 % at 3.3 V; −43.0 % at 4.8 V; −44.8 % at 5.0 V.
- Effective at −40 °C and 4.8 V, approximate sum: about 0.55 µF of the nominal 1 µF.

**C13, C14, C20: Taiyo Yuden TMK107B7105KA-T, now MSAST168SB7105KTNA01 (1 µF X7R 25 V 0603).** Source: TY-COMPAS characteristic data, `detailGraphRest` endpoint behind https://ds.yuden.co.jp/TYCOMPAS/ut/detail?pn=MSAST168SB7105KTNA01&u=M (graph types CTCCP and CDCBA, 19 and 106 points).
- Temperature (AC 1 Vrms): −10.76 % at −45 °C and −8.84 % at −35 °C (tabulated points), about −9.8 % at −40 °C interpolated; −8.71 % at −55 °C.
- DC bias (25 °C): −7.4 % at 3.0 V (C20); −10.4 % at 3.3 V (C14); −27.8 % at 5.0 V and −32.5 % at 5.5 V (C13).
- Effective at −40 °C, approximate sum: C20 about 0.83 µF, C14 about 0.80 µF, C13 about 0.62 µF (5 V).

Interpretation (hypothesis, for Andy): at −40 °C and working bias, C6 falls below half its nominal value (about 4.4 µF of 10 µF) and C10 sits near half (about 0.55 µF of 1 µF); the others keep 60–83 %. In every case the DC bias, not the cold, takes most of it. Whether that matters depends on what each capacitor is for, which this sweep did not check.

## Automotive-grade options

Every option below is the same case size and value as the BoM line it replaces, and the same or higher voltage rating; no part is proposed smaller. Read on Digi-Key 2026-11-11.

| Replaces | Option | Maker | Dielectric/type | Op. temp | AEC-Q200 | DK cut-tape number | Price at 100 | DK stock | Note |
|---|---|---|---|---|---|---|---|---|---|
| C6, C15 (GRM21BR61C106KE15K) | GRT21BR61C106KE01L | Murata | X5R 16 V 0805 | −55 to +85 °C | Yes (DK) | 490-12379-1-ND | $0.29640 | 34,386 | Only in-stock automotive 10 µF 0805 found. Same dielectric; its DC-bias curve was not retrieved (UNVERIFIED that it matches the GRM's). About 7x the price. |
| C6, C15 | GRT21BC71C106KE13L | Murata | X7S 16 V 0805 | −55 to +125 °C | Yes (DK) | 490-GRT21BC71C106KE13LCT-ND | $0.14450 | 0 (3,000 due 24-Mar-2027) | |
| C6, C15 | CGA4J1X7S1C106K125AC | TDK | X7S 16 V 0805 | −55 to +125 °C | Yes (DK) | 445-16110-1-ND | $0.19290 | 0 (2,000 due 15-Feb-2027) | |
| C6, C15 | GCM21BC71C106KE36L/K | Murata | X7S 16 V 0805 | −55 to +125 °C | Yes (DK) | not shown on the DK page | not shown ($0.45 at 1) | 0 | |
| C6, C15 | CL21Y106KOQ4PNE | Samsung | X7S 16 V 0805 | −55 to +125 °C | Yes (DK) | 1276-CL21Y106KOQ4PNECT-ND | $0.22090 | not shown (61-week lead time) | |
| C10 (CL05A105KA5NQNC) | GRT155R61E105KE01D | Murata | X5R 25 V 0402 | −55 to +85 °C | Yes (DK) | 490-12263-1-ND | $0.04360 | UNVERIFIED (DK page showed no stock figure; 21-week lead time) | Same dielectric and voltage as the BoM part. |
| C10 | GRT155C81E105KE13D | Murata | X6S 25 V 0402 | −55 to +105 °C | listed under Ratings, value not shown (UNVERIFIED) | 490-18215-1-ND | $0.03010 | 0 | |
| C10 | GCM155C71A105KE38D | Murata | X7S 10 V 0402 | −55 to +125 °C | listed under Ratings, value not shown (GCM is Murata's automotive series) | 490-13409-1-ND | $0.03870 | 0 (10,000 due 05-Apr-2027) | 10 V rating: below the BoM part's 25 V; C10 sees up to 5.5 V (6.0 V absolute maximum). |
| C13, C14, C20 (TMK107B7105KA-T) | GCM188R71E105KA64D | Murata | X7R 25 V 0603 | −55 to +125 °C | GCM series is Murata's automotive line; DK lists AEC-Q200 under Ratings without a value (UNVERIFIED at maker) | 490-10673-1-ND | $0.07120 | 194,942 | Same dielectric, voltage and size as the BoM part. |
| R1, R2, R14–R21 | ERJ-2RKF1002X (already the ALT) | Panasonic | thick film 1 % 0402 | −55 to +155 °C | Grade 0 | P10.0KLCT-ND | $0.01550 | 772,011 | Promote ALT to primary. |
| R1, R2, R14–R21 | AC0402FR-0710KL | Yageo | thick film 1 % 0402 | −55 to +155 °C | Yes (DK) | YAG3436CT-ND | $0.01290 | 1,520,702 | Yageo's automotive twin of the RC part. |
| R3, R4 | ERJ-2RKF27R0X (ALT) | Panasonic | as above | −55 to +155 °C | Grade 0 | P27.0LCT-ND | $0.01640 | 371,675 | Promote ALT. |
| R3, R4 | AC0402FR-0727RL | Yageo | thick film 1 % 0402 | −55 to +155 °C | Yes (DK) | YAG5278CT-ND | $0.01290 | 5,399 | |
| R5–R9, R11–R13 | ERJ-2RKF3300X (ALT) | Panasonic | as above | −55 to +155 °C | Grade 0 | P330LCT-ND | $0.01550 | 326,441 | Promote ALT. |
| R5–R9, R11–R13 | AC0402FR-07330RL | Yageo | thick film 1 % 0402 | −55 to +155 °C | Yes (DK) | YAG3476CT-ND | $0.01370 | 2,134 | |
| R22–R24 | RG1608P-103-B-T5 (ALT) | Susumu | thin film 0.1 % ±25 ppm/K 0603 | −55 to +155 °C | Yes (DK) | RG16P10.0KBCT-ND | $0.06390 | 551,979 | Promote ALT; same tolerance and TCR as the Bourns part. |
| R22–R24 | ERA-3AEB103V | Panasonic | thin film 0.1 % ±25 ppm/K 0603 | −55 to +155 °C | Yes (DK) | P10KDBCT-ND | $0.06040 | 0 (55-week lead time) | Second automotive source, not stocked today. |
| R31, R32 | ERJ-2RKF5101X (ALT) | Panasonic | thick film 1 % 0402 | −55 to +155 °C | Grade 0 | P5.10KLCT-ND | $0.01640 | 810,122 | Promote ALT. |
| R31, R32 | AC0402FR-075K1L | Yageo | thick film 1 % 0402 | −55 to +155 °C | Yes (DK) | YAG3503CT-ND | $0.01290 | 0 (10,000 past due, est. 09-Nov-2026) | |

Observation: for every resistor line, the export's ALT is already an AEC-Q200 part in stock, so the fix is a swap of primary and ALT, not a new search. For C13/C14/C20, a Murata GCM drop-in is stocked. For C6/C15 the only stocked automotive 10 µF 0805 is the GRT X5R at about 7x the price; the X7S automotive parts are all out of stock until 2027.

## Sources log

Fetched 2026-11-11. "OK" = data used above; "dead end" = tried and failed.

- Digi-Key keyword-search pages (`https://www.digikey.com/en/products/result?keywords=<term>`, via WebFetch; curl gets HTTP 403): 490-6473-1-ND, 490-4759-1-ND, 445-5585-1-ND, 1276-1445-1-ND, 587-2984-1-ND, MSAST168SB7105KTNA01, CGA4J1X7S1C106K125AC, GCM21BC71C106KE36, GRT21BC71C106KE13L, CL21Y106KOQ4PNE, GRT21BR61E106KE13 (X5R 25 V, AEC-Q200 value not shown, stock not shown), GRT21BR61C106KE01, GCM155C71A105KE38D, GCM188R71E105KA64D, GRT155R61E105KE01D, GRT155C81E105KE13D, RC0402FR-0710KL, ERJ-2RKF1002X, RC0402FR-0727RL, ERJ-2RKF27R0X, RC0402FR-07330RL, ERJ-2RKF3300X, ERJ-3EKF1303V, RMCF0603FT130K, RMCF0603FT130KCT-ND, CRT0603-BY-1002ELF, RG16P10.0KBCT-ND, RC0402FR-075K1L, ERJ-2RKF5101X, 311-5.10KLRCT-ND, AC0402FR-0710KL, AC0402FR-07330RL, AC0402FR-0727RL, AC0402FR-075K1L, ERA-3AEB103V, YAG3086CT-ND, P27.0LCT-ND: OK.
- Digi-Key searches by Digi-Key number 311-10.0KLRCT-ND, P10.0KLCT-ND, P27.0LCT-ND: returned a listing card without stock; re-run by MPN, OK.
- Digi-Key dead ends: `products/detail/murata-electronics/GRM21BR61C106KE15K/2433666` (wrong product ID, returned a Vishay connector); CGA4J3X5R1C106K125AB, CGA2B3X5R1E105K050BB, CGA2B3X5R1C105K050BB, GCM155R61C105KE, GCM155D71E105KE36D (no results); free-text "10uF 0805 AEC-Q200 16V" (36 results, table not rendered); filter URL and `cross-reference?search=CL05A105KA5NQNC` (no table rendered).
- Digi-Key product detail https://www.digikey.com/en/products/detail/susumu/RG1608P-103-B-T5/1240450: OK.
- Murata: `murata.com/.../productdetail?partno=GCM155R71C104KA55%23` redirects to pim.murata.com, which is JavaScript-only (empty): dead end. `search.murata.co.jp/Ceramy/image/img/A01X/G101/ENG/<part>-01.pdf` (404), `psearch.en.murata.com/capacitor/product/<part>.pdf` (404), `murata.com/.../api/pdfdownloadapi` (HTML, not PDF): dead ends. Murata "Product Search Data Sheet" for GRM21BR61C106KE15#, last updated 9/8/2026, copy at https://extranet.mandieselturbo.com/electronics/datasheets/muRata/GRMxx%20Series/GRM21BR61C106KE15.pdf: OK (status, ratings, C–Temp. and C–DC-bias curves, digitized from vector paths).
- TDK: `product.tdk.com/en/search/capacitor/ceramic/mlcc/info?part_no=CGA2B2C0G1H120J050BA` and two PDF URL patterns: HTTP 403, dead end. CGA2B2C0G1H120J050BA data taken from DK and confirmed by search results (Arrow, Future Electronics, RS listings): OK at distributor level only.
- Samsung Electro-Mechanics: https://product.samsungsem.com/mlcc/CL05A105KA5NQN.do: OK (status "Mass Production", X5R −55 to +85, embedded TCC and DC-bias data).
- Taiyo Yuden TY-COMPAS: https://ds.yuden.co.jp/TYCOMPAS/ut/detail?pn=TMK107B7105KA-T&u=M (rename notice), detail pages for MSAST168SB7105KTNA01 and MLAST168SB7105KTNA01, and `ut/detailGraphRest` (POST, gtype CDCBA and CTCCP): OK. `ut/specSheet?pn=TMK107B7105KA-T`: 404, dead end.
- Panasonic: product pages https://industrial.panasonic.com/ww/products/pt/general-purpose-chip-resistors/models/ERJ2RKF1002X and .../ERJ3EKF1303V (no status label shown); datasheet https://industrial.panasonic.com/cdbs/www-data/pdf/RDA0000/AOA0000C304.pdf (dated 29-May-25; "AEC-Q200 compliant (except ERJ1R, ERJXG, ERJ1GN)"; ERJ2RK and ERJ3EK −55 to +155 °C, Grade 0; NRFND marked on ERJ8EN, ERJ14N, ERJ12N, ERJ12S, ERJ1TN only): OK. curl to industrial.panasonic.com failed to connect; WebFetch worked. A search-result summary claimed 2RK/3EK were NRFND; the datasheet table shows they are not.
- Yageo: RC_L product specification V.3 (21 Aug 2015) at https://www.digikey.co.uk/en/resources/datasheets/yageo/rc-series-l-suffix-datasheet, Table 2: RC0402 and RC0603 −55 to +155 °C, no AEC-Q200 statement found in the readable text: OK. yageo.com PDF URLs (PYu-RC_Group_51_RoHS_L_12, PYu-AC_51_RoHS_L_10/13, lowercase app/ paths): 404, dead ends. Mouser copy (PYu_RC_Group_51_RoHS_L_11): curl returned a JavaScript page, WebFetch timed out, dead end. Farnell 3727334.pdf is the RC_P series V.4 (May 2022), not RC_L: not used.
- Bourns: https://www.bourns.com/docs/Product-Datasheets/CRT.pdf: OK (−55 to +155 °C; features list has no AEC-Q200).
- Susumu: `susumu.co.jp/common/pdf/n_catalog_partition05_en.pdf` is not the RG series; Mouser copy of partition 26 returned JavaScript: dead ends. RG data from DK only.
- Stackpole: `seielect.com/catalog/sei-rmcf_rmcp.pdf` (both cases): HTTP 403, dead end. RMCF data from DK only.
- Applied bias: KiCad netlist from `kicad-cli sch export netlist` on `Project-Margay/Hardware/KiCAD/Margay.kicad_sch` (written to the scratchpad, not the repository); input range from `Project-Margay/README.md`.


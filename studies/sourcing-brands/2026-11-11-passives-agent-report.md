# Passive-component brands for Northern Widget: sourcing survey

Status: COMPLETE

Agent report, 2026-11-11. Scope: MLCCs, thick- and thin-film resistors, inductors and ferrite beads, tantalum and polymer capacitors, aluminum electrolytics, PPTCs. Criteria in order: (1) geopolitical resilience, (2) wide-temperature quality, (3) consistent quality, (4) workers' rights.

Evidence labels: **[maker]** = the manufacturer's own claim; **[indep]** = independent source (press, regulator, NGO, benchmark, test lab, engineer account); **UNVERIFIED** = not confirmed against a source in this session.

## 1. What the boards buy

Method: the Margay CSV was read with Python `csv.DictReader`; the Okapi Eagle partlist (`CAMOutputs/Assembly/Okapi.txt` from `Okapi_2024-11-02.zip`, via `unzip -p`) was parsed by the fixed-width column positions of its header line. A line counts as in-scope when its Description contains resistor, capacitor, inductor, PPTC or tantalum. "Lines" = BoM rows; "placements" = sum of Qty. Manufacturer spellings normalized: "Yaiyo Yuden" to Taiyo Yuden, "Vishay Sprague" to Vishay, "Wurth" to Würth, "AVX" to KYOCERA AVX, "Kemet" to KEMET.

Margay v3.0 (`Project-Margay/Production/Margay_BoM_3v0_-_2026-11-04.csv`):

| Manufacturer | Lines | Placements |
|---|---|---|
| Yageo | 7 | 25 |
| Murata | 3 | 15 |
| TDK | 1 | 2 |
| Taiyo Yuden | 1 | 2 |
| Bourns | 1 | 1 |
| Total | 13 | 45 |

Okapi (2024-11-02 partlist):

| Manufacturer | Lines | Placements |
|---|---|---|
| Yageo | 28 | 61 |
| Murata | 5 | 39 |
| Panasonic | 6 | 11 |
| TE Connectivity | 1 | 8 |
| Würth Elektronik | 5 | 5 |
| (blank MF, R0805 x4) | 1 | 4 |
| Samsung Electro-Mechanics | 2 | 3 |
| Bourns | 1 | 2 |
| Stackpole | 1 | 2 |
| TDK | 1 | 2 |
| Taiyo Yuden | 1 | 2 |
| Vishay | 1 | 1 |
| KYOCERA AVX | 1 | 1 |
| Rohm | 1 | 1 |
| KEMET | 1 | 1 |
| Total | 56 | 143 |

Out of scope but noted: Okapi also carries three Würth LED lines (8 placements), and Margay one Würth SD-card holder.

Dependence: **Yageo** (RC-series thick-film chip resistors) is the largest by both measures on both boards: 25 of 45 Margay passive placements and 61 of 143 Okapi. **Murata** MLCCs are second (15 and 39 placements), concentrated in two part numbers: `GCM155R71C104KA55D` (0.1 µF X7R 0402, Murata's automotive GCM line) and `GRM21BR61C106KE15K` (10 µF X5R 0805). Every other brand is one to six lines.

BoM observations made while counting (data-quality, not sourcing; verified by reading the rows above):
- The Okapi `10 µF`, `22 µF` and `4.7 µF` Murata parts are X5R (`GRM...R61...`), rated to +85 °C; low end −55 °C [maker part-number system, UNVERIFIED against datasheet in this session].
- Okapi rows whose package and MPN disagree: `330` in `R0402` with MPN `RC0603FR-07330RL` (8 placements); Samsung `CL10C120JB8NNNC` and `CL10B105MO8NNWC` (CL10 = 0603 size) on `C0402` footprints; `287R` rows carrying MPNs for 232 Ω and 453 Ω. These are Eagle attribute errors or intentional value overrides; not checked further.
- Okapi `PPTC1.5A` description says "Bel Fuse PPTC" but MF is Bourns (`MF-NSMF150-2`).

## 2. Brand findings

(One section per brand; facts appended as confirmed.)

### 2.0 Cross-brand: RBA membership (retrieved 2026-11-11)

Source: RBA member list, https://www.responsiblebusiness.org/about/members/ (fetched with curl 2026-11-11, text grepped). The page says: "The RBA has four membership categories: Full, Regular, Affiliate, and Supporter ... Full and Regular members are designated by an 'F' or 'R' following their company names." An unmarked name is therefore Affiliate or Supporter. **[indep]** (the RBA's own list; membership is a commitment, not an audit result).

| Listed name | Marker | Brand |
|---|---|---|
| Murata Manufacturing Co., Ltd. | R (Regular) | Murata |
| Vishay Intertechnology, Inc. | R (Regular) | Vishay |
| TDK Group | none (Affiliate or Supporter) | TDK |
| Panasonic Holdings Corporation | none | Panasonic |
| KYOCERA Corporation; KYOCERA AVX Components Corporation | none | KYOCERA AVX |
| Bourns, Inc. | none | Bourns |
| TE Connectivity | none | TE |
| Amphenol Corporation | none | (not passives) |

Not on the list: Taiyo Yuden, Samsung Electro-Mechanics (Samsung Electronics, Samsung SDI and Samsung Display are listed; Electro-Mechanics is not), KEMET, Yageo, Walsin, Würth Elektronik, Susumu, Stackpole, Coilcraft, Littelfuse, Rohm. Absence from this list is not evidence of poor practice; some of these publish their own code-of-conduct programs (checked per brand below).


### 2.0b Cross-brand: KnowTheChain ICT benchmark **[indep]**

KnowTheChain (Business & Human Rights Resource Centre) scores forced-labor practice in supply chains, 0–100. Only the largest ICT firms are covered; of the passives makers, only Murata, Kyocera, Panasonic and (2022 only) TE are benchmarked.

| Company | 2022 score (rank of 60) | 2025 score (rank of 45) |
|---|---|---|
| Murata Manufacturing | 13 (33rd) | 10 (34th) |
| Panasonic Holdings | 9 (45th) | 10 (34th) |
| Kyocera (parent of KYOCERA AVX) | 3 (55th) | 6 (41st) |
| TE Connectivity | 11 | not in 2025 sample |
| Samsung Electronics (not Electro-Mechanics) | 46 | 61 (top) |

Sources: 2022 report, https://www.business-humanrights.org/documents/38423/KTC_2022_ICT_Benchmark_Report.pdf, p. 5 "2022 ranking" (median 14/100; published January 2023); 2025 scorecards, https://media.bhrrc.org/media/documents/2025_KTC_ICT_Scorecard_Murata_Manufacturing.pdf, `..._Kyocera.pdf`, `..._Panasonic.pdf` (each p. 1, overall ranking and score); 2025 briefing (2 April 2025, 45 companies, average 20/100), https://www.business-humanrights.org/en/from-us/briefings/2025-knowthechain-ict-benchmark/. Murata's 2025 scorecard records "First-tier supplier list: No", "Risk assessment: No", "Remedy for supply chain workers: No", and a no-fee (Employer Pays) recruitment policy: Yes. Kyocera and Panasonic: First-tier supplier list: No; no-fee policy: Yes.

Interpretation (hypothesis): all three Japanese passives makers sit well below the ICT average on forced-labor due diligence. Samsung Electronics' high score does not transfer to Samsung Electro-Mechanics, which is a separate listed company.

### Yageo (and KEMET, Yageo group)

BoM dependence: largest passive supplier on both boards (Margay 7 lines/25 placements; Okapi 28/61), all `RC0402`/`RC0603` thick-film chip resistors. KEMET: one Okapi line (`C0805C475K4RACTU`, 4.7 µF X7R 0805).

Criterion 1, geography and ownership:
- Yageo is a Taiwan-listed company (TWSE 2327); its 2024 annual report (printed 2 May 2025) lists the Yageo-brand GHG inventory sites as "Yageo Taipei Headquarters, Kaohsiung Dashe Plant, Kaohsiung Nanzi Plant, and Kaohsiung Dafa Plant", plus China plants. https://yageogroup.com/content/Resource%20Library/Financial/yageo_2025-annual-report_25052810_107.pdf (section 9, GHG inventory, text line ~1915). **[maker]**
- The Yageo ESG 2023 report scopes its emissions to "the Taiwan factory, the two factories in Suzhou, China (SZ-R, SZ-C) and the Dongguan factory (DG Backend + TH DG)". https://www.yageogroup.com/content/Resource%20Library/Compliance%20Report/YAGEO_ESG2023_en.pdf (GHG table, Note 1). **[maker]** Interpretation (hypothesis): Yageo-brand chip resistors come from Taiwan and southern/eastern China; whether a given RC-series reel is Taiwan- or China-made is not published per part number, and would need a Digi-Key country-of-origin field or a Yageo query. UNVERIFIED per part.
- Yageo acquired KEMET (US) in June 2020 (https://iconnect007.com/index.php/article/123280/kemet-and-yageo-complete-merger/123283?skin=ein **[indep press]**). KEMET's own former site states "22 manufacturing plants located across North America, Europe, and Asia"; secondary sources place tantalum and polymer production in Matamoros and Ciudad Victoria, Mexico, and plants in Pontecchio/Sasso Marconi (Italy), Suzhou and Anting (China), Portugal and others (search summary 2026-11-11 of kemet.com and trade press; individual plants UNVERIFIED).
- Ownership event: Yageo's unsolicited bid for Shibaura Electronics (Japan, thermistors), launched February 2025, required a security review under Japan's Foreign Exchange and Foreign Trade Act. METI cleared it with undisclosed conditions on 2 September 2025, and the tender offer closed 20 October 2025 with 88.32 % of voting rights. Sources: https://www.digitimes.com/news/a20250903PD217.html; https://media.dealstreetasia.com/stories/yageo-completes-tender-offer-shibaura-460473; https://filingreader.com/news-wire/tokyo/2025-10-21/yageo-completes-shibaura-electronics-tender-offer-secures-majority **[indep press, read via search summary]**. The annual report confirms the 5 February 2025 bid (text line ~3862). Relevance: Japan treated a Taiwanese acquirer of a component maker as a national-security matter; this is evidence of the regulatory climate, not of a supply risk to Yageo parts.
- Yageo's annual report notes only that "in 2025 Tariffs on international trade will be closely monitored" (section 5.6.4). **[maker]**
- Second sources: `RC0402FR-07xxxxL` 1 % thick-film resistors are commodity parts. Drop-in equivalents in the same 0402/0603 1 % 100 ppm/K class exist from Panasonic (ERJ-2RKF/ERJ-3EKF), Vishay (CRCW), Stackpole (RMCF), KOA (RK73H), Walsin (WR), Bourns (CR) and Samsung (RC1005F) [standard industry knowledge; not checked line by line on Digi-Key in this session, UNVERIFIED].

Criterion 2, temperature:
- RC_L series (the part family on both BoMs): operating range −55 °C to +155 °C for RC0402–RC2512, per Yageo product specification V.3 (Aug. 2015) hosted at https://www.digikey.co.uk/en/resources/datasheets/yageo/rc-series-l-suffix-datasheet **[maker; read via search snippet, PDF not opened]**; TCR ±100 ppm/K for 10 kΩ 1 % (distributor listings, e.g. https://www.futureelectronics.com/p/passives--resistors--fixed-resistors/rc0402fr-0710kl-yageo-3388022). −40 °C is well inside the rating. Yageo's AEC-Q200 automotive equivalent is the AC series (UNVERIFIED in this session).

Criterion 3, consistency:
- ESG 2023 report: "All YAGEO factories are certified to relevant ISO standards, including ISO 9001, ISO 14001, and ISO 45001. Additionally, some factories that produce automotive products have achieved IATF 16949 certification." (text line ~3436) **[maker]**
- No independent report of a Yageo resistor quality escape or recall was found in this session (searches below). Evidence is thin either way.

Criterion 4, workers:
- Yageo is not an RBA member (section 2.0). ESG 2023: "All factories are required to complete the Responsible Business Alliance (RBA) self-assessment questionnaire" and Yageo "conducts RBA audits for suppliers" (text lines ~247, ~2879). **[maker]** Self-assessment is not third-party validated audit. Yageo and KEMET are not in the KnowTheChain samples.

### Murata

BoM dependence: second-largest on both boards (Margay 3 lines/15 placements; Okapi 5/39). Parts: `GCM155R71C104KA55D` (0.1 µF X7R, automotive GCM), `GCM1555C1H180JA16D` (18 pF C0G, GCM), `GRM21BR61C106KE15K` (10 µF X5R), `GRM219R61C226ME15L` (22 µF X5R), `GRM188R61C475KAAJD` (4.7 µF X5R), `GRT155R61E224KE01D` (0.22 µF X5R, GRT = AEC-Q200 "for infotainment" line, UNVERIFIED decoding).

Criterion 1, geography and ownership:
- Japan-listed (TSE 6981), no ownership event found 2022–2026. MLCC production in Japan at Fukui Murata and Izumo Murata, with Okayama Murata (Setouchi) to become the third Japanese MLCC site; overseas at Murata Electronics (Thailand), the Philippines, and Wuxi, China. Okayama MLCC building scheduled for construction April 2027 to end 2028; ¥1 trillion MLCC investment FY2026–FY2030. Source: Evertiq, 30 October 2026, https://evertiq.com/design/2026-10-30-murata-to-invest-57-billion-to-double-mlcc-sales **[indep press reporting Murata's announcement]**. Wuxi production site completed 2024, Thailand 2023, Philippines building October 2025, Izumo building April 2026 (search summary of https://evertiq.com/design/2026-04-07-murata-completes-new-mlcc-production-building-in-japan and https://autotechinsight.spglobal.com/news/5285235/ **[indep press]**).
- A TrendForce estimate (via Evertiq, date not confirmed, probably about 2022) put Murata MLCC capacity at 56 % Japan, 36 % China, 3 % Singapore, 5 % Philippines. UNVERIFIED date; treat as a rough baseline only.
- Interpretation (hypothesis): Murata has the largest Japan-resident MLCC capacity of any maker, plus Southeast Asian plants outside China; this is the strongest geographic spread among MLCC makers surveyed. Per-part country of origin is not published.
- Second sources: `GCM155R71C104KA55D` (0402 X7R 16 V AEC-Q200) has direct equivalents from TDK (CGA2B3X7R1C104K), Samsung (CL05B104KO5... automotive variants), KEMET, Yageo/KEMET and Taiyo Yuden automotive lines [general knowledge, UNVERIFIED by part]. The 22 µF X5R 0805 has fewer exact equivalents at equal DC-bias performance; this needs part-specific checking.

Criterion 2, temperature:
- `GCM155R71C104KA55D`: X7R, −55 °C to +125 °C, 16 V, AEC-Q200 (Murata datasheet excerpt and Farnell listing, https://be.farnell.com/en-BE/murata/gcm155r71c104ka55d/cap-aec-q200-0-1uf-16v-mlcc-0402/dp/3582682) **[maker via distributor]**.
- X5R parts (GRM...R61) are rated to +85 °C and are not automotive grade; low-end rating is −55 °C [EIA class-II code definition; Murata part numbering, UNVERIFIED against each datasheet]. For outdoor −40 °C use the rating is met; the issue is capacitance loss at temperature extremes and DC bias, which Murata publishes in SimSurfing curves (not retrieved this session).
- Flex cracking: Murata markets the GCJ (automotive) and GRJ series with a conductive-resin termination that "absorb[s] mechanical stress"; its product page warns cracks can still occur beyond the "guaranteed range of board bending strength" in the specification sheet. https://www.murata.com/en-us/products/capacitor/ceramiccapacitor/overview/lineup/smd/gcj **[maker]**; trade press https://www.electronicspecifier.com/products/passives/gcj-grj-murata-soft-termination-capacitors-reduce-cracks-due-to-board-bending **[press restating maker test]**.

Criterion 3, consistency: see cross-brand quality section (2.Q). No Murata-specific recall or quality escape found this session.

Criterion 4, workers: RBA Regular member; KnowTheChain 13/100 (2022), 10/100 (2025), with no first-tier supplier list and no supply-chain remedy (section 2.0b) **[indep]**.

### TDK

BoM dependence: one line each board, `CGA2B2C0G1H120J050BA` (12 pF C0G 0402, CGA = TDK automotive series), 2 placements each.

Criterion 1:
- Japan-listed (TSE 6762). New MLCC building at Kitakami Factory, Iwate, construction from March 2023, mass production planned September 2024; new site at Inakura Factory, Nikaho, Akita announced 2022. TDK press release 10 May 2022, https://www.tdk.com/en/news_center/press/20220510_01.html **[maker]**. TDK's overseas MLCC plants (China, Philippines) were not confirmed in this session (UNVERIFIED).
Criterion 2:
- CGA series is TDK's automotive (AEC-Q200) MLCC line [maker part-numbering; UNVERIFIED datasheet not opened]. TDK publishes a flex-crack solution guide at https://product.tdk.com/en/products/solutionguide/mlcc_flex-crack.html (HTTP 403 to fetch; a search snippet quotes it as warning that the short-circuit failure mode "may cause problems such as abnormal heat generation or ignition of the MLCC") **[maker]**.
Criterion 4: RBA member, tier not marked (Affiliate or Supporter); not in KnowTheChain sample.

### Taiyo Yuden

BoM dependence: one line each board, `TMK107B7105KA-T` (1 µF 0603, 25 V class "TMK", B7 = X7R, UNVERIFIED decoding), 2 placements each. Okapi spells it "Yaiyo Yuden".

Criterion 1:
- Japan-listed (TSE 6976). Production bases in Japan (Niigata, Gunma), Malaysia (Taiyo Yuden (Sarawak) Sdn. Bhd., Kuching), South Korea, and China (Guangdong; Changzhou, factory completed about July 2023). Sources: distributor EDOM, https://www.edomtech.com/en/product-detail/taiyo-yuden-mlcc/ **[distributor restating maker]**; https://passive-components.eu/taiyo-yuden-announces-completion-of-china-factory-to-expand-mlcc-production/ and https://epci.eu/taiyo-yuden-completes-mlcc-factory-at-sarawak-malaysia/ **[trade press]**.
Criterion 4: not an RBA member; not in KnowTheChain sample. Evidence thin.

### Samsung Electro-Mechanics (SEMCO)

BoM dependence: Okapi only, 2 lines/3 placements (`CL10C120JB8NNNC` 12 pF C0G; `CL10B105MO8NNWC` 1 µF). Both are CL10 (0603 size) on 0402 footprints in the Okapi partlist; see section 1.

Criterion 1:
- Korea-listed; separate company from Samsung Electronics. MLCC production is overseas: two plants in Calamba, Laguna, Philippines (SEMPHIL) and one in Tianjin, China; Suwon and Busan described as R&D-focused (Korea Economic Daily, 7 October 2024, https://amp.kedglobal.com/newsView/ked202410070008 **[indep press]**). SEMPHIL accounted for "nearly half" of SEMCO's worldwide MLCC output at end of 2024 (search summary, Korea Times 2024, https://www.koreatimes.co.kr/www/tech/2024/10/129_383767.html; UNVERIFIED exact figure). Location page also lists Thai Nguyen, Vietnam (https://samsungsem.com/global/about-us/company/location.do **[maker]**, not opened).
Criterion 4: Samsung Electro-Mechanics is not on the RBA list (section 2.0); KnowTheChain benchmarks Samsung Electronics only. Evidence thin.

### Vishay (Sprague, Dale, Draloric, Vitramon)

BoM dependence: Okapi only, 1 line: `TL8A0107M010D` (100 µF 10 V molded tantalum, Vishay Sprague, case 1206). Vishay also competes in thick/thin-film resistors (CRCW, TNPW), inductors (IHLP) and MLCCs.

Criterion 1:
- US-listed (NYSE VSH). Form 10-K for 2024 (filed 2025): "At December 31, 2024, our business had 60 manufacturing locations." Owned capacitor and resistor plants include Dimona (resistors and capacitors), Migdal Ha'Emek (capacitors) and Be'er Sheva (resistors, inductors, capacitors), Israel; Blatna, Dolni Rychnov, Prachatice and Volary, Czech Republic; Selb, Heide and others, Germany; Nice and others, France; Loni, India; Miharu, Japan (capacitors); Juarez, Mexico (resistors); Famalicão, Portugal (capacitors). https://www.sec.gov/Archives/edgar/data/103730/000010373025000017/form10k.htm, Item 2 Properties (p. 27) **[maker, SEC filing]**.
- Same 10-K, risk factors: Vishay has operated in Israel for 54 years and "never experienced any material interruption in our operations attributable to these factors, in spite of several Middle East crises, including the recent war with Hamas". **[maker]** The 10-K's plant table does not say which plant makes the TL8 series; tantalum capacitors are made at Israel, Czech and Portugal sites per the table's "Capacitors" entries (assignment of TL8 to a plant UNVERIFIED).
- Raw material concentration (same 10-K, Item 1): "There are few suppliers that process tantalum ore into capacitor grade tantalum powder." **[maker]** This applies to every tantalum brand.
- Interpretation (hypothesis): Vishay is the only surveyed passives maker with most passive capacity in Israel, Central Europe, India and Mexico rather than East Asia; this is a different risk profile from the Japan/Taiwan/China makers, not necessarily a lower one.
Criterion 4: RBA Regular member (section 2.0). Not in KnowTheChain sample. Conflict minerals: Vishay files SEC Form SD (not retrieved this session; UNVERIFIED content).

### KYOCERA AVX

BoM dependence: Okapi only, 1 line: `TPSY227K010R0100` (220 µF 10 V TPS low-ESR MnO2 tantalum, case Y/2917).

Criterion 1:
- Wholly owned by Kyocera Corp. (Japan) since Kyocera's 2020 buyout of the AVX minority (date from general knowledge; UNVERIFIED this session). A 2019 AVX product change notice says El Salvador "currently manufactures automotive grade TAJ EIA Standard and TPS Low ESR molded tantalum chip" (search summary; PCN document at https://file.aichiplink.com/r/pcnassemblyorigin/... not opened; UNVERIFIED current). The Czech subsidiary (Lanškroun, founded 1992 as AVX Czechoslovakia) is part of the tantalum division and runs four factories, https://kyocera-avx.cz/en/o-nas **[maker]**.
Criterion 4: KYOCERA Corporation and KYOCERA AVX Components Corporation are RBA members, tier not marked. Kyocera scored 3/100 (2022, 55th of 60) and 6/100 (2025, 41st of 45) in KnowTheChain (section 2.0b) **[indep]**.

### Panasonic

BoM dependence: Okapi only, 6 lines/11 placements: `ERA-3AEB103V` (10 kΩ 0603 thin-film, 0.1 %, 25 ppm/K class, UNVERIFIED decoding) and five `ERJ-3EKF` 1 % thick-film values. Panasonic also makes the 2-button switch `EVP-BB2A9B000` (out of scope). Panasonic competes in polymer (POSCAP, SP-Cap, OS-CON), aluminum electrolytics and power inductors.

Criterion 1:
- Panasonic Industry "manufactures the majority of its passive components in" Japan, Indonesia and Malaysia; "Japan is home to several of Panasonic's core production sites for capacitors, resistors, and inductors." No family-level assignment, no date. https://industry.panasonic.eu/products/components/country-origin-passive-components **[maker]**. A Panasonic ISO/TS registration page lists "Fixed Chip Resistors ... Thin Film Fixed Chip Resistor" under a Malaysian entity (search snippet of https://industrial.panasonic.com/tw/iso_ts_certification; UNVERIFIED in full).
- Interpretation (hypothesis): Panasonic is the only surveyed resistor maker that states its passives come mainly from outside China and Taiwan. This matters for the thin-film precision resistor, for which second sources (Susumu RG, Vishay TNPW, KOA RN73, Yageo RT) exist but are not all 0.1 %/25 ppm drop-ins.
Criterion 4: Panasonic Holdings is an RBA member, tier not marked. KnowTheChain 9/100 (2022), 10/100 (2025) **[indep]**.

### Würth Elektronik (eiSos)

BoM dependence: Okapi only, 5 in-scope lines/5 placements: four power inductors (`74439346100` WE-XHMI 10 µH; `74404032010` WE-LQS 1 µH; `78438356047` WE-MAIA 4.7 µH; `74438323068` WE-MAPI 6.8 µH) and one MLCC (`885012005060`, 68 pF 0402, WCAP-CSGP family). Every Okapi inductor is Würth, and no inductor on either board has a second source named in the BoM. Out of scope: three LED lines (Okapi) and the SD holder (Margay).

Criterion 1, geography and ownership:
- Family-owned Würth Group (Germany); no ownership event found. Würth's location list (87 locations) shows Thyrnau, Germany (Würth Elektronik iBE) as "Hauptsitz, Produktion, Lager, Vertrieb"; Waldenburg is the eiSos headquarters. https://www.we-online.com/de/unternehmen/standorte (first page only) **[maker]**.
- Shenyang, China: an automotive-division production site making "kundenspezifische Stabkerndrosseln und SMD-Leistungsinduktivitäten für Automotive-Anwendungen" (custom rod-core chokes and SMD power inductors for automotive), 355 employees. https://www.we-online.com/de/unternehmen/standorte/shenyang **[maker]**. Shenzhen hosts the Quality Design Center (test laboratory, phase II opened 5 March 2026) (https://iconnect007.com/article/149667/wrth-elektronik-expands-laboratory-in-shenzhen-china/149664/ein **[trade press]**).
- Würth does not publish which plant (or contract manufacturer) makes the catalog WE-XHMI, WE-MAPI, WE-MAIA, WE-LQS or WCAP-CSGP series. Digi-Key's page for `74439346100` lists no country of origin (https://www.digikey.com/en/products/detail/w%C3%BCrth-elektronik/74439346100/5225475, fetched 2026-11-11). Whether eiSos catalog MLCCs and resistors are made in-house or sourced from another maker is UNVERIFIED; no source either way was found this session. This is the main evidence gap for Würth on criterion 1.
- Second sources: molded metal-alloy power inductors in the same footprints exist from Coilcraft (XGL/XEL), TDK (SPM/TFM), Bourns (SRP), Vishay (IHLP) and Murata (DFE) [general knowledge, footprints not checked part by part; UNVERIFIED]. Footprint-compatible drop-ins are less certain for inductors than for resistors, because each maker's body size and pad layout differ.

Criterion 2, temperature:
- `74439346100` (WE-XHMI) datasheet: "Component Qualification AEC-Q200 Grade 1"; "Operating Temperature −40 °C up to +125 °C"; "Ambient Temperature (referring to IRP) −40 °C up to +85 °C". (Würth datasheet PDF, https://www.we-online.com/components/products/datasheet/74439346100.pdf, fetched 2026-11-11) **[maker]**. Digi-Key lists −40 °C to 85 °C. Note: −40 °C is the rated floor, exactly the Minnesota design minimum, with no margin. The other three inductor datasheets could not be fetched (we-online.com returns an HTML bot page to curl); their lower limits are UNVERIFIED.

Criterion 3: no Würth-specific independent quality evidence found this session.

Criterion 4, workers:
- Not an RBA member. Würth's compliance page states commitment to the RBA Code of Conduct with an undated WE Group "Declaration of Commitment", a UK Modern Slavery Statement, an LkSG (German Supply Chain Due Diligence Act) reporting channel and human-rights policy statements for eiSos and CBT; it says conflict-mineral use "is not an option for us" but does not mention a CMRT. https://we-online.com/en/company/legalinformation/compliance **[maker]**. The eiSos human-rights statement is dated 1 August 2023 per search snippet (https://www.we-online.com/files/pdf1/grundsatzerklaerung.pdf; not opened, UNVERIFIED date). LkSG makes these statements a legal duty enforced by Germany's BAFA, which is a stronger external check than a voluntary code (interpretation; LkSG applicability to eiSos UNVERIFIED by headcount).
- Not in KnowTheChain sample.

### Bourns

BoM dependence: Margay 1 line (`CRT0603-BY-1002ELF`, 10 kΩ 0603 thin-film, 0.1 %, 25 ppm/K "BY", UNVERIFIED decoding); Okapi 1 line/2 placements (`MF-NSMF150-2` PPTC 1206, 1.5 A hold).

Criterion 1:
- Privately held (US, Riverside CA). A Bourns infographic lists sites in Heredia, Costa Rica; Tijuana and Chihuahua, Mexico; Xiamen, Suzhou, Xiang'an and Shanghai, China; Linkou and Taipei, Taiwan. https://www.mouser.lt/pdfdocs/bourns_k1636_infographic.pdf **[maker via distributor; undated, UNVERIFIED as current]**. A 2013 Bourns customer notice said PPTCs were qualified at Xiamen, China and South Korea, moving MF-RX/250 to Xiamen and MF-R/600 to Taipei (search summary; 2013, likely outdated).
- PPTC second sources: Littelfuse (PolySwitch, ex-TE Raychem), TE, Bel Fuse (0ZCx), Eaton. The BoM description field already reads "Bel Fuse PPTC", which suggests a past substitution between these.
Criterion 4: Bourns, Inc. is an RBA member, tier not marked (section 2.0).

### Stackpole Electronics

BoM dependence: Okapi only, 1 line/2 placements (`RMCF0603FT1M62`, 1.62 MΩ 0603 thick-film).
Criterion 1: privately held, Raleigh, NC; "Now part of the Akahane Stackpole Manufacturing Group (ASMG), Stackpole has manufacturing facilities in Japan, Taiwan, China and Mexico" (trade directory text, https://www.manufacturing.net/home/electrical-electronic/company/20831480/stackpole **[secondary, undated]**). Not to be confused with Stackpole International (Johnson Electric, 2015). Ownership stake UNVERIFIED.
Criterion 4: not an RBA member; no other evidence found. Thin.

### Coilcraft

BoM dependence: none on either board.
Criterion 1: privately held, Cary, Illinois; European HQ Cumbernauld, Scotland (https://www.coilcraft.com/en-us/about/ **[maker]**). Plant list varies by source: Mexicali (Mexico), Huizhou (China), Singapore, Taiwan, Cary (directory and older profiles, **[secondary]**, UNVERIFIED as current).
Criterion 4: not an RBA member; no other evidence found. Thin.

### Susumu

BoM dependence: none. Competes in precision thin-film resistors (RG series, 0.05 %, 5–25 ppm/K) against the Panasonic ERA and Bourns CRT parts on Okapi and Margay.
Criterion 1: founded 1964, headquartered in Kyoto (secondary sources via search, e.g. https://www.manufacturingtechnologyinsights.com/susumu). Plant locations not found from a primary source this session; UNVERIFIED.
Criterion 4: not an RBA member; no evidence found. Thin.

### Littelfuse

BoM dependence: none on either board. Competes with Bourns and TE in PPTCs (PolySwitch, acquired from TE in 2016, date from general knowledge, UNVERIFIED) and in TVS diodes.
Criterion 1: US-listed. Opened a 106,000 ft² plant in Piedras Negras, Coahuila, Mexico, in May 2024 (https://littelfuse.com/about-us/news/news-releases/2024/littelfuse-announces-grand-opening-of-manufacturing-plant-in-piedras-negras.aspx **[maker]**). FY2025 10-K Exhibit 21.1 lists Philippine and Chinese subsidiaries (Wuxi, Kunshan) (search summary of https://www.boardroomalpha.com/sec/lfus-10-k-2026-02-19-0001628280-26-009585/exhibit211-12272510k.htm; not opened). Holds about 6.7 % of Polytronics Technology (Taiwan PPTC maker) (search summary, UNVERIFIED). Which plant makes PolySwitch PPTCs: not found.
Criterion 3: the FY2024 10-K reportedly disclosed material weaknesses in internal control tied to inventory cycle counts and skilled personnel at certain non-US manufacturing locations (search summary; financial-control finding, not a product-quality finding; UNVERIFIED wording).
Criterion 4: not an RBA member. Thin.

### Walsin Technology

BoM dependence: none. Competes in MLCCs and chip resistors (Yageo's Taiwanese peer).
Criterion 1: Taiwan-listed; main MLCC base Kaohsiung, with production in China (Dongguan, Suzhou) per trade press 2005–2020 (https://apps.digitimes.com/news/a20201210PD206.html and older DigiTimes items **[trade press, old]**). No 2022+ primary source found this session. UNVERIFIED as current.
Criterion 4: not an RBA member. Thin.

### Rohm, TE Connectivity (on the Okapi BoM)

- Rohm: 1 Okapi line, `PMR10EZPFV3L00` (3 mΩ 0805 current-sense shunt). Not an RBA member; not in KnowTheChain. Plant locations not researched this session (UNVERIFIED).
- TE Connectivity: 1 Okapi line/8 placements, `CRGCQ0402F220R` (220 Ω 0402 thick-film, CRGCQ = AEC-Q200 variant, UNVERIFIED decoding). TE is an RBA member (tier not marked) and scored 11/100 in KnowTheChain 2022. Plant for CRG resistors not found.

### 2.Q Cross-brand evidence on quality, failure mechanisms and counterfeits

Counterfeits (ERAI, independent reporting service; counts are of parts reported to ERAI, not a market sample) **[indep]**:
- 2024: "ERAI reported a total of 1,055 suspect counterfeit and nonconforming parts"; "The decline in reporting of suspect counterfeit and non-conforming capacitors continued with only 6 reported in 2024 (please note: ERAI reported 165 capacitors during the capacitor shortage of 2019)". https://www.erai.com/erai_blog/3187/2024_annual_report
- 2025: "ERAI reported a total of 748 parts"; "the decline in reported nonconforming capacitors appears to have ended, with an upward trend observed in 2025 increasing to 3.74%"; "obsolete parts continued to be most often counterfeited (60.02%)". https://www.erai.com/erai_blog/3192/2025_annual_report
- 2019: an MLCC was the most-counterfeited device type and Murata the most-counterfeited brand (search summary of ERAI 2019/2023 reporting; not fetched, UNVERIFIED wording). Interpretation (hypothesis): counterfeit exposure for passives tracks shortages and brand popularity, not maker quality; buying through an authorized distributor such as Digi-Key removes most of it whatever the brand.
- Field case, 2026: Ford recall NHTSA 26V605 (Ranger) and 26E065 (46 service displays): an MLCC on the display board "is susceptible to cracking, leading to an electrical short"; the part came via tier-2 supplier Suzhou Dongshan Display and is described by Ford as "potentially"/"suspected" counterfeit. Autoevolution, 27 September 2026, https://www.autoevolution.com/news/potentially-counterfeit-capacitors-prompt-2026-ford-ranger-safety-recall-over-black-screens-276179.html **[indep press]**. No MLCC brand was named.
- No 2022–2026 recall or published quality escape was found for any surveyed passives brand (two searches, listed below). This is absence of evidence from a short search, not evidence of clean records.

Flex cracking and MLCC mechanics **[indep]**:
- NASA NEPP (Teverovsky, 2008): flex cracks "mostly originate at the bottom surface near the edge of the termination margin and propagate inside at angles close to 45°"; cites a CALCE analysis of about 40 mechanical capacitor failures: "25% were caused by flex cracking, 23% by thermal shock cracking, and 34% were due to manufacturing defects". https://xdevs.com/doc/NASA/nepp%202008%20ceramic%20capacitors.pdf (mirror; search snippet).
- NASA NEPP 2018 presentation: X7R is weaker than C0G, and larger chips are more crack-susceptible. https://ntrs.nasa.gov/api/citations/20180002843/downloads/20180002843.pdf (search snippet).
- Maker mitigations: Murata GCJ/GRJ, TDK soft-termination (CGA...with "flex" options), KEMET FT-CAP, Würth WCAP-CSST soft-termination lines exist [Murata confirmed above; others general knowledge, UNVERIFIED].

Capacitance versus temperature (EIA class II code, as restated by KEMET and Samsung datasheets) **[maker restating EIA standard]**: X = −55 °C lower limit; 5 = +85 °C, 7 = +125 °C upper limit; R = ±15 % maximum capacitance change across that range. https://www.allaboutcircuits.com/technical-articles/x7r-x5r-c0g...-a-concise-guide-to-ceramic-capacitor-types/; Samsung CL10C datasheet hosted at https://e2echina.ti.com/cfs-file/__key/communityserver-discussions-components-files/24/CL10C_094E1F66FB7C1752C4893C68664E_.pdf. Every Class II MLCC on both BoMs is therefore rated through −40 °C with at most ±15 % change (before DC-bias loss). C0G parts (12 pF, 18 pF, 68 pF) are essentially flat.

Sulfur corrosion of thick-film resistors (relevant to outdoor, agricultural and coal-adjacent sites) **[indep]**:
- Silver sulfide growth in silver-electrode thick-film resistors raises resistance until the part opens; in a Flowers-of-Sulfur test "all 0402 resistors failed", larger sizes far less; only two of seven conformal coatings protected significantly. Universal Instruments study, https://www.circuitnet.com/tech-paper/56279.html (search snippet). A DTU study found anti-sulfur thick-film resistors stayed largely free of corrosion where standard parts corroded within days (https://elmac.dtu.dk/-/media/6e542ccdc8b84d95973b1cc604313f02.pdf, search snippet).
- Panasonic: choosing sulfur-resistant parts is "the most effective prevention"; its anti-sulfur line uses Pd-Ag or gold electrodes. https://industrial.panasonic.com/tw/ss/technical/r5 **[maker]**.
- Relevance (hypothesis): Margay and Okapi use standard (not anti-sulfur) Yageo RC-series resistors: on Okapi, 53 Yageo placements sit on `R0402` footprints and 44 carry an `RC0402` MPN (the difference is the 0603-MPN-on-0402 rows noted in section 1). Anti-sulfur equivalents exist (Yageo AF/AT, Panasonic ERJ-S/ERJ-U, Vishay CRCW-HP e3, KOA RK73-RT, Stackpole RMCF-AS family names from general knowledge, UNVERIFIED). Whether field sites carry enough H₂S/S₈ to matter is unknown.

Conflict minerals (tantalum is a 3TG mineral) **[maker, SEC filing]**:
- Vishay Form SD exhibit 1.01 for 2024: survey responses from suppliers covering "99.74% of the dollar value of 2024 in-scope procurement"; "identified 206 smelters and refiners of 3TG"; some 3TG "may have originated in the Covered Countries"; policy goal "a supply chain that consists of material that is DRC Conflict Free" under OECD guidance. https://www.sec.gov/Archives/edgar/data/103730/000010373025000044/exhibit1-01.htm
- KEMET published a Conflict Minerals Report in May 2024 stating OECD-conformant due diligence (search snippet of https://www.kemet.com/content/dam/kemet/lightning/documents/kemet-docs/KEMET-Conflict-Minerals-Report-May-2024.pdf; PDF now redirects, not read).
- KYOCERA AVX: no report found this session.

## 3. Summary table

Evidence strength: **strong** = primary document read this session (filing, datasheet, benchmark); **moderate** = maker web page or reputable trade press; **weak** = search summary, secondary directory, or old source; **none** = nothing found.

| Brand (BoM placements M/O) | 1. Geopolitical resilience | 2. Wide-temperature quality | 3. Consistent quality | 4. Workers' rights |
|---|---|---|---|---|
| Yageo (25/61) | Taiwan (Kaohsiung ×3) + China (Suzhou ×2, Dongguan); commodity resistors with 6+ drop-in brands (strong for sites; moderate for second sources) | RC_L −55 to +155 °C (moderate) | ISO 9001 all factories, IATF 16949 some; no escapes found (maker claim only; weak) | Not RBA; RBA self-assessment only (strong for membership) |
| Murata (15/39) | Japan-heavy MLCC base (Fukui, Izumo, Okayama coming) plus Thailand, Philippines, Wuxi; ¥1 T expansion to 2030 (moderate) | GCM line AEC-Q200, X7R −55 to +125 °C; soft-termination GCJ/GRJ (moderate) | Most-counterfeited brand in 2019 shortage per ERAI (weak); no escapes found | RBA Regular; KTC 10/100 (2025) (strong) |
| Panasonic (0/11) | States majority of passives made in Japan, Indonesia, Malaysia (moderate) | ERA thin-film; ERA-2V AEC-Q200 (weak) | Publishes sulfur-failure guidance and anti-sulfur line (moderate) | RBA member (unmarked tier); KTC 10/100 (strong) |
| TE (0/8) | Plant for CRG unknown (none) | CRGCQ automotive variant (weak, decoding) | none | RBA member; KTC 11/100 in 2022 (strong) |
| Würth Elektronik (0/5) | German family-owned; Shenyang (China) inductor plant; catalog-series plant and MLCC origin unpublished (moderate; key gap) | WE-XHMI AEC-Q200 Grade 1, −40 to +125 °C (floor = −40 °C, no margin) (strong) | none independent | Not RBA member but commits to RBA code; LkSG channel (moderate) |
| Samsung EM (0/3) | MLCCs made overseas: Philippines (~half) + Tianjin; Vietnam site (moderate) | Class II ±15 % −55 °C rating (moderate) | none | Not RBA (strong); Samsung Electronics' KTC score does not apply |
| Bourns (1/2) | Private US; Costa Rica, Mexico, China, Taiwan (weak, undated) | PPTC and thin-film CRT; not checked | IATF 16949 for MF-USHT PPTC (maker; weak) | RBA member, unmarked (strong) |
| Stackpole (0/2) | Private US, Akahane group; Japan, Taiwan, China, Mexico (weak) | not checked | none | Not RBA; none found |
| TDK (2/2) | Japan MLCC expansion (Iwate, Akita) (moderate); overseas plants unconfirmed | CGA automotive line; flex-crack guide (weak, 403) | none | RBA member, unmarked (strong) |
| Taiyo Yuden (2/2) | Japan, Malaysia (Sarawak), Korea, China (Changzhou, Guangdong) (moderate) | not checked | none | Not RBA (strong); none else |
| Vishay (0/1) | Israel, Czech Republic, Portugal, Germany, India, Mexico, Japan; no material Israel interruption reported (strong) | TL8 tantalum, not checked | Form SD: 206 smelters, OECD due diligence (strong, conflict minerals) | RBA Regular (strong) |
| KYOCERA AVX (0/1) | Kyocera-owned; TPS made in El Salvador per 2019 PCN; Czech tantalum plants (weak/moderate) | not checked | none | RBA member, unmarked; Kyocera KTC 6/100 (strong) |
| KEMET (0/1) | Yageo-owned since 2020; Mexico, Italy, China and others (weak) | not checked | Conflict-minerals report May 2024 (weak, not read) | Not RBA (strong) |
| Rohm (0/1) | not researched | not checked | none | Not RBA (strong) |
| Coilcraft (0/0) | Private US; Mexico, China, Singapore, Taiwan (weak) | not checked | none | Not RBA; none found |
| Susumu (0/0) | Kyoto HQ; plants unconfirmed (weak) | not checked | none | Not RBA; none found |
| Littelfuse (0/0) | New Mexico plant 2024 (moderate); PPTC plant unknown | not checked | 10-K control weakness at non-US plants (weak; financial, not product) | Not RBA (strong) |
| Walsin (0/0) | Taiwan + China (weak, pre-2021) | not checked | none | Not RBA (strong) |

## 4. Open questions

1. Country of origin per part number for the top lines (Yageo RC0402 values, Murata GCM155/GRM21B), from Digi-Key's product pages or the makers' certificates of conformance. The sites are known by brand, not by part.
2. Where Würth makes (or sources) the four Okapi inductors and the WCAP-CSGP MLCC; ask Würth directly. Also the lower operating limit of WE-LQS, WE-MAIA and WE-MAPI (only WE-XHMI was read: −40 °C floor).
3. Whether Margay and Okapi field sites see enough sulfur (agricultural, peat, coal-plant air) to justify anti-sulfur resistors for the 0402 Yageo parts.
4. Murata and TDK X5R/X7R capacitance at −40 °C and at operating DC bias for the 10 µF and 22 µF 0805 parts (SimSurfing / SEAT curves not retrieved).
5. The Okapi BoM rows whose package and MPN disagree (330 Ω 0603 MPN on 0402 footprint, Samsung CL10 on C0402, 287 Ω rows carrying 232 Ω and 453 Ω MPNs) – which is correct.
6. RBA validated-audit (VAP) status per plant, which the member list does not show; and KYOCERA AVX's and Würth's conflict-minerals reports (CMRT).
7. Plant locations for Rohm, Susumu and TE's CRG resistors, and current Walsin sites (only pre-2021 sources found).

## 5. Sources checked (including dead ends)

- 2026-11-11 RBA member list, https://www.responsiblebusiness.org/about/members/ – useful; tier legend confirmed in page text.
- 2026-11-11 KnowTheChain 2022 ICT report PDF and 2025 scorecards (Murata, Kyocera, Panasonic) – useful. TDK, Vishay, Yageo, Taiyo Yuden, Rohm, Samsung Electro-Mechanics not in either sample (grepped 2022 report text; 2025 company list from briefing page).
- 2026-11-11 Yageo 2024 Annual Report PDF (yageogroup.com) – useful (sites, Shibaura, tariffs).
- 2026-11-11 Yageo ESG 2023 English PDF – useful (factory scope, ISO/IATF, RBA SAQ).
- 2026-11-11 yageogroup.com/en/Company/Location – dead end (JavaScript page, no content).
- 2026-11-11 kemet.com sustainability page – dead end (redirects to yageogroup.com, JavaScript).
- 2026-11-11 web search "Yageo Shibaura tender FEFTA" – press summaries used, primary filings not read.
- 2026-11-11 Evertiq 2026-10-30 Murata ¥1 trillion article – useful (fetched).
- 2026-11-11 search: Murata/TDK/Taiyo Yuden/SEMCO plant locations – press summaries; TDK overseas plants not found.
- 2026-11-11 product.tdk.com flex-crack guide – HTTP 403 (dead end for direct fetch).
- 2026-11-11 search: Murata GCJ/GRJ soft termination – maker product page and trade press.
- 2026-11-11 Vishay Form 10-K FY2024 (sec.gov, accession 0000103730-25-000017) – useful (Item 2 plant table; Israel risk factor; tantalum powder suppliers).
- 2026-11-11 search: KYOCERA AVX TPS plant – 2019 PCN via search only; current plant assignment not found.
- 2026-11-11 Panasonic EU country-of-origin page – useful but family-level assignment absent.
- 2026-11-11 we-online.com Standorte and Shenyang pages – partly useful (only page 1 of 87 locations rendered).
- 2026-11-11 we-online.com datasheet PDFs via curl – dead end (bot page); WE-XHMI datasheet obtained via WebFetch.
- 2026-11-11 we-online.com modern-slavery-statement_wegroup.pdf – HTTP 404.
- 2026-11-11 we-online.com compliance page – useful (RBA commitment, LkSG channel).
- 2026-11-11 Digi-Key product page 74439346100 – temperature listed, no country of origin.
- 2026-11-11 searches: Bourns sites, Stackpole ownership, Coilcraft sites, Susumu plants – secondary sources only.
- 2026-11-11 ERAI 2024 and 2025 annual-report blog pages – useful (fetched).
- 2026-11-11 Autoevolution Ford Ranger recall article – useful (fetched); NHTSA filings not opened.
- 2026-11-11 search: Japan passive-component data falsification – dead end (only 2017–2021 cases in steel, materials, brakes; none in passives).
- 2026-11-11 search: MLCC recall by Murata/TDK/SEMCO/Yageo – dead end except Ford case (no brand named) and a TDK CGJ end-of-life notice (2023, not a defect).
- 2026-11-11 Vishay Form SD exhibit 1.01 (2024) – useful (fetched with curl).
- 2026-11-11 KEMET conflict minerals PDF – dead end (redirect/HTML).
- 2026-11-11 searches: NASA NEPP MLCC cracking, sulfur corrosion, EIA class II codes – snippets used; PDFs not opened.
- 2026-11-11 searches: Walsin plants (only 2005–2020 trade press), Littelfuse sites (press release + 10-K exhibit via summary).

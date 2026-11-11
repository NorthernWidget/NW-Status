# Semiconductor brands for Northern Widget loggers: sourcing survey

Status: COMPLETE (2026-11-11)

Agent report, 2026-11-11. Scope: analog and power ICs, microcontrollers, logic and level shifters, discretes, RTC and memory. Criteria in order: (1) geopolitical resilience, (2) wide-temperature quality, (3) consistent quality, (4) workers' rights.

Evidence labels: **[MAKER]** the manufacturer's own claim; **[INDEP]** independent source (government, press, NGO, benchmark, distributor data); **UNVERIFIED** not confirmed by a source fetched in this session.

## 1. What the boards actually buy

Method: Margay BoM read with Python `csv.DictReader` from `Project-Margay/Production/Margay_BoM_3v0_-_2026-11-04.csv` (46 lines); Okapi BoM `CAMOutputs/Assembly/Okapi.txt` extracted with `unzip -p` from `Project-Okapi/Hardware/Okapi_2024-11-02.zip` and split on the header's column offsets (122 lines). Manufacturer names were normalized to the current owner: Atmel → Microchip; Maxim and LT → Analog Devices; Fairchild and "ON Semiconductor" → onsemi. One BoM error was corrected: `MCP23018T-E/MJ` is listed with MF = "TI" but is a Microchip part. Sensors (Bosch, Melexis, Vishay VEML6030) are counted because they are semiconductors, though their deep survey may belong to another agent.

"Lines" = BoM rows; "placements" = sum of the Qty column.

| Owner | Margay lines | Okapi lines | Combined lines | Combined placements |
|---|---|---|---|---|
| Texas Instruments | 8 | 18 | 26 | 36 |
| Microchip (incl. Atmel, and MCP23018 mislabeled TI) | 3 | 7 | 10 | 13 |
| Diodes Incorporated | 4 | 3 | 7 | 11 |
| Analog Devices (Maxim 3, Linear 2) | 2 | 3 | 5 | 5 |
| Bosch Sensortec | 1 | 2 | 3 | 3 |
| FTDI | 1 | 1 | 2 | 2 |
| Central Semiconductor | – | 2 | 2 | 3 |
| onsemi (Fairchild FDN360P, BAT54C) | – | 2 | 2 | 3 |
| Fujitsu / RAMXEED (MB85RC512T) | – | 1 | 1 | 1 |
| NXP (PCA9634) | – | 1 | 1 | 1 |
| Melexis (MLX90393) | – | 1 | 1 | 1 |
| Vishay Semiconductors (VEML6030) | – | 1 | 1 | 1 |
| **Total semiconductor lines** | **19** | **42** | **61** | **80** |

Single-source parts that would stop a build: ATmega1284P (both boards), DS3231M (both), FT231XQ (both), MB85RC512T (Okapi), LT3652 (Okapi), TPL5010/TPL5111, TPS22916/22917. Particle B-series SoM (Okapi, via TE M.2 connector 2199230-4) is not a BoM line but is the cellular dependency.

Not in scope but noted: Rohm appears on Okapi only as a current-sense resistor (PMR10EZPFV3L00); Vishay Sprague tantalum (passive).

**Headline:** the boards depend on Texas Instruments above all (26 of 61 semiconductor lines, 43 %), then Microchip (10, including the MCU on both boards), Diodes Inc (7, all discretes), and Analog Devices (5, including the RTC on both boards).

## 2. Per-brand findings

(Appended as confirmed.)

### Texas Instruments (TI)

BoM: 26 lines (43 % of semiconductor lines), every power, logic, level-shift and timer part.

**Criterion 1 – geography and ownership**
- Wafer fabs [MAKER]: 300 mm fabs at Sherman TX (SM1 in production, SM2 construction complete), Lehi UT (LFAB1 in 300 mm production from 2022; LFAB2 under construction), Richardson TX (RFAB1 2009, RFAB2 production 2022); Aizu, Japan named as a GaN factory (Oct 2024 news item). TI states 15 manufacturing sites and seven assembly/test (A/T) sites, and that internal wafer and A/T operations will support "more than 95% of our production by 2030". Source: https://www.ti.com/about-ti/company/ti-at-a-glance/manufacturing.html (fetched 2026-11-11).
- Second A/T factory opened in Melaka, Malaysia, November 2025 [MAKER], same page.
- Properties list, FY2025 Form 10-K, Item 2 [MAKER, regulatory filing]: North Texas (Dallas, Richardson, Sherman); Lehi UT; South Portland ME; Tucson AZ; Santa Clara CA (leased); Houston TX; Chengdu, China; Shanghai, China (leased); Freising, Germany; Bangalore, India; Aizu and Miho, Japan; Kuala Lumpur and Melaka, Malaysia; Aguascalientes, Mexico (leased); Baguio and Pampanga (Clark), Philippines; Taipei, Taiwan. The table as fetched does not classify sites as fab or A/T, so which of the Asian sites are fabs versus A/T is UNVERIFIED here (from memory: Chengdu has both a fab and A/T; the Philippine, Malaysian, Mexican and Taipei sites are A/T). https://www.sec.gov/Archives/edgar/data/97476/000009747626000059/txn-20251231.htm
- Same 10-K, Item 1: "In 2025, we sourced the majority of our wafer fabrication, as well as assembly and test, internally" and "we selectively use the capacity of outside suppliers, commonly known as foundries". About 50 % of 2025 revenue was products shipped into China; about 20 % from customers headquartered in China. [MAKER]
- Ownership: US-listed (NASDAQ: TXN), no ownership change. Independent check on the 2024 internal-share figure (90 % wafers internal, ~70 % A/T internal) is from secondary press only: https://marklapedus.substack.com/p/ti-to-invest-60-billion-in-us-fabs – UNVERIFIED against a primary source.
**Criterion 4**: RBA member, Regular tier (RBA members page, fetched 2026-11-11). KnowTheChain 2025: 30th of 45, 12/100, down from 23rd of 60 (21/100) in 2022. Form SD filed 2026-06-01.

- Practical reading: TI is the least foundry-dependent analog maker in this survey; its Taiwan exposure is one Taipei A/T-area site, not a foundry. But almost all its packaging is in Southeast Asia (Malaysia, Philippines) and China, so a part's back-end country depends on the part.


### Nexperia

BoM: 0 lines. Relevant because Nexperia is the main pin-compatible second source for the boards' generic discretes (2N7002W, BAT54C, BAT43WS-class Schottkys) and for 74AUP/74LVC single-gate logic.

**Criterion 1 – geography and ownership (dated)**
- Fabs [MAKER]: two wafer fabs, Hamburg (Germany; 6- and 8-inch) and Manchester (UK; TrenchMOS power MOSFETs). Assembly/test: Guangdong (Dongguan; "largest small-signal assembly site", >50 billion pieces/yr), Seremban (Malaysia; ~20 billion pieces/yr), Cabuyao (Philippines; back-end for Manchester). https://www.nexperia.com/about/worldwide-locations/manufacturing ; factsheet https://nexperia.com/dam/jcr:23b7e538-602b-4d56-a066-a58b2abadeed/Nexperia%20Factsheet%20July%202024.pdf (as summarized by search; fetched indirectly).
- Ownership: wholly owned subsidiary of Wingtech Technology (China). [INDEP and MAKER]
- 2 Dec 2024: US Commerce placed Wingtech on the Entity List; Nexperia acknowledged it was affected as Wingtech's subsidiary [MAKER]: https://www.nexperia.com/about/news-events/press-releases/update-on-company-developments-2
- 1 Mar 2024: UK final order under the National Security and Investment Act 2021 completed Nexperia's forced sale of Newport Wafer Fab to Vishay (agreed Nov 2023; reported ~US$177 M) [INDEP]: https://www.semiconductor-today.com/news_items/2024/mar/vishay-060324.shtml ; https://www.theregister.com/2023/11/09/nexperia_sells_newport_wafer_fab/
- 29 Sep 2025: BIS "Affiliates Rule" extended Entity List restrictions to entities ≥50 % owned by listed parties, which would cover Nexperia [INDEP]: https://www.wr.no/en/news/affiliates-rule-suspended-as-dutch-nexperia-case-highlights-extraterritorial-impact . Suspended by Federal Register notice of 10 Nov 2025 for one year; on 5 Nov 2026 BIS extended the suspension to 10 Jan 2027 [INDEP]: https://www.thompsonhinesmartrade.com/2026/11/bis-extends-affiliates-rule-until-january-2027/ ; https://www.cliffordchance.com/briefings/2026/11/bis-suspends-affiliates-rule-until-january-10-2027.html
- 30 Sep 2025 (made public 12 Oct 2025): the Dutch Minister of Economic Affairs invoked the Goods Availability Act (Wet beschikbaarheid goederen) against Nexperia; the Amsterdam Enterprise Chamber separately suspended CEO Zhang Xuezheng [INDEP]: https://foreigninvestment.bakermckenzie.com/2025/10/21/dutch-government-uses-rare-emergency-powers-to-intervene-in-chinese-owned-nexperia/ ; https://nltimes.nl/2025/10/13/dutch-govt-takes-rare-move-oust-ceo-chip-firm-nexperia-china-ties
- ~4 Oct 2025: China's commerce ministry barred Nexperia China and its subcontractors from exporting finished products made in China; automakers reported shortages [INDEP]: https://nltimes.nl/2025/10/14/china-imposes-export-ban-dutch-intervention-chipmaker-nexperia . (Exact date of the Chinese notice UNVERIFIED; sources say early October.)
- 9 Nov 2025: China eased the export ban; 19 Nov 2025: Minister Karremans suspended (did not revoke) the Goods Availability Act order; the Enterprise Chamber ruling stayed in force [INDEP]: https://www.euronews.com/2025/11/19/dutch-government-suspends-takeover-of-chinese-owned-nexperia ; https://www.aljazeera.com/economy/2025/11/20/the-netherlands-suspends-takeover-of-nexperia-easing-tensions-with-china
- Feb 2026: Enterprise Chamber ordered a formal investigation (secondary report only, UNVERIFIED).
- 23 Sep 2026 [INDEP, Chinese press]: the dispute is unresolved; Nexperia operates as "two systems" (Dutch HQ versus Nexperia China); Nexperia China cannot get wafers from Hamburg or Manchester, and the Dutch HQ has no access to the China-controlled back-end; about 70 % of Nexperia's shipments came from Dongguan before the dispute; Nexperia China brought up a 12-inch wafer platform with Chinese partners (risk production July–August 2026). https://www.yicaiglobal.com/news/dutch-chipmaker-nexperia-has-rebuilt-supply-chain-in-china-despite-control-dispute
- 31 Aug 2026: Wingtech reported a Dongguan court froze about CNY 2.1 billion of Nexperia assets in China (secondary report, UNVERIFIED): https://www2.yicaiglobal.com/news/wingtech-secures-freeze-on-dutch-chipmaker-nexperias-china-assets-amid-control-battle
- Practical reading: a Nexperia part number now can mean two different supply chains (Dutch-controlled wafer → Malaysia/Philippines back-end, or China-controlled). Which one ships under a given Digi-Key reel is not stated on the listing (UNVERIFIED; no source found). Nexperia is the brand in this survey with the most live ownership and export-control events.



### Analog Devices (ADI; includes Maxim Integrated and Linear Technology)

BoM: 5 lines – DS3231MZ+ RTC (both boards), MAX6070 reference (Margay), LT3652 solar charger and LTC4412 PowerPath controller (Okapi).

**Criterion 1 – geography and ownership**
- FY2025 Form 10-K (fiscal year ended 1 Nov 2025), Item 1 [MAKER, regulatory filing]: ICs are fabricated at internal fabs in Wilmington MA, Camas WA, Beaverton OR and Limerick, Ireland, "and also on a mix of proprietary and non-proprietary processes at third-party wafer fabricators. We currently source more than half of our wafer requirements annually from third-party wafer fabrication foundries, such as Taiwan Semiconductor Manufacturing Company (TSMC)". Back-end: "an assembly, wafer sort and testing facility in Penang, Malaysia and wafer sort and test facilities in the Philippines and Thailand", plus "extensive use of third-party subcontractors for the assembly and testing". The Penang facility is classified as held for sale. Item 2 lists Cavite (Philippines) and Chonburi (Thailand) as wafer probe and test sites. Risk factors name "tensions across the Taiwan Strait". https://www.sec.gov/Archives/edgar/data/6281/000000628125000153/adi-20251101.htm
- Reading: ADI has the largest stated Taiwan-foundry dependence of the US analog makers in this survey (more than half of wafers from foundries, TSMC named). Which fab makes a given legacy Maxim part such as the DS3231M is not published per part (UNVERIFIED; Maxim's product-reliability reports historically name the fab process, see open questions).
- Ownership: US-listed (NASDAQ: ADI). Acquired Linear Technology (2017) and Maxim Integrated (completed August 2021) – dates from memory, UNVERIFIED in this session.
- Second sources: DS3231M has no pin-compatible second source at the same accuracy (UNVERIFIED; the closest alternatives such as Micro Crystal RV-3028 or NXP PCF2129 are not pin-compatible). LT3652 and LTC4412 are single-source. MAX6070 has functional but not pin-identical alternatives (UNVERIFIED).

**Criterion 4**: RBA member, Regular tier (https://www.responsiblebusiness.org/about/members/, fetched 2026-11-11). KnowTheChain 2025: 31st of 45, 11/100 (see cross-brand table).

### Microchip Technology (includes Atmel and Micrel)

BoM: 10 lines – ATmega1284P-MUR MCU (both boards), MCP3421, MCP4726, MCP23018, PAC1934, LM4040, MIC94090/94094, MIC2544.

**Criterion 1 – geography and ownership**
- FY2026 Form 10-K (fiscal year ended 31 Mar 2026; filed May 2026) [MAKER, regulatory filing]: owned wafer fabs are Fab 4, Gresham OR (8-inch, 0.11–0.5 µm; expansion paused "through fiscal 2027"), Fab 5, Colorado Springs CO (6-inch, discrete and specialty), and Lawrence MA; Fab 2 (Tempe AZ) closed May 2025 and is held for sale. "In fiscal 2026, approximately 65% of our sales came from products that were produced at outside wafer foundries", "including all of our 300mm wafer requirements". Assembly/test: owned facilities in Chachoengsao, Thailand, and Calamba (Lamesa and Canlubang), Philippines; "approximately 67% of our assembly requirements" and "approximately 69% of our test requirements were performed in internal facilities". Sales: 18 % China, 15 % Taiwan. https://www.sec.gov/Archives/edgar/data/827054/000082705426000016/mchp-20260331.htm
- The filing does not name the foundries; Taiwan exposure through foundries is likely but UNVERIFIED from this filing. Which fab makes the ATmega1284P is UNVERIFIED.
- Ownership: US-listed (NASDAQ: MCHP); acquired Atmel in 2016 and Micrel in 2015 (from memory, UNVERIFIED in this session).
- Quality-system certifications stated in the same 10-K [MAKER]: ISO 9001:2015, IATF 16949:2016, AS9100, TL9000.

**Criterion 4**: RBA member, Full tier (RBA members page, fetched 2026-11-11). KnowTheChain 2025: joint 31st of 45, 11/100.


### Diodes Incorporated

BoM: 7 lines, 11 placements – 2N7002W-7-F, DMG3404L-7, DMP3099L-7 MOSFETs; BAT43WS-7-F and B340A-13-F Schottkys. All are generic parts with many pin-compatible second sources (Nexperia, onsemi, Vishay, Rohm, Toshiba; per-part cross not checked, UNVERIFIED).

**Criterion 1 – geography and ownership**
- FY2025 Form 10-K (filed Feb 2026) [MAKER, regulatory filing]: wafer fabrication at Shanghai and Wuxi (China), Oldham (England), Greenock (Scotland), Hsinchu (Taiwan) and South Portland (Maine, bought from onsemi June 2022); assembly and test at Shanghai, Chengdu and Wuxi (China), Neuhaus am Rennweg (Germany), and Chongli (Taiwan). Risk factors: "The majority of our manufacturing facilities are located in China"; "We have a significant portion of our manufacturing capacity in mainland China"; about 45 % of 2025 sales shipped to customers in China. Acquired Lite-On Semiconductor (Taiwan) in 2020, and Greenock fab from TI in 2019. https://www.sec.gov/Archives/edgar/data/29002/000119312526044918/diod-20251231.htm
- Certifications [MAKER]: ISO 9001:2015, ISO 14001:2015, IATF 16949:2016 for automotive products; C-TPAT. Same filing.
- Ownership: US-listed (NASDAQ: DIOD), headquartered Plano TX. No sanction or export-control event found in this session.
- Reading: US company, China-centered manufacturing. The back-end for the SOT-23/SOD-323 discretes on the BoM is very probably China (UNVERIFIED per part; the filing lists no Southeast Asian back-end).

**Criterion 4**: not on the RBA members list (fetched 2026-11-11); not in KnowTheChain 2022 or 2025.

### onsemi (includes Fairchild)

BoM: 2 lines, 3 placements – FDN360P P-MOSFET (Fairchild) ×2, BAT54C dual Schottky (no MPN on the Okapi BoM).

**Criterion 1**
- FY2025 Form 10-K [MAKER, regulatory filing]: "We operate front-end wafer fabrication facilities in the United States, the Czech Republic, Japan, South Korea, and Malaysia and back-end assembly and test site facilities in Canada, China, Malaysia, the Philippines, Vietnam and the United States." Front-end sites: East Fishkill NY, Gresham OR, Rožnov pod Radhoštěm (Czechia), Seremban (Malaysia), Bucheon (S. Korea), Mountaintop PA, Aizuwakamatsu (Japan), Nampa ID, Hudson NH. Back-end: Burlington (Canada), Leshan (China; 80 % JV, Leshan-Phoenix), Seremban (Malaysia), Carmona, Tarlac City and Cebu (Philippines), Shenzhen and Suzhou (China), Bien Hoa (Vietnam). 2025 revenue 51 % automotive. https://www.sec.gov/Archives/edgar/data/1097864/000109786426000006/on-20251231.htm
- Ownership: US-listed (NASDAQ: ON). Sold South Portland fab to Diodes (2022).
- Reading: geographically the most spread front-end of any discrete maker here, with no Taiwan fab and back-end split across China, SE Asia and Vietnam.

**Criterion 4**: RBA member, Full tier. Not in KnowTheChain 2022 list; 2025 scorecard not found.

### Vishay Intertechnology (semiconductors)

BoM: 1 semiconductor line – VEML6030 ambient-light sensor (Vishay Semiconductors opto). Vishay is also a second source for the generic MOSFETs and Schottkys.

**Criterion 1**
- FY2025 Form 10-K [MAKER, regulatory filing]: owned semiconductor sites include Turin, Italy (diodes), Melaka, Malaysia (optoelectronic components), Taipei, Taiwan (diodes), Kaohsiung, Taiwan (MOSFETs), and Newport, Wales (MOSFETs; bought from Nexperia 2024); leased diode sites in Vöcklabruck (Austria), Tianjin, Shanghai and Xi'an (China); a 12-inch fab under construction in Itzehoe, Germany. Manufacturing is placed in India, Israel, Malaysia, Mexico, China and the Philippines "where we can benefit from lower labor costs". Class B shareholders hold about 49.5 % of voting power (31 Dec 2025). https://www.sec.gov/Archives/edgar/data/103730/000010373026000019/form10k.htm
- Reading: the VEML6030 is probably made in Melaka (the only listed optoelectronics site), UNVERIFIED per part.

**Criterion 4**: RBA member, Regular tier. Not in KnowTheChain.

### NXP Semiconductors

BoM: 1 line – PCA9634 LED driver (Okapi). NXP is also a second source for 74AUP/74LVC logic and TXS/TCA-class level shifters (UNVERIFIED per part).

**Criterion 1**
- FY2025 Form 10-K [MAKER, regulatory filing]: front-end fabs at Singapore (SSMC, 61.2 % NXP, JV with TSMC; 8-inch), Nijmegen (Netherlands; 8-inch), Chandler AZ (8-inch, and 6-inch GaN), Austin TX (8-inch). Back-end, all 100 % owned: Kaohsiung (Taiwan), Bangkok (Thailand), Kuala Lumpur (Malaysia), Tianjin (China); "Most of our assembly and test activities are maintained in-house." New JV fabs: VSMC Singapore (40 % NXP, with Vanguard; production targeted 2027) and ESMC Dresden (10 % NXP, 70 % TSMC; production targeted 2028). Uses third-party foundries for the rest (share not stated in the passages read). https://www.sec.gov/Archives/edgar/data/1413447/000141344726000008/nxpi-20251231.htm
- Ownership: Dutch NV, US-listed (NASDAQ: NXPI).

**Criterion 4**: RBA member, Full tier. KnowTheChain: best semiconductor score in this survey – 6th of 45, 36/100 in 2025 (10th of 60, 39/100 in 2022).

### STMicroelectronics

BoM: 0 lines. Candidate second source for MCUs (STM32), logic, LDOs, discretes, and an ST RTC/FRAM-alternative EEPROM.

**Criterion 1**
- 2025 Form 20-F [MAKER, regulatory filing]: front-end fabs at Agrate (Italy; 200 and 300 mm), Ang Mo Kio (Singapore), Catania (Italy), Crolles and Rousset (France), Norrköping (Sweden; SiC substrate). Back-end: Bouskoura (Morocco), Calamba (Philippines), Kirkop (Malta), Marcianise (Italy), Muar (Malaysia), Rennes (France), Shenzhen (China; jointly owned with Shenzhen SEG Hi-Tech, a Shenzhen Electronics Group subsidiary). "In 2025, we subcontracted approximately 25% of the value of our total silicon production to external foundries." A 200 mm SiC JV with Sanan Optoelectronics in Chongqing, China, was announced 7 June 2023. https://www.sec.gov/Archives/edgar/data/932787/000093278726000009/stm-20251231.htm
- Ownership: ST Holding N.V. owned about 27.5 % of shares at 31 Dec 2025; its shareholders are "ultimately controlled by the French or Italian government". Same filing.
- Reading: the most Europe-centered front-end in this survey, with three EU countries and Singapore; three back-end sites in the EU or Malta plus Morocco.

**Criterion 4**: RBA member, Full tier. KnowTheChain 2025: joint 19th of 45, 20/100.


### FTDI (Future Technology Devices International)

BoM: 2 lines – FT231XQ-R USB–UART bridge (both boards). Single source: no pin-compatible second source for the FT231X QFN-20 footprint is known (UNVERIFIED; functional alternatives such as Silicon Labs CP2102N or WCH CH340/CH9102 need a different footprint and driver).

**Criterion 1 – ownership event (dated)**
- FTDI describes itself as fabless, headquartered in Glasgow, with R&D in Glasgow, Singapore and Taipei [MAKER]: https://www.ftdichip.com/old2020/FTContact.htm . Manufacturing by Asia-Pacific subcontractors (Wikipedia, https://en.wikipedia.com/wiki/FTDI – secondary); the foundry for the FT231X is not published (UNVERIFIED).
- 5 Nov 2024: UK final order under the National Security and Investment Act 2021 requires China-registered FTDI Holding Limited to sell its 80.2 % stake in FTDI; the stake had passed 75 % in Dec 2021 [INDEP, government]: https://www.gov.uk/government/publications/acquisition-of-802-of-shares-in-future-technology-devices-international-limited-by-ftdi-holding-limited-notice-of-final-order/acquisition-of-802-of-shares-in-future-technology-devices-international-limited-by-ftdi-holding-limited-notice-of-final-order-variation ; https://evertiq.com/news/56717 (7 Nov 2024). The original 2021 buyer group was led by Beijing Jianguang Asset Management (JAC Capital) per Caixin (https://www.caixinglobal.com/2026-02-05/chinese-consortium-forced-to-sell-uk-chipmaker-ftdi-in-national-security-crackdown-102411619.html, paywalled).
- 25 Jul 2025: the High Court rejected FTDI Holding's challenge to the order [INDEP]: https://cms.law/en/gbr/legal-updates/uk-high-court-rejects-second-challenge-under-uk-investment-screening-regime-key-takeaways-for-investors
- Divestment deadline: Caixin (Feb 2026) reports February 2027 – UNVERIFIED. No completed sale or named buyer found as of 2026-11-11.
- Reading: FTDI is a single-source part on both boards whose owner is under a forced-sale order. The order does not stop FTDI trading; it is a governance risk, not a supply stop, on present evidence.

**Criterion 4**: not an RBA member; not benchmarked.

### RAMXEED (formerly Fujitsu Semiconductor Memory Solution) – FRAM

BoM: 1 line – MB85RC512TPNF FRAM (Okapi). Infineon's FM24-series I²C FRAM (ex-Cypress/Ramtron) is the likely second source; whether a 512 kbit FM24 part is pin- and protocol-compatible with the MB85RC512T was not checked (UNVERIFIED).

**Criterion 1**
- Renamed RAMXEED effective 1 Jan 2025; established 31 Mar 2020 as a Fujitsu spin-off; HQ Yokohama; "over 20 years of mass production of FeRAM, with a cumulative total of 4.4 billion units shipped" [MAKER]: https://ramxeed.com/company/about ; https://www.ramxeed.com/news/notification-of-company-name-change/
- A February 2021 profile lists Fujitsu Semiconductor Limited as 100 % shareholder [MAKER]: https://www.mouser.com/pdfDocs/FUJITSU_Memory_Solution_Profile.pdf . Current ownership after the rename is UNVERIFIED (no source found).
- Wafer source: UNVERIFIED. The former Mie Fujitsu fab is now United Semiconductor Japan (UMC group) and offers non-volatile memory on 300 mm, but no source ties it to RAMXEED FeRAM: https://www.usjpc.com/en/business-e
- Fujitsu-era automotive FeRAM rated to 125 °C exists (MB85RS4MTY) [MAKER]: https://www.fujitsu.com/jp/group/fsm/en/products/feram/device/spi-125c-4m-mb85rs4mty.html

**Criterion 4**: RAMXEED not on the RBA list; Fujitsu Limited (the former parent) is an RBA member (unmarked tier).


### Particle (cellular SoM; criterion 1 only)

Okapi carries a Particle B-series SoM in an M.2 E-key socket (TE 2199230-4). Which SKU is fitted is not on the BoM.

- Modems [MAKER]: B404X uses the u-blox SARA-R510S-01B (LTE Cat M1); operating range normal −20 to +65 °C, extended −40 to +85 °C "RF performance may be affected": https://docs.particle.io/reference/datasheets/b-series/b404x-datasheet/ . B524/B523 use the Quectel EG91-E (LTE Cat 1); normal −20 to +75 °C, extended −40 to +85 °C: https://docs.particle.io/reference/datasheets/b-series/b524-b523-datasheet/
- Where the SoMs are assembled: not published; Particle's Japan certificate gives only its San Francisco address (https://docs.particle.io/assets/pdfs/b524-japan-201-240198.pdf). UNVERIFIED.
- u-blox: Swiss, fabless; modules built by contract manufacturers in unnamed countries (secondary source, UNVERIFIED). Taken private by Advent International: tender completed 26 Nov 2025, >98 % of shares, squeeze-out and SIX delisting to follow [INDEP/acquirer]: https://adventinternational.com/news/advent-completes-acquisition-of-u-blox
- Quectel: Chinese (Shanghai HQ); its own factory in Changzhou, China (Global Intelligent Manufacturing Center, opened 2023; production began 2020; maker claims up to 150 million modules/yr) [MAKER]: https://www.quectel.com/news-and-pr/innovation-headquarters-advanced-smart-factory ; https://quectel.com/company/history/
- Quectel export-control and procurement events [INDEP, secondary]: added to the US DoD Section 1260H "Chinese military companies" list on 7 Jan 2025; the FY2024 NDAA Section 805 DoD procurement ban on such modules took effect 30 Jun 2026 (https://5gstore.com/blog/2025/06/19/dod-1260h-and-5g-routers/ – retailer blog, confirm against the Federal Register; UNVERIFIED). An FCC Covered List addition of Quectel requires a national-security-agency determination; none found as of this search. May 2026 press reported the administration debating a ban on Chinese cellular modules (https://gigazine.net/gsc_news/en/20260513-fcc-debating-ban-on-chinese-cellular-modules/). On 22 Jul 2026 the FCC voted to close the "component part loophole" for Covered-List makers (Huawei named; Quectel not named): https://www.thestar.com.my/tech/tech-news/2026/07/23/fcc-votes-to-bar-sales-of-devices-with-parts-from-chinese-firms-posing-risks
- Reading: for US deployments the B404X (u-blox, Swiss-owned, now private-equity) carries less regulatory exposure than a Quectel-based B524/B523, which faces a live risk of US sale restrictions on devices containing Chinese modules. This is a hypothesis about direction of policy, not a prediction.

### Infineon Technologies

BoM: 0 lines. Relevant as owner of the Cypress/Ramtron FRAM line (FM24 series, a second source for the MB85RC FRAM) and of International Rectifier MOSFETs.

- New back-end site opened in Samut Prakan (Bangkok), Thailand, 1 Oct 2026, with wafer test and room for five modules [MAKER]: https://evertiq.com/design/2026-10-01-infineon-opens-backend-site-in-bangkok-with-room-for-five-modules
- Full front-end and back-end list not fetched this session. From memory, UNVERIFIED: front-end Dresden and Regensburg (Germany), Villach (Austria), Kulim (Malaysia), Austin TX (ex-Cypress), Cegléd (Hungary); back-end Melaka (Malaysia), Batam (Indonesia), Wuxi and Beijing (China), Cavite (Philippines), Cheonan (S. Korea). Check Infineon's annual report.
- ESMC Dresden JV with TSMC: Infineon 10 % (NXP 10-K, above).
- Criterion 4: RBA Regular member; KnowTheChain 2025 joint 37th of 45, 8/100 (lowest score among benchmarked brands here).

### Renesas Electronics

BoM: 0 lines. Candidate RTC (ISL1208/ISL12022 family, ex-Intersil), MCU and power second source.

- Kofu, Japan reopened 2024 as a dedicated 300 mm power-semiconductor fab [MAKER]: https://www.renesas.com/en/about/newsroom/renesas-commences-operations-kofu-factory-dedicated-300-mm-wafer-fab-power-semiconductors
- Front-end as of 2022: Naka, Takasaki, Saijo, Kawashiri (Japan), Palm Bay FL (ex-Intersil); back-end: Yonezawa, Oita, Nishiki (Japan), Beijing and Suzhou (China), Kuala Lumpur and Penang (Malaysia) – from a Wikipedia mirror, secondary, possibly stale: https://en.wikipedia.com/wiki/M32C (Renesas article mirror). UNVERIFIED for 2026.
- Feb 2026: expanded foundry partnership with GlobalFoundries (US, Germany, Singapore fabs) [INDEP press]: https://www.nippon.com/en/news/yjj2026021700453
- Criterion 4: RBA Regular member; KnowTheChain 2022 41st of 60, 11/100.

### ROHM

BoM: 0 semiconductor lines (one ROHM current-sense resistor on Okapi). Candidate second source for small-signal discretes and LDOs.

- Front-end mainly in Japan, back-end mainly overseas: seven manufacturing sites in Japan and six overseas, excluding SiC (May 2025 IR Q&A) [MAKER]: https://micro.rohm.com/en/financial/account/2503_41811104_QA_en ; domestic front-end sites include Miyazaki, Miyagi, Hirokawa and Yukuhashi (Fukuoka) and Kasaoka (Okayama) [MAKER]: https://fscdn.rohm.com/en/company/profile/corporate-profile-print-en.pdf . Overseas back-end includes Thailand and the Philippines (press): https://evertiq.com/news/54034
- Oct–Nov 2025: domestic manufacturing reorganized into a wafer-process company and an assembly company that also parents overseas back-end subsidiaries [MAKER]: https://fscdn.rohm.com/en/financial/ir-news-releases/20251106_news4-en.pdf
- March 2026: MoU between Toshiba, JIP, TBJ Holdings, ROHM and Mitsubishi Electric to begin discussing integration of Toshiba Electronic Devices & Storage's semiconductor business, ROHM's semiconductor business and Mitsubishi Electric's power devices; no terms decided [INDEP]: https://www.semiconductor-today.com/news_items/2026/mar/toshiba-rohm-mitsubishielectric-300326.shtml
- Criterion 4: not on the RBA list (fetched 2026-11-11); not in KnowTheChain.

### Toshiba Electronic Devices & Storage (TDSC)

BoM: 0 lines. Candidate second source for small-signal MOSFETs, Schottkys and logic.

- Kaga Toshiba Electronics (Ishikawa, Japan) is "the main discrete semiconductor production base"; a new 300 mm power fab there was completed May 2024 [MAKER]: https://toshiba.semicon-storage.com/eu/company/news/2024/05/corporate-20240523-1.html ; https://toshiba.semicon-storage.com/us/company/news/2023/04/corporate-20230424-1.html
- Back-end countries not found (UNVERIFIED).
- Ownership: Toshiba was taken private by a JIP-led consortium (TBJ Holdings) in Dec 2023 (from memory, UNVERIFIED in this session; TBJH appears as an MoU party above). The March 2026 integration talks with ROHM and Mitsubishi Electric are the live ownership event.
- Criterion 4: Toshiba Corp. is an RBA member (unmarked tier); not in KnowTheChain.


### Central Semiconductor

BoM: 2 lines, 3 placements – CMSH3-40MA (×2) and CMDSH2-3 Schottkys (Okapi). Both are generic packages with many second sources (UNVERIFIED per part).

- US company (Hauppauge NY); wafer probing in its own Class 1000 clean room, and "majority of Central's die inventory is held in the U.S. at Hauppauge" [MAKER]: https://www.centralsemi.com/bare-die . Where die are fabricated and packaged is not published (UNVERIFIED); US import records show Asian suppliers including Pan Jit (Wuxi, China) in 2019 (https://panjiva.com/Central-Semiconductor-Corp/1877588 – indicative only).
- Ownership: CB Insights reports acquisition "by AEM" in February 2023, terms undisclosed – UNVERIFIED, acquirer identity unclear: https://www.cbinsights.com/company/central-semiconductor
- Criterion 4: not on the RBA list; not benchmarked.

### Sensor makers on the BoM (brief; deeper survey may belong to the sensor agent)

- **Bosch Sensortec** (BME280 both boards, BMA456 Okapi): BME280 operating range −40 to +85 °C [MAKER]: https://www.bosch-sensortec.com/media/boschsensortec/downloads/datasheets/bst-bme280-ds002.pdf (pdftotext, "Operating temperature TA operational -40 25 +85 °C"). Single source, no pin-compatible second source (UNVERIFIED). Robert Bosch GmbH is an RBA member (unmarked tier). Bosch is a 10 % partner in ESMC Dresden (NXP 10-K).
- **Melexis** (MLX90393 Okapi): Belgian. See criterion 2 finding below – the fitted part is the −20 °C grade. Not on the RBA list.

### Cross-brand: workers' rights benchmarks (criterion 4)

**KnowTheChain ICT benchmark** (Business & Human Rights Resource Centre; forced-labor due diligence, scores out of 100) [INDEP]. 2025 edition: 45 companies, scorecards dated 20 March 2025 (PDF CreationDate), average 20/100. 2022 edition: 60 companies, published 10 Jan 2023, median 14/100. Scores below were extracted with `pdftotext` from the scorecard PDFs at `https://media.bhrrc.org/media/documents/2025_KTC_ICT_Scorecard_<Company>.pdf` and the 2022 PDFs named in each row.

| Company | 2025 rank / 45 | 2025 score | 2022 rank / 60 | 2022 score |
|---|---|---|---|---|
| NXP Semiconductors | 6 | 36 | 10 | 39 (https://media.bhrrc.org/media/documents/2022_ICT-NXP_KTC.pdf) |
| STMicroelectronics | joint 19 | 20 | not in 2022 list | – |
| Texas Instruments | 30 | 12 | 23 | 21 (https://media.bhrrc.org/media/documents/2022_ICT_Scorecard_Texas_Instruments_1.pdf) |
| Analog Devices | 31 | 11 | 33 (search snippet, UNVERIFIED) | not fetched |
| Microchip Technology | joint 31 | 11 | joint 28 (search snippet, UNVERIFIED) | not fetched |
| Infineon Technologies | joint 37 | 8 | 41 | 11 (https://media.bhrrc.org/media/documents/2022_ICT_Scorecard_Infineon_AG.pdf) |
| Renesas Electronics | 2025 scorecard not found at guessed URLs | – | 41 | 11 (https://media.bhrrc.org/media/documents/2022_ICT-Scorecard-Renesas_1.pdf) |
| onsemi, Rohm, Toshiba, Vishay, Diodes, Nexperia, FTDI, RAMXEED | not benchmarked (2025 URL guesses returned no PDF; none appear in the 2022 company list at https://www.business-humanrights.org/de/from-us/briefings/2022-knowthechain-ict-benchmark/) | – | – | – |

TI 2025 scorecard notes it adopted version 8 of the RBA Code since 2022; theme scores include Commitment & Governance 42, Traceability & Risk Assessment 10, Purchasing Practices 3, Monitoring 0 (pdftotext of the 2025 TI scorecard). Reading: these are disclosure scores for forced-labor due diligence, not audit findings; low scores mean little published, not proven abuse.


### Cross-brand: temperature grade of the parts actually on the BoMs (criterion 2)

Method: datasheets downloaded with curl and searched with `pdftotext | grep` for the operating-temperature line, 2026-11-11. "Suffix" means the range was read from the maker's part-number temperature code, not from a datasheet fetched this session.

**Two Okapi sensors are not rated to −40 °C** [MAKER datasheets]:
- **MLX90393SLW-ABA-011**: temperature code S = "from -20°C to 85°C"; the E code, MLX90393**E**LW-ABA-011, is "-40°C to 85°C" in the same package and I²C address (ordering table, MLX90393 datasheet): https://media.melexis.com/-/media/files/documents/datasheets/MLX90393-datasheet-melexis.pdf . Drop-in fix: order the E grade.
- **VEML6030**: operating range −25 to +85 °C (Vishay datasheet, absolute maximum table; Digi-Key lists −25 to 85 °C): https://www.vishay.com/docs/84366/veml6030.pdf . No −40 °C grade of this part was found.

**One Okapi charger is −40 °C only "by design"**: LT3652**E**DD "is guaranteed to meet performance specifications from 0°C to 125°C junction temperature. Specifications over the –40°C to 125°C operating junction temperature range are assured by design, characterization, and correlation with statistical process controls. The LT3652**I**DD specifications are guaranteed over the full –40°C to 125°C" (Note 2, LT3652 datasheet Rev E): https://www.analog.com/media/en/technical-documentation/data-sheets/3652fe.pdf . The I grade is the tested −40 °C part. The LTC4412**E**S6 very probably carries the same E-grade note (Linear convention) but its datasheet could not be downloaded this session (UNVERIFIED).

**Everything else checked reaches −40 °C or lower** [MAKER datasheets, ti.com/lit/ds/symlink/<part>.pdf]:
- TI, −40 to 85 °C ambient: SN74AUP3G34, SN74LVC1G3157, SN74AUP1G04, TCA9406, TXS0102, TXS0104E, TPS2104/TPS2105, TPS22916, TLV61220, TPS61032, BQ2980 (characterized −40 to 85). TPS797: junction −40 to 85 °C.
- TI, −40 to 105 °C: TPL5010, TPL5111. TI, −40 to 125 °C: TLV3691, ADS1115, SN74AHC1G86, SN74AUP2G08; TPS7A05 and TPS62822 junction −40 to 125 °C. TPS22917 "–40°C to" (upper limit not captured).
- DS3231M: −45 to +85 °C (workspace copy of datasheet 19-5312, `NW-Status/studies/okapi-hardware-audit/sources/2026-11-10-ds3231m-datasheet-19-5312.pdf`).
- ATmega1284P: electrical characteristics given for −40 to 85 °C and −40 to 105 °C (Microchip DS40002070B). FT231X: −40 to 85 °C (FTDI product page, https://www.ftdichip.com/old2020/Products/ICs/FT231X.html, via search).
- Suffix only (UNVERIFIED by datasheet this session): Microchip "-E/" parts (MCP3421, MCP4726, MCP23018) −40 to 125 °C; PAC1934T-I −40 to 85 °C; MIC2544-1**Y**MM, MIC94090/94094 **Y** −40 to 85 °C; MAX6070**A/B**AUT −40 to 125 °C; MB85RC512T −40 to 85 °C; PCA9634 −40 to 85 °C; BMA456 −40 to 85 °C; discretes (Diodes, onsemi, Central) junction −55 or −65 to 150 °C.

**AEC-Q100/Q101 grades.** Not checked part by part at Digi-Key this session (Digi-Key pages not fetched). Many of the TI parts have -Q1 variants and the Diodes "-7-F" discretes have "Q" automotive variants (from memory, UNVERIFIED). Note that AEC-Q grading certifies a qualification test flow (temperature cycling, HTOL, etc.); for a −40 °C deployment the industrial "I"/"E" range already covers the temperature, and Q-grade is a reliability-process premium, not a temperature necessity.

**Published FIT/MTBF data.** TI offers a per-part MTBF/FIT estimator (generic by technology group; typically 60 % confidence, 0.7 eV) [MAKER]: https://www.ti.com/quality/docs/estimator.tsp . Coverage is incomplete per TI E2E threads. ADI, Microchip and the others were not checked this session (open question).

### Cross-brand: consistency, longevity, counterfeits (criterion 3)

- **Longevity programs [MAKER]:** NXP Product Longevity, minimum 10 or 15 years from launch per listed product, not auto-discontinued at the end: https://nxp.com/ProductLongevity . ST longevity program with 7/10/15/20-year tiers and a public part list; SPC58 automotive MCUs extended to 20 years: https://www.eejournal.com/industry_news/stmicroelectronics-sets-20-year-availability-for-popular-automotive-microcontrollers/ . Microchip "Client-Driven Obsolescence": products with active demand "will remain available, subject to manufacturability"; "EOL occurrences are rare": https://www.microchip.com/en-us/about/corporate-overview/product-longevity ; https://microchip.com/en-us/support/quality/end-of-life-eol-policy . TI: no formal longevity program found; discontinuance is by Product Discontinuance Notice, typically about 12 months to last order and 6 more to last ship (e.g. PDN with last order 10 Feb 2027, last ship 10 Aug 2027, via third-party-hosted copies; search summary).
- **TI fab consolidation [INDEP press + MAKER PCN]:** TI is closing its last 150 mm fabs (Sherman SFAB; Dallas DFAB keeps 200 mm and GaN); SFAB closure activities "expected to begin by the end of 2025" (PCN20250416002.1, Mouser-hosted: https://www.mouser.com/PCN/Texas_Instruments_PCN20250416002.1_Change_Notification.pdf). A Farnell-hosted TI notice says TI will no longer support certain tube, small-reel and "temp variants" of 150 mm devices (https://www.farnell.com/datasheets/4001168.pdf, search summary). Reading: TI parts on the BoM may see fab-transfer PCNs and drops of odd packing options; check each BoM part's PCN history.
- **Errata culture, one dated example [MAKER]:** the DS3231M Rev A1 errata sheet (19-5311, Rev 0, June 2010) lists four deviations, including the BBSQW behavior, and says Maxim "intends to correct these errata when the opportunity to redesign the product presents itself"; no later die revision was found in this session (workspace copy, `NW-Status/studies/okapi-hardware-audit/sources/2026-11-10-ds3231m-a1-errata-19-5311.pdf`). Published errata are good practice; a 16-year-old uncorrected errata is the norm for a mature analog part, not a red flag on its own.
- **Counterfeit exposure [INDEP]:** ERAI logged 748 reported parts in 2025, down 29.1 % from 2024; Xilinx "ranked as the most targeted brand"; ERAI notes counterfeiters "continue to target parts that are readily available through authorized distribution channels" (meaning such parts are copied for the gray market, not that authorized stock is counterfeit): https://www.erai.com/erai_blog/3192/2025_annual_report . In the 2022 data TI was "the brand most targeted by counterfeiters (9% of all parts reported)": https://www.erai.com/erai_blog/3183/2023_annual_report (search summary). Reading: counterfeit risk tracks popularity and is controlled by buying only from an authorized distributor such as Digi-Key; it does not distinguish the brands for Northern Widget.
- **Nexperia supply after the split [INDEP, distributor/broker blogs – weak]:** Jan 2026: some customers told new Nexperia material may not come until July 2026 or later for legacy devices; Apr 2026: spot shortages "elevated ... but still manageable": https://thecomponentclub.com/news/2026-01-27-nexperia-supply-chain-conditions-shift-going-into-2026 ; https://smithweb.com/general/nexperia-shortages-update-april-23-2026/
- **Independent quality-escape evidence:** none found for any brand in this session beyond the above. This is a gap, not a clean bill of health.

### Cross-brand: conflict minerals (criterion 4)

All US-listed makers here file SEC Form SD (conflict minerals). Latest Form SD filing dates on EDGAR, checked 2026-11-11: TI 2026-06-01; ADI 2026-05-22; Microchip 2026-05-28; onsemi 2026-05-18; Diodes 2026-05-28; Vishay 2026-05-28; NXP 2026-05-28; ST 2026-05-12 (https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&type=SD&CIK=<cik>). Contents not read. FTDI, RAMXEED, Rohm, Toshiba, Renesas, Infineon, Central, Melexis do not file with the SEC; their conflict-minerals reporting was not checked.

### Workers' rights evidence not found

Electronics Watch findings, Corporate Human Rights Benchmark scores and RBA audit (VAP) status by company were not retrieved this session. RBA membership tier is not audit status.

## 3. Summary table

One finding per cell, with evidence strength: **[F]** regulatory filing or maker document fetched this session; **[I]** independent source fetched; **[S]** secondary or search summary only; **[U]** UNVERIFIED. BoM lines are combined Margay + Okapi semiconductor lines.

| Brand (BoM lines) | 1. Geopolitical resilience | 2. Wide-temperature quality | 3. Consistent quality | 4. Workers' rights |
|---|---|---|---|---|
| Texas Instruments (26) | US-owned; majority of wafers and A/T internal, own 300 mm fabs in TX and UT; back-end mostly Malaysia, Philippines, China [F] | Every BoM TI part checked is rated −40 °C or lower; per-part FIT estimator published [F] | No formal longevity program; 150 mm fab closures bring PCNs and option drops; most-counterfeited brand in 2022 ERAI data [S] | RBA Regular; KnowTheChain 2025 30/45, 12/100 [I] |
| Microchip (10) | US-owned; ~65 % of sales from outside foundries; own back-end in Thailand and Philippines [F] | BoM parts in I or E grades, −40 °C; suffix-based only [U] | Client-Driven Obsolescence, EOL "rare" [F, maker claim] | RBA Full; KnowTheChain 2025 joint 31/45, 11/100 [I] |
| Diodes Inc (7) | US-owned, but "majority of our manufacturing facilities are located in China"; fabs also UK, Taiwan, Maine [F] | Discretes, −55 °C class junction; IATF 16949 [F/U] | Generic parts with many second sources; no escape found [U] | Not RBA; not benchmarked [I] |
| Analog Devices (5) | US-owned; more than half of wafers from foundries, TSMC named; Penang back-end held for sale [F] | LT3652**E** is tested 0–125 °C only, −40 °C "by design"; the I grade is tested; DS3231M −45 °C [F] | DS3231M errata (2010) never corrected; LT3652, LTC4412, DS3231M single-source [F/U] | RBA Regular; KnowTheChain 2025 31/45, 11/100 [I] |
| FTDI (2) | Fabless, Glasgow; UK ordered China-registered owner to sell 80.2 % stake (Nov 2024), court challenge lost (Jul 2025); no sale found yet [I] | FT231X −40 to 85 °C [S] | Single source on both boards; no pin-compatible alternative [U] | Not RBA; not benchmarked |
| onsemi (2) | US-owned; front-end US, Czechia, Japan, Korea, Malaysia; back-end China, SE Asia, Vietnam, Canada [F] | Discretes, −55 °C class [U] | No evidence either way found [U] | RBA Full; not in KnowTheChain |
| Central Semi (2) | US, private; die and assembly locations unpublished; ownership change Feb 2023 reported [S/U] | Discretes [U] | Thin evidence [U] | Not RBA; not benchmarked |
| NXP (1) | Dutch; own fabs NL, US, Singapore (JV with TSMC); own back-end Taiwan, Thailand, Malaysia, China [F] | PCA9634 −40 °C [U] | Product Longevity 10/15 yr [F, maker claim] | RBA Full; KnowTheChain 2025 6/45, 36/100, best here [I] |
| RAMXEED (1) | Fujitsu spin-off (2020), renamed Jan 2025; current owner and wafer source unknown [F/U] | MB85RC512T −40 to 85 °C [U]; 125 °C automotive FeRAM exists [F] | Single source on Okapi; Infineon FM24 compatibility unchecked [U] | Not RBA (Fujitsu is) |
| Vishay (1) | US-owned; opto in Melaka, MOSFETs Taiwan and Newport UK, diodes China and Europe [F] | VEML6030 rated only −25 °C [F] | No evidence found [U] | RBA Regular; not benchmarked |
| Melexis (1) | Belgian; not researched in depth [U] | Fitted MLX90393**S** is −20 °C; the E grade is −40 °C, same package [F] | – | Not RBA |
| Bosch (3) | German; not researched in depth [U] | BME280 −40 to 85 °C [F] | Single source [U] | Bosch GmbH RBA member |
| Nexperia (0) | Wingtech (China)-owned; Dutch order Sep 2025, suspended Nov 2025; split into Dutch and China halves since; ~70 % of output was Dongguan [I] | – | Shortages through 2026 for legacy discretes [S] | RBA member (tier unmarked) |
| STMicroelectronics (0) | 27.5 % held by French and Italian states; fabs in Italy, France, Singapore; 25 % foundry; back-end EU, Malta, Morocco, Malaysia, Philippines, China [F] | – | Longevity program 7–20 yr, public list [S] | RBA Full; KnowTheChain 2025 joint 19/45, 20/100 [I] |
| Infineon (0) | German; new Bangkok back-end (Oct 2026); full site list not fetched [S/U] | – | – | RBA Regular; KnowTheChain 2025 joint 37/45, 8/100 [I] |
| Renesas (0) | Japanese; Kofu 300 mm reopened 2024; GlobalFoundries deal Feb 2026; site list stale [S] | – | – | RBA Regular; KnowTheChain 2022 41/60, 11/100 [I] |
| ROHM (0) | Japanese; front-end in Japan, back-end overseas (Thailand, Philippines); integration talks with Toshiba and Mitsubishi (Mar 2026) [F/I] | – | – | Not RBA; not benchmarked |
| Toshiba (0) | Japanese, private (JIP-led); main discrete fab Kaga, Japan (300 mm, 2024); same integration talks [F/I] | – | – | Toshiba Corp RBA member |
| Particle (SoM) | B404X uses u-blox (Swiss, Advent-owned since Nov 2025); B524/B523 use Quectel (China, own Changzhou factory; on DoD 1260H list per secondary source) [F/S] | Modems −20 °C normal, −40 °C extended with RF caveat [F] | – | – |

## 4. Open questions

1. Which Particle SKU does Okapi ship with? If B524/B523 (Quectel), check the current FCC and DoD status of Chinese cellular modules against the Federal Register before choosing.
2. Replace MLX90393SLW with MLX90393ELW (−40 °C, same footprint)? This is a BoM change for Andy to decide.
3. VEML6030 is rated to −25 °C only: is a −40 °C ambient-light sensor needed, or is the part acceptable out of spec in winter?
4. LT3652EDD → LT3652IDD (tested at −40 °C), and check whether LTC4412ES6 has an I grade. Price and Digi-Key stock not checked.
5. FTDI: no named buyer under the divestment order yet; is a second USB–UART footprint (e.g. CP2102N) worth carrying on a future board revision?
6. RAMXEED: current ownership and wafer fab are unknown; ask RAMXEED or a Digi-Key FAE. Check Infineon FM24V05 pin and protocol compatibility with MB85RC512T.
7. Country of origin per Digi-Key reel for the Diodes, onsemi and Nexperia discretes (Digi-Key lists a COO field; not fetched this session).
8. AEC-Q100/Q101 variants at Digi-Key for each BoM line, with stock and price.
9. FIT data from ADI, Microchip, Diodes and RAMXEED for the BoM parts.
10. Infineon full site list; Renesas current site list; Toshiba back-end countries.
11. KnowTheChain 2022 scorecards for ADI and Microchip (ranks from search snippets only); RBA audit (VAP) status; Electronics Watch and CHRB, which were not searched.
12. ADI's acquisition dates for Maxim and Linear, Microchip's for Atmel and Micrel, and Toshiba's take-private date were stated from memory.

## Sources checked
- ti.com manufacturing page – fetched, used.
- TI FY2025 10-K on sec.gov – fetched (two parts), used; site types not classified.
- Web search "Texas Instruments manufacturing locations ..." – secondary press only.
- Nexperia: web searches on Dutch intervention, 2026 status, sites, Newport sale, Entity List, Affiliates Rule – used; Yicai 2026-09-23 fetched; nexperia.com manufacturing page not fetched directly (search summary only).
- KnowTheChain 2022 and 2025 scorecards – downloaded (curl) and parsed with pdftotext; 2025 URL guesses for Renesas, onsemi, ON_Semiconductor, Rohm, Toshiba, Vishay, TE returned non-PDF (dead ends).
- RBA members page https://www.responsiblebusiness.org/about/members/ – fetched and grepped 2026-11-11. "F"/"R" mark Full/Regular; unmarked names are Affiliate or Supporter (page does not distinguish). Not listed: Diodes, Rohm, RAMXEED, FTDI, Melexis, Central Semiconductor, Particle, u-blox, Quectel.
- ADI FY2025 10-K (sec.gov) – fetched with curl, used.
- Microchip FY2026 10-K (sec.gov) – fetched with curl, used.
- Diodes FY2025 10-K, onsemi FY2025 10-K, Vishay FY2025 10-K, NXP FY2025 10-K, ST 2025 20-F – all fetched from sec.gov with curl and grepped; used.
- FTDI: evertiq 2024-11-07 fetched; GOV.UK final-order variation page (search result only, not fetched); ftdichip contact page (search result only). Current owner after divestment: dead end.
- RAMXEED: ramxeed.com/company fetched (no ownership data); ownership after 2021 and wafer source: dead ends.
- Particle datasheets (B404X, B524/B523) fetched; SoM assembly location: dead end. u-blox manufacturing country: dead end. Quectel factory page via search; 1260H listing from a secondary blog only.
- Infineon full site list: dead end this session (search returned only the Bangkok opening).
- Renesas, ROHM, Toshiba: searches only; ROHM and Toshiba primary pages via search summaries.
- Datasheets downloaded and grepped: 22 TI parts (ti.com/lit/ds/symlink), MLX90393, LT3652, BME280, ATmega1284P family. Download failures (dead ends): DS3231M, LTC4412, MAX6070 from analog.com (curl refused); FT231X, PCA9634, MB85RC512T (HTML returned instead of PDF).
- Longevity: NXP, ST, Microchip pages via search summaries; TI PDN copies via search summaries; PDN20240404000 addendum fetch timed out (dead end).
- ERAI 2025 annual report fetched (brand chart is an image; only Xilinx named).
- SEC Form SD filing dates via EDGAR browse, curl.
- Central Semiconductor: search only.
- Not attempted: Electronics Watch, CHRB, RBA audit status, Digi-Key AEC-Q availability per part.

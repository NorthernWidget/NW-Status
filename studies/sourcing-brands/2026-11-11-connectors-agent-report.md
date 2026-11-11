Status: COMPLETE

# Brand survey: connectors, electromechanical parts, crystals and oscillators, battery holders, enclosures (2026-11-11)

Agent report, one of four. Criteria, in Andy's order: (1) geopolitical resilience, (2) wide-temperature quality, (3) consistent quality, (4) workers' rights. Makers' own claims are labeled **[maker]**; independent evidence **[independent]**; anything not confirmed is UNVERIFIED. Facts are appended as confirmed.

## BoM dependence (verified from files, 2026-11-11)

Sources: `Project-Margay/Production/Margay_BoM_3v0_-_2026-11-04.csv` (column MF); `Project-Okapi/Hardware/Okapi_2024-11-02.zip` member `CAMOutputs/Assembly/Okapi.txt` (column MF), read with `unzip -p`. One BoM line = one MPN row. In scope: connectors, switches, battery holders, crystals. Out of scope but noted: Würth inductors, LEDs and capacitor on Okapi; TE resistor CRGCQ0402F220R on Okapi.

| Brand (as written in MF) | Margay lines | Okapi lines | Parts |
|---|---|---|---|
| On Shore Technology ("On Shore"/"OnShore") | 2 | 4 | Margay J2 OSTVN10A150, J3 OSTVN06A150; Okapi J5–J7 OSTVN02A150, J2 OSTVN10A150, J3 OSTVN04A150, J1/J4 OSTVN08A150 |
| GCT | 1 | 1 | USB4105-GF-A (USB-C) |
| Amphenol (FCI) | 1 | 1 | 67997-206HLF (2x3 ISP header) |
| Linx (now TE) | 1 | 1 | BAT-HLD-012-SMT (coin-cell holder) |
| C&K | 1 | 2 | PTS810 SJG 250 SMTR LFS (tact switch, both); Okapi also PCM12SMTR (slide switch) |
| ECS | 1 | 0 | ECS-80-18-30-JGN-TR (8 MHz crystal) |
| TXC | 0 | 1 | 7A-8.000MAAE-T (8 MHz crystal) |
| Würth Elektronik | 1 | 0 | 693063010911 (SD holder) |
| Molex | 0 | 2 | 5025700893 (microSD holder), 1051330001 (micro-USB) |
| TE Connectivity | 0 | 1 | 2199230-4 (M.2 socket for Particle B-SoM) |
| JST | 0 | 1 | S2B-PH-SM4-TB(LF)(SN) (PH battery connector) |
| Panasonic (electromechanical) | 0 | 1 | EVP-BB2A9B000 (tact switch) |
| PolyCase | – | – | WH-16-03 enclosure for Okapi (not on the assembly BoM; named in the brief) |

Totals in scope: Margay 8 lines, Okapi 15 lines. On Shore terminal blocks are the largest single dependence (6 lines, every field-wiring terminal on both boards). Margay's On Shore count was rechecked with `grep -ic shore` (2).

## Cross-brand facts

### RBA membership (fetched 2026-11-11)

Source: RBA member list, https://www.responsiblebusiness.org/about/members/ (fetched 2026-11-11). The page suffixes members "- F" or "- R"; unsuffixed names are listed without a tier. The meaning of the tiers (Full, Regular, and unsuffixed presumably Affiliate) is from the RBA's membership structure as I understand it: UNVERIFIED on this page.
- Listed: **Amphenol Corporation** (no suffix), **Molex - R**, **TE Connectivity** (no suffix), **Murata Manufacturing - R**, **Seiko Epson Corporation - R**, **Panasonic Holdings** (no suffix), **KYOCERA Corporation** and **KYOCERA AVX Components** (no suffix), **3M Electronics and Energy Business Group**, Bourns, Vishay - R, TDK Group, Foxconn - R.
- Not listed: JST, Hirose, Phoenix Contact, Würth Elektronik, Samtec, Harwin, Keystone, SiTime, Abracon, ECS, TXC, C&K, Littelfuse, Bel Fuse, Japan Aviation Electronics (JAE), Luxshare, Yageo/KEMET. (Name checks run by WebFetch on the page; absence from a list is not evidence of poor practice.)
- [independent] Murata became an RBA participant in June 2022 (Murata CSR page, https://corporate.murata.com/en-us/csr/people/suppliers, via search snippet; the RBA listing above confirms current membership).

### KnowTheChain ICT benchmark 2025 (read 2026-11-11)

[independent] KnowTheChain (Business & Human Rights Resource Centre) 2025 ICT benchmark, published 2 April 2025, 45 companies; top three Samsung 61, HPE 53, Cisco 51 (https://www.business-humanrights.org/en/from-us/briefings/2025-knowthechain-ict-benchmark/). Scorecards read as PDFs from `https://media.bhrrc.org/media/documents/2025_KTC_ICT_Scorecard_<Company>.pdf` (pdftotext, 2026-11-11):

| Company | 2025 score /100 | 2025 rank /45 | 2022 rank /60 | Notes from scorecard |
|---|---|---|---|---|
| Amphenol | 8 | 37 | 35 | Commitment & Governance 17 (industry avg 52); Purchasing, Enabling Workers' Rights, Monitoring, Remedy all 0; no-fee policy yes (Employer Pays); risk assessment yes; remedy for supply-chain workers no |
| Murata | 10 | 34 | 33 | Commitment & Governance 46; Traceability 0; Purchasing 0; Remedy 0; first-tier supplier list no; risk assessment no |
| Panasonic | 10 | 34 | 45 | (theme scores not transcribed) |
| Kyocera | 6 | 41 | 55 | (theme scores not transcribed) |

- Not in the 2025 benchmark: TE Connectivity, Seiko Epson, Molex (Koch Industries, private), Hirose, JAE, Würth, and every smaller brand in this scope. The TE and Seiko Epson URLs return XML errors (not found).
- TE Connectivity: a 2018 KTC scorecard ranking it 28 of 40 appears in search results only (UNVERIFIED; not read).
- Context: the 2025 average was 20/100 (search summary of the briefing). Every connector or crystal maker that was scored sits well below the ICT average.

## Brand sections

### On Shore Technology (OST) – 6 BoM lines (all field-wiring terminal blocks)

- [maker] Founded 1988, headquarters Tempe, Arizona; "leading international supplier of interconnect products"; sales reps in the U.S., Canada, Mexico and Asia (https://www.on-shore.com/company/, fetched 2026-11-11). The site names **no factory, no country of manufacture, no owner beyond the company itself, and no ISO 9001 certificate** (company, documentation and FAQ pages read 2026-11-11).
- [maker] FAQ: "Standard lead time for non-stock items is 4-6 weeks but can be affected by conditions such as weather, material shortages, customs, and other"; "OST manufactures many of our products to be compatible with other manufacturers such that our male plug terminal blocks would easily fit and mate to other manufacturers PCB female headers" (https://www.on-shore.com/faq-page/, 2026-11-11). The reference to customs is consistent with imported manufacture; country of origin UNVERIFIED.
- [maker] Conflict minerals: a one-page undated "Conflict Minerals Commitment" letter (scanned image, read by OCR), "we are working with our suppliers to confirm to the extent possible that any metals used in our manufacturing process does not contain minerals sourced from the conflict region", signed by the quality/manufacturing head, Tempe address (http://on-shore.com/wp-content/uploads/2015/09/conflictminerals.pdf, upload path dated 2015-09). No CMRT, no smelter list, no RMI membership stated.
- [maker] OSTVNxxA150 drawing (https://www.on-shore.com/wp-content/uploads/OSTVNXXA150.pdf, read by OCR 2026-11-11, so digits may be misread): 2.54 mm pitch rising-clamp screw terminal; 150 V / 6 A; AWG 30–18; withstand AC 1300 V/min; insulation resistance ≥1000 MΩ at DC 500 V; M1.6 screw, 0.15 N·m torque; **temperature range −40 °C to 115 °C**; RoHS. No housing material, plating or contact-resistance figure was legible in the OCR text.
- [independent observation] The drawing carries the boilerplate "Transfer or duplication of this document ... utility model or design patent registrations", which is the standard legend on drawings from Taiwanese and Chinese terminal-block OEMs. That OST buys from such an OEM is an inference: UNVERIFIED.
- Not in RBA (list above); no KTC, CHRB or Electronics Watch record found.
- Evidence strength: thin on every criterion except the temperature rating. OST is the largest in-scope dependence on both boards and also the least documented.

#### OST second sources (Digi-Key, fetched 2026-11-11)

- Digi-Key OSTVN10A150 page (https://www.digikey.com/en/products/detail/on-shore-technology-inc/OSTVN10A150/1588872): 2,599 in stock, Active; **operating temperature −30 °C to 105 °C** (this contradicts the −40 to 115 °C on OST's own drawing read by OCR; which is correct is UNVERIFIED); contact brass; housing "Thermoplastic"; no country of origin, ECCN or HTSUS shown.
- Digi-Key "Parametric Equivalent" substitutes: **Amphenol Anytek VN12A1500000G** (0 stock) and **GCT TBC05-12-1-G-G** (0 stock). Similar products: Phoenix Contact 1729225, Molex 0430450402, Chip Quik SBBTH1508-1.
- [independent observation] The Anytek series name "VN..A150" mirrors OST's "OSTVN..A150", which suggests Anytek (Taipei, Taiwan) as the original maker of OST's VN series. UNVERIFIED: no document links them.
- [independent, search summary] FCI signed to buy a majority stake in Anytek Technology Corp. (Taipei, founded 1952, terminal blocks) on 20 May 2011 (search result summary via IBS Electronics pages; primary press release not read: UNVERIFIED). Amphenol later acquired FCI (see Amphenol section), which is why Anytek trades as "Amphenol Anytek".
- Land-pattern compatibility of a substitute (pitch 2.54, pin row, rising clamp) must be checked against the drawing for each; not done here.

### Amphenol (including FCI and Anytek) – 2 BoM lines (67997-206HLF ISP header, both boards)

- [maker, SEC filing] Amphenol 10-K for fiscal 2025, filed 2026-02-11 (https://www.boardroomalpha.com/sec/aph-10-k-2026-02-11-0001104659-26-013549, Item 1 and 1A, first 100,000 characters read): manufacturing "facilities in approximately 40 countries"; about 170,000 employees, about 15,000 in the U.S. (about 90 % outside the U.S.); China about 16 % of 2025 net sales; **about 37 % of long-lived assets in China, up from 29 % in 2024**, attributed mainly to AI-related investment; tariffs "in certain cases, increased our costs of doing business"; some products subject to export controls.
- Interpretation (hypothesis, not measured): a 40-country footprint gives Amphenol room to move a commodity header between plants, but its China asset share is rising, not falling. Which plant makes 67997-206HLF is UNVERIFIED.
- Workers' rights [independent]: KTC 2025 ICT score 8/100, rank 37 of 45 (scorecard read, see cross-brand section). RBA: listed, no tier suffix.
- 67997-206HLF quality data: not yet read (see below).

- Ownership chain [maker, SEC filing]: Amphenol completed its purchase of FCI Asia Pte Ltd on **8 January 2016**, through Amphenol East Asia Limited, from Fidji Luxembourg (BC4) Sàrl (Amphenol 8-K and Exhibit 99.1, https://www.sec.gov/Archives/edgar/data/0000820313/000110465916088826/a16-1544_18k.htm, via search summary). Amphenol called it "the largest acquisition in the Company's history" (Q4 2015 results, 20 January 2016, https://s21.q4cdn.com/564806605/files/doc_financials/2015/q4/2015_APH_Fourth_Quarter_Results.pdf, via search summary). Ten years settled; no ownership event since found for FCI/Anytek.

### C&K (switches) – 3 BoM lines (PTS810 tact switch on both boards; PCM12SMTR slide switch on Okapi)

- [maker, SEC filing] **Littelfuse completed the acquisition of C&K Switches on 19 July 2022 for $540 million in cash**; C&K had annualized sales over $200 million; its assets sit in the Americas, Europe and Asia-Pacific regions (Littelfuse 10-Q, https://www.sec.gov/Archives/edgar/data/889331/000088933122000046/lfus-20221001.htm, via search summary; Business Wire release https://www.businesswire.com/news/home/20220719005972/en).
- [maker, via search summary] Plants: **Dole, France** ("vertically integrated, highly automated", about 183,000 ft²) and **Huizhou, China** ("vertically-integrated and semi-automated", about 463,000 ft², from C&K's 2011 acquisition of Gaoming Industrial) (https://www.ckswitches.com/about/ and a company profile, via search summary, 2026-11-11). ckswitches.com/about-us/ now redirects (HTTP 301) to https://www.littelfuse.com/company, so the C&K brand pages are being folded into Littelfuse (fetched 2026-11-11).
- Interpretation (hypothesis): one EU plant and one China plant; which makes PTS810 is not stated. Two of C&K's three BoM lines are fine on temperature (PTS810 −40 °C); the third (PCM12SMTR) is obsolete (see part-level facts).
- Workers' rights: neither C&K nor Littelfuse is on the RBA list or in KTC 2025.

### Linx (now TE) – 2 BoM lines (BAT-HLD-012-SMT coin-cell holder, both boards)

- [maker] TE announced its acquisition of Linx Technologies on 19 July 2022; the deal closed **1 July 2022** (https://www.te.com/en/about-te/news-center/acquires-linx-technologies.html, via search summary). Linx's battery holders now sell under TE ("Linx Technologies, Now Part of TE Connectivity", https://www.te.com/en/products/brands/linx-technologies.html). The brief's "Linx/TE" is correct; the date is 2022, not 2021.

### Same Sky (formerly CUI Devices) – 0 BoM lines

- [maker] Rename announced in early September 2024 (Same Sky release dated 2024-09-05, https://sameskydevices.com/news/press-releases/cui-devices-has-a-new-name-say-hello-to-same-sky; Digi-Key blog https://www.digikey.ca/en/blog/cui-devices-has-a-new-name-same-sky: "The company and its products are the same ... model numbers, pricing, supply chain, business processes, quality, and customer support ... will remain the same"). A rename, not a sale. Owners not named in any source found: UNVERIFIED.

### TE Connectivity – 1 BoM line (2199230-4 M.2 socket, Okapi) plus 2 via Linx; also the obsolete TE 2041021-4 SD holder of Margay v2.2/v2.3

- [maker, SEC filing] TE 10-K for fiscal year ended 26 September 2025 (https://www.stocktitan.net/sec-filings/TEL/10-k-te-connectivity-plc-files-annual-report-a96d82bb44b6.html, read in two parts 2026-11-11): "We manufacture our products in over 25 countries worldwide"; **105 manufacturing facilities: Asia–Pacific 26, EMEA 38, Americas 41**; "We have sizeable operations in China, including 19 principal manufacturing sites"; about 25 % of fiscal 2025 net sales to customers in China; tariffs and U.S.–China trade tension listed as risks; export licenses needed for a small portion of products (defense-related).
- [maker] Ownership event: redomiciled from Switzerland to Ireland, completed **30 September 2024** (TE fiscal 2025 annual report, via search summary of https://s1.q4cdn.com/769663331/files/doc_financials/2025/ar/te-connectivity-annual-report-2025.pdf; the PDF itself returned an HTML block page to curl). A legal-domicile change, not a change of control.
- Interpretation (hypothesis): TE's footprint is the most Americas- and Europe-weighted of the large connector makers surveyed (79 of 105 plants outside Asia–Pacific), though which plant makes a given commodity part is not published per part.
- Workers' rights: RBA listed (no tier suffix). Not in KTC 2025. A 2018 KTC scorecard (rank 28 of 40) appears in search results only: UNVERIFIED.
- Consistency evidence: the TE 2041021-4 SD holder Margay used in v2.2/v2.3 went Obsolete at Digi-Key, with the Würth 693063010911 as Digi-Key's suggested substitute (prior survey, `../okapi-hardware-audit/sources/2026-11-11-margay-sd-holder-agent-report.md`, F4). That is one end-of-life on Northern Widget's own BoM history; the PCN date was not found.

### Molex – 2 BoM lines (Okapi: 5025700893 microSD holder, 1051330001 micro-USB)

- [independent] Owned by **Koch Industries (private) since 2013** (search summary citing Connector Supplier, https://connectorsupplier.com/an-eventful-decade-of-change-and-growth-for-molex/). Private ownership means no SEC plant table.
- [maker] Footprint: "74 plants located in 19 countries" and 42,000 employees per a Bishop Report profile republished by Molex (https://www.molex.com/en-us/news/bishop-report-profiles-molex-innovator-in-electronics, via search summary; date of the profile UNVERIFIED). Expansions: a second Vietnam plant at Hung Yen (https://www.molex.com/en-us/news/molex-opens-expanded-vietnam-manufacturing-plant), a $110 million campus at Katowice, Poland, 2023, and a second Guadalajara, Mexico, factory in 2022 (search summaries; dates as reported there).
- Workers' rights: RBA "Molex - R" (listed with a tier). Not in KTC 2025 (Koch is private).

### JST (J.S.T. Mfg. Co.) – 1 BoM line (Okapi J8 S2B-PH-SM4-TB battery connector)

- [independent, thin] Osaka headquarters; founding plant Kurayoshi, Japan; Malaysia has four plants in the Port of Tanjung Pelepas Free Trade Zone, Johor (third-party directory listings via search, https://craft.co/j-s-t-connectors-malaysia; UNVERIFIED against JST's own pages). JST is privately held and publishes no plant list that I found. China and Vietnam plants: UNVERIFIED.
- JST PH is the most-cloned 2.0 mm battery connector; drop-in clones exist from many Chinese makers, but mating quality across brands is not guaranteed (no source checked: UNVERIFIED).
- Workers' rights: not in RBA, not in KTC.

### Hirose Electric – 0 BoM lines (competes for SD/microSD holders and board-to-board)

- [maker] "8 Hirose factories (Korea, Indonesia, Malaysia, two in China and three in Japan) plus subcontractors" (https://www.hirose.com/corporate/en/about/dev_pro/, via search summary; page date UNVERIFIED). A new factory in Chennai, India, about ¥1 billion initial investment, partial production from summer 2027 (https://www.hirose.com/corporate/en/additional/pressreleases/202603-india-manufacturing-site/, March 2026, via search summary).
- [maker, risk disclosure] Hirose states some products can be produced only at specific sites, which makes alternative production hard if one region stops (search summary of Hirose risk disclosures, envalith.com; UNVERIFIED wording).
- Workers' rights: not in RBA, not in KTC.

### ECS Inc. International – 1 BoM line (Margay ECS-80-18-30-JGN-TR); also Okapi's KiCad replacement crystal

- [maker] "Founded in 1980, ECS Inc. is headquartered in Lenexa, Kansas, USA"; "a global engineering and sales support system of more than 18 locations in South Korea, Japan, China, Singapore and the United States"; "The global supply chain network ... allows ECS Inc. to remain as one of the primary providers"; leadership now under Eric Slatten with a new logo (https://ecsxtal.com/about-ecs-inc-international/, fetched 2026-11-11). **No factory is named.** Ownership: private; owners not stated. A third-party directory claims manufacturing in the U.S., China, Taiwan and Singapore (search summary, ensun.io): UNVERIFIED.
- [maker] Conflict-minerals policy: commits to due diligence on 3TG (and cobalt), requires suppliers to source "only from conflict free sources", cites Dodd-Frank §1502; no CMRT or smelter list on the page (https://ecsxtal.com/about-ecs-inc-international/conflict-minerals-policy/, 2026-11-11).
- [maker] Counterfeit policy: "counterfeit frequency control devices ... resemble ECS markings"; buy from ECS or authorized distributors; non-conforming parts destroyed (https://ecsxtal.com/about-ecs-inc-international/counterfeit-prevention-policy/). Digi-Key is an authorized ECS distributor (ECS distributor list not read: UNVERIFIED, though Digi-Key stocks ECS as a franchised line).
- ECS publishes a "Change Notices" page (site menu, 2026-11-11); its content was not read.
- Part [Digi-Key, https://www.digikey.com/en/products/result?keywords=ECS-80-18-30-JGN-TR, 2026-11-11]: ECX-53 series, 5.0 × 3.2 mm, **−40 °C to 85 °C**, ±20 ppm tolerance, ±30 ppm stability, 18 pF, ESR 100 Ω; 41,736 in stock; Active; $0.634 (10), $0.5508 (100).
- Workers' rights: not in RBA, not in KTC; nothing beyond the policy pages.

### TXC Corporation – 1 BoM line (Okapi 2024-11-02 BoM: 7A-8.000MAAE-T)

- **The TXC part is Obsolete and rated −20 °C to 70 °C** [Digi-Key, https://www.digikey.com/en/products/result?keywords=7A-8.000MAAE-T, 2026-11-11: "Obsolete and no longer manufactured"; 7A series, 5.0 × 3.2 mm, ±30/±30 ppm, 12 pF, ESR 80 Ω; Digi-Key suggests ECS-80-12-30-JGM-TR]. The KiCad Okapi already replaces it: commit `47a944d` (2026-11-06) "KiCad: XTAL1 is the ECS-80-12-30-JGN-TR; the TXC 7A-8.000MAAE-T is obsolete", and `Hardware/KiCAD-10import/Microcontroller.kicad_sch` carries MPN ECS-80-12-30-JGN-TR (verified by grep, 2026-11-11). The Eagle files (`Hardware/Okapi.sch` line 10739, `Hardware/Okapi_BoM.csv` line 74) still name the TXC part.
- [maker, via search] TXC is listed in Taiwan (TWSE 3042), headquartered in Taoyuan; plants at Pingzhen (Taiwan), Ningbo and Chongqing (China), with a further Ningbo site under construction in 2024 and an Indonesia (Surabaya) site on an investor slide (search summaries of txccorp.com downloads, e.g. https://www.txccorp.com/download/212/; slide date UNVERIFIED). This is a Taiwan/China footprint with an Indonesian addition.
- Workers' rights: not in RBA; no KTC record.

### Epson (Seiko Epson, timing devices) – 0 BoM lines (competes with ECS for the 8 MHz and 32.768 kHz parts)

- [maker] A 2021 Epson presentation lists timing-device plants at Ina, Hachinohe and Miyazaki (Japan), Kuala Lumpur (Malaysia), Chachoengsao (Thailand), plus Suzhou (China) and Longview, Washington (USA) on the same slide (https://tam.atis.org/wp-content/uploads/2021/03/Presentation-Epson-1.pdf, via search summary; whether Suzhou and Longview are crystal plants UNVERIFIED). Epson grows its own synthetic quartz and states control from quartz growth through assembly (https://corporate-origin.epson.biz/en/technology/overview/microdevice/artificial-crystal.html, via search summary).
- Interpretation (hypothesis): vertical integration from quartz bar to package, with Japan, Malaysia and Thailand capacity, is the strongest published resilience case among the crystal makers surveyed.
- Workers' rights: RBA "Seiko Epson Corporation - R". Not in KTC 2025.

### SiTime (MEMS oscillators) – 0 BoM lines

- [maker, SEC filings] Fabless: MEMS wafers from **Bosch** (ten-year supply agreement through February 2027 with automatic renewal, FY2024 10-K), analog CMOS from **TSMC**, assembly/test historically at ASE, Carsem and UTAC, ceramic packages from Daishinku and UTAC (FY2019 and FY2021 10-Ks); most sub-suppliers single- or sole-source; Malaysia, Taiwan and Thailand facilities named as exposed to instability (FY2023 10-K); moving to a backup supplier could take several quarters (FY2019 10-K). Filings at https://www.sec.gov/Archives/edgar/data/1451809/ (via search summary; FY2025 10-K https://www.sec.gov/Archives/edgar/data/1451809/000145180926000012/sitm-20251231.htm not read in full).
- Interpretation (hypothesis): a MEMS oscillator removes the crystal's cold-start and load-capacitance questions, but every unit depends on one MEMS fab (Bosch, Germany) and one CMOS foundry (TSMC, Taiwan). That is less resilient in supply than quartz from several makers.
- Workers' rights: not in RBA, not in KTC.

### Abracon – 0 BoM lines

- [independent, trade press] **Genstar Capital bought Abracon from The Riverside Company, announced 6 July 2022** (Riverside had held a majority since 2018 and added ProAnt, AEL Crystals, Fox Electronics and ILSI America); Abracon then agreed to buy NEL Frequency Controls, announced 5 July 2023 (https://passive-components.eu/abracon-announces-acquisition-by-genstar-capital; https://app.mergerlinks.com/transactions/2023-07-05-nel-frequency-controls-inc; via search summaries). Two private-equity owners in four years and several roll-up acquisitions.
- Factory locations: abracon.com blocked curl with Cloudflare (dead end). Not established. Abracon is widely understood to source from Asian quartz makers under its own brand (UNVERIFIED).
- Workers' rights: not in RBA, not in KTC.

### Würth Elektronik (eiSos) – 1 in-scope BoM line (Margay SD holder 693063010911); 8 further Würth lines on Okapi are inductors, LEDs and a capacitor, outside this scope

- [maker] Headquarters Waldenburg, Germany; 23 production sites worldwide (company page "This is us", https://www.we-online.com/en/company/this-is-us, via search summary); Tianjin is described by Würth as "a significant sales and logistics center" (https://we-online.com/en/company/locations/tianjin, via search summary); the Asia Quality Design Center in Shenzhen opened Laboratory Phase II in April 2026 (Würth press release wth1pi1833, https://www.we-online.com/files/docx1/wth1pi1833---pi-laboratory-qdc-shenzhen_260415_en_final.docx, via search summary). **Which plant or contract manufacturer makes Würth's connectors is not published in any source found**: UNVERIFIED.
- [maker] Ownership: part of the Würth Group, family-owned (Würth Elektronik group page; the family-ownership statement is well known but was not read in a source this session: UNVERIFIED).
- [maker] SD holder 693063010911: −25 °C to +85 °C, 10,000 cycles, "Selective Gold" with no thickness, LCP UL94 V-0 housing (prior survey F3, datasheet rev 003.002 dated 2026-07-16). Andy's field record is that these holders "have been used in past deployments at −40C" (same report, Decision section). Würth's connector datasheets give fewer test figures than Amphenol FCI's GS-12-497 (prior survey F3 vs F7).
- [maker] Würth offers no USB 2.0 vertical Type-C receptacle on Digi-Key and its horizontal Type-C is the 24-pin USB 3.1 part 632723300011 at $4.37 (1) against GCT's $0.80 (USB-C prior survey, "Rejected while searching" and "Other Digi-Key vertical USB-C"). Würth competes on SD holders and terminal blocks; it is not price-competitive on USB-C.
- Workers' rights: **not in RBA**; not in KTC (private). Würth's own supplier code was not read.

### PolyCase – enclosure WH-16-03 for Okapi (not on the assembly BoM; named in `Project-Okapi/README.md` line 456)

- [maker] PolyCase company profile 2026 (https://www.polycase.com/media/wysiwyg/polycase_company_profile_2026.pdf, fetched 2026-11-11): Avon, Ohio; manufacturing since 1951; injection molding, CNC machining and digital printing in house; "The majority of our enclosures are made in the United States"; 40,000 ft² facility; **privately held**, discloses no financials or headcount; "UL Certified Molder"; QMS "ISO 9001:2015 compliant" but "**not certified**".
- [maker, via search summary] **Not every WH-series size is made in Ohio**: the WH-18 and WH-08 pages list South Korea as origin and the WH-14 page lists Taiwan, and the WH-18 page points buyers to U.S.-made ZH and HP series (https://www.polycase.com/wh-18, https://www.polycase.com/wh-14, https://www.polycase.com/wh-08, via search summary). The WH-16 page's origin field could not be read (polycase.com returns 403 to curl and WebFetch): **WH-16 country of origin UNVERIFIED, and on the sibling evidence probably imported.**
- [maker, via search summary] WH-16: 11 × 7.9 × 5.1 in; gray flame-retardant ABS (indoor) or gray polycarbonate (outdoor, optional clear cover); IP65, IP66, NEMA 1, 2, 4, 4X; a WH-14 press release (2017) calls that size UL Listed and polycarbonate (https://www.polycase.com/wh-series). Which material the "-03" suffix selects, and the rated temperature range and UV stabilization, are UNVERIFIED.
- Second sources: hinged NEMA 4X polycarbonate boxes of this size are made by Hammond (Canada), Bud Industries (U.S.), Fibox (Finland) and others (general knowledge, not checked this session: UNVERIFIED); none shares WH-16 mounting-panel geometry unless checked.

### Keystone Electronics – 0 BoM lines (competes with Linx/TE for the coin-cell holder)

- [maker, via search summary] Headquarters 55 S. Denton Avenue, New Hyde Park, New York; offices in Canada, Europe, Australia and Asia (Keystone press releases 2018–2019 via GlobalSpec/Design News). Whether its holders are made in the U.S. was not confirmed by any source found: UNVERIFIED. Founded 1939 (impomag.com listing, search summary).

### Part-level facts for in-scope BoM lines (Digi-Key, fetched 2026-11-11)

**Linx/TE BAT-HLD-012-SMT (BT1, both boards): the bare part is Obsolete; the tape-and-reel twin is Active and rated −30 °C.**
- Digi-Key keyword search `BAT-HLD-012` (https://www.digikey.com/en/products/result?keywords=BAT-HLD-012): BAT-HLD-012-SMT **Obsolete, 0 stock**; BAT-HLD-012-SMT-TR Active, 1,518 stock, $0.55 (1), $0.46 (1,000 T&R); BAT-HLD-012-THM Obsolete; BAT-HLD-012-THM-TR Active, 0 stock.
- Both KiCad boards still carry MPN `BAT-HLD-012-SMT` (grep of `*.kicad_sch` in Project-Okapi and Project-Margay, 4 hits, 2026-11-11).
- [maker] TE product sheet for BAT-HLD-012-SMT-TR (generated 09/14/2024, via https://pf.unikeyic.com/datasheet/19/37/96e0/193796e03fc17ac16bc0d09ad5e065dc.pdf): "CR1216 / CR1225, 1 Position, Horizontal, Nickel"; holder material phosphor bronze; contact plating nickel; **operating temperature −30 to 70 °C**; China RoHS 2 "Restricted Materials Above Threshold". The sheet names CR1216 and CR1225, not the CR1220 that Northern Widget fits (NW-Status `studies/okapi-hardware-audit/margay-rtc-cold.md` line 27); a 12.5 mm cell between those two thicknesses is presumably held, UNVERIFIED.
- Second sources on Digi-Key for 12 mm SMD coin holders (keyword `12mm coin cell retainer`, 2026-11-11; all Active): Keystone 3000 (12,568 stock, $0.40) and 3000TR (27,549), Keystone 3080TR (16,381), Keystone 2894TR (CR1220 only, 4,045), MPD BK-885-TR (91,469, $0.66), MPD BK-916-TR (45,748, $0.56), Assmann A-BAT-CH-C2-EA-CRR1/2 (CR1225). Temperature not listed on the result page for these. **Land-pattern compatibility with the Linx footprint: not checked (UNVERIFIED).**

**Amphenol FCI 67997-206HLF (ISP1, both boards)**: BERGSTIK II; gold 15 µin (0.38 µm) on phosphor bronze; UL94 V-0; **−65 °C to 130 °C**; 69,117 stock; Active; $0.48 (10). Digi-Key "Similar" substitutes: TE 826942-3 (11,215, $1.01), Sullins PBC03DAFN / PEC03DAGN (low stock). A 2.54 mm 2×3 header is the most interchangeable part on either BoM (https://www.digikey.com/en/products/result?keywords=67997-206HLF).

**C&K PTS810 SJG 250 SMTR LFS (both boards)**: **−40 °C to 85 °C**; 50 mA at 16 VDC; 100,000 cycles; 37,969 stock; Active; lead 16 weeks; $0.56 (10), $0.466 (100). No substitutes named; sibling PTS810 SJK (https://www.digikey.com/en/products/result?keywords=PTS810%20SJG%20250%20SMTR%20LFS).

**JST S2B-PH-SM4-TB (Okapi J8)**: tin-plated contacts (thickness not given); housing PA6T (nylon 6T); **−25 °C to 85 °C**; 133,904 stock; Active; $0.417 (10), $0.3547 (100). Digi-Key "Similar": Sullins SWR201-NRTN-S02-HM-BG and Adam Tech 2SH-C-02-TR-SMT-T/R, both 0 stock (https://www.digikey.com/en/products/result?keywords=S2B-PH-SM4-TB(LF)(SN)). Tin-on-tin at a battery connector is the plating most prone to fretting under thermal cycling (general connector engineering; no JST-specific test found: UNVERIFIED for this part).

**GCT USB4105-GF-A (both boards)**: −40 °C to +85 °C, 20,000 cycles, 263,569 Digi-Key stock, $0.676 (10) (USB-C prior survey, section 1). Its land pattern is shared, within small differences, by HRO TYPE-C-31-M-12 and HCTL HC-TYPE-C-16P-01A (same survey, KiCad table); neither of those is on Digi-Key.

**C&K PCM12SMTR (Okapi S1, S2): Obsolete and rated −20 °C.** Digi-Key detail page (https://www.digikey.com/en/products/detail/c-k/PCM12SMTR/1640112, 2026-11-11): "This product is no longer manufactured and will no longer be stocked once stock is depleted"; 2,726 left; −20 °C to 85 °C; 10,000 cycles; silver on copper alloy; $1.087 (10). Digi-Key "Similar": **Nidec Components CUS-12TB** (74,403, $0.86) and **Same Sky SLW-662712-15A-SMT-TR** (5,400, $0.50); land compatibility and temperature of those UNVERIFIED. The KiCad Okapi (`Hardware/KiCAD-10import/*.kicad_sch`) still carries PCM12SMTR (3 symbol fields, grep 2026-11-11).

**Panasonic EVP-BB2A9B000 (Okapi S5)**: **−40 °C to 85 °C**, 160 gf, 500,000 cycles, **IP67**; 30,044 stock; Active; $0.497 (10) (https://www.digikey.com/en/products/result?keywords=EVP-BB2A9B000). Panasonic Holdings is RBA-listed and scored 10/100 in KTC 2025.

**Molex 5025700893 (Okapi SD1)**: microSD push-push; gold 20 µin (0.51 µm); temperature not on the result page; 20,107 stock; Active; $3.521 (10), $2.9924 (100) (https://www.digikey.com/en/products/result?keywords=5025700893).

**TE 2199230-4 (Okapi J9, M.2 for the Particle B-SoM)**: "CONN M.2 FMALE 67POS 0.020 GOLD", $1.66 (result page https://www.digikey.com/en/products/result?keywords=2199230-4); stock, status and temperature not shown on that page: UNVERIFIED. Particle's own B-SoM documentation names the socket; whether an alternative M.2 Key-E socket of equal height fits was not checked.

**Interpretation of the part-level facts (hypothesis, for Andy):** at the part level, the BoM's weak points are not the brands' reputations but four specific lines: two obsolete parts still in the KiCad sources (Linx BAT-HLD-012-SMT, where the -TR twin is active; C&K PCM12SMTR), and three in-scope parts rated above −40 °C (Linx holder −30 °C, JST PH −25 °C, C&K PCM12 −20 °C; plus Würth's SD holder at −25 °C, accepted on field record).

### Phoenix Contact – 0 BoM lines (competes with On Shore for terminal blocks; Digi-Key lists 1729225 as similar to OSTVN10A150)

- [maker, via search summary] Family-owned, headquarters Blomberg, Germany; its 2024 sustainability report says "we manufacture in nine countries with varying degrees of vertical integration" (other profiles say 10 or 11 sites); a Querétaro, Mexico, plant began sample production of power supplies at the start of 2026, aiming at about 700 employees by 2032 (https://www.phoenixcontact.com/en-ch/first-phase-of-construction-for-phoenix-contacts-new-mexican-production-facility-in-queretaro-officially-inaugurated); a Vietnam plant near Ho Chi Minh City with about 100 employees (same search). Which plant makes PCB terminal blocks: UNVERIFIED.
- Workers' rights: not in RBA; not in KTC (private).

### Samtec – 0 BoM lines

- [independent, certificate directory] Privately held, founded 1976, New Albany, Indiana. BSI certificate directory lists sites at Alajuela (Costa Rica), Huizhou and Dongguan (China), Johor Bahru and Perai/Penang (Malaysia), and a Vietnam site; a company profile names manufacturing at New Albany, Colorado, Oregon, Costa Rica, China, Malaysia and Singapore (search summaries of bsigroup.com client directory and craft.co, 2026-11-11). A U.S.–Central America–Asia spread.
- Workers' rights: not in RBA; not in KTC.

### Harwin – 0 BoM lines

- [maker, trade press] Main production site Portsmouth, UK, AS9100D; £3.8 million for a 1,200 m² Hi-Rel factory floor there (https://www.eenewseurope.com/en/3-8m-for-hi-rel-connector-factory-industry-4-0-expansion/; https://www.harwin.com/harwin-invests-a-further-1m-in-state-of-the-art-connector-manufacturing-facility/, via search summary). A Southeast Asia (Malaysia) facility is mentioned only in a third-party profile: UNVERIFIED. Private.
- Interpretation: the only connector maker in scope with its main plant in the UK/EU and aerospace accreditation, at a hi-rel price point.

### 4UCON – 0 BoM lines (origin of Margay's SD footprint, "4UCON part #06132", per the prior survey F1)

- Digi-Key carries no 4UCON parts (keyword search `4UCON`, 0 results, 2026-11-11). 4uconnector.com did not answer curl (timeout, dead end). Web search found no company profile (dead end). Under Andy's Digi-Key criterion 4UCON is a weaker candidate; the footprint lineage matters only because the TE 2041021 and Würth 693063010911 share its outline class (prior survey F10).

### GCT (Global Connector Technology) – 2 BoM lines (USB4105-GF-A, both boards)

- [independent, thin] "Part of a privately held group of companies"; headquarters and engineering in Hong Kong; manufacturing in mainland China, city not named (Design News company profile, https://showcase.designnews.com/global-connector-technology-comp232359.html, via search summary 2026-11-11). Owners not named: UNVERIFIED. A distributor lists a U.S. presence at Salem, New Hampshire (thepartsdirect.com, via search summary).
- [maker] ISO 9001:2015 certified, with "zero identified major/minor non-conformities" at audit (https://gct.co/news/gct-iso9001-2015-certified, via search summary; gct.co returns HTTP 403 to curl and WebFetch, so neither the news item's date nor the certifying body was read). No IATF 16949 certificate found.
- [maker] USB4105 drawing (4 October 2019) gives −40 to +85 °C and 20,000 cycles; no plating thickness, salt-spray or thermal-shock data appear in the drawing as summarized in the USB-C prior survey.
- Geopolitics (hypothesis): a single-country (China) manufacturing base with a Hong Kong parent is the most concentrated geopolitical exposure among the BoM's connector brands. Mitigation is the land pattern, not the brand: USB4105's 16-pin top-mount pattern is shared within small differences by HRO and HCTL parts (prior survey), but those are also Chinese makers and not on Digi-Key; Molex 2171790001 (Digi-Key 65,872 stock, −40 °C) is a non-Chinese-brand horizontal candidate whose land pattern was not checked (prior survey).
- Workers' rights: not in RBA, not in KTC; nothing found.

### JST note on change notification

- [independent] TTI Europe hosts JST product-change notices as PDFs, e.g. https://www.tti.com/content/dam/tti-europe/products/PCN/JST/JST-G25-05825.pdf (found by search 2026-11-11; not opened). JST does issue PCNs through franchised distributors; content and coverage of the PH series not read.
- Counterfeit exposure: no JST-published authentication guide found; vendor blogs advise buying from authorized distributors (search 2026-11-11, results weak). Digi-Key is a JST franchised distributor (UNVERIFIED from a JST list, though Digi-Key stocks 133,904 of J8's part).

### Murata (ceramic resonators only) – 0 BoM lines in scope (Murata capacitors on both BoMs are another agent's scope)

- [maker, via search summary] CERALOCK CSTNE resonators come in −40 to 85 °C and −40 to 125 °C (automotive) grades (Murata catalog excerpts and https://www.murata.com/products/timingdevice/ceralock/overview/app/auto). A ceramic resonator (±0.5 % class) is not a substitute for the RTC or USB-timing crystal; for an ATmega1284P system clock it is (fact about resonator tolerance from the same catalog summary; suitability for UART timing at Northern Widget's baud rates not checked).
- Production site for resonators: not found (dead end).
- Workers' rights [independent]: RBA "Murata Manufacturing - R"; KTC 2025 10/100, rank 34 of 45 (scorecard read).

### Conflict-minerals reporting (SEC Form SD, U.S.-listed brands only)

- [maker, SEC] Amphenol filed Form SD for calendar 2025, dated 29 May 2026 (https://www.sec.gov/Archives/edgar/data/820313/000110465925054617/tm2516344d1_sd.htm is the 2024-period filing found; the 2025-period filing was reported by search, accession not confirmed); Amphenol states RMI membership and an RMAP-based program (https://www.amphenol.com/docs/conflict-minerals, via search summary).
- [maker, SEC] TE filed Form SD for calendar 2025, signed 29 May 2026, with Exhibit 1.01 Conflict Minerals Report (https://www.sec.gov/Archives/edgar/data/0001385157/000110465926068087/tm2615812d1_sd.htm, via search summary). Smelter counts and RMAP-conformant shares were not read for either.
- Littelfuse (C&K) and SiTime are also SEC filers and file Form SD (not checked this session: UNVERIFIED). Private makers (Molex, JST, Hirose, Würth, Samtec, Harwin, Phoenix, GCT, On Shore, ECS, PolyCase, Abracon) have no SEC obligation; On Shore and ECS publish policy statements only (see their sections).

### Corporate Human Rights Benchmark and Electronics Watch

- CHRB (World Benchmarking Alliance): its ICT assessments cover large OEMs and chipmakers; no connector, crystal or enclosure brand in this scope was found in it (search not run to completion: UNVERIFIED negative).
- Electronics Watch: search for findings naming TE, Amphenol, Molex or Luxshare returned none; the nearest case found was Tripod (Wuxi, 2024), a PCB maker by general knowledge (https://electronicswatch.org/en/impact-story-worker-testimony-leads-to-remediation-for-sexual-harassment-at-tripod_2688785). Negative search result, not evidence of clean records.

## Summary table (one finding per cell; strength in brackets)

Strength key: **[S]** read in a primary document or distributor record this session; **[M]** maker's claim via search summary or one secondary source; **[W]** inference, thin, or UNVERIFIED. BoM lines are Margay + Okapi.

| Brand | BoM lines | 1. Geopolitical resilience | 2. Wide-temperature quality | 3. Consistent quality | 4. Workers' rights |
|---|---|---|---|---|---|
| On Shore Technology | 2 + 4 | Tempe, AZ distributor-brand; no factory or country published; maker probably Taiwanese OEM (Anytek name match) [W] | OSTVN drawing −40…115 °C, Digi-Key says −30…105 °C: conflict [S] | No ISO certificate or PCN practice published [S] | 2015 one-page conflict-minerals letter only; not RBA [S] |
| Amphenol (FCI, Anytek) | 1 + 1 | ~40 countries, but 37 % of long-lived assets in China, rising (10-K FY2025) [S] | 67997-206HLF −65…130 °C, 15 µin Au; FCI SD spec has salt spray, thermal shock, −40 °C cycling [S] | Header has 5 Digi-Key substitutes; most interchangeable line on the BoM [S] | KTC 2025 8/100, rank 37/45; RBA listed [S] |
| TE Connectivity (incl. Linx) | 0 + 1 (+2 Linx) | 105 plants, 79 outside Asia–Pacific; 19 principal sites in China (10-K FY2025) [S] | Linx coin holder −30…70 °C, nickel on phosphor bronze [S] | BAT-HLD-012-SMT obsolete (still in KiCad); 2041021-4 SD holder went obsolete earlier [S] | RBA listed; not in KTC 2025; Form SD filed [S] |
| C&K (Littelfuse since 2022) | 1 + 2 | Plants Dole (France) and Huizhou (China) [M] | PTS810 −40…85 °C; PCM12SMTR −20…85 °C [S] | PCM12SMTR obsolete, 2,726 left, still in KiCad [S] | Not RBA; not KTC [S] |
| GCT | 1 + 1 | Hong Kong parent, manufacturing in mainland China only [M] | USB4105 −40…85 °C, 20,000 cycles; no plating or environmental test data [S] | ISO 9001:2015 claimed; land pattern cloned by HRO/HCTL (not on Digi-Key) [M] | Nothing found; not RBA [S] |
| Molex (Koch) | 0 + 2 | 74 plants in 19 countries; new Vietnam, Poland, Mexico capacity [M] | microSD 5025700893 20 µin Au; temperature not on Digi-Key page [S] | Both parts Active, 20,107 and ample stock [S] | RBA "R" tier; private, not in KTC [S] |
| JST | 0 + 1 | Private; Japan and Malaysia plants, rest unpublished [W] | PH SMT header −25…85 °C, tin plating [S] | PCNs issued via distributors (TTI) [M]; PH widely cloned and counterfeited [W] | Not RBA; not KTC [S] |
| Würth Elektronik | 1 + 0 (in scope) | German family firm, 23 production sites; connector plant unpublished [M] | SD holder −25…85 °C, selective gold, no thickness; used at −40 °C in the field [S] | Digi-Key's named substitute for TE's obsolete SD holder; 17,469 stock [S] | Not RBA; private, not KTC [S] |
| ECS Inc. | 1 + 0 (Okapi KiCad now ECS too) | Lenexa, KS; no factory named; sales in KR, JP, CN, SG, US [S] | ECX-53 −40…85 °C [S] | Counterfeit and conflict-mineral policies published; change-notice page exists [S] | Policy pages only; not RBA [S] |
| TXC | 0 + 1 (Eagle only) | Taiwan + China plants, Indonesia site added [M] | 7A-8.000MAAE-T −20…70 °C [S] | Part obsolete; already replaced in KiCad (`47a944d`) [S] | Not RBA [S] |
| Panasonic (switch) | 0 + 1 | Not researched (another agent's brand scope) [W] | EVP-BB2A9B000 −40…85 °C, IP67, 500,000 cycles [S] | Active, 30,044 stock [S] | KTC 2025 10/100; RBA listed [S] |
| Epson | 0 | Grows own quartz; plants in Japan, Malaysia, Thailand (2021 slide) [M] | Not checked per part [W] | Not checked [W] | RBA "R" tier; not in KTC [S] |
| SiTime | 0 | Single MEMS fab (Bosch) + TSMC, single/sole-source sub-suppliers (10-Ks) [M] | Not checked per part [W] | Not checked [W] | Not RBA [S] |
| Abracon | 0 | PE-owned (Genstar, 2022), roll-up of Fox, ILSI, AEL, NEL [M] | Not checked [W] | Not checked [W] | Not RBA [S] |
| Murata (resonators) | 0 | Not researched here [W] | CSTNE −40…85 or −40…125 °C [M] | Not checked [W] | KTC 2025 10/100; RBA "R" [S] |
| Hirose | 0 | 8 factories (KR, ID, MY, 2 CN, 3 JP), India from 2027; some products single-site [M] | DM3 microSD −25…85 °C (prior survey) [S] | Not checked [W] | Not RBA [S] |
| Phoenix Contact | 0 | German family firm, 9 production countries, Mexico plant from 2026 [M] | Not checked per part [W] | Not checked [W] | Not RBA [S] |
| Samtec | 0 | Private; US, Costa Rica, China, Malaysia, Vietnam sites [M] | Not checked [W] | Not checked [W] | Not RBA [S] |
| Harwin | 0 | Main plant Portsmouth, UK, AS9100D [M] | Not checked [W] | Not checked [W] | Not RBA [S] |
| Same Sky (CUI) | 0 | Rename 2024, owners unnamed [M] | UJ20-C-V-C-2 vertical USB-C −40 °C (prior survey) [S] | Offers drop-in for PCM12SMTR (SLW-662712-15A) [S] | Not RBA [S] |
| Keystone | 0 | New Hyde Park, NY; U.S. manufacturing not confirmed [W] | Not checked [W] | 12 mm SMD holders 3000/3000TR/3080TR in stock as Linx alternatives [S] | Not RBA [S] |
| 4UCON | 0 | No Digi-Key line; no company data found [S] | – | – | – |
| PolyCase | enclosure | Avon, OH; "majority" U.S.-made, but WH siblings made in Korea and Taiwan; WH-16 origin unknown [M] | WH-16 polycarbonate outdoor variant, IP66, NEMA 4X; temperature range unknown [M] | UL Certified Molder; ISO 9001 "compliant", not certified [S] | Private; nothing published [S] |

## Open questions

1. On Shore OSTVN temperature: OST's drawing (OCR) says −40 to 115 °C; Digi-Key says −30 to 105 °C. A clean copy of the drawing, or an email to OST, settles which; OST's country of manufacture and whether Anytek is its OEM can be asked in the same email.
2. Linx BAT-HLD-012-SMT is obsolete but still in both KiCad sources; the -TR twin is the same part on reel at 1,518 stock. Swap the MPN to -TR, or move to a Keystone/MPD holder rated to −40 °C? Land compatibility of Keystone 3000 and MPD BK-885 with the Linx footprint is unchecked.
3. C&K PCM12SMTR on Okapi is obsolete (2,726 left) and rated −20 °C. Nidec CUS-12TB and Same Sky SLW-662712-15A-SMT-TR are Digi-Key's suggestions; their land patterns and temperature ratings are unchecked.
4. JST PH (−25 °C) for Okapi's battery: is a −40 °C-rated 2 mm battery connector wanted, or is the rating accepted on field record as for the Würth SD holder?
5. PolyCase WH-16-03: material (ABS or polycarbonate), country of origin and temperature range need reading from polycase.com in a browser (403 to scripts). The README calls it "outdoor-rated", which points to polycarbonate.
6. GCT: who owns the group, and which plant makes USB4105? Its China-only base is the most concentrated exposure among the BoM's connectors. A Molex 2171790001 land-pattern check (prior USB-C survey, open question) would give a non-GCT horizontal option.
7. TE 2199230-4 (M.2 socket) stock, status and temperature were not read (Digi-Key result page incomplete).
8. Smelter and RMAP-conformance numbers in Amphenol's and TE's 2025 Conflict Minerals Reports were not read.
9. TE's KnowTheChain history (2018 rank 28 of 40) is from search results only.
10. Würth's connector plants and Würth's supplier code of conduct were not found; Würth is not an RBA member.
11. Crystal makers' factory locations: ECS and Abracon publish none. An email to ECS asking where ECX-53 is made would settle the one crystal both boards now use.

## Sources checked (including dead ends)

- BoMs: `Project-Margay/Production/Margay_BoM_3v0_-_2026-11-04.csv`; `Project-Okapi/Hardware/Okapi_2024-11-02.zip` → `CAMOutputs/Assembly/Okapi.txt` (`unzip -p`); KiCad `Project-Okapi/Hardware/KiCAD-10import/*.kicad_sch` and `Project-Margay` `*.kicad_sch` (grep for MPN fields); `Project-Okapi` git log (`-S'ECS-80-12-30'` → `47a944d`); `Project-Okapi/README.md` line 456 (enclosure).
- Prior surveys reused: `NW-Status/studies/okapi-hardware-audit/sources/2026-11-11-usb-c-connector-agent-report.md`, `2026-11-11-margay-sd-holder-agent-report.md`.
- RBA member list (read). KnowTheChain 2025 briefing (read); scorecard PDFs for Amphenol, Murata, Kyocera, Panasonic (read with pdftotext); TE Connectivity and Seiko Epson scorecard URLs (XML error, dead end).
- On Shore: on-shore.com home, company, documentation, FAQ, OSTVNXXA150 part page (read); conflict-minerals PDF and OSTVN drawing (image PDFs, read by tesseract OCR); 2019 brochure (no extractable text, dead end); /about-us and /about (404, dead end).
- GCT: gct.co (403 Cloudflare to curl and WebFetch, dead end); Design News profile and GCT news item via search only.
- PolyCase: polycase.com product pages (403, dead end); company profile 2026 PDF (read).
- ECS: ecsxtal.com about, conflict-minerals, counterfeit pages (read); /about-ecs/ and /quality/ (404).
- Abracon: abracon.com (Cloudflare block, dead end); trade-press via search.
- Mouser product page for OSTVN10A150 (WebFetch timeout, dead end).
- 4uconnector.com (no response, dead end); Digi-Key `4UCON` (0 results).
- C&K: ckswitches.com/about/ (301 to home), /about-us/ (301 to littelfuse.com/company); plant facts via search only.
- SEC: Amphenol 10-K FY2025 via boardroomalpha (first 100,000 characters); TE 10-K FY2025 via stocktitan (both parts); TE annual report PDF on q4cdn (HTML block page to curl, dead end); Littelfuse 10-Q, Amphenol 8-K (2016), SiTime 10-Ks, Form SDs via search summaries only.
- Digi-Key pages read: OSTVN10A150 detail; result pages for ECS-80-18-30-JGN-TR, 7A-8.000MAAE-T, BAT-HLD-012-SMT, BAT-HLD-012, 12mm coin cell retainer, 67997-206HLF, PTS810 SJG 250 SMTR LFS, S2B-PH-SM4-TB(LF)(SN), 5025700893, 2199230-4, EVP-BB2A9B000, 4UCON; PCM12SMTR detail; `CR1220 holder SMD` (0 results); a 2199230-4 detail URL guessed wrongly (returned an Amphenol PT05 page, discarded).
- TE product sheet BAT-HLD-012-SMT-TR via pf.unikeyic.com mirror (read); Mouser-hosted drawing (returned JavaScript, dead end).
- Web searches (summaries only, cited as such above): Hirose, JST, Molex, Phoenix Contact, Samtec, Harwin, Würth, Keystone, TXC, Epson, SiTime, Abracon, Same Sky, Linx/TE, Littelfuse/C&K, Amphenol/FCI/Anytek, JST counterfeits, Electronics Watch, crystal cold-start escapes (no maker-specific case found), Murata CERALOCK, Form SD for Amphenol and TE.

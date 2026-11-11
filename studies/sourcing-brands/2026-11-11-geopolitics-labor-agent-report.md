# Component sourcing: geopolitics, export continuity, and labor frameworks

Status: COMPLETE (2026-11-11)

Agent report, 2026-11-11. Cross-cutting evidence base for the passives, semiconductors and connectors brand surveys. Every fact carries its URL. Labels: **[company claim]** = the company's own statement; **[independent]** = an association, government, benchmark, journalist or NGO; **UNVERIFIED** = not confirmed against a primary source in this session.

## Part A: geopolitics and export continuity

### A1. Where components are made

**Semiconductors, front end and back end** [independent: SIA/BCG, "Emerging Resilience in the Semiconductor Supply Chain", May 2024, https://www.semiconductors.org/wp-content/uploads/2024/05/Report_Emerging-Resilience-in-the-Semiconductor-Supply-Chain.pdf ; downloaded and text-extracted 2026-11-11. Sources cited by the report: SEMI, Yole, IHS, Gartner, BCG analysis.] Shares are by location of installed capacity, 2022:

| Activity | US | EU | Japan | S. Korea | Taiwan | Mainland China | Rest of world |
|---|---|---|---|---|---|---|---|
| Wafer fabrication (all), Exhibit 2, p. 10 | 10% | 8% | 17% | 17% | 18% | 24% | 7% |
| Assembly, test and packaging (ATP), Exhibit 2, p. 10 | 3% | 3% | 6% | 9% | 28% | 30% | 20% |
| Wafer fab, discretes, analog, opto and sensors (DAO), Exhibit 6, p. 14 | 14% | 17% | 25% | 7% | 5% | 25% | 9% |

The DAO row is the relevant one for a logger's regulators, op-amps, MOSFETs and sensors. Its column assignment is inferred: the extracted text loses the legend order, so I mapped Exhibit 6 by the order of Exhibit 2, which reproduces Exhibit 2's "Total" row exactly and puts sub-10 nm logic at US 0%, Korea 31%, Taiwan 69%, as the report's text states. Treat the DAO split as UNVERIFIED until read off the chart image.

Text on ATP (p. 20): "Mainland China and Taiwan together host nearly 60% of global ATP capacity"; "Southeast Asia is already home to significant ATP activity, accounting for ~20% of total global capacity, with Malaysia capturing the greatest share within the region"; emerging markets forecast to grow "from 20% of global capacity in 2022 to 27% in 2032"; "The United States accounts for only a small share of global ATP capacity." Fab forecast: US share of fab capacity projected from 10% (2022) to 14% (2032) (SIA press release, https://semiconductors.org/america-projected-to-triple-semiconductor-manufacturing-capacity-by-2032-the-largest-rate-of-growth-in-the-world/ ). Forecasts are the report's, recorded here only as its stated projection.

What this means for a part on a Digi-Key shelf: a US- or European-brand analog chip is commonly fabbed in the US, Europe or Japan and then assembled and tested in Malaysia, the Philippines, Thailand or China. Which of those countries appears as "country of origin" is a customs determination, not a description of the whole chain. US Customs (CBP) rulings generally hold that front-end wafer processing is the substantial transformation and that back-end assembly and test in another country does not change origin [independent: CBP rulings]. Example: ruling N352561 (2025-09-10), a 24-bit delta-sigma ADC in a wafer-level chip-scale package, wafer fabricated in Singapore, wafer-level packaging front end (redistribution layer, bumping) in Taiwan, test, grind, mark and saw in the Philippines: "the country of origin of the finished AZ33A Device will be the Taiwan for country of origin marking purposes." (Read from a mirror, https://open-gov.usebase.io/rulings/N352561 ; the authoritative copy is CBP's CROSS database, https://rulings.cbp.gov/ .) A search summary also describes a 2006 ruling that MCU origin "is the country where the wafer was fabricated" and 2025 rulings that a Chinese or Philippine back end did not confer origin; those ruling numbers were not individually confirmed. Rulings are case-specific. The consequence for a buyer: a COO of "Malaysia" or "Philippines" may mean the die was made there, or that the manufacturer labels by a different rule (EU and manufacturer practice were not checked), and a COO of "US" or "Japan" does not mean the part avoided Southeast Asian assembly.

**MLCCs** (evidence thin; no country-level production statistic found):
- [company claim] Murata: "Murata's share of the MLCC market is 40%" (undated, no source given), https://corporate.murata.com/company/business/capacitor .
- [independent, trade press relaying Korean and Chinese press] Passive Components Blog, 2025-06-16, crediting DigiTimes: Samsung Electro-Mechanics "Held 24% of the global market in H1 2024, second only to Japan's Murata"; Chinese MLCC makers' share "surged to 10% of total revenue in the second half of 2024", up four points from 2019. https://passive-components.eu/chinas-mlcc-makers-reach-10-market-share/ . The same article says SEMCO, TDK, Yageo and Taiyo Yuden hold "10% to 20%", which does not reconcile arithmetically with Murata >40% plus SEMCO 24%; treat all of these as rough.
- Murata production geography [trade press, UNVERIFIED against Murata filings]: MLCC plants in Japan (Fukui, Izumo, and a new Okayama site) plus China, Singapore, the Philippines and Thailand; Thailand described as its largest MLCC plant; Murata's president said in February 2025 "While most of our latest capacitors are produced in Japan, we may reduce that share from 60% to about 50%" (search summaries of https://iconnect007.com/article/152207/murata-to-expand-production-capacity-of-multilayer-ceramic-capacitors-going-forward/ and https://nationthailand.com/business/corporate/40031356 ; not fetched directly).
- Reading: the MLCC market is headquartered in Japan and Korea, with Taiwan (Yageo, Walsin) and a growing Chinese segment; manufacturing is spread across Japan, Korea, China and Southeast Asia (Thailand, the Philippines, Malaysia). No published country-share table was found; the paid Paumanok and similar reports were not accessible.

**Resistors** (evidence thin): no country-share production statistic found. Market-research listings name Yageo first, with Vishay, KOA, Walsin, Ralec, Rohm, Panasonic and Uniohm commonly listed, and mainland Chinese makers (e.g. Fenghua Advanced Technology) gaining in mid- and low-end products; one report summary puts Asia-Pacific at roughly 75% of the market. All from paid-report blurbs (e.g. https://www.gii.tw/report/qyr2038265-chip-resistor-global-market-share-ranking-overall.html , https://www.dri.co.jp/auto/report/qyr/251103-chip-resistor-global-market-share-and.html ); UNVERIFIED. The headquarters picture is Taiwan (Yageo, Walsin, Ralec, Uniohm, Ta-I), Japan (KOA, Rohm, Panasonic), the US (Vishay, Bourns) and China; plant locations are per company and belong to the passives agent.

**Connectors** [independent: Bishop & Associates via Passive Components Blog, 2025-12-05, https://passive-components.eu/bishop-reveals-top-10-connector-manufacturers/ ]: worldwide connector sales $86.48 billion in 2024; top 10 held $46.0 billion (53.2%): TE Connectivity $12,884.0 M, Amphenol $11,510.7 M, Molex $4,871.5 M, Aptiv $4,636.5 M, Foxconn (FIT) $2,950.2 M, Luxshare $2,642.8 M, Yazaki $2,214.1 M, Rosenberger $1,749.9 M, BizLink $1,302.7 M, JAE $1,262.7 M. "Four of the top 10 companies are based in North America." These are sales by headquarters, not production by country; Bishop's country breakdown is in a paid report and was not found. Thin evidence on where connectors are made.

**Crystals and oscillators** (evidence thin): market-research summaries name Seiko Epson, NDK, TXC (Taiwan), Kyocera and KDS (Daishinku) as leading makers and state Japan as the largest producing area with "a share above 30%" (single paid-report summary, e.g. https://pdf.marketpublishers.com/globalinfo/global-quartz-crystals-n-oscillators-supply-demand-n-key-producers-2023-2029.pdf ); UNVERIFIED.

### A2. Disruptions, dated

Each entry: what happened, dates, who kept shipping, source. No forecasts.

**2018–2020 MLCC shortage** [independent: contract-manufacturer market update, Daniella Baldock, JJS Manufacturing, I-Connect007, 2018-10-04, https://iconnect007.com/article/113012/electronic-components-market-update/113015/ein ]. "Panasonic are quoting 99 weeks on out of stock chip capacitors and Kemet in excess of 52 weeks." "Yageo, TDK, AVX and Kemet have all issued price increases in recent months," some applying to backorders already placed. Murata "issued product change notifications" covering a large share of legacy MLCCs, with last-time-buy dates from March 2019, and was expanding capacity (construction from October 2018, online by end of 2019). A search summary of a 2018 broker email in the same thread quotes MLCC lead times "up to 50 weeks plus" and Yageo running "bidding" for stock (UNVERIFIED; not in the fetched text). [Interpretation, mine, not from the source]: a demand-driven shortage (automotive and smartphone MLCC counts) aggravated by the Japanese makers shifting capacity to high-value parts and ending legacy commodity lines. No country stopped exporting; the constraint was allocation and price, and it fell hardest on low-volume buyers without contracts. The end-of-life wave is the lesson that carries: commodity case sizes and values were discontinued by the market leader.

**2020–2023 chip shortage** [independent: SIA/BCG, "Strengthening the Global Semiconductor Supply Chain in an Uncertain Era", April 2021, https://www.semiconductors.org/wp-content/uploads/2021/05/BCG-x-SIA-Strengthening-the-Global-Semiconductor-Value-Chain-April-2021_1.pdf , downloaded and text-extracted 2026-11-11]. Executive summary (p. 3): "The widespread shortage of semiconductors that began in late 2020". Sidebar of past disruptions (p. 40), quoted: the September 1999 Taiwan earthquake "caused a six-day shutdown of the Hsinchu Science Park due to power outages"; after the 2011 Japan earthquake and tsunami "25% of the global production of silicon wafers and 75% of the global supply of hydrogen peroxide was affected ... Several fabs were shut down for several months"; in 2019 "Japan imposed export controls on semiconductor materials to Korea"; "In December 2020, a power outage affected a memory fab located in Taiwan for just one hour, impacting 10% of global DRAM supply"; "Two fires at a package substrate plant in Taiwan in October 2020 and February 2021 aggravated the global capacity shortage for assembly, packaging and testing services"; "Widespread power failures following a polar vortex in Texas, and a fire in a Renesas fab in Japan in early 2021 further exacerbated the global chip supply shortage, especially for the automotive market." The same report: "all of the world's most advanced semiconductor manufacturing capacity—in nodes below 10 nanometers—is currently located in South Korea (8%) and Taiwan (92%)". The dated events below are the ones that hit the parts a logger uses.

**Texas winter storm, February 2021** [independent: AP via TechXplore, 2021-02-19, https://techxplore.com/news/2021-02-winter-weather-texas-chip-worsening.html ]. NXP's Austin plant "was closed amid the state's electric power difficulties"; Infineon was told power would be turned off at its Austin plant, a notice that "gave us a few hours to prepare for the disruption," and put the fab in a "safe state"; Samsung suspended operations at its Texas facilities. A search summary of a 2021-03-05 report says the fabs had not yet resumed by that date (UNVERIFIED). Samsung's Austin foundry went offline "at 4 pm local time on Feb. 16, 2021" per the Korea Economic Daily (https://www.kedglobal.com/newsView/ked202102170012 ; search summary, UNVERIFIED by direct fetch). [Interpretation, mine]: the cause was the grid, not the plants; a US domestic fab was lost for weeks to a utility failure.

**Renesas Naka fire, 2021** [company claim: Renesas, UPDATE 10, dated 2021-06-25, https://www.renesas.com/en/about/press-room/update-10-notice-regarding-semiconductor-manufacturing-factory-naka-factory-fire-production-capacity ]. Fire "on March 19, 2021" in the N3 Building (300 mm line) at Naka, Hitachinaka, Ibaraki; the building "resumed operation on April 17"; production returned to "100% of the pre-fire level as of the evening of June 24"; shipments expected to return to pre-fire levels "around the third week of July," varying by product. [independent, trade press via search summary, UNVERIFIED]: about two-thirds of the line's output was automotive chips, and Renesas held roughly 30% of the automotive MCU market (https://convergedigest.com/fire-at-renesas-naka-semiconductor-fab/). From the dates above: about four months from fire to the expected shipment recovery.

**Malaysia COVID lockdowns, June–September 2021** [independent: Bloomberg via Transport Topics, 2021-08-24, https://ttnews.com/articles/chip-shortage-set-worsen-covid-rampages-through-malaysia ]. "During June lockdowns, companies could operate with 60% of their workforces," returning to 100% when more than 80% of workers were vaccinated; unofficial guidelines shut a factory "for up to two weeks" if more than three workers caught COVID-19. STMicroelectronics "suspended its assembly plant in Muar and resumed operations after 11 days"; Infineon closed facilities and put the impact in the "high-double-digit" millions of euros. Ford paused F-150 production at one US plant for "a semiconductor-related part shortage as a result of the COVID-19 pandemic in Malaysia"; Toyota suspended production at 14 plants; Nissan shut its Smyrna, Tennessee lines for two weeks in August; chip lead times rose to 20.2 weeks in July. A search summary says Infineon's Melaka production "stopped for 20 days in June" (UNVERIFIED). [Interpretation, mine]: this is the clearest dated example of back-end concentration; Malaysia did not restrict exports, but capacity limits at its assembly-and-test plants stopped shipments for weeks.

**Chinese export controls on gallium, germanium and related materials, 2023 onward.**
- 2023-07-03: MOFCOM and the General Administration of Customs announced licensing for gallium- and germanium-related items, effective 2023-08-01 [independent: Herbert Smith Freehills note, August 2023, https://www.hsfkramer.com/notes/sanctions/2023-08/china-releases-latest-export-control-measures-on-gallium-and-germanium ; IEA policy record, https://www.iea.org/policies/17893-announcement-on-the-implementation-of-export-control-of-items-related-to-gallium-and-germanium ; both via search summary]. Press reports of Chinese customs data said exports of the two metals fell to zero in August 2023 (https://mining.com/?p=1127526 ; search summary, UNVERIFIED by direct fetch).
- 2024-12-03: MOFCOM Notice 2024 No. 46, "Notice Concerning Strengthening Controls on Exports of Relevant Dual-Use Items to the United States": exports of gallium, germanium, antimony and superhard materials to the United States "in principle, not permitted"; stricter end-user checks for graphite; effective the day it was promulgated [independent: CSET translation, https://cset.georgetown.edu/publication/china-rare-earth-export-ban/ , fetched]. WilmerHale notes the notice included "for the first time a prohibition on export to third countries intended for transshipment to the United States" (https://www.wilmerhale.com/en/sitecore/content/whlaunch/home/research/news-publications/20241223-china-imposes-series-of-measures-to-counter-us-export-restrictions ; search summary).
- 2025-11-09: MOFCOM suspended the US-specific prohibitions of Notice No. 46 until 2026-11-27; general licensing stays in place and the military-end-user ban remains [independent: Fastmarkets, https://www.fastmarkets.com/insights/china-suspends-export-prohibition-on-superhard-materials-us/ ; Evertiq, https://evertiq.com/news/2025-11-10-china-suspends-ban-on-gallium-and-germanium-exports-to-the-us ; search summaries]. That suspension runs out sixteen days after this report's date; what happens then is not reported here.
- Relevance to a logger [interpretation, mine]: gallium and germanium matter mainly for compound semiconductors (GaN, GaAs, some LEDs and RF parts) and optics, not for ordinary silicon MCUs, regulators or passives. I found no report of a component shortage at distribution level traced to these controls; that is absence of evidence from a short search.

**Nexperia / Wingtech, 2024–2025** [independent: SCMP timeline syndicated on Yahoo Finance, 2025-11-21, https://finance.yahoo.com/news/timeline-sino-dutch-row-over-093000431.html , fetched; dates below quoted from it]:
- December 2024: Wingtech Technology, Nexperia's parent, added to the US Entity List.
- 2025-09-29: US BIS extended export controls to entities at least 50% owned by listed companies (the "Affiliates Rule"), bringing Nexperia under them.
- 2025-09-30: Dutch Ministry of Economic Affairs took control of Nexperia under the 1952 Goods Availability Act.
- 2025-10-04: China's Ministry of Commerce banned exports of finished components and sub-assemblies made by Nexperia's China unit and its subcontractors; "The Dongguan facility produces about 70% of Nexperia's global output." (Other outlets date the ban to mid-October; NLTimes, https://nltimes.nl/2025/10/14/china-imposes-export-ban-dutch-intervention-chipmaker-nexperia .)
- 2025-10-07: Dutch Enterprise Chamber removed CEO Zhang Xuezheng and put Wingtech's voting rights under an administrator.
- 2025-10-18: Nexperia China declared itself an independent Chinese entity, telling staff to follow local management.
- 2025-10-29: Nexperia's head office suspended wafer supply to Dongguan.
- 2025-10-30: Xi–Trump meeting in Busan; truce covering the Affiliates Rule.
- 2025-11-06: MOFCOM approved export licenses and exemptions for eligible exports; 2025-11-10: BIS suspended the Affiliates Rule for one year, "with automatic reimposition on November 10, 2026, unless BIS takes further action"; 2025-11-11: first exempted shipments heading to Europe; 2025-11-19: Dutch government suspended its order.
- Impact: production pauses reported in Mexico, and EU automakers warned they were "days away" from stopping lines (search summary of https://www.just-auto.com/newsletters/european-vehicle-production-nexperia-dispute ; UNVERIFIED by direct fetch).
- After 2025-11: Wingtech said on 2025-12-26 that Dongguan kept running despite a "significant gap in wafer supply" (search summary of Caixin and Tom's Hardware coverage, e.g. https://www.tomshardware.com/tech-industry/nexperia-china-seeks-new-wafer-suppliers-amid-legal-standoff-with-dutch-parent ; UNVERIFIED by direct fetch). No 2026 status report found in one search; open question.
- [Interpretation, mine]: this is the dated case in which a European-headquartered brand's parts stopped shipping because its back end sat in China and its owner sat on a US list; the front end (Hamburg and Manchester fabs; locations from memory, UNVERIFIED) kept running but the assembled parts could not leave Dongguan. Nexperia's discretes and logic (diodes, small-signal MOSFETs, 74-series logic) are common on logger boards; equivalents exist from onsemi, Diodes Inc, Rohm, Toshiba and Vishay for many such parts (from memory, part-by-part equivalence not checked).

**US export controls** [independent: law-firm and Federal Register summaries via search; primary BIS texts not fetched]. 2022-10-07: BIS interim final rule on advanced computing ICs and semiconductor manufacturing items (87 FR 62186, published 2022-10-13). 2024-12-02: BIS package adding 140 entities to the Entity List (China, Japan, South Korea, Singapore) and new controls on manufacturing equipment, software and HBM (https://bis.gov/press-release/commerce-strengthens-export-controls-restrict-chinas-capability-produce-advanced-semiconductors-military ; Federal Register 2024-28270, https://govinfo.gov/content/pkg/FR-2024-12-05/pdf/2024-28270.pdf). 2025-09-29: the 50% "Affiliates Rule", suspended 2025-11-10 for one year (see Nexperia). [Interpretation, mine]: these rules restrict exports *to* China of advanced chips and tools; they do not restrict a US buyer importing commodity parts. Their effect on a logger maker has come through retaliation (Chinese mineral controls, the Nexperia ban), not through the rules themselves.

**US tariffs on Chinese components** [independent: Sheppard Mullin via National Law Review, 2026-01-16, https://natlawreview.com/article/blank-slate-or-bargaining-chip-additional-section-301-tariffs-chinese , fetched]:
- 2018-08-23: the first Section 301 action "resulted in a 25% tariff on Chinese semiconductors, which took effect August 23, 2018." (Other component headings, such as capacitors and resistors, fell under the 2018–2019 Section 301 lists at 25% or 7.5%; list assignments by HTS heading not checked here, UNVERIFIED.)
- 2025-01-01: after the statutory review, the semiconductor rate rose to 50%: "The increase took effect on January 1, 2025." Covered subheadings (18): 2804.61.00, 3818.00.00, 8541.10.00, 8541.21.00, 8541.29.00, 8541.30.00, 8541.49.10, 8541.49.70, 8541.49.80, 8541.49.95, 8541.51.00, 8541.59.00, 8541.90.00, 8542.31.00, 8542.32.00, 8542.33.00, 8542.39.00, 8542.90.00 (diodes, transistors, transducers, ICs, high-purity silicon).
- 2025-12-23: a second Section 301 action on Chinese legacy semiconductors set an additional rate of 0%, rising on 2027-06-23 "to a rate that will be announced in the future"; "the additional tariff will not apply to derivative articles". (Also https://www.strtrade.com/trade-news-resources/tariff-actions-resources/301-tariffs-china-semiconductors .)
- 2025 IEEPA tariffs ("fentanyl" tariffs on China, Canada and Mexico; worldwide "reciprocal" tariffs) were held unlawful on 2026-02-20 in Learning Resources v. Trump: IEEPA "does not authorize the President to impose tariffs"; Section 232 and Section 301 tariffs remain; refunds likely but procedure not set by the Court [independent: DLA Piper, 2026-02-24, https://www.dlapiper.com/insights/publications/2026/02/us-supreme-court-holds-ieepa-does-not-authorize-tariffs , fetched]. A 10% Section 122 tariff on most imports took effect 2026-02-24 for 150 days (same source) and expired 2026-07-24 (AP, 2026-07-16, https://www.ttnews.com/articles/trump-tariffs-expire-july-24). Replacement Section 301 duties of 10% and 12.5% on about 60 economies: AP on 2026-07-16 reported them as proposed and not yet imposed; Z2Data on 2026-07-28 reported they "took effect the same moment the Section 122 duties expired," with the EU and Taiwan capped at 10% and Japan, South Korea and Switzerland at 12.5% (https://www.z2data.com/insights/how-the-termination-of-section-122-tariffs-impacts-your-supply-chain). The two sources disagree on whether they took effect; UNVERIFIED against the Federal Register.
- 2026-01-15: Section 232 Proclamation 11002 imposed 25% on a narrow class of advanced AI chips only (EY, https://taxnews.ey.com/news/2026-0209 ; search summary). Not relevant to logger parts as described.
- Since US customs origin for an IC follows the wafer-fab or WLP front-end country (A1), a TI or ADI chip fabbed in the US and assembled in China is not Chinese-origin for these tariffs, while a part fabbed in China is, wherever it was packaged [interpretation from the CBP rulings above; a case-by-case question].

**Thailand floods, 2011** [independent: AFP via Phys.org, 2011-11-18, https://phys.org/news/2011-11-thai-ripple-global-chain.html ; IEEE Spectrum, Joshua J. Romero, 2012-11-01, https://spectrum.ieee.org/computing/hardware/the-lessons-of-thailands-flood ; both fetched]. Severe flooding from October 2011 in the Ayutthaya industrial zone about 80 km upriver of Bangkok; "Thai factories supply about 40 percent of the world HDD market"; more than 400 Japanese companies had suspended operations or cut output by late October. Western Digital's Bang Pa-In plant took "nearly 2 meters of water"; its first drive came off the line 46 days after the flood and full capacity took about two more months; recovery cost "in the hundreds of millions of dollars." Western Digital built a 3 m wall, kept the Thai cluster, and began production in Penang, Malaysia. Component makers: a search summary of a November 2011 list says Rohm "partially resumed operations and aim[ed] for full recovery of all products by February" (https://circuitsassembly.com/ca/editorial/menu-news/20350-thailand-flooding-update.html ; UNVERIFIED by direct fetch). This was a regional physical event in a country that kept exporting; supply returned within months.

### A3. Practical policies and Digi-Key country-of-origin data

**Digi-Key country of origin (COO)** [company statements by Digi-Key TechForum staff; no official help page found]:
- Not shown on the product detail page. A TechForum guide, "How to view Country Of Origin (COO) with DigiKey myList" (https://forum.digikey.com/t/how-to-view-country-of-origin-coo-with-digikey-mylist/59804), says: click "Add to List" on the product page (login required); the COO then appears beside the item in the myList view. Staff pointed to this guide as recently as 2026-03-19 (https://forum.digikey.com/t/where-can-i-find-out-which-country-each-product-is-manufactured/66803).
- Staff caution that "Country of Origin is batch specific and subject to change," and that myList COO "might not be accurate" for past orders; for parts already bought, COO is on the invoice and packing slip (myDigiKey > Orders); otherwise ask orders@digikey.com. (Search summaries of https://forum.digikey.com/t/country-of-origin/68326 and related threads; exact wording UNVERIFIED by direct fetch.)
- Barcode labels carry COO as an ISO 3166 two-letter code (https://www.digikey.com/en/resources/quality).
- Practical consequence: a BoM-level COO check is possible by putting the whole BoM in a myList, but the value describes current stock, not what will ship next time; the packing slip is the record of what was actually received.

**Digi-Key PCN and lifecycle data** [company claims]:
- Registered users get "direct access to Manufacturer Product Change Notices on parts you have ordered in the past three years" (https://digikey.com/en/help/why-register ; search summary).
- End-of-life email alerts: enable under My DigiKey > Preferences; the alert fires only if "you must have a DigiKey invoice with the EOL part on it and the manufacturer's part change notice/EOL has to have been sent to DigiKey after your order has been processed"; EOL status for a part not yet bought is under "Documents & Media" on the product page (TechForum guide, https://forum.digikey.com/t/how-to-implement-automatic-notifications-for-end-of-life-parts-a-step-by-step-guide/42860 ; search summary).
- The Product Information v4 API has a ProductChangeNotifications endpoint (https://developer.digikey.com/products/product-information-v4/productchangenotifications).
- The industry standards behind PCNs [independent, via search summaries]: J-STD-046 (JEDEC/ECIA) requires notice "at least 90 days prior to the planned first shipment" of a changed product; J-STD-048 covers product discontinuance (cited on Altera's quality page, https://www.altera.com/quality/pcn-pdn-adv). Last-time-buy windows under J-STD-048 were not confirmed; UNVERIFIED.

### A4. Which countries' suppliers kept shipping (synthesis of A2; dated facts only, interpretation marked)

| Event | Dates | Where supply stopped | What stopped it | Export policy change by the producing country? |
|---|---|---|---|---|
| Thailand floods | Oct 2011 – early 2012 | Thailand (Ayutthaya) | Physical flooding | No |
| Japan earthquake/tsunami | Mar 2011 | Japan | Physical damage, power | No |
| Japan–Korea materials controls | 2019 | Japan to Korea | Japanese export licensing | Yes (Japan) |
| MLCC shortage | 2018–2020 | Global (Japan-led makers) | Demand, capacity shifted to high-value parts, legacy EOL | No |
| Taiwan substrate fires | Oct 2020, Feb 2021 | Taiwan | Fires | No |
| Texas winter storm | Feb–Mar 2021 | US (Austin) | Grid failure | No |
| Renesas Naka fire | Mar–Jul 2021 | Japan | Fire | No |
| Malaysia lockdowns | Jun–Sep 2021 | Malaysia (back end) | Public-health capacity limits | No |
| Ga/Ge controls | Aug 2023 – (US ban suspended to 2026-11-27) | China | Chinese export licensing, US-specific ban | Yes (China) |
| US export controls | Oct 2022 onward | US to China | US licensing | Yes (US), outbound |
| Nexperia | Oct–Nov 2025 | China (Dongguan back end) | Chinese export ban after Dutch seizure | Yes (China) |
| US tariffs | 2018 onward | China-origin parts to US | Price, not availability | Import side (US) |

[Interpretation, mine, offered as hypothesis for Andy]: in the dated record above, every case where a producing country's *government* stopped parts or materials leaving was China (2023 metals, 2024 US ban, 2025 Nexperia), with Japan in 2019 as the one non-Chinese case (and that was aimed at Korea). Japan, Taiwan, Korea, Malaysia, Thailand, the Philippines, the EU and the US lost output to physical events and to COVID rules but did not restrict exports of finished components to US buyers. Mexico, Vietnam and the Philippines did not appear in any dated disruption found here; that is thin evidence, not a clean record. Physical concentration (one fab, one flood plain, one country's back end) caused the longest outages: about four months for Renesas, about three months for Western Digital, weeks for Malaysia.

## Part B: workers' rights frameworks

### B1. Responsible Business Alliance

**Member list, fetched 2026-11-11** [independent: RBA's own register] – https://www.responsiblebusiness.org/about/members/ . The page shows no as-of date (footer "© 2026"). Tiers on the page: [F] Full, [R] Regular, and no bracket (tier not shown on the page; see B1 tier notes for what that means).

Watch-list companies present on the page: Murata [R]; TDK Group (no tier); Vishay Intertechnology [R]; Panasonic Holdings (no tier); KYOCERA AVX Components (no tier) and KYOCERA Corporation (no tier); Bourns (no tier); TE Connectivity (no tier); Molex [R]; Amphenol (no tier); Texas Instruments [R]; Analog Devices [R]; Microchip [F]; STMicroelectronics [F]; Infineon [R]; NXP [F]; onsemi [F]; Nexperia (no tier); Toshiba Corp. (no tier); Renesas [R]; Seiko Epson [R].

Watch-list companies NOT on the page: Taiyo Yuden, Samsung Electro-Mechanics (Samsung Electronics, Samsung SDI and Samsung Display are listed, not SEMCO), Yageo, KEMET, Walsin, Würth Elektronik, JST, Hirose, Phoenix Contact, Diodes Inc, Rohm, Digi-Key. Absence from the list is checked against the page only; individual follow-ups are below.

**Tier notes** [independent: RBA]. The members page legend reads: "Full and Regular members are designated by an "F" or "R" following their company names below" and states the four categories are Full, Regular, Affiliate and Supporter; it does not say how Affiliate and Supporter entries are marked. The unmarked entries above are therefore Affiliate or Supporter (inferred from the legend, not stated per company). The page says "the RBA core membership (not counting initiative-only members) is comprised of more than 250" and "The RBA and its Responsible Minerals, Labor and Factory Initiatives have more than 600 members." Source: https://www.responsiblebusiness.org/about/members/ (fetched 2026-11-11).

Requirements per tier, quoted from the RBA help center, https://help.responsiblebusiness.org/en_US/members-only/understanding-rba-membership-types (undated; footer © 2026):
- Supporter: "Support the overall mission/vision of the RBA"; letter of commitment; NDA; "Pay Annual Dues: ($35,000 - $45,000 depending on company size)".
- Affiliate: "Senior executive commitment to the RBA Code of Conduct"; "Public commitment on the company website"; "Submission of a corporate Self-Assessment Questionnaire (SAQ)".
- Regular: "Complete a risk profile and audit plan"; "Meet sharing requirements"; "Accept VAP audits from other members"; "Close all disqualifying priority findings".
- Full: "Verify all requirements"; "Publish corporate responsibility data".

What this means for a buyer: only Regular and Full membership commits a company to an audit plan and to closing priority findings. An unmarked (Affiliate/Supporter) member such as TDK, Panasonic, KYOCERA AVX, Bourns, TE, Amphenol, Nexperia or Toshiba has, at minimum, a signed commitment and an SAQ; the page does not show which.

**Validated Assessment Program (VAP)** [independent: RBA]. "The Validated Assessment Program (VAP) is the RBA's flagship assessment," covering labor, health and safety, environment, ethics and management systems against the Code's criteria; it is conducted by "RBA-approved, independent third-party firms"; "Each finding carries a defined severity rating and a remediation timeline"; the report is "available in RBA-Online." Source: https://www.responsiblebusiness.org/vap/about-vap/ (fetched 2026-11-11). (The RBA's help center calls it the "Validated Audit Process": https://help.responsiblebusiness.org/vap/vap_audit_steps .) Recognition tiers as described by an approved audit firm: Platinum = VAP score at least 200 with all Priority, Major and Minor findings closed; Gold = 180 with Priority and Major closed; Silver = 160 with Priority closed; only full manufacturing VAPs are eligible. Source: https://www.dqsglobal.com/intl/certify/rba-audit [independent, but an audit vendor; not confirmed on an RBA page this session – UNVERIFIED against RBA].

**How to look up a member and its audit status.** Membership: the public list above. Audit status: VAP reports are held in RBA-Online and shared with the audited facility and the customers it chooses; I found no public per-facility audit database. A small buyer cannot look up an audit result directly; the practical route is to ask the supplier for its VAP recognition level or audit summary for the specific factory. Some companies publish their own recognition results in sustainability reports [company claims, which vary].

**Raw-HTML confirmation.** The members page was also downloaded (42,853 bytes) and its text grepped for each watch-list name, so absence is not an artifact of a summarizer: Yageo, KEMET, Taiyo, Walsin, Würth, JST, Hirose, Phoenix, Diodes, ROHM, Digi-Key, Mouser and Avnet return no match; "Samsung" matches only Samsung Display, Samsung Electronics (R) and Samsung SDI (R).

**Follow-ups on companies absent from the list (code adoption is not membership):**
- Samsung Electro-Mechanics [company claim]: press release dated 2023-07-12 says it "joined the Responsible Business Alliance (RBA)" and will "actively participate in the RBA VAP Audit" at domestic and overseas sites. https://m.samsungsem.com/global/newsroom/news/view.do?id=6941 . It is not on the RBA list fetched 2026-11-11. Either it has left, or it is listed under another name; UNVERIFIED which.
- Yageo/KEMET [company claim]: KEMET's Human Rights Policy says "In 2008, we adopted the Responsible Business Alliance (RBA) Code of Conduct ... which has been fully integrated into our YAGEO Group Global Code of Conduct." https://www.kemet.com/content/dam/kemet/lightning/documents/kemet-docs/Human-Rights-Policy.pdf . Code adoption, not membership; neither name is on the RBA list.
- Würth Elektronik eiSos [company claim]: compliance page says its guidelines include the RBA Code "which we expressly commit ourselves to comply with"; its principles declaration says it signed the Code voluntarily in 2013; a signed RBA Code v8.0 conformity declaration is at https://we-online.com/files/pdf1/v8_en_konformitaetserklaerung-rba_we-group_signed.pdf . Sources: https://www.we-online.com/en/company/legalinformation/compliance , https://www.we-online.com/files/pdf1/declaration-of-principles.pdf . Not an RBA member.
- Diodes Inc [company claim]: its CSER Supplier Code of Conduct (DIC-1005 R6, dated 2025-03-10) is "based on the Responsible Business Alliance ("RBA") Code of Conduct". https://www.diodes.com/assets/Sustainability-Site-Assets/DIC_1005_R6_CSER_Supplier_Code_of_Conduct_.pdf . Not an RBA member.
- ROHM [company claim]: its supply-chain guidelines cite the RBA Code among reference standards. https://fscdn.rohm.com/en/company/sustainability/supply-chain/communication/ROHMGroupSupplyChainManagementGuidelines_en.pdf . Not an RBA member.
- Taiyo Yuden, Walsin, JST, Hirose, Phoenix Contact: no RBA statement found in one search each; thin evidence, not a finding of absence of policy.

Distributors on the list for comparison: Arrow Electronics (no tier). Digi-Key is not listed.

### B2. KnowTheChain ICT benchmark

**2025 edition** [independent: KnowTheChain, a Business & Human Rights Resource Centre project]. Published 2025-04-02 (briefing page: https://www.business-humanrights.org/en/from-us/briefings/2025-knowthechain-ict-benchmark/). Assesses the 45 largest ICT companies on efforts to address forced labor in their supply chains, scored 0–100. The average ICT company "scored just 20/100". Scores below are pasted from the ranking chart on page 5 of the Key Findings Report, https://www.business-humanrights.org/documents/41810/KTC_2025_ICT_Key_findings_report.pdf (downloaded and text-extracted 2026-11-11):

| Company (watch list) | 2025 score /100 |
|---|---|
| NXP Semiconductors | 36 |
| STMicroelectronics | 20 |
| Texas Instruments | 12 |
| Microchip Technology | 11 |
| Analog Devices | 11 |
| Panasonic | 10 |
| Murata Manufacturing | 10 |
| Infineon Technologies | 8 |
| Amphenol | 8 |
| Kyocera | 6 |

Benchmark context from the same chart: Samsung Electronics 61 (top), HPE 53, Cisco 51, BOE Technology 0 (bottom). Samsung Electronics is not Samsung Electro-Mechanics; SEMCO is not assessed. Not assessed in 2025: TDK, Taiyo Yuden, SEMCO, Yageo/KEMET, Vishay, Walsin, Würth, Bourns, TE, Molex, JST, Hirose, Phoenix Contact, onsemi, Nexperia, Diodes, Rohm, Toshiba, Renesas, Epson, Digi-Key.

Findings in the same report that name watch-list companies:
- Page 6: "On 27 December [2024], 251 Bangladeshi workers filed an OECD complaint with the Japanese National Contact Point against Panasonic and Sony, the primary two companies reported to be buying from Kawaguchi [Manufacturing]," a plastics factory in Malaysia where workers reported in August 2024 not being paid for up to six months, seven-day weeks, and recruitment fees. [independent: KnowTheChain reporting worker accounts]
- Page 6: Transparentem's February 2025 investigation and Peter Bengtsen's March 2025 investigation into Taiwanese electronics facilities supplying "companies including Amazon, Broadcom, Motorola Solutions, Panasonic and Sony"; endnote 3: "Transparentem says Broadcom, Panasonic and Sony did not respond". [independent]
- Key findings section: all 45 companies were also assessed in 2022. "seven companies newly disclosed board oversight of supply chain forced labour policies" including Infineon; "six companies disclosing how they conduct a human rights risk assessment for the first time" including Analog Devices, Infineon and Kyocera. 58% of companies adopted RBA Code version 8.
- Regional performance: the seven European companies, including Infineon, NXP and STMicroelectronics, "saw an average score drop of five points" since 2022; "US companies saw the largest score drops, falling by seven points on average."
- Grievance mechanisms: "Only 13% of companies (Apple, Dell, HP, NXP, Samsung and Walmart) disclosed how they communicated their grievance mechanism to workers".

**2022 edition** [independent: KnowTheChain]. 60 companies; report at https://www.business-humanrights.org/documents/38423/KTC_2022_ICT_Benchmark_Report.pdf (26 pages, downloaded and text-extracted 2026-11-11); briefing https://www.business-humanrights.org/en/from-us/briefings/2022-knowthechain-ict-benchmark/ . Scores pasted from the "2022 ranking" chart on page 5 (top: HPE 63):

| Company (watch list) | 2022 score /100 |
|---|---|
| NXP Semiconductors | 39 |
| STMicroelectronics | 29 |
| Texas Instruments | 21 |
| Microchip Technology | 14 |
| Murata Manufacturing | 13 |
| Analog Devices | 13 |
| Amphenol | 12 |
| TE Connectivity | 11 |
| Infineon Technologies | 11 |
| Renesas Electronics | 11 |
| Panasonic Holdings | 9 |
| Kyocera | 3 |

TE Connectivity and Renesas were assessed in 2022 and not in 2025. Not assessed in either edition: TDK, Taiyo Yuden, SEMCO, Yageo/KEMET, Vishay, Walsin, Würth, Bourns, Molex, JST, Hirose, Phoenix Contact, onsemi, Nexperia, Diodes, Rohm, Toshiba, Epson, Digi-Key (grep of both text extractions). The 2022 and 2025 scores are in the same methodology family but the 2025 report notes changed expectations; treat the drop for most companies as KnowTheChain's own comparison, not a re-scored series.

Named finding in the 2022 report (page 10): "It was reported that over a number of months, 19 workers at STMicroelectronics Malaysia (supplier to companies such as Apple, Cisco, and HP) died from Covid-19." [independent: KnowTheChain citing reporting; underlying source not opened this session]

### B3. CHRB, Electronics Watch, BHRRC

**Corporate Human Rights Benchmark (CHRB)** [independent: World Benchmarking Alliance]. ICT manufacturing was a CHRB sector in the 2019, 2020 and 2022 rounds; the 2023 round covered 110 apparel and extractives companies only (https://www.worldbenchmarkingalliance.org/research/2023-corporate-human-rights-benchmark). The 2022 dataset: https://archive.worldbenchmarkingalliance.org/research/2022-corporate-human-rights-benchmark-data-set/ (scores for individual watch-list companies not extracted this session). A search summary reported Murata at 19.4/100 in CHRB 2022, and Infineon 13.5 and Texas Instruments 8.1 in a CHRB ICT ranking of unstated year: all UNVERIFIED, because the Murata scorecard URL (assets.worldbenchmarkingalliance.org) redirected to an unrelated domain, which I did not follow, and the current WBA ranking page now shows the 2026 Benchmark Hub with only the top five per benchmark. The 2026 CHRB covers 105 companies chosen from those previously assessed (https://www.worldbenchmarkingalliance.org/research/the-methodology-for-the-2026-corporate-human-rights-benchmark); whether any watch-list company is among them is not checked. Evidence here is thin; KnowTheChain is the better-documented benchmark for this sector.

**Electronics Watch: Possehl Electronics, Melaka, Malaysia** [independent: Electronics Watch case study dated Jan 2022, https://electronicswatch.org/impact-story-courageous-migrants-self-organise-to-get-out-of-forced-labour_2605497.pdf ]. "Brands: NXP Semiconductors, ST Micro, Infineon, Vishay"; products "Mechatronic parts for semiconductor, LED & automotive industries"; "Time: April 2019 – Nov 2021". Migrants employed via an unlicensed outsourcing agency (JS Global Services) documented "high fees charged for work permits, passport confiscation, late wages, illegal wage deductions and excessive overtime"; Electronics Watch "corroborated their claims of violent threats from the agency, all indicators of forced labour." Outcome: buyers and the RBA "were quick to act": reimbursements, late wages paid, the agency barred; "RBA itself compensated" workers who had returned home and committed to cover regularization costs. Electronics Watch's criticism: reimbursements "appeared to be based on out-of-date minimum-wage calculations" and the workers were not party to the remediation. Note this is a supplier to the brands (a tier-1 or tier-2 parts maker), not the brands' own fabs, and it is an example of the RBA remedy process working, with stated limits.

**Danwatch, "Forced labour behind your screen" (June 2019), Malaysian component factories** [independent: Danwatch, via BHRRC page dated 2019-07-15, https://www.business-humanrights.org/en/latest-news/malaysia-investigation-reveals-forced-labour-migrant-worker-abuses-at-factories-producing-for-electronics-brands-incl-co-responses/ ]. Brands named: "Infineon, Possehl, ST Micro, NXP, Panasonic, Toshiba, Vishay and Texas Instruments." Allegations: "excessive recruitment fees and forced labour, violent threats, passport confiscation and illegal wage deductions." BHRRC invited NXP, Texas Instruments and Vishay to respond in July 2019: NXP responded 2019-07-11 (working with Possehl and industry on "the repayment of fees and back-wages"); Texas Instruments and Vishay did not respond. Danwatch reported Toshiba would audit on site, Panasonic would "consider" a deeper survey, and Infineon, Possehl and ST Micro were investigating. This appears to be the same Possehl case that Electronics Watch then followed to remedy (above).

**ASPI, "Uyghurs for Sale" (Policy Brief 26/2020, March 2020)** [independent: Australian Strategic Policy Institute; read from a mirror copy at https://let.iiec.unam.mx/sites/let.iiec.unam.mx/files/Uyghurs%20for%20sale.pdf , original at https://www.aspi.org.au/report/uyghurs-sale ]. ASPI identified "83 foreign and Chinese companies directly or indirectly benefiting from the use of Uyghur workers outside Xinjiang through potentially abusive labour transfer programs as recently as 2019"; the list includes watch-list names Panasonic, TDK and Toshiba (and Samsung, meaning Samsung Electronics). "Adidas, Bosch and Panasonic, said they had no direct contractual relationships with the suppliers implicated ... but no brands were able to rule out a link further down their supply chain." Appendix (report p. 33): 105 Uyghur workers were transferred on 2018-05-17 to Hubei Yihong Precision Manufacturing, a subsidiary of Dongguan Yidong Electronic, which "says they supply directly to BYD, Goertek, Mitsumi, TDK and Toshiba" and whose "LCD components are directly supplied to Kyocera". The link is a supplier's own claimed customer list, not a finding against the brands' factories.

**Panasonic: Kawaguchi Manufacturing, Malaysia** [independent: OECD Watch case record, https://www.oecdwatch.org/complaint/employees-of-kawaguchi-manufacturing-vs-kawaguchi-manufacturing-sony-and-panasonic/ ; BHRRC tracker, https://www.business-humanrights.org/de/neuste-meldungen/update-panasonic-disclosure-re-allegations-of-labour-rights-abuse-of-bangladeshi-workers-at-malaysian-supplier (German-locale URL of the English item, as found) ]. Complaint filed 2024-12-27 at Japan's OECD National Contact Point by 251 workers against Kawaguchi, Sony and Panasonic, alleging non-payment of wages, passport confiscation, intimidation and recruitment fees; OECD Watch lists it as "Filed" (no final NCP statement found). Panasonic [company claim, via BHRRC] said it was "proportionally reimbursing the recruitment fees" and had asked Kawaguchi to correct violations. Kawaguchi is a plastics supplier; this concerns Panasonic's group supply chain generally, and I found no link to Panasonic's component (capacitor, resistor) factories specifically.

### B4. Conflict minerals

**The rule** [independent: SEC]. Dodd-Frank section 1502, implemented as Exchange Act Rule 13p-1 and Form SD, requires SEC registrants whose products need tin, tantalum, tungsten or gold (3TG) to file an annual Form SD by May 31. On 2017-04-07 the SEC Division of Corporation Finance said it "will not recommend enforcement action to the Commission if companies" file only under Items 1.01(a) and (b) of Form SD, that is, without the full Conflict Minerals Report of Item 1.01(c); the statement "expresses the Division's position on enforcement action only." https://www.sec.gov/news/public-statement/corpfin-updated-statement-court-decision-conflict-minerals-rule . Many filers still attach a full Conflict Minerals Report voluntarily.

**Who files, checked on EDGAR 2026-11-11** [independent: SEC EDGAR submissions API, https://data.sec.gov/submissions/CIK##########.json , counting form type "SD" within each company's recent-filings window]. Latest Form SD filing date:

| Company | CIK | Latest Form SD |
|---|---|---|
| Texas Instruments | 97476 | 2026-06-01 |
| Analog Devices | 6281 | 2026-05-22 |
| Microchip | 827054 | 2026-05-28 |
| STMicroelectronics | 932787 | 2026-05-12 |
| NXP | 1413447 | 2026-05-28 |
| onsemi | 1097864 | 2026-05-18 |
| Vishay | 103730 | 2026-05-28 |
| Amphenol | 820313 | 2026-05-29 |
| TE Connectivity | 1385157 | 2026-05-29 |
| Diodes Inc | 29002 | 2026-05-28 |
| Kyocera | 57083 | 2018-05-30 (none since) |
| Infineon | 1107457 | none (ADR, not a Form SD filer) |
| Murata | 1450468 | none (ADR, not a Form SD filer) |
| Arrow Electronics (distributor) | 7536 | 2026-05-27 |
| Avnet (distributor) | 8858 | 2026-05-29 |

Not SEC registrants, so no Form SD (by listing status; only Infineon, Murata and Kyocera were checked on EDGAR individually): Japanese, Korean, Taiwanese and European companies without a US listing (Murata, TDK, Taiyo Yuden, SEMCO, Yageo/KEMET since the 2020 acquisition, Walsin, Panasonic, Rohm, Toshiba, Renesas, Epson, Infineon), privately held companies (Würth, Bourns, Molex under Koch, JST, Hirose, Phoenix Contact, Nexperia under Wingtech), and Digi-Key (private). Most of these publish a voluntary conflict-minerals policy and supply CMRTs on request [company claims, not checked one by one]; KEMET's May 2024 Conflict Minerals Report is an example: https://www.kemet.com/content/dam/kemet/lightning/documents/kemet-docs/KEMET-Conflict-Minerals-Report-May-2024.pdf .

**Responsible Minerals Initiative and the CMRT** [independent: RMI]. The Conflict Minerals Reporting Template is "a free, standardized reporting template developed by the Responsible Minerals Initiative (RMI)" that "facilitates the transfer of information through the supply chain" and feeds RMI's smelter and refiner assurance process; RMI also publishes an Extended Minerals Reporting Template (EMRT, for cobalt and mica per RMI, scope not confirmed on the fetched page). https://www.responsiblemineralsinitiative.org/reporting-templates/cmrt/ . The RMI is an RBA initiative (RBA members page counts RMI among its initiatives). Digi-Key points customers to manufacturers' CMRTs through the ECIA (B5). For a small buyer, the CMRT is the document to request; it is the industry's common format whether or not the maker files with the SEC.

### B5. Digi-Key

- **RBA:** not a member (absent from the member list and the raw-HTML grep, 2026-11-11; see B1). Arrow Electronics is listed (unmarked tier). [independent: RBA list]
- **Conflict minerals** [company claim]: the sustainability page carries a "Conflict Minerals Statement" opening "DigiKey is aware of the Dodd-Frank Consumer Protection Act, Section 1502 regarding Conflict Minerals," and points customers to the ECIA member-company page for manufacturers' CMRTs (https://www.ecianow.org/member-company-information) and to an information-request form. Source: https://www.digikey.com/en/resources/environmental/sustainability (fetched 2026-11-11). Digi-Key is privately held and does not file SEC Form SD (see B4).
- **Supplier code of conduct, human-rights statement, modern-slavery statement:** none found. The full sustainability page (114,074 characters, read in two parts) contains no RBA, supplier-code, labor or human-rights text; a search of the UK modern-slavery registry returned other companies (the registry ID that surfaced, CN9C22xH, is Coilcraft's). Thin evidence: absence from two searches and one page, not proof that no document exists.
- **Quality and traceability** [company claim]: "genuine, manufacturer-warranted, first-quality components"; member of ECIA, CEDA and ECSN; "counterfeit product controls as outlined in the AS6496 standard"; date and lot codes and barcodes support tracing. Country of origin is defined as "Country where the part was manufactured," carried in barcodes as an ISO 3166 two-letter code. Source: https://www.digikey.com/en/resources/quality (fetched 2026-11-11).
- **Country-of-origin disclosure:** see A3. In short, COO is not on the product detail page; it appears in myList after "Add to List" (logged in), and on the invoice and packing slip for parts received.

Side finding for the passives agent [company claim]: Coilcraft's 2025 Modern Slavery and Human Trafficking Statement says its Social Responsibility program "is built around and compliant with the Responsible Business Alliance (RBA) code of conduct" and that suppliers must have an RBA-compliant management system and supply an RMI conflict-minerals letter; production centers in "China, Malaysia, Scotland, Vietnam, and others". https://downloads.modern-slavery-statement-registry.service.gov.uk/pdf-published/CN9C22xH/2026/Modern%20Slavery%20Statement%202025.pdf . Coilcraft is not an RBA member (not on the list).

## Company table

RBA: membership list at https://www.responsiblebusiness.org/about/members/ as fetched 2026-11-11 (tier F = Full, R = Regular, "–" = listed with no tier, which the page legend implies is Affiliate or Supporter). KnowTheChain: ICT benchmark score /100, 2025 edition (45 companies) and 2022 edition (60 companies); "n.a." = not assessed. Allegations: "Yes" only where a named independent source in B3 or B2 names the company or its supply chain; "None found" means none turned up in the searches logged below, which were not an exhaustive search of every company, and is not a clean bill.

| Company | RBA member (2026-11-11) | KnowTheChain 2025 | KnowTheChain 2022 | Documented allegations (source in B2/B3) |
|---|---|---|---|---|
| Murata | Yes (R) | 10 | 13 | None found |
| TDK | Yes (–) | n.a. | n.a. | Yes: ASPI 2020, named among 83 brands; supplier Dongguan Yidong lists TDK as a customer |
| Taiyo Yuden | No | n.a. | n.a. | None found |
| Samsung Electro-Mechanics | No (announced joining 2023-07-12; not on current list) | n.a. | n.a. | None found |
| Yageo / KEMET | No (KEMET adopted RBA Code 2008) | n.a. | n.a. | None found |
| Vishay | Yes (R) | n.a. | n.a. | Yes: Danwatch 2019 (did not respond to BHRRC); Electronics Watch, Possehl Electronics, 2019–2021 |
| Panasonic | Yes (–) | 10 | 9 | Yes: OECD NCP complaint 2024-12-27 (Kawaguchi, Malaysia); ASPI 2020; Danwatch 2019; Transparentem 2025 (named by KnowTheChain) |
| KYOCERA AVX | Yes (–; KYOCERA Corp also –) | 6 (Kyocera Corp) | 3 (Kyocera Corp) | Yes (Kyocera Corp): ASPI 2020 appendix, supplier lists Kyocera as a customer |
| Walsin | No | n.a. | n.a. | None found |
| Würth Elektronik | No (signed RBA Code 2013) | n.a. | n.a. | None found |
| Bourns | Yes (–) | n.a. | n.a. | None found |
| TE Connectivity | Yes (–) | n.a. | 11 | None found (BHRRC profile lists "Other allegations" N/A, per search summary) |
| Molex | Yes (R) | n.a. | n.a. | None found |
| Amphenol | Yes (–) | 8 | 12 | None found |
| JST | No | n.a. | n.a. | None found |
| Hirose | No | n.a. | n.a. | None found |
| Phoenix Contact | No | n.a. | n.a. | None found |
| Texas Instruments | Yes (R) | 12 | 21 | Yes: Danwatch 2019 (did not respond to BHRRC) |
| Analog Devices | Yes (R) | 11 | 13 | None found |
| Microchip | Yes (F) | 11 | 14 | None found |
| STMicroelectronics | Yes (F) | 20 | 29 | Yes: Danwatch 2019; Electronics Watch, Possehl; KnowTheChain 2022 reports 19 Covid-19 deaths at ST Malaysia |
| Infineon | Yes (R) | 8 | 11 | Yes: Danwatch 2019; Electronics Watch, Possehl |
| NXP | Yes (F) | 36 | 39 | Yes: Danwatch 2019 (responded 2019-07-11); Electronics Watch, Possehl |
| onsemi | Yes (F) | n.a. | n.a. | None found |
| Nexperia | Yes (–) | n.a. | n.a. | None found (labor); export-continuity case in A2 |
| Diodes Inc | No (supplier code based on RBA Code) | n.a. | n.a. | None found |
| Rohm | No | n.a. | n.a. | None found |
| Toshiba | Yes (–) | n.a. | n.a. | Yes: ASPI 2020, named among 83 brands; Danwatch 2019 named |
| Renesas | Yes (R) | n.a. | 11 | None found |
| Epson (Seiko Epson) | Yes (R) | n.a. | n.a. | None found (not searched individually) |
| Digi-Key | No | n.a. | n.a. | None found |

Reading the table [interpretation, mine]: the allegation column tracks who has been investigated as much as who has done wrong. The firms with "Yes" are the large brands with Malaysian or Chinese supplier networks that NGOs have examined (Danwatch, Electronics Watch, ASPI); the Japanese and Taiwanese passives makers and the private connector makers were mostly not assessed by any benchmark, which is an absence of scrutiny rather than evidence of good practice. Several "Yes" cases (NXP, Infineon, ST, Vishay at Possehl) ended in documented remedy through the RBA.

## Practical sourcing policies for a small buyer

Each tied to the evidence above; the thresholds are for Andy to set.

1. **Approve two sources per position, and make them differ in back-end country, not just brand.** Evidence: Malaysia 2021 stopped ST Muar for 11 days and Infineon's plants for weeks (A2); Nexperia 2025 stopped a European brand because its back end was in Dongguan (A2); SIA/BCG puts 58% of ATP capacity in China and Taiwan and ~20% in Southeast Asia (A1). Two brands assembled in the same country share the same failure.
2. **Hold buffer stock of the long-lead and single-source parts, not of everything.** Evidence: the outages that hurt were months long (Renesas fire to shipment recovery about four months; Western Digital about three months; MLCC lead times of 52–99 weeks in 2018, A2). How many months of builds to hold is a parameter for Andy.
3. **Record country of origin from the packing slip at receipt, per lot.** Evidence: Digi-Key says COO "is batch specific and subject to change," shows it in myList and on invoices and packing slips, not on the product page (A3). US customs origin for an IC follows the front-end country (CBP ruling N352561, A1), so the label alone does not tell you where the part was assembled.
4. **Subscribe to PCN and EOL alerts by buying through one account and enabling Digi-Key's EOL notifications; check "Documents & Media" before designing a part in.** Evidence: the alert fires only for parts on an invoice (A3); the 2018 MLCC shortage came with Murata PCNs ending legacy parts, last-time buys from March 2019 (A2); J-STD-046 gives 90 days' notice of a change.
5. **Watch the dated expiry points that are already on the calendar** (facts, not forecasts): China's suspension of its US-specific Ga/Ge/antimony ban runs to 2026-11-27; the US suspension of the BIS Affiliates Rule ends 2026-11-10 "unless BIS takes further action"; the second Section 301 action on Chinese legacy chips rises from 0% on 2027-06-23 (A2).
6. **For labor, prefer RBA Regular or Full members where a choice exists, and ask suppliers for the VAP recognition level of the specific factory.** Evidence: only Regular and Full membership commits a company to an audit plan and closing priority findings; Affiliate and Supporter tiers need only a commitment and an SAQ (B1); VAP reports are not public (B1). The Possehl case shows the RBA route producing remedy, with limits (B3).
7. **Request CMRTs from makers that do not file Form SD.** Evidence: US-listed makers file Form SD annually (B4 table); the Japanese, Taiwanese and private makers do not, and the RMI CMRT is the free common format (B4).

## Open questions

- Samsung Electro-Mechanics announced RBA membership on 2023-07-12 but is not on the 2026-11-11 list: lapsed, renamed, or a list error? (Ask SEMCO or RBA.)
- The tier of each unmarked RBA member (TDK, Panasonic, KYOCERA AVX, Bourns, TE, Amphenol, Nexperia, Toshiba): Affiliate or Supporter? The public page does not say.
- CHRB company scores (2022 and 2026 editions) for the watch list were not extracted; the WBA scorecard link redirected to an unrelated domain.
- Whether the replacement Section 301 duties of 10–12.5% took effect on 2026-07-24 (Z2Data) or were still proposed (AP, 2026-07-16), and how they apply to China; and the HTS list assignment of capacitors, resistors and connectors under the 2018–2019 Section 301 lists.
- Nexperia's status after December 2025 (court hearing reported for January 2026).
- Country-level production shares for MLCCs, resistors, connectors and crystals: only headquarters and sales shares were found; the paid Paumanok, Bishop and QYResearch reports were not accessible.
- The DAO fab-capacity row in A1 should be read off the SIA/BCG chart image to confirm the column assignment.
- Whether manufacturers' own COO labels follow the CBP front-end rule, the EU rule, or assembly country; a sample of Digi-Key packing slips against datasheet COO statements would answer it for Northern Widget's own BoM.
- Labor allegations were searched by cluster (Malaysia, ASPI, BHRRC), not company by company; Taiyo Yuden, Walsin, JST, Hirose, Phoenix Contact, Rohm, Epson, onsemi and Microchip each deserve one dedicated BHRRC profile check.

## Sources checked (including dead ends)

- 2026-11-11 https://www.responsiblebusiness.org/about/members/ – full member list read; productive.
- 2026-11-11 https://www.business-humanrights.org/documents/41810/KTC_2025_ICT_Key_findings_report.pdf – 18-page PDF, ranking on p. 5; productive.
- 2026-11-11 https://www.business-humanrights.org/documents/38423/KTC_2022_ICT_Benchmark_Report.pdf – 2022 ranking p. 5; productive.
- 2026-11-11 Electronics Watch Possehl PDF – text extracted; productive.
- 2026-11-11 search CHRB 2023 ICT – dead end (2023 round had no ICT sector).
- 2026-11-11 search Electronics Watch + TI/onsemi Malaysia – no case naming TI or onsemi found.
- 2026-11-11 BHRRC Danwatch 2019 page – productive.
- 2026-11-11 search ASPI 'Uyghurs for Sale' (2020) – the 83 named firms are brands and Chinese assemblers; Panasonic named as saying it had no direct contract; no other watch-list component maker confirmed in results (full ASPI list not opened).
- 2026-11-11 search Malaysia 2023–24 investigations naming onsemi, Microchip, Renesas, Kyocera – nothing found.
- 2026-11-11 Murata CHRB 2022 scorecard PDF – redirected to an unrelated domain (awkwardconversation.org); not followed; dead end.
- 2026-11-11 WBA CHRB ICT ranking page (current and archive) – now the 2026 Benchmark Hub, top five only; dead end for company scores.
- 2026-11-11 ASPI 'Uyghurs for Sale' PDF (UNAM mirror) – text extracted and grepped; Panasonic, TDK, Toshiba on the 83-company list; Kyocera in appendix; productive.
- 2026-11-11 Digi-Key sustainability page (two parts), quality page, TechForum COO threads – productive.
- 2026-11-11 search Digi-Key modern slavery / supplier code – nothing found; UK registry hit CN9C22xH was Coilcraft (dead end for Digi-Key, side finding recorded).
- 2026-11-11 SEC EDGAR submissions JSON for 15 CIKs – productive. (Count of SD filings is limited to the API's recent window; latest dates are reliable.)
- 2026-11-11 SEC 2017-04-07 Corp Fin statement – productive.
- 2026-11-11 RMI CMRT page – productive but sparse (no version or mineral list on page).
- 2026-11-11 SIA/BCG May 2024 report PDF – productive (Exhibits 2 and 6, p. 20 ATP text). SIA/BCG April 2021 report also downloaded for disruption context.
- 2026-11-11 CBP origin rulings via search and the open-gov.usebase.io mirror (N352561 confirmed); tarifflens.ai mirror 403.
- 2026-11-11 MLCC market-share searches – mostly paid market-research blurbs (gminsights, marketsandmarkets, gii.tw): dead ends; Murata corporate page and Passive Components Blog fetched.
- 2026-11-11 resistor, connector, crystal market-share searches – paid-report blurbs only, except the Bishop top-10 article (fetched).
- 2026-11-11 escatec Oct 2018 market review – page now shows only 2025–26 teasers; dead end.
- 2026-11-11 Renesas UPDATE 10 (businesswire 403; renesas.com fetched); nippon.com Reuters item 404.
- 2026-11-11 TechXplore (Texas), Transport Topics (Malaysia) – fetched.
- 2026-11-11 CSET MOFCOM Notice 46 translation; SCMP/Yahoo Nexperia timeline – fetched.
- 2026-11-11 searches on Ga/Ge 2023 and Nov 2025 suspension – summaries only (HSF, IEA, Fastmarkets, Evertiq not fetched directly).
- 2026-11-11 natlawreview (Sheppard Mullin), DLA Piper, AP/ttnews, Z2Data, Phys.org, IEEE Spectrum – fetched. ABA Procurement Lawyer fall 2026 – 403 dead end.
- 2026-11-11 members page raw HTML via curl, grepped (scratchpad copy) – confirms absences.
- 2026-11-11 searches for RBA status of Yageo/KEMET, SEMCO, ROHM, Taiyo Yuden, Würth, Diodes, Digi-Key, Hirose/JST/Phoenix/Walsin – results above; Taiyo Yuden, Walsin, JST, Phoenix Contact searches returned nothing on the company.
- 2026-11-11 https://www.tdk.com/en/sustainability/governance/environmental-issues-manufacturing/rba-vap-audit – 403 dead end.
- 2026-11-11 https://www.responsiblebusiness.org/about/membership/ – 404 dead end.
- 2026-11-11 https://help.responsiblebusiness.org/en_US/members-only/understanding-rba-membership-types – tier requirements; productive.
- 2026-11-11 https://www.responsiblebusiness.org/vap/about-vap/ – VAP description; no scoring or recognition thresholds on the page.


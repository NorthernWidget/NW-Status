# Horizontal USB 2.0 Type-C receptacle: second source outside China (Okapi J10 and USB2)

Status: COMPLETE

Agent report, 2026-11-11. Builds on `2026-11-11-usb-c-connector-agent-report.md` (read first; not redone here).

Question: should both Okapi USB ports (J10 and the B-SoM's USB2, moving to the right edge per Project-Okapi #68) use GCT USB4105-GF-A, and is there a footprint-compatible 16-pin USB 2.0 horizontal receptacle assembled outside China to serve as a second source?

Every fact cites its source with the fetch date. UNVERIFIED marks anything not confirmed from a manufacturer or distributor page.

## Sources checked (appended as checked, dead ends included)

- Digi-Key GCT USB4105-GF-A product page https://www.digikey.com/en/products/detail/gct/USB4105-GF-A/11198441 (fetched 2026-11-11): stock and prices re-confirmed; Digi-Key page shows no Country of Origin value.
- Mouser USB4105-GF-A page via WebFetch: timed out (dead end). Mouser via curl: not attempted further (blocked by harness policy).
- WebSearch "USB4105-GF-A country of origin" (2026-11-11): search summary attributes "Mainland China" to Octopart and "China" to element14; element14 page https://my.element14.com/.../dp/3588199 timed out on direct fetch, so this rests on the search-engine summary (see row 1).
- WebSearch "Würth WR-COM USB 2.0 Type C receptacle horizontal 16 pin SMT 632722" (2026-11-11): the 632722 prefix is 24-position or 6-position; the 16-pin USB 2.0 horizontal is 629722000214; 629722330214 is a mid-mount sibling.
- we-online.com/catalog/en/WR-COM_USB_20_TYPE_C_RECEPTACLE_HORIZONTAL_SMT: HTTP 404 (dead end).
- Würth datasheet https://www.we-online.com/components/products/datasheet/629722000214.pdf (revision 002.000, dated 2025-09-04, PDF created 2025-09-04): OK, saved as `2026-11-11-wurth-629722000214-datasheet.pdf`.
- Digi-Key search https://www.digikey.com/en/products/result?keywords=629722000214 (fetched 2026-11-11): OK.
- Octopart USB4105-GF-A: HTTP 403. element14/Farnell/Newark pages (sg, my, de): all timed out on WebFetch (dead end for direct reads; search-engine summaries used instead, flagged). Bürklin: 403. TME search for 629722000214: no product. lioncircuits.com 629722000214: no COO field.

- WebSearch "JAE DX07S016JA1R1500 country of origin" (2026-11-11): search summary reports RS Online (https://my.rs-online.com/web/p/usb-connectors/2017048) "COO (Country of Origin): CN", and OnlineComponents / Master Electronics "COO: CN", HTS 8536694040. Not read directly.
- WebSearch "Molex 2171790001 country of origin" (2026-11-11): no origin found; Molex part page https://www.molex.com/en-us/products/part-detail/2171790001 shows no origin field (per search summary); Digi-Key forum states Digi-Key does not publish COO. Dead end.
- WebSearch "Hirose CX90B-16P ... country of origin" (2026-11-11): search summary reports Farnell full-reel SKU 3587500 (https://ie.farnell.com/hirose-hrs/cx90b-16p/usb-conn-3-1-type-c-r-a-rcpt-16pos/dp/3587500) "Country of Origin: South Korea". Not read directly (element14/Farnell time out).
- Digi-Key CX90B-16P https://www.digikey.com/en/products/detail/hirose-electric-co-ltd/CX90B-16P/13176897 (fetched 2026-11-11): OK.
- Hirose product page https://www.hirose.com/product/p/CL0480-0755-0-00: HTTP 403 (dead end; 2D drawing not retrieved from Hirose).
- Hirose CX90B-16P product specification, RS-hosted https://docs.rs-online.com/1c1d/A700000015681941.pdf (fetched 2026-11-11; footer "Apr.1.2026", rev 4 21.12.16): OK, saved as `2026-11-11-hirose-cx90b-16p-specsheet.pdf`. Issued by "HIROSE KOREA.CO.,LTD PRODUCT SPECIFICATION", DWG ELC4-632698.
- Molex 217179-0001 COO: WebSearch "rs-online Molex 217179-0001 USB Type C COO" (2026-11-11): search summary reports RS UK/SE/DK (RS stock 285-7966, https://uk.rs-online.com/web/p/usb-connectors/2857966) "COO: CN". Direct fetch of RS: 403.
- Digi-Key JAE DX07S016JA3R1500 https://www.digikey.com/en/products/detail/jae-electronics/DX07S016JA3R1500/12354006 (fetched 2026-11-11): OK. JAE product sheet (Digi-Key mirror https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/8893/DX07S016JA3R1500.pdf, a web-page print dated 2026-03-05): "Shell-DIP length 1.2mm, Without rear shield, 16 pos., 1-row SMT", USB 2.0, 5 A, center height 1.58 mm, TID 10724; no land pattern. JAE DX07 slide deck MB_0335E_DX07.pdf: encrypted, no part data (dead end). jae.com topic page: 403.
- Lumberg USB-C search (2026-11-11): only 24-position USB 3.x parts (2436-01, 2436-04); no USB 2.0 16-pin (dead end).
- gct.co/connector/usb4105: 403 (dead end).
- WebSearch for 16-position USB-C receptacles with a Taiwan, Japan or Malaysia origin (extended, 2026-11-11): no hit. Witacon (catalog only, no Digi-Key) not pursued.
- RS-hosted https://docs.rs-online.com/8aa8/A700000015681986.pdf: CX90BW-16P spec sheet (the IPX4 gasket variant), not saved.
- Hirose CX Series Catalog (chipdip mirror https://static.chipdip.ru/lib/883/DOC031883743.pdf, page footer "Aug.1.2022", 25 pages): OK, saved as `2026-11-11-hirose-cx-series-catalog-datasheet.pdf`; page 19 is CX90B-16P with recommended PCB layout.
- XON-hosted Hirose CX catalog (https://xonstorage.z8.web.core.windows.net/pdf/hirose_cx90b16p_apr22_xonlink.pdf; Hirose catalog dated 2018-09): older, does not list CX90B-16P.
- Hirose Americas CX flyer 03/2025 (https://info.hirose.com/hubfs/Hirose%20Americas%20CX%20USB%20Type%20C%20Flyer%20032025.pdf): OK; lists CX90B-16P as Top-Mount, Right-Angle (SMT Single-row), 16 pos., 480 Mbps.
- flux.ai cx90b-16p page: no footprint data (dead end). Mouser CX_catalog.pdf: timed out.

- Digi-Key 12402012E212A https://www.digikey.com/en/products/detail/amphenol-cs-commercial-products/12402012E212A/13683192 (fetched 2026-11-11): OK.
- WebSearch "12402012E212A country of origin Amphenol" (2026-11-11): no origin found (Avnet field blank per summary). Dead end for COO.
- amphenol-cs.com product page and cdn.amphenol-cs.com io_usb_type_c.pdf: HTTP 403 (dead end).
- Amphenol customer drawing C12402012 rev 4 (2020.07.10), Digi-Key mirror https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/2614/C12402012-4.pdf (URL found via https://www.flux.ai/adrian95/12402012e212a.md): OK, saved as `2026-11-11-amphenol-12402012E212A-datasheet.pdf`.

- Molex 2171790001: sales drawing https://www.molex.com/content/dam/molex/molex-dot-com/products/automated/en-us/salesdrawingpdf/217/217179/2171790001_sd.pdf and part page https://www.molex.com/en-us/products/part-detail/2171790001 both timed out (dead end). LCSC https://www.lcsc.com/product-detail/C3197684.html: key attribute "TYPE C 16 PIN TOP MOUNT SMT", -40 to +85 C, no COO; https://www.lcsc.com/datasheet/C3197684.pdf "document link is invalid" (dead end). WebSearch for a mirror of the 2171790001 drawing: none found.
- WebSearch "UJU Electronics USB Type-C 16 pin receptacle Digi-Key": no UJU part on Digi-Key; results were Same Sky UJ20 (dead end for UJU).
- WebSearch Kycon USB-C 2.0 16-pin: Kycon on Digi-Key lists 24-contact (14+10 dummy) THT parts such as KUSBX-SL-CS1N14-B; no 16-pin top-mount USB4105-pattern part found (not pursued further).
- WebSearch TE USB-C 2.0 16-pos right angle: TE 2340901-1 found; Digi-Key search https://www.digikey.com/en/products/result?keywords=2340901-1 shows "USB TYPE C 2.0 CONN REC MID-MOUN..." (mid-mount; not a top-mount drop-in; not pursued).
- Digi-Key search https://www.digikey.com/en/products/result?keywords=2137160001 (Molex 213716-0001): "Through Hole, Right Angle", -30 to 85 C (fails -40 C), 4,589 stock, $1.29000/$1.09700/$0.93260. Rejected on temperature.
- Digi-Key search https://www.digikey.com/en/products/result?keywords=UJ20-C-H-G-SMT (fetched 2026-11-11): 21 Same Sky horizontal USB 2.0 parts; 15 read. -40 C variants: -1A-, -2A-, -3A-, -T-5D-, -T-1D-, and UJ20-C-H-G-SMT-TR; the rest are -25 C.
- Same Sky datasheets https://www.sameskydevices.com/product/resource/uj20-c-h-g-smt-2a-p16-tr.pdf (date 11/03/2025; saved as `2026-11-11-uj20-c-h-g-smt-2a-p16-tr-datasheet.pdf`), .../uj20-c-h-g-smt-1a-p16-tr.pdf (11/03/2025), .../uj20-c-h-g-smt-tr.pdf (09/12/2024, PCB 1.6 mm, PDF metadata names a "USB3.0 ... DIP TYPE" source file), .../uj20-c-h-g-smt-t-5d-p16-tr.pdf (11/04/2025, PCB 1.6 mm, different land pattern: 6.60 peg spacing, 1.20-wide front pads, rear slots 1.50). Not saved except 2A.
- WebSearch "Same Sky CUI Devices UJ20-C-H-G-SMT country of origin" (2026-11-11): e-sonic lists UJ20-C-H-G-SMT-4-P16-TR "COO CN", HTS 8536694040; RS lists sibling UJC-HP-G-SMT-TR "CN" (search summary). No Same Sky part found with a non-China origin.

## Candidate rows (appended as confirmed)

### GCT USB4105-GF-A (baseline)

- Country of manufacture: **China (distributor data)**. WebSearch "USB4105-GF-A country of origin" (2026-11-11): search summary reports Octopart (https://octopart.com/part/gct/USB4105-GF-A) "Country of Origin Mainland China", ECCN EAR99, and element14 (https://my.element14.com/gct-global-connector-technology/usb4105-gf-a/usb-conn-2-0-type-c-rcpt-16pos/dp/3588199) "China", tariff 85366930. Direct fetches: Octopart 403, element14 timed out. Not read by me directly.
- Digi-Key (fetched 2026-11-11): 2073-USB4105-GF-ACT-ND, 263,569 in stock, $0.80000 (1), $0.67600 (10), $0.57450 (100), -40 to 85 C. Datasheet link on Digi-Key: https://gct.co/files/specs/usb4105-spec.pdf. Mating cycles 20,000, 4 through-hole shell stakes 0.95 mm, top mount (earlier report).
- KiCad: `Connector_USB:USB_C_Receptacle_GCT_USB4105-xx-A_16P_TopMnt_Horizontal`.


### Würth 629722000214, WR-COM USB 2.0 Horizontal Receptacle SMT (top mount)

- Datasheet (rev 002.000, 2025-09-04), page 1 "Recommended Land Pattern", general tolerance +-0.05: shell stakes 8.64 apart; front slot 0.6 x 1.7 in a 1.0 x 2.1 pad; rear slot 0.6 x 1.4 in a 1.0 x 1.8 pad; rows 4.18 apart; rear row 2.62 from the product edge; locating pegs dia 0.65, 5.78 apart, 3.68 from the rear row; 12 signal pads 1.15 long, 0.6 wide outer (x = +-3.2, +-2.4, i.e. 6.4 and 4.8 apart) and 0.3 wide inner at 0.5 pitch (+-0.25 ... +-1.75). Pin assignment page 2: A5 = CC1, B5 = CC2, SBU1/SBU2, D+/D- on both rows.
- **Comparison with the GCT USB4105 land pattern** (GCT drawing as transcribed in the earlier report): identical in every listed dimension except the rear-row distance to the board edge (Würth 2.62, GCT 2.60; a 0.02 mm difference inside the +-0.05 tolerance). Body 8.94 wide (both); Würth body 7.53 +-0.20 long against GCT 7.35. On these numbers it drops onto the KiCad `USB_C_Receptacle_GCT_USB4105-xx-A_16P_TopMnt_Horizontal` footprint unchanged.
- Article properties: **PCB thickness 0.8 mm (recommended)**, footnote "This PCB thickness is recommended for optimal use. Processing temperature has to be adapted to respect JEDEC requirements if using other panel thicknesses." Okapi is 1.67 mm (earlier report). Stake length below the board is **not dimensioned** on the drawing (the side-view 0.8 +-0.20 and 1.3 +-0.20 are horizontal stake widths; 1.73 +-0.20 is a height above the board): UNVERIFIED. The 0.8 mm PCB recommendation suggests stakes sized for a thin board.
- Durability **10 000 mating cycles** (GCT USB4105: 20,000). Operating temperature **-40 C up to +85 C**. Rated current 5 A max; working voltage 48 V DC. Insertion force 5-20 N; extraction force 8-20 N. Shell steel, nickel plated; contacts brass, gold over nickel.
- Digi-Key (search fetched 2026-11-11): cut tape DK **732-629722000214TRCT-ND**; "USB-C (USB TYPE-C) USB 2.0 Receptacle Connector 24 (16+8 Dummy) Position Surface Mount, Right Angle; Through Hole"; **In-Stock 11,360**; cut tape $2.80000 (1), $2.65000 (10), $2.34400 (100); -40 to 85 C; 5 A.
- Country of manufacture: **China (distributor data)**. WebSearch "element14 629722000214 wurth USB type C 16 pos country of origin China" (2026-11-11): the search summary reports element14 Singapore (https://sg.element14.com/wurth-elektronik/629722000214/usb-conn-2-0-type-c-r-a-rcpt-16pos/dp/4146212) and element14 China listing "Country of Origin: China" and Bürklin (https://buerklin.com/en/p/wuerth-elektronik-eisos/usb-connectors-pc-connectors/629722000214/72F4074) giving origin CN. Direct fetch of the element14 page timed out and Bürklin returned 403, so I have not read the field myself. Würth publishes no manufacturing location in the datasheet (the title block names only Würth Elektronik eiSos GmbH & Co. KG, Waldenburg, Germany, the legal manufacturer). Sibling WR-COM USB parts 632723100011, 614108646521 and 692141030100 are also listed "Country of Origin: China" by Farnell/element14 (same search, 2026-11-11). **Würth does not satisfy the different-country rule against GCT.**
- KiCad official library: no Würth USB-C footprint by name in `Connector_USB.pretty` (listing in the earlier report); the GCT USB4105 footprint fits per the comparison above.

### Hirose CX90B-16P (top mount, right angle, SMT single row, 16 pos.)

- Country of manufacture: **South Korea (distributor data plus manufacturer document)**. The product specification is issued by "HIROSE KOREA.CO.,LTD" (spec sheet, saved); Farnell SKU 3587500 lists "Country of Origin: South Korea" per search summary (not read directly). Whether every lot ships from Korea is UNVERIFIED.
- Spec sheet (Hirose Korea, DWG ELC4-632698, rev 4 dated 21.12.16, printed Apr.1.2026): current "1.25A Max. for each power pin (A1, A4, A9, A12, B1, B4, B5, B9, B12)", 0.25 A others; 48 V AC/DC; **operating -40 C to +105 C (including temp. rise)**; durability "Mated 10,000 times"; insertion 5-20 N, extraction 8-20 N initial, 6-20 N after test.
- Digi-Key (fetched 2026-11-11): cut tape **26-CX90B-16PCT-ND**; "CONN RCP USB3.2 TYP C 24P SMD RA" (Digi-Key's title) with detailed description "USB 2.0 Receptacle Connector 24 (16+8 Dummy) Position Surface Mount, Right Angle; Through Hole"; **In-Stock 2,975**; $2.98000 (1), $2.53000 (10), $2.15020 (100); -40 to 85 C (Digi-Key field; the spec sheet says +105 C); 5 A; 10000 cycles; lead time 16 weeks; Active.
- **Land pattern: NOT the USB4105 pattern.** Catalog page 19 (Aug.1.2022) recommended PCB layout: 16 separate signal lands ("16-0.85" long; 0.20 / 0.25 / 0.425 / 0.57 widths) instead of 12 merged lands; shell slots 8.64 apart (same as GCT) but drilled "8-R0.30 (THRU)" with "R0.55"/"R0.60" lands; locating holes "2-dia 0.45 (Thru)" in dia 0.75 lands, **6.64 apart** (GCT 5.78). Side view: shell dip **0.45 mm** below the board (GCT stakes 0.95 mm, Amphenol 0.90, Same Sky 2A 1.10). It needs its own footprint; it is not a drop-in, and the two land patterns cannot share one footprint (the signal lands overlap with different splits).
- Catalog page 19 HRS No. is CL 0480-0733-0-00; the Hirose product page for CX90B-16P is CL0480-0755-0-00. Whether 0755 is a revision of the same part is UNVERIFIED.
- KiCad official library: no Hirose CX footprint (earlier report's list).

### JAE DX07S016JA1R1500 (country only; other facts in earlier report)

- Country of manufacture: **China (distributor data)**, RS Online "COO (Country of Origin): CN", OnlineComponents and Master Electronics COO CN (search summary 2026-11-11, not read directly). Different land pattern from USB4105 (earlier report). **Fails the different-country test against GCT.**

### Amphenol ICC 12402012E212A ("USB TYPE C 2.0 Top Mount")

- Customer drawing C12402012, rev 4 dated 2020.07.10 (saved). Title "Customer Drawing For USB TYPE C 2.0 Top Mount"; company block "Amphenol East Asia Limited"; RoHS stamp reads "Amphenol Shenzhen". Center height 1.68.
- **Land pattern (sheet 2, "RECOMMENDED PCB LAYOUT (TOP VIEW)", "THICKNESS 0.80MM; DEFAULT TOLERANCE: +-0.05"): identical to GCT USB4105** in every dimension listed: signal spans 8.64 / 6.40 / 4.80 / 3.50 / 2.50 / 1.50 / 0.50; pad widths 0.30 (8x) and 0.60 (4x); pads from 4.17 to 5.32 from the edge (1.15 long); front slots 1.70 in a 2.10 pad, rear slots 1.40 in a 1.80 pad, 0.60 wide; pegs dia 0.65, 5.78 apart, 3.68 from rear row; rows 4.18 apart; rear row 2.60 from the product edge. Body 8.94 x 7.35 (same as GCT). Side view gives stake rows "2X2.60" and "2X4.20" and stake protrusion **0.90** below the board.
- Pin assignments (sheet 1): A5 = CC1, B5 = CC2, SBU1/SBU2, D+/D- both rows.
- Notes: contact current rating 5 A max; insertion 5-20 N, extraction 8-20 N, 6-20 N after durability; **durability 10000 cycles**. **Operating temperature is not stated on the drawing**, and Digi-Key lists none: UNVERIFIED.
- Country of manufacture: **not published**. The drawing names Amphenol East Asia Limited and carries an "Amphenol Shenzhen" stamp, which points to Shenzhen, China, but no distributor COO was found (UNVERIFIED). On the evidence it does not meet the different-country rule.
- Digi-Key (fetched 2026-11-11): cut tape **664-12402012E212ACT-ND**; "CONN RCP USB2.0 TYP C 24P SMD RA"; **In-Stock 70,751**; $0.73000 (1), $0.62200 (10), $0.52840 (100); 5 A; 10000 cycles; lead time 18 weeks; Active; temperature not listed.
- KiCad official library: no footprint by this name; the GCT USB4105 footprint fits per the land pattern.

### Same Sky UJ20-C-H-G-SMT-2A-P16-TR (top mount, horizontal)

- Datasheet (date 11/03/2025, saved), page 3 "Recommended PCB Layout, Top View", PCB tolerance +-0.05, **PCB thickness 1.0 mm**: signal spans 8.64 / 6.40 / 4.80 / 3.50, pad widths 0.30 x 8 and 0.60 x 4, 0.50 pitch; front slots 0.60 x 1.70 in 1.00 x 2.10 pads; rear slots 1.40 in 1.80 pads; pegs dia 0.65, 5.78 apart, 3.68 from the rear row; rows 4.18 apart; rear row 2.60 from the product edge. **Same as USB4105 except signal-pad length: 1.80 against GCT's 1.15.** The extra length would have to be added to a shared footprint (UNVERIFIED whether the part solders well on 1.15 pads).
- Page 2: body 8.94 wide x 7.30 (7.80 overall); stake length below board 1.10 +-0.10 (side view); shell SUS304. Page 1 (pdftotext): life 10,000 cycles; operating -40 to 85 C.
- Pin connections: A5 = CC1, B5 = CC2, SBU1/2, Dp/Dn both rows.
- Digi-Key (fetched 2026-11-11): cut tape **2223-UJ20-C-H-G-SMT-2A-P16-TRCT-ND**; **In-Stock 1,749**; $0.39000 (1), $0.32900 (10), $0.27960 (100); -40 to 85 C; 0.25 A / 1.25 A / 5 A; lead time 8 weeks; Active.
- Country of manufacture: **not published** by Same Sky; sibling UJ20-C-H-G-SMT-4-P16-TR listed COO CN (e-sonic, search summary). Treat as China (UNVERIFIED for this exact part). Fails the different-country test.
- KiCad official library: none by name.

### Hirose CX90M-16P, TE 2340901-1 (mid-mount; excluded by geometry)

- Both are mid-mount (board cut-out) designs per the Hirose flyer (CX90M-16P "Mid-Mount, Right-Angle (SMT Single-row)") and the Digi-Key TE description ("MID-MOUN"). Neither fits the USB4105 top-mount land pattern. Not pursued.

### Molex 217179-0001 (2171790001), country only

- Country of manufacture: **China (distributor data)**, RS UK/SE/DK "COO: CN" (search summary, not read directly). LCSC lists it as "TYPE C 16 PIN TOP MOUNT SMT", -40 to +85 C. Land pattern UNVERIFIED (sales drawing not retrievable). Digi-Key data in the earlier report: 900-2171790001CT-ND, 65,872 stock, $0.764 (10), $0.6487 (100). Fails the different-country test.

### JAE DX07S016JA3R1500 (single-row SMT sibling)

- Digi-Key (fetched 2026-11-11): cut tape **670-DX07S016JA3R1500CT-ND**; **In-Stock 8,481**; $2.02000 (1), $1.72000 (10), $1.46160 (100); -40 to 85 C; 10000 cycles; lead time 21 weeks; Active.
- JAE product sheet: shell DIP length 1.2 mm, 1-row SMT, 16 pos., 5 A, center height 1.58 mm. Land pattern: UNVERIFIED (not retrieved). Country: UNVERIFIED for this exact part; the sibling DX07S016JA1R1500 is listed CN. Not a demonstrated non-China source.

## Comparison: USB4105 land pattern and non-China candidates

| Part | Fits USB4105 land pattern | Country (source quality) | Temp (C) | Cycles | Shell retention | Rec. PCB | DK cut-tape PN | DK stock 2026-11-11 | $ 1 / 10 / 100 | KiCad official fp |
|---|---|---|---|---|---|---|---|---|---|---|
| GCT USB4105-GF-A | yes (reference) | China (distributor, via search) | -40 to 85 | 20,000 | 4 THT stakes 0.95 mm + 2 pegs | not stated (UNVERIFIED) | 2073-USB4105-GF-ACT-ND | 263,569 | 0.800 / 0.676 / 0.5745 | yes (GCT_USB4105) |
| Würth 629722000214 | yes (all dims; rear row 2.62 vs 2.60) | China (distributor, via search) | -40 to 85 | 10 000 | 4 THT stakes + 2 pegs; length not dimensioned | 0.8 mm | 732-629722000214TRCT-ND | 11,360 | 2.800 / 2.650 / 2.344 | use GCT_USB4105 |
| Amphenol 12402012E212A | yes (all dims) | not published; drawing from Amphenol East Asia, "Amphenol Shenzhen" stamp | not published (UNVERIFIED) | 10000 | 4 THT stakes 0.90 mm + 2 pegs | 0.80 mm | 664-12402012E212ACT-ND | 70,751 | 0.730 / 0.622 / 0.5284 | use GCT_USB4105 |
| Same Sky UJ20-C-H-G-SMT-2A-P16-TR | yes except signal pads 1.80 long (GCT 1.15) | not published; sibling CN | -40 to 85 | 10,000 | 4 THT stakes 1.10 mm + 2 pegs | 1.0 mm | 2223-UJ20-C-H-G-SMT-2A-P16-TRCT-ND | 1,749 | 0.390 / 0.329 / 0.2796 | no |
| Molex 2171790001 | UNVERIFIED | China (distributor, via search) | -40 to 85 | (earlier report) | SMT + TH | UNVERIFIED | 900-2171790001CT-ND | 65,872 (earlier report) | 0.900 / 0.764 / 0.6487 (earlier report) | no |
| JAE DX07S016JA1R1500 | no | China (distributor, via search) | -40 to 85 | (earlier report) | 4 THT | – | 670-DX07S016JA1R1500CT-ND | not stated | 1.800 / 1.531 / 1.3009 (earlier report) | yes (own) |
| **Hirose CX90B-16P** | **no (own footprint)** | **South Korea** (Hirose Korea spec sheet; distributor via search) | -40 to 105 (spec sheet); DK says 85 | 10,000 | 4 THT slots, shell dip 0.45 mm + 2 pegs | UNVERIFIED | 26-CX90B-16PCT-ND | 2,975 | 2.980 / 2.530 / 2.1502 | no |

All candidates are top mount with four through-hole shell stakes in slots and two locating pegs; no mid-mount part was kept, because a mid-mount needs a board cut-out at the edge.

## For Andy (proposal, not a decision)

**Finding.** Every horizontal USB 2.0 Type-C receptacle that drops onto the USB4105 land pattern and that I could trace (GCT, Würth, Amphenol, Same Sky, Molex) is made in China, or names no origin and carries a Shenzhen stamp. Würth's own part (629722000214) is a true drop-in, rated -40 to +85 C, but distributors list it as made in China. The one candidate with a documented non-China origin is the Hirose CX90B-16P (Hirose Korea), and it needs its own footprint.

**Proposal.** (1) Use GCT USB4105-GF-A for both J10 and USB2, on the KiCad official `USB_C_Receptacle_GCT_USB4105-xx-A_16P_TopMnt_Horizontal` footprint (it has the slots the nw-cold-silicon copy lost). It has the most stock by far, the best published endurance (20,000 cycles), -40 C, and 0.95 mm stakes. (2) Approve Würth 629722000214 as the same-footprint alternate: it is your preferred brand, the land pattern matches to 0.02 mm, and it is -40 C. However, it does **not** satisfy "assembled in a different country", and nothing on this footprint that I found does. (3) If the different-country rule must hold for this part, the only way I found is to design one port (or a future revision) around the Hirose CX90B-16P (South Korea, -40 to +105 C, 10,000 cycles). That costs a new footprint, $2.53 at 10 against $0.676, 2,975 in stock, a 16-week lead time, and shorter 0.45 mm shell stakes. Whether the rule should apply to a $0.70 connector with 263,569 in stock is your call.

**Open.** (1) Würth and Amphenol recommend a 0.8 mm board, and Okapi is 1.67 mm. Their stakes will sit short of the bottom surface and solder only by pin-in-paste. GCT's recommended thickness is not stated. (2) The Amphenol operating temperature is unpublished. (3) The JAE DX07S016JA3R1500 land pattern and origin, and the Molex 2171790001 land pattern, were not retrieved.

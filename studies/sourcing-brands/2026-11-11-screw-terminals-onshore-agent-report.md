# On Shore OSTVN, Amphenol Anytek VN, GCT TBC05: 2.54 mm rising-clamp terminals

Status: COMPLETE

Agent report, 2026-11-11. Read-only extraction for line-by-line comparison against the Phoenix Contact MPT 0,5/..-2,54 extraction.

Source keys:
- OST-DWG: On Shore drawing OSTVNXXA150, "OSTVN Series 2.54mm", Rev A, drawn 2016.05.18, checked 2016.08.09, one sheet. Read by eye at 400 and 600 dpi; tesseract agreed on every technical-data digit and the BOM.
- ANY-DWG: Anytek drawing "VN 2.54mm Series", DWG NO. 8VN0001, part VNxxA1x0xxxxG, Rev E, drawn 2008.11.12, revision block dated 11/12'08. Read by eye at 400 dpi.
- GCT-DWG: GCT drawing TBC05, drawing date 18 October 2024, release date 08/05/25, 2 sheets. Text PDF, read with pdftotext and by eye at 300 dpi.
- GCT-SPEC: GCT product specification TBC05, Rev A1, 10/01/25, 5 pages.
- DK: Digi-Key product pages, read 2026-11-11 in Chrome.

## Field table

| # | Field | On Shore OSTVN10A150 / OSTVN06A150 | Amphenol Anytek VN10A1500000G / VN06A1500000G | GCT TBC05-10-1-G-G / TBC05-06-1-G-G |
|---|---|---|---|---|
| 1 | Positions | 2-16 on On Shore's own copy; 2-24 on Digi-Key's copy of the same sheet (OST-DWG legend) | 2-24 (ANY-DWG legend) | 2-24 (GCT-DWG ordering grid) |
| 1 | Pitch | 2.54 mm (OST-DWG) | 2.54 mm (ANY-DWG) | 2.54 mm (GCT-DWG) |
| 2 | Clamp type | Rising cage: item 2 "CAGE", brass, carries the M1.6x0.35 thread; the section shows the screw through the cage, which rises and clamps the wire against the serrated underside of the contact strip (item 4) (OST-DWG section, BOM) | Rising clamp: item 3 "Clamp", brass, threaded on the screw; same section geometry (ANY-DWG section); DK: "Screw - Rising Cage Clamp" | "Rising Clamp Type" (GCT-DWG title, GCT-SPEC); section C-C shows the same arrangement |
| 2 | Screw thread | M1.6 (M1.6x0.35) (OST-DWG Technical data 6, BOM item 3) | M1.6 (ANY-DWG Electrical) | M1.6 (GCT-DWG "Torque: 1.5kgf.cm/M1.6") |
| 2 | Screw head | Slotted (plan view slots, section) (OST-DWG) | Slotted, "'-' slot type" (ANY-DWG Material item 2) | Combination slot/Phillips, "'-/+' Combination Type" (GCT-DWG Material; plan view shows crosses) |
| 2 | Torque | 1.5 kgf.cm (0.15 N.m), single value, not called min or max (OST-DWG Technical data 5) | 1.3 lb-in, single value (ANY-DWG); 1.3 lb-in = 0.147 N.m, the same value in other units | 1.5 kgf.cm (GCT-DWG); the torque test uses 110 % of this (GCT-SPEC 6.2) |
| 3 | Wire range | AWG 30-18; no solid/stranded split; no mm² (OST-DWG Technical data 2) | Solid AWG 18-30; stranded AWG 18-30 (ANY-DWG, revision 3 of 11/12'08 widened it from 20-30) | Solid AWG 18-30; stranded AWG 18-30 (GCT-DWG) |
| 3 | Stripping length | 4-5 mm (OST-DWG Technical data 7) | 4-5 mm (ANY-DWG) | 4.0-5.0 mm (GCT-DWG) |
| 3 | Ferrules | – | – | – |
| 4 | Rated current; voltage | 6 A; 150 V ("Nominal voltage: 150V/6A") (OST-DWG Technical data 1) | 6 A; 150 V AC (ANY-DWG, revision 2 raised it from 125 V AC) | 6.0 A per position; 150 V AC (GCT-DWG, GCT-SPEC 4.0) |
| 4 | Standard for rating | None stated (OST-DWG) | None stated (ANY-DWG) | No standard named for the rating itself; dielectric, temperature-rise, torque and secureness tests cite UL 1059, pull-out cites UL 486E (GCT-SPEC 6.1, 6.2) |
| 4 | Approvals | cRUus mark (UL recognized, US and Canada) on the end view and as item 10; no file number (OST-DWG). Web search for an On Shore file number found none | cULus (ANY-DWG heading "Electrical cULus" and "Safety Approval" mark); no file number | UL recognized mark on end view; UL file E543462 (GCT-DWG); no CSA or VDE |
| 5 | Operating temperature | -40 to 115 °C (OST-DWG Technical data 8). DK lists -30 to 105 °C, which conflicts with the drawing | -40 to 115 °C (ANY-DWG); DK agrees | -40 to 105 °C (GCT-DWG, GCT-SPEC 4.0); high-temperature life test 105 °C, 168 h (GCT-SPEC 6.3) |
| 5 | Derating curve | None (OST-DWG) | None (ANY-DWG) | None; temperature rise +30 °C max at 6 A on AWG 18, 3 poles in series (GCT-SPEC 6.1) |
| 5 | Storage / assembly | Soldering 250 ±10 °C for 5 s; no storage range (OST-DWG) | Soldering 250 °C ±10 °C for 5 s; no storage range (ANY-DWG) | Storage -40 to 70 °C at 30-70 % RH (GCT-SPEC 4.0); solderability 245 ±5 °C for 5 s (GCT-DWG), 4-5 s dip (GCT-SPEC 6.3) |
| 6 | Housing | PA66 UL94V-0, all colors (BOM item 1); green standard; black, red, orange, yellow, blue, gray (OST-DWG) | PA66 (UL94V-0) (ANY-DWG item 1); colors black, green RAL 6018, blue, gray RAL 7035 | Nylon 66, 0 % glass fill, UL94V-0; green only in the ordering grid (GCT-DWG); glow-wire 850 °C to IEC 60695-2-10 (GCT-SPEC 6.3) |
| 6 | Contact (wire-guard / solder pin) | Brass, tin plated; thickness not stated (OST-DWG BOM item 4). DK lists "Brass" without plating | Brass, tin plated, "Wire guard solder pin (entry)" (ANY-DWG item 4) | Copper alloy, tin plated, "Wire Guard Solder Pin" (GCT-DWG) |
| 6 | Cage / clamp | Brass, Ni plated, M1.6x0.35 thread (OST-DWG BOM item 2) | Brass, Ni plated (ANY-DWG item 3) | Copper alloy, nickel plated (GCT-DWG) |
| 6 | Screw | Steel, Zn plated (OST-DWG BOM item 3) | Steel, zinc plated (ANY-DWG item 2) | Stainless steel; no plating (GCT-DWG) |
| 7 | Length | L = P x 2.54 + 0.4: 10 pos 25.80 mm, 6 pos 15.64 mm (formula OST-DWG note 9; arithmetic mine); ±0.20 at 0-30 mm | A = N x 2.54 + 0.4: 25.80 and 15.64 mm (ANY-DWG); ±0.15 at 2-6p, ±0.20 at 7-12p | Tabulated A: 10 pos 25.80 mm, 6 pos 15.64 mm (GCT-DWG table) |
| 7 | Depth | 6.5 mm (OST-DWG plan view) | 6.5 mm (ANY-DWG dimension G) | 6.5 mm (GCT-DWG) |
| 7 | Height above board | 8.5 mm (OST-DWG) | 8.5 mm (ANY-DWG dimension B) | 8.5 mm (GCT-DWG, GCT catalog "Profile 8.50mm") |
| 7 | Wire entry | Horizontal, parallel to the board ("side entry" on DK). Opening 1.5 mm tall (dimensioned). Bottom of the opening about 1.6 mm above the board, center about 2.3 mm, SCALED from the section against the 1.5 mm dimension (UNVERIFIED: not dimensioned) | Horizontal. 1.6 mm dimensioned from the board to the bottom of the clamp jaw at the entry (ANY-DWG section) | Horizontal. Entry opening □1.4 x 1.5 mm (GCT-DWG front view); height above board not dimensioned |
| 7 | Pin row position | 3.3 mm from the wire-entry face, therefore 3.2 mm from the back face (OST-DWG section and PCB layout "(3.3)"); end pins 1.47 mm from body ends | 3.3 mm from the BACK face (section dimension J runs from the pin to the face opposite the entry), therefore 3.2 mm from the entry face; end pins 1.5 mm from body ends (ANY-DWG; 1.5 is the rounded form of 1.47) | 3.25 mm from each face (GCT-DWG section and PCB layout); end pins 1.47 mm from body ends |
| 8 | Pin cross-section | Flat rectangle 0.90 x 0.40 mm; the pin is the bent tail of the contact strip (OST-DWG front and section) | 0.90 x 0.40 mm, same construction (ANY-DWG dimensions E and I) | 0.9 x 0.4 mm, same construction (GCT-DWG) |
| 8 | Pin length below body | 3.5 mm (OST-DWG) | 3.5 mm (ANY-DWG dimension H) | 3.5 mm (GCT-DWG) |
| 8 | Recommended hole | Ø1.30 mm (OST-DWG PCB layout) | Ø1.30 mm (ANY-DWG PCB layout) | Ø1.3 mm, layout tolerance ±0.05 (GCT-DWG) |
| 8 | Pins per position; second row | 1, single row, no pegs (OST-DWG) | 1, single row, no pegs (ANY-DWG) | 1, single row, no pegs (GCT-DWG) |
| 9 | Withstand voltage | AC 1300 V for 1 min (OST-DWG Technical data 3) | 1.3 kV (ANY-DWG; revision 4 raised it from 1.25 kV) | 1300 V AC for 60 s, no arcing or breakdown (GCT-DWG, GCT-SPEC 6.1) |
| 9 | Insulation resistance | 1000 MΩ or more at DC 500 V (OST-DWG Technical data 4) | – | 5000 MΩ min at DC 1000 V; 5 MΩ min after humidity and heat (GCT-SPEC 6.1, 6.3) |
| 9 | Contact resistance | – | – | 20 mΩ max new, 30 mΩ max after humidity, heat life and salt spray (GCT-SPEC) |
| 9 | Wire pull-out | – | – | AWG 18: 30 N; AWG 30: 2.2 N, 1 min, to UL 486E (GCT-SPEC 6.2) |
| 9 | Insertion cycles | – | – | Torque test: 5 repetitions at 110 % torque, max and min wire (GCT-SPEC 6.2); no cycle rating |
| 10 | Interlocking | Fixed lengths, no dovetail in any view (OST-DWG) | Fixed lengths, no dovetail (ANY-DWG) | Fixed lengths, no dovetail (GCT-DWG) |
| 11 | Digi-Key 10 pos | ED10567-ND; $3.79 / $2.701 / $1.9717 at 1 / 10 / 100; 3,325 in stock; lead time 10 weeks; country of origin not shown (DK) | VN10A1500000G-ND; not stocked; only in 2,580 multiples at $1.54308; lead time 16 weeks (DK) | 2073-TBC05-10-1-G-G-ND; $3.60 / $2.565 / $1.8666 at 1 / 10 / 100; 754 in stock; lead time 8 weeks; country of origin not shown (DK) |
| 11 | Digi-Key 6 pos | ED10565-ND; $2.40 / $1.721 / $1.2415 at 1 / 10 / 100; 7,403 in stock; lead time 10 weeks (DK) | VN06A1500000G-ND; not stocked; only in 3,000 multiples at $0.92708; lead time 16 weeks (DK) | 2073-TBC05-06-1-G-G-ND; not stocked; only in 840 multiples at $0.87164; lead time 8 weeks (DK) |

Digi-Key attribute errors on the On Shore pages: -30 to 105 °C (drawing -40 to 115 °C); contact and clamp "Brass" with no plating (drawing: tin and nickel); housing "Thermoplastic" (drawing: PA66 UL94V-0). Digi-Key's Anytek pages match the Anytek drawing. Digi-Key lists Würth 691210910006 as a third parametric equivalent for the 6-position part only (not examined here).

## Footprint fit

Margay's 1X10_SCREW and 1X06_SCREW (read from nw-cold-silicon.pretty): round plated holes, 1.016 mm drill, 1.524 mm pads, outline from -3.3 to +3.2 mm about the pin row (6.5 mm), with a second line at -2.54 mm that marks a 0.76 mm band along the -3.3 face. Outline length 25.86 mm (10 pos) and 15.70 mm (6 pos).

Pin in hole. All three parts have the same 0.90 x 0.40 mm flat pin. Its diagonal is sqrt(0.90² + 0.40²) = 0.985 mm at nominal, against a 1.016 mm drill: 0.031 mm clearance across the diagonal before plating. A plated barrel is smaller than its drill (a 25 µm wall would leave 0.966 mm; that wall thickness is an assumption, not the fab's figure), which is smaller than the pin's nominal diagonal. At the drawings' own tolerance (On Shore X.XX ±0.10, so up to 1.00 x 0.40 mm) the diagonal reaches 1.077 mm. All three makers recommend Ø1.30 mm, which is 0.284 mm larger than the present drill. Verdict: the pin does not fit the 1.016 mm hole reliably; it would be a press or a reject depending on the board. A 1.30 mm hole in the present 1.524 mm pad leaves a 0.112 mm annular ring, so the pad would also need to grow.

Body in outline. Depth: all three are 6.5 mm, equal to the outline's 3.3 + 3.2 mm. Pin row: On Shore's drawing puts the pins 3.3 mm from the wire-entry face, Anytek's 3.3 mm from the back face, GCT's 3.25 mm from both; the differences are 0.05-0.1 mm, inside the drawings' ±0.30 tolerance for X.X dimensions, and each part fits the outline whichever face is the entry to within 0.1 mm. Which side of the Margay outline is the wire-entry side is not established here (the -3.3 band suggests the entry lip, UNVERIFIED). Length: 25.80 mm in a 25.86 mm outline (0.03 mm per end) for 10 positions, and 15.64 mm in 15.70 mm (0.03 mm per end) for 6. Verdict: the body fits the outline, and the outline looks drawn for this body size.

## Anytek versus On Shore

What matches, from the two drawings:
1. Every dimension: 6.5 depth, 8.5 height, 3.5 pin, 0.90 x 0.40 pin, 2.54 pitch, Ø1.30 hole, L = N x 2.54 + 0.4, the 3.3 mm pin-to-face figure, the (6.5)/(3.3) PCB-layout box.
2. Every electrical and process value: 150 V, 6 A, AWG 18-30, 1.3 kV (1300 V) for 1 min, M1.6, 4-5 mm strip, 0.15 N.m (1.5 kgf.cm and 1.3 lb-in are the same torque), -40 to 115 °C, soldering 250 ±10 °C for 5 s, cULus.
3. Materials, item for item: PA66 UL94V-0 housing; brass Ni-plated clamp; steel Zn-plated slotted screw; brass tin-plated contact that is also the solder pin.
4. Drawing layout: the same set of views in the same places (plan view top, front view with dimensioned pins below it, sectioned side view, plain end view at left, hatched P.C.B. LAYOUT below, technical data at right), and an almost line-for-line identical section drawing (screw, threaded clamp, serrated contact strip, 4 serration marks on the wire, contact bent down into the pin).
5. Part-number structure: On Shore OSTVN xx A 1 x 0 against Anytek VN xx A 1 x 0 xxxx G; the color digits agree where both list them (0 black, 5 green, 6 blue, 8 gray). On Shore's number reads as "OST" prefixed to Anytek's.

What differs: (1) title block, logo and dates (Anytek 2008 Rev E, On Shore 2016 Rev A); (2) the item numbering of screw and clamp is swapped; (3) Anytek dimensions the pin 3.3 mm from the back face, On Shore 3.3 mm from the entry face; (4) On Shore states insulation resistance (1000 MΩ at DC 500 V) and Anytek does not; (5) end offset written 1.5 by Anytek and 1.47 by On Shore; (6) screw clearance shown as 2.20 by Anytek (revision 1 enlarged it from 2.10) and Ø2.1 in On Shore's plan view; (7) On Shore adds red, orange and yellow.

What the documents show and no more: On Shore's drawing carries Anytek's part-number pattern, Anytek's dimensions, ratings and materials, and a section view of the same construction, and it postdates Anytek's by eight years. That is consistent with On Shore selling an Anytek-pattern part, or both drawing from a common source; the documents do not say who makes On Shore's part. GCT's TBC05 shares every key dimension (6.5, 8.5, 3.5, 0.9 x 0.4, Ø1.3, 1.47) and the ratings, but its drawing is GCT's own layout and its screw is stainless with a combination head, so it is the same design type with different screw hardware and a fuller test specification.

## Sources log


- https://www.on-shore.com/wp-content/uploads/OSTVNXXA150.pdf: downloaded, PDF 1.6, 2022-07-26, title "OSTVNXXA150.dwg Model (1)". One sheet, image only (pdftotext returns nothing). Rasterized at 400 and 600 dpi into the scratchpad tb-onshore directory; read by eye; tesseract cross-check of technical data and BOM agreed.
- Digi-Key via curl (search and product URL for OSTVN10A150): HTTP 403, dead end; switching to browser.
- Digi-Key OSTVN10A150 product page (ED10567-ND, /detail/on-shore-technology-inc/OSTVN10A150/1588870), read in Chrome: prices, stock, attributes, substitutes (VN10A1500000G, TBC05-10-1-G-G).
- Digi-Key OSTVN06A150 product page (ED10565-ND, /1588866): prices, stock; substitutes Würth 691210910006, VN06A1500000G, TBC05-06-1-G-G.
- Digi-Key copy of the drawing, https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/1123/OSTVNXXA150.pdf: PDF created 2021-11-10, different file (md5 differs) from On Shore's 2022-07-26 copy. Read at 300 dpi: same sheet, same Rev A and dates, every value identical except the pole range in the part-number legend, which reads 02-24 poles here against 02-16 on On Shore's own copy.
- Digi-Key VN10A1500000G page (VN10A1500000G-ND, /amphenol-anytek/VN10A1500000G/4957648): price, MOQ, attributes; datasheet and drawing links both go to the Anytek drawing below.
- Anytek drawing http://www.anytek.com.tw/UserUpFiles/20120512/L_wOt9EJEyJN.pdf ("VN 2.54mm Series", DWG NO. 8VN0001, Rev E, drawn 2008.11.12, A4, PDF dated 2012-05-12): downloaded to scratchpad tb-anytek, read at 400 dpi.
- GCT spec https://gct.co/files/specs/tbc05-spec.pdf (TBC05 product specification, Rev A1, 10/01/25 [dd/mm/yy], 5 pages, text PDF): downloaded to scratchpad tb-gct, read with pdftotext. It says "Please refer to drawing" for dimensions and materials.
- Digi-Key TBC05-10-1-G-G page (2073-TBC05-10-1-G-G-ND, /gct/TBC05-10-1-G-G/26408888): prices, stock, attributes; links to the spec, a Digi-Key catalog sheet and the drawing.
- GCT drawing https://gct.co/files/drawings/tbc05.pdf (2 pages; page 2 is packing quantities): downloaded to scratchpad tb-gct, read with pdftotext and at 300 dpi.
- Digi-Key "TBC05 Datasheet" https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/6799/TBC05%20Datasheet.pdf: one-page GCT series catalog sheet (2024); confirms UL file E543462, stainless screws, TBC05 6 A / 150 V AC / AWG 18-30 / 8.50 mm profile.
- Digi-Key TBC05-06-1-G-G page (/26408930): not stocked, 840 MOQ, $0.87164.
- Digi-Key VN06A1500000G page (/amphenol-anytek/VN06A1500000G/4957644): not stocked, 3,000 MOQ, $0.92708.
- Web search "On Shore Technology terminal block UL file number E OSTVN": no file number found (distributor listings only). Dead end; UL Product iQ not checked.
- nw-cold-silicon/nw-cold-silicon.pretty/1X10_SCREW.kicad_mod and 1X06_SCREW.kicad_mod: read only, for the outline coordinates and pads.
- Note: the shared Chrome tab group also held another agent's Phoenix Contact tab (1279253007); one early read landed on it, and all later reads used a separate tab, closed at the end.

COMPLETE

# Margay v4: convenient outline sizes (agent report, 2026-11-12)

Findings are appended as confirmed. Each number is pasted from a source, measured (method stated), or marked UNVERIFIED.

## Findings

### F1. Current Margay v3 outline and holes (measured)

Source: `Project-Margay/Hardware/Margay.brd` (Eagle, layer 20 wires, lines 191-197) and `Hardware/KiCAD/Margay.kicad_pcb` (Edge.Cuts gr_line/gr_arc), parsed with Python.

- Outline 50.145 x 30.404 mm (Eagle wires span x 0 to 50.145, y 0 to 30.404; KiCad Edge.Cuts x 123.4286 to 173.5736, y 89.8016 to 120.2056, same size).
- Corners: 2 mm radius on three corners; the top-left corner (Eagle (0, 30.404), the J2 end nearest pin 1) is square.
- Two mounting holes only, on a diagonal: H1 at (2.159, 2.159) mm and H2 at (48.006, 28.194) mm from the bottom-left corner (Eagle element lines 2868-2869). Center spacing 45.847 mm in x and 26.035 mm in y (computed). Footprint `4_40_CLOSE`, NPTH drill 2.9464 mm (0.116 in, #4 close fit; KiCad pad drill). README v3.0 notes: "Increased mounting hole sizes to fit #4 screws".
- KiCad board has 84 footprints (grep count).

### F2. Where the field parts sit (measured, KiCad footprint at/rotation plus Fab/CrtYd extents, board coordinates converted to "from left edge / from top edge")

- J2, 10-position 2.54 mm screw terminal (`1X10_SCREW`): left edge, along the 30.4 mm side. Pins 1-10 at x = 3.30 mm from left edge, y = 1.58 to 24.44 mm from top (pitch 2.54, span 22.86 mm). Fab body 6.5 mm deep (x 0.10 to 6.60 from left) and 25.86 mm long (y 0.08 to 25.94 from top). It therefore already uses 25.9 of the 30.4 mm short side.
- J3, 6-position 2.54 mm screw terminal (`1X06_SCREW`): right edge. Pins at 3.79 mm from right edge, y = 14.28 to 26.98 mm from top. Fab body 6.5 x 15.7 mm (y 12.78 to 28.48 from top).
- J4, USB-C (`USB_C_CUSB31-CFM2AX-01-X`): top long edge, centered 40.26 mm from left (Eagle x = 40.259). Courtyard x 35.19 to 45.33 mm from left and overhangs the top edge by 1.47 mm (courtyard y 88.33 vs edge 89.80).
- J1, full-size SD (`SD_WURTH_WR-CRD`, Eagle rot MR180 = bottom side; KiCad B.Cu): courtyard x 4.91 to 34.21 mm from left (29.3 mm), y -0.63 to 26.91 mm from top, i.e. the card mouth is at the top long edge and the courtyard overhangs it by 0.63 mm. It covers most of the left 70 % of the bottom.
- BT1, 12 mm coin cell holder (Linx BAT-HLD-012-SMT): Eagle element rot R180, not mirrored, and KiCad layer F.Cu: it is on the TOP side, centered 17.91 mm from left, 5.59 mm from bottom; silk extent 13.5 x 8.9 mm. It sits directly above the SD card (stacked through the board). DISCREPANCY: README line 428 says the CR1220 is "mounted on the back of the board". Both design files say top. Worth a photo check.
- Consequence for a single machine-assembled side: today both sides carry SMT parts (J1 SD and jumpers JP1/JP2 on B.Cu; everything else F.Cu), so the SD holder is the only large bottom part.

### F3. Existing mounts and the board geometry they assume (measured)

Method: binary STL parsed with numpy (scratch script `stl.py`), bounding boxes from all vertices, then planar slices at stated z heights with loops chained and their bounding boxes printed (`slice.py`). SVG paths of the WQ-48 plate sampled as Bezier curves and scaled by 25.4 mm/in. Git history from `git log -- 3Dprint Mounting_Plate`: mounts added 2020-04-30 ("Battery and Margay box mounts; fab stencil"); WQ-48 plate 2021-04-13, "Updated for both orientations and No.4 holes" 2021-04-16.

Every Margay mount locates the board by its TWO DIAGONAL HOLES ONLY, at 45.85 x 26.04 mm center spacing, which equals the board's H1-H2 spacing (45.847 x 26.035 mm). No mount uses the board edge, so a larger board that keeps those two holes (or adds holes and keeps these two) still fits every printed mount, as long as the larger outline clears the walls described below.

- `MargayMount_WH02_lid.STL`: plate 54.41 x 78.74 mm, 1.2 mm thick, rounded corners; two standoffs 7.00 mm OD, 1.78 mm bore, to z = 6.2 mm (5.0 mm above the plate), at (4.28, 13.33) and (50.13, 39.37) mm. Spacing 45.85 x 26.04 mm. The plate is only 54.4 mm wide; the left standoff center is 4.28 mm from the plate edge and the right one 4.28 mm from the other edge (54.41 - 50.13). With the board's holes 2.16 mm in from its edges, the 50.1 mm board overhangs neither plate edge (board spans x 2.12 to 52.27 mm on the plate, computed). Any growth in the 50 mm direction over about 54 mm overhangs this plate (the plate itself is not the limit; the WH-02 lid cavity is; see F5).
- `MargayMount_WH10.STL`: plate 129.93 x 79.93 mm, 1.2 mm thick; two 4.00 mm holes at (14.97, 39.97) and (114.97, 39.97), 100.0 mm apart (enclosure-side screws); two board standoffs 7.00 mm OD, 2.50 mm bore, 5.0 mm tall, at (56.81, 13.93) and (102.66, 39.97): spacing 45.85 x 26.04 mm. Placed so the board occupies x about 54.7 to 104.8, y about 11.8 to 42.2 (computed from hole offsets): the plate has free room for a board up to roughly 125 x 75 mm if the standoffs stay put, minus whatever the battery mount occupies in the same box.
- `BatteryMount_WH10.STL`: 128.0 x 78.5 x 11.2 mm frame; through pocket 69.0 x 49.0 mm (69.96 x 49.96 at the top lip); two 2.49 mm holes 68.0 mm apart at (64.00, 5.25) and (64.00, 73.25). What battery the 69 x 49 pocket holds is UNVERIFIED (not stated in the repo files I read).
- `BatteryMount_Strap.STL`: 75.0 x 10.05 x 15.0 mm strap, two small tabs 2.36 x 1.20 mm at the ends. Board-independent.
- `StencilMount_Margay.STL`: 45.5 x 124.4 x 1.2 mm plate with a board pocket 31.0 x 50.74 mm (measured across the waist with a point-in-polygon scan), i.e. the 30.4 x 50.1 mm board plus about 0.3 mm per side, with corner-relief extensions to 39.0 x 58.7 mm. This jig is board-specific: ANY outline change needs a new one (a cheap print, but a change).
- `Mounting_Plate/Margay-Mounting-Plate_WQ-48`: ABS plate 184.78 x 134.29 mm (stock "190.5 mm x 139.7 mm x 3.175 mm", settings.txt), 1/16 in upcut bit; two 5.75 mm enclosure holes 160.43 mm apart at mid-height; one 71.17 x 71.17 mm square cutout (purpose UNVERIFIED; perhaps cable or battery pass-through); two 3.20 mm board holes at (134.42, 44.18) and (108.38, 90.03) mm: spacing 26.04 x 45.85 mm, the Margay pattern rotated 90 degrees. Workpiece 1 and 2 have identical path data, only rotated for stock orientation. Free area right of the square cutout: x 95 to about 170 mm (75 mm), full 134 mm height less margins.

### F4. Photo check of v3.0 (Documentation/images/Margay_v30_top_20250206.jpg and _back_with_quarter_20250206.jpg, viewed)

- The CR1220 holder is on the TOP side, beside the 10-position terminal; the design files are right and README line 428 ("mounted on the back of the board") is wrong. The full-size SD holder fills the bottom.
- Both green screw-terminal blocks visibly overhang the PCB edges on the left and right (wire entry outboard of the outline). The real envelope in the 50 mm direction is therefore larger than 50.1 mm; amount not measured (UNVERIFIED; the Fab body in F2 spans 6.5 mm in x from 0.10 mm inside the edge, so the photo overhang is the terminal's wire-entry face beyond the Fab line, or a Fab outline that is not the true body).
- A 2x3 through-hole ICSP header sits on the top side near J3; the board is mixed SMT/through-hole on top, SMT (SD) on the bottom.
- `Documentation/MargayGuide_20190730.pdf` and `_20220622.pdf` (pdftotext + grep for enclosure, Polycase, box, mount, battery, holder, D cell, strap): only operating notes ("Turn battery pack on/off"), no enclosure, battery-pack or mount dimensions. README holds no enclosure model numbers (grep for enclos|polycase|WH|WQ|mount: none relevant).

### F5. Okapi outline and holes, for shared mounts (measured)

Source: `Project-Okapi/Hardware/Okapi.brd` layer-20 wires and `<element name="H*">`, cross-checked against `Hardware/KiCAD-10import/Okapi.kicad_pcb` Edge.Cuts (bbox 116.1261 to 180.8761, 37.5036 to 172.5036 = 64.75 x 135.00 mm; agrees).

- Bounding box 64.75 x 135.00 mm, 2 mm corner radii, with one corner notch: the region x 0 to 25 mm, y 100 to 135 mm (Eagle coordinates, y up) is cut away, so the top 35 mm of the board is 39.75 mm wide (x 25 to 64.75).
- Three holes, footprint `4_40`, drill 3.175 mm (KiCad), at (19.812, 6.858), (19.812, 86.858) and (59.812, 86.858) mm: an L on a 40.000 x 80.000 mm grid. Okapi README line 125: "Mounting holes for #4 screws".
- Okapi housing (README lines 452-464): PolyCase WH-16-03 enclosure; Okapi on three #4-40 x 2 in standoffs over a milled 1/8 in ABS plate; 3x AA pack "BK-1280-PC6" (MPD) on #4-40 x 1/2 in standoffs. WH-16 plate drawing `Mounting_Plate/WH-16/Resnik_Mounting_Plate_Drawing.pdf` (pdftotext): plate 10.500 x 5.910 in (266.7 x 150.1 mm), 4x dia 0.216 in enclosure holes, 11x dia 0.125 in holes, drawn by Karen Wickert 10/2/2020. A second plate `Mounting_Plate/WQ-57_unproven` (stock 255 x 165 x 3.175 mm ABS per settings.txt) is marked unproven.
- Shared-mount implication (computed, not a recommendation): Margay's holes (45.847 x 26.035 mm diagonal pair) share no spacing with Okapi's 40 x 80 mm grid. A Margay whose hole pair sat 40.000 mm apart (or 80.000 mm apart) along one axis would drop onto two of Okapi's three standoffs. Hole sizes also differ: Margay `4_40_CLOSE` 2.946 mm vs Okapi `4_40` 3.175 mm; both pass a #4 screw.

### F6. The enclosures are Polycase WH-02, WH-10 and WQ-48 (confirmed)

polycase.com returns HTTP 403 to WebFetch and to curl; the pages were read from the Internet Archive (web.archive.org snapshots 2025-11-28 for WH-02, 2025-11-26 for WH-10, 2025-07-07 for WQ-48), text extracted with Python. Polycase states its dimensions are "approximate" and to use the drawings/models for fit. Inch values pasted; mm computed at 25.4 mm/in.

| Enclosure | External (in) | Approx. internal (in) | Internal (mm, computed) | Internal panel sold | Notes pasted |
|---|---|---|---|---|---|
| WH-02 Hinged NEMA | 5.1 x 3.9 x 2.7 | 4.2 x 3.0 x 2.5 | 106.7 x 76.2 x 63.5 | WH-02K | "Secure your PCB utilizing the 2 mounting bosses located in the base"; IP65, IP66; unit price $13.21 |
| WH-10 Hinged NEMA | 5.9 x 5.9 x 3.5 | 5.2 x 5.2 x 3.3 | 132.1 x 132.1 x 83.8 | WH-10K | "4 mounting bosses located in the base"; $18.54 |
| WQ-48 Hinged Waterproof Box | 8.2 x 6.2 x 3.9 | 7.2 x 5.3 x 3.6 | 182.9 x 134.6 x 91.4 | WQ-48P | polycarbonate, IP65/66/67; $39.19 |

Fit of the repo mounts against these (computed): the WH-02 lid plate's 78.74 mm (3.10 in) length matches the 3.0 in internal width class, and its 54.41 mm width leaves the lid's long axis (4.2 in = 106.7 mm) mostly free, so a WH-02 lid could take a board up to roughly 100 x 70 mm before the cavity, not the plate, limits it (UNVERIFIED: lid cavity depth and lid inner dimensions were not in the page text; need the Polycase drawing). The WH-10 plate (129.93 x 79.93 mm) fits the 132.1 mm internal span. The WQ-48 plate (184.78 x 134.29 mm) matches the 182.9 x 134.6 mm internal footprint to within Polycase's "approximate" tolerance.

### F7. Fab price structure by size (pasted from fab pages, read 2026-11-12)

- JLCPCB, https://jlcpcb.com/help/article/How-do-I-place-an-order: "The cheapest option is $2 for 5pcs, 2-layer, PCB sizes ≤ 10cmx10cm."
- JLCPCB, https://jlcpcb.com/help/article/in-what-cases-will-there-be-charged-extra:
  - Section 7: "For a single PCB that is within or equal to 102*102mm, there is a special price charged only." ... "when it is panelized (i.e. PCB has V-Cuts or routed lines with or without mouse bites between boards), it will turn into its original cost of Engineering fee+board fee." So the special price is lost the moment JLC is asked to panelize, and the real threshold in the help text is 102 x 102 mm.
  - Section 10: "For circuit boards with small dimensions (≤3cm on either one side) ... with a delivery format of "Single PCB", an additional charge will be applied according to the smaller side dimension". Today's Margay short side is 30.404 mm, i.e. 0.4 mm above this surcharge line (computed). Any candidate keeps the short side above 30 mm.
  - Section 15: "When the area of one board exceeds 650 square centimeters, an additional charge will be added every 50 square centimeters." Irrelevant at logger sizes.
  - Stencils: "Generally, the stencil price is calculated by the stencil size."
- JLCPCB stencil page, https://jlcpcb.com/pcb-stencil: "Precise laser-cut stencil starts at just $3 (100 × 100mm)"; frameless stencils "you can customize any dimensions within 650 × 580mm"; "Framed stencils do not support size customization."
- Price above 102 x 102 mm at JLCPCB: not found in a primary source (live quote needed; UNVERIFIED). A JLCPCB blog (https://jlcpcb.com/blog/custom-pcb-cost, via search summary, not opened) advises staying within 100 x 100 mm for prototype rates.
- PCBWay: "$5.00 for 10 pieces of 1-2 layer boards" on pcbway.com promo pages; the 100 x 100 mm limit comes from a PCBWay-sponsored review (radiolocman.com, review article di=534889), not a PCBWay page (search summary only; UNVERIFIED as current).
- OSH Park, https://docs.oshpark.com/services/two-layer/: "$5 per square inch, which includes three copies of your design"; multiples of three; max "16in (406.4mm) by 22in (558.8mm)". Linear in area: no tier. Today's board = 50.145 x 30.404 mm = 2.363 sq in = $11.82 for 3 (computed). 
- Aisler, https://community.aisler.net/t/our-simple-pricing/102 (posted 2023-08-27): "PCB Price = Job Fee + Area x Area-usage Fee x Quantity"; 2-layer 1.6 mm HASL Budget: EUR 12.00 job fee + EUR 0.067 per cm2 (the page's own worked example uses EUR 0.051; inconsistent on the page); "Minimum order quantity is always 3"; prototype stencil EUR 5.00 + EUR 0.095 per cm2. Linear in area: no tier.

Implication (computed, not a recommendation): only JLCPCB (and PCBWay's promo) has a step at 100-102 mm on a side; OSH Park and Aisler charge by area, where growth costs pro rata. A stencil sized for any board up to about 100 x 100 mm costs the JLC minimum.

### F8. Local fabs and assembly houses in Argentina and Nigeria

**Argentina (Buenos Aires): local fabrication, stencils and assembly exist.**
- Ernesto Mayer S.A. (Mayer Circuitos Impresos), "CARLOS PELLEGRINI 1257/61 (B1604ASG) FLORIDA OESTE. BUENOS AIRES - ARGENTINA" (https://mayerpcb.com/, curl + text extraction).
  - https://mayerpcb.com/promociones.php: "PRODUCCIÓN 100% NACIONAL ... SIMPLE FAZ LOTE 3 UNIDADES U$S 79 DOBLE FAZ LOTE 3 UNIDADES U$S 99 METAL CORE (ALUMINIO) LOTE 3 UNIDADES U$S 99 MULTICAPA LOTE 3 UNIDADES U$S 169 * Válido para pedidos de hasta 2 dm2 por circuito". So the size step is 2 dm2 = 200 cm2 per circuit (e.g. 100 x 200 mm or 141 x 141 mm, computed). Today's Margay is 15.2 cm2 (computed).
  - https://mayerpcb.com/montaje.php: "Contando con un equipamiento flexible para montaje SMT y THT, junto con la provisión de stenciles y componentes". Prototypes "En 6 días"; double-sided "3 días".
  - https://mayerpcb.com/stenciles.php: "stenciles en latón y en acero inoxidable". No stencil sizes stated.
  - https://mayerpcb.com/informacion-tecnica.php: hole 0.40 mm, pad/via 0.70 mm, trace/space 0.125 mm, copper-to-edge 0.30 mm. No maximum panel size stated.
  - "Circuitos que Inspiran": prototypes for technical-school and university students "a un precio simbólico".
- Eleprint, "José E. Rodó 5959/63, 1440 ... C.A.B.A" (https://eleprint.com.ar/circuitos-impresos/, via WebFetch summary): double-sided PTH on FR4 0.80-1.6 mm; SMD stencils "fotograbado o Laser", stainless or brass, aluminum frame; no assembly on that page; no size limit stated.
- Dydelec (https://www.dydelec.com.ar/, WebFetch summary): "Montaje de componentes SMD y Convencionales"; +54 11 phone; no sizes.
- Also listed by search (not opened; UNVERIFIED): GS Ingeniería, PCB Factory (Ciudadela), Solydes División PCB (Ezeiza), Exemso, SEI Circuitos.
- None of the Argentine pages read states a maximum board or stencil size.

**Nigeria: no confirmed local bare-board fab found; one large SMT assembler found.**
- Gospell Digital Technology (GDT), 34 Old Aba Road, Port Harcourt (http://gospelldigital.com/, WebFetch): "capable of placing 250,000 components per hour, spread over 3 SMT lines"; "in excess of 150,000 printed circuit boards per month"; products are prepaid meters, vehicle trackers, TV main boards, detonator boards. The page does not say it fabricates bare boards or takes contract work. Port Harcourt, not Lagos.
- "PCBONLINE" lists "Obikings C plot 50, Amuwo Odofin, Lagos, Nigeria" as an office (https://www.electronicsassemblers.com/about/); the page does not place any factory in Nigeria. Treat it as a sales office of an overseas fab (inference).
- Dead ends: Farway "Top 10 PCB suppliers in Nigeria" (farway.hk/technology/425.html) and ensun.io directory (not opened; directory content, unverifiable); Vanguard 2026-04 article on Nigerian tech manufacturing (no PCB content); Lagos/Yaba search for local etching services (only print shops and 3D printing).
- Finding, stated as such: for Lagos the practical route appears to be imported boards and stencils (JLCPCB/PCBWay ship to Nigeria: UNVERIFIED, not checked) with local hand or hot-plate assembly. That makes the overseas fab price tiers in F7 the relevant ones there.

### F1a. DXF agrees with the board files (measured)

`Hardware/Margay_Outline.dxf` parsed by hand (group-code pairs in ENTITIES): 4 lines, 3 arcs (r = 2.0, 1.999, 2.0), square corner at (0, 30.404); holes are CIRCLEs r = 1.473 mm (dia 2.946 mm) at (2.159, 2.159) and (48.006, 28.194); four more small circles are SD and USB-C locating holes. The bottom edge runs from (2.0, 0.0) to (48.145, 0.011): out of square by 0.011 mm over 46 mm, a drafting artifact a v4 outline need not inherit.

### F9. Reflow tooling sizes (sets an upper bound for hot-plate assembly)

- Miniware MHP30: heating area 30 x 30 mm; MHP50: 50 x 50 mm (Miniware MHP50 introduction PDF at core-electronics.com.au and retailer listings, via search summary; consistent across sources). Today's 50.1 x 30.4 mm board already exceeds the MHP30 and only just fits the MHP50 on its long side. Any growth puts these mini plates out of reach.
- UYUE 946-1010: "Platform size: 100*100mm" (diyfixtool.com listing, via search summary; UNVERIFIED primary). 200 x 200 mm plates are sold as "946C" variants by several unbranded sellers (search summary).
- T-962 infrared bench oven: "Soldering area (max) 180 x 235 mm" (Elektor product listing, via search summary, several sources agree).
- Implication (computed): a board up to about 100 x 100 mm (or a panel of smaller boards) fits the common 100 x 100 mm hot plate; up to 180 x 235 mm fits a T-962. Toaster ovens have no standard size (not researched).

### F10. Ecosystem form factors (pasted)

- Adafruit Feather, https://learn.adafruit.com/adafruit-feather/feather-specification: "The 'classic' Feather and Wing size is 0.9" x 2.0" with 0.1" holes at each corner" (22.86 x 50.8 mm). Okapi carries a `FEATHERWING_MIN` footprint (MS1); Margay does not. Margay's long side (50.145 mm) is 0.655 mm short of 2.0 in (computed).
- Arduino Uno Rev3, https://store.arduino.cc/products/arduino-uno-rev3: "Length 68.6 mm", "Width 53.4 mm". Uno hole pattern not retrieved (UNVERIFIED).
- Arduino Nano, https://store.arduino.cc/products/arduino-nano: "18 x 45 mm".
- mikroBUS add-on boards: "Three sizes are prescribed ... S, M and L"; S = 28.6 x 25.4 mm (search summary of the MikroElektronika spec v2.00 and CNX Software); M and L lengths 42.9 and 57.15 mm appear in the spec drawing but were not tied to M and L in the extracted text (UNVERIFIED which is which). mikroe.com returned 403.
- SparkFun Qwiic: Standard breakout 1" x 1" with four holes for 4-40 screws, Micro 0.75 x 0.30 in; SparkFun staff: "we don't have any standard hole pattern for any of our boards, Qwiic included" (community.sparkfun.com thread 47044 and the BMA400 hookup guide, via search summary).
- DIN rail: DIN 43880:1988-12 "Built-in equipment for electrical installations; overall dimensions and related mounting dimensions" is current; module width 1M = 17.5 mm (secondary sources: industriegehaeuse.de series 175, Weidmüller CH20M17; standard text not read). The 45 mm front-face height is from a trade-fair page (UNVERIFIED against the standard). A Margay inside a DIN housing would be limited to a multiple of 17.5 mm minus walls in one direction; Polycase sells DIN-rail kits for WH-02 (DR-10) and WH-10 (DR-16).
- Batteries: README: "three alkaline AA or D cells". Okapi README names the MPD BK-1280-PC6 3x AA holder, 16.70 mm tall, mounts with "2-56 machine screws" (MPD product page via search summary); its footprint and hole spacing were not retrieved (MPD datasheet URL 404; UNVERIFIED). The Margay `BatteryMount_WH10` pocket is 69.0 x 49.0 mm (measured), holder model not stated. 3x D holder footprints (Keystone 1199, 153, 190) were not found in dimensioned form (dead end).
- Screw sizes: Margay holes are 2.946 mm (#4 close fit); Okapi 3.175 mm. Both pass #4-40 (0.112 in = 2.845 mm major diameter, standard value) and nominal M3 (3.0 mm); 2.946 mm is a tight fit for M3 (computed from these numbers; no source read on M3 clearance classes).

### F11. What fixes one dimension (from F2, computed)

- The 10-position terminal body is 25.86 mm long; the 6-position 15.7 mm; each 6.5 mm deep. On a short side of length S, the 10-position block needs S >= about 26 mm plus corner and hole clearance; today S = 30.4 mm leaves a hole in one corner and a square corner at the other.
- The SD holder courtyard is 29.30 x 27.54 mm, card mouth at a long edge. With one machine-assembled side, either the SD holder stays on the bottom as a hand-soldered SMT part or moves to the top beside everything else (an area question for the other agent).
- USB-C courtyard 10.14 mm wide at an edge, overhanging 1.47 mm. The 12 mm coin-cell holder silk extent is 13.5 x 8.9 mm.
- Edge-facing parts today: J2 (left short edge), J3 (right short edge), J4 USB-C and the SD mouth (top long edge). A bigger board that keeps these on edges needs perimeter, not only area: today's perimeter is 2 x (50.145 + 30.404) = 161.1 mm (computed).

## Candidate outlines

Ranked by how many existing things each one reuses, not by preference; the area the board needs (the other agent's question) decides between them. Prices are computed from the formulas in F7 for 3 boards, 2-layer: OSH Park at $5/sq in; Aisler at EUR 12.00 + EUR 0.067/cm2 x 3. "WH-02 fit" compares against Polycase's approximate internal 106.7 x 76.2 mm, before bosses and walls (lid cavity UNVERIFIED). Every candidate keeps the short side above JLCPCB's 30 mm small-board surcharge line and inside the 102 x 102 mm special price and Mayer's 2 dm2 promo, and every candidate needs a new `StencilMount_Margay` pocket.

| Rank | Outline (mm) | Area (cm2) | Enclosure fit | Mount reuse | Fab price | Form-factor match | Okapi match | Costs |
|---|---|---|---|---|---|---|---|---|
| 1 | 50.8 x 40.64 (2.0 x 1.6 in) | 20.6 | WH-02 lid, WH-10, WQ-48 | All four board mounts unchanged if the 45.85 x 26.04 mm diagonal hole pair is kept (the board grows only along the short side, and the WH-02 lid plate is 54.41 mm wide in the 50 mm direction) | OSH $16.00, Aisler EUR 16.15; JLC/PCBWay minimum tier | 0.1 in grid; Feather length (50.8 mm) | none | +36 % area only; perimeter 183 mm against 161 today, so little more edge for terminals |
| 2 | 64.75 x 50.8 | 32.9 | WH-02 (needs a new lid plate: 64.75 exceeds the 54.41 mm plate), WH-10, WQ-48 | WH-10 and WQ-48 standoffs still usable if the old diagonal pair is kept as two of the holes | OSH $25.49, Aisler EUR 18.61 | 0.1 in grid on the short side | Okapi's 64.75 mm width; a hole pair 40.000 mm apart lands on Okapi's H3-H1 standoffs | Two hole patterns on one board if both old and Okapi mounts are to work |
| 3 | 80 x 50 | 40.0 | WH-02 (new lid plate), WH-10, WQ-48 | As rank 2 | OSH $31.00, Aisler EUR 20.04 | none in particular | Holes 80.000 mm apart along the long axis land on Okapi's H3-H2 standoffs; 40.000 mm across lands on H3-H1 | Lid plate redesign |
| 4 | 68.6 x 53.4 (Arduino Uno outline) | 36.6 | WH-02 (new lid plate), WH-10, WQ-48 | As rank 2 | OSH $28.39, Aisler EUR 19.36 | Uno outline; generic Uno cases and standoff kits (Uno hole pattern UNVERIFIED) | none | Uno holes are not on a regular grid (from memory; UNVERIFIED), so matching them costs layout freedom |
| 5 | 100 x 70 | 70.0 | Largest that plausibly fits WH-02 internal (about 3 mm per side, before bosses); WH-10; WQ-48 | WH-10 plate (free room about 125 x 75 mm with standoffs as placed), WQ-48 plate (75 mm free beside the square cutout: tight) | OSH $54.25, Aisler EUR 26.07; JLC/PCBWay minimum tier; JLC $3 100 x 100 mm stencil | Fits a 100 x 100 mm hot plate | Can carry Okapi's full 40 x 80 mm hole L | Out of reach of Miniware-class mini hot plates; OSH cost scales 4.6x today |
| 6 | 100 x 100 | 100.0 | Does NOT fit WH-02 (76.2 mm internal); fits WH-10 (132.1 mm), WQ-48 | WH-10 only after a new plate; WQ-48 plate needs rework | OSH $77.50, Aisler EUR 32.10; top of the JLC/PCBWay tier | Fills a 100 x 100 mm hot plate exactly; JLC stencil reference size | Carries Okapi's full hole L | Loses WH-02; largest price at area-priced fabs |

Not tabled: today's 50.145 x 30.404 mm (15.2 cm2; OSH $11.82, Aisler EUR 15.06) and its grid-rounded 50.8 x 30.48 mm (2.0 x 1.2 in, 15.5 cm2), for reference only. A board that matched Okapi's full 64.75 x 135 mm outline was not costed: it exceeds WH-02 and the JLC tier.

## Open questions for Andy

1. Should v4 keep the 45.85 x 26.04 mm diagonal hole pair (keeps every printed mount and the WQ-48 plate), add Okapi's 40 x 80 mm grid, or both?
2. Is WH-02 still a target enclosure? It is the only one that caps the board near 100 x 70 mm; WH-10 and WQ-48 take 100 x 100 mm.
3. Does "one machine-assembled side" mean the SD holder moves to the top, or stays on the bottom as a hand-soldered part? This sets whether the board grows by about 29 x 28 mm of top area.
4. Which hot plate or oven do you expect a Lagos or Buenos Aires lab to have? A 50 x 50 mm mini plate already cannot take today's board; 100 x 100 mm plates fit every candidate.
5. Which battery holder does `BatteryMount_WH10` (69 x 49 mm pocket) hold, and are D cells still a deployment option? D holders were not found dimensioned.
6. The README says the CR1220 is on the back; the board files and the photo put it on the top. Fix the README line?
7. Should the v4 outline drop the square corner and the 0.011 mm skew of the bottom edge (F1a)?

## Sources checked (dead ends included)

Repository files (all read and measured this session):
- Project-Margay: README.md; Hardware/Margay.brd; Hardware/KiCAD/Margay.kicad_pcb; Hardware/KiCAD/README.md; Hardware/Margay_Outline.dxf; Hardware/Margay_PCB_3v0.STL (50.145 x 30.404 x 1.57 mm); 3Dprint/*.STL (five); Mounting_Plate/Margay-Mounting-Plate_WQ-48/Workpiece 1 and 2 (design.svg, settings.txt); Documentation/MargayGuide_20190730.pdf and _20220622.pdf (no enclosure data); Documentation/images/Margay_v30_top_20250206.jpg and _back_with_quarter_20250206.jpg.
- Project-Okapi: README.md (Housing section); Hardware/Okapi.brd; Hardware/KiCAD-10import/Okapi.kicad_pcb; Mounting_Plate/WH-16/Resnik_Mounting_Plate_Drawing.pdf; Mounting_Plate/WQ-57_unproven/Workpiece 1/settings.txt. Not read: Okapi 3Dprint STLs, WH-16 SVG/STEP/DWG, WQ-57 dev drawings.

Web:
- polycase.com/wh-02, /wh-10, /wq-48, /wh-16, /wh-series: HTTP 403 (WebFetch and curl). Read via web.archive.org snapshots (2025-11-28, 2025-11-26, 2025-07-07). Polycase drawings/STEP not retrieved.
- jlcpcb.com/help/article/How-do-I-place-an-order (read); .../in-what-cases-will-there-be-charged-extra (read); .../extra-charge-for-stencil (only one 37 x 47 cm example); jlcpcb.com/pcb-stencil (read); jlcpcb.com/help/article/how-to-get-2-dollar-pcb (no content). JLCPCB price above 102 mm: not found; Reddit r/synthdiy thread on size thresholds unreachable (ECONNRESET on mirror, old.reddit blocked); github.com/Hive-RSI-Lab/hive-hwde/issues/12 (no measured prices).
- PCBWay: search summaries only (pcbway.com promo pages, radiolocman review). Not opened.
- docs.oshpark.com/services/two-layer/ (read). community.aisler.net/t/our-simple-pricing/102 (read); aisler.net/en/help/pricing (404).
- Argentina: mayerpcb.com index, circuitos-impresos.php, montaje.php, stenciles.php, informacion-tecnica.php, promociones.php (read; stencil.php is 404); eleprint.com.ar/circuitos-impresos/ (read); dydelec.com.ar (read). Listed but not opened: gs-ingenieria.com.ar, pcbfactory.com.ar, portal-industrial (Solydes), exemso.com.ar, seicircuits.com; pcbmay.com "top 10" is a foreign fab's marketing page.
- Nigeria: gospelldigital.com (read); electronicsassemblers.com/about (read; Lagos office only); vanguardngr.com 2026-04 article (no PCB content); farway.hk and ensun.io directories (not opened, unverifiable); Lagos/Yaba local-etching search (nothing).
- Reflow tools: search summaries for Miniware MHP30/MHP50, T-962, UYUE 946 series (primary pages not opened).
- Form factors: learn.adafruit.com Feather specification (read); store.arduino.cc Uno Rev3 and Nano (read); docs.arduino.cc/hardware/uno-rev3 (no dimensions); mikroe.com/mikrobus (403), spec PDF via search summary only; SparkFun Qwiic via search summary; DIN 43880 via secondary sources.
- Battery holders: MPD BK-1280-PC6 datasheet URL guessed at memoryprotectiondevices.com (404); products.memoryprotectiondevices.com/?p=858 (HTTP 500); Keystone 3x D holders (no dimensioned source found).

Scratch scripts (not part of the record): /tmp/claude-1000/-home-awickert-Dropbox-NorthernWidget-github/cf0342fa-36e3-4818-be1e-2b4b31cc1756/scratchpad/stl.py, slice.py, fp.py.

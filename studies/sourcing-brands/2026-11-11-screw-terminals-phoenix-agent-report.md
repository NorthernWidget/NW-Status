Status: COMPLETE

# Phoenix Contact MPT 0,5 2.54 mm screw terminals: extraction for comparison with On Shore OSTVN

Parts: MPT 0,5/10-2,54 (order number 1725737) and MPT 0,5/ 6-2,54 (order number **1725698**, confirmed on Phoenix's own product page, title "MPT 0,5/ 6-2,54 - Bloc de jonction C.I. - 1725698").

Source key:

- **P10** = Phoenix product page for 1725737, French edition (`https://www.phoenixcontact.com/fr-fr/produits/borne-de-circuit-imprime-mpt-0510-254-1725737`), all sections expanded, read 2026-11-11. The page carries the same technical-data fields as Phoenix's PDF datasheet (the PDF itself returned 403 to curl and to WebFetch; see the log).
- **P6** = the same for 1725698 (`.../borne-de-circuit-imprime-mpt-05-6-254-1725698`).
- **DRW** = Phoenix product-family drawing, document 00899121 /03, dated 03.03.2021, "MPT 0,5/..-2,54", files `pxc_1725737_10_03_MPT-0-5-10-2-54_FAM.pdf` (SHA256 1ce7833a..., matches the checksum Phoenix publishes on P10) and `pxc_1725698_10_03_MPT-0-5-6-2-54_FAM.pdf`. The two files render pixel-identically at 100 dpi (6 bytes differ, metadata): one drawing covers 2–12 positions.
- **DIAG** = Phoenix derating diagram image on P6 (`https://caas.phoenixcontact.com/caas/v1/stable/media/48634/full/b1000?format=png`).
- **DK10** = Digi-Key `https://www.digikey.com/en/products/detail/phoenix-contact/1725737/267470`; **DK6** = `https://www.digikey.com/en/products/detail/phoenix-contact/1725698/267466`; both read 2026-11-11.

French labels are quoted where the translation matters.

| # | Field | 10-position (1725737) | 6-position (1725698) | Source |
|---|---|---|---|---|
| 1a | Positions | 10 (1 row, 1 pin per position) | 6 (1 row, 1 pin per position) | P10, P6 |
| 1b | Pitch | 2.54 mm (±0.1 per pitch on DRW) | 2.54 mm | P10, P6, DRW |
| 2a | Clamp type | "Raccordement vissé avec bague" (screw connection with sleeve; Phoenix's English name for the MPT clamp is "tension sleeve", from memory, UNVERIFIED this session). Front view on DRW shows a box-shaped clamp sleeve in a funnel per position, screw from above: a rising-cage type, not screw-on-wire | same | P10, P6, DRW |
| 2b | Screw thread | M1.6 (Digi-Key attribute; not stated on Phoenix's page) | M1.6 (Digi-Key) | DK10, DK6 |
| 2c | Screw head | Slotted ("Fente longitudinale (L)"); Phoenix lists screwdriver SZS 0,4X2,0 (1205202), 0.4 x 2.0 mm blade | same | P10, P6 |
| 2d | Torque | 0.12–0.15 N·m (range given; no separate "maximum") | 0.12–0.15 N·m | P10, P6 |
| 3a | Wire, AWG | 26–20 (IEC data); UL 30–20; CSA 28–20 | same | P10, P6 (approvals block) |
| 3b | Wire, mm² solid | 0.14–0.5 | 0.14–0.5 | P10, P6 |
| 3c | Wire, mm² stranded | 0.14–0.5 | 0.14–0.5 | P10, P6 |
| 3d | Two wires per clamp | 0.14–0.34 mm², solid or stranded, same cross-section | same | P10, P6 |
| 3e | Stripping length | 4.5 mm | 4.5 mm | P10, P6 |
| 3f | Ferrules | Allowed: 0.25–0.34 mm², with or without plastic collar | same | P10, P6 |
| 4a | Rated current, IEC | 6 A ("Intensité nominale IN") | 6 A | P10, P6 |
| 4b | Rated voltage, IEC | 160 V (III/2); 63 V (III/3); 320 V (II/2); rated impulse 2.5 kV in each | same | P10, P6 |
| 4c | IEC standard | Temperature-rise, short-time current and aging tests to DIN EN IEC 60947-7-4 (VDE 0611-7-4):2019-10; clearances and creepage to DIN EN 60947-1:2015-09 | same | P10, P6 |
| 4d | UL rating | cULus Recognized, file E60425 (certificate E60425-19770427): use group B, 125 V, 6 A, 30–20 AWG. The UL standard number (1059) is not printed on the page | same | P10, P6 |
| 4e | CSA rating | CSA 13631: use group B, 125 V, 6 A, 28–20 AWG | same | P10, P6 |
| 4f | VDE | VDE mark 40053682: 160 V, 6 A, 0.14–0.5 mm² | same | P10, P6 |
| 5a | Operating temperature | −40 to 105 °C, "en fonction de la courbe de capacité de courant / de derating" | same | P10, P6 |
| 5b | Derating curve | Present. For 0.5 mm²: 6 A flat to about 83 °C, then falling to 0 A at 105 °C (about 5 A at 90 °C, about 2.5 A at 100 °C; read off the plot, approximate) | same (curve read on P6; P10 lists the same dependence) | DIAG |
| 5c | Storage/transport | −40 to 70 °C, 30–70 % RH | same | P10, P6 |
| 5d | Assembly | −5 to 100 °C ("Température ambiante (montage)"). "Montage" is installation: the ambient range in which the part may be mounted and wired, not an operating limit | same | P10, P6 |
| 6a | Housing | PA (polyamide; grade, e.g. PA66, not stated), green RAL 6021, insulation group I, CTI 600, UL 94 V0, GWFI 850 °C, GWIT 775 °C, ball pressure 125 °C | same | P10, P6 |
| 6b | Contact material | Cu alloy | same | P10, P6 |
| 6c | Plating | Electroplated tin: Sn 5–7 µm over Ni 2–3 µm, at the clamp and at the solder pin; whisker-free per IEC 60068-2-82 / JESD 201 | same | P10, P6 |
| 6d | Screw material | – (not stated) | – | P10, P6 |
| 7a | Body length (w) | 25.86 ±0.20 mm | 15.70 ±0.15 mm | DRW table; P10 "Largeur [w] 25,86", P6 "15,7" |
| 7b | Pin span (a) | 22.86 ±0.20 mm; end pin center 1.5 ±0.1 mm from body end | 12.70 ±0.15 mm; 1.5 mm | DRW |
| 7c | Depth, front to back | 6.2 ±0.15 mm | 6.2 mm | DRW, P10, P6 ("Longueur [l]") |
| 7d | Height above board | 8.5 ±0.15 mm ("Hauteur de montage"). Phoenix's "Hauteur [h] 12 mm" is 8.5 body + 3.5 pin | same | DRW, P10, P6 |
| 7e | Wire entry | Horizontal, parallel to the board ("sens d'enfichage conducteur/circuit imprimé: 0 °") | same | P10 |
| 7f | Entry height above board | Not dimensioned. Scaled from the DRW front view: clamp window center about 2.2 mm, funnel about 0.1–4.6 mm above the board. UNVERIFIED (scaled, not a stated dimension) | same | DRW (scaled) |
| 7g | Pin row position | Pin centerline 3.1 ±0.1 mm from the back face (DRW side view and footprint), hence 6.2 − 3.1 = 3.1 mm from the entry face: centered | same | DRW |
| 8a | Pin cross-section | Rectangular 0.5 ±0.05 x 0.9 +0.05/−0.15 mm (section A-A, sharp-cornered); tapered tip | same | DRW, P10 ("Dimensions des picots 0,5 x 0,9") |
| 8b | Pin length below body (P) | 3.5 ±0.2 mm | 3.5 mm | DRW, P10, P6 |
| 8c | Recommended PCB hole | 1.1 mm drill ("Diamètre de perçage") | 1.1 mm | DRW footprint, P10, P6 |
| 8d | Pins per position | 1 | 1 | P10, P6 |
| 8e | Locating pin / second row | None at 6 or 10 positions. Only 2- and 3-pole versions carry a locating pin: ø1 ±0.1 mm, 1.5 ±0.1 mm long, 2.54 mm behind the pin row, 1.1 mm hole | none | DRW |
| 9a | Wire pull-out | DIN EN 60999-1:2000-12: 0.14 mm² solid and stranded > 10 N; 0.5 mm² solid and stranded > 20 N; damage and loosening test passed | same | P10, P6 |
| 9b | Insulation resistance | > 5 MΩ between adjacent poles, DIN EN 60512-3-1:2003-01 | same | P10, P6 |
| 9c | Withstand voltage | Rated impulse withstand 2.5 kV (III/3, III/2, II/2); no power-frequency dielectric value listed. Clearance min 1.5 mm; creepage min 1.5–1.6 mm | same | P10, P6 |
| 9d | Contact resistance | – (not listed) | – | P10, P6 |
| 9e | Insertion cycles | – (not listed) | – | P10, P6 |
| 9f | Vibration | DIN EN 60068-2-6:2008-10, 10–150–10 Hz, 1 octave/min, 0.35 mm (10–60.1 Hz), 5 g (60.1–150 Hz), 2.5 h per axis, X, Y, Z | same | P10, P6 |
| 9g | Other | Glow wire DIN EN 60695-2-10, 850 °C, 5 s; application note: hold the block while tightening, because a soldered pin alone cannot take the torque (stated for 2- and 3-pole) | same | P10, P6 |
| 10 | Interlocking | Fixed lengths, 2–12 positions, each its own order number (DRW table). No dovetail or end-to-end stacking feature is shown or listed. UNVERIFIED as an absence (not stated either way) | same | DRW |
| 11a | Digi-Key number | **277-1281-ND** (not 277-1233-ND as briefed) | 277-1277-ND | DK10, DK6 |
| 11b | Price, 1 | $7.16 | $4.32 | DK10, DK6 |
| 11c | Price, 10 | $5.873 | $3.541 | DK10, DK6 |
| 11d | Price, 100 | – (Digi-Key showed only the 1 and 10 tiers) | – (same) | DK10, DK6 |
| 11e | Stock | 457 | 3,914 | DK10, DK6 |
| 11f | Lead time | 6 weeks (manufacturer standard) | 6 weeks | DK10, DK6 |
| 11g | Stock history | – (no source showed it) | – | – |
| 11h | Country of origin | DE (Germany) | DE | P10, P6 |
| 11i | Other commercial | Phoenix pack and minimum order 100; 2.692 g per piece; GTIN 4017918116330; status Active | pack 100 (DK); 1.7 g | P10, P6, DK |

## Footprint fit

Margay's footprint (nw-cold-silicon 1X10_SCREW, 1X06_SCREW, as briefed): 1.016 mm drill, 1.524 mm pad, single row at 2.54 mm; outline 3.3 mm to one side of the pin row and 3.2 mm to the other (6.5 mm deep), 25.86 mm long for 10 positions.

**Hole: does not fit as drawn.** The pin is a 0.5 x 0.9 mm rectangle, and a rectangle must pass a round hole on its diagonal:

- nominal: sqrt(0.5² + 0.9²) = sqrt(1.06) = 1.030 mm, which exceeds the 1.016 mm drill;
- largest pin (0.55 x 0.95): sqrt(0.3025 + 0.9025) = 1.098 mm;
- smallest pin (0.45 x 0.75): sqrt(0.2025 + 0.5625) = 0.875 mm.

The finished hole after through-hole plating is smaller than the drill (about 1.016 − 2 x 0.025 = 0.966 mm for typical 25 µm copper; plating thickness is an assumption, not a Phoenix figure). A nominal pin therefore will not enter; only pins near the bottom of the tolerance band will. Phoenix's recommended 1.1 mm drill clears the largest pin by 0.002 mm before plating, which suggests Phoenix's 1.1 mm means a finished-hole-friendly drill size intended for this pin. A 1.1 mm drill in the present 1.524 mm pad leaves a (1.524 − 1.1)/2 = 0.212 mm annular ring.

**Body: fits in depth; exactly at the limit in length.** Depth: the pin row sits 3.1 mm from each face (6.2 − 3.1 = 3.1). The outline gives 3.2 and 3.3 mm, so 0.1 and 0.2 mm of clearance; at the +0.15 mm depth tolerance split evenly (3.175 mm per side) it still fits. Length: Phoenix's 10-position w = 25.86 ±0.20 mm equals the outline's 25.86 mm exactly, with the end pins 1.5 mm from each body end; a part at the upper tolerance runs 0.10 mm past each end. For 6 positions, w = 15.70 ±0.15 mm; the 1X06 outline length was not briefed, but if it follows the same 1.5 mm end rule it is 5 x 2.54 + 3.0 = 15.70 mm (UNVERIFIED, not checked against the library).

Observation: the outline's 25.86 mm length matches Phoenix's MPT 0,5/10 body length to the hundredth, while the 1.016 mm drill does not match Phoenix's 1.1 mm. The footprint outline looks drawn from Phoenix MPT dimensions; the drill does not (hypothesis, not checked against the Eagle library history).

## Sources log

- `https://www.phoenixcontact.com/{us,en-us,en-pc}/products/1725737/pdf`, `.../fr/produits/1725737/pdf`, `.../de/produkte/1725737/pdf` via curl: 403 (Akamai). Dead end.
- `https://www.phoenixcontact.com/fr/produits/1725737/pdf` via WebFetch: 403. Dead end.
- `https://www.phoenixcontact.com/en-us/products/1725737` in Chrome: "Access Denied". Dead end.
- `https://www.phoenixcontact.com/fr/produits/1725737` in Chrome: redirects to `/fr-fr/produits/borne-de-circuit-imprime-mpt-0510-254-1725737`. Read in full (P10); transcript in `/tmp/claude-1000/-home-awickert-Dropbox-NorthernWidget-github/cf0342fa-36e3-4818-be1e-2b4b31cc1756/scratchpad/tb-phoenix/page_1725737_fr_transcript.txt`. Cookie banner answered "Seulement nécessaire".
- `https://www.phoenixcontact.com/fr-fr/produits/1725737/pdf` in Chrome: "Page non trouvée". The product PDF is generated by a button; not retrieved. The page's technical data were used instead.
- `https://www.phoenixcontact.com/product/product/MTcyNTczNw/downloads/12613328?_realm=fr&_locale=fr-FR&licenseTermsAccepted=false` via curl: 200, the family drawing for 1725737, SHA256 matches Phoenix's published value. Saved as `.../scratchpad/tb-phoenix/pxc_1725737_FAM.pdf`, rasterized at 150 and 500 dpi.
- `https://www.phoenixcontact.com/product/product/MTcyNTY5OA==/downloads/12613324?...` via curl: 200, the drawing for 1725698, `pxc_1725698_FAM.pdf`; renders identically to the 10-position file.
- `https://www.phoenixcontact.com/fr-fr/produits/1725698` and a guessed slug: "Page non trouvée". `https://www.phoenixcontact.com/fr/produits/1725698`: redirects to `/fr-fr/produits/borne-de-circuit-imprime-mpt-05-6-254-1725698` (P6), read.
- `https://www.phoenixcontact.com/fr-fr/search?q=1725698`: not found. Dead end.
- `https://caas.phoenixcontact.com/caas/v1/stable/media/48634/full/b1000?format=png`: derating diagram (DIAG), saved `diag_b1000.png`. `.../media/44594/...` is the dimension-drawing thumbnail (not fetched).
- `https://www.farnell.com/datasheets/1725737.pdf`: 200 but an unrelated Fairchild FCD7N60 MOSFET datasheet (Farnell's own numbering). Discarded.
- `https://docs.rs-online.com/1725737.pdf`: 403. `https://media.distrelec.com/Web/Downloads/_t/ds/1725737_eng_tds.pdf`: 404. `https://www.buerklin.com/medias/sys_master/download/1725737.pdf`: 404. `https://www.mouser.com/datasheet/2/324/1725737-1.pdf`: HTML, not a PDF. Dead ends.
- `https://www.digikey.com/en/products/detail/phoenix-contact/1725737/260601` via curl: 403. In Chrome: Digi-Key search for 1725737 led to `/detail/phoenix-contact/1725737/267470` (DK10), read.
- `https://www.digikey.com/en/products/detail/phoenix-contact/1725698/267466` (DK6), read.
- Digi-Key search for 277-1233-ND: page did not refresh before the read; what 277-1233-ND is remains unchecked.
- WebSearch "MPT 0,5/6-2,54 Phoenix Contact order number": distributor listings (Farnell, Bürklin, RS) give 1725698; confirmed on P6.

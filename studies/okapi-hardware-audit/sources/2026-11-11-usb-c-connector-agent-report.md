# USB-C receptacle survey for Okapi v0.8 (J10 and USB2)

Status: COMPLETE

Agent report, 2026-11-11.

**Sourcing criterion (Andy, relayed by the coordinator 2026-11-11):** Digi-Key for everything if possible. Every candidate leads with its Digi-Key part number and stock. A part Digi-Key does not carry is a weaker candidate and is flagged, not dropped. Facts are appended as confirmed, each with its source. UNVERIFIED marks anything not confirmed from a datasheet or distributor page.

## Sources checked

- Same Sky UJ20-C-V-C-2-SMT-TR datasheet https://www.sameskydevices.com/product/resource/uj20-c-v-c-2-smt-tr.pdf (date 03/28/2025) – OK, saved as `2026-11-11-uj20-c-v-c-2-smt-tr-datasheet.pdf`.
- Same Sky UJ20-C-V-G-SMT-P16-TR datasheet https://www.sameskydevices.com/product/resource/digikeypdf/uj20-c-v-g-smt-p16-tr.pdf (date 09/12/2024) – OK (-25 C).
- GCT drawings usb4085/4110/4115/4120/4125/4145/4155/4220/4235 at https://gct.co/files/drawings/ – all OK.
- Molex 2171790001 datasheet at molex.com – curl returned no response (dead end via curl).
- `gh search code` for candidate parts in sparkfun/adafruit/particle-iot orgs – GitHub API rate limit exceeded (dead end this session).

- https://gct.co/files/drawings/usb4105.pdf – OK, saved as `2026-11-11-usb4105-datasheet.pdf`.
- https://www.sameskydevices.com/product/resource/cusb31-cfm2ax-01-x.pdf and `/pdf/...` – 404 (dead end).
- WebSearch "CUSB31-CFM2AX-01-X datasheet Same Sky ..." and "\"CUSB31-CFM2AX-01\"" and "... Adafruit Feather" – no manufacturer part found (dead end).
- `gh search code "CUSB31-CFM2AX"` – Adafruit-derived footprints only; HaasoscopePro BoM pairs it with HCTL HC-TYPE-C-16P-CH3.18-3A-02.
- `Project-Okapi/Hardware/Okapi.brd` lines 3373-3468 (Eagle package with layer-46 slots) and `Project-Okapi/Hardware/KiCAD-10import/Okapi.kicad_pcb` (J10 block, round drills).

- `nw-cold-silicon/nw-cold-silicon.pretty/USB_C_CUSB31-CFM2AX-01-X.kicad_mod` (read pads, 352 lines). A second copy at `Project-Okapi/KiCad-v7import/Okapi.pretty/` differs from byte 38 (format/version header); not compared further.
- `Project-Okapi/Hardware/KiCAD-10import/USB_ISP_Feather.kicad_sch` lines 5109-5166: J10 Footprint `nw-cold-silicon:USB_C_CUSB31-CFM2AX-01-X`, DIGIKEY `2073-USB4105-GF-ACT-ND`, MPN `USB4105-GF-A`.

## Facts: J10 footprint and USB4105 vs CUSB31 compatibility

### The footprint as it stands (nw-cold-silicon, read 2026-11-11)

Coordinates in mm, KiCad footprint frame; Fab outline runs y = 0 to -7.35, x = +-4.47 (so the body is 8.94 wide; y = 0 is one end of the body, the pad row is at the other).

| Feature | Pads | Position | Size | Drill |
|---|---|---|---|---|
| Signal row, 12 SMD pads | A1B12, A4B9, B8, A5, B7, A6, A7, B6, A8, B5, B4A9, B1A12 | y = -7.355; x = -3.20, -2.40, -1.75, -1.25, -0.75, -0.25, 0.25, 0.75, 1.25, 1.75, 2.40, 3.20 | 0.575 x 1.15 (GND/VBUS pairs), 0.275 x 1.15 (the rest) | – |
| Locating pegs, NPTH | 2 unnamed | x = +-2.89, y = -6.28 | 0.65 | 0.65 round |
| Shell, front pair | M1, M2 | x = +-4.32, y = -6.78 | oval 2.0 x 1.0 (rotated 90) | **0.6 round** |
| Shell, rear pair | M3, M4 | x = +-4.32, y = -2.60 | oval 2.0 x 1.0 | **0.6 round** |

- Pitch: 0.5 mm on the inner eight signal pads, 0.65 between x = 1.75 and 2.40, 0.80 between 2.40 and 3.20.
- Paste on F.Paste is drawn as four polygons about 0.99 x 1.98 mm over each shell pad (pin-in-paste).
- Shell drills are round 0.6 mm in a 2.0 x 1.0 oval copper pad. A real shell stake is a flat tab, normally given a slot; this footprint (an Eagle import) has no slot. Whether a 0.6 mm round hole accepts the stakes of either part is checked against the datasheets below.
- CC1 = A5, CC2 = B5: both present as separate pads.

### GCT USB4105 recommended layout (GCT drawing "USB4105", dated 4 October 2019, https://gct.co/files/drawings/usb4105.pdf, "Recommended PCB Layout, as viewed from component side, Tolerance +-0.05 mm"; fetched 2026-11-11)

- Signal pads: 12x, length 1.15; width 4x 0.60 (A1B12, A4B9, B4A9, B1A12) and 8x 0.30; spacings 0.50 / 3.50 / 4.80 / 6.40 across, i.e. x = +-0.25, +-0.75, +-1.25, +-1.75, +-2.40, +-3.20. Matches the footprint's x positions exactly.
- Locating pegs: 2x dia 0.65 at 5.78 apart, 3.68 behind the rear shell row. Footprint: dia 0.65 at x = +-2.89, 3.68 from the rear shell row (6.28 - 2.60). Match.
- Shell stakes: 4 **slots**, 8.64 apart, drilled 0.60 wide; front pair slot 1.70 long in a 2.10 x 1.00 pad, rear pair slot 1.40 long in a 1.80 x 1.00 pad. Rear row 2.60 from the PCB edge; front row 4.18 behind it.
- Footprint y-positions referred to the PCB edge at y = 0: rear shell 2.60, pegs 6.28, front shell 6.78, pad inner edge 6.78 (= 7.355 - 0.575) – all equal the GCT dimensions (2.60, 2.60 + 3.68, 2.60 + 4.18, 12x 4.18).
- Body: 8.94 wide, 7.35 long; footprint Fab outline 8.94 x 7.35. Match.
- Stake length "S" options: blank = 0.95 mm (so USB4105-GF-A has 0.95 mm stakes), 060 = 0.60, 120 = 1.20.
- Electrical: VBUS 5.00 A collectively, GND 6.25 A collectively, A5/B5 (CC) 1.25 A, others 0.25 A per pin; 48 V DC; 20,000 cycles.
- Operating temperature: **-40 to +85 C**. Mating force 5-20 N, unmating 6-20 N after test.
- Pin map: A5 = CC1, B5 = CC2 both brought out; 16 positions (A1/B12, A4/B9, B8, A5, B7, A6, A7, B6, A8, B5, B4/A9, B1/A12), SBU1/SBU2 present.
- Title block: "USB Type C Receptacle for USB 2.0, SMT Type, PCB Top Mount".

**Finding (footprint vs USB4105).** The nw-cold-silicon footprint is the USB4105 land pattern in every position, despite its CUSB31 name. Two deviations: (1) the signal pads are 0.025 mm narrower (0.575 / 0.275 against 0.60 / 0.30; within the drawing's +-0.05 tolerance, cosmetic); (2) **the four shell holes are round 0.6 mm drills, not 0.6 x 1.70 / 0.6 x 1.40 slots, and the copper is 2.0 x 1.0 on both rows (GCT: 2.10 x 1.00 front, 1.80 x 1.00 rear).** A stake that needs a 1.4-1.7 mm long slot cannot enter a 0.6 mm round hole; as drawn, the footprint will not accept the part's shell stakes unless the fabricated board carried slots from another layer. See the PCB check below.

### Where the slots went (Eagle source vs KiCad import)

- `Project-Okapi/Hardware/Okapi.brd` lines 3373-3468, package `USB_C_CUSB31-CFM2AX-01-X` (library `microbuilder`; element J10 at line 5348 carries DIGIKEY `2073-USB4105-GF-ACT-ND`, MPN `USB4105-GF-A`): pads M1-M4 are `drill="0.6" diameter="1" shape="long"`, and **each is overdrawn by a slot outline on Eagle layer 46 (Milling)**: front pair 0.60 x 1.70 (y 5.93-7.63), rear pair 0.60 x 1.20 (y 2.0-3.2). The Eagle board therefore milled slots (rear slots 1.20 long against GCT's 1.40).
- `Project-Okapi/Hardware/KiCAD-10import/Okapi.kicad_pcb`, J10 footprint block: layers used are only F.Cu, F.SilkS, F.Fab; M1-M4 `(drill 0.6)` round; no Edge.Cuts or slot geometry inside the footprint. Same in `nw-cold-silicon.pretty`. **The layer-46 milling slots did not survive the import.** A v0.8 board fabricated from the KiCad footprint as it stands would have four 0.6 mm round holes where the shell stakes go. Fix (not made here; outside scope): oval drills `(drill oval 0.6 1.7)` front and `(drill oval 0.6 1.4)` rear with 1.0 x 2.1 / 1.0 x 1.8 pads per GCT, or the KiCad official USB4105 footprint (checked below).

### What "CUSB31-CFM2AX-01-X" is

- `nw-cold-silicon/PROVENANCE.md` line 29: the package comes from Adafruit's `microbuilder` Eagle library (named by Okapi.brd and Margay.brd).
- `gh search code "CUSB31-CFM2AX"` (2026-11-11): the name appears only as Adafruit-derived footprint/package names (Adafruit Feather ESP32-C6 and ESP32 Feather V2 KiCad conversions, Fritzing Adafruit parts, `microbuilder.lbr` copies). One third-party BoM (drandyhaas/HaasoscopePro, `adc board/bom.csv`) fits this footprint with HCTL `HC-TYPE-C-16P-CH3.18-3A-02` (LCSC C5307756).
- Web searches for "CUSB31-CFM2AX-01" and "CUSB31-CFM2AX-01-X datasheet Same Sky" (2026-11-11) returned no manufacturer part. Same Sky's (CUI's) USB-C part numbers follow `UJ20-...`/`UJ31-...`, not `CUSB31-...`. **No datasheet for a "CUSB31-CFM2AX-01-X" exists that I could find; the manufacturer is UNVERIFIED, and the CUI/Same Sky attribution is not supported by any source found.**
- Consequence for the compatibility question: there is no second land pattern to compare. The footprint *is* the GCT USB4105 recommended layout (all positions match to 0.01 mm), less the slots. USB4105-GF-A fits it once the slots are restored.

### KiCad official library (kicad-footprints, Connector_USB.pretty, master, listed via the GitLab API 2026-11-11)

USB-C receptacle footprints present by exact name: `USB_C_Receptacle_Amphenol_12401548E4-2A`(+`_CircularHoles`), `..._Amphenol_12401610E4-2A`(+`_CircularHoles`), `..._Amphenol_12401948E412A`, `..._Amphenol_124019772112A`, `..._CNCTech_C-ARA1-AK51X`, `..._G-Switch_GT-USB-7010ASV`, `..._G-Switch_GT-USB-7025`, `..._G-Switch_GT-USB-7051x`, `..._GCT_USB4085`, `..._GCT_USB4105-xx-A_16P_TopMnt_Horizontal`, `..._GCT_USB4110`, `..._GCT_USB4115-03-C`, `..._GCT_USB4125-xx-x(-0190)_6P_TopMnt_Horizontal`, `..._GCT_USB4135-GF-A_6P_TopMnt_Horizontal`, `..._HCTL_HC-TYPE-C-16P-01A`, `..._HRO_TYPE-C-31-M-12`, `..._HRO_TYPE-C-31-M-17`, `..._JAE_DX07S016JA1R1500`, `..._JAE_DX07S024WJ1R350`, `..._JAE_DX07S024WJ3R400`, `..._Molex_105450-0101`, `..._Palconn_UTC16-G`, `..._XKB_U262-16XN-4BVC11`. There is no `CUSB31` footprint.

Parsed pads (raw files from `gitlab.com/kicad/libraries/kicad-footprints/-/raw/master/Connector_USB.pretty/`):

| Footprint | Signal pads | Shell holes | Pegs | Courtyard (mm) |
|---|---|---|---|---|
| GCT_USB4105-xx-A_16P_TopMnt_Horizontal | 16 SMD (12 lands), 0.6/0.3 x 1.15, x = +-0.25 ... +-3.20 | 4, x = +-4.32, oval drill 0.6 x 1.7 front (pad 1.0 x 2.1), 0.6 x 1.4 rear (pad 1.0 x 1.8), 4.18 apart | 0.65 at +-2.89 | 10.64 x 8.94 |
| HRO_TYPE-C-31-M-12 | 16 SMD, 0.6/0.3 x 1.45; outer GND/VBUS at x = +-3.25, +-2.45 | 4, +-4.32, oval 0.6 x 1.7 front, 0.6 x 1.2 rear, 4.18 apart | 0.65 at +-2.89 | 10.64 x 9.42 |
| HCTL_HC-TYPE-C-16P-01A | 16 SMD, 0.6/0.3 x 1.3, x as USB4105 | 4, +-4.32, oval 0.6 x 1.7 front, 0.6 x 1.2 rear | 0.65 at +-2.89 | 10.64 x 9.08 |
| JAE_DX07S016JA1R1500 | 18 SMD | 4, +-4.32, pads 1.3 x 2.3 / 1.3 x 2.6, 3.825 apart | 0.6 round + 0.85 x 0.6 oval at +-3.0 | 10.94 x 8.43 |
| GCT_USB4110 | 20 SMD, no THT shell | none (SMD shell tabs) | 0.65 at +-2.89 | 13.4 x 8.94 |

- Observation from the table: USB4105, HRO TYPE-C-31-M-12 and HCTL HC-TYPE-C-16P-01A share shell-stake x (+-4.32), peg positions (+-2.89, dia 0.65) and front-to-rear stake spacing (4.18); they differ in pad length (1.15 / 1.45 / 1.3), outer-pad x (HRO +-3.25/+-2.45 vs +-3.20/+-2.40), and rear slot length (1.4 vs 1.2). This is the widely cloned "16P top-mount" pattern; whether one part solders reliably on another's land pattern is UNVERIFIED (no manufacturer cross-reference found). JAE DX07S016 is a different pattern.

## Facts: J10 candidates (horizontal, top side)

### 1. GCT USB4105-GF-A (current part)

- Digi-Key https://www.digikey.com/en/products/detail/gct/USB4105-GF-A/11198441 (fetched 2026-11-11): DK 2073-USB4105-GF-ACT-ND (cut tape); In-Stock 263,569; Status Active; cut tape $0.800 (1), $0.676 (10), $0.5745 (100); -40 to 85 C; "Surface Mount, Right Angle; Through Hole"; 5 A; title "CONN RCP USB2.0 TYP C 16P SMD RA".
- Datasheet facts above (GCT drawing): -40 to +85 C, VBUS 5 A collectively, CC1/CC2 on A5/B5, 4 through-hole shell stakes 0.95 mm long (standard), 2 locating pegs, top mount on a single-sided board (no bottom parts).
- KiCad official footprint: `USB_C_Receptacle_GCT_USB4105-xx-A_16P_TopMnt_Horizontal` (slots correct).

### 2. JAE DX07S016JA1R1500

- Digi-Key search https://www.digikey.com/en/products/result?keywords=DX07S016JA1R1500 (fetched 2026-11-11): DK 670-DX07S016JA1R1500CT-ND; Active; cut tape $1.800 (1), $1.531 (10), $1.3009 (100); -40 to 85 C; "Surface Mount, Right Angle; Through Hole"; 24 (16+8 dummy); current "0.25A, 1.25A" (VBUS rating UNVERIFIED from this page); USB 2.0; mfr lead time 19 weeks. **Stock: not stated on the fetched page (UNVERIFIED; possibly zero).**
- KiCad official footprint `USB_C_Receptacle_JAE_DX07S016JA1R1500` (4 THT shell holes, 1.3 x 2.3 / 1.3 x 2.6 pads, 3.825 apart; not the USB4105 pattern).

### 3. Molex 217179-0001 (2171790001)

- Digi-Key https://www.digikey.com/en/products/detail/molex/2171790001/13913749 (fetched 2026-11-11): DK 900-2171790001CT-ND; 65,872 in stock; Active; cut tape $0.900 (1), $0.764 (10), $0.6487 (100); -40 to 85 C; "Surface Mount, Right Angle; Through Hole"; 24 (16+8 dummy); 5 A; USB 2.0; lead 8 weeks; datasheet https://www.molex.com/webdocs/datasheets/pdf/en-us/2171790001_IO_CONNECTORS.pdf.
- Not in KiCad official library by exact name (list above).
- Land pattern and stake geometry: see datasheet check below.

### 4. GCT USB4110-GF-A

- Digi-Key search https://www.digikey.com/en/products/result?keywords=USB4110-GF-A (fetched 2026-11-11): DK 2073-USB4110-GF-A-1-ND; 228,801 in stock; Active; cut tape $1.270 (1), $1.076 (10), $0.9147 (100); -40 to 85 C; **"Surface Mount, Right Angle" (no through hole)**; 24 (16+8 dummy); 5 A; USB 2.0; lead 7 weeks.
- KiCad official footprint `USB_C_Receptacle_GCT_USB4110`: 20 SMD pads, no plated shell holes, courtyard 13.4 mm wide. Retention is by SMD shell tabs only.

### 5. GCT USB4085-GF-A (all through-hole, horizontal)

- GCT drawing https://gct.co/files/drawings/usb4085.pdf (title "USB 2.0 Type C Receptacle, Dip Type, PCB Top Mount", 9 April 2018, rev B 28/02/23; fetched 2026-11-11): 16 through-hole signal pins in two rows 1.35 apart, 0.85 pitch (KiCad: drill 0.4); 4 THT shell stakes (KiCad: oval drills 0.6 x 2.1 and 0.6 x 1.4); body 8.94 wide, 9.17 long; top mount, horizontal. Pin table: A5 = CC1, B5 = CC2. VBUS 5.00 A collectively, GND 6.25 A, CC 1.25 A. **-40 to 85 C**. 20,000 cycles.
- Digi-Key https://www.digikey.com/en/products/result?keywords=USB4085-GF-A (fetched 2026-11-11): DK 2073-USB4085-GF-ACT-ND; 78,786 in stock; Active; $0.910 (1), $0.772 (10), $0.6561 (100); "Through Hole, Right Angle"; 5 A; USB 2.0; lead 7 weeks.
- KiCad official footprint `USB_C_Receptacle_GCT_USB4085` (courtyard 10.55 x 10.17).
- Single-sided-board note: no bottom-side *component*, but all 20 leads pass through and are soldered from the bottom (hand, selective/wave, or pin-in-paste). Whether the Okapi assembly flow accepts a THT part is a question for Andy (open question below).

### Rejected while searching (recorded so a restart skips them; flagged, not dropped)

- Würth 632723300011: Digi-Key 732-9618-1-ND, "CONN RCP USB3.1 TYPEC 24P SMD RA", USB 3.2 Gen 2, -40 to 105 C, $4.37/$4.051/$3.145 (1/10/100), 21,791 stock (fetched 2026-11-11). 24-pin SuperSpeed, not USB 2.0 only. Würth 632722300011: no Digi-Key result.
- Amphenol 12401610E4#2A: Digi-Key "CONN RCP USB3.1 TYPEC 24P SMD RA", USB 3.2 Gen 2, 79,753 stock, $1.43/$1.217/$1.0343 (fetched 2026-11-11). SuperSpeed 24-pin.
- Molex 2171750001: Digi-Key "CONN RCP USB2.0 C 6POS SMD RA", **power only** (no D+/D-), 3 A, -40 to 85 C. Unusable for data.
- HRO TYPE-C-31-M-12: no Digi-Key result (search 2026-11-11). LCSC-only part; KiCad footprint exists.

## Facts: USB2 candidates (vertical, top side)

Current part: Molex 105133-0001 vertical micro-B (KiCad footprint `USB_Micro-B_Molex-105133-0001` exists in the official library).

### GCT vertical USB 2.0 family (drawings fetched 2026-11-11 from https://gct.co/files/drawings/<part>.pdf)

**All four GCT vertical USB 2.0 receptacles are rated -25 C to +85 C, not -40 C.**

| Part | Drawing facts | Height above board | Body (W x D) | Retention |
|---|---|---|---|---|
| USB4120-03-C | "USB 2.0 Type C Receptacle, 16contacts, Vertical, SMT, H=6.5mm", 28 Sept 2020, rev A6 29/10/24; VBUS 5.00 A coll., CC 1.25 A; -25 to +85 C; USB-IF TID 11253 | 6.50 | 8.94 x 3.16 (SMT tails span 4.30 +-0.20) | 4 shell stakes, 0.50 wide, 0.95 long (stake pitch 4.80 and 7.50); 2 pegs dia 0.40 |
| USB4235-03-C | "USB2.0 Type C Receptacle, Vertical, SMT, 16Pin", 21 Aug 2024 rev A; VBUS 5.00 A; -25 to +85 C | 6.50 | 8.94 x 3.16; leads span 10.00 +-0.25 wide | through-hole legs 0.50 wide, 1.05 long (Digi-Key highlight calls them "in-line through-hole shell stakes"); 2 pegs dia 0.40 at 7.50 |
| USB4145-03-xxxx-C | "USB2.0 Type C Receptacle, Vertical, SMT, H=7.46mm, 16 Pin", 28 June 2022 rev A2; -25 to +85 C | 7.46 | 8.94 x 3.16; stakes 2x 8.00 apart | 4 stakes 0.70 wide, length S = 0.70 / 1.70 / 2.30 mm by suffix 0070 / 0170 / 0230; 2 pegs dia 0.56 |
| USB4220-03-xxxx-C | "USB2.0 Type C Receptacle, Vertical, SMT, 16Pin"; profile height "H" by suffix (10.4 mm shown; Digi-Key lists 0930 and 1040); -25 to +85 C | 9.3 / 10.4 | UNVERIFIED | UNVERIFIED |

- Pin tables on USB4120/USB4235/USB4145: A5 = CC1 and B5 = CC2 present (16 contacts incl. SBU). (USB4220 pin table not read: UNVERIFIED.)
- None of USB4120/4235/4145/4220 is in the KiCad official library by exact name (list above). The official `GCT_USB4115-03-C` is a USB 3.2 Gen 2 vertical, H = 9.25, -25 to +85 C (drawing usb4115.pdf), 24 signal pads: not USB 2.0 only.
- GCT USB4125 is horizontal 6-pin, 3.00 A, -30 to +85 C; USB4155 is a plug. Neither is a vertical receptacle.


### Same Sky UJ20-C-V-C-2-SMT-TR (vertical, all through-hole, -40 C)

- Datasheet (date 03/28/2025): USB 2.0; VBUS/GND pins collectively 5.0 A; CC (A5, B5) 1.25 A each; others 0.25 A; 20 Vdc; 10,000 cycles; **operating -40 to 85 C**. Pin table: A5 = CC1, B5 = CC2. Recommended PCB layout (page 3): **16 plated through-holes** in two rows (pad 0.60, hole 0.40; 0.90/2.70/4.60/6.50 spans; rows 1.40 apart per drawing) plus 4 slotted shell holes (1.80 x 0.60 pad, 1.40 x 0.40 slot, 4.00 between slot centers in each row; rows 3.86 apart). Mechanical drawing (page 2): body 8.94 wide, 10.0 +-0.25 tall above the board; footprint body outline about 9.50 x 3.80. Despite "SMT" in the name, it is through-hole.
- Digi-Key https://www.digikey.com/en/products/result?keywords=UJ20-C-V-C-2-SMT-TR (fetched 2026-11-11): DK 2223-UJ20-C-V-C-2-SMT-TRCT-ND; 5,181 in stock; Active; $1.010 (1), $0.854 (10), $0.7259 (100); -40 to 85 C; "Through Hole". Siblings listed: UJ20-C-V-C-1-SMT-TR (4,314 stock, $0.81 at 1) and -3- (775 stock, $0.95); their differences (likely height) UNVERIFIED.
- Same Sky offers a PCB footprint and 3D model link (datasheet header "Product Page | 3D Model | PCB Footprint"); KiCad format UNVERIFIED. Not in KiCad official library.

### Same Sky UJ20-C-V-G-SMT-P16-TR (vertical, SMT + stakes, -25 C)

- Datasheet (09/12/2024): operating **-25 to 85 C**.
- Digi-Key https://www.digikey.com/en/products/detail/same-sky-formerly-cui-devices/UJ20-C-V-G-SMT-P16-TR/24818604 (fetched 2026-11-11): DK 2223-UJ20-C-V-G-SMT-P16-TRCT-ND; 4,907 in stock; Active; $1.040 (1), $0.886 (10), $0.7527 (100); "Surface Mount, Through Hole"; USB 2.0; lead 8 weeks. Height UNVERIFIED (not read).

### Molex 217182-0001 (2171820001) (vertical, SMT + retention, -40 C)

- Digi-Key https://www.digikey.com/en/products/detail/molex/2171820001/13913754 (fetched 2026-11-11): DK 900-2171820001CT-ND; **30,240 in stock** (43,200 factory); Active; $1.200 (1), $1.022 (10), $0.8688 (100); **-40 to 85 C**; "Surface Mount, Through Hole"; Mounting Feature "Vertical"; 5 A; USB 2.0; 24 (16+8 dummy); lead 14 weeks; Digi-Key links EDA/CAD models (/en/models/13913754).
- Molex part-detail sheet (via https://store.comet.bg/download-file.php?id=32752, a Molex-generated PDF; saved as `2026-11-11-molex-2171820001-spec.pdf`): "Shielded I/O Receptacle, Type C, Vertical, Surface Mount, **Height 6.40mm**, 16 Circuits"; Status Active; current max per contact 1.25 A; 30 V; durability 10,000; PCB Locator Yes; PCB Retention Yes; Termination Surface Mount; **PCB Thickness - Recommended 0.80 mm**; -40 to +85 C; Molex offers "Symbol and Footprint (Multi-Format)".
- Footprint dimensions, stake form (through-hole vs SMT tabs) and whether retention works in a 1.6 mm board: **UNVERIFIED** (sales drawing 2171820001_sd.pdf not retrievable: molex.com refused curl, WebFetch timed out). The 0.80 mm recommended PCB thickness needs checking against Okapi's board thickness.
- CC1/CC2: 16-circuit USB 2.0 Type-C, so A5/B5 should be present; UNVERIFIED from a pin table.
- Not in KiCad official library.

### Other Digi-Key vertical USB-C seen (Digi-Key keyword searches fetched 2026-11-11)

- Molex 2193200001, "16P HEIGHT 8.8MM TYPE C", USB 2.0, -40 to 85 C, SMT + TH: **0 Digi-Key stock** (5,450 via Marketplace), $2.29 at 1. Weaker on sourcing.
- Molex 2171780001, vertical, USB 2.0, -40 to 85 C, 3,996 stock, $0.89: **24 (6+18 dummy) – power only**, no D+/D-. Unusable for B-SoM data.
- Würth 632722110112, "WR-COM_USB 3.1_TYPE C_VERTICAL", -40 to 85 C, SMT + TH, 6,149 stock, $5.14 at 1: SuperSpeed 24-pin, not USB 2.0 only. Würth offers no vertical USB 2.0 Type-C receptacle in the search.
- Amphenol vertical USB-C seen: 12402082E512A (USB4, $3.72), 10151348-00011LF (upright flag, -25 C). None is a USB 2.0 vertical rated -40 C; the search page was truncated at 18 of 145 results, so this is not exhaustive.

### GCT vertical family, Digi-Key data (keyword searches fetched 2026-11-11)

- USB4120-03-C: DK 2073-USB4120-03-CCT-ND; 99,000 in stock; Active; $0.890 (1), $0.755 (10), $0.6416 (100); -25 to 85 C; "Surface Mount, Through Hole"; lead 7 weeks.
- USB4235-03-C: DK 2073-USB4235-03-CCT-ND; 1,465 in stock; Active; $0.890 / $0.755 / $0.6416; -25 to 85 C; SMT + TH; lead 7 weeks.
- USB4145-03-0070-C: DK 2073-USB4145-03-0070-CCT-ND; 9,924 in stock; Active; $1.050 / $0.890 / $0.7562; -25 to 85 C; SMT + TH; lead 7 weeks.

### Okapi context for USB2 (read 2026-11-11)

- `Project-Okapi/Hardware/KiCAD-10import/Okapi.kicad_pcb`: board `(thickness 1.671118)` (general section, line 6). USB2 is footprint `nw-cold-silicon:USB_MICRO_VERT_MOLEX` (MPN 1051330001) at (178.36, 68.36), rotated 90; its copper pads span 7.40 x 3.25 mm; the footprint has no Fab, silk or courtyard lines. Every vertical USB-C candidate above is wider than this (body 8.94 mm minimum, since the Type-C receptacle shell is 8.34 mm wide by specification).

### Open-hardware use (searched 2026-11-11)

- WebSearch for USB4105/USB4085/USB4110 in Adafruit or SparkFun BoMs found no published BoM naming them. SparkFun forum (https://community.sparkfun.com/t/bom-for-dev-15795/39678): SparkFun does not publish full BoMs with MPNs; the USB-C socket named there is A40-00118-A52-12. USB4105-GF-A is a JLCPCB/LCSC basic-catalog part (LCSC C3020560; also -060 stake variant C3025063), which is why it is common in hobby designs. Adafruit's Eagle footprint `USB_C_CUSB31-CFM2AX-01-X` is the USB4105 land pattern (see compatibility section), so Adafruit Feathers drawn with it use a USB4105-pattern part; which MPN Adafruit buys is UNVERIFIED.
- GitHub code search across adafruit/sparkfun/particle-iot was rate-limited this session (dead end); Particle eval-board connector MPNs UNVERIFIED.
- Digi-Key also stocks USB4105 stake-length variants USB4105-GF-A-060 and USB4105-GF-A-120 (search result URLs https://www.digikey.fi/en/products/detail/gct/USB4105-GF-A-060/14559043 and https://www.digikey.de/en/products/detail/gct/USB4105-GF-A-120/14559037); stock and price not fetched.

## Comparison tables (neutral; no weighting)

### J10: horizontal, top side, USB 2.0 to FT231X

| Candidate | Digi-Key PN | DK stock (2026-11-11) | Status | Temp (C) | VBUS | CC1/CC2 | Shell retention | Single-sided board | KiCad official fp | Price 10 / 100 (cut tape) |
|---|---|---|---|---|---|---|---|---|---|---|
| GCT USB4105-GF-A (current) | 2073-USB4105-GF-ACT-ND | 263,569 | Active | -40 to 85 | 5 A | both (A5, B5) | 4 THT stakes (slots) + 2 pegs | yes (SMT signals, THT stakes) | yes (`..._GCT_USB4105-xx-A_16P_TopMnt_Horizontal`) | $0.676 / $0.5745 |
| GCT USB4085-GF-A | 2073-USB4085-GF-ACT-ND | 78,786 | Active | -40 to 85 | 5 A | both | 4 THT stakes; all 16 signals THT | yes, but every lead is soldered from the bottom | yes (`..._GCT_USB4085`) | $0.772 / $0.6561 |
| Molex 2171790001 | 900-2171790001CT-ND | 65,872 | Active | -40 to 85 | 5 A | UNVERIFIED (16-pos USB 2.0) | "SMT, Right Angle; Through Hole" (stake form UNVERIFIED) | UNVERIFIED | no (Molex multi-format footprint) | $0.764 / $0.6487 |
| JAE DX07S016JA1R1500 | 670-DX07S016JA1R1500CT-ND | not stated (UNVERIFIED; 19-week lead) | Active | -40 to 85 | UNVERIFIED | UNVERIFIED | 4 THT shell holes (KiCad) | yes | yes (`..._JAE_DX07S016JA1R1500`) | $1.531 / $1.3009 |
| GCT USB4110-GF-A | 2073-USB4110-GF-A-1-ND | 228,801 | Active | -40 to 85 | 5 A | UNVERIFIED (16-pos) | **SMT only, no THT stakes** | yes | yes (`..._GCT_USB4110`) | $1.076 / $0.9147 |
| HRO TYPE-C-31-M-12 | **not carried by Digi-Key** (weaker on sourcing) | – | – | UNVERIFIED | UNVERIFIED | both (KiCad pin names) | 4 THT slots + 2 pegs | yes | yes | – |

USB4105 / footprint compatibility: the nw-cold-silicon `USB_C_CUSB31-CFM2AX-01-X` is the GCT USB4105 land pattern (pads, pegs, stake positions all match), but its four shell holes are 0.6 mm round instead of 0.6 x 1.7 / 0.6 x 1.4 slots, because the Eagle layer-46 milling slots were lost in the KiCad import. No "CUSB31-CFM2AX-01-X" manufacturer part was found.

### USB2: vertical, top side, B-SoM USB 2.0 + VBUS

| Candidate | Digi-Key PN | DK stock (2026-11-11) | Status | Temp (C) | Height above board | Footprint / body | Retention | CC1/CC2 | KiCad official fp | Price 10 / 100 |
|---|---|---|---|---|---|---|---|---|---|---|
| Molex 2171820001 | 900-2171820001CT-ND | 30,240 | Active | **-40 to 85** | 6.40 | UNVERIFIED (sales drawing not retrieved); recommended PCB 0.80 mm | "PCB Retention Yes", SMT + TH (form UNVERIFIED) | UNVERIFIED | no (Molex multi-format) | $1.022 / $0.8688 |
| Same Sky UJ20-C-V-C-2-SMT-TR | 2223-UJ20-C-V-C-2-SMT-TRCT-ND | 5,181 | Active | **-40 to 85** | 10.0 | body 8.94 x ~3.8; holes span 6.5 x 3.86 | all-THT: 16 signal holes + 4 slotted shell holes | both | no (Same Sky footprint offered) | $0.854 / $0.7259 |
| GCT USB4120-03-C | 2073-USB4120-03-CCT-ND | 99,000 | Active | -25 to 85 | 6.50 | body 8.94 x 3.16; tails 4.30 deep | 4 THT stakes 0.95 long + 2 pegs | both | no | $0.755 / $0.6416 |
| GCT USB4235-03-C | 2073-USB4235-03-CCT-ND | 1,465 | Active | -25 to 85 | 6.50 | 10.00 wide x 3.16 | THT legs 1.05 long + 2 pegs | both | no | $0.755 / $0.6416 |
| GCT USB4145-03-0070-C | 2073-USB4145-03-0070-CCT-ND | 9,924 | Active | -25 to 85 | 7.46 | body 8.94 x 3.16; stakes 8.00 apart | 4 THT stakes (0.7/1.7/2.3 mm options) + 2 pegs | both | no | $0.890 / $0.7562 |
| Same Sky UJ20-C-V-G-SMT-P16-TR | 2223-UJ20-C-V-G-SMT-P16-TRCT-ND | 4,907 | Active | -25 to 85 | UNVERIFIED | UNVERIFIED | SMT + TH | UNVERIFIED | no | $0.886 / $0.7527 |
| Molex 2193200001 | **0 DK stock** (Marketplace only; weaker) | 0 | – | -40 to 85 | 8.8 | UNVERIFIED | SMT + TH | UNVERIFIED | no | $2.29 at 1 |

Current USB2 footprint (Molex 105133-0001 micro-B) copper spans 7.40 x 3.25 mm; every vertical Type-C body is at least 8.94 mm wide.

## Open questions

1. J10 footprint: restore slots in nw-cold-silicon (oval drills per GCT) or switch J10 to the KiCad official `USB_C_Receptacle_GCT_USB4105-xx-A_16P_TopMnt_Horizontal`? Either way, rename so the footprint name matches the part.
2. Did any fabricated Okapi built from the KiCad files carry round 0.6 mm holes at J10? (Eagle-built boards had the layer-46 slots, if the fab honored layer 46.)
3. Stake length vs Okapi's 1.67 mm board: USB4105-GF-A has 0.95 mm stakes; -120 (1.20 mm) exists. Which length GCT recommends for 1.6 mm is UNVERIFIED.
4. Is through-hole soldering acceptable in Okapi assembly (USB4085, UJ20-C-V-C-2 are all-THT)?
5. Molex 2171820001: need the sales drawing (footprint size, stake form) and whether its 0.80 mm recommended PCB thickness rules out a 1.67 mm board.
6. For USB2, is -25 C acceptable (GCT and Same Sky -G- verticals), or is -40 C a hard requirement (leaves Molex 2171820001 and Same Sky UJ20-C-V-C-2 among Digi-Key-stocked USB 2.0 verticals found)?
7. Height budget beside the M.2 socket / B-SoM: candidates span 6.40-10.0 mm; the 105133-0001 height and the enclosure clearance were not checked.
8. Open-hardware usage of each candidate is largely UNVERIFIED (GitHub search rate-limited).

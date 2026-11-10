COMPLETE

# Okapi v0.7.0: room for ESD/surge protection at external connectors

Method log and per-connector findings appended below as they are finished.


## Method (logged as done)

- Board copied to this folder; never opened in place. Netlist: `kicad-cli sch export netlist --format kicadxml` (net.xml); connector pin/net table from the board's pads via pcbnew (conn_nets.txt). Issue #51 saved as issue51.txt.
- Board outline: 116.10..180.90 x 37.48..172.53 mm (64.8 x 135.05 mm). Footprints: 244 on F, 8 on B (B side: seven SMT solder jumpers JP1..JP7 and LOGO1; no assembled parts on B).
- No rule areas (keepouts) on the board. Zones: GND on B.Cu (2) and on F.Cu (4); non-GND pours on F.Cu only (5V_LP, V_HP x2, 3V3_AUX, 5V_AUX x2, FEATHER_BAT, V_BETA, two inductor nodes).
- 109 of 252 footprints have no courtyard (Eagle import). For those the obstruction is a proxy: bounding box of pads plus F/B Fab and Silkscreen graphics, inflated 0.25 mm (ESTIMATE). The other 143 use their courtyards.
- Copper obstructions: every pad on the layer (THT on both sides), every via, every track on the layer, each inflated by the 0.127 mm netclass clearance. GND pours are treated as free (a refill clears them around new pads); non-GND F.Cu pours are flagged as soft (a part there cuts the pour) but not counted as blocked.

- Free rectangles: grid at 0.05 mm per side, inside the board outline inset 0.3 mm; the largest empty rectangle (min 1 x 1 mm) found, blocked, repeated up to six times. "As-is" = free of courtyards/proxies, pads, tracks and vias. "Reroute" = free of courtyards/proxies and pads only; the tracks crossing it are named. Scripts: occ.py, free.py, plot.py, near.py; raw output out_<region>.txt, free_<region>.json.
- Part land sizes used for "fits" are ESTIMATES (courtyard): SOT-5X3 2.2 x 2.2; SOT-143 3.4 x 3.2; 0402 or X1SON-0402 1.6 x 1.0; SON-6 2x2 2.6 x 2.6; 4-line 2.5 x 1.0 array 3.0 x 1.5; SMF/SOD-123F 4.4 x 2.2; SMA 6.0 x 3.0; SMB 6.5 x 4.0.

## Board-wide facts that change every verdict

- **There is no ground plane.** The only pours are 16 small local zones (largest: B.Cu GND 142.6 mm2 at x 139.9..148.1, y 127.9..154.7). Every GND connection is a track. A clamp needs a GND track or via of its own, and its return path to the connector ground is whatever track exists. The white area in the B-side pictures is bare laminate, not ground.
- **J10's shell pads (M1..M4) have no net**; the USB-C shell floats. USB2's shell pads (P$1, P$3, P$5) are also unconnected.
- **B side**: no assembled parts today (only solder jumpers JP1..JP7 and the logo), so any B-side clamp adds a second assembly side. B side is 60..90 % free in every connector region; F side is 12..21 % free.
- **No keepouts or rule areas** anywhere on the board.
- B silkscreen pin labels sit right beside the J1..J7 pins (Andy's legend text); B-side parts there mean moving that silk.

## Connectors, pins, nets (from the board pads; netlist net.xml agrees by construction, both from the schematic)

"Direct" = the external line reaches an IC pin with no series element.

| Conn | Pin | Net | Goes to | Series element? |
|---|---|---|---|---|
| J10 USB-C | A6/B6 | D+ | R35 27 ohm (to U23 FT231X), C24 12 pF | R35 series (C24 shunt on connector side) |
| J10 | A7/B7 | D- | R34 27 ohm, C23 12 pF | R34 series |
| J10 | A4B9/B4A9 | VUSB | U23.12 VCC, C21, C22, F1 1.5 A PTC | **U23 VCC direct** (ahead of F1) |
| J10 | A5 / B5 | CC1 / CC2 | R85 / R84 5.1k to GND | no IC |
| J10 | A8/B8, M1..M4 | SBU no-connect; shell no net | – | – |
| J1 (8-pos screw, primary bus) | 1 | GND | – | – |
| J1 | 2 | VBUS_PRIME | U19/U20 MIC2544 OUT, U27/U29 TXS0104 and U28 TCA9406 VCCB, C20, R65 | MIC2544 output direct |
| J1 | 3,4 | RX_OUT_PRIME, TX_OUT_PRIME | U29.10, U29.11 (TXS0104) | **direct** |
| J1 | 5,6 | GPIO_1_OUT, GPIO_0_OUT | U29.12, U29.13 | **direct** |
| J1 | 7 | DAC_OUT | U30.1 MCP4726, C33 68 pF | **direct** |
| J1 | 8 | ADC_0 | U33.4 ADS1115 | **direct** |
| J2 (10-pos screw, primary bus) | 1 | ADC_1 | U33.5, JP6 (B-side jumper) | **direct** |
| J2 | 2 | VREF | D6 LM4040, U30.6, R48, C31 | **direct** (reference output) |
| J2 | 3..6 | SCK_OUT, MOSI_OUT, MISO_OUT, CS_OUT | U27.10..13 (TXS0104) | **direct** |
| J2 | 7,8 | SCL_OUT_PRIME, SDA_OUT_PRIME | U28.8, U28.1 (TCA9406) | **direct** |
| J2 | 9, 10 | VBUS_PRIME, GND | as J1 | – |
| J3 (4-pos screw, secondary bus) | 1,2 | GND, VBUS_SEC | VBUS_SEC: U17/U18 MIC2544 OUT, U42, U36, C19, R66 | – |
| J3 | 3,4 | RX_OUT_SEC, TX_OUT_SEC | U42.13, U42.12 (TXS0104) | **direct** |
| J4 (8-pos screw, secondary bus) | 1,2 | GND, VBUS_SEC | – | – |
| J4 | 3,4 | SDA_OUT_SEC, SCL_OUT_SEC | U36.1, U36.8 (TCA9406) | **direct** |
| J4 | 5,6 | ADC_2, ADC_3 | U33.6, U33.7 (+ JP7) | **direct** |
| J4 | 7,8 | GPIO_2_OUT, GPIO_3_OUT | U42.10, U42.11 | **direct** |
| J5 backup pack | P1 / P2 | V_PRIME- / V_PRIME_SENSE | Q6.3 / R73 20 mohm and **U32.11 PAC1934 sense pin direct** | – |
| J6 (screw) and J8 (JST) Li-ion | 1 / 2 | LI- / LI+ | LI-: **U5.3 BQ2980 direct**, R10, C11; LI+: Q1, R9 220R, R11 27R, S5 | – |
| J7 solar | P1 / P2 | GND / V_SOLAR | V_SOLAR: D1 (DO-214AC) anode only | D1 series |
| USB2 micro-USB (B-SoM) | 1 / 2 / 3 / 5 | BSOM_VUSB / PD- / PD+ / GND | F2 PTC and **J9.16 direct**; **J9.13, J9.11 direct** | none on PD+/PD- |
| SD1 microSD | card slot, not an external lead; lines go through U25 buffer | – | – |

**Sensor ports = J1, J2 (primary bus, VBUS_PRIME from U19/U20) and J3, J4 (secondary bus, VBUS_SEC from U17/U18). Signal lines: J1 6, J2 8, J3 2, J4 6 = 22, every one direct into an IC pin** (TXS0104 x3, TCA9406 x2, ADS1115, MCP4726, LM4040). Plus 4 VBUS pins on 2 switched nets.

## J10 USB-C (D+, D-, VBUS). Pictures: /tmp/claude-1000/-home-awickert-Dropbox-NorthernWidget-github/cf0342fa-36e3-4818-be1e-2b4b31cc1756/scratchpad/okesd/J10_F.png, /tmp/claude-1000/-home-awickert-Dropbox-NorthernWidget-github/cf0342fa-36e3-4818-be1e-2b4b31cc1756/scratchpad/okesd/J10_B.png

Measured free area within about 8 mm (window x 116.1..136, y 155..172.6): F 20.7 % free as-is, 34.5 % if tracks moved; B 74.9 % / 94.1 %.
- F as-is: A1 116.45..122.4 x 159.15..162.15 (5.95 x 3.00), empty, directly above C23/C24/R34/R35 and left of U23; A2 128.5..130.1 x 168.95..172.2 (1.60 x 3.25), between R84 and R70.
- F between the J10 pad row (y 166.29) and R34/R35 (y 162.72, 163.87): only a 1.0 mm strip, 116.45..127.45 x 164.45..165.45, and it carries D+, D-, VUSB, GND, USBDP, USBDM. **Nothing fits there as-is.** The connector-side D+/D- run from the pads to R35/R34 pad 2 (120.56) is only 2..4 mm long.
- B as-is: A1 116.4..123.05 x 158.15..164.05 (6.65 x 5.90) under the R/C row; A6 120.1..124.85 x 165.7..167.9 (4.75 x 2.20) under the pad row; also 130.6..134.15 x 162.05..170.85 (3.55 x 8.80). B copper near: GND track y 164.39 (x 119.68..130.22) tied to the J10 GND pad by via (119.30, 164.77); VUSB B track y 165.26 between vias (120.19, 165.26) and (124.25, 165.26).

Options:
1. F, minor re-layout: move C23, C24, R34, R35 up about 2.5 mm into F-A1 (P2), and put TPD2E2U06 (SOT-5X3) or a 3-line SOT-5X3 array in the vacated band about 116.6..122.4 x 162.0..165.4 (P1, about 5.8 x 3.4 including the 1 mm strip; ESTIMATE). Reroute the connector-side D+/D- segments (about 6 short 0.2 mm segments) and the R pad 1 -> U23.8/U23.9 USBDP/USBDM tracks (about 8 segments, now running round U23's lower-left corner). SOT-143 (3.4 x 3.2 est.) is marginal there.
2. VBUS 0402 clamp on F in A2 (P3), "ahead of F1": GND from the existing via (129.08, 168.31) at its top edge; VUSB needs a new trace of about 3 mm from F1 pad 1 (131.87, 167.30) past R70's upper pad. Fits, tight (ESTIMATE).
3. B side, as-is: the D+/D- array in B-A1 (P4) with two new vias on the connector-side D+/D- F tracks between C2x pad 2 (118.81) and R3x pad 2 (120.56), where a 0.6 mm via has about 1.15 mm between pad edges (est.); GND straight from the B GND track at y 164.39. The VBUS clamp (0402) in B-A6 (P5) tapping the B VUSB track at y 165.26; its GND needs one via onto the F GND stub of J10 pad A1B12 (x 119.28) or a jumper across the VUSB track (ESTIMATE).
Verdict J10: **F minor re-layout (move 4 passives); B fits as-is with 2-3 new vias.** A 3-line array covering VBUS too fits the same P1 or P4 spots if its package is SOT-5X3 class.

## J1 and J2 (primary sensor bus, 14 signal lines). Pictures: /tmp/claude-1000/-home-awickert-Dropbox-NorthernWidget-github/cf0342fa-36e3-4818-be1e-2b4b31cc1756/scratchpad/okesd/J1J2_F.png, /tmp/claude-1000/-home-awickert-Dropbox-NorthernWidget-github/cf0342fa-36e3-4818-be1e-2b4b31cc1756/scratchpad/okesd/J1J2_B.png

Window x 116.1..132, y 110..160. F 14.8 % free as-is (24.4 % if tracks moved); B 59.6 % / 92.5 %.
- F: the terminal bodies occupy x 116.61..123.36 (courtyard-less, proxy from Fab outline). The signal tracks leave the THT pins and run straight into U29 (TXS0104), U30 (MCP4726), D6, U33 (ADS1115), U27 (TXS0104) and U28 (TCA9406), whose courtyards start at x 123.6..124. **There is no gap between the terminal body and the ICs.** Largest F as-is pieces are 6..8 mm from the pins and away from the lines: 129.6..132.0 x 136.9..140.25 (2.40 x 3.35), 129.75..130.8 x 145.25..152.0 (1.05 x 6.75). F verdict: **re-layout** (the IC column would have to move right about 3.5-4 mm to open a strip).
- B: THT pins are reachable on B. A series R can sit on B between the pin pad and a via back up to the line's own F track; the clamp sits beside it with GND from a B GND run between J1.1 (y 114.08) and J2.10 (y 157.26). Strip x 120.8..124.5 (P1 in the picture, drawn to 125.5) beside the pins:
  - as-is free: 120.8..122.35 x 118.15..128.65 (1.55 x 10.5) beside J1 RX..DAC; 120.8..124.8 x 138.6..144.2 (4.00 x 5.60) beside J2 SCK/MOSI/MISO.
  - blocking the rest of the strip (B tracks): VBUS_PRIME (y 117.6..154.3, the run joining J1.2 and J2.9, plus 3 vias), 3V3_AUX (y 118.9..125.6), VREF (y 128.6..131.1, via), ADC_0, ADC_1, Net-(JP6-Pad2) (via), BUS_LOGIC_EN_PRIME (via), 5V_AUX (y 135.2..138.6), Net-(D4-BLUE_CATH) (via), V_LI (y 153.7..156.4, via), and GND tracks.
  - If those are moved, x 120.8..123.9 x 135.75..160 (3.10 x 24.25) and x 120.8..123.9 x 118.95..133.05 (3.10 x 14.1) are free; with R1 the free zone widens to x 132 (8.1 x 39.75) once the further B tracks listed in out_J1J2.txt move.
  - Need per line (ESTIMATE): one 0402 R (1.6 x 1.0) + one 0402 clamp (1.6 x 1.0) + one via, in a 2.54 mm pitch cell about 3.6..4.7 mm wide. 14 cells span y 113..158. Fits in the strip once VBUS_PRIME and the short stubs are rerouted; a 4-line array (3.0 x 1.5) per 4 lines instead of single clamps saves about 30 % of the clamp area.
- The 14 new vias land on F inside the terminal-body footprint (x 121..123.4), on each line's own F track, so the F trace after the via stays as it is; the F stub from pin to via is cut. ESTIMATE: this is feasible but needs checking line by line against the F fan-out.
Verdict J1/J2: **F re-layout; B moderate reroute (VBUS_PRIME B run about 37 mm, plus 8-10 short stubs) plus 14 vias, second assembly side.**

## J3 and J4 (secondary sensor bus, 8 signal lines). Pictures: /tmp/claude-1000/-home-awickert-Dropbox-NorthernWidget-github/cf0342fa-36e3-4818-be1e-2b4b31cc1756/scratchpad/okesd/J3J4_F.png, /tmp/claude-1000/-home-awickert-Dropbox-NorthernWidget-github/cf0342fa-36e3-4818-be1e-2b4b31cc1756/scratchpad/okesd/J3J4_B.png

Window x 164..180.9, y 122..158. F 21.3 % free as-is (30.2 %); B 68.6 % (92.1 %).
- F: J3/J4 bodies x 173.66..180.41; lines fan out leftward to U42 (TXS0104), U36 (TCA9406), U33. As-is F: 164.5..173.4 x 144.8..147.65 (8.90 x 2.85), between the ADC_2/ADC_3 fan-out tracks and U1/C3, 1..9 mm from J4.A2/SCL; it could hold 0402s for 2-3 lines with jogs (P3). 164.0..166.95 x 137.05..139.4 (2.95 x 2.35) is 7-10 mm away. F verdict: **re-layout** for all 8 lines; P3 is a partial option.
- B beside the pins (x 171.5..176.2), as-is:
  - 171.5..175.45 x 124.55..131.45 (3.95 x 6.90) beside J3 GND/VBUS;
  - 171.5..176.2 x 134.25..140.5 (4.70 x 6.25) beside J3 TX and J4 GP3, GP2 (P1; J3 RX at y 131.86 is at its upper edge);
  - 169.5..175.4 x 147.3..154.65 (5.90 x 7.35) beside J4 SCL, SDA, VBUS (P2);
  - 164.0..169.5 x 142.8..149.0 (5.50 x 6.20) further in.
  - Between y 140.5 and 147.3 (J4 A3, A2): JP7 (174.67, 142.02) and tracks Net-(JP7-Pad2) (via), ADC_3, SCL_OUT_SEC.
  - A GND B track runs along the pins at x about 175.9 (y 122..156): a ready clamp return.
- Verdict J3/J4: **B fits as-is for 6 of 8 lines (RX, TX, GP3, GP2, SCL, SDA); ADC_2 and ADC_3 need a minor reroute (Net-(JP7-Pad2), SCL_OUT_SEC stubs, ADC_3 stub) or JP7 moved; 8 vias; F re-layout.**

## J5 backup pack (TVS0500 after Q6, or TPD1E10B06 across J5). Pictures: /tmp/claude-1000/-home-awickert-Dropbox-NorthernWidget-github/cf0342fa-36e3-4818-be1e-2b4b31cc1756/scratchpad/okesd/J5toJ8_F.png, /tmp/claude-1000/-home-awickert-Dropbox-NorthernWidget-github/cf0342fa-36e3-4818-be1e-2b4b31cc1756/scratchpad/okesd/J5toJ8_B.png

Window x 145..180.9, y 155..172.6 (J5, J6, J8, J7 together). F 20.4 % free as-is (32.4 %); B 72.3 % (97.1 %).
- F as-is 176.3..180.6 x 156.6..161.85 (4.30 x 5.25), directly above Q6 (P1). Q6 pin 1 V_PRIME is at (177.74, 162.66), about 0.8 mm below the box; a B GND track runs (177.09, 160.95) -> (178.74, 162.60) under the box. TVS0500 (2.6 x 2.6 est.) fits as-is with one GND via onto that B track.
- B as-is 168.6..178.3 x 164.0..167.8 (9.70 x 3.80), just above the J5 and J6 THT pads on B (P2): a TPD1E10B06 across J5 (pads 175.82 and 178.36, y 168.69) fits with two short B traces and no vias.
- Verdict J5: **fits as-is, F (TVS0500 after Q6, one via) or B (across J5, no via).**

## J6 and J8 Li-ion cell (LI+, LI-)

- J6's THT pads on B (LI+ 169.47, LI- 172.01, y 168.69) open onto the same B as-is rectangle (P2). A clamp across LI+/LI- fits as-is on B with no vias; J8 is in parallel on the same nets.
- F: U5, Q1, Q2, R9..R12, C11, C12 fill the area; the nearest F as-is gap is 173.15..174.9 x 158.45..161.25 (1.75 x 2.80), not on LI nets; 157.45..158.65 x 164.0..172.2 (1.2 x 8.2) beside J8's LI+ pin but LI- is 2 mm further across J8.
- Verdict J6/J8: **B fits as-is; F minor re-layout (ESTIMATE).**

## J7 solar (V_SOLAR clamp, SMA/SMB class)

- F: J7 body 151.48..157.18 x 165.42..172.12; D1 (SMA) 148.9..151.2 left of it; L4, C14 above; F GND track (152.70..155.62, y 163.80, 0.61 mm, C14 return to J7.P1) between C14 and J7. Nearest F as-is gap 153.7..158.35 x 160.4..163.35 (4.65 x 2.95): an SMF/SOD-123F (4.4 x 2.2 est.) fits the box, but V_SOLAR cannot reach it without crossing that GND track; SMA (6.0 x 3.0 est.) does not fit. F verdict: **re-layout.**
- B: J7 is fenced. 3V3_CORE (y 170.29, x 141.0..156.5) and BMS_CTR (y 169.86, x 141.2..156.4) run along the bottom edge directly under J7 and D1, then turn north at x 156.4..157.1 and 156.0; V_SOLAR_IN and V_SOLAR_SENSE diagonals (x 149..155, y 158..169) close the top. The B as-is rectangles nearby (145..148.75 x 160.75..169.6, 3.75 x 8.85; 157.4..168.6 x 163.85..172.2, 11.2 x 8.35) cannot be reached from V_SOLAR without crossing one of those runs.
- With 3V3_CORE and BMS_CTR rerouted off the edge (about 16 mm each), the strip 145..157.3 x 169.6..172.2 (about 12 x 2.6, P3) opens for an SMF (fits) or an SMA (marginal, 3.0 est. tall); SMB (4.0) does not fit. V_SOLAR via on the F V_SOLAR track (150.04..153.08 at y 170.62).
- Verdict J7: **B moderate reroute (two B power/control runs), SMF-class package; SMA marginal, SMB needs re-layout. F re-layout.** The 32 V / 40 V clamp selection is separate and still open in #51.

## USB2 (Particle B-SoM micro-USB, optional). Pictures: /tmp/claude-1000/-home-awickert-Dropbox-NorthernWidget-github/cf0342fa-36e3-4818-be1e-2b4b31cc1756/scratchpad/okesd/USB2_F.png, /tmp/claude-1000/-home-awickert-Dropbox-NorthernWidget-github/cf0342fa-36e3-4818-be1e-2b4b31cc1756/scratchpad/okesd/USB2_B.png

Window x 165..180.9, y 58..78. F 12.1 % free (the B-SoM J9 body covers x < 176); B 90.2 %.
- F as-is 176.2..180.6 x 58.0..64.0 (4.40 x 6.00) north of USB2, but PD+/PD- leave the connector south (F tracks x 176.45 and 178.61) under the body; bringing them north passes the P$5 shell tab with about 0.5 mm. F verdict: **re-layout.**
- B as-is 173.55..180.6 x 73.1..78.0 (7.05 x 4.90) south of USB2 (P1), right under the PD+/PD- F tracks; BSOM_VUSB via (177.47, 72.68) at its top edge; F GND track x 173.93 (y 62.7..80.1) at its left edge. A 3-line array fits as-is with 3 new vias (PD+, PD-, GND).
- Verdict USB2: **B fits as-is with 3 vias; F re-layout.**

## Verdict table

| Connector | Lines to protect | F side | B side | Best free area near pins |
|---|---|---|---|---|
| J10 USB-C | D+, D-, VBUS | minor re-layout: move C23/C24/R34/R35 up 2.5 mm into empty 5.95 x 3.00 | fits as-is, 2-3 vias | F 116.45..122.4 x 159.15..162.15; B 116.4..123.05 x 158.15..164.05 (6.65 x 5.90) and 120.1..124.85 x 165.7..167.9 |
| J1 + J2 | 14 signals (+VBUS_PRIME) | re-layout (no gap between terminals and ICs) | moderate reroute (VBUS_PRIME B run + ~10 stubs), 14 vias | B strip x 120.8..123.9, y 113..158 once rerouted; as-is only 1.55 x 10.5 and 4.0 x 5.6 |
| J3 + J4 | 8 signals (+VBUS_SEC) | re-layout (partial: 8.90 x 2.85 at 164.5..173.4 x 144.8..147.65) | fits as-is for 6 lines, minor reroute for ADC_2/ADC_3, 8 vias | B 171.5..176.2 x 134.25..140.5 (4.70 x 6.25), 169.5..175.4 x 147.3..154.65 (5.90 x 7.35) |
| J5 backup | V_PRIME | fits as-is (TVS0500 above Q6, 1 via) | fits as-is (across J5) | F 176.3..180.6 x 156.6..161.85 (4.30 x 5.25); B 168.6..178.3 x 164.0..167.8 (9.70 x 3.80) |
| J6/J8 Li-ion | LI+/LI- | minor re-layout | fits as-is | B 168.6..178.3 x 164.0..167.8 (shared with J5) |
| J7 solar | V_SOLAR | re-layout | moderate reroute (3V3_CORE, BMS_CTR along edge); SMF fits, SMA marginal, SMB no | B 145..157.3 x 169.6..172.2 after reroute |
| USB2 (B-SoM) | PD+, PD-, VBUS | re-layout | fits as-is, 3 vias | B 173.55..180.6 x 73.1..78.0 (7.05 x 4.90) |


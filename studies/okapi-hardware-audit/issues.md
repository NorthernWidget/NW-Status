STATUS: COMPLETE

# Okapi open hardware issues audited against the Eagle files

Date: 2026-10-30. Files: `Project-Okapi/Hardware/Okapi.sch` and `Okapi.brd` (commit b4032d4, 2024-11-04; 376 parts, 345 nets; two layers, 64.75 x 135 mm). Read-only; nothing posted.

## Sources checked

- `gh issue list -R NorthernWidget/Project-Okapi --state open --limit 100` (24 open); `gh issue view N` for every one of them.
- `Okapi.sch` and `Okapi.brd` parsed with xml.etree (parts, nets, unconnected pins, text positions; element positions, contactrefs, pad coordinates, wire layers, GND polygons and vias, MPN attributes).
- `Hardware/Okapi_BoM.csv` (2020) for Q7, XTAL1, U30, U37 MPNs; `README.md` for the panel (Voltaic 6 W); `KiCAD-10import/Okapi_3.kicad_sch` (USB2 still present).
- Datasheets: `/tmp/okapi_route/tlv61220.txt`, `pac1934.txt`; fetched and pdftotext'd: TPL5111 (SNAS659B), MCP23018 (DS22103A), TPS62822 (SLVSDV6C), ATmega1284P (40002070B); Voltaic 6 V panel page (Voc 7.28 V, Vmp 6.23 V).
- Dead ends: LT3652 datasheet (analog.com timed out three times, Mouser mirror timed out, curl refused): its numbers are UNVERIFIED below. TXC 7A crystal PDF unreadable: the 18 pF rating is the issue's claim.

## Facts from the Eagle files

1. IC1 (ATmega1284P) VCC x3, AVCC and AREF are all on **3V3_CORE**, not 5V_AUX as #15, #17 and #28 state. The only nearby decoupling is C42 (1 µF, 0402), 2.2 mm from the AVCC/AREF pads (27, 29) and 6–9 mm from the VCC pads (5, 17, 38); C50 is 31.8 mm away.
2. U41 (MCP23018) runs on 3V3_CORE; its one free pin is GPA2. IC1 has no free port pin.
3. I2C: IC1 SDA goes through U24 (SN74LVC1G3157 SPDT switch, select = PC5 `SDA_CTRL`) to either `SDA_OB` (on-board) or `SDA_EXT` (TCA9406 U28/U36 to the ports); SCL is one net. `SDA_OB` also reaches the 5 V segment through U26 and the SoM through U34 (enabled by 3V3_FEATHER). No discrete pull-up exists on `SDA_OB` or `SCL`; the bus relies on the shifters' internal 10 k, which vanish when 3V3_CORE_ISO is off.
4. U4 (LT3652): pads 9 (BAT) and 10 (SENSE) are both on `V_LI` with no resistor between them; NTC unconnected; TIMER grounded. UNVERIFIED consequence: charge current is set by 100 mV across RSENSE, so RSENSE = 0 leaves the current loop unprogrammed. Not in any open issue.
5. No schematic value: R51, R72–R75 (no MPN either); R54, R84–R87 and D1/D2/D3/D9 (board MPNs present: 10 k, 5.1 k, 5.1 k, 10 k, 10 k).

## Issue rows

| # | Title | Verified against Eagle? | Evidence | Fix scope | Blocks a first build? | Depends on / conflicts |
|---|---|---|---|---|---|---|
| 3 | Always-on port | Premise confirmed (question) | U29 TXS0104: VA = 3V3_CORE_ISO, VB = VBUS_PRIME. No jumper exists. | Both (jumper + TXS→TXB) | No | Question |
| 5 | LTC4412 STAT | Confirmed unconnected | N$46: U7.STAT – R21 470 k – V_BETA only; U7.CTL = GND. | Both (new trace) | No | Wants a pin; only GPA2 is free (conflicts with #26) |
| 7 | Output drain MOSFET Q7 | Confirmed not applied | Q7 drains 5V_AUX, gate from U13. Board MPN and BoM: `2N7002W-7-F`, the part the issue says latches; Q4 and Q8 share it. | BoM | Yes: known field failure, one-line fix | – |
| 13 | v1.0 Updates | 9 of 10 items present | USB-C (J10), LED grid (U45, D10–D18), CSA (U32), FRAM (U35), light/accel/mag (U44/U43/U38), SoM I2C buffer (U34). Its open item, "solar charger performance", overlaps #20 and #30. It lists none of #15–#31. | – | No | Not an umbrella |
| 14 | SIM pins | Confirmed unconnected | J9 SIM_VCC/CLK/DATA/RST unconnected (also NFC, ADC0–7, GPIO0/1, PWM1–3, CS, UB_VBUS). | Both, if routed | No | Question |
| 15 | AREF tied to supply | Confirmed, rail wrong | AREF (pad 29) hard-wired to 3V3_CORE, not 5V_AUX; no AREF capacitor. Datasheet: with "a fixed voltage source connected to the AREF pin, the user may not use the other reference voltage options... they will be shorted to the external voltage" (40002070B). Shorted, not destroyed. | Both | No, while firmware uses REFS=01 (AVCC) only – flag for firmware. | Same cut as #28.2 |
| 16 | PG pull-up to 5 V vs MCP23018 | **Not reproducible** | Path confirmed (U2.PG – R1 180 k – 5V_AUX; net to U41.GPB2), but MCP23018 GPIO absolute maximum is "−0.6 V to 5.5 V" and every GPIO is "5.5 volt tolerant" (DS22103A p. 33, pin table). TPS62822 PG leakage is specified at VPG = 5 V. | None | No | Close with the quote |
| 17 | VCC bypass missing | Partly confirmed | C42 (1 µF) sits by AVCC/AREF; VCC pads 5, 17, 38 have nothing within 6 mm; no GND via within 4 mm of IC1. | Both (3 x 100 nF) | No | – |
| 18 | Crystal load caps | Confirmed arithmetic; part rating unverified | C40, C41 = 12 pF (MPN CL10C120JB8NNNC, a 0603 part on a 0402 footprint). XTAL1 = TXC 7A-8.000MAAE-T, 18 pF per the issue. If so: C_eff = 6 + ~3 = 9 pF; 27 pF gives 16.5 pF. AVR Table 9-5 recommends 12–22 pF, so 27 pF sits just above the AVR's range; 22 pF (C_eff 14 pF) is the in-range compromise. Caps 2.7/3.6 mm from the crystal. | BoM + footprint | No (cold-start margin is the risk) | With #28.3 |
| 19 | No ESD on SoM USB | Confirmed | PD+/PD-: J9.USB_P/N – USB2, no TVS. Primary USB (J10 → R34/R35 → U23) has none either. KiCad import marks UB_USB no-connect but still carries USB2. | Both (1 part per port) | No | Decide first whether USB2 stays |
| 20 | MPPT 6.56 V | Confirmed arithmetic; threshold value UNVERIFIED | R22 143 k, R69 100 k: 2.7 x 2.43 = 6.56 V with the 2.7 V reference the issue cites. Voltaic 6 V panel: Vmp 6.23 V, Voc 7.28 V. R69 = 120 k gives 5.94 V. The !SHDN network (R71 1 M, R70 200 k via Q8 when not charging) also locks the charger out until Vsolar/6 ≥ ~1.2 V, i.e. ~7.2 V. UNVERIFIED (memory): LT3652 wants VIN ≥ VBAT(FLT)+3.3 V = 7.5 V for full current, which a 6 V panel never gives; the panel is the larger question. | BoM (R69) | No | #30 touches the same network; #13 |
| 21 | R72–R75 unvalued | Confirmed | No value, no MPN. R72: V_LI (cell, bidirectional, carries the SoM's 2 A path); R73: V_PRIME; R74: V_SOLAR_IN; R75: V_BETA (core + USB via D9). FSR ±100 mV (pac1934.txt l. 295). R51 (ADDR_SEL) is also unvalued: 0 R = 0x10, 499 R = 0x11... (Table 5-1). | BoM (5 values) | **Yes**: cannot be ordered; firmware address depends on R51 | #30 reads V_LI through R72 |
| 22 | FB dividers too high | **Not reproducible** as stated; one minor finding | U1 TLV61220: R4 1.62 M / R5 180 k → 5.0 V; datasheet asks R2 < 500 k and uses 180 k in its own example (tlv61220.txt l. 766–773); FB current 0.01 µA. U2 TPS62822: R6 820 k / R7 180 k + C6 68 pF → 3.33 V; datasheet asks R2 ≤ 120 k (100 k recommended, CFF 120 pF); FB leakage 10–50 nA. 1.5x the guidance, not 10x. | BoM (R6/R7/C6 → 453 k/100 k/120 pF) if wanted | No | – |
| 23 | /RESET capacitor | Confirmed absent; fix conflicts with auto-reset | RST: IC1.RESET, R52 10 k, S4, U41.!RESET, Q4 drain (RST_TRIG from SoM PWM0), ISP1, C39 (100 nF) whose other end is DTR: the auto-reset coupling, not a bypass. 100 nF to GND would form a 1:1 divider with C39 and halve the DTR pulse. Datasheet: RRST 30–60 k, no capacitor requirement. | Both | No | Retest DTR reset or raise C39 |
| 24 | Ground under switchers | Confirmed for U4; mild for U2, U1 | Bottom-layer non-GND traces within 4 mm of U4: six nets (BMS_CTR, MPPT_SHDN, MPPT_CHRG, MPPT_FAULT, 3V3_CORE, MPPT_VIN_REG); U2/L3: 5V_AUX, 3V3_AUX_PG; U1/L1: V_BETA. GND vias within 2 mm: U4 0 (exposed pad unstitched), U2 3, U1 2. | Layout | No (EMI/thermal) | #30 moves one of those traces |
| 25 | SD series R, power switch | Confirmed; "no power control" overstated | MOSI/SCK/CS come straight from U25 (SN74AUP3G34), MISO straight to IC1/J9/MS1/ISP: no series R. SD1.VDD is on 3V3_AUX, which IC1 switches via POWER_EN (U40 → U2.EN), so a card can be power-cycled, but only with every 3V3_AUX load. | Both (3 R + load switch + a pin) | No | Needs a GPIO: conflicts with #26, #5 |
| 26 | No MCU reset to SoM | Confirmed | J9.RESET on !RST: R86 (10 k) to 3V3_FEATHER, S7. No path from IC1 or U41; the reverse path exists (J9.PWM0 → Q4 → RST). U41 is 37 mm from J9; GPA2 is the only free pin. R86 pulls up to an unsourced rail (#31). | Both (1 trace) | No | Takes GPA2: conflicts with #5, #25 |
| 27 | TPL5111 not suppressible | **Not reproducible**: circuit misread | U8 EN = 3V3_CORE (timer mode); DRVn → U10.ON (FEATHER_BAT switch); DONE from J9.ADC3/MS1.GPIOA3, not IC1. DELAY/M_DRV: R20 130 k or R62 330 k via JP8, plus Q3 (FDN360P, source 3V3_CORE, gate FEATHER_EN = U41.GPB7). FEATHER_EN low drives DELAY high = manual power-on, and "an extended assertion ... will turn on DRVn for a time longer than the programmed time interval" (SNAS659B 7.5.2.1). It is the SoM's power timer, overridable by the expander; it never resets IC1. Findings: R20 → 3943 s (66 min) by Equation 1 set 5; R62 330 k is outside the 500 R–170 k range (7.5.1), so JP8 position 2 is invalid. | BoM (R62) | No | Firmware: FEATHER_EN is an active-low hold-on; 66 min cycle |
| 28 | Minor issues | Mixed, see sub-rows | (1) R34/R35 27 R: FT231X's reference design uses 27 R. (2) AVCC = 3V3_CORE directly; datasheet: "If the ADC is used, it should be connected to VCC through a low-pass filter": confirmed. (3) C42 is 1 µF on schematic and board; the mismatch is MPN CL10B105MO8NNWC (0603) on a C0402 footprint, and C40/C41 share it. (4) "Check current rating!!" sits on the USB & ISP sheet beside F1 (MF-NSMF150-2, 1.5 A) on VUSB → VUSB_POWER → D9 → V_BETA; R84/R85 are 5.1 k by MPN, so the question is what the logger may draw from USB. (5) SDA_OB: 9 chips + 3 shifters, well under 400 pF; the weakness is no discrete pull-up (fact 3). (6) TLV3691 has no threshold variants; U37 is a bare comparator (5V_LP vs V_PRIME → U6.EN), MPN TLV3691IDCKR. | (2) both; (3) BoM/footprint; (4) decision | (3) yes: 0603 parts on 0402 pads will not assemble | (3) with #18 |
| 29 | I2C occupancy | Resolved from files | On-board segment: DS3231M 0x68, BME280 0x77 (SDO high), VEML6030 **0x48** (ADDR = 3V3_AUX), BMA456 0x18 (SDO = GND), MLX90393 0x0C (A0 = A1 = GND), MB85RC512T 0x50 (A0–A2 = GND), PCA9634 0x52 (A1, A4, A6 high), MCP23018 0x20 (ADDR = GND), PAC1934 = f(R51), ADS1115 0x4B (ADDR = 5V_AUX; only one exists, not two), MCP4726A2 0x62 (memory). The external segment reaches IC1 only through U24, so sensor addresses cannot collide with on-board ones: Haar 0x48 and Walrus 0x57 are clear. | BoM (R51) + spec table | No | R51 with #21 |
| 30 | Re-land !FAULT on !SHDN | Confirmed and strengthened | MPPT_FAULT: U4 pad 5 – R56 1 M (3V3_CORE) – U41 pad 19 (GPA4). MPPT_SHDN: pad 3 – R71 1 M (V_SOLAR_IN) – R70 200 k – Q8.D; Q8.G = !CHRG. Pads 3 and 5 are 0.9 mm apart. Lockout recomputed: ~7.2 V; with R56 left, ~5.1 V. Strengthened: NTC floating and TIMER grounded mean !FAULT (NTC or timer fault only) can never assert on this board; the "lost" side of the trade-off is empty. SHDN threshold UNVERIFIED (memory, ~1.2 V). | Layout + schematic (R56 out, net renamed) | No | Firmware: GPA4 becomes CHARGER_SHDN (Okapi_Library#9) |
| 31 | No 3.3 V for the SoM | Confirmed | 3V3_FEATHER: D7, J9 3V3@10/@12, MS1.3V, R86/R87, C37, U34 VB/EN; no source. FEATHER_BAT = V_LI via U10 (ON from U8.DRVn). BSOM_VUSB = 5V_AUX via F2. Core: V_BETA → U1 → 5V_LP → U6 → U9 → 3V3_CORE. PAC1934 !PWRDN = 3V3_CORE, SLOW → GPB4, no pull-up. Not in the issue: U34 (SoM I2C bridge) is enabled by 3V3_FEATHER, so a B-SoM also has no I2C link. | Both | **Yes** with a B-SoM; no with a Boron (its 3V pin sources the net) | Enable from FEATHER_EN; #26's pull-up moves to the new rail |

Skipped (not hardware): #10 (repository housekeeping); #12 (firmware sketch).

## Ranked: fix before a first board is ordered

1. **#21 + #29 (R51)**: five unvalued resistors; nothing can be ordered and the PAC1934 address is undefined. BoM.
2. **#31**: a 3.3 V regulator for the SoM socket, enabled with FEATHER_EN; also restores the SoM I2C bridge. Both. Skip only for a Boron build.
3. **LT3652 RSENSE (no open issue)**: pads 9 and 10 shorted on V_LI, NTC floating. Verify against the datasheet, then add RSENSE in the V_LI trace. Both.
4. **#28.3 + #18**: C40, C41, C42 carry 0603 MPNs on 0402 pads; set C40/C41's value at the same time. BoM/footprint.
5. **#7**: Q7 (Q4, Q8 share the MPN) to 2N7002WT1G. BoM.
6. **#30**: re-land !FAULT on !SHDN, drop R56; the pin it costs can never assert here. Both.
7. **#27 (R62)**: 330 k is outside the TPL5111's range. BoM.
8. **#15 / #28.2**: lift AREF off the rail, add 100 nF; ferrite + caps into AVCC. Both, small.
9. **#17**: three 100 nF at the VCC pads with GND vias. Layout.

## Can wait for a later revision

#3, #5, #14 (questions); #19 (after deciding whether USB2 stays); #20 (R69 → 120 k is one value, but the panel/VIN question belongs with #13's open item); #22 (optional); #23 (only with a DTR retest); #24 (vias at U4's pad are cheap and can ride along with #30); #25 and #26 (one free pin, GPA2: decide which of #5, #25, #26 gets it, or add an expander); #28.1, 28.5, 28.6 (no defect); #28.4 (a decision on USB draw).

## Could not verify from the files alone

Every LT3652 number (2.7 V VIN_REG reference, ~1.2 V SHDN threshold, VIN ≥ VBAT+3.3 V, the RSENSE requirement, NTC-floating behavior); XTAL1's 18 pF rating; #7's bench claim; #24's EMI consequence; MCP4726A2 at 0x62.

## Edit count estimate

Schematic: about 12 (AREF cut + C; AVCC ferrite + 2 C; three VCC caps; RSENSE; R56 out + rename; SoM 3.3 V regulator block of ~4; USB TVS if taken). Layout: about 10 (those parts placed; the !FAULT re-land; vias at U4; three 0402 → 0603 footprints). BoM-only: 9 values (R51, R72–R75, Q4/Q7/Q8 MPN, R62, C40/C41, R69 if taken).

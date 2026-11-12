COMPLETE

# Margay v4.0.0 ESD and surge protection design (agent report, 2026-11-12)

## Findings log

### F1. The board today: connector pins, nets and what each line reaches

Measured from a copy of `Project-Margay/Hardware/KiCAD/Margay.kicad_pcb` at ca24e31 with `pcbnew` (pads and nets), and from `kicad-cli sch export netlist` on `Margay.kicad_sch` (pin functions). Script: scratchpad `v4esd/conn.py`. No protection part exists on any of these nets today.

| Connector pin | Net | Reaches (ref.pin, function) |
|---|---|---|
| J2.1 | GND | GND, by a 0.406 mm F.Cu track |
| J2.2 | 3V3_AUX | U7.5 TPS7A05 VOUT; C15 4.7 µF, C16 0.1 µF; RTC1, U12, U13, U14, U4, U5, J1 supplies |
| J2.3 | TX_EXT | U1.12 ATmega1284P, direct (no resistor) |
| J2.4 | RX_EXT | U1.11, direct |
| J2.5 | ADC_EXT_A0 | U1.37 (PA0/ADC0), direct |
| J2.6 | GPIO_EXT_D0 | U1.43, direct |
| J2.7 | GND | GND, 0.406 mm F.Cu |
| J2.8 | 3V3_AUX | as J2.2 |
| J2.9 | SDA_EXT | U4.1 (SN74LVC1G3157 analog switch, B2) and JP1.2 (to SDA_OB); U4 A side to SDA at the ATmega |
| J2.10 | SCL | U1.19 (PC0/SCL), RTC1.8, U12.4 BME280, U14.3 MCP3421, R16 10 kΩ pull-up to 3V3_AUX; all direct |
| J3.1 | GND | GND, 0.305 and 0.406 mm B.Cu |
| J3.2 | VSWITCH | U11.1 MIC9409 VOUT (input from JP2: VMAIN or 3V3_AUX) |
| J3.3 | VBAT- | Q1.3 drain (DMG3404L, low-side reverse-polarity FET) |
| J3.4 | VBAT+ | Q1.1 gate, U6.4 TPS797 VIN, U8.A2 TPS22916 VIN, C12 1 µF |
| J3.5 | AX | U14.1 MCP3421 VIN+, direct; R24 10 kΩ to GND through JP3 (normally closed) |
| J3.6 | VREF | U13.5/.6 MAX6070BAUT18 output, U1.34 (PA3/ADC3), C18 0.1 µF |
| J4 A4/B9, B4/A9 | VUSB | C6 10 µF, C5 and C11 0.1 µF, D1 BAT43WS (to FT231X VCC), Q3 gate, R21, U9.3 TPS2104 IN2 |
| J4 A6/B6, A7/B7 | D+, D- | C8, C7 12 pF to GND; R4, R3 27 Ω to U2 (FT231X) USBDP/USBDM |
| J4 A5, B5 | CC1, CC2 | R32, R31 5.1 kΩ only |
| J4 A8, B8 | SBU1, SBU2 | unconnected |
| J4 A1/B12, B1/A12, shell S1 x4 | GND | contacts by 0.254-0.305 mm F.Cu tracks; two of the four shell pads have a track (1.3 and 1.9 mm, 0.305 mm), the other two none (the shell's metal joins them) |

Two facts from this that shape the design:
1. **3V3_AUX is off in sleep** (U7 EN from 3V3_AUX_CTRL; `powerAux(OFF)` per the v3.1 room study). VREF (U13 runs from 3V3_AUX), AX (R24 to GND), SCL (R16 pull-up to 3V3_AUX), SDA_EXT (U4 VCC on 3V3_AUX) and VSWITCH therefore sit at 0 V in sleep, and a clamp on them costs no sleep current. Only TX, RX, ADC and GPIO (ATmega pins on the always-on 3V3) and VBAT+ can leak in sleep.
2. **No series element can go on AX or VREF.** AX feeds the MCP3421 directly with R24 as the lower arm of a half-bridge that VREF excites. A resistor in series with VREF drops the excitation that J3 delivers below the voltage that ADC3 measures on the board; a resistor in series with AX adds to the sensor's arm of the divider. Both are measurement errors, not protection (reasoning from the netlist; see F6 for the size).

### F2. The board's ground structure today

Measured with `pcbnew` (scratchpad `v4esd/gnd.py`): 2 copper layers; **no copper zone of any kind** (`Board.Zones()` is empty; the 9 `(zone` entries in the file are keepouts inside J1's footprint). GND is routed as tracks only: 254.9 mm on F.Cu and 152.7 mm on B.Cu, widths 0.152-0.406 mm, with 11 GND vias. The one netclass is Default, 0.2 mm track, 0.1524 mm clearance. H1 and H2 are non-plated holes (`MOUNTING_HOLE4_NP_CLOSE`), so there is no earth or chassis point. Any clamp added to this board returns its current through a 0.3-0.4 mm track, about 1 nH per mm (ESTIMATE, the usual rule of thumb for a thin track over no plane), which is what SLVA680A warns against ("Minimizing inductance between the TVS and ground is critical", quoted in the 2026-11-09 report, F19).

### F3. TPD4E1U06 (TI), the signal-line clamp: datasheet SLVSBQ9E (revised October 2026)

Downloaded 2026-11-12 from `ti.com/lit/ds/symlink/tpd4e1u06.pdf` (plain curl), read with `pdftotext -layout`.
- Four ground-referenced unidirectional channels. DBV (SOT-23-6) pinout, Table 4-1: 1 D1+, 2 GND, 3 D2+, 4 D2-, 5 NC ("Can be left floating, grounded, or connected to VCC"), 6 D1-. No supply pin, so it cannot back-power a rail.
- §5.6: VRWM 5.5 V (defined at IIO = 10 µA); VBR 6.5 min / 8.5 max V at 1 mA; VCLAMP 11 V at 1 A and 15 V at 3 A (8/20 µs); CL 0.8 typ / 1 max pF at 2.5 V bias; **ILEAK 1 nA typ / 10 nA max at VIO = 2.5 V** (25 °C table; leakage at 3.3 V is not specified). Figure 5-6 (typical ILEAK vs temperature at 2.5 V) is drawn on a 0-500 pA axis from -55 to 125 °C.
- §5.1: IEC 61000-4-5 3 A, 45 W (8/20 µs). §5.3: IEC 61000-4-2 ±15 kV contact and air. §5.4 and orderable table: -40 to 125 °C. §7.4.1: "The optimum placement is as close to the connector as possible."
- No automotive (-Q1) version: Digi-Key search "TPD4E1U06Q" returns no result (2026-11-12).
- Digi-Key (fetched 2026-11-12): TPD4E1U06DBVR, 296-35965-1-ND (cut tape), 11,045 in stock, $0.94 at 1, Active.

### F4. Second source for the TPD4E1U06 footprint: USBLC6-4SC6 / USBLC6-4SC6Y (ST), not IP4234CZ6

- **IP4234CZ6 (Nexperia) is NOT a drop-in, though distributor cross-references suggest it.** Its datasheet (Rev. 3.0, 31 January 2018, mirror `cdn.components.ru/media/PDF/7192183.pdf`; Nexperia's own site returns HTTP 403) Table 1: pins 1 and 3 are both "ESD protection I/O channel 1", pins 4 and 6 both channel 2, with a 0.5 Ω series resistance (Table 5, Rs): a two-channel pass-through filter. On a TPD4E1U06 footprint it would join D1+ to D2+ and D2- to D1-. Recorded as a dead end so it is not re-proposed.
- **USBLC6-4SC6Y (ST, automotive)**, datasheet Doc ID 023199 Rev 2, September 2012 (mirror `cdn.components.ru/media/PDF/2182484.pdf`; st.com timed out): pinout 1 I/O1, 2 GND, 3 I/O2, 4 I/O3, 5 VBUS, 6 I/O4, which matches the TPD4E1U06 pad for pad (I/O on 1, 3, 4, 6; GND on 2; pin 5 is NC on the TI part). Table 2 at 25 °C: **IRM 10 nA typ / 150 nA max at VRM = 5.25 V**; VBR (VBUS to GND) 6 V min; VCL 12 V max at 1 A and 17 V max at 5 A (8/20 µs); Ci/o-GND 3 typ / 4 max pF at 1.65 V. Tj -40 to +150 °C (Table 1). Digi-Key: 497-11883-1-ND, 3,006 in stock, $0.80 at 1, Active, AEC-Q101, -40 to 125 °C (TJ).
- **USBLC6-4SC6 (ST, industrial)**: Digi-Key 497-4492-1-ND, 282,690 in stock, $0.57 at 1, Active, -40 to 125 °C (TJ), VRWM 5.25 V. Digi-Key lists it as a "Direct" substitute for the -Y part.
- **The rule that makes the two interchangeable: pin 5 is left unconnected on every J2 and J3 instance.** USBLC6-4's pin 5 is the top of a rail-to-rail steering structure. Tied to 3V3_AUX, it would clamp TX, RX, ADC and GPIO to one diode drop above an unpowered rail in sleep and back-power 3V3_AUX through them; tied to 3V3, it would dump a strike into the logic rail. Floating, its internal 6 V-minimum Zener (VBUS to GND) is the clamp. That floating-pin behavior is reasoning from ST's block structure, not a statement found in the datasheet (UNVERIFIED as an ST statement). At J4, pin 5 goes to VBUS, as the USBLC6-4 intends and the TPD4E1U06 permits.
- Countries: TI is in the US; ST is Franco-Italian, headquartered in Switzerland.

### F5. USB arrays checked against #72's SP0503BAHTG and #55's PRTR5V0U2X

- **SP0503BAHTG (Littelfuse)**, SP05 Series datasheet "Revised: JC.12/11/20" (mirror `cdn.components.ru/media/PDF/1683628.pdf`; littelfuse.com 403): VRWM 5.5 V at IR ≤ 1 µA; leakage 1 typ / 100 nA max at 5.0 V; **capacitance 30 pF typ at 2.5 V, 1 MHz**; 3 A, 25 W 8/20 µs; IEC 61000-4-2 30 kV contact; -40 to 125 °C. Digi-Key F2715CT-ND, 20,508 in stock, $1.50 at 1, Active.
- **PRTR5V0U2X,215 (Nexperia, not Littelfuse as #55 says)**: Digi-Key 1727-PRTR5V0U2X,215CT-ND, **0 in stock, 3,000 expected 22-Nov-2027**, $0.84, -40 to 85 °C, 2 channels, 1 pF. It is a D+/D- array, not the battery TVS #55 proposes it for. Out of the running on stock.
- Consequence: the TPD4E1U06 (0.8 pF typ) beats the SP0503BAHTG (30 pF typ) on D+/D- by a factor of about 37 in capacitance, at a lower price, and it is the same part as the sensor-line clamps. Against today's C7 and C8 (12 pF each on D- and D+), the TPD4E1U06 adds 0.8 pF and the USBLC6-4 3 pF; the SP0503BAHTG would more than triple the line's added capacitance, to about 42 pF (computed). The USB 2.0 full-speed limit on a device's D+/D- capacitance is not checked here (from memory, about 20 pF for the transceiver; UNVERIFIED).

### F6. What leakage and capacitance cost on the precision lines (computed from datasheets)

- **MCP3421** (Microchip DS22003E, downloaded from ww1.microchip.com): LSB 15.625 µV at 18 bits, PGA = 1 (Table 4-1); differential input impedance 2.25/PGA MΩ, "due to 3.2 pF internal input sampling capacitor"; §4.6: "the input source impedance should be zero".
- **AX source impedance** is R24 (10 kΩ, through JP3) in parallel with the sensor's upper arm. For a 10 kΩ upper arm (ESTIMATE: a 10 kΩ thermistor at 25 °C; the sensor is not specified in the board files) that is 5 kΩ. A clamp's leakage through it is an offset:
  - TPD4E1U06: 1 nA typ x 5 kΩ = 5 µV (0.3 LSB); 10 nA max = 50 µV (3.2 LSB).
  - USBLC6-4SC6: 10 nA typ = 50 µV (3.2 LSB); 150 nA max = 750 µV (48 LSB). (The guaranteed figures are at 2.5 V and 5.25 V respectively; AX sits at 0-2.048 V, where leakage is lower than at either.)
  - Consequence: **on AX, the TPD4E1U06 is the part to build with; the USBLC6-4 is an acceptable substitute for the logic lines, but on AX it is a fallback with a possible offset of tens of LSB at its guaranteed maximum.**
- **Capacitance on AX**: 0.8 pF (TI) or 3 pF (ST) beside the MCP3421's 3.2 pF sampling capacitor. A capacitor on a sampling input supplies the charge the sampling switch takes, so a small one does no harm (MCP3421 §4.6 describes the source-impedance error, which capacitance does not add to).
- **Series resistor on AX: none.** 330 Ω in series with the sensor arm is a 330/10,000 = 3.3 % change of a 10 kΩ arm (computed); placed after R24 instead, it adds 330 Ω to the 5 kΩ source impedance against the MCP3421's 2.25 MΩ, a further 0.015 % gain error, about 19 LSB at full scale (computed). Neither is worth it when the clamp alone meets the ESD target.
- **VREF**: MAX6070 output with C18 0.1 µF. 10 nA of clamp leakage against a buffered reference is negligible (no load-regulation figure checked; the MAX6070 datasheet was not opened, UNVERIFIED). 0.8 pF beside 100 nF is nothing. **No series resistor**: the sensor's excitation current would drop across it and put the J3 voltage below the VREF that ADC3 measures; a 1.8 V half-bridge of two 10 kΩ arms draws 90 µA, so 330 Ω drops 30 mV, 1.7 % (computed; same 10 kΩ ESTIMATE).
- **ADC_EXT_A0** (ATmega 10-bit ADC): 10 nA x 10 kΩ = 0.1 mV against an LSB of 3.3 V / 1024 = 3.2 mV (computed; the AVCC/AREF choice is not checked). The 330 Ω series resistor adds 330 Ω to the source impedance; the ATmega's recommended source limit (10 kΩ, from memory, UNVERIFIED) is far above it.
- **I2C**: 0.8 pF per line against the bus's 400 pF limit (NXP UM10204; the figure is from memory, UNVERIFIED here) is negligible. 330 Ω in series raises the low level by the pull-up current: 3.3 V / 10 kΩ (R16) x 330 Ω = 0.11 V; with a sensor's own 2.2 kΩ pull-up also on the line (1.8 kΩ in parallel, 1.8 mA), 0.6 V (computed). UM10204 §7.3 asks the designer to "add the additional resistance into their calculations".

### F7. Sleep-current cost (from F1, F3, F4 and the 2026-11-09 report)

- Lines at 0 V in sleep (3V3_AUX off): 3V3_AUX, SDA_EXT, SCL, AX, VREF, VSWITCH. Cost: 0.
- USB lines (unpowered without a cable): 0.
- TX, RX, ADC, GPIO: only if firmware holds a line high in sleep. Four TPD4E1U06 channels: 4 nA typ / 40 nA max at 2.5 V, 25 °C (2.4 % of the 1.7 µA sleep current at the maximum); four USBLC6-4 channels: 40 nA typ / 600 nA max at 5.25 V (35 % at the maximum, computed). The 3.3 V figures are not specified by either maker.
- VBAT+ with TVS0500: 0.07 nA typ / 5.5 nA max at 5 V, 27 °C; 6.5 nA typ / 220 nA max at 85 °C (SLVSED2C §7.6, from the 2026-11-09 report, F2; the datasheet text was re-checked here). The pack is at most 4.95 V fresh alkaline (#72), below the 5 V VRWM.

### F8. TVS0500 (VBAT+): stock and the second-source search

- Digi-Key (2026-11-12): TVS0500DRVR, 296-48382-1-ND, 1,929 in stock, $1.10 at 1, Active, -40 to 125 °C. DRV pinout (SLVSED2C §6): pins 1-3 GND, 4-6 IN, exposed pad GND. Leadless, so top side only.
- No second source with nA leakage was found. **Closest: ESDA7P60-1U1M (ST)**: Digi-Key 497-16253-1-ND, 80,245 in stock, $0.54 at 1, Active, VRWM 5 V, VBR 6.4 V min, VCL 11.6 V max, 60 A / 700 W 8/20 µs, Tj -55 to 150 °C, 2-pin 1610 UDFN. Its leakage is **200 nA max at 5 V, 25 °C** (web search summary of the ST datasheet and RS listing; the ST PDF itself timed out, UNVERIFIED against ST's document). That is 12 % of the 1.7 µA sleep current at the maximum, 36 times the TVS0500's maximum. A different footprint: the two cannot share pads.
- Not checked: whether a TVS0500-Q1 exists (the -q1 datasheet URL returned an HTML page).

### F9. Footprint areas used below (KiCad 10 standard library, measured with `pcbnew.FootprintLoad`)

Courtyard bounding boxes: SOT-23-6 4.19 x 3.49 = 14.62 mm²; SC-74-6 (SOT-457) 4.49 x 3.49 = 15.67 mm²; SOT-143 3.29 x 3.49 = 11.48 mm²; WSON-6-1EP 2 x 2 mm 2.75 x 2.59 = 7.12 mm²; R_0402 1.95 x 1.03 = 2.01 mm²; R_0603 3.05 x 1.55 = 4.73 mm². A 2-position 2.54 mm terminal: (2-1) x 2.54 + 3.25 = 5.79 mm by 6.75 mm = 39.1 mm² (the body formula calibrated on J2 and J3 in the 2026-11-12 growth-direction report, G3; ESTIMATE for a part not chosen). To turn courtyard area into board area, this report divides by today's top packing density, 0.645 (margay-v4-board-size.md), which is the same rule the area budget used.

J2 and J3 are through-hole (pads on both copper layers); J4's contacts are SMD on top, its shell through-hole.

## Recommendation for v4.0.0

Everything in this section is a proposal for Andy. Thresholds, distances and the earth-point choice that are mine are labeled PROPOSAL.

### 1. Per line

One clamp part number covers every signal line on the board: **TPD4E1U06DBVR** (TI, SOT-23-6, leaded), with **USBLC6-4SC6** or **USBLC6-4SC6Y** (ST) on the same pads as the second source. Pin 5 stays unconnected everywhere except J4, where it goes to VBUS (F4). Series resistors use the 330 Ω 0402 line already on the BoM (Panasonic ERJ-2RKF3300X, P330LCT-ND, 326,441 in stock, $0.10; Yageo RC0402FR-07330RL, 311-330LRCT-ND, 2,769,037 in stock, $0.10; both -55 to 155 °C, Japan and Taiwan). The battery keeps #72's **TVS0500DRVR**.

**J2 (sensor terminal)**
- TX_EXT (3), RX_EXT (4), ADC_EXT_A0 (5), GPIO_EXT_D0 (6): **clamp then 330 Ω**. One TPD4E1U06 ("array A") takes all four. Leakage 1 nA typ / 10 nA max per line at 2.5 V; these four are the only sensor lines that can leak in sleep (F7). On ADC_EXT_A0 the offset is 0.1 mV at most against a 3.2 mV LSB (F6).
- SDA_EXT (9), SCL (10): **clamp then 330 Ω**, on a second TPD4E1U06 ("array B"). The SCL resistor goes between J2.10 and the board's SCL net, so the on-board RTC, BME280 and MCP3421 keep an unresistored bus; the SDA_EXT resistor goes between J2.9 and U4/JP1. 0.8 pF per line; low level up by 0.11 V on R16 alone, 0.6 V with a sensor's 2.2 kΩ pull-up as well (F6). A sensor with pull-ups below about 2 kΩ would eat into the 0.99 V margin of a 0.3 VDD input low (I2C input threshold from memory, UNVERIFIED).
- 3V3_AUX (8): **clamp only**, the third channel of array B. Zero sleep cost (rail off). The fourth channel stays spare. J2.2 shares the net and is left to the net's clamp and C15 (4.7 µF) rather than a third array (PROPOSAL).
- GND (1, 7): the clamps' return (section 2).

**J3 (power and analog terminal)**
- VBAT+ (4): **TVS0500DRVR, IN to VBAT+, GND pins and pad to board GND** (that is, on the GND side of Q1), never from J3.4 to J3.3: a reversed pack would forward-bias it (#72, 2026-11-09 report A2). Leakage 5.5 nA max at 5 V and 27 °C, 220 nA max at 85 °C. Clamp 8.8 V max at 24 A. With C12 (1 µF) beside it. No series element: a PTC was ruled out on 2026-11-09 (F16, recommendation 6).
- VBAT- (3): **nothing**. It reaches only Q1's drain, which conducts to GND once the pack is in; a strike there is a strike on GND. (Q1 DMG3404L drain rating not re-checked, UNVERIFIED.)
- AX (5) and VREF (6): **clamp only, no series resistor** (F1, F6), on one TPD4E1U06 ("array C"), the other two channels spare. Build these with the TI part: its 10 nA maximum is a 3.2 LSB offset on the MCP3421 at a 5 kΩ source, against 48 LSB for the ST part's 150 nA maximum (F6). Zero sleep cost.
- VSWITCH (2): **clamp only**, one channel of a further TPD4E1U06 ("array D") at J3.2. VSWITCH can be VMAIN (up to 5.25 V on USB), inside the 5.5 V VRWM. Zero sleep cost (switched off). Considered and set aside: the TVS0500 here, because SLVSED2C limits its input slew to 2.5 V/µs at 27 °C and the MIC9409's turn-on edge was not checked (UNVERIFIED); and a single-channel TPD1E10B06, which would be a second single-source BoM line to save 11 mm².
- GND (1): bonded to the pour.

**J4 (USB-C)**
- D+ (A6/B6), D- (A7/B7), VBUS (A4/B9, B4/A9): **one TPD4E1U06 ("array E") at the receptacle, on the connector side of R3/R4 (27 Ω) and C7/C8**, with VBUS on one channel and on pin 5. 0.8 pF typ / 1 pF max added to each data line beside today's 12 pF (F5). No sleep cost.
- CC1, CC2: **nothing**; they reach only 5.1 kΩ resistors (2026-11-09 report, recommendation 5). The spare fourth channel of array E can take CC1 at no cost if Andy wants it; CC2 would need another part (PROPOSAL: leave both).
- SBU1, SBU2: unconnected, nothing.
- Shell: all four tabs to the GND pour (section 2).
- Not added: the TPD1S514 OVP (2026-11-09 report, recommendation 3, and #72 "Not recommended"); unchanged.

### 2. Ground

Today: no plane and no pour on either layer; GND is 0.15-0.41 mm tracks; the J4 shell reaches GND through two 0.305 mm tracks; no earth point (F2). A clamp there returns its current through a track of a few nanohenries, and the rise of an IEC 61000-4-2 pulse (sub-nanosecond, from memory, UNVERIFIED) turns that into volts on top of the clamp voltage.

For v4:
1. **A solid GND pour on B.Cu over the whole board**, broken only where J1's own keepouts forbid copper, and **GND fill on F.Cu** wherever the top has room, stitched to B.Cu. PROPOSAL: a stitching via within 0.5 mm of every clamp GND pad, and a row of vias at about 5 mm spacing along each connector strip. A plane, not a pour of islands, is what gives the clamps their low-inductance return (SLVA680A, "Minimizing inductance between the TVS and ground is critical").
2. **Each clamp's GND pin also ties by a short, wide F.Cu connection to its connector's GND pin**: arrays A and B to J2.7 and J2.1 (J2.1 is 5.1 mm from TX at J2.3; J2.7 is 2.5 mm from GPIO and 2.5 mm from 3V3_AUX at J2.8, measured from F1's pad coordinates); arrays C and D and the TVS0500 to J3.1 through the pour (J3.1 is 7.6 mm from J3.4 and 2.5 mm from J3.2); array E to J4's A1/B12 and B1/A12 contacts and the shell.
3. **An earth point at the J2 end.** PROPOSAL: make H1 (2.946 mm, today non-plated, 4.0 mm from J2.10, center to center) a plated hole with a GND annular ring tied into the pour, marked EARTH on the silkscreen, for a ring lug and a short heavy wire to the rod. Campbell asks for 14 AWG minimum to its brass lug (2026-11-10 commercial report, C6); a 2.54 mm screw terminal like J2 will not take that gauge (the terminal's wire range was not looked up, UNVERIFIED), which is why a lug rather than a terminal position. Cable shields go to J2.1 or J2.7 at the logger end only (Campbell CR300 manual, quoted in the same report). Board GND and earth are one net, bonded at that one point, as Campbell's loggers do; no separate chassis net (PROPOSAL). Fallback with no copper change: J2.1 labeled EARTH, which is what #72 asks for v3.1.

### 3. Placement rules and area

Rules (TI §7.4.1 for TPD4E1U06, SLVSED2C §11.1 for TVS0500, SLVA680A; distances are PROPOSALS):
- The line runs **pin, then clamp pad, then series resistor, then IC**, with the trace passing through the clamp pad (no stub). The clamp sits within 3 mm of its pin and closer to the pin than any IC is.
- The series resistor sits immediately after the clamp on the IC side, not at the IC. Placed there, it limits the current into the ATmega's own diodes to (15 V - 3.8 V) / 330 Ω = 34 mA during a 3 A, 8/20 µs surge at the TPD4E1U06's 15 V clamp (computed; 3.8 V is the ATmega's VCC + 0.5 V absolute maximum, from memory, UNVERIFIED).
- Clamp GND: section 2.
- No pin of any array is tied to 3V3 or 3V3_AUX.
- On the bottom (if a growth option leaves no top room): the SOT-23-6 arrays qualify under the one-machine-side rule (leaded, iron-soldered) and can sit on B.Cu directly at J2's and J3's through-hole pads. The 0402 resistors and the TVS0500 (leadless WSON) cannot; on the bottom the resistors become 0603 (4.73 mm² each instead of 2.01, a new BoM line).

Area, summed per connector (F9; "board area" = courtyard / 0.645):

| Connector | Parts | Courtyard (mm²) | Board area (mm²) | Where |
|---|---|---|---|---|
| J2 | 2 x TPD4E1U06, 6 x 330 Ω 0402 | 29.24 + 12.06 = 41.30 | 64.0 | top, a strip along J2's inner edge (x > 130.2 today), pins 3-10 |
| J2, resistors on the bottom as 0603 | 2 x TPD4E1U06, 6 x 0603 | 29.24 + 28.38 = 57.62 | 89.3 | all bottom |
| J3 | 2 x TPD4E1U06, TVS0500 | 29.24 + 7.12 = 36.36 | 56.4 | top; or arrays on the bottom and only the TVS0500 on top (7.12, 11.0 board area) |
| J4 | 1 x TPD4E1U06 | 14.62 | 22.7 | top, between J4's contact row and R3/R4 |
| Earth lug | H1 plated | 0 | 0 | the hole and its keepout already exist |
| Total | 5 x TPD4E1U06, TVS0500, 6 resistors | 92.28 | 143.1 | |

Read against the growth-direction report's free-area table (G3, its numbers, not recomputed here; top / bottom mm² within 8 mm of J2's pins, 6 mm of J3's and J4's):
- J2 needs 64 mm² on top: met by A1 (78.6), B2 (150.6) and C1 (69.3); not by S0, A0, B1 or B3 (42.5-55.2). In every scenario the bottom has 91.2-280.5 mm² there, enough for the all-bottom variant (89.3), but only just in S0, A0, A1, B1, B3 and C1 (91.2-103.9).
- J3 needs 56 mm² on top for all three parts: met by A1 (67.4) and C1 (79.5); B1 (54.1) is just short. With the arrays on the bottom (162.7-196.3 mm² there in every scenario), the top need is 11 mm² for the TVS0500, which S0's 10.7 almost meets and every other scenario meets.
- J4 needs 23 mm² on top: met by every scenario (27.2-76.8).
- Only **A1 and C1** give J2 and J3 their full top-side protection; **B2** is the only one that gives J2 room for the resistors, clamps and a future earth terminal with margin, but it leaves J3 at 11 mm², so J3's arrays would go on the bottom.

### 4. What changes from #72's v3.1 plan, and what v3.1 keeps

Changes for v4:
1. **USB: TPD4E1U06 in place of SP0503BAHTG.** 0.8 pF typ against 30 pF typ on D+/D-, $0.94 against $1.50, and the same part as every other clamp (F3, F5). #72's alternative (TPD2E2U06 plus TPD1E10B06) becomes unnecessary.
2. **Clamp before resistor, at the pin.** #72's priority 4 puts the J2 clamps "behind the resistors", and the room study placed the 4-line clamp 7-8 mm from the connector at U1 for that reason. TI's layout rule for this part ("as close to the connector as possible", §7.4.1), SLVA680A ("Place the TVS as near to the connector as design rules allow") and SLAA530B (a resistor used as the primary protection "must withstand the full electrostatic voltage", quoted in the 2026-11-10 open-loggers report) all point the other way. With room in v4, the clamp goes at the pin and the resistor behind it.
3. **Discrete 330 Ω resistors instead of the 4 x 0402 array**, from the existing BoM line: one fewer new part, no estimated footprint, and the room v4 gives makes the array's density unnecessary.
4. **SOT-23-6 clamps, all one part, with a second source on the same pads,** instead of #72's SC-70-6 clamps and the USON-10 4-line option (leadless, fails the bottom rule; larger-board report).
5. **VSWITCH and 3V3_AUX are protected**, no longer optional: they cost no sleep current.
6. **A GND pour and an earth lug** (section 2), which #72 does not cover beyond labeling an existing GND terminal.
7. Unchanged: TVS0500 on VBAT+ on the GND side of Q1; no OVP, PTC or battery overvoltage IC; the ±8 kV contact IEC 61000-4-2 target and no surge claim without a test.

Corrections to #55 (the v4 issue this report answers): PRTR5V0U2X is a Nexperia two-line USB data array, not a Littelfuse battery TVS, and Digi-Key has none until 22-Nov-2027 (F5). A conventional SMBJ5.0A-class TVS leaks hundreds of µA at 5 V (SMAJ5.0A: 800 µA max, 2026-11-09 report F11; SMBJ itself not checked), 470 times the sleep current at that figure. #55's 5.5 V battery maximum predates the ban on lithium cells; the pack is now at most 4.95 V fresh. The SRDA3.3-4 was not checked here.

What v3.1 should still carry, so that nothing is built twice:
- **Keep: the USB clamp at J4.** The room study found a SOT-143 fits behind J4 with no track moved. Use the TPD4E1U06 there if its 4.19 x 3.49 mm courtyard fits the same spot (0.9 mm wider than SOT-143's; not checked here), else SP0503BAHTG, the Mayfly's part.
- **Keep: 330 Ω on SDA_EXT and SCL**, which fit as routed, with the SCL resistor on the J2 side of the on-board bus as above.
- **Keep: the earth label on J2.1 and the README field-installation text** (no copper).
- **Move to v4: the four J2 signal resistors (the array), every clamp, and the TVS0500.** Each needs tracks moved and, for the 4-line clamp, untested routing around U1, and v4 replaces all of it with a different part and a different order. The TVS0500 needs 3V3, SCL and SDA_OB moved (room study); the 1 µF C12 already on VBAT+ absorbs an 8 kV discharge's charge as a step of about 1.2 V (2026-11-09 report A1, an estimate) in the meantime. If Andy's v3.1 reroute moves those three tracks anyway, the TVS0500 can go in then and carry over to v4 unchanged.

## Per-connector table

| Connector | Line (pin) | Protection | Part (second source) | Package | Leakage, datasheet | Courtyard (mm²) |
|---|---|---|---|---|---|---|
| J2 | TX_EXT (3) | clamp, then 330 Ω | TPD4E1U06DBVR array A (USBLC6-4SC6); ERJ-2RKF3300X (RC0402FR-07330RL) | SOT-23-6; 0402 | 1 typ / 10 max nA at 2.5 V (ST: 10 / 150 nA at 5.25 V) | share of 14.62; 2.01 |
| J2 | RX_EXT (4) | clamp, then 330 Ω | array A; 330 Ω | as above | as above | share; 2.01 |
| J2 | ADC_EXT_A0 (5) | clamp, then 330 Ω | array A; 330 Ω | as above | as above; 0.1 mV max offset at 10 kΩ | share; 2.01 |
| J2 | GPIO_EXT_D0 (6) | clamp, then 330 Ω | array A; 330 Ω | as above | as above | share; 2.01 |
| J2 | SDA_EXT (9) | clamp, then 330 Ω | TPD4E1U06DBVR array B; 330 Ω | as above | as above; 0 in sleep | 14.62; 2.01 |
| J2 | SCL (10) | clamp, then 330 Ω | array B; 330 Ω | as above | as above; 0 in sleep | share; 2.01 |
| J2 | 3V3_AUX (8; 2 by the net) | clamp | array B | SOT-23-6 | 0 in sleep | share |
| J2 | GND (1, 7) | clamp return, shield drains | – | – | – | – |
| J2 | **total** | | 2 arrays, 6 resistors | | | **41.30** |
| J3 | VBAT+ (4) | TVS to GND, GND side of Q1 | TVS0500DRVR (fallback ESDA7P60-1U1M, other pads) | WSON-6 2 x 2 | 0.07 typ / 5.5 max nA at 5 V, 27 °C; 220 nA max at 85 °C | 7.12 |
| J3 | VBAT- (3) | none (Q1 drain) | – | – | – | – |
| J3 | AX (5) | clamp only | TPD4E1U06DBVR array C (USBLC6-4SC6 as fallback only) | SOT-23-6 | 10 nA max = 3.2 LSB at 5 kΩ; 0 in sleep | 14.62 |
| J3 | VREF (6) | clamp only | array C | SOT-23-6 | 0 in sleep | share |
| J3 | VSWITCH (2) | clamp only | TPD4E1U06DBVR array D (USBLC6-4SC6) | SOT-23-6 | 0 in sleep | 14.62 |
| J3 | GND (1) | clamp return | – | – | – | – |
| J3 | **total** | | 2 arrays, 1 TVS | | | **36.36** |
| J4 | D+, D- | clamp at receptacle, then existing 27 Ω | TPD4E1U06DBVR array E (USBLC6-4SC6) | SOT-23-6 | no sleep cost; 0.8 pF typ | 14.62 |
| J4 | VBUS | clamp (channel and pin 5) | array E | SOT-23-6 | no sleep cost | share |
| J4 | CC1, CC2, SBU | none | – | – | – | – |
| J4 | shell, GND | to the pour, all four tabs | – | – | – | – |
| J4 | **total** | | 1 array | | | **14.62** |
| Earth | H1 | plated, GND ring, EARTH silkscreen | – | – | – | 0 |

Board area at today's density (courtyard / 0.645): J2 64.0, J3 56.4, J4 22.7 mm²; 143.1 mm² in all. Sleep cost of the whole set: 4 nA typ / 40 nA max (TPD4E1U06 on TX, RX, ADC, GPIO if held high) plus 5.5 nA max (TVS0500 at 27 °C), about 2.7 % of 1.7 µA at the guaranteed maxima (computed).

## Sources checked (dead ends included)

- Project-Margay issues #72 and #55 (`gh issue view --json body,comments`): read.
- NW-Status sources: 2026-11-09 surge report, 2026-11-10 commercial, open-logger and Okapi board-space reports, margay-v3.1-room-study.md, margay-v4-board-size.md; 2026-11-12 larger-board-area and growth-direction reports (sections on #72 parts and free area): read. Not redone: TVS0500 leakage, TPD1S514, PTC and OVP analysis (2026-11-09).
- Margay.kicad_pcb and Margay.kicad_sch at ca24e31, copied to scratchpad `v4esd/`; `conn.py`, `gnd.py`, footprint and courtyard scripts run there; `kicad-cli sch export netlist` -> `net.xml`.
- TI datasheets via `ti.com/lit/ds/symlink/`: tpd4e1u06 (read), tvs0500 (pinout read), tpd1e10b06, tpd2e2u06, tpd1e10b06-q1 (downloaded, not needed further); tpd4e1u06-q1 and tvs0500-q1 returned HTML (no such documents, or not at that URL).
- Microchip MCP3421 DS22003E (ww1.microchip.com): read.
- Nexperia IP4234CZ6: assets.nexperia.com and nexperia.com HTTP 403; mirror cdn.components.ru/media/PDF/7192183.pdf read (pass-through pinout, rejected). Digi-Key IP4234CZ6 page: 1727-1217-1-ND, 15,416 in stock, $0.66 (recorded, not used).
- ST USBLC6-4SC6Y Doc ID 023199 Rev 2: mirror cdn.components.ru/media/PDF/2182484.pdf read. st.com PDF for ESDA7P60-1U1M: curl failed (no response); leakage from a web search summary (UNVERIFIED).
- Littelfuse SP05 datasheet: littelfuse.com 403 (WebFetch); mirror cdn.components.ru/media/PDF/1683628.pdf read. SP0503BAHTG pin assignment: from the Mayfly netlist in the 2026-11-10 open-loggers report (pin 1 GND), not re-read from the drawing.
- Digi-Key pages (WebFetch, 2026-11-12): TPD4E1U06DBVR; TPD4E1U06Q (no result); IP4234CZ6 search (no listing), IP4234CZ6-115 detail; SP0503BAHTG search and detail; PRTR5V0U2X search, a wrong detail ID (returned a MOSFET), PRTR5V0U2X,215 search and detail; TVS0500 search (no listing), TVS0500DRVR; ESDA7P60-1U1M; USBLC6-4SC6Y; USBLC6-4SC6 detail; ERJ-2RKF3300X; RC0402FR-07330RL; TPD1E10B06DYAR (price only); PESD5V0S1BB (only a GOODWORK listing, not Nexperia).
- Web searches: TPD4E1U06 drop-in alternatives (distributor cross-references only); IP4234CZ6 pinout; SP0503BAHTG specs; low-leakage 5 V TVS alternatives to TVS0500 (none from Nexperia, ST or Semtech found with nA leakage); USBLC6-4SC6 pinout.
- Not checked: MAX6070 datasheet (load regulation); ATmega1284P datasheet (absolute maxima, ADC source limit, I2C thresholds, all marked from memory); FT231X USB capacitance guidance and the USB 2.0 full-speed capacitance limit; MIC9409 turn-on slew; DMG3404L drain rating; J2's wire range; Semtech SRDA3.3-4.

# COMPLETE

# Margay v3.1.0: surge and ESD protection on the power and USB inputs (agent report, 2026-11-09)

Research only. Nothing is decided. Numbers carry a source or are marked UNVERIFIED; thresholds chosen by the agent are marked PROPOSAL.

## Source log

- Project inputs read: margay-power-path-decision.md (sections 4-8), margay-power-path-lm66100.md, sources/2026-11-09-margay-voltage-rating-agent-report.md.
- LM66100 SLVSEZ8A and TPS22917 SLVSDW8B: text copies already in the session scratchpad (ds/), re-read for absolute maxima and ESD ratings.
- TI datasheets downloaded 2026-11-09 from ti.com/lit/ds/symlink/<part>.pdf (plain curl, no header changes), converted with pdftotext: TVS0500 SLVSED2C, TVS0701 SLVSEQ1A, TPD1E10B06 SLLSEB1G, TPD2E2U06 SLLSEG9C, TPD4E05U06/TPD1E05U06 SLVSBO7O, TPD6S300A SLVSEL8, TPD8S300A SLVSEL9, TPD1S514 SLVSCF6F, TPD1S414 SLLSEH9B, TPD4S311 SLVSF72C, TPD2EUSB30 SLVSAC2G, TPD4E02B04 SLVSD85B, ESD321 SLVSEN8C, TPD2S300 SLVSDL1, TPS2595 SLVSE57C, TPS25947 SLVSFC9C, TPS2660 SLVSDG2G.

## Findings (appended as confirmed)

### F1. Ratings of the parts a protection device must protect (from datasheets)

- LM66100 (SLVSEZ8A §6.1): VIN -6 to 6 V; VOUT, CE, ST -0.3 to 6 V. ESD (§6.2): HBM ±2000 V, CDM ±500 V (JEDEC component ratings, not IEC system ratings).
- TPS22917 (SLVSDW8B §7.1): VIN, VOUT, ON, QOD -0.3 to 6 V. ESD (§7.2): HBM ±2000 V, CDM ±500 V.
- FT231X (FT_000565 v1.4, Table 5.1/5.2): VCC -0.3 to 5.5 V; ESD HBM > ±2 kV, CDM 500 V.
- Note: a JEDEC HBM ±2 kV rating is a factory-handling rating. IEC 61000-4-2 level 4 (±8 kV contact) is a system-level test with roughly 30 A peak current (the TI datasheets below state IEC ratings separately from JEDEC ratings for this reason). None of the Margay ICs on VBUS, D+/D-, CC or BAT+ carries an IEC 61000-4-2 rating of its own.

### F2. TVS0500 (TI flat-clamp, 5 V), SLVSED2C

- VRWM 5 V (§7.4, recommended maximum). VBR 7.5 min / 7.9 typ / 8.4 max V at 1 mA (§7.6).
- VCLAMP 8.6 typ / 8.8 max V at 24 A 8/20 µs; 9.2 typ / 9.5 max V at 43 A 8/20 µs (§7.6). RDYN 30 typ / 50 max mΩ.
- ILEAK at VIN = VRWM (5 V): 0.07 nA typ / 5.5 nA max at 27 °C; 6.5 nA typ / 220 nA max at 85 °C; 38 typ / 755 nA max at 105 °C (§7.6). Leakage at 5.5 V is NOT specified (5.5 V is above its 5 V VRWM).
- CIN 155 pF at 5 V. IEC 61000-4-2 ±24 kV contact, ±30 kV air (§7.3). 43 A / 400 W 8/20 µs; 2 kV through 42 Ω IEC 61000-4-5 (§1, §8).
- Caution, §7.6 and §8.x: maximum input slew rate 2.5 V/µs at 27 °C, 0.7 V/µs at 105 °C; faster edges make it clamp and conduct "for a few microseconds", harmless but heating if repeated. A USB hot-plug or battery-terminal connection can exceed 2.5 V/µs (UNVERIFIED for Margay; not measured).
- Package DRV 2 x 2 mm SON-6.
- Consequence: even the flattest 5 V TVS clamps at 8.6-9.5 V at its rated surge current, 2.6-3.5 V above the 6 V absolute maximum of the LM66100, TPS22917, TPS797, TPS22916 and TPS7A05. No TVS with a working voltage of 5 V or more can clamp below 6 V at a rated surge current of amperes: breakdown must sit above the working voltage, and clamp sits above breakdown.

### F3. TPD1E10B06 (TI, single bidirectional ESD), SLLSEB1G

- VRWM 5.5 V (pin to pin). ILEAK 100 nA max at 5 V (no typical given; no figure at 5.5 V). VBR 6 V min at 1 mA.
- VCLAMP 10 V at 1 A, 14 V at 5 A (8/20 µs, strike on pin 1); 8.5 V at 1 A, 14 V at 5 A (strike on pin 2).
- CIO 12 pF typ at 2.5 V. IEC 61000-4-2 ±30 kV contact and air. IEC 61000-4-5 6 A, 90 W (8/20 µs).
- Packages: DPY (0402 X1SON) and DYA (SOD-523) (§1 and orderable addendum). §1 names "VBUS pin and ID pin of USB ports" among its applications. An ESD part, not a surge part: 6 A 8/20 µs.

### F4. TVS0701 (TI flat-clamp, bidirectional 7 V), SLVSEQ1A

- VRWM ±7 V. ILEAK 0.25 nA typ / 40 nA max at ±VRWM, 27 °C; 200 nA max at 85 °C. VBR 9.3 min / 10 typ V. RDYN 120 mΩ. ±30 A 8/20 µs, 360 W.
- Noted because a bidirectional part survives a reversed pack across the terminals; but its 9.3 V minimum breakdown clamps even higher above the 6 V maxima than the TVS0500.

### F5. ESD321 (TI), SLVSEN8C: VRWM 3.6 V only, leakage 10 nA max at 3.6 V, 0.9 pF. Too low a working voltage for VBUS, battery or D+/D- at 3.3 V signaling with margin; dead end for these lines.

### F6. TPD2E2U06 (TI, 2-channel low-capacitance ESD), SLLSEG9C

- VRWM 5.5 V (IIO < 10 µA). VBR 6.5 min / 8.5 max V at 1 mA. ILEAK 1 nA typ / 10 nA max at VIO = 2.5 V.
- VCLAMP IO to GND 9.7 V at 1 A TLP, 12.4 V at 5 A TLP; GND to IO 1.9 V at 1 A, 4 V at 5 A.
- CL 1.5 typ / 1.9 max pF at 2.5 V bias; §8 "supporting USB 2.0 data rates". IEC 61000-4-2 ±25 kV contact, ±30 kV air. IPP 5.5 A 8/20 µs.
- Packages: DRL (SOT-5X3) and DCK (SC70-5). The two channels fit D+ and D-, or CC1 and CC2.

### F7. TPD4E05U06 / TPD1E05U06 (TI), SLVSBO7O

- VRWM 5.5 V. VBR 6.5-8.5 V. ILEAK 0.01 nA typ / 10 nA max at 2.5 V. VClamp 10 V at 1 A TLP, 14 V at 5 A TLP.
- CIO 0.5 pF typ (TPD4E05U06), 0.42 pF (TPD1E05U06). IEC 61000-4-2 ±12 kV contact, ±15 kV air. IEC 61000-4-5 2.5 A 8/20 µs.
- Four channels: D+, D-, CC1, CC2 in one package (USON-10 DQA). Lower ESD rating (±12 kV contact) than TPD2E2U06 (±25 kV); capacitance far below what USB full speed needs.

### F8. USB-C port protectors with CC OVP: TPD6S300A (SLVSEL8), TPD4S311 (SLVSF72C), TPD2S300 (SLVSDL1)

- These put high-voltage FETs in series with CC (and SBU) to survive a short to a 20 V VBUS (CC OVP threshold 5.75-6.2 V, TPD6S300A and TPD4S311).
- TPD6S300A needs VPWR 2.7-4.5 V and draws IVPWR 90 typ / 135 max µA (§7.5). TPD2S300 quotes 3.23 µA typical quiescent at VPWR, VM = 3.3 V (§1).
- Not warranted on Margay (agent's judgment, PROPOSAL): Margay is an Rd-only 5 V sink that never negotiates USB PD, so a compliant source never raises VBUS above 5 V; a CC pin shorted to VBUS sees 5 V, and CC1/CC2 run only to 5.1 kΩ resistors, which tolerate even 20 V briefly (20 V across 5.1 kΩ is 78 mW, UNVERIFIED against the resistor's rating). There is no CC controller IC to protect. Powering any of these from the always-on 3V3 would cost 3-135 µA in sleep; powering them from USB defeats their dead-battery purpose. A low-capacitance ESD diode on CC is enough.

### F9. TPD1S514-1 (TI USB VBUS OVP + surge + ESD), SLVSCF6F

- One chip: an nFET switch in VBUS with OVP, surge clamp and IEC ESD on the connector side. VBUS_CON tolerates 30 V DC (§7.1); VBUS_SYS 20 V.
- OVP threshold, TPD1S514-1: 5.90 min / 5.95 typ / 5.99 max V, 100 mV hysteresis (§5, §7.9). Recommended VBUS_CON 3.5-5.9 V.
- Surge on VBUS_CON: IEC 61000-4-5 100 V open circuit (1.2/50 µs), 30 A, 900 W (8/20 µs) (§7.1); §1: "Precision Clamp Circuit Limits the VBUS_SYS Voltage < VOVP". IEC 61000-4-2 ±15 kV contact and air on VBUS_CON (§7.2).
- RON 39 typ / 50 max mΩ at 5 V, 1 A (§7.8). Startup delay 20 ms, soft start 3.5 ms (§5). EN active low (enables when EN low, per §1 description "After the EN pin toggles low").
- Current from VBUS while enabled, no load: IVBUS 228 typ / 354 max µA at 5 V (§7.5). Drawn only while USB is plugged in: on Margay, VUSB is isolated from VSYS by the TPS22917 (always-on reverse current blocking, SLVSDW8B) and U_A, so the battery sleep current does not change (inference from the circuit, not measured). IVBUS_SYS 210 µA typ with VBUS_CON Hi-Z means a part held up from the system side would drain it; not the case here.
- Package: 12-ball WCSP, 1.29 x 1.99 mm (YZ). This is its main cost for Margay's assembly.
- The 5.99 V maximum threshold sits just under the 6 V absolute maxima of the TPS22917, LM66100 and the parts behind them, but above the FT231X's 5.5 V VCC maximum (D1's 0.26-0.45 V drop is the FT231X's only margin; see the voltage-rating report).

### F10. eFuses and integrated OVP: quiescent current (datasheets)

- TPS2595 (SLVSE57C §7.5): IQ 175 typ / 250 max µA while on; ISD 0.45 typ / 2 max µA in shutdown (5 V < VIN ≤ 18 V), but shutdown means off. 2.7-18 V, 20 V absolute maximum. Package DSG, 8-pin WSON (§6).
- TPS25947 (SLVSFC9C §7.5): IQ(ON) 426-428 typ / 610 max µA. 2.7-23 V, 28 V absolute maximum, QFN 2 x 2 mm.
- TPS2660 (SLVSDG2G §1): "300-µA in operating, 20-µA" in shutdown; 60 V, reverse input polarity protection.
- TPD1S514-1: 228 typ / 354 max µA (F9).
- Web search for nA-quiescent battery OVP (2026-11-09, query "overvoltage protection IC nanoamp quiescent current battery input load switch OVP"): AAT4684 30 µA typ, onsemi NUS6160MN 24-35 µA, OmniVision WS3235 330-400 µA (search summaries, UNVERIFIED, datasheets not opened). No integrated OVP with nA quiescent current was found.
- ADI LTC4365: not opened (UNVERIFIED); from the family's class, expect tens to hundreds of µA while on.
- Consequence for the battery line: every integrated OVP or eFuse found draws 24-610 µA while conducting, which is 14 to 360 times the 1.7 µA sleep current. None is compatible with the battery input. On VBUS they cost nothing in sleep, because VUSB is dead when USB is unplugged.

### F11. Conventional TVS leakage near 5 V (Diodes Inc SMAJ, DS19005 Rev. 19-2, electrical table)

| Part | VRWM | VBR min-max | IR max at VRWM | VC at IPP | IPP |
|---|---|---|---|---|---|
| SMAJ5.0A | 5.0 V | 6.40-7.25 V | 800 µA | 9.2 V | 43.5 A |
| SMAJ6.0A | 6.0 V | 6.67-7.37 V | 800 µA | 10.3 V | 38.8 A |
| SMAJ6.5A | 6.5 V | 7.22-7.98 V | 500 µA | 11.2 V | 35.7 A |
| SMAJ7.0A | 7.0 V | 7.78-8.60 V | 200 µA | 12.0 V | 33.3 A |
| SMAJ7.5A | 7.5 V | 8.33-9.21 V | 100 µA | 12.9 V | 31.0 A |
| SMAJ8.5A | 8.5 V | 9.44-10.4 V | 10 µA | 14.4 V | 27.7 A |
| SMAJ9.0A | 9.0 V | 10.0-11.1 V | 5.0 µA | 15.4 V | 26.0 A |

- Note 10: "For Bidirectional devices having VRWM of 10V and under, the IR is doubled." IPP is 10/1000 µs for this family (UNVERIFIED which waveform; the table heading says only "Max. Peak Pulse Current").
- A guaranteed 800 µA is 470 times the logger's 1.7 µA sleep current. Typical leakage is not given. A standard silicon-avalanche SMA/SMB/SOD-123FL TVS of 5-7 V standoff is ruled out on the battery line on its guaranteed numbers, whatever its typical leakage may be.

### F12. Diodes Inc D5V0L1B2LP4 (bidirectional ESD, X2-DFN1006-2), DS35586 Rev. 7-2

- VRWM 5 V. IRM 10 nA typ / 100 nA max at 5 V. VBR 6 min / 7 typ / 8 max V at 1 mA.
- VCL 7.0 typ / 9.0 max V at 1 A; 9.0 / 11.0 at 3.5 A; 10.5 / 12.0 at 5 A; 11.5 / 14.0 at 6 A (8/20 µs). CT 15 typ / 20 max pF at 0 V.
- IEC 61000-4-2 ±30 kV contact and air; IPP 6 A 8/20 µs. An ESD part; 5 V VRWM is below a 5.5 V maximum battery.

### F13. TVS0701 clamp (SLVSEQ1A §7.6)

- VCLAMP 11 typ / 11.7 max V at ±IPP (30 A) 8/20 µs, VIN = 0 V before, 27 °C; 12.9 V max at 125 °C. CIN 77 pF. SON-8 3 x 3 mm. Leakage 40 nA max at ±7 V (27 °C), 200 nA max (85 °C).

### F14. Digi-Key (US site, fetched 2026-11-09)

- TVS0500DRVR: 296-48382-1-ND, 1,950 in stock, $1.10 at 1 (cut tape).

- TPD2E2U06DRLR: 296-38361-1-ND, 68,436 in stock, $1.10 at 1.
- TPD1S514-1YZR: 296-38344-1-ND, 5,153 in stock, $1.45 at 1.
- TPD4E05U06DQAR: 296-35765-1-ND, 0 in stock (3,000 expected 28 Dec 2026), $0.86 at 1.
- TPD1E10B06DPYR: 296-30406-1-ND, 85,314 in stock, $0.41 at 1.

### F15. Placement (TI datasheet layout sections)

- TPD2E2U06 SLLSEG9C §10.1, TPD1E10B06 SLLSEB1G §7.4.1, TPD4E05U06 SLVSBO7O §7.4.1: "The optimum placement is as close to the connector as possible." TVS0500 SLVSED2C §11.1: "The optimum placement is close to the connector."
- TPD2E2U06 §8.2: TI's own design example is "one TPD2E2U06 device ... in a USB 2.0 application", signal range 0-3.3 V.
- Consequence for Margay's D+/D-: the ESD array goes at J4, on the connector side of the 27 Ω series resistors. The resistors then sit between the clamp and the FT231X and limit the residual current into the FT231X's own pins during the clamp. (The benefit of series resistance after the clamp is standard practice; no TI document quoted for it in this session, UNVERIFIED as a quotation.)

### F16. PTC resettable fuses (Bourns)

- MF-PSMF series (REV. Q 09/26): Vmax 6 V for every size listed (MF-PSMF050X: Ihold 0.50 A, Itrip 1.00 A, R 0.15-0.9 Ω; MF-PSMF075X: 0.75 A, 1.50 A, 0.09-0.35 Ω). A 6 V PTC is not rated to interrupt a 12 V fault, so it is the wrong family for the miswiring case.
- MF-FSMF050X (0603): Vmax 6 V, Ihold 0.50 A, R 0.10-0.80 Ω. Same limitation.
- MF-MSMF series (1812, REV. BE 09/26): MF-MSMF075/24X Vmax 24 V, Imax 100 A, Ihold 0.75 A, Itrip 1.50 A, Rmin 0.11 Ω, R1max 0.40 Ω, max time to trip 0.2 s at 8.0 A; MF-MSMF050/24X Vmax 24 V, Ihold 0.50 A, Itrip 1.00 A, 0.15-1.3 Ω, 0.20 s at 8.0 A. Ihold derating (MF-MSMF075/24X): 1.06 A at -40 °C, 0.75 A at 23 °C, 0.37 A at 85 °C. Operating -40 to +85 °C.
- Cost on the battery line: no leakage (series element). Voltage drop at the board's 210 mA design load (3V3_AUX full plus core, from margay-power-path-decision.md §6): 0.11-0.40 Ω x 0.21 A = 23-84 mV for MF-MSMF075/24X (R1max is the post-trip one-hour resistance, so 84 mV is the conservative figure). At the 710 mA case (Vs at 500 mA): 78-284 mV. That drop comes straight off the 3.63 V low-end floor in the voltage-rating report, so a PTC shortens the usable discharge of an alkaline pack. Its hold current at 85 °C (0.37 A) also sits below the 710 mA case: with the Vs output loaded, a hot logger could trip its own fuse. These are PROPOSAL-grade observations; neither is measured.

### F17. Dead ends and unverified items in the OVP search

- ADI LTC4365: analog.com product page and PDF timed out (WebFetch and curl, 2026-11-09). Figures from a search summary of aggregator copies (radiolocman.com), not the ADI PDF: 2.5-34 V operation, 60 V overvoltage, -40 V reverse, about 125 µA quiescent, 10 µA shutdown, 36 ms turn-on delay (1 ms for -1). UNVERIFIED against ADI's own document. At 125 µA it is about 74 times the 1.7 µA sleep current.
- TI TPS3840 (SNVSB03E): 300 nA typ / 700 nA max supply current, VDD 1.5-10 V, thresholds 1.6-4.9 V only, SOT23-5. Considered as the sense element of a discrete nA battery OVP; rejected as a ready answer because its thresholds stop at 4.9 V and its 10 V supply limit is below a 12 V fault. A discrete nA OVP is possible in principle but is a design project in its own right, not a part to drop in.
- ST USBLC6-2: st.com PDF timed out (WebFetch). The Digi-Key-hosted "USBLC6-2SC6.pdf" (mm.digikey.com) turned out to be a UMW (umw-ic.com) second-source datasheet, not ST's, and is not used. Search summary of ST copies (UNVERIFIED): ST DocID11265, 150 nA max leakage, 3.5 pF max line capacitance, VBUS on pin 5.
- Nexperia (assets.nexperia.com and nexperia.com product pages): HTTP 403 to plain curl and to WebFetch. No Nexperia numbers in this report.
- Littelfuse datasheet URLs (littelfuse.com): HTTP 403 to plain curl. No Littelfuse numbers in this report; Diodes Inc's SMAJ table stands in for the conventional-TVS class.
- onsemi SMF5.0AT1 PDF URL returned an HTML page, not the PDF. Vishay SMF and Diodes SMAJ alternative URLs: 404.

- TVS0701DRBR: 296-53062-1-ND, 5,392 in stock, $1.40 at 1.
- TPD2E2U06DCKR (SC70 alternative): 296-TPD2E2U06DCKRCT-ND, 0 in stock (3,000 expected 1 Dec 2026), $0.66 at 1.
- MF-MSMF075/24X-2 (Bourns): 118-MF-MSMF075/24X-2CT-ND, 1,863 in stock, $0.78 at 1.
- Not fetched: D5V0L1B2LP4-7B stock and price.

### F18. TPD1S514 behavior in detail (SLVSCF6F §8)

- §8.1: "offers an ESD and Precision Clamp for the VBUS_CON pin, thus eliminating the need for external TVS clamp circuits"; "If at any time VBUS_CON rises above VOVP, the nFET switch is turned OFF within 100 ns."
- §8.3.8: "A Precision Clamp diverts the current to ground and active circuitry switches OFF the nFET earlier than 100 ns before an over voltage can get through to VBYS_SYS [sic] ... holds the voltage on VBUS_SYS to less than VOVP during surge events of up to 100 VPP."
- §8.3.6 Case 1: "The EN pin can be tied to ground so that the nFET is always ON (when VUVLO < VBUS_CON < VOVP)". This is Margay's case: no PMIC, EN to GND.
- VBUS_POWER is an always-on LDO output from VBUS_CON (4.9 V at 3 mA for -1); it can be left with its capacitor only (§8.1; recommended CPOWER 1 µF, §7.3).
- At attach the nFET stays off for the 20 ms delay, then soft-starts over 3.5 ms (§5). The TPS22917 behind it still sets the 40 ms ramp into VSYS. C6 (4.7 µF) moves to VBUS_SYS, where TPD1S514's 3.5 ms soft start charges it at about 4.7 µF x 5 V / 3.5 ms = 6.7 mA (computed). Only the VBUS_CON capacitor (TI recommends 1 µF, §7.3) is exposed at the instant of attach.

### F19. TI application notes

- SLVAE37 (January 2019), "How to select a Surge Diode", §2.1: "In a design, VRWM should be selected to ensure that it is above the expected maximum operating voltage. If the applied voltage rises above VRWM, there is a chance to see diode leakage increase significantly." §2.2: "Ensure that nominal voltage stays below VRWM, rather than VBR, to assure very low system leakage." §2.4 (VCLAMP and RDYN): "if VCLAMP violates the absolute maximum voltage of your input circuitry system, failures can occur even if the TVS diode is shunting current." §2.6: "Particularly for lower voltage TVS diodes, leakages can rise to close to 1 mA ... on battery powered systems an always-on 1 mA leakage can be a large power drain". §3 example: "the SMAJ33A, SMBJ33A have 25°C leakage at 1 µA, while the TVS3300 has a much lower leakage with <30 nA at 25°C."
- SLVA680A (February 2015), "ESD Protection Layout Guide", summary list: "Place the TVS as near to the connector as design rules allow"; "Place the Protected IC much further from the TVS than the TVS is to the connector"; "Do not use stubs between the TVS and the Protected Line"; "Minimizing inductance between the TVS and ground is critical".
- SSZB130E (August 2025), "System-Level ESD Protection Guide", and SLVA711 (June 2015), "IEC 61000-4-x Tests for TI's Protection Devices": downloaded and searched; no Margay-specific rule beyond the above was extracted.
- Not found in this session: a TI, Nexperia, Littelfuse, ST or Semtech application note specific to USB-C sinks in battery-powered outdoor equipment.

### F20. Comparable loggers

- EnviroDIY Mayfly v1.1 rev B (github.com/EnviroDIY/EnviroDIY_Mayfly_Logger, hardware/Mayfly_v1p1/Mayfly_v1p1_revB.sch, parsed 2026-11-09): USB-C receptacle J6 (USB4105, the same family as Margay's J4) with D6 SP0503BAHTG (Littelfuse 3-channel TVS array) on VUSB, D+ and D-; CC1 and CC2 go only to resistors (R28, R30); no TVS or fuse on the LiPo or solar JST inputs; Schottky diodes MSS2P2 OR the sources. So the Mayfly protects USB data and VBUS against ESD and nothing else.
- Adafruit Feather M0 Adalogger (adafruit/Adafruit-Feather-M0-Adalogger-PCB) and Feather RP2040 Adalogger (adafruit/Adafruit-Feather-RP2040-Adalogger-PCB), schematics parsed 2026-11-09: no TVS or ESD part on VBUS, D+, D-, CC1, CC2 or VBAT. The RP2040 version has series resistors R9/R10 in D+/D-.
- Campbell Scientific CR1000X specification sheet (s.campbellsci.com, US copy "Revision: 05/2026" and an older French-site copy): "Power inputs are protected against surge, over-voltage, over-current, and reverse power. IEC 61000-4 Class 4 level." Input 10-18 VDC; "Sustained Input Voltage without Damage: 30 VDC". Older copy: "ESD: per IEC 61000-4-2; ±15 kV air, ±8 kV contact"; "Surge: per IEC 61000-4-5; 4 kV power, 4kV I/O"; Ethernet with "TVS surge protection"; USB is a Micro-B device port. Idle current drain "<1 mA, typical", about 600 times Margay's 1.7 µA sleep, which is why a CR1000X can afford protection parts that leak µA.
- Onset HOBO U30: Onset documents not reached; a reseller page (search summary, UNVERIFIED) cites CE EN 61326 "criterion C for ESD". Nothing found on power-port protection.

## Analysis

### A1. What a TVS can and cannot do here

- No clamp protects a 6 V part against a rated surge. A TVS with a working voltage at or above the 5.5 V battery and USB maximum has its breakdown above that, and its clamp above the breakdown: 8.6-9.5 V for the flattest part found (TVS0500, F2), 10-14 V for the ESD diodes (F3, F6, F7, F12). For ESD (nanosecond pulses, about a microcoulomb) the IC's own ±2 kV HBM structures and the board capacitance take the residue behind the clamp; for an amperes-scale 8/20 µs surge, the 6 V parts would see the clamp voltage.
- Board capacitance is itself a zero-leakage ESD absorber (agent's estimate, inductance ignored, PROPOSAL-grade): the IEC 61000-4-2 network stores 150 pF at the test voltage (from memory, UNVERIFIED), so an 8 kV discharge carries about 1.2 µC. Into C12's 0.1 µF on VBAT+ that is a 12 V step; into 1 µF, 1.2 V; into C6 (4.7 µF X7R, about 2.7 µF effective at 5 V per margay-power-path-decision.md §8), about 0.44 V. The TVS still has to handle the fast edge that the capacitor's ESL and the trace pass.
- Consequence: the target for every Margay input is IEC 61000-4-2 ESD (field laptops plugged in by hand, battery leads handled in cold, dry air). IEC 61000-4-5 surge is the target only on ports with long outdoor cables. Which product standards require surge on which ports (for example the 30 m cable-length criterion in the generic immunity standards) is from memory and UNVERIFIED here. The USB port is connected only during a visit, through a short cable to a battery-powered laptop: surge is not a credible threat there. A battery pack inside the enclosure is the same. Long battery leads run outside the enclosure (an external D-cell box, a solar-charged pack) are where surge starts to matter, and the sleep budget then decides what can be fitted (A3).

### A2. Reverse polarity and where the battery TVS sits

- Q1 (DMG3404L, low-side N-FET, source on GND, drain on VBAT-, gate on VBAT+) blocks a reversed pack: with the pack reversed, its gate is at the most negative node and its body diode (anode at the source, GND; cathode at the drain, VBAT-) blocks current from VBAT- into GND (from the netlist description in the voltage-rating report; reasoning, not a bench test).
- A unidirectional TVS (TVS0500) from VBAT+ (cathode) to board GND (anode), that is, after Q1 in the return path, is safe with a reversed pack: no current loop closes through the board while Q1 blocks. The same TVS placed straight across J3 pins 4 and 3 (before Q1) would be forward-biased by a reversed pack and short it; TVS0500's DC forward current maximum is 500 mA (SLVSED2C §7.1), far below what an alkaline D cell supplies (UNVERIFIED for D cells, not looked up).
- A bidirectional part (TPD1E10B06, VRWM ±5.5 V; TVS0701, ±7 V) can sit directly across J3, because a reversed three-cell pack (at most 4.95 V fresh alkaline, 5.49 V fresh lithium, from the fresh-AA report) stays inside its reverse working voltage. Across the terminals is the better place for ESD (SLVA680A: as near the connector as possible), and it clamps a discharge between the two leads before Q1 sees it.
- LM66100's VIN is rated -6 to +6 V (SLVSEZ8A §6.1), so U_B itself tolerates a reversed input up to 6 V. It does not replace Q1, which protects U6, U8 and C12 as well.

### A3. The leakage budget on the battery line

- PROPOSAL: allow a protection part on the battery line 5 % of the 1.7 µA sleep current, 85 nA, at its guaranteed maximum and 25-27 °C; and check the 85 °C maximum separately, because a logger in summer sun runs hot.
- TVS0500 at 5 V: 0.07 nA typ / 5.5 nA max at 27 °C (0.3 % of 1.7 µA at the maximum); 6.5 nA typ / 220 nA max at 85 °C (13 % at the maximum, 0.4 % typical). At 5.5 V it is outside its 5 V VRWM and leakage is not specified (UNVERIFIED; its 7.5 V minimum breakdown suggests it stays small, but SLVAE37 §2.1 says not to rely on that). It fits the alkaline and NiMH chemistries (at most 4.95 V fresh) and is out of specification with fresh lithium L91 (5.37-5.49 V).
- TPD1E10B06 at 5 V: 100 nA max over the full operating temperature range (SLLSEB1G §5.6; no typical given): 5.9 % of 1.7 µA at the worst case anywhere in temperature. VRWM 5.5 V matches the board's rated maximum, which satisfies SLVAE37 §2.1 for every supported chemistry including lithium.
- TVS0701 at 7 V: 40 nA max at 27 °C (2.4 %), 200 nA max at 85 °C (12 %). Leakage at 5.5 V is below the 7 V figure in the usual monotonic sense (UNVERIFIED; not specified at 5.5 V). Its clamp (11.7 V max at 30 A) is the highest of the three.
- Conventional SMAJ5.0A-SMAJ7.5A: 100-800 µA guaranteed at VRWM (DS19005), 59 to 470 times the sleep current. Ruled out.
- A larger ceramic on VBAT+ (for example C12 from 0.1 µF to 1 µF X7R) adds ESD charge absorption with no meaningful leakage (insulation resistance of class 2 MLCCs is in the GΩ range, UNVERIFIED for a specific part). PROPOSAL; it also counts nothing against USB's 10 µF because VBAT+ is on the other side of U_B.

### A4. Overvoltage beyond transients

- Battery line: a 4-cell alkaline pack is 6.24-6.60 V fresh (four times the 1.56-1.65 V per cell implied by the fresh-AA report's 4.68-4.95 V three-cell figures; computed), above the 6.0 V absolute maximum of U6, U8, U_B and the parts behind them, and below every TVS's breakdown (TVS0500 7.5 V minimum). A 12 V supply is far above both. No TVS stops either: the TVS does not conduct at 6.2-6.6 V, and at 12 V DC it must carry the source's full current (TVS0500's DC breakdown current maximum is 50 mA, SLVSED2C §7.1) and fails.
- A PTC plus TVS crowbar does not rescue it: a 6 V PTC (MF-PSMF, MF-FSMF) is not rated to interrupt 12 V, and a 24 V PTC (MF-MSMF075/24X) takes up to 0.2 s to trip at 8 A while the TVS dissipates tens of watts (8 A x 9 V = 72 W, computed), far beyond a 400 W-for-20 µs rating.
- An integrated OVP or eFuse on the battery line costs 24-610 µA (F10, F17), which is 14-360 times the sleep current. None fits. A discrete OVP with a nanopower comparator is possible in principle, but every part ahead of its switch must tolerate the fault voltage, and the nanopower supervisor found (TPS3840) tops out at 10 V supply and 4.9 V thresholds. That is a design study, not a drop-in part.
- Negative result: at a 1.7 µA sleep current, there is no off-the-shelf protection against a 4-cell pack or a 12 V supply on BAT+. The practical defenses are a connector or pack that cannot take four cells (a three-cell holder wired to a keyed plug) and a printed statement of the limit on the board and in the README (the voltage-rating report found no chemistry or cell-count warning anywhere in Project-Margay). Q1 still covers reversal.
- USB: a non-compliant source (a broken charger, a 9-20 V adapter with a USB-C plug, a PD source misbehaving) is the case an OVP covers for free in sleep, because VUSB is dead when unplugged. TPD1S514-1 trips at 5.90-5.99 V and tolerates 30 V DC, 100 V surge (F9, F18). Quick Charge and similar chargers raise VBUS only after a D+/D- handshake that the FT231X does not perform (from general knowledge, UNVERIFIED for specific chargers).
- One limit remains on USB even with TPD1S514-1: its 5.99 V maximum threshold leaves the FT231X (5.5 V absolute maximum) protected only by D1's 0.26-0.45 V drop, as today.

## Recommendations, ranked by value for a field logger

Each one is a proposal for Andy; nothing here is decided. "Essential" means the port is exposed to a credible, routine threat with no protection today.

1. **D+/D-: TPD2E2U06DRLR. Essential.** Two channels, 1.5 pF typ / 1.9 pF max, ±25 kV contact IEC 61000-4-2, VRWM 5.5 V, breakdown 6.5-8.5 V, clamp 9.7 V at 1 A and 12.4 V at 5 A TLP, leakage 1 nA typ / 10 nA max at 2.5 V, SOT-5X3 (DRL) (SLLSEG9C §6.5). At J4, on the connector side of the 27 Ω resistors, with both D+ pins and both D- pins of the receptacle tied at the clamp and no stubs (SLVA680A). The 27 Ω then sits between the clamp and the FT231X, whose pins carry only ±2 kV HBM. TI's own USB 2.0 design example (SLLSEG9C §8.2). Digi-Key 296-38361-1-ND, 68,436 in stock, $1.10. Sleep cost: none (the lines are unpowered without USB). Alternative with no stock until 28 Dec 2026: TPD4E05U06DQAR (four channels: D+, D-, CC1, CC2; 0.5 pF; ±12 kV contact; $0.86).
2. **VBUS: an ESD clamp at J4. Essential.** Two choices:
   - (a) TPD1E10B06DPYR: bidirectional, VRWM 5.5 V, leakage 100 nA max at 5 V, VBR 6 V min, clamp 10 V at 1 A and 14 V at 5 A (8/20 µs), 12 pF, ±30 kV contact, 6 A surge, 0402 X1SON (SLLSEB1G §5.6; §1 lists "VBUS pin ... of USB ports"). 296-30406-1-ND, 85,314 in stock, $0.41.
   - (b) TVS0500DRVR: VRWM 5 V, clamp 8.8 V max at 24 A and 9.5 V max at 43 A, ±24 kV contact, 43 A surge, 155 pF, SON-6 2 x 2 mm (SLVSED2C §7). 296-48382-1-ND, 1,950 in stock, $1.10. Its 5 V VRWM is below a 5.25-5.5 V VBUS, and its 2.5 V/µs slew limit can be exceeded by a hot plug (conducts for microseconds, harmless per §8). Leakage on VBUS does not matter, because VBUS draws nothing from the battery.
   - Proposal: (a) for ESD alone. Sleep cost: none.
3. **VBUS: TPD1S514-1YZR in series ahead of the TPS22917. Strongly recommended, optional.** The only part found that protects the 6 V parts against a DC overvoltage: OVP 5.90-5.99 V, 30 V DC tolerant, 100 V / 30 A IEC 61000-4-5 surge with VBUS_SYS held below VOVP, ±15 kV IEC 61000-4-2, 39 mΩ typ / 50 mΩ max, EN tied to GND (SLVSCF6F §5, §7, §8). It replaces the ESD clamp in item 2. Its cost: (1) a 12-ball WCSP (1.29 x 1.99 mm), which needs fine-pitch assembly; (2) 228 µA typ / 354 µA max drawn from VBUS while plugged in, nothing from the battery; (3) $1.45 (296-38344-1-ND, 5,153 in stock); (4) it moves C6 behind it and needs about 1 µF on VBUS_CON and VBUS_POWER (§7.3), which changes the capacitance arithmetic in margay-power-path-decision.md §8 (C6 is then behind a 20 ms delay; only the VBUS_CON capacitor counts at the instant of attach).
4. **Battery: one low-leakage clamp at J3. Recommended.** Choose by the chemistry Margay will support:
   - (a) alkaline and NiMH only (at most 4.95 V fresh): TVS0500DRVR, unidirectional, from VBAT+ to GND after Q1 (never across J3 directly). Leakage 0.07 nA typ / 5.5 nA max at 5 V, 27 °C; 6.5 nA typ / 220 nA max at 85 °C. Clamp 8.8 V max at 24 A. 43 A surge rating covers long external leads as well as ESD.
   - (b) lithium L91 allowed (to 5.49 V): TPD1E10B06DPYR, bidirectional, directly across J3 pins 4 and 3 (reversal-safe). Leakage 100 nA max at 5 V over the full temperature range; 6 A surge, so an ESD part rather than a surge part.
   - Sleep cost: (a) under 0.3 % of 1.7 µA at 27 °C by the guaranteed maximum, up to 13 % at 85 °C; (b) up to 5.9 % anywhere in temperature by the maximum.
   - Zero-leakage companion (PROPOSAL): C12 from 0.1 µF to 1 µF.
5. **CC1/CC2: optional, low value.** On Margay, CC1 and CC2 go only to the 5.1 kΩ Rd resistors; no semiconductor sits on CC, so an ESD strike there has no IC to damage (reasoning from the circuit; the resistors' own pulse rating not looked up, UNVERIFIED). The USB-C port protectors (TPD6S300A, TPD4S311, TPD2S300) solve a short-to-20 V-VBUS problem that an Rd-only 5 V sink without PD does not have, and drawing their supply from the always-on 3V3 would cost 3-135 µA in sleep (F8). If CC protection is wanted, TPD4E05U06 in place of item 1 covers it in the same package as D+/D-.
6. **Battery PTC: not recommended for the standard 3-cell pack.** A 6 V PTC cannot interrupt 12 V; a 24 V PTC (MF-MSMF075/24X-2, 118-MF-MSMF075/24X-2CT-ND, 1,863 in stock, $0.78; 0.11-0.40 Ω; Ihold 0.75 A at 23 °C, 0.37 A at 85 °C) costs 23-84 mV at 210 mA and 78-284 mV at 710 mA off the 3.63 V low-end floor, and could trip on a hot day with Vs loaded. It protects only against a fault on the board itself, not against a short in the leads. Zero leakage. Worth reconsidering only if a high-current pack (D cells, lithium) is to be standard.
7. **Battery OVP: no part recommended (negative result, A4).** Document the three-cell limit on the silkscreen and in the README; prefer a pack or connector that cannot take a fourth cell.

Sensor terminals (J2), briefly: low-capacitance ESD diodes at the terminal block on each signal line (TPD4E05U06 or TPD1E10B06 class, 10 nA max at 2.5 V for the former), with the existing or added series resistance between the clamp and the MCU pin. A clamp on the switched Vs output (after U11) leaks only while Vs is on. The 6 A ratings of these parts are ESD-grade; sensor cables tens of meters long outdoors are the one place on Margay where an IEC 61000-4-5 rated part (TVS0500 on a 3.3-5 V line) earns its 155 pF. Not researched further here.

## Sleep-current cost of the recommended set

- Items 1, 2, 3 and 5 (USB side): zero from the battery. VUSB is isolated from VSYS by the TPS22917's always-on reverse current blocking (SLVSDW8B) and by U_A, and D+/D-/CC are unpowered without USB (circuit reasoning, not a bench measurement).
- Item 4: TVS0500 0.07 nA typ / 5.5 nA max at 27 °C and 5 V (6.5 nA typ / 220 nA max at 85 °C); or TPD1E10B06 100 nA max at 5 V over temperature.
- Item 6 (not recommended): zero leakage, 23-284 mV of drop.
- Against the 1.7 µA sleep current: under 0.3 % (TVS0500, guaranteed, 27 °C) or under 6 % (TPD1E10B06, guaranteed, all temperatures).

## Open items for a bench check

- TVS0500 leakage at 5.5 V and at 5.49 V (fresh lithium), 25 °C and warm: not specified by TI.
- TPD1E10B06 typical leakage at 4.5-5 V: only a 100 nA maximum is published.
- The ESD charge estimate in A1 (12 V step on 0.1 µF) is arithmetic, not a measurement.

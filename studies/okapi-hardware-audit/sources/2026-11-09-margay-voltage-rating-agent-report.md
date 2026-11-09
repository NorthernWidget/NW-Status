COMPLETE

# Margay v3.1 input-voltage rating, built from the parts (agent report, 2026-11-09)

## Sources checked (log)

- Netlist: scratchpad bomlines/margay2.xml (KiCad v3.1 XML). Parsed with a short script; nets touching VBAT+/VUSB and their descendants listed below.
- Background read: NW-Status/studies/okapi-hardware-audit/margay-vmain-switchover.md (topology agrees with the netlist as parsed here).
- TPS797: scratchpad cc/dl/tps797.txt, SLVS332J (March 2001, revised December 2016).

## Nets reached from VBAT+ and VUSB (from the netlist)

- VBAT+: J3 pin 4, C12, Q1 gate (pin 1), U6 TPS79733 IN (pin 4), U8 TPS22916C VIN (A2).
- VBAT- : J3 pin 3, Q1 drain (pin 3); Q1 source on GND. (Q1 is the low-side reverse-polarity N-FET; its gate sits on VBAT+, so Vgs = VBAT.)
- VBAT_SW (U8 VOUT): C10, U9 TPS2104 IN1 (pin 5), R17 (R17/R18 10k/10k to U10 TLV3691 IN-), R22 (R22/R23 10k/10k to BAT_SENSE, ATmega1284P PA2/ADC2 pin 35).
- VUSB: J4 VBUS (USB-C), C5, C6, C11, D1 BAT43WS anode (cathode to U2 FT231X VCC pin 12), Q3 2N7002W gate, R21 (10k to GND), U9 IN2 (pin 3).
- VMAIN (U9 OUT): C13, U7 TPS7A0533 VIN, JP2 pin 1.
- JP2 (3-pad, 1-2 normally closed per its symbol name "JUMPER-SMT_3_1-NC"): pad 2 to U11 MIC94090 VIN; pad 3 on 3V3_AUX. U11 VOUT is VSWITCH, J3 pin 2. So with the default jumper, VSWITCH carries VMAIN (battery or USB voltage) to the screw terminal, and U11 sees VMAIN.
- U10 TLV3691: VCC on core 3V3; IN- = VBAT_SW/2; IN+ = 3V3_FTDI. U10 OUT to U9 EN.
- Core 3V3 (U6 OUT): ATmega, U10, U3 TPL5010, LEDs, D4 to RTC VBAT, Q2 source. Not exposed to battery voltage except through U6.

## Component rows

Format: part (ref, MPN) | pin, net | abs max | recommended max | min | source, quote.

- U6 TPS79733DCKR | IN, VBAT+ | abs max 6 V ("Input voltage (2) -0.3 6 V", 6.1, p4) | rec max 5.5 V ("VI Input voltage 1.8 5.5 V", 6.3, p5) | min: 1.8 V, or VO + V(DO); V(DO) at IO = 10 mA, VI = VO(NOM) - 0.1 V: TPS79733 105 mV typ, 200 mV max (6.5, p5); note (1) "Minimum VI = VO + V(DO)". Rated IO 0-50 mA (6.3). Source SLVS332J.

- U8 TPS22916CYFPT | VIN (A2), VBAT+; VOUT (A1), VBAT_SW | abs max VIN 6 V, VOUT 6 V, VON 6 V ("VIN Input voltage -0.3 6 V", 6.1, p4) | rec max VIN 5.5 V ("VIN Input voltage 1 5.5 V", 6.3, p4) | min VIN 1 V (6.3). Source tps22916.txt, SLVSDO5F (July 2017, revised December 2021).
- U9 TPS2104DBVT | IN1 (pin 5), VBAT_SW; IN2 (pin 3), VUSB; OUT, VMAIN | abs max IN1 6 V, IN2 6 V, EN 6 V ("Input voltage range, VI(IN1) ... -0.3 V to 6 V", absolute maximum ratings, p5) | rec max 5.5 V ("Input voltage, VI(INx) 2.7 5.5 V", recommended operating conditions, p5) | min 2.7 V (same row); the charge pump "operates from input voltages as low as 2.7 V" (p3); UVLO "Whenever the input voltage falls below approximately 2 V, the power switch quickly turns off" (undervoltage lockout, p13 per the switchover study). Source tps2104.txt, SLVS235A (September 1999, revised April 2000).
- U7 TPS7A0533PDBVR | VIN (pin 1), VMAIN | abs max 6.0 V ("IN -0.3 6.0", 6.1, p6); EN abs max VIN + 0.3 V (6.1) | rec max 5.5 V ("VIN Input supply voltage 1.4 5.5 V", 6.3, p6) | min: VOUT + VDO; VDO max at IOUT = 200 mA, VOUT = 3.3 V: 212 mV (TJ -40 to +85 C), 235 mV (TJ -40 to +125 C) (6.5, p8; "Dropout is measured by ramping VIN down until VOUT = VOUT(nom) - 5%"). UVLO falling 1.17-1.33 V. Source tps7a05.txt, SBVS254D (February 2018, revised August 2019).
- U11 MIC94090YC6-TR | VIN (pin 4), VMAIN through JP2 1-2 (default) or 3V3_AUX through JP2 2-3 | abs max 6 V ("Input Voltage (VIN) ... +6V", Absolute Maximum Ratings, DS20006706B p2) | operating 1.7 to 5.5 V ("Operating Ratings: Input Voltage (VIN) +1.7 to +5.5V", p2; "‡ The device is not guaranteed to function outside its operating ratings") | Note 3: "Continuous body diode current conduction (reverse conduction, i.e. VOUT to VIN) is not recommended." Source icreq/txt/mic94094.txt, Microchip DS20006706B (2022-2024); the older Micrel copy (mic9409x_old.txt) gives the same +6 V / 1.7-5.5 V.
- U10 TLV3691IDPFR | IN- (pin 3), VBAT_SW/2 via R17/R18 10k/10k; supply on core 3V3 | abs max signal input (V-) - 0.5 V to (V+) + 0.5 V, i.e. 3.8 V at V+ = 3.3 V, so VBAT_SW <= 7.6 V (6.1, p4) | rec: VCM (V-) - 0.1 V to (V+) + 0.1 V (6.5), 3.4 V at V+ = 3.3 V, so VBAT_SW <= 6.8 V; supply 0.9-6.5 V (6.3, p4) | Not limiting. Source vmain/tlv3691.txt, SBOS694A (December 2013, revised November 2015).
- U2 FT231XQ-R | VCC (pin 12), VUSB through D1 BAT43WS | abs max 5.5 V ("VCC Supply Voltage -0.3 to +5.5 V", Table 5.1, p14) | operating max 5.5 V, typ 5, min 2.97 V ("VCC Operating Supply Voltage 2.97 5 5.5 V Normal Operation", Table 5.3, p14); Icc1 8-8.4 mA; 3V3OUT "3V3 output at 50mA" (Table 3.1). The abs max equals the operating max: no margin above 5.5 V at the pin. D1's forward drop sits between VUSB and this pin. Source icreq/txt/ft231x.txt, FT_000565 Version 1.4.
- Q1 DMG3404L-7 | gate (pin 1) on VBAT+, source on GND, drain on VBAT- | VGSS +/-20 V (Maximum Ratings, p2), VDSS 30 V | VGS(TH) 1.0-2.0 V (VDS = VGS, ID = 250 uA); RDS(ON) max 35 mOhm at VGS = 4.5 V, 25 mOhm at VGS = 10 V (Electrical Characteristics). No RDS(ON) is specified below 4.5 V, so its on-resistance at a 3.3-4 V pack is not rated (UNVERIFIED how much it rises; the typical curves would say). Not limiting at the high end (20 V). Source: Diodes Inc DS37640 Rev. 2-2, downloaded 2026-11-09 from diodes.com/assets/Datasheets/DMG3404L.pdf.
- Q3 2N7002W-7-F | gate (pin 1) on VUSB, source GND, drain to Q2 gate/R19 | VGSS +/-20 V continuous, +/-40 V pulsed ("Gain-Source Voltage VGSS", sic, Maximum Ratings, p2); VDSS 60 V | VGS(th) 1.0-2.0 V. Not limiting. Source: Diodes Inc DS30099 Rev. 17-2, diodes.com/assets/Datasheets/2N7002W.pdf. (The switchover study cites "2N7002PW" thresholds from an Arrow listing; the netlist MPN is 2N7002W-7-F, whose own datasheet gives 1.0-2.0 V.)
- Q2 DMP3099L-7 (for completeness) | source on 3V3, drain on 3V3_FTDI, gate on R19/Q3 drain | VGSS +/-20 V, VDSS -30 V. Sees only 3.3 V levels; not on an input net. Source DS36081 Rev. 5-2.
- D1 BAT43WS-7-F | anode on VUSB, cathode to FT231X VCC | VRRM/VRWM 30 V (Maximum Ratings, p2) | VF 0.26-0.33 V at IF = 2.0 mA, max 0.45 V at 15 mA, max 1.0 V at 200 mA (Electrical Characteristics, TA = 25 C, p2). With the FT231X drawing 8-8.4 mA (Icc1), VF is roughly 0.3-0.45 V (interpolation, UNVERIFIED), so the FT231X VCC sits that much below VUSB. Source: Diodes Inc DS30100 Rev. 15-2 (2022), diodes.com/assets/Datasheets/ds30100.pdf. (Tried ds30120.pdf and BAT43WS.pdf first: 404.)
- R21 RC0402FR-0710KL (10k, VUSB to GND), R17/R22 (10k, VBAT_SW) | 0402/0603 thick-film resistors; working-voltage ratings (Yageo RC0402 50 V; Bourns CRT0603 rating not looked up) are an order of magnitude above any input here. UNVERIFIED: the 50 V figure is from memory, not read in this session. Not limiting.
- C12 (VBAT+), C5 and C11 (VUSB) GCM155R71C104KA55D | 16 V DC rated (Murata code "1C" = DC16V; Farnell and Digi-Key listings "0.1 uF +/-10% 16V X7R 0402"). Murata's own product page is JavaScript-only and returned nothing to a fetch.
- C6 (VUSB) GRM21BR61C106KE15K | 16 V DC (Murata code "1C" = DC16V; from the part-numbering scheme, not a part-specific page). Note X5R 10 uF 0805 at 16 V loses capacitance under DC bias at 5 V (not quantified here).
- C10 (VBAT_SW) CL05A105KA5NQNC | 25 V (Samsung code; Future Electronics "Rated Voltage: 25V", JLCPCB C52923 "1uF 25V X5R 0402").
- C13 (VMAIN) TMK107B7105KA-T | 25 V (Taiyo Yuden "TMK" = 25 V; Arrow "Cap Ceramic 1uF 25V X7R 10% 0603"; datasheets.com 25 V DC).
- J3 OSTVN06A150, J4 USB4105-GF-A | connector ratings not looked up; both far above 6 V in their class (UNVERIFIED, not read). Not plausibly limiting.
- U1 ATmega1284P-MUR | PA2/ADC2 (pin 35), BAT_SENSE = VBAT_SW/2 (R22/R23, 10k/10k, 0.1 % Bourns CRT0603); AREF (pin 29) tied to 3V3 | abs max "Voltage on any pin except RESET with respect to ground -0.5V to VCC + 0.5V" and "Maximum operating voltage 6.0V" (Section 28, Absolute maximum ratings, DS40002070B p325): 3.8 V at the pin at VCC = 3.3 V, so VBAT_SW <= 7.6 V | ADC "0 - VCC ADC input voltage range" with AREF = 3V3: full scale at VBAT_SW = 6.6 V. Operating 1.8-5.5 V; speed grades "0 - 10MHz @ 2.7 - 5.5V" (p1). Not limiting. Source: Microchip DS40002070B (2020), downloaded from ww1.microchip.com.

## Low end

- Core 3V3 (U6 TPS79733, input straight from VBAT+): minimum VI = VO + V(DO). V(DO) at 10 mA: 105 mV typ, 200 mV max (SLVS332J 6.5 p5). So 3.41 V typical and 3.50 V worst case at 10 mA hold 3.3 V. The output accuracy (-4 % to +4 %) is specified only for "VO + 1 V <= VI <= 5.5 V", i.e. 4.3 V and above; below that the datasheet guarantees dropout, not accuracy. The real core load is not measured (no figure found in Project-Margay or NW-Status). The ATmega active current at 8 MHz is a few mA (the ATmega324A table, the only one read, gives 1.5 mA typ at 4 MHz / 3 V and 5.2 mA typ at 8 MHz / 5 V, p328); LEDs D2/D3 through 330 Ohm add a few mA each when lit (UNVERIFIED, not computed from LED Vf). The 10 mA dropout point is therefore a reasonable upper bound for the core, not a measurement.
- 3V3_AUX (U7 TPS7A0533, input VMAIN, reached from VBAT+ through U8 and U9 IN1, and through Q1 in the return): worst case at the TPS7A05's 200 mA rating, -40 to +85 C: U7 VDO 212 mV (SBVS254D p8) + U9 IN1 rDS(on) 435 mOhm max at TJ = 125 C (SLVS235A p5; 250 mOhm typ at 25 C) x 0.2 A = 87 mV + U8 RON 120 mOhm max at VIN = 3.6 V, -40 to +85 C (SLVSDO5F, ON-resistance table) x 0.2 A = 24 mV + Q1 35 mOhm (rated only at VGS = 4.5 V) x 0.2 A = 7 mV. Sum: 3.3 + 0.330 = 3.63 V at the battery terminals. At 50 mA, scaling each term linearly with current (dropout linearity ASSUMED, UNVERIFIED), about 3.38 V. Battery internal resistance under load is not included.
- U9 IN1 is rated from 2.7 V (recommended operating conditions); its UVLO turns the switch off near 2 V. U8 runs from 1 V. Neither binds before the regulators do.
- ATmega brown-out: Northern Widget board package (installed copy ~/.arduino15/packages/NorthernWidget/hardware/avr/0.3.1/boards.txt), board "NW1284p" ("ATMega1284p 8MHz", the board the README tells users to select): low 0xF7, high 0xDE, extended 0xFE. Extended fuse bits 2:0 are BODLEVEL2:0 (Table 27-3), so 0xFE gives BODLEVEL = 110, VBOT 1.7 / 1.8 / 2.0 V min/typ/max (Table 28-13, p334). The README's MightyCore alternative recommends "BOD 2.7v" (README lines 322-331), so the two documented routes set different brown-out levels. With the NW package's 1.8 V level and an 8 MHz clock, VCC between 2.0 and 2.7 V is outside the 0-10 MHz speed grade (2.7-5.5 V) and is not caught by the BOD. The board package source repository (NorthernWidget/Arduino_Boards) was not opened; only the installed 0.3.1 copy.
- Firmware battery threshold: Margay_Library src/Margay.h line 233, "float batVoltageError = 3.3; ///< Battery voltage threshold [V] below which BatError is set and logged" (overridable from Page 1 offset 0x22, Margay.cpp line 208). README: "Batteries <3.3V, voltage too low to properly function".

## Rating, built from the parts

BAT+ (J3 pin 4):
- Recommended operating maximum: 5.5 V. Set jointly by five parts, all rated 5.5 V recommended: U6 TPS79733 VIN (direct), U8 TPS22916 VIN (direct), U9 TPS2104 IN1 (through U8), U7 TPS7A05 VIN (through U8 and U9) and U11 MIC94090 VIN (through U8, U9 and JP2 in its default position).
- Absolute maximum: 6.0 V. Set by the same five parts, all 6 V. The next limits up are U10 TLV3691 IN- and the ATmega's ADC pin, both 7.6 V referred to the battery through their 1:2 dividers; then the 16 V capacitor C12 and Q1's 20 V VGS.
- Minimum for full regulation: about 3.5 V for the core 3V3 at up to 10 mA (TPS79733 dropout, 200 mV max), and about 3.63 V for 3V3_AUX at its full 200 mA (TPS7A05 dropout plus the switch chain), about 3.4 V at 50 mA (ASSUMED linear scaling). The README's 3.3 V floor is below both; at 3.3 V both regulators are in dropout and their outputs follow the battery minus the dropout.

USB (J4 VBUS, VUSB):
- Recommended operating maximum: 5.5 V. Set by U9 TPS2104 IN2 (direct), U7 TPS7A05 and U11 MIC94090 (through U9 IN2), and U2 FT231X VCC (5.5 V operating, behind D1).
- Absolute maximum: 6.0 V at U9 IN2, U7 and U11. The FT231X's VCC absolute maximum is also 5.5 V, but D1 sits in front of it: at the FT231X's 8-8.4 mA, D1 drops roughly 0.3-0.45 V (BAT43WS VF max 0.33 V at 2 mA, 0.45 V at 15 mA; no minimum given), so VUSB would reach roughly 5.8 V before the FT231X pin reaches 5.5 V. Because D1's minimum drop is not specified, the conservative statement is that the FT231X sets the USB absolute maximum somewhere between 5.5 V and about 5.8 V, below the 6 V of the other parts. USB 2.0's 4.75-5.25 V source range (UNVERIFIED, from memory; also the switchover study's figure) sits inside all of these.
- Minimum: U9 IN2 is rated from 2.7 V; FT231X VCC from 2.97 V plus D1's drop. 3V3_AUX from USB needs VUSB >= 3.3 V + 212 mV + IN2's 2.4 Ohm max (TJ = 125 C) x I, about 3.75 V at the IN2 switch's 100 mA continuous rating.
- Side observation: the README's VSwitch table gives 220 mA for "VMain | USB". The TPS2104's recommended IN2 continuous current is 100 mA, with the footnote "The device can deliver up to 220 mA at IO(IN2)" at the cost of more drop and switchover droop (SLVS235A p5).

Parts with the least margin at 5.5 V: U6 TPS79733, U8 TPS22916, U9 TPS2104, U7 TPS7A05 and U11 MIC94090, each 0.5 V from its 6 V absolute maximum; and, on USB, U2 FT231X, whose 5.5 V absolute maximum equals its operating maximum and is protected only by D1's forward drop.

## Three-AA chemistries against the rating (pack voltages from sources/2026-11-09-fresh-aa-voltages-agent-report.md)

- Alkaline, fresh open circuit 4.68-4.95 V: 0.55-0.82 V under the 5.5 V recommended maximum, 1.05-1.32 V under 6 V. End of life (the firmware's 3.3 V threshold, 1.1 V per cell) is at or below the regulation floors above, so the last part of an alkaline pack runs both regulators in dropout.
- Lithium iron disulfide (L91 class), fresh open circuit 5.37-5.49 V: inside the 5.5 V recommended maximum by 0.01-0.13 V, and 0.51-0.63 V under the 6 V absolute maximum. Inside the rating, with the least margin of the three. No manufacturer figure for LiFeS2 open-circuit voltage against temperature was found by the earlier agent, so whether a cold or warm pack moves above 5.5 V is not known from these sources.
- NiMH, 3.75 V (400 mA plateau) to 4.26 V (start at 400 mA): well under the maximum. The plateau is about 0.25 V above the core's worst-case 3.5 V floor and about 0.1 V above 3V3_AUX's worst-case 3.63 V at 200 mA; NiMH is near or below these floors late in discharge.

## Search for a Northern Widget statement against lithium cells

Not found. Where I looked:
- Project-Margay, every tracked and untracked text file (grep for lithium, li-ion, LiPo, L91, LiFeS2, "Energizer Ultimate"; KiCad and Eagle library files excluded): no hits. README says "Input voltage designed for use with easy to find alkaline batteries" (lines 35, 60) and "BAT+ ... voltage range 3.3v ~ 5.5v" (line 163), with no chemistry warning.
- Project-Margay git history, all branches: git log -S lithium, and -G "L91|li-?ion|LiFeS2": no commits.
- Project-Margay/Documentation: MargayGuide.odt (content.xml extracted), MargayGuide_20190730.pdf and MargayGuide_20220622.pdf (pdftotext): battery text is only "Batteries <3.3V" and "(>3.3 V)"; no lithium.
- Margay_Library (source, git history): no lithium; Margay.h says the percentage fit is "developed for Duracell AA alkaline cells ... accuracy not guaranteed for other chemistries".
- NW-Status: lithium appears only in this session's own studies (margay-vmain-switchover.md, margay-power-path-lm66100.md, margay-power-path-decision.md, which already notes "not found in Project-Margay's README, docs or guides", and two agent reports).
- Whole workspace (*.md, *.html, *.txt, excluding _site): the only battery-chemistry statements are in Project-Okapi's README ("3 primary ... Alkaline (or better) AA batteries", line 111) and NW-Device-Specification (a chemistry selector for the battery curve). Neither warns against lithium.
- Local website repositories NorthernWidget.github.io, -archive, -archive2 (including the 2018 project-margay post): no lithium, alkaline or 5.5 V text.
- northernwidget.com (Shopify; home page and products.json): Margay's product description is 44 characters with no battery text. northernwidget.github.io/loggers/: no hits.
- Wickert et al. (2019), HESS 23, 2065 (hess.copernicus.org/articles/23/2065/2019/): covers the ALog loggers only, not Margay; mentions lithium only as "rechargeable battery (typically lithium ion)" for solar setups. Read through WebFetch's summarizer, not the PDF directly.
- Web search "Northern Widget Margay data logger battery lithium AA": nothing relevant.

## Other observations (proposals only, not part of the rating)

- U7 TPS7A05 EN absolute maximum is VIN + 0.3 V (SBVS254D 6.1). EN is driven by the ATmega (3V3_AUX_CTRL, 3.3 V) from the always-on core, while VIN is VMAIN, which is near 0 V when U8 is off and USB is absent. Whether firmware ever drives 3V3_AUX_CTRL high with VBAT_SW off was not checked.
- With JP2 in its default position, Vs (J3 pin 2) carries VMAIN, i.e. up to the battery voltage less the switch drops, to external sensors: a sensor on Vs must tolerate 5.5 V (5.49 V with fresh lithium).
- The README (line 405) says the DS3231M "is powered exclusively by the CR1220 coin cell", but in the v3.1 netlist RTC1 VCC (pin 2) is on 3V3_AUX. Not part of this task; noted for whoever revises the README.

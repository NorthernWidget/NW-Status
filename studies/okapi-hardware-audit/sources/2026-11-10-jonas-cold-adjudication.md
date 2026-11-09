<!-- Blind adjudication. Key: list A = field, B = circuit, C = firmware, D = physics, E = margay-rtc-cold.md candidates 1-7 -->
COMPLETE

# Adjudication of candidate lists A-E: Margay clock failures in the cold

Inputs: adj/evidence.md, adj/list-A.md ... list-E.md. Judged blind. "Verified" below means I checked it myself in this session against the source named; anything else is marked UNVERIFIED or attributed to a list.

Observations: (O1) clock failures on battery power in the cold (email: about 0 °C and windy; Andy recalls about -20 °C); (O2) cure by a warm/replacement coin cell (written); (O3) cure by powering through a USB cable spliced to the same D cells (Andy's unwritten 2026 recollection).

## 1. Frame facts (verified)

- F1. RTC1 (DS3231M) VCC is on 3V3_AUX only, which is U7 (TPS7A05) VOUT; U7 EN = 3V3_AUX_CTRL = PC6. RTC1 VBAT = VCOIN+ = BT1(+) and C19 (0.1 uF, 0402) only. Source: eagle.json nets 3V3_AUX, 3V3_AUX_CTRL, VCOIN+.
- F2. PC6 = D22 (NW1284p pins_arduino.h); Margay model 2 sets `Ext3v3Ctrl = 22`, `BatSwitch = 19` (PC3, U8 EN), `RTCInt = 2` (PB2/INT2), and `powerAux()` uses positive logic for model >= 2. Source: Margay.cpp (2024 cache) lines 36-62, 877-891; Margay.h MODEL_2v2 = 2.
- F3. Every sleep: `sleepNow()` -> `turnOffSDcard()` -> `powerAux(OFF); powerOB(OFF);` (Margay.cpp 951, 1006-1007). Every wake: `powerOB(ON); powerAux(ON); delay(6)` (1037-1039). This is library code, so it holds whatever the (unknown) field sketch was, unless the sketch bypassed `run()`.
- F4. VMAIN = U9 TPS2104 OUT; IN1 = VBAT_SW (U8 out), IN2 = VUSB; EN = U10 TLV3691 OUT, IN+ = 3V3_FTDI, IN- = R17/R18 tap of VBAT_SW (10k/10k). TPS2104 function table: EN = H gives OUT = VIN2 even with VIN2 = 0 V; EN = L gives VIN1. TPS2104 features: "No Reverse Current Flow (No Parasitic Diodes)"; operating range 2.7-5.5 V; "Unused INx should not be grounded". Source: eagle.json; tps2104.txt lines 8, 24, 110-117, 219.
- F5. USB detection: Q3 (2N7002, G = VUSB, R21 10k to GND) pulls N$6 low; Q2 (FDN360P, S = 3V3, D = 3V3_FTDI, G = N$6 with R19 100k to 3V3) then ties the FT231X 3V3OUT/VCCIO/RESET# node to the MCU 3V3 rail. MCU 3V3 = U6 TPS79733 from VBAT+ (J3.4). Battery return J3.3 = VBAT- through Q1; USB GND goes straight to GND. Source: eagle.json.
- F6. DTR# of the FT231X couples through C1 to MCU RST (net DTR, net RST also has R2, S1, U3 TPL5010 RSTN). Source: eagle.json.
- F7. DS3231_Logger at 850dfbf, byte-identical to ~/Arduino/libraries/DS3231_Logger/src/DS3231_Logger.cpp (diff): begin() writes 0x0E = 0x24; setAlarm writes 0x0E = 0x05 (or 0x06); clearAlarm writes 0x0F = 0x00. BBSQW is never set; OSF is never read and is cleared.
- F8. DS3231M datasheet (icreq/txt/ds3231m.txt): VBAT 2.3-5.5 V; IBATTC 575 uA (3.63 V) / 650 uA (VBATMAX); tCONV 10 ms; conversions every 10 s on VBAT; tVCCF min 300 us; VPF 2.45/2.575/2.70 V; "When BBSQW is logic 0, INT/SQW goes high impedance when VCC falls below VPF"; on the first application of VCC power after total loss the time resets to 01/01/00 01 00:00:00; I2C "accessible whenever either VCC or VBAT is at a valid level" and can desynchronize on an MCU reset.
- F9. Time can be set only in `begin()`, from any bytes on Serial within about 100 ms of the banner (Margay.cpp 224-235); the only other setTime is commented out (477). `clockTest()` (453-491): NACK -> " FAIL" + OBError (red); seconds not advancing in 1.1 s -> OBError with nothing printed; year == 00 -> " PASS, BAD TIME" + TimeError (cyan).
- F10. The 2022 Operations Guide (jonas/guide2022.txt) has no USB step at deployment: Initialize is "turn battery pack on" and wait for the flash; Download and SD swap say "turn battery pack off". Cyan is "Clock time is incorrect ... Connect the logger to a computer and reset the clock using the Northern Widget Time Set GUI".
- F11. TPS7A05 8.1.3 (tps7a05.txt 1599-1606): below 15 °C ambient, IN must ramp down no faster than 10 ms and EN no faster than 100 us, or "the next startup may exhibit a partial startup, shutoff, followed by a normal soft-start startup". Startup 1.5 typ / 2.8 max ms. RPULLDOWN 120 ohm (P version), active when disabled or in UVLO.
- F12. Energizer CR1220 (jonas/cr1220/CR1220.txt): pulse test at 21 °C, 1 kohm pulse gives 2.8 mA at 2.65 V fresh; the IR axis of the plot runs to 280 ohm over life. Panasonic CR1220 (jonas/dl): operating -30 to +85 °C, continuous drain 0.1 mA. No pulse-voltage-at--20 °C figure exists in either sheet.

## 2. Contradictions resolved

R1. "The clock runs on its coin cell during every sleep in both power modes" (A, B, C, D): HOLDS. F1 + F2 + F3: the firmware disables U7 before every sleep, and U7 is the clock's only VCC source. In USB mode VMAIN stays live, so U7's 120 ohm pulldown holds 3V3_AUX at 0 V; on the battery terminal VMAIN loses its source too (U8 off). The coin-cell load in sleep is therefore identical in the two modes, and no coin-cell mechanism acting during sleep can explain O3 by itself.

R2. List E's late handover at the USB unplug: THE ELECTRICAL FACT HOLDS, THE CONCLUSION DOES NOT.
- Holds (verified from topology, F4 + F5): while VUSB stays above Q3's gate threshold, Q2 keeps 3V3_FTDI tied to the U6-held 3V3 rail, so U10 IN+ is about 3.3 V against IN- of about VBAT_SW/2 (about 2.25 V with three fresh D cells), EN stays high and U9 keeps VMAIN on the collapsing VUSB. VMAIN, and 3V3_AUX behind U7, follow VUSB down until Q3 releases. The handover voltage is set by the 2N7002 threshold (generic range about 1-2.5 V, UNVERIFIED for this part); E's "about 2 V" is plausible and UNVERIFIED. Below about 1.2-1.4 V on VMAIN, U7 also enters UVLO and must soft-start again (F11).
- Does not hold, three reasons. (1) It matters only if the logger is awake at the unplug. Asleep, U7 is already off and the clock is already on VBAT (F3). The logger sleeps within seconds of `begin()` finishing (`run()` sleeps once `AwakeCount > 5`). (2) It is not specific to battery-terminal loggers. J4 is the only serial port and time is set only over it (F9), so every logger whose time was set, spliced ones included, ended its time-set session with a USB unplug. E's "the spliced-USB loggers never see an unplug" is false. (3) As a coin-cell stress it is one VCC-to-VBAT switchover among the one at every sleep entry, in both modes; it adds nothing a cold cell would not already face daily. It is also slower than the sleep-entry fall, which is the direction the datasheet wants (tVCCF is a minimum).
- What survives of E #1: a brown-out of the I2C pull-ups (R15, R16 are on 3V3_AUX) while the MCU is awake, possibly mid-transaction, and a possible MCU reset through DTR#/C1 as the FT231X loses power (F6; UNVERIFIED on hardware). Both feed M3 (wedged bus) and M9 (spurious serial set) below. The Operations Guide (F10) puts no unplug at deployment, so this happens in the lab, at time-set, unless Jonas set the time in the field (which a coin-cell swap forces: R4).

R3. Can INT/SQW wake the MCU on VBAT with BBSQW = 0? BY THE DATASHEET, NO; BY SERVICE RECORD, APPARENTLY YES; UNRESOLVED BY DOCUMENTS. The text is unambiguous (F8), BBSQW is always 0 (F7), and VCC is 0 V in every sleep (R1). Every list noticed the conflict and none resolved it; I cannot either without a measurement. It is cheap to settle and it decides whether the whole sleep/wake model is right, so it is in the test order (T2). Note that an RTC_INT that never fires leaves wakes to the TPL5010 (RSTN is on RST, F6), whose interval with R10 = 130 k lies between the 1 h (124.91 k) and 1 h 30 min (149.39 k) rows of TPL5010 Table 3 (verified, tpl5010.txt 891-894); each such reset re-runs `begin()` and sets `NewLog = true` (Margay.cpp 320), so it leaves a signature in any existing Margay dataset: a new Log file roughly every hour.

R4. Does a coin-cell swap force a USB connection, confounding O2 with a USB session? YES, ALMOST ALWAYS. Removing BT1 while 3V3_AUX is off (any time the logger sleeps, and whenever the pack is off, which the guide requires for SD work) leaves the DS3231M with no supply; the next VCC brings it up at 01/01/00 (F8), which `clockTest()` reports as cyan (F9). The library offers no way to set the time except Serial at `begin()` (F9), and the guide's cyan remedy is the Time Set GUI on a computer (F10). The exceptions are a swap made during the few seconds the logger is awake with VCC up, or a field sketch that sets the time some other way (sketch unknown). So the warm-cell cure most likely bundled: a new cell, a reseat, a full RTC power-on reset, a fresh `begin()` with alarms rewritten, a laptop session, and an unplug at its end. It also means a laptop was in the field.

Other list claims checked:
- A says VMAIN collapses at sleep entry through U9's IN1 N-channel body diode in "roughly a sub-millisecond ramp". CONTRADICTED by F4: the TPS2104 advertises no reverse current and no parasitic diodes. With both U9 inputs dead, VMAIN on C13 (1 uF) decays only through U7's and U11's quiescent currents and U9's own supply current, so its ramp-down may be slow. Whether the TPS7A05 10 ms caution is violated on the battery path is therefore open and needs a scope (it weakens, but does not kill, M6).
- B, C, D say U9 EN = H selects IN2 even when VUSB = 0 V: VERIFIED (F4 function table).
- A, B, C, D say the alarm interrupt has no external pull-up (only `INPUT_PULLUP` to the MCU 3V3): VERIFIED (net RTC_INT = RTC1 SQW + U1 PB2 only; Margay.cpp 268).
- TPL5010 interval: A and B interpolate about 1 h; A quotes a README figure of "approximately 36 minutes". The datasheet table (above) puts 130 k past the 1 h row, so 36 min is not consistent with R10 = 130 k.

## 3. Deduplicated mechanisms

Notation: O1 cold, O2 warm/new cell, O3 USB splice. Y = explains, P = partly or only through another mechanism, N = does not.

### M1. Cold or worn CR1220 cannot carry the DS3231M's conversion pulses on VBAT (A-C1, B-C, C-1, D-1, E-3)
- Explains: O1 Y; O2 Y; O3 N (R1).
- For (verified): F1 (C19 0.1 uF is the only reservoir on VCOIN+), F3 (VBAT duty every sleep), F8 (575-650 uA for 10 ms every 10 s, 2.3 V floor). Arithmetic: 0.1 uF supplies 575 uA for about 17 us per 0.1 V of droop, so the cell carries the pulse. F12: a fresh Energizer cell at 21 °C has roughly 100 ohm pulse IR (0.06 V at 575 uA), up to about 280 ohm late in life (0.16 V). The cell would need about 1 kohm or more to dip below 2.3 V.
- Against: the pulse IR at -20 °C is not in any sheet read (UNVERIFIED in every list, including D's 1.6-2.5 V bracket, which is an extrapolation). At the email's 0 °C, a fresh cell rated to -30 °C (Panasonic) is unlikely to reach 1 kohm; the case needs Andy's -20 °C, a worn cell, or both. A warm cell returns to ambient in minutes (A; order of magnitude, UNVERIFIED), so a lasting O2 cure cannot be the warmth alone. It cannot produce O3.
- Test cost: low to moderate. Bench coin-cell emulator (supply plus series R, 100 ohm-3 kohm) at room temperature with a sketch that reads 0x0F before any write: half a day, gives the failing resistance. Then a real CR1220 pulsed at 575 uA/10 ms at +20, 0, -20 °C, fresh and used: half a day with a freezer.

### M2. The "warm cell" cure was a new cell, a reseat and a full RTC reset (A-C2, B confound, C-8, D-2, E-2)
- Explains: O2 Y; O1 P (contact or worn-cell variants only); O3 P (only if the USB rewire also reseated or reset the clock, or if "USB" was the laptop session the swap forced: R4).
- For (verified): R4 (a swap power-cycles the RTC and forces a laptop time-set session). BT1 is a 12 mm holder (eagle.json dev 12MM); whether it is loose on a 2.0 mm 1220 is UNVERIFIED.
- Against: on its own it does not say why only cold units failed; it is a confound that hides which mechanism was cured.
- Test cost: free first (ask Jonas the order of operations, whether a laptop was used, whether swapped units failed again later); then put the original cells back in failed units on the bench.

### M3. RTC I2C state wedged and held alive by the coin cell; only removing the cell clears it (A-C5 part, B-F, C-2)
- Explains: O2 Y (as a power cycle); O1 P (needs something cold-related to cause the reset or brown-out that starts it); O3 P (only through M4/M5/M14 events being absent on USB).
- For (verified): F8 (datasheet's own desync warning and SCL-toggle recovery); no bus recovery in the driver or library (F7, `Wire.begin()` only); I2C pull-ups on 3V3_AUX, which is cut every sleep while the RTC stays powered (F1, F3). Old Wire without timeouts (lists A, C; not re-checked by me).
- Against: no evidence the bus was stuck; "Clock: FAIL" (NACK) is what it would show, and the symptom is unknown.
- Test cost: low on a failed unit as received (scope or meter SDA_OB with the logger awake before touching the cell; nine SCL clocks from a test sketch). Endurance cycling at -20 °C is higher cost.

### M4. Field wiring on the battery terminal: brief supply loss, MCU reset mid-I2C (A-C5, D-8 for Q1)
- Explains: O1 P (cold leads and contacts); O2 P (through M3, cured by the power cycle in R4); O3 Y (different connector, ground path without Q1, and MCU regulator; F5).
- For (verified): J3 is a 2.54 mm screw terminal (eagle.json dev SCREW_2.54); battery return through Q1 (F5). Against: requires flaky wiring on several units; D argues Q1 is fully enhanced at pack voltage (UNVERIFIED).
- Test cost: free to cheap (ask about pack, leads and connector; tug test and inspection of returned units).

### M5. Pack voltage too low or sagging at wake on the battery-terminal path, with a 1.8 V BOD (B-B, C-4, D-7, E-6)
- Explains: O1 Y (alkaline IR rises in the cold); O3 Y for three cells (IN2 PMOS needs no charge pump; VMAIN not switched at wake in USB mode, F3/F4); O2 P (through M3 or a POR). With two cells, O3 is not explained either, since the FT231X then sees about 2.7 V (B's point; the FT231X minimum is from B, not re-checked).
- For (verified): TPS2104 charge pump "as low as 2.7 V" (tps2104.txt 219); firmware cycles U8 every wake only on the battery path (F3); extended fuse 0xFE (A, B, C, D read boards.txt; BOD decode 1.8 V is UNVERIFIED in all lists). The firmware assumes three cells (B: `getBatPer()` /3.0; not re-checked).
- Against: with three fresh D cells there is about 1 V of margin over U6 (D, from E95 data); D-cell sag acts on both paths alike.
- Test cost: free (ask the cell count); bench voltage sweep on both connectors, room temperature then -20 °C, a few hours.

### M6. TPS7A05 cold power-cycling on the battery path, below 15 °C (A-C3, E-4, C frame note)
- Explains: O1 Y (the caution applies below 15 °C, so it is live at 0 °C and -20 °C); O3 Y (in USB mode VMAIN is never cut, so the IN ramp-down half of the caution never applies; verified F3/F4); O2 P (only if the resulting 3V3_AUX glitches harm the clock through a weak cell, or through M3).
- For (verified): F11 text; firmware switches EN by GPIO (nanoseconds, so the EN half of the caution, 100 us minimum, is violated on both paths at every sleep). E-4's slow 3V3_AUX rise on battery (U8 1.4 ms 5 V turn-on per C, U9, then U7 up to 2.8 ms) against `delay(6)`: the first RTC access at wake comes much later (in `addDataPoint`), so a late rail threatens the SD card more than the clock.
- Against: A's sub-millisecond VIN ramp rests on a body-diode path the TPS2104 datasheet denies (section 2, "Other list claims checked"), so the VIN half may not be violated at all. TI does not quantify the harm; nobody has observed it. The EN half applies equally in USB mode, so only the VIN half discriminates O3.
- Test cost: moderate (four-channel scope, freezer, one day): 3V3_AUX, VMAIN, VBAT, INT across sleep/wake on J3 and on the USB splice at +20 and -20 °C. Firmware A/B (keep U8 on through sleep) is cheap once the scope rig exists.

### M7. 3V3_AUX falls faster than tVCCF at every sleep entry (A-C4, B-D, C-5, D-5)
- Explains: O1 P and O2 P (only as an amplifier of M1); O3 N (U7's pulldown is at least as strong in USB mode).
- For (verified): tVCCF min 300 us (F8); 120 ohm pulldown (F11); C15 10 uF 0805 (eagle.json). Arithmetic for C15 + C16 = 10.1 uF and 120 ohm alone: tau = 1.21 ms, 2.70 to 2.45 V in 0.118 ms. Loads only make it faster. A real spec violation either way.
- Against: it happens identically at room temperature, where loggers work; the datasheet does not say what the violation does.
- Test cost: low once a scope is on 3V3_AUX (same rig as T5); A/B with added capacitance.

### M8. U10 selects the dead USB input on battery because 3V3_FTDI is back-fed (A-C9, B-A, C-7b, D-4)
- Explains: O3 Y (by construction: with USB present EN = H selects a live IN2, verified F4/F5); O1 P (cold lowers VBAT_SW/2 and changes leakage; direction argued, size UNVERIFIED); O2 N (a coin cell does not change the comparator).
- For (verified): 3V3_FTDI has no driver on battery (Q2 off, FT231X unpowered; F5); TX idles high into FT231X RXD through R9 330 ohm (net TX/N$35); LED D2 cathodes go through R8/R5 to CBUS1/CBUS2 (nets). The back-fed voltage itself is UNVERIFIED in every list.
- Against: if the back-fed level could exceed VBAT_SW/2, loggers would lose VMAIN at room temperature too unless the margin is thin; the failure would also take down the SD card, BME280 and MCP3421 (all on 3V3_AUX), which a field team would report as more than "the clock". It does not explain O2.
- Test cost: very low (multimeter, 10 minutes, room temperature: 3V3_FTDI, N$14 and VMAIN on battery with the logger awake; repeat at -20 °C only if the margin is small).

### M9. Back-fed or unpowering FT231X injects a byte or a reset at boot on battery, and the unvalidated time-set zeroes the clock (C-3, C-7a)
- Explains: O3 Y (with USB powered, TXD idles high and DTR# is steady); O1 P (UNVERIFIED temperature dependence); O2 P (a swap forces a correct time-set anyway, R4).
- For (verified): any byte within about 100 ms of the banner triggers `setTime()` with `toInt()` fields, so garbage gives 2000/00/00 00:00:00 (F9); DTR# couples to RST through C1 (F6), so the FT231X losing power at an unplug can plausibly pulse RST (UNVERIFIED on hardware).
- Against: the FT231X inputs are "5V tolerant" (C, D quoting ft231x.txt), which argues against back-feed; no list measured RX at boot.
- Test cost: free discriminator in the data (2000/00/00 00:00 means a spurious set; 2000/01/01 01:00 means a DS3231M power-on reset); low bench cost (logic analyzer on PD0 and RST over 50 boots; scope RST during an unplug).

### M10. 3V3_AUX floating or back-fed in battery-mode sleep, pinned to 0 V in USB mode (D-3, E-5)
- Explains: O1, O2, O3 all, if a back-feed source exists.
- For (verified): in USB mode VMAIN stays live, so U7's pulldown is biased; on battery U8 is off (F3/F4).
- Against: no list found an on-board source that drives 3V3_AUX in sleep (D searched; E-5 names an SPI back-feed without tracing it). My check weakens the premise further: with no reverse path in U9 (F4), VMAIN may hold on C13 for a while in battery sleep, keeping the pulldown biased. Needs an external source (probes on J2) or an untraced path.
- Test cost: very low (meter or scope on RTC pin 2 during a long battery-mode sleep, with field probes attached).

### M11. Alarm cannot assert INT/SQW on VBAT with BBSQW = 0 (A-C10, B-E, C-6, D-6)
- Explains: none of O1-O3 by itself; it governs whether the logger wakes on the clock at all (R3). It becomes a cold mechanism only if the undocumented assertion on VBAT is marginal at low VBAT or temperature.
- For (verified): F7, F8, R1. Against: service record (loggers log on schedule, per the lists; not verified by me).
- Test cost: free first (inspect any existing Margay field dataset for hourly new Log files); then a room-temperature scope on RTC_INT and 3V3_AUX through one sleep (an hour).

### M12. Cold MEMS oscillator start exceeds the 1.1 s self-test after a power-on reset (A-C8, B-G)
- Explains: O1 P; O2 P (warmer restart); O3 N. A startup indication (red, nothing printed), not lasting failure.
- For (verified): F8 "Typical oscillator startup time is less than 1s"; F9 1.1 s window. Against: the DS3231M is specified to -45 °C; nothing says start time grows in the cold.
- Test cost: moderate (freezer, insert cell, time the first seconds increment, ten trials).

### M13. Condensation, frost or flux leakage at VCOIN+ or the holder (A-C7, E-7, D holder note)
- Explains: O1 P; O2 P (handling dries or reseats); O3 N.
- For: VCOIN+ is a microamp node (IBATT 2-3.5 uA, F8). Against: nothing observed; 0 °C wind argues for condensation only if units were handled warm and closed.
- Test cost: low (megohmmeter VCOIN+ to GND with BT1 out; inspect under BT1).

### M14. USB unplug at deployment with a late VMAIN handover (E-1)
- See R2. Explains: O1 P and O2 P (only through M1, which acts every sleep anyway, or through M3/M9); O3 N as argued (spliced loggers had unplugs too). The verified residue is folded into M3 and M9.
- Test cost: low (scope 3V3_AUX and RST while unplugging USB during `begin()` with the pack connected, 30 minutes).

### M15. Provenance: the "USB splice" may be Jonas's proposed D-cell-to-clock (VBAT) rewire (A-C6; D asks to confirm the recollection)
- Explains: all three, if what was done was to feed VBAT from the D cells; that removes M1, M2, M7 and M13 at once.
- For (verified): evidence.md item 1 records Jonas proposing "connect the clock to the D batteries" and "will decide then if we'll try to rewire the clock"; item 2 says the USB recollection is unwritten. Against: Andy's recollection is specific about USB.
- Test cost: free (ask Jonas for a description or photo of the rewire, and which units).

### M16. Self-heating in USB mode (D-10)
- Explains: O3 P (warms the same coin cell). Against: D's own estimate is 1-2 K (UNVERIFIED), against a 20 K problem. Negligible. Test: none needed unless everything else dies.

### Not a mechanism, a diagnostic blind spot (A, B, C, D)
The firmware clears OSF before `clockTest()` and at every alarm (F7, F9), so an oscillator stop on VBAT short of a full reset leaves no trace. Any bench sketch must read 0x0F before writing it.

### Ruled low by the lists and not contested (D-9)
Regulators, switches, comparator, MCU and ceramics are all specified to -40 °C (D, from the datasheets in the pack); I did not re-check every rating.

## 4. Ranking

Ordered by observations explained, weighted by how much of the chain I verified, then by test cost.

| Rank | Mechanism | O1 | O2 | O3 | Chain verified | Cheapest test |
|---|---|---|---|---|---|---|
| 1 | M1 cold/worn CR1220 vs conversion pulses | Y | Y | N | all but the cell's cold pulse IR | half-day bench emulator |
| 2 | M2 swap = new cell + reseat + RTC reset + laptop session | P | Y | P | swap forces POR and a serial time-set (R4) | free: ask Jonas |
| 3 | M15 "USB" was the D-cell-to-VBAT rewire | Y | Y | Y | written record shows the proposal only | free: ask Jonas |
| 4 | M6 TPS7A05 below-15 °C ramp caution, battery path only | Y | P | Y | caution and mode difference verified; VIN ramp unmeasured, A's ramp path refuted | one-day freezer scope |
| 5 | M5 pack sag / two cells / 1.8 V BOD at wake | Y | P | Y (3 cells) | path difference verified; pack unknown, BOD decode unverified | free: ask cell count |
| 6 | M8 comparator picks dead USB input | P | N | Y | topology verified; back-feed voltage unmeasured | 10-minute meter check |
| 7 | M4 J3 wiring interruptions | P | P | Y | connector and Q1 path verified | free: ask, inspect |
| 8 | M3 wedged RTC bus held by coin cell | P | Y | P | no recovery code, desync warning verified | low: probe failed unit |
| 9 | M9 spurious serial byte / DTR reset zeroes clock | P | P | Y | code path and DTR-C1-RST verified; back-feed unverified | free: timestamp pattern |
| 10 | M7 tVCCF violation | P | P | N | verified violation, effect unknown | low with T5 rig |
| 11 | M10 floating 3V3_AUX in battery sleep | Y | Y | Y | no source found; premise weakened by U9 having no reverse path | 10-minute meter check |
| 12 | M14 E's unplug handover | P | P | N | handover verified; discrimination refuted (R2) | 30-minute scope |
| 13 | M11 BBSQW = 0 alarm on VBAT | - | - | - | datasheet conflict verified | free: existing data |
| 14 | M12 cold oscillator start vs 1.1 s test | P | P | N | text verified | freezer trials |
| 15 | M13 condensation/leakage | P | P | N | none | megohmmeter |
| 16 | M16 USB self-heating | - | - | P | none | none |

No single mechanism with a verified chain explains all three observations. The best-supported reading is two parts: M1 (the coin cell is the clock's only supply in every sleep, in both modes) accounts for O1 and O2, and O3 is either a confound (M2, M15) or a battery-path-only effect (M6, M5, M8, M4), each of which still lacks one measured link. The list that claimed a three-way fit from the USB unplug (E-1) fails on R2.

## 5. Recommended test order (cheapest discriminating step first)

T0. Ask Jonas (free; separates M1/M2/M3/M8/M9/M15 before any bench work):
  (a) what "the clock failed" looked like: STAT color (cyan, red, or other), serial text ("PASS, BAD TIME", "FAIL", or "Clock:" with nothing), and bad timestamps (2000/01/01 01:00 = DS3231M power-on reset, M1/M2/M13; 2000/00/00 00:00 = spurious serial set, M9; garbage = I2C read failure; correct but lagging = oscillator stop);
  (b) when it showed: at first power-on in the field after transport, or later in the data;
  (c) whether a laptop re-set the time after each cell swap, and whether swapped units failed again later;
  (d) the pack: cell count, connector, lead length;
  (e) exactly what the "rewire" or USB splice was, on which units, with a photo, and whether those units' coin cells were also changed;
  (f) whether he kept the original coin cells and the SD cards.
T1. Read existing data (free): Jonas's SD files and any in-house Margay dataset, for (i) the timestamp pattern in T0(a) and (ii) a new Log file roughly every hour, which would mean wakes come from the TPL5010 and not the RTC alarm (M11, R3).
T2. Room-temperature meter and scope checks, under an hour on one bench unit: on J3 with no USB, logger awake, measure 3V3_FTDI, N$14 (U9 EN) and VMAIN (M8); through a long sleep, RTC pin 2 with probes attached (M10); RTC_INT and 3V3_AUX across one alarm (M11); unplug USB during `begin()` with the pack on and scope 3V3_AUX and RST (M14, M9 DTR path).
T3. Coin-cell emulator at room temperature (half day): bench supply plus series resistor in place of BT1, instrumented sketch reading 0x0F and 0x0E before any write; find the resistance at which OSF sets or time resets (M1, M7).
T4. Real CR1220 pulse test in a freezer (half day): 575 uA for 10 ms every 10 s at +20, 0, -20 °C, fresh and used cells, and the failed units' originals if kept (M1, M2). This says whether 0 °C or only -20 °C is in reach.
T5. Freezer A/B on a four-channel scope (one day): the same unit on J3 and on the USB splice from the same pack at +20 and -20 °C; 3V3_AUX, VMAIN, VBAT and INT across sleep and wake (M6, M7, M5 with a pack-voltage sweep, M11 in the cold).
T6. Failed units as received, before touching the cell: dump RTC registers 0x00-0x12, probe SDA_OB awake, inspect J3 terminations and the BT1 holder, megohm VCOIN+ to GND with BT1 out (M3, M4, M13).

## 6. Sources checked (dead ends included)

- adj/evidence.md, adj/list-A.md to list-E.md.
- rtc/eagle.json: nets 3V3, 3V3_AUX, 3V3_AUX_CTRL, 3V3_FTDI, VCOIN+, VMAIN, VUSB, VBAT+, VBAT-, VBAT_SW, VBAT_SW_CTRL, N$6, N$7, N$12, N$14, DTR, RST, RTC_INT, SCL, SDA, SDA_OB, TX, RX, N$25, N$35, LED nets; parts Q1, Q2 (FDN360P), Q3 (2N7002), U9, U10, C13, C15, C19, R10 (130k), R17, R18, R19 (100k), R21, BT1 (12MM), J3 (SCREW_2.54).
- Margay_Library-Wickert-Local-cached20241227/src/Margay.cpp lines 30-62, 160-275, 440-520, 700-1060; Margay.h model enum. Not checked: the uncommitted diff B mentions, `getBatPer()`, the Wire library in the board package.
- NW1284p variants/pins_arduino.h (D2 = PB2, D19 = PC3, D22 = PC6). boards.txt fuses: not re-read (all four lists agree on 0xFE).
- DS3231_Logger at 850dfbf (git show), diffed against ~/Arduino/libraries copy: identical.
- icreq/txt/ds3231m.txt (electrical tables, pin descriptions, power control, Control register).
- cc/dl/tps7a05.txt (8.1.3, 7.3.2, 7.3.4, switching characteristics), tps2104.txt (features, function table, description), tpl5010.txt (Table 3).
- jonas/guide2022.txt (2022 Operations Guide).
- jonas/dl/CR1220_Datasheet_EN.txt (Panasonic), jonas/cr1220/CR1220.txt (Energizer CR1220).
- Dead ends: jonas/cr1220/lithiumcoin_appman.pdf and CR1220_DataSheet_e.pdf are HTML pages, not PDFs (no cold IR data obtained). No 2N7002PW, FDN360P, FT231X or ATmega1284P data re-read; their numbers above are marked UNVERIFIED or attributed to a list.
- Not read, per instructions: NW-Status, GitHub issues, the other reports in the parent directory (report-*.md, key.txt), and the margay-vmain-switchover.md that list E cites.

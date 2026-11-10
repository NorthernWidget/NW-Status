COMPLETE

# DS3231M BBSQW / INTCN alarm on VBAT

## Sources checked

## Findings
### F1. DS3231M datasheet 19-5312 (local text icreq/txt/ds3231m.txt), verified by grep
- Control reg BBSQW (line 812): "When set to logic 1 with INTCN = 0 and VCC < VPF, this bit enables the 1Hz square wave. When BBSQW is logic 0, INT/SQW goes high impedance when VCC falls below VPF."
- INTCN (line 823): "When the INTCN bit is set to logic 1, a match between the timekeeping registers and either of the alarm registers activates the INT/SQW output (if the alarm is also enabled)." No VCC condition stated.
- Pin 3 (line 466): open drain, "requires an external pullup resistor connected to a supply at 5.5V or less."
- VPF = 2.45 / 2.575 / 2.70 V min/typ/max (line 127).
- The second BBSQW sentence carries no INTCN qualifier: read literally, BBSQW=0 tri-states INT/SQW below VPF whatever INTCN is.

### F2. Firmware (Margay_Library src/Margay.cpp + NW_Logger src/NW_Logger.cpp at 000ffce), verified by reading
- Model 2/3: RTCInt = 2 (D2 = PB2/INT2 on 1284P Mighty core), WDHold = 23, Ext3v3Ctrl = 22, BatSwitch = 19.
- NW_Logger::attachLoggerInterrupts: `attachInterrupt(digitalPinToInterrupt(RTCInt), NW_Logger::isr1, FALLING);` then `pinMode(RTCInt, INPUT_PULLUP);` -> MCU internal pull-up IS enabled on RTC_INT; wake mode is FALLING edge.
- Margay::turnOffSDcard (called by sleepNow): `powerAux(OFF)` and `powerOB(OFF)` before sleep_cpu; SLEEP_MODE_PWR_DOWN, BOD disabled.
- run(): after a row, `_rtc.setAlarm(_logInterval)` then `resetWDT()` (pulse on WDHold = TPL5010 DONE). Also: `if (!digitalRead(RTCInt)) { ... _rtc.setAlarm(...) }` catch.
- 2024 cached copy (Margay_Library-Wickert-Local-cached20241227/src/Margay.cpp): same: line 257 attachInterrupt(RTCInt, isr1, FALLING); line 268 pinMode(RTCInt, INPUT_PULLUP); turnOffSDcard powerAux(OFF) + powerOB(OFF) before PWR_DOWN.
### F3. DS3231_Logger driver (DS3231_Logger @2d6925b; DS3231_Logger_NWcore @66b7a1c; ~/Arduino/libraries copy @a4f537e: identical control writes)
- begin(): 0x0E <- 0x24 ("Start oscilator, turn off BBSQW, Turn off alarms, turn on convert") = CONV|INTCN.
- setAlarm(60): 0x0E <- 0x06 (INTCN|A2IE); otherwise 0x0E <- 0x05 (INTCN|A1IE). BBSQW = 0 and EOSC = 0 always.
### F4. Netlist (Project-Margay @5b5d358, Hardware/KiCAD/Margay.kicad_sch rev 2.2 title block, exported with kicad-cli 10.0.8 to scratchpad bbsqw/margay.net)
- RTC1 (DS3231M) VCC pin 2 on 3V3_AUX; VBAT pin 6 on Net-(BT1-+) with BT1, C19, C20, D4.C (D4 BAT43WS anode on 3V3: the v3.1 change, per #70).
- RTC_INT = RTC1.3 (SQW) and U1.42 PB2/INT2 only: no external pull-up (confirmed). MCU INPUT_PULLUP supplies the only pull-up, to always-on 3V3.
- RTC1 RST pin 4 unconnected; 32KHZ unconnected.
- U3 TPL5010: VDD on 3V3, DONE = WD_HOLD (PC7), RSTN -> MCU RESET, WAKE unconnected. R10 on DELAY. So the watchdog RESETS the MCU if not fed; it does not wake it.
- SCL pull-up R16 10k and SDA pull-up R15 10k both to 3V3_AUX (no back-feed from always-on 3V3 via I2C pull-ups). Other 3V3_AUX parts: BME280 U12, MCP342x U14, U4 SN74LVC1G3157, U13 MAX6070, U5, U7, J1 (SD), J2.
### F5. Project-Margay #70 (gh issue view 70, OPEN): keeps VCC on 3V3_AUX; D4 holds VBAT ~3.1 V from 3V3. The clock still selects VBAT whenever 3V3_AUX < VPF, so the INT/SQW battery-mode question is unchanged by #70.
### F6. STRONGEST SOURCE: Maxim errata sheet 19-5311 Rev 0 6/10, "DS3231M Revision A1 Errata" (analog.com ds3231ma1.pdf; live site timed out, retrieved from Wayback snapshot 20240806225820, saved scratchpad bbsqw/dl/e.pdf)
- "This errata sheet only applies to DS3231M revision A1 components. Revision A1 components are branded on the topside of the package with a six-digit code in the form yywwA1"
- Item 2 "BBSQW BIT FUNCTION IS NOT IDENTICAL TO DS3231 / Description: DS3231 BBSQW bit (if = 1) enables SQW when operating on VBAT supply. DS3231M BBSQW bit (if = 1) enables SQW and RTC alarm interrupt when operating on VBAT supply. Workaround: Write BBSQW = 1 if user desires an RTC alarm interrupt during battery operation."
- Item 1: CONV does not auto-clear on A1 ("Only write CONV bit to logic 0"). Relevant: DS3231_Logger begin() writes 0x24 (CONV=1).
- Reading: listed as an erratum (A1 "performs differently than expected"), so the intended behavior (DS3231, and DS3231M other than A1) is that the alarm interrupt asserts on VBAT with BBSQW = 0; on A1 it does not. Local datasheet is 19-5312 Rev 5 7/13, which does not fold this in.
### F7. Arduino forum thread 334435 "DS3231 - No Alarm when powered Off. Why?" (fetched via Discourse JSON, pages 1-5)
- MEASURED, DS3231 (ZS-042), jboyton #22/#24 2015-09-11: alarm at seconds = 0, "pulled the plug and set Vcc=Gnd ... The line went low even with Vcc=0." "I left BBSQW=0." Pull-up to Vcc (#26). Self-described as "Just one test. Repeated several times."
- MEASURED, DS3231 ZS-042, guix #29/#54: failure was the module's on-board pull-up resistor pack to the switched Vcc acting as a pull-down; after removing RP1 and enabling MCU pull-up "the RTC running on battery correctly awakes my arduino with its alarm". (guix had BBSQW=1 set, #23.)
- OPINION (wrong, retracted): guix #5 "the DS3231 does not check alarms when running on battery" then "Sorry I was completely wrong".
- MEASURED, DS3231M rev A1 (date code 1123A1), amazed #78/#81/#85 2020-05: alarm stopped when Vcc removed with BBSQW=0, pull-ups OK; cites erratum; recommends BBSQW=1 for A1. Whether BBSQW=1 then worked is not stated explicitly in the posts read (UNVERIFIED).
### F8. Cave Pearl Project (Ed Mallon), via WordPress.com public API search, DS3231 (SN modules), not DS3231M
- 2014-05-21 "using-a-cheap-3-ds3231...": "according to the datasheet , Bit 6 (Battery-Backed Square-Wave Enable) of control register 0Eh, can be set to 1 to force the wake-up alarms to occur when running the RTC from the back up battery alone ... I have tested this and it seems to work fine" (tested WITH BBSQW=1; no BBSQW=0 control reported).
- 2015-11-05 build part 4 and 2019-01-11 EDU v2: same advice, "provided you set the Battery-Backed Square-Wave Enable bit".
- 2024-10-22 GPS/aging-offset post: "The BBSQW battery power alarm enable (bit 6 of the 0x0E register) must be set when running the RTC on Vbat." Stated as practice; no BBSQW=0 failure measurement given in the passages found.
- 2014-06-09 bench-power post: same datasheet-based statement. So Cave Pearl is a practice/opinion source for BBSQW=1, not a measurement that BBSQW=0 fails.
### F9. ATmega1284P wake from power-down (Microchip DS40002070B, local text scratchpad avcc/txt/...40002070B.txt, lines 3766-3770 and 2663-2667)
- "Low level interrupts and the edge interrupt on INT2:0 are detected asynchronously. This implies that these interrupts can be used for waking the part also from sleep modes other than Idle mode."
- Power-down: "Only an External Reset, a Watchdog Reset, a Brown-out Reset, two-wire Serial Interface address match, an external interrupt on INT2:0, or a pin change interrupt can wake up the MCU." Table 10-1 has no "level only" footnote for INT2:0.
- So the brief's premise (only LOW level on INT2 wakes) does not hold for the 1284P (that restriction is the ATmega328P's INT1:0). FALLING on INT2 is a documented power-down wake source.
### F10. The clock really is on VBAT in sleep (NW-Status/QUEUE.md line 1331, Andy's measurement, not re-measured here)
- "Margay sleeps at about 1.6 uA measured (Andy): the MCU in power-down, the TPS79733's 1.2 uA, the TPL5010's 35 nA, and the whole 3V3_AUX rail switched off by the TPS22916."
- DS3231M ICCS on VCC is 130 uA max at 3.63 V (datasheet line ~112): a VCC-powered clock could not hide inside 1.6 uA. So no back-feed is holding 3V3_AUX above VPF; the clock runs from VBAT (IBATT 2 typ / 3.0 max uA at 3.63 V, EN32KHZ = 0).
### F11. Watchdog cannot be the source of interval logging
- TPL5010 RSTN -> MCU RESET, WAKE unconnected (netlist). Period 2110 s (v2.x) / 3853 s floor (v3.0) per Margay.cpp. A reset re-runs begin() and opens a new file (initLogFile on _newLog). Starved of RTC alarms, a logger would write one row per new file every ~35 or ~64 min, not rows at the set interval in one file.

## Sources checked (incl. dead ends)
- Local DS3231M datasheet 19-5312 Rev 5 7/13 (icreq/txt/ds3231m.txt): used.
- analog.com ds3231ma1.pdf: live fetch timed out (curl HTTP/2 error, then 90 s timeout; WebFetch 60 s timeout); wcm-cce.cldnet.analog.com mirror: connection refused. Wayback 20240806225820: retrieved (dl/e.pdf). Used.
- Arduino forum 334435 pages 1-5 (Discourse JSON; HTML page returned 403 to WebFetch): used. Threads 527951 (ZS-042) and 1095762 downloaded (dl/z.json, dl/y.json) but not read in detail: search-summary claims from them are UNVERIFIED.
- Cave Pearl Project via public-api.wordpress.com search (site's own wp-json and ?s= returned 404 page): used.
- DS3231 (non-M) datasheet: NOT fetched directly. Its BBSQW wording is known here only as quoted in forum 334435 #15: "When BBSQW is logic 0, the INT/SQW pin goes high impedance when VCC < VPF." (the same as the DS3231M's). UNVERIFIED against the PDF.
- ADI EngineerZone, EEVblog: not searched specifically (time); no entries.
- ATmega1284P DS40002070B local text: used.
- Margay_Library, Margay_Library-Wickert-Local-cached20241227, NW_Logger @000ffce, DS3231_Logger (3 copies), Project-Margay KiCad netlist, Project-Margay #70, NW-Status QUEUE.md: used.

## Answer
On the datasheet text alone the case is ambiguous. Maxim's own A1 erratum settles the intent: only revision A1 needs BBSQW = 1 for an alarm interrupt on VBAT; it lists that as a deviation from the DS3231, whose BBSQW gates only the square wave. So on DS3231 and non-A1 DS3231M parts, with INTCN = 1 and A1IE = 1, the alarm match DOES pull INT/SQW low on VBAT with BBSQW = 0. The deployed loggers logging at their interval with 3V3_AUX switched off (1.6 uA floor) is consistent with this and is itself field evidence for the parts Margay uses. The watchdog cannot produce it.

## Recommendation
Set BBSQW = 1 in every control write (0x24 -> 0x64, 0x05 -> 0x45, 0x06 -> 0x46). With INTCN = 1 there is no square wave to enable, so on non-A1 parts the bit should be a no-op (inferred from the erratum, not bench-measured); no extra VBAT current is specified for it (IBATT conditions name only EN32KHZ). It makes the board immune to A1 parts and to the literal reading of the datasheet, and it is Cave Pearl's long-standing practice on VBAT-run DS3231 loggers. #70 does not change this: VCC stays on 3V3_AUX, so the clock still selects VBAT in every sleep; #70 changes only what supplies VBAT. A bench check worth doing once: scope RTC_INT on a Margay in sleep with BBSQW = 0 and = 1, and read the DS3231M top mark for a yywwA1 date code.

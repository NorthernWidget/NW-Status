# NW-Sim: the DS3231M on the switched 3V3_AUX rail (Margay v3.0)

COMPLETE

Agent report, 2026-11-10. Work in NW-Sim only, starting at HEAD 8212170.

## Sources checked

- DS3231M datasheet, Maxim 19-5312 Rev 5 7/13 (the "ds3231m_sparkfun.pdf" in the session scratchpad; page 1 footer reads "19-5312; Rev 5; 7/13", title "DS3231M ±5ppm, I2C Real-Time Clock", 20 pages). It IS the DS3231M datasheet. Copied durably beside this report as `2026-11-10-ds3231m-datasheet-19-5312.pdf` (sha256 2b81f145df39529b936dc63d7401e7dc98d9fe6144b269533613b834c3843cfd). Read as pages 1-16 with Read/pages.
- DS3231M Revision A1 Errata, Maxim 19-5311 Rev 0 6/10 (retrieved by the BBSQW agent from the Wayback Machine; scratchpad bbsqw/dl/e.pdf). Copied as `2026-11-10-ds3231m-a1-errata-19-5311.pdf` (sha256 530ce44dbb792a27dd350f59e352bf8531eb34656c3cb84ee3a7e36e19082abe). Read whole (2 pages).
- Project-Margay at a8a4a6f, Hardware/KiCAD/Margay.kicad_sch (title block rev "2.2"), exported with kicad-cli 10.0.8 to scratchpad rail/margay.net.
- Background, treated as hypotheses: 2026-11-10-ds3231m-bbsqw-agent-report.md.

## Datasheet findings

All quotes from 19-5312 Rev 5, read as page images.

- D1, timekeeping continues on VBAT. p.10, Operation: "Once the oscillator is running, it continues to run as long as a valid power source is available (VCC or VBAT)". p.9, Power-Supply Configurations: "When VCC is greater than VPF, the device is powered by VCC. When VCC is less than VPF but greater than VBAT, the device is powered by VCC. If VCC is less than VPF and is less than VBAT, the device is powered by VBAT" (sentence runs onto p.10). VPF = 2.45 / 2.575 / 2.70 V min/typ/max (p.3).
- D2, I2C stays accessible on VBAT, at the chip. p.10, I2C Interface: "The I2C interface is accessible whenever either VCC or VBAT is at a valid level." Table 1 (p.9) lists IBATA, "I/O ACTIVE", for VCC < VPF and VCC < VBAT.
- D3, INT/SQW on VBAT. p.13, Control register bit 6: "BBSQW: Battery-backed square-wave enable. When set to logic 1 with INTCN = 0 and VCC < VPF, this bit enables the 1Hz square wave. When BBSQW is logic 0, INT/SQW goes high impedance when VCC falls below VPF. This bit is disabled (logic 0) when power is first applied." The second sentence carries no INTCN condition. Read literally: with BBSQW = 0 the pin is high impedance on VBAT whatever INTCN, A1IE and A1F are, so an alarm cannot pull it low. BBSQW = 1 with INTCN = 1 is not addressed by any sentence about VBAT; the INTCN sentences (p.7 pin 3; p.13 bit 2) carry no VCC condition, which reads as: the alarm drives the pin.
- D4, alarm flags on VBAT. p.13, INTCN: "The corresponding alarm flag is always set regardless of the state of the INTCN bit." p.12, Alarms: "The match is tested on the once-per-second update of the time and date registers." Nothing in the document makes the flag conditional on the supply. The model keeps setting A1F/A2F on VBAT.
- D5, power-up defaults are for FIRST power only. p.10: "On the first application of VCC power, or (if VBAT powered) when a valid I2C address is written to the device, the time and date registers are reset to 01/01/00 01 00:00:00" (this paragraph is about the oscillator's first start: "the first time VBAT is applied to the device the oscillator does not start up until VCC exceeds VPF or until a valid I2C address is written"). p.13: EOSC, BBSQW, A2IE, A1IE are "disabled (logic 0) when power is first applied", INTCN "set to a logic 1 when power is first applied". With the coin cell holding VBAT, VCC returning is not a first application: registers are kept, and nothing sets OSF (p.15 lists OSF's causes; VCC loss with VBAT valid is not among them).
- D6, VCC returning. p.10: tREC (250 ms typ) holds RST low after VCC rises; "Assertion of the RST output, whether by pushbutton or power-fail detection, does not affect the device's internal operation." RST is unconnected on the Margay (netlist below). Nothing delays I2C or INT on VCC return.
- D7, temperature on VBAT. p.10 and p.16: conversions once every 10 s on VBAT instead of once a second. The model serves a fixed temperature, so this does not change anything the model does today; recorded, not modeled.
- D8, errata 19-5311 item 2 (rev A1 parts only, top mark yywwA1): "DS3231 BBSQW bit (if = 1) enables SQW when operating on VBAT supply. DS3231M BBSQW bit (if = 1) enables SQW and RTC alarm interrupt when operating on VBAT supply. Workaround: Write BBSQW = 1 if user desires an RTC alarm interrupt during battery operation." The A1 behavior it describes is the SAME as the literal datasheet reading D3. The erratum implies, without saying, that a non-A1 DS3231M (like the DS3231) would raise the alarm on VBAT with BBSQW = 0; the Rev 5 datasheet, written three years after the erratum, still says high impedance. This is the one ambiguity: see the open questions.

## Board (netlist) findings

From the Project-Margay a8a4a6f netlist export:

- B1. RTC1 (DS3231M) pin 2 VCC is on 3V3_AUX. 3V3_AUX is U7 (TPS7A05) VOUT; U7 EN is net 3V3_AUX_CTRL = U1 pin 25, PC6, which is PIN_AUX_3V3 in the model.
- B2. RTC1 pin 6 VBAT is on Net-(BT1-+): BT1 (coin cell), C19, C20, and D4 cathode (D4 anode on 3V3).
- B3. RTC_INT = RTC1 pin 3 (SQW) and U1 pin 42 (PB2/INT2) ONLY. No external pull-up. The only pull-up is the MCU's internal one, on always-on 3V3, which the firmware enables (INPUT_PULLUP, per the BBSQW report's F2, not re-read here). When the clock releases the pin, high-Z on VBAT included, the line idles high. The model already holds the released line high, so this needs no change.
- B4. I2C: SCL (R16 10k to 3V3_AUX) goes to RTC1 pin 8 directly. RTC1 pin 7 SDA is on SDA_OB, which reaches the MCU's SDA only through U4 (SN74LVC1G3157, VCC on 3V3_AUX, select S = SDA_CTRL = PC5, the I2C_SW pin); SDA pull-up R15 10k is also on 3V3_AUX. So with 3V3_AUX off the clock's SDA is behind an unpowered analog switch with no pull-ups, and with the switch on external the clock is off the MCU's SDA altogether, on BOTH v3.0 and v3.1. This is a board fact the model does not represent today (update_buses() leaves the clock reachable in both cases); it is not a clock_on_aux fact, so it is not part of this change. See the open questions.
- B5. RTC1 pin 1 32KHZ and pin 4 RST unconnected.

## Model and tests

- T0, before any change (NW-Sim 8212170, build/nw_sim as built): tests/run.sh margay-3.0 OK=19 exit 0; margay-3.1 OK=19 exit 0; in_the_loop margay-3.0 OK=2, margay-3.1 OK=2; usi_conformance ok=12; chip_conformance ok=23.
- M1, the part (src/parts/ds3231.c/.h): new `ds3231_set_vcc(p, powered)` and `on_vbat` state. On VBAT the part keeps time, keeps setting A1F/A2F, keeps answering I2C, keeps every register; INT/SQW is forced released (high impedance) when BBSQW = 0, and driven by the alarm as on VCC when BBSQW = 1 and INTCN = 1. VCC returning re-evaluates INT at once (a set flag pulls it low). The 1 Hz square wave (INTCN = 0) is not modeled on either supply, as before.
- C1, conformance (tests/chip_conformance/check.c, 11 new checks, drives the part with simavr TWI messages into its own input and reads INT where the board reads it): with the VBAT line removed from the part (scratch copy), 2 checks FAIL ("an alarm match leaves INT/SQW released": expected 1, got 0; "VCC falls below VPF and the pin goes high impedance": expected 1, got 0). With BBSQW ignored (always high-Z on VBAT), "an alarm match pulls INT/SQW low" FAILS (expected 0, got 1). Against HEAD's part the check does not link (no ds3231_set_vcc). With the change: all pass.
- M2, the board (src/boards/margay.c): clock_on_aux = 1 calls ds3231_set_vcc on every 3V3_AUX change, and starts the clock on VBAT because the rail starts off (aux_rail_on = 0 until PC6 drives it, as the model already assumed for the BME280). clock_on_aux = 0 (margay-3.1) never calls it.

## Open questions for Andy
- T1, part change + conformance (build with the part only, board not yet calling it): run.sh margay-3.0 OK=19, margay-3.1 OK=19; in_the_loop 2 + 2; usi ok=12; chip ok=34 (23 + 11). Committed 6709b71 (part) and 4184051 (check).
- T2, board change built: run.sh margay-3.0 OK=19, exit 0: NO margay-3.0 baseline moved. Cause, from a verbose margay_basic run on margay-3.0 with today's DS3231_Logger (4179b06): the control register is written 0x64 at boot and 0x45 at each alarm (BBSQW set), the clock goes to VBAT at every sleep ("ds3231: VCC off, running on VBAT (BBSQW 1)"), and all 4 "INT low (alarm)" events of the run occur while the rail is off, i.e. on VBAT. So the logger wakes on a VBAT alarm, as the datasheet allows with BBSQW = 1. Transcript byte-identical to the baseline.

## BBSQW demonstration (DS3231_Logger 2d6925b, not committed)

Scratch workspace: every repository symlinked except DS3231_Logger, exported with `git archive 2d6925b` (scratchpad rail/ws_2d6925b). Built Margay_Library/examples/Basic, run 25 s on margay-3.0 with the committed model.

- X1, with the simulator as committed: the transcript is byte-identical to the margay_basic baseline (5 rows). The control register is 0x24 at boot and 0x05 at each alarm (BBSQW = 0). The parts log shows WHY it still logs, and it is not the clock waking it: on VBAT the alarm sets A1F but INT stays released; every "INT low (alarm)" (4 of them) comes right after "ds3231: VCC on", i.e. when the firmware has ALREADY woken and switched 3V3_AUX back on. The simulated MCU never stays asleep: 293 "aux rail off" events in a 25 s run with 4 logged intervals (head build), because simavr has no sleep-mode model and any enabled interrupt wakes the core (simavr sim_interrupts.c: a raised, enabled vector sets `avr->state = cpu_Running` whatever the sleep mode). A timer interrupt is what wakes it: masking TIMSK0-3 during power-down (X2) stops the wakes. Which timer was not isolated; Timer0's overflow, which drives millis(), is the likely one (UNVERIFIED). On an ATmega1284P in power-down Timer0's clock is stopped and cannot wake it (Microchip DS40002070B power-down wake sources, as quoted in the BBSQW report F9: external reset, watchdog, brown-out, TWI address match, INT2:0, pin change; not re-read here).
- X2, scratch experiment (scratchpad rail/pd, a copy of src/nw_sim.c that masks TIMSK0-3 while SMCR selects power-down and restores them once the core runs; NOT committed): with today's DS3231_Logger, margay-3.0 and margay-3.1 both log 5 rows, power-down entered 5 times, INT low 4 times, and the margay-3.0 transcript is byte-identical to the margay_basic baseline. With DS3231_Logger 2d6925b: margay-3.1 logs 5 rows (clock on VCC); margay-3.0 logs ONE row (00:00:01 LoggingStarted), enters power-down once, sees INT low 0 times, and never wakes again: the rail goes off at parts-log line 1630 and never comes back. The TPL5010 that would reset it on hardware is not modeled.
- Answer: with the datasheet-nominal DS3231M (literal reading of p.13), a v3.0 Margay running DS3231_Logger without BBSQW does NOT wake on its alarm; with BBSQW (4179b06) it does. The committed model alone cannot show this in a transcript, because the simulated core does not really sleep; that is a separate simulator gap (see open questions).

## Further measurements

- F1. No clock I2C traffic happens while 3V3_AUX is off: 0 "ds3231: selected" lines between "aux rail off" and "aux rail on" in the margay_basic verbose run, with today's DS3231_Logger and with 2d6925b. So whether the clock is reachable on VBAT (datasheet: yes at the chip; board: SDA behind U4 on 3V3_AUX and both pull-ups on 3V3_AUX, so in practice no) does not affect any current case.
- F2. The clock IS read with the bus switch on EXTERNAL: 20 "ds3231: selected" lines while "margay: I2C bus external" in the same run, e.g. parts-log lines 1263-1279: temperature 0x11-0x12, then time 0x00-0x06, between "I2C bus external" and "I2C bus internal". The source is Margay::addDataPoint() (Margay_Library src/Margay.cpp: `switchExternalI2C(ON); readSensors(); farmGateI2C(...)`). SN74LVC1G3157 Rev. O, Table 7-1 (Function Table, read from pdftotext -layout of the scratchpad copy, not as a page image): control L -> B1 on, H -> B2 on. In the netlist U4 B1 = SDA_OB (the clock, BME280, MCP3421) and B2 = SDA_EXT, S = PC5, and the firmware drives PC5 HIGH for external. On that reading the clock's SDA is disconnected from the MCU while the row's timestamp and RTC temperature are read. Field loggers log sensible times, so something in that chain does not hold on real boards (the KiCad conversion's B1/B2, the switch polarity, or the firmware's reading point). Not modeled, not chased; flagged for Andy.

## Commits (NW-Sim, local only, nothing pushed)

- 6709b71 ds3231: the DS3231M on its backup battery, behind ds3231_set_vcc()
- 4184051 chip_conformance: the DS3231M on VBAT, against its datasheet
- 52c7fdb Margay model: on a v3.0 the clock runs on its coin cell while 3V3_AUX is off
- 9eb2951 README, CLAUDE.md: the clock's coin cell on a v3.0, and its conformance checks
- 7324ae5 README: a simulated core never stays asleep

Final suite counts (code at 52c7fdb; the two later commits are README/CLAUDE.md only): run.sh margay-3.0 19 OK, margay-3.1 19 OK; in_the_loop margay-3.0 2 OK, margay-3.1 2 OK; usi_conformance 12 ok; chip_conformance 34 ok (23 before plus 11 DS3231M). No baseline re-recorded on either board.

## Open questions for Andy

1. BBSQW = 0 on VBAT for non-A1 DS3231M parts. The model follows the Rev 5 datasheet literally (high impedance, no alarm on the pin), which is also what errata 19-5311 says of rev A1. The erratum implies other revisions alarm on VBAT with BBSQW = 0 (as the DS3231 forum measurement in the BBSQW report suggests for the DS3231). If you want that reading available, it is a one-line option in ds3231_update_int(); not built, because it is not in the datasheet. A rev A1 option is unnecessary: A1 behaves as the literal datasheet already modeled.
2. The simulated core never stays asleep (X1). Model power-down properly (an ATmega1284P sleep-mode model, with its own conformance check from the 1284P datasheet)? The scratch masking left today's margay_basic transcript byte-identical on margay-3.0, which suggests the baselines would survive it, but only margay_basic was tried. Until then a transcript cannot show a logger failing to wake on its clock.
3. F2: the clock read with U4 on the external side. Which of netlist, switch polarity or firmware is wrong?
4. The TPL5010 (U3, RSTN to MCU reset) is not modeled, so a logger that misses its alarm sleeps forever in the simulator rather than resetting.
5. The rail is taken to start off at power-up (as the model already assumed for the BME280); U7 EN on PC6 has no external resistor in the netlist, and whether TPS7A05's EN has an internal pull-down was not checked.
6. The 1 Hz square wave (INTCN = 0, on VCC or with BBSQW on VBAT) is not modeled; no current firmware uses it.

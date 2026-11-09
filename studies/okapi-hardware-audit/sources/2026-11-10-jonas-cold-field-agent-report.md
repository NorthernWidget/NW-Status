COMPLETE

# Margay clock failures in the cold: field-practice candidates

Scope: the built Eagle design (netlist `scratchpad/rtc/eagle.json`), the 2024 Margay library
(`Margay_Library-Wickert-Local-cached20241227/src/Margay.cpp`), the DS3231_Logger driver at commit
`850dfbf` (2022-09-18, the last commit before 2026, so the version a 2024 build used), the
NorthernWidget board package 0.3.1, and the datasheets in the scratchpad. I read Project-Margay
README.md and the 2022 Operations Guide for field procedure. The README's "Cold-weather deployments"
paragraph is earlier analysis, so I did not use it as evidence.

## 1. The power facts everything below depends on (verified from netlist and code)

Where the parts get their power (Eagle netlist):
- RTC1 DS3231M: VCC pin 2 is on **3V3_AUX**, and VBAT pin 6 is on **VCOIN+** = BT1 (+) and C19 (0.1 uF). Nothing else is on VBAT.
- 3V3_AUX comes from U7 TPS7A05 (EN = 3V3_AUX_CTRL = PC6 = D22). U7 also feeds the I2C pull-ups R15/R16, the SD card, BME280, MCP3421, MAX6070, and J2 pins 2 and 8.
- U7 VIN = VMAIN = U9 TPS2104 OUT. U9 IN1 = VBAT_SW (U8 TPS22916 output, EN = VBAT_SW_CTRL = PC3 = D19). U9 IN2 = VUSB. U9 EN = U10 TLV3691 output (IN+ = 3V3_FTDI, IN- = VBAT_SW/2 via R17/R18).
- MCU 3V3 = U6 TPS79733, fed from VBAT+ (J3 pin 4). VBAT- (J3 pin 3) returns through Q1 DMG3404L (gate on VBAT+), the reverse-polarity FET.
- With USB: VUSB feeds U9 IN2, feeds FT231X VCC through D1 BAT43WS, and turns Q3 on, which turns Q2 on and ties 3V3_FTDI (the FT231X 3V3OUT) to the MCU 3V3 rail.

Pin mapping checked against `variants/NW1284p/pins_arduino.h`: with `model_ == 2` the constructor sets
`Ext3v3Ctrl = 22` (PC6, U7 EN), `BatSwitch = 19` (PC3, U8 EN), `RTCInt = 2` (PB2 = RTC_INT), `LogInt = 28` (PA4), `WDHold = 23` (PC7) and `I2C_SW = 21` (PC5). All match the netlist.

What the firmware does every sleep (`Margay.cpp`, `sleepNow()` -> `turnOffSDcard()`):
`powerAux(OFF); //turn off external 3v3 rail` then `powerOB(OFF); //Turn off battery connection to sense divider`.
U7 goes off, and so does the RTC's VCC. The 2024 build fits U7 as TPS7A0533**P**DBVR (KiCad netlist MPN; evidence.md says the MPNs match the built boards). The P suffix means "an active output discharge feature" (TPS7A05 datasheet 11.1.2), a 120 ohm pulldown (7.3.2).
**Result: on these boards the CR1220 is the RTC's only supply for the whole of every sleep, and for every hour the battery pack is off.** It is not a backup that only matters in an outage.

How the two supply routes differ:

| | Battery terminal J3 | USB cable spliced to the D cells |
|---|---|---|
| MCU 3V3 | U6 TPS79733 from VBAT+ | FT231X 3V3OUT (50 mA) through Q2 |
| Ground return | through Q1 | straight to J4 GND, bypassing Q1 |
| VMAIN source | U9 IN1 = VBAT_SW, which U8 switches **off every sleep** (TPS22916C quick discharge, 150 ohm) | U9 IN2 = VUSB, **never switched off** |
| U7 (TPS7A05) VIN during sleep | collapses | stays up |
| RTC VCC during sleep | off | off (U7 EN is still low) |
| RTC VBAT | CR1220 | CR1220 (no change) |
| BAT_SENSE | real value | 0 V, because VBAT_SW = 0. `batTest()` then sets BatError and the STAT LED flashes red 10x at startup |
| Firmware path | identical. The library has no USB detection | identical |

**The USB splice does not change what powers the clock during sleep.** A USB cure therefore has to
act through (a) U7's input no longer collapsing, (b) the different connector, ground path and MCU
regulator, or (c) something else done at the same visit.

DS3231_Logger at 850dfbf (verified):
- `begin()` writes Control 0x0E = 0x24 (`//Start oscilator, turn off BBSQW, Turn off alarms, turn on convert`).
- `setAlarm()` writes 0x0E = 0x05 (INTCN + A1IE) or 0x06, and Status 0x0F = 0x00.
- `clearAlarm()` writes 0x0F = 0x00 (`//Clear all flags`).
- OSF (Status bit 7) is never read and is cleared on every alarm. **An oscillator stop during sleep is wiped without a report.**
- BBSQW is always 0. The DS3231M datasheet: "When BBSQW is logic 0, INT/SQW goes high impedance when VCC falls below VPF." Read literally, the alarm could not wake the MCU during sleep. Margays do wake in service, so either the DS3231M does assert the alarm from VBAT with BBSQW = 0, or I have misread the sleep rail. UNVERIFIED; a scope on INT/SQW settles it (test T3).

Wire: the NW1284p platform carries its own `libraries/Wire` (old twi.c, no timeout), which takes
precedence over the core's 1.8.6 Wire. A bus that never becomes free hangs the MCU in
`while(...)` loops. Recovery is the TPL5010 watchdog (U3, R10 = 130 k). By TPL5010 Table 3,
130 k lies between 124.91 k (1 h) and 149.39 k (1 h 30 min), so about 1 h 06 min. That is my
interpolation; the README says "approximately 36 minutes". UNVERIFIED which one is right.

## 2. What "the clock failed" could have looked like (derived from the 2024 code)

A field team sees one of these. Each points to a different mechanism, and Jonas can say which it was.

| What the team saw | Code path | Mechanism class |
|---|---|---|
| STAT **cyan** at power-on | `clockTest()`: `YearNow == 00` -> TimeError | RTC lost all power (POR) at some point: time reset to "01/01/00" (DS3231M "On the first application of VCC power ... reset to 01/01/00") |
| STAT **red** at power-on, serial "Clock: FAIL" | I2C write to 0x68 fails -> OBError | no ACK: RTC VCC rail or pull-ups not up, a hung bus, or a dead part |
| STAT **red**, clock ACKs | seconds unchanged after `delay(1100)` -> OscStop | oscillator not running within 1.1 s |
| Timestamps "2000/01/01 ..." in the log | POR | as cyan |
| Timestamps like "20165/25/45 18:85:85" | `Wire.read()` returns -1 (0xFFFF) and the BCD decode gives 165/25/45/18/85/85 (I worked this through the `getTime()` arithmetic; UNVERIFIED on hardware) | I2C read failure during logging |
| Plausible time, but offset or with gaps | OSF cleared without a report | oscillator stopped during sleep |
| No new rows; a new Log file roughly every hour | alarm never fires, watchdog reboots | RTC POR (alarms disabled at POR), a bad alarm write, or no alarm assertion on VBAT |
| AUX green stays on, nothing further | Wire hang during startup | no pull-ups (3V3_AUX not up) or a stuck SDA |

The email does not say which. **The cheapest test of all is to ask Jonas** for (1) the LED color,
(2) a log file from a failed unit, (3) whether a laptop re-set the time after the cell swap, (4)
the pack's cell count and connector, (5) what "rewire" was actually done, with a photo, and (6)
whether he kept the original coin cells.

## 3. Candidate causes

### C1. A cold (and/or partly used) CR1220 cannot carry the DS3231M through its sleep-time current pulses
- **Mechanism.** On VBAT the DS3231M runs a temperature conversion every 10 s ("When VBAT is the presently selected power source, temperature conversions are executed once every 10s"). Each one draws IBATTC = 575 uA max at 3.63 V and 650 uA max at VBATMAX for tCONV = 10 ms (datasheet, VBAT current table). The only reservoir is C19 (0.1 uF, GCM155R71C104KA55D). It holds a 650 uA load for 0.1 uF x 0.5 V / 0.65 mA = 77 us of the 10 ms, so the cell supplies the pulse itself. To stay above the 2.3 V VBAT minimum from about 3.0 V, the cell's internal resistance must stay below about 0.7 V / 0.65 mA = 1.1 kohm. A cold, small, partly discharged Li-MnO2 cell can exceed that (UNVERIFIED: no CR1220 resistance-versus-temperature data in the pack). A dip gives either an oscillator stop (time lost, OSF wiped by firmware) or a full POR (time = 2000, alarms disabled, so the logger sleeps until the watchdog).
- **Evidence.** Netlist VCOIN+ = {BT1+, C19, RTC1 VBAT}. Every sleep runs `powerAux(OFF)`. DS3231M: VBAT 2.3 to 5.5 V; IBATTC 575/650 uA; conversions every 10 s on VBAT. The later KiCad design adds C20 (1 uF) and D4 (BAT43WS, anode on 3V3, cathode on BT1+/VBAT), which diode-ORs the always-on MCU rail onto VBAT. That is consistent with a supply weakness here, though it does not prove one.
- **Explains.** Cold: yes. Warm-cell cure: yes, but only briefly (see C2). USB cure: **no**, because the coin cell still powers the RTC in sleep on USB.
- **Likelihood.** High as the underlying weakness, because the design makes the coin cell primary rather than backup. It weakens at the 0 °C in the email: Li-MnO2 coin cells are commonly rated to -20 or -30 °C (UNVERIFIED for the fitted brand), and wind cannot cool an unpowered box below air temperature. Only clear-sky radiative cooling can. It is stronger at Andy's recalled -20 °C.
- **Tests.**
  - T1: put a failed unit's original cell, a fresh cell of the same lot, and a BR1220 each in series with a 10 ohm shunt into a board in a freezer at +20, 0, -10, -20 and -30 °C. Scope VBAT pin 6 against ground during sleep. Look for the 10 ms dips every 10 s and their depth against 2.3 V.
  - T1b: on the bench, swap BT1 for a supply with a series resistor (100 ohm to 3 kohm). Find the resistance at which time is lost; that turns the hypothesis into a threshold.
  - Kill condition: VBAT never drops below about 2.5 V at -20 °C with the original cells.

### C2. The cure was a new or reseated cell, not a warm one (depleted or poorly seated coin cell)
- **Mechanism.** (a) Cells may have been partly depleted in storage or shipping (the guide tells operators to switch the pack off for SD swaps and downloads, so the RTC lives on the cell then too). A cell from a pocket is also a *new* cell. (b) BT1 is a 12 mm SMT holder (BAT-HLD-012-SMT); the README says it takes both 2.0 mm 1220 and 2.5 mm 1225 cells, so contact force on a 1220 may be low (UNVERIFIED). Cold contraction and wind vibration could open the contact for milliseconds. With 0.1 uF, VBAT collapses at once under a conversion pulse, causing a POR. Reseating restores contact.
- **Thermal argument against "warm".** A CR1220 weighs under a gram. In a 0 °C wind it returns to ambient within minutes (order-of-magnitude estimate, UNVERIFIED). Any cure that lasted past setup cannot have been the warmth. The startup self-test runs within about 5 s of power-on, so it would see a still-warm cell, but the self-test barely depends on the cell (VCC is up then; see C8).
- **Also inherent in a swap.** Removing the cell while the logger sleeps leaves the RTC with no supply: POR, time 2000, alarms off. Re-inserting it does not start the oscillator ("the first time VBAT is applied ... the oscillator does not start up until VCC exceeds VPF or until a valid I2C address is written"). The swap must therefore have been followed by a re-initialization, and probably a laptop time set, for the clock to "work". **So the warm-cell cure always comes bundled with a full RTC power cycle and a fresh `begin()`**, which also cures C5 and any latched RTC state.
- **Explains.** Cold: partly (contraction, stiffer contacts). Warm-cell cure: yes. USB cure: only if the cell was reseated during the rewire.
- **Likelihood.** Medium-high.
- **Tests.**
  - T2: measure the original cells' open-circuit voltage and their voltage under a 1 mA, 10 ms load at room temperature. Compare with fresh cells.
  - T2b: with a scope on VBAT, tap and vibrate the board at -20 °C. Measure holder contact force or inspect the spring.
  - T2c: put the original cell back in a failed unit and re-run the cold test T1. If a warmed original cell fails as often as a cold one, it is the cell's condition, not its temperature.

### C3. TPS7A05 cold power-cycling on the battery path (TI's below-15 °C caution), worsened by a weak coin cell
- **Mechanism.** TPS7A05 datasheet 8.1.3, "Special Considerations When Ramping Down VIN and Enable": "when the operating free-air temperature is less than 15°C. The minimum ramp-down time for the IN pin is 10 ms. The minimum ramp-down time for the EN pin is 100 us." It warns that a faster VIN ramp gives "a partial startup, shutoff, followed by a normal soft-start startup", and a faster EN ramp gives "a delay time of up to 130 ms". The firmware switches EN with a GPIO, in nanoseconds.
  - On the battery path only, VIN also collapses at every sleep: U8 (TPS22916C, "QOD: 150 ohm") discharges VBAT_SW, and VMAIN (C13, 1 uF) follows through U9's IN1 N-channel body diode (OUT to IN1). That is roughly a sub-millisecond ramp. My estimate, UNVERIFIED; it needs a scope.
  - On the USB path VMAIN stays up through U9 IN2, so the VIN half of the caution never applies.
  - On every wake, 3V3_AUX (RTC VCC and the I2C pull-ups) may therefore glitch or arrive late. Each glitch is a VCC-to-VBAT switchover that a cold, high-resistance coin cell with 100 nF must ride through.
- **Firmware timing.** In `turnOnSDcard()`, `powerOB(ON); powerAux(ON); delay(6); ... delay(10); SD.begin(...)`. The SD card can be initialized before a 130 ms-late rail is up. The first RTC read comes later, after the two `delay(100)` calls in `getBatVoltage()`, so a late rail most directly threatens SD writes. A glitching rail threatens the RTC.
- **Explains.** Cold: yes, and it is active at 0 °C, well inside TI's 15 °C threshold. USB cure: yes, through VIN not collapsing; it is the only candidate with a mechanism for that. Warm-cell cure: yes, if the harm reaches the clock through switchover brown-outs of a weak cell.
- **Likelihood.** Medium-low. Every link is grounded in a datasheet, but nobody has observed the chain, and TI does not quantify "undesired startup behavior" beyond the figures.
- **Tests.**
  - T3: with the board in a freezer at +20 and -20 °C, scope 3V3_AUX (RTC pin 2), VMAIN, VBAT (pin 6) and INT/SQW (pin 3) across a sleep-to-wake cycle, once on J3 and once on the USB splice. Look for a partial start or a delay of 10 ms or more on J3 at -20 °C, absent on USB and absent at +20 °C.
  - T3b, a firmware A/B: keep `powerOB(ON)` through sleep, or ramp EN slowly. If failures stop on J3 in the cold, C3 is confirmed.

### C4. RTC VCC falls faster than the DS3231M's power-switch specification at every sleep (both paths)
- **Mechanism.** DS3231M AC power-switch table: "VCC Fall Time, VPFMAX to VPFMIN, tVCCF, min 300 us". With U7's 120 ohm active discharge on C15 (10 uF nominal, X5R 0805, perhaps 5 to 8 uF at 3.3 V bias, UNVERIFIED) plus loads, the time constant is about 0.6 to 1.2 ms. The time from 2.70 V to 2.45 V is then tau x ln(2.70/2.45), or about 60 to 120 us: 3 to 5x faster than the minimum. Each sleep entry dumps the RTC onto VBAT abruptly, and the cell (and C19) must take the full load instantly.
- **Explains.** Cold: yes, together with C1. Warm-cell cure: yes. USB cure: **no**, because U7 still switches off on USB. The fall may differ between paths, since on J3 U7 also loses VIN; T3 measures this.
- **Likelihood.** Medium as a contributor to C1. It cannot be the sole cause, because it happens identically at room temperature, where loggers work.
- **Test.** Measured in T3: the 3V3_AUX fall time through 2.70 to 2.45 V. A/B test: add 47 to 100 uF on 3V3_AUX, or a resistor in series with the discharge path, then repeat the cold run.

### C5. Battery-terminal wiring in the field: brief supply loss, MCU reset mid-I2C, and an RTC left latched
- **Mechanism.** J3 is a 2.54 mm screw terminal (OSTVN06A150). Field practice puts a D-cell pack on long leads, possibly with a splice, in wind and cold that stiffen insulation. Any interruption collapses U6/3V3 and resets the MCU. The RTC stays alive on VBAT through the reset, so a reset in the middle of a transfer can leave it holding SDA low (DS3231M datasheet: "If a microcontroller connected to the device resets because of a loss of VCC ... I2C communications could become unsynchronized"). The board's Wire has no timeout, so the next `begin()` either hangs (watchdog) or fails `clockTest()` (red).
  - A further risk: extended fuse 0xFE gives BODLEVEL 110, which is 1.8 V brown-out detection (my decoding from the ATmega1284P fuse table, UNVERIFIED here). An 8 MHz ATmega1284P is specified only from 2.7 V up (from memory, UNVERIFIED). During a slow sag the MCU can execute out of specification and write junk to the RTC, for example EOSC = 1, which stops the oscillator on VBAT.
  - **The warm-cell cure clears this**, because removing the cell power-cycles the RTC. **The USB cure avoids it**, because it uses a different connector and ground path (no Q1) and a different MCU regulator.
- **Explains.** Cold: partly (alkaline D-cell resistance rises in the cold, connections loosen). Warm-cell cure: yes, through the RTC power cycle. USB cure: yes.
- **Likelihood.** Low-medium. It explains both cures, but needs flaky wiring on several units.
- **Tests.**
  - T5: inspect the failed units' J3 terminations and pack leads, and run a tug test per the Operations Guide ("gently tugging on the wires").
  - T5b: interrupt VBAT+ for 1 to 50 ms at random times on a bench unit (relay or MOSFET), and count stuck-bus or EOSC outcomes with a logic analyzer on SDA/SCL.
  - T5c: read register 0x0E on a "failed" unit before touching its cell (connect USB and dump the RTC registers). EOSC = 1 or nonsense values confirm it.

### C6. Andy's "USB" recollection may be Jonas's proposed VBAT rewire (D cells to the clock)
- **Mechanism (provenance, not physics).** The written record has Jonas proposing "connect the clock to the D batteries" and, on 29 July, "will decide then if we'll try to rewire the clock". Andy's reply concerned the RTC's 2.3 to 5.5 V range. A D-cell feed into VBAT, replacing the coin cell, would cure C1, C2 and C4 directly. The 2026 memory of "USB spliced into the D cells" is unwritten (evidence.md observation 2).
- **Explains.** All three observations, if that is what was done.
- **Likelihood.** Medium. It is cheap to settle.
- **Test.** Ask Jonas for a photo or description of exactly what was wired, and on which units.

### C7. Condensation or frost, and board leakage at the coin-cell node
- **Mechanism.** Loggers set up or handled in a warm vehicle or tent, then closed and carried into 0 °C wind, collect condensation inside the housing. VCOIN+ is a microamp node: 1 Mohm of surface leakage at 3 V adds 3 uA, doubling IBATT (2 to 3.5 uA), and 100 kohm adds 30 uA. Flux under the SMT holder makes this worse. Warming dries the board.
- **Explains.** Cold/humid conditions: yes. Warm-cell cure: weakly (handling dries the board). USB cure: no.
- **Likelihood.** Low-medium.
- **Test.** T7: with BT1 removed, measure resistance from VCOIN+ to GND with a megohmmeter on a failed unit, dry and after a freezer-to-room condensation cycle. Inspect under BT1 for flux. Measure the cell's sleep current in series (expected about 2 to 3.5 uA; DS3231M IBATT).

### C8. Startup self-test false failure in the cold (MEMS oscillator start versus the 1.1 s test)
- **Mechanism.** After any POR (including a cell swap), `clockTest()` reads the seconds, waits `delay(1100)`, and flags OscStop and red if they have not changed. The datasheet gives only "Typical oscillator startup time is less than 1s"; a slower start in the cold gives a red light on a healthy clock. POR also sets year 00, giving cyan.
- **Explains.** Cold: yes. Warm-cell cure: yes, if they re-powered warmer. USB: no.
- **Likelihood.** Low. It describes a startup indication, not lasting failure.
- **Test.** T8: in the freezer, remove and replace the cell, apply power, and timestamp the first seconds increment over I2C at +20 and -30 °C.

### C9. Wrong source selection by U9 on the battery path (back-powered 3V3_FTDI)
- **Mechanism.** On battery alone, U10 compares 3V3_FTDI (IN+) with VBAT_SW/2 (IN-), and U9 selects IN2 (VUSB = 0 V) whenever EN is high (TPS2104 table: "0V 5V H VIN2" etc.). If the MCU's TX (driven high once `Serial.begin`) back-powers the unpowered FT231X's VCCIO through R9 (330 ohm), 3V3_FTDI can rise. If it exceeds VBAT_SW/2, VMAIN switches to 0 V and 3V3_AUX (RTC VCC) drops while the MCU is awake. The FT231X is "Tolerant of 5V input", which suggests no clamp to VCCIO and argues against this. On USB the comparator state is unambiguous.
- **Explains.** USB cure: yes. Cold: weak (a cold pack lowers VBAT_SW/2). Warm-cell: no.
- **Likelihood.** Low.
- **Test.** T9: on J3 power with USB unplugged, measure 3V3_FTDI and U9 EN (U10 OUT) while the logger is awake and printing. If EN stays at 0 V, C9 is dead.

### C10. Alarm assertion from VBAT with BBSQW = 0 being marginal in the cold
- **Mechanism.** See section 1: the firmware never sets BBSQW, and the datasheet text says INT/SQW goes high-impedance below VPF when BBSQW = 0. If the DS3231M does assert alarms from VBAT anyway (service experience says it must), that behavior is outside the written specification and may depend on VBAT level or temperature. A missed alarm leaves the logger asleep until the watchdog.
- **Explains.** Cold and warm-cell: possibly. USB: no.
- **Likelihood.** Low. UNVERIFIED.
- **Test.** From T3: scope INT/SQW at the alarm time during sleep, at -20 °C, with weak and fresh cells. A/B with BBSQW set (0x0E = 0x45).

### Contributing factor, not a cause: firmware discards the evidence
`clearAlarm()` and `setAlarm()` write Status = 0x00, which clears OSF without reading it. A stop
during sleep therefore leaves no flag, and the next `setAlarm()` computes from a wrong time.
`setAlarm()` also indexes `MonthDay[AlarmTime[5]]` with whatever month was read, which is out of
bounds after a failed read (month 25). Reading and logging OSF in `begin()` and at each wake would
let one deployment tell C1, C2 and C4 apart from the others.

## 4. Confounds between the cures and other changes

1. A coin-cell swap is a full RTC POR, so it implies re-initialization and probably a laptop time set (C2). That one act cures C1, C2, C5 and C8 at once.
2. The new cell was also *fresh*: new versus warm is confounded (C2).
3. A warm cell stays warm only for minutes (C2). A lasting cure cannot be its temperature.
4. The USB rewire happened at a later visit (29 July: "We're going to go to collect the data in a couple of days ... will decide then"). Time of day, weather, re-initialization and reseating all changed with it.
5. The recollection may conflate USB with the proposed D-cell-to-VBAT wiring (C6).
6. The units with problems were "some of them": a unit effect (cell lot, holder, solder or flux, U7 or U8 parts) is as plausible as temperature.
7. Temperature: the email says about 0 °C, Andy recalls about -20 °C. C1 strengthens sharply between those; C3 is active at both.

## 5. One bench session that separates most of these

Use Jonas's failed units with their original cells, plus one good unit. A freezer to -30 °C; a
4-channel scope on RTC pins 2 (VCC), 6 (VBAT) and 3 (INT/SQW) and on VMAIN; a 10 ohm shunt in
series with BT1; a 60 s logging interval.
- Run 1, J3 versus USB at +20 °C: baseline.
- Run 2, J3 versus USB at -20 °C with the original cells: C1 shows VBAT dips at 10 s intervals on both paths. C3 shows a 3V3_AUX start anomaly on J3 only. C4 shows a fast VCC fall. C10 shows no INT on alarm.
- Run 3, -20 °C with a fresh cell and with a BR1220: separates new from warm (C1 versus C2).
- Run 4, -20 °C with VBAT fed from a bench supply (the C6 rewire): if all failures vanish, the fault lives on the VBAT node (C1, C2, C4, C7).
- Before any of this, dump RTC registers 0x00 to 0x12 on each failed unit as received (C5).

---

**Summary.** The design makes the CR1220 the clock's only power for every sleep and every hour
the pack is off. The firmware turns off the clock's 3.3 V rail each sleep, and the clock's
current pulses (up to 650 uA for 10 ms every 10 s) fall on the coin cell with only 0.1 uF of
help. A cold or partly used cell (C1), helped by the clock's supply falling faster than its
specification (C4), is therefore the leading explanation for the cold failures and the
warm-cell cure. A new or reseated cell (C2) explains that cure at least as well, because a
warm coin cell cools in minutes and every swap power-cycles and re-initializes the clock. The
USB splice does not change what powers the clock during sleep. Only TI's below-15 °C caution on
the TPS7A05 (C3) gives it a direct mechanism, because on USB the regulator's input never
collapses. Otherwise the USB cure is a confound, or a memory of the D-cell-to-clock rewire
Jonas proposed (C6). Ask Jonas what he saw and wired, then run one freezer session with a scope
on the clock's VCC, VBAT and INT pins on both supply routes.

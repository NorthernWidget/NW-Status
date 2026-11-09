COMPLETE

# Margay cold clock failure: circuit-first analysis

Sources used: Eagle netlist JSON (scratchpad/rtc/eagle.json, the built design), KiCad XML (scratchpad/bomlines/margay2.xml, for MPNs only), Margay library at Margay_Library-Wickert-Local-cached20241227/src/Margay.cpp (working tree, which differs from its HEAD 8e1b83c by a small uncommitted diff), NW1284p variant pins_arduino.h and boards.txt from the board package 0.3.1, and the datasheets in the scratchpad. Pin numbers below are checked against pins_arduino.h (D2=PB2, D19=PC3, D21=PC5, D22=PC6, D9=PD1).

## 1. Net-by-net trace (verified from eagle.json)

### DS3231M (RTC1, MPN in KiCad BOM: DS3231MZ+, rated -45 to +85 C)
| RTC1 pin | Net | Everything else on the net |
|---|---|---|
| 2 VCC | 3V3_AUX | U7 TPS7A0533P VOUT; C15 10 uF, C16 0.1 uF; R15, R16 (I2C pull-ups); U4 VCC (SDA switch); U5 VCC (SD buffer); J1.VDD (SD card); U12 BME280; U13 MAX6070; U14 MCP3421; J2.2, J2.8 (screw terminal 3V3 out); JP2.3 |
| 6 VBAT | VCOIN+ | BT1.+ (CR1220), C19 0.1 uF. Nothing else: no series diode, no bulk capacitor (the KiCad C20 and D4 are not on the built boards) |
| 5 GND | GND | common ground; note J4 (USB) GND is GND directly, while J3 battery negative (VBAT-) reaches GND only through Q1 DMG3404L (low-side reverse-polarity NMOS, gate = VBAT+) |
| 8 SCL | SCL | U1 PC0 directly; R16 10k to 3V3_AUX; U12, U14; J2.10 (off-board SCL, no isolation) |
| 7 SDA | SDA_OB | U4 B1 (SN74LVC1G3157 SPDT switch powered from 3V3_AUX); U12, U14; JP1.1 (open). MCU SDA reaches SDA_OB only through U4; the only SDA pull-up (R15) is on the MCU side of U4 |
| 3 INT/SQW | RTC_INT | U1 PB2 (INT2) only. No external pull-up: the firmware's `pinMode(RTCInt, INPUT_PULLUP)` (Margay.cpp line 268) is the only pull-up, to the MCU 3V3 rail |
| 4 RST, 1 32KHZ | not in the netlist | The Eagle symbol has only six pins; RST and 32KHZ are unconnected. Datasheet allows both open (RST has an internal 50k pull-up to VCC) |

### Power paths
- **Battery terminal J3.4 (VBAT+)** feeds two things directly: U6 TPS79733 (VIN, always on, makes the MCU rail 3V3, PG to PC2) and U8 TPS22916C (VIN). U8 EN = VBAT_SW_CTRL = PC3 (D19, `BatSwitch`). U8 VOUT = VBAT_SW, which goes to (a) the battery-sense divider R22/R23, (b) comparator divider R17/R18 (10k/10k) to U10 IN-, and (c) U9 TPS2104 **IN1** (the 250 mOhm NMOS, gate from an internal charge pump).
- **USB J4.VBUS (VUSB)** feeds: U9 TPS2104 **IN2** (1.3 Ohm PMOS) directly; D1 BAT43WS to U2 FT231X VCC (N$7); Q3 gate (R21 10k pull-down). Q3 pulls Q2 gate (N$6, R19 100k to 3V3) low, turning on Q2 (P-channel, S = 3V3, D = 3V3_FTDI), which ties the FT231X 3V3OUT/VCCIO rail to the MCU 3V3 rail.
- **U9 TPS2104 selects VMAIN** by its EN pin only (datasheet function table: EN = H gives OUT = VIN2 even when VIN2 = 0 V; EN = L gives OUT = VIN1). EN = N$14 = U10 TLV3691 output. U10: IN+ = 3V3_FTDI, IN- = VBAT_SW/2, VCC = 3V3. So VMAIN = battery only while 3V3_FTDI < VBAT_SW/2; otherwise VMAIN = VUSB.
- **VMAIN** feeds U7 TPS7A0533P (EN = 3V3_AUX_CTRL = PC6, D22) which makes 3V3_AUX, and through JP2 (1-2 closed by paste) U11 MIC94090 (EN = PD4) for the external VSWITCH.

### What differs between the two modes
| | Battery terminal (J3) | USB cable spliced to the D cells (J3 open) |
|---|---|---|
| MCU 3V3 rail | U6 TPS79733 from VBAT+ | FT231X internal 3V3OUT regulator (VCC = D cells minus one BAT43 drop) through Q2 (UNVERIFIED whether U6 also back-feeds VBAT+ from its output) |
| VMAIN source | VBAT+ through U8 (firmware-gated) then TPS2104 IN1 (NMOS, charge pump, specified for VIN >= 2.7 V) | VUSB through TPS2104 IN2 (PMOS), not gated by firmware |
| TPS2104 EN state that is needed | LOW, which requires 3V3_FTDI < VBAT_SW/2 at every wake | HIGH, which is guaranteed (3V3_FTDI = 3.3 V vs VBAT_SW/2 near 0) |
| Ground return | through Q1 | J4 GND directly (Q1 bypassed) |
| VMAIN during sleep | 0 V (U8 off) | stays at the D-cell voltage |
| 3V3_AUX (RTC VCC) during sleep | 0 V (U7 off, `powerAux(OFF)` in turnOffSDcard, Margay.cpp line 1006) | 0 V as well (U7 off): **the RTC runs on the coin cell during sleep in both modes** |
| 3V3_AUX at wake | U8 on, then (same instant) U7 on; VMAIN appears only after VBAT_SW rises, the comparator decides, and the TPS2104 switches | U7 on with VMAIN already up |

### Firmware facts the trace depends on (verified, 2024 code)
- Sleep entry, `turnOffSDcard()` (Margay.cpp lines 980-1015): `powerAux(OFF)` then `powerOB(OFF)` with no delay between, i.e. U7 EN low then U8 EN low. Wake, `turnOnSDcard()` (lines 1029-1050): `powerOB(ON)`, `powerAux(ON)`, `delay(6)`, then `SD.begin`.
- UART is never stopped: `Serial.begin(38400)` in `begin()` (line 202); `pinMode(9, INPUT)` before sleep does not release TX while the USART transmitter is enabled (AVR port override; from the ATmega datasheet, from memory, UNVERIFIED this session). So PD1 (TX) idles HIGH through R9 330 Ohm into FT231X RXD in sleep and awake.
- RTC driver in use in 2024 (NorthernWidget-libraries/DS3231_Logger, identical md5 to ~/Arduino/libraries copy dated 2024-11-30): `begin()` writes Control 0x0E = 0x24 (EOSC=0, BBSQW=0, CONV=1, INTCN=1); `setAlarm()` writes 0x0E = 0x05 (INTCN, A1IE; BBSQW=0); `clearAlarm()` writes Status 0x0F = 0x00 (clears OSF every alarm, and OSF is never read). No I2C bus recovery anywhere (only `Wire.begin()`).
- `clockTest()` (lines 456-490): fails (`OBError`, red LED) if the address does not ACK or if the seconds register has not changed after `delay(1100)`; sets `TimeError` (cyan, "PASS, BAD TIME") if year == 00. Time can be set only over Serial inside `begin()` (lines 224-232), so any coin-cell swap that resets the clock forces a USB connection to set the time.
- Battery assumptions: `getBatPer()` divides by 3.0 (three alkaline cells); `BatVoltageError = 3.3` V (Margay.h line 169). Two D cells would trip the low-battery flash on every start.
- Fuses (boards.txt NW1284p): efuse 0xFE, i.e. BODLEVEL 1.8 V, at 8 MHz (ATmega1284P speed grade 0-10 MHz needs 2.7 V, from memory, UNVERIFIED).
- TPL5010 R10 = 130k gives an interval between the 1 h (124.9k) and 1.5 h (149.4k) rows of TPL5010 Table 3, so a missed RTC wake shows up as a watchdog reset about an hour later and a new log file.

## 2. Candidate causes

Ranking is my judgment, given what is known (no description of the failure, no cell count, no firmware build).

### A. The comparator (U10) can select the dead USB input while on battery, collapsing VMAIN and with it the clock's VCC
**Mechanism.** On battery, VMAIN exists only while TPS2104 EN is LOW, i.e. while TLV3691 IN+ (3V3_FTDI) < IN- (VBAT_SW/2). With no USB, 3V3_FTDI is not driven by anything: Q2 is off, the FT231X is unpowered (its VCC N$7 sits behind D1 and VUSB is held at 0 by R21). It is a floating node set by leakage and back-feed: (1) MCU TX idles HIGH into FT231X RXD through R9 330 Ohm, and the FT231X datasheet says "When used in Input Mode, the input pins are pulled to VCCIO via internal 75kOhm (approx.) resistors" (Rpu 40-190 kOhm, Table 5.4); in an unpowered chip that pull-up is a path from the TX line into VCCIO = 3V3_FTDI (UNVERIFIED that it conducts backwards; the datasheet also says "Tolerant of 5V input"); (2) the RGB LED D2 has its anode on 3V3 and its red and blue cathodes go through R8/R5 330 Ohm to CBUS1/CBUS2, another route from 3V3 into the FT231X I/O ring; (3) Q2 off-state leakage from 3V3. If 3V3_FTDI rises above VBAT_SW/2 (17 mV hysteresis, TLV3691 VHYS), the TPS2104 obeys its function table ("VIN1 5V, VIN2 0V, EN H: OUT = VIN2") and VMAIN goes to 0 V. 3V3_AUX then dies, the DS3231M drops to VBAT, its I2C pull-ups (R15, R16) and its SDA switch (U4) lose power, and the clock stops answering. The BME280 and MCP3421 die with it, but "clock" is the first labeled test that fails.
**Why the cold matters.** IN- falls with the cell voltage (alkaline cells lose voltage under load in the cold); the back-fed IN+ is held down only by leakage in the unpowered FT231X, which falls steeply in the cold, so the node can float higher. Both push toward the wrong state. The size of either effect is UNVERIFIED. With two D cells, IN- is only about 1.4-1.5 V, so even a modest back-fed voltage flips it.
**Explains.** Cold: yes (plausible, direction argued above, unmeasured). USB cure: yes, by construction; with USB the required state (EN high, IN2) is guaranteed and VMAIN is not gated by firmware or the comparator. Warm-cell cure: only indirectly, as the coin cell must carry the RTC through an abrupt VCC loss (see C and D); otherwise no.
**Likelihood.** Medium-high. It is the one mechanism I found that is specific to the battery-terminal path and absent in the USB path. It hinges on one unmeasured voltage.
**Bench test.** Power from the battery terminal (no USB). Probe 3V3_FTDI (at C9), U10 IN- (N$12, R17/R18 junction), U9 EN (N$14), VMAIN (C13) and 3V3_AUX (C15) through a full log cycle, awake and asleep, at room temperature and then at -20 C in a freezer with the batteries cold too. Confirms if 3V3_FTDI approaches VBAT_SW/2 and N$14 goes high while awake. A second, decisive variant: lift R9 (or add `Serial.end()` and drive TX low before sleep) and repeat. Kill: 3V3_FTDI stays well below VBAT_SW/2 (say under half of it) and N$14 stays low throughout at -20 C.

### B. Battery voltage below what the battery-terminal path needs (two cells, or cold sag)
**Mechanism.** The battery path to the clock is U8, then the TPS2104 IN1 NMOS, whose gate comes from a charge pump: "The charge pump operates from input voltages as low as 2.7 V" and the recommended range is "2.7 to 5.5" V. Below that, IN1 may not fully enhance and VMAIN sags or fails, taking 3V3_AUX below the DS3231M's VPF (2.45-2.70 V). If 3V3_AUX < VPF and < VBAT, the DS3231M runs on the coin cell (Table 1). The same low cell voltage puts the MCU rail (TPS79733, dropout about 110 mV at 10 mA) below 2.7 V at 8 MHz with BOD at 1.8 V, so the MCU may run out of its speed grade without resetting. The USB path reaches VMAIN through the IN2 PMOS, which needs no charge pump.
**Explains.** Cold: yes (alkaline cells sag). USB cure: yes (IN2 path), but note that with two cells the USB path is also marginal for the FT231X (VCC = cells minus a BAT43 drop; FT231X wants 2.97/3.3 V minimum), so USB would not obviously help with two cells. Warm cell: no.
**Likelihood.** High if Jonas used two D cells (Andy's reply allowed "2 or 3"), low with three fresh cells (about 4.5 V). The firmware assumes three.
**Bench test.** Ask Jonas the cell count first. Then, from a bench supply on the battery terminal, step from 4.5 V down to 2.4 V in 0.1 V steps at room temperature and at -20 C, recording VMAIN, 3V3_AUX, 3V3 and the serial self-test; repeat through the USB connector. Confirms if the battery-terminal path fails at a voltage the USB path survives.

### C. The CR1220 cannot carry the DS3231M's battery-mode current pulses in the cold
**Mechanism.** During every sleep, in both modes, 3V3_AUX is off and the RTC runs from the coin cell (trace above). On VBAT the DS3231M runs a temperature conversion every 10 s: IBATTC 575 uA typ at 3.63 V (650 at VBATmax), tCONV 10 ms. The only local storage is C19 (0.1 uF), which supplies that pulse for only about 17 us per 0.1 V of droop; 575 uA for 10 ms from C19 alone would need 57.5 V of droop, so the cell supplies the pulse. Energizer's CR1220 sheet plots pulse internal resistance up to about 280 Ohm over life at 21 C (0.16 V drop at 575 uA); Energizer's coin-cell handbook says IR rises in extreme cold and the loss is reversible on warming (numbers at -20 C not found, UNVERIFIED). At 1 kOhm the drop would be 0.58 V. VBAT minimum is 2.3 V. If VBAT dips below that, the oscillator can stop or the registers can be lost; on the next VCC the part may come up at 01/01/00 (datasheet, "On the first application of VCC power ... the time and date registers are reset to 01/01/00") or with the oscillator stopped, failing `clockTest()`.
**Explains.** Cold: yes. Warm-cell cure: yes, directly (reversible IR). USB cure: no. The RTC's VBAT duty is the same in both modes, because `powerAux(OFF)` turns U7 off in sleep regardless of where VMAIN comes from.
**Likelihood.** Medium. It fits the one written observation best, but a fresh CR1220 at 0 C (the email's temperature) should manage a 0.6 mA pulse; it needs a used cell or about -20 C.
**Bench test.** Logger asleep on battery in a freezer at -20 C; scope VCOIN+ (C19) AC-coupled for more than 60 s to catch several 10 s conversion pulses; compare a fresh cell and a used one. Confirms if the pulse minimum falls near 2.3 V. Kill: droop under about 0.2 V with a used cell at -20 C. A cheap A/B: add 47-100 uF low-leakage across C19 and see if the cold failure disappears.

### D. 3V3_AUX falls faster than the DS3231M allows, at every sleep
**Mechanism.** DS3231M power-switch spec: "VCC Fall Time, VPFMAX to VPFMIN, tVCCF, min 300 us". U7 is a TPS7A0533**P**, which "connects a 120-Ohm resistor to ground when the device is disabled". With C15 + C16 = 10.1 uF and the 120 Ohm alone, tau = 1.21 ms and the fall from 2.70 to 2.45 V takes 118 us (99 us if the 0805 X5R has lost 15 % to bias and cold); computed, ignoring the other loads, which only make it faster. That is roughly a third of the minimum, every sleep. A switchover that is too fast asks the coin cell to take over abruptly, and a high-resistance cold cell is the worst case for that.
**Explains.** Cold and warm-cell: yes, through the coin cell's IR at the switchover. USB cure: no. In USB mode VMAIN stays up, so the active discharge is fully driven and the fall is, if anything, faster.
**Likelihood.** Medium-low as the cause; it is a verified spec violation either way.
**Bench test.** Scope 3V3_AUX at sleep entry and read the 2.70-2.45 V interval. A/B: run many fast sleep/wake cycles (short log interval) in the freezer with a used coin cell, then read the Status register's OSF (the firmware clears it, so read it with a test sketch before `setAlarm`), with and without a slowed fall (for example a larger C15, or a TPS7A0533 without the P option).

### E. The alarm may not be able to wake the logger while the clock runs on the coin cell
**Mechanism.** The driver leaves BBSQW = 0, and the datasheet says "When BBSQW is logic 0, INT/SQW goes high impedance when VCC falls below VPF". In this design VCC is below VPF throughout every sleep (U7 off). Read literally, the alarm cannot pull RTC_INT low during sleep in either mode, and the logger would wake only on the button or the TPL5010 reset about an hour later. That contradicts working deployments, so either silicon asserts alarms on VBAT with INTCN = 1 anyway, or 3V3_AUX is not actually near 0 V in sleep on some boards (some back-feed I have not found). If it is the second, that back-feed is temperature-dependent and this becomes a cold mechanism.
**Explains.** Not mode-specific in my trace; cold only if a back-feed is involved. Warm cell: no.
**Likelihood.** Low as the field cause; high value to measure, because it governs how the logger wakes at all.
**Bench test.** Battery-powered, room temperature: scope 3V3_AUX and RTC_INT across an alarm while asleep. If RTC_INT falls with 3V3_AUX at 0 V, the datasheet sentence does not apply to alarms and this candidate dies.

### F. A coin-cell-held I2C hang, cured by removing the cell rather than by warming it
**Mechanism.** The DS3231M keeps its I2C state on VBAT ("The I2C interface is accessible whenever either VCC or VBAT is at a valid level"), and the datasheet warns that an MCU reset mid-read can leave the two "unsynchronized". The firmware never toggles SCL to recover. Only removing the coin cell with the D cells off clears it. SCL is wired straight to the off-board J2.10 and is pulled toward the dead 3V3_AUX through R16 during sleep, so each wake gives the RTC a single SCL edge.
**Explains.** Warm-cell cure: yes, as a power reset. Cold: only if the cold causes the resets that start it (B). USB: no.
**Likelihood.** Low-medium.
**Bench test.** On a failed unit: before touching the cell, measure SDA_OB (RTC pin 7) with the board awake; low means a hung slave. Then remove and reinsert the same cold cell. If that cures it, temperature was not the cure.

### G. A cold oscillator that starts too slowly for the 1.1 s self-test after a coin-cell change
**Mechanism.** "the first time VBAT is applied to the device the oscillator does not start up until VCC exceeds VPF or until a valid I2C address is written ... Typical oscillator startup time is less than 1s." `clockTest()` allows 1100 ms for the seconds register to change. A cold MEMS start that runs longer than that fails the test (red), with no "FAIL" text printed for that branch.
**Explains.** Cold: yes. Warm cell: partly, since a cell inserted and powered at once is the first-VBAT case. USB: no.
**Likelihood.** Low.
**Bench test.** At -20 C, insert a cell, apply power, and log the time from power-up to the first seconds increment across about 10 trials.

### A confound in the field procedure (verified from code and datasheet)
Swapping the coin cell with the D cells disconnected resets the DS3231M to 01/01/00, and `begin()` can set the time only over Serial. So a coin-cell swap in the field forces a USB connection to set the clock. The "warm cell" and "USB" cures may be one event, and the USB session also warms and power-cycles the board. Ask Jonas the order of operations.

## 3. Tests in priority order
1. Ask Jonas: cell count (2 or 3 D); what "the clock failed" looked like (LED color, serial text, or wrong timestamps); whether the cured units were set over USB after the swap.
2. Test A (3V3_FTDI, N$14, VMAIN, 3V3_AUX on battery, room temperature then -20 C; then with R9 lifted). Cheapest, and it alone separates the battery path from the USB path.
3. Test B voltage sweep, both connectors, both temperatures.
4. Test C coin-cell droop in the freezer with fresh and used cells.
5. Test D fall-time scope plus OSF count; test E RTC_INT during sleep (same setup as A).
6. Tests F and G on any unit that fails, before its cell is touched.

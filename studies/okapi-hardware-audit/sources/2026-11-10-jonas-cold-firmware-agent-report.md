COMPLETE

# Margay cold clock failures: firmware-first analysis

Analyst: firmware-track subagent, 2026-11-10. Independence rules observed: nothing read under NW-Status/, Project-Margay docs/rtc-decoupling-history.md, QUEUE.md, or GitHub issues.

## Sources read (all of them, dead ends included)
- Evidence pack: scratchpad/jonas/evidence.md.
- Library (2024): /home/awickert/Dropbox/NorthernWidget/github/Margay_Library-Wickert-Local-cached20241227/src/Margay.cpp, Margay.h (LibVersion "0.3.0", Margay.h:124). Example MargayDemo_v10 is stale (old API, Model_0v0) and tells nothing about the field sketch.
- RTC driver: /home/awickert/Dropbox/NorthernWidget/github/DS3231_Logger at commit 850dfbf (2022-09-18), the last commit before 2026; byte-identical to ~/Arduino/libraries/DS3231_Logger/src/DS3231_Logger.cpp (checked with diff). Later commits do not change the register values written (0x24, 0x05, 0x06, 0x0F=0x00).
- Board package /home/awickert/.arduino15/packages/NorthernWidget/hardware/avr/0.3.1/: boards.txt NW1284p (lines 91-111), variants/NW1284p/pins_arduino.h, libraries/Wire (utility/twi.c). Core is arduino:arduino 1.8.6 (HardwareSerial, Stream).
- Netlist: scratchpad/rtc/eagle.json (built Eagle design); KiCad scratchpad/bomlines/margay2.xml for MPNs only.
- Datasheets: icreq/txt/ds3231m.txt, ft231x.txt; cc/dl/tps2104.txt, tps22916.txt, tps7a05.txt, tps797.txt, tpl5010.txt.
- Not obtained: ATmega1284P datasheet (speed grade and BOD table quoted from memory, marked UNVERIFIED); CR1220 manufacturer data (internal resistance vs. temperature, UNVERIFIED); TLV3691 hysteresis (not checked).

## What the hardware does under this firmware (verified from netlist + code)
- RTC1 (DS3231M) VCC is on 3V3_AUX = U7 TPS7A0533P output. U7.EN = PC6 = D22 = `Ext3v3Ctrl` (Margay.cpp:50; pins_arduino.h maps D22 to PC6). U7 is the "P" (active-discharge) part: "RPULLDOWN 120 Ω, P version only" (tps7a05.txt:433).
- RTC1 VBAT = VCOIN+ = BT1 (CR1220) with only C19 = 0.1 µF. No other source on that net.
- RTC INT/SQW = RTC_INT, to PB2/INT2 only. No external pull-up: the firmware supplies the MCU's internal pull-up (Margay.cpp:268 `pinMode(RTCInt, INPUT_PULLUP)`), from the always-on 3V3.
- MCU 3V3 is U6 TPS79733 with VIN = VBAT+ (battery terminal J3). With USB present, Q3 (gate = VUSB) turns on Q2 and ties 3V3 to the FT231X 3V3OUT (3V3_FTDI).
- VMAIN (input of U7) = U9 TPS2104 OUT. IN1 = VBAT_SW (U8 TPS22916C, ON = PC3 = D19 = `BatSwitch`), IN2 = VUSB. U9.EN = U10 TLV3691 output, IN+ = 3V3_FTDI, IN- = VBAT_SW/2 (R17/R18 10k/10k). TPS2104: "EN = L: OUT = VIN1; EN = H: OUT = VIN2" (tps2104.txt:110-117). So USB, when present, wins.
- I2C pull-ups R15/R16 are on 3V3_AUX. The RTC's SDA is SDA_OB, behind U4 (SN74LVC1G3157, powered from 3V3_AUX); SDA_OB has no pull-up of its own. SCL goes straight to the RTC.
- Fuses NW1284p: low 0xF7, high 0xDE, extended 0xFE (boards.txt:100-102). 0xDE leaves JTAGEN unprogrammed, so PC2-PC5 work as GPIO (good: `BatSwitch`, `I2C_SW` are on JTAG pins). 0xFE = BODLEVEL 110 = 1.8 V (UNVERIFIED decode from memory of the ATmega1284P table). F_CPU 8 MHz.

### The sleep and wake sequence
1. `run()` sleeps after `AwakeCount > 5` (Margay.cpp:773-779).
2. `sleepNow()` -> `turnOffSDcard()` (Margay.cpp:951, 982-1026): SCL/SDA (D16/D17) and RX/TX (D8/D9) set INPUT (990-995, pull-ups off); `powerAux(OFF)` then `powerOB(OFF)` (1006-1007) cut 3V3_AUX and VBAT_SW; SD_CS low; SPCR = 0; SPI clock off. Then PWR_DOWN with BOD disabled in sleep (961-967, `sleep_bod_disable()`).
3. **So every sleep, the RTC loses VCC and runs from the CR1220.** In battery mode VMAIN also dies (U8 off). In USB mode VMAIN stays at VUSB through U9 IN2, but U7 is still disabled, so the RTC is on the coin cell in both modes.
4. Wake: RTC INT falling edge on INT2 (isr1, Margay.cpp:257, 917, 848-853) or the log button (PCINT, 262-266). `turnOnSDcard()` (1028-1054): `powerOB(ON)`, `powerAux(ON)`, 6 ms, SPI on, 10 ms, `SD.begin`. Then `addDataPoint()` reads the RTC, then `RTC.setAlarm()` (747), `resetWDT()` pulses the TPL5010 DONE (783-788).
5. Backstop: TPL5010 (U3) resets the MCU if DONE is missed (tpl5010.txt:560-563). With R10 = 130 kΩ the period is on the order of an hour (current-library commit 63bbec9 says 3853 s; UNVERIFIED by me).

### How the clock is set, checked and reported
- Time is set only from serial, in `begin()`: any byte present 100 ms after the banner (Margay.cpp:225-235) makes the code `readString()` (1 s timeout) and call `RTC.setTime()` on six 2-digit fields parsed with `toInt()`. Non-digit garbage parses as 0, giving `setTime(2000, 0, 0, 0, 0, 0)`. `setTime()` returns nothing and never reads back ("//Read back time to test result of write??", DS3231_Logger.cpp:60).
- `clockTest()` (Margay.cpp:453-491) reports three things only: (1) NACK at 0x68 -> "Clock:  FAIL", OBError, red LED; (2) seconds not advancing over 1.1 s -> OBError and red LED, **but nothing is printed after "Clock: "**; (3) year register == 00 -> "PASS, BAD TIME", TimeError, cyan LED.
- **The oscillator-stop flag is never read, and it is erased before anyone could look at it.** `begin()` calls `RTC.clearAlarm()` (Margay.cpp:196) before `clockTest()`, and `clearAlarm()` writes 0x0F = 0x00 (DS3231_Logger.cpp:329-334), which clears OSF (ds3231m.txt:909-911: "This bit remains at logic 1 until written to logic 0"). `setAlarm()` calls `clearAlarm()` at its end (DS3231_Logger.cpp:326), so OSF is also erased at every logged point. A clock that stopped and restarted on VBAT is therefore invisible unless it went all the way to year 00.
- During logging (`run()`, `addDataPoint()`), nothing checks the time at all. If the RTC resets, its control register goes to the power-up value (INTCN = 1, A1IE = 0; ds3231m.txt:800-804), the alarm interrupt is disabled, and the logger sleeps until the TPL5010 reset. The reboot then shows year 00 (cyan) and logging resumes with 2000-01-01 timestamps in a new file.
- `RTC.begin()` and `clearAlarm()` run microseconds after `powerOB(ON)`/`powerAux(ON)` (Margay.cpp:169-170 vs 195-196). 3V3_AUX needs U8 (C version, "5-V turn-on time 1400 µs", tps22916.txt:21-23), U9 IN1 (tr about 0.3 ms, tps2104.txt:342) and U7 ("Start-up time 1.5 typ, 2.8 max ms", tps7a05.txt:455). Their return values are ignored. Old Wire has no timeouts (twi.c:141, 180, 220, 262), so the result is either a delayed transaction or a silent NACK. `setAlarm()` rewrites 0x0E later, so the consequence is small, but nothing confirms the RTC configuration at boot.
- Control register values written: 0x24 at begin (CONV, INTCN; BBSQW = 0); 0x05 at `setAlarm` (INTCN, A1IE; BBSQW = 0); 0x06 for 60 s mode. EOSC = 0 always (oscillator runs on VBAT).

### What differs when USB is present (verified from netlist + code)
- VMAIN is not power-cycled by the firmware: `powerOB()` only switches U8, and IN2 = VUSB is not under firmware control. In battery mode, firmware switches VMAIN on and off every log cycle.
- The MCU runs from the FT231X 3V3 LDO ("3V3 output at 50mA", ft231x.txt:358) through Q2, instead of U6 (TPS797, "50-mA", tps797.txt:9). The battery terminal's Q1/U6/U8/U9-IN1 path is not used.
- The FT231X is powered, so its TXD drives the MCU's RX (through R7) to a firm idle-high. In battery mode the FT231X has no VCC; the MCU's RX then sees an unpowered (or partly back-fed) output. The core stores framing-error bytes (HardwareSerial_private.h:103: only parity errors are dropped), so any edge on RX at boot becomes `Serial.available()`.
- `getBatVoltage()` reads VBAT_SW, which is 0 V on USB-only power, so BatError fires at boot (red flashes). This is cosmetic.

## Candidate causes

Legend: C = explains the cold; W = explains the warm-coin-cell cure; U = explains the USB cure.

### 1. The CR1220 cannot hold the DS3231M on VBAT in the cold; the firmware puts the RTC on VBAT every sleep and hides the evidence
- Mechanism: the firmware cuts RTC VCC every sleep (Margay.cpp:1006, U7.EN). The RTC also runs from the coin cell whenever the logger is unpowered (transport, setup). On VBAT the DS3231M draws its timekeeping current plus a 10 ms temperature-conversion pulse every 10 s: "IBATTC ... 575 µA (VBAT = 3.63 V), 650 µA max" (ds3231m.txt:159-161); "When VBAT is the presently selected power source, temperature conversions are executed once every 10s" (ds3231m.txt:621-623); "tCONV 10 ms" (ds3231m.txt:143). VBAT must stay at or above 2.3 V (ds3231m.txt:82). C19 = 0.1 µF holds 575 µA for 10 ms only with a 57 V sag (arithmetic), so the cell alone carries the pulse. A cold, small, partly used lithium coin cell with high internal resistance (UNVERIFIED: about 1 kΩ is needed for a 0.6 V sag; plausible for an aged CR1220 near -20 °C, not established) dips below the minimum. The result is either an oscillator stop (OSF set, time lags) or a full reset (time 01/01/00 01:00:00 per ds3231m.txt:636-640, A1IE = 0). The firmware clears OSF before testing (Margay.cpp:196 -> DS3231_Logger.cpp:331-332) and only catches a full reset (year 00) or a stopped oscillator at boot.
- Explains: C yes; W yes; U **no**. The RTC is on the coin cell during sleep in USB mode as well, because U7 is still disabled.
- Likelihood: high for the cold and warm-cell observations, because it is the only path by which the coin cell matters at all. While awake the RTC is on VCC (3V3_AUX = 3.3 V > VPF 2.45-2.70 V, ds3231m.txt:127), and the coin cell is irrelevant then. Lower if the cells were fresh and it was really near 0 °C, as in the email.
- Bench test: replace BT1 with a bench supply at 3.0 V through a series resistor and sweep the resistor (100 Ω to 3 kΩ) at room temperature with the normal 1-minute logging cycle. Record VBAT at 1 µs resolution across a conversion pulse and find the resistance at which OSF sets or the time resets. Then measure a real CR1220's pulse resistance (0.6 mA, 10 ms) at +20, 0 and -20 °C, fresh and partly used. Use a test sketch that reads 0x0F **before** any write and prints OSF and 0x0E. Confirm: OSF = 1 or POR time at the measured cold-cell resistance. Kill: no failures below several kΩ.

### 2. RTC I2C state machine wedged and kept alive by the coin cell; swapping the cell is really a power cycle
- Mechanism: every sleep entry and wake toggles the bus supply under the RTC. R16 pulls SCL to 3V3_AUX as it is shut off, and SDA_OB floats with U4 unpowered and no pull-up of its own. An MCU reset in the middle of an RTC transaction can also leave the DS3231M driving SDA low. The datasheet warns of exactly this: "the microcontroller and device's I2C communications could become unsynchronized ... toggling SCL until SDA is observed to be at a high level" (ds3231m.txt:647-658). The firmware never does that recovery. Wire has no timeouts, so the MCU hangs until the TPL5010 resets it, then reports "Clock: FAIL" (NACK) or hangs again. The coin cell keeps the RTC powered through MCU resets and D-cell disconnects, so the only reset is removing the coin cell. The "warmer" cell may be incidental.
- Explains: C weakly (edge timing and thresholds shift with temperature; not established); W yes (any cell swap); U no.
- Likelihood: medium. It fits "replace the cell and it works" without needing the cell to be weak.
- Bench test: on a failed unit, **before** touching the cell, probe SDA_OB and SCL with the logger awake. SDA_OB held low while SCL is high confirms it. Then send nine SCL clocks from a test sketch: recovery without removing the cell confirms the mechanism; a unit that still NACKs points elsewhere. Also cycle sleep and wake 10,000 times at -20 °C and count wedges.

### 3. Spurious serial byte at boot in battery mode zeroes the clock (`setTime(2000,0,0,0,0,0)`)
- Mechanism: Margay.cpp:225-235 sets the clock from **any** received byte within about 100 ms of the banner, without validating it. In battery mode the FT231X is unpowered. Once `Serial.begin()` (Margay.cpp:204) drives TX high into the FT231X RXD through R9, the chip may be partly back-fed (UNVERIFIED; the FT231X inputs are "5V tolerant", ft231x.txt:665, and its input-mode pins have 75 kΩ pull-ups to VCCIO, ft231x.txt:413). Its TXD can then glitch, so the MCU RX sees an edge, the core stores the byte even with a framing error, `toInt()` gives zeros, and the clock is written to 00/00/00 00:00:00. `clockTest()` then reports "PASS, BAD TIME" (cyan): "the clock failed". On USB power the FT231X drives TXD idle-high, so no spurious byte arrives.
- Explains: U yes, directly through code; C possible (back-feed and threshold levels are temperature dependent; UNVERIFIED); W only if the crew re-set the time after the swap, which they would have had to do anyway. A swap with the logger unpowered resets the DS3231M to year 00 as well (ds3231m.txt:636-640).
- Likelihood: medium-low. It is the only firmware path found that turns "USB present" into a clock fault, so it deserves the cheap test.
- Bench test: in battery mode at room temperature and at -20 °C, put a logic analyzer on PD0 (RX), DTR#/RST and 3V3_FTDI during 50 boots. Print `Serial.available()` and the received bytes. **Discriminator in the data**: a spurious set leaves day = 00 and month = 00, while a DS3231M power-on reset leaves 01/01/00 01:00:00. The serial log also shows the "0  0" debug lines from Margay.cpp:232.

### 4. Supply dip at wake in battery mode only, with BOD at 1.8 V, corrupting RTC transactions or resetting the MCU mid-transaction
- Mechanism: in battery mode the firmware switches VMAIN on every wake (U8 then U9 IN1 then U7 into C15 = 10 µF, the SD card and the other loads). The inrush comes from the same VBAT+ node that feeds U6, the MCU's 3V3. Cold alkaline D cells and field leads raise the source resistance. On USB, VMAIN is never switched, the MCU's LDO is separate (FT231X behind D1), and no inrush occurs. The BOD at 1.8 V (efuse 0xFE, boards.txt:102; decode UNVERIFIED) lets the 8 MHz MCU run below its safe operating voltage (about 2.4 V by interpolating the ATmega1284P speed grade, UNVERIFIED). Corrupted execution can write wrong bytes to the RTC (time, or EOSC), or reset in the middle of an I2C transaction, which feeds candidate 2.
- Explains: C yes (D-cell resistance); U yes; W no, unless it acts through candidate 2.
- Likelihood: low with three fresh D cells (about 4.5 V); higher with two cells or long, thin leads. The pack configuration is UNVERIFIED.
- Bench test: in a freezer at -20 °C, with the field cable and pack, scope VBAT+ and 3V3 at the wake edge in battery mode and then in USB mode. Confirm: 3V3 falls below about 2.5 V in battery mode only. Second test: program efuse 0xFD (BOD 2.7 V). If clock faults turn into clean BOD resets (MCUSR BORF), this is confirmed.

### 5. The firmware's sleep entry violates the DS3231M's minimum VCC fall time, and a weak coin cell must catch the switchover
- Mechanism: "VCC Fall Time, VPFMAX to VPFMIN, tVCCF, 300 µs min" (ds3231m.txt:171-173). `powerAux(OFF)` engages U7's 120 Ω pulldown on 3V3_AUX (C15 10 µF + C16 0.1 µF + loads). The 2.70 V to 2.45 V fall takes at most τ·ln(2.70/2.45) = 1.21 ms x 0.097 = 0.12 ms (nominal C, loads ignored; arithmetic). That is about 2.5 times faster than the minimum, every log cycle. The consequence is unspecified; a stiff VBAT probably absorbs it, and a cold, high-resistance coin cell may not.
- Explains: C and W yes; U no (in USB mode U7's VIN stays up, so the pulldown is fully biased, and if anything the fall is faster).
- Likelihood: low-medium. It is a datasheet violation produced by the firmware sequence, but its effect is not documented.
- Bench test: scope 3V3_AUX at sleep entry and measure the 2.70-2.45 V time. With the series-resistor coin-cell emulator from test 1, compare failure rates at a fixed resistance with and without an added 47 µF on 3V3_AUX, or with U7 left enabled during sleep (test firmware). A difference confirms this candidate.

### 6. The firmware relies on alarm interrupts from VBAT while the datasheet says INT/SQW goes high impedance there
- Mechanism: BBSQW is written 0 every time (DS3231_Logger.cpp:31, 242, 276). The datasheet says: "When BBSQW is logic 0, INT/SQW goes high impedance when VCC falls below VPF" (ds3231m.txt:812-814). In sleep, RTC VCC is 0 V, so read literally, the alarm cannot pull INT2 low, and wakes would come only from the TPL5010. Margays do log on schedule, so either the part asserts the alarm on VBAT in practice or I am misreading the condition. Either way, the wake depends on behavior the datasheet does not promise, which could be marginal at a low VBAT.
- Explains: C and W only if the undocumented drive weakens at low VBAT (speculative); U no.
- Likelihood: low as the cause; high value to check, because the answer decides whether the firmware should set BBSQW.
- Bench test: 60 s interval, scope RTC_INT and 3V3_AUX during sleep. Does INT fall while 3V3_AUX = 0? Repeat with VBAT from a bench supply at 3.0, 2.6 and 2.35 V, and at -20 °C. If INT never falls, wakes are TPL5010 resets (new log file each time). If it stops falling at low VBAT or in the cold, this becomes a C+W candidate.

### 7. Back-fed FT231X in battery mode: spurious resets through DTR#, or the power mux choosing the dead USB input
- Mechanism: with 3V3_FTDI partly back-fed (UNVERIFIED, see 3), (a) DTR# -> C1 -> RST can pulse the MCU reset, feeding candidates 2 and 3; (b) U10 compares 3V3_FTDI with VBAT_SW/2 (about 2.2-2.4 V for three cold to fresh D cells). If the back-fed level exceeds that, U9 selects IN2 = 0 V, VMAIN and 3V3_AUX collapse while awake, and the RTC drops to the coin cell with its bus unpowered ("Clock: FAIL"). Cold lowers VBAT_SW/2, so the comparison gets more marginal.
- Explains: C possible; U yes (with USB, IN2 is live); W partly (it decides whether time survives the collapse).
- Likelihood: low. Variant (b) would also kill the SD card and BME280, and Jonas reported only the clock.
- Bench test: battery mode, awake, room temperature and -20 °C: measure 3V3_FTDI, U9.EN (U10 OUT) and VMAIN, and watch RST. Any U9.EN high in battery mode confirms (b); RST pulses with no TPL5010 RSTn confirm (a).

### 8. Coin-cell holder contact in the cold (hardware; noted only)
- Mechanism: a momentary open at BT1 when contraction relaxes the spring, with only 0.1 µF to ride through it, resets the RTC whenever it is on VBAT (every sleep). Handling or swapping the cell reseats it.
- Explains: C and W; U no. Likelihood: low-medium; UNVERIFIED.
- Bench test: cold-soak with the board flexed or tapped, logging VBAT on a scope with a dropout trigger at 2.2 V.

## The cheapest first test (no lab)
Ask what "the clock failed" looked like, because the firmware's outputs separate the candidates. Serial "Clock:" followed by nothing, or a red LED, means the oscillator was not running while on VCC (rare; points to an RTC fault). "Clock:  FAIL" means a NACK or wedged bus (candidates 2 and 7). "PASS, BAD TIME" or cyan means year 00 (candidates 1 and 3). In the SD logs, timestamps of 2000/01/01 01:00 point to a DS3231M power-on reset (candidates 1, 5 and 8); 2000/00/00 00:00 points to a spurious serial set (candidate 3); a new log file at about the TPL5010 period points to a lost alarm.

## One instrumented sketch serves every bench test
At boot and at every wake, before any write, read and log 0x0E, 0x0F (OSF, A1F) and the time registers raw, plus the ADC on BAT_SENSE. Ignore serial time strings that are not 12 digits. Run two units side by side at -20 °C with the same aged CR1220 type, one on the terminal and one on USB from the same D-cell pack type.

---

**Summary.** I traced the 2024 firmware (Margay library 0.3.0, DS3231_Logger as of 2022) against the built Eagle netlist. The firmware turns off the clock's main supply on every sleep, so the DS3231M runs from the CR1220 for most of its life, and the code erases the oscillator-stop flag before it tests the clock and again at every logged point. A clock that browns out on a cold coin cell therefore shows only as a year-2000 time or a missed alarm. That makes a coin cell unable to carry the 575 µA, 10 ms conversion pulses in the cold the leading explanation for the cold and the warm-cell cure (candidate 1). A wedged RTC bus that only a cell swap can reset is second (candidate 2). Nothing in the sleep path explains the USB cure, because the RTC sleeps on the coin cell in both modes. The firmware-level USB differences are an unvalidated serial time-set that can zero the clock when the FT231X is unpowered (candidate 3), and the firmware power-cycling VMAIN at each wake only in battery mode, with a 1.8 V BOD (candidate 4). The first, free discriminator is the symptom itself: the LED color or serial line, and whether bad timestamps read 2000/01/01 or 2000/00/00.

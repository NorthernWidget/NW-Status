COMPLETE

# Margay clock failures in the cold: component physics

Scope: how each part on the clock's power paths behaves at -20 °C, from manufacturers' data, and which candidate causes explain (A) failure in the cold, (B) the cure by a warmer coin cell, (C) the cure by feeding the same D cells through USB. Circuit and firmware are covered only as far as the physics needs them. Built design: Eagle netlist (eagle.json); values from it where Eagle and KiCad differ (R19 is 100k in Eagle).

## The frame the physics sits in (verified)

1. **The clock's VCC is the switched rail, not the coin cell alone.** eagle.json: `RTC1 VCC (pin 2)` is on net `3V3_AUX`, the output of U7 (TPS7A0533P, EN = PC6 `3V3_AUX_CTRL`); `RTC1 VBAT (pin 6)` is on `VCOIN+` with BT1 and C19 (0.1 uF, GCM155R71C104KA55D X7R) and nothing else.
2. **The firmware turns that rail off in every sleep.** Margay.cpp (2024 cache) `turnOffSDcard()`, lines 1006-1007: `powerAux(OFF); //turn off external 3v3 rail` and `powerOB(OFF);`. So between readings the DS3231M runs on the CR1220, in both battery and USB operation.
3. **BBSQW is always 0.** DS3231_Logger at 850dfbf (2022, the version current in 2024): `begin()` writes 0x0E = 0x24 ("turn off BBSQW"); `setAlarm()` writes 0x05 or 0x06. DS3231M datasheet, Control register: "When BBSQW is logic 0, INT/SQW goes high impedance when VCC falls below VPF."
4. **Power paths.** Battery terminal: VBAT+ -> U6 TPS79733 (MCU 3V3, always on) and -> U8 TPS22916C (EN = PC3) -> VBAT_SW -> U9 TPS2104 IN1. USB: VUSB -> U9 IN2, and -> D1 -> FT231X VCC; FT231X 3V3OUT (`3V3_FTDI`) -> Q2 -> 3V3. U9 OUT = VMAIN -> U7 -> 3V3_AUX. U9 EN = U10 TLV3691 OUT, IN+ = `3V3_FTDI`, IN- = VBAT_SW x R18/(R17+R18) = VBAT_SW/2. Q1 DMG3404L is the low-side reverse-polarity FET (G = VBAT+, D = VBAT-); the USB ground bypasses it. With USB fed from the D cells and nothing on the battery terminal, U6 and U8 are unpowered and the MCU runs from the FT231X regulator through Q2.
5. **MCU.** Fuses (boards.txt NW1284p): low 0xF7, high 0xDE, extended 0xFE, 8 MHz crystal. Extended 0xFE = BODLEVEL 110 = 1.8 V (mapping from memory of the ATmega1284P datasheet, UNVERIFIED here). JTAG is disabled (0xDE), which the PC2-PC5 assignments need.

## DS3231M facts that set the load on the coin cell (DS3231M datasheet, Maxim)

- VBAT recommended range "2.3 3.0 5.5 V" (min, typ, max).
- "Temperature Conversion Current IBATTC (I2C Inactive) VBAT = +3.63V ... 575 µA; VBAT = VBATMAX ... 650 µA".
- "Temperature Conversion Time tCONV ... 10 ms".
- "When VBAT is the presently selected power source, temperature conversions are executed once every 10s."
- "Timekeeping Battery Current IBATT ... 2 / 3.0 µA" (averaged, includes conversions); "Active Battery Current (I2C Active) 70 / 150 µA".
- "The temperature-conversion current IBATTC is specified since the system must be able to support the periodic higher current pulse and still maintain a valid voltage level."
- "Power-Fail Voltage VPF 2.45 2.575 2.70 V"; "VCC Fall Time, VPFMAX to VPFMIN tVCCF 300 µs (min)".
- Power control: "When VCC is less than VPF but greater than VBAT, the device is powered by VCC. If VCC is less than VPF and is less than VBAT, the device is powered by VBAT."
- "On the first application of VCC power ... the time and date registers are reset to 01/01/00"; "Oscillator Stop Flag (OSF) Delay tOSF 125 / 200 ms" (oscillator must be stopped that long to set OSF).
- The MEMS oscillator is specified -45 °C to +85 °C ("±5ppm ... from -45°C to +85°C"). Nothing in the datasheet says the oscillator itself fails at -20 °C.

So the coin cell must deliver **575-650 µA for 10 ms every 10 s**, at or above 2.3 V, with only 0.1 uF beside it.

## Part-by-part physics at -20 °C

**CR1220 (Panasonic CR1220 datasheet, Feb 2026, energy.panasonic.com).** Nominal 35 mAh, "Continuous drain 0.1mA", "Operating temperature -30°C to +85°C". Read from its curves: under a 30 kΩ (95 µA) load the plateau is about 2.88 V at 20 °C and about 2.70 V at -10 °C (with an initial dip to about 2.67 V); there is no -20 °C curve. "Operating voltage vs. load resistance (50% discharge depth), 20 °C": about 2.90 V at 0.03 mA, 2.80 V at 0.28 mA, 2.72 V at 0.54 mA, 2.40 V at 1 kΩ. Derived (my arithmetic on read-off values): incremental resistance at 20 °C, 50 % depth, about 350 Ω between 0.03 and 0.54 mA, so about 2.7 V under a 575 µA load at room temperature, half-discharged. The cold penalty at 95 µA is 0.18 V from 20 °C to -10 °C. Treated as a resistance (worst case) that is about 1.9 kΩ extra, which at 575 µA would add 1.1 V and put VBAT near 1.6 V; treated as charge-transfer polarization (logarithmic in current) it adds perhaps 0.1-0.2 V. The truth for a 10 ms pulse lies between, nearer the logarithmic end because the cell's double-layer capacitance carries part of a short pulse. **UNVERIFIED: the cell voltage under a 575 µA, 10 ms pulse at -20 °C has not been measured; the datasheets bracket it from about 1.6 V to about 2.5 V, straddling the DS3231M's 2.3 V minimum.** Maxell's CR1220 sheet (per a search snippet, not opened) gives -20 to +85 °C, so the brand matters; the brand in the field cells is unknown. Internal resistance also climbs steeply in the last part of a cell's life, so an old or partly used cell fails at a warmer temperature than a fresh one.

**C19 (0.1 uF X7R).** X7R holds ±15 % from -55 to +125 °C, so the cold changes nothing that matters. The point is size: carrying 575 µA for 10 ms from 0.1 uF alone would need 57.5 V of droop; from the KiCad redesign's 1 uF (C20), 5.75 V. Riding through a conversion with 0.2 V droop needs about 29 uF. **Neither the built board nor the redesign buffers the conversion pulse; the cell supplies it.** The DS3231M datasheet calls the VBAT capacitor optional in backup use.

**Alkaline D cells (Energizer E95 datasheet, Energizer document via a distributor mirror; data.energizer.com returned 404).** "Nominal IR: 150 to 300 milliohms (fresh)"; "Operating Temp: -18°C to 55°C". -20 °C is just outside rating. The rise of IR at -20 °C is not in the sheet (UNVERIFIED; a several-fold rise is typical of alkaline chemistry). Even at 1 Ω per cell, three cells under a 100 mA wake load lose 0.3 V, which leaves about 4.2 V against the TPS79733's regulation floor of about 3.5 V. The same cells feed both the battery and the USB path, so D-cell sag cannot by itself explain the USB cure.

**TPS79733 (U6).** "Operating Junction Temperature Range of -40°C"; "Typical Dropout Voltage of 105 mV at 10 mA". Not a cold weak point with three D cells. Absent in USB operation.

**TPS22916C (U8).** Specified -40 to +85 °C; "Quick Output Discharge (QOD): 150 Ω (typ.)" (C version has it); "Slow Timing in C Version ... 5-V turn-on time (tON): 1400 µs". Not a cold weak point.

**TPS2104 (U9).** "-40°C to 85°C"; "The charge pump operates from input voltages as low as 2.7 V". Function table: "5V 0V H -> VIN2" and "0V 5V L -> GND": **the EN pin selects an input outright; it does not fall back to the live one.** EN high selects IN2 (VUSB) even when VUSB is 0 V.

**TLV3691 (U10).** "VOS ... TA = -40°C to 125°C ±22 mV"; "IB ... 20 nA" max; hysteresis 17 mV. Its own drift is negligible. What decides its output is the voltage on `3V3_FTDI` when no USB is attached, which the netlist leaves undriven (see candidate 4).

**TPS7A0533P (U7).** "-40°C to +125°C"; "Start-up time 1.5 2.8 ms"; "UVLO threshold VIN rising 1.21 1.3 1.37 V"; "RPULLDOWN Pulldown resistor VIN = 3.3 V, P version only 120 Ω". The pulldown is an active transistor biased from VIN. Two consequences: (1) with the rail's ~6-10 uF (C15 10 uF X5R derated by DC bias, plus C16 and the loads) and 120 Ω, the rail falls from 2.70 V to 2.45 V in about 58-117 µs, below the DS3231M's 300 µs minimum tVCCF; (2) the pulldown only holds 3V3_AUX at 0 V while VMAIN is live, which in sleep is true in USB operation and false on the battery terminal.

**DMG3404L (Q1).** Gate driven at the full pack voltage (about 4.5 V) against a threshold of order 1 V; the threshold rises by roughly 2 mV/K in the cold (generic MOSFET behavior, UNVERIFIED for this part), about 0.1 V at -20 °C. Not a cold weak point. Its only role in the story: the battery-terminal ground return passes through it and the USB return does not.

**ATmega1284P.** CMOS logic speeds up in the cold; the 8 MHz full-swing crystal oscillator starts with a 65 ms delay (SUT = 11) and is robust. BOD at 1.8 V. Nothing here is clock-specific.

**FT231X (U2).** "Extended operating temperature range; -40 to"; "8mA (active-typ) and 125uA (suspend-typ)"; UART pins "Tolerant of 5V input"; "the input pins are pulled to VCCIO via internal 75kΩ (approx.) resistors"; "3V3 output at 50mA".

**Coin-cell holder BT1 (BAT-HLD-012-SMT).** Nickel-plated phosphor bronze per a distributor listing (TE datasheet not opened, UNVERIFIED). The negative contact is the PCB pad. Phosphor bronze stiffens slightly in the cold, so spring force does not collapse; the cold risks are a frost or condensation film (0 °C and windy) and a marginal contact that a reseat cures.

## Candidate causes, ranked

### 1. Coin cell sags below 2.3 V during the DS3231M's temperature conversions (most likely for A and B)
- **Mechanism.** In sleep the DS3231M is on VBAT and draws 575-650 µA for 10 ms every 10 s. A cold CR1220's polarization rises (0.18 V extra at only 95 µA between 20 °C and -10 °C), C19 cannot carry the pulse, and VBAT dips toward or below 2.3 V. Effects: oscillator stall (OSF set, seconds lost), corrupted registers, or a full reset to 01/01/00. A reset clock then misses its alarm (alarm 1 matches date, hour, minute, second), the logger stops until the TPL5010 resets it (R10 = 130 kΩ; the datasheet's table gives 40 min at 104.6 kΩ, so the interval is longer than 40 min, exact value UNVERIFIED), and `clockTest()` then reports `" PASS, BAD TIME"` (Margay.cpp 474-480) with the cyan LED.
- **Evidence.** DS3231M IBATTC, tCONV, 10 s interval and VBAT min (quoted above); Panasonic CR1220 temperature curves; netlist `VCOIN+` = BT1 + C19 + RTC1 VBAT only; Margay.cpp 1006.
- **Explains.** A yes; B yes (a warm cell is the direct remedy, and the replacement was probably also fresher); C **no**: the firmware turns 3V3_AUX off in sleep in USB operation too, so the clock is on the coin cell between readings either way.
- **Likelihood.** High for A and B. The datasheet numbers put a cold, partly used CR1220 right at the edge of the DS3231M's 2.3 V floor, and nothing else on the board stresses the coin cell.
- **Bench test.** Run a logger asleep on battery in a freezer at -25 °C. Scope VCOIN+ DC-coupled with a 10 ms/div window, triggered on a falling edge, for several 10 s cycles, and record the minimum. Repeat with a fresh cell, a half-used cell, and warm. Separately, load a bare CR1220 with 575 µA for 10 ms every 10 s at -25, -10 and +20 °C. Add a read of OSF (0x0F bit 7) after each wake (the firmware never reads it). **Confirms** if VBAT dips below about 2.3 V and OSF sets or the time resets only in the cold. **Kills** if VBAT stays above 2.5 V at -25 °C with a used cell.

### 2. The warm-cell swap was also a reseat and a full RTC power cycle (confound on B)
- **Mechanism.** Pulling the coin cell with the board off removes all DS3231M power: it restarts with defaults and the time is cleared. A marginal or frosted contact is also renewed. Either makes "a warmer cell cured it" ambiguous.
- **Evidence.** DS3231M first-power reset text above; holder contact as above.
- **Explains.** B only.
- **Likelihood.** Medium as a confound; low as the whole story, because the cold is the common factor.
- **Bench test.** In the freezer, remove and reinsert the same cold cell, then swap in a warm cell. If reseating alone cures it, the cause is the contact or the reset state, not cell chemistry.

### 3. Floating 3V3_AUX during battery-mode sleep, pinned to 0 V in USB mode (only candidate on the regulator side that explains A, B and C together)
- **Mechanism.** On the battery terminal, sleep turns off U7 and U8 together (Margay.cpp 1006-1007), VMAIN collapses, and U7's 120 Ω pulldown loses its bias. After that 3V3_AUX is undriven and settles wherever leakage puts it. In USB operation VMAIN stays live from VUSB through U9 IN2, so the pulldown holds 3V3_AUX at 0 V all night. If anything holds 3V3_AUX at an intermediate voltage, then whenever it sits above VBAT (but below VPF) the datasheet rule "powered by VCC" hands the DS3231M to a rail that cannot supply a 575 µA conversion. A cold cell makes this more likely because its VBAT is lower (2.70 V versus 2.88 V at 95 µA, -10 °C versus 20 °C), and leakage falls in the cold, which changes where an undriven node settles.
- **Evidence.** TPS7A05 "RPULLDOWN ... VIN = 3.3 V, P version only 120 Ω"; DS3231M power-control rule; netlist (3V3_AUX feeds RTC VCC, J2 pins 2 and 8, SD, BME280, MCP3421, MAX6070, U4, U5). **UNVERIFIED: I found no on-board source that drives 3V3_AUX up during sleep** (SDA/SCL pull-ups are disabled by `pinMode(16/17, INPUT)`, U5 has partial-power-down inputs, the battery divider is behind U8). The likely source would be the external probes on J2/J3, whose wiring is unknown.
- **Explains.** A, B and C, if a back-feed source exists.
- **Likelihood.** Medium-low. It fits all three observations, but it needs a source I could not find on the board.
- **Bench test.** With the field probes attached, log 3V3_AUX (RTC pin 2) and VCOIN+ through a long sleep on the battery terminal, then on USB from the same pack, at +20 °C and -25 °C. **Confirms** if 3V3_AUX hovers between about 1 V and 2.7 V on battery and sits at 0 V on USB. **Kills** if it is near 0 V in both.

### 4. TLV3691 selects USB input with no USB present, leaving VMAIN dead while awake (explains C cleanly; A partly)
- **Mechanism.** U10 compares `3V3_FTDI` with VBAT_SW/2 (about 2.25 V from three D cells). With no USB cable, `3V3_FTDI` is undriven: no regulator, Q2 off. It can still be lifted by the MCU's idle-high TX through R9 (330 Ω) into the FT231X RXD pin and its "internal 75kΩ" pull-up to VCCIO, and by the aux LED cathode paths into CBUS1/CBUS2. If it rises above VBAT_SW/2, U10 drives EN high and the TPS2104 selects IN2 = 0 V ("5V 0V H -> VIN2"). VMAIN and 3V3_AUX then stay dead while the logger is awake, so the clock runs from the coin cell even during I2C reads (IBATA up to 150 µA), and R15/R16 pull the bus toward a dead rail. The cold pushes the comparator in the wrong direction twice: leakage loads on the undriven node fall, and cold D cells lower VBAT_SW/2. USB cures it outright because IN2 is then live.
- **Evidence.** Netlist (U10 IN+ = 3V3_FTDI, IN- = R17/R18 tap of VBAT_SW, OUT = U9 EN); TPS2104 function table; FT231X pin text; UART TX stays driven during sleep because the USART overrides `pinMode(9, INPUT)` (AVR behavior, UNVERIFIED on hardware). **UNVERIFIED: the voltage `3V3_FTDI` actually reaches with the board on battery.** The back-fed FT231X may load the node enough to keep it low; it would need under about 14 µA of load through 75 kΩ to exceed 2.25 V.
- **Explains.** C fully; A plausibly; B only partly (a warm cell would help the clock survive on VBAT, but not the dead I2C pull-ups).
- **Likelihood.** Medium-low. It would also break loggers at room temperature unless the margin is thin, and those loggers work.
- **Bench test.** Battery terminal only, no USB, logger awake: measure `3V3_FTDI`, U10 OUT (net N$14), VMAIN and 3V3_AUX at +20 °C and -25 °C. **Kills** if U10 OUT is low and VMAIN tracks VBAT in the cold.

### 5. 3V3_AUX falls faster than the DS3231M's switchover allows
- **Mechanism.** The datasheet requires at least 300 µs from 2.70 V to 2.45 V. U7's 120 Ω pulldown on about 6-10 uF gives about 58-117 µs, at every sleep entry. A cold, high-impedance cell is slower to take over the internal supply during the switchover. The consequence of violating tVCCF is not stated in the DS3231M datasheet (UNVERIFIED: register or oscillator upset is the usual concern).
- **Explains.** A and B; not C. In USB operation VMAIN stays up and the pulldown stays biased, so the fall is at least as fast.
- **Likelihood.** Low-medium.
- **Bench test.** Scope 3V3_AUX at sleep entry and measure the 2.70-2.45 V fall time. Cycle sleep thousands of times in the cold with OSF and time checks, with and without a slowed fall (series resistance in the pulldown path or more capacitance).

### 6. The clock alarm cannot wake the logger while on VBAT (frame check, not temperature-specific)
- **Mechanism.** BBSQW = 0 makes INT/SQW high-impedance once VCC < VPF, and VCC is off in every sleep. If that holds for alarm interrupts, wakes would come only from TPL5010 resets (longer than 40 min), each starting a new log file through `begin()`.
- **Evidence.** DS3231_Logger 0x24, 0x05 and 0x06 writes; DS3231M BBSQW text; Margay.cpp 1006.
- **Explains.** None of A, B or C by itself, but it decides whether the clock ever wakes the logger on the coin cell.
- **Likelihood.** Unknown. Loggers are reported to work, so either the alarm does assert on VBAT or 3V3_AUX is not really off.
- **Test.** On the bench (warm), scope INT/SQW and RTC VCC through one sleep interval. Look in field data for many single-line `LogNNNNN.txt` files spaced at the watchdog interval.

### 7. D-cell sag in the cold
- Energizer E95: 150-300 mΩ fresh at 21 °C, rated to -18 °C. Three cells leave about 0.7 V of margin over the TPS79733's 3.5 V floor even with a several-fold IR rise. The same cells feed USB, so this cannot explain C. **Low.** Test: log VBAT+ during an SD write at -25 °C.

### 8. Reverse-polarity FET Q1
- Fully enhanced at about 4.5 V gate drive; the cold raises the threshold by about 0.1 V (UNVERIFIED for this part). Only the battery-terminal path carries ground through it. **Low.** Test: measure VBAT- to GND while awake at -25 °C (expect a few mV).

### 9. Regulators, switches, comparator, MCU and ceramics in the cold
- All are specified to -40 °C (TPS79733, TPS7A05, TPS22916, TPS2104 at -40 to 85 °C; TLV3691 at -40 to 125 °C; FT231X at -40 °C). Dropouts and UVLO thresholds (TPS7A05 1.21-1.37 V) are far from the operating point. X7R and X5R hold ±15 %. **Low**, except as the mechanisms named in 3-5.

### 10. Self-heating in USB operation (weak contributor to C)
- With USB fed from the D cells the FT231X stays powered (8 mA active typical) and dissipates about 36 mW continuously, against near zero in battery sleep. Warming of the enclosure is of order 1-2 K (UNVERIFIED; it depends on enclosure and wind). **Low**, but it acts on the same coin cell as candidate 1.

## What fails first as it gets colder

The CR1220 is the first part to leave its comfort zone. It is the only source on the clock's sleep path, it must deliver 575-650 µA pulses every 10 s with no buffer, and Panasonic's own curves show it losing 0.18 V between 20 °C and -10 °C at a sixth of that current. Every semiconductor on the power paths is specified to -40 °C, and the D cells have volts of margin. The coin cell explains the cold and the warm-cell cure. **It does not explain the USB cure on the firmware as written**, because sleep turns the clock's VCC off in both modes. Only the floating-rail mechanism (3) or the comparator mechanism (4) ties the USB cure to the clock, and both need the bench measurements above. Andy's USB recollection is unwritten (evidence item 2), so the first test should also confirm it: does a cold logger with a cold cell keep time on USB and lose it on the battery terminal?

## Side notes

- Project-Margay README, "Cold-weather deployments" (lines 426-428), says the RTC "is powered exclusively by the CR1220 coin cell" and that CR1220 cells are "rated to −20°C". The netlist puts RTC VCC on 3V3_AUX. Panasonic's CR1220 is rated -30 to +85 °C (Maxell's is -20 °C per a search snippet). This README was not used as evidence.
- The KiCad redesign's C20 (1 uF) and D4 on VBAT do not buffer a 10 ms conversion pulse: that needs about 29 uF for 0.2 V droop.

## Sources

- DS3231M datasheet (scratchpad icreq/txt/ds3231m.txt).
- TPS2104, TPS79733, TPS7A05, TPS22916, TPL5010 (scratchpad cc/dl); TLV3691 (vmain); FT231X (icreq/txt).
- Panasonic CR1220 datasheet, energy.panasonic.com/dam/master/pdf/en/datasheet/lithium/CR1220_Datasheet_EN.pdf (downloaded to jonas/dl/).
- Energizer E95 datasheet, Energizer document via files.batteryjunction.com mirror (data.energizer.com returned 404) (jonas/dl/E95_mirror.pdf).
- Holder material: Farnell listing for BAT-HLD-012-SMT-TR (distributor, not opened).
- Netlist: rtc/eagle.json. MPNs: bomlines/margay2.xml. Firmware: Margay_Library-Wickert-Local-cached20241227/src/Margay.cpp; DS3231_Logger at 850dfbf; board package NorthernWidget avr 0.3.1 boards.txt.

# Margay's clock failing in the cold: a hypothesis tested on paper, and a fix

2026-11-09, for Andy. The observations (Jonas Eschenfelder, SFU, emails of July 2024, and in
conversation): some Margays' clocks failed at about 0 °C in wind; a warmer coin cell fixed them;
powering a Margay through its USB cable, spliced to the same D cells, also stopped the failures.

## The hypothesis, and what the code says

Hypothesis (QUEUE desk item 14): in battery sleep, 3V3_AUX (the DS3231M's VCC) floats because U8
cuts VMAIN and the TPS7A05's 120 Ω active pulldown needs a powered input (SBVS254D §7.3.2), and
the I2C pull-ups back-feed it. The DS3231M runs from VCC whenever VCC is above VBAT, even below
VPF (19-5312, Power Control), so a back-fed rail could beat a cold coin cell.

**The I2C part is refuted.** The 2024 library (Margay_Library-Wickert-Local-cached20241227,
`turnOffSDcard()`) sets `pinMode(16, INPUT); pinMode(17, INPUT);` on SCL and SDA before
`powerAux(OFF)`, and the board package's `pinMode()` clears the pull-up (NorthernWidget AVR core
0.3.1, wiring_digital.c: `*out &= ~bit;`). The current library does the same.

**A stronger path may remain: the SPI pins.** The same function leaves `pinMode(5/6/7, INPUT)`
commented out, writes `SPCR = 0` (MOSI and SCK keep their last state as port outputs), and drives
SD_CS low. A MOSI left high (SdFat ends transfers on 0xFF: from memory, to check) drives the SD
card's DI pin, and through the card's input protection, the card's VDD: 3V3_AUX. A port pin can
source milliamperes, so this back-feed can carry the 3V3_AUX loads (the MAX6070 at 150 µA, the
clock at 130 µA on VCC). Not measured.

**The cold coin cell alone explains the warm-cell fix.** The DS3231M draws 575 µA for 10 ms during
each temperature conversion, also from VBAT (19-5312, p3). A cold CR1220's internal resistance
rises, so those pulses can pull VBAT below the clock's 2.3 V minimum, setting the oscillator-stop
flag. A warm cell holds. This needs no back-feed.

**USB remains unexplained by the code alone.** On USB, VMAIN stays live in sleep (U8 does not
switch USB), so the TPS7A05 is powered and its pulldown is active; that changes 3V3_AUX's state
but by itself does not power the clock. The bench test below should separate the cases.

## Bench test (room temperature first)

1. A Margay running the 2024 firmware, in sleep: 3V3_AUX at C15, VMAIN at C13, MOSI (D5) and SCK
   (D7) levels. Once on battery, once on USB. A few volts on 3V3_AUX on battery would confirm a
   back-feed; MOSI high would name the path.
2. The coin cell replaced by a bench supply through about 100 Ω (to imitate a cold cell's
   resistance), stepped from 3.0 V down: when does the clock stop? Once on battery, once on USB.
3. If a freezer is at hand: the same logger at about -10 °C on a real CR1220.

## The fix

**Firmware, for every Margay in the field (no hardware change):** release the SPI pins with the
I2C pins before 3V3_AUX goes off, so nothing on the core side drives the 3V3_AUX domain. In
`turnOffSDcard()`, after `power_spi_disable();`:

```cpp
  pinMode(5, INPUT);  // MOSI: release, so it cannot power the SD card through its input
  pinMode(6, INPUT);  // MISO
  pinMode(7, INPUT);  // SCK
```

`SPI.begin()` restores them on wake; SD_CS stays low.

**Superseded 2026-11-10, not applied.** Two facts defeat this fix. (1) On v3.0, MOSI, SCK and SD_CS
reach the card only through U5 (SN74AUP3G34, VCC on 3V3_AUX), which "supports partial-power-down
mode" with Ioff at most 0.6 µA per pin at VCC = 0 (its datasheet); MISO is an input. There is no
back-feed path to stop. (2) `SPI.begin()` sets the pins only while its `initialized` count is zero
(NorthernWidget core 0.3.1, SPI.cpp), and SdFat never calls `SPI.end()`, so after the first wake
the pins would stay inputs and the SD card would stop working. To check on the bench: sleep current before
and after, and that the card still mounts on every wake.

**v3.1 hardware, the ALog approach:** feed the clock's VBAT from main power and keep the coin
cell as the last resort. A diode-OR: D4 (BAT43WS, already in the v3.1 KiCad design) from the core
3V3 to VBAT, plus a second Schottky in series with the coin cell (BT1+ to VBAT). While a main
battery is fitted, VBAT sits at about 3.3 V less D4's drop and the coin cell supplies nothing,
cold or not; the coin takes over only when main power is gone. The second diode also stops
D4 from pushing current into the primary cell (desk item 14). Costs: the clock's 2-3 µA of
timekeeping current moves from the coin cell to the main battery (about +3 % of the typical
5-minute deployment's 87.7 µA average); the coin's backup voltage falls by the diode's drop
(the DS3231M runs on VBAT down to 2.3 V). With #66, VSYS stays live in sleep, so the TPS7A05's
pulldown also holds 3V3_AUX at 0 V on battery.

## More broadly: candidate causes (2026-11-09), tracked with the bench test as Project-Margay #69

1. **The USB unplug at deployment, plus a cold cell (the best fit).** The clock is set over USB,
   then USB is pulled. U9 hands over only after VUSB has fallen to about 2 V
   (`margay-vmain-switchover.md`), so 3V3_AUX, the clock's VCC, drops out at the unplug. The
   clock falls back to VBAT at that moment, and a cold CR1220 may not carry it. The spliced-USB
   loggers never see an unplug. This fits the cold, the warm-cell cure and the USB cure.
   **Superseded 2026-11-10** (blind adjudication, `sources/2026-11-10-jonas-cold-adjudication.md`):
   the firmware turns 3V3_AUX off at every sleep (`powerAux(OFF)`, Margay.cpp line 1006 in the
   2024 library, verified), so the clock hands over to VBAT every cycle in both power modes. An
   unplug adds one handover to thousands, and the spliced loggers were also set over USB.
2. **The holder's contact.** "Replacing the pin battery" also reseats it.
3. **Conversion pulses on a cold cell.** These explain the warm-cell cure, not the USB cure.
4. **3V3_AUX slow to rise on wake on battery** (U8, U9, U7 in turn, with a 6 ms settle), against
   the first I2C read. On USB, VMAIN is already live.
5. **The SPI back-feed in sleep.**
6. **Brown-out at 1.8 V** while the ATmega needs 2.7 V at 8 MHz.
7. **Moisture** at the holder or the RTC.

## Keeping the coin cell useful in the cold (Andy: it should still work when it is the last resort)

Each temperature conversion takes 575 µA for 10 ms, 5.75 µC, from VBAT (19-5312). C19 and C20
(about 1 µF) cannot carry it, so the cell supplies every pulse; a cold cell's rising resistance is
what sags. Buffering the pulse at VBAT (droop = 5.75 µC / C_eff):

| VBAT capacitance | Droop per conversion |
|---|---|
| C19 + C20 today (about 1 µF) | the cell carries it |
| 22 µF 0805 (11.5 µF effective at 3.3 V) | 0.50 V |
| two 22 µF 0805 | 0.25 V |
| 100 µF 1206 (about 50 µF effective near 3 V) | 0.115 V |

Proposal: **1 kΩ in series from the cell, and one 100 µF 1206 (the shared C43/VSYS line) at
VBAT.** The capacitor supplies each pulse. The cell refills it through 1 kΩ, at a 50 ms time
constant against the clock's 2-3 µA (a 3 mV drop), and never sees the 575 µA step. The resistor
also limits any current D4 could push into the cell. Two points to weigh:
- **The DS3231M recommends 0.1-1.0 µF on VBAT** when VBAT is the primary source (19-5312, pin
  description). It gives no reason, so this exceeds a recommendation without a known limit.
- **The ceramic's leakage adds to the cell's load.** Murata's guaranteed insulation resistance
  for this class is from memory and to check, and the typical leakage is far lower.

**A supercapacitor is not recommended.** Its leakage of a few µA matches the clock's own
current, and its resistance rises in the cold too.

**Cell chemistry stays the simplest cold fix**: the README already names the BR1220 (to -30 °C)
and the BR1225A (to -40 °C). A larger holder (CR2032 class, lower resistance and about six times
the capacity) is a v3.1 copper option.

## The CR1220 in the cold, and what the buffer buys (agent report, 2026-11-10)

`sources/2026-11-10-cr1220-cold-agent-report.md`. Corrections first: on VBAT the DS3231M converts
"once every 10s" (19-5312), not every 64 s as an earlier line of this work said; the 575 µA,
10 ms pulse averages 0.575 µA, inside IBATT's 2-3 µA.

No maker publishes a CR1220's resistance or pulse voltage in the cold; the limits below are
estimates bracketed from continuous-load curves (Panasonic to -10 °C, Renata and Maxell to -20 °C).
Fresh cell, VBAT at or above 2.3 V through the pulse:

| | Panasonic-type CR1220 | Maxell CR1220 | BR1220 / BR1225A |
|---|---|---|---|
| Unbuffered | about -25 °C (pessimistic bound) to below -40 °C | about -5 °C to -17 °C | about 0 °C |
| Buffered (1 kΩ + BAT43WS + 100 µF) | below -40 °C (2.47 V estimated at -40 °C) | about -34 °C | about -12 to -14 °C |

- The buffer gains about 15-30 °C against the pessimistic bound and little against the
  optimistic one, because the Schottky costs 0.12 V at 20 °C and about 0.27 V at -40 °C. Its larger
  gain is that the clock stops seeing the cell's resistance, which roughly triples by late life
  (Energizer: 45 Ω fresh, 150 Ω near the end).
- **The BR cells are worse here, not better**: about 0.2 V below a CR1220 at the same load, and
  Panasonic rates the BR1220 to -40 °C only at about 9 µA down to 2.0 V, below the clock's 2.3 V.
  The README's advice to fit a BR1220 or BR1225A for cold deployments needs revisiting.
- **The capacitor's leakage is the open risk**: if the 100 µF part carries Murata's usual 50 ΩF
  insulation floor, worst-case leakage is 6 µA at room temperature (UNVERIFIED: the part's own
  specification was not retrieved), which would cut the cell's backup life from about 1.6 to
  0.47 years. Measure one board's VBAT current with main power off before choosing the part; a
  smaller capacitor (two 22 µF) halves the risk at 0.25 V of droop.
- The agent's proposal, unchecked against the schematic: drop D5 and feed the cell through 1 kΩ
  alone, recovering the diode's 0.12-0.27 V, at the cost of the capacitor's leakage drawing on
  the cell while main power is present, and of losing D5's block against reverse current.

## Unbiased agents and blind adjudication (2026-11-10)

Four agents (circuit, firmware, physics, field practice) worked without these notes; a fifth ranked
their lists and ours blind. Reports: `sources/2026-11-10-jonas-cold-*`. The ranking:

1. A cold or worn CR1220 sags under the 575-650 µA, 10 ms conversion pulses (all five lists).
   Explains the cold and the warm-cell cure, not the USB cure.
2. The "warm cell" cure was a new cell, a reseat, a full clock reset and a laptop session.
3. The "USB" recollection may be Jonas's proposed D-cell-to-VBAT rewire (29 July email).
4. The TPS7A05 below-15 °C ramp-down caution, which only the battery path triggers.
5. Pack sag, two cells, or the 1.8 V brown-out setting at wake.
6. U10 selects the dead USB input because 3V3_FTDI is back-fed.
7. Then terminal wiring, a wedged I2C bus, a spurious serial time-set, the 300 µs VCC fall,
   a floating 3V3_AUX, the unplug handover, BBSQW, cold oscillator start, condensation.

Andy, 2026-11-10: the clock reset to 2000 on battery and never after the USB hack. The date
separates two causes: 2000-01-01 is the DS3231M's power-on reset (both supplies lost); 2000/00/00
is `begin()` setting the clock from serial garbage (Margay.cpp lines 225-234, verified).
**Answered, Andy 2026-11-10: Jan 1 2000, the normal reset.** The DS3231M lost both supplies; the
serial time-set is out. Because the clock sleeps on VBAT in both modes, the cell alone cannot be
the whole cause: the reading that fits all three observations is a weak (cold) cell plus a VCC
disturbance that only the battery path makes, such as the TPS7A05 restart at wake or pack sag.
A fresh cell restores the margin; USB removes the disturbance.

### The TPS7A05 caution (SBVS254D §8.1.3, read)

Below 15 °C, IN must ramp down over at least 10 ms and EN over at least 100 µs. Faster, and the next
start is either partial, off and then normal (IN) or delayed up to 130 ms (EN). The 2024 firmware
drops EN on a GPIO edge every sleep in both modes, then turns U8 off (line 1007), which takes
U7's input down on battery only; on USB, VMAIN stays up from VUSB. At wake it allows 6 + 10 ms
(lines 1037-1050). How fast VMAIN falls on battery is not measured: the TPS2104 has no body
diode, but its IN1 switch is on in battery mode and conducts back towards U8's 150 Ω discharge
until its gate drive fails. The chain from a late or glitching 3V3_AUX to a clock reset is
inference. Tests: freezer scope of 3V3_AUX and VMAIN at wake on J3 and on USB; a firmware variant
holding `powerOB(ON)` through sleep. The v3.1.0 VSYS design removes the IN half; the EN half needs
an RC on EN or a longer settle.

### Test order (adjudication)

- T0, free: ask Jonas the failure's appearance (LED, serial text, timestamp form), when it
  showed, whether a laptop re-set each swapped unit and whether it failed again, the cell count,
  what the "USB" wiring was (photo), and whether he kept the cells and SD cards.
- T1, free: his SD data and ours for hourly new log files (the watchdog waking, not the alarm).
- T2, under an hour: on J3 awake, meter 3V3_FTDI, U9 EN, VMAIN; RTC pin 2 in sleep; scope
  RTC_INT across an alarm.
- T3-T5, half a day each: coin-cell emulator with an OSF-reading sketch; a real CR1220 pulsed at
  +20, 0 and -20 °C; freezer scope, J3 against the USB splice.
- T6: inspect failed units as received (register dump, holder, leakage at VCOIN+).


## The clock's supply through one cycle, and what the VBAT changes still buy (2026-11-10)

Battery path, 2024 firmware, three fresh D cells (about 4.5 V). Netlist from the Eagle `Margay.sch`
(U6 core LDO on VBAT+; U8 TPS22916CYFPT VBAT+ to VBAT_SW; U9 TPS2104 IN1 VBAT_SW, IN2 VUSB, OUT
VMAIN; U7 TPS7A0533PDBVR VMAIN to 3V3_AUX; RTC1 VCC on 3V3_AUX; R15/R16 I2C pull-ups on 3V3_AUX;
VBAT on BT1 and C19 0.1 µF only). Times computed from datasheet values; nothing measured.

| Moment | What happens | Datasheet rule | Path |
|---|---|---|---|
| Sleep, t = 0 | U7 EN falls on a GPIO edge (ns) | EN ramp-down ≥ 100 µs below 15 °C (TPS7A05 §8.1.3) | both |
| Sleep, t = 0 | 3V3_AUX 2.70 to 2.45 V in 58-118 µs (120 Ω on 5-10 µF effective); the clock hands over to the cell | tVCCF ≥ 300 µs (DS3231M) | both |
| Sleep, t ≈ µs | U8 off; VMAIN 4.5 to 2.7 V in 61-84 µs through U8's 150 Ω QOD and U9's on IN1 switch; below 2.7 V unspecified (U9's charge pump limit) | IN ramp-down ≥ 10 ms below 15 °C | battery only |
| Sleep, 5 min | Clock on the cell; 575 µA for 10 ms every 10 s; C19 holds 0.1 µC of the 5.75 µC | VBAT ≥ 2.3 V | both |
| Wake, 0-5 ms | U8 tON 1.4-1.7 ms, U9 IN1 rise about 0.34 ms, U7 tSTR 1.5-2.8 ms: 3V3_AUX valid at about 3-5 ms | firmware starts at 16 ms | battery; on USB only U7 |
| Wake, cold | after a fast EN fall: up to 130 ms of delay; after a fast IN fall: partial start, shutoff, normal start | | EN both, IN battery only |

A partial start lifts VCC; once VCC exceeds the cell's voltage (VCC < VPF but > VBAT) the clock runs
from it, and the shutoff then drops it through the 120 Ω pulldown, a second fast handover onto the
cold cell. The battery path makes three handovers a cycle in the cold and the USB path one. The USB
loggers ran the same cells through the same sleep pulses in the same cold without resetting (Andy's
recollection), which argues that the pulses alone do not reset the clock; the handovers do. Inference.

**What the VBAT changes buy now.** The v3.1 KiCad schematic already has D4 (BAT43WS) from 3V3 to
Net-(BT1-+), with no diode in series with the cell (verified from a fresh netlist export): as drawn it
charges a primary lithium cell.
- D4: the fix. VBAT sits near 3.1 V from the core rail whenever the pack is in, every handover lands
  on it, and the cell leaves the loop. Keep.
- D5, a Schottky in series with the cell: now required, to stop D4 charging it. Keep.
- R_BAT 1 kΩ: the second protection element beside D5, and the cell's isolation from C_BUF. Keep.
- C_BUF 100 µF: no longer load-bearing. It serves only when the pack is out (a cold pack swap, a dead
  pack). Its leakage risk mostly goes, because while the pack is in, D4 feeds the leakage and D5
  blocks the cell. It exceeds the DS3231M's 0.1-1.0 µF recommendation. Optional.
  **Superseded the same day: required.** Andy, 2026-11-10: "I want a backup battery for the clock:
  batteries are frequently unplugged in deployment." The pack-out case is routine, and C19 + C20
  (about 1 µF) carry a fresh cell only to about -5 to -25 °C by cell maker; the buffer extends it to
  about -34 °C (Maxell) and below -40 °C (Panasonic-type), per the CR1220 table above.
- C20 out: unchanged.
- Option, unchecked: ground the clock's VCC (Maxim's VBAT-only configuration, Figure 5) so that no
  handover happens at all. Needs the alarm output's behavior in VBAT-only mode checked (BBSQW).

**For the v3.0 boards already built**, firmware cannot stop the IN ramp cheaply: holding U8 on through
sleep costs about 450 µA in the R22/R23 and R17/R18 dividers. A longer settle at wake (about 150 ms,
about 4.3 µA average at 8.6 mA awake every 5 min) covers the 130 ms EN delay for I2C and the SD card
but not the clock's handovers. The hardware fix there is a D4 + D5 rework.

## Decision: the clock runs from main power; the coin cell is the backup (Andy, 2026-11-10)

"I think we need to define the purpose of the clock battery. In the past, it was the main battery
for keeping the clock going. This seems more precarious now. Switching to main power is necessary,
I think." Purpose, as now defined: **while a main pack is connected, the clock runs from main power
(D4 from 3V3 to VBAT); the coin cell keeps time only while the pack is disconnected**, which is
routine in deployment. In v3.0 and earlier the coin cell was the clock's supply through every sleep,
by design: on VCC the DS3231M draws up to 130 µA (ICCS at 3.63 V) against 2-3 µA on VBAT (19-5312).
Parts: D4, D5, R_BAT 1 kΩ, C_BUF 100 µF; C20 out.

Old-design cell life from the arithmetic (clock on VBAT nearly all the time, IBATT 2 µA typical and
3 µA maximum at 3.63 V): 35 mAh lasts 1.3-2.0 years at 3-2 µA and 2.7 years at 1.5 µA; 40 mAh lasts
1.5-2.3 years at 3-2 µA. Loggers that kept time for years are inside this range; the cold failures
needed the cold-only handover behavior on top.

## Does the alarm wake the logger while the clock is on VBAT? (2026-11-10)

Yes. Maxim's errata sheet 19-5311 (DS3231M revision A1, 6/10; text read from the PDF in
`sources/2026-11-10-ds3231m-bbsqw-agent-report.md`'s download) lists as an A1 fault: "DS3231M BBSQW
bit (if = 1) enables SQW and RTC alarm interrupt when operating on VBAT supply. Workaround: Write
BBSQW = 1 if user desires an RTC alarm interrupt during battery operation." So on other revisions the
alarm asserts on VBAT whatever BBSQW is; the datasheet's "high impedance" sentence belongs to the
square wave. The firmware holds RTC_INT high with the MCU's internal pull-up and wakes on a FALLING
edge on INT2, a documented power-down wake source on the ATmega1284P. The TPL5010 resets the MCU
(about every 64 min on v3.0) and cannot produce rows at the set interval.

Proposal: the driver sets BBSQW = 1 in its three control writes (DS3231_Logger.cpp: `begin()` 0x24
to 0x64, Alarm 1 0x05 to 0x45, Alarm 2 0x06 to 0x46), covering any A1 part. With INTCN = 1 there is no
square wave for the bit to enable. #70 does not change this: VCC stays on the switched rail.

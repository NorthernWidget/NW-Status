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

`SPI.begin()` restores them on wake; SD_CS stays low. To check on the bench: sleep current before
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

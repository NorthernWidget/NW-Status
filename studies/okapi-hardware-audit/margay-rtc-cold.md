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

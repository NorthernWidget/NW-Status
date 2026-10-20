# Okapi's eight-cell array: quantity, brightness, autonomy and the part

## Recommendation

**Position is the only new dimension worth building; the rest are either too expensive in current, too fragile, or too poor in bits per second of training.** The PCA9634 (U45) can blink any subset on its own clock with no MCU attention, dim each cell in 256 steps and the whole array in 256 more, but every one of those features needs its 25 MHz oscillator running, and that costs **2.5 mA typical** (Table 18) – **31 times** the README's 80 µA sleep budget. The part therefore reshapes nothing in the field: it is a verdict-window device, awake for three seconds per boot, and asleep (2.9 µA typical at 3.3 V) otherwise. Brightness, count and bar graphs stay out of the first build. One exception worth costing is the first upload after boot, where a hardware-autonomous "breath" on one cell adds 9–23 % to a transmission the Boron is already paying for.

## 1. The PCA9634 as a design resource

Source: NXP PCA9634 product data sheet Rev. 7.1, 18 Dec 2017, fetched today and read from text (register and section numbers are the datasheet's).

| Fact | Value | Where |
|---|---|---|
| Individual PWM | 8-bit (256 steps), fixed **97 kHz**, duty 0–99.6 %, registers PWM0–PWM7 (02h–09h) | 7.3.3, Table 8 |
| Group dimming (DMBLNK = 0) | GRPPWM (0Ah), 8-bit, a **190 Hz** signal superimposed on the 97 kHz; GRPFREQ ignored | 7.3.4 |
| Group blinking (DMBLNK = 1) | GRPFREQ (0Bh) sets period = (GFRQ + 1)/24 s, **41 ms (24 Hz) to 10.73 s**, 256 linear steps; GRPPWM sets duty, 8-bit | 7.3.5, eq. 3 |
| Which cells blink | Only outputs with LDRx = 11 in LEDOUT0/1 (0Ch/0Dh); LDRx = 01 is steady full-on, 10 is individual PWM only, 00 off | 7.3.6, Table 11 |
| MCU-free blinking | Yes: write MODE2, GRPFREQ, GRPPWM, LEDOUT once; the part blinks until told otherwise. Oscillator must be on | 7.3.1 fn 2 |
| OUTDRV (MODE2 bit 2) | 1* totem-pole, 0 open-drain; "normal LEDs can be driven directly in either mode" | Table 7 |
| !OE high | Outputs follow OUTNE[1:0]: 00 → LEDn = 0 (**would light Okapi's LEDs**), 01* → 1 if totem-pole, high-Z if open-drain, 10 → high-Z | 7.6, Table 14 |
| Sink per output | ≥ 17 mA at VOL = 0.5 V, VDD = 3.0 V; each bit ≤ 25 mA, package ≤ 200 mA | Table 18 fn 2 |
| Supply, awake | **2.5 mA typ, 10 mA max** (no load, fSCL = 1 MHz), independent of VDD | Table 18 |
| Supply, SLEEP (MODE1 bit 4) | **2.9 µA typ, 12 µA max** at 3.3 V | Table 18 |
| Wake-up | ≤ 500 µs for the oscillator after SLEEP → 0; PWM/GRP timings not guaranteed inside that window | Table 6 fn 1 |
| In SLEEP | "LED outputs cannot be turned on, off or dimmed/blinked" | Table 6 fn 2 |
| All Call | ALLCALLADR (11h) default **E0h** (7-bit 0x70), enabled at power-up (MODE1 ALLCALL = 1*) | 7.1.2, 7.3.8 |
| Sub Call | SUBADR1–3 (0Eh–10h) default E2h/E4h/E8h, disabled at power-up | 7.1.3, Table 12 |
| Software reset | General Call 0000 0110 | 7.1.1 |

What the Okapi wiring needs (verified in `Okapi.sch` today): each of D10–D18 has its **anode through 220 Ω to 3V3_CORE** (R53, R60, R64, R76–R80) and its **cathode straight to LEDn**, with no resistor on the cathode side. U45's address pins give 1010010 = 0x52, matching. Consequences: (1) current per lit cell is about (3.3 − Vf − VOL)/220 ≈ **5–6 mA** (Vf UNVERIFIED, no part number on the LEDs; an InGaN green at Vf ≈ 3 V would run under 1 mA and read dim); (2) either OUTDRV works, and the power-up defaults (OUTNE = 01, OUTDRV = 1, !OE pulled high by R18) hold every output at 1, so the array is dark at boot; the driver must never write OUTNE = 00; (3) the default All Call at 0x70 ACKs alongside anything else at 0x70 on SDA_OB (a TCA9548 mux lives there by default): clear MODE1 ALLCALL at init – whether Okapi has a 0x70 device is UNVERIFIED.

**Hardware-autonomous displays.** Writing six bytes once gives: any subset breathing or blinking at any period from 41 ms to 10.73 s at any duty, each cell at its own brightness, for as long as the part stays awake. The "transmitting" breath on one cell during the 180 s modem wait (`Okapi.cpp:291`) costs **2.5 mA (part) + 5 mA × 25 % duty ≈ 3.75 mA × 180 s = 675 mA·s ≈ 0.19 mA·h**, against the Boron's 16–40 mA × 180 s = 2880–7200 mA·s (0.8–2.0 mA·h): **a 9–23 % surcharge**. Autonomy buys nothing today, because that wait is a busy loop and the MCU is awake anyway (~10 mA); it would matter only if the wait became a sleep on a FeatherGPIO interrupt, and then the 2.5 mA would be the largest wakeful load after the modem. In the field, with no modem running, 2.5 mA × 24 h = 60 mA·h/day is 31× the sleep budget: no autonomous pattern is ever affordable there.

## 2. Brightness as a dimension

Weber fraction for luminance is 1–2 % under lab conditions, so 256 steps look rich. Three things reduce it to almost nothing: (1) Stevens' power law for brightness (exponent ≈ 0.33) makes a 256:1 range only about six perceptual doublings; (2) a 0603 at 5 mA against a daylight-lit board loses the dim end entirely – in sun the usable levels are **off, dim, bright**, and dim is unreliable; (3) LEDs age and bin differently, and the fixed colours have different luminous efficacies (yellow and red appear far brighter than green at equal current), so "dim yellow" and "bright green" can swap order between boards. Brightness could in principle carry "how long ago" (dimming the band light as a message ages across cycles), but the viewer has no reference against which to read absolute brightness and sees one board at a time.

The current argument closes it: a **1 % duty cell averages 50 µA**, under the sleep budget – but PWM requires the oscillator, so the dim cell's chip costs **2500 µA** to run it. A dim steady cell cannot be the field display. A *full-on* LDRx = 01 cell may hold through SLEEP (the datasheet says the state cannot be changed in sleep, not that it is dropped – UNVERIFIED), at 5 mA ≈ 120 mA·h/day, 62× the budget. Brightness is a never, apart from a single global GRPPWM level to tame glare indoors if the array proves blinding.

## 3. Quantities

What is known when `showVerdict()` runs (first cycle, `run()`):

| Quantity | Known at verdict? | Worth three levels? | Column |
|---|---|---|---|
| Battery voltage | Yes: `readOnBoard()` reads VBeta/VPrime via the ADS1115 before the row | Yes – it is the one number a technician acts on at install (swap the cell) | B, two tall only: yellow/green = below/above the warning line |
| Cycle time / interval | Yes: `keepInterval()` runs before the verdict; `cycleSeconds()` and `_logInterval` | Marginal: CYCLE_OVERRAN and INTERVAL_LENGTHENED already say the two states that matter | C |
| Sensors found of expected | Partly: SENSOR_MISSING is a bit, not a count; `_numSensors` is known; the missing count is not stored | Yes if stored (which of three sensors is dead is the field question) | C, up to three cells |
| Card free space | **No**: nothing reads it, and a cluster scan on a large card takes seconds | Yes in principle, but not before measuring the scan time | A |
| Messages raised | Yes: popcount(`_messages`) | No: the Note column has the list, and "three things wrong" prompts nothing specific | – |

How a quantity coexists with the band: it cannot on the same cells at the same time, because a band display lights one cell per column and a bar lights one to three. The only clean coexistence is sequential (verdict for 3 s, then quantities for 3 s), which doubles the instruction and breaks the fixed window Margay promised. Battery is the one quantity I would consider, and the yellow/green pair in column B already renders it as a two-level bar: BATTERY_LOW lights B1, otherwise B2. That is the band display.

## 4. Count as a dimension

Subitising holds to about four (Kaufman et al. 1949; Trick & Pylyshyn 1994); eight cells with a hole at B3 forces counting and the hole itself reads as a missing light. A count beats a position only when the quantity is ordinal and the viewer compares it to a known full scale – a battery gauge – and even then three cells in a labelled column is the ceiling. Count of *faults* is never better than position of faults.

## 5. D4 and D5

`Okapi.sch` shows D4 is the same common-anode RGB arrangement as Margay's D2: **red and blue cathodes go through 330 Ω to U23 (FT231X) CBUS1/CBUS2**, green through R37 to `ALIVE_LED` (pin 20). D4 is already the USB/serial-side light and lights on cable traffic; its green stays "alive/busy until the verdict". The array changes neither role: D5 is the Margay-compatible verdict a Margay-trained person reads, and the array adds where. Keep the per-row blip on D5: moving it costs a wake, two I2C writes and the 2.5 mA while awake (~0.19 mA·s per row against ~0.1 on D5), it adds traffic to the on-board bus every cycle, and it makes "row written" depend on the bus being alive, which D5 today does not.

## 6. Error and ambiguity

| Dimension | One dead LED | Missing B3 | Upside down | Red/green deficiency |
|---|---|---|---|---|
| Position (column/band) | That column reads "no verdict", which collides with "bus dead"; detectable because the other two columns light | None: B is two tall by design | A and C swap, and the fixed colours are 180°-rotation-symmetric (A3 red ↔ C1 red, A1 green ↔ C3 green), so the *subsystem* is misassigned while the band reads correctly; the hole is the orientation cue | Band also rides on row position; colour is redundancy. GaP green (~570 nm) merges with yellow (~590) for deuteranopes under Brettel/Viénot/Mollon simulation; InGaN green (~525 nm) survives. Wavelength UNVERIFIED |
| Count / bar | Off by one, silently | Column B caps at two | Fill direction inverts | Fine |
| Brightness | Aging alone shifts the level | – | Fine | Fine, but efficacy differs by colour |
| Hardware blink | Fine | – | Fine | Fine |

## 7. Field safety

The standing rule holds. Exceptions costed, with the part at 2.5 mA while awake and ~5 mA per cell:

| Exception | Cost | Against 1.92 mA·h/day sleep |
|---|---|---|
| Breath on one cell, first upload after boot only | 0.19 mA·h once | 9–23 % of the Boron's own transmit; once |
| BAD verdict repeated 3 s each cycle, one cell | 22.5 mA·s/cycle: 9.0 mA·h/day at 1 min, 0.9 at 10 min | 4.7× / 47 % |
| Button press shows the verdict | 127 mA·s per press (all eight cells) ≈ 0.035 mA·h | Negligible; see below |
| Per-row blip moved to array | 0.075 mA·h/day at 1 min | 3.9 % |

There are buttons: **S3 is the log button** on `LOG_INT` (10 k pull-up R45, to IC1 PA3), already handled by `manualLog` in `run()`; S4/S7 are reset, S5 is the Li-ion switch, S6 is the Feather's `!MODE`. A press today writes a row with no verdict. Showing the array verdict on a press is the cheapest exception in the table and the only one that puts a display in front of a person who is certainly looking; it needs a second accumulator, because `_messages` is cleared each cycle. (Note: `NW_Logger.cpp:135` says LogInt is PA4; the Okapi schematic puts it on PA3 – UNVERIFIED which pin number the variant assigns.)

## 8. Verdict

| Rank | Dimension | Bits per unit of training | First build? |
|---|---|---|---|
| 1 | Position: column = subsystem, lit row = band | High: stoplight is overlearned, three columns in the subitising range | Yes |
| 2 | Button-press verdict (worst since boot) | High, zero new vocabulary | Yes, if a boot-persistent set is added |
| 3 | Hardware breath during the first upload | Low but cheap; one new meaning | Optional, second build |
| 4 | Battery as a two-level bar in B | Already the band display | Yes, as it is |
| 5 | Three-level bars (cycle, sensors, card space) | Medium, but needs a second window or a lookup | Not yet; card space never without a measured scan |
| 6 | Count of lit cells | Low; the hole breaks it | Never |
| 7 | Brightness as a carrier | Very low; fragile; needs 2.5 mA to exist | Never |

Driver rules that fall out: wake (MODE1 = 0x00, wait 500 µs), clear ALLCALL, never write OUTNE = 00, LDRx = 01 steady for the verdict, then LEDOUT = 0, SLEEP = 1, PB0 high. The 2.9 µA standby is 3.6 % of the sleep budget and is the only current the array may draw between verdicts.

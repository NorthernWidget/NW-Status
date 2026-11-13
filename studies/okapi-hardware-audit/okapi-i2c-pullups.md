# Okapi's on-board I²C pull-ups (#28 item 5)

Study of 2026-11-13, from the v0.7.0 KiCad netlist (Project-Okapi c7d8c71), Okapi_Library, the NorthernWidget AVR core, and the datasheets in the audit's text extracts. Andy asked whether the ATmega's internal pull-ups would do, or pull-ups on a rail that switches on and off with the chips.

## What pulls the bus up today

SDA_OB and SCL have no discrete pull-up. Three things can pull them high:

| Source | Rail | Value | On when |
|---|---|---|---|
| U26 TXS0102 (to the 5 V DAC and ADC), internal | 3V3_CORE_ISO | 10 kΩ | 3V3_AUX is on (U39 switches 3V3_CORE onto 3V3_CORE_ISO, enabled by 3V3_AUX) |
| U34 TXS0102 (to the Particle module), internal | 3V3_CORE | 10 kΩ | PARTICLE_3V3 is on (its OE) |
| ATmega1284P internal pull-up, set by `Wire.begin()` | 3V3_CORE | 20–50 kΩ (RPU, DS40002070B) | from `Wire.begin()` on, including sleep |

TXS0102 datasheet §7.3.5: each port has "an internal 10kΩ pullup resistor", and "The internal pull-ups of the TXS0102 are disabled when the OE pin is low." NorthernWidget AVR core 0.3.1, `libraries/Wire/utility/twi.c` lines 75–77: `twi_init()` sets `digitalWrite(SDA, 1)` and `digitalWrite(SCL, 1)`, and only `twi_disable()` clears them.

## When the firmware uses the bus

Only while 3V3_AUX is on. `beginBoard()` calls `powerAuto()` before its first I²C call. `sleepNow()` turns the rail off in `turnOffSDcard()` (`powerAux(OFF)`) just before `sleep_cpu()`, and turns it back on in `turnOnSDcard()` (`powerAuto()`) just after. No interrupt handler uses the bus.

## Option 1: the ATmega's internal pull-ups alone

Not enough. The rise time asked by standard mode (100 kHz) is at most 1000 ns, and an RC rise from 30 % to 70 % takes 0.8473 RC.
- SCL carries 14 chip pins and 187.4 mm of track, and SDA_OB 12 pins and 134.0 mm (measured from the board).
- The pin capacitances read from the datasheets are 5–10 pF (ATmega 10, DS3231M 10, PAC1934 10, PCA9634 10, MB85RC 8, BMA456 5, TXS0102 10). BME280, MLX90393, VEML6030, MCP23018 and TCA9406 are not stated in the extracts. Taken at 10 pF each, with 1 pF/cm of track (UNVERIFIED), SCL is about 160 pF (an ESTIMATE).
- At 160 pF, 20–50 kΩ gives 2.7–6.8 µs. A pull-up must stay under 1000 ns / (0.8473 × 160 pF) = 7.4 kΩ.

The internal pull-ups also sit on 3V3_CORE, which stays on in sleep (below).

## Option 2: pull-ups on a rail that switches with the chips

This is what both boards already do, Okapi implicitly and Margay explicitly:
- Okapi: U26's internal 10 kΩ to 3V3_CORE_ISO. That is 10 kΩ against a 7.4 kΩ estimate. The TXS0102's one-shot edge accelerators drive rising edges once they start, which is what the design relies on.
- Margay: R15 and R16, 10 kΩ from SDA and SCL to 3V3_AUX.

A rail that switches with 3V3_AUX matters because five of Okapi's on-board chips lose their supply in sleep: DS3231M (it keeps running on BT1), BME280, MLX90393, BMA456 and VEML6030. Their datasheets on driving a pin with the chip unpowered:
- BME280: "It is prohibited to keep any interface pin (SDI, SDO, SCK or CSB) at a logical high level when VDDIO is switched off. Such a configuration can permanently damage the device due an excessive current flow through the ESD protection diodes."
- BMA456: "if the VDDIO supply is switched off, all interface pins (CSB, SDX, SCX) must be kept close to GNDIO potential."
- MLX90393: digital I/O maximum min(4, VDD + 0.3) V.
- DS3231M: any pin −0.3 to +6.0 V (powered from its battery).
- TXS0102 and SN74LVC1G3157: Ioff partial-power-down, ±1 µA.

A pull-up to an always-on rail would hold these pins high in sleep, which the BME280 and the BMA456 forbid.

## What the study found: the firmware breaks this in sleep

Neither library calls `Wire.end()` before cutting 3V3_AUX. The ATmega's internal pull-up therefore holds SCL (IC1 pin 19) toward 3V3_CORE through the whole sleep, against the chips listed above, whose supply is off. The current is set by what back-powers through their protection diodes. The internal pull-up bounds it at 3.3 V / 20 kΩ = 165 µA per line. The real value has not been measured.
- Okapi: SCL reaches the unpowered chips directly. SDA reaches only U24's A pin, whose supply (3V3_AUX) is off.
- Margay: the same firmware path (`powerAux(OFF)` in `turnOffSDcard()`, Margay_Library line 601), and here the internal pull-ups on SDA and SCL also feed R15 and R16 into 3V3_AUX. Margay's published sleep current is 1.68 µA. If that was measured with this firmware, the back-powered current there is small, because the rail floats up until its loads balance. Whether it was is UNVERIFIED.

Fix, in both libraries: `Wire.end()` before `powerAux(OFF)`, and `Wire.begin()` after the rail is back. With the pull-ups off, SDA_OB and SCL sit near 0 V in sleep, held by the unpowered chips' protection diodes and leakage. That is a valid low level for the four chips that stay powered (MCP23018, PAC1934, FRAM, PCA9634), so their inputs do not float mid-rail. This is reasoning from the datasheets, not a measurement.

## Proposal for v0.7.0 (values are proposals)

1. Add two pull-ups from SCL and SDA_OB to 3V3_CORE_ISO, the rail of U26's existing pull-ups, which turns on and off with 3V3_AUX. 4.7 kΩ brings the estimated rise to 0.64 µs without leaning on the TXS0102's accelerators. 10 kΩ matches Margay's R15 and R16 and an existing line, but stays above the 7.4 kΩ estimate. The lower bound is (3.3 − 0.4) V / 3 mA = 967 Ω. TI notes that lower external pull-ups raise the TXS0102's output-low level (§7.3.5).
2. The firmware fix above, in Okapi_Library and Margay_Library.
3. Keep the board check from #28: an I²C scan of the on-board chips with 3V3_CORE_ISO on and off, plus a sleep-current reading before and after the firmware fix.

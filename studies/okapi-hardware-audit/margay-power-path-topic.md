# Topic to consider: Margay's power path, USB supply against sleep current

2026-11-09, for Andy. Background: `margay-vmain-switchover.md`.

## The question

Is it worth adding to the logger's sleep current so that USB can power the whole board?

## As built

- The core 3V3 (the ATmega, the LEDs, the RTC's feed through D4) comes from U6, whose input is
  the battery alone. On the bench with a battery fitted, the core runs from the battery even
  while USB is plugged in; USB carries only the switched 3V3_AUX (SD card, J2, the RTC's VCC).
- With no battery, the core runs from the FT231X's internal regulator through Q2: "a maximum
  current of 50mA", meant mainly for the USB transceiver. The README's "Make sure battery power
  is applied" reflects this.
- The USB-to-battery handover on 3V3_AUX happens late (VMAIN falls to about 2 V at every unplug).
  This is fixable without touching the core: U10 watches a VUSB divider (two resistors and a
  1 MΩ feedback resistor), with no added sleep current.

## The alternative

A selector upstream of both regulators makes one system rail from USB (preferred) and the
battery, with reverse blocking on both. USB then powers everything, the FT231X no longer
carries the core, and the handover becomes the selector's job. The cost is the selector's
quiescent current, which adds to the sleep current that Margay publishes as 1.68 µA:

| Option | Added sleep current | USB powers the core | Clean handover |
|---|---|---|---|
| Re-point U10 (no new part) | 0 | no (50 mA FTDI path without a battery) | yes, with a bulk capacitor on VMAIN |
| Two LM66100 ideal diodes | about 0.3 µA (150 nA typical each), about +18 % | yes | yes, if USB priority works through the CE pins |
| TPS2116 power mux | 1.32 µA typical, about +79 % | yes | yes, priority mode built in |

Figures are from TI's product pages. The datasheets, the 1.68 µA itself, and the logger's
average current (sleep against wake) are not checked here.

## What would decide it

1. How often a Margay runs on USB alone, or on the bench where a battery drains while USB is
   present, against how long a deployment runs on its battery.
2. How much of a deployment's energy is sleep. If wake cycles dominate, 0.3 µA is lost in the
   noise; if the logger sleeps nearly always, it is about a sixth of the budget.
3. Whether the RTC conversation (QUEUE, desk item 14) wants a system rail anyway, to feed the
   RTC's battery input from main power as the ALog did.

## A typical deployment (Andy, 2026-11-09)

Measure every 5 minutes for about 3 s and sleep the rest. Awake, the logger alone draws 8.6 mA,
and sensors typically add up to 20 mA. Average current, with the published 1.68 µA sleep
current (not measured here) and each selector's typical quiescent current added during sleep:

| Interval | Awake load | Average | Sleep's share | +0.3 µA (LM66100 pair) | +1.32 µA (TPS2116) |
|---|---|---|---|---|---|
| 5 min | 8.6 mA | 87.7 µA | 1.9 % | +0.34 % | +1.49 % |
| 5 min | 28.6 mA | 287.7 µA | 0.6 % | +0.10 % | +0.45 % |
| 60 min | 8.6 mA | 8.8 µA | 19.0 % | +3.39 % | +14.91 % |
| 60 min | 28.6 mA | 25.5 µA | 6.6 % | +1.17 % | +5.17 % |

At 5 minutes the awake cycles carry 98 % or more of the energy, and either selector is lost in
the noise. The selector's cost appears only at long intervals with light sensors, and even
there the LM66100 pair stays near 3 %.

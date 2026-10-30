# Okapi's LEDs: a design note

## Recommendation

**The "bar" is not a bar.** The eight LEDs are a 3×3 grid with one cell empty, each LED a fixed colour, and the documentation layer draws three vertical boxes around them: three stoplight columns, A and C three tall (green/yellow/red), B two tall (yellow/green). That geometry settles the design: **one column per subsystem group, and the lit LED within a column is that group's band** – `NW_BAND_FINE/CAUGHT/BAD` rendered as green/yellow/red by the part itself. All three columns light at once for the three-second verdict window, steady, while D5 plays Margay's rhythm unchanged. The bar adds *where* and *all of it*; D5 keeps *which* and *how bad*, and is the only indicator that can say the on-board bus is dead. No new rhythms. Nothing in the field except the existing 20 ms blue blip on D5, with one option for Andy below.

The healthy picture is a geometric accident worth building on: the three greens (A1, B2, C3) are collinear – a rising diagonal – and the two reds (A3, C1) are the ends of the falling one. A good boot draws one line; any fault breaks it.

## Layout, measured (`Project-Okapi/Hardware/Okapi.brd`, mm, +y up)

Reading orientation is the one in `Documentation/images/Resnik_v040_top_annotated_interior_20200428.png` and the one all tDocu text is set in: power terminals and USB-C (J10 at 6.35, −1.14) at the bottom, SD slot (SD1 at 0.76, 82.17) upper-left, Feather socket and cell module at the top. Board 64.75 × 135 mm.

| Column (x) | Row 3 (y 49.022) | Row 2 (y 46.99) | Row 1 (y 44.958) |
|---|---|---|---|
| A (35.814) | D18 red = LED7 | D17 yellow = LED6 | D16 green = LED5 |
| B (38.481) | – (empty) | D13 green = LED3 | D14 yellow = LED4 |
| C (41.148) | D10 green = LED0 | D11 yellow = LED1 | D12 red = LED2 |

Pitch 2.667 mm across, 2.032 mm up; the whole array is 5.3 × 4.1 mm. Channel map from `Okapi.sch` nets N$25, N$67, N$70–N$75 (D10→LED0 … D18→LED7). Colours are the schematic part values (`LEDGREEN0603` etc.); **the BoM (`Okapi_BoM.csv`) predates the array** – it lists D6/D7 as LM4040 and has no U45 or D10–D18 – so which colours were actually placed on built boards is UNVERIFIED. The array arrived in commit 7dc65e8 (2024-10-30). Labels "A B C" (y 51.94), "1 2 3" (x 34.16), "STAT" under D5 and "AUX" beside D4, plus the three column outlines, are all on layer 51 (tDocu), not 21 (tPlace); whether the fab printed them is UNVERIFIED.

D5 (status RGB) sits at (31.37, 58.17), 7 mm left and 11 mm above the array; D4 (aux) at (10.54, 21.08) in the bottom-left corner beside the USB-C; U45 at (41.02, 40.64) directly below the array. Pins verified against `Arduino_Boards/NorthernWidgetAVR/variants/NW1284p/pins_arduino.h` and the schematic: 13/14/15 = PD5/PD6/PD7 = LED1/LED2/LED3 = D5 red/blue/green; 20 = PC4 = `ALIVE_LED`; **0 = PB0 = `!LED_EN`**, pulled to 3V3 by R18 (100k).

**A collision, independent of the design:** `Okapi.h:206` sets `ADC_Sense_SW = 0` and `Okapi.cpp:189–198` drives it HIGH and LOW around every battery read. The v1.0 schematic has no such switch on IC1; this is a Resnik leftover that now toggles the bar's `!OE`. Harmless today (LEDOUT powers up all-off) but the renderer must own pin 0 and the stale define goes.

## The vocabulary

| Condition (band) | Bar | D5 | Aux (D4) |
|---|---|---|---|
| boot, before verdict | dark, `!OE` high | dark | green steady |
| READY (FINE) | A1, B2, C3 green: the rising line | blue chirp 1000/300/100/100/100 | off |
| card missing/unreadable/write failed (BAD) | A3 red; other columns show their own band | red flutter 60/60 | off |
| ROW_NOT_WRITTEN, NOTE_TRUNCATED, NEW_FILE | A2 yellow / A2 yellow / A1 green | amber 500/500 ×3 (if worst) | off |
| BATTERY_LOW, ONBOARD_MISSING, PAGE0_INVALID (CAUGHT) | B1 yellow | amber ×3 (if worst) | off |
| CLOCK_NOT_SET (BAD) | C1 red | red syncopation 250/100/100/100 | off |
| NO_SCHEDULE (BAD) | C1 red | solid red 3 s | off |
| SENSOR_MISSING (BAD) | C1 red | eight pips 100/300 | off |
| CYCLE_OVERRAN, BACKUP_WOKE, BME_MISSING (CAUGHT) | C2 yellow | amber ×3 (if worst) | off |
| on-board I2C dead | dark (cannot show) | whatever D5 renders – the clock shares that bus, so syncopation | off |
| field, per row written | dark | 20 ms blue blip | off |

Within a column the highest band present lights; the bar stays steady for the window and goes dark with D5. Column B has no red, and the power/identity messages have no BAD member, which is why power is B.

## Why, per choice

- **Parallel, not a sweep.** At 0.4 m the 2–2.7 mm pitch is 0.3–0.4° per step, well inside the short-range apparent-motion range, so a chase *would* read as motion (Wertheimer's beta movement; Korte's laws put the optimal ISI near 30–60 ms at this separation). But motion is a preattentive *attractor* (Treisman; Nakayama & Silverman 1986), not a carrier of content: a three-step chase conveys one bit, direction, and it spends the one thing the grid has that D5 lacks, simultaneity. The design's known loss is that `worstMessage()` hides a second fault; three steady columns repair exactly that.
- **Position as identity, colour and height as severity, rhythm on D5.** Location is encoded automatically (Hasher & Zacks 1979) and a lit light among dark ones is a feature search. The column outlines group by common region (Palmer 1992), three groups of ≤3 – inside the subitizing limit (Kaufman 1949), so nothing is counted.
- **Redundancy for red/green deficiency.** The LED colours are fixed, so the renderer cannot drop colour; the *position* within a column carries the band as a traffic light does for deuteranopes. The inverted columns (A green at bottom, C green at top) break the "top = bad" rule, but they buy the collinear line: good continuation is detected preattentively (Field, Hayes & Hess 1993) and a break in it pops out. That is Margay's "form carries the meaning" moved into space, and it reads in sunlight better than any flicker because a steady 3 s light integrates where a 60 ms pulse from a 0603 at ~6 mA does not.
- **One rhythm, not two.** The bar does not blink. Two rhythms compete for attention and are the start of alarm fatigue; D5 keeps the overlearned Margay set, the bar is still.
- **Fewer, not more.** Okapi needs no rhythm Margay lacks. The D5 rhythm disambiguates inside column C (syncopation = clock, pips = sensor, solid = schedule), which is compatibility by construction: a Margay user reads D5 and the bar tells them where to look.
- **Column order, left to right, is check order.** A = the record (card outranks everything, as the BAD order says), B = power, C = time and sensing. Nothing on the board is adjacent to the array, so proximity to the SD slot is not available as a cue.

## Two decisions for Andy

**1. The column groups.** Proposal: A = card and file (`CARD_*`, `ROW_NOT_WRITTEN`, `NOTE_TRUNCATED`, `NEW_FILE`); B = power and identity (`BATTERY_LOW`, `ONBOARD_MISSING`, `PAGE0_INVALID`, all CAUGHT – which is what a redless column can show); C = time and sensing (`CLOCK_NOT_SET`, `NO_SCHEDULE`, `SENSOR_MISSING`, `CYCLE_OVERRAN`, `BACKUP_WOKE`, `BME_MISSING`). The alternative is C = sensors only with the clock folded into A as "a row with no time is a bad row". I hold for the proposal because a technician's action for the clock (bring a laptop) differs from the card (reseat) and D5 already separates clock from sensor. Note: if a BAD power message is ever added, B cannot show it.

**2. The field.** Default: nothing, as on Margay. The one state worth costing: `Okapi.cpp:291` blocks up to 180 s waiting on `FeatherGPIO` for the modem, so the MCU knows telemetry is in progress. One LED is ~6 mA (220 Ω from 3V3, Vf ~1.9 V – estimated, not measured) against the Boron's 16–40 mA (README) – a quarter of the transmit cost, for the one moment somebody *is* watching: the first upload after install. Option: light C2 during the first transmission after boot only, never after. Whatever is chosen, the driver must set MODE1 SLEEP and raise `!OE` between uses: the PCA9634 draws 2.5 mA typical awake and 2.9 µA in standby (datasheet Table 18), and 2.5 mA is thirty times the README's 80 µA sleep budget.

## Testable, and what the driver needs

NW-Sim has no Okapi board model. A bar trace needs (1) a PCA9634 model at 0x52 recording MODE1/MODE2/LEDOUT0/LEDOUT1 writes with ms timestamps, (2) the PB0 edge on the existing pin-trace path, (3) a decoder from LDRx bits to "A1 on" via the channel map above, emitting a `.leds`-style file. Short of that, the host Wire stub can assert the exact byte sequence per verdict. The driver: MODE1 = 0x00 (wake; 500 µs before outputs are valid), optionally MODE2 OUTDRV = 0 (open-drain, the datasheet's recommendation for direct LEDs), LEDOUT0/1 with LDRx = 01 per channel, PB0 low; then LEDOUT = 0, SLEEP = 1, PB0 high. No PWM needed. Group blink (GRPFREQ, 41 ms–10.73 s) exists in hardware if a field display is ever wanted without MCU attention.

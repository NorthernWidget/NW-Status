# Okapi's eight-cell array: five design notes (2026-10-20)

Five read-only agents studied the array independently. The first measured the
hardware and proposed three steady stoplight columns. The other four were sent
to argue for other ideas: alphanumeric glyphs, motion, 1D and 2D liftings of
Margay's 0D rhythms, and the dimensions those three miss (brightness, quantity,
count, and what the PCA9634 itself can do). Read them in order.

| Note | Angle | Verdict on its own idea |
|---|---|---|
| `1-columns.md` | hardware, three columns | the frame: one lit cell per column, steady, 3 s |
| `2-lifting-0d-to-2d.md` | rhythms in space | keep columns; blink the worst column's cell in lockstep with D5 |
| `3-motion.md` | moving flashes | reject for the verdict; a green diagonal shuttle during the modem wait |
| `4-glyphs.md` | shapes and letters | no alphabet; add a lamp test and PWM equalisation |
| `5-part-brightness-quantity.md` | datasheet, brightness, bars, buttons | position only; a button-press verdict; nothing autonomous in the field |

## What all five agree on

The grid is a 3×3 with the top-middle cell empty and fixed colours (green,
yellow, red) in three columns. Its one gain over Margay's status LED is
simultaneity: it can show two faults at once where `worstMessage()` shows one.
Every proposal that spends that simultaneity (a sweep, a glyph sequence, a tape,
a fill) loses to the columns, and Margay's rhythms cannot be turned into motion,
because rhythm lives at gaps above 200 ms and motion below 100 ms. The all-green
rising diagonal (A1–B2–C3) is the READY picture whichever way it is derived.

## Additions that survived

1. **Lamp test**: all eight cells lit while the aux LED says busy, before the
   verdict. The PCA9634 cannot detect an open LED (note 4).
2. **Per-channel PWM equalisation**: each LED has its anode through 220 Ω to
   3V3_CORE, and green's forward voltage is about 1 V higher than red's, so the
   green cells will run dim at equal register values. Measure on a built board
   (note 4, note 5).
3. **Lockstep cell**: the lit cell of the worst column plays D5's rhythm on the
   same milliseconds. Common onset binds the two lights into one event (note 2).
4. **Button-press verdict**: S3 (the log button, PA3, `LogInt = 27`) is the one
   field moment with a certain observer. Showing the worst message since boot
   on a press needs a second accumulator, because `_messages` clears each cycle
   (note 5).
5. **Driver rules from the datasheet** (note 5): MODE1 = 0x00 and 500 µs before
   outputs are valid; never write OUTNE = 00 (it lights every cell when !OE is
   high); clear ALLCALL; LDRx = 01 for the verdict; then LEDOUT = 0, SLEEP = 1,
   PB0 high. Awake the part draws 2.5 mA, 31 times the 80 µA sleep budget;
   asleep 2.9 µA. Nothing autonomous is affordable in the field.

## Hazards found

- The colour layout is symmetric under a 180° turn, so a board read upside down
  swaps columns A and C. Only the empty cell and the board's own shape cue the
  orientation (notes 2, 4, 5). The A B C labels are on tDocu, not tPlace.
- `ADC_Sense_SW = 0` in `Okapi.h` drives pin 0, which is now the array's !OE
  (note 1). The define goes when the renderer takes the pin.
- Okapi's first telemetry push runs after the fifth row (`_logCountPush = 5`),
  not at boot, so no "transmitting" display has an observer today (note 3).
- `NW_MSG_BATTERY_LOW` is defined and raised nowhere, as expected while the
  battery messages wait on the four bench readings (note 2).

## Rejected, with the reason

Glyph alphabets (below the 3×5 legibility floor, and no top-centre cell means no
arrows); motion for the verdict (one bit, direction); timelines, tapes and fills
(the rhythms need 16–50 cells, and a fill lies with one dead cell); bar graphs
(no measured quantity worth three levels, and Okapi has no battery percentage);
brightness (unreadable in sun, and PWM needs the 2.5 mA oscillator); count (the
hole breaks subitising).

## Second round (2026-10-21): does each light earn its place?

Andy's question on the first design: "Are you using the extra LEDs because
they add information, or because they are there?" Three more studies answer it.

| Note | Angle | Verdict |
|---|---|---|
| `6-cognitive-science.md` | alarm fatigue, redundancy, dark board, glance capacity | no fine cells; no second light blinking with the first; dark grid when healthy; lamp test is the price of dark-means-fine |
| `7-standards-and-practice.md` | IEC 60073, MIL-STD-411F, ISA 18.2, IALA E-110, FAA 25.1322, PLC/storage/network/battery-pack practice | fine-beside-fault splits by observer (monitor dark, technician lit); lamp test yes; one synchronised rate at most; press-to-show is the field convention; rhythm over count |
| `8-margay-audit.md` | every Margay LED decision from queue, code, tests and traces | Margay's LED is a pointer to the file: one worst message, as a shape, in 3 s, to a person who is there. What it cannot say: a second fault, and bus-dead versus clock-dead |

The design that follows: D5 and aux identical to Margay; all eight cells lit
while aux says busy (lamp test); in the verdict window only fault cells lit,
steady, no green, nothing blinking; dark otherwise. The grid's two gains are
the hidden second fault and the bus-versus-clock case, where B1, C1 and C2
light together.

Housekeeping the audit found: the queue's message table is stale against
`NW_Message.h` (13 of 20); `NW_Logger.h` still documents `note()` as "an
orange pulse on the LED" and `ORANGE` is unused; the first row's blip plays
94 ms before aux-off; the chirp is ALog's 1000/300/100/100/100, not Margay's
2021 651/300/100/200/100, and nobody recorded choosing. "Blue because of
red/green deficiency" is Andy's (this session, 2026-10-09: "population
stereotypes: blue good, not green (red/green colorblind)") and is not yet in
the queue.

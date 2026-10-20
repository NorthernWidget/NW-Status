# Handoff: the LED vocabulary (item 1)

Written 2026-10-20 for the next session. Andy's three to-dos were (1) the LED
vocabulary, an easy advance and the one assigned to me, (2) the DS3231 absolute
alarms, which are his, and (3) the watchdog, now filed as Project-Margay#61. This
file covers item 1 and the frame around it.

The design rationale is in `QUEUE.md` under **"Logger messages and the LED
vocabulary, settled (Andy, 2026-10-09)"**. Read that before changing any of it:
the shape was argued out at length and one earlier attempt went wrong by forcing
these messages into the sensor Report register's number space.

---

## Done, and verified

Picked up 2026-10-20 by Fable 5.1, same day. Steps 1, 2, 3(a), 3(b) and 4 are
built and committed; HEADs `NW_Logger` a51aee7, `Margay_Library` 6a168ca,
`Okapi_Library` da69d00, `NW-Sim` 37345c4.

- **`NW_Logger/src/NW_Message.h`** – eighteen messages now: the sixteen, plus
  `CLOCK_SET` (FINE; the stamp over the serial line had nowhere else to go) and
  `CARD_UNREADABLE` (BAD; a card that is inserted and will not mount, which set
  only the aggregate `_onBoardError` and reported nothing). The set is a
  `uint32_t` with a `static_assert` holding the list to 32.
- **A recursion bug in the code the first handoff called done.** `raise()` on a
  full Note buffer called `raise(NW_MSG_NOTE_TRUNCATED)`, which printed into the
  same full buffer, truncated again, and recursed without bound. Found by reading
  the body – the host harness does not link `NW_Logger.cpp`. A full buffer now
  sets the bit directly.
- **The boot verdict.** `ledReport()`'s colour blocks and the unconditional
  `blinkGood()` are gone. `run()` turns the aux LED off and calls `showVerdict()`
  once the first row is on the card; `printReadyToLog()` is the one Serial line
  that remained. Boot is two seconds faster, which moved the first row's
  timestamp from :03 to :01 in the transcripts and nothing else.
- **The self-tests raise where they detect**, at the branch and not on the flag
  – because the flags aggregate (`_sdTestFailed` is set by a missing card, an
  unmountable card and a failed write test alike). Seven sites in
  `NW_Logger.cpp`, `BME_MISSING` in each board. The write test raises once after
  its loop, not per mismatched byte.
- **The four notice latches raise too**: `LOG_STARTED` and `ROW_NOT_WRITTEN` in
  each board, `NEW_FILE` and `CLOCK_SET` in `NW_Logger.cpp`. The chip-addressed
  `_pages.latch*()` calls stay beside them, commented as pending the decision
  below.
- **`margay_missing`**, a seventh NW-Sim case: `Programmed_Margay` with no Apis on
  the bus. Its transcript shows `Fail At: 41`, `Note: SensorMissing`, and a first
  row whose Note field reads `SensorMissing;LoggingStarted;NotAnswering`. Shown
  to bite: removing the one `raise()` fails the case. Nothing had exercised a
  raise before it.

## Reviewed, and the findings fixed (2026-10-20, later)

An independent review of the design and the code found the shape sound and six
things wrong with my implementation of it, all verified against the code and all
fixed in the same session. `NW_Logger` 546d5af, 3745cfc, 6e35db0, 3edaa52,
ada0d6a, 4d8d525; `NW_Core` da46f8a; `Margay_Library` 7db9ee8; `Okapi_Library`
f366d8f. Seven NW-Sim transcripts stayed byte-identical throughout, which is the
correct result for healthy simulated boards.

1. **A CAUGHT-only boot showed nothing.** `signal()` returned for any message
   without a pattern of its own, so a dead BME280 – which still logs – left the
   status LED dark after the aux went out. The default now renders by band:
   amber slow for CAUGHT, solid red for BAD, nothing for FINE.
2. **`NO_SCHEDULE` could not reach the verdict.** `keepInterval()` ran only from
   the alarm branch; the first row was written unmeasured. The first cycle is now
   timed, and the alarm re-armed only if that lengthened the interval.
3. **No card: no rows on the terminal, and the Note buffer grew without bound.**
   `logRow()` returned before the echo and the clear. Both now happen regardless.
4. **The per-row blip** the design asked for is in: 20 ms of blue when a row
   reaches the card. **The message set is cleared per cycle**, as documented.
5. **The card outranks the clock.** `worstMessage()` shows the first message of
   the highest band, so the order within BAD is a rule; it is now card, then
   `NO_SCHEDULE`, then sensor, then clock – ordered by how little the data file
   can tell you – and the comment claiming order was not relied on is gone. The
   harness prints the whole table, so a reorder that moves the enum and not the
   table shows as a word beside the wrong value.
6. **Two conditions gained words**: `ONBOARD_MISSING` (the battery ADC on
   BUILD_B/C, after which `batTest()` read 0 V in silence) and `PAGE0_INVALID`
   (a fresh flash). Twenty messages. And `Serial.begin()` now precedes the BME280
   init on both boards, so its failure line can reach a terminal.

One fact from the review bears on the Report-register decision below: dropping
the served byte also empties the logger's `Code` column in its own status-file
boot row, not only the backhauled page.

## Tested, and what the tests found (2026-10-20, later still)

Andy asked for unit tests covering the capabilities and a safe sequence. What now
exists, each shown to fail without the code it guards:

- **The verdict's choice is pure and tested.** `nwWorstMessage(set)` lives in
  `NW_Message.h`; the host harness tries thirteen sets, and the line that
  matters – "no card AND clock not set → CardMissing" – flips to ClockNotSet
  when the band comparison is broken. (`NW_Logger` 57696d5)
- **The LED story is a tested artefact.** The Margay board model traces its four
  LED pins with millisecond timestamps (`NW-Sim` 6c49312); run.sh lifts them into
  a `.leds` file per case and diffs it like the transcript (b7a37af). So the boot
  sequence a person sees – aux out, then the status LED's rhythm, after the first
  row is on the card – is asserted: in `margay_basic` the aux goes out at 1992 ms
  and blue comes on at 1993, then 1000/300/100/100/100 to the millisecond, then a
  20 ms blip on every row.
- **Three boots the firmware must report**, each a case: `margay_nocard` (red
  flutter, 60/60, rows still reaching the monitor, the Note not accumulating),
  `margay_blank` (Page0Invalid, amber), `margay_overrun` (NoSchedule, solid red
  for exactly 3000 ms). The runner gained `nocard` and `nostored` words. Nineteen
  OK in all: nine transcripts, nine LED stories, and "both ways".

**What the LED trace found on its first recording:** red never moved after boot in
any case, while a bare sketch toggling the same pin reported every edge. The cause
was in `LED_Color()`, Bobby's, for years: `255 - (red * lum) / 0xFF` in `int`,
which is 16 bits here, so full brightness overflows to a level of 257 and
`analogWrite()` takes its PWM path – Timer1's red sticks, Timer2's green and blue
run at 1/255 duty. `blinkGood()` was bright only because it wrote the pin
directly, and the old green all-clear was the dim "green light" Andy described.
**Every new verdict goes through `LED_Color()`, so on hardware they would have
been dim or invisible.** Fixed in 32 bits (`NW_Logger` acd7714); the trace now
shows levels.

**A precedence fact, for Andy:** `begin()` reads Page 1, so a sketch that sets
`wdtSeconds` *before* `begin()` has it overwritten by the stored 2110 s. The
overrun sketch sets it after. Whether an explicit sketch value should win over
Page 1 is a design question; today Page 1 wins unless the sketch writes last.

**A design note:** with no schedule that holds, `NoSchedule` is raised on every
cycle and the asked interval is kept, so the Note column repeats it each row. True
each time, and noisy. Andy may prefer it once.

**Still untestable on the host:** `signal()`'s dispatch and `raise()`'s Note
append live in `NW_Logger.cpp`, which no host harness links. The LED trace and the
transcripts cover them end to end instead.

## What remains: step 5, Okapi's renderer

Sized from `Okapi.sch`, not started. It is a new I2C driver on a prototype board,
so it is proposed here rather than built.

- **D5 is the status RGB on pins 13/14/15 – the same map as Margay**, which is
  why `Okapi.cpp` never sets `RedLED`/`GreenLED`/`BlueLED` and inherits
  `NW_Logger`'s defaults correctly. `signal()` already renders on it.
- **D4 is Okapi's aux, exactly like Margay's D2**: green on `IC1 PC4` (D20,
  `ALIVE_LED`), red and blue on the FT231X's CBUS1/CBUS2.
- **D7** sits on `3V3_FEATHER` and belongs to the cell module.
- **The bar**: eight LEDs (D10–D14, D16–D18) on **U45, a PCA9634** at I2C address
  **0x52** (A6, A4, A1 high), on `SDA_OB`/`SCL`, with `!OE` on `IC1 PB0` = D0
  (`!LED_EN`, active low). **No PCA9634 driver exists anywhere in the
  workspace**; `Okapi.cpp`'s only `0x52` is a Page 2 offset.

The design that follows: one bar LED per subsystem, lit together at the verdict,
so two faults are both visible and nothing is counted; the RGB on D5 keeps the
patterns and is the only indicator that can report an I2C failure, since the bar
is behind the bus. A minimal driver is MODE1 init, LEDOUT0/LEDOUT1 for on/off per
channel, `!LED_EN` low to enable – perhaps eighty lines, testable on the host with
the Wire stub.

**Two decisions inside it, Andy's:** which eight subsystems get a bar LED (card,
clock, sensor bus, BME, battery, watchdog, cell module, ... – pick eight), and
whether the bar shows anything in the field. The design says nothing in the
field, but a bar invites a standing display, and that costs current.

## Waiting on Andy

**The BAD order is mine to be overruled:** card, `NO_SCHEDULE`, sensor, clock. The
card first is the reviewer's argument and I agree with it; where `NO_SCHEDULE`
sits is a judgement.

**One visible change to veto if unwanted:** every first data row now carries
`LoggingStarted` in its Note column, and a later file pair carries `NewLogFile`.
The status file's boot row said this already. It follows the approved design –
every message reaches the Note column – and is isolated in its own commits
(`Margay_Library` 6a168ca, `Okapi_Library` da69d00, `NW-Sim` 4770412), so it can
be reverted alone.

**Does a logger still populate its own Report register?** Margay and Okapi are
Schema 1 devices that serve their own pages, and Okapi backhauls them, so
something may read that byte. Two ways, and 3(b) needs the answer:

1. **Derive it from the message table** – add a `code` column, so one table
   decides the word, the band and the served byte. One source of truth, and the
   `else if` defect cannot return. **Recommended.**
2. **Drop it for loggers**, since the specification's own entry for a controller
   is identity-only. Simpler, though it silently changes what a backhauled page
   says.

**Bench-gated: the battery messages.** A Margay on USB with no cells reads a flat
3.29 V against a 3.3 V threshold, and real cells reach 3.42 V, so no level
separates them. The discriminator is differential – the same reading with
`BatSwitch` enabled and disabled means no battery – and it needs the four
readings listed in `QUEUE.md` under "Battery present or absent". Until then,
`NW_MSG_BATTERY_LOW` should not be wired to the existing `_batError`.

## How to verify

```sh
cd ~/Dropbox/NorthernWidget/github
python3 NW-Tests/style_check.py NW_Logger          # must print "style: OK"
sh NW_Logger/extras/test/run.sh                    # "OK: output identical to baseline"
python3 NW-Tests/compile.py                        # 20 of 22; MaxBotix_* is the known pair
bash NW-Sim/tests/run.sh                           # 19 OK: nine transcripts, nine LED stories, "both ways"
cd NW-Provision && PYTHONPATH=src python3 -m pytest -q   # 131 passed
```

The formatter is Arduino's own, at
`/usr/local/bin/arduino-ide_2.3.3_Linux_64bit/resources/app/lib/backend/resources/clang-format`.
There is also an `nw-verify` skill with the full sequence and its expected counts.

**`set -e` is silently ineffective in the Bash tool's own shell** (tested: `set -e;
false; echo X` prints X). A chained script that relies on it to stop at a failing
check does not stop. Gate explicitly with `|| exit 1`, and read a check's verdict
before the step it guards runs – a baseline re-record and four commits went in
past a failing gate on 2026-10-20, and only a commit message was wrong, but only
by luck.

MaxBotix fails for a reason that predates this work: Andy's uncommitted `Serial1`
conversion in `MaxBotix_Library`. Leave it alone.

## Guardrails

- **Never** push, tag, release, bump a version, submit to a registry or close an
  issue without Andy saying so in the current message. Local commits are
  encouraged and are the rollback mechanism; everything downstream of one is
  gated. Nothing has been pushed since 2026-10-09 – about thirty local commits
  across six repositories.
- **`DS3231` is read-only.** Andy inserts the alarm functions himself; they are
  at `DS3231/PROPOSED-absolute-alarms.md`, untracked. His uncommitted
  `CITATION.cff` change is in that tree; do not touch it.
- Run `python3 NW-Tests/style_check.py <repo>` before every commit touching
  `.ino/.cpp/.h`, and gate the commit on it. A hook enforces it.
- House style: one statement per line, 2-space indent, attached braces, `if (`.
  Match the file's comment form – `//x` in NW_Logger's own sources.
- Commit messages end with the `Co-Authored-By:` and `Claude-Session:` trailers
  used throughout this history; GitHub comments and issue bodies end with the
  Claude Code line.
- Write prose in Andy's voice: spaced en-dashes, never em-dashes. See the
  workspace `CLAUDE.md`.

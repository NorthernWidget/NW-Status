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

`NW_Logger` commit **4eebddd**, steps 1, 2 and 4 of the plan.

- **`NW_Logger/src/NW_Message.h`** — one flat list of sixteen messages covering
  everything a logger says about itself, hardware and runtime alike. The band
  (`NW_BAND_FINE`, `NW_BAND_CAUGHT`, `NW_BAND_BAD`) is a **column in a table**,
  never a pattern in the number, so the compiler assigns the values and nothing
  renumbers when a message is added. Words and table are in PROGMEM, so the list
  costs no RAM. Accessors: `nwMessageBand()`, `nwMessageWord()`.
- **`raise(message)`** — records into the Note column, the serial line and a
  `uint16_t` bitmask of this cycle's messages. It does **not** flash.
- **`worstMessage()`** — the highest band raised, answering `NW_MSG_READY` when
  the worst is merely FINE, so a clean boot earns the chirp.
- **`showVerdict()`** — `signal(worstMessage())`.
- **`signal(message)`** — virtual, the board's renderer. The default carries five
  patterns inside one three-second window, so a user is told once how long to
  look: ALog's long-short-short chirp for READY, its 60/60 flutter for the card,
  its 250/100/100/100 syncopation for the clock, eight 100/300 pips for a missing
  sensor, 500/500 x3 amber for the battery, and solid red for NO_SCHEDULE.
  Anything else renders nothing, which is most of them.
- `note()`'s 300 ms orange flash is gone. It fired on every note written and had
  no observer in the field.
- The three logger messages that were being latched into `_pages` (the sensor
  Report register) no longer are.

## What remains

### Step 3(a): the boot verdict

In `NW_Logger::ledReport()` (`NW_Logger.cpp:140`): replace the colour blocks with
`showVerdict()`. Move `digitalWrite(AuxLED, HIGH)` — currently the first line of
that function — to immediately before the verdict, which is **after** the first
row is written, or there is a dark gap of a few hundred milliseconds while
`initLogFile()` and `addDataPoint()` run. The verdict then means "tests passed
**and** a row reached the card", which is the only claim a user wants.

What is left of `ledReport()` is its serial output, so rename it accordingly.

Note that `blinkGood()` at `NW_Logger.cpp:497` is called unconditionally from
`run()`'s `_newLog` branch, because `_newLog = true` is set regardless of the
self-tests (`Margay.cpp`). So today a board with a dead clock shows the fault
colour and then the happy chirp anyway. The verdict replaces it.

### Step 3(b): the hardware conditions must raise()

**The bigger half, and it fixes a defect rather than changing a cosmetic.** Both
boards run an `else if` chain of chip-addressed latches, so only the **first**
condition found is reported — a board with no card and a dead clock says only
"no card":

- `Margay_Library/src/Margay.cpp:227-233` — `_sdCardMissing` 0x01,
  `_sdTestFailed` 0x05, `_clockError` 0x21, `_bmeError` 0x41, `_sensorError`
  0x61, `_batError` 0x84, then `latchNotice(0xF0)`
- `Okapi_Library/src/Okapi.cpp:103-108` — the same chain without the battery

Raising each as a message fixes it by construction. Also migrate:

- `Margay.cpp:252` — `latchNotice(0x90)` BatteryWarning → `NW_MSG_BATTERY_LOW`
  (**bench-gated**, see below)
- `Margay.cpp:494` and `Okapi.cpp:245` — `latchNotice(0xF2)` RowNotWritten
- `NW_Logger.cpp:390` — `latchNotice(0xF1)` NewLogFile
- `NW_Logger.cpp:99` — `latchNotice(0x30)` ClockSet. **Needs a seventeenth
  message**, `NW_MSG_CLOCK_SET`, band FINE.
- `NW_Logger.cpp:74` — `latchFault(0xE3)` Page 0 invalid. This one is genuinely
  about the logger's identity page; decide with the question below.

### Step 5: Okapi's renderer

Read off `Project-Okapi/Hardware/Okapi.sch`, so this is no longer blocked:

- **Three RGB LEDs**: D4 (R39/R36/R37), D5 (R42/R43/R44), D7 (R81/R82/R83). D7's
  anode is on `3V3_FEATHER`, so it belongs to the cell module rather than to the
  MCU.
- **Eight single LEDs**: D10-D14 and D16-D18, cathodes to **U45 = PCA9634**, an
  8-channel I2C LED driver at **0x52** (A6, A4 and A1 to 3V3_CORE; A0, A2, A3, A5
  to GND), on `SDA_OB`/`SCL`, with a hardware blanking line on `!LED_EN`.

That allows what Margay cannot do: **one LED per subsystem, lit at once.**
Presentation becomes parallel instead of a three-second queue, two simultaneous
faults are both visible, and nothing has to be counted. One constraint decides
the design: **the bar is behind I2C and so cannot report an I2C failure**, which
is exactly when a user most wants an indicator. Keep one MCU-direct RGB for the
"the bus is dead" case and put the per-subsystem detail on the bar.

## Waiting on Andy

**Does a logger still populate its own Report register?** Margay and Okapi are
Schema 1 devices that serve their own pages, and Okapi backhauls them, so
something may read that byte. Two ways, and 3(b) needs the answer:

1. **Derive it from the message table** — add a `code` column, so one table
   decides the word, the band and the served byte. One source of truth, and the
   `else if` defect cannot return. **Recommended.**
2. **Drop it for loggers**, since the specification's own entry for a controller
   is identity-only. Simpler, though it silently changes what a backhauled page
   says.

**Bench-gated: the battery messages.** A Margay on USB with no cells reads a flat
3.29 V against a 3.3 V threshold, and real cells reach 3.42 V, so no level
separates them. The discriminator is differential — the same reading with
`BatSwitch` enabled and disabled means no battery — and it needs the four
readings listed in `QUEUE.md` under "Battery present or absent". Until then,
`NW_MSG_BATTERY_LOW` should not be wired to the existing `_batError`.

## How to verify

```sh
cd ~/Dropbox/NorthernWidget/github
python3 NW-Tests/style_check.py NW_Logger          # must print "style: OK"
sh NW_Logger/extras/test/run.sh                    # "OK: output identical to baseline"
python3 NW-Tests/compile.py                        # 19 of 21; MaxBotix_* is the known pair
bash NW-Sim/tests/run.sh                           # 6 OK, including "both ways"
cd NW-Provision && PYTHONPATH=src python3 -m pytest -q   # 131 passed
```

The formatter is Arduino's own, at
`/usr/local/bin/arduino-ide_2.3.3_Linux_64bit/resources/app/lib/backend/resources/clang-format`.
There is also an `nw-verify` skill with the full sequence and its expected counts.

MaxBotix fails for a reason that predates this work: Andy's uncommitted `Serial1`
conversion in `MaxBotix_Library`. Leave it alone.

## Guardrails

- **Never** push, tag, release, bump a version, submit to a registry or close an
  issue without Andy saying so in the current message. Local commits are
  encouraged and are the rollback mechanism; everything downstream of one is
  gated. Nothing has been pushed since 2026-10-09 — about thirty local commits
  across six repositories.
- **`DS3231` is read-only.** Andy inserts the alarm functions himself; they are
  at `DS3231/PROPOSED-absolute-alarms.md`, untracked. His uncommitted
  `CITATION.cff` change is in that tree; do not touch it.
- Run `python3 NW-Tests/style_check.py <repo>` before every commit touching
  `.ino/.cpp/.h`, and gate the commit on it. A hook enforces it.
- House style: one statement per line, 2-space indent, attached braces, `if (`.
  Match the file's comment form — `//x` in NW_Logger's own sources.
- Commit messages end with the `Co-Authored-By:` and `Claude-Session:` trailers
  used throughout this history; GitHub comments and issue bodies end with the
  Claude Code line.
- Write prose in Andy's voice: spaced en-dashes, never em-dashes. See the
  workspace `CLAUDE.md`.

STATUS: COMPLETE

# Margay v3: what remains, from the firmware side

Surveyed 2026-11-02, read-only, across NW-Status (QUEUE.md, README.md, ITEM1-HANDOFF.md, studies/okapi-leds), Margay_Library, NW_Logger, NW-Sim, Project-Margay, DS3231, DS3231_Logger and the Deployments repository. About 100 v3 boards exist, so every item below is judged by one question: does it make those boards work better with firmware alone. Hardware alternatives are noted and marked out of scope.

Labels: **BUILT** (verified in code), **BUILT-UNTESTED** (in code, no harness or simulator coverage), **OPEN-BUILDABLE** (decided, nobody has built it), **OPEN-DECISION** (waits on Andy, with the decision named), **PROPOSED** (my own reading of the code, not yet in any queue). Sources are file:line, an issue number, a commit, or a QUEUE.md section. Every number is pasted from a command run today. The raw findings log, in the order found, is the appendix at the end; `sources.md` beside this file lists every source checked.

## 1. What a Margay v3 does today in firmware

A v3 boots through `Margay::beginBoard()` (Margay.cpp:164-190): both rails on, aux LED on, clock and battery ADC started, `Serial.begin(38400)`, BME280 started. `NW_Logger::begin()` then reads Page 0 for identity and Page 1 for calibration and the watchdog period (Margay.cpp:200-213: divider at 0x20, `batVoltageError` at 0x22, warning percentage at 0x24, `wdtSeconds` at 0x30 when nonzero, else the compiled 2110 s from R10 = 100 kΩ, Margay.cpp:50-59), takes a YYMMDDHHMMSS clock stamp from Serial if one is waiting (NW_Logger.cpp:84-115), and runs the self-tests (I2C, clock, card, battery, power rail, BME280), each raising its message where it detects the fault. `run(interval)` (NW_Logger.cpp:449-523) arms the DS3231 with `_rtc.setAlarm(_logInterval)`, opens a `log`/`sta` file pair, writes the first row, measures that cycle, and only then turns the aux LED off and plays the verdict on the status LED. Each later alarm wakes the board from `SLEEP_MODE_PWR_DOWN` (Margay.cpp:600-634, rails and SPI off in between; about 1.6 uA measured, QUEUE.md line 1275), writes a row, measures the cycle, lengthens the interval if the cycle outgrew it, re-arms the alarm, feeds the TPL5010 through `WDHold` (NW_Logger.cpp:745-749) and sleeps. The schedule is relative: `setAlarm(60)` is absolute (once a minute at :00) and every other interval is `now + N` (QUEUE.md "CORRECTED 2026-10-08"), so a 5 s or 300 s logger carries its boot latency as a permanent phase and creeps by a second whenever a cycle crosses a second boundary. The 20-message vocabulary in `NW_Message.h` reaches three places from one table: the Note column, the serial line, and the LED. The messages a v3 can raise today are 17 of 20 (grep of `raise(NW_MSG` across NW_Logger.cpp and Margay.cpp): BACKUP_WOKE and INTERVAL_SHORTENED wait on unbuilt work, ON_BACKUP_POWER is Okapi's. Battery state is not a message: it is the color of the chirp and of the per-row blip (Margay.cpp:250-271, placeholder thresholds, unpushed).

What the field sketches say about how a v3 is run: nothing yet. `Deployments/Margay/` holds 28 sketches, all against the removed PascalCase API (`Logger.Run(Update, UpdateRate)` in 26, `Logger.begin(I2CVals, sizeof(I2CVals), Header)`, `Model_1v0`), none naming `MODEL_3v0`; 26 log at 60 s, one at 300 s, and the two hand-rolled TP-Downhole sketches at 900 and 5 s. A v3 today runs `examples/Basic` (5 s), the other four examples, or the NW-Tests sketches (60 s).

## 2. The LED work

Built, and covered by NW-Sim (nine transcripts and nine `.leds` traces, `NW-Sim/tests/run.sh` lines 55-63; today's run is in section 7):

| Item | Label | Source |
|---|---|---|
| 20 messages, band a table column, words in PROGMEM; set is a `uint32_t` | BUILT | `NW_Message.h`; NW_Logger 4eebddd, 18e3dda, ada0d6a |
| Self-tests raise at the branch; four notice latches raise | BUILT | NW_Logger 12a13a7, a51aee7; Margay 2db4e5d, 6a168ca; `margay_missing` shown to bite |
| Boot verdict replaces `ledReport()` and the unconditional `blinkGood()`; aux-off beside it | BUILT | NW_Logger 61d3af0; Margay d109565; `margay_basic.leds` (aux off 1992 ms, chirp 1994-3595) |
| Five rhythms in a 3 s window; a verdict is never dark | BUILT | NW_Logger.cpp:655 `signal()`; 546d5af; `margay_nocard`, `margay_blank`, `margay_overrun` |
| Every distinct rhythm plays, worst to least, 1 s dark between; amber counts the CAUGHT messages first | BUILT | NW_Logger 8f1c53e, 2c26197, 6425cf7 (unpushed); NW-Sim 02f6601, 44ca663 |
| Chirp follows the faults in three forms (`nwChirpForm()`, all 2^20 sets) | BUILT | NW_Logger 2345abb, 34ae385, e2ede92 (unpushed); NW-Sim b24cd31, a37c977 |
| `nwWorstMessage()` and the verdict sequence host-tested | BUILT | NW_Logger 57696d5; `extras/test/run.sh` OK today |
| `LED_Color()` 16-bit overflow fixed; full-brightness colors were dim or stuck | BUILT-UNTESTED on hardware | NW_Logger acd7714; ITEM1-HANDOFF.md "What the LED trace found" |
| 20 ms blue blip per row written | BUILT | NW_Logger.cpp `logRow()`; every `.leds` baseline |
| `note()`'s orange pulse retired; `ORANGE` removed; doc line fixed | BUILT | NW_Logger 4eebddd, 2d3ab8d (unpushed) |
| Chirp and blip color from `chirpColour()`/`rowBlipColour()` hooks | BUILT | NW_Logger ef201d3, 8342b75 (unpushed) |
| Margay's chirp and blip carry the pack level (red < 20 %, purple < 50 %, blue; no judgment below 3.4 V) | BUILT-UNTESTED | Margay ebb3750 (TEMPORARY, unpushed), Margay.cpp:250-271. All nine NW-Sim baselines run at `--battery` 4.02 (nw_sim.c:47), so the red and purple branches have never executed in the simulator |

Open:

| Item | Label | Decision or gate | Source |
|---|---|---|---|
| Battery thresholds (20 %, 50 %, 3.4 V) are placeholders | OPEN-DECISION | Andy sets them, Page 1 battery block | QUEUE.md "The grid's first job" (line 1378); Margay.cpp:250 |
| USB discriminator: sense the FT231X TXD on PD0 before `Serial.begin()` | OPEN-BUILDABLE | after the four bench readings | Margay_Library#34; QUEUE.md "Battery present or absent" |
| No-card verdict plays two segments (flutter, then one-blip amber for ROW_NOT_WRITTEN) | OPEN-DECISION | keep or suppress | desk item 0; `margay_nocard` |
| Order within BAD: card, NO_SCHEDULE, sensor, clock | OPEN-DECISION | overrule in `NW_Message.h` or keep | desk item 6; NW_Message.h:65-80 |
| Whether the chirp stays at ALog's 1000/300/100/100/100 rather than Margay's 2021 651/300/100/200/100 | OPEN-DECISION | Andy's | QUEUE.md line 1189; studies/okapi-leds/8-margay-audit.md section 5 |
| First row's blip plays 94 ms before aux-off | OPEN-DECISION | reorder or leave | QUEUE.md line 1188; `margay_basic.leds` 1878 vs 1992 ms |
| The field: nothing, or a button replay of the verdict (needs a second accumulator, `_messages` clears per cycle) | OPEN-DECISION | Andy's | QUEUE.md line 1186; studies/okapi-leds/README.md "Additions" 4 |
| Does a logger still populate its own Report register (derive from the message table, or drop)? The `else if` chain at Margay.cpp:226-238 waits on it | OPEN-DECISION | derive or drop | ITEM1-HANDOFF.md "Waiting on Andy"; QUEUE.md "The decision inside step 3" |
| RESET_BY_WATCHDOG / BROWN_OUT from MCUSR, read once in `begin()` | OPEN-BUILDABLE | none (Andy: useful) | QUEUE.md "Six more messages" 1; no `MCUSR` in Margay.cpp or NW_Logger.cpp |
| SENSOR_FAULT when a watched device's `report().isFault()` | OPEN-BUILDABLE | none | QUEUE.md "Six more messages" 2; Margay_Library#7 |
| CLOCK_LOST (OSF) distinct from CLOCK_NOT_SET; TIME_ESTIMATED recovery from the last row | 5a OPEN-BUILDABLE; 5b OPEN-DECISION | 5b: Andy wants to discuss | QUEUE.md "Six more messages" 5; NW_Logger.cpp:310-350 never reads OSF; DS3231#90 |
| Board temperature and RH out of range (BME280), CAUGHT | OPEN-DECISION | thresholds | QUEUE.md "Six more messages" 6 |
| Card nearly full | OPEN-DECISION | real cost, unlikely case | NW_Logger#2 |
| CYCLE_OVERRAN on the LED (cyan ten-flash proposal) and the chronic-overrun policy | OPEN-DECISION | hold the interval and flash, or lengthen | QUEUE.md "An alarm firing inside a cycle" |
| Margay_Library README still documents the old colors (green/orange/cyan/pink/red, yellow and red fast blink) and "an orange pulse on the LED" | OPEN-BUILDABLE | none | README.md lines 20-34, 48, 70-90 |

Count: 12 built (2 of them untested on hardware or in the simulator), 15 open (5 buildable, 10 decisions).

## 3. Everything in the active queue that touches Margay

From `NW-Status/QUEUE.md` (last edited 2026-11-02), with the desk-list number where it has one.

1. **Absolute alarms into DS3231** (desk 1). `DS3231/PROPOSED-absolute-alarms.md` (105 lines, untracked, dated 2026-10-09) holds `setAlarmAt()` and `setAlarm2At()`. OPEN-DECISION: Andy inserts. Then the logger owes four pieces, OPEN-BUILDABLE: `dateTimeAt()`, the leapfrog pair in place of the four `_rtc.setAlarm(_logInterval)` sites (NW_Logger.cpp:462, 470, 489, 512), the read-back after arming, and reading A1F/A2F before clearing so BACKUP_WOKE is raised. `NW_Schedule.h` is BUILT and host-swept (92,000 wakes; `extras/test` OK today), but `nwNextWake`, `nwBackupWake`, `nwScheduleHolds` and `nwCycleOverran` are called nowhere in NW_Logger.cpp (grep): only `nwLengthenStep` is wired. This is the item that fixes a defect every v3 at an interval other than 60 s has today (phase and creep, QUEUE.md "CORRECTED 2026-10-08"). The license question (QUEUE.md "Gate 0": DS3231 is public domain, DS3231_Logger GPL-3, Bobby's call) applies only if a DS3231_Logger line moves; the proposal writes the functions fresh.
2. **Adaptive logging** (desk 2, NW_Logger#1). Four OPEN-DECISIONs: the ladder (nine nested steps recommended), the resolution and units, slow cycles before relaxing, and how the rate is measured (the one with science in it). Build items 1-2 (`nwPrevLegibleStep`, `trackValue()`/`sampleOnChange()` seam) are OPEN-BUILDABLE on the host now; the rest is "not before the bench" because the cycle duration is unmeasured.
3. **Decouple the interval from the watchdog, route (a): make the reset the wake** (QUEUE.md "Three to-dos" 3). The only route with no hardware change. OPEN-BUILDABLE, firmware-only, and the most work of the three: read MCUSR early (never read today), and resume into the existing file pair after a watchdog reset (`initLogFile()` takes the first unused number, so a reset every 36 minutes would open about forty pairs a day). Routes (b) #61 and (c) #60 are hardware: out of scope, noted.
4. **Watchdog period** (QUEUE.md "The schedule's open items" 2): DONE. `wdtSeconds = 2110` (Margay.cpp:59, commit 92812bb), Page 1 0x30 overrides. Consequence recorded in the code: the longest interval a v3 can keep is 1800 s; 3600 s is refused.
5. **Page 1's reader has no test** (QUEUE.md section of that name). BUILT-UNTESTED: NW-Provision asserts the written bytes; nothing observes what Margay reads back (proven: pointing `batVoltageError` at the old offset left every transcript byte-identical). Two fixes, OPEN-BUILDABLE: print the thresholds at boot (re-record nine baselines) or give Margay a host harness.
6. **Desk 7: should an explicit sketch value beat Page 1?** `begin()` overwrote a `wdtSeconds` the sketch set before it; today the last writer wins. OPEN-DECISION.
7. **Desk 8: `NoSchedule` once, or every cycle?** Every cycle today (NW_Logger.cpp:557). OPEN-DECISION.
8. **Desk 9: veto `LoggingStarted` in every first row's Note and `NewLogFile` in later pairs.** Isolated commits (Margay 6a168ca, NW-Sim 4770412). OPEN-DECISION, default keep.
9. **Desk 10: push.** 22 commits across Margay_Library, NW_Logger and NW-Sim (section 6). Gated on Andy's word.
10. **Battery present or absent: four bench readings** (QUEUE.md lines 1828-1876). Gate for #34, the discriminator and any change to `batVoltageError`. Bench.
11. **The bench critical path** (QUEUE.md "The bench is now the critical path"): the rewritten `DS3231_Logger::readTime()`/`formatTime()` (first column of every row), the clock stamp parser, and `scan()` on a real bus have never run on silicon. BUILT-UNTESTED (hardware).
12. **Margay_Library#32 tracking list** items 3-5 (sketch addresses, #27/#31, #7 faults) and #33 (done in code, not closed). QUEUE.md "The queue, in order" 3 and 9.
13. **Bus scan (a) DONE; (b) `discover()` needs a second modeled part; (c) NW-Build candidate header unbuilt.** QUEUE.md desk-work item 17.
14. **Fast logging** (geophone rate): Andy to find the old sketches; after the ordinary path settles. QUEUE.md item 12.
15. **Logger-core architecture review** parked 2026-09-24 (five virtual hooks plus `begin()` in six pieces). QUEUE.md item 10.
16. **Desk 5: whether to close Margay_Library#33.** Andy's word.

## 4. Open GitHub issues across the four repositories

Counts from `gh issue list --state open --limit 100` today: Margay_Library 16, Project-Margay 21, NW_Logger 2, NW-Sim 1. Total 40. (DS3231 has 8 and DS3231_Logger 1; the three that bear on the logger are listed last.)

**Margay_Library (16), all firmware unless marked:**

| # | Title (short) | Label |
|---|---|---|
| 34 | False low-battery on USB; sense USB from the RX line in v3 | OPEN-BUILDABLE after the four bench readings; firmware (the v4 wire is hardware, out of scope) |
| 33 | Stream the header instead of a String | done in code (2026-10-03), not closed: OPEN-DECISION (close) |
| 32 | Tracking list vs Schema 1 libraries | items 1-2 done; 3-5 OPEN-BUILDABLE |
| 31 | Aligned columns on the serial monitor | OPEN-BUILDABLE, polish |
| 30 | MargaySetup.ino depends on DS3231 | superseded by NW-Provision: OPEN-DECISION (close or amend) |
| 29 | Granular startup diagnostics to SD | largely met by the message set and the status file's boot row: OPEN-DECISION (close) |
| 28 | GitHub Pages docs | docs |
| 27 | Raw-reading sink without String churn | OPEN-BUILDABLE (LIBRARY-DESIGN section 15), deferred by Andy 2026-10-03 |
| 26 | `ExtInt` member vs `ExtIntPin` global (dead member) | OPEN-BUILDABLE, small |
| 20 | SdFat v2 compatibility (2021) | UNVERIFIED whether still live |
| 19 | Section placement | docs |
| 15 | PG detect before SD writes, lock out until power cycle | OPEN-BUILDABLE, firmware-only; `PG = 18` is a pin field never read (Margay.h:223) |
| 9 | Clock fault raises both OBError and TimeError | partly met by CLOCK_NOT_SET; the OSF/CLOCK_LOST item is its modern form: OPEN-BUILDABLE |
| 7 | General per-sensor fault condition | SENSOR_FAULT is its modern form: OPEN-BUILDABLE |
| 5 | Link `LibVersion` to library.properties | `MARGAY_LIBRARY_VERSION` exists (1fbe8ec); UNVERIFIED whether that closes it |
| 1 | Pinout selection (2018) | firmware, low |

**Project-Margay (21):**

| # | Title (short) | Class |
|---|---|---|
| 61 | v4: WAKE to PA7 | hardware alternative to the watchdog ceiling: out of scope, noted; its firmware half (the clock decides whether to log; the liveness check earns the feed) is reusable in route (a) |
| 60 | v4: R10 to 130 kΩ | hardware alternative: out of scope, noted |
| 9 | PG as cutoff before SD writes (labeled firmware) | firmware-workaround-possible: the same work as Margay_Library#15 |
| 48 | No pull-up on DS3231 SQW/INT | hardware; the firmware workaround is already in place (`INPUT_PULLUP` on RTCInt, NW_Logger.cpp:140) |
| 57 | BME280 placed near heat sources | hardware-only (firmware could flag, not fix) |
| 42, 47, 49-56, 58, 59 | RTC supply, R19, bypass caps, crystal, ESD, USB traces, 3V3_FTDI contention | hardware-only |
| 40 | SCL not switched (wontfix) | hardware |
| 37, 29, 22 | KiCad conversion, silkscreen, installation docs | hardware/docs |

**NW_Logger (2):** #1 adaptive logging (OPEN-DECISION, four decisions; firmware), #2 card nearly full (OPEN-DECISION; firmware).

**NW-Sim (1):** #1 model the Okapi board. Not Margay.

**DS3231, bearing on the logger:** #13 no return value when the RTC does not answer (the `begin()` gap the merge needs), #90 OSF needs an independent reset (the CLOCK_LOST item). **DS3231_Logger #1** alarm Y2K (2018; the relative alarm is to be retired).

## 5. Firmware changes that would make the built boards work better, no hardware change

The first four are in the queue already and are restated here because they are the ones that change what a v3 does in the field. The rest are PROPOSED from reading the code today.

1. **Absolute, grid-aligned alarms** (queue item 1). Every v3 at 5, 300 or 900 s drifts today; at 60 s it does not. The schedule arithmetic exists; the clock functions are written and waiting. OPEN-DECISION then OPEN-BUILDABLE.
2. **Make the watchdog reset a wake** (route (a)). Lifts the 1800 s ceiling on the built boards by letting the reset re-arm on the grid, at the cost of a reset-cause read and a resume-into-file path. OPEN-BUILDABLE.
3. **RESET_BY_WATCHDOG and BROWN_OUT from MCUSR.** Small, both boards, and the prerequisite for 2. OPEN-BUILDABLE.
4. **The USB discriminator on PD0** (#34). Removes the one false message every bench user meets. Gated on the four readings.
5. **PG before SD writes** (Margay_Library#15, Project-Margay#9). PROPOSED as the next-cheapest protection for the card on a dying pack: the pin is wired and declared (`PG = 18`) and read nowhere. The lock-out rule in #15 (print one line, then refuse writes until a power cycle) is a design choice for Andy.
6. **PROPOSED: a bus-dead verdict.** A dead on-board I2C bus raises CLOCK_NOT_SET, ONBOARD_MISSING and BME_MISSING together and the LED plays the clock syncopation, naming a chip when the truth is the bus (studies/okapi-leds/8-margay-audit.md section 4; NW_Logger.cpp:310-350 and :224). Whether that deserves its own message is Andy's.
7. **PROPOSED: cover the battery colors in NW-Sim.** `--battery <V>` exists (nw_sim.c:157) and every baseline runs at 4.02 V; a `margay_lowbat` case at a value Andy names would exercise the red and purple branches of `batteryColour()` before any board does. No new modeling.
8. **PROPOSED: a v3 deployment sketch.** None exists; the 28 in Deployments target v0-v2 through a removed API. One sketch per field configuration that a v3 actually runs (which sensors, which interval) is the artifact that would show the schedule and verdict on a real card. Which configurations is Andy's.
9. **PROPOSED: re-lead the Margay_Library README.** "Logging Start" and "Note column" describe the 2018 colors and the retired orange pulse. The vocabulary in `NW_Message.h` and the patterns in QUEUE.md "The patterns" are the content.
10. **PROPOSED, record only: `_awakeCount > 5`** (NW_Logger.cpp:515-521). Bobby's own comment says the five extra `run()` iterations before sleep may be unnecessary. One `delay(1)` loop each, so the cost is small; not measured.
11. **Print the Page 1 thresholds at boot** (queue item 5), so the transcript proves what the firmware read. Costs a baseline re-record.

## 6. Unpushed commits

Counted with `git log @{u}..HEAD --oneline` today.

- **Margay_Library: 2** (`[ahead 2]`)
  - ebb3750 TEMPORARY: Margay's chirp and per-row blip carry the pack's level - blue, purple, red
  - b8d872c Margay: batPercentFromVoltage() - the alkaline fit as a pure function of a voltage already read
- **NW_Logger: 13** (`[ahead 13]`)
  - 8342b75 logRow: the per-row blip's colour comes from rowBlipColour(), a board hook; blue by default
  - be9eb4f chirp: the backup-battery form goes; a board with more power sources appends its own segments
  - ef201d3 chirp(): colour from chirpColour(), a board hook; three shorts on the backup battery
  - b8182a5 NW_Message.h: ON_BACKUP_POWER, and a third chirp form for running on the backup battery
  - 6425cf7 amber: drop the trailing 500 ms, so the segment ends on light and the separator is a uniform second
  - e2ede92 chirp(): long-short-short, or long then five of the card's pulses when running but not saving
  - 34ae385 NW_Message.h: nwChirpForm() - three chirps for three running states
  - 17656f1 NW_Message.h: BATTERY_LOW leaves the vocabulary - battery state is the chirp's colour
  - fff5ec5 showVerdict: the chirp plays after the fault segments whenever the logger is running
  - 2345abb NW_Message.h: nwChirpAfter() - the chirp follows the faults unless the logger cannot run
  - 2c26197 showVerdict plays every distinct rhythm raised, worst to least; the amber counts first
  - 8f1c53e NW_Message.h: the verdict sequence, pure and tested - one segment per distinct rhythm
  - 2d3ab8d NW_Logger.h: note() no longer claims an orange LED pulse; drop the unused ORANGE define
  (commit subjects quoted verbatim) <!-- spelling: ok -->
- **NW-Sim: 7** (`[ahead 7]`)
  - 8b5133b baselines: Margay's row carries the alkaline fit; traces stay blue, overrun rows 4 ms longer
  - fb6857a baselines: jitter from the rowBlipColour() hook; no behaviour change
  - dc8adb8 baselines: jitter from the chirpColour() hook; no behaviour change
  - 44ca663 baselines: the amber ends on light, so the chirp follows it after exactly one second
  - a37c977 baselines: the no-card verdict ends in the long-and-buzz chirp
  - b24cd31 baselines: the chirp follows the faults - missing-sensor and blank cases end with long-short-short
  - 02f6601 baselines: the verdict sequence - blank gains the amber count, no-card plays two segments
  (commit subjects quoted verbatim) <!-- spelling: ok -->
- **Project-Margay: 0.** Untracked `.claude/` and `CITATION_TODO.md`.
- **DS3231: 0.** Working tree: ` M CITATION.cff` (Andy's, untouched), `?? PROPOSED-absolute-alarms.md`.
- **DS3231_Logger: 0.**
- For the desk-10 push as a whole, the other repositories it names: NW-Status 43, Project-Okapi 14, Okapi_Library 10, NW-Tests 4, NW_Core 0, NW-Provision 0.

Total across the Margay repositories: 22. Across everything the desk list names: 93.

## 7. Verification run today

- `sh NW_Logger/extras/test/run.sh`: `OK: output identical to baseline`, exit 0 (outputs gitignored).
- `bash NW-Sim/tests/run.sh` with `TMPDIR` in the scratchpad: 19 lines beginning `OK` (nine transcripts, nine LED stories, "both ways"), exit 0. The handoff's expected count holds with the seven unpushed baseline commits in place.

## 8. What to do next, in order

1. **Insert the absolute alarms into DS3231, then wire the grid into `run()`.** Gated on Andy inserting `PROPOSED-absolute-alarms.md`. Then four logger pieces, a transcript at an interval other than 60 s, and the sweep's "consecutive wakes land on the grid" property. This is the one change that fixes a defect every v3 at a non-60 s interval has now.
2. **Read MCUSR in `begin()` and raise RESET_BY_WATCHDOG / BROWN_OUT.** Gated on nothing (Andy said useful, 2026-10-22). Small, both boards, and it is the prerequisite for item 3.
3. **Route (a): make the watchdog reset a wake, with resume-into-file.** Gated on item 2 and on Andy confirming route (a) for v3 (the queue recommends (b) for v4 and (a) "for boards that already exist"). Lifts the 1800 s ceiling on the built boards.
4. **The bench session that gates the battery work: the four `BatSwitch` readings and the cycle duration.** Gated on hardware time. Unblocks #34's discriminator, the threshold decisions, and the adaptive-logging floor. Beforehand, a `--battery` NW-Sim case at a value Andy names covers the color branches at no cost.
5. **Push the 22 commits in Margay_Library, NW_Logger and NW-Sim, after the ten open LED decisions are answered or explicitly deferred.** Gated on Andy's word. The decisions with a default already in the code (BAD order, no-card second segment, `LoggingStarted` in Note, `NoSchedule` every cycle, Page 1 precedence) cost one sentence each.

---

**Summary.** A Margay v3 today boots, self-tests, reads its identity and calibration from EEPROM, logs on a relative DS3231 alarm, sleeps at about 1.6 uA, feeds a 2110 s watchdog, and reports through a 20-message vocabulary that reaches the file, the serial line and one RGB LED, with the verdict sequence and the fault-aware chirp built and asserted to the millisecond in nine simulator traces. What it does not yet do is keep an absolute schedule at any interval other than 60 s, know why it last reset, log slower than every 30 minutes, tell USB from a dead pack, or protect the card on a dying one. The first of those is waiting on two clock functions Andy has in hand; the second and third are firmware-only and buildable now; the last two wait on four bench readings. Across the four repositories 40 issues are open, 22 commits are unpushed, and the LED work stands at 12 built against 15 open, 10 of them decisions. No deployment sketch for a v3 exists, and the Margay README still describes the 2018 colors.

---

## Appendix: raw findings log, in the order found

### From NW-Status/QUEUE.md (last edited 2026-11-02), lines 1-1035

- QUEUE.md "ON ANDY'S DESK" (lines 7-63), Margay-relevant items:
  - Desk 1: insert absolute alarms into DS3231 (`DS3231/PROPOSED-absolute-alarms.md`, untracked). OPEN-DECISION (Andy inserts). Logger then owes four pieces (QUEUE.md "Andy to insert", lines 933-960): `dateTimeAt()`, replace `_rtc.setAlarm(_logInterval)` at NW_Logger.cpp :492/:509/:532 with leapfrog pair, read-back after arming, read A1F/A2F before clearing (BACKUP_WOKE). Those four are OPEN-BUILDABLE once the clock side lands.
  - Desk 2: four decisions inside adaptive logging, NW_Logger#1 (ladder, resolution, slow cycles before relaxing, how the rate is measured). OPEN-DECISION. Build items 1-2 (`nwPrevLegibleStep`, `trackValue`/`sampleOnChange` seam) are host-sweepable now; the rest "not before the bench" (QUEUE.md lines 810-931).
  - Desk 3: Project-Margay#60 vs #61 for v4 (watchdog ceiling). Hardware; OUT OF SCOPE for this survey, noted.
  - Desk 0: missing card also raises ROW_NOT_WRITTEN, so no-card verdict plays flutter, dark, one-blip amber (NW-Sim `margay_nocard`, 2026-10-21). Keep or suppress? OPEN-DECISION.
  - Desk 6: order within BAD (card, NO_SCHEDULE, sensor, clock) set by the session, overrule in `NW_Message.h`. OPEN-DECISION.
  - Desk 7: should an explicit sketch value beat Page 1? `begin()` reads Page 1 and overwrote a `wdtSeconds` the sketch set earlier; last writer wins today. OPEN-DECISION (ITEM1-HANDOFF.md).
  - Desk 8: `NoSchedule` raised once or every cycle? Today every cycle. OPEN-DECISION (ITEM1-HANDOFF.md).
  - Desk 9: veto if unwanted: `LoggingStarted` in every first row's Note column, `NewLogFile` in later pairs; isolated commits. OPEN-DECISION (default: keep).
  - Desk 10: push. Nothing pushed since 2026-10-09 except claude-kicad-text; local commits in NW_Logger, NW-Sim, NW-Status, NW-Tests, Okapi_Library, Margay_Library, Project-Okapi. (Counts verified below per repo.)
  - "Waiting on the bench": four battery readings, cycle duration, Okapi's unfed watchdog.
- QUEUE.md "Merge DS3231_Logger into DS3231" (lines 65-148): decided 2026-10-07, DS3231 survives. Gate 0: license mismatch (DS3231 public domain, DS3231_Logger GPL-3; Bobby's call). DS3231 lacks `begin()`, absolute `setAlarmAt()`, a timestamp formatter. OPEN-DECISION (license), then OPEN-BUILDABLE. No edits in DS3231 without Andy's word.
- QUEUE.md "CORRECTED 2026-10-08: the alarm must be absolute" (lines 175-231): `DS3231_Logger::setAlarm(60)` is absolute (once-per-minute mask); every other interval is `now + N`, relative, phase set by boot latency and creeping. Measured in NW-Sim at 5 s: 00:00:03, :08, :13... The relative path (5, 150, 300, 900 s in deployments) has never appeared in a transcript. **This is a firmware defect that affects built boards at any interval other than 60 s.** Fix = grid + absolute alarms (desk 1). Logger side `NW_Schedule.h` BUILT (2026-10-09, host-swept, 92,000 wakes); clock side OPEN-DECISION.
- QUEUE.md "Where to read the clock, and the backup alarm" (lines 290-380): backup A2 = first whole-minute grid point after A1; three layers A1/A2/TPL5010; fourth: `if (!digitalRead(RTCInt))` at NW_Logger.cpp:522. Open: device-specific notice kinds for "woken by backup" and "cycle overran" (Andy picks the numbers). Cycle duration never measured (bench).
- QUEUE.md "The guard's floor" (lines 487-507): hard floor 2 s; `nwScheduleHolds()` refuses a step under the guard (BUILT per text; verify in NW_Schedule.h).
- QUEUE.md "An alarm firing inside a cycle" (lines 509-557): `nwCycleOverran()` detection; LED warning proposal cyan ten-flash; policy question open (hold configured interval and flash vs lengthen). OPEN-DECISION.
- QUEUE.md "Three to-dos (Andy, 2026-10-19)" (lines 597-684): (1) LED vocabulary - "easy advance", since built in October (see LED section); (2) DS3231 absolute alarms - Andy's; (3) decouple logging interval from watchdog. Route (a) "make the reset the wake, no hardware change" is the one for the ~100 built boards: needs `MCUSR` read early (firmware never reads it, so it cannot tell a watchdog reset from power-up) and a resume-into-existing-file path (`initLogFile()` takes the first unused number, so each reset opens a new log/sta pair, ~40 pairs a day at a 36-min reset). OPEN-BUILDABLE, firmware-only, and it is the most firmware work of the three. Route (b) is #61 (v4 hardware), route (c) is #60.
- QUEUE.md "The schedule's open items" (lines 686-808): item 2 DONE: Margay `wdtSeconds` = 2160 s (36 min) from R10 = 100 kΩ, TPL5010 datasheet (Margay_Library c50ae85); consequence: with a 2 s cycle the longest interval a Margay can keep is 1800 s; 3600 s is refused. Item 1 superseded by the flat message list; `NW_Logger.h` carried provisional codes 16-19 (check whether still there).
- QUEUE.md "Page 1's reader has no test" (lines 962-981): NW-Provision asserts written bytes; nothing observes what the firmware reads back (transcript prints `Bat = 4.01V 73.44%` only). Proven: pointing `batVoltageError` at the old 0x32 leaves every transcript byte-identical. Two fixes: print thresholds at boot (re-record baselines) or give Margay a host harness (does not exist). OPEN-BUILDABLE. BUILT-UNTESTED for the Page 1 reader itself.
- QUEUE.md "Okapi's watchdog is not being fed" (lines 983-1033): Okapi-only; corrected 2026-10-30. Not Margay.

### From QUEUE.md "Logger messages and the LED vocabulary, settled" (lines 1035-1304)

- Message table: 20 messages in `NW_Message.h` (READY, LOG_STARTED, NEW_FILE, INTERVAL_LENGTHENED, INTERVAL_SHORTENED, CLOCK_SET, BME_MISSING, ROW_NOT_WRITTEN, NOTE_TRUNCATED, CYCLE_OVERRAN, BACKUP_WOKE, ONBOARD_MISSING, PAGE0_INVALID, ON_BACKUP_POWER, CARD_MISSING, CARD_UNREADABLE, CARD_WRITE_FAILED, NO_SCHEDULE, SENSOR_MISSING, CLOCK_NOT_SET). "Raised today?" column: all yes except INTERVAL_SHORTENED (adaptive logging, NW_Logger#1), BACKUP_WOKE (alarm work), ON_BACKUP_POWER (Okapi only). BATTERY_LOW removed 2026-10-22. (QUEUE.md lines 1043-1080; to verify against NW_Message.h.)
- Margay LEDs, verified in Margay.sch: D3 full RGB (pins 13/15/14, MCU), D2 green only on pin 20 (`AuxLED`); D2 red/blue are on the FT231X CBUS1/CBUS2 and unreachable by firmware. Aux = "powered and running" steady from `begin()` to the verdict; status D3 = verdict + 20 ms blue blip per row. (lines 1082-1106)
- LED decisions 2026-10-21 (lines 1108-1190): blue stays for READY; Margay shows every message in sequence, 3 s segments, 1 s dark; one segment per distinct rhythm; amber segment with count prefix (100/200 ms blips, one per CAUGHT); longest sequence 5 segments, 21 s; FINE messages file-only; chirp plays only when nothing else raised. Chirp follows the faults in three forms (`nwChirpForm()`, checked over all 2^20 sets; `chirp(form)` virtual). **Battery state as chirp color: NOT BUILT on Margay** - waits on Page 1 battery thresholds (Andy's) and on the USB discriminator, Margay_Library#34 (USB-present signal reaches no MCU pin; sense RX line in v3 firmware). OPEN-DECISION (thresholds) + OPEN-BUILDABLE (RX sensing). `NW_Logger::chirpColour()` hook exists (blue default), Okapi overrides. The 20 ms row blip stays. BUILT 2026-10-21 (NW_Logger 8f1c53e, 2c26197): `nwVerdictSequence()`, `nwMessageRhythm()`, `showVerdict()`; NW-Sim baselines re-recorded (`margay_blank` gains one-blip prefix, `margay_nocard` second segment).
- Still open (line 1183-1190): column groups (Okapi); the field (nothing, or a button replay of the verdict on both boards); whether the first row's blip plays before aux-off; whether the chirp stays at ALog's 1000/300/100/100/100; desk item 0. OPEN-DECISION.
- "Six more messages, Andy's disposition" (lines 1213-1271), both-board items relevant to Margay:
  1. RESET_BY_WATCHDOG / BROWN_OUT from MCUSR, read once in `begin()`, CAUGHT. Andy: useful. OPEN-BUILDABLE, firmware-only, both boards. (Also the prerequisite for route (a) of the watchdog decoupling.)
  2. SENSOR_FAULT (CAUGHT) raised when a watched device's `report().isFault()`; today the Report register reaches Note/status file (NW_Logger.cpp:932, 1011) but no LED. OPEN-BUILDABLE.
  3. Card nearly full: NW_Logger#2, Andy: real cost, unlikely case.
  5. Clock lost power (DS3231 OSF): (a) CLOCK_LOST distinct from CLOCK_NOT_SET (logger folds OSF into CLOCK_NOT_SET today, NW_Logger.cpp:329) - OPEN-BUILDABLE; (b) provisional time from last row's timestamp + TIME_ESTIMATED - Andy "wants to discuss": OPEN-DECISION; (d) computer-vs-logger offset on plug-in, host tool.
  6. Board temperature/RH out of range from BME280, CAUGHT, thresholds Andy's, Page 1 has room. OPEN-DECISION (thresholds).
  Proposed build order: 1, 2, 6 first; then 5a, 5b.
- Margay sleeps at about 1.6 uA measured (Andy, 2026-10-28, line 1275). Okapi sections (1192-1211, 1273-1347) are Okapi-only.

### From QUEUE.md lines 1349-1567 (Okapi LED order, the grid's first job, patterns, defects, order of work)

- "Full-time messaging, decided (Andy, 2026-10-28)" (lines 1378-1405): per-row blip color = pack level via `NW_Logger::rowBlipColour()` hook (blue default). **Margay too**: chirp and blip carry the pack level from the alkaline fit's percentage, red below 20 %, purple below 50 %, placeholders for Page 1; below 3.4 V no judgment (blue), the stand-in for Margay_Library#34's USB discriminator (USB alone reads 3.29 V). Text says built for Okapi; whether Margay's override exists must be verified in Margay.cpp. Thresholds are placeholders: OPEN-DECISION.
- Patterns table (lines 1420-1481): card 60/60 red; clock 250/100/100/100 red; sensor 100/300 x8 red; no schedule solid red; caught N x (100/200), 300 dark, 500/500 x3 amber; READY chirp 1000/300/100/100/100 blue.
- "What the field sees: nothing" (line 1483): no pattern after boot except the per-row blue blip; `note()`'s orange flash retired.
- Three defects found and (per order of work) fixed: `_sdTestFailed`/`_clockError`/`_bmeError` never shown; chirp unconditional (`Margay.cpp:223`, `:497`); Okapi never sets `_batError`. Order of work items 1-4 DONE 2026-10-20 (NW_Logger 4eebddd, 61d3af0, 12a13a7, a51aee7, 546d5af..4d8d525). Item 5 (Okapi renderer) not started. (lines 1490-1549)
- "The decision inside step 3, for Andy" (lines 1551-1567): does a logger still populate its own Report register? Derive from message table (recommended) or drop. OPEN-DECISION. "The served-byte latch chains stay, commented, pending the decision." Battery messages gated on the bench (USB-only reads 3.29 V vs 3.3 V threshold, real cells 3.42 V).

### From QUEUE.md lines 1700-2005 (bench critical path, battery readings, queue in order)

- "The bench is now the critical path" (2026-10-04, lines 1700-1736): items in the row path for Margay: (4) `DS3231_Logger::readTime()`/`formatTime()` rewritten 2026-10-03, never run on a real DS3231; (5) boot clock stamp `nwParseTimeStamp()`, no transcript sends a stamp; (6) `scan()`/`discover()` on a real bus (`Margay_Library/examples/BusScan`). Firmware is 2290 bytes of flash smaller than the last version run on silicon and links no `String`. All BUILT-UNTESTED on hardware.
- "Battery present or absent: four readings" (lines 1828-1876): on USB with no cells a Margay reports a low-battery error (3.29-3.30 V against `batVoltageError = 3.3`, serial 4D03-4157-0001-0000, logs 00001-00003); real cells reach 3.42 V in log 00014, 0.13 V apart; `VUSB` never reaches an MCU pin. Four-reading bench test (BatSwitch enabled/disabled x cells in/out) is the prerequisite for every battery-message change. OPEN (bench), gates the chirp-color battery work on Margay.
- "The queue, in order" (lines 1973-2003): item 3, Margay_Library #33 (stream the header) is done in code and not closed; item 9, Margay_Library #32 tracking list: many-readings sink (#27), aligned columns on the monitor (#31), folding sensors' Block 0 faults into `SensorError` (#7); items 1-2 of that list done.
- Queue table (line 2354): bus scan (a) DONE (NW_Logger b265871, Margay 075cde3, NW-Sim 3670291, `margay_scan` transcript); (b) `discover()` needs a second modeled part on the Margay board in NW-Sim; (c) NW-Build candidate header - not built. Line 2367: fast logging (geophone-rate) - Andy to find the sketches, revisit after ordinary logging path. Line 2369: Logger core architecture review PARKED 2026-09-24 (five virtual hooks + begin() in six pieces: right shape?).

### From NW-Status/README.md (generated table, dated 2026-09-24 - STALE by five weeks of work)

- Table header says "Status" dated 2026-09-24 (README.md line 6). Margay row (line 30): 14 open library issues, 19 open hardware issues, hardware repo 2 uncommitted files, at scan time. Margay Schema 1 library column (line 186): "MISSING (no Page 0 read)" - superseded by B4 in QUEUE.md (Margay is a Schema 1 device, watches itself, 2026-09-23); the manual CSV cell is stale. Next-action cell (line 214) lists tracking list #32 items. Live counts are taken from `gh` below.
- README line 250: NW-Sim is private, runs Margay firmware on simulated ATmega1284P.

### From NW-Status/ITEM1-HANDOFF.md (written 2026-10-20, updated 2026-10-21)

- BUILT (lines 15-49): `NW_Message.h` message set as `uint32_t` with static_assert <= 32; `raise()` recursion bug on full Note buffer fixed; boot verdict replaces `ledReport()` color blocks and unconditional `blinkGood()`; `run()` turns aux off and calls `showVerdict()` after the first row; self-tests raise at the branch (seven sites in NW_Logger.cpp, BME_MISSING per board); four notice latches raise (LOG_STARTED, ROW_NOT_WRITTEN per board; NEW_FILE, CLOCK_SET in NW_Logger.cpp); `margay_missing` NW-Sim case shown to bite.
- Reviewed and fixed (lines 51-84): CAUGHT-only boot showed nothing (now amber by band); NO_SCHEDULE could not reach the verdict (first cycle now timed); no card left Note buffer growing; per-row 20 ms blue blip; set cleared per cycle; card outranks clock; ONBOARD_MISSING and PAGE0_INVALID added; `Serial.begin()` before BME init. NW_Logger 546d5af..4d8d525, NW_Core da46f8a, Margay_Library 7db9ee8, Okapi_Library f366d8f.
- Tested (lines 86-130): `nwWorstMessage()` host-tested over thirteen sets (NW_Logger 57696d5); NW-Sim traces four LED pins with ms timestamps (NW-Sim 6c49312, b7a37af) into `.leds` files; cases `margay_nocard`, `margay_blank`, `margay_overrun` added; "Nineteen OK in all: nine transcripts, nine LED stories, and both ways". **`LED_Color()` 16-bit overflow fixed (NW_Logger acd7714)**: `255 - (red * lum) / 0xFF` in 16-bit `int` overflowed at full brightness so red stuck and green/blue ran at 1/255 duty; every verdict goes through it, so on hardware the new verdicts would have been dim or invisible. This is a correctness fix that matters for the built boards and has never been seen on silicon: BUILT-UNTESTED (hardware).
- Precedence fact: `begin()` reads Page 1 and overwrites a `wdtSeconds` the sketch set before it (stored 2110 s in the sim's Page 1). Desk 7. `NoSchedule` raised every cycle: desk 8.
- Still untestable on the host: `signal()` dispatch and `raise()`'s Note append live in `NW_Logger.cpp`, which no host harness links; covered by NW-Sim end-to-end only.
- Verification commands (lines 221-244): style_check NW_Logger; `sh NW_Logger/extras/test/run.sh`; `python3 NW-Tests/compile.py` (20 of 22; MaxBotix pair known); `bash NW-Sim/tests/run.sh` (19 OK); NW-Provision pytest 131 passed. Expected counts as of 2026-10-21; whether they still hold is checked below if the runs are cheap and read-only.
- Guardrails (line 246+): about thirty local commits across six repositories unpushed since 2026-10-09 (as of 2026-10-21; recounted below).

### From NW-Status/studies/okapi-leds/README.md and 8-margay-audit.md (2026-10-20/21)

- 8-margay-audit.md written before the 2026-10-21 multi-segment sequence; its section 4 "a second fault cannot be shown" is superseded by `nwVerdictSequence()` (every distinct rhythm plays). What still stands from its gaps (section 5): `NW_Logger.h:249` documents `note()` as "shown as an orange pulse", retired 2026-10-20 (doc stale; verify); `ORANGE` defined and unused; the first row's blip plays 94 ms before aux-off in `margay_basic` (open item in QUEUE line 1188); the chirp is ALog's 1000/300/100/100/100, not Margay's 2021 651/300/100/200/100 (QUEUE line 1189, OPEN-DECISION); an on-board bus failure plays the clock syncopation (names a chip when the truth is the bus) - PROPOSED candidate: a bus-dead verdict.
- Study note 5 (README "Additions that survived" 4): a button-press verdict on S3 (the log button) needs a second accumulator because `_messages` clears each cycle. OPEN-DECISION ("the field: nothing, or a button replay", QUEUE line 1186).
- LED traces: in NW-Sim the aux *on* edge is never recorded (pin driven LOW from LOW default), so the trace cannot assert the aux lit.

### Margay_Library (read 2026-11-02)

- `git status -sb`: `## master...origin/master [ahead 2]`. Unpushed (`git log @{u}..HEAD --oneline`):
  - ebb3750 TEMPORARY: Margay's chirp and per-row blip carry the pack's level - blue, purple, red
  - b8d872c Margay: batPercentFromVoltage() - the alkaline fit as a pure function of a voltage already read
- Open issues (`gh issue list -R NorthernWidget/Margay_Library --state open --limit 100`): 16 - #34, #33, #32, #31, #30, #29, #28, #27, #26, #20, #19, #15, #9, #7, #5, #1.
- `src/Margay.cpp` 665 lines, `src/Margay.h` 336 lines. Examples: Basic, BusScan, HighSpeed_NoSleep, Laser_Ranging, SensorDemo_TP-Downhole.
- Margay.cpp:50-59 (model 3): `WDHold = 23`, `BatSwitch = 19`, `wdtSeconds = 2110` with the derivation in the comment (R10 = 100k, TPL5010 Equation 1 gives 2159.65 s, 1 % tolerance puts the real period between 2110 and 2209 s; "the longest the grid can hold here is 1800 s"). Commit 92812bb. BUILT.
- Margay.cpp:200-213: Page 1 read in `begin()`: `_batteryDivider` from 0x20, `batVoltageError` from 0x22, `batPercentageWarning` from 0x24, `wdtSeconds` from 0x30 if nonzero. This is the "Page 1 wins over a sketch value set before begin()" precedence (desk 7). BUILT; reader has no test (QUEUE "Page 1's reader has no test").
- Margay.cpp:226-238: served Report-register `else if` latch chain kept "Pending Andy's decision" (desk: Report register derive-or-drop). Reports only the first fault met. OPEN-DECISION.
- Margay.cpp:250-271: TEMPORARY battery thresholds `MARGAY_BAT_UNJUDGED_V = 3.4`, `MARGAY_BAT_LOW_PCT = 20`, `MARGAY_BAT_MID_PCT = 50`; `batteryColour()` feeds `chirpColour()` and `rowBlipColour()`. So the "Margay too" chirp color IS built (commit ebb3750, unpushed), with placeholder thresholds: BUILT-UNTESTED (NW-Sim baselines re-recorded in NW-Sim 8b5133b, "traces stay blue" because the simulated battery reads 4.01 V above both cut-offs - so the red and purple branches have no simulator coverage). Thresholds OPEN-DECISION (Andy's, Page 1 battery block).
- Margay.cpp:273-287 `batTest()`: `_batError` when `batVoltage < batVoltageError` (3.3 V default, Margay.h:236); `_batWarning` and served notice 0x90 when below `batPercentageWarning` (50 %). `_batError` still feeds `chipFaults()` 0x10 and the served chain 0x84, but no LED message (BATTERY_LOW removed). The false-low-battery-on-USB defect (#34) therefore now shows only in the served byte and the status file, not on the LED. BUILT.
- Margay.cpp:508-522 `addDataPoint()`: `bme280.begin(0x77)` each row ("FIX??"), bus dance, `logRow()`, raises ROW_NOT_WRITTEN; `fillPages()`, `reportRows()`.
- Margay.cpp:447-476 `readOnBoard()`: carries `//FIX!!! Dumb!` and `//FIX!` comments (Bobby's); `getTime()` called inside `readOnBoard()`.
- No `MCUSR` anywhere in Margay.cpp/Margay.h (grep). Reset cause is never read. Confirms QUEUE route (a) prerequisite is unbuilt.

### NW_Logger (read 2026-11-02)

- `git status -sb`: `## master...origin/master [ahead 13]`. Remote exists (https://github.com/NorthernWidget/NW_Logger.git). Unpushed 13:
  - 8342b75 logRow: the per-row blip's colour comes from rowBlipColour(), a board hook; blue by default
  - be9eb4f chirp: the backup-battery form goes; a board with more power sources appends its own segments
  - ef201d3 chirp(): colour from chirpColour(), a board hook; three shorts on the backup battery
  - b8182a5 NW_Message.h: ON_BACKUP_POWER, and a third chirp form for running on the backup battery
  - 6425cf7 amber: drop the trailing 500 ms, so the segment ends on light and the separator is a uniform second
  - e2ede92 chirp(): long-short-short, or long then five of the card's pulses when running but not saving
  - 34ae385 NW_Message.h: nwChirpForm() - three chirps for three running states
  - 17656f1 NW_Message.h: BATTERY_LOW leaves the vocabulary - battery state is the chirp's colour
  - fff5ec5 showVerdict: the chirp plays after the fault segments whenever the logger is running
  - 2345abb NW_Message.h: nwChirpAfter() - the chirp follows the faults unless the logger cannot run
  - 2c26197 showVerdict plays every distinct rhythm raised, worst to least; the amber counts first
  - 8f1c53e NW_Message.h: the verdict sequence, pure and tested - one segment per distinct rhythm
  - 2d3ab8d NW_Logger.h: note() no longer claims an orange LED pulse; drop the unused ORANGE define
  (commit subjects quoted verbatim) <!-- spelling: ok -->
  (So the stale `note()` doc and unused `ORANGE` from 8-margay-audit.md are fixed in 2d3ab8d.)
- Open issues: 2 - #2 card nearly full (2026-10-22), #1 adaptive logging (2026-10-09).
- src: NW_Logger.cpp, NW_Logger.h, NW_Message.h, NW_Schedule.h, NW_TimeStamp.h. extras/test: host harness (run.sh, test_output.cpp, baseline.txt).

### NW-Sim (read 2026-11-02)

- `git status -sb`: `## master...origin/master [ahead 7]`. Unpushed 7, all baseline re-records:
  - 8b5133b baselines: Margay's row carries the alkaline fit; traces stay blue, overrun rows 4 ms longer
  - fb6857a baselines: jitter from the rowBlipColour() hook; no behaviour change
  - dc8adb8 baselines: jitter from the chirpColour() hook; no behaviour change
  - 44ca663 baselines: the amber ends on light, so the chirp follows it after exactly one second
  - a37c977 baselines: the no-card verdict ends in the long-and-buzz chirp
  - b24cd31 baselines: the chirp follows the faults - missing-sensor and blank cases end with long-short-short
  - 02f6601 baselines: the verdict sequence - blank gains the amber count, no-card plays two segments
  (commit subjects quoted verbatim) <!-- spelling: ok -->
- Open issues: 1 - #1 model the Okapi board (2026-10-28). Not Margay.
- `tests/run.sh` cases (lines 55-63): margay_basic (examples/Basic, 25 s), walrus_margay (NW-Tests Walrus_Margay, 130 s), margay_scan (BusScan, --walrus --apis), margay_programmed, margay_discovered, margay_missing (Programmed_Margay without Apis), margay_overrun (Overrun_Margay, 20 s), margay_nocard (Basic, nocard), margay_blank (Basic, nostored). Nine Margay transcripts, nine `.leds` traces, plus "both ways" diff = 19 checks. Baseline files: 9 x .txt + 9 x .leds for Margay cases + apis_in_the_loop.txt + walrus_in_the_loop.txt (20 files in tests/baseline).
- Margay model (from CLAUDE.md and QUEUE line 2312): simavr ATmega1284P, DS3231 at 0x68 with both alarms and INT pin, SD card in SPI mode, BME280 at 0x77, MCP3421 at 0x69, MCU ADC fed for the battery (reads 4.01 V), 3V3 aux rail switching, I2C bus switch. All sketches in the cases log at 5 s (Basic) or 60 s; **no case at a relative-alarm interval other than 5 s and no case with a battery below 3.9 V**, no case sending a clock stamp, no case with a watchdog reset (the TPL5010 is not modeled: UNVERIFIED, check the model source).

### Project-Margay (read 2026-11-02)

- `git status -sb`: `## master...origin/master`, no unpushed commits; untracked `.claude/` and `CITATION_TODO.md`.
- Open issues: 21 - #61, #60, #59, #58, #57, #56, #55, #54, #53, #52, #51, #50, #49, #48, #47, #42, #40, #37, #29, #22, #9.

### DS3231 and DS3231_Logger (read 2026-11-02; read-only)

- DS3231: `## master...origin/master`, no unpushed; working tree: ` M CITATION.cff` (Andy's uncommitted change, untouched) and `?? PROPOSED-absolute-alarms.md` (105 lines, dated Oct 9 23:07). Open issues: 8 - #111, #104, #103, #97, #90, #76, #13, #11. Relevant to the logger: #13 "No return value when failing to talk to the RTC" (the `begin()` gap), #90 "OSF flag needs independent reset function" (the CLOCK_LOST item).
- DS3231_Logger: `## master...origin/master`, no unpushed. Open issues: 1 - #1 "Fix alarm Y2K issue" (2018).

### NW_Message.h and raise() sites (read 2026-11-02)

- `NW_Message.h` (275 lines) defines 20 messages (enum NW_MSG_READY .. NW_MSG_CLOCK_NOT_SET, `NW_MSG_COUNT`, static_assert <= 32): matches QUEUE table. BAD order in the enum: CARD_MISSING, CARD_UNREADABLE, CARD_WRITE_FAILED, NO_SCHEDULE, SENSOR_MISSING, CLOCK_NOT_SET (desk 6).
- `grep -n 'raise(NW_MSG'` across NW_Logger.cpp, Margay.cpp, Okapi.cpp: raised somewhere = BME_MISSING (Margay.cpp:185), LOG_STARTED (:239), ROW_NOT_WRITTEN (:530), PAGE0_INVALID (NW_Logger.cpp:76), CLOCK_SET (:103), SENSOR_MISSING (:208), ONBOARD_MISSING (:224), CARD_MISSING (:250), CARD_UNREADABLE (:253), CARD_WRITE_FAILED (:297), CLOCK_NOT_SET (:327, :338, :348), NEW_FILE (:365), CYCLE_OVERRAN (:547), NO_SCHEDULE (:557), INTERVAL_LENGTHENED (:568), NOTE_TRUNCATED (:946, :1055), ON_BACKUP_POWER (Okapi.cpp:251 only). **Never raised on any board: INTERVAL_SHORTENED, BACKUP_WOKE.** READY is the empty set. So 17 of 20 are raisable on a Margay today; 2 are defined for unbuilt work; 1 is Okapi's.
- NW_Logger.cpp alarm arming: `_rtc.setAlarm(_logInterval)` at lines 462, 470, 489, 512 (four sites now; QUEUE said :492/:509/:532 - line numbers moved). `if (!digitalRead(RTCInt))` level catch at :510. `resetWDT()` at :477, :490, :498, :505 pulses `WDHold` (:745-749). `keepInterval()` at :536 measures the cycle with `millis()`, lengthens via `nwLengthenStep()` (:553). `showVerdict()` :596, `chirp()` :626, `signal()` :655.
- `NW_Schedule.h` (270 lines): `nwStepDividesDay`, `nwNextWake` (with `NW_ALARM_GUARD_SECONDS`), `nwBackupWake`, `nwScheduleHolds`, `nwNextLegibleStep`, `nwLengthenStep`, `nwCycleOverran`. BUILT, host-swept. **None of `nwNextWake`/`nwBackupWake` is called from NW_Logger.cpp** (the grep for setAlarm shows only `_rtc.setAlarm(_logInterval)`, the relative path): the grid is built but not wired to the clock, waiting on the DS3231 absolute-alarm functions. Verify with a grep for nwNextWake in NW_Logger.cpp below.
- NW_Logger.h hooks (virtual): `beginBoard`, `addDataPoint`, `readOnBoard`, `sleepNow`, `afterLogEvent`, `signal`, `chirp`, `chirpColour`, `rowBlipColour`, `writeDataToSD`, `buttonLog`. `wdtSeconds` public (:310), `run(unsigned long logInterval)` (:280), `_logInterval` kept vs `_intervalAsked` (:552-553).

### Margay_Library issues, read (2026-11-02)

- #34 (bug, 2026-10-22): false low-battery on USB; v3 firmware fix = sense the FT231X TXD on PD0 before `Serial.begin()` (hypothesis, UNVERIFIED on the bench); four bench readings are the acceptance test. Firmware-workaround-possible; OPEN-BUILDABLE after the bench readings (the discriminator must be written against measured numbers, QUEUE "Gate").
- #33 (2026-09-30): stream the header - QUEUE says done in code (streaming landed 2026-10-03), issue not closed. Firmware; closing is Andy's.
- #32 tracking list: items 1-2 done (include migrated, Page 0 read); 3 sketch addresses; 4 #27/#31; 5 #7 faults. Firmware.
- #31 aligned columns on the serial monitor (AlignedPrint adapter). Firmware, OPEN-BUILDABLE, polish.
- #30 MargaySetup.ino depends on DS3231 - superseded by NW-Provision (writes Page 0/1) and the DS3231 merge decision; OPEN-DECISION (close or amend).
- #29 granular startup diagnostics to SD - largely superseded by the message set reaching the Note column and the status file's boot row (ITEM1-HANDOFF); OPEN-DECISION (close?).
- #28 GitHub Pages docs. Docs; not firmware behavior.
- #27 many-readings sink without String churn. Firmware, OPEN-BUILDABLE (design in LIBRARY-DESIGN section 15; deferred).
- #26 unify `ExtInt` member with `ExtIntPin` static global (dead member). Firmware, OPEN-BUILDABLE, small.
- #20 SdFat v2 compatibility (2021). Firmware; UNVERIFIED whether still live (which SdFat the compile uses was not checked).
- #19 section placement, #22-style docs. Docs.
- #15 add PG detect: check regulator PG line before SD writes, lock out writes until power cycle. Firmware-only, OPEN-BUILDABLE; pairs with Project-Margay#9 (PG as cutoff, labeled firmware). `PG = 18` is already a pin field in Margay.cpp:46 (model 3). Protects the card from brown-out corruption on the built boards: no hardware change.
- #9 fix clock fault condition: no clock battery -> both `OBError` and `TimeError`; wants only one. Firmware. Partly superseded by CLOCK_NOT_SET (one message for both); the CLOCK_LOST/OSF item (QUEUE six-more-messages 5a) is the modern form. OPEN-BUILDABLE.
- #7 general fault condition per sensor - the SENSOR_FAULT message (QUEUE six-more-messages 2) is its modern form. OPEN-BUILDABLE.
- #5 link `LibVersion` to library.properties - `MARGAY_LIBRARY_VERSION` build identity exists (commit 1fbe8ec); UNVERIFIED whether the issue is fully met. OPEN-DECISION (close?).
- #1 pinout selection (2018). Firmware, low.

### Project-Margay issues (21 open), classified

- #61 v4 WAKE to PA7 (labels enhancement, firmware, v4): hardware alternative, OUT OF SCOPE, noted. Its firmware half (clock decides whether to log; liveness check earns the feed) is reusable in route (a).
- #60 R10 to 130 kΩ: hardware alternative, OUT OF SCOPE, noted.
- #9 "Use PG as cutoff" (enhancement, firmware, 2026-06-01): PG pin to prevent SD writes below cutoff; alternative CRC on SdFat writes. Firmware-workaround-possible (firmware half = Margay_Library#15).
- #42 power RTC from main supply with CR1220 backup: hardware-only.
- #47-#59 (13 issues, June 2026 review): hardware-only (crystal, bypass caps, ESD, USB traces, SQW pull-up #48, 3V3_FTDI contention #50, R19 BoM mismatch #47, BME280 placement #57). #48 (missing pull-up on DS3231 SQW/INT): firmware already uses INPUT_PULLUP on RTCInt (NW_Logger.cpp:140), which is the firmware workaround in place. #57 (BME280 near heat sources): firmware could annotate but not fix; hardware-only.
- #40 SCL not switched (wontfix): hardware.
- #37 Eagle to KiCad, #29 silkscreen, #22 installation formatting: hardware/docs.

### Examples and field sketches

- `Margay_Library/examples/Basic/Basic.ino`: `Margay Logger(MODEL_3v0)`, `Logger.begin()`, `Logger.run(5)` - 5 s interval, the relative-alarm path.
- `HighSpeed_NoSleep.ino`: polls `addDataPoint()` every 150 ms, no sleep, no alarm; bench only.
- Workspace has `./Deployments` and `./Deployments.old` directories (not yet read).

### Code reads for the "today" paragraph (NW_Logger.cpp, Margay.cpp; 2026-11-02)

- `NW_Logger::run()` (NW_Logger.cpp:449-523): on `_newLog` arms `_rtc.setAlarm(_logInterval)`, opens a file pair, writes the first row, measures the cycle (`keepInterval`), re-arms only if lengthened, aux off, `showVerdict()`, `resetWDT()`. On `_logEvent`: clears `_messages`, row, `afterLogEvent()`, `keepInterval`, re-arm, `resetWDT()`. Button (`manualLog`) and external-interrupt counter branches also feed the watchdog. Level catch at :510. Sleeps after `_awakeCount > 5` (Bobby's comment says the 5 may be unnecessary).
- `keepInterval()` (:536-570): raises CYCLE_OVERRAN when `took / 1000 >= _logInterval`; lengthens via `nwLengthenStep(_intervalAsked, cycleSeconds(), wdtSeconds)`; raises NO_SCHEDULE when none holds; raises INTERVAL_LENGTHENED. `nwLengthenStep` is the ONLY NW_Schedule.h function NW_Logger.cpp calls (grep): `nwNextWake`, `nwBackupWake`, `nwScheduleHolds`, `nwCycleOverran` are built and host-swept but unwired.
- `clockTest()` (:310-350): oscillator-stopped (seconds not incrementing over 1.1 s), year == 0 ("never set"), and no-ACK all raise CLOCK_NOT_SET; OSF is not read (the CLOCK_LOST item).
- `serialTimeSet()` (:84-115): a YYMMDDHHMMSS stamp on Serial at boot sets the clock, raises CLOCK_SET; malformed stamp refused.
- `Margay::beginBoard()` (Margay.cpp:164-190): `powerOB(ON)`, `powerAux(ON)`, aux LED on, `_rtc.begin()`, `_rtc.clearAlarm()`, MCP3421 init on BUILD_B/C, `Serial.begin(38400)`, BME280 init (raises BME_MISSING).
- `Margay::sleepNow()` (:600-634): `turnOffSDcard()` (releases SCL/SDA/RX0/TX0, `powerAux(OFF)`, `powerOB(OFF)`, SPI off), `SLEEP_MODE_PWR_DOWN`, BOD disabled, ADC disabled; on wake `turnOnSDcard()` re-powers rails and `_sd.begin()`. Margay sleeps at about 1.6 uA measured (Andy, QUEUE line 1275).
- `PG = 18` is a pin field only (Margay.h:223, Margay.cpp:42/92/140); it is never read. Margay_Library#15 and Project-Margay#9 (PG before SD writes) are unbuilt.
- Margay_Library `README.md` "Logging Start" (lines 20-34) still documents the pre-2026-10-20 LED scheme (green all-OK, orange sensor, cyan clock, pink card, red critical, yellow fast blink battery < 50 %, red fast blink < 3.3 V) and the Note section (line 48) still says a note is "shown as an orange pulse on the LED". Both are stale against the built vocabulary. Troubleshooting (lines 70-90) keyed to those colors. OPEN-BUILDABLE (docs).

### NW-Sim coverage facts (2026-11-02)

- `src/boards/margay.c`: battery fed to A2 as `env->battery_v / 2` and to the MCP3421 model; `--battery <V>` option, default 4.02 (nw_sim.c:47). All nine baselines were recorded at the default, so `batteryColour()`'s red and purple branches have no simulator coverage; a case at `--battery 3.6` (or any value Andy picks) would cover them without new modeling.
- No TPL5010 model: grep for tpl5010/watchdog/WDHold/DONE in `src/` returns nothing. A watchdog reset, route (a)'s reset-cause read, and the interval ceiling in real time are outside the simulator.
- LED traces (`tests/baseline/margay_basic.leds`): first-row blip blue 1878-1899 ms, aux off 1992, chirp blue 1994-2994, 3294-3395, 3495-3595 (1000/300/100/100/100). `margay_nocard.leds`: aux off 1788, red 60/60 from 1789. `margay_blank.leds`: aux off 2000, amber (red+green PWM) from 2001.
- NW_Logger host harness (`extras/test/run.sh`): compiles `NW_TimeStamp.h`, `NW_Schedule.h` and `NW_Message.h` against the NW_Core stubs; "the rest of the logger needs a card, a clock and a board, and lives in NW-Sim's transcripts". Outputs gitignored.

### Field sketches (Deployments repository, 2026-11-02)

- `Deployments/Margay/` holds 28 sketches (last commit 73a4b59, 2026-09-22, "include NW_BME280.h"). All use the removed PascalCase API: `Logger.Run(Update, UpdateRate)` (26 sketches), `Logger.begin(I2CVals, sizeof(I2CVals), Header)`, and `Model_0v0/1v0/2v0` enumerators; `Run(` and `Model_1v0` no longer exist in `Margay.h` or `NW_Logger.h` (grep: only `MODEL_1v0`). None names `MODEL_3v0`. Intervals: `UpdateRate = 60` in 26, `300` in 1; the two hand-rolled TP-Downhole sketches use 900 and 5 s. **There is no deployment sketch for a Margay v3 in the repository, and none of the 28 compiles against the current library** (UNVERIFIED by compile; verified by grep of the removed names). The v3 boards can run only `examples/Basic`, `BusScan`, `HighSpeed_NoSleep`, `Laser_Ranging`, `SensorDemo_TP-Downhole`, or the NW-Tests sketches (all at 5 or 60 s).


# Margay v3: the firmware to-do list, in order (2026-11-02)

About 100 Margay v3 boards are built. Nothing here changes the hardware. Each
item has a label, a gate, and an acceptance test; an item Andy has not reached
is pending, not declined. Sources and the reasoning are in
`studies/margay-firmware-status/report.md`; the decisions' detail is in
`QUEUE.md` under the sections named. Mark an item DONE here with the commit,
in the same commit that does it.

Labels: BUILT (in code, verified), BUILT-UNTESTED (in code, nothing exercises
it), BUILDABLE (decided, nobody has built it), DECISION (waits on Andy; the
decision is stated), BENCH (waits on hardware time).

## A. The spine: five items, in order

1. **Absolute, grid-aligned alarms.** DECISION then BUILDABLE. Andy inserts
   `setAlarmAt()` and `setAlarm2At()` from `DS3231/PROPOSED-absolute-alarms.md`
   (105 lines, untracked) into DS3231. Then NW_Logger owes four pieces:
   `dateTimeAt()`; the leapfrog pair in place of the four
   `_rtc.setAlarm(_logInterval)` sites (NW_Logger.cpp:462, 470, 489, 512); the
   read-back after arming; A1F/A2F read before clearing so BACKUP_WOKE is
   raised. `NW_Schedule.h` is BUILT and host-swept (92,000 wakes) but only
   `nwLengthenStep` is called. Defect fixed: every v3 at an interval other
   than 60 s carries its boot latency as a phase and creeps a second at
   boundaries (QUEUE.md "CORRECTED 2026-10-08"). Acceptance: an NW-Sim
   transcript at an interval other than 60 s whose wake times land on the
   grid; the nine existing baselines unchanged.
2. **RESET_BY_WATCHDOG and BROWN_OUT from MCUSR, read once in `begin()`.**
   BUILDABLE, no gate (Andy: useful, 2026-10-22). No `MCUSR` read exists in
   Margay.cpp or NW_Logger.cpp. Acceptance: the message in the Note column
   and on the LED after a simulated watchdog reset and a brown-out; harness
   and baselines green.
3. **The watchdog reset as a wake, route (a), with resume-into-file.**
   BUILDABLE, gated on item 2 and on Andy confirming route (a) for v3 (the
   queue recommends (b) for v4 and (a) for boards that exist). Lifts the
   1800 s ceiling (`wdtSeconds = 2110`, Margay.cpp:59). `initLogFile()` takes
   the first unused number, so without resume a reset every 36 minutes opens
   about forty file pairs a day. Acceptance: a 3600 s transcript with one
   file pair and rows on the grid. Routes (b) Project-Margay#61 and (c) #60
   are hardware: out of scope.
4. **The bench session.** BENCH. The four `BatSwitch` readings (QUEUE.md
   "Battery present or absent", lines 1828-1876) and the cycle duration.
   Unblocks the USB discriminator (#34), the battery thresholds (B1), and the
   adaptive-logging floor. Before the bench: an NW-Sim `--battery` case at a
   voltage Andy names, so the red and purple chirp branches run somewhere
   (every baseline runs at 4.02 V, nw_sim.c:47).
5. **Push.** 22 commits: Margay_Library 2, NW_Logger 13, NW-Sim 7. Gated on
   Andy's word, after the ten decisions in B are answered or deferred.

## B. The LED vocabulary: open items

Built: 12 (list in the report, section 2). Two of those are untested:
`LED_Color()`'s 16-bit overflow fix (NW_Logger acd7714) has never run on
hardware; the battery chirp and blip colors (Margay ebb3750, TEMPORARY) have
never executed below 3.9 V anywhere.

Decisions, one sentence each; the default in the code stands until then:
1. Battery thresholds 20 %, 50 %, 3.4 V are placeholders (Margay.cpp:250).
2. No-card verdict: keep the second segment (one-blip amber for
   ROW_NOT_WRITTEN) or suppress it (desk item 0, `margay_nocard`).
3. Order within BAD: card, NO_SCHEDULE, sensor, clock (desk 6,
   NW_Message.h:65-80).
4. Chirp timing: ALog's 1000/300/100/100/100 or Margay 2021's
   651/300/100/200/100 (QUEUE.md line 1189).
5. First row's blip 94 ms before aux-off: reorder or leave (QUEUE.md line 1188).
6. The field: nothing, or a button replay of the verdict, which needs a second
   accumulator (QUEUE.md line 1186).
7. Does a logger still populate its own Report register: derive from the
   message table, or drop (ITEM1-HANDOFF.md "Waiting on Andy").
8. TIME_ESTIMATED recovery from the last row after clock loss: Andy wants to
   discuss (QUEUE.md "Six more messages" 5b).
9. Board temperature and RH out of range as CAUGHT messages: thresholds
   (QUEUE.md "Six more messages" 6).
10. CYCLE_OVERRAN on the LED, and the chronic-overrun policy: hold and flash,
    or lengthen (QUEUE.md "An alarm firing inside a cycle"). Card nearly full
    (NW_Logger#2) sits with it.

Buildable now, no gate:
11. SENSOR_FAULT when a watched device's `report().isFault()` (Margay_Library#7).
12. CLOCK_LOST from OSF, distinct from CLOCK_NOT_SET (NW_Logger.cpp:310-350
    never reads OSF; DS3231#90).
13. A bus-dead verdict, PROPOSED: a dead bus raises CLOCK_NOT_SET,
    ONBOARD_MISSING and BME_MISSING together and names a chip. Whether it is
    its own message is Andy's; the detection is buildable.
14. The Margay_Library README re-led: lines 20-34, 48 and 70-90 describe the
    2018 colors and the retired orange pulse.
15. Print the Page 1 thresholds at boot so the transcript proves what the
    firmware read (QUEUE.md "Page 1's reader has no test"); re-record the
    nine baselines.

## C. Protection and robustness of the built boards, firmware only

1. **PG before SD writes** (Margay_Library#15, Project-Margay#9). BUILDABLE.
   `PG = 18` is declared (Margay.h:223) and read nowhere. The lock-out rule in
   #15 (one line, then refuse writes until a power cycle) is a DECISION.
2. **USB discriminator on PD0** before `Serial.begin()` (Margay_Library#34).
   BUILDABLE after A4. Removes the false low-battery message every bench user
   meets.
3. **Adaptive logging** (NW_Logger#1, QUEUE.md "Plan: adaptive logging").
   Four DECISIONs (ladder, resolution and units, slow cycles before relaxing,
   how the rate is measured). Build items 1-2 (`nwPrevLegibleStep`, the
   `trackValue()`/`sampleOnChange()` seam) BUILDABLE on the host now; the rest
   not before A4.
4. **`_awakeCount > 5`** (NW_Logger.cpp:515-521), record only: Bobby's comment
   says the five extra `run()` iterations may be unnecessary. Unmeasured.

## D. Decisions on behavior already in the code (one sentence each)

1. Should an explicit sketch value beat Page 1? Today the last writer wins
   (desk 7).
2. `NoSchedule` once, or every cycle? Every cycle today (NW_Logger.cpp:557;
   desk 8).
3. Veto `LoggingStarted` in every first row's Note and `NewLogFile` in later
   pairs (Margay 6a168ca, NW-Sim 4770412; desk 9). Default keep.
4. Close Margay_Library#33 (done in code 2026-10-03), #29 (largely met by the
   message set), #30 (superseded by NW-Provision); amend or close #5
   (`MARGAY_LIBRARY_VERSION` exists). Closing an issue is gated on Andy's word.

## E. Never run on silicon (BUILT-UNTESTED, hardware)

- The rewritten `DS3231_Logger::readTime()`/`formatTime()`, the first column of
  every row.
- The clock stamp parser (NW_Logger.cpp:84-115).
- `scan()` on a real bus.
- `LED_Color()` overflow fix (B, above).
- Page 1's reader: NW-Provision asserts the bytes written, nothing observes
  what Margay reads back (proven: moving `batVoltageError`'s offset left every
  transcript byte-identical). B15 is the cheap fix.

## F. Deployment and documentation

1. **A v3 deployment sketch.** None exists: the 28 in `Deployments/Margay`
   use the removed PascalCase API (`Logger.Run()`, `Model_1v0`) and none
   names `MODEL_3v0`. One sketch per field configuration a v3 actually runs
   (which sensors, which interval) is the artifact. Which configurations:
   Andy's.
2. The README (B14).
3. Margay_Library#32 tracking list items 3-5 (sketch addresses, #27/#31, #7).
4. Small firmware issues: #26 (`ExtInt` dead member), #31 (aligned serial
   columns), #27 (raw-reading sink, deferred by Andy 2026-10-03), #20 (SdFat
   v2, UNVERIFIED whether live).

## Out of scope, noted

Project-Margay#60 (R10 to 130 kΩ) and #61 (WAKE to PA7) are the hardware
routes past the watchdog ceiling, for v4. #61's firmware half (the clock
decides whether to log; the liveness check earns the feed) is reusable in A3.
The remaining Project-Margay issues (#42, #47-#59, #40, #48 with its firmware
workaround already in place) are hardware.

## G. v3.1.0, the KiCad board (2026-11-05)

v3.0.0-rc.2 is released (the 2023 copper, parts corrected; Zenodo
10.5281/zenodo.23971433) and v3.0.0 is a GitHub draft until a reworked board
passes `docs/v3.0-as-built-checks.md`. Development continues on master toward
v3.1.0, the KiCad board in `Hardware/KiCAD/`, whose milestone holds the issues.

1. **The defining change:** TPL5010 WAKE to PA7, one trace, and the firmware
   that answers it (#61). The reason it is a minor bump: Page 0 carries
   major.minor, and firmware tells a WAKE-wired board apart by that byte.
2. **Five small hardware fixes from the 2025 review**, a part or a value each:
   a pull-up on the DS3231's INT line (#48), C12 to the TPS79733's minimum
   (#49), bypass capacitors at the MCP3421 (#52) and the SD slot (#53), the
   crystal's load capacitors against its CL (#54).
3. **Two decisions**: SBU1/SBU2 to ground or left as the no-connects the board
   has (#58); whether the USB D+/D− pair needs 90 Ω control on a full-speed link
   (#56, likely wontfix).
4. **Open since 2025:** switch SCL as well as SDA in the I²C isolation (#40,
   marked wontfix; close or reopen).
5. **Housekeeping, done in substance, close on Andy's word:** #37 (the
   conversion), #62 (BoM fields, parity 0), #63 and #42 (D4 and C20 stay).
6. **Optional:** R10 to the 0402 130 kΩ so every Yageo resistor is one
   package; a footprint change.
7. **Firmware, no hardware needed, first in time:** MCUSR reset-cause messages
   (A.2), then route (a) of the watchdog plan (A.3).
8. **Release path as for v3.0:** v3.1.0-rc.1 before the run, v3.1.0 after a
   built board confirms it; each tag on Andy's word.

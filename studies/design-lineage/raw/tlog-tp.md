STATUS: COMPLETE

# Design lineage: TLog, TP-DownHole, TP-DownHole-No2

Read-only survey, 2026-11-20. Paths are relative to the workspace
(`/home/awickert/Dropbox/NorthernWidget/github`). Line numbers are from the
working-tree files as checked out locally. Nothing was written inside any repository.

## TP-DownHole (v0.1.0 and its descendants)

The original TP-DownHole board descends directly from the SparkFun MS5803-14BA breakout.
Every later TP-DownHole board (v2, Longbow, Longbow Mountable) carries the same MS5803
symbol and footprint, which keeps a SparkFun production ID.

| Claim | Evidence | Confidence |
|---|---|---|
| v0.1.0 board modified from the SparkFun MS5803-14BA breakout | First commit `8be4902` (2017-01-26, Andy Wickert): "Modified from Sparkfun MS5803-14BA breakout"; it adds `TP-DownHole.sch` and `TP-DownHole.brd` | verified |
| Original SparkFun designer named in the title block | `TP-DownHole/Hardware/TP-DownHole.sch:7895-7896`: "Andy Wickert (Modif. from Casey Kuhns, SparkFun)" | verified |
| MS5803 part is SparkFun's | `TP-DownHole/Hardware/TP-DownHole.sch:214` `PROD_ID` = `IC-12111` (SparkFun's internal production-ID form) in library `MS5803`, deviceset `MS5803-14BA` (part U1, line 7866) | likely (PROD_ID scheme is SparkFun's; library itself has no SparkFun description) |
| SparkFun CC-BY-SA 4.0 frame retained | `TP-DownHole/Hardware/TP-DownHole.sch:222-228` SparkFun-Aesthetics library, "Licensing: Creative Commons ShareAlike 4.0"; FRAME1 = `SparkFun-Aesthetics/FRAME-LETTER` (line 7867), frame text "Released under the Creative Commons Attribution Share-Alike 4.0 License" (lines 382-384); OSHW logo LOGO3 (line 7884) | verified |
| SparkFun passives and connectors | Parts C1 `SparkFun-Capacitors` (PROD_ID CAP-00810), R1-R4 `SparkFun-Resistors` (RES-08272, RES-00824), SJ2 `SparkFun-Passives`, J1 `SparkFun-Connectors/CONN_04X2` (`TP-DownHole.sch:7868-7890`) | verified |
| SparkFun design rules | `TP-DownHole/Hardware/TP-DownHole.brd:1462` `<designrules name="SparkFun">` | verified |
| Parts matched to ALog BottleLogger (NW) | Commit `30a57ec` "Same parts as ALog BottleLogger: easier inventory" (I2C pull-ups 2.2k -> 3k); commit `ebae734` "Eagle .gitignore from ALog-BottleLogger"; schematic note "plug into same terminal on ALog, for example" (`TP-DownHole.sch:7904`) | verified (component/inventory sibling, not circuit parent) |
| Repo license | `TP-DownHole/LICENSE.md`: hardware CC-BY-SA 4.0, firmware GNU GPL v3; added `8120727` (2017-01-26, CC) and `07b7934`/`b9e2b56` (2018-10-27, GPL v3 added). GitHub reports `NOASSERTION` | verified |

### TP-DownHole v2 (2018-03), Longbow (2017-10), Longbow Mountable (2018-10), Longbow_Prog

| Claim | Evidence | Confidence |
|---|---|---|
| v2 and Longbow descend from TP-DownHole v0.1.0 | Same repository; MS5803 library with `PROD_ID IC-12111` in `TP-DownHole_v2.sch:219`, `TP-DownHole_Longbow.sch:219`, `TP-DownHole_Longbow_Mountable.sch:219`, and boards (`TP-DownHole_v2.brd:626`, `TP-DownHole_Longbow.brd:722`); board document-layer text "Andrew D. Wickert" carried over (`TP-DownHole_v2.brd:176`, `TP-DownHole_Longbow.brd:177`, v0.1.0 `TP-DownHole.brd:159`) | verified (same MS5803 part and carried-over board text) |
| Longbow first design | Commit `ba5fda8` (2017-10-09, Bobby Schulz) "Added Longbow First Design" | verified |
| SparkFun libraries still present | SparkFun-Jumpers, SparkFun-Aesthetics, SparkFun-PowerSymbols in v2 and Longbow schematics; Longbow keeps the SparkFun CC-BY-SA frame text (`TP-DownHole_Longbow.sch:593-595`) | verified |
| v2 title block replaced by NW "ColdSilicon frame" | Commit `33ca930` (2018-06-28): "also added ColdSilicon frame"; the diff removes the SparkFun "CC BY-SA 4.0 License ... placeholder for designer name" frame. Current `TP-DownHole_v2.sch` and `TP-DownHole_Longbow_Mountable.sch` carry no "Released under the Creative Commons" text (0 matches) | verified (share-alike notice dropped from those sheets; repo LICENSE.md still applies) |
| Longbow_Prog uses Adafruit parts | `TP-DownHole/Hardware/Longbow_Prog.sch` libraries `adafruit` (x2), `SparkFun-Connectors`; part LED1 `adafruit/LED` | verified (library use) |
| Firmware is Arduino | `TP-DownHole/Firmware/*/Longbow_*.ino`, `Downhole_Longbow_Firmware.ino`: Arduino sketches including `EEPROM.h`, `SlowSoftWire.h` | verified (Arduino framework; no derived-code claim) |
| Design rules: OSH Park / Bay Area Circuits | `TP-DownHole_Longbow.brd:543` `oshpark-2layer`; `TP-DownHole_v2.brd:447` `BayArea-2layer` | verified (fab rules, not lineage) |

## TP-DownHole-No2 ("Local logger", 2017-07)

| Claim | Evidence | Confidence |
|---|---|---|
| Derived from TP-DownHole v0.1.0 | Identical title-block text "Andy Wickert (Modif. from Casey Kuhns, SparkFun)" and identical ALog/MS5803 notes (`TP-DownHole-No2/TP-DownHole-No2.sch:8577-8586` vs `TP-DownHole/Hardware/TP-DownHole.sch:7895-7904`); same board text "7 Feb 2017"/"A. Wickert"/"Andrew D. Wickert" pattern (`TP-DownHole-No2.brd:156-159`); same U1 MS5803-14BA with `PROD_ID IC-12111` (`.sch:214`) | verified |
| Grand-parent: SparkFun MS5803-14BA breakout | via TP-DownHole (above); SparkFun-Aesthetics CC-BY-SA frame retained (`TP-DownHole-No2.sch:232-233, 382-384`); `<designrules name="SparkFun">` (`TP-DownHole-No2.brd:1722`) | verified |
| Added logger core from SparkFun libraries | U$1 `SparkFun-IC-Microcontroller/ATTINY84`, U2 `SparkFun-IC-Memory/EEPROM-I2C`, RTC1 `SparkFun-Clocks/DS3231M`, X1 `con-molex/52745-0490` | verified (library use) |
| Repo license | GitHub: `CC-BY-SA-4.0`; remote `LICENSE` (commit `6adaa11`, 2018-06-17 "CC-BY-SA") is CC BY-SA 4.0 text | verified |
| Local clone is behind GitHub | Local has 1 commit (`534f662`); GitHub has 3 (`534f662`, `5dd61d6` "Added alternative prelim design..." ATtiny441/AT24C512C/TPS79718/DS1337, `6adaa11` LICENSE). Remote `TP-DownHole-No2_Alternative.sch` uses `adafruit`, `atmel`, `SparkFun-Batteries`, `SparkFun-PowerSymbols` libraries (read via `gh api`, not stored in repo) | verified |

## TLog (Telemetry Logger; Logger_v2 "BETA" -> TLog Mrk 1.x)

| Claim | Evidence | Confidence |
|---|---|---|
| Built around the ALog 3.0 platform (NW) | GitHub description: "hardware designs associated with the TLog (Telemetry Logger) designed around the ALog 3.0 platform"; folder name `ALog-TLog/` | verified (stated); no ALog schematic is copied into the repo, so circuit descent is not shown in-file |
| TLog Mrk 1 descends from Logger_v2 (TLog BETA) | Commit `c5b0b0d` (2017-07-14) "Added initial developments on the TLog BETA" adds `Logger_v2.sch/.brd`; commit `6caf12b` (2017-08-16) "Initial TLog v2 Development ... Changes have been made to crystal oscilator, GPS, switching FETs, removal of resistor header, EEPROM removed, 5v buck-boost added, and primarilly ATMEGA644 added"; shared part names (DS3231M RTC1, RFM69H U3, LTC2495 U$7, SX1509 U4, P-FETs Q5-Q7, CONN_10 J8/J10) in `Logger_v2.sch` and `TLog.sch` | verified |
| Logger_v2 (BETA) built from SparkFun and Adafruit libraries | `TLog/ALog-TLog/Logger_v2.sch`: U1 `SparkFun-IC-Microcontroller/ATSAMD21G`, RTC1 `SparkFun-Clocks/DS3231M`, U3 `SparkFun-RF/RFM69H`, U4 `SparkFun-IC-Special-Function/SX1509`, `SparkFun-Connectors` (USB_MICRO-B, I2C_STANDARD), `SparkFun-DiscreteSemi`, `SparkFun-Fuses`, `SparkFun-LED`; `adafruit` MICROSD (U$2), SMACONNECTOR (X1), AVRISP (ISP2); SparkFun CC-BY-SA notices (e.g. `Logger_v2.sch:169`) | verified (library use) |
| No Arduino Zero / Feather M0 parent shown | SAMD21 in Logger_v2 but no Arduino Zero, Feather, or Adafruit board reference in text (grep for "feather", "zero" board names: none; only SparkFun library datasheet links) | not found |
| TLog Mrk 1 uses `bschulz` library whose parts are copies of SparkFun parts | `TLog/ALog-TLog/TLog.sch` library `bschulz` (lines 6047-15563) contains SparkFun descriptions ("SparkFun Products", sparkfun.com datasheet links for DS3231M, SX1509, connectors) and a battery package `AWICKERT_LINX_BAT-HLD-012-SMT` (line 7183) from the `awickert` library; also `SparkFun-Connectors` (line 160, CC-BY-SA notice at line 170), `SparkFun-Jumpers`, `SparkFun-PowerSymbols` | likely (copied library parts) |
| MCU changed to ATmega644P(A) | `TLog.sch:13044-13046` DIGIKEY `ATMEGA644PA-MURCT-ND`, MPN `ATMEGA644PA-MUR`; commit `e6c07b7` "Changed part number for ATMEGA644P" | verified (Mighty-core family; no core named in files) |
| TLog_HighSpeedADC and TLog_TopBat are TLog variants | `TLog_HighSpeedADC.sch` added in `343f16d` ("High Speed ADC daughter board preliminary files"); mixes `atmel/ATMEGA644*`, `FT231X`, SparkFun and Adafruit libraries; `TLog_TopBat.sch` shares the TLog `bschulz` part set | verified |
| BatteryModule uses SparkFun ATtiny45 part | `TLog/ALog-TLog/BatteryModule.sch` U$4 `SparkFun-IC-Microcontroller/ATTINY45`, J6 `SparkFun-Connectors/AVR_SPI_PROG_3X2` | verified (library use) |
| UMN credit on the board silkscreen | `TLog/ALog-TLog/TLog.brd:220-225`: "Open-source for the outdoors" and "Developed in part at the University of Minnesota in parntnership with Northern Widget LLC" (TLog_TopBat.brd:222 likewise) | verified |
| Repo license is LGPL v3, not CC-BY-SA | `TLog/LICENSE` is "GNU LESSER GENERAL PUBLIC LICENSE Version 3" (initial commit `4443fa3`); GitHub `LGPL-3.0`. No CC-BY-SA notice at repo level, although SparkFun CC-BY-SA library parts are embedded | verified (license mismatch with SparkFun share-alike parts) |

## Authorship facts relevant to the openness/IP question

- TLog: 19 commits by Bobby Schulz with a umn.edu address, 4 by Chad Sandell (northernwidget.com), 11 by Bobby's gmail. TP-DownHole: 30 commits by Bobby Schulz (umn.edu), 14 by Andy Wickert (northernwidget.com). TP-DownHole-No2: 1 by Andy Wickert (northernwidget.com). Source: `git log --format='%an <%ae>' | sort | uniq -c`.
- TP-DownHole v0.1.0 (Jan-Feb 2017) was authored entirely from Andy's northernwidget.com address and released CC-BY-SA 4.0 on day one (`8120727`).

## Sources checked (dead ends included)

- `TLog/LICENSE`, `TP-DownHole/LICENSE.md`, `TP-DownHole/README.md`, `TP-DownHole/CC-BY-SA-4.0.txt`, `TP-DownHole/GNU-GPL-V3.txt`; no README, CITATION.cff, or .zenodo.json in TLog or TP-DownHole-No2.
- Every `.sch`/`.brd` in `TLog/ALog-TLog/`, `TP-DownHole/Hardware/`, `TP-DownHole-No2/` (library names, parts, free text, designrules). `TLog/ALog-TLog/TLog.lbr` has no `<library name>` tag (standalone library file).
- `TP-DownHole/*.job`, `.dri`, `.gpi`, `.pro`: no SparkFun/Adafruit names (dead end).
- Firmware `.ino` files: Arduino includes only; no attribution headers (dead end).
- Full `git log` of all three repos; commits `8be4902`, `8120727`, `30a57ec`, `ebae734`, `33ca930`, `c5b0b0d`, `6caf12b`, `343f16d`, `fe3d8a1` inspected.
- `gh api repos/NorthernWidget/{TLog,TP-DownHole,TP-DownHole-No2}`: none is a fork; created 2017-07-14, 2017-01-27, 2017-07-28; licenses LGPL-3.0, NOASSERTION, CC-BY-SA-4.0. GitHub commits/contents for TP-DownHole-No2 (two commits absent locally).
- Searches for "feather", "arduino", "mighty", "1284", "328P": only SparkFun library description text (Arduino stackable headers, RedBoard links); no board-level Arduino/Adafruit parent found.

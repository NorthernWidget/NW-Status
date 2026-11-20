STATUS: COMPLETE

# ALog lineage: ALog-BottleLogger, ALog-LogMega, ALog-Shield

Checked 2026-11-20, read-only. Paths are relative to the workspace
`/home/awickert/Dropbox/NorthernWidget/github`. Local clones of ALog-BottleLogger and
ALog-LogMega are behind GitHub (local HEADs 0973b37 and 269627d; GitHub HEADs aab407e
2026-11-04 and 507e2b7 2018-06-17); remote-only facts below are marked "GitHub".

## Family tree (summary)

```
Arduino reference designs (SmartPrj / MyPOW Eagle libraries; ATmega328 + FT232RL USB core)
  + SparkFun Eagle libraries (CC-BY-SA 3.0, later 4.0) + Adafruit Eagle library
        |
ALog BottleLogger v0.6.6 (Apr 2012, ATmega328P-PU DIP, Eagle 5 binary)
        |
ALog BottleLogger v1.0.0 (2013; ATmega328 + FT232RL + USB-B, Duemilanove-style)
   |            |                                   |
   |      ALog-LogMega v0.8.2/0.8.3 (2013-2014)     ALog-Shield v1 (Aug 2015; Uno R1/R2 shield
   |      = BottleLogger + Arduino Mega 2560         carrying BottleLogger peripherals)
   |                                                     |
BottleLogger v1.1-v1.4 (2016, 328) -> v2.x (2017, 328P-MU, FT231X)  -> ALog-Shield v2.x (2017,
   |                                                                    "based on new BottleLogger")
BottleLogger v3.0.0 (2017-18, 1284P/644 family, Schulz libraries)
   |
Project-Margay (2018, Schulz; README: "based on the ALog series")
network-logger-umn (2017, UMN senior design; copy of BottleLogger v2 hardware)
```

## Design 1: ALog-BottleLogger

- License: `ALog-BottleLogger/LICENSE` = CC BY-SA 4.0 full text (line 1). `LICENSE.html` names
  "Andrew D. Wickert and Northern Widget LLC" (mixed wording "4.0 ... Unported"). History:
  23c123a 2013-09-11 "Create LICENSE.html: CC-BY-SA" (content = by-sa/3.0); 7bb0081 2017-06-06
  "CC-BY-SA 3.0"; 3650093 2018-06-16 "CC-BY-SA 3.0 --> 4.0". Schematic frame text
  `ALog-BottleLogger.sch:22098` "This work is licensed under the Creative Commons
  Attribution-ShareAlike 4.0". GitHub license: CC-BY-SA-4.0.
- First commit: 553b069 2013-09-11 Andy Wickert; GitHub created 2013-09-11T14:07:15Z; not a
  fork. Oldest design: branch origin/0.6.6 (0389e1f) `logger066_4ch_16APR12.sch` (Eagle 5
  binary; filename dates it 16 Apr 2012); strings show libraries SparkFun, adafruit, awickert;
  ATMEGA328P-PU; Adafruit SDMMC 06132, LP298X/LP2985; DS3231SN; 4050 level shifter. A SparkFun
  library description string is present ("+/- indicate SparkFun standard batteries and wiring").
- v1.0.0 (tag 1.0.0 = 6a0750b, 2013-09-11) `logger100.sch`: MCU = library "SparkFun"
  deviceset ATMEGA168 value "ATMega328"; U1 = SparkFun-DigitalIC FT232RL-BASIC; JP5 =
  SparkFun-Connectors USB; COUT from library "SmartPrj"; VUSB symbols from "MyPOW"; SD, LP2985
  LDOs and AVRISP from "adafruit"; RTC from "comfile" DS3231SN; OSHW logo from
  SparkFun-Aesthetics; board design rules `<designrules name="SparkFun">`.
- Arduino parent: README (all versions) "Arduino-based"; GitHub description "Arduino-compatible".
  SmartPrj and MyPOW are the library names in Arduino's own Eagle reference files: a GitHub copy
  of Arduino's reference `Arduino_Micro_Rev03j.sch` (repo BeAnotherLab/The-Machine-to-be-Another-Unity,
  path Arduino/Shield/Arduino_Micro_Rev03j.sch) contains both `<library name="MyPOW"` and
  `<library name="SmartPrj"` and the title "Arduino MICRO" (checked via gh api 2026-11-20).
  ATmega328 + FT232RL USB-serial is the Arduino Duemilanove topology (inference, not stated in
  files). Confidence: Arduino lineage likely (verified that the board is "Arduino-based";
  specific board parent not named).
- SparkFun: libraries SparkFun, SparkFun-LED, SparkFun-PowerSymbols, SparkFun-Retired (current
  sch lines 8311, 8895, 13395); SparkFun library header `ALog-BottleLogger.sch:8321` "Licensing:
  Creative Commons ShareAlike 4.0 International". v1.0.0 MCU and FTDI symbols are SparkFun's.
- Adafruit: library "adafruit" (sch:160) for SD socket and ISP header (brd:4317, brd:4250).
- Collaborator credit: 0bb16e6 2016-04-27 "10nF chip caps for analog, following Gerhard
  Oberforcher"; 32e9d9e "power-saving clock circuits (h/t Gerhard), with Chad Sandell".
- Evolution: 1.1.0/v1.4 (2016) still SparkFun ATMEGA168/ATMega328; v2.0.0 (2017-02-07) ATMEGA328P-MU
  from Atmel_By_element14, FT231X; bcd69e2 2017-07-19 Chad Sandell "Major revision, 1284P 16 channel
  16-bit ADC"; v3.0.0 (2018-09-14) MCU IC2 bschulz ATMEGA644* (MPN ATMEGA644PA-MUR, sch:22733),
  FT231X, LTC2495, DS3231M from bschulz libraries.
- UMN: silkscreen `ALog-BottleLogger.brd:235-238` "Developed in part at the University of
  Minnesota in parntnership with Northern Widget LLC" (first appears bcd69e2, 2017-07-19, via
  `git log -S`); "Made in Minnesota" (brd:232). GitHub .zenodo.json: creators Sandell, Wickert,
  Schulz all "Northern Widget LLC".
- Descendants: README deprecation note names Project-Margay ("Small form factor ALog-like data
  logger") and Project-Resnik as successors. Project-Margay/README.md:9 "Project Margay is a
  micro-scale environmental data logger based on the ALog series" (verified). network-logger-umn
  (first commit 773f6de 2017-02-04 cesar034) README:3 "heavily based off the Alog library by
  Northern Widget"; `network-logger-umn/Hardware/Logger_PreviousDesigns/` is a copy of ALog
  BottleLogger v2 (README line 1 "ALog-BottleLogger"; MCU ATMEGA328P-MU) (verified).
  TLog/ALog-TLog (Schulz 2017) carries the ALog name and the MyPOW library (possible).
- Patents: only the CC BY-SA 4.0 clause, `LICENSE:215` "Patent and trademark rights are not
  licensed under this Public License." No patent notice anywhere in the three repos.

## Design 2: ALog-LogMega

- License: local `LICENSE.html` CC BY-SA 3.0, "Andrew D. Wickert and Northern Widget LLC".
  GitHub has an added LICENSE (507e2b7 2018-06-17 "Update LICENSE", first line
  "Attribution-ShareAlike 4.0 International"); GitHub license CC-BY-SA-4.0.
- First commit 984db03 2013-09-11; second 809a124 2013-09-11 "Starting to splice together the
  ALog BottleLogger and Arduino Mega" (verified, two parents named). GitHub created
  2013-09-11T15:07:36Z, not a fork. 15 commits, all Andy Wickert; last local 269627d 2014-06-16.
- Arduino Mega: IC3 = library "SmartPrj" deviceset ATMEGA2560 (logmega.sch:21408); README "Arduino
  Mega (ATmega 2560) version of the ALog"; awickert devicesets ARDUINO_SHIELD_BIGLOG_1/2
  (sch:9982, 10028) whose symbol carries "ARDUINO / Duemilanove / Diecimila / UNO R1/R2 / Shield
  Layout for Pin Purposes (ALog)" (sch:9813-9845): it hosts Arduino shields.
- SparkFun: libraries SparkFun, -Aesthetics, -Connectors, -DigitalIC (FT232RL-BASIC U1),
  -Electromechanical, -LED; DS3234 RTC from SparkFun; board design rules `<designrules
  name="SparkFun *"` (logmega.brd:1939); SparkFun library licensing text logmega.sch:10151 "CC
  v3.0 Share-Alike".
- Adafruit: adafruit AVRISP, LP298X (LP2985), SDMMC. awickert library parts copied from Adafruit,
  stated outright: sch:9723 "Based on Adafruit, except w/ keepout on top." (CR2032-SMD package),
  sch:9904 "From Adafruit (3V)" (COIN3V symbol), sch:10125 "Adafruit's CR2032 except with a
  keepout." (verified).
- Descendants: none named in files. Branch origin/FoleyMechatronics (= 269627d) suggests an
  outside builder (possible).

## Design 3: ALog-Shield

- License: `ALog-Shield/LICENSE` CC BY-SA 4.0 (d9854b7 2018-06-16 "Create LICENSE"; LICENSE.html
  deleted 3bfc6cf). Schematic text still says 3.0: ALog-Shield.sch:30930 "Released under the
  Creative Commons Attribution Share-Alike 3.0 License ... Design by: Andrew D. Wickert and Chad
  T. Sandell with assistance from Bobby Schulz". .zenodo.json: Wickert "University of Minnesota,
  Department of Earth Science"; Sandell "Northern Widget"; Schulz (no affiliation); license
  cc-by-sa-4.0.
- First commit c1b5bf9 2016-03-17; 3fcbb73 2016-03-17 "First version from August 2015"
  (shield100r1.sch). GitHub created 2016-03-17, not a fork.
- Parent BottleLogger v1.0.0: shield100r1.sch reuses the BottleLogger v1.0.0 designators and
  parts one-for-one: LSHIFT 4050, LD0_SD/LD0_SENSE adafruit LP298X, SD adafruit SDMMC, RTC
  comfile DS3231SN, MANUAL_LOG awickert TL3350, Q1/Q2 FDN360P, IC1 LTC4412, COUT SmartPrj, VUSB
  MyPOW; it drops the MCU and USB and adds awickert ARDUINO_SHIELD_PIN_PURPOSE (likely, strong).
  v2 explicitly: ebadf7f 2017-03-01 "Update based on new ALog BottleLogger from weeks ago"
  (verified).
- Arduino Uno shield: README "An Arduino shield with all the capabilities of the ALog
  BottleLogger"; symbol text "ARDUINO Duemilanove Diecimila UNO R1/R2 Shield Layout"
  (ALog-Shield.sch:22930-22934); "POWER: SIMPLY USE ARDUINO 3V3" (sch:30923); c320763 2018-09-14
  "fixed IOREF issue" (verified: Arduino Uno shield form factor).
- SparkFun: SparkFun, -Aesthetics, -Connectors, -LED libraries; SparkFun DS3231M datasheet link
  (sch:24680). Board design rules `oshpark-2layer *` (OSH Park, not SparkFun).
- Adafruit: SD1 adafruit SDMMC 06132 (sch:30313).
- UMN: silkscreen ALog-Shield.brd:172-176 "Northern Widget LLC and University of Minnesota"
  (v2.2.0, 06 June 2017), brd:216-219 "Developed in part at the University of Minnesota in
  parntnership with Northern Widget LLC" (first in 79eeeea 2017-06-06).

## Openness and patent timeline (facts only)

- Public, share-alike-licensed disclosure: BottleLogger v0.6.6 (Apr 2012 design) and v1.0.0
  published on GitHub 2013-09-11 under CC BY-SA 3.0; LogMega the same day; ALog-Shield
  2016-03-17. Paper: Wickert (2014) Bull. Ecol. Soc. Am. 95(2) 68-78 (cited in BottleLogger README).
- The UMN credit on silkscreen first appears 2017-06/07, years after the first public release.
- No patent claim, notice, or UMN license text in any of the three repos. CC BY-SA 4.0 explicitly
  does not license patents (BottleLogger LICENSE:215); it is a copyright license on the design files.

## Sources checked (dead ends included)

- README.md, LICENSE, LICENSE.html in all three; .zenodo.json (ALog-Shield local; BottleLogger GitHub).
- ALog-BottleLogger.sch/.brd (current), tags 1.0.0, 1.1.0, v1.4, v2.0.0, v2.2.0, v3.0.0, branch
  origin/0.6.6 (binary Eagle 5; strings only).
- logmega.sch/.brd; commits 809a124, e179f75, 6d46d2b.
- ALog-Shield.sch/.brd; shield100r1.sch at 3fcbb73.
- git log keyword search (arduino, sparkfun, adafruit, based, from, fork, license, patent, UMN)
  in all three: hits listed above.
- gh api repos/NorthernWidget/{ALog-BottleLogger,ALog-LogMega,ALog-Shield}: none are forks.
- gh code search for SmartPrj/MyPOW: confirmed in Arduino_Micro_Rev03j.sch copy and Adafruit
  METRO-328 schematics. No local Arduino reference file exists in the workspace (dead end).
- Backups: ALog-Shield-backup2/.backup3 history begins at the same c1b5bf9 (no older history);
  ALog-Shield.backup and ALog-Shield-Local are not git repos; ALog-BottleLogger2 has 4 commits from
  2015-11-10 (not examined further); ALog (382 commits, 2013-09-08) is the firmware library, not
  hardware (not examined: outside this assignment).
- grep "patent|minnesota|regents": only LICENSE:215, silkscreen text, ALog-Shield .zenodo.json.

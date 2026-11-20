STATUS: COMPLETE

# Margay lineage (raw findings)

Repositories: Project-Margay (primary), with Project-Margay.old, pre-LFS-Project-Margay and Project-Margay.lfs for history only. Paths are relative to the workspace `/home/awickert/Dropbox/NorthernWidget/github`. All work was read-only (`git show`, `git log`, `grep`). A copy of the first schematic, `git show ed9bf1c:Blackfoot.sch`, went to the session scratchpad and nowhere inside a repository.

## Design: Margay (Eagle v0.x to v3.0, and the KiCad conversion v3.1)

### Licensing as found
- `Project-Margay/LICENSE.md`: CC BY-SA 4.0 (full text). Line 75: "Patent and trademark rights are not licensed under this Public License."
- `Project-Margay/README.md:626`: hardware and documentation are CC BY-SA 4.0, and `Software/` is GPL v3. `README.md:135`, "Open-source licensing via GNU GPL 3.0", sits under the software/firmware heading, so the two lines agree.
- `Project-Margay/Software/LICENSE`: the GPL v3 text.
- GitHub (`gh api repos/NorthernWidget/Project-Margay`): fork=false, parent=null, created 2018-02-28T22:29:24Z, license CC-BY-SA-4.0. The old NorthernWidget-Skunkworks name redirects to the same repository (it was transferred).
- License history:
  - db93dcd (2018-02-28, the initial commit): `LICENSE` was **MIT**, "Copyright (c) 2018 NorthernWidget-Skunkworks".
  - 12e2a61 / 4c54ef2 (2018-06-28, Bobby Schulz, "Updated licence"): MIT removed. Added `LICENSE.md` ("Project Margay (c) by R. C. Schulz ... licensed under a Creative Commons Attribution-ShareAlike 4.0 International License"), a CC BY-SA badge in the README, and a file `CC-BY-SA-4.0.txt`.
  - 296967a (2023-01-22, Andy Wickert, "Incorrect license CC-BY-SA 4.0 is (see LICENSE.md)"): deleted `CC-BY-SA-4.0.txt`, whose text began "Attribution-NonCommercial-ShareAlike 4.0 International". **From 2018-06-28 to 2023-01-22 the repository therefore carried the BY-NC-SA text under a BY-SA filename**, while the README and LICENSE.md said BY-SA.
  - d7846fc (2023-10-24): LICENSE.md now holds the full BY-SA 4.0 text in Markdown.
- Patents: no patent mention anywhere in README, docs or Production apart from the CC clause above.

### Parent 1: ALog TLog (Bobby Schulz, NorthernWidget/TLog), the direct predecessor. LIKELY, strong
- `Project-Margay/README.md:9`: "Project Margay is a micro-scale environmental data logger based on the ALog series." (verified as a statement of descent from the ALog family, though it names no specific board)
- The first Margay design was called **Blackfoot**. ed9bf1c (2018-02-28, Bobby Schulz, "First commit, schematic complete, board routing in progress") added `Blackfoot.sch`/`Blackfoot.brd`. 5371856 (2018-03-06, "Final Gerbers, renamed design") renamed them `Blackfoot.* => Margay.*`.
- `TLog/ALog-TLog/TLog.sch` (TLog "Mrk 1.2"; commits 3d896eb 2018-02-07 "Presumptive Mrk 1.2" and b15ec1a 2018-02-08 "Updated Gerbers, ready for final review") was finished three weeks before Blackfoot, by the same author.
- Parts overlap. Of the 26 distinct library:deviceset pairs in Blackfoot, 21 are also in TLog.sch: bschulz:ATMEGA644* (device "M" in both, part name IC1 in both), FT231X, DS3231M, MAX6070AAUT*, MIC842, MICRO_USB_LONGPADS, CRYSTAL_5X3.2_2LEAD, BATTERY_COIN, AVRISP, BUTTON, CLVBA-FKA, MOSFET-NCH, MOSFET_PCH, bschulz_passives:C-EU, bschulz:R-EU_, bschulz:C-EU, MyPOW:VUSB, SparkFun-PowerSymbols GND/VCC, supply1/supply2 GND. Blackfoot's extras are the Adafruit SDMMC, two SparkFun-Jumpers, MCP3425, TPS797*, CONN_02/4/6. Method: grep of `<part ... library= deviceset=>` in both files, then `comm`.
- Named nets shared by Blackfoot and TLog.sch: 3.3V_EXT_CTRL, EXT_3.3V, ALIVE_LED, LOG_INT, RTC_INT, EXT_INT, SD_CD, SD_CS, LED1, LED2, LED3, DTR, RX, TX, RST, MISO, MOSI, SCK, SDA, SCL, VUSB, 3V3. That is 22 named nets of Blackfoot's 56 total nets.
- TLog itself: `TLog/LICENSE` is LGPL v3. GitHub: created 2017-07-14, license LGPL-3.0, not a fork. Its directory is named `ALog-TLog`, and its other schematics (`Logger_v2.sch`, `TLog_HighSpeedADC.sch`, `BatteryModule.sch`) use many SparkFun-* Eagle libraries (Clocks, Connectors, DiscreteSemi, Fuses, IC-Microcontroller, IC-Special-Function, LED, RF, Passives, PowerSymbols, Jumpers) and `adafruit`. That points to SparkFun ancestry one step up, for the TLog agent to confirm.
- Why "likely" rather than "verified": no file or commit says "based on TLog" in words. However, the README's "ALog series" combined with the 21 shared devicesets, the same IC1 designator and the 22 named nets is strong.

### Parent 2: ALog BottleLogger (Wickert / Schulz / Sandell). LIKELY, as a grandparent through the shared ALog circuit
- `ALog-BottleLogger/ALog-BottleLogger.sch` (file commits 2017-06-06 to 2017-12-29 by Andy Wickert and Chad Sandell, cleanup 59a8b08 2018-09-14) shares 14 devicesets with Blackfoot: ATMEGA644* (bschulz, IC2), AVRISP, DS3231M, FT231X, MAX6070AAUT*, MIC842, MICRO_USB_LONGPADS, MOSFET-NCH, MOSFET_PCH, SDMMC, VUSB, C-EU, R-EU_, GND.
- It also shares 10 named nets: 3.3V_EXT_CTRL, EXT_3.3V, RTC_INT, SD_CS, DTR, RST, SCL, SDA, VUSB, GND. That is fewer than TLog shares (22), so TLog is the nearer parent.
- `README.md:9` ("based on the ALog series") covers this.
- Compared and weak: `ALog-LogMega/logmega.sch` (6 generic devicesets, 4 nets) and `ALog-Shield/ALog-Shield.sch` (7 devicesets including DS3231M and SDMMC, 5 nets). `ALog-BottleLogger2/BL1284P_DataLogger_V2.00/*` (a different design lineage, BL1284P) has no overlap.

### Parent 3: SparkFun Eagle libraries (CC BY-SA 4.0 per SparkFun). VERIFIED for specific parts
- `Project-Margay/Hardware/Margay.sch:224` and `:10833`: `<library name="SparkFun-PowerSymbols">` (urn:adsk.eagle:library:530), with SparkFun's text "If you enjoy using this library, please buy one of our products at SparkFun.com" (`:231`). Used for GND1–4, GND17, GND20, GND22 and GND25 (parts list from `:12464`).
- Blackfoot `ed9bf1c:Blackfoot.sch` lines 10539 and 10571: JP1 `library="SparkFun-Jumpers" library_urn="urn:adsk.eagle:library:528" deviceset="JUMPER-SMT_3_1-NC_PASTE"` (package3d urn 39293/1) and JP2 `SparkFun-Jumpers` `JUMPER-SMT_2_NO` (package3d 39279/1).
- In current `Margay.sch` these sit inside the `bschulz` library but keep SparkFun's package3d URNs: `:12511` JP2 JUMPER-SMT_3_1-NC_PASTE urn 39293/1, `:12561` JP1 JUMPER-SMT_2_NO urn 39279/1, and `:12541` JP3 JUMPER-SMT_2_NC_PASTE urn 39282/1. They also keep SparkFun's descriptions: `:5070`–`:5071` "SparkFun Product that uses the round pads: SparkFun EL Sequencer". So these were copied from SparkFun-Jumpers into bschulz.lbr (verified by the URN and the text).
- bschulz devicesets that carry SparkFun description text verbatim (verified copied from SparkFun libraries) and are placed on the board:
  - DS3231M, `Margay.sch:3290`–`:3297`, "SparkFun Products ... CryptoCape (DEV-12773) ... SparkFun CryptoShield (DEV-13183)". Used as RTC1 (`:12459`).
  - MOSFET_PCH, `:3324`–`:3329`, "SparkFun Products: SparkFun ESP32 Thing ... ESP8266 Thing". Used as Q2 FDN360P (`:12547`).
  - The same DS3231M and MOSFET_PCH text is already in Blackfoot (ed9bf1c, Blackfoot.sch lines 5116–5119 and 5149).
- Unplaced bschulz packages with SparkFun text (library content only, not on the board): TO220V `:441`, 1X10-2MM `:1176`, 1X10-2MM-SMD `:1213`, 1X10_SMD_COMBINED `:1393`, 1X10_SMD_MALE `:1450`.
- MOSFET-NCH (`:3921`, symbol LABELED-NMOS): the naming matches SparkFun-DiscreteSemi, but the description here carries no SparkFun text. POSSIBLE.
- KiCad conversion: the SparkFun text survives into `Project-Margay/Hardware/KiCAD/Control_Connectors.kicad_sch:1887` (normally-open jumper, "Round pads are ..."), `Power_Sensors.kicad_sch:1231` (DS3231M, cdn.sparkfun.com datasheet link) and `Power_Sensors.kicad_sch:3695` (P-channel MOSFETs, "SparkFun Products: SparkFun ESP32 Thing"). Every KiCad symbol and footprint now comes from `nw-cold-silicon` (126 lib_id, 84 footprint references; `sym-lib-table` and `fp-lib-table` name only nw-cold-silicon). The SparkFun lineage therefore passes through NW-Cold-Silicon.

### Parent 4: Adafruit Eagle library (adafruit.lbr, CC BY-SA). VERIFIED for the SD-card part's origin
- Blackfoot `ed9bf1c:Blackfoot.sch:10531`: `<part name="U$3" library="adafruit" deviceset="SDMMC" device="06132"/>`. The adafruit library begins at line 9936, and its first package is "SCDA".
- Current `Margay.sch:4251`: bschulz SDMMC deviceset, description "SD MMC Card holder ... 4UCON part #06132 - easy to solder". Its devices are SCDA, 18650/SDCARD, 06132 and WR-CRD, and `<package name="SCDA">` is at `:905`. The deviceset is the Adafruit one moved into bschulz.lbr.
- The placed J1 (`:12510`; `Margay.brd:2609`) uses the added device WR-CRD on package SD_WURTH_WR-CRD. The **footprint** on the v3 board is therefore a later NW addition (Würth), while the symbol and deviceset descend from Adafruit's. The Adafruit-library origin is verified by commit; the attribution of the "4UCON 06132" text to Adafruit's own library rests on its first appearance under `library="adafruit"`.

### Parent 5: microBuilder.eu Eagle library (Kevin Townsend). VERIFIED, public domain
- `Margay.sch:12272`: `<library name="microbuilder">`, whose description (`:12273`–`:12282`) says "This work is placed in the public domain". It supplies J4 USB_C (`:12616`, deviceset at `:12424`). The library first appears in 364c9ef (2022-05-01, Andy Wickert, "USB-C conversion in progress: moving parts"). Public domain carries no share-alike obligation.

### Parent 6: Cadsoft/Autodesk Eagle stock libraries. LIKELY
- `Margay.sch:191`: `supply1` (urn:adsk.eagle:library:371), used for 26 GND symbols.
- bschulz_passives C-EU / R-EU_ ("CAPACITOR, European symbol" `:8393`; "RESISTOR, European symbol" `:9334`) match Eagle's `rcl` library text.
- bschulz ATMEGA1284* (`:3225`), with "Source: http://www.atmel.com/dyn/resources/prod_documents/doc2593.pdf" and symbol ATMEGA644E, matches Eagle's stock `atmel` library entry (likely; no URN kept).
- FRAME_A_L (`:4349`) matches Eagle's `frames` library.

### Arduino / MightyCore (firmware lineage, not board copper). VERIFIED as a software dependency, not as a hardware parent
- `README.md:343`: "the MightyCore board files can be used. These are the board files the Northern Widget ones were based on".
- `Arduino_Boards/NorthernWidgetAVR/cores/MightyCore/` exists, and `variants/NW1284p/pins_arduino.h:7` is headed "MIGHTYCORE STANDARD PINOUT".
- `Arduino_Boards/README.md:5`: "(This repository and README based gratuitously off of Sparkfun's)".
- The README (`:286`) and 12e2a61 tell users to select the "TLog v1" definition, which also ties Margay to TLog. However, the current `Arduino_Boards/NorthernWidgetAVR/boards.txt` names only ALog BottleLogger (legacy), ALog BottleLogger v2, ATMega644p 8MHz and ATMega1284p 8MHz (lines 13, 39, 65, 91). "TLog v1" is not present.
- The board does not follow an Arduino Uno/Mega shield form factor. The ATmega644 (v0/v1) and then ATmega1284P (v2 from 3c04469 2018-09-10, "First round of v2 updates to schematic") run Arduino through MightyCore. No Arduino reference-design copper was found.

### Margay-internal versions (self-lineage)
- v0 "Blackfoot" (ed9bf1c 2018-02-28) became Margay and then Margay 1.0 (834f646 2018-04-10 "Margay 1.0 initial layout").
- v2 (3c04469 2018-09-10 to a424de6 2018-09-17), v2.1 (ba247f6 2019-04-12) and v2.2 (f82b580 2019-05-12) followed.
- USB-C conversion started 2022-05-01 (364c9ef), leading to v3.0. The KiCad port is v3.1 (fa76224 2026-11-04 Production/README).
- Branches in old copies: 0603-wdt-select-resistor (PR #30/#32), Dev_v2 (PR #20/#21) and awickert-dev. Sibling folders Project-Margay-0603wdt and Project-Margay-newUSBinProgress exist in the workspace but were not opened (they are working copies of those branches by name only, unverified).

## Sources checked
- Project-Margay: LICENSE.md, README.md (whole-file grep), CITATION.cff, Software/LICENSE, Hardware/Margay.sch, Hardware/Margay.brd, Hardware/KiCAD/{fp-lib-table, sym-lib-table, README.md, *.kicad_sch, Margay.kicad_pcb}, `git log` (all branches, 363 commits), commits db93dcd, ed9bf1c, 5371856, 12e2a61, 4c54ef2, 296967a, d7846fc, 364c9ef. No .dru or .cam file exists anywhere in its history (dead end).
- Project-Margay.old (72 commits, last 2020-04-25), pre-LFS-Project-Margay (150, last 2021-02-28), Project-Margay.lfs (153, last 2020-04-26): same root commits and early history (hashes differ in .old). No additional lineage messages beyond "Updated licence" and "Vector diagram for analog jumper on silk" (dead end).
- `gh api repos/NorthernWidget/Project-Margay`, `repos/NorthernWidget-Skunkworks/Project-Margay` (redirect) and `repos/NorthernWidget/TLog`.
- TLog: LICENSE, ALog-TLog/*.sch library lists, TLog.sch parts and nets, `git log`.
- ALog-BottleLogger/ALog-BottleLogger.sch (libraries, parts, nets, history); ALog-BottleLogger2 (3 schematics, no overlap); ALog-LogMega/logmega.sch; ALog-Shield/ALog-Shield.sch.
- Arduino_Boards: README.md, NorthernWidgetAVR/boards.txt, cores/, variants/NW1284p/pins_arduino.h.
- Patent grep: README.md, LICENSE.md, docs/, Production/.

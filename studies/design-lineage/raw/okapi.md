STATUS: COMPLETE

# Okapi design lineage (raw findings)

Repository: Project-Okapi (read-only inspection, 2026-11-20)

## Design: Okapi (dev code name "Resnik"), Eagle original `Project-Okapi/Hardware/Okapi.sch` / `.brd`

### License and credits (verified)
- `Project-Okapi/LICENSE:1` reads "Attribution-ShareAlike 4.0 International" (CC BY-SA 4.0 full text; added in commit 6e41aeb, 2018-10-18, Bobby Schulz, "Added Creative Commons Licence").
- `Project-Okapi/CITATION.cff:9` `license: CC-BY-SA-4.0`; `.zenodo.json` `"license": "cc-by-sa-4.0"`; concept DOI 10.5281/zenodo.3766482 (CITATION.cff:6). Authors: Bobby Schulz, Andrew D. Wickert; both listed with affiliation "Northern Widget LLC; University of Minnesota" (CITATION.cff:14,18).
- `Project-Okapi/README.md:76` "Open-source licensing via CC BY-SA 4.0" (hardware); `README.md:87` "Open-source licensing via GNU GPL 3.0" (software); `README.md:689` CC BY-SA 4.0 badge.
- `README.md:678-684` Acknowledgments: support from UMN ESCI, USGS, WMO (logos only; no grant numbers in the file).
- `README.md:123-125` "The socket holds a [Feather-form-factor board](https://learn.adafruit.com/adafruit-feather/feather-specification). This standard, designed by [Adafruit], has been widely adopted, including by ... [Particle]." `README.md:8` "interfaces with a range of 'Feather'-form-factor boards for telemetry."
- `README.md:8,22,82` Arduino framework / "Arduino compatible"; `README.md:83` custom bootloader/board definition for ATmega1284p in NorthernWidget/Arduino_Boards.
- No README text names a parent board (no "based on", "derived from" Margay or any vendor design).

### Eagle libraries embedded in Okapi.sch (verified, line numbers in `Project-Okapi/Hardware/Okapi.sch`)
| Library | sch line | Parts that use it | Stated license in the embedded library |
|---|---|---|---|
| bschulz | 198 | almost every IC, connector, LED, switch | none stated |
| bschulz_passives | 12624 | all R/C | none stated |
| awickert | 18791 | U$1, U$2 (VDIV-JP); board logo U$4 NWLOGO_MED (brd) | none stated |
| microbuilder | 20103 | J10 USB-C (package USB_C_CUSB31-CFM2AX-01-X) | "This work is placed in the public domain" (sch 20103-20115) |
| SparkFun-Jumpers (urn:adsk.eagle:library:528) | 18429 | JP1-JP7 (JUMPER-SMT_2_NO _SILK), JP8 (JUMPER-SMT_3_1-NC_PASTE _SILK) | "Creative Commons ShareAlike 4.0 International" (sch ~18440) |
| SparkFun-PowerSymbols (urn:adsk.eagle:library:530) | 18729 | GND46, GND66-69, SUPPLY9, SUPPLY10 (symbols only) | "Creative Commons ShareAlike 4.0 International" |
| supply1, supply2 | 18377, 18701 | GND/VCC symbols | Eagle stock libraries; no license text |
The `.brd` carries the same set minus the symbol-only libraries (`Okapi.brd`: bschulz 484, bschulz_passives 363, awickert 2025, microbuilder 3360, SparkFun-Jumpers 1966).

### SparkFun-origin content inside the `bschulz` library (verified text; origin = likely)
The bschulz library carries SparkFun library description text verbatim, which indicates the entries were copied from SparkFun Eagle libraries (SparkFun-Connectors, SparkFun-Clocks, etc.). Entries actually placed on Okapi:
- DS3231M deviceset (RTC1, package SO08), sch 9924-9932: "Datasheet https://cdn.sparkfun.com/datasheets/Dev/Beagle/DS3231M.pdf ... SparkFun Products: CryptoCape (DEV-12773), SparkFun CryptoShield (DEV-13183)".
- JST_2MM_MALE deviceset (J8, package JST-2-SMD), sch 11562-11578: "Here is the connector we sell at SparkFun: ... (PRT-08612) ... It was used on these SparkFun products: SparkFun MOSFET Power Controller (PRT-11214), SparkFun Battery Babysitter (PRT-13777)". Package JST-2-SMD sch 3583 has SparkFun's "Datasheet referenced for footprint" format.
- MOSFET_PCH deviceset (Q-parts), sch 10245-10250: "SparkFun Products: SparkFun ESP32 Thing, SparkFun ESP8266 Thing".
- MICROSD deviceset sch 10860: "For the 3M # 2908-05WB-MG and/or 4UCON #19656 push-push type" (SparkFun-Connectors wording; possible); placed part SD1 uses bschulz's own MICROSD_CD package (sch 4165, "built for the Molex 5025700893 socket"), i.e. NW-drawn footprint.
- Unplaced SparkFun-text packages also present in bschulz (1X10-2MM 2361, SCREWTERMINAL-3.5MM-2 3554, JST-2-PTH 3833 "match SparkFun LiPo battery terminations", TO220V 441 "SparkFun SKU: COM-10213"); these are library baggage, not on the board.
- ATMEGA1284* deviceset (IC1, MLF44-TH) sch 10795 and package sch 3258: "Source: http://www.atmel.com/dyn/resources/prod_documents/doc2593.pdf" (wording of Eagle's stock atmel.lbr; possible).
- No Adafruit library and no Adafruit attribution text anywhere in Okapi.sch or Okapi.brd (grep -i adafruit: 0 hits).

### Feather form factor (verified as a form-factor relation)
- bschulz deviceset FEATHERWING (prefix MS), sch 9611, devices "", _NODIM, LAYOUT, _SMD, _SMD_LAYOUT; packages FEATHERWING (2836), FEATHERWING_DIM (2878), FEATHERWING_MIN (2924), FEATHER_SMD (5484, "SMD plug to be inserted into Feather form-factor socket", TE drawing 1241150). Okapi places MS1 = FEATHERWING_MIN (brd element list). No description or attribution on the FEATHERWING packages (no Adafruit text): the footprint is NW-drawn to Adafruit's published Feather specification (README.md:123).
- Commit 2232870 (2018-10-30, Bobby Schulz) "Continued layout, starting on SD and Feather header".

### Particle (verified as an interface relation)
- bschulz deviceset B_SERIES_M.2EKEY_NOPROG (J9, package PARTICLE_M.2EKEY_NOPROG), sch 12130-12142 and symbol B_SERIES_M.2EKEY-1 sch 7204: "Particle B Series SoM ... 3042 M.2 Connector with E Key ... Width = 30mm Length = 42mm". No license or source line; whether the symbol was taken from Particle's published Eagle files is not stated (possible).
- `Project-Okapi/Particle_Files/` holds Boron sketches and `Resnik_Boron_Firmware.bin`; README.md:124-125,378-394 describe Boron/B-SoM integration. No Particle reference-design text or library found.

- Feather symbol (verified): FEATHERWING gate uses symbol MICROSHIELD (sch 9613, symbol at sch 6485) whose 28 pins are `!RESET 3V AREF GND GPIOA0-A5 GPIOSCK GPIOMOSI GPIOMISO GPIORX GPIOTX NC GPIOSDA GPIOSCL GPIO5 GPIO9 GPIO6 GPIO10 GPIO11 GPIO12 GPIO13 EN USB VBAT`, i.e. the Adafruit Feather 16+12 pin set. FEATHERWING is present from the very first schematic commit (52cc92c, 2018-10-23).

### Relation to Margay (likely: Margay v2 logger core reused)
- First schematic commit 52cc92c (2018-10-23, Bobby Schulz) created `Hardware/Resnik.sch` (renamed to Okapi in bb041bd, 2021-07-05, "Okapi naming"). Libraries then: bschulz, bschulz_passives, SparkFun-Jumpers, supply1. It holds the power path (LT3652, LTC4412, BQ2980, TPS6103x, TPS6282x, TLV61220, TPS22917), the FEATHERWING, DS3231M, BME280; no MCU yet.
- Next commit 45eee75 (2018-10-24, "Continued schematic additions, prelim part placement") adds ATMEGA644*, FT231X, AVRISP, SN74LVC1G3157, SparkFun-PowerSymbols. Named nets: 40 of the 44 non-auto nets in Margay v2 at Project-Margay a424de6 (2018-09-17, "Main v2 layout complete") appear in Resnik at 45eee75 (3V3_FTDI, DTR, ALIVE_LED, LOG_INT, RTC_INT, MOSI_BUF, SCK_BUF, SD_CS_BUF, SD_CD, SDA_CTRL, SDA_OB, SDA_EXT, RX_EXT, TX_EXT, VREF, VUSB, LED1-3, ...). Missing from Resnik: A0, VBAT-, VBAT_SW, VSWITCH. Method: `<net name=` sets from `git show a424de6:Hardware/Margay.sch` and `git show 45eee75:Hardware/Resnik.sch`, `comm -12`.
- Shared devicesets with Margay v2 (a424de6): AVRISP, BATTERY_COIN, BME280, BUTTON, CLVBA-FKA, CONN_02, CONN_4, CRYSTAL, DS3231M, FT231X, MOSFET-NCH, MOSFET_PCH, SN74AUP3G34, SN74LVC1G3157, TPS797*, SparkFun-Jumpers JUMPER-SMT_2_NO and _3_1-NC_PASTE, SparkFun-PowerSymbols. Both use ATMEGA644* in 2018; Okapi moves to ATMEGA1284* in 06fe36e (2019-08-14).
- `Project-Okapi/Hardware/Documents/PinConnections.txt:24` "LogButton (Input, PCINT) --PA4 (FIXEDish) //Keep convention w/Margay, not hardcore fixed" (added aaa1780, 2018-10-18): verified statement that the pin map follows Margay's convention.
- `README.md:577,583` serial-number Schema 0 is "the same 8-byte EEPROM block used by Margay ... identical scheme to Margay".
- USB-C J10 (added to Okapi in 7dc65e8, 2024-10-30, Bobby Schulz) sits in a library named `microbuilder` in both Okapi.brd and Margay.brd; NW-Cold-Silicon's footprint description says "Laid out by Andy Wickert (Project-Margay 364c9ef, 2022)" (`NW-Cold-Silicon/nw-cold-silicon.pretty/USB_C_CUSB31-CFM2AX-01-X.kicad_mod`), and `NW-Cold-Silicon/PROVENANCE.md:29` says Adafruit's microbuilder library "does not hold it in the 2015 release". Project-Margay 364c9ef = 2022-05-01 Andy Wickert "USB-C conversion in progress: moving parts". So the USB-C block descends from Margay's 2022 USB-C conversion (likely), and the microbuilder library tag is a carried name, not a microBuilder/Adafruit footprint (the embedded library header itself states public domain).
- Note: the current Project-Margay/Hardware/Margay.sch also shares ATMEGA1284*, MIC9409*, TLV3691, TPS210*, microbuilder USB_C with Okapi; the direction after 2019 runs both ways (common NW logger core), not only Margay to Okapi.

### Relation to Particle reference designs: not found
- No Particle reference-design text, library name or license in Okapi.sch/.brd. Particle appears as (1) the B-SoM M.2 E-key connector J9 (bschulz deviceset, added 7dc65e8 2024-10-30; `NW-Cold-Silicon/PROVENANCE.md:27` "from Bobby's working copy of bschulz, never committed to Cold-Silicon") and (2) Feather-socket use of the Boron (README.md:124-125). Interface relation only.

### Design rules and CAM (verified)
- 2018 board (52cc92c) design rules `oshpark-2layer` (OSH Park vendor DRU); 2024 board `Okapi.brd:3480` `jlcpcb-2layer` "JLC PCB Design Rules" (from 7dc65e8). Margay.brd:2142 also `oshpark-2layer`. Vendor rule files, not design parents.
- 2024 CAM `Hardware/Okapi_2024-11-02/CAMOutputs/GerberFiles/gerber_job.gbrjob`: Application EAGLE 9.6.2 (Autodesk), ProjectId Okapi, Owner Bobby Schulz (umn.edu address). File set copper_top.gbr etc. is Eagle's default CAM naming, not SparkFun's sfe-gerb274x. `Hardware/Resnik_2020-02-13_274x.zip` uses .cmp/.sol/.plc/.pls/.stc/.sts (Eagle's legacy gerb274x CAM naming). No SparkFun CAM job.

### KiCad conversion `Hardware/KiCAD-10import` (verified)
- `fp-lib-table` and `sym-lib-table` each hold one library, `nw-cold-silicon` (`../../../NW-Cold-Silicon`). All 250 footprints and 390 symbol instances use `nw-cold-silicon:`. The vendor-origin entries carry through by name: SMT-JUMPER_2_NO_SILK (JP1-JP7, SparkFun-Jumpers origin), JST-2-SMD (J8, descr keeps SparkFun text "JST-Right Angle Male Header SMT ... Datasheet referenced for footprint"), SO08 (RTC1), USB_C_CUSB31-CFM2AX-01-X (J10), FEATHERWING_MIN (MS1), PARTICLE_M.2EKEY_NOPROG (J9).
- NW-Cold-Silicon is itself CC BY-SA 4.0 (`NW-Cold-Silicon/LICENSE:1`); `NW-Cold-Silicon/PROVENANCE.md` table row "okapi": 68 embedded names, 50 identical to the library, 11 pads identical, 4 pads differ, 3 added, 2 unchecked.

### Archive branches (verified)
- `archive/c43-ct3528-attempt`: one commit ea0827e (2026-11-08, Andy Wickert), C43 in CT3528; merge-base 26d9ddc. No lineage content.
- `archive/resnik-polarity-marks-2020`: one commit 013bc0f (2020-04-30, Andy Wickert), polarity marks; merge-base 2bbd133. No lineage content.

### Derivatives inside the repository
- RockBlock breakout (`Hardware/RockBlock_Breakout.sch/.brd`, e8041fe 2018-11-09 onward) moved out in 37541ab (2021-07-05, "Moved to RockBLOCK-feather repo"): an Okapi-era Feather-format child, now its own repository.
- `Hardware/5V_LP_Test/` test boards (2019-02) use only bschulz, bschulz_passives, supply1: no vendor libraries.

### Software in the repository (verified)
- `HighPower_Tester/LICENSE`, `Serial_Ctrl/LICENSE`, `Particle_Files/LICENSE`: GNU GPL v3. `Serial_Ctrl/Serial_Ctrl.ino:4` includes `Adafruit_ADS1015.h` (Adafruit library dependency, not derived code). README.md:160 links Adafruit_ADS1X15 for the ADS1115.

### GitHub metadata (verified)
- `gh api repos/NorthernWidget/Project-Okapi`: fork false, parent null, created 2018-10-18T23:23:12Z, license CC-BY-SA-4.0, public.
- First commit d626c0c 2018-10-18 Bobby Schulz "Initial commit". Commit authors (all branches): Andy Wickert 402, Bobby Schulz 60, morandagny 7, Karen 7, Unknown 2.

### Openness and share-alike notes (facts only)
- Okapi's own license is CC BY-SA 4.0 since 2018-10-18 (6e41aeb), the day the repository was created and before any hardware file existed (52cc92c, 2018-10-23).
- Embedded third-party Eagle content placed on the board: SparkFun-Jumpers (CC BY-SA 4.0, stated in the embedded library), SparkFun-PowerSymbols (CC BY-SA 4.0, stated), SparkFun-text entries copied into bschulz (DS3231M, JST_2MM_MALE/JST-2-SMD, MOSFET_PCH; license not restated in bschulz), microbuilder (public domain, stated). The SparkFun CC BY-SA 4.0 content gives a share-alike obligation on the design files that include it, consistent with the CC BY-SA 4.0 Okapi already carries.
- Patents: nothing in the repository mentions a patent beyond license text. `Project-Okapi/LICENSE:215` (CC BY-SA 4.0 Section 2(b)(2)): "Patent and trademark rights are not licensed under this Public License"; the GPL v3 files (e.g. `HighPower_Tester/LICENSE:61-66`) carry GPL v3 patent language. Not checked against patent databases.

### Sources checked (dead ends included)
LICENSE; CITATION.cff; .zenodo.json; README.md (grep for vendors, Margay, licence); docs/v0.7-pre-build-checks.md (no lineage); Hardware/Documents/PinConnections.txt (Margay convention line 24); Hardware/Okapi.sch and .brd (libraries, part map, descriptions, design rules); git history all branches (grep of subjects; -S searches for FT231X, ATMEGA1284, AVRISP, microbuilder, B_SERIES, awickert, SparkFun-PowerSymbols, SN74LVC1G3157, jlcpcb-2layer); 52cc92c and 45eee75 Resnik.sch; Project-Margay a424de6 and HEAD Margay.sch, 364c9ef, Margay.brd design rules; Hardware/KiCAD-10import (lib tables, footprint and lib_id prefixes, vendor grep); NW-Cold-Silicon PROVENANCE.md, LICENSE, footprint descrs; Hardware/Okapi_2024-11-02 CAM and zip; Hardware/Resnik_2020-02-13_274x.zip listing; Hardware/5V_LP_Test/*.sch libraries; HighPower_Tester, Serial_Ctrl, Particle_Files licenses and includes; archive branches; gh api metadata; grep for MightyCore/Sanguino/Optiboot (none); BoM and assembly file vendor grep (none). Not examined: Mounting_Plate, 3Dprint, Simulations (mechanical/simulation, no electrical lineage expected); Okapi-backups zips (KiCad autosaves).

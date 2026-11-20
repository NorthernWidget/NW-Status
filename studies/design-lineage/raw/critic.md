STATUS: COMPLETE

# Completeness critic: design-lineage raw reports

Read-only on every repository. Checks run 2026-11-20. Paths relative to `/home/awickert/Dropbox/NorthernWidget/github`.

## Log of checks (appended as run)

### C1. Scope of the repository table (question 3)
- `upstream.md:86` built its table from `gh api orgs/NorthernWidget/repos` only. Two designs the reports *do* cover live in the other org: `gh api repos/NorthernWidget/ALog-LogMega` resolves to `NorthernWidget-Skunkworks/ALog-LogMega` (public, CC-BY-SA-4.0, created 2013-09-11) and `TP-DownHole-No2` to `NorthernWidget-Skunkworks/TP-DownHole-No2` (public, CC-BY-SA-4.0, 2017-07-28). The table therefore misses the whole public Skunkworks org.
- Board files in public repos that NO report covers (checked with `gh api repos/<r>/git/trees/<default>?recursive=1`, grep `.sch|.brd|.kicad_pcb`):
  - NorthernWidget org: `AtlasShield` (AtlasShield.sch/.brd, CC-BY-SA-4.0, 2014-06-26); `MaxBotix-Helper` (.sch/.brd, CC-BY-SA-4.0, 2019-03-21); `Break44` (fork of bschulz1701/Break44, 26 boards incl. `MS5803/MS5803_Breakout`, `PrimalLog/PrimalLogger_Feather`, `FeatherTestPointBreakout`, `DPS368`, `MS5837`, BQ2980/BQ25616 eval boards); `network-logger-umn` (11 files incl. `Hardware/Logger v2/Logger_v2.sch`, `Senior Design Prototypes/SAM21.sch`; named in `alog.md:74-76` only as a BottleLogger v2 copy, its own Logger_v2/SAM21 boards not traced); `ALog-BottleLogger2` (BL1284P_DataLogger_V2.00, 4 schematics; `margay.md:34` notes "a different design lineage" but nobody traced it).
  - NorthernWidget org, no board files (not designs): ALog-BottleLogger2.2, datalogger, DataCollector-Foley-Mechatronics, Wire-Strip-Card, AtlasNW, Margay-housing-WQ48.
  - NorthernWidget-Skunkworks (public, all CC-BY-SA-4.0): `ALog_telemeter` (logger_2G_GSM, 2016-11-23), `Project-Raven` (CurrentAmp), `Project-Longbow` (LongbowWidget), `Project-Astron` (Astron, Astron_AltOsc), `Project-Calypso` (SensorInterface, TSL238T-breakout, 1206LED-breakout), `Project-Tally` (EventCounter, EventCounter_I2C, SwitchedPowerAdapter), `Project-ThermalStake` (ThermistorControl, ProbeBoard 8/16, Probe Board 1.0), `ICSP-half-size-adapter`, `RockBLOCK-feather` (RockBlock_Breakout; `okapi.md:157` names it as an Okapi child but does not trace it), `Project-Monarch__Archive` (Long/ShortWaveModule; the Dyson/Monarch parent of Liasis and Libelle, cited in `sensors-b.md:12,23` from history only).
  - `Project-Bonnet` (public): no board files.

### C2. TLog: a verified parent the reports missed (question 1)
- `tlog-tp.md:208` rests TLog's NW parent on a GitHub description ("designed around the ALog 3.0 platform") and says "circuit descent is not shown in-file".
- Check: `network-logger-umn` (NorthernWidget org, GPL-3.0, UMN senior-design repo, first commit 773f6de 2017-02-04 cesar034) holds `Hardware/Logger v2/Logger_v2.sch` and `BatteryModule.sch`, the same filenames as `TLog/ALog-TLog/`. History: c4cbccb 2017-03-21 Bobby Schulz "Added logger schematic", 79fc417 2017-03-30 "PCB Complete, Ready for Checking", d68c9c8 2017-03-31 "PCB Major Issues Fixed". TLog's copy arrives in c5b0b0d 2017-07-14 "Added initial developments on the TLog BETA".
- Result: of 137 `<part name library deviceset>` lines in TLog's Logger_v2.sch, 135 are identical to network-logger-umn's (136 lines). The differences are GND36 (supply1) added and U3 `SparkFun-RF/RFM69` -> `RFM69H`. Of 92 net names in TLog's file, all are in the UMN file, which has one more (`EEPROM_WP`). Method: `grep -o` of `<part ...>` and `<net name>` then `diff`.
- Verdict: **VERIFIED** – TLog BETA (Logger_v2) is the network-logger-umn "Logger v2" board carried over with a radio-variant change. Chain: network-logger-umn Logger v2 (2017-03) -> TLog BETA (2017-07) -> TLog Mrk 1.x (2018-02) -> Margay "Blackfoot" (2018-02-28).
- BatteryModule.sch differs more (27 vs 49 parts, 26 differing part lines): likely an extended version; not traced further.
- Authorship and license of network-logger-umn: network-logger-umn commit authors are UMN students (cesar034, luke/Luke, David Nickel, nicke166, Jeffrey K Worm/wormx026, jeff-worm-delcom) plus Bobby Schulz (4 commits, including all three Logger v2 hardware commits); its README:3 says the code is "heavily based off the Alog library by Northern Widget"; `LICENSE` is GPL v3 (no separate hardware license in the repo).

### C3. Okapi Feather footprint is Adafruit's, not NW-drawn (question 2: claim refuted)
- Claim: `okapi.md:120` "No Adafruit library and no Adafruit attribution text anywhere"; `okapi.md:123` "the footprint is NW-drawn to Adafruit's published Feather specification".
- Check: fetched `adafruit/Adafruit-Eagle-Library` `adafruit.lbr` (3,508,703 bytes, raw.githubusercontent.com, master) to the session scratchpad and compared entries with `Project-Okapi/Hardware/Okapi.sch` after stripping `urn`/`library_version`/`locally_modified` attributes.
- Result: package FEATHERWING (42 lines), package FEATHERWING_DIM (46 lines) and symbol MICROSHIELD (52 lines) are **byte-identical** (same md5) in the two files. adafruit.lbr's deviceset FEATHERWING (line 55091) has `prefix="MS"` and gate symbol MICROSHIELD, as Okapi's does; Okapi's deviceset is longer (182 vs 77 lines) because bschulz added devices. The placed footprint FEATHERWING_MIN (`Okapi.brd:4187`, MS1) is not in adafruit.lbr, but 28 of its 28 `<pad>` lines are identical to lines in Adafruit's FEATHERWING package (which has 30): a trimmed copy.
- Verdict: **VERIFIED** – Okapi's Feather symbol and footprint descend from the Adafruit Eagle library, and that lineage continues into `NW-Cold-Silicon/nw-cold-silicon.pretty/FEATHERWING{,_DIM,_MIN}.kicad_mod` (`NW-Cold-Silicon/PROVENANCE.md` has no "feather" line: grep 0 hits). License consequence per `upstream.md:55`: adafruit.lbr states no license at all.

### C4. Okapi MICROSD text is Adafruit's, not SparkFun's (question 2: attribution corrected)
- Claim: `okapi.md:117` MICROSD description "SparkFun-Connectors wording; possible".
- Check: grep for "4UCON #19656". adafruit.lbr line 48844 is in `<deviceset name="MICROSD">` (line 48841). In `TLog/ALog-TLog/Logger_v2.sch:1181-1184` the same text sits inside `<library name="adafruit">` (opens line 779). Okapi.sch:10863 carries it inside bschulz.
- Verdict: **VERIFIED, Adafruit origin** (symbol/deviceset text). The placed footprint is still NW's own MICROSD_CD (Molex), per `okapi.md:117`.

### C5. ATMEGA1284* "Source: ... doc2593.pdf" (question 2: upgraded)
- Claims: `margay.md:59` (likely), `okapi.md:119` (possible): Eagle stock atmel.lbr.
- Check: `/usr/local/bin/eagle-9.6.2/cache/lbr/atmel.lbr` has the exact line "Source: http://www.atmel.com/dyn/resources/prod_documents/doc2593.pdf" 5 times (e.g. lines 3240, 6935, 12549), on ATMEGA644 entries (line ~12540 `deviceset name="ATMEGA644-*PU"`).
- Verdict: **VERIFIED text match** to Eagle's stock atmel library (ATmega644 entry, which matches the ATMEGA644E symbol name the reports cite). Eagle stock libraries carry no license text.

### C6. bschulz FRAME_A_L CC BY-SA text (question 2: Eagle-stock source refuted)
- Claim: `sensors-a.md` "Not resolved" bullet: origin of "This work is licensed under the Creative Commons Attribution-ShareAlike 4.0" in bschulz FRAME_A_L is SparkFun or Eagle stock, POSSIBLE.
- Check: Eagle 9.6.2 `frames.lbr` has FRAME_A_L (package line 291, symbol 890, deviceset 1134) and 0 occurrences of "Creative Commons". SparkFun's frame wording is different: "Released under the Creative Commons Attribution Share-Alike 4.0 License" (`TP-DownHole/Hardware/TP-DownHole.sch:232`).
- Verdict: frame geometry and name are Eagle stock; the CC BY-SA sentence is neither Eagle's nor SparkFun's wording, so it is most likely NW-added (`Project-Haar/Hardware/Haar_HardMount.sch:1071`). Not a SparkFun link.

### C7. Margay MOSFET-NCH (question 2: upgraded)
- Claim: `margay.md:45` POSSIBLE (no SparkFun description text).
- Check: within `<deviceset name="MOSFET-NCH">` of `Project-Margay/Hardware/Margay.sch`, PROD_ID values TRANS-08089, TRANS-09984, TRANS-10060, TRANS-11151, TRANS-12437, TRANS-12988: the same six SparkFun production IDs `sensors-a.md` lists for bschulz MOSFET-NCH in Walrus.
- Verdict: **VERIFIED** SparkFun-DiscreteSemi origin (by PROD_ID).

### C8. Margay -> TLog board definition (question 2: supporting evidence)
- Claim: `margay.md:66` "TLog v1" is not present in current boards.txt.
- Check: `git log --all -S'TLog'` in Arduino_Boards: 7b7d670 2018-01-29 "Added TLog pin definitions", 0108590 2019-01-01 "Include TLog in JSON", then 6de76d0/a4406a9 2019-08-06 ("rm redundant 644p", "update for boards.txt"). The TLog definition existed and was removed in 2019.
- Verdict: supports `margay.md:21` (Margay ran on the TLog definition); together with C2 the Margay -> TLog link stays LIKELY-strong (no file says "based on TLog"), but TLog's own parent is now verified.

### C9. Okapi Particle B-SoM connector is Particle's library part (question 2: upgraded from possible)
- Claim: `okapi.md:127` "whether the symbol was taken from Particle's published Eagle files is not stated (possible)"; `okapi.md:141-142` "Relation to Particle reference designs: not found".
- Check: fetched `particle-iot/hardware-libraries` `Eagle/Particle-Devices.lbr` (repo CC-BY-SA-4.0 per GitHub, created 2013-08-13) to the scratchpad. Compared Okapi.sch symbol B_SERIES_M.2EKEY-1 with Particle's B_SERIES_M.2EKEY (pin lines with x/y stripped), and package PARTICLE_M.2EKEY_NOPROG with Particle's PARTICLE_M.2EKEY (`<smd>`/`<pad>` lines).
- Result: 69 of 69 symbol pins identical; **70 of Okapi's 70 pads byte-identical** to Particle's (Particle's package has 74; NOPROG drops 4).
- Particle's licensing text (`Particle-Devices.lbr:193`): "Designed by Particle. Distributed under a Creative Commons Attribution, Share-Alike license. Development kits based on this library should be distributed under a similar license. Commercial products using this library as a reference design need not comply with this license". README:78 "All files distributed under a Creative Commons Attribution, Share-Alike license."
- Verdict: **VERIFIED** – J9 symbol and footprint descend from Particle's CC BY-SA Eagle library. This is a fourth vendor (after Arduino, SparkFun, Adafruit) in the binding set. The same Particle-Devices library appears in RTGS-Lab/Project-Kestrel (C10).

### C10. Downstream derivatives outside the NW organizations (not in any report)
- `RTGS-Lab` org (GitHub). `Project-Kestrel` (CC-BY-SA-4.0, created 2021-09-29, "Hardware files for the Kestrel data logger"): `Hardware/MainLogger.sch` uses libraries bschulz, bschulz_passives, GEMS_Plugs, Particle-Devices, SparkFun-Connectors, SparkFun-PowerSymbols, supply1, and `DESIGNER="Bobby Schulz"`; its README keeps Haar README template lines (README:43 "Haar v0.0 - Bottom", README:90 "Haar Connector Pinout").
- `RTGS-Lab/DFM_-_Haar` (CC-BY-SA-4.0, 2022-12-15): README:3 "Model(s): Haar v2.0", files `Haar_Primal_HardMount_2v0*` – a Haar derivative. `RTGS-Lab/Driver_-_Haar` (GPL-3.0, 2022-06-24) is its driver. Talon-I2C/SDI12/Auxiliary, Hedorah, Gonk etc. are further boards in the same family, not traced.
- Single next check: compare `RTGS-Lab/DFM_-_Haar` board (zip) and `Project-Kestrel/Hardware/MainLogger.sch` part/net sets against `Project-Haar/Hardware/Haar_HardMount.sch` and `Project-Okapi/Hardware/Okapi.sch` the way C2 did. Not run here.

### C11. Quick traces of the uncovered designs from C1 (local clones, read-only)
- **RockBLOCK-feather** (Skunkworks, public): d4651b5 2021-07-05 "From Resnik repo (bschulz1701)". `RockBlock_Breakout.sch` md5 00dfade4 equals `Project-Okapi` `37541ab^:Hardware/RockBlock_Breakout.sch`. **VERIFIED** byte-identical move out of Okapi. Libraries bschulz, bschulz_passives, supply1 only.
- **Project-Longbow / LongbowWidget** (Skunkworks): 83725cf 2020-04-30 "From deprecated TLog header", 6efe8b0 "Deprecated connector for TLog". Child of TLog (verified by commit message; parts not compared). Libraries awickert, bschulz, bschulz_passives, SparkFun-Jumpers, SparkFun-PowerSymbols, supply1.
- **ALog_telemeter / logger_2G_GSM** (Skunkworks, CC-BY-SA-4.0): f65269d 2016-11-23 Andy Wickert "Current version of next-generation ALog"; MCU ATSAMD21J. Against ALog-BottleLogger tag v2.0.0: 33 of 42 library/deviceset pairs and 39 of 60 net names shared. **LIKELY** a BottleLogger-v2-line derivative. Against network-logger-umn Logger v2 (also SAMD21): only 2 pairs, 16 nets shared, so it is not that board's parent.
- **ALog-BottleLogger2 / BL1284P_DataLogger_V2.00** (NorthernWidget, NOASSERTION): 8480a42 2015-11-10 Gerhard Oberforcher "First Upload of BL1284P V2.00 CAD Files". The files are Protel binaries ("Protel for Windows - Schematic Capture Binary File Version 1.2 - 2.0W"), so no Eagle library can be compared. Netlist `Logger100.NET` names ATMEGA1284P-AUR, CD4050BPWR, FT232RL, LP2985-33DBVR, SD_CS, VUSB: the BottleLogger v1.0.0 functional core (4050 shifter, FT232RL, LP2985) moved to a 1284P, and the project name "Logger100" matches BottleLogger's `logger100.sch`. **LIKELY** a functional redraw of BottleLogger v1.0.0 in another EDA tool. A redraw shares no design files with its source, so share-alike would not reach it.
- **Project-ThermalStake / ThermistorControl** (Skunkworks; c078554 2019-02-06 "Control board by Ryan Doxsey"): libraries Smartprj (ATMEGAXX8, package MLF32-M1-A), MyPOW (+5V, COM), SparkFun, SparkFun-Passives, plus a Murata CSTCE16M0V53A resonator. Smartprj + MyPOW are Arduino's reference-design library names (`alog.md:50-53`). **LIKELY** Arduino reference-design content; no specific Arduino board identified (a GitHub code search for ATMEGAXX8 in .sch found no Arduino-owned file). No overlap with BottleLogger parts (0 shared pairs at v1.4, v2.0.0 and v2.2.0).
- **Project-Tally, Project-Calypso, Project-Astron, Project-Raven, ICSP-half-size-adapter, MaxBotix-Helper**: libraries are only bschulz/bschulz_passives/supply1 plus SparkFun-Jumpers/-PowerSymbols/-Aesthetics/-Connectors. No commit message names a parent (grep for based/from/fork/deriv/sparkfun/adafruit/arduino/copy/feather). Calypso holds "Senior Design 2018 archive" files (a second UMN senior-design link). Vendor link: SparkFun library parts (CC BY-SA 4.0) via the named libraries and via bschulz (as in every other bschulz design).
- **AtlasShield, Break44** (NorthernWidget org): not cloned locally and not traced. Break44 is a fork of `bschulz1701/Break44` and contains `MS5803/MS5803_Breakout`, `PrimalLog/PrimalLogger_Feather` and `FeatherTestPointBreakout`: likely candidates for SparkFun MS5803 and Adafruit Feather links. Next check: `gh api` the schematics and repeat the C3 comparison.

## Answers

### (1) Designs with no verified parent link, with the single most useful check
| Design | Report | Status after this pass | Next single check |
|---|---|---|---|
| TLog | `tlog-tp.md:208` | **Now VERIFIED**: network-logger-umn Logger v2 (C2) | – |
| Margay | `margay.md:21` | LIKELY (TLog); vendor parts verified | Diff `ed9bf1c:Blackfoot.sch` against `TLog.sch` at b15ec1a for part coordinates (copied sheet vs redraw) |
| Okapi (board, not parts) | `okapi.md:132` | LIKELY (Margay v2); Adafruit Feather and Particle parts now VERIFIED (C3, C9) | Same coordinate diff of `45eee75:Resnik.sch` against Margay `a424de6` |
| Haar, Apis | `sensors-a.md` | NW sibling POSSIBLE; SparkFun parts verified | Coordinate/segment diff of ATTINY1634+TXS0102 block against Walrus `d284535` |
| Inclinometer-breakout-SCA100T | `small.md:75` | none: only SparkFun-Sensors SCA1000 part | `gh search repos SCA100T` found no SparkFun board (only hutasunet/SCA100T, a library, and awoz92). Stays none |
| Instrumentation-Amp, LiIon-18650-Parallel, Lux | `small.md` | none external; internal predecessors verified | Not checked: a search of sparkfun/adafruit repos for AD8227/AD623/MAX44009 boards |
| Liasis, Libelle, Ophiura | `sensors-b.md` | NW parent (Dyson) verified; no external parent | `Project-Monarch__Archive` (C1) holds the Dyson/Monarch files and can confirm |
| ALog-BottleLogger (specific Arduino board) | `alog.md:49-56` | Arduino lineage LIKELY | Compare SmartPrj/MyPOW part values and net names in `logger100.sch` (tag 1.0.0) with an Arduino Duemilanove Eagle file. No Arduino-owned copy was found by gh code search in this pass |

### (2) Weak claims checked
- Upgraded to VERIFIED: Okapi Feather symbol and footprint from Adafruit (C3); Okapi MICROSD text from Adafruit (C4, attribution corrected from SparkFun); ATMEGA1284* text from Eagle stock atmel.lbr (C5); Margay MOSFET-NCH from SparkFun (C7); Okapi B-SoM connector from Particle (C9); TLog parent (C2).
- Refuted: "no Adafruit" in Okapi (`okapi.md:120`) and "NW-drawn" Feather footprint (`okapi.md:123`); Eagle-stock or SparkFun origin of bschulz frame CC text (C6).
- Supported, not upgraded: Margay on the TLog board definition (C8).
- Left as is: Walrus–Haar solder-cup package (library reuse, `sensors-a.md` parent 5); Lux BSS138 shifter (generic topology); LogMega FoleyMechatronics branch (`alog.md:101`). `NorthernWidget/DataCollector-Foley-Mechatronics` exists but holds only firmware (`ATMEGA_GSM.ino`, `Cheker/`), background PDFs and field photos: no board files and no README, so it does not settle the branch.

### (3) Designs missing from the reports
See C1 (table) and C11. Thirteen public repositories with board files were not covered at all: ten in NorthernWidget-Skunkworks, which `upstream.md:86` did not list, and AtlasShield, MaxBotix-Helper and Break44 in the NorthernWidget org. Two more (network-logger-umn, ALog-BottleLogger2) were named but not traced. Further downstream derivatives sit in RTGS-Lab (C10).

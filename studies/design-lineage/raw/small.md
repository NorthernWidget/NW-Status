STATUS: COMPLETE

# Design lineage: small boards

Repositories: Inclinometer-breakout-SCA100T, Instrumentation-Amp, LiIon-18650-Parallel, MAX44009_local

## 1. Inclinometer-breakout-SCA100T (SCA100T inclinometer breakout)

- GitHub: NorthernWidget/Inclinometer-breakout-SCA100T; not a fork (`fork:false`, `parent:null`); created 2016-04-27T00:46:34Z; GitHub license CC-BY-SA-4.0 (gh api).
- License in repo: `Inclinometer-breakout-SCA100T/LICENSE.txt` line 1 "Attribution-ShareAlike 4.0 International" (commit 451219e, 2018-06-16, Andy Wickert, "Create LICENSE.txt"; earlier 415c1a7, 2016-04-26, "CC-BY-SA", with a LICENSE.html later deleted in a5d2101). `.zenodo.json`: `"license": "cc-by-sa-4.0"`, creators Wickert and Sandell.
- First commit: bd6221e 2016-04-26 Andy Wickert "Initial commit"; cef3686 2016-04-26 "Schematic has all components"; 26ad8b1 2017-04-11 Chad Sandell "updated files". No commit message names a parent board.
- Eagle 6.6.0 files. Libraries in `inclinometer-breakout-SCA100T.sch`: SparkFun-Sensors (line 143), SparkFun-Passives (222), SparkFun-Aesthetics (949), con-phoenix-254 (5014, Eagle stock). The `.brd` adds library `SparkFun` (line 317) for four STAND-OFF holes JP1-JP4.
- Parts taken from SparkFun libraries: U$1 = SparkFun-Sensors deviceset `SCA1000` ("Dual 4g accelerometer, SPI and analog out", sch line 193-194), valued SCA100T (sch line 5117) - i.e. the main sensor footprint/symbol is SparkFun's; C1-C3, R1-R2 from SparkFun-Passives 0603; GND/VDD symbols and the OSHW logo (LOGO1, SparkFun-Aesthetics OSHW-LOGO) from SparkFun-Aesthetics.
- The embedded SparkFun library text states its license: sch line 148 (and 227, 954) "Licensing: Creative Commons ShareAlike 4.0 International - https://creativecommons.org/licenses/by-sa/4.0/".
- Design rules: `<designrules name="default">` (brd line 340); no SparkFun DRU/CAM. No README.
- Parent links:
  - SparkFun Eagle libraries (SparkFun-Sensors, -Passives, -Aesthetics, SparkFun): **uses library parts, CC-BY-SA 4.0** - verified (library names and embedded license text above).
  - No parent board (SparkFun/Adafruit/Arduino/NW) found: no form factor, no "based on" text.
- Board text: only >NAME/>VALUE (no silkscreen credits).

## 2. Instrumentation-Amp (AD623 instrumentation amplifier; plus CMP3_Amp on GitHub only)

- GitHub: NorthernWidget/Instrumentation-Amp; `fork:false`, `parent:null`; created 2016-07-19T20:34:41Z; license CC-BY-SA-4.0; description "Instrumentation amplifier to boost low-voltage signals; developed for scientific sensors" (gh api).
- **Local clone is stale.** Local HEAD is c55133b (2017-07-18) and holds no LICENSE; GitHub master is f093082 (2018-11-30), 20 commits further, with LICENSE (commit 9f91b64, 2018-06-17, Andy Wickert, "CC-BY-SA"; remote `LICENSE` line 1 "Attribution-ShareAlike 4.0 International") and a second design `CMP3_Amp.sch/.brd` (ed44c81, 2018-11-20, Bobby Schulz, "Initial layout of CMP3 Amp"). Remote files were read via `gh api` into the scratchpad only; nothing was fetched into the repository.
- README (`Instrumentation-Amp/README.md`, same locally and on GitHub): "Breakout board for the AD623 instrumentation amplifier"; line "We use connect all of the jumpers to use a pyranometer." No credit to any parent.
- History of the design:
  - v1: 6796cb3 2016-07-19 Chad Sandell "Version one of instrumentation amplifier" (`Instrumentation amp.sch`): AD8227 from `Analog_devices_element14_Batch_1`, MAX4734 from `csandell`, connectors M02/M06 from `SparkFun-Connectors`, SJ1 SOLDERJUMPER_2WAY from `SparkFun-Retired`. 5405132 2016-07-20 "Improved tracing and changes for OSH Park compliance"; at 232d2ab the brd uses `<designrules name="oshpark-2layer">` (v1 at 6796cb3 used "default").
  - v2: 4e4aa69 2017-06-26 Andy Wickert "AD623R Redesign" replaces v1 (v1 files deleted in the same commit; a9fc386 "Deprecated" removes the .pro). AD623 from Eagle stock `analog-devices`; SparkFun-Capacitors, -Connectors (CONN_04 LOGGER, CONN_02 SENSOR), -Jumpers (JUMPER-SMT_2_NC_PASTE), -PowerSymbols.
  - "Amp 2.0": c55133b 2017-07-18 Bobby Schulz "Initial layout of Amp 2.0" (local working `InstrumentationAmp.sch`, Eagle 8.1.1): adds `Custom` (MAX4638, TCA9534A, FDN358P, MIC842, TPS306X, WE-MAIA inductor), SparkFun-LED, SparkFun-DiscreteSemi (MOSFET-NCH), SparkFun-Connectors `I2C_STANDARD` (J1). GitHub version (Eagle 8.3.0) adds library `bschulz`; brd design rules "PCB-POOL Standard".
  - CMP3_Amp (GitHub only, Eagle 9.2.1): libraries `bschulz`, `bschulz_passives`, `supply1` only; LTC2054 x2, MCP342*, TXS0102, TPS797*; brd DRU `oshpark-2layer`; silkscreen "To Logger", "To Sensor", "(CMP3)".
- SparkFun license text embedded in local `Instrumentation-Amp/InstrumentationAmp.sch`: lines 164, 2201, 2305, 2386, 8976, 9229 "Licensing: Creative Commons ShareAlike 4.0 International".
- `bschulz` library carries copied SparkFun content: in the GitHub CMP3_Amp.sch (scratchpad copy) line 242 package TO220V "N-Channel MOSFET SparkFun SKU: COM-10213"; deviceset MOSFET-NCH (line 896) lists "SparkFun Products: SparkFun OpenScale ... Digital Sandbox ... Monster Moto Shield" (lines 899-902). This is SparkFun-DiscreteSemi text inside Bobby Schulz's personal library.
- Parent links:
  - SparkFun Eagle libraries (Connectors, Retired, Capacitors, Jumpers, PowerSymbols, LED, DiscreteSemi): uses library parts, CC-BY-SA 4.0 - verified.
  - bschulz personal Eagle library (NW in-house): uses; it contains SparkFun-derived parts - verified (CMP3_Amp.sch lines 242, 896-902 on GitHub).
  - Earlier NW design: v2 (4e4aa69) supersedes Chad Sandell's v1 AD8227 board in the same repository (internal predecessor) - verified (commit 4e4aa69 deletes v1 files).
  - No parent board from SparkFun/Adafruit/Arduino named; no form factor. OSH Park DRU only (fab rules, not a design parent).
- Board text (local brd): "Controller", "VCC", "VS+", "VS-", "Vref", "SCL", "SDA" etc.; no credits or logo.

## 3. LiIon-18650-Parallel (1S2P 18650 battery holder board)

- GitHub: NorthernWidget/LiIon-18650-Parallel; `fork:false`, `parent:null`; created 2020-02-04T22:32:24Z; license CC-BY-SA-4.0 (gh api).
- License in repo: `LiIon-18650-Parallel/LICENSE` line 1 "Attribution-ShareAlike 4.0 International" (commit 5fd468c, 2020-02-04, Andy Wickert, "CC-BY-SA"). README: "Lithium-ion 18650 battery power supply: PCB" only.
- History: 784fcb1 2020-02-04 Andy Wickert "Initial commit"; 6aa1838 "First draft"; 6db777a 2020-02-05 "Bobby Schulz design review: address"; a601d8d, 086cb98 2020-02-05 Bobby Schulz. No message names a parent.
- Eagle 9.5.2. Libraries in `batt18650parallel.sch`: "Keystone - 1042" (lines 164-240; description "Upverter Parts Library / Created by Upverter.com", line 165-167) for BT1/BT2 holders; SparkFun-PowerSymbols (241-302, urn:adsk.eagle:library:530; license line 251 "Creative Commons ShareAlike 4.0 International") for VCC/GND symbols only; "100SP1T2B4M6QE" E-Switch toggle (303-392; "Created by SamacSys", line 305); `bschulz` (393-1430) for J1-J3 connectors and H1-H4 4-40 holes.
- The `bschulz` connector devices carry SparkFun-Connectors text: lines 431, 455, 557, 618, 673, 735, 795, 826, 853, 902, 1024 "Datasheet referenced for footprint" linking sparkfun.com/datasheets/Prototyping/...; lines 730, 820, 846 "polarity for connections that match SparkFun LiPo battery terminations" (JST-2 footprint, J2 = `JST-2-SMD`).
- Board: design rules `oshpark-2layer`; silkscreen "Batteries in Parallel (1S2P)", "ON", "OFF", "+", "-".
- Parent links:
  - SparkFun-PowerSymbols (schematic symbols only): uses, CC-BY-SA 4.0 - verified.
  - bschulz Eagle library (NW in-house) whose connector footprints derive from SparkFun-Connectors: uses - verified that bschulz is used; SparkFun origin of those footprints likely (SparkFun-specific description text copied into bschulz, lines 730, 735).
  - Upverter (Keystone 1042) and SamacSys (E-Switch) vendor parts: uses library parts; their license terms are not stated in the file - not a share-alike link.
  - No parent board found (no Adafruit/SparkFun/Arduino battery board named).

## 4. MAX44009_local (MAX44009 "Lux" ambient-light breakout; home on GitHub is NorthernWidget/Lux)

- Repository identity: the local folder's `origin` is NorthernWidget/MAX44009 (the Arduino *library*, GPL-3.0, created 2017-11-13), but its local `master` holds only the two hardware commits 921faf5 (2017-06-28 Chad Sandell "initial design") and d16c6ba (2017-06-29 Bobby Schulz "Added 5v compatable Lux breakout"); `git status` reports "ahead 2, behind 4" against the library's four commits (4b36ca4 ... 254234f, 2017-11-13, bschulz1701/Bobby Schulz). The same two hardware hashes are the first commits of **NorthernWidget/Lux** on GitHub (`fork:false`, created 2017-06-28T20:58:22Z, license CC-BY-SA-4.0, description "Lux sensor"), which adds 1132d28 (2017-09-27 Chad Sandell "Add label for pin 1") and 2d72eb9 (2018-06-17 Andy Wickert "CC-BY-SA", adds LICENSE). So the hardware design is NorthernWidget/Lux; the local folder has no LICENSE.
- Two designs:
  - `Lux.sch/.brd` (Eagle 7.7.0, Chad Sandell): MAX44009 from library `Maxim` (sch line 3046; no author/description), J1 = SparkFun-Connectors M05 (brd 1X05_NO_SILK), passives from Eagle stock `rcl`/`resistor`, frame `frames` LETTER_P; four STAND-OFF holes from library `SparkFun` (brd); board design rules `<designrules name="SparkFun *">` (`Lux.brd` line 1357) - SparkFun's DRU file used for this board. Embedded SparkFun license: `Lux.sch` line 2531 "Creative Commons ShareAlike 4.0 International".
  - `Lux_5V Compatable.sch/.brd` (Eagle 8.1.1, Bobby Schulz): MAX44009 (UTDFN6) and TPS715XX LDO from `Custom`; Q1/Q2 = SparkFun-DiscreteSemi MOSFET-NCH device `-BSS138`; R3-R7 10k; nets SDA/SDA_IN, SCL/SCL_IN, 5V, VCC; JP2 SparkFun-Jumpers; J1 SparkFun-Connectors CONN_07 (1X07); SparkFun-PowerSymbols. SparkFun license text at sch lines 278, 6046, 6146, 6459. DRU "PCB-POOL Standard". Silkscreen "MAX44009", "3.3V", "5V", "A0", "INT", "SCL", "SDA".
- Parent links:
  - SparkFun Eagle libraries (Connectors, DiscreteSemi, Jumpers, PowerSymbols, SparkFun): uses library parts, CC-BY-SA 4.0 - verified.
  - SparkFun design rules ("SparkFun *" DRU in `Lux.brd`): uses SparkFun fab rules - verified (fab rules, not circuit lineage).
  - BSS138 + 10k pull-up bidirectional I2C level shifter in the 5 V version: same topology as the generic Philips/NXP MOSFET shifter that SparkFun's logic-level-converter breakout also uses - possible only; nothing in the files names a source.
  - Bobby's 5 V version descends from Chad's `Lux.sch` in the same repository (d16c6ba "Added 5v compatable Lux breakout") - verified as an internal predecessor by commit message; the 5 V version was redrawn with different libraries rather than edited from Lux.sch (no shared library besides rcl and SparkFun-Connectors).
  - No Adafruit/SparkFun/Arduino parent board named.

## Sources checked (all four repositories)

- Files: every tracked file listed by `git ls-files` (Inclinometer: .gitignore, .zenodo.json, LICENSE.txt, .brd, .sch, datasheet PDF; Instrumentation-Amp: .gitignore, AD623.pdf, .brd, .sch, BoM .xls (not opened), README.md; LiIon-18650-Parallel: .gitignore, LICENSE, README.md, .brd, .sch; MAX44009_local: Lux and Lux_5V Compatable .sch/.brd, .DS_Store). Eagle backup files (.b#N/.s#N) not examined: untracked.
- Eagle XML: `<library name>`, `<part>`/`<element>` library attributions, library `<description>` and "Licensing" lines, `<designrules name>`, board `<text>` labels.
- No CITATION.cff in any of the four. No KiCad files. No Arduino/Adafruit/Feather/microbuilder library names found in any file (grep for "adafruit", "arduino" returned nothing in these schematics).
- git: full `git log` of each local repository; `git show` of Instrumentation-Amp commits 6796cb3, 232d2ab, 4e4aa69 for the v1 libraries.
- GitHub (gh api): repos NorthernWidget/Inclinometer-breakout-SCA100T, Instrumentation-Amp, LiIon-18650-Parallel, MAX44009, Lux (metadata, contents, commits); Instrumentation-Amp remote LICENSE, README, InstrumentationAmp.sch/.brd and CMP3_Amp.sch/.brd copied to the session scratchpad. Dead ends: NorthernWidget/MAX44009_local and NorthernWidget/MAX44009-Breakout do not exist (404). Org repo list searched for lux/max44/light/amp/incl/18650/batt/liion: hits Inclinometer-breakout-SCA100T, Instrumentation-Amp, Lux, MAX44009, LiIon-18650-Parallel only.
- Not done: no web lookup of SparkFun's own SCA100T or level-converter products to compare footprints or schematics.

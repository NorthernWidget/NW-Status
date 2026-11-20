STATUS: COMPLETE

# Design lineage: Project-Liasis, Project-Libelle, Project-Ophiura

Paths are relative to the workspace `/home/awickert/Dropbox/NorthernWidget/github`. All work read-only.

## Project-Liasis (longwave pyrgeometer, board `Hardware/LongWaveModule`)

- License in repo: hardware CC BY-SA 4.0 (`Project-Liasis/LICENSE` line 1; README "License"); code GPL-3.0 (`LICENSE_for_code`). `CITATION.cff` `license: CC-BY-SA-4.0`; `.zenodo.json` `cc-by-sa-4.0`. GitHub API: `NorthernWidget/Project-Liasis`, fork=false, parent=null, created 2026-05-12T22:57:39Z, license CC-BY-SA-4.0.
- License history: first commit `ba1b59c` (2018-06-05, Bobby Schulz) added an MIT `LICENSE` (21 lines; "MIT License / Copyright (c) 2018"); `d7015dc` (2018-06-28, "CC-BY-SA") replaced it with CC BY-SA 4.0 (+427 lines).
- First commit: `ba1b59c` 2018-06-05 Bobby Schulz "Initial commit"; design files in `eda7d22` 2018-06-05 15:04:17 "Rebuild repo". 36 commits.
- Parent 1, NW (verified): Project-Dyson / Project-Monarch combined pyranometer repo. `ba1b59c:README.md` reads "# Project-Dyson / Designs for a small scale and low cost pyronometer operating in both the short wave and long wave spectral regions". `5cecf13` (2026-05-13) diff removes "# Project-Monarch" and DOI 10.5281/zenodo.5643930 and adds "# Project-Liasis ... longwave". Renames `60e7f42`/`1b14e96` (2021-11) "Dyson-->Monarch". The root commit `ba1b59c` is byte-identical (same hash) in Project-Libelle: Liasis and Libelle are siblings from one Dyson root.
- Parent 2, SparkFun (verified, library content): `Hardware/LongWaveModule.sch` line 6219 `<library name="SparkFun-Jumpers" urn="urn:adsk.eagle:library:528">`, licensing text line 6229 "Creative Commons ShareAlike 4.0 International"; part JP1 line 6403 (`JUMPER-SMT_3_1-NC_PASTE`); placed in `LongWaveModule.brd` line 926.
- Parent 3, SparkFun via Bobby's `bschulz` library (likely): `bschulz` deviceset `MOSFET-NCH` (sch line 1142) carries SparkFun's description verbatim, "SparkFun Products: SparkFun OpenScale ... Monster Moto Shield ... MOSFET Power Controller" (lines 1145-1149); package `TO220V` line 329 "N-Channel MOSFET SparkFun SKU: COM-10213"; connector packages `1X04`/`1X04_SCREW`/`1X04_NOSILK` (lines 396-472) use SparkFun-Connectors' template ("Plated Through Hole - 4 Pin / Specifications: Pin count / Pin pitch / Example device(s): CONN_04"); symbol `CONN_04` line 758 "4 Pin Connection".
- Other: `supply1` (Autodesk stock, line 1366). Design rules `oshpark-2layer` (`.brd`): a fab rule set, not a design parent. Frame symbol `DOCFIELD` in `bschulz` carries the CC BY-SA 4.0 notice (sch lines 754-755).
- No Arduino, Adafruit, Feather, or shield form factor found in any file. No firmware in this repo.

## Project-Libelle (spectral shortwave pyranometer; `Hardware/Libelle.sch/.brd`, `Hardware/Libelle_SmallBoard.sch/.brd`)

- License in repo: hardware CC BY-SA 4.0 (`Project-Libelle/LICENSE`), firmware GPL-3.0 (`LICENSE_for_code`); `CITATION.cff` CC-BY-SA-4.0; `.zenodo.json` cc-by-sa-4.0. GitHub API: `NorthernWidget/Project-Libelle`, fork=false, parent=null, created 2018-06-05T19:59:52Z, CC-BY-SA-4.0. Stale MIT text remains at `Analysis/SpectrumResponsePlots/Captures/LICENSE` ("MIT License / Copyright (c) 2018").
- License history: MIT in `ba1b59c` (2018-06-05); CC BY-SA in `a70f1d1` (2018-06-28, "CC-BY-SA").
- First commit `ba1b59c` 2018-06-05 Bobby Schulz; design files in `66baecf` "Rebuild repo" (as `Hardware/ShortWaveModule*.sch/.brd`). 92 commits.
- Parent 1, NW (verified): same Project-Dyson root as Liasis (`ba1b59c:README.md` "# Project-Dyson"). Renames: `6a125b3`/`dd60aac` 2021-11 "Dyson-->Monarch"; `9021d1e`/`e0254ef`/`5d4ddef` 2026-05-13 "Monarch→Libelle", "ShortWaveModule→Libelle". README: "Legacy deployed units carry board types 0x2300/0x2301 (formerly Dyson SW, Monarch SW)".
- Parent 2, SparkFun (verified, library content): `Libelle_SmallBoard.sch` line 9023 `SparkFun-Jumpers` (urn 528), CC BY-SA 4.0 text line 9033; JP1 line 9290, JP2 line 9305 (`JUMPER-SMT_2_NO`); placed in `Libelle_SmallBoard.brd` lines 1184, 1225. The larger `Libelle.sch` (Eagle 8.5.1) uses no SparkFun library (libraries: bschulz, bschulz_passives, supply1, frames).
- Parent 3, SparkFun via `bschulz` (likely): `Libelle.sch` line 303 `TO220V` "SparkFun SKU: COM-10213"; lines 1097-1101 the SparkFun MOSFET-NCH description; same in `Libelle_SmallBoard.sch` lines 308, 2894-2898, 9144-9145 ("SparkFun EL Sequencer", inside SparkFun-Jumpers).
- Firmware dependencies (not design parents, not vendored): `SlowSoftI2CMaster.h`, `WireS.h` (`Firmware/Libelle_Driver_ShortWave/Libelle_Driver_ShortWave.ino` lines 3-4); test sketches use NW `Margay.h`, `MCP3421.h`, `DS3231_Logger.h` (`Firmware/Libelle_KippZonen_Test`, `Firmware/PyroLoggingEval`). No Adafruit or SparkFun code text found in firmware (grep for adafruit/sparkfun/copyright/derived: none).
- Possible third-party analysis input: `Analysis/SpectrumResponsePlots/Captures/Solar_spectrum_en.svg.png` (file name matches a Wikimedia file; no attribution in repo; not verified).
- No Arduino/Adafruit form factor found. MCU is a bare ATtiny841 (README "Hardware").

## Project-Ophiura (bus breakouts: BusBreakout_I2C, BusBreakout_I2C_Mini, Switched_I2C, RS485_Breakout)

- License in repo: CC BY-SA 4.0 (`Project-Ophiura/LICENSE`, README "License"); `.zenodo.json` line 15 `cc-by-sa-4.0`; `CITATION.cff` has NO `license:` field (gap). GitHub API: `NorthernWidget/Project-Ophiura`, fork=false, parent=null, created 2018-03-02T18:57:30Z, CC-BY-SA-4.0.
- License history: MIT in `7c4cdfd` (2018-03-02, Bobby Schulz, "Initial commit"); CC BY-SA in `7b26ecc` (2018-12-18, Andy Wickert, "CC-BY-SA").
- First commit `7c4cdfd` 2018-03-02 Bobby Schulz; I2C board `623cd80` same day; Switched_I2C `a7b7949` 2018-03-06; RS485 `0b2c048` 2018-10-19 "Added RS485 Heptapod"; Mini `88b1c2c` 2020-08-11. 35 commits.
- Former name (verified): `20feb19:README.md` "# Project-Heptapod / Eagle designs for bus breakout boards"; `04ddd5b` 2026-05-13 renames images Heptapod→Ophiura.
- Internal lineage (verified by README): BusBreakout_I2C_Mini is "Electrically identical to the BusBreakout_I2C but in a smaller footprint" (README).
- SparkFun (verified, library content): `RS485_Breakout.sch` line 323 SparkFun-Jumpers, line 333 CC BY-SA 4.0, JP1/JP2 lines 522-523; `Switched_I2C.sch` line 757 SparkFun-Jumpers, line 3321 SparkFun-PowerSymbols (urn 530), parts JP1-JP3 and GND1-GND3 lines 3379-3387. BusBreakout_I2C and _Mini use only `bschulz` (+ `awickert` NW logo on BusBreakout_I2C.brd).
- SparkFun via `bschulz` (likely): `BusBreakout_I2C.sch` lines 163-171 package `1X04` with SparkFun-Connectors template text ("Example device(s): CONN_04"); `Switched_I2C.sch` line 304 TO220V "SparkFun SKU", lines 641-645 MOSFET-NCH SparkFun description, used by Q1 line 3388 (`MOSFET-NCH -DMG3404L`).
- Possible Eagle stock origin: `RS485_Breakout.sch` line 164 package `1X06_SCREW` "<b>PIN HEADER</b>" (Eagle `pinhead` style); `R-EU_` deviceset in `bschulz_passives` (Switched_I2C.sch line 2500; Eagle `rcl` naming). Not openly licensed lineage.
- Documentation credit (verified): README "Ophiura albida ... Photo by Andrea Bonifazi, CC BY-SA 4.0".
- Design rules `BayArea-2layer` / `default` (fab rules only). Gerbers `.GTL/.GBL/.TXT` naming: no SparkFun CAM text found inside.
- No Arduino/Adafruit form factor found. README names Margay as the typical upstream logger (companion, not parent).

## Openness and patents (all three)

- All three LICENSE files are CC BY-SA 4.0, whose Section 2(b)(2) (line 215) reads "Patent and trademark rights are not licensed under this Public License." The GPL-3.0 code licenses (Liasis, Libelle) carry an express patent grant (Section 11).
- `grep -i patent` over the three repositories outside .git: hits only in the license texts. No patent notice, no UMN assignment text, no affiliation in `.zenodo.json` creators (all `None`).
- Earliest public dates: Ophiura repo created 2018-03-02; Libelle and Liasis root 2018-06-05; CC BY-SA from 2018-06-28 (Liasis/Libelle) and 2018-12-18 (Ophiura). These public disclosures predate by years any filing date that would rely on them.

## Sources checked (dead ends included)

- README.md, LICENSE, LICENSE_for_code, CITATION.cff, .zenodo.json in each repo.
- Every .sch and .brd: library names, descriptions, part/element libraries, designrules name, Eagle version.
- git log --reverse; log grep for monarch|dyson|heptapod|based|fork|deriv|sparkfun|adafruit|arduino|feather|from (only rename commits found); git show of root commits and license commits.
- gh api repos/NorthernWidget-Skunkworks/{Project-Liasis,Project-Libelle} (redirects to NorthernWidget org) and repos/NorthernWidget/Project-Ophiura.
- Libelle firmware .ino includes and comments; Libelle Documentation/*.txt; Hardware/DESIGN_NOTES.md (TPS62172 PSpice from TI `slvm434a`, simulation only, removed from tree).
- Gerber/CAM files for SparkFun strings: none. Searched for Adafruit/Arduino/Feather/microbuilder in all EDA files: none.

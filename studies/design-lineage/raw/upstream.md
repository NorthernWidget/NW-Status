STATUS: COMPLETE

# Upstream licenses and terms (primary sources)

Compiled 2026-11-20 by the upstream-facts subagent of the design-lineage study. Quotes are short phrases copied from the cited source. "Verified" means the text was read directly in this session (raw file, `gh api`, or text extracted with `pdftotext`/`curl`); a source read only through a search-engine summary is marked as such.

## 1. Arduino board hardware designs

**Current statement: CC BY-SA 4.0 (verified).** The schematic PDFs that docs.arduino.cc serves today each print, in the title block: "This project's hardware is licensed under the Creative Commons Attribution-ShareAlike 4.0 International License", with a link to `creativecommons.org/licenses/by-sa/4.0/deed.en`. The same PDFs carry the disclaimer "Reference Designs ARE PROVIDED "AS IS"" and the line "All Arduino SA Trademarks cannot be used without owner's formal permission".

| Board | SKU (from its docs.arduino.cc product page) | Schematic URL | License line found |
|---|---|---|---|
| Uno Rev3 | A000066 (PDF also prints "Arduino(TM) UNO Rev3") | https://docs.arduino.cc/resources/schematics/A000066-schematics.pdf | CC BY-SA 4.0 |
| Mega 2560 Rev3 | A000067 (PDF shows ATMEGA2560-15AU) | https://docs.arduino.cc/resources/schematics/A000067-schematics.pdf | CC BY-SA 4.0 |
| Leonardo | A000057 | https://docs.arduino.cc/resources/schematics/A000057-schematics.pdf | CC BY-SA 4.0 |
| Nano | A000005 | https://docs.arduino.cc/resources/schematics/A000005-schematics.pdf | CC BY-SA 4.0 |

SKU mapping: verified by grepping https://docs.arduino.cc/hardware/uno-rev3/, `/leonardo/`, `/nano/` and `/mega-2560/` for the SKU each links. The product page itself (uno-rev3) carries no license text; the license is on the schematic. The CAD zip (`A000066-cad-files.zip`) returned an HTML page to `curl`, so the Eagle files themselves were not inspected.

**Historical statement: CC BY-SA 2.5 (verified for the 2007 post; FAQ version from a mirror).**
- Arduino blog, 22 October 2007, https://blog.arduino.cc/?p=17 : Diecimila and BT Eagle reference designs "now available under a Creative Commons Attribution Share-Alike license"; the license link is to CC BY-SA 2.5 (read via WebFetch).
- Old Arduino FAQ, as shipped in the Debian `arduino` 0018 package, https://sources.debian.org/src/arduino/0018%2Bdfsg-6/reference/FAQ.html : derivatives must "credit Arduino and release their designs under the same license"; modified Eagle files must be released under the same license (read via WebFetch). The search summary said this mirror names version 2.5; the WebFetch reading found no version number on that page, so treat "2.5 in the FAQ" as unverified. The version is verified only from the 2007 blog post.
- Interpretation for the lineage study (a reading, not a source): an NW board derived from an older Arduino Eagle file inherits the license that file carried when it was copied (2.5 for 2007-era designs); a derivative of a current Arduino file inherits 4.0. CC BY-SA 4.0 Section 3(b)(1) lets an adapter use "this version or later" (see section 5), and BY-SA 2.5 and 3.0 carry a similar later-version clause in their share-alike sections (3.0 text read; 2.5 not read this session).

## 2. SparkFun hardware and SparkFun Eagle libraries

**SparkFun-Eagle-Libraries: CC BY-SA 4.0 today, CC BY-SA 3.0 earlier (verified from git history via `gh api`).**
- Repository `sparkfun/SparkFun-Eagle-Libraries`, created 2012-01-17, no GitHub-detected license (no LICENSE file; the license is in `readme.md`).
- Current `readme.md`, line 88: "This library is released under the Creative Commons ShareAlike 4.0 International license", linked to `creativecommons.org/licenses/by-sa/4.0/`. (The wording says "ShareAlike" but the link is BY-SA 4.0.)
- At commit `e8d68b3` (2014-11-17), `readme.md` line 3: "released under the CC v3.0 Share-Alike license", linked to `by-sa/3.0`. It adds that commercial use is welcome and asks for an email with a link to the product.
- By commit `fa55224` (2014-12-30) the text reads 4.0. The switch from 3.0 to 4.0 happened between those two commits.
- Consequence for the lineage study: an NW Eagle file that copied SparkFun library parts before late 2014 drew them under BY-SA 3.0; after that, under 4.0.

**SparkFun-KiCad-Libraries: CC BY 4.0, not share-alike (verified).** `sparkfun/SparkFun-KiCad-Libraries` (created 2017-01-20) `README.md` line 111: "released under the Creative Commons Attribution 4.0 International license". This matters for NW boards converted to KiCad that pull in SparkFun KiCad footprints: those footprints carry attribution only.

**SparkFun board designs: CC BY-SA 4.0, code MIT (verified).** SparkFun product repositories carry a `LICENSE.md` that begins "SparkFun uses two different licenses for our files" and states "SparkFun hardware is released under Creative Commons Share-alike 4.0 International" (linked to by-sa/4.0) and "SparkFun code, firmware, and software is released under the MIT License". Checked in `sparkfun/RedBoard` (`LICENSE.md`, lines 4, 9, 33; file commits 2015-06-22 and 2017-02-20), `sparkfun/OpenLog`, and `sparkfun/SparkFun_BME280_Arduino_Library`. `sparkfun/Arduino_Pro_Mini_328` has no LICENSE file (dead end).

**SparkFun policy post (not read).** https://news.sparkfun.com/3296 (Open COVID Pledge) returned HTTP 403. A search summary says it states SparkFun hardware is under CC BY-SA. Unverified; cite the LICENSE.md files instead.

## 3. Adafruit board designs, the Feather form factor, and the Adafruit Eagle library

**Feather board design files: CC BY-SA 3.0 Unported (verified).** Each of these repositories has a README "License" section reading "Creative Commons Attribution/Share-Alike, all text above must be included in any redistribution" and a `license.txt` whose header is "Creative Commons Legal Code / Attribution-ShareAlike 3.0 Unported". GitHub reports `NOASSERTION` for all of them.

| Repository | Created | Design files in repo |
|---|---|---|
| adafruit/Adafruit-Feather-32u4-Basic-Proto-PCB | 2015-12-07 | `Adafruit Feather 32u4 Basic rev B.sch/.brd` |
| adafruit/Adafruit-Feather-M0-Basic-Proto-PCB | 2015-12-08 | `Adafruit Feather M0 Basic rev C.sch/.brd` |
| adafruit/Adafruit-Feather-M0-Adalogger-PCB | 2016-06-08 | `Adafruit Feather M0 Adalogger.sch/.brd` |
| adafruit/Adafruit-Feather-M0-Express-PCB | 2017-03-31 | `Adafruit Feather M0 Express.sch/.brd` |

Also listed by `gh api` with `NOASSERTION`, not opened: `adafruit/Adafruit-Feather-32u4-Adalogger-PCB` (2016-09-21) and `adafruit/Adafruit-Feather-M0-RFM-LoRa-PCB` (2016-06-08).

**Feather specification / form factor: no license stated (verified).** https://learn.adafruit.com/adafruit-feather/feather-specification (page title "Introducing Adafruit Feather") states no license and links no template design files. It invites compatible boards ("Adafruit encourages you to do so!") but grants no rights in writing. A `gh` search of the adafruit organization for a Feather template or specification repository returned nothing. The Feather form factor is therefore a published dimensional convention without a license; a lineage claim to "Feather" rests on a specific Adafruit `.brd` being copied, not on the form factor.

**Adafruit Eagle library: no license found (verified).** `adafruit/Adafruit-Eagle-Library` (created 2010-01-13) has `README.md`, `README.txt`, and `adafruit.lbr`. Neither README mentions a license, GitHub detects none, and a case-insensitive grep of the 3.5 MB `adafruit.lbr` for "license", "licence", "creative commons", "share alike", and "public domain" found 0 hits.

## 4. MightyCore and mighty-1284p (ATmega1284P)

**No published hardware design files found (verified for the repositories).**
- `MCUdude/MightyCore` (created 2015-11-19; GitHub `NOASSERTION`). Top level: `LICENSE`, `README.md`, `avr/`, and docs; no schematic or board files. `LICENSE` is Arduino's combined notice ("the gnu general public license, which covers the main body", then the LGPL for the core) with the GPL Version 2 text. README "Hardware" section (line 285): "I've designed a development board for this particular core", with no design files linked in that section. README line 317 shows "a simple schematic showing a minimal setup" as an image. The pinout variants are "Standard", "Bobuino" (an "Arduino UNO pinout setting"), and "Sanguino".
- `maniacbug/mighty-1284p` (created 2011-11-23; no license detected): `README.md`, `boards.txt`, `bootloaders/`, `cores/`, `variants/` only. README line 34 credits "'Bobuino'. CrossRoads' board" for Uno-shield compatibility. No hardware files and no license file.
- `JChristensen/mighty-1284p` (created 2014-01-28): no license detected; contents not opened.
- Interpretation: a MightyCore or mighty-1284p lineage link for an NW board is a software/pin-map dependency (GPL/LGPL core code), not a hardware-file parent.

## 5. License terms in plain words

**CC BY-SA 4.0** (legal code read from https://creativecommons.org/licenses/by-sa/4.0/legalcode.en):
- *Adapted work.* Section 1: "Adapted Material means material subject to Copyright and Similar Rights" that is derived from the licensed material and altered "in a manner requiring permission under the Copyright and Similar Rights". In plain words, a derivative counts only where copying or modifying the work needs copyright permission.
- *Rights covered.* "Copyright and Similar Rights means copyright and/or similar rights closely related to copyright".
- *Patents excluded.* Section 2(b)(2): "Patent and trademark rights are not licensed under this Public License."
- *Share-alike.* Section 3(b)(1): "The Adapter's License You apply must be a Creative Commons license with the same License Elements, this version or later, or a BY-SA Compatible License."
- CC FAQ (https://creativecommons.org/faq/): CC licenses "do not license trademark or patent rights". The FAQ also says "The only categories of works for which CC does not recommend its licenses are computer software and hardware", and that BY-SA 4.0 "is one-way compatible with" GPLv3.

**CC BY-SA 3.0 Unported** (https://creativecommons.org/licenses/by-sa/3.0/legalcode.txt, read): the word "patent" does not occur in the text (0 hits). It neither grants nor expressly excludes patents. Section 1(a): "Adaptation" means "a work based upon the Work".

**Does share-alike reach hardware?** OSHWA FAQ (https://oshwa.org/resources/open-source-hardware-faq/, read via `curl`):
- "The design files are likely protected by copyright, even if the hardware itself is not."
- "Copying the design files (potentially including doing so as a step in making the hardware) would be copyright infringement". Building from the files without copying them would not be.
- "Unless you have a patent, someone else can manufacture the hardware without your permission".
- In plain words: BY-SA binds an NW `.sch`/`.brd` that copies or modifies an Arduino, SparkFun, or Adafruit file, and that adapted file must go out under BY-SA (same or later version). It does not by itself bind the physical board, and it neither grants nor blocks patents.

**GPL v3 Section 11** (https://www.gnu.org/licenses/gpl-3.0.txt, lines 471-490, read): "Each contributor grants you a non-exclusive, worldwide, royalty-free patent license under the contributor's essential patent claims". The grant covers "make, use, sell, offer for sale, import". The GNU HTML page returned HTTP 429; the plain-text file was used.

## 6. Northern Widget organization repositories (declared licenses)

Command: `gh api orgs/NorthernWidget/repos --paginate -q '.[]|[.name,.license.spdx_id,.created_at,.fork,(.parent.full_name//"")]|@tsv'` (raw output in `NW-Status/studies/design-lineage/raw/nw_repos.tsv`).
- The list endpoint does not return `.parent`, so the parent column came back empty. Parents of the five forks were filled from `gh api repos/NorthernWidget/<name>`.
- Counts by GitHub-detected SPDX id: GPL-3.0 39, CC-BY-SA-4.0 20, none 10, MIT 4, NOASSERTION 4, LGPL-2.1 1, LGPL-3.0 1, Unlicense 1. Total 80, of which 5 are forks.
- Fork parent licenses: Arduino-SDI-12's parent is LGPL-2.1, Break44's parent is CC-BY-SA-4.0, and the other three parents have no detected license.

| Repository | SPDX (GitHub) | Created | Fork | Parent |
|---|---|---|---|---|
| ALog | GPL-3.0 | 2013-09-09 | false | – |
| DS3231 | Unlicense | 2013-09-11 | false | – |
| ALogTalk | GPL-3.0 | 2013-09-11 | false | – |
| ALog-BottleLogger | CC-BY-SA-4.0 | 2013-09-11 | false | – |
| DS3234 | – | 2014-05-13 | true | garthoff/ds3234 |
| RTClib | – | 2014-05-13 | true | maniacbug/RTClib |
| Arduino-SDI-12 | LGPL-2.1 | 2014-06-16 | true | Kevin-M-Smith/Arduino-SDI-12 |
| AtlasShield | CC-BY-SA-4.0 | 2014-06-26 | false | – |
| NorthernWidget-Eagle-Libraries | CC-BY-SA-4.0 | 2015-08-26 | false | – |
| ALog-BottleLogger2 | NOASSERTION | 2015-11-10 | false | – |
| ALog-BottleLogger2.2 | NOASSERTION | 2015-11-11 | false | – |
| datalogger | – | 2016-01-07 | false | – |
| ALog-Shield | CC-BY-SA-4.0 | 2016-03-17 | false | – |
| Inclinometer-breakout-SCA100T | CC-BY-SA-4.0 | 2016-04-27 | false | – |
| Component-Optimization | GPL-3.0 | 2016-06-13 | false | – |
| eRCaGuy_analogReadXXbit | – | 2016-06-24 | true | ElectricRCAircraftGuy/eRCaGuy_analogReadXXbit |
| Instrumentation-Amp | CC-BY-SA-4.0 | 2016-07-19 | false | – |
| Arduino_Boards | GPL-3.0 | 2016-12-30 | false | – |
| AtlasNW | GPL-3.0 | 2017-01-26 | false | – |
| TP-DownHole | NOASSERTION | 2017-01-27 | false | – |
| Crufty-NorthernWidget.github.io | MIT | 2017-06-01 | false | – |
| Lux | CC-BY-SA-4.0 | 2017-06-28 | false | – |
| DataCollector-Foley-Mechatronics | – | 2017-07-05 | false | – |
| TLog | LGPL-3.0 | 2017-07-14 | false | – |
| MS5803 | GPL-3.0 | 2017-07-28 | false | – |
| LTC2495 | GPL-3.0 | 2017-10-19 | false | – |
| UbloxGPS | GPL-3.0 | 2017-11-10 | false | – |
| MAX44009 | GPL-3.0 | 2017-11-13 | false | – |
| PCINT | GPL-3.0 | 2017-11-13 | false | – |
| TCA9534 | GPL-3.0 | 2017-12-01 | false | – |
| network-logger-umn | GPL-3.0 | 2017-12-11 | false | – |
| MCP3421 | GPL-3.0 | 2018-02-21 | false | – |
| Project-Margay | CC-BY-SA-4.0 | 2018-02-28 | false | – |
| Project-Ophiura | CC-BY-SA-4.0 | 2018-03-02 | false | – |
| SetTime_GUI | GPL-3.0 | 2018-04-03 | false | – |
| DS3231_Logger | GPL-3.0 | 2018-04-04 | false | – |
| TP-Downhole_Library | GPL-3.0 | 2018-05-08 | false | – |
| VEML6075 | GPL-3.0 | 2018-05-16 | false | – |
| VEML6030 | GPL-3.0 | 2018-05-16 | false | – |
| Project-Libelle | CC-BY-SA-4.0 | 2018-06-05 | false | – |
| Deployments | GPL-3.0 | 2018-06-22 | false | – |
| Margay_Library | GPL-3.0 | 2018-07-03 | false | – |
| Libelle_Library | GPL-3.0 | 2018-07-05 | false | – |
| NW_BME280 | GPL-3.0 | 2018-07-12 | false | – |
| MaxBotix_Library | GPL-3.0 | 2018-07-16 | false | – |
| Project-Okapi | CC-BY-SA-4.0 | 2018-10-18 | false | – |
| Project-Walrus | CC-BY-SA-4.0 | 2018-10-27 | false | – |
| Firmware-Aggregator | GPL-3.0 | 2019-01-02 | false | – |
| MaxBotix-Helper | CC-BY-SA-4.0 | 2019-03-21 | false | – |
| Project-Haar | CC-BY-SA-4.0 | 2019-03-26 | false | – |
| T9602_Library | GPL-3.0 | 2019-05-06 | false | – |
| NW-libs | GPL-3.0 | 2019-05-17 | false | – |
| Project-Apis | CC-BY-SA-4.0 | 2019-07-10 | false | – |
| Okapi_Library | GPL-3.0 | 2019-07-19 | false | – |
| Haar_Library | GPL-3.0 | 2019-08-06 | false | – |
| Walrus_Library | GPL-3.0 | 2019-11-04 | false | – |
| LiIon-18650-Parallel | CC-BY-SA-4.0 | 2020-02-04 | false | – |
| version-numbering-standards | – | 2020-04-30 | false | – |
| Apis_Library | GPL-3.0 | 2020-05-01 | false | – |
| NorthernWidget-libraries | GPL-3.0 | 2020-06-03 | false | – |
| Experimental-NorthernWidget.github.io | MIT | 2020-06-04 | false | – |
| NorthernWidget.github.io | MIT | 2020-06-05 | false | – |
| I2C-master-directory | – | 2020-08-07 | false | – |
| Wire-Strip-Card | CC-BY-SA-4.0 | 2020-08-11 | false | – |
| Break44 | CC-BY-SA-4.0 | 2021-03-06 | true | bschulz1701/Break44 |
| shop | MIT | 2021-07-04 | false | – |
| Margay-housing-WQ48 | – | 2025-04-13 | false | – |
| Liasis_Library | GPL-3.0 | 2026-05-12 | false | – |
| Project-Liasis | CC-BY-SA-4.0 | 2026-05-12 | false | – |
| .github | – | 2026-05-14 | false | – |
| NW-Device-Specification | NOASSERTION | 2026-05-31 | false | – |
| NW-Registry | – | 2026-06-01 | false | – |
| NW-Provision | GPL-3.0 | 2026-06-01 | false | – |
| NW-Status | GPL-3.0 | 2026-09-21 | false | – |
| NW_Core | GPL-3.0 | 2026-09-22 | false | – |
| NW-Tests | GPL-3.0 | 2026-09-23 | false | – |
| NW-Sim | GPL-3.0 | 2026-09-24 | false | – |
| NW_Logger | GPL-3.0 | 2026-09-24 | false | – |
| NW_Thermistor | GPL-3.0 | 2026-10-04 | false | – |
| NW-Cold-Silicon | CC-BY-SA-4.0 | 2026-11-04 | false | – |

## Sources checked (log, including dead ends)

- OK: docs.arduino.cc schematic PDFs A000066, A000067, A000057, A000005 (curl + pdftotext). ABX00017 also prints BY-SA 4.0; its board was not identified, so it is not used.
- OK: docs.arduino.cc/hardware/uno-rev3, leonardo, nano, mega-2560 (SKU mapping). Dead end: uno-rev3 page has no license text. Dead end: A000066-cad-files.zip returned HTML.
- Dead end: www.arduino.cc/en/Main/FAQ redirects to support.arduino.cc (not followed).
- OK: blog.arduino.cc/?p=17 (2007, BY-SA 2.5 link). OK, partial: sources.debian.org Arduino 0018 FAQ.html (no version seen).
- OK: gh api sparkfun/SparkFun-Eagle-Libraries readme.md at HEAD, e8d68b3, fa55224, 14c7bc3; sparkfun/SparkFun-KiCad-Libraries README.md; sparkfun/RedBoard, OpenLog, SparkFun_BME280_Arduino_Library LICENSE.md. Dead ends: sparkfun/Arduino_Pro_Mini_328 (no license file); sparkfun/Qwiic_Shield_Arduino (404); news.sparkfun.com/3296 (403).
- OK: gh api adafruit/Adafruit-Feather-{32u4-Basic-Proto,M0-Basic-Proto,M0-Adalogger,M0-Express}-PCB README.md + license.txt; adafruit/Adafruit-Eagle-Library (README.md, README.txt, adafruit.lbr grep). Dead end: learn.adafruit.com Feather specification has no license. Dead end: gh search for an Adafruit Feather template/spec repo found nothing.
- OK: gh api MCUdude/MightyCore (LICENSE, README.md); maniacbug/mighty-1284p (README.md). Not opened: JChristensen/mighty-1284p.
- OK: CC BY-SA 4.0 legalcode.en; CC BY-SA 3.0 legalcode.txt; creativecommons.org/faq/. Dead end: creativecommons.org/compatiblelicenses/ had no GPL text in the static HTML.
- OK: oshwa.org/resources/open-source-hardware-faq/. Dead end: oshwa.org/faq/ (404).
- OK: gnu.org/licenses/gpl-3.0.txt. Dead end: the HTML page returned 429.

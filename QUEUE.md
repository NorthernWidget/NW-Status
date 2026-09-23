# Desk queue and held items

Work that is decided or open but not yet started, with what blocks it. One line per item; the linked issue holds the detail. Kept here so the list survives sessions; NW-Status/README.md carries the per-repository state.

Last edited 2026-09-23.

## Desk work (no hardware needed)

| # | Item | Where | Blocker | Notes |
|---|------|-------|---------|-------|
| 1 | MaxBotix rebuild on NW_Core (Apis-form surface, sketch-owned serial port); weigh the ATtiny-on-Helper option first | [MaxBotix_Library #5](https://github.com/NorthernWidget/MaxBotix_Library/issues/5) | none – Walrus and Haar are done | working tree holds an uncommitted Serial1 experiment |
| 2 | Okapi library bugs: radio never powered off (#3), WDHold/Sw_Bus_Prime both on pin 23 (#4), PowerState not initialised (#5), setExtInt-before-begin ordering (#6), getVoltage leaves bus EXTERNAL (#7) | [Okapi_Library issues](https://github.com/NorthernWidget/Okapi_Library/issues) | Andy: Okapi is its own chain, done all together, not piecemeal (2026-09-23) | verify by compile; add a harness with the fixes |
| 3 | Batch abandonment: keep the Apis firmware's 2 s device-side timer (since patch 4 reported as notice kind 10, batch abandoned), or hold the batch until the next batch word | [Project-Apis #25](https://github.com/NorthernWidget/Project-Apis/issues/25) item 5 | Andy's decision (batch semantics are settled) | affects Apis only; nothing on Walrus or Haar is powered per batch |
| 4 | Project-Apis issue hygiene: #16 (32-byte map), #17 (on-demand trigger), #18 (signal strength) delivered by Schema 1; #22 (accelFail inversion) to check against patch 2 | [Project-Apis issues](https://github.com/NorthernWidget/Project-Apis/issues) | Andy's word to comment/close | |
| 5 | Spec README em-dashes (99) to spaced en-dashes | [NW-Device-Specification #2](https://github.com/NorthernWidget/NW-Device-Specification/issues/2) | Andy's decision | mechanical, one commit |
| 6 | Cleanup: Apis_Library `stash@{0}` (superseded header edit); branches `backup-before-swp-filter` (T9602_Library), `backup-before-rebase` (DS3231_Logger), `backup-default-address-on-stale-Dev_I2C` (Tally_Library) | local clones | Andy's authorisation to delete | all superseded by pushed history |
| 7 | Tally onto NW_Core (firmware Block 0 first) | NW-Status README, NW_Core row | Andy's decision on the proposed Tally appendix | T9602 and Libelle done 2026-09-23, same recipe as Walrus and Haar |
| 8 | Project-Okapi Serial_Ctrl needs a DS3231 header (DS3231_Logger migration) | Project-Okapi | none | |
| 9 | ~~Review how Margay writes files to the SD card~~ DONE for Margay 2026-09-23 (Andy: skip NW, csv; Margay definitive): `/<SN>/log00001.csv` + `sta00001.csv` + `HWTest.txt`, header row first, versions in the status file's boot row (Margay_Library 3333492, b63a8ce, 10a1650, README). Okapi copies later, in its own chain | Okapi_Library | Okapi chain | per-row open and close kept |
| 13 | Version inconsistencies found by NW-Tests version_check.py (2026-09-23): T9602_Library library.properties 0.0.0 vs CITATION.cff 1.0.0 and tag v1.0.0; MaxBotix_Library 1.1.0 vs CITATION.cff 1.0.0; DS3231_Logger 0.1.0 vs CITATION.cff 1.0.0 | those repos | Andy's word (version-bearing files) | CI's Versions step stays red until they agree |
| 14 | Build identity (decided in outline 2026-09-23): library version constants (`<LIB>_LIBRARY_VERSION`, held to library.properties by version_check.py) + commit defines (`<LIB>_LIBRARY_COMMIT`, blank in IDE builds) printed as Lib/LibCommit columns of the status row; firmware commit hash in Page 0 Block 3 0x18–0x1B + flags 0x1C (served copy only; EEPROM zeros); 0x0B–0x0D kept (Andy: "just in case"); loggers' 0x0A to be zeroed in their appendices (proposal); the wrapper that injects hashes is planned in Skunkworks/NW-Build (agent, 2026-09-23) | spec, NW_Core, four libraries, four firmwares, NW-Build | Andy's word per step; spec paragraph first | nothing written yet |
| 12 | Fast logging: an option to log as quickly as possible (geophone-rate data, for example); Andy has sketches of this from long ago; revisit once the ordinary logging path is settled (Andy 2026-09-23: "something to revisit") | Margay_Library, Okapi_Library, NW_Core (the reading interface's logReading is the per-reading primitive) | Andy to find the sketches; after items 9 and 10 | the SD write path (open and close per row) is the first constraint to measure |
| 11 | Status-file decoder: a script beside the spec that expands a logger's status file (Page 0-2 hex) into named fields per device and firmware patch; the calibration values of a re-zero row are decoded here, not on the logger (Andy 2026-09-23: "After the fact") | NW-Device-Specification or NW-Tests | after the status file exists on a logger | no Faults column; the note word is the only translation the logger writes |
| 10 | A shared logger core for Margay and Okapi? Andy raised it 2026-09-23; the only earlier design is the logger-side templates in LIBRARY-DESIGN (collectReadings, report-all; Margay_Library #27), not a shared class | Margay_Library, Okapi_Library, NW_Core | Andy's decision after item 9's review | |

## Waiting for the bench

| # | Item | Where | Needs |
|---|------|-------|-------|
| B1 | Bench Apis, Walrus, Haar, T9602 on Margay after NW-Provision writes Page 0 | Project-Apis #23, Project-Walrus #17/#18, Project-Haar | boards in hand; Haar's address moved 0x42 → 0x48 |
| B2 | Apis mode pin pull-down | [Project-Apis #24](https://github.com/NorthernWidget/Project-Apis/issues/24) | board revision |
| B3 | LiDAR power-up and acquisition timings; set firmware and library timeouts from them | [Project-Apis #25](https://github.com/NorthernWidget/Project-Apis/issues/25) | bench |
| B4 | Status file DONE 2026-09-23 through the device rows and the logger's own: Margay is a Schema 1 device (spec 026fb26; NW_Core NW_Pages df6652a; Margay 'Margay is a Schema 1 device' commit) and watches itself. Remaining: NW-Provision writes Margay's Page 1 (divider, thermistor constants, thresholds by model); the scheduled "check" row (off unless wanted); the decoder (11); Okapi's copy with the UART page serving | NW-Provision, Margay_Library, Okapi | Andy's word on the check row | hardware-untested |

## Decided, for the record

- Pages renumbered before any release (2026-09-23): 0x00-0x3F stored (Page 0 identity, Page 1 calibration, one 64-byte EEPROM image in bus order), Pages 2-5 served data with Block 0 at 0x40 and data from 0x48, Pages 6-7 reserved. Spec 4c3b18d and 65a8f68; NW_Core d2e4252; every firmware, library, harness, NW-Provision and Margay follow. No housekeeping page: Margay cuts the sensor rail every sleep, so a sensor keeps nothing between readings.
- Every sensor library carries the reading interface and N readings with statistics; statistics (`NW_Readings`) and batch mechanics (`NW_Device::beginBatch`, `takeReadings`, `batchFaulted`) live in NW_Core (2026-09-23).
- Apis stays on the Garmin LiDAR-Lite v3HP; Benewake and radar notes live in the private repositories Project-Benewake and Project-Radar (2026-09-23).
- NW_Core stays unversioned and unregistered until the overhaul ends.

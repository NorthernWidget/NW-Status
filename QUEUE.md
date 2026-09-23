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
| 9 | Review how Margay (and therefore Okapi) writes files to the SD card overall: open/close per row, folder layout, the header path, the SdFat version, error handling | Margay_Library, Okapi_Library | none (Andy 2026-09-23: "make a note of a task") | feeds the report sink (#7) and any status-file writing |
| 10 | A shared logger core for Margay and Okapi? Andy raised it 2026-09-23; the only earlier design is the logger-side templates in LIBRARY-DESIGN (collectReadings, report-all; Margay_Library #27), not a shared class | Margay_Library, Okapi_Library, NW_Core | Andy's decision after item 9's review | |

## Waiting for the bench

| # | Item | Where | Needs |
|---|------|-------|-------|
| B1 | Bench Apis, Walrus, Haar, T9602 on Margay after NW-Provision writes Page 0 | Project-Apis #23, Project-Walrus #17/#18, Project-Haar | boards in hand; Haar's address moved 0x42 → 0x48 |
| B2 | Apis mode pin pull-down | [Project-Apis #24](https://github.com/NorthernWidget/Project-Apis/issues/24) | board revision |
| B3 | LiDAR power-up and acquisition timings; set firmware and library timeouts from them | [Project-Apis #25](https://github.com/NorthernWidget/Project-Apis/issues/25) | bench |
| B4 | Failure sink for logged faults (Caveat 2): where a logger records device faults beyond the Note column | [Margay_Library #7](https://github.com/NorthernWidget/Margay_Library/issues/7) | after base Apis works with base Margay on the bench |

## Decided, for the record

- Every sensor library carries the reading interface and N readings with statistics; statistics (`NW_Readings`) and batch mechanics (`NW_Device::beginBatch`, `takeReadings`, `batchFaulted`) live in NW_Core (2026-09-23).
- Apis stays on the Garmin LiDAR-Lite v3HP; Benewake and radar notes live in the private repositories Project-Benewake and Project-Radar (2026-09-23).
- NW_Core stays unversioned and unregistered until the overhaul ends.

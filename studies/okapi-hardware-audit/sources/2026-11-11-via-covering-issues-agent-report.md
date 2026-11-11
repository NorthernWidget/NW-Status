# Via covering (tenting) issues across NW sensor boards: agent report

Status: COMPLETE (2026-11-11)

Task (Andy, 2026-11-11): file "Cover (tent) vias with solder mask at the next board revision" on each NorthernWidget sensor-board hardware repository. Decision record: https://github.com/NorthernWidget/Project-Margay/issues/78. Margay and Okapi skipped (already covered in their KiCad conversions).

Repository list: `gh repo list NorthernWidget --limit 300` returned 80 repositories.

## Results

| Repo | Board file | Via setting found | Vias | Existing issue | Filed issue URL | Note |
|------|------------|-------------------|------|----------------|-----------------|------|
| Project-Margay | (skipped by instruction) | KiCad conversion already tents all vias | – | #78 (decision) | – | skipped: already done |
| Project-Okapi | (skipped by instruction) | KiCad conversion already tents all vias | – | – | – | skipped: already done |
| Inclinometer-breakout-SCA100T | inclinometer-breakout-SCA100T.brd | Eagle DRU "default", mlViaStopLimit 0mil, mvStopFrame 1 | 0 | none | NOT FILED | sensor breakout but board has no vias; listed for Andy |
| MaxBotix-Helper | MaxBotix-Helper.brd | Eagle DRU "default", mlViaStopLimit 0mil, mvStopFrame 1 | 0 | none | NOT FILED | sensor-interface board with no vias; listed for Andy |
| Project-Apis |Hardware/LiDAR_Lite_Interface_HardSwitch.brd (+2 untested) | oshpark-2layer, mlViaStopLimit 0mil, mvStopFrame 1 | 51 (24, 24) | none (search hits #18, #21, #23 unrelated)| https://github.com/NorthernWidget/Project-Apis/issues/26 | filed with label enhancement |
| Project-Haar |Hardware/Haar_HardMount.brd (+legacy/Haar.brd) | oshpark-2layer, mlViaStopLimit 0mil, mvStopFrame 1 | 31 (24) | none| https://github.com/NorthernWidget/Project-Haar/issues/14 | filed with label enhancement |
| Project-Liasis |Hardware/LongWaveModule.brd | oshpark-2layer, mlViaStopLimit 0mil, mvStopFrame 1 | 18 | none (#2 unrelated)| https://github.com/NorthernWidget/Project-Liasis/issues/3 | filed with label enhancement |
| Project-Libelle |Hardware/Libelle_SmallBoard.brd (+Libelle.brd, 0 vias) | oshpark-2layer, mlViaStopLimit 0mil, mvStopFrame 1 | 30 (0) | none (#3, #19, #20, #22 unrelated)| https://github.com/NorthernWidget/Project-Libelle/issues/24 | filed with label enhancement |
| Project-Walrus |Hardware_HardMount/TPDH-Walrus_HardMount.brd (+2 LargePTH) | oshpark-2layer, mlViaStopLimit 0mil, mvStopFrame 1 | 40 (24, 38) | none (#7, #16, #17 unrelated)| https://github.com/NorthernWidget/Project-Walrus/issues/19 | filed with label enhancement |
| TP-DownHole |Hardware/TP-DownHole_v2.brd (+Longbow x2, Longbow_Prog, TP-DownHole.brd) | v2 BayArea-2layer 0mil; Longbow oshpark 0mil; TP-DownHole.brd SparkFun 25mil (covered) | 13 (13, 13, 4, 14 covered) | #4 related (via size under ADC), not tenting; referenced| https://github.com/NorthernWidget/TP-DownHole/issues/6 | filed with label enhancement |
| Lux |Lux_5V Compatable.brd (+Lux.brd) | 5V: PCB-POOL Standard 0mil, mvStopFrame 0; Lux.brd SparkFun 25mil (covered) | 5 (1 covered) | none| https://github.com/NorthernWidget/Lux/issues/1 | filed with label enhancement |
| Instrumentation-Amp |InstrumentationAmp.brd (+CMP3_Amp.brd) | PCB-POOL Standard 0mil, mvStopFrame 0; CMP3 oshpark 0mil | 35 (11) | none| https://github.com/NorthernWidget/Instrumentation-Amp/issues/2 | filed with label enhancement |
| AtlasShield |AtlasShield.brd | default, mlViaStopLimit 0mil, mvStopFrame 1 | 11 | none| https://github.com/NorthernWidget/AtlasShield/issues/1 | filed with label enhancement |

Method: board files fetched from each repository's default branch with `gh api .../contents` (local clones of Project-Apis, Project-Walrus and Instrumentation-Amp were behind their remotes, so remote copies were used throughout). Design rules read from `<designrules>` params. Vias counted as `<via>` elements under `<signals>`; none carries `alwaysstop="yes"`. Gerber solder-mask confirmation was not done.

## Repositories considered and skipped

- Margay, Okapi: skipped by instruction (KiCad conversions already tent every via).
- Inclinometer-breakout-SCA100T, MaxBotix-Helper: sensor or sensor-interface boards with 0 vias (rules 0 mil). Not filed; Andy to decide.
- Loggers, not sensors: ALog-BottleLogger, ALog-Shield, TLog, network-logger-umn.
- Adapters and power, not sensors: Project-Ophiura (I2C/RS485 bus breakouts), LiIon-18650-Parallel (battery supply).
- No board file in the repository tree: every other non-archived, non-fork repository (libraries, specs, tools, websites). Checked by scanning each tree for `.brd`/`.kicad_pcb`.
- Archived or fork: excluded by `gh repo list` flags (Arduino-SDI-12, Break44, DS3234, RTClib, eRCaGuy_analogReadXXbit are forks).
- Outside the NorthernWidget organization (NorthernWidget-Skunkworks), with boards in the local workspace: Project-Dyson, Project-Calypso, Project-Longbow, Project-Raven, Project-Tally, Project-ThermalStake, Project-Symbiont-LiDAR, Project-Astron, ICSP adapter, RockBLOCK-feather. Not filed (out of scope). Andy to decide.

## Failed commands

- The board-tree scan loop exited 1 (its last `grep` found no match); the output was complete.
- A `grep -c` loop split `Lux_5V Compatable.brd` on its space; rerun with quoting.

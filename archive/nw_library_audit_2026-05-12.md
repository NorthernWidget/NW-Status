# NorthernWidget Library Manager Readiness Audit

Source: `nw_library_audit_2026-05-12.csv`

## Tier 1 — Minor fixes only

| Library | Type | library.properties | Examples | keywords.txt | getHeader/getString | API case | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Apis_Library | Sensor | OK | OK (2) | OK | Implemented | lowercase | Most complete; ready for Core dependency wiring |
| DS3231 | Component | OK | OK (10) | OK | N/A (RTC) | N/A | Cleanest repo in the set |
| Margay_Library | Logger | OK | OK (3) | OK | N/A | N/A | In good shape |
| Haar_Library | Sensor | OK | MISSING | MISSING | Implemented | lowercase | version=0.0.0; needs examples + keywords.txt |
| T9602_Library | Sensor | OK | MISSING | MISSING | Implemented | lowercase | version=0.0.0; URL points to Haar repo (wrong) |
| Tally_Library | Sensor | OK (missing category) | OK (1) | OK | Implemented | CAPITAL G | GetHeader/GetString need rename; URL uses underscore in org name |
| TP-Downhole_Library | Sensor | OK | OK (1) | OK | Implemented | CAPITAL G | GetHeader/GetString need rename |

## Tier 2 — Moderate work

| Library | Type | library.properties | Examples | keywords.txt | getHeader/getString | API case | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Walrus_Library | Sensor | OK (missing maintainer + blank URL) | MISSING | MISSING | Implemented | lowercase | Needs maintainer field, URL, examples, keywords.txt |
| MaxBotix_Library | Sensor | OK | MISSING | MISSING | Implemented | lowercase | Header returns 'Distance [mm], ' — trailing space bug; needs examples + keywords.txt |
| MS5803 | Sensor | OK (blank paragraph) | OK (1) | MISSING | NOT implemented | N/A | Needs keywords.txt and sensor API implementation |
| BME_Library | Sensor | MISSING | MISSING | MISSING | Implemented | lowercase | Has working API despite no metadata; needs library.properties + examples + keywords.txt |
| VEML6075 | Sensor | MISSING | OK (1) | MISSING | NOT implemented | N/A | Needs library.properties + keywords.txt + sensor API |
| DS3231_Logger | Component | OK (blank paragraph) | MISSING | OK | N/A (RTC) | N/A | Needs examples |

## Tier 3 — Substantial work or blocked

| Library | Type | library.properties | Examples | keywords.txt | getHeader/getString | API case | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| VEML6030 | Sensor | MISSING | MISSING | MISSING | NOT implemented | N/A | Essentially a stub; full work needed |
| TCA9534 | Component | MISSING | MISSING | MISSING | N/A | N/A | Bare repo |
| MCP23018 | Component | MISSING | MISSING | MISSING | N/A | N/A | Bare repo |
| MCP4725 | Component | MISSING | MISSING | MISSING | N/A | N/A | Bare repo |
| MCP3421 | Component | OK | OK (1) | OK | NOT implemented | N/A | BLOCKED: name conflicts with existing Arduino Library Manager entry; needs rename |
| Monarch_Library | Sensor | MISSING | NOT in examples/ folder | MISSING | Partial (LW only) | CAPITAL G | BLOCKED: cross-contaminated with Dyson files; Monarch is successor to Dyson; rename undecided; no SW API |
| Dyson_Library | Sensor | MISSING | NOT in examples/ folder | MISSING | NOT implemented | N/A | BLOCKED: contains only Monarch* source files — no Dyson-specific code; superseded by Monarch |
| Okapi_Library | Logger | WRONG (says Resnik_Library) | MISSING | OK | N/A | N/A | Wrong name + URL in library.properties; version=0.0.0; deferred |
| Resnik_Library | Logger | OK | MISSING | OK | N/A | N/A | Deferred per repolist |
| Symbiont-LiDAR_Library | Sensor | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | N/A | NOT CLONED LOCALLY — only Project-Symbiont-LiDAR backups present |

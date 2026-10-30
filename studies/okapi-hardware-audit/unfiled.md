STATUS: COMPLETE

# Okapi hardware audit: findings not yet filed as issues (2026-10-30)

Every hardware change, check or measurement the working notes call for on the Okapi v1.0 board, against the open issue lists. Nothing filed. "Verified" means read today from `Project-Okapi/Hardware/Okapi.sch`, parsed by net.

## The table

| # | Item | Where it is recorded | Already an issue? | Proposed title if unfiled | Repo | Blocks a first build? |
|---|---|---|---|---|---|---|
| 1 | LED grid labels (A B C, 1 2 3, STAT, AUX, column outlines) sit on tDocu (layer 51), not tPlace: not printed | `okapi-leds/1-columns.md` (final report, "Layout, measured"); README "Hazards"; Okapi_Library#9 last paragraph | no (a line inside Okapi_Library#9, the wrong repo) | Move the LED grid's labels and column outlines from tDocu to tPlace | Project-Okapi | yes (layout, before fab) |
| 2 | Column C runs the opposite way to A (green at C3, at A1); the color layout is symmetric under a 180° turn, so an upside-down board swaps A and C | `2-lifting-0d-to-2d.md` lines 7, 52; `4-glyphs.md` line 75; `5-part-brightness-quantity.md` section 6; Okapi_Library#9 | no | Fit column C's LEDs the same way up as A, or label its direction | Project-Okapi | yes (placement, before fab) |
| 3 | Pin 0 (PB0) is the PCA9634's `!OE` (`!LED_EN`, R18 100k; verified) and `Okapi.h:224` still defines `ADC_Sense_SW = 0`, toggled around every battery read | `1-columns.md` "A collision"; QUEUE "LED work" item 5; Okapi_Library#9 item 7 | hardware: nothing. Firmware: inside Okapi_Library#9 only | Reclaim pin 0 from the stale `ADC_Sense_SW` define | Okapi_Library | no |
| 4 | PAC1934 `SLOW/!ALERT` on expander GPB4 (a floating input) and `!PWRDN` on 3V3_CORE: hardware default 585 uA | QUEUE "sleep floor"; Project-Okapi#31 rec. 3. Verified: `CSA_!ALERT` = U32, U41 GPB4; `!PWRDN` on 3V3_CORE | yes, #31 | – | Project-Okapi | no (firmware single-shot) |
| 5 | PAC1934 shunts R72–R75 unvalued | #21; `Okapi.cpp:235`. Verified: all four `value=None` | yes, #21 | – | Project-Okapi | yes |
| 6 | PAC1934 `ADDR_SEL` resistor R51 unvalued, so the firmware scans 0x10–0x1F for the product ID | `Okapi.cpp:331-332`. Verified: R51 `value=None`, net N$21 | no (#21 covers R72–R75 only) | Give R51 (PAC1934 ADDR_SEL) a value and record the address in the bus-occupancy table | Project-Okapi | yes (BoM) |
| 7 | Re-land the charger's `!FAULT` on `!SHDN` | #30 | yes, #30 | – | Project-Okapi | yes (layout) |
| 8 | B-SoM 3V3 unsourced; core path boost-then-LDO | #31; `okapi-power/README.md` | yes, #31. The power study adds one thing #31 lacks: a redesign must keep the comparator failover (V_BETA against a fixed reference) | – (comment on #31) | Project-Okapi | yes |
| 9 | TPL5111 DONE reaches no MCU pin. **Verified, and the notes have it wrong:** net `WD_DONE` = U8 DONE, **MS1 GPIOA3 (the FeatherWing socket's A3)** and J9 ADC3 (the B-SoM); no U41 pin is on the net, so "drive DONE through the expander" is not available | QUEUE "Okapi's watchdog is not being fed"; `Okapi.cpp:25-33`; Okapi_Library#4 | no. #27 assumes a "DONE signal connection to IC1 GPIO" that does not exist | Route TPL5111 DONE (WD_DONE) to an MCU or expander pin | Project-Okapi | yes: it runs unfed from power-up with DRVN gating a supply; bench check first |
| 10 | JP8's second period, R62 330k, exceeds the TPL5111's 170k maximum | QUEUE, same section; `Okapi.cpp:30-31`. Verified: R20 130k, R62 330k | no | Replace R62 (330k) on JP8 with a value inside the TPL5111's 170k limit | Project-Okapi | no |
| 11 | Firmware reads ADS1115s at 0x48 and 0x49; v1.0 has none (**verified: no `ADS111*` part in Okapi.sch**). `Okapi_BoM.csv` lists ADS1115 as U32/U33 and has no U45 or D10–D18 | QUEUE grid table requisite 1; `Okapi.h:169`; `1-columns.md` | firmware: no own issue (TEMPORARY in code). Hardware: #29 and #28 item 5 list the ADS1115 as on-board, wrongly | Regenerate Okapi_BoM.csv from the v1.0 schematic; correct #29 and #28 | Project-Okapi | yes (fab input) |
| 12 | 220 Ω anode resistors on all eight grid LEDs; green runs dim; whether 220 Ω is right next time | Okapi_Library#11; `5-part...md` section 1 | yes, Okapi_Library#11 | – | Okapi_Library, then Project-Okapi if the value changes | no |
| 13 | Grid LED part numbers absent (`LEDGREEN0603` etc.), so Vf and wavelength are unknown; GaP green merges with yellow for deuteranopes | `5-part...md` sections 1, 6; `1-columns.md` | no | Specify manufacturer part numbers for D10–D18 (an InGaN green) | Project-Okapi | yes (BoM) |
| 14 | Solar under-voltage lockout R71 1M / R70 200k / Q8 on `!CHRG`, "about 7 V" (unverified), against a 6 V panel with Voc 7–7.5 V | #30 "Why not a new trace"; #20 covers only the MPPT divider; #13's unchecked box. Nets verified | no | Verify the LT3652 solar lockout threshold (R70/R71/Q8) against the panel's Voc | Project-Okapi | yes (a charger that may never start) |
| 15 | LTC4412 STAT unconnected | #5. Verified: STAT goes only to R21, other end V_BETA | yes, #5 | – | Project-Okapi | no |
| 16 | FRAM U35 is `MB85RC*`, no value: capacity, address, standby current unknown | QUEUE "sleep floor"; #31; #29 to-do 1 | no (named in passing, chosen nowhere) | Choose the MB85RC FRAM part (U35): capacity, address strap against Walrus 0x57, standby current | Project-Okapi | yes (BoM) |
| 17 | Measured sleep current on a built board | QUEUE "sleep floor"; #31 acceptance 3 | yes, #31 | – | Project-Okapi | no |
| 18 | PCA9634 All Call at 0x70 enabled at power-up; whether a 0x70 device sits on SDA_OB is unverified | `5-part...md` section 1 (3) | no; #29 does not list U45 | Add the PCA9634 (0x52, All Call 0x70) to the bus-occupancy check (comment on #29) | Project-Okapi | no |
| 19 | LogInt: `NW_Logger.cpp:135` says PA4, the schematic puts S3 on PA3 | `5-part...md` section 7 | no | Confirm the log button's pin against the variant | Okapi_Library | no |

## Unfiled items: two-sentence summaries

**1. Grid labels on the wrong layer.** The labels and column outlines are on tDocu and are not printed. Move them to tPlace before fab: the outlines group the cells into stoplights.

**2. Column C's direction.** Column A has green at the bottom and C at the top, and the colors map A to C under a half turn, so only the empty cell cues orientation. Fit C's LEDs the same way up as A, or print the direction.

**6. R51 unvalued.** The PAC1934's ADDR_SEL resistor has no value, so the address is unknown and the firmware scans for the chip. Choose the value and record the address in the spec's bus-occupancy table.

**9. The watchdog's DONE line goes to the cell module.** `WD_DONE` lands on the FeatherWing socket's A3 and the B-SoM's ADC3, not on the ATmega or the MCP23018, so no MCU firmware can feed the TPL5111; the notes' fix rests on misreading MS1 as the expander. Route DONE to an MCU or expander pin, or decide that the Particle owns the watchdog, and bench-check what an unfed TPL5111 does to the supply.

**10. R62 out of range.** JP8's second position selects 330k, above the TPL5111's 170k maximum, so that position is undefined. Replace it with a value in range (130k gives 3943 s).

**11. The BoM predates v1.0.** `Okapi_BoM.csv` lists ADS1115s at U32/U33, which v1.0 reassigned (the schematic carries no ADS1115), and has no PCA9634 or grid LEDs. Regenerate it from the schematic, then correct #29 and #28.

**13. Grid LED parts.** D10–D18 carry color names only, so forward voltage, wavelength and brightness are unknown, and a GaP green is unreadable for a deuteranope. Specify parts, with an InGaN green.

**14. Solar lockout threshold.** The R70/R71/Q8 network holds the charger off until the panel reaches about 7 V (unverified), near a 6 V panel's open-circuit voltage. Compute the threshold and lower it if the charger cannot restart under load.

**16. FRAM part unchosen.** U35 is `MB85RC*` with no capacity, address or standby current; the 0x50–0x57 range may clash with Walrus at 0x57. Choose the part and its address strap.

**18, 19.** Small checks: add the PCA9634 to the bus-occupancy table; confirm the log button's pin (PA3 in the schematic, PA4 in `NW_Logger.cpp:135`).

## Sources checked

- `NW-Status/QUEUE.md`: ON ANDY'S DESK (7-56); watchdog (975-1007); LEDs and decisions (1055-1164); grid table through order of work (1165-1494); bench (1626-1663); battery readings (1754-1803); Group 2 (1853-1883); queue (1899-1938).
- `NW-Status/studies/okapi-leds/README.md`; `1-columns.md` (a 4.8 MB JSONL agent transcript, not a note: final report extracted with Python); `5-part-brightness-quantity.md`; grep of `2-lifting-0d-to-2d.md` and `4-glyphs.md`.
- `NW-Status/studies/okapi-power/README.md`. `okapi-route/README.md` does not exist (dead end): the directory holds `route_search.py` and two PNGs, summarized in #30.
- `NW-Status/ITEM1-HANDOFF.md`, every Okapi mention.
- `Okapi_Library/src/Okapi.cpp`, `Okapi.h`: grep for FIX!, TEMPORARY, UNVERIFIED and part names; lines 20-34, 163-180, 228-237; h 165-172.
- `gh issue list -R NorthernWidget/Project-Okapi --state open --limit 100` (25 open); `gh issue view` 31, 30, 29, 28, 27, 21, 20, 16, 13, 7, 5, 3. `gh issue list -R NorthernWidget/Okapi_Library --state open` (11 open); `gh issue view` 9, 11, 4.
- `Project-Okapi/Hardware/Okapi.sch`: parts U32, U35, U7, U4, U45, R51, R20, R62, R56, R72-R75, U41, MS1; nets `WD_DONE`, `!LED_EN`, `CSA_!ALERT`, `MPPT_*`, N$46, N$21; part search for ADS1115 and the on-board sensors. `Okapi_BoM.csv`: grep for ADS1115, U45, D10-D18.

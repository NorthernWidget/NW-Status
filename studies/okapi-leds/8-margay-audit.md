I have the record end to end now. Report follows.

# Margay's LED protocol: the decisions, the traces, and Andy's question applied to Margay

## Verdict

Margay's LED philosophy, as actually decided: **the LED speaks once, at deployment, to a person who is there, and says one thing.** Two lights divide one job: the aux (D2 green) means only *alive and busy*, and the status RGB (D3) gives one verdict – the worst message raised – as a rhythm inside a fixed three-second window, after the first row is on the card. Severity is Andy's, defined by the action required (none / next visit / now), not by the event. Identity rides on rhythm read as a shape, never on counting ("this becomes a look-up table with everything given equal weight" is what he rejected). Colour is a second carrier of the same severity, not an independent channel. After boot nothing shows but a 20 ms blue blip per row written, because "an interval change at three in the morning has no observer"; everything else goes to the Note column and the serial line. The LED is a pointer to the file, not a substitute for it – which is exactly why, with no card, the card outranks every other fault. Any Okapi extension that adds a standing display, a second tempo, a count, or a message the file could carry instead contradicts this.

## 1. The decision list

Sources: **Q** = `NW-Status/QUEUE.md`, "Logger messages and the LED vocabulary, settled (Andy, 2026-10-09)" and subsections; **H** = `NW-Status/ITEM1-HANDOFF.md`; **M** = `NW_Logger/src/NW_Message.h`; **L** = `NW_Logger/src/NW_Logger.cpp` `signal()`/`run()`/`logRow()`; **G** = Margay_Library git.

| Decision | Reason given | Whose | Source |
|---|---|---|---|
| Three bands, about the action required | "fine means none, caught means act at the next visit, actively bad means it is not logging as asked"; severity belongs to the cause, not the event | Andy | Q "The messages" |
| Flat list in the logger's own namespace, not the sensor Report register | "You pulled our entire work into an incompatible format" | Andy | Q heading; M header |
| One worst message, not a list or a count | 1–4 flash counts rejected: "a look-up table with everything given equal weight" | Andy (rejection); agent (mechanism) | Q "Design rules"; M 42–44, 147–158 |
| Severity on colour and rhythm; identity on rhythm as a shape; absolute rate dropped (IEC 60073 bands kept for colour only) | one LED to one person has nothing to rank against; "Duration is not a severity lever" | agent, in session with Andy | Q rules 1–4 |
| Colour redundant; blue = all well | "Blue already means 'all well' through the chirp"; red/amber/green "genuinely overlearned" | agent | Q "The two LEDs", "Design rules" |
| ↳ *because of red/green deficiency* | **UNVERIFIED as Andy's.** Appears only in the Okapi study brief (`studies/okapi-leds/1-columns.md` line 1, a parent-agent paraphrase) and note 2; not in Q, H, M or L | – | – |
| Blue itself | inherited: Andy's 2021 `BlinkGood()` wrote `BlueLED` | Andy, 2021-07-03 | G a5f84a4 "The return of LONG short short" |
| Fixed 3 s window | "so the instruction is one sentence"; a late glance still catches whole cycles | agent | Q "The patterns"; L `NW_SIGNAL_WINDOW_MS` |
| Ready chirp 1000/300/100/100/100 from ALog | "Peppy blinky pattern" – `LEDgood()`, 2013 | Andy (ALog) | `Logger/Logger.cpp` fb1a551 2013-09-11; L |
| Clock syncopation 250/100/100/100 from ALog | "Syncopated pattern to show that the clock has probably reset" – "the form carries the meaning" | Andy (ALog); Q endorses | Q; `ALog/src/ALog.cpp:1226` |
| Three card faults, one pattern | "the user does the same thing about either – reseat or replace – and the file says which" | agent | L comment; commit 4eebddd |
| Card at 60/60 not ALog's 40/40 | "better safe" | Andy | Q |
| 500/500 ×3 amber | Q: battery low; code: the whole CAUGHT band, so no verdict is dark (a dead BME280 read as a dead board) | reviewer/agent | Q table; H fix 1; L `default:` |
| 100/300 ×8 sensor, last gap dropped | "calling out and hearing nothing back" | Andy | Q; L `if (i < 7)` |
| Solid red for the rest of BAD | "the strongest state gets the one signal with no rhythm" | agent | L; H fix 1 (not in Q's table) |
| Nothing in the field; `note()`'s orange flash retired | no observer; the only in-field signal "fires on every note written" | agent, approved | Q "What the field sees" |
| Per-row blip on status, not aux, in blue | "the same statement in miniature... same colour on the same LED" | agent; heritage Andy 2021-07-17 | Q; G a49a567; L `logRow()` |
| Aux = powered and busy, from `begin()`'s first instruction to the verdict | "the one thing the status LED cannot say yet"; D2's red/blue belong to the FT231X | agent, from the schematic; heritage Bobby 2018 | Q "The two LEDs"; G 0f0548b, 5dcfbf1 |
| Aux-off moved to just before the verdict, after the first row | "no dark gap while the file is opened and the row is written" | agent | L `run()`; commit 61d3af0 |
| BAD order: card, NO_SCHEDULE, sensor, clock | "with no card the LED is the only channel left" | **agent's, awaiting overrule** | M 65–67; Q desk item 6 |
| FINE messages file-only; FINE-only set answers READY | "a field message has no observer"; a clean boot gets the chirp, not housekeeping | agent | L `default:`; M 139–145 |
| Message set cleared each cycle | the boot set lives until the verdict | agent | L `run()`; H fix 4 |
| Old boot sequence replaced | Bobby 2018: aux on; one 2 s solid colour per failed flag (red/orange/cyan/purple); green 2 s if clean; `Blink()` blue 500/500 ×5 at log start. Andy 2021: `BlinkGood()` long–short–short (651/300/100/200/100) and per-row blue. Replaced because the chirp was unconditional ("fault colour and then the happy chirp anyway"), the colours were a look-up table, and `LED_Color()`'s 16-bit overflow left every full-brightness colour dim – "the dim 'green light' Andy described" | agent; defect verified | Q "Three defects"; G 0f0548b, a5f84a4; H; `NW_Logger` acd7714 |

Note on the brief's "green, then blue, then blue long–short–short": verified history is green (2 s, `begin()`) then blue 500/500 ×5 in 2018, and green then blue long–short–short from 2021. No solid blue step existed.

## 2. What the LEDs do today (`NW-Sim/tests/baseline/*.leds`)

All traces open with red/green/blue off at ~248 ms (`LED_Color(OFF)`). The aux *on* edge is never recorded: the pin is driven LOW from a LOW default, so the trace cannot assert the aux lit (UNVERIFIED on the simulator, by construction).

| Baseline | Sketch (`run.sh`) | Recorded sequence | Against the protocol |
|---|---|---|---|
| margay_basic | examples/Basic | blue 1878–1898 (first-row blip); aux off 1992; blue 1993–2993, 3293–3394, 3494–3594; blips 20 ms every 5 s | chirp 1000/300/100/100/100 exact; **the first row's blip precedes the aux-off by 94 ms** |
| margay_nocard | Basic, no card | aux off 1788; red 60/60, 25 cycles, 1788–4745; no blips after | 60/60 ×25 = 3000 ms exact; no blip without a card, correct |
| margay_missing | Programmed_Margay, no Apis | aux off 2300; red on at 2300, 2701, 3101, 3502, 3903, 4303, 4704, 5105, each 100 ms; off 5205; blips at 60 s | eight pips, 2905 ms, last gap dropped, correct |
| margay_blank | Basic, no stored Page 0 | aux off 2000; red 2000–2501, 3001–3501, 4002–4502 with stray green edges; blips every 5 s | 500/500 ×3 amber (Page0Invalid, CAUGHT); green edges are `analogWrite` set-up writes, not PWM – `margay.c:91` says partial channels are "not seen", which is true in substance, UNVERIFIED in mechanism |
| margay_overrun | Overrun_Margay (`wdtSeconds = 3`) | aux off 2071; red 2072–5072; blips every ~1 s | solid red 3000 ms exact (NoSchedule) |
| margay_programmed / margay_discovered / walrus_margay | Programmed / Discovered / Walrus_Margay | blip, aux off, chirp, blips at 60 s | READY, correct |
| margay_scan | examples/BusScan | three off edges only | no logger, nothing to show |

## 3. Andy's question applied to Margay

| Element | Carries information no other channel gives at that moment? | Or there because the LED is there? | Cost to remove |
|---|---|---|---|
| Aux busy light | Yes – during the self-tests the serial line may be unplugged and the status LED is dark; "alive, not dead" has no other channel. Also marks *when* to look | Partly: its pin was already a "built-in LED" in 2018 | Lose the cue that starts the 3 s count; a slow boot reads as a dead board |
| Ready chirp | Yes, exactly one bit: tests passed **and** a row reached the card, which no serial line says in one glance | The *form* is heritage ("peppy"), 1.6 s where 100 ms would carry the bit | Nothing technical; the long–short–short is overlearned by ALog and Margay users since 2013, and that is its whole value |
| Per-row blip | Yes at a bench with no serial: "the card took that row". In the field, nobody sees it | Partly; 20 ms is already the floor | ~0 µA·s; removing it removes the only confirmation that logging continues when a laptop is not attached |
| Five rhythms | Yes: four of five name a distinct technician action (reseat card; bring laptop and set clock; check sensor wiring; shorten the cycle or fix the watchdog). The colour alone could not | The syncopation and flutter are iconic, so no table is needed | Collapsing to band-only would make clock, sensor and schedule one solid red; three actions become "open the file" |
| Colour | Redundant by design; it never disambiguates anything rhythm does not | Yes – it is there because the LED is RGB. Its value is speed for a normal-vision reader and continuity with stoplight habit | None in information; removing it would strand the "blue = well" habit |
| 3 s window | Yes: it makes the instruction one sentence and rescues a late glance | No; it is a constraint, not a display | Removing it makes every pattern a one-shot and reintroduces "did I miss it" |
| Amber band for eight CAUGHT causes | Carries one bit – look at the file at the next visit – which is the right bit, because CAUGHT is defined as "the file has it" | The slow 500/500 is the least informative rhythm in the set | Zero; subdividing would be adding information the Note column already carries |

## 4. What Margay cannot say

- **A second fault.** The self-tests are independent, so these co-occur: no card + unset clock (the commonest bench state; shows card only); card + sensor; clock + sensor; PAGE0_INVALID or BME_MISSING with anything (hidden under any BAD). Within the card set and within the clock set the causes are mutually exclusive (`else if`; `clockTest()` branches).
- **An on-board I2C bus failure.** The clock, the battery ADC and the BME280 share that bus, so a dead bus raises CLOCK_NOT_SET + ONBOARD_MISSING + BME_MISSING and the LED plays the clock syncopation – it names a chip when the truth is the bus.
- **Which CAUGHT.** Eight words, one shape; six are raisable today. BATTERY_LOW and BACKUP_WOKE are defined and raised nowhere (verified by grep of the three `src/` trees).
- **Anything after boot.** `_messages` clears each cycle; a button-press verdict needs a second accumulator (study note 5).
- **That the aux ever lit**, on the simulator (above).

## 5. Inconsistencies and gaps

1. **Q's message table is stale against the code**: 13 (+3 to add) versus 20 in `NW_Message.h`; Q's pattern table still assigns amber to "battery low" and omits solid red. Code and H are authoritative on the rendered set; Q on Andy's categories and words.
2. **Blue-for-colour-deficiency is not in the record** (section 1). The brief and the Okapi studies carry it as a premise; Andy's recorded reason is continuity with the chirp.
3. **The BAD order is the agent's**, explicitly flagged for overrule (desk item 6); the verdict tests encode it as if settled (`test_output.cpp:192–194`).
4. **`NW_Logger.h:249`** still documents `note()` as "shown as an orange pulse on the LED"; the pulse was retired 2026-10-20. `ORANGE` remains defined, unused.
5. **The first row's blip plays before the aux goes out** (`margay_basic`), a 20 ms blue flash while the aux is still "busy", undescribed in Q or H. Harmless; it predates the verdict ordering.
6. The 2026 chirp uses ALog's 1000/300/100/100/100, not Margay's 2021 651/300/100/200/100. Q claims ALog provenance, so the code is consistent with Q and discontinuous with Margay's own 2021–2026 behaviour; nobody recorded choosing between them.

## 6. Verdict, restated for Okapi

Margay's protocol is a pointer: one worst message, read as a shape in three seconds, aimed at the file. Every element that survives Andy's question does so because it names a distinct action or marks when to look; colour and the amber band survive as redundancy, not as information. The Okapi grid's one genuine gain is simultaneity – the hidden second fault and the bus-versus-clock confusion in section 4 are the only things Margay cannot say that a technician would act on. A design that spends the eight cells on anything else is using them because they are there.

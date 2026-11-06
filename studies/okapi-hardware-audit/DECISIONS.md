# Okapi and Margay: the decisions, for one sitting

Andy, 2026-11-04: grind through the mechanical items first and keep every real
decision for the end. The mechanical items are done (`CHECKS-TODO.md` here and in
`studies/margay-kicad/`, `KICAD-TODO.md`). Later the same day, on the DRC items:
"make many decisions to match the prior ways in which the Eagle boards printed";
the fabricated board (Bobby's CAM Gerbers, Eagle's rule set) settled those, and
they are recorded at the end as the record of what was done.

Each open entry names the options and what each costs. Nothing is started until
Andy picks. Within each board the order is the one to take them in: design first,
since those can change the board.

## Okapi

### The plan (2026-11-05), split by who should do it

Okapi checked the way Margay was: the conversion lost no copper (every one of
Eagle's 3897 wires and 345 vias is on the KiCad board, at the first import and
now); the BoM has Margay's slips and one gap of its own (the KiCad fields carry a
number on 16 of 117 lines where Eagle's device technologies hold one for 222 of
376 parts); the built prototypes say REV 1.0 and the registry 1.0.0 while
GitHub's latest release is v0.6.0; 24 issues are open on no milestone. The
findings are in `parts-audit.md` beside this file. Andy, 2026-11-05: Fable-tier
work first, then the rest with a cheaper model.

**A. Fable, first** (judgment, datasheets, anything that changes a rule or a
board):

A1. **DONE 2026-11-05, Andy's call: Okapi stays pre-1.0 until it is ready.** The 25
    boards (late 2019 or early 2020; 15 registered as board type 0x9950, hardware
    0.4.0, "formerly Resnik") are the v0.4 design and the only Okapi boards ever
    built or run (Andy, 2026-11-05: v0.5.0's 2020-02-13 files and the 2024
    v0.6.0 redesign were never built); their silk's "v1.0" is
    the one outlier and nothing reads silk. v0.6.0 stays the marker of the 2024
    redesign. The KiCad board continues at v0.7.0 and up, pre-1.0 minors allowed
    to break; v1.0.0 and board type 0x4F01 (reserved, "Okapi 1.0.0", matching the
    2024 title block's REV 1.0) are for the design judged ready, with rc's before
    a run and the as-built confirmation after, as Margay's. No retroactive tags.
    Still to do under this item (B3): milestones for v0.7.0 and v1.0.0 and the sort
    of the 24 open issues onto them, from a triage list Andy approves.
A2. **R26 to R33**: the schematic says 287R, the build ordered 232 Ω and 453 Ω
    (ILIM of the four port switches U17 to U20, the second in parallel through
    JP1 to JP4). Read the switches' datasheet for what each sets, decide the
    intended limits, then the value fields and the as-built row.
A3. **R72 to R75 and R51** (PAC1934 shunts and address select, #21). Checked
    2026-11-05 against the Eagle nets and the full datasheet (DS20005850B, 56
    pages; the 26-page copy in scratch lacks Table 5-1). Channels: 1 is V_PRIME
    through R73, 2 is V_LI through R72, 3 is V_BETA through R75, 4 is V_SOLAR_IN
    through R74, and `Okapi.h`'s channel 2 = V_LI, channel 4 = V_SOLAR agree.
    Range ±100 mV; LSB 1.5 µV unidirectional, 3.05 µV bidirectional (16 bits);
    shunt = 0.1 V / I_max. **Correction to the evening's table:** the ERJ-L06
    series the 2021 BoM used for R18 (ERJ-L06KF50MV) is 0.25 W by Digi-Key's
    listing, not 0.5 W; the ERJ-6BW series is 0.5 W, ±1 %, 200 ppm/°C, same 0805
    footprint: ERJ-6BWFR020V 20 mΩ (P.02AQCT-ND, $0.63 at 1, $0.374 at 10,
    41,559 in stock) and ERJ-6BWFR050V 50 mΩ. Proposal, Andy to pick: (1) one
    line, all four 20 mΩ, full scale 5 A, LSB 76 µA (153 µA bipolar on V_LI),
    0.18 W at a 3 A burst; or (2) two lines, 50 mΩ on V_SOLAR_IN (2 A full
    scale, LSB 31 µA on the charge current, 0.11 W at 1.5 A) and 20 mΩ on the
    other three. V_PRIME takes 20 mΩ either way, since Andy wants telemetry
    possible on it (3 A on 50 mΩ would be 0.45 W). **R51:** Table 5-1 maps the
    pull-down to the address: 0 Ω (tie to ground) 0x10, 499 Ω 0x11, 806 Ω 0x12,
    1.27 k 0x13, 2.05 k 0x14, 3.24 k 0x15, 5.23 k 0x16, 8.45 k 0x17, 13.3 k
    0x18, 21.5 k 0x19, 34 k 0x1A, 54.9 k 0x1B, 88.7 k 0x1C, 140 k 0x1D, 226 k
    0x1E, tie to VDD 0x1F; latched at power-up. 0x10 is free on the on-board
    segment, read from the strapping: VEML6030 ADDR to 3V3_AUX gives 0x48,
    PCA9634 A6..A0 = 1010010 gives 0x52, MCP23018 ADDR to ground 0x20, MB85RC
    A2..A0 = 000 0x50, BME280 SDO high 0x77, MLX90393 A1A0 = 00 0x0C, DS3231
    0x68, BMA456 0x18 or 0x19 (its SDO pin is not in the Eagle pin list); the
    registry's 0x10–0x1F row holds only the PAC itself and a VEML6030 strapped
    low, which Okapi's is not (this strapping answers #29's item 1 for six of
    its seven chips). `pacFind()` scans 0x10–0x1F, so any row works: R51 = 0 Ω
    now (a jumper line in B1), or drop R51 and tie ADDRSEL to ground in v0.7.0
    copper (B8, if Andy wants the line gone). Firmware follow-up (B7): the
    current constants `Okapi.cpp` 182 and 239 say "waits on the shunt value".
    **Decided 2026-11-05.** Andy: the PAC1934 asleep is a tenth of the board's
    floor, so current metering is kept as Bobby laid it out. Values, from a
    blank slate (no 2024 board was ever built): R72, R73, R75 = 20 mΩ
    ERJ-6BWFR020V (P.02AQCT-ND); R74 = 50 mΩ ERJ-6BWFR050V (P17581CT-ND), the
    line shared with #32's restored charger sense resistor; R51 = 0 Ω
    RC0402JR-070RL (311-0.0JRCT-ND), address 0x10. The 0.5 W ERJ-6BW series
    rather than the 0.25 W ERJ-L06: a 3 A burst on 20 mΩ is 0.18 W. All five
    are field edits in B1; the firmware constants follow in B7. The sleep-floor
    itemization (about fifteen parts from their datasheets) stays with #31.
A4. **Consolidation decisions** from `parts-audit.md`. Decided 2026-11-05:
    package merges filed as Project-Okapi #33 (R69, R71 to 0402 now; R1, R8 now and
    R5, R7 with #22; R49/R50 keep their 0.1 %: divider legs behind JP6/JP7; R48: **decided
    2026-11-06, 1 kΩ 0402 (RC0402FR-071KL, R12's line)**, after reading the LM4040
    (D6, 2.5 V shunt reference, 60 µA minimum, 15 mA maximum, 0.3 Ω dynamic
    impedance): the pin's only loads are the DAC's buffered reference input and
    whatever a user wires to J2's VREF terminal, and with load cells ruled out
    (they arrive on their own bridge ADC) the heaviest plausible load is a
    potentiometer, so the pin promises 2 mA and R48 drops from 7.6 mA to 2.5 mA
    for the whole awake time (POWER_EN is up for every logging cycle). Andy's
    rule for it: pads that take an 0603 or an 0402, the BoM item 0402, so a
    user who wants more current can hot-air a 330 Ω 0603 onto the same pads;
    documented in the README's pinout as "VREF supplies up to 2 mA"; filed as
    Project-Okapi #36 (dual pads, a millimeter right of C31, silk, README). Also
    found: POWER_EN enables both aux rails at once, filed on #31 for the next
    board; C1/C18 both 0603,
    decided 2026-11-05, an X7R 16 V part for the 5 V rail; R69, R71 to 0402 confirmed). **R19 to 100 kΩ: decided** (the
    pull-up on Q3's gate, no specification binds it; checked). **C40, C41 to the TDK
    0402 12 pF of C23/C24 and C42 to an 0402 1 µF: decided** (0603 numbers on 0402
    pads). **R62**: Andy's interval choice (JP8's second TPL5111 period; 330 k is
    out of range, 100 k gives 36 min on an existing line, 130 k would copy R20).
    All of these ride in B1 as field edits except #33's footprint changes.
A5. **Items 1 to 4 below** (SENSOR_INT, the MCU watchdog, R62, the V_SOLAR_IN
    airwire) and the review issues that change behavior (**#22 checked 2026-11-05
    against both datasheets: the TLV61220 half is not a defect, R5 = 180 k is the
    datasheet's own example value and its rule is R2 < 500 k (divider current 2.8 µA
    against a 10 nA FB current); the TPS62822 half is a documented trade, R7 = 180 k
    against the datasheet's "R2 ≤ 120 k for 5 µA in the divider", chosen for light-
    load efficiency, with C6 = 68 pF exactly the datasheet's 12 ms / R2. Options:
    keep, or R7 100 k with R6 453 k and C6 120 pF for noise robustness at a small
    light-load cost. **Andy, 2026-11-05: keep as is; the trade is written into the
    Okapi README under "Regulator feedback dividers"**; #22 closes on his word**; **#20 checked
    2026-11-05: VIN_REG = 2.7 V × (1 + 143/100) = 6.56 V matches the Vmp Voltaic
    publishes for the P106 the README recommends (6.5 V, Voc 7.7 V); resellers list
    6.0 V / 7.0 V for the P106C tough variant, and the P106 is end-of-life. The
    setting is a panel choice, erring high is the safe side (the charger throttles
    early rather than collapsing the panel), and 6.0 V would be R69 = 118 k or R22 =
    122 k. **Closed 2026-11-06 on GitHub, with the comment; #22 closed the same day.** Andy: R22 and R69 are "replaceable"
    items to be customized per panel. On the board they are 0603 on the top side at
    (136.8, 170.3) and (134.8, 170.3) mm, 2.0 mm apart in a row with R71 and R70
    (the SHDN divider), nothing taller than an 0805 within 4 mm and the mounting
    hole H2 at 4.8 mm, so a swap with an iron is easy as built. To make it easier
    on v0.7.0: keep them 0603 (so R69 leaves #33's 0402 merge), label the pair on
    the silk ("MPPT: R22 top, R69 bottom; see README"), and the README's power
    section carries the table of values per panel. The alternative that needs no
    iron, a three-pad solder jumper choosing between two bottom resistors (100 k
    for 6.5 V, 118 k for 6.0 V), is the JP8 pattern and is Andy's to want. Andy,
    2026-11-05, on the picture: R69 and R22 beside the mounting hole are already
    among the easier parts to replace with hot air, and 0603 is the smallest size a
    less-skilled hand should be asked to solder. So: as built, labeled on v0.7.0,
    no pitch change; and a rule for both boards, a part a user is meant to swap
    is 0603 or larger and sits clear of tall neighbors**; **#16
    checked 2026-11-05: not a defect, the MCP23018's GPIO pins are rated to 5.5 V
    (DS22103 absolute maximum ratings); closes on Andy's word**).
    **Added 2026-11-05, found while sizing the PAC1934 shunts: the LT3652 charger
    has no charge-current sense resistor.** In the 2021 design R18 (50 mΩ) sat
    between SENSE (the inductor side, L4) and BAT (V_LI), shared with the INA
    current-sense amplifier U35, and set the charge limit at 0.1 V / 50 mΩ = 2 A.
    The 2024 "CSA layout" commit (677d839) that replaced the INAs with the PAC1934
    removed it and tied SENSE and BAT together on V_LI, so the charger has no
    current regulation: a copper change for the KiCad board, and an issue to file.
    The PAC1934's V_LI shunt R72 sits on the cell side of that node and cannot
    double as the charger's sense resistor without moving the topology.
    **Added 2026-11-05, found while reading the TPL5111: the firmware's Feather
    power-on has the wrong polarity, on both designs.** FEATHER_EN is the gate of
    Q3, a P-channel FET with R19 pulling it to 3V3_CORE; Q3 conducts when the
    expander pulls the gate LOW, putting 3V3 on the TPL5111's DELAY/M_DRV, which is
    its manual power-on (a pulse of at least 20 ms). `Okapi::afterLogEvent()`
    writes `FeatherEN` HIGH "to turn on Feather power": on the open-drain MCP23018
    that releases the pin, Q3 stays off, and nothing happens; the module is only
    ever powered by the timer's own 66-minute expiry. Same circuit in the 2020
    Resnik.sch, so the 25 boards behave this way. Bobby's 2021 original had both
    lines commented out, with "HIGH: turn off battery to feather by default" and,
    at the backhaul, "turn on Feather power //FIX! Needed??", so the deployed
    firmware never drove the pin at all and the polarity reading matches his own
    first comment. Andy, 2026-11-05: the backhaul after N (usually 5) logs "has
    worked" on the existing boards. The reading that fits both: the module is
    powered by the timer alone, and it is powered nearly always, because a module
    that never pulses DONE stays on for the whole 66-minute interval less 50 ms, so
    the backhaul always finds it listening (the README's "16 mA background"). To
    verify on a board: FEATHER_BAT over an hour. **Refined the same evening from
    `Particle_Files/Boron_Test.ino` (2019-07-30; the deployed image is
    `Resnik_Boron_Firmware.bin`, 2020-04-25, which may differ):** the Boron runs an
    ApplicationWatchdog of 90 s, checked in on every serial line it receives, whose
    handler Mayday() pulses WD_DONE low then high ("Cycle VBat if in use"). So the
    cycle Andy saw on the LEDs is: the timer powers the Boron every 66 min, it
    stays on while rows arrive on Serial1, and 90 s after the last line it pulses
    DONE and the TPL5111 cuts its power. With a logging interval under 90 s it
    never goes quiet and stays on; above 90 s it is on about 1.5 min per 66, and a
    "START BACKHAUL" sent while it is off is lost, so the backhaul after N logs
    works only when it lands inside an on-window. The fix is unchanged: FEATHER_EN
    pulsed low by the logger when it has rows to send, and DONE from the Boron
    when sent. The test sketch also pulses RST (the ATmega's reset through Q4)
    every loop once 90 s have passed since boot, which cannot be the deployed
    behavior; the deployed .bin is the thing to read on a board.
A6. **Any nw-cold-silicon build rule** these need, and any copper.

**B. Cheaper model, after A** (specified, with a count as the test):

B1. **The BoM port**: a tool that reads each Eagle part's device technology
    (MF, MPN, DIGIKEY; `Hardware/Okapi.sch`) and writes the KiCad symbol fields,
    then `rebody.py` so the footprints carry them; parity stays 0; the BoM export
    shows a number on every line Eagle has one for. Fix in the same pass the
    eight 330 Ω 0402s to RC0402FR-07330RL / 311-330LRCT-ND, C40/C41 to the TDK
    0402 number, and the value fields of R54, R84 to R87 from their numbers.
B2. **The as-built checks document** for Okapi, as Margay's
    `docs/v3.0-as-built-checks.md`: R26 to R33 first, the 330 Ω size, C42, R19.
    Andy, 2026-11-05: the 2024 design has never been built; the 25 existing
    boards are the 2019/2020 design. So this document is the pre-build checklist
    for the first v0.7.0 run, R72 to R75 and R51 included, and nothing on it has
    an as-built value yet. The firmware's PAC1934 path has not run on hardware.
B3. **Milestones and issue moves** from A1's list; comments in Andy's voice.
B4. **Capacitor line edits** from A4 (the free 12 pF merge now; the rest when
    decided).
B5. **ERC/DRC residue** (items 5 to 8) once Andy says accept, exclude or reroute;
    the stackup block (item 9) once chosen; page cosmetics (item 10) last.
B6. **The release mechanics** of A1 when authorized: tag, notes, draft, as
    Margay's were done on 2026-11-05.
B7. **Firmware, specified 2026-11-05, no board needed to write, a board to accept:**
    (a) Okapi_Library: the backhaul pulses FEATHER_EN LOW for 20 to 30 ms (expander
    port B pin 7, configured as an output) when it has rows to send, instead of
    writing it HIGH, and reads MCUSR at boot (shared with Margay's item);
    (b) the Boron sketch arms its 90 s watchdog on the first line received from
    the logger, not at power-on, and pulses WD_DONE when its transmission is sent;
    (c) a BMA456 driver and the orientation reading (Okapi_Library #12);
    (d) acceptance for (a) and (b) on a board: FEATHER_BAT on when the logger
    backhauls and off otherwise, measured over an hour; the same measurement
    before the fix is the diagnosis (always on, 90 s per hour, or on at backhauls).
B8. **The v0.7.0 board edits now filed and decided:** #32 the LT3652 sense resistor,
    #33 the package merges, #34 remove JP8/R62, #35 the TPL5010, #36 R48 on dual
    pads, #37 the PAC1934's hardware default, the MPPT pair's silk label and README table (#20), the BMA456
    no-connect (done).

**Status of A on 2026-11-05 late: A1 to A4 decided; A5 all items decided or filed
except #26/#31 (the next board's power path, a design conversation for a sitting
of its own); A6 nothing arose. The cheaper model starts at B1.**

**2026-11-06: A3 and A4 closed (the PAC1934 shunts, R48 as #36); #20 and #22
closed on GitHub. #31 split, on Andy's word, into #37 (PAC1934 hardware default,
v0.7.0), #38 (B-SoM 3.3 V regulator, v0.8.0 unless v0.7.0 hosts a B-SoM), #39
(core path buck-boost, v0.8.0) and #40 (separate 5 V boost enable, v0.8.0);
milestone v0.8.0 (#3, "the next power section") created; #31 stays open as the
parent. #26 moved to v0.8.0 with the reset options written in (cold exists, warm wants
a second expander, soft is firmware). A5 is complete. B8 gains #37.**

### Notes for the model doing the B list (Fable, 2026-11-06)

1. **Read before acting:** this file's "Okapi: The plan" and its status lines;
   the planned resistor table at the end of `parts-audit.md`; the `nw-kicad`
   skill for the gate numbers (Okapi: 17 sheets and the board round-trip
   identical, nets 208 of 209, ERC 8, DRC 5/0/0; tolerated unconnected J10
   A8/B8 and U43 pin 5). Run the gates before the first edit to see them pass,
   and after every commit. A number that moves is a regression until shown
   otherwise; do not explain it away.
2. **B1 is a tool, then a run.** Eagle's device technologies live in
   `Hardware/Okapi.sch` as `<technology>` attributes (MF, MPN, DIGIKEY) under
   each deviceset's device; the part's `technology=""` picks which. Use the
   field names Margay's KiCad sheets already use for manufacturer, part number
   and Digi-Key (grep them first; do not invent new names). Write the symbol
   properties, then `rebody.py` so the footprints carry them. Tests: parity 0,
   round-trip identical, and the BoM export shows a number on every line Eagle
   has one for (222 of 376 parts). The value edits ride in the same pass, one
   commit each, from the planned table: R26 to R33, the eight 330 Ω, R19, R54,
   R84 to R87, R51, R72 to R75, R48 (value only; its pads are #36), C40 to C42.
3. **Text editing traps that have each cost a session:** anchors change after
   `kicad-cli pcb upgrade` or `--save-board` (find segments by endpoints, not
   by uuid or line); the file's own decimals (`110.89175`, not DRC's rounded
   `110.8918`); the cwd resets between Bash calls, so every path is absolute;
   never `git add -A` (`Okapi-backups/` is untracked on purpose); a no-connect
   goes on both the sheet and the pad net; the Eagle originals are never
   edited.
4. **Two small corrections on the way:** #32 names the 0.25 W ERJ-L06KF50MV
   and wants ERJ-6BWFR050V (0.5 W); the README's J2 pinout entry needs "VREF
   supplies up to 2 mA; R48 sets it" (#36).
5. **Questions only Andy answers, so ask, do not fill:** R5/R7 to 0402 (the
   last pending row); which module v0.7.0 hosts (decides #38's milestone); the
   TPL5010 interval (#35's DELAY value); the firmware mode for energy
   (snapshot or accumulate, B7). Any threshold or default you pick is a
   proposal stated in one sentence.
6. **Gates on outward acts:** commits are yours, granular, with the
   Co-Authored-By and Claude-Session lines; pushes, closes, tags, releases,
   milestone deletions need Andy's word in the current message and the
   `CLAUDE_ALLOW=` prefix. Issue comments are allowed and are written in
   Andy's voice (American spelling, spaced en-dashes, no em-dashes, the
   Claude Code line and session URL at the end).
7. **Reports:** short answers by default; the closing `**Summary.**` paragraph
   only for substantial work, one paragraph, no list after the rule.

**The order of the B list, and the model for each (Andy, 2026-11-06: start with
Sonnet):**

| Step | Item | Model | Why this order |
|---|---|---|---|
| 1 | **B3** milestones and issue sort: the open issues onto v0.7.0, v0.8.0 or none, from a list Andy approves; the #32 part-number comment (ERJ-6BWFR050V, 0.5 W); the README's VREF line (#36) | Sonnet | GitHub and prose, no KiCad files; it fixes what the later steps are measured against |
| 2 | **B2** the pre-build checklist for the first v0.7.0 run (`docs/v0.7-pre-build-checks.md`, Margay's `docs/v3.0-as-built-checks.md` as the model): R26 to R33, the 330 Ω size, C42, R19, R48, R51, R72 to R75, the MPPT pair | Sonnet | Written from the planned table; nothing to run |
| 3 | **B1** the BoM port: the tool from Eagle's technologies to the KiCad fields, `rebody.py`, then the value edits from the planned table, one commit each | Opus | KiCad text, the gates after every commit |
| 4 | **B4** the capacitor edits in the same pass: C40/C41 to the TDK 0402 12 pF of C23/C24, C42 to an 0402 1 µF part, C1 to an 0603 X7R 4.7 µF beside C18 (Andy, 2026-11-05) | Opus | Same files and gates as B1 |
| 5 | **The unique-parts audit, repeated from the export:** regenerate the resistor and capacitor line counts from the KiCad BoM export for both boards and compare with the planned tables (Okapi 31 resistor lines with R5/R7 pending, 10 capacitor lines; Margay 5 and 5). Any further merge is a proposal to Andy, never applied unasked; user-swappable parts (MPPT pair, watchdog period, R48) stay 0603 or larger | Sonnet | A count against a number already written down |
| 6 | **B8** the filed board edits, least copper first: #33 footprints (R71, R1, R8 to 0402; R5/R7 if Andy says), #37 the SLOW pull-up, #36 R48's dual pads and the move clear of C31, #34 JP8 and R62 out, #32 the charger sense resistor between L4 and V_LI, #35 the TPL5010 (symbol and footprint from Margay's in nw-cold-silicon) | Opus | Copper and footprints; DRC and the round-trip after each |
| 7 | **B5** ERC/DRC residue (items 5 to 8) as Andy rules on each, the stackup block, page cosmetics last | Opus | Judgment on what KiCad reports |
| 8 | **B7** firmware: the FEATHER_EN pulse and MCUSR in Okapi_Library, the Boron sketch's watchdog arming and DONE, the PAC1934 current constants from the shunts, the BMA456 driver (#12) | Opus | Library code with the harness and NW-Sim as the gates |
| 9 | **B6** release mechanics for v0.7.0 when Andy authorizes: the review, the notes for approval, the tag, the draft | Sonnet | Mechanics, each step gated |

Steps 1, 2 and 5 are Sonnet's; a Sonnet session that reaches step 3 stops and
says so rather than starting on the KiCad files.

**Progress, 2026-11-06 (Sonnet):** step 1 (B3) done. The #32 part-number
comment and the README's "Reference voltage on the sensor port" section
(Project-Okapi 4dee0fc; the pinout has no J2 entry, as it describes the built
v0.4 board) are in. Andy approved the sort in `issue-triage.md` and said he has
nothing yet for a v1.0.0 milestone, so none was created: #3, #13, #14, #19 and
#23 stay unplaced, with #10, #12 and #27. Applied on GitHub: #7, #15, #17, #18,
#21, #24, #28, #29, #30 to v0.7.0 (15 issues there now); #5, #25, #31 to v0.8.0
(7 there); #10 off v0.6.0, which is now empty. Comments posted on #7, #13, #15,
#17, #21, #28, #29. **Andy, 2026-11-06, on reviewing the sort:** #18 moves to
v0.8.0. v0.7.0 keeps everything it holds (14 issues now), and v0.8.0 is the set
of hardware upgrades that come after it; the two stay separate milestones
because v0.7.0 must remain a complete board he can build as a debug baseline
while v0.8.0 is developed (he is not sure he will build it). A version number
tracks the design, so a port alone would not earn a minor bump; he chose to
keep v0.7.0 as the KiCad board with its decided fixes regardless. This also
settles #18 against A4: C40/C41 take the TDK 0402 12 pF number in v0.7.0 (the
part-number slip only), and whether 12 pF suits the 18 pF crystal is v0.8.0's
question. #18 is on v0.8.0 with a comment. His rule for placing an issue:
innocent goes to v0.7.0, possibly needing debugging to v0.8.0, really big to a
later version. By it #3, #14, #19 and #23 went to v0.8.0 (he said do it), each
with a comment; v0.8.0 now holds 12 issues. **#27 closed 2026-11-06 on his word**
(not planned): the TPL5111 is the B-SoM's power timer, not a logger watchdog;
its wiring (EN and VDD on 3V3_CORE, DRVn to U10.ON, DONE = WD_DONE from MS1
GPIOA3 and J9 ADC3, the FEATHER_EN hold-on of SNAS659B 7.5.2.1) is recorded in
a comment on #34, with a pointer from #35. Nothing is left to his word on the
issue sort. Next: step 2.

### Design (can change the board)

1. **SENSOR_INT on the BMA456's INT pin (U43, Sensors page).** The label is alone
   on the pin; ERC's one warning. **Checked 2026-11-05 at Andy's question: no record
   anywhere plans a wake on motion.** The "wake on shaking" reading was mine, from
   the pin's name and the BMA456's feature list, not from Bobby or Andy; the only
   recorded purpose for an accelerometer in the workspace is orientation (pitch and
   roll, read over I2C: QUEUE.md "The accelerometer's three layers", about Apis's
   LIS3DH), and the v0.6.0 notes say only "BMA456 accelerometer". **DONE
   2026-11-05, Andy: U43 is read for the board's orientation when desired, never
   continuously or for impulses; the no-connect is on (Project-Okapi, "the BMA456's
   INT pin is a no-connect"), ERC 9 to 8.** Firmware: none exists for the BMA456
   anywhere in the workspace (Apis's LIS3DH pitch/roll code is the pattern); a
   driver is new work, B-tier from the datasheet, with the Bosch feature-engine
   configuration blob a question to settle first.
2. **DONE 2026-11-05: Project-Okapi #35, a TPL5010 for the logger on v0.7.0, no ATmega
   pin taken (WAKE onto GLOBAL_INT through one FET, DONE through the expander's
   GPA2, RSTn on RESET), RTS/CTS kept for the Particle, Margay's firmware plan
   shared.** The analysis that led there: Okapi has no dedicated
   one; the TPL5111 is the Particle module's power timer and `resetWDT()` pulses
   pin 23, the primary bus switch. **Checked 2026-11-05 at Andy's question: there is
   an indirect chain, and it is the design's intent.** The Particle can reset the
   logger: its RST_TRIG line (FeatherWing pin 9 / M.2 GPIO9) drives Q4, whose
   drain is the ATmega's RESET net, with R54 holding the gate low while the module
   is unpowered. The 2019 Boron sketch uses it: when its 90 s serial-silence
   watchdog fires it pulses RST (resetting the logger) and then WD_DONE (powering
   itself off). So the logger's watchdog today is the TPL5111 waking the Particle
   hourly and the Particle resetting a logger it cannot hear. Its flaws: it needs
   the module present and its firmware right; its grain is the 66-minute wake; and
   as written it fires whenever the logger has printed nothing for 90 s, which for
   any logging interval above 90 s is every wake, a reset an hour on a healthy
   logger (to verify on a board; MCUSR would show EXTRF each hour). Options for
   v0.7.0: (a) a TPL5010 fed on every wake, as Margay, with Margay's route (a)
   firmware (the reset as a wake, resume-into-file) shared; (b) the AVR's internal
   watchdog in interrupt mode, firmware only, waking every 8 s at a few µA; (c) keep
   the Particle chain but make its condition "no DONE handshake from the logger
   within the session" rather than "90 s of silence". **Andy, 2026-11-05:** the
   90 s was meant as a session timeout, to start once the Particle and the logger
   are awake and talking, not from the module's power-on; (b) is out, a few
   microamps being 100 to 1000 times the sleep draw (backup power sleeps at 4 µA);
   (c) the handshake is the better criterion whatever else is chosen; (a) maybe.
   So two items follow: the Boron firmware arms its 90 s clock on the first line
   from the logger (a handshake) rather than at boot, with Mayday's reset then
   meaning "the logger stopped mid-session"; and the TPL5010 question stays open
   for v0.7.0. **Pins, checked 2026-11-05 from the netlist: all 32 of the 1284P's
   I/O pins are on nets.** The two to free are FEATHER_CTS (PA6, D30) and
   FEATHER_RTS (PA7, D31), the UART flow-control lines to the Particle socket that
   no firmware has ever used (`Okapi.cpp` reads only FEATHER_GPIO). A TPL5010 then
   lands as Margay's: RSTn on the RESET net (open-drain, beside the ISP header,
   the button, Q4 and the expander's !RESET), DONE on PA6, WAKE on PA7 (PCINT7, the
   Port A ISR Margay's #61 already plans), fed on every wake and answered on the
   clock's schedule. Cost: the Particle socket loses CTS/RTS, two traces.
   **Inbound messages (Andy, 2026-11-05: the logger wakes the Particle, so both are
   awake while they talk; but a human's instruction reaching the Particle needs a
   way to the logger). Analyzed from the netlist and the code:** the data path
   exists (UART0 TX/RX through R38/R40 to both sockets) and nothing uses it inward:
   the Boron sketch never writes to Serial1, its only cloud entry is
   Particle.function("Reset") which pulses RST, and the logger reads Serial once,
   at boot, for a time stamp (serialTimeSet). Two paths, no new pins: (1)
   synchronous, inside the session the logger opens: the Particle connects, the
   cloud delivers what it queued, the Particle forwards it as lines on Serial1,
   and the logger listens for a few seconds after END BACKHAUL before letting the
   module go; (2) asynchronous, at the hourly wake: FEATHER_GPIO already lands on
   PA5, PCINT5, in the Port A group whose ISR NW_Logger runs for the log button
   (PCINT0_vect, enabled per pin in PCMSK0), so the Particle raising that line
   wakes a sleeping logger with one mask bit and an ISR that reads PINA to tell
   the button from the module; FEATHER_GPIO's meaning changes from "busy" level
   to "attention" edge, which afterLogEvent's 180 s wait must follow. Both need the
   UART framing choice (COBS or the magic preamble, project_uart_framing) and a
   command grammar. **Andy, 2026-11-05: keep the standard handshake; RTS and CTS
   stay the UART's, so either side can wake the other and the logger can be
   rescued through the Particle.** Then the TPL5010 takes no MCU pin: RSTn on
   RESET; DONE through an expander output (a rising edge is all it needs); WAKE
   wired-OR onto GLOBAL_INT (PA4, PCINT4), the MCP23018's INTA, which IOCON can set
   open-drain and active-low: the TPL5010's active-high WAKE pulse drives one
   N-FET that pulls the line low, the ATmega's pull-up holds it, and the firmware
   reads the expander's INTF to tell an expander event from a watchdog wake. One
   transistor, no new pins; RTS/CTS cannot do this because flow control is a held
   level and a wake is an edge, and two push-pull drivers on one net would short.
3. **DONE 2026-11-05: R62 and JP8 go; R20's 66 minutes stays** (Project-Okapi #34).
   The timer's hourly wake is the module's receive window and the session bound;
   the logger's own cadence is firmware through FEATHER_EN. Was: R62 330 k on JP8's
   second position, above the TPL5111's 170 k maximum.
4. **DONE 2026-11-05: not a gap.** The "airwire" is Eagle's own 0.03 mm: in
   Okapi.brd the top-layer trace on V_SOLAR_IN ends at (23.990, 4.188) and the
   LT3652's VIN pad (pin 1, 0.25 mm wide) has its connection point at (24.021,
   4.188), and Eagle draws an unrouted-layer wire between the two because a wire
   must reach the pad's origin to count. The trace end lies inside the pad's
   copper, so the fabricated copper is continuous, and KiCad, which connects by
   overlap, reports the net complete (unconnected 0, with every Eagle wire present
   per the comparison). Nothing to route; the audit's "never routed" was Eagle's
   bookkeeping. Was: a layout change for the laptop.

### ERC residue (accept, or exclude in the GUI)

5. **Eight warnings that are the design, not a fault.** (a) The converters' switch
   nodes (U1, U2, U3 SW, typed power input by the import): passive, or left.
   (b) Five warnings where two switches feed one rail by design (U21 and U22 on
   V_HP, U17 and U18 on VBUS_SEC, U19 and U20 on VBUS_PRIME): accept them, or an
   ERC exclusion each.

### DRC residue (what the fabricated board carries; accept, reroute, or exclude)

6. **Two B.Cu tracks under S5's bottom restrict** (V_PRIME and V_PRIME_SENSE at
   (161.9, 162.9) mm). Eagle carried them through Bobby's own restrict. (a) Reroute
   the two tracks around the switch. (b) A DRC exclusion each, in the GUI, if the
   restrict was precautionary. (c) Drop the restrict from the package.
7. **The floating GND island, 46 mm2 at (142 to 153, 128 to 137) mm on B.Cu,**
   between U2, U33 and the LED column, with no via or track into it; Bobby's
   Gerber carries the same piece at 45 mm2. (a) A stitching via. (b) Remove it (a
   zone keepout or a smaller zone). (c) Leave it, as the built boards are.
8. **Two dangling track ends** (V_LI at (117.4, 154.7) mm, 3V3_AUX at
   (127.1, 127.4) mm on B.Cu, 0.4 and 0.25 mm long). Delete the stubs, or leave.

### Standards (a default set once, for every board)

9. **The two-layer stackup** (KICAD-TODO step 5). Eagle's DRU names no copper or
   core thickness, so the values are a choice: (a) KiCad's default two-layer
   stackup for a 1.6 mm board (0.035 mm copper, 1.51 mm FR4 core), JLCPCB's
   standard 1 oz build. (b) No stackup block, as now; nothing checks it.
10. **The page cosmetics, held on 2026-11-04** ("functional first, cosmetic later"):
    Bobby's dashed sub-dividers inside the Okapi pages, and the order of things
    within each page, which Andy said he would set himself. The pages are at the
    relevance order of stage 17 (Project-Okapi 95668fe).

## Margay

### Design (can change the board)

11. **THERM_SENSE: DONE 2026-11-04.** The v1.0 thermistor divider's label, alone on
    PA1 since 8454dbc (2018-09-10). Andy: no v0.0 or v1.0 board is in service;
    remove. Margay_Library 2a0eb69 drops the thermistor path (getTemp() branch,
    tempConvert(), the Steinhart-Hart constants, ThermSense_Pin, the model < 2.0
    branches, the Page 2 0x4B write that published a floating pin on a v3): flash
    73040 to 71528 and RAM 3640 to 3561 on Programmed_Margay, of which the
    Steinhart-Hart evaluation alone (log, pow) was 1000 B. Project-Margay: PA1
    no-connect and the pad's unconnected net; README rows. ERC 1 to 0, parity 0.
12. **Three copper gaps: DONE 2026-11-05** (Andy: "Find out the cause ... Once all
    issues are found: fix KiCad's version"). The cause of each, verified:
    (a) **BT1's two + pads** were the conversion's one omission on either board:
    Eagle's device maps the holder's + pin to both pads with `route="any"`, the
    import made two pins and two pads, and KiCad asked for copper between springs
    that are one piece of metal. Fixed in the library (nw-cold-silicon ca48709:
    PAD_SAME_NUMBER, PIN_DROP and the footprint's duplicate_pad_numbers_are_jumpers
    yes, which is what KiCad 9+ needs; net-tie groups and same numbers alone do
    not do it, tested) and both boards re-bodied (Margay, Okapi 8c4ee82; rebody.py
    now carries the flag, NW-Tests be621bb). (b), (c) **VSWITCH_CTRL and WD_HOLD**
    were not the conversion's: DRC on the first import (5bab1ac) and on the board
    before b82f7d8 finds only BT1, and a wire-by-wire comparison of Eagle's copper
    with the first import finds every one of 1443 wires and 120 vias present (the
    one curved wire, a 0.1 mm corner on 3V3_FTDI, became two straight segments);
    all 44 wires absent today left in the June 2026 D4/C20 rework. Both rejoined on
    B.Cu as parallel staircases between ISP1's pads 1 and 2 at 6 mil clearance
    (Project-Margay, "the June reroute finished"). The scan for the same failure
    mode: every one-pin-many-pads part in both Eagle schematics (MOSFETs, BME280,
    USB-C, the combo headers, Okapi's QFNs) has copper to all its pads on its
    board; only the coin holders rely on the part's metal. Counts now: Margay DRC
    1 (Eagle's 0.11 mm VBAT_SW stub) / unconnected 0 / parity 0, ERC 0, Eagle nets
    72 of 75; Okapi DRC 5 / 0 / 0, Eagle nets 208 of 209, the one difference BT1's
    second pin that KiCad no longer has.
### Firmware, found 2026-11-04 while checking the watchdog resistor

12a. **DONE 2026-11-05 (Margay_Library 63bbec9, NW_Logger 0d29627 and 000ffce): the period is set by model, 3853 s for v3.0 and 2110 s for v2.x; the harness shows 3600 s holding at the first and no step holding at the second.** The finding as recorded: the firmware's watchdog period was v2.2's, not v3.0's. `Margay.cpp:59` sets
    `wdtSeconds = 2110` "from R10 = 100k", read in October from
    `Local-Project-Margay/Hardware/Margay.sch`, a 2021-02-20 checkout. Project-Margay
    itself has had R10 = 130 kΩ since Andy's 755ffd9 (2022-05-02, "~65:47 WDT ... 1 hour
    logging intervals"), and both 2023 production BoMs carry RC0603FR-07130KL, so every
    v3.0 board's period is 3854 to 4033 s (Equation 1, 1 % resistor), 3943 s nominal.
    Consequences: the library refuses a 3600 s interval that a v3.0 keeps with 254 s
    of headroom; Project-Margay#60 asks v4 for the 130 kΩ that v3.0 already has
    (QUEUE.md "schedule's open items" 2, marked DONE, rests on the same stale read);
    v2.2 boards (100 kΩ, 2110 s) do need the lower value. Options: (a) 3853 in the
    constructor and the v2.2 boards' 2110 provisioned through Page 1 0x30, which
    exists for this; (b) the reverse. Then amend #60 (gated: a comment is outward).
    Route (a) of the watchdog-as-wake plan (MARGAY-TODO 3) is unchanged by this.

### Issues already filed

13. **Project-Margay #62**: four BOM fields where the footprint disagreed with the
    symbol (R7, R9, R23, U13); the parity check's four items. **#63**: C20 and D4,
    added on the KiCad side on 2026-06-01 and absent from the Eagle files; the net
    check's three differences.

    **The Eagle side of #62 was settled on 2026-11-04 in the CV session**, from a
    v3.0 board Andy measured (R7 = R9 = 330 Ω, R19 = 100 Ω, sleep 1.6 µA): eleven
    local, unpushed commits on Project-Margay master after 8a28592 (c5e6a32 to
    6920e9c, verified in git) put R7 and R9 at 330 Ω (RC0402FR-07330RL, as before
    Bobby's 904d985 relabel), R19 at 100 kΩ, U13 at the MAX6070BAUT18 (grade B
    stays; grade A is #64), and C13/C14's manufacturer at Taiyo Yuden. Tag
    v3.0.0-rc.1 sits on 8a28592, the design as Caltronics built it (50 boards, UMN).
    **Ported 2026-11-04 (Andy: "Make the updates and ensure that the proper part
    number is printed to the BoM")**: R19 RC0402FR-07100KL / 311-100KLRCT-ND on
    symbol and footprint (Project-Margay fc29ee4), U13's footprint MAX6070BAUT18+T /
    MAX6070BAUT18+TCT-ND (2265994), C13, C14, C20 Taiyo Yuden (b6e127a), R23's
    symbol MPN without the CT-ND suffix (00f4534). `kicad-cli sch export bom` with
    fields Reference, Value, Footprint, MF, MPN, DIGIKEY prints R19 as RC0402FR-07100KL.
    Parity 4 to 2; the two left are R7 and R9. R23 itself is a KiCad-side choice of
    Andy's (42cc7cf, 2026-06-01: Bourns CRT0603-BY-1002ELF 0.1 % on the battery-sense
    divider, where Eagle has Yageo RC0603FR-0710KL), kept with the updated KiCad v3.0.0.
    **R7 and R9 decided 2026-11-04 (Andy, after the history: 330 Ω was v1.0 to
    v2.1, Bobby's 904d985 set 1k with the 330 Ω MPN override left in place, every
    build since carried 330 Ω, the ALog BottleLogger uses 1K, either works):** 330 Ω,
    the value that shares a BoM line with the LED resistors (Project-Margay c872856;
    parity 2 to 0). **R19 100 kΩ to 10 kΩ** the same day, Andy's choice from the
    unique-parts review: Q2's gate pull-up carries current only on USB (0.33 mA at
    10 kΩ), and the change removes the board's only 100 kΩ part (d76c9bb; a design
    change from Eagle v3.0, which keeps 100 kΩ). Resistor lines 8 to 6: 27, 330,
    5.1k and 10k in 0402, Bourns 10k 0.1 % and 130k in 0603. The 130 kΩ (R10) sets
    the TPL5010 interval at 3943 s by Equation 1 of SNAS651A; no other value on the
    board gives a usable interval (10 kΩ is 7.6 s, two 10 kΩ in series 52 s), and
    the datasheet asks 1 %, which the Yageo part is.
    **Decided by Andy, 2026-11-04:** "v3.0.0 will be the converted and then updated
    KiCad version. We can produce rc.2 before production and confirm after
    production." So D4, C20 and the oval USB-C slots stay in v3.0.0, #63's three net
    differences are the design and the gate's 72 of 75 is the intended figure; the
    KiCad board is tagged rc.2 before the next run and v3.0.0 once a built board
    confirms it (each tag on Andy's word at the time).

### Version numbers, settled 2026-11-04

A trace change that the firmware must know about takes at least a minor bump,
because Page 0 carries the hardware version as major.minor only and that byte is
the only way firmware can tell two boards apart. NW-Registry already names the
50 built boards "Margay 3.0.0" (board type 0x4D03), so 3.0.0 stays theirs and
carries no electrical change. Wiring the TPL5010's WAKE to PA7 (#61) adds a
capability that old firmware ignores: a minor bump, 3.1. Andy, on the clean
numbering (rc.1 to v3.0.0 for the built boards; the KiCad board with D4, C20
and WAKE as v3.1.0, run as its rc.2): "Great ... Good points all around", and
asked for it in Issues with v3.0.0 and v3.1.0 milestones. This amends the
earlier "v3.0.0 will be the converted and then updated KiCad version" under
item 13. The sequence Andy confirmed later that evening ("Precisely. Correct.",
to the CV session): v3.0.0-rc.1 the 2023 boards as built; v3.0.0-rc.2 the same
copper with the corrected part numbers, built from Margay_BoM_3v0_-_2026-11-04.csv;
v3.0.0 once an rc.2 build confirms; the KiCad board v3.1.0, first prerelease
v3.1.0-rc.1. Milestones on Project-Margay: v3.0.0 (created 2026-11-04), v3.1.0
(existing, rewritten: the KiCad board), v4.0.0 (existing: the larger changes).

## Both boards: housekeeping, each a sentence from Andy

16. **DONE 2026-11-05.** Project-Margay v3.0.0-rc.2 released (tag 299f9de on 76849ad,
    normal release, Latest; Zenodo 10.5281/zenodo.23971433 under concept 3766638,
    minted on the release event, the 409s in the hook log being the duplicate
    created/published deliveries). CITATION.cff was 3.0.0-rc.2 at the tag and is
    3.0.0 on master (a995a55, local, the date left at rc.2's until the release).
    v3.0.0 exists only as a GitHub draft, no tag, notes marked placeholder, to be
    published once a reworked board (U13 MAX6070BAUT18, R19 100 kΩ) passes the
    as-built checks. Andy's plan, 2026-11-05: prepare and bypass the bench so
    development continues; the draft rather than a tag so nothing irreversible
    names an untested state.

## Resolved as fabricated on 2026-11-04 (the record)

The fabricated board is the reference; each line says what was done.

- **U3's nine thermal pads, ring 1 mil in the package:** Eagle's restring rule in
  the library build, every through-hole pad at the ring Eagle fabricates
  (nw-cold-silicon e747648; Okapi 6911cdf). annular_width 9 to 0.
- **USB2's shell** (mask bridges 12, hole clearance 4, shorting 3, clearance 9,
  unconnected 3): Eagle's package draws each slot as two plated holes joined by a
  copper bar; in the library each pair is one pad with the bar as its primitive,
  the symbol has three unconnected shell pins, the footprint allows one mask
  opening (nw-cold-silicon 38f98b3; Okapi "the micro-USB shell as Eagle built
  it"). Every item gone, no rule needed.
- **Silkscreen** on both boards (Okapi 333, Margay 245): Bobby's Gerbers print
  the references over pads and the outlines over the edge, and the fab clips silk
  over copper; the five silk and text checks are set to ignore (Okapi 9fcdf0c,
  Margay 5ac35ce).
- **Hole-to-hole and copper-to-edge**: Eagle's DRU values (6 mil, 15 mil) in both
  projects; neither finds an item.
- **The USB-C's own holes** (4 on each board): a rule naming J10 or J4 and the
  measured 0.18 mm (Okapi 2289f04, Margay 149734d).
- **Margay's RST via**, 0.146 and 0.152 mm from C20's pad and a MOSI track: a rule
  at 0.14 mm (149734d).
- **Every undriven power pin and open pin** on both boards: not a decision after
  all; typed by datasheet in the library or flagged from ERC's report (CHECKS-TODO
  ERC items 3 to 6).

Counts after all of it: Okapi ERC 9, DRC 5, unconnected 0, parity 0; Margay ERC
1, DRC 5, unconnected 3, parity 4.

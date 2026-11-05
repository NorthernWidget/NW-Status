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
    0.4.0, "formerly Resnik") keep their tags v0.4/v0.5.0; their silk's "v1.0" is
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
A3. **R72 to R75 and R51** (PAC1934 shunts and address select, #21): values from
    the PAC1934's range and the expected currents; a datasheet decision.
A4. **Consolidation decisions** from `parts-audit.md`. Decided 2026-11-05:
    package merges filed as Project-Okapi #33 (R69, R71 to 0402 now; R1, R8 now and
    R5, R7 with #22; R49/R50 keep their 0.1 %: divider legs behind JP6/JP7; R48 stays
    0603 or becomes 1 kΩ 0402 on the existing line, Andy to pick; C1/C18 both 0603,
    decided 2026-11-05, an X7R 16 V part for the 5 V rail; R69, R71 to 0402 confirmed). **R19 to 100 kΩ: decided** (the
    pull-up on Q3's gate, no specification binds it; checked). **C40, C41 to the TDK
    0402 12 pF of C23/C24 and C42 to an 0402 1 µF: decided** (0603 numbers on 0402
    pads). **R62**: Andy's interval choice (JP8's second TPL5111 period; 330 k is
    out of range, 100 k gives 36 min on an existing line, 130 k would copy R20).
    All of these ride in B1 as field edits except #33's footprint changes.
A5. **Items 1 to 4 below** (SENSOR_INT, the MCU watchdog, R62, the V_SOLAR_IN
    airwire) and the review issues that change behavior (#22 at least; **#20 checked
    2026-11-05: VIN_REG = 2.7 V × (1 + 143/100) = 6.56 V matches the Vmp Voltaic
    publishes for the P106 the README recommends (6.5 V, Voc 7.7 V); resellers list
    6.0 V / 7.0 V for the P106C tough variant, and the P106 is end-of-life. The
    setting is a panel choice, erring high is the safe side (the charger throttles
    early rather than collapsing the panel), and 6.0 V would be R69 = 118 k or R22 =
    122 k. Keep unless the standard panel changes; closes on Andy's word**; **#16
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
B3. **Milestones and issue moves** from A1's list; comments in Andy's voice.
B4. **Capacitor line edits** from A4 (the free 12 pF merge now; the rest when
    decided).
B5. **ERC/DRC residue** (items 5 to 8) once Andy says accept, exclude or reroute;
    the stackup block (item 9) once chosen; page cosmetics (item 10) last.
B6. **The release mechanics** of A1 when authorized: tag, notes, draft, as
    Margay's were done on 2026-11-05.

### Design (can change the board)

1. **SENSOR_INT on the BMA456's INT pin (U43, Sensors page).** The name says Bobby
   meant to route the accelerometer's interrupt to the MCU; on v1.0 it reaches
   nothing (ERC's one warning). (a) A no-connect flag: open on this revision, one
   line. (b) Keep the label as a note of intent and accept the warning. (c) Route it
   on the next board: an issue, not an edit here.
2. **A hardware watchdog for the MCU on the next board.** Okapi v1.0 has none: the
   TPL5111 is the Particle module's power timer (QUEUE.md, "Corrected 2026-10-30"),
   and `resetWDT()` pulses pin 23, the primary bus switch. (a) Add a TPL5010 fed by
   `resetWDT()`, as Margay has. (b) The AVR's internal watchdog only, and
   `resetWDT()`/`WDHold` fixed in Okapi_Library so they do nothing. Either way the
   firmware fix is its own item.
3. **DONE 2026-11-05: R62 and JP8 go; R20's 66 minutes stays** (Project-Okapi #34).
   The timer's hourly wake is the module's receive window and the session bound;
   the logger's own cadence is firmware through FEATHER_EN. Was: R62 330 k on JP8's
   second position, above the TPL5111's 170 k maximum.
4. **The V_SOLAR_IN airwire** (KICAD-TODO step 9): the audit found the net
   unrouted. A layout change, on the laptop with the board in front of you.

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

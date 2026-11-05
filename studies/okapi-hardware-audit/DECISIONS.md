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
3. **R62, 330 k on JP8's second position, above the TPL5111's 170 k maximum**
   (unfiled item 10). (a) 130 k, the same 3943 s as R20. (b) Another in-range value
   for a second interval. (c) Drop the jumper position. BoM and schematic.
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
12. **Three copper gaps, traced 2026-11-05: none is on the fabricated board.**
    (a) **BT1's two + pads** (POWER0 at 148.96, POWER1 at 133.72 mm, net VCOIN+):
    the coin holder's two terminals are one piece of metal, and Eagle's board says
    so (`route="any" routetag="G$1.+"` on both contactrefs), so no copper joins them
    there either; POWER1's 2.65 mm stub is Eagle's. KiCad does not know the pads are
    joined. Fix in nw-cold-silicon's build: give LINX_BAT-HLD-012-SMT's POWER0 and
    POWER1 one pad number (the PAD_RENUMBER rule) or a net-tie pad group; no board
    edit. (b) **VSWITCH_CTRL on B.Cu**: Eagle has a 7.8 mm diagonal from (30.25, 12.7)
    to (35.76, 7.18) in Eagle's frame; KiCad has no segment between (153.68, 107.51)
    and (159.26, 112.27). (c) **WD_HOLD**: Eagle runs on F.Cu from the via at
    (33.10, 6.35) to (37.74, 5.04); KiCad's via at (156.52, 113.86) reaches nothing
    and the B.Cu run resumes at (158.88, 114.20). Both (b) and (c) sit where D4 and
    C20 were placed on 2026-06-01 (b82f7d8 introduced the geometry at (159.26,
    112.27)), so they are the June rework's unfinished reroutes on the KiCad board,
    v3.1.0 work, and the built v3.0 boards are whole. Two tracks to draw and one
    library rule; the dangling 0.11 mm VBAT_SW stub is Eagle's own.
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

16. **Project-Margay CITATION.cff** says version 3.0.0 and date-released 2023-08-01 at
    the top level and in preferred-citation (read 2026-11-04), while the published tag
    is v3.0.0-rc.1 and v3.0.0 is now the KiCad board after a built-board check. A
    version bump is gated: set it with each release (rc.2, then v3.0.0) on Andy's word
    at the time; .zenodo.json carries no version. Raised by the CV session.
14. **DONE 2026-11-04** (Andy: "in NorthernWidget github"): https://github.com/NorthernWidget/nw-cold-silicon,
    created private (the visibility was not said; one setting flips it) and pushed.
15. **DONE 2026-11-04** (Andy: "push"): NW_Logger, NW-Sim, Okapi_Library, Margay_Library,
    Project-Okapi, Project-Margay, NW-Status, NW-Tests and nw-cold-silicon pushed after the
    verification sequence (style OK on the three libraries, 20 of 22 sketches compile with
    MaxBotix the known failure, 11 of 11 harnesses, the three version failures older and
    elsewhere: T9602, MaxBotix, DS3231_Logger).

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

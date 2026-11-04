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

11. **THERM_SENSE**, a label alone on one pin, Okapi's item 1 again: a no-connect,
    keep the label as a note, or route it on the next board.
12. **Three copper gaps the Eagle board carried**, worth a board in hand:
    VSWITCH_CTRL's two B.Cu tracks that do not meet, WD_HOLD's via and track end,
    the RTC battery pad's 0.25 mm track short of BT1's POWER1. Two are logic lines,
    and a true gap would be a fault Bobby's boards did not show, so something
    bridges them that KiCad does not see, or they are open. Route them, or leave
    them as fabricated (DRC's three unconnected items and five dangling ends).

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
    **R7 and R9 (the UART series resistors, ATmega1284P to FT231X) wait on Andy:**
    he asked for the value to be checked before the schematic goes to 330 Ω. Found:
    330 Ω was the v1.0 to v2.1 value (R7, R10); Bobby's 904d985 (2019-07-19) set
    technology 1K on both in a pass that also changed R15/R16, R10 and R19, with the
    part-level MPN override RC0603FR-07330RL left in place, so every BoM since
    (2v2, 2v3, 3v0) says 1k with the 330 Ω number and the v3.0 board measures 330 Ω;
    the ALog BottleLogger (2018-09-14) uses a 1K network (RN1) on the same lines;
    electrically either value works (10 mA or 3.3 mA into a fault at 3.3 V, RC far
    below any baud rate). Options: (a) 330 Ω on both sides, as built and measured,
    one BoM line shared with the LED resistors. (b) 1 kΩ, the 2019 design intent and
    the ALog lineage, a BoM line of its own and the first build at that value; the
    Eagle commit 292ea53 would be reverted.
    **Decided by Andy, 2026-11-04:** "v3.0.0 will be the converted and then updated
    KiCad version. We can produce rc.2 before production and confirm after
    production." So D4, C20 and the oval USB-C slots stay in v3.0.0, #63's three net
    differences are the design and the gate's 72 of 75 is the intended figure; the
    KiCad board is tagged rc.2 before the next run and v3.0.0 once a built board
    confirms it (each tag on Andy's word at the time).

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

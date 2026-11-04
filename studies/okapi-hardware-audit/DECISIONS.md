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

## Both boards: housekeeping, each a sentence from Andy

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

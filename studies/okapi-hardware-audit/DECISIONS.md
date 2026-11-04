# Okapi: the decisions, held for a sitting with dedicated brainpower

Andy, 2026-11-04: grind through the mechanical items first and keep every real
decision for the end. This is that list. Each entry names the options and what
each costs; nothing here is started until he picks. The mechanical items are in
`CHECKS-TODO.md` and `KICAD-TODO.md` and are being done in order.

## Schematic

1. **SENSOR_INT on the BMA456's INT pin (U43, Sensors page).** The name says Bobby
   meant to route the accelerometer's interrupt to the MCU; on v1.0 it reaches
   nothing. (a) A no-connect flag: open on this revision, ERC 44 to 43, one line.
   (b) Keep the label as a note of intent and accept the ERC warning. (c) Route it
   on the next board: an issue, not an edit here.
2. **A hardware watchdog for the MCU on the next board.** Okapi v1.0 has none: the
   TPL5111 is the Particle module's power timer (QUEUE.md, "Corrected
   2026-10-30"), and `resetWDT()` pulses pin 23, the primary bus switch. (a) Add
   a TPL5010 fed by `resetWDT()`, as Margay has. (b) The AVR's internal watchdog
   only, and `resetWDT()`/`WDHold` fixed in Okapi_Library so they do nothing.
   Either way the firmware fix is its own item.
3. **R62, 330 k on JP8's second position, above the TPL5111's 170 k maximum**
   (unfiled item 10). (a) 130 k, the same 3943 s as R20. (b) Another in-range
   value for a second interval. (c) Drop the jumper position. BoM and schematic.
4. **ERC item 6's residue after the mechanical part.** Done by datasheet and by
   KiCad's own typing: the regulators' and switches' outputs are power outputs,
   every diode, LED, MOSFET and fuse has passive pins, a PWR_FLAG stands where a
   rail enters from a connector or through a passive part. What stays: (a) the
   converters' switch nodes (U1, U2, U3 SW, typed power input by the import):
   passive, or left; (b) five warnings where two switches feed one rail by design
   (U21 and U22 on V_HP, U17 and U18 on VBUS_SEC, U19 and U20 on VBUS_PRIME):
   accept them, or an ERC exclusion each.

## Board

5. **U3's nine thermal pads, ring 1 mil in Bobby's package** (DRC item 5, 9
   annular_width). Eagle's restring rule drew 5 mil, so the fabricated boards
   carry 0.508 mm pads. (a) Eagle's restring rule in build.py for through-hole
   pads (157 pads in 33 footprints), re-body both boards; the library then says
   what was fabricated. (b) Widen the nine pads only. (c) The rule relaxed to
   1 mil for this board.
6. **USB2's six shell slots** (DRC item 7: hole clearance 4, mask bridges 12,
   shorting 3, the 3 unconnected items). The schematic joins them into one net
   the board never routed. (a) No-connects, as Eagle had them, and the pads'
   nets cleared. (b) One copper joining them, as the schematic says. (c) Leave
   it, with DRC exclusions.
7. **325 silkscreen faults from reference texts over pads and each other** (DRC
   items 9 and 10). (a) Hide the references on silk; Bobby's boards print values.
   (b) Move 199 texts. (c) Leave them: the fabricated boards carry them.
8. **The seven connector outlines that hang over the board edge by design** (DRC
   item 6). (a) A DRC exclusion each. (b) Trim the outlines in the library.
9. **The V_SOLAR_IN airwire** (KICAD-TODO step 9): the audit found the net
   unrouted. A layout change, on the laptop with the board in front of you.
10. **The isolated copper island at (148.08, 128.78) mm after the refill**
    (KICAD-TODO step 7). Measured 2026-11-04: a 46 mm2 piece of the B.Cu GND pour
    between U2, U33 and the LED column (x 142 to 153, y 128 to 137 mm), with no via
    or track into it; Bobby's fabricated Gerber (copper_bottom.gbr, 2024-11-02)
    carries the same piece at 45 mm2, so the built boards have it floating too.
    (a) A stitching via into it. (b) Remove it (a zone keepout or a smaller zone).
    (c) Leave it, as the fabricated boards are.

11. **The two-layer stackup** (KICAD-TODO step 5). Eagle's DRU names no copper or
    core thickness (mlCopperThickness and mlIsolate are empty), so the values are
    a choice: (a) KiCad's default two-layer stackup for a 1.6 mm board (0.035 mm
    copper, 1.51 mm FR4 core), which is JLCPCB's standard 1 oz build. (b) Leave the
    board without a stackup block, as it is now; nothing checks it.
12. **Two B.Cu tracks under S5's bottom keepout** (V_PRIME and V_PRIME_SENSE at
    (161.9, 162.9) mm, DRC items_not_allowed 2). Eagle carried them through
    Bobby's own restrict. (a) Reroute the two tracks around the switch, on the
    laptop. (b) A DRC exclusion each, if the restrict was precautionary. (c) Drop
    the restrict from the package.
13. **nw-cold-silicon's home**: public or private, and the push word.
14. **Pushes waiting**: NW_Logger (13 commits), NW-Sim (7), Okapi_Library (10),
    Margay_Library (2).
15. **Project-Margay #62** (BOM fields on R7, R9, R23, U13) and **#63** (C20 and
    D4 on the KiCad side only).
16. **The Okapi dashed sub-dividers** inside pages, as Bobby drew Margay's: add
    them, or not. Held with the rest of the page cosmetics.

## Margay (the same evening; `studies/margay-kicad/CHECKS-TODO.md` has the numbers)

17. **THERM_SENSE**, a label alone on one pin, as Okapi's SENSOR_INT (item 1): a
    no-connect, keep the label as a note, or route it on the next board.
18. **Three copper gaps the Eagle board carried**: VSWITCH_CTRL's two B.Cu tracks that
    do not meet, WD_HOLD's via and track end, the RTC battery pad's 0.25 mm track.
    Route them on the laptop, or leave them as fabricated.
19. **J4's four USB-C pads against the footprint's own holes** (hole_clearance 4): an
    exclusion each, or the hole rule relaxed for this part.
20. **The RST via's two clearances** (against MOSI and C20's pad; C20 is #63's
    KiCad-side part): move the via, or accept.
21. **Silkscreen**, as Okapi's items 6 to 8: J1, J2, J4 outlines over the edge by
    design; references and outlines over pads; U1's thin reference.


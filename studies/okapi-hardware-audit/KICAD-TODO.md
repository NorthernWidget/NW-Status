# KiCad conversion of Okapi: the to-do list, in order (2026-10-30)

From `kicad.md`, the audit of `Project-Okapi/Hardware/KiCAD-10import/` against the
Eagle originals. Each step has an acceptance test; `tools/` holds the scripts the
audit used (`parse_eagle.py` reads Eagle pinrefs, `parse_knet.py` reads a KiCad
netlist export, `compare.py` reports nets exact / lost / fragmented). kicad-cli
10.0.7 is at /usr/bin/kicad-cli. Commit after each step; never squash.

**Start state**: the import (6b6530f) and the power-net fix (faaf72e) are sound.
HEAD (fb54477) deleted 62 global labels on Okapi_3 and lost 54 connections.

1. **DONE 2026-10-30** (Project-Okapi, "restore the 60 global labels"): 168 of
   209 nets exact at the old HEAD, 206 of 209 after, no Eagle pin missing; the
   three left are items 2 and 9 below. **Restore the labels.** Take Okapi_3.kicad_sch's 62 global labels from
   faaf72e; keep the 7 no-connect flags from HEAD; delete only SIM_VCC and
   UB_VBUS, the two that were stray. Acceptance: export the netlist
   (`kicad-cli sch export netlist --format kicadxml`), run `compare.py` against
   the Eagle pinrefs: 206 of 209 nets exact, 0 lost connections, no fragmented
   nets. About an hour, mostly the check.
2. **Redraw the two status-LED wires** at D5 so N$59 reaches GREEN_CATH without
   crossing the RED_CATH pin end (Eagle keeps an explicit netlist; KiCad joins
   by geometry). Acceptance: 208 of 209. Minutes.
3. **Walk every sheet by eye for the same pattern**: wires crossing a pin end
   they should not touch. Start at the 112 dangling and 27 off-grid wire
   endpoints the audit counted. Acceptance: ERC's unconnected-wire count falls;
   the netlist comparison does not get worse. An hour.
4. **Give the footprints a library.** Export the 252 embedded footprints to
   `Okapi.pretty`, add a project `fp-lib-table`, resolve the eight `_528`
   jumper footprint names, run Update PCB from Schematic with re-link by
   reference so every footprint carries a path. Acceptance: DRC schematic
   parity 0, ERC footprint-link errors 0. Half a day.
5. **Carry the design rules.** Default netclass clearance 0.127 mm and track
   0.127 mm, via drill 0.2 mm, from Eagle's `jlcpcb-2layer` set (the project
   has KiCad's 0.2 mm default and an empty `Okapi.kicad_dru`); add a two-layer
   stackup; refill zones; save. Acceptance: clearance errors 499 to 9, all nine
   inside the USB2 connector footprint; confirm by eye that USB2's shell pads
   overlap by design. An hour.
6. **Recreate the two bRestrict keepouts** on B.Cu from the Eagle board, the
   only geometry the import dropped. Acceptance: DRC shows the keepout areas;
   zones refill around them. An hour.
7. **Walk the refilled GND pours** against the Eagle rendering for islands (one
   isolated B.Cu island after refill). Acceptance: no isolated copper, or each
   island explained. An hour.
8. **ERC hygiene.** PWR_FLAG per rail; add the two embedded power symbols to the
   library; clear the `${DISP}` fields; decide whether the 24 local labels that
   carry Eagle global names should be global; exclude U$1/U$2/H1-H3 from the
   BOM; relax the 0.8 mm silkscreen text rule or re-size the text, then check
   silk legibility by eye. Acceptance: ERC down from 622 to the residue you
   accept, listed. Half a day, no connectivity risk.
9. **Decide the Eagle-origin discrepancies** (they are not conversion faults):
   J9 pins 67 and 74 (SIM_VCC, UB_VBUS) and U21/U22 pin 5 (QOD) are connected
   on the board and not in the schematic; V_SOLAR_IN is an airwire that was
   never routed. Each becomes a schematic change, a board change, or a recorded
   decision. Acceptance: DRC parity 0 after the decisions.
10. **Baseline the clean conversion**: commit, tag nothing, record the netlist
    comparison and the DRC/ERC counts here as the numbers every later hardware
    change is measured against.

After step 10 the hardware fixes begin (QUEUE.md, "Okapi hardware audit":
charger RSENSE, PAC1934 resistor values, the SoM 3.3 V regulator, footprints
and crystal caps, MOSFET part numbers, !SHDN re-land, TPL5111 interval resistor,
AREF/AVCC filtering, VCC bypass, the solar input route).

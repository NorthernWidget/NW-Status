# KiCad conversion of Okapi: the to-do list, in order (2026-10-30)

From `kicad.md`, the audit of `Project-Okapi/Hardware/KiCAD-10import/` against the
Eagle originals. Each step has an acceptance test; `tools/` holds the scripts the
audit used (`parse_eagle.py` reads Eagle pinrefs, `parse_knet.py` reads a KiCad
netlist export, `compare.py` reports nets exact / lost / fragmented), with the
scratch-directory paths they ran with. The maintained copies, with every path on
the command line, are `NW-Tests/kicad/` (`check_conversion.sh` runs the three in
one call, `roundtrip.sh` checks that KiCad re-saves a sheet byte-identically),
and the `nw-kicad` skill holds the expected numbers. kicad-cli 10.0.7 is at
/usr/bin/kicad-cli. Commit after each step; never squash.

**Next action (2026-11-02): step 4** against the shared library `nw-cold-silicon`
(workspace repository, local, built 2026-11-02 from the Eagle libraries by its
`tools/build.py`; Andy's two collision decisions are in it), as its own commits
with DRC schematic parity as the gate: fp-lib-table naming `nw-cold-silicon`,
the 338 `Okapi:NAME` footprint fields and 252 board footprint names rewritten to
the library's names (the `_528` jumper suffix dropped; R48 maps to the square
R0603), the footprint path links, then the 88 board net names. Steps 4 to 8 are text work from the tablet, not
laptop work as first written: the board already holds every footprint under its
reference, so re-linking is a footprint-field edit checked by `kicad-cli pcb drc
--schematic-parity`; the netclasses live in `Okapi.kicad_pro` and the stackup and
keepouts in `Okapi.kicad_pcb`; and `kicad-cli pcb drc --refill-zones --save-board`
refills the pours. Only step 9's V_SOLAR_IN route needs the laptop. Method and
scripts: the `kicad-text` skill (`~/.claude/skills/kicad-text`, repository
NorthernWidget-Skunkworks/claude-kicad-text); Okapi's expected numbers: the
`nw-kicad` skill. Two decisions inside step 8 are Andy's: no-connects on SBU1 and
SBU2, and whether the 24 local labels carrying Eagle global names become global.

**Open beside the conversion, pending, not declined** (2026-11-02): the Okapi
thresholds (alkaline red 3.3 to 3.6 V, purple near 3.9 V, solar-online 5 V, the
3.4 V guard; Margay 20 and 50 percent); the grid column groups and the scope of
Okapi_Library#9; the rewrite of Project-Okapi#27 and the correction to #31,
drafted and never posted; the eleven issues in `unfiled.md`; the clock-loss
recovery discussion; the root sheet's two import leftovers (one optional commit).
Local commits unpushed in NW_Logger, NW-Sim, NW-Status, NW-Tests, Okapi_Library,
Margay_Library and Project-Okapi.

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
2. **DONE 2026-10-30** (Project-Okapi, "separate the status LED's green and red
   cathodes"): the fault was a placement collision, R43's top pin end on the red
   cathode's pin end, so R43 moved one grid step left under the green cathode
   with its lead and label, and the joining wire went. 206 to 208 of 209.
   **Redraw the two status-LED wires** at D5 so N$59 reaches GREEN_CATH without
   crossing the RED_CATH pin end (Eagle keeps an explicit netlist; KiCad joins
   by geometry). Acceptance: 208 of 209. Minutes.
3. **DONE 2026-11-01** (Project-Okapi fabcef7 to d345b59, five commits): ERC's
   unconnected-wire-endpoint count 60 to 0 and endpoint-off-grid 27 to 0, the
   netlist 209 of 209 throughout. The ERC JSON put every one of the 87 under
   /Okapi_1/, wrongly, and its position is the wire's connected end, not the
   free one, so each was attributed and diagnosed from the file geometry
   (`NW-Tests/kicad` plus the walk scripts in the session scratch directory).
   The patterns: 59 wires running past the label that names it (trimmed to the
   label, four removed outright); one 2 mm stub above the VUSB junction; GND13,
   GND14 and Q3 a quarter-tick off grid; and the D4 RGB LED block, redrawn as
   D5 was. Open from the walk, for step 8: SBU1 and SBU2 on J10 are single-pin
   named nets in Eagle and now bare pins with a local label each, candidates
   for no-connect flags. Follow-up the same day (7e5a8a3, 492011d, d6aa0d6):
   the D4 and D5 resistor columns widened to 7.62 mm so each reference reads
   beside its own part (Andy's note on the D4 picture), and the D5 anode fed
   straight down from its supply symbol. The walk tools are now
   `NW-Tests/kicad/sch_walk.py`, `sch_edit.py` and `erc_counts.sh`
   (NW-Tests). **Walk every sheet by eye for the same pattern**: wires crossing a pin end
   they should not touch. Start at the 112 dangling and 27 off-grid wire
   endpoints the audit counted. Acceptance: ERC's unconnected-wire count falls;
   the netlist comparison does not get worse. An hour.
4. **DONE 2026-11-02** (Project-Okapi 17df2c4 to the net-rename commit, eight
   commits, each gated on KiCad's re-save returning the board unchanged and
   on the pad-net table by (reference, pad)): the board re-saved by KiCad
   10.0.7 (format only); every footprint reference pointed at the shared
   `nw-cold-silicon` library (ERC footprint links 251 to 0, total 398 to 147);
   Eagle's 2.5 mil mask frame as the board rule; every footprint body replaced
   by the library's (the one pad change on the board: R48's 0603 from 1.0 by
   1.1 mm to the library's 1.0 by 1.0); every footprint linked to its symbol by
   path with the symbol's value and 61 BOM fields; 106 nets renamed to the
   schematic's. DRC 1292 violations (1291 before, one more silkscreen
   overlap), 17 unconnected items as before. kicad-cli's parity check reports
   172 "extra" footprints and 22 net conflicts that are its own limitation:
   the importer made the six sheets six top-level sheets (`top_level_sheets`
   in Okapi.kicad_pro, a KiCad 10 structure) and the CLI's parity walks only
   the first, while the netlist export walks all six. The by-reference link
   and the pin-matched net rename are complete. **Resolved 2026-11-03** (Andy:
   build the better structure): the root sheet re-saved by KiCad (c29b4e5,
   the two import leftovers gone), then one root over six sub-sheets
   (971e900; the former root is Okapi_1.kicad_sch), footprints linked into
   the hierarchy and the 75 open pads given the schematic's unconnected-(...)
   nets. Now: nets 209 of 209, ERC 147, all seven sheets and the board
   re-save identical, **schematic parity 1** (the logo U$4, no symbol), DRC
   1282 violations and 20 unconnected items (three of them ratsnest lines
   among the USB2 shell pads, which the KiCad schematic joins and Eagle did
   not).
   **Give the footprints a library.** Export the 252 embedded footprints to
   `Okapi.pretty`, add a project `fp-lib-table`, resolve the eight `_528`
   jumper footprint names, run Update PCB from Schematic with re-link by
   reference so every footprint carries a path. Acceptance: DRC schematic
   parity 0, ERC footprint-link errors 0. Half a day.
4b. **DONE 2026-11-03, the symbol half** (Andy: replace all components with
   the library's, checking at each batch): `symbol_map.py` measured 377 placed
   symbols against nw-cold-silicon (244 identical in pins and geometry, 2
   differing in pin names only, 6 absent, 125 power symbols); batch A moved
   the 246 (11776ab, nets pin for pin identical); the 6 and the three rails
   as power symbols were lifted into the library (nw-cold-silicon 3b2d109);
   batch B moved the last 131 (f5ae35d) with one difference found and
   rewired: Okapi_3's 3V3_CORE variant had its pin at the symbol origin where
   the library's sits one tick below, so #SUPPLY9 and #SUPPLY10 moved up one
   tick. Okapi-eagle-import.kicad_sym retired (d8d6c7e). Every symbol and
   footprint on Okapi is nw-cold-silicon's. ERC 147 to 112 (CHECKS-TODO items
   1 and 2); DRC 1282, 20 unconnected, parity 0, unchanged.
4c. **DONE 2026-11-03, pages and title blocks** (Andy: KiCad's own place for
   the designer data, standard page sizes; Project-Okapi ffa5859 to 37978d3,
   four commits). Eagle printed a border and a title block from a frame
   symbol; KiCad draws them from a drawing sheet, so nw-cold-silicon now
   holds `nw-cold-silicon.kicad_wks` (5e5ca68), Bobby's FRAME_A_L title
   block on KiCad's default border, and both of Okapi's page-layout settings
   name it through `${KIPRJMOD}`. Each sheet took the smallest A size that
   holds its drawing inside the 10 mm margins and clear of the title-block
   corner (Okapi_1 and Okapi_3 A2, Okapi_2 A3, the rest A4; the import had
   sized each page to its drawing); every sheet and the board carry
   `(title_block (date "2024-11-02") (rev "1.0"))`, the date and the "v1.0
   updates" of the Eagle schematic's last commit b4032d4; the project's text
   variables PROJECT = Okapi and DESIGNER = Bobby Schulz fill the rest.
   Acceptance: `kicad-cli sch export pdf` through the project prints Project,
   Designer, TITLE (the sheet's name), REV, Date, Sheet n/7 and the license
   line on all seven pages; nets 209 of 209, ERC 112, DRC 1282/20/parity 0,
   seven sheets and the board re-save identical, all unchanged. The script
   is `sheet_page.py` (NW-Tests 6f5a503, mirrored in the skill).
4d. **DONE 2026-11-03, the ten thematic pages** (Andy: "Make it so" on layout H
   of `pages.md`; Project-Okapi c79791c to eae24bc, ten commits, one per step). The
   six imported sheets became ten US Letter pages, each one named function, by
   rigid block moves (`sheet_lift.py`, `root_sheets.py`; the plan is
   `tools/pages_build.py`): Power_Input, Core_Supply, Aux_Rails, Microcontroller
   (Okapi_6 renamed), Indicators, Cell_Module, Level_Shifters (Okapi_4), Sensors
   (Okapi_5), Sensor_Ports, USB_ISP_Feather. RST_TRIG became a global label; the
   SDA-jumper note wraps onto three lines; no wire was cut. The three sheets that
   stayed whole kept their uuids. The board followed: footprints re-linked by
   path, 24 nets renamed, pad-net partition identical. At every one of the ten
   commits: KiCad re-saved every sheet identically, Eagle nets 209 of 209, ERC
   112; at the end the printed ink of all eleven pages inside the Letter border
   and clear of the title block, DRC 375, 3 unconnected, parity 0. The repository
   build reproduces the scratch build byte for byte (deterministic page uuids).
4e. **DONE 2026-11-03, the pages organized by section** (Andy: like Bobby's Margay
   pages; Project-Okapi, eight commits after bbe67d7): a heading per theme in Bobby's
   Margay form (5.08 x 4.318 bold), a divider between themes, blocks moved down or
   across by whole ticks under their headings, his notes beside their parts ("To
   Battery Connectors" to the terminals, "Remove PG pullup?" to U2), the mounting
   holes out from under the Feather socket. The plan is `tools/pages_tidy.py`, run
   once on a scratch copy and once on the repository (same result). Checks unchanged:
   every sheet re-saves identically, 209 of 209, ERC 112, DRC 375/3/parity 0, every
   page's ink inside the border and clear of the title block.
4f. **DONE 2026-11-04, Andy's second round of notes** (okapi_2026-11-03_v2-AW.pdf:
   hold font sizes constant, a small label per circuit, expand rather than cram):
   one size per kind on every page (labels 1.27, notes 1.778, fields 1.27; stage 4);
   sixteen content pages, six blocks lifted to pages of their own (Core_Power_Path,
   GPIO_Expander, Level_Shifters_Ports, Analog_Clock_Power, Sensor_Terminals,
   Feather_ISP; stage 5, GLOBAL_INT made global; the board re-linked, parity 0); a
   3.048 mm label for every circuit, 60 of them, seated by a raster search for a clear
   band above (or below) each part, the pages that sat against their headings moved
   down six ticks (stages 6 to 10); `pages_headings_check.py` reports 77 headings and
   labels with zero overlapping ink. The gate at every commit: seventeen sheets re-save
   identically, Eagle nets 209 of 209, ERC 112, every page inside the border. Two
   process slips are in the history (c9581de undid fifteen commits made without a
   per-page gate; 9630d9c re-applied a plan run twice); both are rules in the loop now.
4g. **DONE 2026-11-04, Andy's third round** (the SD card over the edge, a circuit label
   over nothing, collisions above "Pull-ups", "Select address", the RTC's wires, J2's
   leads; "seek to solve general problems instead of tweaking locally"). The general
   fixes, each a stage of `pages_tidy.py` or a tool: the edge rule tightened to 4 mm
   inside the border and every page shifted by the whole ticks its own printed ink
   needs, dividers clipped to the printable area (stage 12); every circuit label
   centered on its part and re-seated by a band search whose column slides by ticks
   when a vertical wire blocks it (stage 13); printed BOM fields and the screw
   terminals' package-name values hidden; `pages_collisions.py` now sees a note over a
   label; `pages_fix_labels.py` judges each candidate against the whole page without
   that one annotation, pushes a label out along its wire with the wire lengthened,
   and nudges notes. Collisions at 30 px or more: 47 before the first fixer pass, 18
   before the second, 3 left (RST on R52, GPIO_1_OUT beside a capacitor's fields,
   RST_TRIG on the Feather socket, each the least-ink candidate). Project-Okapi 1f32fcc
   to 2f22c40.
4h. **DONE 2026-11-04 (evening), the use of space per page** (Andy: "uniform spacing, not
   crowding, grouping by function", then "execute the list"): twenty whole-block moves
   by ticks from the measured ink boxes (stage 14; Project-Okapi b94b6fd), then a third
   fixer pass. Blocks that touched have a gap (Power_Input, Core_Supply), stacks that
   left half a page empty are two columns or a row (Level_Shifters, Sensors,
   Analog_Clock_Power, Sensor_Terminals, Feather_ISP), the ATmega has its clock and reset
   clear of it, C44 is back beside its chip, the battery switch beside the ideal diode,
   Bobby's "USB & ISP" block label gone. Lesson in sheet_lift.py (NW-Tests 7840cce): on
   one page a later rectangle must not cover where an earlier move has just put things,
   and an in-place move keeps the head. Open: the Okapi dashed sub-dividers; the final
   look is Andy's in the GUI.
5. **Begun 2026-11-02**: pad-to-mask clearance 0.0635 mm, Eagle's 2.5 mil stop
   frame, as the board rule (Project-Okapi 96bf37b; the library carries no
   per-pad margins). **2026-11-03**: default netclass at 0.127 mm (9faa2fc), silk text rules at Bobby's sizes (dd3872b), zones refilled and saved (a94ed86): DRC 1282 to 379, unconnected 20 to 3, parity 0 (CHECKS-TODO DRC items 1 to 3). Still open here: the two-layer stackup. **Carry the design rules.** Default netclass clearance 0.127 mm and track
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
8. **ERC hygiene.** The walk, easiest first, with the count each item takes
   off, is `CHECKS-TODO.md` beside this file (ERC 147, DRC 1282, the 20
   unconnected items), written 2026-11-03. PWR_FLAG per rail; add the two embedded power symbols to the
   library; clear the `${DISP}` fields; decide whether the 24 local labels that
   carry Eagle global names should be global; exclude U$1/U$2/H1-H3 from the
   BOM; relax the 0.8 mm silkscreen text rule or re-size the text, then check
   silk legibility by eye. Acceptance: ERC down from 622 to the residue you
   accept, listed. Half a day, no connectivity risk.
9. **DONE in part, 2026-10-30** (Andy: "place the three of them not connected"):
   U21/U22 QOD and J9 pins 67/74 are no-connects in the schematic and their
   board pads carry no net; 209 of 209 Eagle nets exact. **Still open: the
   V_SOLAR_IN airwire**, a layout change for the laptop. Also done the same
   day: the status LED wiring redrawn to Andy's layout (one tick out, right
   angles, mirrored). **Decide the Eagle-origin discrepancies** (they are not conversion faults):
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

## Margay, the same program (2026-11-02)

Project-Margay's `Hardware/KiCAD/` (the KiCad 7 import) went through the
same steps, six commits bf97651 to 7d92919: KiCad 10 format (twice; the
first pass converts, the second settles); references onto `nw-cold-silicon`;
the mask rule; every body from the library (no pad changed; H1 and H2 keep
their circle off the silkscreen because the library took Bobby's later
drawing from Margay.brd); values and 208 BOM fields from the symbols. DRC
399 against 398 at the start, 3 unconnected items throughout, parity 5.
Open: (1) the Eagle netlist check gives 72 of 75 nets exact with 3
differences, before and after: not a conversion fault but C20 and D4, added on
the KiCad side on 2026-06-01 and absent from the Eagle files, filed as
Project-Margay#63; (2) four BOM fields where the footprint disagreed with
the symbol (R7, R9, R23, U13), filed as Project-Margay#62; (3) DONE 2026-11-03: DRC listed the SD slot J1 and the logo as not matching the
library; J1's nine keepout zones had been copied in library coordinates and the logo's
mirrored coordinates rounded to four decimals (rebody.py, fixed in NW-Tests 660405e and
39a2cce); re-bodied (d723fcb, 02dc996), DRC 399 to 397, no mismatches; (4) DONE 2026-11-03: every placed symbol
moved onto nw-cold-silicon in two batches (fc9e682, 82 symbols; f4ecd20, the 34 GND
rails, 6 page frames and J1's SDMMCWR-CRD, lifted as nw-cold-silicon 668ce0d), then
`Margay-eagle-import.kicad_sym` (efb5fae) and `Margay.pretty` (86c2bff) retired; ERC
76 to 50, nets and DRC unchanged; the record is `studies/margay-kicad/symbols.md`.
Flagged there: the library's FRAME_A_L carries no title-block texts, so the pages no
longer printed Project, Designer and REV. (5) DONE 2026-11-03 (d1e067b to a8262f8, four
commits, as Okapi's item 4c): the six frame symbols removed, Margay_1 to _3 on A3 (the
root A4; then all four on US Letter, Bobby's frame size, at 4c5 below), `(title_block (date "2024-11-01") (rev "2.2"))` on the four sheets and the
board (REV from Bobby's frames, the date from the Eagle schematic's last commit 2e755b0),
the project naming nw-cold-silicon's drawing sheet for schematic and board with
PROJECT = Margay and DESIGNER = Bobby Schulz, the importer's empty.kicad_wks removed.
The PDF through the project prints every title-block field on all four pages; nets
72 of 75, ERC 50, DRC 399/3/parity 4, four sheets and the board re-save identical.
(6) DONE 2026-11-03 (aa9fa4f, 3bc8b89): the sheets named as Bobby's headings and paged in his
Eagle order, Digital_Core, Control_Connectors, Power_Sensors (sheet symbols keep their uuids;
the board's 14 sheet-prefixed nets renamed, pad-net partition identical). (7) DONE 2026-11-03
(992e152; Okapi bbe67d7 the same): the logo symbol draws its footprint's silkscreen at twice
the size (nw-cold-silicon f6ed331, every GRAPHIC symbol) and sits in the empty top-right
corner with reference and value hidden; before, it printed its stand-in text over the page
heading.
(4c5) DONE 2026-11-03 (Andy: US Letter, or A4 if it fits; A4 does not, Margay_3's
drawing is 212 mm tall): the drawing sheet's margins 2.5 mm (nw-cold-silicon 0df320b,
Bobby's border sat at the paper's edge), all four sheets USLetter, each drawing moved by
whole ticks onto the page with `sheet_page.py --translate` (NW-Tests ac950c3), the
Margay_3 divider line shortened and H1/H2/U$1 moved two ticks up, clear of the title
block; the printed ink measured inside the border on every page. Checks unchanged.

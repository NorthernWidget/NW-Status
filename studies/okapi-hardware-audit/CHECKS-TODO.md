# Okapi: what ERC and DRC still report, easiest first (2026-11-03)

Measured at Project-Okapi a96a6a8 with kicad-cli 10.0.7 (`erc_counts.sh`,
`pcb drc --severity-all --schematic-parity`, and two trial runs on copies
that are quoted where they change a count). Each item: what it is, what
fixes it, and what the count becomes. Mark an item DONE here with the commit.
Rules of the walk: the Eagle originals are the reference; a change that
alters a pad or a net is its own commit gated on the netlist check, KiCad's
re-save and the pad-net table.

## ERC, 147 (131 errors, 16 warnings); 112 after items 1 and 2 (2026-11-03); 44 after items 3 and 4, 43 after item 5 (2026-11-04)

1. **DONE 2026-11-03**, not by patching: every placed symbol now takes its
   definition from nw-cold-silicon (Project-Okapi 11776ab, f5ae35d, d8d6c7e),
   whose symbols carry DISP as a field and no text; the import library is
   retired. ERC 147 to 112, items 1 and 2 together. **unresolved_variable, 22.** Sixteen `${DISP}` texts in symbol fields (U2,
   U3, U6, U9, U17 to U20, U24 to U27, U29 to U31, U34, U35, U39, U40, U42,
   U43, U45): Eagle's DISP attribute, which the importer turned into a KiCad
   text variable nobody defines. Fix: delete the sixteen field texts (the
   value they displayed is the part number, which the Value field already
   shows), or define `DISP` as empty in Okapi.kicad_pro's text_variables.
   Text edit. 147 to 125.
2. **DONE 2026-11-03** with item 1: the three rails are nw-cold-silicon power
   symbols. **lib_symbol_issues, 13.** The power symbols 3V3_AUX (nine placements) and
   3V3_CORE (four) exist only embedded in the sheets, not in
   Okapi-eagle-import.kicad_sym. Fix: copy the two symbol definitions from a
   sheet's lib_symbols into the library file. Text edit. 125 to 112.
3. **DONE in part 2026-11-04** (Project-Okapi 9ffbd69): SBU1 and SBU2 are no-connects and
   their board pads carry the unconnected names; SENSOR_INT waits for Andy's word. ERC
   46 to 44. **isolated_pin_label, 3.** SBU1 and SBU2 on J10 (USB-C, single-pin named
   nets in Eagle) and SENSOR_INT on U43 pin INT (the BMA456's interrupt,
   one pin in Eagle too). Fix: a no-connect flag at each pin end, the label
   removed or left as a note. Decision: SENSOR_INT's name says Bobby meant to
   route it; a flag says it is open on this revision. Andy's. 112 to 109.
4. **DONE 2026-11-04** (Project-Okapi 3983a5d, `tools/erc_noconnects.py` from ERC's own
   report): 61 flags, USB2's shell net renamed on the board to match; ERC 112 to 46,
   pin_not_driven 6 to 1 with it; DRC 375, unconnected 3, parity 0 unchanged. **pin_not_connected, 61.** Every one open in Eagle as well: J9's 27 unused
   M.2 pins, MS1's 12, U23's six handshake and CBUS pins, SD1's DAT1/DAT2,
   USB2's ID and shell, J8's two pads, U38's three, RTC1's 32KHZ and RST,
   U41's INTB and GPA2, U44's INT, U3's FB, U4's NTC, the three load
   switches' CT. Fix: a `no_connect` at each pin end, placed from the pin
   positions `sch_walk.py` gives; the board pads already carry the matching
   unconnected-(...) nets. Mechanical, one commit. Also clears five of the six
   in item 5. 109 to 48.
5. **DONE 2026-11-04** (nw-cold-silicon b6f9491, build rule PIN_TYPES; Project-Okapi 2d6b034):
   DRVn is an output; ERC 44 to 43. **pin_not_driven, 1 left after item 4.** U8 (TPL5111) pin DRVN drives U10's
   ON (Eagle net N$64) but the imported symbol types it Input. Fix: electrical
   type Output on that pin in the library symbol and the sheet's embedded
   copy. 48 to 47.
6. **power_pin_not_driven, 42.** The importer typed every Eagle "pwr" pin
   Power input and none Power output, so no rail has a driver. Two kinds of
   fix, both judgment per pin: (a) pin types in the library symbols: the
   regulators' outputs (U1 VOUT, U6 OUT, U17 and U19 OUT) to Power output,
   converter switch nodes (U1, U2, U3 SW) and the nine LEDs' anodes and
   cathodes (D10 to D14, D16 to D18, 18 pins), D6, U26 VA, U5's three to
   Passive; (b) a PWR_FLAG on each rail fed from outside the schematic: GND,
   VBUS at J10/J9/MS1, BT1's +, 3V3_AUX and 3V3_CORE if their regulators'
   pins stay inputs, J9's VCC and 3V3. Hardest: 42 pins on about 14 nets.
   47 to a residue of what Andy accepts.

## DRC, 1282 (536 errors, 746 warnings); 375 after items 1 to 4 (2026-11-03); 377 after S5's keepout was made Eagle's (2026-11-04, two tracks under it, DECISIONS 12)

1. **DONE 2026-11-03** (Project-Okapi 9faa2fc): default netclass clearance 0.127 mm, via 0.508 on a 0.254 drill (the board's most used); clearance 499 to 9, all nine USB2's shell pads against tracks (item 7); 1282 to 783. **clearance, 499.** The project has KiCad's 0.2 mm default netclass where
   the board was routed to Eagle's 5 mil (0.127 mm) rules. Fix: default
   netclass clearance 0.127, track 0.127, via drill 0.2 in Okapi.kicad_pro
   (KICAD-TODO step 5). Measured on a copy: 499 to 9, all inside the USB2
   connector footprint. One edit. 1282 to 792.
2. **DONE 2026-11-03** (Project-Okapi dd3872b): min text height 0.4 mm and thickness 0.07 mm, under every reference text Bobby placed (0.53/0.078 mm for 205 of 243, the rest down to 0.42/0.078); both counts to 0; 783 to 385. **text_height and text_thickness, 199 each.** One rule (silk text min
   height 0.8 mm, min thickness 0.08 mm) against every reference text, which
   Bobby set at 0.53 mm. Fix: the rule to his size, or the texts to the rule.
   Decision: the fabricated boards carry 0.53 mm and read fine, so the rule.
   792 to 394.
3. **DONE 2026-11-03** (Project-Okapi a94ed86): zones refilled and saved; via_dangling 0, track_dangling 2, one isolated_copper warning (the island at 148.08, 128.78 mm, step 7), unconnected 20 to 3 (USB2's shell only; V_HP's track end joined through the pour), 385 to 379; re-save identical, pad-net table unchanged. **via_dangling, 6; most of track_dangling, 3; 14 of the 20 unconnected
   items.** Zones are unfilled since the import. Fix: `kicad-cli pcb drc
   --refill-zones --save-board` (step 7). Measured on a copy: vias 6 to 0,
   tracks 3 to 2, unconnected 20 to 3, and one isolated copper island
   appears (the audit's known one, step 7). 394 to about 388.
4. **DONE 2026-11-03** (Project-Okapi 92610e4, aeb1460; Margay d723fcb, 02dc996; NW-Tests 660405e, 39a2cce): two rebody.py defects, found with the pcbnew Python module as the judge (`FootprintNeedsUpdate`). (a) A footprint's zone polygon is written in board coordinates where pads and graphics are local, and the script had copied the library's unmoved, so SD1's two keepouts, U43's and S5's (and Margay J1's nine) sat near the board origin: now mirrored, rotated and translated to the part, layer list masked to the board's copper. (b) Coordinates rounded to four decimals where KiCad writes six and compares exactly, which left the mirrored logo microns off; now six, with the library's descr and artwork attributes on the instance. Mismatches 4 to 0 on Okapi (DRC 379 to 375), 2 to 0 on Margay (399 to 397). **lib_footprint_mismatch, 4.** SD1, U43, S5 and the logo U$4 differ from
   the library in something DRC compares beyond pads and graphics (pads and
   graphics checked equal). Fix: a GUI "update footprint from library" on
   the four says what; U$4 is item 8. 388 to 384.
5. **Measured 2026-11-03:** U3's nine thermal pads are drill 0.254 mm at diameter 0.3048 (ring 0.0254 mm, 1 mil) in Bobby's package; Eagle's DRU (rvPadTop 25 %, rlMinPadTop 5 mil) draws every pad ring at max(25 % of drill, 0.127 mm), so the fabricated boards carry 0.508 mm pads there. The converters took the package's nominal size, and the library holds many such pads (count in the report below). Proposal: apply Eagle's restring rule to through-hole pads in build.py (diameter = max(nominal, drill + 2 x max(0.25 x drill, 0.127))) and re-body; or raise just U3's nine in the library. Andy's call. **annular_width, 9.** U3's nine thermal vias (PAD@1 to PAD@9, GND) have an
   annulus below the 0.0508 mm rule. Fix: the rule to Eagle's (rlMinViaOuter
   5 mil = 0.127 mm would be stricter; read what Eagle actually passed) or
   the pads' size. Step 5 territory. 384 to 375.
6. **Measured 2026-11-03:** 7 are connector outlines (J10 two lines, SD1 five arcs and lines) that hang over the edge by design, 1 is USB2's reference text; KiCad's native answer for the seven is a DRC exclusion each (stored in Okapi.kicad_pro) and for the text a move. **silk_edge_clearance, 8.** SD1, J10 and USB2 outlines over the board
   edge: connectors that hang off the edge by design. Fix: DRC exclusions on
   the eight, or trim the three outlines. 375 to 367.
7. **USB2's shell: hole_clearance 13, solder_mask_bridge 12, shorting_items 3,
   hole_to_hole 2, and the 3 unconnected items that remain after the refill.**
   The micro-USB's six shell slots sit closer than the 0.25 mm hole rules
   and the schematic joins them into one net the board never routed. Fix:
   with Eagle's rules (item 1) hole clearance falls to 4; then either a
   no-connect on each shell pin in the schematic (Eagle had them separate)
   or one copper joining them. Decision, Andy's. 367 to about 340.
8. **DONE 2026-11-03** (nw-cold-silicon f37fd81, Project-Okapi and Project-Margay "the logo is a schematic part"): parity 0 on Okapi, 4 on Margay (#62's fields). **The logo U$4, and the parity check's one item.** Board-only in Eagle and
   KiCad alike, no symbol. Fix: place nw-cold-silicon's NWLOGO_MED symbol on
   the schematic as LOGO1 with the library's artwork attributes (no BOM line,
   no position row, no simulation) and rename the footprint to match. Parity
   1 to 0, and the BOM exclusion for free.
9. **silk_over_copper, 199.** Every reference text sits over a pad somewhere
   ("silkscreen clipped by solder mask"). Fix: hide the references on silk
   (Bobby's boards print values, not references) or move 199 texts. Decision.
   340 to 141.
10. **silk_overlap, 126.** Reference texts over outlines and each other.
    Same decision as item 9: hidden references take most of these with them.
    141 to the residue.

## Unconnected items, 20, a separate item; 3 after DRC item 3 (2026-11-03)

14 on GND and 2 on 5V_AUX join through the pours and vanish when the zones
are refilled (DRC item 3). The remaining 3 are USB2's shell (DRC item 7).
V_HP has one: a track end on the front, to be looked at with the refill.
The audit's V_SOLAR_IN airwire (KICAD-TODO step 9) is not among the 20: the
import carries it as a ratsnest line only when the schematic net exists on
the board, which it does not yet.

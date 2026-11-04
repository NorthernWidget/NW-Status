# Margay: what ERC and DRC still report (2026-11-04)

Measured at Project-Margay eb0e569 with kicad-cli 10.0.8 (`scratchpad/wks/mgate.sh`:
four sheets and the board re-save identically, Eagle nets 72 of 75, the three
differences being Project-Margay#63; parity 4, the fields of #62). Written like
Okapi's `okapi-hardware-audit/CHECKS-TODO.md`, after the mechanical items were done
in the same evening; what is left needs Andy's word and is on `DECISIONS.md` there,
Margay section.

## ERC, 50 at the start of the evening; 1 after the mechanical items

Done 2026-11-04 (Project-Margay 38868b0 to 5f9a38d, nw-cold-silicon b9d62b8 to the
MAX6070 rules): ten symbols' sheet copies refreshed from the library's retyped pins;
16 no-connect flags from ERC's report and the USB-C's SBU labels replaced by flags
(board pads renamed); the ISP header passive and the TPS22916's output a driver;
seven PWR_FLAGs where rails enter; the RGB LED block put on the grid (Eagle's 0.1 mm
placements); six wire tails trimmed, two stubs deleted, two labels snapped to the
grid (`erc_stubs.py`); U13 (MAX6070) typed by datasheet.

Left: **isolated_pin_label 1**, THERM_SENSE, a label alone on one pin: Bobby's name
says he meant to route the thermistor sense; a no-connect says it is open on this
revision. Decision.

## DRC, 397 at the start; 256 after items 1 and 2

1. **DONE** (c71c242): netclass via 0.554/0.3 mm (81 of 119 vias), annular ring
   Eagle's 5 mil; clearance was already Eagle's 6 mil. No count moved.
2. **DONE** (d342098): silk text rules at Bobby's sizes (0.4 mm, 0.07 mm): text_height
   75 to 0, text_thickness 67 to 1 (U1's reference is thinner still). 397 to 256.
3. **DONE, nothing to do** (eb0e569): the zones were already filled; the save pass
   wrote the project's text variables into the board.
4. **unconnected items 3, track_dangling 4, via_dangling 1**: three gaps in the
   copper that the Eagle board carried too: VSWITCH_CTRL (two B.Cu tracks 3.58 and
   1.78 mm long that do not meet), WD_HOLD (a via and a 0.13 mm track end), and the
   RTC's battery pad (a 0.25 mm F.Cu track short of BT1's POWER1). Layout; decision.
5. **hole_clearance 4**: J4's four VBUS and GND pads against the USB-C footprint's
   own non-plated holes, closer than the 0.25 mm board rule. Footprint geometry from
   Eagle; an exclusion each, or the rule. Decision.
6. **clearance 2**: the RST via against a MOSI track on B.Cu and against C20's GND
   pad (C20 is a KiCad-side addition, #63). Layout; decision.
7. **silk_edge_clearance 11, silk_over_copper 199, silk_overlap 34**: J1, J2 and J4's
   outlines over the board edge by design; references and outlines over pads. The
   same decision as Okapi's items 6, 9 and 10.
8. **text_thickness 1**: U1's reference text. With item 7.

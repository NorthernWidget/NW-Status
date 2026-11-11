# Eagle-to-KiCad conversion losses: footprint and board audit

Status: COMPLETE

Agent report, 2026-11-11. Read-only audit of Okapi and Margay: every Eagle package used on each board against its KiCad footprint (library copy in `nw-cold-silicon.pretty` and board instance), then board-level features. Scripts: `2026-11-11-eagle-conversion-losses/`. Layer 46 in `USB_C_CUSB31-CFM2AX-01-X` and `USB_MICRO_VERT_MOLEX` is out of scope (being fixed by another agent).

Classes: (a) fab-affecting; (b) DRC/design intent; (c) cosmetic.

## Log of checks

Scripts (run with `run.sh <workspace> <scratch>`, then `layers.py`, `pads.py`, `instances.py`, `geometry.py` on the JSON):
`inventory.py` (Eagle package from the `.brd` `<libraries>` against the `nw-cold-silicon.pretty` footprint and every board instance, through pcbnew),
`layers.py` (item counts per layer), `pads.py` (pad by pad, matched by position), `instances.py` (each board instance's pads against its library footprint),
`geometry.py` (area and extent per Eagle layer against the mapped KiCad layer, Eagle shapes in shapely, KiCad's through pcbnew `TransformShapeToPolygon`).

1. Packages used: Okapi 70 packages, 252 elements; Margay 37 packages, 82 elements (`inventory.py`). Not on the KiCad board: Okapi JP8 and R62, removed deliberately in Project-Okapi 701f7e7 (#34); their library footprints are still compared. `U$4`/`U$2` are LOGO1 in KiCad.
2. Pads, Eagle package against library footprint (`pads.py`): packages compared Okapi 68, differences 7; Margay 35, differences 0. Checked per pad: kind (pad/smd/hole), position, size after rotation, Eagle's fabricated through-hole size (diameter grown to the DRU restring), drill, oblong drill, shape (square/round/long/offset/octagon; SMD roundness against roundrect ratio r/200), stop="no" against the mask layers, cream="no" against the paste layers (26 pads on Okapi, 18 on Margay, all carried), thermals="no" and first="yes" (neither is used in any package on either board), local mask/paste margins (none). The 7 differences: R48 (R0402_0603, the deliberate dual land of Project-Okapi 4fe12e7) and USB2's three custom shell pads (USB_MICRO_VERT_MOLEX, out of scope). CLEAN otherwise.
3. Board instances against the library footprint (`instances.py`): Okapi 250 instances, 10 differ, every one a deliberate KiCad footprint change in git (C1 5aaf6fd, C22 dfd0f57, R1/R8 4c4c996, R5/R7 9fc83f9 to 0402 or 0603; R22/R69/R70/R71 to R0402_0603 4fe12e7). Margay 82 instances, 1 differs: J4 USB-C, the library already holds the other agent's slotted M1-M4 (drill 1.7/1.2 mm long) and the board instance still the 0.6 mm round drills. Out of scope.
4. Item counts per layer (`layers.py`): every Eagle layer used in a package maps to a KiCad layer except 57 tCAD (see finding C1) and 46 Milling (out of scope, only in the two USB packages on both boards). Mapping found: 1 F.Cu, 16 B.Cu, 21 F.SilkS, 25 tNames and 27 tValues to footprint fields (a tNames circle in QFN24 to F.SilkS), 31 F.Paste, 35 F.Adhes, 39 F.CrtYd, 41 tRestrict and 43 vRestrict to keepout zones, 45 holes to NPTH pads, 49 Reference to User.Comments, 51 F.Fab, 52 B.Fab. Layers 20, 29, 30, 32, 40, 42 appear in no package on either board; no package contains a via.
5. Geometry per layer (`geometry.py`): Okapi 107 layer comparisons, 9 differ by more than 1 % of area; Margay 54, 2 differ. Paste (31), glue (35), keepout (39), restrict (41, 43) all match to 0.0000 mm2 except the USB-C paste (finding A1) and R48 (deliberate). Silkscreen differences remaining are method: KiCad's polygon includes text (AVRISP) and the tNames circle (QFN24), and arc polygonization (4_40, 1.4 %).
6. Copper drawn in packages (layers 1/16): only USB_MICRO_VERT_MOLEX (3 wires each side), folded into custom pads by build.py PAD_RENUMBER. Out of scope.
7. Gerbers, Eagle 2024/2023 fab against `kicad-cli pcb export gerbers` of the current boards (`render_diff.py`, gerbv at 1000 dpi, the KiCad image shifted by the element offset Okapi (116.1261, -172.5036) mm, Margay (123.4286, -120.2056) mm; regions over 0.05 mm2 after a 2-pixel opening, each named by its nearest Eagle pad). Fab references: `Project-Okapi/Hardware/Okapi_2024-11-02.zip`; `Project-Margay/Production/Margay_3v0_2023-08-01.zip` (Margay.brd's last design commit is 2023-03-17, f2cbf69). Method check: all 1062 Okapi F.Mask pads have a KiCad mask flash at their center.
   - Okapi F.Paste: 25 regions only in Eagle, every one a part removed or refitted in KiCad by commit (JP8, R62, C1, C22, R1, R5, R7, R8, R48, R22, R69, R70, R71); 0 only in KiCad. B.Paste empty on both. CLEAN.
   - Okapi F.Cu: every region beside the same deliberately changed parts. CLEAN. B.Cu: one 0.125 mm2 stub near J2 (V_LI), deleted by commit 540a50a; and finding A2.
   - Okapi masks: 341 regions on Eagle vias each side (finding A1); the rest are the deliberate parts and USB2 (out of scope).
   - Margay: every copper, mask and paste difference sits in the June 2026 reroute around ISP1, R2, D4 and C20 (commits 0af2117 and the KiCad additions D4, C20), plus the vias (finding A1). B.Paste matches. CLEAN otherwise.
8. Drills (`drills.py`, Eagle `drill_1_16.xln` against the KiCad merged `.drl`): Okapi and Margay identical in every diameter and position apart from the USB stake holes now slotted (out of scope) and Margay's four vias moved or removed by the reroute. Plated against non-plated per pad: CLEAN (step 2). Note for the USB work: the fab drill files carry the USB-C stakes as round 0.6 mm hits and the CAM zips hold no milling layer, so the 2024 and 2023 fab outputs do not themselves show slots.
9. Board outline (`board_items.py`): 12 (Okapi) and 7 (Margay) Eagle layer-20 segments all present in Edge.Cuts with the same end points; arc midpoints agree within 0.0003 and 0.0004 mm. No layer 20 or 46 item outside packages; no hole outside packages. CLEAN.
10. Polygons against zones: Okapi 16 Eagle polygons, 16 KiCad zones (2 on B.Cu). thermals="no" became solid connection (15 zones), the one thermals polygon a thermal one; rank 1/2/3 became priority 6/4/3 in the same order; no isolate is set. The refilled copper matches the Eagle Gerbers apart from A2. KiCad's minimum width is half the Eagle polygon width on every zone (0.1524 to 0.0762 mm), which moved no copper measurably. Margay has no polygons. CLEAN apart from A2.
12. Full re-run with `run.sh` after the other agent's USB commits landed (Project-Margay 7c55635 and the library): pads Okapi 68 packages, 18 differences; Margay 35 packages, 4 differences; the new ones are all in USB_C_CUSB31-CFM2AX-01-X and USB_MICRO_VERT_MOLEX (out of scope). Margay instances now 82, 0 differing. Every other number above reproduced.
11. Design rules: srRoundness 0 and psTop -1 on both boards, so pad shapes are the library's (checked in step 2); cream frame 0 against KiCad paste margin 0; stop frame 2.5 mil against pad-to-mask 0.0635 mm (set by build.py and the boards, known).

## Findings


### (a) Fab-affecting

**A1. Vias tented in KiCad, open in Eagle (both boards, every via).** Eagle's DRU sets `mlViaStopLimit` 0 mil (Okapi.brd line 3538, Margay.brd line 2204), so every via gets a solder-mask opening. The fab Gerbers confirm it: all 345 Okapi vias and all 120 Margay vias have a mask flash on both sides, the opening 0.635 mm on a 0.254 mm drill (via plus 2 x 2.5 mil). Both KiCad boards set `(tenting (front yes) (back yes))` in their setup, and the KiCad export has 0 of 345 (Okapi) and 0 of 118 (Margay) vias open on either side. Proven (`gerber_vias.py`). Either choice fabricates; covered vias are the more common default, so this is a decision for Andy rather than a fix to make blind. Mask area: Okapi F.Mask 1384.80 mm2 Eagle against 1238.01 mm2 KiCad.

**A2. Okapi bottom GND pour loses its orphan island (42.7 mm2 of copper).** The Eagle polygon at Okapi.brd line 6110 (GND, layer 16, width 0.1524, `orphans="yes"`, `thermals="no"`) keeps unconnected islands; the import set its zone to island removal mode 0 (always remove). The fab B.Cu has a 42.692 mm2 region at Eagle (28.57, 31.67), 7.80 x 7.75 mm, that the KiCad B.Cu export lacks. Refilling a scratch copy with that zone set to keep islands raises its fill from 99.90 mm2 (2 outlines) to 142.56 mm2 (3 outlines): the difference, 42.66 mm2, is the missing region. Proven (`render_diff.py`, `islands.py`). The other 15 Okapi zones have no `orphans` attribute in Eagle, so removing islands is their Eagle behavior too.

**A3. USB-C paste windows slightly smaller (USB_C_CUSB31-CFM2AX-01-X; Okapi J10, Margay J4).** The four tCream polygons (Okapi.brd lines 3428, 3438, 3448, 3458; Margay.brd 2090, 2100, 2110, 2120) have curved vertices; the converter wrote each 90-degree corner as a few chords. Total paste area 7.0062 mm2 in Eagle (arcs evaluated) against 6.9186 mm2 in the library footprint, 0.0876 mm2 (1.25 %) less stencil opening. No region exceeded 0.05 mm2 in the Gerber comparison, so the effect is small. Layer 31, not 46; the package is the other agent's, so this is for them to fold in if they wish.

### (b) DRC and design intent

**B1. Okapi board-level bRestrict polygons dropped (known fault class).** Two plain polygons on layer 42 (Okapi.brd lines 214 and 224): 27.5 mm2 under XTAL1, C40 and C41 (bounds 22.48-30.10, 64.01-69.34) and 60.5 mm2 under L2 (bounds 15.11-22.48, 20.57-28.83). Eagle had no bottom wire or via inside either. KiCad has 0 board-level rule areas. The crystal and the inductor are where a keepout matters (noise under the oscillator, switch node under the inductor).

**B2. build.py rewrites vRestrict as if it were bRestrict (library, not on either board).** Eagle layer 43 is vRestrict (no vias), as both `.brd` files' own layer tables say; bRestrict is 42. `build.py`'s `brestrict()` (comment "Eagle's bRestrict (layer 43)") turns the converter's via-only keepout on all copper into a no-copper keepout on B.Cu. All 6 rewritten zones came from layer 43: HL (1), HC49UP (1), MICROSD_HIROSE_HINDGED (3) and SWITCH_2.6X1.6 (1). PHOTON's true bRestrict zones came through on B.Cu without the rewrite. Verified by converting `Cold-Silicon/bschulz.lbr` afresh with `kicad-cli fp upgrade` into scratch: HC49UP, MICROSD_HIROSE_HINDGED and SWITCH_2.6X1.6 come out as keepouts on every copper layer with only vias not allowed (Eagle's vRestrict, rendered correctly), PHOTON's layer-42 zones come out on B.Cu with everything not allowed. On the boards only SWITCH_2.6X1.6 (Okapi S5) is affected, and KEEPOUT_FIX then sets it to F.Cu with vias not allowed, which keeps Eagle's restriction; its comment's premise ("Bobby's bottom restrict") is wrong, its outcome is not. The three library-only footprints carry a bottom no-copper rule where Eagle meant no vias.

**B3. Wire-drawn restricts dropped by the library converter (library only).** SIM_SF72 in bschulz.lbr draws its vRestrict as six 0.127 mm wires; the library footprint has 0 zones. Not on either board.

Restricts that came through correctly: LGA-12_2X2 (Okapi U43, tRestrict 1), MICROSD_CD (Okapi SD1, tRestrict 2), SD_WURTH_WR-CRD (Margay J1, vRestrict 9, via-only on both copper layers): areas identical to 0.0000 mm2. tKeepout (39) maps to courtyard in every package and on Margay's two board-level circles.

### (c) Cosmetic

**C1. tCAD (layer 57) dropped from SOT23-6L** (Okapi U7, U30; Margay U13, U14; Okapi.brd line 1081, Margay.brd line 578): 28 hairline wires (0.0011 mm) of a package drawing. No KiCad layer received them.

**C2. Okapi dimensions on layer 47 (Measures) dropped** (Okapi.brd lines 316-319): 4 dimensions, two of them duplicates of the three layer-48 dimensions that did come through to User.Comments.

**C3. Margay text on layer 122 `_bsilk` dropped** (Margay.brd line 228): one "J2" label, mirrored, on a layer hidden in Eagle. Whether it reached the fab silkscreen: UNVERIFIED.

**C4. Silkscreen and fab drawings** match in count per layer in every package. Remaining area differences in `geometry.py` are method (text and a tNames circle are counted on the KiCad side; arc polygonization), not losses.

## Fixes applied (coordinator, 2026-11-11, after Andy: "conversion-audit fixes, first on Margay and then on Okapi")

- **Library (nw-cold-silicon 4e7e507, a69d849, dd472f7):** B2, layer 43 is kept as the converter wrote it (via-only keepout); B3, SIM_SF72's wire-drawn vRestrict becomes the keepout it encloses. Four library-only footprints change; SWITCH_2.6X1.6 (Okapi S5) is byte-identical.
- **New finding D1, found while checking C3: the printed docu labels.** Both fabs' silkscreen Gerbers carry Eagle layers 51 (top) and 52 (bottom): pin labels, jumper and port-limit notes, the credit blocks. The import put them on F.Fab and B.Fab, which do not print. C3's layer-122 "J2" was not printed (rendered, 33 lit pixels in its window, none of them its text). Moved to F.SilkS and B.SilkS: Margay 33 items (Project-Margay 151562f), Okapi 116 (Project-Okapi 0cd727b). Renders of the KiCad silkscreen now match the fab's for these labels.
- **B1 (Project-Okapi 651735b):** the two bottom keepouts restored as B.Cu rule areas, 27.50 and 60.51 mm2; refilling changes no copper.
- **A2:** already done before this audit (Project-Okapi cb8bdce, 2026-11-10).
- **Open for Andy:** A1 (vias stay tented unless Andy says otherwise); the GCT slot length (1.2 mm as fabricated, 1.4 mm per GCT); package-level docu that Eagle printed and KiCad does not (part outlines such as IC1's pins, the jumper schematic glyphs on Okapi's and Margay's bottoms); reference designators, which KiCad prints on Margay where Eagle did not (Okapi's fab printed them). A3, C1, C2: no action proposed.

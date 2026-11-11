# USB shell-stake slot fix: agent report

Status: COMPLETE

Task: restore layer-46 (Milling) slots dropped by the Eagle-to-KiCad import for
USB_C_CUSB31-CFM2AX-01-X (Okapi J10, Margay J4) and USB_MICRO_VERT_MOLEX (Okapi USB2).

## Log

### 1. Layer-46 scan of the workspace (every .brd and .lbr)

Script: `/tmp/claude-1000/-home-awickert-Dropbox-NorthernWidget-github/cf0342fa-36e3-4818-be1e-2b4b31cc1756/scratchpad/slot/scan46.py` (packages with any child on layer 46). Output:

```
files scanned 161 unparsed 2
  unparsed ./ALog-Shield.backup/ALogShield.brd
  unparsed ./ALog-Shield-backup2/ALogShield.brd
BUTTON-10MM
    2 SparkFun-Eagle-Libraries/SparkFun-Retired.lbr
BUTTON-18MM
    2 SparkFun-Eagle-Libraries/SparkFun-Switches.lbr
JST04_1MM_RA_STRESSRELIEF
    2 SparkFun-Eagle-Libraries/SparkFun-Connectors.lbr
LED_1206_BOTTOM
    4 Cold-Silicon/bschulz.lbr
M.2-CARD-E-22
    8 Cold-Silicon/bschulz.lbr
    8 SparkFun-Eagle-Libraries/SparkFun-MicroMod.lbr
MICRO:BIT-RA_SMD
    2 SparkFun-Eagle-Libraries/SparkFun-Connectors.lbr
MUSB-K152-30
    8 Cold-Silicon/bschulz.lbr
MUSB-K552-30
    8 Cold-Silicon/bschulz.lbr
POWER_JACK_PTH_SLOT
    3 SparkFun-Eagle-Libraries/SparkFun-Connectors.lbr
POWER_JACK_SLOT
    19 Cold-Silicon-awickert/bschulz.lbr
    19 Cold-Silicon-awickert/bschulz_Old.lbr
    19 Cold-Silicon/bschulz.lbr
    19 Cold-Silicon/bschulz_Old.lbr
SM5100B
    4 SparkFun-Eagle-Libraries/SparkFun-RF.lbr
SMA-EDGE-SMD
    10 SparkFun-Eagle-Libraries/SparkFun-RF.lbr
SMA-THREADED
    3 SparkFun-Eagle-Libraries/SparkFun-Hardware.lbr
SPARKFUN-CONNECTORS_POWER_JACK_SLOT
    19 TLog/ALog-TLog/TLog.lbr
TFT_2.83IN_240X320_50PIN
    1 Adafruit-Eagle-Library/adafruit.lbr
USB-C-16P-2LAYER-PADS
    4 SparkFun-Eagle-Libraries/SparkFun-Connectors.lbr
USB-C-16P-4LAYER-ISOLATED
    16 SparkFun-Eagle-Libraries/SparkFun-Connectors.lbr
USB-C-16P_4LAYER-PADS
    4 SparkFun-Eagle-Libraries/SparkFun-Connectors.lbr
USB-MICROB-PTH-MILL
    24 SparkFun-Eagle-Libraries/SparkFun-Connectors.lbr
USB_A_3.0_MALE_TENSILITY
    8 Cold-Silicon/bschulz.lbr
USB_A_MALE_0480372200
    8 Cold-Silicon/bschulz.lbr
USB_A_UP2-AH
    9 Cold-Silicon/bschulz.lbr
USB_C_CUSB31-CFM2AX-01-X
    24 Andy-Project-Margay/Hardware/Margay.brd
    24 Project-Margay-0603wdt/Hardware/Margay.brd
    24 Project-Margay-newUSBinProgress/Hardware/Margay.brd
    24 Project-Margay/Hardware/Margay.brd
    24 Project-Okapi/Hardware/Okapi.brd
USB_MICRO_VERT_MOLEX
    18 Project-Okapi/Hardware/Okapi.brd
```

The two unparsed files (ALog-Shield backups, malformed XML) hold no `layer="46"` text (grep count 0).
Okapi.brd and Margay.brd carry only the two target packages; the Margay package is identical to Okapi's
(element-by-element comparison: True). Not fixed, reported: bschulz.lbr's LED_1206_BOTTOM, M.2-CARD-E-22,
MUSB-K152-30, MUSB-K552-30, POWER_JACK_SLOT, USB_A_3.0_MALE_TENSILITY, USB_A_MALE_0480372200 and USB_A_UP2-AH
are in nw-cold-silicon and carry the same importer loss; none is placed on Okapi or Margay.

### 2. Eagle geometry (Okapi.brd packages)

USB_C_CUSB31-CFM2AX-01-X: M1/M2 at (±4.32, 6.78), slot 0.6 x 1.7 (y 5.93..7.63); M3/M4 at (±4.32, 2.6),
slot 0.6 x 1.2 (y 2.0..3.2). Pads drill 0.6, diameter 1, shape long, R90: copper 1 x 2. Slot centers equal the pad centers.

USB_MICRO_VERT_MOLEX: three slots, each enclosing a pair of 0.5 mm drills (pad diameter 1.1, 0.7 or 1.1 mm apart):
P$1/P$2 slot 1.2 x 0.5 centered (-2.8, 1); P$3/P$4 1.2 x 0.5 at (2.8, 1); P$5/P$6 1.6 x 0.5 at (0, -1.15).
The current library footprint (38f98b3) already joins each pair as one pad number with a 1.1 mm copper bar primitive;
the copper of a pair is therefore a stadium 1.8 x 1.1 (or 2.2 x 1.1), which an oval pad of that size reproduces exactly.

### 3. GCT USB4105 datasheet (page 1, Recommended PCB Layout, drawing dated 4 October 2019)

Rendered at 300 dpi and read: slot width 4x 0.60, pad width 4x 1.00. Rear pair (beside the SMD row, 4.18 from the
front pair): slot 2x 1.70, pad 2x 2.10. Front pair (2.60 from the PCB edge): slot 2x 1.40, pad 2x 1.80.
Eagle: rear slot 1.7 (agrees), front slot 1.2 (GCT 1.40), pads 1 x 2 on both pairs (GCT 2.10 rear, 1.80 front).
Positions agree (8.64 across, 4.18 between pairs, NPTH 3.68 from the front pair).
KiCad's USB_C_Receptacle_GCT_USB4105-xx-A_16P_TopMnt_Horizontal agrees with GCT: oval 0.6x1.7 in 1x2.1, 0.6x1.4 in 1x1.8.
Decision for Andy, not changed here: front slot 1.2 (Eagle, fabricated) vs 1.4 (GCT).

### 4. Library rule: nw-cold-silicon 26badbb

`MILLED_SLOTS` in tools/build.py (after the restring, which reads round drills only); README line added. Build:
`848 footprints, 1403 symbols; second pass: 0 fp changed, sym identical; collisions 1844` (1 m 49 s).
Diff: the two footprints only, plus COLLISIONS (2 lines) and PROVENANCE (date, slot line, mask margins 7608 -> 7605,
the three micro-USB pads removed). pcbnew `GetEffectiveHoleShape` on the library footprints:
M1/M2 0.6 x 1.7 at y -6.78, M3/M4 0.6 x 1.2 at y -2.6; P$1/P$3 1.2 x 0.5 at (±2.8, -1), P$5 1.6 x 0.5 at (0, 1.15).

### 5. Okapi baseline gates (library at 26badbb, board not yet refreshed)

Board copies saved first: `/tmp/claude-1000/-home-awickert-Dropbox-NorthernWidget-github/cf0342fa-36e3-4818-be1e-2b4b31cc1756/scratchpad/slot/ok0/*.kicad_pcb.save`. `gates.sh`:

```
linked 250 footprints; values set 250; fields added 0; fields updated 0; no symbol: []
== Eagle nets: 209  exactly reproduced in one KiCad net: 204  with differences: 5
sheets identical 17 rt=0
Okapi.kicad_pcb  identical
unconnected_wire_endpoint 0  endpoint_off_grid 0  total 5
drc 2 unconnected 0 parity 0
padnets identical
```
The 2 DRC items are both `lib_footprint_mismatch` warnings (J10, USB2): the new library, i.e. 0 before 26badbb.

Margay baseline (`mgates.sh`): Eagle nets 75 / 72 / 3; 4 sheets identical; board identical; ERC 0; drc 2
(lib_footprint_mismatch J4, track_dangling VBAT_SW 0.1078 mm, the known one) unconnected 0 parity 0; padnets identical.

### 6. Okapi refresh

`rebody.py ... --only J10,USB2`: 2 re-bodied, USB2's three pads moved to the slot centers and widened (P$1, P$3 1.8x1.1, P$5 2.2x1.1),
no pad only on one side. Then `kicad-cli pcb upgrade --force` twice. Gates after:

```
linked 250 footprints; values set 250; fields added 0; fields updated 0; no symbol: []
== Eagle nets: 209  exactly reproduced in one KiCad net: 204  with differences: 5
sheets identical 17 rt=0
Okapi.kicad_pcb  identical
unconnected_wire_endpoint 0  endpoint_off_grid 0  total 5
drc 0 unconnected 0 parity 0
padnets identical
J10 needs update False
USB2 needs update False
```

### 7. Free check: KiCad drill file against the fabricated 2024 profile.gbr

`kicad-cli pcb export drill --excellon-separate-th --excellon-oval-format alternate -u mm`; script `/tmp/claude-1000/-home-awickert-Dropbox-NorthernWidget-github/cf0342fa-36e3-4818-be1e-2b4b31cc1756/scratchpad/slot/slotcheck.py`.
Offset from J10's two 0.65 mm NPTH holes in Eagle's drill_1_16.xln (both give the same offset). Output:

```
Eagle 0.65 holes [(3.46, 5.137), (9.24, 5.137)] KiCad Excellon 0.65 holes (x, Y as written) [(119.586, -167.367), (125.366, -167.367)]
offsets Excellon(x,y) - Eagle: [(116.126, -172.504), (116.126, -172.504)]
Eagle profile small outlines (cx, cy, w, h), Eagle coords:
   (2.03, 1.457, 0.6, 1.2)
   (2.03, 5.637, 0.6, 1.7)
   (3.46, 5.137, 0.65, 0.65)
   (9.24, 5.137, 0.65, 0.65)
   (10.67, 1.457, 0.6, 1.2)
   (10.67, 5.637, 0.6, 1.7)
   (14.121, 52.921, 0.9, 0.9)
   (17.121, 52.921, 0.9, 0.9)
   (34.947, 87.9, 1.55, 1.55)
   (47.014, 52.667, 0.9, 0.9)
   (50.014, 52.667, 0.9, 0.9)
   (54.947, 87.9, 1.1, 1.1)
   (61.23, 101.34, 0.5, 1.2)
   (61.23, 106.94, 0.5, 1.2)
   (63.38, 104.14, 0.5, 1.6)
KiCad PTH slots -> Eagle coords (cx, cy, w, h) and residuals against the nearest profile outline:
  tool 0.500 center (61.2300, 106.9400) size 0.500 x 1.200 | profile (61.2300, 106.9400) 0.500 x 1.200 | residual dx -0.0000 dy 0.0000 dw 0.0000 dh 0.0000
  tool 0.500 center (61.2300, 101.3400) size 0.500 x 1.200 | profile (61.2300, 101.3400) 0.500 x 1.200 | residual dx -0.0000 dy 0.0000 dw 0.0000 dh 0.0000
  tool 0.500 center (63.3800, 104.1400) size 0.500 x 1.600 | profile (63.3800, 104.1400) 0.500 x 1.600 | residual dx -0.0000 dy -0.0000 dw 0.0000 dh 0.0000
  tool 0.600 center (2.0300, 5.6370) size 0.600 x 1.700 | profile (2.0300, 5.6370) 0.600 x 1.700 | residual dx 0.0000 dy -0.0000 dw 0.0000 dh -0.0000
  tool 0.600 center (2.0300, 1.4570) size 0.600 x 1.200 | profile (2.0300, 1.4570) 0.600 x 1.200 | residual dx 0.0000 dy -0.0000 dw 0.0000 dh -0.0000
  tool 0.600 center (10.6700, 5.6370) size 0.600 x 1.700 | profile (10.6700, 5.6370) 0.600 x 1.700 | residual dx 0.0000 dy -0.0000 dw 0.0000 dh -0.0000
  tool 0.600 center (10.6700, 1.4570) size 0.600 x 1.200 | profile (10.6700, 1.4570) 0.600 x 1.200 | residual dx 0.0000 dy -0.0000 dw 0.0000 dh -0.0000
```
All seven slots (J10's four and USB2's three) land on the fabricated milling outlines with zero residual at the
drill file's 3-decimal precision. USB2's slots are in the 2024 profile too, so they are checked against the
fabricated board as well as the package.

Okapi committed: Project-Okapi 33070ed. Board diff: the slot drills, USB2's three removed pads and bar primitives,
and fresh uuids on the two footprints' body items (rebody gives new uuids, as KiCad does on placement).

### 8. Margay J4 refresh: Project-Margay 7c55635

`rebody.py ... --only J4` (front side, rot 180): 1 re-bodied, no pad moved. Two upgrade passes. `mgates.sh` after:

```
linked 84 footprints; values set 84; fields added 0; fields updated 0; no symbol: []
== Eagle nets: 75  exactly reproduced in one KiCad net: 72  with differences: 3
sheets identical 4
Margay.kicad_pcb  identical
unconnected_wire_endpoint 0  endpoint_off_grid 0  total 0
drc 1 unconnected 0 parity 0
padnets identical
track_dangling warning ['Track [/Power_Sensors/VBAT_SW] on F.Cu, length 0.1078 mm']
J4 side F.Cu rot 180.0 needs update False
```
check_conversion's report tail identical to the baseline. Free check against the fabricated
Production/Margay_3v0_2023-08-01.zip profile.gbr (`/tmp/claude-1000/-home-awickert-Dropbox-NorthernWidget-github/cf0342fa-36e3-4818-be1e-2b4b31cc1756/scratchpad/slot/slotcheck2.py`):

```
Eagle 0.65 holes [(37.369, 25.343), (43.149, 25.343)] KiCad Excellon 0.65 holes (x, Y as written) [(160.798, -94.863), (166.578, -94.863)]
offsets Excellon(x,y) - Eagle: [(123.429, -120.206), (123.429, -120.206)]
Eagle profile small outlines (cx, cy, w, h), Eagle coords:
   (2.159, 2.159, 2.9464, 2.9464)
   (8.058, 7.334, 1.1, 1.1)
   (29.058, 7.334, 1.6, 1.6)
   (35.939, 24.843, 0.6, 1.7)
   (35.939, 29.023, 0.6, 1.2)
   (37.369, 25.343, 0.65, 0.65)
   (43.149, 25.343, 0.65, 0.65)
   (44.579, 24.843, 0.6, 1.7)
   (44.579, 29.023, 0.6, 1.2)
   (48.006, 28.194, 2.9464, 2.9464)
KiCad PTH slots -> Eagle coords (cx, cy, w, h) and residuals against the nearest profile outline:
  tool 0.600 center (35.9390, 29.0230) size 0.600 x 1.200 | profile (35.9390, 29.0230) 0.600 x 1.200 | residual dx -0.0000 dy 0.0000 dw 0.0000 dh 0.0000
  tool 0.600 center (35.9390, 24.8430) size 0.600 x 1.700 | profile (35.9390, 24.8430) 0.600 x 1.700 | residual dx -0.0000 dy 0.0000 dw 0.0000 dh -0.0000
  tool 0.600 center (44.5790, 29.0230) size 0.600 x 1.200 | profile (44.5790, 29.0230) 0.600 x 1.200 | residual dx 0.0000 dy 0.0000 dw 0.0000 dh 0.0000
  tool 0.600 center (44.5790, 24.8430) size 0.600 x 1.700 | profile (44.5790, 24.8430) 0.600 x 1.700 | residual dx 0.0000 dy 0.0000 dw 0.0000 dh -0.0000
```

### 9. Skill note: claude-kicad-text deb7a42

references/eagle-conversion.md step 0 names the fault (layer 46 dropped, milled slots lost), how to find, write and
check the slots; SKILL.md's list of importer faults gains "milled slots". NW-Tests/kicad mirrors only the scripts,
not the references, so it has no copy to sync and no commit there.

### 10. Library rebuild record: nw-cold-silicon 5c3e56b

A second build after the board refreshes changed only COLLISIONS.md and PROVENANCE.md: the board pass (which compares
each board's footprint with the raw conversion) now reports USB_C_CUSB31-CFM2AX-01-X as pads differ on both boards
(Okapi identical 62 -> 61, differ 3 -> 4; Margay 33 -> 32, 1 -> 2), as the micro-USB and coin holder already were.
A third build left the tree clean.

### Commits (local only, nothing pushed)

- nw-cold-silicon 26badbb build: Eagle's milled slots (layer 46) become oval drills (USB-C and micro-USB shells)
- Project-Okapi 33070ed KiCad: J10 and USB2 shell stakes in milled slots, re-bodied from nw-cold-silicon 26badbb
- Project-Margay 7c55635 KiCad: J4 shell stakes in milled slots, re-bodied from nw-cold-silicon 26badbb
- claude-kicad-text deb7a42 eagle-conversion: the importer drops layer 46 (Milling), and with it every milled slot
- nw-cold-silicon 5c3e56b Library rebuilt after the boards took the slots: board pass reports J10 and J4 as pads differ

### Open, for Andy

1. USB-C front slot length: Eagle (fabricated) 0.6 x 1.2, GCT USB4105 drawing (page 1, Recommended PCB Layout,
   4 October 2019) 0.6 x 1.40; GCT pads 1.00 x 2.10 rear and 1.00 x 1.80 front against Eagle's 1 x 2 on both.
   Rear slot 1.7 agrees. Eagle's stands in the library until decided.
2. Other layer-46 packages in nw-cold-silicon sources, unfixed and unplaced on these boards: LED_1206_BOTTOM,
   M.2-CARD-E-22, MUSB-K152-30, MUSB-K552-30, POWER_JACK_SLOT, USB_A_3.0_MALE_TENSILITY, USB_A_MALE_0480372200,
   USB_A_UP2-AH (bschulz.lbr). Adding one to MILLED_SLOTS is one line, once its outlines are confirmed to be stadiums
   around pad drills (the rule asserts that).
3. Observation: the USB-C shell pads M1-M4 have no net on either board, as in Eagle (no contactref); unchanged here.

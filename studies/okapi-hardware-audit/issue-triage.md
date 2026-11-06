# Project-Okapi open issues: a proposed sort onto milestones (B3)

2026-11-06, Sonnet, from `issues.md` (the 2026-10-30 audit against the Eagle
files) and DECISIONS "Okapi: The plan". A proposal: nothing on GitHub has been
moved, commented or closed from this list. Milestones today: v0.6.0 (#1, the
2024 redesign's marker), v0.7.0 (#2, the KiCad board), v0.8.0 (#3, the next
power section). The list below needs a v1.0.0 milestone ("the design judged
ready for a run", Andy 2026-11-05) for what is not v0.7.0 or v0.8.0; creating
it is one of the yeses asked for.

| # | Title | Move to | Why, from the audit | Action beyond the move |
|---|---|---|---|---|
| 3 | Always-on port | v1.0.0 | a question; needs a jumper and a level-shifter change | none |
| 5 | LTC4412 STAT | v0.8.0 | wants a pin; only GPA2 was free and #35 took it, so it waits for #26's second-expander answer | none |
| 7 | Output drain MOSFET Q7 | v0.7.0 | confirmed not applied: Q7 is still 2N7002W-7-F, the part that latches; Q4 and Q8 carry the same number. BoM only; blocks a first build | comment; take it off v0.6.0 |
| 10 | Move RockBlock Feather to its own repo | none | repository housekeeping, not hardware | take it off v0.6.0 |
| 12 | Serial_Ctrl.ino | none | firmware sketch; Okapi_Library, not the board | none |
| 13 | v1.0 Updates | v1.0.0 | a checklist, nine of ten done; its open item overlaps #32 and #20 | comment that #32 covers the charger |
| 14 | SIM pins | v1.0.0 | a question | none |
| 15 | AREF tied to supply | v0.7.0 | confirmed, but the rail is 3V3_CORE, not 5V_AUX as the issue says; shorted references, not damage | comment with the correction |
| 17 | VCC bypass missing | v0.7.0 | partly confirmed: VCC pads 5, 17 and 38 have nothing within 6 mm; again 3V3_CORE | comment with the correction |
| 18 | Crystal load capacitors | v0.7.0 | confirmed arithmetic, part rating unverified. **Conflicts with a decision already made**: A4 sets C40/C41 to the 12 pF TDK 0402 number (fixing the part number only), while #18 says 12 pF is too small for an 18 pF crystal | **Andy decides the value** before B4 touches C40/C41 |
| 19 | No ESD on SoM USB | v1.0.0 | decide first whether the second USB stays | none |
| 21 | R72 to R75 unvalued | v0.7.0 | values decided 2026-11-05 (A3), applied in B1 | comment with the values; close when B1 lands, on your word |
| 23 | /RESET capacitor | v1.0.0 | a bypass would halve the DTR auto-reset pulse through C39; needs a retest | none |
| 24 | Ground under switchers | v0.7.0 | confirmed for U4; vias at its exposed pad are cheap and ride with #30 | none |
| 25 | SD series resistors | v0.8.0 | wants a GPIO for the power switch; one pin question with #5 and #26 | none |
| 27 | TPL5111 not suppressible | none | **not reproducible**: the circuit was misread; the real finding (R62 above the part's range) is #34 | close with a comment on your word |
| 28 | Accumulated minor issues | v0.7.0 | sub-item 3 (C42) is B4; 1, 5 and 6 are no defect; 2 (AVCC filter) rides with #15; 4 (USB current) is yours | comment with which sub-items are decided |
| 29 | I2C bus occupancy | v0.7.0 | resolved from the files; the PAC1934 is at 0x10 by R51 = 0 Ω | comment; close when the spec table in NW-Device-Specification is filled in |
| 30 | Re-land !FAULT on !SHDN | v0.7.0 | confirmed and strengthened in the audit; a layout change, never milestoned | none |
| 31 | B-SoM 3.3 V and the core path | v0.8.0 | parent of #37 to #40 | none |

Already placed: #26 (v0.8.0), #32 to #37 (v0.7.0), #38 to #40 (v0.8.0).

Counts: of the 20 issues listed, 9 go to v0.7.0 (#7, #15, #17, #18, #21, #24,
#28, #29, #30), 3 to v0.8.0 (#5, #25, #31), 5 to v1.0.0 (#3, #13, #14, #19,
#23), and 3 stay unplaced (#10, #12, #27). Closes waiting on your word: #27 now,
and #21 and #29 when their work lands.

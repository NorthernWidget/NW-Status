# Margay v4.0.0: how large, and which size

Two agent reports, checked here, and how they combine. The form-factor-preserving plan for v3.1 is `margay-v3.1-room-study.md` and stays as it is.

- `sources/2026-11-12-margay-larger-board-area-agent-report.md` (tools in `tools/margay-larger/`): how much top area the circuit needs if every machine-placed part is on top, including #66. `required.py` re-run here gives the same output.
- `sources/2026-11-12-margay-convenient-sizes-agent-report.md`: which outlines are convenient, and why. The hole pattern (2.946 mm drills at (125.588, 118.047) and (171.435, 92.012), 45.85 x 26.04 mm apart) and the WH-02 lid mount's 54.41 mm width were re-measured here from the KiCad board and the STL.

## The rule

One machine-assembled side, the top. The bottom takes only parts that are easy to add with an iron after reflow (0603 or larger, leaded packages). J1, the SD holder, stays on the bottom and is hand-soldered as now. This keeps Margay buildable in university labs and modest assembly houses (Andy, 2026-11-12, naming Lagos and Buenos Aires).

## What the circuit needs

Today's top: 1423.6 mm² usable (outline inset 0.4 mm, less the two hole keepouts), filled to a density of 0.645 (courtyards, or pads plus 0.25 mm where a footprint has none) or 0.802 (part bodies, which counts the terminal blocks' overhang). The v3.1 issues and #66 add 27 parts (141.8 mm²) and remove 6 (29.2 mm²).

- At today's density: 1564–1598 mm² usable, 10–12 % more than today.
- At 90 % of today's density: 1738–1776 mm².
- At 80 %: 1955–1998 mm². The 90 % and 80 % steps are the agent's proposal for routing relief, not a measurement.

50.1 x 30.4 mm is already the minimum in both directions. The top edge holds J2's pads, the SD card's entry, USB-C and H2. The left edge holds J2's body and H1. The board can only grow.

## Which size

Usable area for each convenient outline, with the holes kept as today (an approximation for the larger boards), and the density at which today's parts plus the additions would fill it:

| Outline (mm) | Why it is convenient | Usable (mm²) | Density, % of today's |
|---|---|---|---|
| 50.8 x 40.64 (2.0 x 1.6 in) | Keeps both holes, so every printed mount and the WQ-48 plate still work. Grows only along the short side, which the WH-02 lid mount (54.41 mm) allows. 0.1 in grid. | 1955 | 80–82 |
| 64.75 x 50.8 | Okapi's width. A hole pair 40.000 mm apart sits on Okapi's standoffs. New WH-02 lid plate. | 3160 | 49–51 |
| 80 x 50 | Holes on Okapi's 40 x 80 mm L. New WH-02 lid plate. | 3859 | 41 |
| 68.6 x 53.4 | Arduino Uno outline and its cases. Uno hole pattern UNVERIFIED. | 3529 | 44–45 |
| 100 x 70 | Largest that plausibly fits a WH-02 (UNVERIFIED cavity). | 6827 | 23 |
| 100 x 100 | Top of JLCPCB's price tier. Does not fit a WH-02. | 9803 | 16 |

**50.8 x 40.64 mm holds the whole v4 circuit, #66 included, at about 80 % of today's packing density**, which is the routing-relief case, and it keeps every mount. A larger outline buys room for future parts or a looser layout, at the price of new mounts and, above about 54 mm on the long side, a new WH-02 lid plate. No outline here has been laid out: these are area budgets.

## Fab and local-build notes

- JLCPCB has a special price up to 102 x 102 mm and a surcharge when a side is 30 mm or less. Today's short side is 0.4 mm over that line. OSH Park and Aisler price by area.
- Mayer, in Buenos Aires, makes double-sided boards and offers SMT assembly and stencils. No bare-board fab was found in Nigeria. The one sizable SMT assembler found is in Port Harcourt.

## Open questions for Andy

1. Keep the 45.85 x 26.04 mm diagonal hole pair (every existing mount), add Okapi's 40 x 80 mm grid, or both?
2. Is WH-02 still a target enclosure? It is the one that caps the board's size.
3. Which reflow tool should a lab be assumed to have? A 100 x 100 mm hot plate takes every candidate; a 50 x 50 mm mini plate does not take today's board.
4. The README puts the CR1220 on the back. The board files and the photo put it on top. Fix the README?

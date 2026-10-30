# Can a trace reach the LT3652's !SHDN from the expander? (2026-10-26)

`route_search.py` rasterizes both copper layers of `Project-Okapi/Hardware/Okapi.brd`
at 0.05 mm, grows every foreign pad, trace, via and hole by the clearance plus half
the trace width, treats the `MPPT_SHDN` net's own copper as the start and the
MCP23018's free GPA2 pad (pad 17) as the goal, and searches for a path that may
change layers wherever a via fits on both. Pours are ignored (they yield to a trace).
Run it from `Project-Okapi/Hardware` with `CL=<mm> TW=<mm> VIA=<mm>` in the environment;
it writes `route_<CL>.png` and `crop_<CL>.png` beside itself.

| Clearance | Width | Result |
|---|---|---|
| 0.1524 mm (6 mil, the board's wire-to-pad rule) | 0.1524 | 302 mm, 13 vias (unweighted); 311 mm, 7 vias (via penalized): around the whole board |
| 0.127 mm (5 mil, the board's wire-to-wire rule) | 0.127 | 252 mm, 17 vias: still around the board |
| 0.10 mm (4 mil, below the board's rules) | 0.127 | 110 mm, 10 vias: a direct corridor opens |
| 0.076 mm (3 mil) | 0.127 | 110 mm, 10 vias |

Under the board's own rules the direct corridor between the charger (bottom left)
and the expander (center) is closed; the only legal path circles the board. The
alternative that needs no corridor: the `!FAULT` line (pad 5, net `MPPT_FAULT`:
U4, a 1 M pull-up R56, expander GPA4 and nothing else) already runs from this
chip to the expander, and pad 3 (`!SHDN`) is 0.9 mm from pad 5 on the DFN-12.
Re-landing that trace on pad 3, a local reroute at the chip, gives the open-drain
expander a shutdown control at the cost of the `!FAULT` report (Project-Okapi#30
holds the plan and the trade-off). The `!CHRG` pin (pad 4) is 0.45 mm away but its
net also carries Q8 and the R70/R71 solar-lockout network on `!SHDN`, so it is the
worse donor. The PNGs show the found routes at 6 mil: cyan top, magenta bottom,
white squares vias, yellow the existing `!SHDN` copper, green the goal pad.

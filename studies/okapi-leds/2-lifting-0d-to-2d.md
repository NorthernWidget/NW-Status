I have everything needed. One verified finding along the way: `NW_MSG_BATTERY_LOW` is defined in `NW_Message.h` and raised nowhere (grep over NW_Logger, Margay_Library, Okapi_Library returns only the definition), and Okapi's `readOnBoard()` yields raw VBeta/VPrime volts with no percentage. That bears on question 3.

# Okapi's grid as a lifted Margay: 1D and 2D versions of the 0D flashes

## Recommendation

Keep the steady-columns proposal as the frame and add one lifting to it: **the worst column's lit cell plays D5's rhythm in lockstep with D5** (same frames, same milliseconds, one `LEDOUT` write per edge), while the other two columns stay steady. That is the 0D→1D "keep time" lifting, with the mixed-colour problem solved by letting the column choose the cell: the rhythm always plays on a cell whose fixed colour is already the band's colour. It costs no new vocabulary, binds the grid to D5 by synchrony so the two channels read as one event, and draws the eye to the column that matters. Every other lifting (timeline, tape, fill, Morse-in-space, bar graph) is rejected for the verdict, with reasons below. One hazard of the columns proposal surfaced: the colour layout is 180°-symmetric about the centre, so a board read upside-down swaps columns A and C.

## 1. Time to space: the four liftings on 3 cells

A rhythm is a list of on/off durations. Three ways to draw it along a line, and how each Margay pattern fares on a 3-cell column (the longest straight line of one colour the grid has) or the full 8:

| Rhythm (on-pulses per cycle) | Timeline (steady strip, 1 cell = 1 time slot) | Tape (scrolls one cell per step) | Fill (one cell per pulse) |
|---|---|---|---|
| READY chirp 1000/300/100/100/100 (3) | Fails: 1600 ms cycle at 100 ms slots needs 16 cells; at 3 cells it is "three lit", shape lost | Works at 100 ms step: solid 3-cell bar for 1 s, dark, then two single dots climb. Long–short–short survives | Fits 3 cells exactly, but 3 identical adds; shape lost unless the add timing carries it |
| Card flutter 60/60 (25) | Fails: 50 slots | Fails: alternating 101/010 at 16.7 steps/s reads as strobe, not motion | Overflows at pulse 4 |
| CLOCK syncopation 250/100/100/100 (2) | Fails: long–short needs ≥4 slots on 3 cells | Marginal: a 2.5-cell bar followed by a dot, at 550 ms per cycle, five times. Legible but it is a new thing to learn | 2 adds then reset; the syncopation (the message itself) is gone |
| SENSOR pips 100/300 (8) | 8 cells = 8 pulses, "all lit": indistinguishable from any full display | Best case: one dot climbs the column every 400 ms, eight times. "Calling out into nothing" becomes a dot sent up a line and lost | Fills all 8 in channel order, which on this board is a zigzag (C3,C2,C1,B2,B1,A1,A2,A3), not a line |
| CAUGHT amber 500/500 (3) | 6 slots at 500 ms: fails on 3, fits 8 but is just "every other cell" | Three slow bars climbing; works, dull | Fits 3 cells, 3 identical adds |
| BAD solid 3 s (1) | All lit | All lit after 3 steps | 1 cell |

Timeline fails for every pattern that has a shape: a strip that is faithful to durations needs 16–50 cells. Fill is counting, which Andy already rejected for Margay ("a look-up table with everything given equal weight"), and a dead cell makes a fill lie. The tape is the one honest lifting: it is a comb filter made of light, and each cell is the rhythm delayed by one step, so a pulse longer than three steps saturates the line and a short one travels as a dot. At 2.667 mm pitch and 100 ms step, held at 0.4 m, the dot moves 0.38° per step: well inside the range where successive flashes read as one moving light (Wertheimer 1912; Korte's laws give optimal inter-stimulus intervals of a few tens of ms at this separation; UNVERIFIED for these exact values). The pips are the pattern that gains most, and the flutter is the one that dies.

## 2. Keeping time: the same rhythm on a column

Playing D5's rhythm on all three cells of a column lights green, yellow and red together. The rhythm survives (rhythm is carried by onset timing, which is colour-independent), but the severity cue is damaged: a red flutter with a green cell fluttering in it is a mixed message, and for a normal-vision user colour is the fastest severity read. The fix is to play on the band's own colour class: READY on the three greens (A1, B2, C3: the rising diagonal), CAUGHT on the three yellows (A2, B1, C2), BAD on the two reds (A3, C1: the ends of the falling diagonal). Blue is not available, so the chirp is green on the grid and blue on D5. Area: three 0603s against one RGB. Furthermore, the colour class and the geometry agree: a rising line is fine, two corners are bad. This is the lifting the recommendation keeps, narrowed to one cell (the worst column's) so it composes with the columns.

## 3. A column as a quantity

What the logger knows at `showVerdict()` (`NW_Logger.cpp:466–476`): `_cycleMillisMax` and `cycleSeconds()` against `_logInterval` (`keepInterval()`, `:536–557`), so the fraction of the interval the first cycle used is measured; `_intervalAsked` against `_logInterval`, one bit, already a FINE message; `wdtSeconds`; and the sensor result, which `I2Ctest()` raises per failing address (`:208`) without storing a count. Battery: Margay has `getBatPercentage()` with `nCells`; Okapi's `readOnBoard()` (`Okapi.cpp:165–200`) produces raw volts and no percentage, and **`NW_MSG_BATTERY_LOW` is raised nowhere** (verified by grep). Of these, one is worth three levels: cycle fraction (under a third, under two thirds, overran), because it is the quantity the adaptive interval acts on and `CYCLE_OVERRAN` is its top bin. Battery is worth three levels once Okapi has a percentage, and not before. Sensor count is not worth a bar: the technician needs the address, which only the Note column has. Interval length is the sketch's choice and needs no display. Verdict: no bar graph now; the cycle fraction is the one candidate, and it conflicts with position-as-identity on a 3-column grid.

## 4. 0D to 2D: rhythm as shape

Long–short–short drawn as a dash and two dots is Morse "D" and needs five cells in a line; the grid's longest line is three. Drawn on the rising diagonal it is three equal cells, which is a count. More fundamentally, a Margay-trained eye knows the chirp as a temporal gestalt, and a frozen strip has to be *read*, which makes it the code Andy rejected. Reject the frozen-shape lifting.

The two-channel design (D5 in time, grid in space) stands or falls on synchrony. Wickens' multiple-resource theory separates visual-spatial from visual-verbal and focal from ambient, but two visual-focal signals share one resource, so the gain is not parallel capacity. The gain is redundancy: the redundant-signals effect gives reaction-time savings of tens of milliseconds (Miller 1982, race-model inequality) and, more usefully here, tolerance of one missed channel. The risk is real: two unrelated patterns in one glance read as noise. Common onset is the strongest cue that binds elements into one object (temporal-synchrony grouping, Blake and Lee 2005; Alais et al. 1998), so the grid must change state on the same millisecond as D5 or not at all. A frozen grid beside a blinking D5 fails this test; a cell blinking in lockstep passes it.

## 5. Dimensional inventory

| Dimension | States | Bits a technician takes without a card | Basis |
|---|---|---|---|
| x position (column) | 3 | 1.6, reliable | Location is encoded automatically (Hasher and Zacks 1979); tDocu boxes group by common region (Palmer 1992) |
| y position within a column | 3 | 1.6, reliable | 2.03 mm pitch is 0.29° at 0.4 m, far above acuity; top/middle/bottom needs no reference |
| cell colour | fixed | 0 new, but redundant with y in A and C: the colour-deficient user's safety net | Colour and position say the same thing |
| rhythm on D5 | 5 patterns | 2.3, proven on Margay | Contrast within the set, not absolute rate |
| D5 colour | 3 | 1.6, redundant with rhythm | Blue/amber/red |
| brightness (PWM) | 256 | about 1 indoors, 0 in sunlight | Absolute luminance judgment without a reference is one or two levels; a 0603 at a few mA (UNVERIFIED mcd) does not resolve "dim" against daylight |
| group blink | 1 rate at a time | 0 to 1 | A second tempo beside D5 competes for the same channel |
| count of lit cells | 0–8 | 2 (subitising to 3–4; Kaufman et al. 1949; Trick and Pylyshyn 1994) | Canonical patterns extend it (dice faces) but the grid is not laid out for them |
| D4 | 2 | 1 | Busy or not |

Orthogonal: column, row-within-column, D5 rhythm, D4. Confusable: brightness with colour (a dim red against a yellow in sun), count with position (more than three lit cells spread over columns get counted and not located), group blink with D5's rhythm (two tempos), and **rotation**: the colour layout maps A3↔C1 (red), A1↔C3 (green), A2↔C2 (yellow) under a 180° turn, so only the empty B3 cell and the board's own asymmetry disambiguate the columns. The rising diagonal is rotation-invariant; column identity is not. The steady display totals 27 states (4.75 bits) plus D5's 2.3; that is the whole budget.

## 6. Compatibility test

- **Lockstep cell** (recommended): "The light that blinks like the status LED is in the column that is wrong." Misread: none new; a Margay user who ignores the grid loses nothing.
- **Colour-class rhythm**: "The grid blinks the same rhythm as the status LED, in its colour." Misread: the green chirp as "something changed from blue".
- **Tape**: "Watch the dot climb the column." Misread: motion as a chase or a progress bar.
- **Timeline / Morse**: needs a chart. Fails the one-sentence test.
- **Fill**: "Count the cells." Misread: as a battery gauge.
- **Bar graph**: "The column is how full the cycle is." Misread: as severity, because height means severity everywhere else on the grid.

## 7. Cost and failure

A tape at 100 ms step over 3 s is 30 `LEDOUT` writes at about 0.3 ms each, 9 ms of bus; the lockstep cell is 5–50 writes per window (chirp to flutter). The MCU is already blocked in `delay()` inside `signal()` for the window, so attention is free. Current is boot-only: driver awake 2.5 mA plus a few mA per lit cell (UNVERIFIED: R and Vf not measured) for 3 s, then `SLEEP` and `!OE` high; nothing against the 80 µA field budget. Dead cell: a steady column with its band's cell dead goes dark, which must be defined as a fault read ("no verdict is ever dark" already holds on D5); the diagonal line breaks toward a false alarm, the safe direction; a lockstep cell that is dead leaves D5 saying the same thing; a fill or count is wrong silently, the worst case.

## 8. Verdict

| Lifting | Verdict | Against steady columns |
|---|---|---|
| Lockstep rhythm on the worst column's cell | **Earns a place** | Complement: adds onset pop-out and synchrony binding, no new vocabulary |
| Rhythm on the colour class (diagonal and corners) | Earns a place as the fallback if columns are dropped | Replace, not stack: both want the whole grid |
| Tape | Reject for the verdict; the pips are the one iconic case | Reject |
| Timeline, Morse-in-space | Reject: cells and legibility | Reject |
| Fill / count | Reject: counting, and lies with one dead cell | Reject |
| Bar graph | Not now: cycle fraction is the only measured quantity, and battery has no percentage on Okapi | Defer |

The grid's one real gain over D5 is simultaneity, and the columns proposal spends it well. The rhythm liftings that survive are the ones that leave Margay's time structure intact and give it more area and a position; the ones that convert time into space lose either the shape or the one-sentence explanation.

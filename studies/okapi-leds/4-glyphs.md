I have what I need; no further reads. Here is the report.

# Okapi LED array: glyphs – design note

## Recommendation

**Do not build a glyph alphabet. Keep two glyphs, and they are already in the columns proposal.** A 3×3 grid with the top-middle cell missing cannot draw characters, only a dozen or so shapes, and the fixed colours are laid out so that the only *band-pure* shapes are the per-band cell sets themselves: the three greens are the rising diagonal (A1 B2 C3), the three yellows are a V (A2 B1 C2), the two reds are the ends of the falling diagonal (A3, C1). So "the slash" for READY is the same five-millimetre picture whichever way you derive it, and a glyph scheme for faults collapses back into "which cells of which colour are lit", which is the columns proposal with a learned vocabulary added and simultaneity taken away. Glyphs earn two things as a **complement**: (1) a lamp test, all eight cells lit while the aux LED says "busy", so a dead cell is seen before it corrupts a verdict; (2) per-channel PWM to equalise the three colours' luminance, which the columns proposal also needs but did not say. Sequential glyphs are not worth the window they cost.

## 1. What the grid can draw

Dot-matrix legibility work puts alphanumerics at 5×7 minimum and 7×9 preferred (Snyder & Maddox 1978; MIL-STD-1472 carries the 5×7 floor – clause number UNVERIFIED, from memory). Digits on 3×5 are a hobbyist floor with known confusions (3/8, 5/6). A 3×3 is below any character threshold, and the missing B3 removes every shape with a top-centre: T, +, ↑, Γ, I, 7, 1, the ring, the full caret. What survives is a set of **shapes with names**, not letters; the grid is bottom-heavy and open at the top. The full readable set, from enumeration (256 raw patterns, 19 nameable):

| Glyph | Cells | n | Colours forced | 180° invariant | Note |
|---|---|---|---|---|---|
| the slash / | A1 B2 C3 | 3 | G G G | yes | the only all-green shape |
| the backslash \ | A3 B2 C1 | 3 | R G R | yes | both reds plus centre |
| the X | corners + B2 | 5 | G G G R R | yes | slash ∪ reds |
| the row _ | A1 B1 C1 | 3 | G Y R | no → becomes "the eyes" | a stoplight laid flat |
| the bar – | A2 B2 C2 | 3 | Y G Y | yes | |
| the vee v | A2 B1 C2 | 3 | Y Y Y | no → two dots | the only all-yellow shape |
| the hat ^ | A1 B2 C1 | 3 | G G R | no → top-vee | |
| the top-vee | A3 C3 B2 | 3 | R G G | no → hat | |
| the L | A col + B1 C1 | 5 | R Y G Y R | no → broken Γ | |
| the J | C col + B1 A1 | 5 | G Y R Y G | no | mirror of L |
| the cup U | all but B2 | 7 | 2R 3Y 2G | no | d = 1 from all-eight |
| the H | both cols + B2 | 7 | 2R 2Y 3G | yes | d = 1 from all-eight |
| left / right post | A col / C col | 3 | R Y G | no → the other post | mirror pair |
| the tick ✓ | A2 B1 C2 C3 | 4 | Y Y Y G | no | d = 1 from the vee |
| the eyes | A3 C3 | 2 | R G | no | too sparse |
| the stub | B2 B1 | 2 | G Y | no | too sparse |
| the equals = | rows 1 + 2 | 6 | | no | |
| all eight | | 8 | | no | lamp test only |

The arrows are the real loss: no up, left or right arrow exists without B3, and a down arrow is the vee. "Motion" glyphs are therefore limited to the vee and the two posts.

## 2. Fixed colours

They hurt shape and help band, and the two effects do not cancel. Gestalt similarity grouping segregates by colour (Wertheimer; Beck 1966): a glyph crossing colour boundaries tends to fragment – the L reads as a red-yellow-green post with a yellow-red foot, not as one letter. Luminance compounds it. Green InGaN sits at the V(λ) peak (555 nm), red at ~0.3 of it, yellow ~0.75; and the forward voltages differ (red/yellow ~2.0 V, green ~3.0 V), so a common series resistor from 3V3 drives the green at a fraction of the red's current (resistor value and parts UNVERIFIED – not in the BoM, which predates the array). A mixed glyph will look like two bright cells and a dim one until the PWM registers are calibrated per channel, which the PCA9634 does at 97 kHz with no visible flicker (datasheet figure, UNVERIFIED). **Calibrate once at boot, eight PWM bytes in one auto-increment write.** For deuteranopes and protanopes, red, yellow and green lie near one confusion line, so colour carries nothing and the shape is what remains; that is the strongest argument *for* a glyph – but the columns proposal already carries band as position, so glyphs add robustness only where columns would rely on colour alone, which they do not.

## 3. The mapping

D5 already names READY, card (all three), clock, sensor and schedule, and lumps eight CAUGHT messages into one amber rhythm. A glyph adds information only where D5 is ambiguous and the technician's *action* differs. Grouped by action:

| Action group | Messages | Glyph | Why this shape |
|---|---|---|---|
| nothing | READY | the slash (G G G) | all-green, 180° safe, iconic rising line |
| reseat or replace card; look at file | CARD_*, ROW_NOT_WRITTEN, NOTE_TRUNCATED, NEW_FILE | the row (G Y R) | "a data row", the stoplight laid flat |
| bring cells or a laptop | BATTERY_LOW, ONBOARD_MISSING, PAGE0_INVALID | the cup (7 cells) | a cell outline, open at the top |
| fix time or schedule | CLOCK_NOT_SET, NO_SCHEDULE, CYCLE_OVERRAN, BACKUP_WOKE | the X | "wrong"; 5 cells, 180° safe |
| check wiring and sensors | SENSOR_MISSING, BME_MISSING | the vee (Y Y Y) | all-yellow, points down at the terminals |
| none – diagnostic | lamp test | all eight | before the verdict, while aux is on |

Five glyphs plus the test. The working set's minimum pairwise distance is 2 (slash ⊂ X: two dead reds turn an X into a slash); every other pair is ≥ 4; computed over the 8-bit patterns. Two defects, computed: the cup is distance 1 from all-eight (lamp test minus B2 looks like the cup), and the row rotates into the eyes. If the lamp test is adopted, replace the cup with the H or drop the power glyph.

This is the honest ceiling of what glyphs add: the CAUGHT split by action. The columns proposal gets the same split by *position* with printed labels and no learning.

## 4. Sequential glyphs

Reading a familiar shape takes ~150 ms (Thorpe et al. 1996); to name and retain it, hold ≥ 500 ms (Potter 1976 RSVP: detection near 113 ms, memory needs several hundred). Between glyphs a dark gap prevents the change reading as motion: apparent motion persists at ISIs up to ~200–400 ms (Wertheimer 1912; Korte's laws), the Ternus display gives group motion around 100 ms ISI, and a shape change with no gap is seen as a morph (Tse, Cavanagh & Nakayama 1998). **Gap ≥ 400 ms.** Three glyphs at 600/400 fill 3.0 s exactly; two at 1100/400 leave margin. A two-character "band then identity" code gives 24 codes, but the band is already on D5 and in the colours. The real cost: a sequence does not repeat inside 3 s, so the late glance that Margay's cycling rhythms rescue catches only the last glyph. The one use that survives is showing the hidden second fault – worst-first, one glyph per raised message – and the columns show that in space with no sequencing.

## 5. Scanning

Rows at < 20 ms each fuse at the critical flicker frequency into a whole glyph, which is multiplexing for no reason (the PCA9634 holds all eight statically). Rows at 100–300 ms each read as a wipe: attention, not content, and the partial frames are glyphs themselves (the L's first row *is* the row). Scanning adds nothing to legibility. Show whole, hold still.

## 6. Cognition

Location and a lit-among-dark cell are preattentive (Treisman; Hasher & Zacks 1979); so is a break in a collinear line (Field, Hayes & Hess 1993). Closure fills small gaps, not a third of a side: the cup is a cup, not a ring. Abstract symbol comprehension without training is poor – ISO 9186's acceptance criterion is 66 % correct and many abstract pictorials fail it (Wolff & Wogalter 1998; figures UNVERIFIED) – so a glyph is held only if its name is its meaning ("the row", "the cup"). Margay's five rhythms already load the technician; five glyphs doubles the vocabulary. Confusion under one dead LED: vee ↔ tick, top-vee ↔ eyes, cup/H ↔ all-eight; the working set has none at distance 1 except via the lamp test.

## 7. Cost

One glyph is one auto-increment write to LEDOUT0/LEDOUT1 (2 data bytes, ~38 bit-times, 0.4 ms at 100 kHz); wake needs MODE1 and 500 µs. Three glyphs plus off: six writes, under 3 ms of bus time in a window `signal()` already spends in `delay()`, so MCU attention is free at rhythm boundaries; a glyph change *mid*-rhythm requires rewriting `signal()` as a timeline. Current: ~2.5 mA for the driver awake plus 2–6 mA per lit cell (UNVERIFIED), 40 mA worst for the 7-cell cup, three seconds; then SLEEP and `!OE` high. The lamp test is one write and ~300 ms.

## 8. Failure modes

A dead cell: handled by distance ≥ 2 and by the lamp test, since the PCA9634 has no open-load detection (UNVERIFIED; the PCA9955 does). The missing cell is a fiducial: upside down, the gap sits at the bottom and the colours (180°-symmetric except B1/B3) land on the same colours, so only shape and gap tell orientation. The slash, backslash, X, bar and H are rotation-invariant; the row, vee, L, posts and cup are not. Prefer invariant glyphs or accept the gap as the cue.

## 9. Verdict

Complement, not alternative. The glyph analysis confirms the columns proposal's READY line (it is the slash), adds the lamp test and the PWM equalisation, and shows that the fault glyphs reduce to "the CAUGHT split by action" – which the columns deliver by position, simultaneously, with no vocabulary and no sequence. Glyphs lose on three counts: forced colour mixing fragments shape, a sequence forfeits the late-glance rescue, and learning cost doubles. Should a future board ever carry a full 3×3 or a 3×5, the arrows and a digit set come back and this answer changes.

# Okapi LEDs: motion – a design note

## Recommendation

**Reject motion as the carrier of the boot verdict; keep the three steady columns and D5's Margay rhythm.** Motion's one real asset on this grid is *liveness*: a changing display is the only light that proves the MCU is running and not hung, and that is worth having during a wait of minutes, not a verdict of 3 s. The one pattern worth adopting is a **green diagonal shuttle (A1–B2–C3) during the 180 s modem wait** – but only if the first backhaul is moved to the boot row. Verified (`Okapi_Library/src/Okapi.cpp:262`, `Okapi.h:244`): today the backhaul runs after the fifth alarm-driven row, not at boot, so a modem-wait display of any kind has no observer until that changes. That is Andy's decision, and the shuttle is conditional on it. One iconic verdict pattern, the SENSOR_MISSING ping, is recorded as the best of the rest and still rejected, because it would blank the columns.

## 1. Would a technician see motion at all?

At 0.3–0.5 m the horizontal pitch (2.667 mm) subtends 0.31–0.51° (18–31 arcmin) and the vertical (2.032 mm) 0.23–0.39° (14–23 arcmin). That sits at or just beyond Braddick's (1974) short-range limit (Dmax ≈ 15 arcmin, ISI ≲ 80 ms), so a step between cells is handled by the long-range process, which tolerates larger jumps and longer intervals and is what Wertheimer measured. Wertheimer's (1912) three regimes, as usually summarised: ISI below ~30 ms the two lights look simultaneous; ~60 ms gives optimal beta movement (one object seen to travel); above ~200 ms they read as succession, two flashes in two places. Korte's laws say a wider step wants a longer interval; Kolers (1972) found the optimum roughly flat in separation at these small angles (my recollection of Kolers – UNVERIFIED in detail). Practical bands for this grid: **frame 60–120 ms with ISI 0–60 ms reads as a moving dot; frame ≥ 250 ms or ISI ≥ 200 ms reads as stepping; ISI < 30 ms with overlapping frames reads as a line.** Two frames suffice to see direction (that is the phi phenomenon itself), so three cells carry direction reliably. What three cells cannot carry is *shape*: a 3-cell line, L and arc are told apart only by remembering where the cells are.

## 2. How much can motion say?

Enumerate the grid's alphabet. Full 3-cell lines: columns A and C, rows 1 and 2, both diagonals (A1–B2–C3 is all green; A3–B2–C1 is red–yellow–red). Column B and row 3 are 2-cell. The ring around B2 has seven cells, broken at B3, and reads as a horseshoe. Dimensions available: direction (2 per line), path (6 lines, ring, centre–ring), fill vs chase (a fill leaves a trail; reliably distinct), expand vs contract, rotation sense, dot count (1–2; Ternus grouping makes two dots at ISI > ~50 ms read as a group, not two objects). Speed: smooth-motion Weber fractions are ~5–10 % (McKee 1981), but a technician identifies a tempo from memory with no comparison, and absolute identification of a single dimension saturates near 2–3 bits (Miller 1956); for tempo without a reference I would trust **two speeds**, slow (~2 Hz) and fast (~8 Hz), no more. Combinatorially the grid offers ~30 motion words. Reliably recalled unaided, 3 s after a glance, by someone who learned them from a card: **6–8**, the same order as Margay's five rhythms. They would be additional learning on top of the rhythms, with nothing new to say: the 20 messages reduce to about six actions (reseat card, bring a laptop for the clock, check sensor wiring, check battery, fix the schedule, nothing), and columns plus D5 already separate those.

## 3. Metaphors people already read

The honest list of messages with a natural motion icon that the geometry supports: **SENSOR_MISSING** (centre B2 flashes, ring flashes, nothing returns – the grid is literally a centre and a ring), **busy/searching** (a shuttle or sweep: the KITT scanner, the spinner), **progress** (a fill). The others do not survive eight LEDs: CYCLE_OVERRAN as a fill overflowing into the empty B3 is a joke only its author gets; BACKUP_WOKE and the INTERVAL pair are field messages with no observer under the settled rule and never render anyway. Heartbeat/breathing needs the MCU to ramp GRPPWM every frame; the hardware gives only on/off group blink unaided.

## 4. Attention versus message

Motion pops out preattentively (Nakayama & Silverman 1986; Dick, Ullman & Sagi 1987), and *motion onset* in particular captures attention (Abrams & Christ 2003). That is the right tool for a display meant to catch a technician who is packing gear 2 m away, and the wrong tool for a verdict that the technician is already staring at. The verdict has a guaranteed observer and 3 s; motion spends that time presenting serially what the columns present at once, and the previous note's point stands: `worstMessage()` hides a second fault, and only simultaneity repairs that. Alarm fatigue does not arise for a progress display shown once per boot. The SD write (tens of ms) is too short for any motion.

## 5. Compatibility with Margay's rhythms

Rhythm and motion are mutually exclusive regimes of the same ISI axis. Margay's identities live in gaps of 100–500 ms, which is Wertheimer's succession band: spatialise the chirp (A1 1000, dark 300, B2 100, dark 100, C3 100) and the eye sees long-short-short *in three places*, not a dot travelling – the rhythm survives and the motion never happens. Compress the gaps to make it move and the rhythm is gone. The one exception is the card flutter: 60/60 is already a 120 ms SOA, so the same timing carried around the ring is a clean spinner. It would be in lockstep with D5's flutter, but a Margay eye reads the flutter from D5 regardless, and the spinner adds nothing the steady red A3 does not. Spatialising a rhythm does not destroy it; it adds nothing, at the cost of the columns.

## 6. Fixed colours

A sweep up column A runs green→yellow→red, a thermometer; up column C runs red→yellow→green, the inverse. Any pattern that crosses columns changes colour arbitrarily, which a trichromat reads as meaning and a deuteranope does not see. The only colour-stable paths are the green diagonal and the red–yellow–red one. **Use the all-green diagonal for anything that moves**, and nothing else: colour then says "fine" throughout and position carries the rest.

## 7. Cost

No hardware motion exists: group blink (GRPFREQ, period 41 ms–10.73 s, UNVERIFIED exact formula) blinks all LDRx = 11 channels together. Every frame is one auto-incremented write of LEDOUT0 + LEDOUT1 (4 bytes, ~0.4 ms at 100 kHz). At 60 ms frames that is <1 % bus duty. The verdict is blocking today, so a verdict animation would use `delay()` like `signal()`. The modem wait is a busy-poll on `FeatherGPIO` (`Okapi.cpp:291`), so a `millis()` frame check drops into that loop with no timer. Power: driver awake ~2.5 mA plus one LED (~6 mA, estimated) at 50 % duty ≈ 5.5 mA for ≤ 180 s, ≈ 0.3 mAh once per boot, against the Boron's 16–40 mA for the same interval.

## 8. Failure modes

A dead middle cell turns the shuttle into two alternating flashes at 240 ms SOA, still readable as motion; a dead end cell shortens it. A ring sweep acquires a second gap and its sense becomes ambiguous. Board upside down: the diagonal shuttle is symmetric under 180° rotation (A1 ↔ C3), the only pattern on the grid that is; vertical fills invert, and the horseshoe rotates its gap to the bottom.

## 9. Verdict and frame tables

**Rejected at the boot verdict.** Steady columns stay. For the record, the best verdict candidate and why it loses:

Ping for SENSOR_MISSING (×4, 2.8 s; conflicts with the columns, which it blanks – not adopted):

| t (ms) | LEDs | Cell |
|---|---|---|
| 0–100 | LED3 | B2 |
| 100–200 | LED0, 1, 2, 4, 5, 6, 7 | ring |
| 200–700 | – | dark |

**Adopt, conditional on the first backhaul moving to the boot row:** the busy shuttle, running from `FeatherEN` HIGH until `FeatherGPIO` falls or the 180 s timeout, then LEDOUT = 0, SLEEP, `!OE` high. ISI 60 ms is Wertheimer's optimum and halves LED current.

| t (ms) | LED | Cell |
|---|---|---|
| 0–60 | LED5 | A1 |
| 60–120 | – | dark |
| 120–180 | LED3 | B2 |
| 180–240 | – | dark |
| 240–300 | LED0 | C3 |
| 300–360 | – | dark |
| 360–420 | LED3 | B2 |
| 420–480 | – | dark, then repeat (period 480 ms, ~2 Hz) |

It complements the columns in a different phase and touches no D5 rhythm, so a Margay-trained eye sees nothing new. If `_logCountPush` stays at 5, the shuttle has no observer and the field stays dark as on Margay.

---

**Summary.** Motion loses the boot verdict on the evidence: at 0.3–0.5° per cell a 60–120 ms step does read as a moving dot, but three cells carry direction and little else, a technician can recall perhaps six to eight motion words unaided, and every one of them costs the simultaneity that lets three steady columns show two faults at once. Margay's rhythms cannot be spatialised into motion without destroying them, because rhythm lives at ISIs above 200 ms and motion below 100. What motion uniquely offers is proof of life, and the right place for that is the 180 s modem wait: a green A1–B2–C3 shuttle at 60/60 ms, colour-stable, rotation-symmetric, under 1 % bus duty and about 0.3 mAh per boot. Its value depends on a firmware fact verified today – the backhaul first runs after the fifth row, not at boot – so adopting it means pulling the first push to the boot row, which is Andy's call.

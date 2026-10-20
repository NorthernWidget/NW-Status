# Cognitive-science review: what each LED on Margay and Okapi should earn

## Verdict

The literature supports a **dark-by-default grid with a boot-time lamp test**, and it does not support lighting "fine" cells or doubling a message across two blinking lights. Point by point:

| Question | Verdict | Load-bearing evidence |
|---|---|---|
| (a) Light "fine" cells beside fault cells | **No.** No evidence of help; several costs. | Smith & Goodwin 1971: blinking the target class cut search time 50 %, but blinking *all* items gave no gain over a steady display. Treisman & Souther 1985: presence of a feature pops out, absence does not – a lit cell among dark ones is the easy search. Jonides & Yantis 1988: static colour singletons do *not* capture attention; abrupt onsets do. Birch 2012: red–green deficiency in ~8 % of Northern-European men, so a red-among-green grid is unreadable to roughly one visitor in twelve. Rosenholtz 2007: clutter is literally "how hard it is to add an item that reliably draws attention". Parasuraman & Riley 1997: when the base rate of faults is low, a display that is mostly green trains the user to stop reading it. |
| (b) A second light blinking in time with the first | **Not as redundancy.** Supported only if the two lights carry *different* facts. | Miller 1982: the redundant-signals effect is a reaction-time gain of tens of milliseconds (magnitude UNVERIFIED for this geometry) – irrelevant against a 3 s window. Wickens' redundancy gain is about coding one fact on two *dimensions* (position + hue in a traffic light), which serves colour-deficient viewers; a synchronous copy of the same rhythm adds no dimension. Let the cell say *which* (position) and the status LED say *how bad* (colour + rhythm). |
| (c) Dark grid when nothing is wrong | **Yes.** | Airbus dark-cockpit (since A300B4/A310, early 1980s): "no light = normal", so every lit lamp demands action. EEMUA 191: fewer than 10 standing alarms per operator; ISA 18.2: a stale alarm (>24 h) is a defect to remove. Treisman & Gelade 1980 / Treisman & Souther 1985: one lit target among dark distractors is a flat-slope, one-fixation search. |
| (d) Lamp test during boot | **Yes – it is the price of (c).** | Annunciator practice (ISA 18.1 era): a lamp-test button was always fitted because a dead lamp reads as "normal". Eastern 401 (1972): a burned-out gear-indicator bulb cost 101 of 176 lives via distraction and ambiguity; the gear was locked down the whole time. A full-grid flash while the aux LED says "booting" resolves "dark = fine" from "dark = dead" once per visit. |

Where the science is thin: no study measures labelled-position against learned-rhythm head-to-head for subsystem identification (UNVERIFIED – not found), and no field study of blink-code recall by infrequent users was located. The verdict on rhythm count below is therefore reasoned from Miller 1956 and Markowitz 1971, not measured.

## 1. The cost of a signal that carries nothing

| Finding | Number | Source |
|---|---|---|
| People match response rate to alarm reliability | 138 subjects; 25/50/75 % true alarms; ~90 % probability-matched, ~10 % all-or-none | Bliss, Gilson & Deaton 1995, *Ergonomics* 38:2300 (PubMed abstract) |
| One false alarm halves the fear response to the next | "close to fifty percent" | Breznitz 1984 (secondary summaries; primary figure UNVERIFIED) |
| Clinical monitor alarms needing no intervention | 85–99 %; 72 papers reviewed | Cvach 2012, *Biomed Instrum Technol* 46:268 |
| Operators disable high-false-rate alarms | – (qualitative) | Sorkin 1988, *JASA* 84:1107 |
| Low base rate + fixed threshold → false-alarm-dominated experience → disuse | – (argument) | Parasuraman & Riley 1997, *Human Factors* 39:230 |

The transfer to a status grid: a green "fine" cell is a signal whose information content is near zero on almost every visit. Bliss's subjects did not ignore alarms out of laziness; they calibrated to the true rate. A grid that is 90 % green teaches the eye that the grid is green.

## 2. Redundancy gain versus clutter

| Finding | Number | Source |
|---|---|---|
| Redundant print + voice warning compliance | 76 % vs 42 % print, 64 % voice | Wogalter & Young 1991, *Ergonomics* 34:79 |
| Blink on target class speeds search; blink on everything does not | 50 % faster vs no significant difference | Smith & Goodwin 1971, *Human Factors* 13:283 |
| Flashing a subclass at 3 Hz; no slowing of unflashed items | 48 % shorter search | van Orden, Divita & Shim 1993, *Human Factors* 35:2 |
| Feature search slope vs serial | ~0 ms/item vs 20–40 ms/item | Treisman & Gelade 1980 |
| Changes to attended objects go unnoticed without an attention cue | – | Rensink, O'Regan & Clark 1997; Simons & Levin 1997 |

Redundancy helps when the second channel reaches a *different* resource (Wickens 2002: modality, code, focal/ambient) or protects against a deficit (colour deficiency). It hurts when it raises feature congestion (Rosenholtz 2007) or removes the contrast the signal depends on (Smith & Goodwin). The direct answer to "does a fine light help the broken one be found": for a normal-vision viewer, red-among-green is still a flat-slope colour search, so it does not *hide* the fault, but nothing in the literature says it helps, and the dark-cockpit, clutter, colour-deficiency and base-rate results all count against it.

## 3. Minimal signalling and the null signal

Dark-cockpit reasoning is explicit: no light means the system is doing what it should; a lit button means off, failed or overridden (Airbus; Boeing's "quiet and dark" uses white lights the opposite way, which is itself a warning about convention). The requirement is a lamp test, because the design makes "healthy" and "dead" the same picture. Eastern 401 is the canonical dark-indicator ambiguity. EEMUA 191 and ISA 18.2 give the same rule for process control: standing alarms under 10, stale alarms zero, ~1 alarm per 10 min.

## 4. How much a glance takes in

| Finding | Number | Source |
|---|---|---|
| Subitising range and slopes | ≤4 items at 40–100 ms/item; beyond that 250–350 ms/item and error-prone | Trick & Pylyshyn 1994, *Psych Rev* 101:80 (term coined Kaufman et al. 1949) |
| Visual working memory | ~4 integrated objects (colour + orientation stored together) | Luck & Vogel 1997, *Nature* 390:279 |
| Chunk capacity across domains | ~4 | Cowan 2001 |

Implication: one blinking RGB plus eight *steady lit* cells is nine objects, past the subitising range, and the viewer must count during the same 3 s they are decoding a rhythm. One RGB plus the one or two cells that are actually faulting is within range. Lamp-test "all lit" is a texture judgement, not a count, so it is cheap.

## 5. Position as identity

Hasher & Zacks 1979 claimed spatial location is encoded automatically; later tests (Naveh-Benjamin 1987/88; Andrade & Meudell 1993) found it depends on intention, load and age. Location is cheap, not free. Preattentive search (Treisman & Gelade 1980; Wolfe's Guided Search) gives a labelled lit position in one fixation (~200–300 ms). No head-to-head study against rhythm was found (UNVERIFIED); the time advantage follows from construction, since a rhythm cannot be read in less than one period.

## 6. Rhythm as identity

| Finding | Number | Source |
|---|---|---|
| Absolute judgement on one dimension | ~2.5 bits ≈ 6 categories before confusion | Miller 1956 |
| Judging steady vs flashing | viewer waits out one expected off-period before deciding | Markowitz 1971, *Human Factors* 13:427 |
| Light-gun vocabulary every pilot must know | 6 signals (2 colours × steady/flash, flashing white, alternating) | FAA AIM / ATC light-gun chart |
| IALA rhythm classes | ~10 (F, Iso, Oc, Fl, LFl, Q, VQ, UQ, Mo, Al plus groups) – read against a chart, not from memory | IALA E-110 |
| OBD-I blink codes | two-digit counts of long/short flashes, decoded from a table | automotive sources |
| Morse to 12 wpm | 26 characters in ~14 h (Koch; secondary) | Koch method summaries |

Five rhythms sit under Miller's ~6-category ceiling, and aviation runs six. The ceiling is for *trained* users; mariners and mechanics use a lookup table. A rhythm is safe only if it is also carried by colour and resolves within about one second (Markowitz), and the file remains the lookup table.

## 7. Sunlight and the field

| Finding | Number | Source |
|---|---|---|
| Indicator luminance contrast | ≥2.0 within the indicator; sunlight-readable symbols ≥50,000 cd/m² against ≥34,000 cd/m² background | MIL-STD-1472 F/G (clause version UNVERIFIED) |
| Display contrast | ≥3:1 minimum, 10:1 preferred | ISO 9241-303 |
| Warning flash rate | 3–5 Hz, 50 % duty; at most two rates ≥2 Hz apart; slow rate ≥0.8 Hz | MIL-STD-1472 |
| Bloch's law critical duration | 30–100 ms (luminance × time constant below it) | Webvision |
| Flicker fusion / peak sensitivity | ~60 Hz photopic / 15–20 Hz | Webvision; DOE flicker review |
| Flashing vs steady conspicuity | equal at high contrast; flashing far better at low contrast; steady lights missed more and acquired slower | Gerathewohl 1953, *JOSA* 43:567; NASA 1975 |

The 20 ms "row written" blip is below Bloch's critical duration, so it is seen on luminance × time: it needs roughly five times the luminance of a 100 ms flash for equal visibility, and in sun it will be the first cue lost. A flashing fault indicator buys conspicuity exactly where sun erodes contrast.

## 8. Principles for the one-LED and nine-LED vocabulary

1. **Every lit lamp means act** (dark cockpit; Bliss 1995; Parasuraman & Riley 1997). No green cells.
2. **The grid is dark unless something is wrong; boot lights it all** (annunciator lamp test; Eastern 401).
3. **Position says which, the status LED says how bad; neither duplicates the other** (Wickens redundancy on different dimensions; Smith & Goodwin 1971).
4. **Keep the lit set within four** (Trick & Pylyshyn 1994; Luck & Vogel 1997). If more than three subsystems fault, light them and let the file carry the rest.
5. **Hold rhythms at five or fewer, each also colour-coded and resolving within a second** (Miller 1956; Markowitz 1971; 8 % colour-deficient viewers need the rhythm, the rest need the colour).
6. **Use flashing for faults and steady or nothing for status** (Gerathewohl 1953; van Orden 1993; MIL-STD-1472 rates).
7. **Treat the 20 ms blip as a shade-only cue, or lengthen it toward 100 ms** (Bloch's law).

Sources: [Bliss et al. 1995](https://pubmed.ncbi.nlm.nih.gov/7498189/) · [Cvach 2012](https://www.ovid.com/journals/bitye2/fulltext/00002644-201207000-00013~monitor-alarm-fatigue-an-integrative-review) · [Sorkin 1988](https://www.semanticscholar.org/paper/FORUM:-Why-are-people-turning-off-our-alarms-Sorkin/90a2d86b07fac72b3e1ca223f4e7e12eba76155a) · [Breznitz 1984](https://www.routledge.com/Cry-Wolf-The-Psychology-of-False-Alarms/Breznitz/p/book/9780898592962) · [Parasuraman & Riley 1997](https://scispace.com/papers/humans-and-automation-use-misuse-disuse-abuse-4z7c2r6dfn) · [Miller 1982 / race model](https://link.springer.com/article/10.3758/s13414-015-1017-z) · [Wogalter & Young 1991](https://www.safetyhumanfactors.org/wp-content/uploads/2020/07/41)Wogalter,Young(1991).pdf) · [Smith & Goodwin 1971](https://doi.org/10.1177/001872087101300309) · [van Orden et al. 1993](https://pubmed.ncbi.nlm.nih.gov/8349285/) · [Treisman & Souther 1985](https://moodle2.units.it/pluginfile.php/379169/mod_resource/content/0/TreismanSouther1985.pdf) · [Yantis & Jonides](https://link.springer.com/article/10.3758/BF03208805) · [Rosenholtz et al. 2007](https://jov.arvojournals.org/article.aspx?articleid=2122001) · [Rensink et al. 1997](https://philarchive.org/archive/RENOFT-2) · [EEMUA 191 benchmarks](https://www.emerson.com/documents/automation/alarm-management-by-numbers-en-38292.pdf) · [Dark cockpit](https://aviaproconsulting.com/article/post/engineering-spotlight-the-ergonomics-of-annunciation-%E2%80%93-airbus-lights-out-vs-boeing-quiet-and-dark) · [Annunciator lamp test](https://en.wikipedia.org/wiki/Annunciator_panel) · [Eastern 401](https://en.wikipedia.org/wiki/Eastern_Air_Lines_Flight_401) · [Trick & Pylyshyn 1994](https://www.semanticscholar.org/paper/Why-are-small-and-large-numbers-enumerated-A-stage-Trick-Pylyshyn/eeb310b29a5e13fabc138671b1bf9a549bee9d0a) · [Luck & Vogel 1997](https://www.semanticscholar.org/paper/The-capacity-of-visual-working-memory-for-features-Luck-Vogel/b418eca76c6557eccfd97caa8bb5a5c4cdc0a9a5) · [Hasher & Zacks challenges](https://link.springer.com/article/10.3758/BF03214224) · [Miller 1956](https://labs.la.utexas.edu/gilden/files/2016/04/MagicNumberSeven-Miller1956.pdf) · [Markowitz 1971](https://pubmed.ncbi.nlm.nih.gov/5113998/) · [FAA light gun](https://www.faa.gov/airports/runway_safety/publications/ATC-Light-Gun-Signals-for-Pilots.pdf) · [IALA E-110](https://www.iala.int/content/uploads/2017/03/E-110-Ed.4-Rhythmic-Characters-of-Lights-on-Aids-to-Navigation_16Dec2016.pdf) · [MIL-STD-1472G](https://mreed.umtri.umich.edu/Anthro/MIL-STD-1472G.pdf) · [ISO 9241-303](https://cdn.standards.iteh.ai/samples/40098/b047ecc057b9478e868875b86f692f44/ISO-9241-303-2008.pdf) · [Bloch / CFF](https://www.ncbi.nlm.nih.gov/books/NBK11559/) · [Gerathewohl 1953](https://opg.optica.org/josa/abstract.cfm?uri=josa-43-7-567) · [NASA 1975 flash conspicuity](https://ntrs.nasa.gov/citations/19750023659) · [Birch 2012 CVD prevalence](https://www.researchgate.net/publication/223985289_Worldwide_prevalence_of_red-green_color_deficiency)

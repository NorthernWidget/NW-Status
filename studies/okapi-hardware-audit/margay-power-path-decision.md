# Margay's power path: the decision and the proposed redesign

2026-11-09. Andy: "Your findings validate the diode." This note records how the decision was
reached and what the new power path is. The detail behind each step is in the notes it names.

## 1. The finding

The capacitor review asked whether VMAIN, the output of U9 (TPS2104, the switch between the
battery and USB), carries enough capacitance through the TPS2104's switchover; the datasheet
recommends 220 µF for 100 mA loads, and Margay has 1 µF (C13). Tracing U9's control showed the
capacitor is not the limit. U9 selects its input only from EN, which comes from U10 (TLV3691)
comparing 3V3_FTDI with VBAT_SW/2. Q2 holds 3V3_FTDI at the core's 3.3 V until VUSB falls below
Q3's gate threshold, so U9 reaches for the battery only after VUSB, and VMAIN with it, has fallen
to about 2 V. 3V3_AUX (the SD card, the J2 sensors, the RTC's VCC) drops out at every USB unplug
while it is on, whatever the capacitance. (`margay-vmain-switchover.md`)

Bobby's 2019 commits call the topology unfinished ("Changed auto power switch topology, cleanup
desired", 8ca38a5). The design is right in both steady states; the comparator's inputs were kept
under its 3.3 V supply (TLV3691: inputs to (V+) + 0.1 V), and the FTDI's 3.3 V rail served as a
"USB present" flag that Q2 makes outlast USB itself.

A second fact came with it: with no battery, Margay's whole core runs from the FT231X's internal
regulator through Q2, rated "a maximum current of 50mA".

## 2. The options

1. Re-point U10 at a VUSB divider (k about 0.6, with a 1 MΩ feedback resistor for a 0.33 V
   hysteresis band). Two resistors, no added sleep current, and a clean handover once VMAIN has
   a bulk capacitor sized at about 0.79 µF effective per mA of 3V3_AUX load. The core stays on
   the battery, and USB alone still runs the core from the FTDI's 50 mA regulator.
2. A power multiplexer (TPS2116) upstream of both regulators: true USB priority, 1.32 µA
   typical quiescent current.
3. Two LM66100 ideal diodes upstream of both regulators: USB powers everything, a clean
   handover, about 0.35 µA in sleep, and the battery wins only when it sits above USB.

## 3. What decided it

**Sleep current is not the constraint.** Andy's typical deployment measures every 5 minutes for
about 3 s, with the logger at 8.6 mA awake and sensors up to 20 mA more. Sleep carries under 2 %
of the energy, and option 3 adds under 0.4 % to the average current; even hourly with light
sensors it adds about 3 %. (`margay-power-path-topic.md`)

**The standard packs sit below USB.** Margay's standard and recommended packs are alkaline AA
and D. A fresh alkaline cell is about 1.6 V open-circuit (Energizer's handbook; spread 1.56-1.65
V), so a fresh 3-cell pack is 4.68-4.95 V unloaded and 4.46-4.80 V under light load, below a 5 V
USB port. The ideal-diode pair therefore gives USB priority with the packs Margay is meant to
use. Fresh lithium AAs (5.37-5.49 V) would carry the board ahead of USB, and they are not a
recommended pack. (`sources/2026-11-09-fresh-aa-voltages-agent-report.md`)

**Decision (Andy, 2026-11-09): the LM66100 ideal-diode pair**, option 3, for Margay v3.1.0.
Andy's weight on it: freeing the core from the FT231X's 50 mA regulator, "because otherwise
there could be unexpected failures when running off of USB".

## 4. The proposed power path

TI's "Dual Ideal Diode ORing for Continuous Output Power" (LM66100, SLVSEZ8A §9.2.2, Figure 17),
adapted (`margay-power-path-lm66100.md`):

```
   VUSB ─── U_A LM66100 ──┐
            CE ← VBAT+    │
            ST ─┬─ 10k to VUSB
                │         ├── VSYS ──┬── U6 TPS797 → 3V3 core (always on)
   VBAT+ ── U_B LM66100 ──┘          └── U7 TPS7A05 → 3V3_AUX (EN from the MCU, as now)
   (after Q1)   CE ← U_A's ST
```

- Removed: U9 (TPS2104), U10 (TLV3691), R17, R18 and the VMAIN net.
- Kept: Q1 for reverse polarity; U8 (TPS22916) with R22/R23 to measure the battery, since VSYS
  no longer reports it.
- Added: two LM66100, three 10 kΩ resistors (R_PU and two series R_CE), and a 10-22 µF bulk
  capacitor on VSYS (27 µF effective covers 200 mA through a 40 µs turn-on with 0.3 V droop).
- To change with it: the FT231X's 3V3OUT leaves 3V3_FTDI, so the core regulator and the FTDI's
  regulator no longer drive one node; VCCIO and RESET# stay behind Q2.

## 5. Open

1. The input voltage rating built from every part on VBAT+ and VUSB (agent running:
   `sources/2026-11-09-margay-voltage-rating-agent-report.md`), and whether the documentation
   already warns against lithium cells (not found in Project-Margay's README, docs or guides).
2. The FT231X configuration against FTDI's self-powered design.
3. The RTC conversation (QUEUE, desk item 14): VSYS is a candidate feed for the RTC's battery
   input.
4. The milestone: Margay v3.1.0 (Andy, 2026-11-09); filed as Project-Margay #66.
5. Bench: today's switchover on a built board, then the new path's handover under an SD write.

## 6. Details settled after the decision (2026-11-09)

**The source switch is the LM66100 pair itself**, with no control net: U_A conducts while USB
clears the battery, U_A's ST holds U_B off, and U_B takes over when U_A lets go. The MCU keeps
3V3_AUX on and off through U7's EN (3V3_AUX_CTRL) as now; U8 only gates the battery-sense
divider.

**The Vs output.** JP2 picks Vs's source for U11 (MIC94090): pin 1 is VMAIN today, pin 3 is
3V3_AUX. Pin 1 moves to VSYS. U11 is enabled by the MCU, as now. Unlike VMAIN, VSYS is live in
sleep, so U7 and U11 now sit on a powered rail while off: U7's shutdown current is 100 nA
typical, 300 nA maximum at 25 °C (TPS7A05, SBVS254D); U11's is 0.01 µA typical, 1 µA maximum
(MIC94090, from the MIC94090-MIC94095 datasheet DS20006706B). The sleep budget becomes about 0.46 µA typical (0.35 µA for the pair
plus 0.11 µA), under 0.6 % of the typical 5-minute deployment.

**The VSYS capacitor, -40 to +85 °C.** The gap is U_B's turn-on: about 41 µs at -40 °C with
3.6 V in, 37 µs at +85 °C, 25-28 µs at 5 V (LM66100 Figure 8, read by eye), plus ST's 1 µs
and U_A's turn-off of about 2 µs (Figure 9): 44 µs. VSYS starts the gap about 0.1 V below the
battery (U_A turns off within 0-80 mV of it, less its on-resistance drop) and must stay above
3.512 V, the TPS7A05's 3.3 V plus its 212 mV maximum dropout at 200 mA over -40 to +85 °C.
U_B's body diode (0.5 V typical, 1.1 V maximum at 10 mA) is a floor beneath that and is not
counted. Effective capacitance needed, C = I x 44 µs / ΔV:

| Battery | 30 mA (typical) | 210 mA (3V3_AUX full + core) | 710 mA (+ Vs at 500 mA) |
|---|---|---|---|
| 4.5 V | 1.5 µF | 10.4 µF | 35.2 µF |
| 4.2 V | 2.2 µF | 15.7 µF | 53.1 µF |
| 4.0 V | 3.4 µF | 23.8 µF | 80.5 µF |
| 3.8 V | 7.0 µF | 49.1 µF | 166 µF |

Worst-case effective value per part (X5R ±15 % over -55 to +85 °C, -20 % tolerance, DC bias at
5 V from Murata's data): a 22 µF 0805 (GRM219R61C226ME15L) about 5.2 µF; a 100 µF 1206
(GRM31CR61A107MEA8L, Okapi's C43) about 23.7 µF. Proposal: **two GRM31CR61A107MEA8L** (47 µF
worst-case effective), the same line as Okapi's C43. They carry 210 mA to a 3.9 V pack and the
full Vs load to about 4.4 V at every temperature in the range. A polymer bulk capacitor is ruled out on VSYS: it is live in
sleep, and a polymer's leakage (tens of µA) would dwarf the logger's sleep current.

**USB inrush with no battery.** Plugging USB into a board with no battery charges VSYS from 0 V:
two 100 µF parts hold about 70 µF effective at 5 V, about 350 µC, where the USB limit is about
50 µC (10 µF at 5 V; USB 2.0 §7.2.4.1, from memory, to check). The LM66100 turns on in about 27
µs and does not limit the slew. With a battery fitted, VSYS only steps from the battery to USB
(0.2-0.5 V, 14-35 µC). Options: a slew-controlled switch ahead of U_A, or accept the overshoot
of the USB limit in the battery-less case. Open.

## 7. USB inrush (2026-11-09, two agent reports in `sources/`)

**The rule.** Margay is an Rd-only USB-C sink with USB 2.0 data, so Type-C defers to USB 2.0
(Type-C R2.5 §4.6.2.1). USB 2.0 §7.2.4.1 allows "10 µF in parallel with 44 Ω", counting "any
capacitive effects visible through the regulator in the device", and requires "some form of VBUS
surge current limiting, such that it matches the characteristics of the above load" for anything
more. Compliance tests read this as under 50 µC of attach charge, integrated only while the
current exceeds 100 mA; current is held to one unit load (100 mA) until configured (§7.2.1).
Type-C caps the receptacle at 10 µF before attach (Table 4-3); PD's 100 µF needs a negotiated
contract Margay never makes. (`2026-11-09-usb-inrush-spec-agent-report.md`)

**Margay as proposed fails it**: about 70-80 µF connected in about 27 µs is 350-400 µC. A real port
would not trip (switches current-limit inside a 4-15 ms flag delay), but VBUS would sag for other
devices on the hub.

**The fix (proposal): a TPS22917 slew-controlled load switch ahead of U_A**, ON tied to VUSB, 4.7
nF from CT to VIN. TI's constants (SLVSDW8B) give about 0.49 V/ms, about 19 ms to full voltage, and
34 mA into 70 µF (98 mA at the 200 µF nominal ceiling), under one unit load with the board's
own attach current added. It draws only from VUSB, so sleep current is unchanged, and it adds
16-24 mV at 200 mA ahead of U_A without touching the battery handover. TPS22917DBVR,
296-50498-1-ND, 57,870 in stock at Digi-Key; second source TPS22918DBVR.
(`2026-11-09-usb-inrush-options-agent-report.md`) Rejected: an RC on U_A's CE (the LM66100
conducts through its body diode when off), the TPS2120/21 (200 µA quiescent), series resistance.

**The capacitance ahead of the limiter still counts in full.** VUSB today carries C5 and C11 (0.1
µF each) and C6 (10 µF): 10.2 µF, at the limit with no margin. C11 leaves with U9; C6 can drop
to 4.7 µF (Okapi's choice for its VUSB) while keeping the ECN's 1 µF minimum.

**Sourcing.** The options agent saw LM66100DCKR at 386 units at Digi-Key (296-53541-1-ND,
UNVERIFIED here); worth a check before the part is fixed.

## 8. The USB side, upstream of U_A (decided, Andy 2026-11-09; on Project-Margay #66, v3.1.0)

```
   J4 VBUS ──┬── VUSB ──┬──────────────── VIN ┌───────────┐ VOUT ── VUSB_SS ── U_A LM66100 VIN
             │          │                     │ U_SS      │                (R_PU 10k to VUSB_SS)
            C6 4.7µF   C5 0.1µF    ON ◄── VUSB│ TPS22917  │
             │          │                     │ CT ── C_CT 0.1 µF ── VIN
            R21 10k     ├── D1 → FT231X VCC   │ QOD open  │
             │          └── Q3 gate           └───────────┘
            GND
   CC1/CC2: R32/R31 5.1k to GND (unchanged)
```

- **U_SS, TPS22917DBVR** (SLVSDW8B): VIN = VUSB; ON tied to VUSB (active high, 1-5.5 V
  input, smart pulldown keeps it from floating); CT through C_CT to VIN; QOD open (slowest
  discharge of VUSB_SS); 2 A continuous; always-on reverse current blocking. It draws only from
  VUSB, so the battery-only sleep current is unchanged.
- **Superseded 2026-11-10 by C_CT = 0.1 µF, below.** Earlier proposal, C_CT = 10 nF: TI's 2300 (mV/µs)·pF at 5 V gives 0.23 V/ms and a 40 ms turn-on,
  so VSYS charges at 16 mA into 70 µF effective and 46 mA into the full 200 µF nominal that two
  100 µF parts present near 0 V. With the board's own attach load (FT231X, the core once VSYS
  passes about 3.4 V, R21's 0.5 mA), the total stays under one unit load (100 mA) with margin.
  4.7 nF (19 ms) would give 98 mA into 200 µF, too close. The part must be rated at least 7 V
  (TPS22917 recommended operating conditions for CT): 10 nF 16 V X7R 0402, for example Murata
  GRM155R71C103KA01D (stock not checked).
- **R_PU moves to VUSB_SS** (TI's Figure 17 pulls ST up to the priority input): U_B stays on
  until the soft-started USB rises past the battery, so the battery carries VSYS through the
  ramp when one is fitted.
- **Ahead of the soft-start (counts fully against USB's 10 µF):** C6 from 10 µF to 4.7 µF (also
  TPS22917's input capacitor), C5 0.1 µF, about 4.8 µF nominal; C11 goes with U9. The USB 2.0
  Device Capacitance ECN's 1 µF minimum is kept (a 4.7 µF X7R holds about 2.7 µF at 5 V).
- **Unchanged:** D1 into the FT231X's VCC, Q3's gate, R21, and the CC resistors. The FT231X's VCC
  has no capacitor of its own today (FTDI's reference shows 100 nF and 4.7 µF); a 100 nF there
  sits behind D1 and counts toward the 10 µF.
- **Not on Margay today, worth deciding:** VBUS surge or ESD protection (no TVS on VUSB).

- **C_CT = 0.1 µF (decided, Andy 2026-11-10), the GCM155R71C104KA55D already on Margay's BoM**
  (16 V X7R 0402, ten positions; the datasheet asks for at least 7 V). Sized by TI's method
  (SLVSDW8B §10.2.2.1: slew = I_rush / C_L, C_T = SR_ON / slew): with 100 mA allowed and the worst
  case of 2 x 100 µF + 20 % = 240 µF near 0 V, C_T must be at least 5.5 nF. 0.1 µF gives 0.023 V/ms,
  a 400 ms turn-on (about 180 ms of rise), and 5.5 mA into 240 µF (1.6 mA into 70 µF effective),
  18 times inside the limit, with no new BoM line. 10 nF gave 1.8 times (55 mA) and 4.7 nF would
  exceed it (117 mA). Murata GRM155R71H103KA88D and Samsung CL05B103KB5NNNC (10 nF, 50 V X7R) were
  the stocked 10 nF options (`sources/2026-11-10-c10-parts-lookups-agent-report.md`).
  **Impact:** with no battery fitted, the board boots about 0.2-0.4 s after USB is plugged in
  (VSYS rises during the last 180 ms of the turn-on, and the core starts as it clears about 3.4 V);
  with 10 nF it was about 40 ms. With a battery fitted there is no delay: the battery carries VSYS
  and USB takes over when its ramp passes the battery. The FT231X runs from VUSB through D1 (#67),
  so USB enumeration does not wait for the ramp. **To check on the first v3.1.0 board:** TI
  characterizes the µs/pF constants for C_T ≥ 100 pF and shows examples to 1000 pF only; scope VSYS
  at USB attach with no battery to confirm the ramp. **To revisit** if a faster battery-less boot
  matters: 10 nF (40 ms) is the smallest value with margin.

Battery fitted at plug-in: VSYS only rises from the battery to USB, slowly. No battery: VSYS
ramps from 0 V over about 0.4 s (with C_CT 0.1 µF), and the core starts when VSYS clears about 3.4 V.

## 9. U7's enable edge below 15 °C (decided, Andy 2026-11-10; Project-Margay #71, v3.1.0)

TPS7A05 (SBVS254D §8.1.3): below 15 °C, IN needs at least 10 ms and EN at least 100 µs to ramp down,
or the next start is partial, off and then normal (IN) or delayed by up to 130 ms (EN). With #66,
U7's IN is VSYS, which stays up in sleep, so the IN rule is met. EN is still a GPIO edge (PC6,
3V3_AUX_CTRL) at every sleep.

Proposal: an RC at U7's EN, 10 kΩ in series from PC6 and 0.1 µF to ground, both lines already on the
board. Computed, with VEN(LO) at most 0.4 V and VEN(HI) at least 0.9 V (SBVS254D):
- τ = 1.0 ms; the fall from 3.3 to 0.4 V takes 2.1 ms, 21 times the 100 µs minimum.
- The rise to 0.9 V takes 0.32 ms, inside the firmware's 6 ms settle.
- Cost: 1.1 nA average at one cycle every 5 min; 0.33 mA peak from the pin; IEN (10 nA max) drops
  0.1 mV across the 10 kΩ.
- The 100k / 10 nF pair gives the same timing at a tenth the charge, but needs a 10 nF line.

Firmware alternative: a 150 ms settle at wake, about 4.3 µA average (8.6 mA awake, every 5 min). It
waits out the delay rather than preventing it.

The rule also asks that VEN not exceed VIN. In the 2024 firmware on v3.0, `powerAux(ON)` raises EN
about 1.5 ms before U8 brings VMAIN up; with VSYS always up in #66, that goes too. Only Margay uses a
TPS7A05; Okapi does not.

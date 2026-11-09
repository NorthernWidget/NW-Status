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

**Decision (Andy, 2026-11-09): the LM66100 ideal-diode pair**, option 3.

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
4. The milestone: Margay's next hardware revision.
5. Bench: today's switchover on a built board, then the new path's handover under an SD write.

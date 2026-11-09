# Margay power path with two LM66100 ideal diodes: a proposed design

2026-11-09, for Andy (QUEUE desk item 15). A proposal, not checked on a bench. It follows TI's
"Dual Ideal Diode ORing for Continuous Output Power" (LM66100 datasheet SLVSEZ8A, §9.2.2,
Figure 17; `sources/2026-11-09-lm66100-figure17.png`).

## The LM66100 in brief (SLVSEZ8A)

A P-channel ideal diode, 1.5-5.5 V, 1.5 A, 79 mΩ at 5 V. CE is an active-low comparator
input: the switch turns on when CE sits 80-250 mV below VIN and off when CE rises 0-80 mV above
VIN (§6.5). ST is an open-drain status output, low when the device is disabled and Hi-Z when
enabled. Quiescent current 0.15 µA typical (0.3 µA maximum); a disabled device leaks 0.2 µA
typical out of its input at 25 °C (2.7 µA maximum at 85 °C). Turn-on 27 µs at 5 V, 40 µs at
3.6 V; status delay 1 µs.

## The circuit

```
   VUSB ──┬────────────── VIN ┌───────────┐ VOUT ──┬── VSYS ──┬── U6 TPS797 → 3V3 (core, always on)
          │                   │ U_A       │        │          └── U7 TPS7A05 → 3V3_AUX (EN as now)
          │       R_PU 10k    │ LM66100   │        │
          ├────────┐   VBAT+ ─┤CE (via R_CE 10k)   │
          │        │          │      ST ──┼──┐     C_SYS bulk (see below)
          │        │          └───────────┘  │
          │        └─────────────────────────┤   ST of U_A, pulled up to VUSB
          │                                  │
   VBAT+ ─┼────────────── VIN ┌───────────┐  │
   (after Q1)                 │ U_B       │VOUT┘ (also to VSYS)
                              │ LM66100   │
                              │CE ◄── U_A's ST (via R_CE 10k)
                              │ST → GND or a spare GPIO (battery-in-use flag)
                              └───────────┘
```

- U_A (USB, the priority input): VIN = VUSB; CE = VBAT+ through R_CE; ST pulled up to VUSB
  through R_PU and wired to U_B's CE.
- U_B (battery): VIN = VBAT+ (after Q1, which keeps reverse-polarity protection); CE = U_A's ST
  through R_CE; ST to GND, or to a spare input as a "running on battery" flag.
- VSYS feeds U6 (core 3V3) and U7 (3V3_AUX, enabled by 3V3_AUX_CTRL as now).
- Removed: U9 (TPS2104), U10 (TLV3691), R17, R18 and the VMAIN net. U8 (TPS22916) and
  R22/R23 stay on VBAT+ to measure the battery, which VSYS no longer reports.
- R_CE: TI recommends a series resistor on CE "to limit the current into the CE pin during a
  negative voltage event"; 10 kΩ drops 6 mV at the 610 nA maximum CE leakage. R_PU 10 kΩ: draws
  0.5 mA from USB only while U_A is disabled with USB present, and drops 6 mV at 610 nA.
  Both values are proposals from the shared resistor list.

## Behavior

| Condition | U_A | U_B | VSYS from |
|---|---|---|---|
| USB only | on (CE = VBAT+ = 0) | no input | USB: the core no longer depends on the FT231X's 50 mA regulator |
| Battery only | off, unpowered | on (CE pulled to the dead VUSB through R_PU) | battery |
| Both, USB above the battery by more than 80-250 mV | on | off (CE = VUSB > VBAT+) | USB; the battery is spared |
| Both, battery higher (for example fresh lithium AAs at 5.4 V) | off | on | battery, as the higher source |
| USB unplugged | turns off as VUSB falls to VBAT+ | turns on within about 1 µs + 27-40 µs | battery; U_B's body diode (0.5 V typical) holds VSYS meanwhile |
| USB plugged in | turns on once VUSB clears VBAT+ | turns off as its CE rises | USB |

TI's Figure 18 shows the 5 V to 3.3 V handover with a small, brief dip
(`sources/2026-11-09-lm66100-figures18-19.png`). USB keeps priority except against a battery
that sits above it, which only fresh lithium cells do.

## Sleep current, battery only

U_B quiescent 0.15 µA plus U_A's reverse leakage 0.2 µA, typical at 25 °C: about 0.35 µA, against
the published 1.68 µA, or under 0.4 % of the typical 5-minute deployment's average current
(`margay-power-path-topic.md`). U_A's leakage rises with temperature: up to 2.7 µA at 85 °C,
datasheet maximum. R_PU and both R_CE carry no current with USB absent.

## C_SYS

The handover gap is U_B's turn-on, 27-40 µs, with U_B's body diode as a floor (VSYS no lower
than the battery less about 0.5-1.1 V). For 3V3_AUX to stay in regulation through it, C_eff >=
I x 40 µs / ΔV: about 27 µF at 200 mA with 0.3 V, and about 2.7 µF at 20 mA. A 10-22 µF part
covers the typical load; the full 200 mA wants more. VUSB keeps its own 10 µF budget, since
VSYS's capacitance sits behind U_A.

## Open points

1. The FT231X: today Q2 ties the core 3V3 to 3V3_FTDI, which is also the FT231X's 3V3OUT. With
   the core powered from USB, two regulators would drive one node. Proposed: 3V3OUT gets its own
   capacitor and leaves 3V3_FTDI; VCCIO and RESET# stay on 3V3_FTDI through Q2 (FT_000565
   allows RESET# to VCCIO). To check against FTDI's self-powered configuration.
2. The 5.5 V ceiling: the LM66100's operating range ends at 5.5 V, Margay's stated battery
   maximum and above USB's 5.25 V.
3. U6 (TPS797) now sees USB voltage on its input; its recommended input is 1.8-5.5 V
   (SLVS332J §6.3), which covers USB.
4. The RTC conversation (desk item 14): VSYS is an obvious source for the RTC's battery input.
5. Bench: the handover under an SD write, and U_A's leakage at temperature.

## Against fresh batteries (2026-11-09, `sources/2026-11-09-fresh-aa-voltages-agent-report.md`)

Fresh alkaline cells measure about 1.6 V open-circuit (Energizer's handbook, checked: "Open
circuit voltage = 1.6 Volts"; the stated spread runs 1.56-1.65 V), so a fresh 3-cell alkaline
pack, AA or D, is 4.68-4.95 V unloaded, 4.80 V typical, and 4.46-4.80 V under the light loads
the manufacturers chart; it falls below 4.75 V within the first few percent of capacity. U_A
takes the load when USB clears the battery by 80-250 mV (150 mV typical), so against 5.0 V USB
an alkaline pack yields to USB. The exception is the top of the fresh spread against a weak
port (USB at or below about 4.9 V with a 4.95 V pack): the battery can carry the board until
it sags, and U_A's CE hysteresis (VON -150 mV, VOFF +35 mV typical) keeps the two from
chattering; an alkaline pack's slow recovery can move the load back and forth only slowly, and
either source holds VSYS. Lithium iron disulfide (L91) packs, 5.37-5.49 V fresh, sit above every
USB voltage and carry the board until they fall below it; they also sit within 0.13 V of the
5.5 V ceiling.

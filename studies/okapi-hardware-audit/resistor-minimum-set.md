# Resistors across Okapi (v0.8.0 plan) and Margay (KiCad v3.1): a minimum set of values

2026-11-09. Andy's question: the smallest set of resistor values that keeps every chip on both
boards running as well as possible, without favoring a value because it is already fitted.
Method: one constraint per position (a range, or a divider equation with a tolerance), each
marked D (datasheet) or P (proposal, Andy to review); an integer program (pulp/CBC) over the
E24 and E96 values picks the fewest distinct values, E24 preferred on ties. The constraints are
in `tools/resistor_minimum_set.py`; the first run's output is
`sources/2026-11-09-resistor-minimum-set-run1.txt`.

Held outside the set (fixed by function): 0 Ω (R51), the shunts 3 mΩ (R10), 20 mΩ (R72, R73,
R75), 50 mΩ (R74, #32), and the 0.1 % 10 kΩ (Okapi R49/R50, Margay R22-R24; one part to choose
for both). R48 is 1 kΩ by Andy's decision; 1 kΩ is in the set.

## Run 1: 10 values, optimal

24 Ω, 220 Ω, 560 Ω, 1 kΩ, 5.6 kΩ, 68 kΩ, 124 kΩ (E96), 169 kΩ (E96), 300 kΩ, 620 kΩ.
Checked by hand:
- TLV61220 620k/68k: 5.06 V. TPS62822 300k/68k: 3.25 V. LT3652 float 169k/620k: 4.200 V, with
  R13 = 124k making R13 + R16||R17 = 257 k. ILIM 220 Ω: 1.05 A; with 560 Ω in parallel, 158 Ω,
  1.46 A. SHDN 620k/124k: 7.2 V. LBI 620k/124k: 3.0 V (edge of the range). MPPT 169k/124k:
  6.38 V (below the P106's 6.5 V Vmp).

Couplings the table does not model, which run 1 breaks or strains:
1. **C6, the TPS62822's feed-forward capacitor, depends on R7** (12 µs / R2: 68 pF at 180 k).
   With R7 = 68 k it wants about 180 pF, a new capacitor line.
2. **USB-C Rd 5.6 kΩ** sits at +9.8 % of 5.1 kΩ under my ±10 % assumption; the USB-C
   tolerance is unverified, and with 1 % parts it may fall outside. Likely fix: hold Rd at 5.1 k.
3. **The timer at 124 kΩ** shortens the 66-minute interval by an amount not yet computed from
   the TPL5111/TPL5010 equation (Andy chose 66 min, "at least for now").
4. **MPPT 6.38 V** is below the P106's maximum-power point; LBI at 3.0 V is at the edge.
5. **Status LEDs at 220 or 560 Ω** change brightness on both boards.
6. Almost every resistor on both boards changes value, Margay's included.

Next: run 2 with Rd fixed at 5.1 kΩ, R7 held at 180 kΩ (or C6 modeled), the timer held to its
interval by equation, and MPPT held to 6.4-6.7 V; then a variant that also counts changed
positions, so Andy can weigh the minimum against the churn.

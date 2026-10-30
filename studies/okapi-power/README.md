# Okapi's core power path: why Bobby boosted to 5 V, and what it costs (2026-10-30)

Question (Andy, 2026-10-30): the Li-ion path to the core's 3.3 V goes through a
boost to 5 V and then an LDO back down. Is that an old structure kept, or a
design with a reason? Read from `Project-Okapi/Hardware/Okapi.sch` (v1.0), the
Resnik board backup (`Resnik.b#1`, 2020), and the TI and Microchip datasheets
fetched on 2026-10-28 and 2026-10-30.

## The core path as drawn

```
Li-ion cell  V_LI --LTC4412 ideal diode (U7)--> V_BETA --TLV61220 boost (U1)--> 5V_LP --+
                                                                                         |  TPS2105 mux (U6)
Alkaline pack  V_PRIME ----------------------------------------------------------------+--> V_CORE --TPS797 LDO (U9)--> 3V3_CORE
                                                                                         ^
                                                   TLV3691 comparator (U37): IN+ = 5V_LP, IN- = V_PRIME, OUT = V_CORE_SW = mux EN
                                                   comparator powered from D8, a diode OR of 5V_LP and V_PRIME
```

TPS2105 function table (TI datasheet, "Function Tables"): EN high selects IN1,
EN low selects IN2. IN1 is 5V_LP, IN2 is V_PRIME. The comparator output is high
when 5V_LP is above V_PRIME.

## The reason

**The 5 V level is the failover discriminator.** A three-cell alkaline pack is
4.5 to 4.8 V fresh. A Li-ion cell is 3.0 to 4.2 V. No comparison of the raw cell
against the raw pack can say "the Li-ion is healthy"; the fresh pack wins. Boosted
to 5 V, the Li-ion rail is above any alkaline pack whenever the boost is running,
and the boost runs whenever the cell is present and above the TLV61220's 0.7 V
floor (its EN is V_BETA). So:

- both packs present: 5V_LP > V_PRIME, EN high, the core runs from the Li-ion and
  the alkalines are untouched;
- cell gone, or cut by the BQ2980 protector: 5V_LP collapses, EN low, the core
  moves to the alkalines in hardware, with no firmware and no hysteresis problem,
  and the comparator itself stays powered through the diode OR from whichever
  source exists;
- the LDO after the mux equalises both sources to one clean 3.3 V, and its 1.2 uA
  is paid once.

The firmware's `powerAuto()` chooses the source for the *high-power* rail (V_HP
through U21/U22 to the TPS61032) by driving C0/C1 and reading EN_BUS_PRIME; the
core rail's failover is the comparator's and happens with the MCU asleep or dead.
That is the property the core must have, and the design delivers it with three
parts whose quiescent currents are 5.5 uA (boost), 1.2 uA (LDO) and 75 nA
(comparator, from memory, UNVERIFIED).

**It was also the lowest-quiescent way to a regulated 3.3 V from a full-range cell
with the parts of 2020.** The Resnik board backup already carries the TLV61220,
TPS2105, LTC4412, TPS61032, TPS79733, TPS62822, LT3652, BQ2980, TLV3691 and
MCP23018: the whole chain is Resnik's, not a remnant of something else. A direct
LDO from the cell drops out below about 3.4 V, which a cold loaded cell reaches at
half charge. The buck-boosts of that time (TPS63001, TPS63020 class) draw 25 to
50 uA quiescent, more than the chain's whole overhead. The ultra-low-quiescent
buck-boost that changes the arithmetic (TPS63900 class, 75 nA; figures from
memory, UNVERIFIED) is newer than the design.

## What it costs today

Sleep load on 3V3_CORE, from the datasheets where read: MCU in power-down about
2 uA; MCP23018 about 1 uA; PCA9634 asleep 2.9 uA; PAC1934 in single-shot 5 uA
(585 uA before Okapi_Library 794a8cf); TPL5111 35 nA; logic and shifters about
1 uA; MB85RC FRAM unknown (part number not in the schematic). Call it 12 uA plus
the FRAM.

| Path | From the cell at 3.7 V, 12 uA load | Basis |
|---|---|---|
| As built: boost to 5 V, LDO to 3.3 V | about 31 uA: LDO input 13.2 uA at 5 V; boost at about 70 % light-load efficiency (ESTIMATE: the TLV61220's light-load curve is in a figure the text extraction does not carry) plus its 5.5 uA | TLV61220, TPS797 datasheets |
| Buck-boost at 3.3 V from the cell | about 13 uA: 12 uA at about 85 % plus 75 nA (ESTIMATE, same caveat) | TPS63900 class |
| Direct LDO (not practical: cold dropout) | about 13 uA | TPS797 |

So the chain's price is about 18 uA of cell current in sleep, roughly half again
awake. Against Margay's measured 1.6 uA floor that is large; against the 585 uA
the PAC1934 drew at its power-up rate until 2026-10-28, it is small.

## What a redesign would have to keep

The failover. A 3.3 V buck-boost output cannot be compared against V_PRIME, so
the comparator would compare V_BETA against a fixed reference instead ("the cell
is above its empty voltage"), with the mux defaulting to the alkalines at power-up
until the reference rail exists. Then one buck-boost (1.8 to 5.5 V in) after the
mux can serve both sources, which removes the LDO and the 5V_LP boost from the core
path and keeps one regulator's quiescent instead of two. That is a change to try
on the next board, where a 3.3 V regulator for the B-SoM must be added anyway
(Project-Okapi#31), and only after a measured sleep current on a built board says
how much of the floor the chain really is.

## Verdict

Bobby's structure is inherited from Resnik and has a good reason: the boosted 5 V
rail is what lets a 75 nA comparator hand the core from the Li-ion to the
alkalines automatically, and in 2020 it was also the lowest-quiescent regulated
3.3 V available from a full-range cell. Its cost is about 18 uA in sleep, which a
modern buck-boost could recover at the price of redesigning the failover sense.

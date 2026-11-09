# USB inrush options for Margay's LM66100 power path: agent report

**COMPLETE** (2026-11-09; ranking at the end)

2026-11-09. Brief: rank practical ways to limit USB inrush into VSYS (two 100 µF 1206 X5R, about
47-70 µF effective) when USB is plugged into a board with no battery, against about 10 µF / 50 µC
at 5 V, without adding sleep current on the battery path and without breaking the USB-to-battery
handover. Design under study: `../margay-power-path-lm66100.md`, `../margay-power-path-decision.md` §6.

Conventions: every number carries its source; UNVERIFIED marks a number not checked against a
source; PROPOSAL marks a value chosen here.

## Source log

| # | Source | Result |
|---|---|---|
| 1 | TI LM66100 datasheet, SLVSEZ8A (Mar 2019, rev. Jun 2019), ti.com/lit/ds/symlink/lm66100.pdf | Read: §6.1, §6.5, §6.6, §8.1, §8.3, §8.4 Table 1, §10. CE is a comparator; OFF state conducts through the body diode |
| 2 | TI TPS22917 datasheet, SLVSDW8B (Sep 2017, rev. Dec 2021), ti.com/lit/ds/symlink/tps22917.pdf | Read: §1, §6 pins, §7.1-7.6, §9.3-9.4, §10.2.2.1. CT slew constants, RCB, leakage |
| 3 | TI TPS22918 datasheet, SLVSD76C (Feb 2016, rev. Jul 2017) | Read: features, §6.6 timing at CT = 1000 pF, §8.3.3 SR equation |
| 4 | TI TPS22916 datasheet, SLVSDO5F (Jul 2017, rev. Dec 2021), C version timing | Read: features, §6.6 continued. Fixed 5 mV/µs at 5 V |
| 5 | TI TPS22919 datasheet, SLVSEN5B | Read: features. Fixed 3.2 mV/µs at 5 V |
| 6 | TI TPS2116 datasheet, SLVSFG1A (Jan 2021, rev. May 2021) | Read: features, §6.5, §6.6, §7.3.2-7.6, §8.2.2, package table |
| 7 | TI TPS2120/TPS2121 datasheet, SLVSEA3F | Read: features, §7.5 IQ. 200 µA typical: rejected |
| 8 | TI TPS22910A (SLVSB49F), TPS22810 (SLVSDH0C), TPS22990 (SLVSDK1C) datasheets | Feature lists only. TPS22810 is 2.7-18 V with 62 µA IQ; TPS22990 needs VBIAS with 5.5 µA shutdown; TPS22910A has a fixed slew. Not pursued; TPS22917 dominates |
| 9 | TI TPS25947, TPS2595 datasheets (eFuses) | Downloaded, not read: eFuses with dV/dt control would work in the TPS22917's place but are larger and their supply current (from VUSB) was not read (UNVERIFIED); not needed |
| 10 | Diodes Inc B0530W, DS30139 Rev. 13-2, diodes.com/assets/Datasheets/B0530W.pdf | Read: ratings, electrical characteristics |
| 11 | Diodes Inc SDM20U30, DS30397 Rev. 14-2 | Read: ratings. VF 0.50 V at 200 mA; IO 200 mA: too small for 210 mA, not used |
| 12 | Nexperia PMEG2010AEH, PMEG3010EJ, PMEG4010CEJ datasheets, assets.nexperia.com | Dead end: HTTP 403 "Access Denied" to curl and to WebFetch. Not retried with other headers |
| 13 | onsemi NSR0320MW2 datasheet | Dead end: HTTP 504 |
| 14 | Vishay BAT54 (vishay.com/docs/85661/bat54.pdf), Diodes SDM40E20LS | Dead end: HTTP 404 |
| 15 | USB 2.0 Electrical Compliance Specification v1.08, usb.org | Read: lists an "Inrush" test for upstream-facing ports; gives no limit or method in this document |
| 16 | USB 2.0 specification and the Device Capacitance ECN, git.nefarius.at mirror | Dead end: the "raw" links returned text, not PDFs. §7.2.4.1 wording therefore UNVERIFIED here (another agent has it) |
| 17 | Web search on USB 2.0 §7.2.4.1 inrush | Secondary sources only (openmoko, Nuvoton FAQ, a blog): 10 µF; "50 µC" not confirmed as normative text |
| 18 | Digi-Key US search pages for TPS22917DBVR, TPS22918DBVR, TPS22916CYFPR, TPS22919DCKR, TPS2116DRLR, LM66100DCKR, GRM155R71C472KA01D, B0530W-7-F (2026-11-09, read through WebFetch's summarizer) | Stock and prices as quoted in each option. LM66100DCKR: 296-53541-1-ND, 386 in stock, $0.36 at 1 (note: thin stock for the part the design already uses). B0530W-7-F: price shown, stock and DK number not shown |
| 19 | `margay-power-path-lm66100.md`, `margay-power-path-decision.md`, `2026-11-09-capacitor-constraints-agent-report.md` | The design, the §6 hold-up formula (reproduced: 10.4/15.7/23.8/49.1 µF), VUSB's 10.2 µF |

## Options

### Common numbers

- Charge to bring VSYS to 5 V: Q = C x V. At 47 µF effective (worst case, decision §6) 235 µC; at
  70 µF (decision §6, at 5 V) 350 µC; at 200 µF (two parts nominal, an upper bound for the low-bias
  start of the ramp, since X5R loses little capacitance near 0 V) 1000 µC. Arithmetic, this report.
- Ramp current: I = C x dV/dt (TI's own Equation 5 in SLVSDW8B and Equation 1 in SLVSFG1A).
- VUSB already holds 10.2 µF nominal, 5.42 µF effective at 5.0 V (C5 + C6 + C11;
  `2026-11-09-capacitor-constraints-agent-report.md`). That charge comes in at plug-in with every
  option here, and anything else USB sees at plug-in adds to it.
- The USB criterion. This report takes the brief's 10 µF / 50 µC. Whether a slow ramp passes it
  depends on its wording, which another agent is confirming: USB 2.0 §7.2.4.1 asks, from memory
  (UNVERIFIED), that a device with more than 10 µF "incorporate some form of VBUS surge current
  limiting, such that it matches the characteristics of" the 10 µF || 44 Ω reference load. Read
  that way, a ramp held near one unit load (5 V / 44 Ω = 114 mA, arithmetic) is compliant. Read as
  a 50 µC cap on the total charge, no option that charges 47-70 µF from USB alone can pass, and
  only a smaller VSYS capacitance (option F) gets there.

### Option A: an RC on U_A's CE (brief option 1). Does not work.

Circuit: R and C from U_A's CE to GND, so CE sits above VIN at plug-in and U_A turns on later.

What SLVSEZ8A says: CE is a comparator input, not a gate. "The chip enable works by comparing the
CE pin voltage to the input voltage. When the CE pin voltage is higher than VIN by 80 mV, the
device is disabled and the MOSFET is off" (§8.1). There is no gate-slew input; the 27 µs turn-on
at 5 V is the internal gate drive, specified "at a load of CL = 100 nF and RL = 1kΩ" (§6.6).
Ramping CE therefore only moves the moment of turn-on. Worse, a disabled LM66100 conducts through
its body diode: Table 1 lists the OFF state as "IN-to-OUT: Diode", "Power Dissipation: IOUT x
VFWD", with VFWD 0.1/0.5/1.1 V min/typ/max at 10 mA (§6.5). VSYS still charges from VUSB to
VUSB - VFWD the instant USB arrives, through the body diode, with nothing limiting the current but
the cable and the host's port switch. Body-diode current is rated "≤0.1 ms, 0.2% Duty Cycle" at 2.5
A (ID,PLS, §6.1).

- Inrush: unchanged, 235-350 µC (more from 0 V bias), peak set by the cable and the host.
- Sleep current: none added.
- Handover: unaffected if CE still reaches VBAT+; but while CE is held high, the load runs through
  the body diode, losing 0.5-1.1 V.
- Parts: none worth buying. Rejected.

### Option B: a slew-controlled load switch ahead of U_A (brief option 2). Works; recommended.

Circuit: VUSB -> U_S (TPS22917DBV) VIN; U_S ON tied to VUSB; U_S CT to VIN through C_T; U_S QOD
open; U_S VOUT -> U_A VIN (node X, with U_A's 1 µF input capacitor per SLVSEZ8A §10). U_A's CE,
ST, R_PU and U_B are unchanged; R_PU stays on raw VUSB. The FT231X and C5/C6 stay on raw VUSB.
Figure 17's logic is untouched: U_A still sees "USB" as node X, which follows VUSB once U_S is on.

The ramp. TPS22917 (SLVSDW8B, Dec 2021): "Adjustable turn ON limits inrush current (tON): 5-V tON
= 100 μs at 72 mV/μs (CT = open); 5-V tON = 4000 μs at 2.3 mV/μs (CT = 1000 pF)". SRON at VIN =
5.0 V, CT ≥ 100 pF: "2300 (mV/µs)*pF"; tON at 5.0 V: "4 µs/pF" (§7.6, typical, 25 °C). Pin 4 CT:
"Connect capacitor from this pin to VIN to increase output slew rate and turn-on time." TI's sizing:
"(Slew Rate) = IRUSH ÷ CL" and "CT = SRON ÷ (Slew Rate)" (§10.2.2.1). Timing capacitor voltage rating
7 V minimum (§7.3).

| C_T (PROPOSAL values) | Slew at 5 V | tON | I at 47 µF | I at 70 µF | I at 200 µF |
|---|---|---|---|---|---|
| open | 72 mV/µs (datasheet) | 100 µs | 3.4 A | 5.0 A | 14 A |
| 1000 pF | 2.3 mV/µs | 4.0 ms | 108 mA | 161 mA | 460 mA |
| 2200 pF | 1.05 mV/µs | 8.8 ms | 49 mA | 73 mA | 209 mA |
| **4700 pF** | **0.49 mV/µs** | **18.8 ms** | **23 mA** | **34 mA** | **98 mA** |
| 10 nF | 0.23 mV/µs | 40 ms | 11 mA | 16 mA | 46 mA |

(Slew and tON from the datasheet constants; currents arithmetic. The datasheet constants are
typical at 25 °C only; no min/max or temperature spread is given for SRON, so the ramp current at
-40/+85 °C is UNVERIFIED.) PROPOSAL: C_T = 4.7 nF, which holds the ramp under one unit load (114 mA)
even if the two 100 µF parts delivered their full nominal value. The total charge is unchanged
(235-350 µC) but spread over about 19 ms. The load itself (core about 8.6 mA awake, from
`margay-power-path-decision.md` §3) rides on top during the ramp.

Heating: dissipation during the ramp is at most I x VIN, about 0.1 A x 5 V = 0.5 W at the start,
falling to zero; the energy is about ½CV² = 0.9 mJ at 70 µF (arithmetic), well inside a part rated
"IPLS Maximum pulsed switch current, pulse < 300-µs, 2% duty cycle 2.5 A" with 183 °C/W θJA (§7.1,
§7.4). The datasheet gives no SOA curve; TI's own example (§10.2) ramps 47 µF at under 150 mA.

Sleep current, battery fitted, USB absent: none added. U_S's VIN is VUSB, dead. U_A blocks VSYS from
node X as it does today from VUSB; whatever U_A leaks (0.2 µA typical, 2.7 µA maximum -40 to +85 °C,
SLVSEZ8A §6.5) now flows through node X and then U_S (VIN reverse leakage "–1 µA" maximum,
SLVSDW8B §7.5) in series, so it cannot exceed U_A's own figure, which is already in the budget
(inference from the two series leakages; UNVERIFIED on a bench). U_S's IQ (0.5 µA typical, 1.0 µA
maximum -40 to +85 °C, §7.5) is drawn from VUSB only.

Handover: unchanged in mechanism. With USB present, U_S adds its 80 mΩ typical, 120 mΩ maximum
(-40 to +85 °C, VIN = 5 V) in series: 16-24 mV at 200 mA (arithmetic). On unplug, node X follows
VUSB down through U_S, and U_A lets go when VBAT+ exceeds node X by VOFF, as before. On plug-in with
a battery fitted, node X ramps slowly from 0; U_A turns on once node X clears VBAT+ by 80-250 mV
(SLVSEZ8A §6.5), and VSYS steps from the battery to USB as today (0.2-0.5 V). U_S's own reverse
blocking ("RCB Activation Current –0.5 A typical, –1 A maximum", §7.5) is not relied on, since U_A
blocks reverse current. The ramp delays "USB takes over" by up to 19 ms after plug-in; the battery
carries the board meanwhile, or, with no battery, the board boots 19 ms later.

Parts (Digi-Key US, 2026-11-09):
- TPS22917DBVR, SOT-23-6: 296-50498-1-ND, 57,870 in stock, $0.58 at 1 (cut tape).
- C_T GRM155R71C472KA01D, 4700 pF 16 V X7R 0402: 490-6334-1-ND, 3,664 in stock, $0.10 at 1. X7R
  carries ±15 % over -55 to +125 °C (the class definition, from memory, UNVERIFIED here), so the
  slew moves by about that much with temperature.

Alternative switches in the same position:
- TPS22918DBVR (SLVSD76C): CT to GND, "SR = 0.55 × CT + 30" with SR in µs/V (§8.3.3); 4700 pF gives
  0.38 mV/µs, 27 mA at 70 µF, 77 mA at 200 µF; rise 0-5 V about 13 ms (arithmetic). IQ 8.3 µA
  typical at 3.3 V, drawn from VUSB only. No reverse blocking listed in its features; not needed
  here because U_A blocks. Digi-Key 296-46278-1-ND, 17,017 in stock, $0.59 at 1. A good second
  source of the same function.
- TPS22916C (fixed slow timing, SLVSDO5F): "SRON Slew Rate VIN = 5 V 5 mV/µs", tON 1400 µs (§6.6):
  235/350/1000 mA at 47/70/200 µF. Too fast for a unit load, and TPS22916CYFPR (4-DSBGA) shows 0 in
  stock at Digi-Key, "3,000 expected in stock on 07-Dec-2026".
- TPS22919 (fixed, SLVSEN5B): "5.0 V Turn ON time (tON): 1.95 ms at 3.2 mV/μs": 150/224/640 mA.
  Too fast, and TPS22919DCKR shows 0 in stock ("3,000 expected in stock on 17-Nov-2026").

### Option C: TPS2116 power mux in place of both LM66100 (brief option 3). Works for inrush; costs sleep current.

Circuit: VIN1 = VUSB, VIN2 = VBAT+ (after Q1), VOUT = VSYS; MODE tied to VIN1 and PR1 from a
divider on VIN1 ("To configure VIN1 as the priority supply, connect MODE to VIN1 and set the proper
threshold through a resistor divider from VIN1 to PR1", SLVSFG1A §7.6.1; VREF 0.92/1.00/1.08 V,
§6.5). ST is the "running on battery" flag ("Pulled low when VIN1 is not being used", pin table).

Inrush: soft start only from a dead output. "When an input voltage is applied to the TPS2116 and the
output voltage is lower than 1 V, the output will be brought up with soft start to minimize the
inrush current due to output capacitance. However, when the device switches from one power supply to
another (switchover) and VOUT > 1 V, soft start is not used" (§7.3.2). tSS "VINx = 5 V, RL = 100 Ω,
CL = 10 uF: 1.7 ms" typical (§6.6), fixed. TI's sizing "IINRUSH = COUT × VOUT / tSS" (§8.2.2) gives
138/206/588 mA at 47/70/200 µF (arithmetic). TI's own example: "the inrush current caused by a
100-µF capacitance would be 294 mA, well below the 500-mA target". Above one unit load at 70 µF.

Sleep current, battery only: "IQ, VIN2 ... VIN2 powers VOUT, VIN2 > VIN1 + 0.2V: 1.35 uA" typical at
25 °C, 3.7 µA maximum -40 to 85 °C (§6.5). Against the LM66100 pair's 0.35 µA typical
(`margay-power-path-lm66100.md`), that adds about 1.0 µA typical to a 1.7 µA sleep, about 60 %
(arithmetic). The VIN1 standby current and the PR1 divider draw from USB only.

Handover: break-before-make, "tSW Switchover time, VINx = 5 V, RL = 10 Ω, CL = 10 uF: 8 us" typical
(§6.6), against the LM66100 pair's 44 µs (decision §6). At 210 mA and 0.3 V droop that needs about
5.6 µF effective in place of about 31 µF (arithmetic, C = I t / ΔV), which would let VSYS shrink and
the inrush with it. "If the output voltage is greater than the input supply being switched to, then
the device will not turn on the new channel until the output has discharged down to VIN + VRCB"
(§7.6.1), with VRCB,R 42 mV typical (§6.5). USB keeps priority even over a higher (lithium) pack,
since PR1 alone decides. Caveat: "If the supply powering the device drops at a rate faster than 1
V/10 μs, the other supply must be at 2.5 V or higher to prevent the device from resetting" (§7.4);
the battery floor is 3.3 V, above that.

Parts: TPS2116DRLR (SOT-5X3, 8 pins): Digi-Key 296-TPS2116DRLRCT-ND, 47,156 in stock, $1.14 at 1.
This reopens the power-path decision (option 2 in `margay-power-path-decision.md` §2), and the
sleep cost is the reason the brief's constraint excludes it.

### Option D: TPS2120/TPS2121. Breaks the sleep budget.

SLVSEA3F: "Low Iq from enabled input: 200 µA (typical)", "Low Iq from disabled input: 10 µA
(Typical)", "Wide operating range: 2.8 V to 22 V". IQ,INx 300 µA typical, 400 µA maximum (§7.5
table). The SS pin does set the soft start, but 200 µA from the battery is about 120 times the
logger's sleep current. Rejected; no stock check made.

### Option E: split the bulk (brief option 4)

E1, bulk on VBAT+ (the battery side of U_B): does not bridge the gap. The battery already holds
VBAT+; the gap is U_B's own channel turning on, during which VSYS is fed only by U_B's body diode
(VFWD 0.5 V typical, 1.1 V maximum at 10 mA, SLVSEZ8A §6.5). A capacitor on VBAT+ adds nothing a
battery does not already supply. It also puts the capacitance on the battery path in sleep (ceramic,
so negligible leakage; not the point). Rejected.

E2, a reservoir behind R and a Schottky. Circuit: the two 100 µF parts move to a node C_R; R_R
(PROPOSAL 1 kΩ) from VSYS to C_R charges it; D_R (Schottky, anode C_R, cathode VSYS) discharges it
into VSYS. VSYS keeps only the regulators' input capacitors.
- Inrush: VSYS (small) charges at once; C_R charges through R_R at no more than 5 V / 1 kΩ = 5 mA,
  with τ = R x C = 70 ms at 70 µF (arithmetic). Under one unit load by a wide margin; the total
  charge is unchanged.
- Sleep: none added. In steady state C_R sits at VSYS through R_R, so D_R is at zero bias and R_R
  carries no current (inference, UNVERIFIED on a bench).
- Handover: the Schottky drop comes out of the margin. Diodes Inc B0530W (DS30139 Rev. 13-2):
  "Maximum Forward Voltage Drop VFM 0.375 V IF = 0.1A, TJ = +25C; 0.430 V IF = 0.5A". Taking about
  0.40 V at 210 mA (interpolated, UNVERIFIED; higher at -40 °C), the effective capacitance needed at
  210 mA through 44 µs becomes 18.9 µF at 4.5 V and 49.1 µF at 4.2 V, and the scheme fails at 4.0 V
  (arithmetic, the decision §6 formula with ΔV reduced by 0.40 V; the same formula without the
  diode reproduces §6's 10.4, 15.7 and 23.8 µF). Today's pair carries 210 mA to about 3.9 V.
  **This breaks the handover for the lower part of the battery range at the full 3V3_AUX load.**
- Parts: B0530W-7-F (SOD-123), $0.27 at 1 at Digi-Key; stock and Digi-Key part number not shown
  on the search page fetched (UNVERIFIED). R_R from the shared resistor list.

### Option F: a Schottky across U_B, and a small VSYS capacitance (added option)

Circuit: D_F (Schottky, anode VBAT+, cathode VSYS) in parallel with U_B; VSYS keeps only the
regulators' input capacitors (about 2 µF nominal, UNVERIFIED count). The Schottky replaces the bulk
as the bridge for U_B's 44 µs: VSYS cannot fall below VBAT+ - VF.
- Inrush: USB sees VUSB's 10.2 µF nominal (5.42 µF effective) plus about 2 µF: about 12 µF nominal,
  about 7 µF effective (UNVERIFIED sum). Inside 10 µF on effective values, over it on nominal.
- Handover: the floor is VBAT+ - VF; with 0.40 V at 210 mA (as in E2) the pack must be at or above
  3.512 + 0.40 = 3.91 V (arithmetic) for 3V3_AUX to stay in regulation, at 25 °C. This matches
  today's 47 µF to within the reading, without depending on the capacitor's derating; Schottky VF
  rises in the cold (not quantified here, UNVERIFIED).
- Sleep: D_F sits at zero bias in battery-only sleep (VSYS = VBAT+ less U_B's microvolt drop), so it
  adds no leakage.
- Costs: with USB present D_F is reverse-biased by VUSB - VBAT+ (0.2-0.5 V), and its leakage flows
  from USB into the primary cells; B0530W lists "IRM 20 µA VR = 15V, TJ = +25C" maximum and gives
  only a typical curve for temperature. Reverse current into primary cells is a safety question
  (UNVERIFIED; not checked against IEC 60086 or UL here). With no battery and USB present, D_F's
  leakage at 5 V reverse lifts the floating VBAT+ node, which is U_A's CE (see the observation
  below). D_F also lets the battery share the load whenever USB sags more than VF below it.
- Parts: B0530W-7-F, $0.27 at 1, as above.

### Option G: series resistance or an NTC in VBUS, or accept the overshoot (brief option 5)

- A series resistor large enough to limit the plug-in current to a unit load (5 V / 114 mA = 44 Ω)
  would drop 8.8 V at 200 mA; even 1 Ω allows 5 A peak and drops 0.2 V at 200 mA (arithmetic).
  Rejected.
- An NTC: its resistance must be low at the 200 mA running load and high at plug-in, and it relies
  on self-heating at a load this small; at -40 °C it is at its highest resistance when the logger
  runs. No part searched. Rejected on mechanism.
- Accepting the overshoot: the event is the battery-less USB case only (bench, configuration). The
  host's port supplies the 235-350 µC in a few tens of µs at whatever its port switch or cable allows
  (UNVERIFIED; no host data checked). Non-compliant on either reading of the USB text; a hub's other
  ports may see a droop. A fallback only.

### Observation (outside the brief): the floating VBAT+ node with no battery

With USB present and no battery, VBAT+ is loaded only by U8's shutdown current and C12 (from
`2026-11-09-capacitor-constraints-agent-report.md`), and U_B leaks "OUT to IN ... Current out of
VIN" into it, 0.2 µA typical, 2.7 µA maximum -40 to 85 °C (SLVSEZ8A §6.5). VBAT+ is U_A's CE. The
leakage can raise VBAT+ toward VSYS but not above it, and U_A's OFF threshold is VOFF = 0-80 mV
above VIN (§6.5), so U_A should stay on, with a margin of only U_A's own drop (I x RON). Inference,
UNVERIFIED; worth a bench look (scope VBAT+ with USB only, warm), and it becomes sharper under
option F.

## Ranking

| Rank | Option | Inrush at 5 V (70 µF; 200 µF bound) | Added sleep current, battery only | Handover | Parts, Digi-Key US, price at 1 |
|---|---|---|---|---|---|
| 1 | B: TPS22917 ahead of U_A, C_T = 4.7 nF (PROPOSAL) | 34 mA; 98 mA, over about 19 ms | none (U_S is on VUSB; series leakage bounded by U_A's) | unchanged; +16-24 mV at 200 mA | TPS22917DBVR 57,870, $0.58; GRM155R71C472KA01D 3,664, $0.10 |
| 2 | B, second source: TPS22918 ahead of U_A, C_T = 4.7 nF | 27 mA; 77 mA, over about 13 ms | none (IQ 8.3 µA from VUSB only) | unchanged | TPS22918DBVR 17,017, $0.59 |
| 3 | C: TPS2116 in place of the LM66100 pair | 206 mA; 588 mA, 1.7 ms fixed | +1.0 µA typical (1.35 against 0.35), 3.7 µA maximum | better: 8 µs break-before-make, smaller bulk | TPS2116DRLR 47,156, $1.14 |
| 4 | F: Schottky across U_B, VSYS capacitance cut to the regulators' inputs | about 12 µF nominal, 7 µF effective on USB | none | floor VBAT+ - VF: pack >= 3.91 V at 210 mA, 25 °C | B0530W-7-F, $0.27 |
| 5 | E2: reservoir behind 1 kΩ and a Schottky | 5 mA, τ 70 ms | none | **breaks** at 210 mA below about 4.2 V | B0530W-7-F, $0.27 |
| 6 | G: accept the overshoot | 235-350 µC unlimited | none | unchanged | none |
| - | A: RC on CE | no effect (body diode conducts) | none | worse while held off | rejected |
| - | D: TPS2120/21 | soft start adjustable | **+200 µA typical: breaks sleep** | - | rejected |
| - | E1: bulk on VBAT+ | - | - | **does not bridge the gap** | rejected |
| - | G: series R or NTC | - | - | drops too much at load | rejected |

Recommendation: option B with the TPS22917DBVR and C_T = 4.7 nF (both PROPOSAL values for Andy).
It leaves Figure 17's logic, the two 100 µF parts and the 44 µs hold-up untouched, adds nothing to
the battery path, and holds the plug-in ramp under one USB unit load even at the capacitors' full
nominal value. It meets the USB text if that text asks for surge limiting to match a 10 µF || 44 Ω
load; it does not meet a literal 50 µC cap on the total charge, which no option holding 47-70 µF on
VSYS can meet (that reading leads to option F or C instead). Bench checks: the plug-in current with
no battery at -40, 25 and 85 °C; the plug-in with a battery fitted (U_A's turn-on as node X ramps);
and the handover under an SD write, which option B should not change.

**COMPLETE**

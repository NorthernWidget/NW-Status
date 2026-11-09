# Margay VMAIN at the USB-to-battery switchover

2026-11-09. Andy: "This sag sounds foundationally important." The question: what capacitance
VMAIN needs to carry 3V3_AUX through U9's switchover from USB to the battery. The answer is that
capacitance alone cannot. U9 changes over only after VUSB has collapsed, so VMAIN collapses with
it. The control has to change first, and the capacitor is then sized for the switch's own gap.

## The circuit (KiCad v3.1 netlist, Project-Margay 136a6f8 and after)

- U9, TPS2104DBVT: IN1 = VBAT_SW (battery, through U8 TPS22916, enabled by the MCU on
  VBAT_SW_CTRL); IN2 = VUSB; OUT = VMAIN. C10 (1 µF) on IN1, C11 (0.1 µF) on IN2, C13 (1 µF)
  on VMAIN, and nothing else on VMAIN.
- VMAIN's only load is U7, TPS7A05 (3.3 V, 200 mA), which makes 3V3_AUX: the SD card (J1), the
  sensor terminals (J2), R1/R15/R16, the DS3231M's VCC, and the parts on C16's net.
- U9's EN comes from U10, a TLV3691 powered from the battery-fed 3V3. IN+ is 3V3_FTDI and IN-
  is VBAT_SW/2 (R17/R18, 10k/10k).
- 3V3_FTDI is the FT231X's 3V3OUT, joined to the core 3V3 through Q2 (FDN360P) while USB is
  present: Q3 (2N7002PW) has its gate on VUSB and pulls Q2's gate low against R19.

The TPS2104 never chooses a source itself. Its function table: EN high selects IN2 whatever the
input voltages, including the row VIN1 = 5 V, VIN2 = 0 V, EN = H, which gives OUT = VIN2
(SLVS235A p2, Function Tables). Its inputs carry no reverse current ("No Reverse Current Flow",
p1), and an input below "approximately 2 V" turns its switch off (p13, undervoltage lockout).

## The sequence when USB is unplugged

1. VUSB decays on C5, C6 and C11 (10.2 µF nominal), loaded by the FT231X and, through U9's IN2
   switch, by VMAIN's load. VMAIN follows VUSB down.
2. While VUSB stays above Q3's gate threshold, Q2 holds 3V3_FTDI at the core's 3.3 V. U10 sees
   3.3 V against VBAT_SW/2 (1.65-2.75 V for the README's 3.3-5.5 V battery) and keeps EN high:
   U9 stays on the dying USB input.
3. Q3 turns off near its threshold (1.75 V typical, 2.4 V maximum, Arrow's listing for the
   2N7002PW; UNVERIFIED against Nexperia's datasheet), and U9's IN2 switch has already opened at
   about 2 V by its own lockout. 3V3_FTDI then falls, U10 flips, EN goes low, and IN1 turns on.
4. Then the switch's own gap: Figure 11 (V_IN1 = V_IN2 = 5 V, 25 °C) gives droop against load
   for 1 to 220 µF. Read as C × ΔV / I, every curve gives a gap of 0.5 to 0.7 ms (1 µF: 0.4 V at
   about 0.56 mA; 10 µF: 0.4 V at about 5.9 mA; 220 µF: 0.32 V at 100 mA). Okapi's reading of
   the TPS2105's same figure was 0.65 ms.

So VMAIN falls to about 2 V before U9 reaches for the battery, at any load and with any
capacitance; more capacitance only stretches the time it takes. The TPS7A05 needs VMAIN at
3.3 V plus its dropout (212 mV maximum at 200 mA, -40 to +85 °C, SBVS254D p8) to hold 3.3 V.
3V3_AUX therefore drops out on every USB unplug while it is on: the SD card, the sensors on J2
and the RTC's VCC lose their supply. The DS3231M moves to VBAT, which is where D4, C19/C20 and
the coin cell come in (QUEUE, ON ANDY'S DESK 14).

When it happens: only at a USB unplug with 3V3_AUX enabled. A logger on its battery alone never
switches. In the field that is a laptop session ending mid-log; on the bench it is every unplug.
The SD card is the exposure: a write in progress loses power.

## What fixes it, and the capacitor that goes with each

The control must change over while VUSB is still well above 3.5 V. Options, each a proposal:
1. U10 watches VUSB itself (a divider from VUSB against a reference, or against VBAT_SW) with a
   threshold near 4.3-4.5 V and some hysteresis, in place of 3V3_FTDI.
2. A power multiplexer that does this itself (for example TI's TPS2120/TPS2121 family, with a
   programmable priority threshold), in place of U9 and U10. Not checked against Margay's
   currents or quiescent budget.
3. An ideal-diode OR of VUSB and VBAT_SW (the LTC4412 pattern Okapi uses), which hands over
   whichever source is higher with no gap to speak of.

With option 1, VMAIN starts the gap at the switchover threshold. The capacitance it then needs:
C_eff >= I x 0.7 ms / (V_switch - 3.51 V). With V_switch = 4.4 V (a proposal), that is about
0.79 µF per mA of 3V3_AUX load:

| 3V3_AUX load | C_eff needed | Notes |
|---|---|---|
| 10 mA | 7.9 µF | logger and RTC, no sensors |
| 50 mA | 39 µF | the README's earlier sensor limit |
| 100 mA | 79 µF | the datasheet's own "220-µF ... for 100-mA loads" sits well above this |
| 200 mA | 157 µF | the TPS7A05's full rating |

A battery near the README's 3.3 V floor cannot hold 3V3_AUX in regulation after the switch in
any case. Margay's VMAIN load during an SD write is not known here: it wants a bench
measurement before a part is chosen.

Option 3 needs no bulk beyond ordinary decoupling. Option 2 depends on the part.

## Okapi does not share it (checked 2026-11-09)

Okapi's U6 is a TPS2105 (EN high selects IN1). Its EN comes from U37, a TLV3691 powered through
D8 from whichever of 5V_LP and V_PRIME is higher, comparing the two inputs themselves: IN+ =
5V_LP (U6's IN1, the TLV61220's 5.06 V boost output from the Li-ion cell), IN- = V_PRIME (U6's
IN2, the backup pack). U6 changes over the moment the falling source crosses the other one, so
V_CORE starts the gap near the backup pack's voltage, as C43's sizing assumed (capacitors.md,
#45).

A different point the same comparison raises: U6 runs from whichever input is higher. A backup
pack above 5.06 V (three fresh lithium AAs, about 5.4 V, ASSUMED cell count) would carry V_CORE
in place of the Li-ion cell until it fell below the boost output. Not yet checked against the
intended priority.

## The proposed control: chatter and USB without a battery (checked 2026-11-09)

Proposal: U10's IN+ from a VUSB divider (Ra 100k, Rb 150k, k = 0.6) in place of 3V3_FTDI; IN-
stays VBAT_SW/2 (R17/R18); Rh from OUT to IN+ for hysteresis. TLV3691 (SBOS694A): push-pull
output, internal hysteresis 17 mV (28 mV referred to VUSB), input range (V-) - 0.1 V to (V+) +
0.1 V. That input limit is why the existing design keeps both inputs under 3.3 V.

**Chatter.** Moving the load onto USB lowers VUSB by the source and cable resistance times the
load, and raises VBAT_SW by the battery's internal resistance times the same load. Both push U10
back toward the battery. With 200 mA (the TPS7A05's rating), 0.5 Ω of USB source and cable, and
0.75 Ω of pack (both ASSUMED, to be measured), that is about 0.1 V at VUSB and 0.15 V at
VBAT_SW, which IN- sees halved: about 0.25 V referred to VUSB, against U10's own 28 mV. Rh = 1 MΩ
(on the shared list) gives a 0.33 V band; IN+ peaks at 3.16 V at VUSB 5.25 V, inside 3.4 V.

| Battery | To USB above | Back to battery below |
|---|---|---|
| 5.5 V | 4.86 V | 4.53 V |
| 5.0 V | 4.42 V | 4.09 V |
| 4.5 V | 3.98 V | 3.65 V |
| 3.6 V | 3.18 V | 2.85 V |

With a fresh 5.5 V pack, USB below 4.86 V (a long cable at the 4.75 V port minimum) leaves the
logger on the battery, which is then the higher source. The handover to the battery happens
0.33 V lower than without Rh, which takes from the VMAIN capacitor's droop allowance.

**USB without a battery.** U10 is powered: the FT231X's 3V3OUT reaches the core 3V3 through Q2,
which Q3 holds on from VUSB. IN- is near 0 V, so U10 selects USB in both designs. (Corrects an
earlier line in this session that called U10 unpowered.) What this shows instead: with no battery
the whole core (the ATmega, LEDs, U10, D4's feed to the RTC) runs from the FT231X's internal
regulator, which the datasheet rates at "a maximum current of 50mA" and describes as mainly for
the USB transceiver (FT_000565 v1.4, §4). The core 3V3 also back-feeds VBAT+ through the TPS797's
PMOS "back diode", which "conducts reverse current when the input voltage drops below the output
voltage ... and is not internally limited" (SLVS332J §7.3.1). Bench work on USB alone runs
the logger near the FTDI regulator's limit; the README's "Make sure battery power is applied"
is consistent with that.

# Okapi v0.8: the Particle under the logger's control

Plan, 2026-11-10. Status: proposal for Andy; nothing here is drawn yet.

Goal: the Particle module (a Boron on the FeatherWing socket MS1, or a B-SoM on
the M.2 socket J9) is powered through one path that the logger firmware owns. It
is on by default for backhaul, can be held on for other uses, and is still
powered hourly by the TPL5111 if the logger hangs. Both sockets must work.

Every netlist fact below is from `kicad-cli sch export netlist` of
Project-Okapi/Hardware/KiCAD-10import at bcfb2e8 (the Particle net rename).
Datasheet facts carry their source; anything not checked says so.

## 1. As built (v0.7 netlist)

### Power

```
V_LI ── U10 TPS22917 ── PARTICLE_VCC ──┬── MS1 pin 28 VBAT        (Feather)
          ON ◄── U8 TPL5111 DRVn       └── J9 pins 2,4,6,8 VCC    (B-SoM modem)
                 DELAY ◄── Q3 FDN360P ◄── PARTICLE_EN (U41 GPB7; R19 100 k to 3V3_CORE = off)
                 DONE  ◄── WD_DONE (MS1 A3, J9 ADC3)
                 R20 130 k to GND sets 3943 s

V_HP ── U3 TPS61032 ── 5V_AUX ──┬── MS1 pin 26 USB                (Feather)
          EN = POWER_EN         └── F2 PPTC 1.5 A ── PARTICLE_BSOM_VUSB ──┬── J9 pin 16 VBUS
                                                                          └── USB2 micro-USB VDD

PARTICLE_3V3 ── MS1 pin 2 "3V" (the Feather's regulator OUTPUT)
             ├── J9 pins 10,12 3V3 (the B-SoM's supply INPUT)
             ├── U34 TXS0102 VB and EN, D7 RGB anode, R86/R87 10 k pull-ups, C37
             └── (no regulator on this net)
```

### Signals (both sockets in parallel)

| Net | MCU / board side | MS1 (Feather) | J9 (B-SoM) |
|---|---|---|---|
| TX | IC1 PD1 (TXD0), R40 330 Ω to U23 FT231X | 14 RX | 38 RX |
| RX | IC1 PD0 (RXD0), R38 330 Ω to U23 FT231X | 15 TX | 36 TX |
| PARTICLE_RTS | IC1 PA7 | 19 GPIO5 | 42 RTS |
| PARTICLE_CTS | IC1 PA6 | 20 GPIO6 | 40 CTS |
| PARTICLE_GPIO | IC1 PA5 (busy line) | 10 A5 | 43 ADC5 |
| SDA_PARTICLE / SCL_PARTICLE | U34 TXS0102 B side; A side SDA_OB/SCL; VA 3V3_CORE, VB = EN = PARTICLE_3V3 | 17 / 18 | 22 / 20 |
| RST_TRIG | Q4 2N7002 gate (R54 10 k to GND); drain on RST (the MCU's reset) | 21 GPIO9 | 66 PWM0 |
| WD_DONE | U8 TPL5111 DONE | 8 A3 | 37 ADC3 |
| /Cell_Module/~{RST}, ~{MODE} | R86/R87 10 k to PARTICLE_3V3, buttons S7/S6 | – | 34 / 32 |
| PD+ / PD- | USB2 micro-USB | – | 11 / 13 |

## 2. What is wrong with it

1. **The Feather's USB pin is on 5V_AUX (MS1 pin 26).** A Feather powers itself
   from USB. Whenever the firmware turns on 5V_AUX (POWER_EN = C0 XOR C1), which it
   does for the 5 V sensor switches (U17, U19 inputs), the ADS1115 (U33) and the
   DAC (U30), the Boron is powered, whatever U10 and the TPL5111 do. This is why
   the radio transmitted every interval although the firmware never drove
   PARTICLE_EN. The firmware cannot run the 5 V sensors without the radio, and the
   README's "the module draws nothing until the next interval" is untrue on a
   Feather build while 5V_AUX is up.
2. **The B-SoM's VBUS is on 5V_AUX too, through F2, and the B-SoM's own micro-USB
   connector (USB2) sits on the same net.** Particle's B404X datasheet describes
   VBUS as "connected to the USB detect pin of nRF52840", 4.35 to 5.5 V; whether it
   also powers the SoM is not stated, so treat it as possibly powering. Plugging a
   cable into USB2 back-feeds 5V_AUX through F2 (and from there U2's input, the
   3V3_AUX buck), against U3's output.
3. **The B-SoM's 3V3 input has no supply.** B404X datasheet: 3V3 is "System
   power in, supply a fixed 3.0-3.6v power", at least 150 mA, 500 mA recommended.
   On Okapi PARTICLE_3V3 is fed only by MS1's "3V" pin, which is the Feather's
   regulator output. With a B-SoM and no Feather, nothing powers the SoM's
   processor. Has a B-SoM ever run on an Okapi? (Question for Andy.)
4. **The B-SoM's VCC wants 3.6 to 4.2 V** (B404X datasheet) and is fed from V_LI
   through U10. A Li-ion cell spends part of its discharge below 3.6 V.
5. **The firmware never drives PARTICLE_EN** (README "The 66-minute timer",
   2026-11-05; Okapi_Library Okapi.cpp:451 writes the latch high and never sets the
   pin as an output). B7 item 1.
6. **Signals into an unpowered module.** TX (through nothing on the Particle
   side), PARTICLE_RTS/CTS/GPIO go straight from the MCU to the module's pins. With
   the module off and the MCU driving a line high, current flows into the module's
   input protection diodes and part-powers it. The I2C pair is already isolated by
   U34 (its EN is PARTICLE_3V3); the UART and GPIO lines are not.
7. **U10's CT pin is unconnected**, so the switch turns on at its fastest slew
   into the module's input capacitance. TPS22917: 2 A continuous, 2.5 A pulsed
   (< 300 µs, 2 %), full-time reverse current blocking (-1 µA max). The Boron's and
   the B-SoM's peak currents during cellular transmit are not yet checked against
   2 A (UNVERIFIED; Particle datasheets to read).
8. **The UART is shared** among the MCU, the module and U23 (FT231X, through R38
   and R40). Not a v0.8 defect by itself; noted because item 6's fix sits on the
   same lines.

## 3. Netlist changes for v0.8

Each is one schematic change with the usual gates (Eagle-net check retired for
v0.8 work; netlist diff, round trip, ERC, DRC, pad-net table), committed alone.

| # | Change | Why | Check |
|---|---|---|---|
| N1 | MS1 pin 26 (USB) off 5V_AUX: no-connect, flagged on both sides | removes the path the firmware cannot switch (problem 1) | netlist: 5V_AUX loses one node; MS1 26 no_connect |
| N2 | F2 off: PARTICLE_BSOM_VUSB fed only by USB2's VDD | the B-SoM sees VBUS only when a cable is in USB2; no back-feed into 5V_AUX (problem 2) | netlist: F2 removed or DNP; 5V_AUX and PARTICLE_BSOM_VUSB disjoint |
| N3 | A 3.3 V regulator for the B-SoM: input PARTICLE_VCC, output PARTICLE_3V3 through a jumper (JPx, open on a Feather build) | the B-SoM needs 3.0 to 3.6 V at 500 mA recommended (problem 3); the jumper keeps it off the Feather's 3V output pin | part chosen from its datasheet (dropout at the lowest V_LI, quiescent current when PARTICLE_VCC is up, output current ≥ 500 mA); footprint on top (Okapi is single-sided) |
| N4 | U10 CT capacitor | bounded inrush into the module's input capacitance (problem 7); value from TPS22917 Equation 5 once the module's input capacitance and the limit are chosen | value is a proposal until computed |
| N5 | Series resistors or a buffer with output enable on TX, PARTICLE_RTS, PARTICLE_CTS, PARTICLE_GPIO, enabled by PARTICLE_3V3 (like U34 for I2C) | no back-powering of an unpowered module (problem 6) | a buffer (e.g. a TXS0104 like U27/U29/U42, already on the BoM) or 1 kΩ series as the minimum; decision for Andy |
| N6 | PARTICLE_PG: PARTICLE_3V3 to a spare expander input (U41 GPA2, pad 17, unconnected today), through a divider or directly (3.3 V into a 3V3_CORE part) | the firmware can see whether the module is powered, for the pulse, the hold, and diagnostics | U41 pin 17 on the new net; firmware reads it |
| N7 | VCC range for the B-SoM: decide whether a B-SoM build needs a boost to keep VCC ≥ 3.6 V, or accept that the modem is unavailable below it | problem 4 | decision for Andy; no change if accepted |
| N8 | Symbol values: MS1 "Particle (Feather)", J9 "Particle (B-SoM M.2)"; a silkscreen note that only one is fitted | the two sockets are one module served two ways | BoM and silk read |

Unchanged on purpose: U10, U8 and R20 (the hourly fallback and the session bound
stay as the README describes them); Q3 and R19 (off by default); WD_DONE (the
module ends its own session); RST_TRIG through Q4 (the module can still reset the
logger; whether it should is a firmware-policy question, section 4); U34 on the I2C
pair.

## 4. Firmware (B7, Okapi_Library)

1. **PARTICLE_EN as an open-drain output** on U41 GPB7 (`pinMode(..., OPEN_DRAIN,
   Port::B)`), released (high) at begin so R19 holds Q3 off.
2. **Power the module**: pulse PARTICLE_EN low 20 to 30 ms (README). Default
   policy: pulse when there are rows to send.
3. **Hold the module on** for other uses: drive PARTICLE_EN low and keep it low
   (the TPL5111 then stays on past its interval, README item 3); release to return
   to the timer. An API such as `particleOn()`, `particleHold(bool)`, `particleOff()`
   is a proposal; names follow the house style once agreed.
4. **Know it is on**: read PARTICLE_PG (N6) before talking to the module.
5. **No lines driven into an unpowered module**: leave TX idle and RTS/CTS/GPIO as
   inputs until PARTICLE_PG is high (needed even with N5, harmless with it).
6. **Names**: the firmware's FeatherEN, FeatherGPIO, FeatherRTS, FeatherCTS follow
   the schematic to the PARTICLE_ names, callers migrated.
7. **Policy on RST_TRIG**: the 2019 Boron sketch resets the logger 90 s after it
   starts (Boron_Test.ino lines 91-97, per the 2026-11-10 NW-Sim scoping report;
   the deployed binary not yet compared). Decide whether the module may reset the
   logger, and when.

## 5. Tests

1. **NW-Sim**: an `okapi-0.8` board version (the per-version structure built for
   Margay) with U10, the TPL5111 (timer, manual drive through Q3, DONE) and a
   scripted Particle peer that is powered only through PARTICLE_VCC. Cases: the
   timer wake, the logger's pulse, the hold, DONE ending a session, and an
   `okapi-0.7` case that shows the module powered by 5V_AUX alone (the bug, pinned).
   See the scoping report, 2026-11-10-nwsim-okapi-scope-agent-report.md.
2. **Bench, on the first v0.8 board**: module current with 5V_AUX on and
   PARTICLE_EN released (should be zero); the pulse powers it; the hold keeps it
   past 66 min; DONE drops it; a B-SoM boots from N3's regulator alone; a cable in
   USB2 leaves 5V_AUX at 0 V with the board unpowered.

## 6. Documentation

The README's "The 66-minute timer" describes the switched path only. Until v0.8
exists it should say that on a Feather build the module is also powered from
5V_AUX through the USB pin; after v0.8 the switched path is the only one and the
text stands.

## 7. Decisions for Andy

1. N1 and N2: no-connect the Feather's USB pin and lift F2 (recommended), or a
   second load switch on the USB path.
2. N3: **decided (Andy 2026-11-10): the B-SoM gets its own 3.3 V regulator, fed
   from the switched PARTICLE_VCC**, not a main-board rail. 3V3_CORE (U9, TPS797;
   rated about 10 mA, from memory, UNVERIFIED) cannot carry 150 to 500 mA, and
   3V3_AUX would tie the module to the sensor rail again. Still open: whether the
   B-SoM build is wanted at all.
3. N5: a buffer with output enable, or series resistors.
4. N7: accept the modem's 3.6 V floor on a B-SoM build, or boost VCC.
5. RST_TRIG: may the module reset the logger.
6. The firmware API names.

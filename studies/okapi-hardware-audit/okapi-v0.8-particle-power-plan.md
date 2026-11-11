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
| SCK_BUF, MOSI_BUF | U25 SN74AUP3G34 outputs (one-way from IC1 SCK/MOSI; also SD1) | 11 SCK / 12 MOSI | 54 / 52 |
| MISO | IC1 PB6 direct (also SD1, ISP1, U27) | 13 MISO | 50 |
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
   processor. Has a B-SoM ever run on an Okapi? No (Andy 2026-11-11): the
   B-SoM socket has never been used, which agrees with the netlist.
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
   (< 300 µs, 2 %), and reverse current blocking that trips only at IRCB = -0.5 A
   typical (-1 A max) while the switch is on; -1 µA is the leakage once blocked
   (corrected 2026-11-10: first read as -1 µA throughout). The Boron's and
   the B-SoM's peak currents during cellular transmit are not yet checked against
   2 A (UNVERIFIED; Particle datasheets to read).
8. **The UART is shared** among the MCU, the module and U23 (FT231X, through R38
   and R40). Not a v0.8 defect by itself; noted because item 6's fix sits on the
   same lines.

## 2a. USB power may be applied (Andy 2026-11-11)

Requirement: a user may program the Particle module over USB while it is
attached to the logger, so a USB cable is a supported condition, not a fault.
USB2 stays on the board.

Where USB power goes, by socket (source report:
sources/2026-11-10-particle-boron-bsom-agent-report.md):

- **Boron.** Its VUSB pin is "internally connected to the VBUS of the USB port"
  (BR3), with no diode named. A cable in the Boron's own jack therefore puts the
  computer's 5 V on MS1 pin 26, which is 5V_AUX as built. N1 opens that path.
  The Boron's bq24195 charger also runs from USB and "will charge and power the
  device when USB source is plugged in" (BR3). Its battery pin is Li+, which on
  Okapi is PARTICLE_VCC, which U10 joins to the logger's cell. With U10 on, the
  Boron's charger can push current backwards through U10 into the cell until
  U10's reverse-current blocking trips at -0.5 A typical (-1 A max); with U10 off
  the switch blocks (-1 µA). The cell then has two chargers. The Boron's default
  charge current under Device OS: UNVERIFIED.
- **B-SoM.** VBUS (J9 pin 16) is USB detect for the nRF52840 (BX4), 4.35 to 5.5
  V. Particle's evaluation board feeds pin 16 from its USB connector and powers
  the SoM's VCC and 3V3 from the same USB node through a Schottky into its PMIC
  (EV2). On Okapi the SoM's VCC and 3V3 come only from PARTICLE_VCC, so with the
  logger not holding U10 on, a cable in USB2 tells the SoM that USB is present
  while nothing powers it. With N2, USB2's 5 V stops at J9 pin 16 and cannot
  reach 5V_AUX.

What this adds to section 3 (proposals):

| # | Change | Why | Check |
|---|---|---|---|
| N10 | Reverse blocking on PARTICLE_VCC that holds at any current (a switch with true reverse blocking in U10's place, or an ideal diode after it) | the Boron's charger must not charge the logger's cell through U10 | part from its datasheet; or accept U10's -0.5 A trip and disable charging in the Particle sketch, which does not cover a user's own Boron firmware |
| N11 | USB2's VBUS ORed into the Particle supply through a diode or ideal-diode switch, ahead of the regulation that serves VCC and 3V3 | a B-SoM programs over USB2 with the logger off, as on Particle's evaluation board (EV2) | needs regulation to the SoM's VCC 3.6 to 4.2 V from 5 V, which ties N11 to N7; a computer port gives 500 mA where the evaluation board asks 2000 mA without a battery (EV1); the alternative with no parts is that the logger holds the module on (`particleHold(true)`) while programming |

USB connectors (Andy 2026-11-11): **two connectors, decided**, for using both
at once and no switch position to get wrong. J10 (USB-C, GCT USB4105) stays on
the logger's FT231X; USB2 (vertical micro-USB, Molex 105133) stays on the B-SoM.

| # | Change | Why | Check |
|---|---|---|---|
| N12 | USB2 as a right-angle USB-C at the right board edge where USB2 is now (option A; 27 mm straight line from J9's USB pads; the strip beside the module is about 5 mm deep, fit unchecked), not beside J10 (option B: that edge holds U4, D1, J7, J8, J6 and J5; 78 mm from J9's pads; figures/okapi-v08-particle-plan.png), with 5.1 kΩ pull-downs on CC1 and CC2 as J10 has (R84, R85); Andy places the board in the box and designs the mounting plates (2026-11-11), so each port can face a drilled wall | one cable for both ports; a C-to-C cable supplies VBUS only when CC sees the pull-downs | proposal, not decided; footprint on top; enclosure openings are drilled in-house (Andy 2026-11-11), so a second port is not a constraint |

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

The README's hardware list says the logger connects by micro-USB; J10 is USB-C.

The README's "The 66-minute timer" describes the switched path only. Until v0.8
exists it should say that on a Feather build the module is also powered from
5V_AUX through the USB pin; after v0.8 the switched path is the only one and the
text stands.

## 6a. The module resets and reprograms the logger (Andy 2026-11-10)

Requirement: the Particle module can reset the logger and reprogram it, whether
the logger is hung or running normally (reset, then program).

From the netlist (bcfb2e8):
- **Reset**: RST_TRIG (MS1 GPIO9, J9 PWM0) drives Q4 (2N7002, R54 10 k gate
  pull-down), whose drain is on RST (IC1 RESET, also ISP1, S4, C39 0.1 µF, R52
  10 k pull-up, U41's ~RESET). The module can pulse or hold the logger in reset.
- **Program over the bootloader**: TX/RX are the MCU's UART0, which is where the
  NW1284p bootloader listens (Arduino_Boards boards.txt: upload.protocol=arduino,
  i.e. STK500v1, 57600 baud, maximum sketch 130048 bytes). Reset through RST_TRIG,
  then speak STK500v1 on Serial1 within the bootloader's post-reset window. This
  path exists on today's board; it needs only Particle-side firmware (an STK500v1
  client, the hex stored on the module, a cloud trigger) and a bench check of the
  reset-to-bootloader timing. Caveat: U23 (FT231X) shares the lines through
  R38/R40 330 Ω; with a USB cable attached the two can contend.
- **Program over ISP** (the only recovery for a damaged bootloader or fuses): not
  possible today. The module's SCK and MOSI (MS1 11/12, J9 54/52) are on
  SCK_BUF/MOSI_BUF, the output side of U25 (SN74AUP3G34, a one-way buffer from the
  MCU to the SD card, powered from 3V3_AUX, no output enable). MISO is direct.
  The module can therefore not drive the MCU's SCK and MOSI.

Netlist change, proposed:

| # | Change | Why | Check |
|---|---|---|---|
| N9 | A path from the module's SCK and MOSI to the MCU's SCK and MOSI that is enabled only while the module holds the logger in reset (a two-channel tristate buffer, output enable from RST_TRIG), and U25 kept from fighting it (a buffer with output enable in its place, disabled by the same signal) | ISP from the module, for a logger whose bootloader or fuses are damaged | the SD card's CS stays deasserted during ISP (SD_CS_BUF through U25 today); MISO shared by SD1, U27 and the MCU; part choices from datasheets |

Firmware, Particle side (a new sketch, replacing the 2019 Boron_Test.ino): reset
policy (section 7, item 5), the STK500v1 client, an ISP programmer once N9
exists, and the hex delivered by the Particle cloud. The research report
(sources/2026-11-10-particle-boron-bsom-agent-report.md) covers SPI pins, storage
and existing libraries for both modules.

## 6b. From the Boron/B-SoM report (2026-11-10)

Source: sources/2026-11-10-particle-boron-bsom-agent-report.md (Particle docs,
cited per fact; Particle's eval-board, PM-BAT and Boron schematics traced). Verified
by me: the NW1284p bootloader is Optiboot 8.0, UART0, 57600 baud, BIGBOOT (strings
in Arduino_Boards bootloaders/NW/NW1284p.hex).

- **Power**: Boron runs from Li+ 3.6 to 4.2 V; its 3V3 pin is an output (1000 mA)
  that "CANNOT be used to power the Boron"; VUSB is its charger input. B404X and
  B524 take VCC 3.6 to 4.2 V and a 3V3 input of 3.0 to 3.6 V (150 mA minimum, 500
  mA recommended); VBUS is USB detect only. Peaks: Boron Li+ 490 mA; B404X 600 mA
  (2 A supply recommended); B524 and B504e "at least 2 A". No EN pin on the
  B-SoM; the Boron's EN still leaves 70 µA flowing.
- **One sketch for both**: every logger-facing line has the same Device OS name on
  both sockets (Serial1 TX/RX, RTS D2, CTS D3, PARTICLE_GPIO A5, WD_DONE A3,
  RST_TRIG D4, Wire D0/D1, SPI). Exceptions: on an M-SoM, J9 pin 43 is SWCLK with
  a boot-time pull-down; a B-SoM sketch leaves PMIC detection off.
- **Reprogramming**: both modules have a 2 MB file system (a full 130048-byte
  sketch is about 6 %); Asset OTA needs Device OS 5.5.0 or later; Particle's
  "Arduino Uno Asset OTA" example drives an STK500v1 upload (no license, no
  verify, 328P only: a reference, not a dependency). Both can be SPI master.
- **Lifecycle**: BRN404X, B404X, B524 and B504e listed GA; the Axion datasheet's
  comparison marks Boron 404X deprecated, which contradicts the Boron's ordering
  table (unresolved).

Revisions proposed by the report (not yet decided):
- **N3, revised**: fit one 3.3 V regulator from PARTICLE_VCC to PARTICLE_3V3 on
  every board and leave the Boron's 3V pin (MS1 pin 2) unconnected. The regulator
  then never meets the Boron's own buck, so no jumper; PARTICLE_3V3 still feeds
  U34, D7 and the pull-ups on a Boron build. Candidates below; no decision.

### The 3.3 V regulator: candidates (no decision; Andy 2026-11-10)

The load: the B-SoM's 3V3 input, 3.0 to 3.6 V, 150 mA minimum, 500 mA recommended
(Particle B404X datasheet, via the report), plus U34, D7 and the pull-ups. The
input: PARTICLE_VCC, the cell through U10 (about 3.0 to 4.2 V), or a fixed 3.9 V
if N7's buck-boost is fitted. The regulator is powered only while U10 is on, so
its quiescent current matters only within a session.

| | TPS62822DLCT (buck) | TLV755P (LDO) | TPS631011 (buck-boost) |
|---|---|---|---|
| On Okapi's BoM | **yes: U2** (makes 3V3_AUX), with L3 1 µH Würth 74404032010, C8/C9 22 µF GRM219R61C226ME15L, R6 820 k / R7 180 k (0.6 V × (1 + 820/180) = 3.33 V), C6 68 pF; every support part already stocked | no | no; Particle's choice for 3V3 on PM-BAT |
| Source read | SLVSDV6C, TI, read 2026-11-10 | SBVS320D, via the report | SLVSGO6B, via the report |
| Input | 2.4 to 5.5 V | 1.45 to 5.5 V | 1.6 to 5.5 V |
| Output current | 2 A (Recommended Operating Conditions); high-side limit 2.7 A min | 500 mA | 2 A for VIN ≥ 3 V at 3.3 V |
| Low cell | 100 % mode: regulates down to VIN(min) = 3.3 V + I × (35 mΩ + L3's DCR) (Equation 3), about 3.35 V at 500 mA with L3's DCR taken as tens of mΩ (UNVERIFIED, Würth datasheet to read); below that the output follows VIN less that drop, still inside the B-SoM's 3.0 V floor down to a cell of about 3.05 V | 238 mV max dropout at 500 mA: regulates down to about 3.54 V, then follows VIN less the dropout | regulates 3.3 V across the whole cell range |
| Efficiency | switching, high | 3.3/VIN: 79 % at 4.2 V | switching |
| IQ | 4 µA typ, 10 µA max; shutdown 0.05 µA typ | 25 µA typ | 8 µA typ |
| Start-up | EN thresholds 0.9 V rising / 0.7 V falling, "do not leave EN floating" (tie EN to its VIN, so it starts when U10 does); soft start about 1 ms after a 250 µs delay; starts into a pre-biased output | (report) | (report) |
| Off | active output discharge, which needs VIN present, so with U10 off the output decays through its load | active output discharge | active output discharge, load disconnect |
| Other | 2.2 MHz switching beside the cellular module (layout and EMI to watch); QFN-8 2 × 1.5 mm; power-good output available | quiet; simplest; "excessive reverse current potentially damages this device" (no back-feed with the Boron's 3V pin unconnected) | WCSP package |

If N7's 3.9 V buck-boost is fitted, every candidate sees a fixed 3.9 V and the
LDO's 600 mV of headroom removes its only weakness.

### The telemetry supply chain (2026-11-10/11)

- **Source decided (Andy 2026-11-11): the Li-ion cell, V_LI**, through U10, "seeing
  as we do not have any other power source currently available". The module's
  supply does not come from V_HP or the main rails.
- **Separate from the main rails (recommended, 2026-11-10).** U3 (TPS61032, 5V_AUX)
  is rated 1000 mA at 5 V from 1.8 V in, with a 3.6 A minimum switch limit
  (SLUS534G); about 1.5 to 2 A at ordinary battery voltages by my estimate from
  the switch limit, shared by the 5 V sensor switches, the ADS1115, the DAC and
  U2. A Cat 1 B-SoM's 2 A peaks do not fit beside them, and sharing would tie the
  module to the sensor rail again.
- **One buck-boost, not boost-then-buck (recommended).** The cell (about 3.0 to
  4.2 V) straddles the module's 3.9 V, which is a buck-boost's job in one stage;
  boost-then-buck would convert twice for the same result.
- The chain, if N7 is taken: V_LI -> U10 -> 3.9 V buck-boost -> PARTICLE_VCC ->
  3.3 V regulator -> PARTICLE_3V3. N7 itself and the 3.3 V part are still open.
- **N7**: a 3.9 V buck-boost after U10 (Particle's PM-BAT uses a TPS63020 with
  220 µF), serving both modules and the bottom of the cell, or accept the 3.6 V
  floor. Candidates: TPS63020, TPS63802.
- **U10's margin**: Cat M1 modules sit well inside 2 A; Cat 1 modules (B524,
  B504e) reach it.

## 7. Decisions

1. N1 and N2: no-connect the Feather's USB pin and lift F2 (recommended), or a
   second load switch on the USB path. **To decide in this conversation (Andy
   2026-11-10), once the Boron/B-SoM report is in**
   (sources/2026-11-10-particle-boron-bsom-agent-report.md). **Direction set
   (Andy 2026-11-11): USB power may be applied while the module is attached, and
   USB2 stays (section 2a).** N1 and N2 follow from it. **N10 decided (Andy
   2026-11-11): reverse blocking in hardware.** **N11 direction set (Andy
   2026-11-11): USB2 powers the B-SoM, so it programs over USB with the logger
   off.** This makes N7's buck-boost required: the OR of USB 5 V and the switched
   cell feeds it, and it holds VCC at 3.6 to 4.2 V. Where N10 sits relative to
   N7, and the OR part, are worked out when drawn.

   How a B-SoM is programmed (B404X datasheet, docs.particle.io, read
   2026-11-11): the module "supports a USB interface for programming the device
   and for USB serial (CDC) communications" and has no USB connector of its own,
   so the base board supplies one (USB2: D+ pin 11, D- pin 13, VBUS detect pin
   16); the bootloader updates the user application "via several different
   methods, USB, OTA, Serial Y-Modem"; and the SWD interface is "4 pads at the
   bottom" of the module, out of reach in a socket. The datasheet recommends a
   battery or power on Li+ when bringing up a board, because the default USB
   input current limit can cause brownouts.
2. N3: **decided (Andy 2026-11-10): the B-SoM gets its own 3.3 V regulator, fed
   from the switched PARTICLE_VCC**, not a main-board rail. 3V3_CORE (U9, TPS797;
   rated about 10 mA, from memory, UNVERIFIED) cannot carry 150 to 500 mA, and
   3V3_AUX would tie the module to the sensor rail again. **The B-SoM build is
   wanted, and is the new standard (Andy 2026-11-10)**; the Feather socket stays
   as the alternative. One power design and one logger-side interface for both
   is the goal.

Items 3 to 6 are mine to bring as recommendations (Andy 2026-11-10: they need the
firmware and the board in mind, which is this work's job, not his):

3. N5, recommended: a TXS0104 (the part already used three times, U27, U29, U42)
   on TX, RX, PARTICLE_RTS and PARTICLE_CTS, A side 3V3_CORE, B side and OE on
   PARTICLE_3V3 as U34 does for I2C, so the lines open when the module is off;
   PARTICLE_GPIO, RST_TRIG and WD_DONE checked one by one (RST_TRIG and WD_DONE are
   driven by the module, not into it). Series resistors are the fallback if board
   space forbids it. To confirm against the agent's pin mapping (directions and
   any open-drain lines) before it is drawn.
4. N7: wait for the agent's B-SoM VCC range and peak current; the choice is
   between accepting the modem's floor (no parts) and a boost.
5. RST_TRIG, recommended: keep it. Okapi has no hardware watchdog for its MCU
   (Okapi.cpp comment, 2026-10-30), so the module resetting a logger that has
   gone silent is the board's only recovery path short of a site visit. The
   policy belongs in the Particle sketch: reset only when the logger has missed
   its backhaul for a set number of intervals or on a remote command, never on a
   fixed timer after start-up as the 2019 sketch does (Boron_Test.ino 91-97,
   unconfirmed against the deployed binary).
6. API names, proposed, in Okapi_Library's camelCase: `particlePower()` (the
   pulse), `particleHold(bool)` (hold on, release), `particlePowered()` (reads
   PARTICLE_PG). Settled when B7 touches the code.
7. From the module report: N3 as revised (always-fitted regulator, Boron 3V pin
   unconnected) in place of the jumper; N7 buck-boost or not; the target B-SoM
   (B404X Cat M1, or a Cat 1 part at 2 A); whether J9 supports the M-SoM (moves
   PARTICLE_GPIO off pin 43); ISP (N9) or the UART bootloader only; bulk
   capacitance on PARTICLE_VCC with N4.

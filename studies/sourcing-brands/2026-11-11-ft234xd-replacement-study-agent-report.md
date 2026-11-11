# FT234XD as a replacement for the FT231XQ on Margay and Okapi: feasibility and sourcing study

Status: COMPLETE (2026-11-11)

Agent report, 2026-11-11. Mirrors the structure of `2026-11-11-cp2102n-replacement-study-agent-report.md`.

## Sources checked (log, dead ends included)

- 2026-11-11 local: read `2026-11-11-cp2102n-replacement-study-agent-report.md` (board facts reused: netlists at Project-Margay 151562f and Project-Okapi 59ba6ea, the 3V3_FTDI trace, avrdude 6.3 source, the FT231X Table 5.1 row, the U2/U23 neighbor gaps), `2026-11-11-usb-uart-bridge-agent-report.md` (survey) and `2026-11-11-ftdi-stock-search-agent-report.md` (IN PROGRESS when read; current FT231X stock left to it).
- 2026-11-11 **FTDI FT234XD datasheet FT_000753 Version 1.2 (Aug 2015), 37 pages**, `curl -L https://web.archive.org/web/2023id_/https://www.ftdichip.com/Support/Documents/DataSheets/ICs/DS_FT234XD.pdf`; the 2024 and 2026 Wayback copies of `https://ftdichip.com/wp-content/uploads/2020/08/DS_FT234XD.pdf` are byte-identical (`cmp`), so v1.2 is the current revision as far as the archive shows. Saved here as `FT234XD-datasheet-v1.2.pdf`. Revision history (App. C): v1.0 January 2013, v1.1 February 2013 "Added clarification that we are 5V tolerant", v1.2 Aug 2015 "Added reference to WDFN chip dimensions". ftdichip.com direct by curl: HTML, DEAD END. `.../wp-content/uploads/2023/09/DS_FT234XD.pdf` (guessed): not archived, DEAD END.
- 2026-11-11 **FTDI FT230X datasheet FT_000566 Version 1.4 (PDF dated 2016-05-24), 44 pages**, `curl -L https://web.archive.org/web/2024id_/https://ftdichip.com/wp-content/uploads/2020/08/DS_FT230X.pdf` (2026 snapshot gives the same Version 1.4). Saved here as `FT230X-datasheet-v1.4.pdf`. The 2023 snapshot of the old `Support/Documents/DataSheets/ICs/DS_FT230X.pdf` URL: HTML, DEAD END. `.../2023/06/DS_FT230X.pdf` (guessed): DEAD END.
- FT231X datasheet FT_000565 Version 1.4: the copy already saved here by the CP2102N study (`FT231X-datasheet-v1.4.pdf`), text by `pdftotext -layout`.
- 2026-11-11 `.gitignore` check: `git check-ignore -v` reports `NW-Status/.gitignore:7: studies/**/*.pdf`, so the two new PDFs are local only.

## Datasheet facts used below

FT234XD (FT_000753 v1.2):

- Page 1: "Configurable CBUS I/O pin"; "Transmit and receive LED drive signals"; "True 3.3V CMOS drive output and TTL input ... Tolerant of 5V input"; "8mA (active-typ) and 70uA (suspend-typ)"; "Extended operating temperature range; -40 to 85⁰C"; "compact Pb-free 12 pin DFN package (3mm x 3mm)".
- Sec. 1.2: FT234XD-R tape and reel, 5,000 per reel; FT234XD-T tray, 490 per tray.
- Table 3.1 (power): pin 4 VCC "5 V (or 3.3V) supply to IC"; pin 9 VCCIO "1.8V – 3.3V supply for the IO cells"; pin 3 3V3OUT "3.3V output at 50mA. May be used to power VCCIO"; pins 5 and 13 GND (13 is the center pad).
- Table 3.2: pin 1 USBDM, pin 12 USBDP, pin 2 RESET# "Reset input (active low)".
- Table 3.3: pin 7 TXD, pin 10 RXD, pin 8 RTS# "Request to Send Control Output / Handshake Signal", pin 11 CTS#, pin 6 CBUS0 "The default configuration is TXDEN". Note 1: "When used in Input Mode, the input pins are pulled to VCCIO via internal 75kΩ (approx.) resistors."
- **There is no DTR#, DSR#, DCD# or RI# pin, and only one CBUS pin (CBUS0).** Table 3.4 lists every CBUS0 option; DTR is not among them (TRI-STATE, DRIVE 1, DRIVE 0, TXDEN, PWREN#, TXLED#, RXLED#, TX&RXLED#, SLEEP#, CLK24/12/6MHz, GPIO, BCD Charger, BCD Charger#, BitBang_WR#, BitBang_RD#, VBUS Sense, Time Stamp, Keep_Awake#). TX&RXLED#: "LED drive – pulses low when transmitting or receiving data via USB."
- Table 5.1 (absolute maximum): VCC −0.3 to +5.5 V; VCCIO −0.3 to +4.0 V; USBDP/USBDM −0.5 to +3.63 V; "DC Input Voltage – High Impedance Bi-directional (powered from VCCIO) −0.3 to +5.8 V"; DC output current 22 mA.
- Table 5.2: VCC 2.97 / 5 / 5.5 V; VCCIO 1.62 to 3.63 V; Icc1 6.5 / 8 / 8.3 mA normal operation; Icc2 125 µA suspend; 3V3 regulator output 2.97 / 3.3 / 3.63 V.
- Table 5.3 (VCCIO 3.3 V): VOH min 2.97 V at ±2 mA, VOL max 0.4 V; VIH 2.0 V, VIL 0.8 V; Rpu and Rpd 40 / 75 / 190 kΩ; Iin and Ioz ±10 µA max, Ioz at "Vin = 5.5V or 0".
- Table 5.7: MTP "Write Cycle 2,000 Cycles", data retention 10 years.
- Sec. 6.1 / Fig. 6.1 bus-powered: 27 Ω series on USBDM/USBDP, 47 pF to GND on each, ferrite bead in VBUS, 10 nF, 4.7 µF and 100 nF on VCC, 100 nF on 3V3OUT, VCCIO tied to 3V3OUT, RESET# shown tied to the 3V3 node.
- Sec. 7.5 / Fig. 7.5 "Single LED Configuration": LED and 270 Ω from VCCIO into CBUS0 configured as TX&RXLED#; "In this configuration the FT234XD will drive only a single LED."
- Table 8.1 defaults: VID 0403h, PID 6015h, serial number enabled, product description "FT234XD BASIC UART", max bus power 90 mA, bus powered, **CBUS0 = TXDEN**, Load VCP Driver enabled. Sec. 8.2.1: MTP programmed "over USB ... the FT_Prog utility is used", or by D2XX commands.
- Sec. 9.1: "nominally 3.00mm x 3.00mm. The solder pads are on a 0.45mm pitch ... Refer to the WDFN column"; center pad "internally connected to ground". (Dimension table is a figure; read in section 5.)

FT230X (FT_000566 v1.4), QFN-16 tables 3.1 to 3.3: pin 10 VCC, pin 1 VCCIO, pin 8 3V3OUT "3V3 output at 50mA", pins 3, 13, 17 GND (17 = center pad), 7 USBDM, 6 USBDP, 9 RESET#, 15 TXD, 2 RXD, 16 RTS#, 4 CTS#, CBUS0 pin 12 (default TXDEN), **CBUS1 pin 11 (default RXLED#), CBUS2 pin 5 (default TXLED#)**, CBUS3 pin 14 (default SLEEP#). **The FT230X has no DTR# either.** Its Table 5.1 high-impedance input row is the same −0.3 to +5.8 V "(powered from VCCIO)"; Table 5.2 Icc1 6.5 / 8 / 8.3 mA, 3V3 2.97 / 3.3 / 3.63 V; Table 8.1 VID 0403h, PID 6015h; MTP write cycles 2,000. Sec. 1.2: FT230XQ-R 5,000 per reel, FT230XQ-T tray 490.

FT231X (FT_000565 v1.4), for comparison: the same Table 5.1 row ("High Impedance Bi-directional (powered from VCCIO) −0.3 to +5.8 V"), Table 5.2 Icc1 8 / 8 / 8.4 mA, "3V3 output at 50mA", Table 8.1 VID 0403h, PID 6015h, QFN CBUS0 pin 15 TXDEN, CBUS1 pin 14 RXLED#, CBUS2 pin 7 TXLED#, CBUS3 pin 16 SLEEP#.

## 1. Pin-by-pin mapping, FT231XQ (QFN-20) to FT234XD (DFN-12) and FT230XQ (QFN-16)

Board nets from the CP2102N study's netlists (section 1 of that report).

| FT231XQ pin | Margay U2 net | Okapi U23 net | FT234XD pin | FT230XQ pin | Note |
|---|---|---|---|---|---|
| 17 TXD | R7 330 Ω to MCU RXD0 | R38 330 Ω to RX | 7 TXD | 15 TXD | same |
| 1 RXD | R9 330 Ω to MCU TXD0 | R40 330 Ω to TX | 10 RXD | 2 RXD | same I/O cell rating (section 2) |
| 18 DTR# | C1 100 nF to RST | C39 100 nF to RST | **none** | **none** | **lost**: move the 100 nF to RTS# |
| 19 RTS# | no connect | no connect | 8 RTS# | 16 RTS# | **new use: drives the 100 nF** (section 1b) |
| 6 CTS# | GND | GND | 11 CTS# | 4 CTS# | tie to GND as now |
| 4 DSR#, 5 DCD#, 2 RI# | no connect | no connect | none | none | not used, nothing lost |
| 14 CBUS1 (default TXLED#, v1.6) | TX_LED, R8 330 Ω to D2 red | R39 330 Ω to D4 red | **none** | 11 CBUS1 (TXLED#, v1.7) | FT234XD: one LED only (section 1c) |
| 7 CBUS2 (default RXLED#, v1.6) | RX_LED, R5 330 Ω to D2 blue | R36 330 Ω to D4 blue | 6 CBUS0 (default **TXDEN**) | 5 CBUS2 (RXLED#, v1.7) | FT234XD needs MTP programming |
| 15 CBUS0, 16 CBUS3 | no connect | no connect | none | 12, 14 | – |
| 8 USBDP, 9 USBDM | R4/R3 27 Ω, 12 pF | R35/R34 27 Ω, 12 pF | 12 USBDP, 1 USBDM | 6 USBDP, 7 USBDM | keep the 27 Ω (FTDI Fig. 6.1, same as FT231X) |
| 12 VCC | VUSB through D1 BAT43WS | VUSB | 4 VCC | 10 VCC | same |
| 10 3V3OUT | 3V3_FTDI | 3V3_FTDI | 3 3V3OUT | 8 3V3OUT | same, 50 mA |
| 20 VCCIO | 3V3_FTDI | 3V3_FTDI | 9 VCCIO | 1 VCCIO | same |
| 11 RESET# | 3V3_FTDI (tied) | 3V3_FTDI (tied) | 2 RESET# | 9 RESET# | same tie (FTDI Fig. 6.1 shows it) |
| 3, 13 GND, EP | GND | GND | 5, 13 (EP) | 3, 13, 17 (EP) | same |

Reading: apart from DTR# and the second LED pin, every net the boards use maps onto the FT234XD one for one, with the same passives. Nothing like the CP2102N's VBUS divider or RSTb pull-up is added. The FT230X maps the same way but keeps both LED pins at their FT231X defaults; it too loses DTR#.

Okapi check (asked): fresh netlists, `kicad-cli sch export netlist --format kicadxml` of `Project-Margay/Hardware/KiCAD/Margay.kicad_sch` at **8706d25** and `Project-Okapi/Hardware/KiCAD-10import/Okapi.kicad_sch` at **2734fc4** (both exit 0; `git status --short` identical before and after: only the pre-existing untracked `.claude/` and an Okapi backup zip), parsed with the CP2102N study's `nets.py`. Okapi U23 pin 14 CBUS1 → `Net-(U23-CBUS1)` → R39 330 Ω → D4 RED_CATH; pin 7 CBUS2 → R36 330 Ω → D4 BLUE_CATH; D4 ANODE on `3V3_CORE` (45 nodes); D4 GREEN_CATH → R37 (not the bridge). Pin 18 DTR# → net `DTR` → C39 0.1 µF → `RST` (8 nodes: IC1 pin 4 RESET, R52 10 k, ISP1, Q4, S4, U41 MCP23018 RESET). Pin 19 RTS# unconnected. Margay U2: pin 14 CBUS1 → `TX_LED` → R8 → D2 RED_CATH; pin 7 CBUS2 → `RX_LED` → R5 → D2 BLUE_CATH; D2 ANODE on `3V3`; pin 18 → `/Digital_Core/DTR` → C1 0.1 µF; pin 19 unconnected. **Okapi uses CBUS1/CBUS2 exactly as Margay does.** U2/U23 pin nets are unchanged from the CP2102N study's commits.

### 1b. Auto-reset from RTS# instead of DTR#

- **The CP2102N study already showed for avrdude 6.3** (tag v6.3, `arduino.c` lines 92 to 98; `ser_posix.c` `ctl |= (TIOCM_DTR | TIOCM_RTS)`; `ser_win32.c` `SETDTR ... SETRTS`) that `-c arduino` drives DTR and RTS together through one call, `serial_set_dtr_rts()`. This machine still has only `~/.arduino15/packages/arduino/tools/avrdude/6.3.0-arduino17` installed (`ls`).
- **New: the avrdude the current Arduino AVR core installs.** `~/.arduino15/package_index.json` (parsed): `arduino:avr` 1.8.6 depends on avrdude `6.3.0-arduino17`; **`arduino:avr` 1.8.7 depends on `8.0.0-arduino1`**. The NorthernWidget platform 0.3.1 declares no tool dependencies (`package_NorthernWidget_index.json`) and calls `{runtime.tools.avrdude.path}` (`platform.txt` line 12), so it uses whichever Arduino avrdude is installed. A fresh IDE with `arduino:avr` 1.8.7 therefore runs avrdude 8.0.
- avrdude v8.0 source (tag v8.0, commit d8c8cf1, `curl https://raw.githubusercontent.com/avrdudes/avrdude/v8.0/src/arduino.c`), `arduino_open()` lines 124 to 143: "This code assumes a negative-logic USB to TTL serial adapter"; `serial_set_dtr_rts(&pgm->fd, 0)`; `usleep(250*1000)`; "Pull the RTS/DTR line low to reset AVR" `serial_set_dtr_rts(&pgm->fd, 1)`; "Max 100 us: charging a cap longer creates a high reset spike above Vcc" `usleep(100)`; "Set the RTS/DTR line back to high" `serial_set_dtr_rts(&pgm->fd, 0)`; `usleep(100*1000)`; then `stk500_getsync()`. `src/ser_posix.c` lines 348 to 373: `ctl |= (TIOCM_DTR | TIOCM_RTS)` / `ctl &= ~(TIOCM_DTR | TIOCM_RTS)` in one `TIOCMSET`. `src/ser_win32.c` lines 288 to 289: `EscapeCommFunction(hComPort, is_on? SETDTR: CLRDTR); EscapeCommFunction(hComPort, is_on? SETRTS: CLRRTS);`. `-x noautoreset` (line 52) disables both.
- **So in both avrdude generations RTS gets the same edge as DTR**: on POSIX in the same ioctl, on Windows one call later. The 8.0 sequence differs from 6.3 in shape (a short assert, then release, rather than release-then-hold), but it differs identically for both lines, so moving C1/C39 from DTR# to RTS# changes nothing. The 8.0 change applies to the present FT231X boards too. With 100 nF into the 10 kΩ pull-up (Margay R2, Okapi R52), RC = 1 ms (arithmetic); the pin is asserted for 100 µs plus however long the second USB control transfer takes (USB latency not measured, UNVERIFIED), against the ATmega1284P's minimum reset pulse (DS40002070B, not re-read here; 2.5 µs from memory, UNVERIFIED). Uploads with avrdude 8.0 have not been tested on either board with either chip: UNVERIFIED.
- **Serial Monitor.** Arduino's pluggable monitor `arduino/serial-monitor` (`main.go` on `main`, fetched 2026-11-11, `go.bug.st/serial v1.6.3` in `go.mod`) declares settings `"rts"` and `"dtr"`, each `Selected: "on"`, and opens with `InitialStatusBits: &serial.ModemOutputBits{DTR: d.getDTR(), RTS: d.getRTS()}` (lines 218 to 220). `go.bug.st/serial` `serial_windows.go` lines 399 to 410 set `DTR_CONTROL_ENABLE` and `RTS_CONTROL_ENABLE` from those bits. On Linux the kernel raises DTR and RTS together on open (from memory, not re-read). **Opening the monitor asserts RTS exactly as it asserts DTR, so the board resets on monitor open as now.** Either line can be turned off in the IDE's monitor settings.
- **Precedent:** Adafruit, "FTDI Friend" guide (https://learn.adafruit.com/ftdi-friend?view=all , fetched 2026-11-11): "Arduino-derivatives and XBees use the RTS line for programming"; "By default, we've set it up so that it matches our FTDI cables. The 6th pin is RTS (as of Arduino IDE v1.8 this will work perfectly for uploading ...". Auto-reset from RTS# through a series capacitor is an established Arduino arrangement.
- **One behavioral difference to note:** RTS# is also the hardware-flow-control output. With flow control off (avrdude clears CRTSCTS, per the CP2102N study; the monitor sets no flow control) the FT-X holds RTS# at the host's setting. If some host program opened the port with RTS/CTS flow control on, RTS# would toggle with buffer state and could reset the MCU (inference from the pin's function in Table 3.3, UNVERIFIED). DTR# has no such second role. Low risk for Arduino use.

### 1c. LEDs with only CBUS0

The FT234XD has one LED-capable pin. Options:

1. **One combined activity LED (FTDI's own Fig. 7.5).** Program CBUS0 = TX&RXLED# ("pulses low when transmitting or receiving data via USB", Table 3.4) and drive one cathode. Keep R8/R39 (red) or R5/R36 (blue) and leave the other cathode resistor unfitted, or tie both cathode resistors to CBUS0 so the LED shows magenta on any traffic (two 330 Ω loads on one pin: red (3.3 − 1.9)/330 = 4.2 mA plus blue (3.3 − 3.0)/330 = 0.9 mA, about 5 mA, using the CP2102N study's CLD-CT1165 average VF; inside the 22 mA absolute maximum of Table 5.1, and the drive strength is configurable 4 to 16 mA, Table 8.1. Whether a 4 mA-setting pin holds VOL at 5 mA is not stated in Table 5.3, which is specified at ±2 mA; choose 8 mA drive in the MTP: a proposal).
2. **Drop one LED** (keep TXLED# or RXLED# only). Loses half the information; no advantage over option 1.
3. **Hand the freed cathode to the MCU.** Margay's D2 and Okapi's D4 already have their green cathodes on other drivers. The unused red or blue cathode could go to a spare MCU pin, but firmware cannot see USB traffic, so that is not an equivalent.

**Without MTP programming the LED is wrong, not dark:** the factory default for CBUS0 is TXDEN (Table 8.1), the RS-485 transmit-enable, which is driven high while the UART transmits (function from Table 3.4: "Enable transmit data for RS485"; its polarity, active high, is from memory, UNVERIFIED). With the LED wired from the 3.3 V rail into CBUS0, an unprogrammed chip would hold the LED **on** while idle and blink it off during transmission (inference, UNVERIFIED). Programming is therefore a required production step (section 4). The FT230X keeps both FT231X LED defaults (CBUS1 TXLED#, CBUS2 RXLED# in FT230X v1.7 Table 8.1; v1.4 had them the other way round, see the revision note below) and needs no programming for the LEDs.

(TXDEN, checked: FT234XD sec. 7.2 "the transmitter is only enabled when a character is being transmitted from the UART ... TXDEN is activated 1 bit period before the start bit. TXDEN is deactivated at the same time as the stop bit"; Fig. 7.2 wires it to the ZT485's enable. Its idle level on the pin is not stated in words; the "LED on while idle" reading above stays UNVERIFIED.)

## 2. Unpowered-input tolerance (the CP2102N's blocking problem)

| Chip | Datasheet row (Table 5.1) | Referenced to VCCIO? | With bridge unpowered, MCU TX idle at 3.3 V |
|---|---|---|---|
| FT231X (present) | "DC Input Voltage – High Impedance Bi-directional (powered from VCCIO) −0.3 to +5.8 V" (FT_000565 v1.4) | no, absolute | within rating |
| **FT234XD** | **same row, same numbers** (FT_000753 v1.2): "−0.3 to +5.8 V"; page 1 "Tolerant of 5V input"; v1.1 revision note "Added clarification that we are 5V tolerant" | no, absolute | **within rating** |
| FT230X | same row, "−0.3 to +5.8 V" (FT_000566 v1.4); page 1 "Tolerant of 5V input" | no, absolute | within rating |
| CP2102N (for reference) | "VIO + 2.5 V when VIO < 3.3 V" (Rev. 1.5 Table 3.10) | yes | 0.8 V over (CP2102N study) |

- **The FT234XD does not have the CP2102N's problem.** Its I/O rating is word for word the FT231X's, and the three FT-X parts share the Table 5.3 I/O specification (Rpu/Rpd 40 / 75 / 190 kΩ, Ioz ±10 µA "Vin = 5.5V or 0"). The ±10 µA Ioz is stated with the chip powered; none of the three datasheets gives a leakage figure with VCCIO = 0 V (`grep -i -E "unpowered|powered down|power(ed)? off|VCCIO *= *0|no power"` on all three texts: the only hits are the self-powered section's USB host "powered down" / "powered off" sentences, about the USB host, not the I/O pins).
- **What is unverified for all three FT-X parts alike.** Note 1 to Table 3.3: "When used in Input Mode, the input pins are pulled to VCCIO via internal 75kΩ (approx.) resistors." If that pull-up conducts backwards when VCCIO is 0 V, RXD at 3.3 V would push at most 3.3 V / 40 kΩ = 83 µA (arithmetic, Rpu minimum) into the VCCIO node, 3V3_FTDI. That is an inference about the cell's structure, not a datasheet statement: UNVERIFIED. **It is the same question already open for the present FT231X** as hypothesis M8 in `NW-Status/studies/okapi-hardware-audit/sources/2026-11-10-jonas-cold-adjudication.md` line 89 ("U10 selects the dead USB input on battery because 3V3_FTDI is back-fed"; line 91 "The back-fed voltage itself is UNVERIFIED in every list"; line 93 test: a 10-minute multimeter check of 3V3_FTDI on battery). Swapping to the FT234XD neither creates nor removes that risk, as far as the datasheets show; the one bench measurement proposed there answers it for the whole family only if the I/O cell is shared, which FTDI does not state (UNVERIFIED).
- Dead ends: WebSearch "FTDI FT-X FT230X FT231X I/O pins 5V tolerant when VCCIO unpowered back-powering RXD" (2026-11-11): no FTDI statement found. A git.howett.net issue titled "FTDI chip leaks 30mA @ 3.3v into EC RX pin when machine-under-debug is off" (search result; the page returned an Anubis "Access Denied", DEAD END) is the opposite direction (a powered FTDI's TXD driving an unpowered target), not this case. A TI E2E thread (https://e2e.ti.com/support/interface-group/interface/f/interface-forum/1067036 , via search summary only) recommends an Ioff or overvoltage-tolerant buffer for an FT230 next to an unpowered MCU, again the other direction.
- **The reverse direction, for completeness:** with USB plugged in and the logger's 3.3 V rail off (bench case only), the bridge's TXD drives the MCU's RXD through 330 Ω (Margay R7, Okapi R38) and its CBUS pins sit on LED cathodes. That is unchanged by the swap.

## 3. 3V3OUT regulator and what 3V3_FTDI powers

- **Rating, identical for all three FT-X parts:** "3V3 output at 50mA. May be used to power VCCIO" (FT234XD Table 3.1; FT230X Table 3.1; FT231X Table 3.1), output 2.97 / 3.3 / 3.63 V (Table 5.2 of each). Whether the 50 mA includes the chip's own Icc1 (8.3 mA max into VCC) is not stated in any of the three (UNVERIFIED). The FT234XD's own current, Icc1 6.5 / 8 / 8.3 mA, is the FT230X's and slightly under the FT231X's 8 / 8 / 8.4 mA.
- **Loads (from the CP2102N study's trace, re-confirmed on the fresh netlists above):**
  - **Okapi:** `/USB_ISP_Feather/3V3_FTDI` has 4 nodes, U23 pins 10, 11, 20 and C25 0.1 µF. The regulator carries only the bridge's own I/O cells. The LED current is sourced from `3V3_CORE` (D4 anode) and sunk into the CBUS pin, so it does not load 3V3OUT. **Fits, unchanged from the FT231X.**
  - **Margay (v3.0, Project-Margay 8706d25):** `3V3_FTDI` has 6 nodes: U2 pins 10, 11, 20, C9, **Q2 FDN360P drain** and **U10 TLV3691 IN+**. With USB present Q2 joins 3V3_FTDI to the logger's `3V3` rail, so the bridge regulator shares that rail with U6 TPS79733. The CP2102N study's estimate of the rail's load, excluding the bridge: MCU 4 to 6 mA (UNVERIFIED scaling), all six LED cathodes on 12.2 mA, pull-ups up to 1.3 mA, about **19.5 mA** (sum of that study's figures; an estimate). Against 50 mA that leaves about 30 mA, or about 22 mA if the 50 mA must also cover the chip's own 8.3 mA (arithmetic). How the load splits between U6 and the bridge regulator in parallel is not known (UNVERIFIED). **The FT234XD stands exactly where the FT231X stands today**; it is no weaker and no stronger.
  - Under the Margay v3.1.0 power-path decision (`NW-Status/studies/okapi-hardware-audit/margay-power-path-decision.md` line 73: "the FT231X's 3V3OUT leaves 3V3_FTDI, so the core regulator and the FTDI's regulator no longer drive one node"), the bridge regulator again carries only itself, as on Okapi.
- **Losing the second LED lowers the load slightly** if one cathode resistor is left unfitted: the red channel at 4.2 mA or the blue at 0.9 mA (CP2102N study's arithmetic), sourced from the logger's rail.
- **Answer: the internal regulator suffices on Okapi with large margin and on Margay with the same margin as now.**

## 4. Drivers and MTP configuration

**Same USB identity as the FT231X.** FT234XD Table 8.1: VID 0403h, PID 6015h; FT230X and FT231X Table 8.1: the same. Every host driver path for the present boards is unchanged:

- **Linux:** `drivers/usb/serial/ftdi_sio_ids.h` line 27 (torvalds/linux master, last commit to `ftdi_sio.c` fad0fd1, 2026-07-11, GitHub API): `#define FTDI_FTX_PID 0x6015 /* FT-X series (FT201X, FT230X, FT231X, etc) */`; `ftdi_sio.c` line 194 `{ USB_DEVICE(FTDI_VID, FTDI_FTX_PID) }`; lines 1544 to 1546: `bcdDevice` `0x1000` → `chip_type = FTX`. The driver knows the FT234XD by name: line 2075, "FIXME: FT234XD alone has 1 GPIO, but how to recognize this IC?" (it assumes 4 CBUS GPIOs for every FT-X; this matters only to someone using the kernel's CBUS GPIO interface, not to the UART).
- **Windows:** Microsoft Update Catalog search `VID_0403&PID_6015` (curl, 2026-11-11): 25 rows, "FTDI - Ports" and "FTDI - USB", newest **2.12.36.20 dated 10/27/2024** for "Windows 11 Client, version 24H2 and later ... Upgrade & Servicing Drivers" and for Windows 10 Vibranium and later; also 2.14.1.8 (2/16/2023) and earlier. The same packages serve the FT231X today, whatever the delivery mode.
- **macOS:** same VID/PID as the FT231X, so whatever works now (Apple's AppleUSBFTDI or FTDI's VCP driver) works the same; not re-checked here.

**Configuration is required for the FT234XD, not for the FT230X.**

- FT234XD: CBUS0 ships as TXDEN (Table 8.1) and must be set to TX&RXLED# (or TXLED#/RXLED#). FTDI's route is FT_PROG (Windows) or the D2XX API (sec. 8.2.1). MTP endurance 2,000 write cycles (Table 5.7), ample for a once-per-board step.
- **Linux, open source, two independent implementations:**
  - libftdi (`git clone git://developer.intra2net.com/libftdi`, HEAD 92d657b, 2026-01-04): `src/ftdi.c` line 695 `bcdDevice == 0x1000` → `TYPE_230X` (all FT-X parts, FT234XD included); `src/ftdi.h` lines 423 to 427 `CBUSX_TRISTATE = 0, CBUSX_TXLED = 1, CBUSX_RXLED = 2, CBUSX_TXRXLED = 3, ... CBUSX_IOMODE = 8, CBUSX_TXDEN = 9`; the EEPROM build for `TYPE_230X` (lines 3463 to 3471) writes `output[0x1a + j] = eeprom->cbus_function[j]`. The `ftdi_eeprom` tool accepts `cbusx0` to `cbusx3` with names including `TXRXLED` (`ftdi_eeprom/main.c` lines 112 to 116, 259 to 262, 520 to 529). **Limit:** line 3466 "FIXME: Make DBUS & CBUS Control configurable", line 3467 `output[0x0c] = 0; /* DBUS drive 4mA, CBUS drive 4mA like factory default */`, so `ftdi_eeprom` cannot set the 8 mA drive proposed in section 1c and resets it to 4 mA.
  - pyftdi (github.com/eblot/pyftdi master, last commit 25d77b0, 2026-06-02): `pyftdi/ftdi.py` lines 73 and 86 list `'234x'` / `'ft234x'` at PID 0x6015; `pyftdi/eeprom.py` line 63 `0x1000: _PROPS(1024, 0x1A, 0xA0, None),  # FT230X/FT231X/FT234X`; line 78 `CBUSX = IntEnum('CBusX', 'TRISTATE TXLED RXLED TXRXLED PWREN SLEEP DRIVE0 DRIVE1 GPIO TXDEN ...', start=0)` (TXRXLED = 3, GPIO = 8); lines 1067 to 1074 and 1137 handle a configurable `cbus_drive` (4, 8, 12, 16 mA); `commit(dry_run=True)` at line 721.
  - **Cross-check:** both tools put the CBUS function bytes at EEPROM byte 0x1A and agree TXRXLED = 3, GPIO = 8, TXDEN = 9; the Linux kernel reads the FT-X CBUS configuration at `cbus_cfg_addr = 0x1a` (`ftdi_sio.c` line 2060) and treats `FTDI_FTX_CBUS_MUX_GPIO 0x8` (`ftdi_sio.h` line 448) as GPIO. Three independent sources agree on address and encoding. Not tested on a chip: UNVERIFIED that a write lights the LED.
- **On a production line:** plug the assembled board into USB once, run pyftdi (Python, fits NW-Provision's Python CLI) or `ftdi_eeprom` with a small config setting CBUS0 to TXRXLED, and verify by reading back. This is the same class of step the CP2102N would need; the FT230X and FT231X need none for the LEDs.
- The FT234XD also lets the product string read "FT234XD BASIC UART" (Table 8.1) instead of the FT231X's; nothing in the NW tooling keys on the string (CP2102N study, section 7: no VID/PID or string checks in NW-Provision, NW-Build or the board package).

## Later datasheet revisions found, and what they change (supersedes parts of the facts above)

- 2026-11-11 KiCad 10.0.8's own symbols point at newer files: `Interface_USB:FT234XD` Datasheet `https://ftdichip.com/wp-content/uploads/2024/05/DS_FT234XD.pdf`, `Interface_USB:FT230XQ` Datasheet `https://ftdichip.com/wp-content/uploads/2025/06/DS_FT230X.pdf` (`/usr/share/kicad/symbols/Interface_USB.kicad_sym` lines 33637 on and 29648 on). Direct curl of both: HTML, DEAD END. Wayback CDX (`https://web.archive.org/cdx/search/cdx?url=ftdichip.com/wp-content/uploads/20*&filter=original:.*DS_FT234XD.*`) lists `2020/08`, `2021/10`, `2024/05` and `2025/06` copies of DS_FT234XD.pdf, and the same four dates for DS_FT231X.pdf. Fetched:
  - **FT234XD FT_000753 Version 1.6 (26-06-2025), 33 pages**, `https://web.archive.org/web/20250806204759id_/https://ftdichip.com/wp-content/uploads/2025/06/DS_FT234XD.pdf`, saved here as `FT234XD-datasheet-v1.6.pdf`. **Cited from here on.**
  - **FT231X FT_000565 Version 1.6 (26-06-2025), 41 pages**, `https://web.archive.org/web/20250806205422id_/https://ftdichip.com/wp-content/uploads/2025/06/DS_FT231X.pdf`, saved here as `FT231X-datasheet-v1.6.pdf`.
  - **FT230X FT_000566 Version 1.7 (26-06-2025), 40 pages**, `https://web.archive.org/web/2026id_/https://ftdichip.com/wp-content/uploads/2025/06/DS_FT230X.pdf`, saved here as `FT230X-datasheet-v1.7.pdf`.
  - The v1.2 / v1.4 copies saved earlier stay as superseded references.
- **FT234XD revision history (v1.6, App. C):** v1.3 (09-12-2018) "Removed Pin 13 from FT234XD"; "Corrected the order of the chip marking text". v1.4 (23-09-2021) "reset can be connected to VCCIO if not used"; sections 3.2 and 7.5 "additional information on Tx and Rx LEDs"; MTTF added. v1.5 (14-05-2024) "Added statement about X-ray and MTP in section 5.3"; "Changed Vih value in table 5.4"; "Added ESD and Latch-up Specifications". v1.6 (26-06-2025) "Added note on memory checksum and recovery text underneath Table 8.1"; "Updated X-ray note"; **"Swapped TXLED and RXLED to match FT_PROG"**.
- Checked unchanged in FT234XD v1.6: pin numbers and names (Tables 3.1 to 3.3, except that GND is now pin 5 only; the center pad is still "internally connected to ground", sec. 9.1); CBUS0 default TXDEN; Table 3.3 note on 75 kΩ pull-ups to VCCIO; **Table 5.1 high-impedance input −0.3 to +5.8 V "(powered from VCCIO)"**; VCC −0.3 to +5.5 V; DC output current 22 mA; Table 5.3 (was 5.2) VCC 2.97 / 5 / 5.5 V, Icc1 6.5 / 8 / 8.3 mA, Icc2 125 µA, 3V3 2.97 / 3.3 / 3.63 V; "3.3V output at 50mA"; MTP 2,000 write cycles, 10 years (Table 5.8); Table 8.1 VID/PID, 90 mA, CBUS0 TXDEN; sec. 7.5 Figure 7.5 single LED with 270 Ω; 0.45 mm pitch, 3.00 x 3.00 mm.
- New in FT234XD v1.6: Table 5.1 "MTTF/MTBF FT234XD 9,185,671 Hours, 60% Confidence Level, FIT = 108.87"; Table 5.2 ESD HBM > ±2 kV, MM > ±200 V, CDM > ±500 V, latch-up > ±200 mA; Table 5.4 (VCCIO 3.3 V) **VIH 1.2 V** (was 2.0 V in v1.2), VIL 0.8 V.
- **X-ray and MTP (new, matters for production).** FT234XD v1.6 sec. 5.4: "Performing X-ray inspection as part of manufacturing process could potentially corrupt the MTP content. Avoid X-ray directly on the IC as part of the manufacturing process if possible or conduct your own evaluation and risk assessment." Below Table 8.1: "The Internal MTP is protected with a checksum. This checksum can fail if the memory is programmed incorrectly by the user, or if it's exposed to X-Ray during PCB inspection. When a device fails this checksum then it automatically reverts back to FTDI default settings ... the default VID and PID will be set as per Table 8.1 and the Product Description would read FT232EX." The FT231X v1.6 (line 1148 of its text) and FT230X v1.7 (sec. 5.4 and under Table 8.1) carry the same notes. **Consequence:** on the FT231X and FT230X a reverted MTP still gives working LEDs (the defaults are TXLED#/RXLED#); on the FT234XD a reverted MTP puts CBUS0 back to TXDEN. So with the FT234XD, the CBUS0 programming step must come **after** any X-ray inspection at the assembler, and a field unit whose MTP reverts would show a wrong LED (UART and auto-reset unaffected: neither depends on MTP settings that the defaults change, as far as Table 8.1 shows).
- **The LED-label question in the CP2102N study is settled.** That study noted Margay names the CBUS1 net `TX_LED` and CBUS2 `RX_LED`, against FT231X v1.4's "CBUS1 ... default configuration is RXLED#". FT231X v1.6 (QFN table): pin 17 [SSOP] / **pin 14 CBUS1 "default configuration is TXLED#"**, pin 10 [SSOP] / **pin 7 CBUS2 "default configuration is RXLED#"**, Table 8.1 "CBUS1 TXLED#", and its revision history v1.6 "Swapped TXLED and RXLED to match FT_PROG". **Margay's (and Okapi's) labels agree with what the chip does by default; v1.4 of the datasheet was wrong.** FT230X v1.7 Table 8.1 likewise: CBUS1 TXLED#, CBUS2 RXLED#.

## 5. Layout fit

- **Package (FT234XD v1.6 Fig. 9.1, WDFN(X312)):** D = E = 3.00 BSC, e = 0.45 BSC, b 0.18 / 0.25 / 0.28, L 0.30 / 0.40 / 0.50, K ≥ 0.20, A 0.70 / 0.75 / 0.80; exposed pad E2 1.50 / 1.60 / 1.65, D2 2.40 / 2.50 / 2.55 mm (read from the rendered page, `pdftoppm -f 27 -l 27 -r 160`). FTDI gives no land pattern.
- **KiCad's own parts (KiCad 10.0.8).** Symbol `Interface_USB:FT234XD` (`/usr/share/kicad/symbols/Interface_USB.kicad_sym` line 33637): pins 1 USBDM, 2 ~RESET, 3 3V3OUT, 4 VCC, 5 GND, 6 CBUS0, 7 TXD/D0, 8 ~RTS/D2, 9 VCCIO, 10 RXD/D1, 11 ~CTS/D3, 12 USBDP, 13 GND (passive, the pad), matching Table 3.1 to 3.3. Its Footprint field is **`Package_DFN_QFN:WDFN-12-1EP_3x3mm_P0.45mm_EP1.7x2.5mm`**, footprint filter `WDFN*1EP*3x3mm*P0.45mm*`. That footprint's own description is "WDFN, 12 Pin (https://www.diodes.com/assets/Datasheets/PAM2306.pdf)", that is, a Diodes Inc. land pattern, not FTDI's. Geometry (parsed from the `.kicad_mod`): pads 0.80 x 0.20 mm at x = ±1.45 mm, pitch 0.45; exposed pad 1.70 x 2.50 mm, paste 2 x 2 of 0.69 x 1.01 mm; copper extent 3.70 x 2.45 mm; courtyard 4.55 x 3.50 mm. Against FTDI's package: the exposed pad is 0.05 mm over E2 max (1.65) in one axis and at D2 nominal in the other; the 0.20 mm pad is narrower than the 0.25 mm nominal terminal. Workable, but a footprint built from Fig. 9.1 in nw-cold-silicon is the conservative choice, as the CP2102N study concluded for its part (a proposal). The alternative library part `DFN-12-1EP_3x3mm_P0.45mm_EP1.65x2.38mm` (Analog Devices / LTC basis) has 0.25 mm pads but a 2.38 mm pad length, under D2 minimum 2.40.
- FT230XQ: KiCad symbol `Interface_USB:FT230XQ` (line 29648) names `Package_DFN_QFN:QFN-16-1EP_4x4mm_P0.65mm_EP2.1x2.1mm`; copper extent 4.75 x 4.75 mm, courtyard 5.26 x 5.26 mm (parsed). (Pitch from the KiCad footprint; FT230X sec. 9.3 drawing not re-read here.)
- **The present footprint** `nw-cold-silicon:QFN20` has no courtyard (CP2102N study); its bounding box at the Margay site is 4.86 x 4.92 mm (`near.py`, Margay null copy).
- **Trial placement and DRC (scratch only).** Fresh copies of `Project-Margay/Hardware/KiCAD/` (8706d25) and `Project-Okapi/Hardware/KiCAD-10import/` (2734fc4) in `/tmp/claude-1000/-home-awickert-Dropbox-NorthernWidget-github/cf0342fa-36e3-4818-be1e-2b4b31cc1756/scratchpad/ft234xd/`. `tools/swap2.py` (pcbnew 10.0.8 Python) replaced U2 / U23 with the KiCad footprint at the same center and rotation (Margay U2 (149.337, 94.806) mm, 90°; Okapi U23 (125.270, 161.328) mm, 0°), and saved; a null save of the same board is the control. `kicad-cli pcb drc --severity-all --format json`, all exit 0. Violations that differ, control → FT234XD → FT230XQ:

| Board | Total | courtyards_overlap | clearance | shorting_items | solder_mask_bridge | track_dangling |
|---|---|---|---|---|---|---|
| Margay | 99 → 134 → 145 | 0 → 0 → 0 | 7 → 13 → 11 | 0 → 3 → 17 | 0 → 15 → 23 | 1 → 13 → 4 |
| Okapi | 206 → 243 → 261 | 3 → 3 → 8 | 0 → 7 → 9 | 0 → 4 → 14 | 0 → 14 → 24 | 0 → 12 → 3 |

  - Okapi's 3 control courtyard overlaps are pre-existing (R84, R85, C22 against J10); with the FT234XD they are the same three, so **the FT234XD adds no courtyard conflict on either board**. The FT230XQ footprint adds five on Okapi (U23 against R40, C25, R38, C39, R35).
  - Clearance to neighbors with the FT234XD (`near.py` on the swapped copies): Margay, no top-side part within 1.0 mm of the new courtyard (only J1, the SD socket on the bottom side, overlaps in plan); Okapi, nearest C25 0.37 mm, R35 0.40, R36 0.45, R34 0.46, J2 0.64, C39 / R38 / R40 0.75 mm. In the CP2102N trial (QFN-24) several of these touched (gap 0) or sat at 0.07 mm.
  - Every shorting, clearance, mask-bridge and dangling-track item is an existing fan-out track of the QFN-20 crossing or ending near pads of the unnetted trial footprint. **Reading: the FT234XD fits both present sites with room to spare, and the pinout is different, so the bridge's local fan-out must be rerouted on both boards.** Routing was not attempted. The fan-out has fewer nets to carry than now (DTR# gone, one LED net gone, RTS# added) and only one extra 0402 part moves (C1 / C39 keeps its place; only its trace changes from DTR# to RTS#).
- Board-file nets that change: the `DTR` net (Okapi) / `/Digital_Core/DTR` (Margay) moves from FT231X pin 18 to FT234XD pin 8 (rename to RTS is a proposal); one of `TX_LED` / `RX_LED` (Margay) or `Net-(U23-CBUS1)` / `Net-(U23-CBUS2)` (Okapi) moves to pin 6 and the other is removed with its 330 Ω, or both join pin 6 (section 1c).

## 7. Current stock, 2026-11-11 (appended as fetched)

| Distributor | Part | Stock | Restock / lead time | Price at 100 | Source (fetched 2026-11-11) |
|---|---|---|---|---|---|
| Digi-Key | FT234XD-R (768-1178-1-ND CT, -2-ND TR, -6-ND Digi-Reel) | **0**, "Active" | "5,000 expected in stock on 18-Jan-2027"; lead time "50 Weeks" | $2.12000 (CT); TR $1.71250 at 5,000 | https://www.digikey.com/en/products/detail/ftdi-future-technology-devices-international-ltd/FT234XD-R/3904921 (WebFetch) |
| Digi-Key | FT230XQ-R | **0**, "Active" | "5,000 expected in stock on 19-Apr-2027"; lead time "50 Weeks" | $2.12000 (CT) | https://www.digikey.com/en/products/result?keywords=FT230XQ-R (WebFetch) |
| Mouser | FT234XD-R (895-FT234XD-R) | **0** | none shown | $2.62 | OEMsTrade, ECIA "Authorized Distributor" badge, https://www.oemstrade.com/search/ft234xd-r (WebFetch). Mouser page itself: WebFetch timeout, DEAD END |
| Mouser | FT234XD-T (895-FT234XD-T, tray) | **0** | none shown | $2.12 | same OEMsTrade page |
| Newark | FT234XD-R (53X3171 CT, 53X3171RL reel) | **0** | not listed | $3.65 | same OEMsTrade page (badge); Newark search page: WebFetch timeout, DEAD END; FindChips shows two Newark rows at 0 |
| TME | FT234XD-R | **0** ("0 in TME stock") | "Please, be advised of changes to the delivery schedule"; MOQ 5,000 | no 100 break; $1.61 net at 5,000 | https://www.tme.eu/en/details/ft234xd-r/usb-integrated-circuits/ftdi/ (WebFetch) |
| RS | FT234XD-R (70403922) | **0** | "12 Weeks, 0 Days" (as listed by OEMsTrade; no badge shown) | no 100 break; $2.85 at 5,000 | OEMsTrade; FindChips RS row 0 |
| Arrow | FT234XD-R | not found | – | – | https://www.arrow.com/en/products/ft234xd-r/ftdi WebFetch timeout, DEAD END; no Arrow row on OEMsTrade (both offsets read) or FindChips |
| Future, Avnet | FT234XD-R | not found | – | – | no row on OEMsTrade or FindChips (Future and Avnet appear only as filter logos); direct pages not tried after Arrow/Newark/Mouser timeouts and the FT231X agent's Future/Avnet dead ends (its log rows 18, 34) |
| Mouser | FT230XQ-R (895-FT230XQ-R) | **0** | none shown | $2.12 | https://www.oemstrade.com/search/ft230xq-r (WebFetch), badge |
| Mouser | FT230XQ-T (895-FT230XQ-T, tray) | **0** | none shown | $2.12 | same |
| Newark | FT230XQ-R (83T7086, 83T7086RL) | **0** | not listed | $3.69 | same, badge; FindChips two Newark rows at 0 |
| TME | FT230XQ-R | **0** | RFQ only | $2.10 | same, badge; FindChips TME 0 |
| Arrow, Future, Avnet, RS | FT230XQ-R | not found | – | – | no rows on OEMsTrade (both offsets) or FindChips (https://www.findchips.com/search/FT230XQ-R) |

Brokers (not authorized, counterfeit risk; recorded, not recommended), same pages: FT234XD-R, Win Source 20,401 (OEMsTrade; 34,775 on FindChips), Unikey 4,990 at $3.6975 to $4.0057, Time Way 40,943, Chipskey 27,073, Chip Stock 5,000, Sierra IC 155,073 "OEM/CM ONLY", GlobalTek 322,236 "OEM/CM QUOTES ONLY". FT230XQ-R: Win Source 25,617 (15,885 on FindChips), YIC 15,000 at $3.006, IC Components 23,702, Sierra IC 179,534, Chipskey 82,074, Sense 78,542. OEMsTrade also notes a "MOUSER" label inside some broker blocks (MountainView, Unicom, ICMILES), which are listing labels, not Mouser stock.

**Reading: every authorized distributor reached shows 0 for both the FT234XD-R and the FT230XQ-R today, exactly as for the FT231XQ-R** (FT231X agent: Digi-Key 0, Mouser 0, TME 0; its Newark figure conflicts, 108 or 4,533). Digi-Key's restock dates: FT234XD-R 18 Jan 2027 (the same date and quantity as the FT231XQ-R), FT230XQ-R 19 Apr 2027. Changing to either part does not get boards built sooner from authorized stock.

## 6. Historical stocking (appended as found; table assembled at the end of this section)

### Notices and secondary reports

- **No FTDI end-of-life notice for the FT234XD, FT230X or FT231X chips was found.** WebSearch "FTDI PCN end of life FT234XD OR FT230X OR FT231X discontinued notice" (2026-11-11). What exists:
  - FTDI EOL notice dated **30 May 2024**, Wayback copy of `https://ftdichip.com/wp-content/uploads/2024/06/EOL-Notice-TTL-234X-3V3-AJ-UMFT234XD-NC-UMFT234XD-WE-and-UMFT230XB-WE.pdf` (curl `web/2025id_/`): "manufacture discontinuation and End of Life" of the **modules** TTL-234X-3V3-AJ, UMFT234XD-NC, UMFT234XD-WE, UMFT230XB-WE, each with a named replacement module (TTL-234X-3V3, UMFT234XD-01, UMFT230XB-01). "Reasons for Obsolescence: This is part of our product life cycle management program." The chips are not listed; the replacement modules still use them.
  - FTDI **PCN_FT_052**, issued 2020-12-1, Wayback copy of `https://ftdichip.com/wp-content/uploads/2024/01/PCN_FT_052.pdf`: FT200XD, FT201X, FT220XS, FT221XQ, FT230X, FT231X, FT240X, FT234XD; "1. Lead Frame 2. Packing Material"; reason "Tooling Change"; "No functional or characteristic changes"; new date codes "FT231XQ ... from 2109-D", "FT230XQ from 2051-D", "FT231XS, FT234XD from 2106-D". A tooling change, not a discontinuation.
  - Search summary only (not fetched, UNVERIFIED): RS UK lists FT234XD-R (888-8744) and FT230XQ-T (888-8716) as "Unavailable", RS "will no longer stock"; Digi-Key lists the LC234X module as obsolete.
- **Findchips Market Brief "Off the Bridge"**, https://blog.findchips.com/ftdi-usb-uart-bridge-alternates-2026/ (WebFetch 2026-11-11), published June 2, 2026, part data "captured live from Findchips on May 31, 2026": "Across the popular FTDI parts the authorized channel has gone to zero"; "Inventory across the category is down almost 33% year-over-year and another 14% on the quarter"; "Pricing is moving the other way, up almost 8% on the quarter"; on the FT234XD-R, "Mouser, RS and TME all read zero on the authorized side, RS quoting a 12-week lead"; "Newark is holding real authorized depth, around 13,541 units near $3.37"; "The constraint is not going to ease before the fourth quarter"; "If the program ships in 2027 or later, respin now, because there is no DFN 12 fallback and the inventory trend points down." **Reliability caveat:** the same brief says the FT234XD has "a VCC input on pin one" and "a 3V3OUT regulator output on pin five", both wrong against FT_000753 v1.6 Table 3.1 (VCC pin 4, 3V3OUT pin 3, pin 1 USBDM). Its stock figures are used below as a dated observation only.
- WebSearch "FTDI lead time 2022 FT231X shortage weeks allocation" and "FTDI 2026 shortage lead time FT230X FT232R out of stock" (2026-11-11): no FTDI lead-time or allocation notice for 2021 to 2023 found; search summaries cite Digi-Key regional pages showing 32 and 42 weeks and Mouser 42 weeks for FT231X parts (undated captures, UNVERIFIED).

### Digi-Key US, Wayback Machine snapshots

Method: Wayback CDX (`https://web.archive.org/cdx/search/cdx?url=digikey.com/...<part>*&filter=statuscode:200&collapse=timestamp:6`, URL forms `en/products/detail/ftdi-.../<part>/<id>`, `product-detail/en/ftdi-.../<part>/<dk#>/<id>` and `product-detail/en/<part>/...`), first capture per month fetched raw (`web/<ts>id_/<url>`) by `tools/dkhist.py`, saved under `scratchpad/ft234xd/hist/snaps/`, and read by `tools/summ.py` (stock from `"qtyAvailable"`, `"In-Stock: N"`, `"N In Stock"`, `Digi-Key Stock: N` or `N Can ship immediately`; lead time from `"standardLeadTime"` or "Manufacturer Standard Lead Time N Weeks"). Every page's title or `manufacturerProductNumber` was checked to be the named part (Digi-Key numbers 768-1178 FT234XD-R, 768-1130 FT230XQ-R, 768-1128 FT231XQ-R). Four captures were Digi-Key "Invalid Request" pages and one was empty (2015-09, 2015-10, 2015-11, 2016-03, 2025-08): no data. The archive has no **digikey.com** capture of any of the three parts between mid-2019 and early 2023. (Superseded in part: Digi-Key's regional sites fill that gap, next subsection.)

| Capture (UTC) | FT234XD-R stock | lead | FT230XQ-R stock | lead | FT231XQ-R stock | lead |
|---|---|---|---|---|---|---|
| 2014-10-09 / 2014-11-06 | 8,739 | – | 15,000 | – | – | – |
| 2015-01-25 / 2015-01-20 | 15,083 | – | 5,000 | – | – | – |
| 2015-03-29 / 2015-03-05 | 23,303 | – | 22,801 | – | – | – |
| 2016-01-15 | 21,504 | – | – | – | – | – |
| 2016-03-20 / 2016-04-11 / 2016-04-24 | 33,547 | – | 25,000 | – | 13,602 | – |
| 2016-04-29 | 17,007 | – | – | – | – | – |
| 2016-05-31 | 37,751 | 12 wk | – | – | – | – |
| 2016-06-19 | 33,621 | 12 wk | 27,786 | 12 wk | 34,924 | 12 wk |
| 2016-07-02 / 07-03 | 31,345 | 12 wk | 23,520 | 12 wk | – | – |
| 2016-08-13 / 08-05 | 24,535 | 12 wk | 5,341 | 12 wk | – | – |
| 2016-09-17 / 09-22 | 20,528 | 12 wk | – | – | 12,535 | 12 wk |
| 2016-10-16 | – | – | 52,850 | 12 wk | – | – |
| 2017-02-11 | – | – | – | – | 31,754 | 12 wk |
| 2019-02-01 / 02-24 | 57,060 | 10 wk | 130,000 | 11 wk | 23,836 | 10 wk |
| 2019-05-12 | 49,088 | 10 wk | – | – | – | – |
| 2023-02-08 / 04-01 | 55,914 | 16 wk | – | – | 44,586 | 14 wk |
| 2024-01-11 / 02-24 / 04-14 | 76,897 | 12 wk | 41,416 | 12 wk | 79,385 | 12 wk |
| 2025-01-16 / 02-13 / 04-22 | 43,921 | 14 wk | 33,902 | 12 wk | 46,884 | 12 wk |
| 2025-11-13 / 11-15 | – | – | **0** | 32 wk | 7,453 | 32 wk |
| 2025-12-06 / 12-14 | – | – | **0** | 32 wk | **0** | 32 wk |
| 2026-04-15 | **0** | 42 wk | – | – | – | – |
| 2026-11-11 (live, section 7 and FT231X agent) | **0**, 5,000 due 18-Jan-2027 | 50 wk | **0**, 5,000 due 19-Apr-2027 | 50 wk | **0**, 5,000 due 18-Jan-2027 | 50 wk |

(Rows join captures from different days where the months coincide; the exact capture of each number is in `hist/dk_<part>.tsv`.)

## 8. Changes per board (FT234XD), and the FT230XQ for comparison

Both boards, FT234XD:

1. U2 / U23: symbol `Interface_USB:FT234XD` (or an nw-cold-silicon copy), footprint per section 5 (KiCad `WDFN-12-1EP_3x3mm_P0.45mm_EP1.7x2.5mm`, or a Fig. 9.1 footprint in nw-cold-silicon: a proposal).
2. The 100 nF auto-reset capacitor (Margay C1, Okapi C39) moves from DTR# (pin 18) to **RTS# (pin 8)**. No part added or removed.
3. LEDs: CBUS0 (pin 6) drives one cathode resistor; the other cathode resistor is removed (Margay R8 or R5; Okapi R39 or R36) or tied to the same pin (section 1c). Which LED color stays is Andy's call.
4. Unchanged: TXD, RXD and their 330 Ω; CTS# to GND; 27 Ω series and 12 pF on D+/D−; VCC, 3V3OUT, VCCIO, RESET# on the same nets and capacitors; nothing added. No VBUS divider, no reset pull-up and no Ioff buffer (the CP2102N's additions) are needed.
5. Production: write CBUS0 = TXRXLED (and, if chosen, 8 mA CBUS drive) over USB after assembly and **after any X-ray inspection** (section 4, v1.6 X-ray note), with pyftdi or `ftdi_eeprom`, then read it back. FT_PROG on Windows does the same.
6. Documentation: the FT231X mentions found by the CP2102N study (`Project-Margay/README.md` line 233 "The FT231X USB chip sets the ceiling there: its absolute maximum is 5.5 V" and line 251 "FTDI USB-Serial converter"; `Project-Okapi/README.md` line 167 "FTDI USB-Serial converter"; grep 2026-11-11) name the chip and its 5.5 V absolute maximum, which the FT234XD shares (Table 5.1, VCC −0.3 to +5.5 V). Driver notes are unchanged (same VID/PID).

Bill of materials delta at 100 (Digi-Key CT, 2026-11-11): FT231XQ-R $2.20000 (FT231X agent) → FT234XD-R $2.12000 (section 7): **−$0.08 per board**, less one 0402 330 Ω if one LED channel is dropped. FT230XQ-R: $2.12000, also −$0.08, with no LED or programming change.

FT230XQ for comparison: same DTR# loss and RTS# move as the FT234XD, but both LED pins keep their FT231X defaults (CBUS1 TXLED#, CBUS2 RXLED#), so **no MTP programming and no LED change**. Its KiCad QFN-16 4 x 4 mm footprint has a 5.26 mm courtyard and collided with five Okapi neighbors in the trial (section 5), so it needs more placement work than the FT234XD on Okapi and none on Margay.

### Digi-Key regional sites (digikey.ca, .co.uk, .de, .fr, .com.au), Wayback snapshots

Same method (`tools/cdx_more.sh`, then `tools/dkhist.py` and `tools/summ.py`); stock read from the page's `<span id="dkQty">` (the CT/TR line, which shares the reel inventory) or the JSON fields above, and, on 2016-2021 pages, the per-package "Quantity Available" lines for the alternate packages. These sites show Digi-Key's single inventory with local prices (that the regional sites draw on the same stock is from memory, UNVERIFIED; the numbers track the .com captures closely, e.g. 2025-04-21 .co.uk 44,134 against 2025-04-22 .com 43,921). CDX found none on digikey.ch, .nl, .se, .dk (empty after retries).

**FT234XD-R:**

| Capture (UTC) | Site | Stock (CT/TR line) | Other packages | Lead time |
|---|---|---|---|---|
| 2016-09-27 | .ca | 18,820 | TR 15,000 | 12 wk |
| 2019-09-19 | .fr | 32,665 | – | 11 wk |
| 2019-11-13 | .co.uk | 11,196 | TR 10,000; tray 561 | 11 wk |
| **2020-11-27** | .de | **0** | **tray (768-1345-ND) 3,762**; TR 0 | 11 wk |
| **2021-01-21** | .com.au | **0** | TR 0; tray 0 | 16 wk |
| 2021-04-11 | .com.au | 21,869 | TR 21,869; tray 2,383 | 16 wk |
| **2021-05-14** | .de | **0** | **tray 5,276**; TR 0 | 16 wk |
| **2021-07-30** | .com.au | **0** | TR 0; tray 0 | **33 wk** |
| 2024-05-30 | .co.uk | 50,509 | – | 12 wk |
| 2024-06-25 | .com.au | 40,047 | – | 12 wk |
| 2024-08-15 | .com.au | 16,245 | – | 12 wk |
| 2024-11-04 | .ca | 11,801 | – | 12 wk |
| 2025-01-23 | .co.uk | 54,442 | – | 12 wk |
| 2025-02-12 | .de | 44,696 | – | 12 wk |
| 2025-03-20 | .fr | 22,473 | – | 12 wk |
| 2025-04-21 | .co.uk | 44,134 | – | 14 wk |
| 2025-05-15 | .com.au | 8,589 | – | 14 wk |
| **2025-10-13** | .ca | **0** | – | 27 wk |
| 2025-12-06 | .com.au | **0** | – | 32 wk |
| 2026-02-10 | .de | **0** | – | 34 wk |
| 2026-03-09 | .fr | **0** | – | 34 wk |
| 2026-06-11 | .co.uk | **0** | – | 42 wk |

Reading for the FT234XD-R: in stock at Digi-Key in every capture from 2014 to 2019; **out of stock on the reel line in four of five captures from November 2020 to July 2021** (the tray FT234XD-T covered two of those four), with the lead time rising from 11 to 33 weeks; back in stock from at least February 2023 to May 2025 (8,589 to 76,897); **0 in every capture from October 2025 to today**, with the lead time rising 27 → 32 → 34 → 42 → 50 weeks.

### History sources tried, dead ends included

- Wayback CDX for `mouser.com/ProductDetail/FTDI/<part>*` (and `FTDI-Chip/`, `895-` forms): first pass empty after retries; a later single query for FT231XQ-R returned 12 captures, all 2012 to 2017 and several 302/405, nothing for 2020-2026; for FT234XD-R the query returned the archive's "Temporarily Offline" page. **No Mouser history used.**
- Wayback CDX for `octopart.com/<part>-ftdi*` and `findchips.com/search/<part>*`: empty. Octopart direct is 403 (FT231X agent, log row 4). **No Octopart or FindChips price/stock history used.**
- Wayback CDX became unavailable during the run ("Internet Archive: Temporarily Offline" HTML returned to the CDX API, 2026-11-11). The regional Digi-Key captures for the FT230XQ-R and FT231XQ-R were therefore located by Wayback's nearest-capture redirect (`curl -I https://web.archive.org/web/<date>/<url>`, reading the `location:` header) for target dates 2020-09, 2021-03, 2021-09, 2022-03 and 2022-09 on digikey.com, .ca, .co.uk, .de, .fr and .com.au (`tools/probe.sh`).

**FT230XQ-R and FT231XQ-R, regional and extra captures** (nearest-capture probe; fetched raw, part number checked on each page):

| Capture (UTC) | Site | Part | Stock (CT/TR line) | Other packages | Lead time |
|---|---|---|---|---|---|
| 2019-02-01 | .com | FT230XQ-R | 131,106 | TR 130,000; tray 764 | 10 wk |
| 2019-12-10 | .ca | FT230XQ-R | 13,815 | TR 10,000; tray 2,133 | 11 wk |
| 2020-09-22 | .ca | FT230XQ-R | 22,127 | – | 11 wk |
| 2021-01-17 | .co.uk | FT230XQ-R | 11,616 | TR 11,616; tray 4,930 | 16 wk |
| **2021-08-03** | .co.uk | FT230XQ-R | **0** | TR 0; tray 0 | **33 wk** |
| 2024-06-12 | .fr | FT230XQ-R | **0** ("0 In Stock") | – | 12 wk |
| 2024-08-05 | .com.au | FT230XQ-R | 15,501 | – | 12 wk |
| 2024-12-04 | .ca | FT230XQ-R | 35,679 | – | 12 wk |
| 2025-01-17 | .de | FT230XQ-R | 45,929 | – | 12 wk |
| 2019-02-24 | .com | FT231XQ-R | 23,836 | TR 20,000; tray 7,450 | 10 wk |
| 2024-12-10 | .co.uk | FT231XQ-R | 54,533 | – | 12 wk |
| **2025-10-06** | .com.au | FT231XQ-R | **0** | – | 27 wk |

The four March 2022 FT231XQ-R captures the probe found (digikey.com, 2022-03-09 and 2022-03-10) are 4,825-byte Wayback redirect stubs to digikey.pt and digikey.ph: no data, DEAD END. No capture of the FT231XQ-R between 2019-02 and 2023-04 holds a stock figure. The 2024-06-12 .fr zero for the FT230XQ-R sits between non-zero readings (41,416 in January, 15,501 in August); taken as a dated observation, not a trend.

### What the history shows

| Period | FT234XD-R | FT230XQ-R | FT231XQ-R |
|---|---|---|---|
| 2014-2019 | in stock in all 16 readings (8,739 to 57,060); lead 10-12 wk | in stock in all 11 readings (5,000 to 131,106); lead 10-12 wk | in stock in all 6 readings (12,535 to 34,924); lead 10-12 wk |
| 2020-11 to 2021-08 (shortage) | **0 in 4 of 5 readings** (2020-11, 2021-01, 2021-05, 2021-07; tray stock in 2 of them); 21,869 in 2021-04; lead 11 → 16 → 33 wk | in stock 2020-09 and 2021-01 (22,127; 11,616); **0 in 2021-08**; lead 11 → 16 → 33 wk | **no reading** |
| 2021-09 to 2023-01 | no reading | no reading | no reading |
| 2023-02 to 2025-05 | in stock in all 12 readings (8,589 to 76,897); lead 12-16 wk | in stock in 5 of 6 (one regional 0, 2024-06); lead 12 wk | in stock in all 4 readings (44,586 to 79,385); lead 12-14 wk |
| 2025-10 to 2026-11 (now) | **0 in all 7 readings** from 2025-10-13; lead 27 → 50 wk; 5,000 due 18-Jan-2027 | **0 from 2025-11-13**; lead 32 → 50 wk; 5,000 due 19-Apr-2027 | 0 on 2025-10-06 (.com.au), **7,453 on 2025-11-15**, **0 from 2025-12-14**; lead 27 → 50 wk; 5,000 due 18-Jan-2027 |

Counts are of the captures in the tables above (arithmetic on the tables; each "reading" is one Wayback capture). Findchips' 31 May 2026 observation of the FT234XD-R adds "Mouser, RS and TME all read zero on the authorized side" with "Newark ... around 13,541 units near $3.37"; that Newark depth is gone today (OEMsTrade, Newark 0, section 7).

**Which part has been easier to buy.** From these captures, at Digi-Key: **none of the three has been reliably easier than the others.** All three sat at 10-12 weeks and tens of thousands of units in 2014-2019 and 2023-2025, and all three ran out in both shortages. Where the record is dense enough to compare: the FT234XD-R went out earlier in the 2020-2021 shortage (0 from November 2020, while the FT230XQ-R still had 22,127 in September 2020 and 11,616 in January 2021) and earlier in the present one (0 by 2025-10-13, while Digi-Key still had 7,453 FT231XQ-R on 2025-11-15). The FT234XD-R also came back sooner in 2021 (21,869 in April) than any reading shows for the others. The FT231XQ-R has no reading at all for 2019-03 to 2023-03, so its behavior in the 2021-2022 shortage is unknown from this source (UNVERIFIED). **The FT234XD-R has not been easier to buy than the FT231XQ-R; on the evidence, it has been slightly less available at the edges of both shortages, with the same restock date today.**

**Precedent for the current FTDI-wide shortage: yes.** The 2021 readings show the same pattern on the FT234XD-R and FT230XQ-R: the reel line at 0, lead time rising from 11 to 33 weeks, recovery to 12-16 weeks by early 2023 (first reading after the gap: 2023-02-08, FT234XD-R 55,914 at 16 weeks). How long the 2021-2022 outage lasted is not resolved (no readings 2021-09 to 2023-01). The present outage has run from about October 2025 (first 0) to today, 13 months, with Digi-Key quoting 50 weeks and first restock in January 2027 (FT234XD-R, FT231XQ-R) and April 2027 (FT230XQ-R).

## Verdict

**The FT234XD-R is a viable replacement for the FT231XQ-R on both boards, and a near drop-in, but it does not solve the supply problem.** Every signal the boards use maps across: TXD and RXD with their 330 Ω, the same 3V3OUT (50 mA) / VCCIO / RESET# node with the same capacitors, the same 27 Ω / 12 pF USB parts, CTS# to GND, the same VID/PID 0403:6015 and the same drivers on Linux, Windows and macOS. Its I/O pins carry the FT231X's own absolute rating, "−0.3 to +5.8 V" (FT_000753 v1.6 Table 5.1), so the CP2102N's unpowered-input problem does not arise. The package fits both present sites with no new courtyard conflict (Margay: nothing within 1.0 mm; Okapi: nearest 0.37 mm).

**Blocking problems: none.** Two required changes, neither blocking:

1. **No DTR#.** The 100 nF auto-reset capacitor moves to RTS# (pin 8). avrdude 6.3 and 8.0 (the version `arduino:avr` 1.8.7 installs) pulse RTS with DTR in the same call, and the Arduino serial monitor asserts both on open, so uploads and monitor resets behave as now. Not bench-tested (UNVERIFIED with hardware).
2. **One CBUS pin, shipped as TXDEN.** Two LEDs become one (TX&RXLED# on CBUS0, FTDI's Fig. 7.5), and each board's MTP must be written once over USB (pyftdi or `ftdi_eeprom` on Linux, FT_PROG on Windows), after any X-ray inspection, because FTDI now warns that X-ray can corrupt the MTP and a corrupted MTP reverts CBUS0 to TXDEN.

**Changes per board.** Margay U2 and Okapi U23: new symbol and footprint; C1 / C39 from DTR# to RTS#; one LED cathode resistor to CBUS0 and the other removed (Margay R8 or R5, Okapi R39 or R36) or joined to it; local fan-out rerouted; one production step to program CBUS0. Nothing added. Price at 100: $2.12 against $2.20 (Digi-Key CT).

**The FT230XQ-R** is the same swap without the LED compromise or the programming step (it keeps CBUS1 TXLED# and CBUS2 RXLED#), but it also loses DTR#, and its 4 x 4 mm QFN-16 footprint collides with five neighbors on Okapi.

**Stocking history against the FT231X.** The FT234XD-R has not been easier to buy. At Digi-Key all three parts held tens of thousands at 10-12 weeks in 2014-2019 and 2023-2025, and all three ran out in both shortages. The FT234XD-R went to 0 first in each: November 2020 (4 of 5 readings at 0 to July 2021, lead 33 weeks) and October 2025, while Digi-Key still had 7,453 FT231XQ-R in mid-November 2025. **Today every authorized distributor reached shows 0 for all three**, and Digi-Key expects 5,000 FT234XD-R on 18 January 2027, the same date and quantity as the FT231XQ-R (FT230XQ-R: 19 April 2027). The present FTDI-wide shortage has a precedent in 2021, which ended with all three back at 12-16 weeks by early 2023. Switching parts buys a smaller footprint, not earlier boards.

Note on the state checked: netlists and board copies at Project-Margay 8706d25 and Project-Okapi 2734fc4. Nothing in any repository was edited except this report and the four datasheet PDFs beside it (gitignored). Scratch work: `/tmp/claude-1000/-home-awickert-Dropbox-NorthernWidget-github/cf0342fa-36e3-4818-be1e-2b4b31cc1756/scratchpad/ft234xd/`.

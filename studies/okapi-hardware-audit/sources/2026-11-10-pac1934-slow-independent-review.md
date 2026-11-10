COMPLETE

# PAC1934 SLOW/ALERT review

## Sources checked
- PAC1934 datasheet text (DS20005850E), scratchpad/icreq/txt/pac1934.txt: sections 1 (DC table), 3.8, 3.9, 4.1.1, 4.1.5-4.1.7, 4.4.1, Register 6-2.
- Netlist exported with kicad-cli from Project-Okapi/Hardware/KiCAD-10import/Okapi.kicad_sch to slowcheck/net.xml.

## Findings
1. SLOW/ALERT behavior (pac1934.txt 3.9): "In default mode, if this pin is forced high, sampling rate is forced to eight samples/second. When it is forced low, the sampling rate is 1024 samples/second unless a different sample rate has been programmed." IDD 585 typ / 675 max uA at 1024 SPS; IDD SLOW 16 uA typ (4 ch, 8 SPS); sleep 5 uA; power-down 0.1 uA. VIH = 0.7 VDD_IO, VIL = 0.3 VDD_IO, ILEAK +/-1 uA. No internal pull stated for SLOW.
2. Netlist: U32 pin 1 SLOW/ALERT on net CSA_~{ALERT} with only U41 (MCP23018) pin 4 GPB4. No resistor. U32 pin 16 PWRDN tied directly to 3V3_CORE (same rail as VDD pin 2, VDD_IO pin 15, MCU VCC). ADDR_SEL to GND via R51 0 ohm.
- MCP23018 datasheet text (DS22103A) scratchpad/icreq/txt/mcp23018.txt: pin table, 1.5, 1.6.7, register summary, DC table.
2b. MCP23018 GPB4: "5.5 volt tolerant inputs; open-drain outputs"; "The outputs are open-drain." POR IODIRB = 1111 1111 (input), GPPUB = 0000 0000 (pull-up off). So at POR the CSA_~{ALERT} net has no driver and no pull: SLOW floats. Internal pull-up exists: IPU 220 uA typ at VDD=5V, pins at VSS (D070, characterized only). GPIO VIH 0.8 VDD, VIL 0.2 VDD, IIL +/-1 uA. The expander can only pull SLOW low or release it; it can never drive it high without a pull-up.
- Firmware: Okapi_Library/src/Okapi.cpp, Okapi.h; MCP23018 library MCP23018/src/MCP23018.cpp (begin, pinMode, digitalWrite).
- PAC1934 Register 6-14 (SLOW, 0x20) POR: R_RISE=1, R_FALL=1, so every SLOW edge runs a limited REFRESH that resets the accumulators. Section 4.1.7: with SING set and SLOW asserted, "the first sampling will begin within 125 ms after the SLOW pin is asserted."
3. Firmware: _io(0x20) constructed, _io.begin() never called, no _io.pinMode anywhere; only _io.digitalWrite(FeatherEN=7, HIGH, Port::B), which writes OLATB (bit 4 = 0) but leaves IODIRB = input. GPB4 is never configured: it stays a floating input at all times. PAC: pacFind() runs inside readOnBoard() on the first row: writes CTRL=0x10 (SING) then REFRESH_V; pacRefresh() sends REFRESH_V, 10 ms, REFRESH_V, 2 ms. sleepNow() does nothing to PAC or expander. Until first row the chip runs at POR default (1024 SPS, 585 uA typ, or 8 SPS if SLOW floats high).
4. Recommendation: external pull-up SLOW to 3V3_CORE (VDD_IO). Upper bound from VIH 0.7*3.3 = 2.31 V and 2 uA total leakage (PAC ILEAK 1 uA + MCP IIL/ILO 1 uA): R < 0.99 V / 2 uA = 495 kOhm. Reading it on the MCP23018 (VIH 0.8 VDD = 2.64 V): R < 330 kOhm. Proposal: 100 kOhm (0.2 V worst drop; 33 uA only while GPB4 or ALERT holds it low). Caveat: pull-up puts single-shot in SLOW mode (125 ms start); firmware must drive GPB4 low (OPEN_DRAIN mode, not library OUTPUT, which also enables the internal ~220 uA pull-up) around a reading, or wait >125 ms.
5. Other: floating CMOS input at all times (undefined rate, spurious limited REFRESH resetting accumulators); PWRDN hard-tied so no hardware off; firmware comment on CSA net naming ALERT though chip never set to ALERT.
- Extra: OVF ALERT "is cleared by REFRESH or REFRESH_G"; "REFRESH_V will not" (4.4.4). The firmware uses only REFRESH_V, so a latched overflow ALERT would hold the pull-up low (33 uA at 100k) indefinitely if OVF ALERT were ever enabled.
- Alternatives considered: pull-down (defined, zero cost, but POR stays 585 uA); firmware-only (configure PAC and hold GPB4 low in begin(); leaves the pre-begin window and any other sketch floating); PWRDN to a GPIO with pull-down (0.1 uA off, but loses config, 20 ms start, and the open-drain expander would need its pull-up to turn it on).

# Okapi on US Letter: page groupings

STATUS: COMPLETE (2026-11-03)

Started 2026-11-03. Analysis only: nothing in Project-Okapi is edited. Every
number below is pasted from a command logged in "Computation log" or is
marked as an estimate with its basis.

## Computation log

All paths below are under `/home/awickert/Dropbox/NorthernWidget/github/`; `$SP` is the
session scratchpad `/tmp/claude-1000/-home-awickert-Dropbox-NorthernWidget-github/cf0342fa-36e3-4818-be1e-2b4b31cc1756/scratchpad/pages/`
(lost on reboot; every command here rebuilds it in under a minute). Tools are in
`NW-Status/studies/okapi-hardware-audit/tools/`.

1. Netlist: `kicad-cli sch export netlist --format kicadxml -o $SP/okapi.xml Project-Okapi/Hardware/KiCAD-10import/Okapi.kicad_sch`
   (279 nets, 377 placed symbols of which 252 are in the netlist; power symbols are not).
2. Regions and cut checks: `python3 tools/pages_regions.py Project-Okapi/Hardware/KiCAD-10import $SP/regions.json --dump > $SP/regions_dump.txt`
   prints `symbols 377 cut wires 0 straddling symbols 0`, the two split local labels and three
   straddling texts. Single lines were tested with `pages_regions.py <dir> --cut <sheet> x|y <c> <lo> <hi>`.
3. Render: `kicad-cli sch export pdf -e -n --black-and-white -o $SP/okapi.pdf <root>` then
   `pdftoppm -r 100 -png $SP/okapi.pdf $SP/pg` (pages 2–7 are Okapi_1–Okapi_6; 1 px = 0.254 mm).
4. Ink per block: `python3 tools/pages_ink.py $SP/regions.json $SP $SP/ink.json > $SP/ink.txt`
   (and `--rewrap` to `ink_rewrap.json`). Its whole-sheet rows reproduce the measurements
   quoted in the brief: Okapi_1 432.1 x 193.3, Okapi_2 359.9 x 199.1, Okapi_3 326.1 x 313.2,
   Okapi_4 231.4 x 158.2, Okapi_5 263.9 x 165.4, Okapi_6 269.7 x 114.3 mm.
5. Net graph: `python3 tools/pages_graph.py $SP/okapi.xml $SP/regions.json $SP/nets.json > $SP/graph.txt`.
6. Candidates: `python3 tools/pages_eval.py $SP/regions.json $SP/ink_rewrap.json $SP/nets.json > $SP/eval_rewrap.md`
   and the same with `ink.json` to `eval.md` (notes as drawn). The tables below are those two files.

## The blocks

Nineteen rigid blocks (regions of the six sheets), every boundary checked three ways: no wire
has its ends in two blocks, no symbol has a pin outside its anchor's block, and free text is
checked by its estimated and then its measured extent. Three boundaries given as verified in the
brief were not: x=170 on Okapi_1 passes through R74 (pins at 162.56 and 172.72, the solar input
chain D1–R74 that feeds the charger), y=176 on Okapi_3 passes through R18 (pins 170.18–180.34,
the ~LED_EN pull-up of the ladder), and x=190 on Okapi_2 passes through U40 (pins at 182.88, its
C0/C1 labels at 177.8). The blocks below carry the corrected lines. Ink is the measured bounding
box of printed pixels inside the block, plus the measured extent of any note that crosses the
line (three notes do: "Remove LBI pullup??" prints to x=206.4 on Okapi_1, "Jump SDA channels
together, prevents using occupied addresses on the external I2C port" prints from 157.5 to 262.3
on Okapi_3, and "Select address", anchored at 205.7 in the SoM block, prints to 241.9 and names
the ladder's address resistors, so it is counted with the ladder).

| Block | Sheet, rectangle (mm) | Contents | Ink w x h (mm) | Signal nets leaving / internal |
|---|---|---|---|---|
| S1L_T | Okapi_1 x ..170 y ..95 | L1 LOGO1 U1 U39 + 3 R, 2 C | 150 x 75 | 1 / 2 |
| S1L_B | Okapi_1 x ..170 y 95.. | L2 L3 Q7 U2 U3 U13 + 7 R, 7 C | 179 x 106 | 4 / 6 |
| S1M_T | Okapi_1 x 170..295 y ..100 | Q1 Q2 S5 U5 + 7 R, 2 C | 105 x 58 | 2 / 7 |
| S1M_B | Okapi_1 x 170..295 y 100..; Okapi_1 x 148..170 y 116..128 | D1 D2 D3 L4 Q8 U4 + 8 R, 3 C | 141 x 96 | 3 / 8 |
| S1R_T | Okapi_1 x 295.. y ..135 | D8 D9 Q5 Q6 U6 U7 U9 U37 + 2 R, 5 C | 151 x 111 | 3 / 5 |
| S1R_B | Okapi_1 x 295.. y 135.. | JP8 Q3 U8 U10 + 3 R, 0 C | 105 x 74 | 2 / 5 |
| S2L_T | Okapi_2 x ..190 y ..160 | JP1 JP2 JP3 JP4 S1 S2 U11 U12 U14 U15 U17 U18 U19 U20 + 12 R, 2 C | 162 x 117 | 4 / 16 |
| S2L_B | Okapi_2 x ..172 y 160.. | U16 U21 U22 + 0 R, 0 C | 90 x 50 | 3 / 6 |
| S2R_T | Okapi_2 x 190.. y ..150 | D4 F1 J10 U23 + 10 R, 5 C | 172 x 101 | 4 / 23 |
| S2R_B | Okapi_2 x 172.. y 150.. | U40 U$1 U$2 + 0 R, 0 C | 120 x 42 | 3 / 0 |
| S3UL | Okapi_3 x ..222 y ..176 | D7 F2 J9 S6 S7 U35 USB2 + 5 R, 1 C | 204 x 159 | 14 / 44 |
| S3LAD | Okapi_3 x 222.. y ..190 | D10 D11 D12 D13 D14 D16 D17 D18 U45 + 9 R, 0 C | 138 x 83 | 3 / 16 |
| S3SD | Okapi_3 x ..105 y 176..240 | SD1 + 1 R, 0 C | 61 x 48 | 5 / 2 |
| S3TERM | Okapi_3 x ..105 y 240.. | J1 J2 J3 J4 + 0 R, 0 C | 67 x 76 | 22 / 0 |
| S3MID | Okapi_3 x 105..205 y 176.. | H1 H2 H3 ISP1 JP5 MS1 Q4 + 1 R, 0 C | 138 x 154 | 17 / 12 |
| S3LR_T | Okapi_3 x 205.. y 176..245 | J5 J6 J7 J8 + 1 R, 0 C | 72 x 68 | 1 / 2 |
| S3LR_B | Okapi_3 x 205.. y 245.. | D5 S3 + 4 R, 0 C | 83 x 66 | 4 / 3 |
| S4 | Okapi_4 x .. y .. | U24 U25 U26 U27 U28 U29 U34 U36 U42 + 2 R, 6 C | 231 x 158 | 41 / 0 |
| S5 | Okapi_5 x .. y .. | BT1 D6 JP6 JP7 RTC1 U30 U31 U32 U33 U38 U43 U44 + 4 R, 13 C | 264 x 165 | 17 / 11 |
| S6 | Okapi_6 x .. y .. | IC1 S4 U41 XTAL1 + 8 R, 4 C | 270 x 114 | 48 / 6 |

The strongest block-to-block signal ties, from `graph.txt` (shared signal nets, rails excluded):
S4–S6 17 (the level shifters are steered by the ATmega and the MCP23018), S3TERM–S4 16 (the
screw terminals carry the shifted `*_OUT` lines), S3MID–S3UL 13 (the Feather socket mirrors the
SoM's lines), S3MID–S6 10, S3MID–S4 9, S3UL–S6 8, S3UL–S4 7, S3TERM–S5 6 (ADC_0–3, DAC_OUT, VREF
to J2), S3LR_B–S6 6 (LED1–3, LOG_INT), S5–S6 5, S1L_T–S1R_T 4 (5V_LP and the V_PRIME chain),
S2L_B–S2R_B 3 (C0, C1, POWER_EN). Local labels: `5V_LP` has one instance in S1L_T and three in
S1R_T; `RST_TRIG` has one in S3UL and two in S3MID. No other local label crosses a block line.

Two facts the brief's inventory lacked, both load-bearing for the page names: IC1, an
ATmega1284 at (81.3, 109.2) on Okapi_6, is the board's microcontroller (the ~40 "Pin n" notes
are its pins; FT231X TX/RX/DTR, the ICSP header, LED1–3, LOG_INT, C0/C1 and every enable line
end at it), so Okapi_6 is the MCU page and not an expansion leftover; and J5–J8 on Okapi_3 are
the power terminals (J6, J8: LI+/LI-; J7: V_SOLAR and GND; J5: V_PRIME- and V_PRIME_SENSE), not
signal connectors. RTC1 (DS3231M) and BT1 sit on Okapi_5 with the sensors.

## Candidates

Scoring as asked: theme first, then wires (no block boundary cuts a wire, so the wire score is
the count of nets that span two or more pages, computed from the netlist), then fit. Fit is a
rigid-block packing of the measured ink boxes on the 274 x 211 mm drawing area with the
101.6 x 35.56 mm title-block corner blocked, blocks two ticks (2.54 mm) apart, best of every
ordering under a bottom-left rule; a packing that fits is real, a "NO" for a page of several
blocks is a bounding-box verdict (the boxes may have empty corners the packer cannot use).
"Nets out" is the number of nets with a member on the page and on another page, all nets and
then signal nets (the 19 rails of `pages_graph.RAILS` excluded). Two tables sets follow: first
with the SDA note re-wrapped onto three lines (a one-item text edit), then the comparison as
drawn, where that 105 mm note hangs off every page that places its block beside another.

### With the SDA note re-wrapped

The ten-page proposal on the table (regions as its cuts, with the three straddling symbols assigned by pin). Page 1 is the root sheet (178 x 80 mm) in every candidate.

| # | Page | Blocks | Parts | Ink, packed (mm) | Fit | Local labels split | Nets out all / signal | Verdict |
|---|---|---|---|---|---|---|---|---|
| 2 | Power_Input | S1M_T S1M_B S1R_T S1R_B | D1 D2 D3 D8 D9 JP8 L4 Q1 Q2 Q3 Q5 Q6 Q8 S5 U4 U5 U6 U7 U8 U9 U10 U37 + 20 R, 10 C | 259 x 210, slack 15 x 1 (S1M_B at 0,0; S1R_T at 0,99; S1R_B at 144,0; S1M_T at 154,99) | yes | 5V_LP | 22 / 10 | battery protection, charger, V_PRIME selection and core LDO, plus the Feather sleep timer: two themes and a stray |
| 3 | Power_Rails | S1L_T S1L_B | L1 L2 L3 LOGO1 Q7 U1 U2 U3 U13 U39 + 10 R, 9 C | 179 x 183, slack 95 x 28 (S1L_B at 0,0; S1L_T at 0,108) | yes | 5V_LP | 12 / 5 | the 5V_LP, 3V3_AUX, 5V_AUX regulators and the POWER_EN gate: one theme (5V_LP feeds the other page) |
| 4 | Processor | S3UL S3SD | D7 F2 J9 S6 S7 SD1 U35 USB2 + 6 R, 1 C | 268 x 159, slack 6 x 52 (S3UL at 0,0; S3SD at 207,0) | yes | RST_TRIG | 22 / 16 | B-series cellular SoM with its USB, buttons, FRAM, SD card: coherent, but the ATmega1284 is the processor and sits elsewhere |
| 5 | IO_Expansion | S6 S3LAD | D10 D11 D12 D13 D14 D16 D17 D18 IC1 S4 U41 U45 XTAL1 + 17 R, 4 C | 270 x 200, slack 4 x 11 (S6 at 0,0; S3LAD at 0,117) | yes | – | 52 / 47 | misnamed: this is the ATmega1284 MCU page, with the MCP23018 and the PCA9634 LED driver |
| 6 | Level_Shifters | S4 | U24 U25 U26 U27 U28 U29 U34 U36 U42 + 2 R, 6 C | 231 x 158, slack 43 x 53 | yes | – | 49 / 41 | one theme |
| 7 | Sensors | S5 | BT1 D6 JP6 JP7 RTC1 U30 U31 U32 U33 U38 U43 U44 + 4 R, 13 C | 264 x 165, slack 10 x 46 | yes | – | 25 / 17 | one theme (on-board I2C sensors, RTC, DAC, ADC) |
| 8 | Sensor_Power | S2L_T S2L_B | JP1 JP2 JP3 JP4 S1 S2 U11 U12 U14 U15 U16 U17 U18 U19 U20 U21 U22 + 12 R, 2 C | 255 x 117, slack 19 x 94 (S2L_T at 0,0; S2L_B at 165,0) | yes | – | 16 / 7 | port power switches and the V_HP/V_BETA switches; their XOR gate is on another page |
| 9 | Connectors | S3TERM S3MID S3LR_T S3LR_B | D5 H1 H2 H3 ISP1 J1 J2 J3 J4 J5 J6 J7 J8 JP5 MS1 Q4 S3 + 6 R, 0 C | 225 x 154, slack 49 x 57 (S3TERM at 0,0; S3LR_T at 69,0; S3MID at 144,0; S3LR_B at 0,79) | yes | RST_TRIG | 56 / 44 | a leftover: field terminals, Feather socket, ICSP, battery and solar terminals, log button, status LED |
| 10 | USB_Programming | S2R_T S2R_B | D4 F1 J10 U23 U40 U$1 U$2 + 10 R, 5 C | 172 x 146, slack 102 x 65 (S2R_T at 0,0; S2R_B at 0,104) | yes | – | 10 / 7 | USB-C and FT231X, plus the U40 XOR and VDIV jumpers that belong to the power switches |

Totals: 10 pages; nets spanning two or more pages 104 (all) / 85 (signal); local labels split 2 (5V_LP@Okapi_1, RST_TRIG@Okapi_3); pages that do not fit 0; wires cut 0 (every block boundary is wire-clean and pin-clean by pages_regions.py).
  - Power_Input signal nets out: /Okapi_1/5V_LP, BMS_CTR, FEATHER_EN, MPPT_CHRG, MPPT_FAULT, PG_LDO, V_BETA_SENSE, V_LI_SENSE, V_SOLAR_SENSE, WD_DONE
  - Power_Rails signal nets out: /Okapi_1/5V_LP, 3V3_AUX_PG, LBI, POWER_EN, V_HP_SYNC
  - Processor signal nets out: /Okapi_3/RST_TRIG, FEATHER_CTS, FEATHER_GPIO, FEATHER_RTS, MISO, MOSI_BUF, RX, SCK_BUF, SCL, SCL_FEATHER, SDA_FEATHER, SDA_OB, SD_CD, SD_CS_BUF, TX, WD_DONE
  - IO_Expansion signal nets out: 3V3_AUX_PG, ADC_EXT_ALERT, ALIVE_LED, BMS_CTR, BUS_LOGIC_EN_PRIME, BUS_LOGIC_EN_SEC, C0, C1, CSA_~{ALERT}, CS_EXT, DTR, EN_BUS_PRIME, EN_BUS_SEC, FAULT_PRIME, FAULT_SEC, FEATHER_CTS, FEATHER_EN, FEATHER_GPIO, FEATHER_RTS, GPIO_0, GPIO_1, GPIO_2, GPIO_3, LBI, LED1, LED2, LED3, LOG_INT, MISO, MOSI, MPPT_CHRG, MPPT_FAULT, PG_LDO, RST, RTC_INT, RX, RX_EXT, SCK, SCL, SDA, SDA_CTRL, SDA_OB, SD_CD, SD_CS, TX, TX_EXT, V_HP_SYNC
  - Level_Shifters signal nets out: BUS_LOGIC_EN_PRIME, BUS_LOGIC_EN_SEC, CS_EXT, CS_OUT, GPIO_0, GPIO_0_OUT, GPIO_1, GPIO_1_OUT, GPIO_2, GPIO_2_OUT, GPIO_3, GPIO_3_OUT, MISO, MISO_OUT, MOSI, MOSI_BUF, MOSI_OUT, RX_EXT, RX_OUT_PRIME, RX_OUT_SEC, SCK, SCK_BUF, SCK_OUT, SCL, SCL_5V, SCL_FEATHER, SCL_OUT_PRIME, SCL_OUT_SEC, SDA, SDA_5V, SDA_CTRL, SDA_EXT, SDA_FEATHER, SDA_OB, SDA_OUT_PRIME, SDA_OUT_SEC, SD_CS, SD_CS_BUF, TX_EXT, TX_OUT_PRIME, TX_OUT_SEC
  - Sensors signal nets out: ADC_0, ADC_1, ADC_2, ADC_3, ADC_EXT_ALERT, CSA_~{ALERT}, DAC_OUT, RTC_INT, SCL, SCL_5V, SDA_5V, SDA_OB, VREF, V_BETA_SENSE, V_LI_SENSE, V_PRIME_SENSE, V_SOLAR_SENSE
  - Sensor_Power signal nets out: C0, C1, EN_BUS_PRIME, EN_BUS_SEC, FAULT_PRIME, FAULT_SEC, POWER_EN
  - Connectors signal nets out: /Okapi_3/RST_TRIG, ADC_0, ADC_1, ADC_2, ADC_3, CS_OUT, DAC_OUT, FEATHER_CTS, FEATHER_GPIO, FEATHER_RTS, GPIO_0_OUT, GPIO_1_OUT, GPIO_2_OUT, GPIO_3_OUT, LED1, LED2, LED3, LOG_INT, MISO, MISO_OUT, MOSI, MOSI_BUF, MOSI_OUT, RST, RX, RX_OUT_PRIME, RX_OUT_SEC, SCK, SCK_BUF, SCK_OUT, SCL_FEATHER, SCL_OUT_PRIME, SCL_OUT_SEC, SDA_EXT, SDA_FEATHER, SDA_OB, SDA_OUT_PRIME, SDA_OUT_SEC, TX, TX_OUT_PRIME, TX_OUT_SEC, VREF, V_PRIME_SENSE, WD_DONE
  - USB_Programming signal nets out: ALIVE_LED, C0, C1, DTR, POWER_EN, RX, TX

### B_corrected

Baseline with four blocks re-homed and two pages renamed; cuts unchanged. Page 1 is the root sheet (178 x 80 mm) in every candidate.

| # | Page | Blocks | Parts | Ink, packed (mm) | Fit | Local labels split | Nets out all / signal | Verdict |
|---|---|---|---|---|---|---|---|---|
| 2 | Power_Input | S3LR_T S1M_T S1M_B S1R_T S1R_B | D1 D2 D3 D8 D9 J5 J6 J7 J8 JP8 L4 Q1 Q2 Q3 Q5 Q6 Q8 S5 U4 U5 U6 U7 U8 U9 U10 U37 + 21 R, 10 C | row 586 x 111, column 151 x 417 | NO | 5V_LP | 19 / 11 | battery and solar terminals join their protection and charger; still carries the selector and the timer |
| 3 | Power_Rails | S1L_T S1L_B | L1 L2 L3 LOGO1 Q7 U1 U2 U3 U13 U39 + 10 R, 9 C | 179 x 183, slack 95 x 28 (S1L_B at 0,0; S1L_T at 0,108) | yes | 5V_LP | 12 / 5 | one theme |
| 4 | Cell_Module | S3UL S3SD | D7 F2 J9 S6 S7 SD1 U35 USB2 + 6 R, 1 C | 268 x 159, slack 6 x 52 (S3UL at 0,0; S3SD at 207,0) | yes | RST_TRIG | 22 / 16 | B-series SoM and SD card |
| 5 | Microcontroller | S6 S3LAD S3LR_B | D5 D10 D11 D12 D13 D14 D16 D17 D18 IC1 S3 S4 U41 U45 XTAL1 + 21 R, 4 C | row 495 x 114, column 270 x 268 | NO | – | 48 / 43 | ATmega1284, MCP23018, LED driver, status LED and log button: the MCU and what it drives |
| 6 | Level_Shifters | S4 | U24 U25 U26 U27 U28 U29 U34 U36 U42 + 2 R, 6 C | 231 x 158, slack 43 x 53 | yes | – | 49 / 41 | one theme |
| 7 | Sensors | S5 | BT1 D6 JP6 JP7 RTC1 U30 U31 U32 U33 U38 U43 U44 + 4 R, 13 C | 264 x 165, slack 10 x 46 | yes | – | 25 / 17 | one theme |
| 8 | Sensor_Power | S2L_T S2L_B S2R_B | JP1 JP2 JP3 JP4 S1 S2 U11 U12 U14 U15 U16 U17 U18 U19 U20 U21 U22 U40 U$1 U$2 + 12 R, 2 C | 212 x 169, slack 62 x 42 (S2R_B at 0,0; S2L_B at 122,0; S2L_T at 0,52) | yes | – | 16 / 7 | port and rail switches with their enable logic: one theme |
| 9 | Connectors | S3TERM S3MID | H1 H2 H3 ISP1 J1 J2 J3 J4 JP5 MS1 Q4 + 1 R, 0 C | 150 x 154, slack 124 x 57 (S3TERM at 0,0; S3MID at 69,0) | yes | RST_TRIG | 46 / 39 | field terminals, Feather socket, ICSP: headers |
| 10 | USB_Programming | S2R_T | D4 F1 J10 U23 + 10 R, 5 C | 172 x 101, slack 102 x 110 | yes | – | 7 / 4 | USB-C and FT231X alone: coherent but 173 x 101 mm on a page |

Totals: 10 pages; nets spanning two or more pages 96 (all) / 81 (signal); local labels split 2 (5V_LP@Okapi_1, RST_TRIG@Okapi_3); pages that do not fit 2; wires cut 0 (every block boundary is wire-clean and pin-clean by pages_regions.py).
  - Power_Input signal nets out: /Okapi_1/5V_LP, BMS_CTR, FEATHER_EN, MPPT_CHRG, MPPT_FAULT, PG_LDO, V_BETA_SENSE, V_LI_SENSE, V_PRIME_SENSE, V_SOLAR_SENSE, WD_DONE
  - Power_Rails signal nets out: /Okapi_1/5V_LP, 3V3_AUX_PG, LBI, POWER_EN, V_HP_SYNC
  - Cell_Module signal nets out: /Okapi_3/RST_TRIG, FEATHER_CTS, FEATHER_GPIO, FEATHER_RTS, MISO, MOSI_BUF, RX, SCK_BUF, SCL, SCL_FEATHER, SDA_FEATHER, SDA_OB, SD_CD, SD_CS_BUF, TX, WD_DONE
  - Microcontroller signal nets out: 3V3_AUX_PG, ADC_EXT_ALERT, ALIVE_LED, BMS_CTR, BUS_LOGIC_EN_PRIME, BUS_LOGIC_EN_SEC, C0, C1, CSA_~{ALERT}, CS_EXT, DTR, EN_BUS_PRIME, EN_BUS_SEC, FAULT_PRIME, FAULT_SEC, FEATHER_CTS, FEATHER_EN, FEATHER_GPIO, FEATHER_RTS, GPIO_0, GPIO_1, GPIO_2, GPIO_3, LBI, MISO, MOSI, MPPT_CHRG, MPPT_FAULT, PG_LDO, RST, RTC_INT, RX, RX_EXT, SCK, SCL, SDA, SDA_CTRL, SDA_OB, SD_CD, SD_CS, TX, TX_EXT, V_HP_SYNC
  - Level_Shifters signal nets out: BUS_LOGIC_EN_PRIME, BUS_LOGIC_EN_SEC, CS_EXT, CS_OUT, GPIO_0, GPIO_0_OUT, GPIO_1, GPIO_1_OUT, GPIO_2, GPIO_2_OUT, GPIO_3, GPIO_3_OUT, MISO, MISO_OUT, MOSI, MOSI_BUF, MOSI_OUT, RX_EXT, RX_OUT_PRIME, RX_OUT_SEC, SCK, SCK_BUF, SCK_OUT, SCL, SCL_5V, SCL_FEATHER, SCL_OUT_PRIME, SCL_OUT_SEC, SDA, SDA_5V, SDA_CTRL, SDA_EXT, SDA_FEATHER, SDA_OB, SDA_OUT_PRIME, SDA_OUT_SEC, SD_CS, SD_CS_BUF, TX_EXT, TX_OUT_PRIME, TX_OUT_SEC
  - Sensors signal nets out: ADC_0, ADC_1, ADC_2, ADC_3, ADC_EXT_ALERT, CSA_~{ALERT}, DAC_OUT, RTC_INT, SCL, SCL_5V, SDA_5V, SDA_OB, VREF, V_BETA_SENSE, V_LI_SENSE, V_PRIME_SENSE, V_SOLAR_SENSE
  - Sensor_Power signal nets out: C0, C1, EN_BUS_PRIME, EN_BUS_SEC, FAULT_PRIME, FAULT_SEC, POWER_EN
  - Connectors signal nets out: /Okapi_3/RST_TRIG, ADC_0, ADC_1, ADC_2, ADC_3, CS_OUT, DAC_OUT, FEATHER_CTS, FEATHER_GPIO, FEATHER_RTS, GPIO_0_OUT, GPIO_1_OUT, GPIO_2_OUT, GPIO_3_OUT, MISO, MISO_OUT, MOSI, MOSI_BUF, MOSI_OUT, RST, RX, RX_OUT_PRIME, RX_OUT_SEC, SCK, SCK_BUF, SCK_OUT, SCL_FEATHER, SCL_OUT_PRIME, SCL_OUT_SEC, SDA_EXT, SDA_FEATHER, SDA_OB, SDA_OUT_PRIME, SDA_OUT_SEC, TX, TX_OUT_PRIME, TX_OUT_SEC, VREF, WD_DONE
  - USB_Programming signal nets out: ALIVE_LED, DTR, RX, TX

### C_thematic

Signal-path order, every page one function; the Feather timer with the selector column. Page 1 is the root sheet (178 x 80 mm) in every candidate.

| # | Page | Blocks | Parts | Ink, packed (mm) | Fit | Local labels split | Nets out all / signal | Verdict |
|---|---|---|---|---|---|---|---|---|
| 2 | Power_Input | S3LR_T S1M_T S1M_B | D1 D2 D3 J5 J6 J7 J8 L4 Q1 Q2 Q8 S5 U4 U5 + 16 R, 5 C | 180 x 167, slack 94 x 44 (S1M_T at 0,0; S3LR_T at 108,0; S1M_B at 0,70) | yes | – | 11 / 6 | battery and solar terminals, start button, BQ2980 protection, LT3652 charger: everything from the terminals to V_LI |
| 3 | Power_Select | S1R_T S1R_B | D8 D9 JP8 Q3 Q5 Q6 U6 U7 U8 U9 U10 U37 + 5 R, 5 C | 259 x 111, slack 15 x 100 (S1R_T at 0,0; S1R_B at 154,0) | yes | 5V_LP | 13 / 5 | V_PRIME selection (TLV3691, TPS2105, LTC4412), TPS797 core LDO; the TPL5111 Feather timer rides along |
| 4 | Power_Rails | S1L_T S1L_B | L1 L2 L3 LOGO1 Q7 U1 U2 U3 U13 U39 + 10 R, 9 C | 179 x 183, slack 95 x 28 (S1L_B at 0,0; S1L_T at 0,108) | yes | 5V_LP | 12 / 5 | 5V_LP, 3V3_AUX, 5V_AUX regulators and POWER_EN |
| 5 | Microcontroller | S6 S3LAD S3LR_B | D5 D10 D11 D12 D13 D14 D16 D17 D18 IC1 S3 S4 U41 U45 XTAL1 + 21 R, 4 C | row 495 x 114, column 270 x 268 | NO | – | 48 / 43 | ATmega1284, MCP23018, PCA9634 ladder, status LED, log button |
| 6 | Cell_Module | S3UL S3SD | D7 F2 J9 S6 S7 SD1 U35 USB2 + 6 R, 1 C | 268 x 159, slack 6 x 52 (S3UL at 0,0; S3SD at 207,0) | yes | RST_TRIG | 22 / 16 | B-series SoM, its USB, buttons, FRAM; SD card on the shared buffered SPI |
| 7 | Level_Shifters | S4 | U24 U25 U26 U27 U28 U29 U34 U36 U42 + 2 R, 6 C | 231 x 158, slack 43 x 53 | yes | – | 49 / 41 | one theme |
| 8 | Sensors | S5 | BT1 D6 JP6 JP7 RTC1 U30 U31 U32 U33 U38 U43 U44 + 4 R, 13 C | 264 x 165, slack 10 x 46 | yes | – | 25 / 17 | one theme |
| 9 | Sensor_Ports | S2L_T S2L_B S2R_B S3TERM | J1 J2 J3 J4 JP1 JP2 JP3 JP4 S1 S2 U11 U12 U14 U15 U16 U17 U18 U19 U20 U21 U22 U40 U$1 U$2 + 12 R, 2 C | 231 x 169, slack 43 x 42 (S2R_B at 0,0; S2L_B at 122,0; S2L_T at 0,52; S3TERM at 165,52) | yes | – | 38 / 29 | the field ports: MIC2544 switched power, V_HP/V_BETA switches and their logic, and the screw terminals they feed |
| 10 | USB_ISP | S2R_T S3MID | D4 F1 H1 H2 H3 ISP1 J10 JP5 MS1 Q4 U23 + 11 R, 5 C | 256 x 154, slack 18 x 57 (S2R_T at 0,0; S3MID at 175,0) | yes | RST_TRIG | 25 / 19 | Bobby's own heading "USB & ISP": USB-C, FT231X, ICSP header, Feather socket, I2C jumper |

Totals: 10 pages; nets spanning two or more pages 97 (all) / 81 (signal); local labels split 2 (5V_LP@Okapi_1, RST_TRIG@Okapi_3); pages that do not fit 1; wires cut 0 (every block boundary is wire-clean and pin-clean by pages_regions.py).
  - Power_Input signal nets out: BMS_CTR, MPPT_CHRG, MPPT_FAULT, V_LI_SENSE, V_PRIME_SENSE, V_SOLAR_SENSE
  - Power_Select signal nets out: /Okapi_1/5V_LP, FEATHER_EN, PG_LDO, V_BETA_SENSE, WD_DONE
  - Power_Rails signal nets out: /Okapi_1/5V_LP, 3V3_AUX_PG, LBI, POWER_EN, V_HP_SYNC
  - Microcontroller signal nets out: 3V3_AUX_PG, ADC_EXT_ALERT, ALIVE_LED, BMS_CTR, BUS_LOGIC_EN_PRIME, BUS_LOGIC_EN_SEC, C0, C1, CSA_~{ALERT}, CS_EXT, DTR, EN_BUS_PRIME, EN_BUS_SEC, FAULT_PRIME, FAULT_SEC, FEATHER_CTS, FEATHER_EN, FEATHER_GPIO, FEATHER_RTS, GPIO_0, GPIO_1, GPIO_2, GPIO_3, LBI, MISO, MOSI, MPPT_CHRG, MPPT_FAULT, PG_LDO, RST, RTC_INT, RX, RX_EXT, SCK, SCL, SDA, SDA_CTRL, SDA_OB, SD_CD, SD_CS, TX, TX_EXT, V_HP_SYNC
  - Cell_Module signal nets out: /Okapi_3/RST_TRIG, FEATHER_CTS, FEATHER_GPIO, FEATHER_RTS, MISO, MOSI_BUF, RX, SCK_BUF, SCL, SCL_FEATHER, SDA_FEATHER, SDA_OB, SD_CD, SD_CS_BUF, TX, WD_DONE
  - Level_Shifters signal nets out: BUS_LOGIC_EN_PRIME, BUS_LOGIC_EN_SEC, CS_EXT, CS_OUT, GPIO_0, GPIO_0_OUT, GPIO_1, GPIO_1_OUT, GPIO_2, GPIO_2_OUT, GPIO_3, GPIO_3_OUT, MISO, MISO_OUT, MOSI, MOSI_BUF, MOSI_OUT, RX_EXT, RX_OUT_PRIME, RX_OUT_SEC, SCK, SCK_BUF, SCK_OUT, SCL, SCL_5V, SCL_FEATHER, SCL_OUT_PRIME, SCL_OUT_SEC, SDA, SDA_5V, SDA_CTRL, SDA_EXT, SDA_FEATHER, SDA_OB, SDA_OUT_PRIME, SDA_OUT_SEC, SD_CS, SD_CS_BUF, TX_EXT, TX_OUT_PRIME, TX_OUT_SEC
  - Sensors signal nets out: ADC_0, ADC_1, ADC_2, ADC_3, ADC_EXT_ALERT, CSA_~{ALERT}, DAC_OUT, RTC_INT, SCL, SCL_5V, SDA_5V, SDA_OB, VREF, V_BETA_SENSE, V_LI_SENSE, V_PRIME_SENSE, V_SOLAR_SENSE
  - Sensor_Ports signal nets out: ADC_0, ADC_1, ADC_2, ADC_3, C0, C1, CS_OUT, DAC_OUT, EN_BUS_PRIME, EN_BUS_SEC, FAULT_PRIME, FAULT_SEC, GPIO_0_OUT, GPIO_1_OUT, GPIO_2_OUT, GPIO_3_OUT, MISO_OUT, MOSI_OUT, POWER_EN, RX_OUT_PRIME, RX_OUT_SEC, SCK_OUT, SCL_OUT_PRIME, SCL_OUT_SEC, SDA_OUT_PRIME, SDA_OUT_SEC, TX_OUT_PRIME, TX_OUT_SEC, VREF
  - USB_ISP signal nets out: /Okapi_3/RST_TRIG, ALIVE_LED, DTR, FEATHER_CTS, FEATHER_GPIO, FEATHER_RTS, MISO, MOSI, MOSI_BUF, RST, RX, SCK, SCK_BUF, SCL_FEATHER, SDA_EXT, SDA_FEATHER, SDA_OB, TX, WD_DONE

### D_nine

C with the selector merged into Power_Input and the Feather timer beside the Feather socket (nine pages). Page 1 is the root sheet (178 x 80 mm) in every candidate.

| # | Page | Blocks | Parts | Ink, packed (mm) | Fit | Local labels split | Nets out all / signal | Verdict |
|---|---|---|---|---|---|---|---|---|
| 2 | Power_Input | S3LR_T S1M_T S1M_B S1R_T | D1 D2 D3 D8 D9 J5 J6 J7 J8 L4 Q1 Q2 Q5 Q6 Q8 S5 U4 U5 U6 U7 U9 U37 + 18 R, 10 C | 249 x 210, slack 25 x 1 (S3LR_T at 0,0; S1R_T at 75,0; S1M_B at 0,113; S1M_T at 144,113) | yes | 5V_LP | 16 / 9 | terminals, protection, charger, V_PRIME selection, core LDO: the whole input chain |
| 3 | Power_Rails | S1L_T S1L_B | L1 L2 L3 LOGO1 Q7 U1 U2 U3 U13 U39 + 10 R, 9 C | 179 x 183, slack 95 x 28 (S1L_B at 0,0; S1L_T at 0,108) | yes | 5V_LP | 12 / 5 | 5V_LP, 3V3_AUX, 5V_AUX regulators and POWER_EN |
| 4 | Microcontroller | S6 S3LAD S3LR_B | D5 D10 D11 D12 D13 D14 D16 D17 D18 IC1 S3 S4 U41 U45 XTAL1 + 21 R, 4 C | row 495 x 114, column 270 x 268 | NO | – | 48 / 43 | ATmega1284, MCP23018, PCA9634 ladder, status LED, log button |
| 5 | Cell_Module | S3UL S3SD | D7 F2 J9 S6 S7 SD1 U35 USB2 + 6 R, 1 C | 268 x 159, slack 6 x 52 (S3UL at 0,0; S3SD at 207,0) | yes | RST_TRIG | 22 / 16 | B-series SoM and SD card |
| 6 | Level_Shifters | S4 | U24 U25 U26 U27 U28 U29 U34 U36 U42 + 2 R, 6 C | 231 x 158, slack 43 x 53 | yes | – | 49 / 41 | one theme |
| 7 | Sensors | S5 | BT1 D6 JP6 JP7 RTC1 U30 U31 U32 U33 U38 U43 U44 + 4 R, 13 C | 264 x 165, slack 10 x 46 | yes | – | 25 / 17 | one theme |
| 8 | Sensor_Ports | S2L_T S2L_B S2R_B S3TERM | J1 J2 J3 J4 JP1 JP2 JP3 JP4 S1 S2 U11 U12 U14 U15 U16 U17 U18 U19 U20 U21 U22 U40 U$1 U$2 + 12 R, 2 C | 231 x 169, slack 43 x 42 (S2R_B at 0,0; S2L_B at 122,0; S2L_T at 0,52; S3TERM at 165,52) | yes | – | 38 / 29 | switched port power and the screw terminals |
| 9 | USB_ISP_Feather | S2R_T S3MID S1R_B | D4 F1 H1 H2 H3 ISP1 J10 JP5 JP8 MS1 Q3 Q4 U8 U10 U23 + 14 R, 5 C | 256 x 178, slack 18 x 33 (S2R_T at 0,0; S3MID at 175,0; S1R_B at 0,104) | yes | RST_TRIG | 27 / 20 | USB-C, FT231X, ICSP, Feather socket and the TPL5111 timer that gates FEATHER_BAT |

Totals: 9 pages; nets spanning two or more pages 96 (all) / 81 (signal); local labels split 2 (5V_LP@Okapi_1, RST_TRIG@Okapi_3); pages that do not fit 1; wires cut 0 (every block boundary is wire-clean and pin-clean by pages_regions.py).
  - Power_Input signal nets out: /Okapi_1/5V_LP, BMS_CTR, MPPT_CHRG, MPPT_FAULT, PG_LDO, V_BETA_SENSE, V_LI_SENSE, V_PRIME_SENSE, V_SOLAR_SENSE
  - Power_Rails signal nets out: /Okapi_1/5V_LP, 3V3_AUX_PG, LBI, POWER_EN, V_HP_SYNC
  - Microcontroller signal nets out: 3V3_AUX_PG, ADC_EXT_ALERT, ALIVE_LED, BMS_CTR, BUS_LOGIC_EN_PRIME, BUS_LOGIC_EN_SEC, C0, C1, CSA_~{ALERT}, CS_EXT, DTR, EN_BUS_PRIME, EN_BUS_SEC, FAULT_PRIME, FAULT_SEC, FEATHER_CTS, FEATHER_EN, FEATHER_GPIO, FEATHER_RTS, GPIO_0, GPIO_1, GPIO_2, GPIO_3, LBI, MISO, MOSI, MPPT_CHRG, MPPT_FAULT, PG_LDO, RST, RTC_INT, RX, RX_EXT, SCK, SCL, SDA, SDA_CTRL, SDA_OB, SD_CD, SD_CS, TX, TX_EXT, V_HP_SYNC
  - Cell_Module signal nets out: /Okapi_3/RST_TRIG, FEATHER_CTS, FEATHER_GPIO, FEATHER_RTS, MISO, MOSI_BUF, RX, SCK_BUF, SCL, SCL_FEATHER, SDA_FEATHER, SDA_OB, SD_CD, SD_CS_BUF, TX, WD_DONE
  - Level_Shifters signal nets out: BUS_LOGIC_EN_PRIME, BUS_LOGIC_EN_SEC, CS_EXT, CS_OUT, GPIO_0, GPIO_0_OUT, GPIO_1, GPIO_1_OUT, GPIO_2, GPIO_2_OUT, GPIO_3, GPIO_3_OUT, MISO, MISO_OUT, MOSI, MOSI_BUF, MOSI_OUT, RX_EXT, RX_OUT_PRIME, RX_OUT_SEC, SCK, SCK_BUF, SCK_OUT, SCL, SCL_5V, SCL_FEATHER, SCL_OUT_PRIME, SCL_OUT_SEC, SDA, SDA_5V, SDA_CTRL, SDA_EXT, SDA_FEATHER, SDA_OB, SDA_OUT_PRIME, SDA_OUT_SEC, SD_CS, SD_CS_BUF, TX_EXT, TX_OUT_PRIME, TX_OUT_SEC
  - Sensors signal nets out: ADC_0, ADC_1, ADC_2, ADC_3, ADC_EXT_ALERT, CSA_~{ALERT}, DAC_OUT, RTC_INT, SCL, SCL_5V, SDA_5V, SDA_OB, VREF, V_BETA_SENSE, V_LI_SENSE, V_PRIME_SENSE, V_SOLAR_SENSE
  - Sensor_Ports signal nets out: ADC_0, ADC_1, ADC_2, ADC_3, C0, C1, CS_OUT, DAC_OUT, EN_BUS_PRIME, EN_BUS_SEC, FAULT_PRIME, FAULT_SEC, GPIO_0_OUT, GPIO_1_OUT, GPIO_2_OUT, GPIO_3_OUT, MISO_OUT, MOSI_OUT, POWER_EN, RX_OUT_PRIME, RX_OUT_SEC, SCK_OUT, SCL_OUT_PRIME, SCL_OUT_SEC, SDA_OUT_PRIME, SDA_OUT_SEC, TX_OUT_PRIME, TX_OUT_SEC, VREF
  - USB_ISP_Feather signal nets out: /Okapi_3/RST_TRIG, ALIVE_LED, DTR, FEATHER_CTS, FEATHER_EN, FEATHER_GPIO, FEATHER_RTS, MISO, MOSI, MOSI_BUF, RST, RX, SCK, SCK_BUF, SCL_FEATHER, SDA_EXT, SDA_FEATHER, SDA_OB, TX, WD_DONE

### E_core_supply

C with the rails column split so the 5V_LP boost sits with the selector that it feeds (no local label split on Okapi_1). Page 1 is the root sheet (178 x 80 mm) in every candidate.

| # | Page | Blocks | Parts | Ink, packed (mm) | Fit | Local labels split | Nets out all / signal | Verdict |
|---|---|---|---|---|---|---|---|---|
| 2 | Power_Input | S3LR_T S1M_T S1M_B | D1 D2 D3 J5 J6 J7 J8 L4 Q1 Q2 Q8 S5 U4 U5 + 16 R, 5 C | 180 x 167, slack 94 x 44 (S1M_T at 0,0; S3LR_T at 108,0; S1M_B at 0,70) | yes | – | 11 / 6 | terminals, start button, protection, charger |
| 3 | Core_Supply | S1L_T S1R_T | D8 D9 L1 LOGO1 Q5 Q6 U1 U6 U7 U9 U37 U39 + 5 R, 7 C | 151 x 188, slack 123 x 23 (S1L_T at 0,0; S1R_T at 0,78) | yes | – | 11 / 2 | MIC94094, TLV61220 5V_LP boost, TLV3691/TPS2105 V_CORE switch, LTC4412 ideal diode, TPS797 LDO: the 3V3_CORE chain |
| 4 | Aux_Rails | S1L_B S2L_B S2R_B | L2 L3 Q7 U2 U3 U13 U16 U21 U22 U40 U$1 U$2 + 7 R, 7 C | 212 x 158, slack 62 x 53 (S2R_B at 0,0; S2L_B at 122,0; S1L_B at 0,52) | yes | – | 11 / 5 | TPS6282 3V3_AUX, TPS61032 5V_AUX, POWER_EN gate, and the V_HP/V_BETA TPS22917 switches with their C0/C1 logic |
| 5 | Microcontroller | S6 S3LAD S3LR_B | D5 D10 D11 D12 D13 D14 D16 D17 D18 IC1 S3 S4 U41 U45 XTAL1 + 21 R, 4 C | row 495 x 114, column 270 x 268 | NO | – | 48 / 43 | ATmega1284, MCP23018, PCA9634 ladder, status LED, log button |
| 6 | Cell_Module | S3UL S3SD | D7 F2 J9 S6 S7 SD1 U35 USB2 + 6 R, 1 C | 268 x 159, slack 6 x 52 (S3UL at 0,0; S3SD at 207,0) | yes | RST_TRIG | 22 / 16 | B-series SoM and SD card |
| 7 | Level_Shifters | S4 | U24 U25 U26 U27 U28 U29 U34 U36 U42 + 2 R, 6 C | 231 x 158, slack 43 x 53 | yes | – | 49 / 41 | one theme |
| 8 | Sensors | S5 | BT1 D6 JP6 JP7 RTC1 U30 U31 U32 U33 U38 U43 U44 + 4 R, 13 C | 264 x 165, slack 10 x 46 | yes | – | 25 / 17 | one theme |
| 9 | Sensor_Ports | S2L_T S3TERM | J1 J2 J3 J4 JP1 JP2 JP3 JP4 S1 S2 U11 U12 U14 U15 U17 U18 U19 U20 + 12 R, 2 C | 231 x 117, slack 43 x 94 (S2L_T at 0,0; S3TERM at 165,0) | yes | – | 31 / 26 | MIC2544 switched port power and the screw terminals |
| 10 | USB_ISP_Feather | S2R_T S3MID S1R_B | D4 F1 H1 H2 H3 ISP1 J10 JP5 JP8 MS1 Q3 Q4 U8 U10 U23 + 14 R, 5 C | 256 x 178, slack 18 x 33 (S2R_T at 0,0; S3MID at 175,0; S1R_B at 0,104) | yes | RST_TRIG | 27 / 20 | USB-C, FT231X, ICSP, Feather socket and its timer |

Totals: 10 pages; nets spanning two or more pages 94 (all) / 79 (signal); local labels split 1 (RST_TRIG@Okapi_3); pages that do not fit 1; wires cut 0 (every block boundary is wire-clean and pin-clean by pages_regions.py).
  - Power_Input signal nets out: BMS_CTR, MPPT_CHRG, MPPT_FAULT, V_LI_SENSE, V_PRIME_SENSE, V_SOLAR_SENSE
  - Core_Supply signal nets out: PG_LDO, V_BETA_SENSE
  - Aux_Rails signal nets out: 3V3_AUX_PG, C0, C1, LBI, V_HP_SYNC
  - Microcontroller signal nets out: 3V3_AUX_PG, ADC_EXT_ALERT, ALIVE_LED, BMS_CTR, BUS_LOGIC_EN_PRIME, BUS_LOGIC_EN_SEC, C0, C1, CSA_~{ALERT}, CS_EXT, DTR, EN_BUS_PRIME, EN_BUS_SEC, FAULT_PRIME, FAULT_SEC, FEATHER_CTS, FEATHER_EN, FEATHER_GPIO, FEATHER_RTS, GPIO_0, GPIO_1, GPIO_2, GPIO_3, LBI, MISO, MOSI, MPPT_CHRG, MPPT_FAULT, PG_LDO, RST, RTC_INT, RX, RX_EXT, SCK, SCL, SDA, SDA_CTRL, SDA_OB, SD_CD, SD_CS, TX, TX_EXT, V_HP_SYNC
  - Cell_Module signal nets out: /Okapi_3/RST_TRIG, FEATHER_CTS, FEATHER_GPIO, FEATHER_RTS, MISO, MOSI_BUF, RX, SCK_BUF, SCL, SCL_FEATHER, SDA_FEATHER, SDA_OB, SD_CD, SD_CS_BUF, TX, WD_DONE
  - Level_Shifters signal nets out: BUS_LOGIC_EN_PRIME, BUS_LOGIC_EN_SEC, CS_EXT, CS_OUT, GPIO_0, GPIO_0_OUT, GPIO_1, GPIO_1_OUT, GPIO_2, GPIO_2_OUT, GPIO_3, GPIO_3_OUT, MISO, MISO_OUT, MOSI, MOSI_BUF, MOSI_OUT, RX_EXT, RX_OUT_PRIME, RX_OUT_SEC, SCK, SCK_BUF, SCK_OUT, SCL, SCL_5V, SCL_FEATHER, SCL_OUT_PRIME, SCL_OUT_SEC, SDA, SDA_5V, SDA_CTRL, SDA_EXT, SDA_FEATHER, SDA_OB, SDA_OUT_PRIME, SDA_OUT_SEC, SD_CS, SD_CS_BUF, TX_EXT, TX_OUT_PRIME, TX_OUT_SEC
  - Sensors signal nets out: ADC_0, ADC_1, ADC_2, ADC_3, ADC_EXT_ALERT, CSA_~{ALERT}, DAC_OUT, RTC_INT, SCL, SCL_5V, SDA_5V, SDA_OB, VREF, V_BETA_SENSE, V_LI_SENSE, V_PRIME_SENSE, V_SOLAR_SENSE
  - Sensor_Ports signal nets out: ADC_0, ADC_1, ADC_2, ADC_3, CS_OUT, DAC_OUT, EN_BUS_PRIME, EN_BUS_SEC, FAULT_PRIME, FAULT_SEC, GPIO_0_OUT, GPIO_1_OUT, GPIO_2_OUT, GPIO_3_OUT, MISO_OUT, MOSI_OUT, RX_OUT_PRIME, RX_OUT_SEC, SCK_OUT, SCL_OUT_PRIME, SCL_OUT_SEC, SDA_OUT_PRIME, SDA_OUT_SEC, TX_OUT_PRIME, TX_OUT_SEC, VREF
  - USB_ISP_Feather signal nets out: /Okapi_3/RST_TRIG, ALIVE_LED, DTR, FEATHER_CTS, FEATHER_EN, FEATHER_GPIO, FEATHER_RTS, MISO, MOSI, MOSI_BUF, RST, RX, SCK, SCK_BUF, SCL_FEATHER, SDA_EXT, SDA_FEATHER, SDA_OB, TX, WD_DONE

### G_indicators

C with an eleventh page for the indicators, so that the MCU page holds the MCU and nothing is a stray. Page 1 is the root sheet (178 x 80 mm) in every candidate.

| # | Page | Blocks | Parts | Ink, packed (mm) | Fit | Local labels split | Nets out all / signal | Verdict |
|---|---|---|---|---|---|---|---|---|
| 2 | Power_Input | S3LR_T S1M_T S1M_B | D1 D2 D3 J5 J6 J7 J8 L4 Q1 Q2 Q8 S5 U4 U5 + 16 R, 5 C | 180 x 167, slack 94 x 44 (S1M_T at 0,0; S3LR_T at 108,0; S1M_B at 0,70) | yes | – | 11 / 6 | terminals, start button, protection, charger |
| 3 | Power_Select | S1R_T S1R_B | D8 D9 JP8 Q3 Q5 Q6 U6 U7 U8 U9 U10 U37 + 5 R, 5 C | 259 x 111, slack 15 x 100 (S1R_T at 0,0; S1R_B at 154,0) | yes | 5V_LP | 13 / 5 | V_PRIME selection and core LDO; the Feather timer rides along |
| 4 | Power_Rails | S1L_T S1L_B | L1 L2 L3 LOGO1 Q7 U1 U2 U3 U13 U39 + 10 R, 9 C | 179 x 183, slack 95 x 28 (S1L_B at 0,0; S1L_T at 0,108) | yes | 5V_LP | 12 / 5 | 5V_LP, 3V3_AUX, 5V_AUX regulators and POWER_EN |
| 5 | Microcontroller | S6 | IC1 S4 U41 XTAL1 + 8 R, 4 C | 270 x 114, slack 4 x 97 | yes | – | 53 / 48 | ATmega1284 and MCP23018, as Okapi_6 is today |
| 6 | Indicators | S3LAD S3LR_B | D5 D10 D11 D12 D13 D14 D16 D17 D18 S3 U45 + 13 R, 0 C | 223 x 83, slack 51 x 128 (S3LAD at 0,0; S3LR_B at 140,0) | yes | – | 9 / 7 | Bobby's heading "Indicators": PCA9634 ladder, D5 status LED, S3 log button; a small page |
| 7 | Cell_Module | S3UL S3SD | D7 F2 J9 S6 S7 SD1 U35 USB2 + 6 R, 1 C | 268 x 159, slack 6 x 52 (S3UL at 0,0; S3SD at 207,0) | yes | RST_TRIG | 22 / 16 | B-series SoM and SD card |
| 8 | Level_Shifters | S4 | U24 U25 U26 U27 U28 U29 U34 U36 U42 + 2 R, 6 C | 231 x 158, slack 43 x 53 | yes | – | 49 / 41 | one theme |
| 9 | Sensors | S5 | BT1 D6 JP6 JP7 RTC1 U30 U31 U32 U33 U38 U43 U44 + 4 R, 13 C | 264 x 165, slack 10 x 46 | yes | – | 25 / 17 | one theme |
| 10 | Sensor_Ports | S2L_T S2L_B S2R_B S3TERM | J1 J2 J3 J4 JP1 JP2 JP3 JP4 S1 S2 U11 U12 U14 U15 U16 U17 U18 U19 U20 U21 U22 U40 U$1 U$2 + 12 R, 2 C | 231 x 169, slack 43 x 42 (S2R_B at 0,0; S2L_B at 122,0; S2L_T at 0,52; S3TERM at 165,52) | yes | – | 38 / 29 | switched port power, rail switches and logic, screw terminals |
| 11 | USB_ISP | S2R_T S3MID | D4 F1 H1 H2 H3 ISP1 J10 JP5 MS1 Q4 U23 + 11 R, 5 C | 256 x 154, slack 18 x 57 (S2R_T at 0,0; S3MID at 175,0) | yes | RST_TRIG | 25 / 19 | USB-C, FT231X, ICSP, Feather socket, I2C jumper |

Totals: 11 pages; nets spanning two or more pages 102 (all) / 86 (signal); local labels split 2 (5V_LP@Okapi_1, RST_TRIG@Okapi_3); pages that do not fit 0; wires cut 0 (every block boundary is wire-clean and pin-clean by pages_regions.py).
  - Power_Input signal nets out: BMS_CTR, MPPT_CHRG, MPPT_FAULT, V_LI_SENSE, V_PRIME_SENSE, V_SOLAR_SENSE
  - Power_Select signal nets out: /Okapi_1/5V_LP, FEATHER_EN, PG_LDO, V_BETA_SENSE, WD_DONE
  - Power_Rails signal nets out: /Okapi_1/5V_LP, 3V3_AUX_PG, LBI, POWER_EN, V_HP_SYNC
  - Microcontroller signal nets out: 3V3_AUX_PG, ADC_EXT_ALERT, ALIVE_LED, BMS_CTR, BUS_LOGIC_EN_PRIME, BUS_LOGIC_EN_SEC, C0, C1, CSA_~{ALERT}, CS_EXT, DTR, EN_BUS_PRIME, EN_BUS_SEC, FAULT_PRIME, FAULT_SEC, FEATHER_CTS, FEATHER_EN, FEATHER_GPIO, FEATHER_RTS, GPIO_0, GPIO_1, GPIO_2, GPIO_3, LBI, LED1, LED2, LED3, LOG_INT, MISO, MOSI, MPPT_CHRG, MPPT_FAULT, PG_LDO, RST, RTC_INT, RX, RX_EXT, SCK, SCL, SDA, SDA_CTRL, SDA_OB, SD_CD, SD_CS, TX, TX_EXT, V_HP_SYNC, ~{LED_EN}
  - Indicators signal nets out: LED1, LED2, LED3, LOG_INT, SCL, SDA_OB, ~{LED_EN}
  - Cell_Module signal nets out: /Okapi_3/RST_TRIG, FEATHER_CTS, FEATHER_GPIO, FEATHER_RTS, MISO, MOSI_BUF, RX, SCK_BUF, SCL, SCL_FEATHER, SDA_FEATHER, SDA_OB, SD_CD, SD_CS_BUF, TX, WD_DONE
  - Level_Shifters signal nets out: BUS_LOGIC_EN_PRIME, BUS_LOGIC_EN_SEC, CS_EXT, CS_OUT, GPIO_0, GPIO_0_OUT, GPIO_1, GPIO_1_OUT, GPIO_2, GPIO_2_OUT, GPIO_3, GPIO_3_OUT, MISO, MISO_OUT, MOSI, MOSI_BUF, MOSI_OUT, RX_EXT, RX_OUT_PRIME, RX_OUT_SEC, SCK, SCK_BUF, SCK_OUT, SCL, SCL_5V, SCL_FEATHER, SCL_OUT_PRIME, SCL_OUT_SEC, SDA, SDA_5V, SDA_CTRL, SDA_EXT, SDA_FEATHER, SDA_OB, SDA_OUT_PRIME, SDA_OUT_SEC, SD_CS, SD_CS_BUF, TX_EXT, TX_OUT_PRIME, TX_OUT_SEC
  - Sensors signal nets out: ADC_0, ADC_1, ADC_2, ADC_3, ADC_EXT_ALERT, CSA_~{ALERT}, DAC_OUT, RTC_INT, SCL, SCL_5V, SDA_5V, SDA_OB, VREF, V_BETA_SENSE, V_LI_SENSE, V_PRIME_SENSE, V_SOLAR_SENSE
  - Sensor_Ports signal nets out: ADC_0, ADC_1, ADC_2, ADC_3, C0, C1, CS_OUT, DAC_OUT, EN_BUS_PRIME, EN_BUS_SEC, FAULT_PRIME, FAULT_SEC, GPIO_0_OUT, GPIO_1_OUT, GPIO_2_OUT, GPIO_3_OUT, MISO_OUT, MOSI_OUT, POWER_EN, RX_OUT_PRIME, RX_OUT_SEC, SCK_OUT, SCL_OUT_PRIME, SCL_OUT_SEC, SDA_OUT_PRIME, SDA_OUT_SEC, TX_OUT_PRIME, TX_OUT_SEC, VREF
  - USB_ISP signal nets out: /Okapi_3/RST_TRIG, ALIVE_LED, DTR, FEATHER_CTS, FEATHER_GPIO, FEATHER_RTS, MISO, MOSI, MOSI_BUF, RST, RX, SCK, SCK_BUF, SCL_FEATHER, SDA_EXT, SDA_FEATHER, SDA_OB, TX, WD_DONE

### H_core_indicators

E (rails column split) with the Indicators page and the Feather timer beside its socket. Page 1 is the root sheet (178 x 80 mm) in every candidate.

| # | Page | Blocks | Parts | Ink, packed (mm) | Fit | Local labels split | Nets out all / signal | Verdict |
|---|---|---|---|---|---|---|---|---|
| 2 | Power_Input | S3LR_T S1M_T S1M_B | D1 D2 D3 J5 J6 J7 J8 L4 Q1 Q2 Q8 S5 U4 U5 + 16 R, 5 C | 180 x 167, slack 94 x 44 (S1M_T at 0,0; S3LR_T at 108,0; S1M_B at 0,70) | yes | – | 11 / 6 | terminals, start button, protection, charger |
| 3 | Core_Supply | S1L_T S1R_T | D8 D9 L1 LOGO1 Q5 Q6 U1 U6 U7 U9 U37 U39 + 5 R, 7 C | 151 x 188, slack 123 x 23 (S1L_T at 0,0; S1R_T at 0,78) | yes | – | 11 / 2 | MIC94094, 5V_LP boost, V_CORE switch, ideal diode, TPS797: the 3V3_CORE chain |
| 4 | Aux_Rails | S1L_B S2L_B S2R_B | L2 L3 Q7 U2 U3 U13 U16 U21 U22 U40 U$1 U$2 + 7 R, 7 C | 212 x 158, slack 62 x 53 (S2R_B at 0,0; S2L_B at 122,0; S1L_B at 0,52) | yes | – | 11 / 5 | 3V3_AUX, 5V_AUX, POWER_EN, and the V_HP/V_BETA switches with their logic |
| 5 | Microcontroller | S6 | IC1 S4 U41 XTAL1 + 8 R, 4 C | 270 x 114, slack 4 x 97 | yes | – | 53 / 48 | ATmega1284 and MCP23018 |
| 6 | Indicators | S3LAD S3LR_B | D5 D10 D11 D12 D13 D14 D16 D17 D18 S3 U45 + 13 R, 0 C | 223 x 83, slack 51 x 128 (S3LAD at 0,0; S3LR_B at 140,0) | yes | – | 9 / 7 | PCA9634 ladder, D5 status LED, S3 log button |
| 7 | Cell_Module | S3UL S3SD | D7 F2 J9 S6 S7 SD1 U35 USB2 + 6 R, 1 C | 268 x 159, slack 6 x 52 (S3UL at 0,0; S3SD at 207,0) | yes | RST_TRIG | 22 / 16 | B-series SoM and SD card |
| 8 | Level_Shifters | S4 | U24 U25 U26 U27 U28 U29 U34 U36 U42 + 2 R, 6 C | 231 x 158, slack 43 x 53 | yes | – | 49 / 41 | one theme |
| 9 | Sensors | S5 | BT1 D6 JP6 JP7 RTC1 U30 U31 U32 U33 U38 U43 U44 + 4 R, 13 C | 264 x 165, slack 10 x 46 | yes | – | 25 / 17 | one theme |
| 10 | Sensor_Ports | S2L_T S3TERM | J1 J2 J3 J4 JP1 JP2 JP3 JP4 S1 S2 U11 U12 U14 U15 U17 U18 U19 U20 + 12 R, 2 C | 231 x 117, slack 43 x 94 (S2L_T at 0,0; S3TERM at 165,0) | yes | – | 31 / 26 | MIC2544 switched port power and the screw terminals |
| 11 | USB_ISP_Feather | S2R_T S3MID S1R_B | D4 F1 H1 H2 H3 ISP1 J10 JP5 JP8 MS1 Q3 Q4 U8 U10 U23 + 14 R, 5 C | 256 x 178, slack 18 x 33 (S2R_T at 0,0; S3MID at 175,0; S1R_B at 0,104) | yes | RST_TRIG | 27 / 20 | USB-C, FT231X, ICSP, Feather socket and its timer |

Totals: 11 pages; nets spanning two or more pages 99 (all) / 84 (signal); local labels split 1 (RST_TRIG@Okapi_3); pages that do not fit 0; wires cut 0 (every block boundary is wire-clean and pin-clean by pages_regions.py).
  - Power_Input signal nets out: BMS_CTR, MPPT_CHRG, MPPT_FAULT, V_LI_SENSE, V_PRIME_SENSE, V_SOLAR_SENSE
  - Core_Supply signal nets out: PG_LDO, V_BETA_SENSE
  - Aux_Rails signal nets out: 3V3_AUX_PG, C0, C1, LBI, V_HP_SYNC
  - Microcontroller signal nets out: 3V3_AUX_PG, ADC_EXT_ALERT, ALIVE_LED, BMS_CTR, BUS_LOGIC_EN_PRIME, BUS_LOGIC_EN_SEC, C0, C1, CSA_~{ALERT}, CS_EXT, DTR, EN_BUS_PRIME, EN_BUS_SEC, FAULT_PRIME, FAULT_SEC, FEATHER_CTS, FEATHER_EN, FEATHER_GPIO, FEATHER_RTS, GPIO_0, GPIO_1, GPIO_2, GPIO_3, LBI, LED1, LED2, LED3, LOG_INT, MISO, MOSI, MPPT_CHRG, MPPT_FAULT, PG_LDO, RST, RTC_INT, RX, RX_EXT, SCK, SCL, SDA, SDA_CTRL, SDA_OB, SD_CD, SD_CS, TX, TX_EXT, V_HP_SYNC, ~{LED_EN}
  - Indicators signal nets out: LED1, LED2, LED3, LOG_INT, SCL, SDA_OB, ~{LED_EN}
  - Cell_Module signal nets out: /Okapi_3/RST_TRIG, FEATHER_CTS, FEATHER_GPIO, FEATHER_RTS, MISO, MOSI_BUF, RX, SCK_BUF, SCL, SCL_FEATHER, SDA_FEATHER, SDA_OB, SD_CD, SD_CS_BUF, TX, WD_DONE
  - Level_Shifters signal nets out: BUS_LOGIC_EN_PRIME, BUS_LOGIC_EN_SEC, CS_EXT, CS_OUT, GPIO_0, GPIO_0_OUT, GPIO_1, GPIO_1_OUT, GPIO_2, GPIO_2_OUT, GPIO_3, GPIO_3_OUT, MISO, MISO_OUT, MOSI, MOSI_BUF, MOSI_OUT, RX_EXT, RX_OUT_PRIME, RX_OUT_SEC, SCK, SCK_BUF, SCK_OUT, SCL, SCL_5V, SCL_FEATHER, SCL_OUT_PRIME, SCL_OUT_SEC, SDA, SDA_5V, SDA_CTRL, SDA_EXT, SDA_FEATHER, SDA_OB, SDA_OUT_PRIME, SDA_OUT_SEC, SD_CS, SD_CS_BUF, TX_EXT, TX_OUT_PRIME, TX_OUT_SEC
  - Sensors signal nets out: ADC_0, ADC_1, ADC_2, ADC_3, ADC_EXT_ALERT, CSA_~{ALERT}, DAC_OUT, RTC_INT, SCL, SCL_5V, SDA_5V, SDA_OB, VREF, V_BETA_SENSE, V_LI_SENSE, V_PRIME_SENSE, V_SOLAR_SENSE
  - Sensor_Ports signal nets out: ADC_0, ADC_1, ADC_2, ADC_3, CS_OUT, DAC_OUT, EN_BUS_PRIME, EN_BUS_SEC, FAULT_PRIME, FAULT_SEC, GPIO_0_OUT, GPIO_1_OUT, GPIO_2_OUT, GPIO_3_OUT, MISO_OUT, MOSI_OUT, RX_OUT_PRIME, RX_OUT_SEC, SCK_OUT, SCL_OUT_PRIME, SCL_OUT_SEC, SDA_OUT_PRIME, SDA_OUT_SEC, TX_OUT_PRIME, TX_OUT_SEC, VREF
  - USB_ISP_Feather signal nets out: /Okapi_3/RST_TRIG, ALIVE_LED, DTR, FEATHER_CTS, FEATHER_EN, FEATHER_GPIO, FEATHER_RTS, MISO, MOSI, MOSI_BUF, RST, RX, SCK, SCK_BUF, SCL_FEATHER, SDA_EXT, SDA_FEATHER, SDA_OB, TX, WD_DONE

### C2_stray_on_usb

C with the MCU page as the baseline has it (MCU + ladder) and the status LED and log button on the USB/ISP page. Page 1 is the root sheet (178 x 80 mm) in every candidate.

| # | Page | Blocks | Parts | Ink, packed (mm) | Fit | Local labels split | Nets out all / signal | Verdict |
|---|---|---|---|---|---|---|---|---|
| 2 | Power_Input | S3LR_T S1M_T S1M_B | D1 D2 D3 J5 J6 J7 J8 L4 Q1 Q2 Q8 S5 U4 U5 + 16 R, 5 C | 180 x 167, slack 94 x 44 (S1M_T at 0,0; S3LR_T at 108,0; S1M_B at 0,70) | yes | – | 11 / 6 | terminals, start button, protection, charger |
| 3 | Power_Select | S1R_T S1R_B | D8 D9 JP8 Q3 Q5 Q6 U6 U7 U8 U9 U10 U37 + 5 R, 5 C | 259 x 111, slack 15 x 100 (S1R_T at 0,0; S1R_B at 154,0) | yes | 5V_LP | 13 / 5 | V_PRIME selection and core LDO; the Feather timer rides along |
| 4 | Power_Rails | S1L_T S1L_B | L1 L2 L3 LOGO1 Q7 U1 U2 U3 U13 U39 + 10 R, 9 C | 179 x 183, slack 95 x 28 (S1L_B at 0,0; S1L_T at 0,108) | yes | 5V_LP | 12 / 5 | 5V_LP, 3V3_AUX, 5V_AUX regulators and POWER_EN |
| 5 | Microcontroller | S6 S3LAD | D10 D11 D12 D13 D14 D16 D17 D18 IC1 S4 U41 U45 XTAL1 + 17 R, 4 C | 270 x 200, slack 4 x 11 (S6 at 0,0; S3LAD at 0,117) | yes | – | 52 / 47 | ATmega1284, MCP23018, PCA9634 ladder |
| 6 | Cell_Module | S3UL S3SD | D7 F2 J9 S6 S7 SD1 U35 USB2 + 6 R, 1 C | 268 x 159, slack 6 x 52 (S3UL at 0,0; S3SD at 207,0) | yes | RST_TRIG | 22 / 16 | B-series SoM and SD card |
| 7 | Level_Shifters | S4 | U24 U25 U26 U27 U28 U29 U34 U36 U42 + 2 R, 6 C | 231 x 158, slack 43 x 53 | yes | – | 49 / 41 | one theme |
| 8 | Sensors | S5 | BT1 D6 JP6 JP7 RTC1 U30 U31 U32 U33 U38 U43 U44 + 4 R, 13 C | 264 x 165, slack 10 x 46 | yes | – | 25 / 17 | one theme |
| 9 | Sensor_Ports | S2L_T S2L_B S2R_B S3TERM | J1 J2 J3 J4 JP1 JP2 JP3 JP4 S1 S2 U11 U12 U14 U15 U16 U17 U18 U19 U20 U21 U22 U40 U$1 U$2 + 12 R, 2 C | 231 x 169, slack 43 x 42 (S2R_B at 0,0; S2L_B at 122,0; S2L_T at 0,52; S3TERM at 165,52) | yes | – | 38 / 29 | switched port power, rail switches and logic, screw terminals |
| 10 | USB_ISP | S2R_T S3MID S3LR_B | D4 D5 F1 H1 H2 H3 ISP1 J10 JP5 MS1 Q4 S3 U23 + 15 R, 5 C | 256 x 170, slack 18 x 41 (S2R_T at 0,0; S3MID at 175,0; S3LR_B at 0,104) | yes | RST_TRIG | 29 / 23 | USB-C, FT231X, ICSP, Feather socket, and a stray status LED and log button |

Totals: 10 pages; nets spanning two or more pages 101 (all) / 85 (signal); local labels split 2 (5V_LP@Okapi_1, RST_TRIG@Okapi_3); pages that do not fit 0; wires cut 0 (every block boundary is wire-clean and pin-clean by pages_regions.py).
  - Power_Input signal nets out: BMS_CTR, MPPT_CHRG, MPPT_FAULT, V_LI_SENSE, V_PRIME_SENSE, V_SOLAR_SENSE
  - Power_Select signal nets out: /Okapi_1/5V_LP, FEATHER_EN, PG_LDO, V_BETA_SENSE, WD_DONE
  - Power_Rails signal nets out: /Okapi_1/5V_LP, 3V3_AUX_PG, LBI, POWER_EN, V_HP_SYNC
  - Microcontroller signal nets out: 3V3_AUX_PG, ADC_EXT_ALERT, ALIVE_LED, BMS_CTR, BUS_LOGIC_EN_PRIME, BUS_LOGIC_EN_SEC, C0, C1, CSA_~{ALERT}, CS_EXT, DTR, EN_BUS_PRIME, EN_BUS_SEC, FAULT_PRIME, FAULT_SEC, FEATHER_CTS, FEATHER_EN, FEATHER_GPIO, FEATHER_RTS, GPIO_0, GPIO_1, GPIO_2, GPIO_3, LBI, LED1, LED2, LED3, LOG_INT, MISO, MOSI, MPPT_CHRG, MPPT_FAULT, PG_LDO, RST, RTC_INT, RX, RX_EXT, SCK, SCL, SDA, SDA_CTRL, SDA_OB, SD_CD, SD_CS, TX, TX_EXT, V_HP_SYNC
  - Cell_Module signal nets out: /Okapi_3/RST_TRIG, FEATHER_CTS, FEATHER_GPIO, FEATHER_RTS, MISO, MOSI_BUF, RX, SCK_BUF, SCL, SCL_FEATHER, SDA_FEATHER, SDA_OB, SD_CD, SD_CS_BUF, TX, WD_DONE
  - Level_Shifters signal nets out: BUS_LOGIC_EN_PRIME, BUS_LOGIC_EN_SEC, CS_EXT, CS_OUT, GPIO_0, GPIO_0_OUT, GPIO_1, GPIO_1_OUT, GPIO_2, GPIO_2_OUT, GPIO_3, GPIO_3_OUT, MISO, MISO_OUT, MOSI, MOSI_BUF, MOSI_OUT, RX_EXT, RX_OUT_PRIME, RX_OUT_SEC, SCK, SCK_BUF, SCK_OUT, SCL, SCL_5V, SCL_FEATHER, SCL_OUT_PRIME, SCL_OUT_SEC, SDA, SDA_5V, SDA_CTRL, SDA_EXT, SDA_FEATHER, SDA_OB, SDA_OUT_PRIME, SDA_OUT_SEC, SD_CS, SD_CS_BUF, TX_EXT, TX_OUT_PRIME, TX_OUT_SEC
  - Sensors signal nets out: ADC_0, ADC_1, ADC_2, ADC_3, ADC_EXT_ALERT, CSA_~{ALERT}, DAC_OUT, RTC_INT, SCL, SCL_5V, SDA_5V, SDA_OB, VREF, V_BETA_SENSE, V_LI_SENSE, V_PRIME_SENSE, V_SOLAR_SENSE
  - Sensor_Ports signal nets out: ADC_0, ADC_1, ADC_2, ADC_3, C0, C1, CS_OUT, DAC_OUT, EN_BUS_PRIME, EN_BUS_SEC, FAULT_PRIME, FAULT_SEC, GPIO_0_OUT, GPIO_1_OUT, GPIO_2_OUT, GPIO_3_OUT, MISO_OUT, MOSI_OUT, POWER_EN, RX_OUT_PRIME, RX_OUT_SEC, SCK_OUT, SCL_OUT_PRIME, SCL_OUT_SEC, SDA_OUT_PRIME, SDA_OUT_SEC, TX_OUT_PRIME, TX_OUT_SEC, VREF
  - USB_ISP signal nets out: /Okapi_3/RST_TRIG, ALIVE_LED, DTR, FEATHER_CTS, FEATHER_GPIO, FEATHER_RTS, LED1, LED2, LED3, LOG_INT, MISO, MOSI, MOSI_BUF, RST, RX, SCK, SCK_BUF, SCL_FEATHER, SDA_EXT, SDA_FEATHER, SDA_OB, TX, WD_DONE

### I_nine_fit

D with the ladder on the MCU page and the status LED and log button beside the Feather socket: the nine-page layout that fits. Page 1 is the root sheet (178 x 80 mm) in every candidate.

| # | Page | Blocks | Parts | Ink, packed (mm) | Fit | Local labels split | Nets out all / signal | Verdict |
|---|---|---|---|---|---|---|---|---|
| 2 | Power_Input | S3LR_T S1M_T S1M_B S1R_T | D1 D2 D3 D8 D9 J5 J6 J7 J8 L4 Q1 Q2 Q5 Q6 Q8 S5 U4 U5 U6 U7 U9 U37 + 18 R, 10 C | 249 x 210, slack 25 x 1 (S3LR_T at 0,0; S1R_T at 75,0; S1M_B at 0,113; S1M_T at 144,113) | yes | 5V_LP | 16 / 9 | terminals, protection, charger, V_PRIME selection, core LDO: the whole input chain |
| 3 | Power_Rails | S1L_T S1L_B | L1 L2 L3 LOGO1 Q7 U1 U2 U3 U13 U39 + 10 R, 9 C | 179 x 183, slack 95 x 28 (S1L_B at 0,0; S1L_T at 0,108) | yes | 5V_LP | 12 / 5 | 5V_LP, 3V3_AUX, 5V_AUX regulators and POWER_EN |
| 4 | Microcontroller | S6 S3LAD | D10 D11 D12 D13 D14 D16 D17 D18 IC1 S4 U41 U45 XTAL1 + 17 R, 4 C | 270 x 200, slack 4 x 11 (S6 at 0,0; S3LAD at 0,117) | yes | – | 52 / 47 | ATmega1284, MCP23018, PCA9634 ladder |
| 5 | Cell_Module | S3UL S3SD | D7 F2 J9 S6 S7 SD1 U35 USB2 + 6 R, 1 C | 268 x 159, slack 6 x 52 (S3UL at 0,0; S3SD at 207,0) | yes | RST_TRIG | 22 / 16 | B-series SoM and SD card |
| 6 | Level_Shifters | S4 | U24 U25 U26 U27 U28 U29 U34 U36 U42 + 2 R, 6 C | 231 x 158, slack 43 x 53 | yes | – | 49 / 41 | one theme |
| 7 | Sensors | S5 | BT1 D6 JP6 JP7 RTC1 U30 U31 U32 U33 U38 U43 U44 + 4 R, 13 C | 264 x 165, slack 10 x 46 | yes | – | 25 / 17 | one theme |
| 8 | Sensor_Ports | S2L_T S2L_B S2R_B S3TERM | J1 J2 J3 J4 JP1 JP2 JP3 JP4 S1 S2 U11 U12 U14 U15 U16 U17 U18 U19 U20 U21 U22 U40 U$1 U$2 + 12 R, 2 C | 231 x 169, slack 43 x 42 (S2R_B at 0,0; S2L_B at 122,0; S2L_T at 0,52; S3TERM at 165,52) | yes | – | 38 / 29 | switched port power, rail switches and logic, screw terminals |
| 9 | USB_ISP_Feather | S2R_T S3MID S1R_B S3LR_B | D4 D5 F1 H1 H2 H3 ISP1 J10 JP5 JP8 MS1 Q3 Q4 S3 U8 U10 U23 + 18 R, 5 C | row 449 x 154, column 172 x 404 | NO | RST_TRIG | 31 / 24 | USB-C, FT231X, ICSP, Feather socket and timer, plus a stray status LED and log button |

Totals: 9 pages; nets spanning two or more pages 100 (all) / 85 (signal); local labels split 2 (5V_LP@Okapi_1, RST_TRIG@Okapi_3); pages that do not fit 1; wires cut 0 (every block boundary is wire-clean and pin-clean by pages_regions.py).
  - Power_Input signal nets out: /Okapi_1/5V_LP, BMS_CTR, MPPT_CHRG, MPPT_FAULT, PG_LDO, V_BETA_SENSE, V_LI_SENSE, V_PRIME_SENSE, V_SOLAR_SENSE
  - Power_Rails signal nets out: /Okapi_1/5V_LP, 3V3_AUX_PG, LBI, POWER_EN, V_HP_SYNC
  - Microcontroller signal nets out: 3V3_AUX_PG, ADC_EXT_ALERT, ALIVE_LED, BMS_CTR, BUS_LOGIC_EN_PRIME, BUS_LOGIC_EN_SEC, C0, C1, CSA_~{ALERT}, CS_EXT, DTR, EN_BUS_PRIME, EN_BUS_SEC, FAULT_PRIME, FAULT_SEC, FEATHER_CTS, FEATHER_EN, FEATHER_GPIO, FEATHER_RTS, GPIO_0, GPIO_1, GPIO_2, GPIO_3, LBI, LED1, LED2, LED3, LOG_INT, MISO, MOSI, MPPT_CHRG, MPPT_FAULT, PG_LDO, RST, RTC_INT, RX, RX_EXT, SCK, SCL, SDA, SDA_CTRL, SDA_OB, SD_CD, SD_CS, TX, TX_EXT, V_HP_SYNC
  - Cell_Module signal nets out: /Okapi_3/RST_TRIG, FEATHER_CTS, FEATHER_GPIO, FEATHER_RTS, MISO, MOSI_BUF, RX, SCK_BUF, SCL, SCL_FEATHER, SDA_FEATHER, SDA_OB, SD_CD, SD_CS_BUF, TX, WD_DONE
  - Level_Shifters signal nets out: BUS_LOGIC_EN_PRIME, BUS_LOGIC_EN_SEC, CS_EXT, CS_OUT, GPIO_0, GPIO_0_OUT, GPIO_1, GPIO_1_OUT, GPIO_2, GPIO_2_OUT, GPIO_3, GPIO_3_OUT, MISO, MISO_OUT, MOSI, MOSI_BUF, MOSI_OUT, RX_EXT, RX_OUT_PRIME, RX_OUT_SEC, SCK, SCK_BUF, SCK_OUT, SCL, SCL_5V, SCL_FEATHER, SCL_OUT_PRIME, SCL_OUT_SEC, SDA, SDA_5V, SDA_CTRL, SDA_EXT, SDA_FEATHER, SDA_OB, SDA_OUT_PRIME, SDA_OUT_SEC, SD_CS, SD_CS_BUF, TX_EXT, TX_OUT_PRIME, TX_OUT_SEC
  - Sensors signal nets out: ADC_0, ADC_1, ADC_2, ADC_3, ADC_EXT_ALERT, CSA_~{ALERT}, DAC_OUT, RTC_INT, SCL, SCL_5V, SDA_5V, SDA_OB, VREF, V_BETA_SENSE, V_LI_SENSE, V_PRIME_SENSE, V_SOLAR_SENSE
  - Sensor_Ports signal nets out: ADC_0, ADC_1, ADC_2, ADC_3, C0, C1, CS_OUT, DAC_OUT, EN_BUS_PRIME, EN_BUS_SEC, FAULT_PRIME, FAULT_SEC, GPIO_0_OUT, GPIO_1_OUT, GPIO_2_OUT, GPIO_3_OUT, MISO_OUT, MOSI_OUT, POWER_EN, RX_OUT_PRIME, RX_OUT_SEC, SCK_OUT, SCL_OUT_PRIME, SCL_OUT_SEC, SDA_OUT_PRIME, SDA_OUT_SEC, TX_OUT_PRIME, TX_OUT_SEC, VREF
  - USB_ISP_Feather signal nets out: /Okapi_3/RST_TRIG, ALIVE_LED, DTR, FEATHER_CTS, FEATHER_EN, FEATHER_GPIO, FEATHER_RTS, LED1, LED2, LED3, LOG_INT, MISO, MOSI, MOSI_BUF, RST, RX, SCK, SCK_BUF, SCL_FEATHER, SDA_EXT, SDA_FEATHER, SDA_OB, TX, WD_DONE

### J_ten_indicators

D with an Indicators page: ten pages, every block on a page named for what it does. Page 1 is the root sheet (178 x 80 mm) in every candidate.

| # | Page | Blocks | Parts | Ink, packed (mm) | Fit | Local labels split | Nets out all / signal | Verdict |
|---|---|---|---|---|---|---|---|---|
| 2 | Power_Input | S3LR_T S1M_T S1M_B S1R_T | D1 D2 D3 D8 D9 J5 J6 J7 J8 L4 Q1 Q2 Q5 Q6 Q8 S5 U4 U5 U6 U7 U9 U37 + 18 R, 10 C | 249 x 210, slack 25 x 1 (S3LR_T at 0,0; S1R_T at 75,0; S1M_B at 0,113; S1M_T at 144,113) | yes | 5V_LP | 16 / 9 | terminals, start button, BQ2980 protection, LT3652 charger, V_PRIME selection, TPS797 core LDO |
| 3 | Power_Rails | S1L_T S1L_B | L1 L2 L3 LOGO1 Q7 U1 U2 U3 U13 U39 + 10 R, 9 C | 179 x 183, slack 95 x 28 (S1L_B at 0,0; S1L_T at 0,108) | yes | 5V_LP | 12 / 5 | 5V_LP, 3V3_AUX, 5V_AUX regulators and POWER_EN |
| 4 | Microcontroller | S6 | IC1 S4 U41 XTAL1 + 8 R, 4 C | 270 x 114, slack 4 x 97 | yes | – | 53 / 48 | ATmega1284 and MCP23018 |
| 5 | Indicators | S3LAD S3LR_B | D5 D10 D11 D12 D13 D14 D16 D17 D18 S3 U45 + 13 R, 0 C | 223 x 83, slack 51 x 128 (S3LAD at 0,0; S3LR_B at 140,0) | yes | – | 9 / 7 | PCA9634 ladder, D5 status LED, S3 log button |
| 6 | Cell_Module | S3UL S3SD | D7 F2 J9 S6 S7 SD1 U35 USB2 + 6 R, 1 C | 268 x 159, slack 6 x 52 (S3UL at 0,0; S3SD at 207,0) | yes | RST_TRIG | 22 / 16 | B-series SoM, its USB, buttons, FRAM; SD card |
| 7 | Level_Shifters | S4 | U24 U25 U26 U27 U28 U29 U34 U36 U42 + 2 R, 6 C | 231 x 158, slack 43 x 53 | yes | – | 49 / 41 | one theme |
| 8 | Sensors | S5 | BT1 D6 JP6 JP7 RTC1 U30 U31 U32 U33 U38 U43 U44 + 4 R, 13 C | 264 x 165, slack 10 x 46 | yes | – | 25 / 17 | one theme |
| 9 | Sensor_Ports | S2L_T S2L_B S2R_B S3TERM | J1 J2 J3 J4 JP1 JP2 JP3 JP4 S1 S2 U11 U12 U14 U15 U16 U17 U18 U19 U20 U21 U22 U40 U$1 U$2 + 12 R, 2 C | 231 x 169, slack 43 x 42 (S2R_B at 0,0; S2L_B at 122,0; S2L_T at 0,52; S3TERM at 165,52) | yes | – | 38 / 29 | switched port power, rail switches and logic, screw terminals |
| 10 | USB_ISP_Feather | S2R_T S3MID S1R_B | D4 F1 H1 H2 H3 ISP1 J10 JP5 JP8 MS1 Q3 Q4 U8 U10 U23 + 14 R, 5 C | 256 x 178, slack 18 x 33 (S2R_T at 0,0; S3MID at 175,0; S1R_B at 0,104) | yes | RST_TRIG | 27 / 20 | USB-C, FT231X, ICSP, Feather socket and the timer that gates FEATHER_BAT |

Totals: 10 pages; nets spanning two or more pages 101 (all) / 86 (signal); local labels split 2 (5V_LP@Okapi_1, RST_TRIG@Okapi_3); pages that do not fit 0; wires cut 0 (every block boundary is wire-clean and pin-clean by pages_regions.py).
  - Power_Input signal nets out: /Okapi_1/5V_LP, BMS_CTR, MPPT_CHRG, MPPT_FAULT, PG_LDO, V_BETA_SENSE, V_LI_SENSE, V_PRIME_SENSE, V_SOLAR_SENSE
  - Power_Rails signal nets out: /Okapi_1/5V_LP, 3V3_AUX_PG, LBI, POWER_EN, V_HP_SYNC
  - Microcontroller signal nets out: 3V3_AUX_PG, ADC_EXT_ALERT, ALIVE_LED, BMS_CTR, BUS_LOGIC_EN_PRIME, BUS_LOGIC_EN_SEC, C0, C1, CSA_~{ALERT}, CS_EXT, DTR, EN_BUS_PRIME, EN_BUS_SEC, FAULT_PRIME, FAULT_SEC, FEATHER_CTS, FEATHER_EN, FEATHER_GPIO, FEATHER_RTS, GPIO_0, GPIO_1, GPIO_2, GPIO_3, LBI, LED1, LED2, LED3, LOG_INT, MISO, MOSI, MPPT_CHRG, MPPT_FAULT, PG_LDO, RST, RTC_INT, RX, RX_EXT, SCK, SCL, SDA, SDA_CTRL, SDA_OB, SD_CD, SD_CS, TX, TX_EXT, V_HP_SYNC, ~{LED_EN}
  - Indicators signal nets out: LED1, LED2, LED3, LOG_INT, SCL, SDA_OB, ~{LED_EN}
  - Cell_Module signal nets out: /Okapi_3/RST_TRIG, FEATHER_CTS, FEATHER_GPIO, FEATHER_RTS, MISO, MOSI_BUF, RX, SCK_BUF, SCL, SCL_FEATHER, SDA_FEATHER, SDA_OB, SD_CD, SD_CS_BUF, TX, WD_DONE
  - Level_Shifters signal nets out: BUS_LOGIC_EN_PRIME, BUS_LOGIC_EN_SEC, CS_EXT, CS_OUT, GPIO_0, GPIO_0_OUT, GPIO_1, GPIO_1_OUT, GPIO_2, GPIO_2_OUT, GPIO_3, GPIO_3_OUT, MISO, MISO_OUT, MOSI, MOSI_BUF, MOSI_OUT, RX_EXT, RX_OUT_PRIME, RX_OUT_SEC, SCK, SCK_BUF, SCK_OUT, SCL, SCL_5V, SCL_FEATHER, SCL_OUT_PRIME, SCL_OUT_SEC, SDA, SDA_5V, SDA_CTRL, SDA_EXT, SDA_FEATHER, SDA_OB, SDA_OUT_PRIME, SDA_OUT_SEC, SD_CS, SD_CS_BUF, TX_EXT, TX_OUT_PRIME, TX_OUT_SEC
  - Sensors signal nets out: ADC_0, ADC_1, ADC_2, ADC_3, ADC_EXT_ALERT, CSA_~{ALERT}, DAC_OUT, RTC_INT, SCL, SCL_5V, SDA_5V, SDA_OB, VREF, V_BETA_SENSE, V_LI_SENSE, V_PRIME_SENSE, V_SOLAR_SENSE
  - Sensor_Ports signal nets out: ADC_0, ADC_1, ADC_2, ADC_3, C0, C1, CS_OUT, DAC_OUT, EN_BUS_PRIME, EN_BUS_SEC, FAULT_PRIME, FAULT_SEC, GPIO_0_OUT, GPIO_1_OUT, GPIO_2_OUT, GPIO_3_OUT, MISO_OUT, MOSI_OUT, POWER_EN, RX_OUT_PRIME, RX_OUT_SEC, SCK_OUT, SCL_OUT_PRIME, SCL_OUT_SEC, SDA_OUT_PRIME, SDA_OUT_SEC, TX_OUT_PRIME, TX_OUT_SEC, VREF
  - USB_ISP_Feather signal nets out: /Okapi_3/RST_TRIG, ALIVE_LED, DTR, FEATHER_CTS, FEATHER_EN, FEATHER_GPIO, FEATHER_RTS, MISO, MOSI, MOSI_BUF, RST, RX, SCK, SCK_BUF, SCL_FEATHER, SDA_EXT, SDA_FEATHER, SDA_OB, TX, WD_DONE

### F_eight

Fewest pages tried: E with Aux_Rails pushed into Sensor_Ports and the ladder moved to the Cell_Module page. Page 1 is the root sheet (178 x 80 mm) in every candidate.

| # | Page | Blocks | Parts | Ink, packed (mm) | Fit | Local labels split | Nets out all / signal | Verdict |
|---|---|---|---|---|---|---|---|---|
| 2 | Power_Input | S3LR_T S1M_T S1M_B | D1 D2 D3 J5 J6 J7 J8 L4 Q1 Q2 Q8 S5 U4 U5 + 16 R, 5 C | 180 x 167, slack 94 x 44 (S1M_T at 0,0; S3LR_T at 108,0; S1M_B at 0,70) | yes | – | 11 / 6 | terminals, start button, protection, charger |
| 3 | Core_Supply | S1L_T S1R_T | D8 D9 L1 LOGO1 Q5 Q6 U1 U6 U7 U9 U37 U39 + 5 R, 7 C | 151 x 188, slack 123 x 23 (S1L_T at 0,0; S1R_T at 0,78) | yes | – | 11 / 2 | the 3V3_CORE chain |
| 4 | Microcontroller | S6 S3LR_B | D5 IC1 S3 S4 U41 XTAL1 + 12 R, 4 C | 270 x 183, slack 4 x 28 (S6 at 0,0; S3LR_B at 0,117) | yes | – | 49 / 44 | ATmega1284, MCP23018, status LED, log button |
| 5 | Cell_Module | S3UL S3SD S3LAD | D7 D10 D11 D12 D13 D14 D16 D17 D18 F2 J9 S6 S7 SD1 U35 U45 USB2 + 15 R, 1 C | row 408 x 159, column 204 x 296 | NO | RST_TRIG | 23 / 17 | B-series SoM, SD card, and a PCA9634 ladder that has nothing to do with it |
| 6 | Level_Shifters | S4 | U24 U25 U26 U27 U28 U29 U34 U36 U42 + 2 R, 6 C | 231 x 158, slack 43 x 53 | yes | – | 49 / 41 | one theme |
| 7 | Sensors | S5 | BT1 D6 JP6 JP7 RTC1 U30 U31 U32 U33 U38 U43 U44 + 4 R, 13 C | 264 x 165, slack 10 x 46 | yes | – | 25 / 17 | one theme |
| 8 | Rails_and_Ports | S1L_B S2L_T S2L_B S2R_B S3TERM | J1 J2 J3 J4 JP1 JP2 JP3 JP4 L2 L3 Q7 S1 S2 U2 U3 U11 U12 U13 U14 U15 U16 U17 U18 U19 U20 U21 U22 U40 U$1 U$2 + 19 R, 9 C | row 628 x 117, column 179 x 401 | NO | – | 39 / 31 | aux regulators, every power switch, and the terminals: too much |
| 9 | USB_ISP_Feather | S2R_T S3MID S1R_B | D4 F1 H1 H2 H3 ISP1 J10 JP5 JP8 MS1 Q3 Q4 U8 U10 U23 + 14 R, 5 C | 256 x 178, slack 18 x 33 (S2R_T at 0,0; S3MID at 175,0; S1R_B at 0,104) | yes | RST_TRIG | 27 / 20 | USB-C, FT231X, ICSP, Feather socket and its timer |

Totals: 9 pages; nets spanning two or more pages 95 (all) / 80 (signal); local labels split 1 (RST_TRIG@Okapi_3); pages that do not fit 2; wires cut 0 (every block boundary is wire-clean and pin-clean by pages_regions.py).
  - Power_Input signal nets out: BMS_CTR, MPPT_CHRG, MPPT_FAULT, V_LI_SENSE, V_PRIME_SENSE, V_SOLAR_SENSE
  - Core_Supply signal nets out: PG_LDO, V_BETA_SENSE
  - Microcontroller signal nets out: 3V3_AUX_PG, ADC_EXT_ALERT, ALIVE_LED, BMS_CTR, BUS_LOGIC_EN_PRIME, BUS_LOGIC_EN_SEC, C0, C1, CSA_~{ALERT}, CS_EXT, DTR, EN_BUS_PRIME, EN_BUS_SEC, FAULT_PRIME, FAULT_SEC, FEATHER_CTS, FEATHER_EN, FEATHER_GPIO, FEATHER_RTS, GPIO_0, GPIO_1, GPIO_2, GPIO_3, LBI, MISO, MOSI, MPPT_CHRG, MPPT_FAULT, PG_LDO, RST, RTC_INT, RX, RX_EXT, SCK, SCL, SDA, SDA_CTRL, SDA_OB, SD_CD, SD_CS, TX, TX_EXT, V_HP_SYNC, ~{LED_EN}
  - Cell_Module signal nets out: /Okapi_3/RST_TRIG, FEATHER_CTS, FEATHER_GPIO, FEATHER_RTS, MISO, MOSI_BUF, RX, SCK_BUF, SCL, SCL_FEATHER, SDA_FEATHER, SDA_OB, SD_CD, SD_CS_BUF, TX, WD_DONE, ~{LED_EN}
  - Level_Shifters signal nets out: BUS_LOGIC_EN_PRIME, BUS_LOGIC_EN_SEC, CS_EXT, CS_OUT, GPIO_0, GPIO_0_OUT, GPIO_1, GPIO_1_OUT, GPIO_2, GPIO_2_OUT, GPIO_3, GPIO_3_OUT, MISO, MISO_OUT, MOSI, MOSI_BUF, MOSI_OUT, RX_EXT, RX_OUT_PRIME, RX_OUT_SEC, SCK, SCK_BUF, SCK_OUT, SCL, SCL_5V, SCL_FEATHER, SCL_OUT_PRIME, SCL_OUT_SEC, SDA, SDA_5V, SDA_CTRL, SDA_EXT, SDA_FEATHER, SDA_OB, SDA_OUT_PRIME, SDA_OUT_SEC, SD_CS, SD_CS_BUF, TX_EXT, TX_OUT_PRIME, TX_OUT_SEC
  - Sensors signal nets out: ADC_0, ADC_1, ADC_2, ADC_3, ADC_EXT_ALERT, CSA_~{ALERT}, DAC_OUT, RTC_INT, SCL, SCL_5V, SDA_5V, SDA_OB, VREF, V_BETA_SENSE, V_LI_SENSE, V_PRIME_SENSE, V_SOLAR_SENSE
  - Rails_and_Ports signal nets out: 3V3_AUX_PG, ADC_0, ADC_1, ADC_2, ADC_3, C0, C1, CS_OUT, DAC_OUT, EN_BUS_PRIME, EN_BUS_SEC, FAULT_PRIME, FAULT_SEC, GPIO_0_OUT, GPIO_1_OUT, GPIO_2_OUT, GPIO_3_OUT, LBI, MISO_OUT, MOSI_OUT, RX_OUT_PRIME, RX_OUT_SEC, SCK_OUT, SCL_OUT_PRIME, SCL_OUT_SEC, SDA_OUT_PRIME, SDA_OUT_SEC, TX_OUT_PRIME, TX_OUT_SEC, VREF, V_HP_SYNC
  - USB_ISP_Feather signal nets out: /Okapi_3/RST_TRIG, ALIVE_LED, DTR, FEATHER_CTS, FEATHER_EN, FEATHER_GPIO, FEATHER_RTS, MISO, MOSI, MOSI_BUF, RST, RX, SCK, SCK_BUF, SCL_FEATHER, SDA_EXT, SDA_FEATHER, SDA_OB, TX, WD_DONE

### Comparison

| Candidate | Pages | Spanning nets, all | Spanning nets, signal | Local labels split | Pages that do not fit |
|---|---|---|---|---|---|
| A_baseline | 10 | 104 | 85 | 2 | 0 |
| B_corrected | 10 | 96 | 81 | 2 | 2 |
| C_thematic | 10 | 97 | 81 | 2 | 1 |
| D_nine | 9 | 96 | 81 | 2 | 1 |
| E_core_supply | 10 | 94 | 79 | 1 | 1 |
| G_indicators | 11 | 102 | 86 | 2 | 0 |
| H_core_indicators | 11 | 99 | 84 | 1 | 0 |
| C2_stray_on_usb | 10 | 101 | 85 | 2 | 0 |
| I_nine_fit | 9 | 100 | 85 | 2 | 1 |
| J_ten_indicators | 10 | 101 | 86 | 2 | 0 |
| F_eight | 9 | 95 | 80 | 1 | 2 |

### As drawn (the 105 mm SDA note kept on one line)


| Candidate | Pages | Spanning nets, all | Spanning nets, signal | Local labels split | Pages that do not fit |
|---|---|---|---|---|---|
| A_baseline | 10 | 104 | 85 | 2 | 1 |
| B_corrected | 10 | 96 | 81 | 2 | 2 |
| C_thematic | 10 | 97 | 81 | 2 | 2 |
| D_nine | 9 | 96 | 81 | 2 | 2 |
| E_core_supply | 10 | 94 | 79 | 1 | 2 |
| G_indicators | 11 | 102 | 86 | 2 | 1 |
| H_core_indicators | 11 | 99 | 84 | 1 | 1 |
| C2_stray_on_usb | 10 | 101 | 85 | 2 | 1 |
| I_nine_fit | 9 | 100 | 85 | 2 | 1 |
| J_ten_indicators | 10 | 101 | 86 | 2 | 1 |
| F_eight | 9 | 95 | 80 | 1 | 3 |

Pages whose fit changes between the two: every page that holds S3MID beside another block (USB_ISP, USB_ISP_Feather, and the baseline's Connectors page) fits only with the note re-wrapped; a Connectors page of S3TERM + S3MID alone fits either way.

## Recommendation: H, eleven pages

Take `H_core_indicators`. Every page is one function a reader would name, nothing is a stray,
every page fits with room (the tightest is USB_ISP_Feather at 256 x 178 mm, 18 x 33 mm of
slack), and it is the only fitting layout with a single local-label split: `5V_LP` stays local
because the TLV61220 that makes it and the TLV3691/TPS2105 that use it share a page. Its 99
spanning nets (84 signal) are the fewest of any layout that fits; the baseline spans 104 (85).
In page order, which follows the signal path from the terminals to the field ports:

1. Root.
2. Power_Input: J5–J8 terminals, S5 start button, U5 BQ2980 with Q1/Q2, U4 LT3652 charger with
   the D1–R74 solar chain and Q8 (S3LR_T, S1M_T, S1M_B; 180 x 167 mm).
3. Core_Supply: U39 MIC94094, U1 TLV61220 5V_LP boost, U37 TLV3691, U6 TPS2105, U7 LTC4412 with
   Q5, U9 TPS797 3V3_CORE LDO, Q6 (S1L_T, S1R_T; 151 x 188 mm, stacked).
4. Aux_Rails: U2 TPS6282 3V3_AUX, U3 TPS61032 5V_AUX, U13/Q7 POWER_EN, and the V_HP source
   switches U21/U22 with their U16/U40 C0/C1 logic and the VDIV jumpers (S1L_B, S2L_B, S2R_B;
   212 x 158 mm). U21 switches V_PRIME and U22 V_BETA onto V_HP, which is U3's input.
5. Microcontroller: IC1 ATmega1284, U41 MCP23018, S4 reset button (S6 as it is; 270 x 114 mm).
6. Indicators: U45 PCA9634 with D10–D18 and the address resistors, D5 status LED, S3 log button,
   under Bobby's own "Indicators" heading (S3LAD, S3LR_B; 223 x 83 mm, the one small page).
7. Cell_Module: J9 B-series SoM, USB2, F2, S6/S7, D7, U35 FRAM, SD1 (S3UL, S3SD; 268 x 159 mm).
8. Level_Shifters: Okapi_4 as it is (231 x 158 mm).
9. Sensors: Okapi_5 as it is (264 x 165 mm).
10. Sensor_Ports: U17–U20 MIC2544 with JP1–JP4, S1/S2, U11/U12/U14/U15, and the J1–J4 screw
    terminals they feed (S2L_T, S3TERM; 231 x 117 mm).
11. USB_ISP_Feather: J10 USB-C, F1, U23 FT231X with D4, ISP1 ICSP header, MS1 Feather socket,
    JP5, Q4, H1–H3, and U8 TPL5111 with JP8, Q3 and U10, the timer that gates FEATHER_BAT to the
    socket (S2R_T, S3MID, S1R_B; 256 x 178 mm). Bobby's heading on Okapi_2 reads "USB & ISP".

Net changes: `RST_TRIG` becomes a global label (one instance on Cell_Module, two on
USB_ISP_Feather); nothing else changes. `5V_LP` stays local. No wire is cut.

Text edits that the move needs, beyond the block moves: (1) re-wrap the 86-character note
"Jump SDA channels together, prevents using occupied addresses on the external I2C port" onto
three lines, or move it as its own item: on one line it prints 105 mm wide and hangs off the
page wherever its block sits beside another (the as-drawn table shows the baseline's own
Connectors page failing on it); (2) move "Select address" (anchored at 205.7, 139.7 in the SoM
block) with the ladder; (3) "Remove LBI pullup??" prints 36 mm to the right of the Aux_Rails
components and stays with them, which the packing already allows for.

Costs, stated plainly: eleven pages against the baseline's ten; three pages under half full
(Core_Supply 151 x 188, Indicators 223 x 83, Aux_Rails 212 x 158, each one named function);
Aux_Rails pulls U21/U22/U16/U40 off Okapi_2, where Bobby drew them under the port switches, and
puts them with the regulators they feed.

If ten pages matter more than the three things H buys, take `J_ten_indicators`: the same pages
with Core_Supply and Aux_Rails folded back into Power_Input (terminals, protection, charger,
selector, core LDO) and Power_Rails (Okapi_1's left column), and U21/U22 with the port switches.
It keeps the `5V_LP` split (two global labels), spans 101 nets (86 signal), and its Power_Input
packs at 249 x 210 mm, one millimeter of vertical slack with the blocks re-stacked (S3LR_T and
S1R_T above, S1M_B and S1M_T below); that page wants a render before anyone commits to it.
`G_indicators` (the Feather timer left on a Power_Select page) is the same count of pages as H
with one stray, and is dominated by it.

Nine pages (`D_nine`, `I_nine_fit`, `F_eight`) are out: each needs the MCU page to hold both the
ladder and the status LED (270 x 274 mm, no packing fits) or a four-block USB page (row 449 mm),
and `F_eight` merges rails, switches and terminals into one 602 mm row.

## What the baseline gets wrong

- `IO_Expansion` is the microcontroller page: IC1, the ATmega1284 that the FT231X, the ICSP
  header, the enables, the LEDs and the log button all talk to, sits on Okapi_6. `Processor` is
  the Particle B-series cellular module. Both names mislead a reader looking for the MCU.
- `Connectors` is a leftover: J5–J8 are the battery, solar and V_PRIME terminals and belong
  with the input power; S3 and D5 are the log button and status LED driven by the ATmega; MS1
  and ISP1 are the Feather socket and the programming header. Nothing on that page is "the
  connectors" as a function.
- `USB_Programming` carries U40 and the VDIV jumpers, whose nets (C0, C1, POWER_EN) belong to
  the U21/U22 switches on `Sensor_Power`.
- `Power_Input` holds two themes (input chain and V_PRIME/V_CORE selection) plus the Feather
  sleep timer, which talks only to the SoM (WD_DONE), the MCP23018 (FEATHER_EN) and the Feather
  socket (FEATHER_BAT). It packs at 259 x 210 mm, one millimeter of slack, and only with the
  right column's two halves separated and re-stacked, not "moved 6 ticks left".
- Three of its "verified" cut lines pass through symbol bodies: R74 on Okapi_1 (x=170), R18 on
  Okapi_3 (y=176) and U40 on Okapi_2 (x=190). The wire test cannot see a cut through a part;
  the pin test in `pages_regions.py` can, and the corrected lines are x=148–170 notch at
  y=116–128 for the solar chain, y=190 for the ladder, x=172 for U40.
- The 105 mm SDA note on Okapi_3 was not in any ink estimate; as drawn it pushes the baseline's
  own Connectors page to 368 mm wide.

---

**Summary.** The Okapi schematic can go onto eleven US Letter pages with every page one named
function, no wire cut, and one local label made global: terminals-protection-charger, the
3V3_CORE chain, the auxiliary rails with their V_HP source switches, the ATmega1284, the
indicators, the cellular module with its SD card, the level shifters, the on-board sensors, the
switched field ports with their screw terminals, and USB/ICSP/Feather with the timer that feeds
the socket. That layout (H) spans 99 nets across pages against the baseline's 104, fits every
page with at least 18 x 33 mm to spare, and keeps `5V_LP` local. It needs one note re-wrapped
and one note moved with its block. The baseline's ten pages all fit too, but two of its page
names point at the wrong chips, its Connectors page is a leftover of four unrelated things, its
power page packs with one millimeter to spare, and three of its cut lines run through R74, R18
and U40. The ten-page fallback J keeps H's names but folds the supply pages together at the
cost of the `5V_LP` split and a one-millimeter power page.

# Part problems: verification against primary sources

Status: COMPLETE

Verification of the table "Part problems on the boards" in `README.md` (this directory), 2026-11-11. Each row cites its sources with the date fetched. Anything not confirmed is marked UNVERIFIED.

## Sources checked (log, dead ends included)

- 2026-11-11 local: `Project-Okapi/Hardware/Okapi_BoM.csv` (only commit bb041bd, 2021-07-05 "Okapi naming"; 111 data rows). This is the 2021 BoM.
- 2026-11-11 local: `Project-Okapi/Hardware/Okapi_2024-11-02.zip`, member `CAMOutputs/Assembly/Okapi.txt` (the BoM the semiconductors survey read).
- 2026-11-11 local: `Project-Okapi/Hardware/KiCAD-10import/*.kicad_sch` (v0.8), symbol properties extracted per instance with a paren-balanced parser.
- 2026-11-11 local: `Project-Margay/Hardware/KiCAD/*.kicad_sch` and `Project-Margay/Production/Margay_BoM_3v0_-_2026-11-04.csv`. (`Project-Margay/Hardware/KiCAD-v10` holds only `Margay.kicad_prl` and backups: dead end.)

## Board facts (from the files, 2026-11-11)

| Board | Ref | MPN in file | Footprint |
|---|---|---|---|
| Okapi v0.8 | BT1 | Linx BAT-HLD-012-SMT (DK BAT-HLD-012-SMT-ND), value BATTERY_COIN12MM | nw-cold-silicon:LINX_BAT-HLD-012-SMT |
| Margay 3v0 | BT1 | Linx BAT-HLD-012-SMT, same | same |
| Okapi v0.8 | S1, S2 | C&K PCM12SMTR (DK 401-2016-1-ND), sheet Sensor_Ports | nw-cold-silicon:PCM12 |
| Okapi v0.8 | J8 | JST S2B-PH-SM4-TB(LF)(SN) (DK 455-1749-1-ND), sheet Power_Input | nw-cold-silicon:JST-2-SMD |
| Okapi v0.8 | J5, J6, J7 | On Shore OSTVN02A150 | 1X02_2.54_SCREWTERM |
| Okapi v0.8 | J1, J4 | On Shore OSTVN08A150 | 1X08_SCREW |
| Okapi v0.8 | J2 | On Shore OSTVN10A150 | 1X10_SCREW |
| Okapi v0.8 | J3 | On Shore OSTVN04A150 | 1X04_SCREW |
| Margay 3v0 | J2 | On Shore OSTVN10A150 (DK ED10567-ND) | 1X10_SCREW |
| Margay 3v0 | J3 | On Shore OSTVN06A150 (DK ED10565-ND) | 1X06_SCREW |
| Okapi v0.8 | U23 | FTDI FT231XQ-R (DK 768-1128-1-ND) | QFN20 |
| Margay 3v0 | U2 | FTDI FT231XQ-R (DK 768-1128-1-ND) | QFN20 |
| Okapi v0.8 | U4 | LT3652EDD#PBF | DFN_12_3X3 |
| Okapi v0.8 | U38 | MLX90393SLW-ABA-011-RE | QFN16_3X3 |
| Okapi v0.8 | U44 | VEML6030-GS15 | VEML6030 |

Margay uses the same FTDI part as Okapi: FT231XQ-R.

## Row 9: 2021 Okapi BoM errors (verified from the files)

Source: `Project-Okapi/Hardware/Okapi_BoM.csv` (2021-07-05). Size codes used: Yageo RC0402/RC0603 is the size in the MPN; Yageo Digi-Key numbers ending `LRCT` are 0402 and `HRCT` 0603 (pattern in this same file, for example `311-1.00MLRCT-ND` for RC0402FR-071ML); Samsung CL05 = 0402, CL10 = 0603; Murata GRM/GCM155 = 0402, 188 = 0603, 21 = 0805. Each "fixed in v0.8" entry is read from the v0.8 KiCad symbol properties.

| # | 2021 row (refs) | Field values | Error | In 2024 zip BoM | In v0.8 KiCad |
|---|---|---|---|---|---|
| 1 | U41 MCP23018QFN | MF `TI`, MPN `MCP23018T-E/MJ`, DK `MCP23018T-E/MJCT-ND` | Manufacturer wrong: Digi-Key lists the MPN under "Microchip Technology" (https://www.digikey.com/en/products/result?keywords=MCP23018T-E%2FMJ, fetched 2026-11-11) | still `TI` | **still `TI`** |
| 2 | R54 10k | package `R0402`, DK `311-10.0KHRCT-ND`, MPN `RC0603FR-0710KL` | MPN and DK number are 0603 on an 0402 footprint | not checked row by row | fixed (RC0402FR-0710KL, 311-10.0KLRCT-ND) |
| 3 | R24, R25, R41, R45, R46, R47, R52, R67 10k | package `R0402`, DK `311-10.0KHRCT-ND`, MPN `RC0603FR-0710KL` | same as row 2 (8 placements) | R45, R52: MPN changed to RC0402FR-0710KL but DK still `311-10.0KHRCT-ND` (0603) | fixed |
| 4 | R69 100k | package `R0603`, DK field `RC0402FR-071ML`, MPN `RC0603FR-07100KL` | DIGIKEY column holds a Yageo MPN, and that MPN is 1 MΩ 0402 | not checked | footprint now `R0402_0603`, MPN RC0402FR-07100KL, DK 311-100KLRCT-ND |
| 5 | R26–R29 | Value `287R`, Device `R-EU_232R0402`, MPN `RC0402FR-07232RL`, VALUE `232` | Value field (287 Ω) disagrees with MPN (232 Ω) | same | Value now `232` |
| 6 | R30–R33 | Value `287R`, Device `R-EU_453R0402`, MPN `RC0402FR-07453RL`, VALUE `453` | Value field (287 Ω) disagrees with MPN (453 Ω) | same | now 464 Ω, RC0402FR-07464RL (value change; reason not checked) |
| 7 | R37, R39 330 | package `R0402`, DK `311-330HRCT-ND`, MPN `RC0603FR-07330RL` | MPN and DK number 0603 on 0402 footprint | same | fixed (RC0402FR-07330RL) |
| 8 | R36, R38, R40, R42, R43, R44 330 | package `R0402`, DK `311-330LRCT-ND` (0402), MPN `RC0603FR-07330RL` | MPN 0603 disagrees with footprint and with its own DK number | same | fixed |
| 9 | C42 1uF | Device `C-EU0.1UFC0402`, package `C0402`, MPN Samsung `CL10B105MO8NNWC` | MPN is 0603 (CL10) on 0402; device name says 0.1 µF | same | now CL05A105KA5NQNC (0402) |
| 10 | C40, C41 12pF | package `C0402`, MPN Samsung `CL10C120JB8NNNC` | MPN is 0603 (CL10) on 0402. A second 12 pF row (C23, C24) uses TDK CGA2B2C0G1H120J050BA (0402) | same | now TDK CGA2B2C0G1H120J050BA |
| 11 | C6 68pF | MPN `8.85012E+11` | Würth MPN mangled by a spreadsheet into floating point (true MPN `885012005060`, from the 2024 BoM and v0.8) | fixed | fixed |
| 12 | D8 BAT54C | MPN `BAT54CLT1G` in column `MFP`; `MPN` column empty | MPN in the wrong column | not checked | MPN column filled |
| 13 | J8 (JST battery) and J8 (CONN_16FEMALE, Sullins) | two rows share designator J8 | duplicate reference designator | not checked | J8 is the JST connector only (Feather headers not checked) |

Legacy maker names that are not errors in the part but are out of date: `Atmel` (ATmega1284P, now Microchip), `LT` (LT3652, LTC4412; now Analog Devices), `Maxim` (DS3231M; now Analog Devices), `Fairchild` (FDN360P; now onsemi). Ownership changes are from memory, UNVERIFIED this session. The TXC crystal row (XTAL1 7A-8.000MAAE-T) is already replaced (README, Project-Okapi 47a944d, not re-checked here).

Not errors on inspection: GRT155/GCM155 0402, GRM188 0603, GRM21B/GRM219 0805 match their footprints; Stackpole RMCF0603 and Panasonic ERJ-3 (0603) on R0603 match. R10 Rohm `PMR10EZPFV3L00` on R0805 is correct: Digi-Key lists it as "0805 (2012 Metric)", "3 mOhms", Active, 80,963 available (https://www.digikey.com/en/products/result?keywords=PMR10EZPFV3L00, fetched 2026-11-11).

Note for the issue: U38 in the 2021 BoM is a TS5A21366 analog switch; in v0.8 U38 is the MLX90393. Refer to parts by MPN in issues, not only by designator.

## Row 1: U38 MLX90393SLW (Okapi): VERIFIED, one correction on the package name

- Melexis datasheet MLX90393, REVISION 012 – NOV 18, 2025, section 4 "Ordering Information" (https://www.melexis.com/-/media/files/documents/datasheets/mlx90393-datasheet-melexis.pdf, fetched 2026-11-11 with curl; the documentation landing page returned HTTP 403). Quoted: "Temperature Code: S: from -20°C to 85°C, E: from -40°C to 85°C"; "Package Code: "LW" for QFN-16 3x3x1mm package with wettable flanks"; table rows "MLX90393 S (-20°C to 85°C) LW ABA-011 RE I2C address = 00011xx" and "MLX90393 E (-40°C to 85°C) LW ABA-011 RE I2C address = 00011xx". Electrical table: "Operating temperature range [S code] -20 25 85 °C", "[E code] -40 25 85 °C". The datasheet's own ordering example is "MLX90393ELW-ABA-011-RE".
- The E grade exists in the same LW package with the same option code ABA-011, hence the same I2C address (00011xx, last two bits from A0/A1). The drop-in MPN is **MLX90393ELW-ABA-011-RE**.
- Digi-Key, search for MLX90393ELW-ABA-011-RE (https://www.digikey.com/en/products/result?keywords=MLX90393ELW-ABA-011-RE, fetched 2026-11-11): Digi-Key numbers MLX90393ELW-ABA-011-RECT-ND (cut tape), -RETR-ND (tape and reel), -REDKR-ND (Digi-Reel); "24,522 in stock"; Active; Operating Temperature "-40°C to 85°C"; Package/Case "16-VFQFN Exposed Pad"; Supplier Device Package "16-QFN (3x3)"; $2.46000 at quantity 1, cut tape.
- Digi-Key, MLX90393SLW-ABA-011-RE (https://www.digikey.com/en/products/result?keywords=MLX90393SLW-ABA-011-RE, fetched 2026-11-11): "In-Stock: 5,698"; Active; "-20°C ~ 85°C"; "16-VFQFN Exposed Pad". The current part is active, not obsolete.
- Correction to the task brief: SLW is not UQFN-16. Melexis calls LW "QFN-16 3x3x1mm package with wettable flanks"; Digi-Key lists 16-VFQFN, 16-QFN (3x3). This matches the v0.8 footprint `QFN16_3X3`.

## Row 2: U44 VEML6030 (Okapi): VERIFIED; a −40 °C Vishay part exists but is not a drop-in

- Vishay VEML6030 datasheet, Rev. 1.8, 28-Nov-2024, Document Number 84366 (https://www.vishay.com/docs/84366/veml6030.pdf, fetched 2026-11-11). Absolute maximum ratings: "Ambient temperature range Tamb -25 +85 °C"; "Storage temperature range Tstg -25 +85 °C". Package "2 x 2 x 0.87" mm. Pins in the block diagram: 2 SDA, 3 INT, 4 ADDR, 5 SCL (pins 1 and 6 not labeled in the extracted text; UNVERIFIED which is GND and which VDD).
- Note beyond the survey: the **storage** range is also −25 °C, so a powered-off logger at −40 °C is outside the rating too.
- Digi-Key VEML6030-GS15 (https://www.digikey.com/en/products/result?keywords=VEML6030-GS15, fetched 2026-11-11): VEML6030-GS15CT-ND; "In-Stock: 17,592"; Active; "-25°C ~ 85°C"; 6-SMD, No Lead.
- Same family, checked and also −25 °C (Vishay datasheets fetched 2026-11-11): VEML7700 (Rev. 1.8, doc 84286, "Operation temperature range -25 +85 °C", 6.8 x 2.35 x 3.0 mm); VEML6035 (Rev. 1.3, doc 84889, "-25 +85 °C", 2.0 x 2.0 x 0.4 mm); VEML3235 (Rev. 1.6, doc 80131, "-25 +85 °C", 2 x 2 x 0.87 mm, the same body size as VEML6030). None of these is a cold fix.

Candidates rated −40 °C (none is a footprint drop-in):

| Candidate | Rating (source) | Package | Address | Digi-Key (fetched 2026-11-11) | Difference from VEML6030 |
|---|---|---|---|---|---|
| Vishay VEML6031X00 | "Operation temperature range Tamb -40 +110 °C"; "Storage temperature range Tstg -40 +110 °C"; AEC-Q100 (datasheet Rev. 1.4, 18-Dec-2025, doc 80007, https://www.vishay.com/docs/80007/veml6031x00.pdf) | 2.67 x 2.45 x 0.6 mm, 6 pins | fixed by ordering code: VEML6031X00 0x29, VEML60311X00 0x10 | 751-VEML6031X00CT-ND, "In-Stock: 5,468", Active, "-40°C ~ 110°C", Automotive, AEC-Q100 (https://www.digikey.com/en/products/detail/vishay-semiconductor-opto-division/VEML6031X00/14831974) | Larger body (new footprint). Pin numbering matches for 2 SDA, 3 INT, 5 SCL, 6 VDD, but pin 4 is GND, not ADDR. Register map compatibility with VEML6030 UNVERIFIED (expect firmware changes). Closest candidate. |
| TI OPT3001 (OPT3001DNPR) | "Operating Temperature Range: –40°C to +85°C" (SBOS681C, revised November 2017, https://www.ti.com/lit/ds/symlink/opt3001.pdf) | USON-6 2.00 x 2.00 mm | ADDR pin sets LSBs | 296-40474-1-ND, "In-Stock: 0", Active, "-40°C ~ 85°C", 6-USON (2x2) (https://www.digikey.com/en/products/detail/texas-instruments/OPT3001DNPR/5039362) | Same body size, different pinout (1 VDD, 2 ADDR, 3 GND, 4 SCL, 5 INT, 6 SDA), different registers. Out of stock at Digi-Key on the fetch date. |
| TI OPT4001 (OPT4001DTSR, SOT-5X3) | "Operating temperature range: –40°C to +85°C" (SBOS993A, revised December 2022, https://www.ti.com/lit/ds/symlink/opt4001.pdf) | SOT-5X3 (8), 1.9 x 2.1 x 0.6 mm | UNVERIFIED | 296-OPT4001DTSRCT-ND, 133 in stock, Active, "-40°C ~ 85°C", lead time 39 weeks (https://www.digikey.com/en/products/result?keywords=OPT4001DTSR) | New footprint and firmware. Interrupt pin only on the SOT-5X3 variant (datasheet). |

## Row 3: U4 LT3652EDD (Okapi): VERIFIED; the I grade is a same-package drop-in at Digi-Key

- LT3652 datasheet, revision code "3652fe" in the page footers (https://www.analog.com/media/en/technical-documentation/data-sheets/3652fe.pdf). Text read 2026-11-11 from a copy of that URL already downloaded into this session's scratchpad by another agent (my own curl to analog.com timed out twice, the second time in the background); the content is the Linear Technology datasheet with footer "www.linear.com/LT3652". Note 2, verbatim: "The LT3652EDD is guaranteed to meet performance specifications from 0°C to 125°C junction temperature. Specifications over the –40°C to 125°C operating junction temperature range are assured by design, characterization, and correlation with statistical process controls. The LT3652IDD specifications are guaranteed over the full –40°C to 125°C operating junction temperature range."
- Order Information table: "LT3652EDD#PBF LT3652EDD#TRPBF LFHT 12-Lead Plastic DFN 3mm × 3mm –40°C to 125°C" and "LT3652IDD#PBF LT3652IDD#TRPBF LFHT 12-Lead Plastic DFN 3mm × 3mm –40°C to 125°C". Same package, same marking.
- Digi-Key LT3652IDD#PBF (https://www.digikey.com/en/products/detail/analog-devices-inc/LT3652IDD-PBF/2181632, fetched 2026-11-11): "LT3652IDD#PBF-ND"; "In-Stock: 239"; Active; "-40°C ~ 125°C (TJ)"; 12-WFDFN Exposed Pad, tube; "$11.73000" at 1. LT3652IDD#TRPBF (product page 2181633): 0 in stock, "Check Lead Time" (search page https://www.digikey.com/en/products/result?keywords=LT3652IDD, fetched 2026-11-11).
- Digi-Key LT3652EDD#PBF (https://www.digikey.com/en/products/result?keywords=LT3652EDD%23PBF, fetched 2026-11-11): "505-LT3652EDD#PBF-ND"; 3,624 in stock; Active; $10.79000 at 1. Digi-Key lists both grades as "-40°C ~ 125°C (TJ)"; the difference is in what is tested, which only the datasheet note shows. The v0.8 schematic carries the older Digi-Key number `LT3652EDD#PBF-ND`.
- Not in the survey, relevant at −40 °C: the datasheet's NTC function suspends charging when "the voltage on this pin is above 1.36 (T < 0°C)". Whether Okapi uses the NTC pin was not checked.

## Row 4: BT1 Linx BAT-HLD-012-SMT (Okapi and Margay): VERIFIED; two −40 °C holders found, both need a new land pattern

Cell: CR1220 (Okapi `README.md` line 126 "CR1220 battery"; Margay `README.md` line 428 and `Production/Margay_BoM_3v0_board_-_2023-03-17.csv` "Panasonic CR1220 ... 12.5mm dia x 2.0mm"). The Margay README already recommends a Panasonic BR1225A (2.5 mm thick, −40 °C cell) below −30 °C.

- Digi-Key search `BAT-HLD-012` (https://www.digikey.com/en/products/result?keywords=BAT-HLD-012, fetched 2026-11-11): "BAT-HLD-012-SMT | Obsolete | 0"; "BAT-HLD-012-SMT-TR | Active | 1,518"; BAT-HLD-012-THM Obsolete; BAT-HLD-012-THM-TR Active, 0, "-30°C ~ 70°C".
- Digi-Key BAT-HLD-012-SMT-TR detail (https://www.digikey.com/en/products/detail/te-connectivity-linx/BAT-HLD-012-SMT-TR/5361776, fetched 2026-11-11): BAT-HLD-012-SMTCT-ND (cut tape), -SMTTR-ND, -SMTDKR-ND; "In-Stock: 1,518"; Active; Battery Series "1216, 1225"; "Coin, 12.0mm"; height "0.140" (3.55mm)"; operating temperature not listed on this page.
- TE product page (https://www.te.com/en/product-BAT-HLD-012-SMT-TR.html, fetched 2026-11-11): "Operating Temperature Range : -30 – 70 °C [ -22 – 158 °F ]"; "Battery Compatibility : CR1216 | CR1225"; "Contact Mating Area Plating Material : Nickel (Ni)"; "Battery Holder Material : Phosphor Bronze"; status "Active", with the notice "This product is not currently available". The TE product sheet mirror the connectors survey cited (https://pf.unikeyic.com/datasheet/19/37/96e0/193796e03fc17ac16bc0d09ad5e065dc.pdf, fetched 2026-11-11) gives the same −30 to 70 °C.
- TE/Linx drawing BAT-HLD-012-SMT-OTL rev B (TE datasheet link from Digi-Key, fetched 2026-11-11 via WebFetch, image-only text read by tesseract OCR): title "CR1216,1225 HOLDER OUTLINE"; part table "BAT-HLD-012-SMT BULK" and "BAT-HLD-012-SMT-TR TAPE & REEL" (the two are the same holder, different packing); revision B "ADDED PART NUMBER TABLE AND SECOND SHEET 23-JUL-18". No temperature on the drawing.
- Neither TE source names CR1220; it lists CR1216 and CR1225. The CR1220 sits between them in thickness; that it is held reliably is UNVERIFIED by TE.
- Current land pattern (`nw-cold-silicon/nw-cold-silicon.pretty/LINX_BAT-HLD-012-SMT.kicad_mod`): one 10.16 x 10.16 mm GND pad at the center (the cell's negative face sits on the PCB) and two 2.54 x 5.08 mm POWER pads at x = ±7.62 mm.

−40 °C candidates (Digi-Key, fetched 2026-11-11):

| Candidate | Rating (maker) | Digi-Key | Cell | Land pattern difference |
|---|---|---|---|---|
| MPD BC501SM | Drawing BC501SM rev M, 01/22/20 (https://memoryprotectiondevices.com/datasheets/BC501SM/BC501SM-datasheet.pdf): "OPERATING TEMPERATURE: -40°C TO +85°C"; "HOUSING: GLASS FILLED PPS"; "TERMINAL: 0.20mm PHOSPHOR BRONZE, GOLD PLATED OVER NICKEL"; title "COIN CELL HOLDER FOR CR1220" | BC501SM-ND, "In-Stock: 24,200", Active, "-40°C ~ 85°C", Battery Series "1220", height "0.157" (4.00mm)", $1.37000 (https://www.digikey.com/en/products/detail/mpd-memory-protection-devices/BC501SM/2439260) | CR1220 by name | Both contacts are tabs at the ends (neg. and pos. pads 3.80 mm wide, 11.82 mm inner span per the drawing's PCB layout) plus two Ø1.40 mm holes for locating pegs; no center pad. Body 17.83 x 15.06 mm. Needs a new footprint and two drilled holes. |
| MPD BHSD-1225-SM | Drawing BHSD-1225-SM rev F, 10/31/19 (https://www.memoryprotectiondevices.com/datasheets/BHSD-1225-SM/BHSD-1225-SM-datasheet.pdf): "Temperature range: -40°C to +280°C"; "Holder material- LCP Zenite"; "Contacts : Phosphor Bronze C5191, Gold Flash"; title "BASE, SURFACE MOUNT, CR1225 BATTERY" | BHSD-1225-SMCT-ND, "9,784", Active, "-40°C ~ 280°C", Battery Series "1225", height "0.190" (4.83mm)", $1.57000 (https://www.digikey.com/en/products/detail/mpd-memory-protection-devices/BHSD-1225-SM/4303956) | CR1225, which fits the BR1225A cold cell; holding a 2.0 mm CR1220 is UNVERIFIED | Two end pads 2.54 x 3.81 mm, 23.37 mm overall, optional adhesive area in the middle; no center pad. Larger than the Linx footprint (body 23.37 x 14.73 mm). |

Checked and not −40 °C, or not stated: Keystone 2894TR (36-2894CT-ND, 4,045, "1220", 2.69 mm; operating temperature not listed on Digi-Key, https://www.digikey.com/en/products/detail/keystone-electronics/2894TR/9921827), Keystone 1056TR (36-1056CT-ND, 15,869, 12.5 mm, "1220", 4.00 mm; not listed, https://www.digikey.com/en/products/detail/keystone-electronics/1056TR/2746328), Keystone 1072 (36-1072-ND; not listed, https://www.digikey.com/en/products/detail/keystone-electronics/1072/9921820). Keystone's all-metal retainers may have no plastic to limit them, but with no published rating they are UNVERIFIED. Adam Tech BH-44D-5/BH-44F-5 (−25 °C) and Assmann A-BAT-CH-C1-EA (−30 °C) per web-search snippets of Digi-Key pages, not opened (UNVERIFIED).

## Row 5: S1, S2 C&K PCM12SMTR (Okapi, sheet Sensor_Ports): VERIFIED from Digi-Key; maker datasheet not reached; one near-drop-in −40 °C switch found

- Digi-Key PCM12SMTR (https://www.digikey.com/en/products/detail/c-k/PCM12SMTR/1640112, fetched 2026-11-11): 401-2016-1-ND (cut tape), -2-ND, -6-ND; "In-Stock: 2,726"; "Obsolete"; "This product is no longer manufactured and will no longer be stocked once stock is depleted."; "-20°C ~ 85°C"; SPDT; "Surface Mount, Right Angle"; "300mA (DC)"; contact "Copper Alloy"; actuator "Polyamide (PA46), Nylon 4/6".
- Maker datasheet: the Littelfuse/C&K PCM series PDF linked from Digi-Key returned HTTP 403 to WebFetch and to curl; https://www.ckswitches.com/media/1424/pcm.pdf returned 403; a mirror at leocom.kr timed out. The −20 °C rating is therefore from Digi-Key (and, per web-search snippets, Farnell and RS), not from C&K's own document: maker figure UNVERIFIED. A search snippet reports an older ITT Cannon catalog figure of −10 °C, and a Digi-Key "Last Time Buy Date: 5/8/2026"; neither was opened (UNVERIFIED).
- Current land pattern (`nw-cold-silicon.pretty/PCM12.kicad_mod`): signal pads 1, 2, 3 at x = −2.25, +0.75, +2.25 mm (y = −1.8), 0.7 x 1.6 mm; two Ø0.9 mm non-plated holes at x = ±1.5 mm; four body pads 0.8 x 1.0 mm at x = ±3.65, y = ±0.965.

Candidates:

| Candidate | Rating | Digi-Key (fetched 2026-11-11) | Land pattern |
|---|---|---|---|
| Same Sky SLW-662712-15A-SMT-TR | Datasheet dated 05/13/2026 (https://www.sameskydevices.com/product/resource/slw-662712-15a-smt-tr.pdf): "operating temperature -40 85 °C"; contact phosphor bronze, silver plated; housing LCP; 1.5 mm actuator | 2223-SLW-662712-15A-SMT-TRCT-ND, "In-Stock: 5,400", Active, "-40°C ~ 85°C", SPDT, 300 mA DC (https://www.digikey.com/en/products/result?keywords=SLW-662712-15A-SMT-TR). Listed by Digi-Key as "Similar" to PCM12SMTR. | Recommended layout: terminals spaced 3.0 then 1.5 mm with pin 2 at 0.75 mm from center (that is, −2.25, +0.75, +2.25, the same as the PCM12 footprint), two Ø0.9 mm holes 3.0 mm apart (same), body pads 1.0 mm wide with 6.3 mm inner span (centers at ±3.65 mm, same x). Signal pads 0.8 x 2.2 mm against 0.7 x 1.6 mm in the current footprint. Body pad y-positions not compared to 0.01 mm. Likely solderable on the existing footprint; confirm with an overlay before ordering. |
| Nidec CUS-12TB | Digi-Key "-20°C ~ 70°C" | 563-1102-1-ND, "In-Stock: 74,403", Active (https://www.digikey.com/en/products/result?keywords=CUS-12TB) | Not a cold fix: rated −20 °C, the same as the part it would replace. |

## Row 6: J8 JST S2B-PH-SM4-TB(LF)(SN) (Okapi, sheet Power_Input): CORRECTED; JST's own datasheet rates PH at −40 °C

- JST PH connector datasheet ePH.pdf (https://www.jst-mfg.com/product/pdf/eng/ePH.pdf; curl got HTTP 403, WebFetch retrieved the PDF on 2026-11-11; PDF CreationDate "Tue Jan 27 09:38:57 2026 CET"). Specifications, verbatim: "Current rating: 2 A AC/DC (AWG #24)"; "Voltage rating: 100 V AC/DC"; "Temperature range: ‑40℃ to +105℃ (including temperature rise in applying electrical current)"; "Contact resistance: Initial value/ 10 mΩ max. After test/ 20 mΩ max." The side-entry SMT header table lists "S2B-PH-SM4-TB" (2 circuits). Header material: "Post: Copper alloy, tin-plated"; "Base housing: PA, natural (white)"; "Note: 1. This product displays (LF)(SN) on a label." Crimp contact: "Copper alloy, tin-plated"; "Contact JST for gold-plated products."
- Digi-Key S2B-PH-SM4-TB (https://www.digikey.com/en/products/result?keywords=S2B-PH-SM4-TB(LF)(SN), fetched 2026-11-11): 455-S2B-PH-SM4-TBCT-ND (cut tape), -TBTR-ND, -TBDKR-ND; "In-Stock: 133,904"; Active; Operating Temperature "-25°C ~ 85°C"; contact finish mating "Tin", post "Tin"; insulation "Polyamide (PA6T), Nylon 6T". Digi-Key links the same ePH.pdf.
- The −25 °C in the survey is Digi-Key's parametric field. JST's current datasheet, which Digi-Key itself links, says −40 to +105 °C. The maker's document outranks the distributor field; Digi-Key's entry appears out of date (that it reflects an older JST revision is a hypothesis, UNVERIFIED).
- The "tin-plated" part of the claim is correct (JST datasheet and Digi-Key agree). Tin-on-tin fretting under thermal cycling remains a general concern, not a rating failure.
- −40 °C alternatives that mate with the JST PH plug: not needed for the rating, since the JST part itself is rated −40 °C; not searched further. The v0.8 schematic carries the older Digi-Key number `455-1749-1-ND`; whether Digi-Key still maps it to this part was not checked.

## Row 7: On Shore OSTVN screw terminals (Okapi and Margay): VERIFIED; the conflict is real

Parts on the boards: Okapi J5, J6, J7 OSTVN02A150; J3 OSTVN04A150; J1, J4 OSTVN08A150; J2 OSTVN10A150. Margay J3 OSTVN06A150; J2 OSTVN10A150.

- On Shore drawing OSTVNXXA150 (https://www.on-shore.com/wp-content/uploads/OSTVNXXA150.pdf, fetched 2026-11-11; PDF CreationDate 26 Jul 2022; image-only, read by tesseract OCR and then confirmed by eye on a 300 dpi crop): "8.Temperature range:-40C°~ 115C°"; "Soldering temperature:250±10C°/5s"; "5.Tightening torque: 1.5kgf.cm (0.15N.m)"; "6.Screw thread: M1.6"; "4.Insulation Resistance: 1000MΩ or more at DC500V". Materials column (OCR): brass, tin plated; screws M1.6x0.35 Zn plated and Ni plated (which part takes which plating not read).
- Digi-Key, each fetched 2026-11-11 from https://www.digikey.com/en/products/result?keywords=<MPN>:

| MPN | Digi-Key | In stock | Status | Digi-Key operating temperature |
|---|---|---|---|---|
| OSTVN02A150 | ED10561-ND | 40,644 | Active | "-30°C ~ 105°C" |
| OSTVN04A150 | ED10563-ND | 18,477 | Active | "-30°C ~ 105°C" |
| OSTVN06A150 | ED10565-ND | 7,403 | Active | "-30°C ~ 105°C" |
| OSTVN08A150 | ED10566-ND | 12,994 | Active | "-30°C ~ 105°C" |
| OSTVN10A150 | ED10567-ND | 3,325 | Active | "-30°C ~ 105°C" |

- Digi-Key's own datasheet link for the series (https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/1123/OSTVNXXA150.pdf, fetched 2026-11-11; a different file, PDF CreationDate 10 Nov 2021) also reads "8.Temperature range:-40C- 115C°" by OCR. Both versions of the maker's drawing say −40 °C; Digi-Key's parametric −30 °C is contradicted by the drawing Digi-Key itself serves. The fix in the README ("ask On Shore") stands, since only On Shore can say which is right.
- Small correction to the connectors survey: it cites https://www.digikey.com/en/products/detail/on-shore-technology-inc/OSTVN10A150/1588872 as the OSTVN10A150 page with 2,599 in stock. That URL now serves OSTVN12A150 (ED10568-ND, 2,599 in stock, "-30°C ~ 105°C"). OSTVN10A150 is ED10567-ND with 3,325 in stock. The temperature conclusion is unchanged.

## Row 8: FTDI FT231X (Okapi U23 and Margay U2, both FT231XQ-R): PARTLY CORRECTED; the UK order has moved on, and Digi-Key shows 0 in stock

Both boards use **FT231XQ-R** (20-pin QFN): Okapi v0.8 U23 (sheet USB_ISP_Feather) and Margay 3v0 U2 (`Margay_BoM_3v0_-_2026-11-04.csv`, DK 768-1128-1-ND). The README's "(both boards use FTDI)" is correct.

- Digi-Key FT231XQ-R (https://www.digikey.com/en/products/detail/ftdi-future-technology-devices-international-ltd/FT231XQ-R/3029140, fetched 2026-11-11): 768-1128-1-ND (cut tape), -2-ND, -6-ND; **"In-Stock: 0"**; Active; "-40°C ~ 85°C"; "20-WFQFN Exposed Pad"; "20-QFN (4x4)"; datasheet https://ftdichip.com/wp-content/uploads/2025/06/DS_FT231X.pdf. The FTDI datasheet itself returned HTTP 403 (2020 and 2025 URLs, WebFetch and curl): FTDI's own temperature figure UNVERIFIED; Digi-Key's −40 °C stands.
- Single source: the FT231X is an FTDI-proprietary part; no other maker's part with the FT231X pinout was found. This is a negative search result, not a confirmed statement from FTDI.
- UK National Security and Investment Act 2021, first order. gov.uk "Acquisition of 80.2% of shares in Future Technology Devices International Limited by FTDI Holding Limited: notice of final order" (https://gov.uk/government/publications/acquisition-of-802-of-shares-in-future-technology-devices-international-limited-by-ftdi-holding-limited-notice-of-final-order/acquisition-of-802-of-shares-in-future-technology-devices-international-limited-by-ftdi-holding-limited, fetched 2026-11-11; "Updated 13 December 2024"): made by "the Chancellor of the Duchy of Lancaster"; "comes into force on 5 November 2024"; "requiring FTDIHL to sell 80.2% of FTDI within a specified period"; risks: "UK-developed semiconductor technology and associated intellectual property" used contrary to national security, and "the ownership of FTDI being used to pose a risk to critical national infrastructure" which uses FTDI products. Variation notice (same collection, "-notice-of-final-order-variation"): "The variation comes into force on 13 December 2024"; it changes the date for a draft disposal plan; "There are no other changes to the divestment process or the divestment timetable."
- **Newer order, not in the README.** gov.uk "Acquisition of an 80.2% shareholding in Future Technology Devices International Limited by Willow Vision Limited" (https://www.gov.uk/government/publications/acquisition-of-an-802-shareholding-in-future-technology-devices-international-limited-by-willow-vision-limited-notices-of-final-order-and-variation-of/acquisition-of-an-802-shareholding-in-future-technology-devices-international-limited-by-willow-vision-limited, fetched 2026-11-11; "Updated 5 August 2026"): a final order under section 26 "which comes into force on 1 July 2026" approves Willow Vision Limited acquiring 80.2% of FTDI "subject to certain requirements relating to payments, communications between the parties and FTDI's activities following completion"; risk stated: "The past ownership of FTDI being used to pose a risk to critical national infrastructure which uses FTDI products." A variation came into force on 4 August 2026 (per web-search snippet of the variation notice; not opened). Who owns Willow Vision Limited, and whether the sale has completed: UNVERIFIED (one web search found nothing).
- Court challenges (web-search snippets of law-firm notes, not opened, UNVERIFIED): High Court refused interim relief on 7 February 2025 and rejected judicial review on 25 July 2025 ([2025] EWHC 1922 (Admin), https://caselaw.nationalarchives.gov.uk/ewhc/admin/2025/1922).

USB-UART alternatives (functional, not pin- or footprint-compatible):

| Part | Digi-Key (fetched 2026-11-11) | Notes |
|---|---|---|
| Silicon Labs CP2102N-A02-GQFN20R | 336-5886-1-ND, "In-Stock: 6,338", Active, "-40°C ~ 85°C (TA)", "20-QFN (3x3)" (https://www.digikey.com/en/products/result?keywords=CP2102N-A02-GQFN20R) | 3 x 3 mm against FT231XQ's 4 x 4 mm: new footprint, new pinout, different driver. Silicon Labs datasheet returned 403 (UNVERIFIED from maker). |
| Microchip MCP2221A-I/ML | MCP2221A-I/ML-ND, "In-Stock: 748", Active, "-40°C ~ 85°C", "16-QFN (4x4)" (https://www.digikey.com/en/products/result?keywords=MCP2221A-I%2FML) | USB to UART and I2C; fewer modem-control lines than FT231X (UNVERIFIED from maker: Microchip datasheet URL redirected and was not followed). Whether it can drive the DTR-based auto-reset the ISP path uses is UNVERIFIED. |

## Corrections to the README table and the survey reports

1. **JST PH (row 6) is rated −40 °C by JST.** JST's current ePH.pdf (PDF dated 27 Jan 2026) says "Temperature range: ‑40℃ to +105℃ (including temperature rise in applying electrical current)". The survey's −25 °C is Digi-Key's parametric field, which disagrees with the datasheet Digi-Key links. The row's problem should read "Digi-Key lists −25 °C; JST's datasheet says −40 to +105 °C; tin-plated". The "tin-plated" part is right.
2. **FTDI (row 8): the UK order has a sequel.** The November 2024 order to sell was followed by a final order in force on 1 July 2026 approving a sale of 80.2 % to Willow Vision Limited, with conditions. "Forced-sale order on its owner since November 2024" is out of date. Completion and the buyer's ownership are UNVERIFIED. Separately, Digi-Key shows **0 in stock** for FT231XQ-R on 2026-11-11.
3. **MLX90393 package name (row 1, task brief):** SLW is not UQFN-16. Melexis: "LW" = "QFN-16 3x3x1mm package with wettable flanks"; the E grade (MLX90393ELW-ABA-011-RE) shares package and option code, therefore address.
4. **U41 MCP23018 is still labeled TI in the v0.8 KiCad schematic,** not only in the 2021 BoM. It needs fixing in the KiCad source; the other 2021 BoM errors in the table are already fixed in v0.8.
5. **On Shore (row 7), minor:** the connectors survey's Digi-Key URL for OSTVN10A150 (product 1588872, "2,599 in stock") now serves OSTVN12A150. OSTVN10A150 is ED10567-ND, 3,325 in stock. Both versions of On Shore's drawing (2021 and 2022 PDFs) read −40 to 115 °C, including the copy Digi-Key serves.
6. **Linx holder (row 4), precision:** BAT-HLD-012-SMT and -SMT-TR are one holder in two packings (TE drawing BAT-HLD-012-SMT-OTL rev B part table). TE rates it −30 to 70 °C and names CR1216 and CR1225, not the CR1220 the boards use.

Rows confirmed as written: U38 MLX90393SLW (−20 °C, E grade −40 °C exists), U44 VEML6030 (−25 °C; storage also −25 °C), U4 LT3652EDD (0 °C guaranteed, −40 °C "assured by design"; LT3652IDD#PBF in stock), C&K PCM12SMTR (obsolete, 2,726 left, −20 °C per Digi-Key), 2021 BoM MCP23018 listed as TI.

## Web dead ends (2026-11-11), so a restart can skip them

- melexis.com datasheet landing page: HTTP 403 to WebFetch (the direct PDF under /-/media/ worked with curl).
- analog.com 3652fe.pdf: curl timed out twice (HTTP/2, then HTTP/1.1).
- digikey.com via curl: Cloudflare challenge (HTTP 403). WebFetch works on Digi-Key.
- te.com DocumentDelivery PDF: HTTP 403 to curl; WebFetch retrieved it, but the text layer is glyph-encoded, so it was read by OCR.
- Littelfuse/C&K PCM datasheet (assetdocs link) and ckswitches.com/media/1424/pcm.pdf: HTTP 403; leocom.kr mirror timed out.
- jst-mfg.com ePH.pdf: HTTP 403 to curl; WebFetch retrieved it.
- silabs.com CP2102N datasheet, ftdichip.com DS_FT231X.pdf (2020 and 2025 paths): HTTP 403. microchip.com MCP2221A datasheet: redirect not followed.
- vishay.com /docs/0/<part>.pdf guesses for VEML6031X00, VEML7710, VEML4031X00, VEML3328, VEML6040: 404 (the real VEML6031X00 path is /docs/80007/).
- Digi-Key keyword searches for "Keystone 3000", "FT231X" and "BC501SM" returned category tiles or partial rows only; detail pages were used instead.
- Search for completion of the Willow Vision Limited purchase of FTDI: no result.

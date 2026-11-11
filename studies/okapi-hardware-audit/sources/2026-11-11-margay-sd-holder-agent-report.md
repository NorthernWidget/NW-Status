Status: COMPLETE

# Margay SD / microSD card holder survey (2026-11-11)

Agent report. Question (Andy): "We have used Adafruit's since the start, but I wonder if it is really the best. Think about long field deployments, temperature swings, etc." This report brings evidence; it does not decide.

## Criteria note (coordinator, relaying Andy, 2026-11-11)

Sourcing preference: Digi-Key for everything if possible. For every candidate the Digi-Key part number and stock come first. A part Digi-Key does not carry is flagged as a weaker candidate, not dropped.

## Confirmed facts (appended as found)

## Sources checked

### F1. Provenance of Margay's SD holder footprint (verified from git, Project-Margay)

- The first Margay schematic with an SD holder (`ed79716`, 2018-04-04, "Added software folder to repo", Bobby Schulz) places `U$3` from **Adafruit's Eagle library**: `<part name="U$3" library="adafruit" library_urn="urn:adsk.eagle:library:420" deviceset="SDMMC" device="06132"/>`. The deviceset description reads "SD MMC Card holder / 4UCON part #06132 - easy to solder". So Andy's "Adafruit's" is correct as to the *footprint/device*: it came from the Adafruit Eagle library, and the land pattern is Adafruit's drawing of a 4UCON 06132 holder. (Command: `git show ed79716:Hardware/Margay.sch | grep '<part ' | grep -i sd`.)
- Commits `ed79716` through `647e501` (2018-04-12) use library `adafruit`; from `89ee30b` (2018-05-31, "Minor mod to hardware test, added BOM") the same deviceset/device is copied into `bschulz` (Bobby's library), unchanged in name.
- Holders bought into that one footprint, from BoMs:
  - Mark 1 (2018-05-31, `Hardware/Margay_Mrk1_BOM.csv` at `89ee30b`): **3M SD-RSMT-2-MQ-WF**, Digi-Key 3M5646CT-ND.
  - v2.2 onward (introduced `904d985`, 2019-07-19; BoMs `Production/Margay_BoM_2v2_-2021-05-10.csv` line 36, `..._2v3_-_2023-03-16.csv` line 38): **TE 2041021-4**, Digi-Key A101492CT-ND. The `06132` device in the bschulz library carries the attributes MF=TE, MPN=2041021-4, DIGIKEY=A101492CT-ND (`git show f2cbf69^:Hardware/Margay.sch`, line ~4246).
  - v3.0 (`f2cbf69`, 2023-03-17, Bobby Schulz, "Updated SD card and analog switch"): new device `WR-CRD`, package `SD_WURTH_WR-CRD`, **Würth 693063010911**, Digi-Key 732-3817-1-ND (`Production/Margay_BoM_3v0_-_2026-11-04.csv` line 38; package description links https://www.we-online.com/components/products/datasheet/693063010911.pdf).
- All of these are **full-size SD** holders, not microSD. Evidence: README.md lines 33 and 58 ("On board full size SD card (for ease of field use)"), line 44 caption ("Full-size SD card for data storage"); the field card in `Production/Margay_BoM_3v0_board_-_2023-03-17.csv` line 5 is "SD card, full-size, 8 GB, industrial (−40°C to +85°C)", SanDisk SDSDAF3-008G-XI, "Available via Mouser; not stocked at DigiKey". The SD pad pitch (2.5 mm, pads 1–9 at x = 6.9, 4.4, 1.9, −0.6, −3.1, −5.6, −8.1, −9.7, ...) is full-SD pitch.
- Both the 06132 and the Würth packages have card-detect (CD) and write-protect (WP) pads; Margay uses CD (README line 187: `SD_CD` D1, "Card detection pin for SD card, active low, AUX power must be on to use").
- Andy's memory "Adafruit's" therefore matches the footprint origin only: no Adafruit *product* was ever bought; the parts were 3M, then TE, then Würth.

### F2. Current footprint size (verified from files)

- Eagle package `SD_WURTH_WR-CRD` (Hardware/Margay.sch line 2340 ff.): body outline (layer 51) x −13.25 to +13.35, y −0.45 to −25.45, i.e. **26.6 × 25.0 mm**; courtyard (layer 39) x ±14.65, y +1.05 to −25.7, i.e. **29.3 × 26.75 mm**. Two NPTH locating holes, 1.1 mm at (−11.5, −2) and 1.6 mm at (9.5, −2). Signal pads 1.0 × 1.5 mm.
- Old Adafruit/4UCON `06132` package (`git show f2cbf69^:Hardware/Margay.sch` line 874 ff.): silk x −13.2 to +13.3, y 0 to −25.1 (26.5 × 25.1 mm), holes 1.1 mm at (−11.6, −2.1) and 1.6 mm at (9.5, −2.1), four shell pads GP/GP2/GP3/GP4 2.8 × 2 mm. Bobby kept the hole positions within 0.1 mm across the change.
- In KiCad, J1 is `nw-cold-silicon:SD_WURTH_WR-CRD` on **layer B.Cu** (the bottom side), Hardware/KiCAD/Margay.kicad_pcb line ~19752. On a 50.1 × 30.4 mm board the holder covers about 26.6 × 25.0 / (50.1 × 30.4) = 44 % of the bottom face (arithmetic on the numbers above).

### F3. Würth 693063010911 (current, v3.0) – datasheet facts

Source: Würth datasheet 693063010911, revision 003.002 dated 2026-07-16, saved beside this report as `2026-11-11-wurth-693063010911-datasheet.pdf` (fetched via https://www.we-online.com/components/products/datasheet/693063010911.pdf; curl got HTTP 403 from Akamai, WebFetch got the PDF).
- Title block (p. 1): "WR-CRD SD Card Connector", size/type "**Push & Pull - with Card Detection - 9 Pins**". It is a full-size SD, **push-pull (friction-retained, no latch)** holder; not push-push.
- Kind properties (p. 1–2): Durability **10 000 mating cycles**; Application SD; Type Push & Pull.
- General information: **Operating temperature −25 °C up to +85 °C**. This does not cover −40 °C.
- Electrical: rated current 0.5 A; working voltage 100 V(AC); withstanding voltage 500 V(AC) 1 min; contact resistance 100 mΩ max; insulation resistance 1000 MΩ min.
- Materials: insulator LCP, UL94 V-0, black; contact copper alloy, **"Selective Gold" plating, no thickness stated**; stamped contacts; shield copper alloy, nickel plated.
- Pins: 1–9 SD signals, 10 = CD (card detection switch), 11 = WP (write protection switch).
- Dimensions (p. 1 drawing): body 27.8 ±0.15 × 25.5 ±0.25 mm (across tabs), body width 25.7 ±0.2 mm; height 2.8 ±0.25 / 3.2 ±0.25 mm (two heights shown in the side view; the larger presumably over the card-detect/WP region – read from drawing, UNVERIFIED which is which). Land pattern span 28.8 mm wide; two locating pegs Ø1.1 and Ø1.6 mm; four hatched SMD shell/hold-down pads (two at the contact end 2.8 tall, two at the rear corners 2.8 tall).
- The "Pull-off force 0.1 N – 1.3 N" on the packaging page sits beside "Tape width 44 mm" and is the carrier-tape cover peel force, not card retention.
- No card retention/withdrawal force, no contact normal force, no humidity or salt-fog test is stated.

### F4. TE 2041021-4 (v2.2/v2.3 baseline) – distributor facts

Source: Digi-Key product page https://www.digikey.com/en/products/detail/te-connectivity-amp-connectors/2041021-4/2571152 (fetched 2026-11-11). TE's own customer drawing was not obtained (te.com DocumentDelivery: curl HTTP 403, WebFetch HTTP 500).
- Part Status: **Obsolete**. No stock and no price breaks shown. Digi-Key's suggested substitute is the Würth 693063010911 (732-3817-2-ND, 17,469 in stock, $3.51 single unit, as shown on that page 2026-11-11).
- Card type Secure Digital – SD (full-size); **Insertion, Removal Method: Push In, Pull Out** (push-pull, like the Würth); 11 positions (9 + 2); features "Board Guide, Switch"; height above board 0.130" (3.30 mm); contact finish gold, **10.0 µin (0.25 µm)**.
- Operating temperature: not on the Digi-Key page. Search-result snippets (GlobalSpec, SnapEDA) give −25 °C to +85 °C: UNVERIFIED (no TE document read).
- Implication from F1–F4 (fact, not interpretation): every holder Margay has used since 2019 is a full-size SD push-pull holder; neither was push-push.

### F5. Würth 693063010911 – Digi-Key (2026-11-11)

Source: https://www.digikey.com/en/products/result?keywords=693063010911 (fetched 2026-11-11).
- Digi-Key **732-3817-1-ND** (cut tape), 732-3817-2-ND (T&R), 732-3817-6-ND (Digi-Reel). **Stock 17,469. Active.**
- Price (cut tape): 1 = $3.51; **10 = $3.43; 100 = $2.88**; 50 = $3.02; T&R 450 = $2.34651.

### F6. Digi-Key keyword listing "SD push push", Memory Connectors – PC Card Sockets (fetched 2026-11-11)

Source: https://www.digikey.com/en/products/filter/memory-connectors-pc-card-sockets/414?keywords=SD%20push%20push (313 results; first 19 read; listing columns as Digi-Key gives them, stock and qty-1 price on 2026-11-11). Used to pick candidates, not as datasheet evidence.

| Mfr | MPN | DK product id | Card | Insert/remove | Gold thickness | Height | Stock | Qty 1 | Status |
|---|---|---|---|---|---|---|---|---|---|
| Amphenol ICC (FCI) | 10067847-001RLF | 2283478 | SD | Push In, Push Out | 50.0 µin (1.27 µm) | 2.80 mm | 25,693 | $2.31 | Active |
| Amphenol ICC (FCI) | 10067847-011RLF | 5207469 | SD | Push In, Push Out | 50.0 µin (1.27 µm) | 2.80 mm | 9,008 | $3.34 | Active |
| Molex | 0473092651 | 3044809 | microSD | Push In, Pull Out | 30.0 µin (0.76 µm) | 2.65 mm | 29,444 | $2.13 | Active |
| Amphenol ICC (FCI) | 10067099-200LF | 4238739 | microSD | Push In, Pull Out | 30.0 µin (0.76 µm) | 2.65 mm | 27,188 | $0.91 | Active |
| Molex | 0475710001 | 3262277 | microSD | Push In, Pull Out | 30.0 µin (0.76 µm) | 2.30 mm | 42,908 | $1.12 | Active |
| Molex | 5033981892 | 4555393 | microSD | Push In, Push Out | 19.7 µin (0.50 µm) | 1.28 mm | 58,827 | $2.92 | Active |
| Hirose | DM3D-SF | 1786510 | microSD | Push In, Pull Out | – | 1.55 mm | 24,564 | $2.32 | Active |
| Hirose | DM3BT-DSF-PEJS | 1982749 | microSD | Push In, Push Out | – | 1.83 mm | 12,108 | $3.16 | Active |
| Würth | 693071010811 | 3124583 | microSD | Push In, Push Out | – | 1.83 mm | 21,505 | $3.11 | Active |
| GCT | MEM2075-00-140-01-A | 9859614 | microSD | Push In, Push Out | 1.00 µin (0.025 µm) | 1.40 mm | 25,561 | $1.92 | Active |
| GCT | MEM2061-01-188-00-A | 9859612 | microSD | Push In, Push Out | 3.00 µin (0.076 µm) | 1.88 mm | 18,316 | $1.14 | Active |
| Amphenol (Commercial) | 1140084168 | 2187086 | microSD | Push In, Pull Out | 15.0 µin (0.38 µm) | 1.55 mm | 44,662 | $1.97 | Active |

Note: plating on these parts spans 1 µin to 50 µin; the TE baseline was 10 µin; Würth gives no figure.

### F7. Amphenol ICC (FCI) 10067847-001RLF – full-size SD, push-push

Sources: (a) Digi-Key https://www.digikey.com/en/products/result?keywords=10067847-001RLF (2026-11-11); (b) customer drawing 10067847 rev K (2014-09-24), saved as `2026-11-11-amphenol-10067847-datasheet.pdf` (from https://www.waldom.com/upload/parts/datasheets/mf-fci/fci-10067847-001rlf.pdf, Digi-Key's datasheet link); (c) FCI product specification GS-12-497 rev G (2009-12-26), saved as `2026-11-11-amphenol-10067847-GS-12-497-spec.pdf` (from https://www.farnell.com/datasheets/2562186.pdf).
- Digi-Key **609-3956-1-ND** (cut tape), 609-3956-2-ND (T&R), 609-3956-6-ND. **Stock 25,693. Active.** Lead time 19 weeks. Price: 1 = $2.31; **10 = $1.961; 100 = $1.6668**; T&R 300 = $1.5424.
- Digi-Key attributes: SD (full size); **Push In, Push Out**; Connector and Ejector; features Board Guide, Switch; gold, **50.0 µin (1.27 µm)**; height 2.80 mm; 12 (9 + 3) positions.
- Drawing sheet 3 note 2: "CONTACT: 50u" NICKEL UNDERPLATED ALL OVER. 100u" MATTE TIN ON SOLDER TAIL AREA. GOLD PLATED ON CONTACT AREA"; note 3 part-number code "1: 50u" Au OVER Ni"; "0: WITH PLASTIC PEG / 1: WITHOUT PLASTIC PEG" (so -001 has pegs, -011 does not). Shield: stainless. Marking note mentions "UD321 LUBRICANT" (a contact lubricant) on V2/V3 production. Pins 1–9 plus CD, WP, GND. Drawing sheet 1 warning: "THE PUSH/PUSH MECHANISM MUST TO BE IN THE UNLOCKING POSITION BEFORE REFLOW."
- Drawing sheet 1: body 28.5 mm wide × 29.00 mm deep (35.40 with card pushed? – the 35.40 dimension is to the card end; UNVERIFIED reading), height 2.80 mm; push stroke 1.00 mm, ejection stroke 4.60 mm. Sheet 2 land pattern: 24.80 mm from pad row to rear, 28.9 mm wide approx. (14.00 + 14.90); two plastic pegs Ø1.50; two rear shield GND pads 1.20 × 2.20 mm. **Not land-compatible with the Würth/TE/4UCON footprint** (different pad row positions and pegs; read from drawings).
- GS-12-497 §3.2.3: **operating temperature −40 to 105 °C**; storage −40 to 105 °C. Housing LCP GF30 UL94V-0; SD contacts phosphor bronze; shield, locking arm, positioning pin stainless; spring SWP-B (piano wire).
- GS-12-497 §4.0 test table: contact resistance 100 mΩ max; **total ejection force 8 N min, insertion force 12 N max**; vibration 10–1000 Hz, 0.35 mm/2 G, 8 h per axis, discontinuity 1 µs max; shock 50 G 6 ms, 50 per axis, discontinuity 1 µs max; **contact force 0.2–0.4 N**; durability **12,000 cycles (500 at −40 °C, 10,500 at 23 °C, 1000 at 85 °C)**, push-push function must work; humidity heat 6 cycles 90–100 % RH; dust test; high/low temperature operation soaks at **+70 °C and −30 °C** for 2 h unpowered; **salt spray 5 % NaCl, 35 °C, 48 h, EIA 364-26, "no harmful corrosion"**; thermal shock 100 cycles −30 °C ↔ +70 °C.
- Note (fact): the rated range is −40…105 °C but the qualification thermal soaks and shocks run only −30…+70 °C; only 500 durability cycles were run at −40 °C.

### F8. Digi-Key keyword listing "microSD hinge" (fetched 2026-11-11)

Source: https://www.digikey.com/en/products/filter/memory-connectors-pc-card-sockets/414?keywords=microSD%20hinge (32 results; first 19 read). All "Hinged Lid". In stock with qty-1 price on 2026-11-11:

| Mfr | MPN | DK product id | Gold | Height | Stock | Qty 1 |
|---|---|---|---|---|---|---|
| GCT | MEM2067-02-180-00-A | 9859613 | Flash | 1.80 mm | 19,356 | $1.09 |
| Molex | 0472192001 | 3044807 | 20.0 µin (0.51 µm) | 1.90 mm | 27,799 | $1.77 |
| JAE | ST1W008S4ER1500 | 1284037 | Flash | 2.00 mm | 18,035 | $1.92 |
| Hirose | DM3CS-SF | 2602739 | – | 1.83 mm | 61,539 | $2.00 |
| JAE | ST1W008S4BR1500 | 2044255 | 20.0 µin (0.51 µm) | 2.00 mm | 19,104 | $2.02 |
| Würth | 693072010801 | 3124584 | – | 1.75 mm | 12,933 | $3.41 |
| JAE | ST1W008S4AR1500 | 3720055 | 19.7 µin (0.50 µm) | 2.00 mm | 4,285 | $2.04 |
| Same Sky | MSD-10-C | 21796089 | Flash | 1.90 mm | 1,592 | $1.07 |
| Hirose | DM3C-SF | 1657771 | – | 1.83 mm | 3,181 | $2.07 |

Obsolete in the same list: Amphenol 101-00303-68, Molex 5009010800, Molex 0472192021, Hirose DM3C-SF(16).

### F9. Molex 0472192001 (series 47219) – microSD, hinged lid

Sources: (a) Digi-Key https://www.digikey.com/en/products/result?keywords=0472192001 (2026-11-11); (b) Molex product summary sheet generated 2021-06-15, saved as `2026-11-11-molex-0472192001-product-summary.pdf` (from https://static.chipdip.ru/lib/289/DOC012289153.pdf; molex.com timed out from curl and WebFetch). Product spec PS-47219-001-001 and drawing SD-47219-001-000 were NOT obtained.
- Digi-Key **WM6698CT-ND** (cut tape), WM6698TR-ND, WM6698DKR-ND. **Stock 27,799. Active.** Lead time 15 weeks. Price: 1 = $1.77; **10 = $1.507; 100 = $1.2809**; T&R 800 = $1.10599.
- Digi-Key: microSD, 8 positions, **Hinged Lid**, gold **20.0 µin (0.51 µm)**, height 1.90 mm.
- Molex summary: "1.10mm Pitch microSD Card Connector, Hinge Type"; **Card Detection Switch: No**; durability 5000 mating cycles max; contact copper alloy; mating plating gold, termination tin; shell stainless steel; PCB retention yes, PCB locator no; **operating temperature −40 to +85 °C**; 0.5 A per contact, 100 V DC; reflow 250 °C max.
- Footprint size: UNVERIFIED (drawing not obtained). Typical hinged microSD bodies are ~14–15 mm × ~15–17 mm (from memory, UNVERIFIED).

### F10. KiCad official footprints (Connector_Card.pretty)

Sources: GitLab API tree listing of kicad/libraries/kicad-footprints master, path Connector_Card.pretty (fetched 2026-11-11: `https://gitlab.com/api/v4/projects/kicad%2Flibraries%2Fkicad-footprints/repository/tree?path=Connector_Card.pretty&per_page=100`); sizes measured from the F.CrtYd / F.Fab lines of the same files in the local KiCad 10.0.8 install, /usr/share/kicad/footprints/Connector_Card.pretty (identical name list).
- SD/microSD footprints on master: SD_TE_2041021 (courtyard 29.30 × 26.66 mm), SD_Hirose_DM1AA_SF_PEJ82 (32.00 × 37.70), SD_Kyocera_1456380x9x11859+ (28.70 × 37.25 to 29.70 × 42.25), SD_Card_Device_16mm_SlotDepth, microSD_HC_Molex_47219-2001 (**15.70 × 15.00**, "Hinge Type"), microSD_HC_Wuerth_693072010801 (16.16 × 15.81), microSD_HC_Molex_104031-0811 (13.68 × 13.05), microSD_HC_Hirose_DM3D-SF (13.80 × 13.00), microSD_HC_Hirose_DM3AT-SF-PEJM5 and DM3BT-DSF-PEJS (15.70 × 17.70), SD-SIM_microSD-microSIM_Molex_104168-1620.
- **Not in the official library: Würth 693063010911** (Margay uses its own `nw-cold-silicon:SD_WURTH_WR-CRD`; Würth's datasheet lists Altium, Cadence, Eagle and KiCad "WR-CRD" downloads), **Amphenol 10067847**, Molex 47309, JAE ST1W, Hirose DM3CS.
- SD_TE_2041021's courtyard (29.30 × 26.66) matches Margay's Würth courtyard (29.3 × 26.75, F2) to 0.1 mm: the TE, 4UCON 06132 and Würth parts share one outline class.

### F11. Hirose DM3CS-SF – microSD, hinged lid, with card detect

Sources: (a) Digi-Key https://www.digikey.com/en/products/result?keywords=DM3CS-SF (2026-11-11); (b) Hirose DM3 series datasheet as hosted by Digi-Key, https://www.digikey.cn/zh/resources/datasheets/hirose/dm3-series-microsd (read via WebFetch at offsets 0 and 100000; PDF not saved: hirose.com 403, arrow/purdue mirrors failed).
- Digi-Key **HR1972CT-ND** (cut tape), HR1972TR-ND, HR1972DKR-ND. **Stock 61,539. Active.** Lead time 16 weeks. Price: 1 = $2.00; **10 = $1.701; 100 = $1.4452**.
- Digi-Key: microSD, 10 (8 + 2) positions, Hinged Lid, feature "Switch", gold (no thickness), height 1.83 mm.
- DM3 datasheet: card detection switch normally open; hinged metal cover with a tactile click on closing; "card contacts are cleaned by a slide action during insertion"; metal cover has four connection points to the PCB; **operating temperature −25 °C to +85 °C** (storage −40 to +85 °C, unmounted); humidity 95 % RH max no condensation; **durability 5,000 cycles for DM3C/DM3D** (10,000 for DM3AT/DM3BT push-push); contact resistance 100 mΩ max, Δ40 mΩ max after tests; vibration 10–55 Hz, 0.75 mm, 2 h per axis; humidity 96 h at 40 °C, 90–95 % RH; temperature cycle 5 cycles −55 ↔ +85 °C. DM3CS/DM3D contacts gold, cover tin-plated. Gold thickness not stated in the part read.
- KiCad official: no DM3CS footprint (F10). Dimensions UNVERIFIED (drawing pages not read).

### F12. Molex 0473092651 (47309-2651) – microSD, push-pull, card detect, 30 µin gold

Sources: (a) Digi-Key https://www.digikey.com/en/products/result?keywords=0473092651 (2026-11-11); (b) Molex product summary generated 2015-03-02, saved as `2026-11-11-molex-47309-2651-product-summary.pdf` (from https://static.chipdip.ru/lib/086/DOC034086494.pdf).
- Digi-Key **WM6700CT-ND** (cut tape), WM6700TR-ND, WM6700DKR-ND. **Stock 29,444 (+18,000 factory). Active.** Lead time 13 weeks. Price: 1 = $2.13; **10 = $1.806; 100 = $1.5346**.
- Digi-Key: microSD, 9 (8 + 1), **Push In, Pull Out**, feature Switch, gold **30.0 µin (0.76 µm)**, height 2.65 mm.
- Molex summary: "1.10mm Pitch microSD Card Header with Detect Switch, Height 2.65mm"; card detection switch yes; **durability 10,000 cycles**; plating min mating 0.762 µm gold, termination 0.051 µm gold; **operating −40 °C to +85 °C**; PCB retention yes, locator no.
- KiCad official: no footprint (F10). Dimensions UNVERIFIED.

### F13. Field reports and guidance on card retention (read 2026-11-11)

- **enDAQ (shock/vibration recorder maker), support article "Replacement / Repair"**, https://support.endaq.com/article/193-replacement-repair: "The SD card used for storage in the enDAQ sensor is in an SD card holder and can be replaced. Occasionally the SD card will come dislodged from the holder and/or damaged but can be replaced." No holder type named.
- **SparkFun forum, "SparkFun OpenLog DEV-13712 -- Faulty SD card socket"** (2021-03-12 to 2021-05-26), https://community.sparkfun.com/t/sparkfun-openlog-dev-13712-faulty-sd-card-socket/41738: a user's five OpenLogs (microSD push-push socket) stopped logging after 3–4 days "due to the SD coming out by itself"; socket "no longer retains the SD card"; internal plastic found brittle. SparkFun disputed a bad batch and suspected use/heat damage; Digi-Key refunded. Cause unresolved.
- **comp.arch.embedded thread "Shock and Vibration specs of SD and Micro SD sockets ?"** (2007-02-12/13), https://www.embeddedrelated.com/showthread/comp.arch.embedded/66348-1.php: larwe: "Use push-pull connectors by preference (push-push may self-eject accidentally)" and "provide an external mechanical lock to prevent the card from sliding out"; rickman: "provide your own mechanical card retention", "You will likely have to do your own testing for this."
- **Same Sky / Digi-Key article "All Designers Need to Know About Memory Card Connectors"** (Nick Grillone, 2025-08-05), https://www.electronicdesign.com/pai-asset/6ad23e00b65736f5c602b342: Push-In/Pull-Out "Best for low-vibration or semi-permanent installations"; Push-Push "ideal for frequent use in consumer devices"; Hinged "Designed for high-vibration environments like automotive or industrial systems where secure retention is critical." (Vendor guidance, no test data.)
- **Cave Pearl Project** (search only; individual posts not opened): reports of lost SD cards in long tests and of breadboard contact noise, and a recommendation about spring-contact quality in cheap SD adapter modules (via search summary of thecavepearlproject.org; UNVERIFIED wording). Nothing found there on board-mounted holder retention.
- **Amphenol GS-12-497** (F7) is the only document found with quantified retention-relevant numbers: ejection force 8 N min (push-push latch), contact force 0.2–0.4 N, vibration and shock with 1 µs discontinuity limits, 48 h salt spray, and 500 durability cycles at −40 °C.
- Not found: any published field statistics comparing push-push, push-pull and hinged holders; any fretting data specific to SD holders. General connector literature (search only) identifies thermal-cycling micro-motion as a fretting driver and contact force and gold thickness as the controlling variables; not SD-specific.
- Margay context (fact): Margay's holder sits on the bottom face (F2); Margay's current Würth part is push-pull with no latch, so its retention is friction from the contact springs plus card-detect/WP springs.

### F14. Soldered SD NAND ("SD chip") alternative

Sources: (a) XTX "SD NAND 1Gb 2Gb 4Gb 8Gb XTSD0xGLGEAG" datasheet Rev 2.6, saved as `2026-11-11-xtx-xtsd-sd-nand-datasheet.pdf` (from https://whycan.com/files/members/3/XTX_SD_NAND_1Gb_2Gb_4Gb_8Gb_XTSD0xGLGEAG_V2.pdf); (b) Digi-Key https://www.digikey.com/en/products/result?keywords=XTSD (2026-11-11); (c) Digi-Key keyword "SD NAND" in Memory: 0 results.
- XTX XTSD01G/02G/04G/08G (1–8 Gbit, i.e. 128 MB–1 GB): LGA8, **8 × 6 mm**; SD 2.0 protocol, SD or SPI mode (CS = CD/DAT3 held low at init), 2.7–3.6 V; built-in hardware ECC and NAND management (datasheet p. 1–2). **Operating Ta −30 to +85 °C**; storage −40 to +85 °C (datasheet §4.1).
- Digi-Key carries **no bare SD NAND chip** under "SD NAND" or "XTSD". It carries only Adafruit's breakout **4899** ("XTSD04G ... 512MB SPI flash SD card", Digi-Key **1528-4899-ND**, stock 50, $9.50, Active, lead time 18 weeks) and related Adafruit SKUs 6038/6039 (stock not shown). Bare XTSD and CS (CSNP…) parts are LCSC items (search results only). Per the sourcing criterion this option is **weaker: not a Digi-Key part**.
- A search snippet attributes −40 to +85 °C to a CS "CSNP4GCR01" part and to a newer XTX industrial series: UNVERIFIED (datasheets not read).
- Tradeoffs (stated, not measured): no connector, so no retention, fretting or card-detect question; capacity 128 MB–1 GB per chip versus the 8 GB industrial card now used; data retrieval needs a cable (USB/serial dump through the ATmega1284P, slow) or a board swap instead of a card swap; the swap procedure in Margay's README ("SD card swap", README lines 453–456) would change; flash wear and failure take the logger with them.

### F15. 3M SD-RSMT-2-MQ-WF (Mark 1, 2018) – Digi-Key

Source: https://www.digikey.com/en/products/result?keywords=SD-RSMT-2-MQ-WF (2026-11-11): **Obsolete**; SD (full size); **Push In, Push Out**; Board Guide, Switch; gold 10.0 µin (0.25 µm); height 3.10 mm. So Margay Mark 1 (2018) used a push-push holder on the Adafruit/4UCON footprint; v2.2 (2019) onward used push-pull holders.

## Comparison table (neutral; no weighting)

Digi-Key PN and stock first (sourcing criterion). Stock and price fetched 2026-11-11. "–" = not stated in any source read. Fact numbers point to the sections above.

| Candidate | Digi-Key PN | DK stock | Card | Retention | Op. temp | Gold on contact | Contact force / cycles | Card detect | PCB anchoring | Body (W × D × H) | KiCad official | Price 10 / 100 | Land-compatible with current | Facts |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Würth 693063010911 (current, v3.0) | 732-3817-1-ND | 17,469 | SD | Push-pull, friction | **−25…+85 °C** | "Selective gold", thickness – | – / 10,000 | Yes (+WP) | 2 pegs (Ø1.1, Ø1.6), 4 shell pads | 27.8 × 25.5 × 2.8–3.2 mm | No (NW library has it) | $3.43 / $2.88 | – (is current) | F3, F5 |
| TE 2041021-4 (v2.2/v2.3) | A101492CT-ND | 0, **Obsolete** | SD | Push-pull, friction | −25…+85 °C UNVERIFIED | 10 µin (0.25 µm) | – / – | Yes ("Switch") | pegs + shell pads (Adafruit/4UCON outline) | – × – × 3.30 mm | Yes, SD_TE_2041021 (29.30 × 26.66 courtyard) | – | Yes (same outline class, F10) | F1, F4 |
| Amphenol FCI 10067847-001RLF | 609-3956-1-ND | 25,693 | SD | **Push-push** latch, ejection force 8 N min | **−40…+105 °C** (qualification soaks −30/+70) | **50 µin (1.27 µm)** over 50 µin Ni; lubricant | **0.2–0.4 N** / 12,000 (500 at −40 °C) | Yes (+WP) | 2 plastic pegs Ø1.5, 2 rear shield pads, stainless shell | 28.5 × 29.0 × 2.80 mm | No | $1.961 / $1.6668 | **No** (new footprint, ~3.5 mm deeper body) | F7 |
| Molex 0472192001 (47219) | WM6698CT-ND | 27,799 | microSD | **Hinged lid** | **−40…+85 °C** | 20 µin (0.51 µm) | – / 5,000 | **No** | "PCB retention yes", stainless shell | courtyard 15.70 × 15.00, H 1.90 mm | Yes, microSD_HC_Molex_47219-2001 | $1.507 / $1.2809 | No | F9, F10 |
| Hirose DM3CS-SF | HR1972CT-ND | 61,539 | microSD | **Hinged lid** (tactile click) | **−25…+85 °C** | gold, thickness – | – / 5,000 | Yes (N.O.) | metal cover, 4 PCB points | – × – × 1.83 mm | No | $1.701 / $1.4452 | No | F11 |
| Molex 0473092651 (47309) | WM6700CT-ND | 29,444 | microSD | Push-pull, friction | **−40…+85 °C** | **30 µin (0.762 µm min)** | – / 10,000 | Yes | "PCB retention yes" | – × – × 2.65 mm | No | $1.806 / $1.5346 | No | F12 |
| Soldered SD NAND (XTX XTSD0xG) | **none for bare chip** (only Adafruit 4899 breakout, 1528-4899-ND, 50) | – | none (chip) | soldered | −30…+85 °C (−40 UNVERIFIED for other makers) | n/a | n/a | n/a | LGA8 | 8 × 6 mm | – | – | No | F14 |

Weaker-candidate flags under the Digi-Key criterion: TE 2041021-4 (obsolete at Digi-Key) and SD NAND (no bare chip at Digi-Key). All other rows are Active and in stock at Digi-Key.

Facts that cut across the table (not interpretation):
- Of the six holders, only the Amphenol 10067847 (full SD) and the two Molex microSD parts state −40 °C; the current Würth and the Hirose state −25 °C.
- The only full-size SD part found with a −40 °C rating is a push-push part; no full-size hinged part was found, and no full-size push-pull part with a −40 °C rating was found (search was not exhaustive: 19 of 313 "SD push push" rows were read).
- No source found gives field statistics comparing push-push, push-pull and hinged holders (F13); the guidance found (one 2007 forum post, one 2025 vendor article) ranks hinged first for vibration and push-push last.
- Moving to microSD changes the card as well: the field card now is the full-size SanDisk SDSDAF3-008G-XI, −40…+85 °C industrial (F1).

## Open questions

1. Has a Margay card ever unseated, or failed to read, in the field? No record was found in Project-Margay or NW-Status (grep for SD terms, F1 and NW-Status hits list). Andy's or Bobby's field memory is the only source.
2. Why did Bobby change TE → Würth in 2023 (`f2cbf69`)? The TE part being obsolete with Würth as Digi-Key's suggested substitute (F4) is consistent with it, but the commit message does not say.
3. Würth's −25 °C lower limit: is there a Würth statement for −40 °C (product spec or test report beyond the datasheet)? Not found. Same for TE 2041021 (TE drawing not obtained).
4. Würth gold thickness ("Selective Gold") and contact normal force: not in the datasheet; would need a Würth query.
5. Amphenol 10067847 is rated −40…+105 °C but its qualification soaks run −30…+70 °C (F7): whether Amphenol has −40 °C data beyond the 500 durability cycles is open.
6. Amphenol 10067847 body is ~29 mm deep against Würth's 25.5 mm; whether it fits Margay's bottom face without moving other parts needs a placement check in Hardware/KiCAD/Margay.kicad_pcb.
7. Hinged microSD without card detect (Molex 47219) would drop Margay's `SD_CD` (README line 187); Hirose DM3CS keeps CD but is −25 °C. JAE ST1W008S4BR1500 (hinged, 20 µin, Digi-Key 19,104 in stock, F8) was not examined for temperature or CD.
8. Dimensions of Hirose DM3CS-SF and Molex 47309 were not read from drawings.
9. Contact plating on the card side (industrial SD vs industrial microSD) and the card's own temperature rating were not surveyed; that interacts with any SD→microSD change.
10. Is an external retention (a strap, a lid in the enclosure, a dab of RTV across the card) already used in Margay deployments? Nothing found in the repository; a retention feature could change the push-pull versus hinged comparison.

## Sources checked (including dead ends)

- Project-Margay git: `git log` for SD/MPN strings (`-S2041021`, `-SSD-RSMT`, `-S693063010911`), schematic history of the J1/U$3 part (`ed79716` … `f2cbf69`), BoMs in `Production/`, `Hardware/Margay_Mrk1_BOM.csv` at `89ee30b`, README.md, Production/README.md, Hardware/KiCAD/Margay.kicad_pcb.
- NW-Status: grep for SD card terms across .md/.csv/.py/.txt; no holder or field-failure record found.
- Würth datasheet: curl → HTTP 403 (Akamai); WebFetch → PDF saved.
- TE 2041021 drawing: te.com DocumentDelivery, curl 403, WebFetch 500 (dead end). Digi-Key page read.
- Amphenol drawing via Waldom (OK); GS-12-497 via Farnell (OK); cdn.amphenol-cs.com 403 (dead end).
- Molex: molex.com PDFs time out from curl and WebFetch (dead end); chipdip.ru mirrors of Molex product summaries (OK, 47219 and 47309).
- Hirose: hirose.com 403; arrow static6 HTTP/2 error; Purdue mirror 503; components.ru unresolvable (dead ends). Digi-Key-hosted DM3 datasheet read via WebFetch (text only).
- XTX datasheet via whycan.com (OK). Digi-Key "SD NAND" (0 results), "XTSD" (Adafruit breakout only).
- Digi-Key listing pages: "SD push push" (313 results, 19 read), "microSD hinge" (32 results, 19 read); product result pages for 693063010911, 2041021-4, 10067847-001RLF, 0472192001, DM3CS-SF, 0473092651, SD-RSMT-2-MQ-WF.
- KiCad: GitLab API tree of kicad-footprints master Connector_Card.pretty; local /usr/share/kicad/footprints (KiCad 10.0.8) for courtyard sizes.
- Field evidence: enDAQ support article; SparkFun OpenLog forum thread; comp.arch.embedded 2007 thread; Same Sky/Digi-Key 2025 article; Cave Pearl (search summaries only, posts not opened); wildlabs.net/comment/6745 (403, dead end); PurpleAir and Siemens LOGO! pages (search snippets only, not used as evidence).

## Decision (Andy, 2026-11-11, added by the parent session)

Margay keeps a **full-size SD** card ("to not lose the card and be able to move it with gloves on") in a **push-pull** holder ("to be more stable"). Of the parts above, only the current Würth 693063010911 and the obsolete TE 2041021-4 meet both, and both are rated to −25 °C. No full-size push-pull holder rated to −40 °C was found (search not exhaustive, line 182). Open: a narrower search for one, or the Würth with its −25 °C rating accepted.

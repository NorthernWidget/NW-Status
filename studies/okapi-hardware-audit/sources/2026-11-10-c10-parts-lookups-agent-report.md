COMPLETE

# Parts lookups, 2026-11-10

## Sources log

- 2026-11-10 DEAD END: https://www.digikey.com/en/products/detail/texas-instruments/LM66100DCKR/10285786 (guessed product ID; resolves to KOA SG73S1ETTP1542D, not LM66100)
- 2026-11-10 WebSearch "LM66100DCKR digikey": found product ID 10273183; regional-site snippets (stock 13,653-66,618) are search-cache snapshots, NOT used.

## Q1 LM66100
| MPN | DK PN | Stock | @10 | @100 | Lead | URL | Date |
|---|---|---|---|---|---|---|---|
| LM66100DCKR | 296-53541-1-ND (CT), -2-ND (TR), -6-ND (Digi-Reel) | 386 | $0.25100 | $0.19270 | 26 wk mfr std | https://www.digikey.com/en/products/detail/texas-instruments/LM66100DCKR/10273183 | 2026-11-10 |
| LM66100DCKT (250-pc reel) | 296-53540-1-ND (CT), -2-ND, -6-ND | 1,389 | $0.78000 | $0.62080 | 26 wk; DK lists op temp -40 to 105 C (DCKR listed differently? check) | https://www.digikey.com/en/products/detail/texas-instruments/LM66100DCKT/10273182 | 2026-11-10 |
| LM66100QDCKRQ1 (AEC-Q100) | 296-LM66100QDCKRQ1CT-ND (CT), ...TR-ND, ...DKR-ND | 5,822 | $0.26000 | $0.19980 | 26 wk; -40 to 125 C | https://www.digikey.com/en/products/detail/texas-instruments/LM66100QDCKRQ1/16341515 | 2026-11-10 |
- 2026-11-10 DEAD END: findchips.com/detail/lm66100dckr returned HTTP 403.
- 2026-11-10 https://www.ti.com/product/LM66100 : op temp -40 to 125 C (junction) for the device; no orderable inventory shown without login. So the DK "-40 to 105 C" on DCKT is a DK listing discrepancy, not a different die (DCKR vs DCKT = 3000 vs 250 reel, per TI convention; not verified on the addendum).
- 2026-11-10 DEAD END: mouser.com/ProductDetail/Texas-Instruments/LM66100DCKR and mouser.com/c/?q=LM66100 both timed out (60 s). octopart.com/search 403.

## Q2 TPS22917 CT
Source: https://www.ti.com/lit/ds/symlink/tps22917.pdf (SLVSDW8B, Sept 2017, rev Dec 2021), fetched 2026-11-10, text in scratchpad c10/ds/tps22917.txt.
- Pin 4 CT: "Switch slew rate control. Connect capacitor from this pin to VIN to increase output slew rate and turn-on time. Can be left floating for fastest timing."
- 7.3 ROC: "VCT Timing Capacitor Voltage Rating ... MIN 7 V". This is the only CT capacitor requirement. No dielectric, tolerance or tempco requirement stated anywhere (grep for dielectric/X7R/X5R/C0G/tolerance/ceramic: none in CT context).
- Eq 2: Turn-On time = CT x tON; tON = 4 us/pF at VIN 5.0 V, 3.8 at 3.6 V (CT >= 100 pF). So 10 nF -> ~40 ms at 5 V (my arithmetic). SRON 2300 (mV/us)*pF at 5 V -> 0.23 mV/us.
- Consequence for dielectric: tON scales linearly with CT, so a +/-10 % X7R gives +/-10 % on tON plus DC-bias/temperature drift; C0G is +/-5 % and flat. Datasheet does not require either.
- 2026-11-10 DEAD END: DK keyword search URLs (digikey.com/en/products/result?keywords=...) return "no results" to WebFetch (JS-rendered); not usable.
- 2026-11-10 DEAD END: two WebSearches for a 10 nF C0G 0402 DK listing (50 V and 25 V, incl. GRM1555C1H103JA01D, GRM1555C1E103JA01D, C1005C0G1E103J) found none; only 1 nF C0G and 10 nF X7R. C0G at 10 nF in 0402 not shown to be a stocked DK item -> go X7R.
| Role | MPN | DK PN (CT) | Spec | Stock | @10 | @100 | Lead | URL | Date |
|---|---|---|---|---|---|---|---|---|---|
| Primary | Murata GRM155R71H103KA88D | 490-4516-1-ND | 10 nF +/-10 % 50 V X7R 0402 | 3,397,145 | $0.02200 | $0.01240 | 17 wk | https://www.digikey.com/en/products/detail/murata-electronics/GRM155R71H103KA88D/1033252 | 2026-11-10 |
| Secondary | Samsung CL05B103KB5NNNC | 1276-1028-1-ND | 10 nF +/-10 % 50 V X7R 0402 | 3,769,991 | $0.01900 | $0.01040 | 61 wk | https://www.digikey.com/en/products/detail/samsung-electro-mechanics/CL05B103KB5NNNC/3886686 | 2026-11-10 |
- 2026-11-10 DEAD END: guessed DK ID https://www.digikey.com/en/products/detail/kemet/C0402C103J5RACTU/411387 resolves to KEMET C0805C180J5GACTU (18 pF); not used.

## Q3 Shunts
### R10 primary: Rohm PMR10EZPFV3L00 (3 mOhm 0805)
- Rohm lineup https://fscdn.rohm.com/en/products/databook/datasheet/passive/resistor/chip_resistor/pmr-e.pdf (2026.09 Rev.002), fetched 2026-11-10: PMR10 3/4/5 mOhm row marked "New": 1 W (rated terminal temp 105 C), F(+/-1 %), +/-150 ppm/C. (Its inch column misprints "3216"; detail sheet says 0805.)
- Rohm PMR series detail datasheet, 2023.9 Rev.014, via https://components101.com/sites/default/files/2024-06/pmr-series-datasheet.pdf (mirror of Rohm doc), fetched 2026-11-10: PMR10 3 mOhm: 0.5 W at 70 C ambient, +/-150 ppm/C; body L 2.00 W 1.20, electrode b 0.75+/-0.25 for 3 mOhm.
- PRIMARY LAND (Rohm PMR10, "Land pattern example"): A gap 0.8, B overall 3.4, C pad width 1.3, D pad length 1.3 (mm). Two 1.3 x 1.3 pads, 0.8 gap.
- DEAD END: fscdn.rohm.com .../pmr10ez-e.pdf 404; rohm.com/datasheet/PMR10EZPFV3L00/pmr-e 403; mouser datasheet fetch not attempted after mouser timeouts.
- DEAD END: Panasonic AOA0000C307.pdf guessed URL 404.
### R10 candidates (DK US, 2026-11-10)
| MPN | DK PN (CT) | R/tol/P/TCR | Body | Stock | @10 | @100 | Lead | URL |
|---|---|---|---|---|---|---|---|---|
| Eaton MSMA0805R0030FSM | 283-MSMA0805R0030FSMCT-ND | 3 mOhm 1 % 0.5 W +/-50 ppm, AEC-Q200 | 2.00x1.25, h 0.90 | 9,341 | $0.22100 | $0.14740 | 20 wk | https://www.digikey.com/en/products/detail/eaton-electronics-division/MSMA0805R0030FSM/16713397 |
| Yageo PA0805FRF470R003L | 13-PA0805FRF470R003LCT-ND | 3 mOhm 1 % 0.5 W +/-100 ppm, AEC-Q200 | 2.03x1.27, h 0.45 | not shown (page lists only substitute PA0805FRE470R003L 5,000) | $0.21700 | $0.14470 | 20 wk | https://www.digikey.com/en/products/detail/yageo/PA0805FRF470R003L/17010697 |
| Vishay WFC08053L000FE66 | 541-WFC08053L000FE66CT-ND | 3 mOhm 1 % 0.5 W +/-100 ppm, anti-sulfur foil | 2.10x1.40, h 0.60 | 3,420 | $0.35800 | $0.24180 | 35 wk | https://www.digikey.com/en/products/detail/vishay-dale/WFC08053L000FE66/15908482 |
- Primary PMR10EZPFV3L00 on DK (2026-11-10): RHM.003AJCT-ND, stock 80,963, @10 $0.60300, @100 $0.41160, 0.5 W, +/-150 ppm, 8 wk. URL via https://www.digikey.com/en/products/result?keywords=PMR10EZPFV3L00 (redirects to product page).
- LAND, Yageo PA series automotive datasheet (Jun. 24, 2026 V.11), https://yageogroup.com/content/datasheet/asset/file/PYU-PA0100_2512_51_ROHS (the DK datasheet link; covers PA0100-PA2512 despite the name), Table 7 / Fig. 10: PA0805 1.5-20 mOhm: A overall 4.60, B gap 1.00, C pad length 1.80, D pad width 1.44. 0805 TCR for 2-20 mOhm: +/-50 (E) available; 3 mOhm terminal b 0.35+/-0.20.
- LAND, Vishay WFC (Doc 30402, rev 19-Aug-2026) https://www.vishay.com/docs/30402/wfc.pdf: 0805 1-5 mOhm: a gap 0.80, b pad length 1.60, c pad width 1.45 (overall 4.00). 0805 5.1-40 mOhm: a 1.20, b 1.20, c 1.40 (overall 3.60).
- DEAD END: Eaton MSMA datasheet https://www.eaton.com/content/dam/eaton/products/electronic-components/resources/data-sheet/eaton-msma-automotive-smd-current-sense-resistor-metal-strip-data-sheet-elx1179.pdf : curl returned 000 (no response), WebFetch timed out 60 s.
- LAND, Eaton MSMA Technical Data ELX1179 (Effective June 2022), mirror https://datasheet.lcsc.com/datasheet/pdf/1d815f7028c8612ac47d461a0b033894.pdf?productCode=C5677855 (fetched 2026-11-10; Eaton's own URL unresponsive): "Recommended PCB layout - mm", MSMA0805 2-25 mOhm: A pad width 1.4, L gap 1.2, B pad length 1.15 (overall 3.5). MSMA0805 1-2 mOhm: A 1.4, L 0.7, B 1.15. Notes: "copper foil thickness of PCB needs 3 oz. minimum"; "resistance will change slightly after soldered; it is dependent on PCB pad size". 0805 3 mOhm: 1/2 W, +/-50 ppm, MnCu; terminal C 0.40+/-0.30 for R>=2.
### R10 fit analysis (Rohm land: gap 0.8, pads 1.3 L x 1.3 W, overall 3.4)
- Vishay WFC0805 (1-5 mOhm rec.: gap 0.80, pad 1.60 x 1.45, overall 4.00): same gap; Rohm pads 0.3 mm shorter and 0.15 narrower than Vishay's; body 1.40 wide vs 1.30 pad. Mounts; closest electrical match (same gap).
- Eaton MSMA0805 (gap 1.2, pad 1.15 x 1.4, overall 3.5): overall nearly same, gap 0.4 smaller on Rohm land -> copper under body, resistance shifts slightly (their note 3). Mounts; not their recommended land.
- Yageo PA0805 (gap 1.00, pad 1.80 x 1.44, overall 4.60): Rohm land much shorter overall (3.4 vs 4.6). Mounts; weakest land match.
### R72/R73/R75 (20 mOhm) and R74 (50 mOhm) primaries, Panasonic ERJ-6BW
- DK 2026-11-10 (datasheet link https://industrial.panasonic.com/cdbs/www-data/pdf/RDN0000/AOA0000C313.pdf, rev 29-Sep-23):
| MPN | DK PN (CT) | Stock | @10 | @100 | Lead | Spec |
|---|---|---|---|---|---|---|
| ERJ-6BWFR020V | P.02AQCT-ND | 41,559 | $0.37400 | $0.25530 | 15 wk | 0.5 W, 1 %, TCR 0/+200 ppm (15-100 mOhm), 2.00x1.25, h 0.75, AEC-Q200 Grade 0 |
| ERJ-6BWFR050V | P17581CT-ND | 162,077 | $0.37400 | $0.25530 | 15 wk | same |
  URLs: https://www.digikey.com/en/products/result?keywords=ERJ-6BWFR020V and ...=ERJ-6BWFR050V (redirect to product pages).
- PRIMARY LAND, Panasonic "Surface Mount Resistors Land Pattern" (04 Dec. 2012) page 5 of https://industrial.panasonic.com/cdbs/www-data/pdf/RDN0000/AOA0000C90.pdf: "High power (double-sided resistive elements structure) type" ERJ6BW 2012/0805: a gap 0.9, b overall 3.2 to 3.8, c pad width 1.1 to 1.4 (so pad length 1.15-1.45). Main ERJ BW datasheet says land pattern is in "data files".
- DEAD END: WebSearch for Panasonic ERJ6BW land pattern gave only generic table snippets; resolved via AOA0000C90.pdf above.
### 20/50 mOhm candidates, DK US 2026-11-10 (URLs: https://www.digikey.com/en/products/result?keywords=<MPN>, redirect to product page)
| MPN | DK PN (CT) | Spec | Stock | @10 | @100 | Lead |
|---|---|---|---|---|---|---|
| Vishay WSLP0805R0200FEA | 541-10035-1-ND | 20 mOhm 1 % 0.5 W +/-75 ppm, 2.03x1.27, h 0.58 | 21,942 | $0.69800 | $0.51230 | 21 wk |
| Vishay WSLP0805R0500FEA | 541-10040-1-ND | 50 mOhm 1 % 0.5 W +/-75 ppm, 2.03x1.27, h 0.58 | 27,136 | $0.69800 | $0.51230 | 21 wk |
| Bourns CRF0805-FZ-R020ELF | CRF0805-FZ-R020ELFCT-ND | 20 mOhm 1 % 0.5 W +/-50 ppm, 2.00x1.25, h 0.80 | 42,446 | $0.23900 | $0.15980 | 18 wk |
- DEAD END: Bourns CRF0805-FZ-R050ELF: DK "did not return any results" (not a DK item).
- Search-snippet-only (not fetched): Yageo PE0805FRF470R02L / R05L, Ohmite LVT08R0200FER, LVK08R050FER, Bourns CFN0805-FX-R020ELF, Stackpole CSRT0805FT50L0 (DK non-stock).
- LAND, Vishay WSLP (Doc 30122, rev 09-Sep-2024) https://www.vishay.com/docs/30122/wslp.pdf p.2: WSLP0805 0.005-0.1 Ohm: a pad length 1.02, b pad width 1.27, l gap 0.50 (overall 2.54). Body 2.03x1.27, terminal T 0.381+/-0.254. TCR +/-75 ppm for 7-500 mOhm.
- LAND, Bourns CRF (REV. 09/26) https://www.bourns.com/docs/Product-Datasheets/CRF.pdf: CRF0805 0.5 W, 1-25 mOhm, +/-50 ppm. Recommended Solder Pad Layout 2-25 mOhm: A pad width 1.4, B pad length 1.15, L gap 1.2 (overall 3.5) [identical to Eaton MSMA0805]. Terminal C 0.40+/-0.20 for 2-25 mOhm.
| Yageo PE0805FRF470R05L | 13-PE0805FRF470R05LCT-ND | 50 mOhm 1 % 0.5 W +/-100 metal film | not stated (substitute PE0805FRM470R05L 2,389) | $0.87600 | $0.60560 | 20 wk |
| Yageo PE0805FRF470R02L | 13-PE0805FRF470R02LCT-ND | 20 mOhm 1 % 0.5 W +/-100 metal film | not stated (substitute FRM 1,742) | $0.87600 | $0.60560 | 20 wk |
| KOA UR73V2ATTD50L0F | 2019-UR73V2ATTD50L0FCT-ND | 50 mOhm 1 % 0.5 W +/-75 thick film, 2.00x1.25, h 0.70 | 9,704 | $0.39100 | $0.26670 | 13 wk |
| Vishay RCWE080550L0FNEA (REJECT: 0.25 W) | 541-2725-1-ND | 50 mOhm 1 % 0.25 W +/-200 | 3,735 | $0.16300 | $0.10040 | 19 wk |
- DEAD END: UR73V2ATTD20L0F not on DK. Rohm UCR10EVHFSR050 rejected (1/3 W, NFND per search snippet). Bourns CRL0805-FW-R050ELF rejected (1/4 W, obsolete per snippet).
| KOA UR73VD2ATTD20L0F | 2019-UR73VD2ATTD20L0FCT-ND | 20 mOhm 1 % 0.5 W +/-75 thick film, 2.00x1.25, h 0.70 | 3,868 | $0.36900 | $0.25160 | 13 wk |
- KOA UR73V datasheet https://www.koaspeer.com/pdfs/UR73V.pdf (11/05/25): UR73V 2A 0.5 W, +/-75 for 39-100 mOhm (and 25m/50m available); UR73VD 2A 0.5 W, +/-75 for 15-36 mOhm. No land pattern in datasheet.
- LAND, KOA Appendix B "pad dimensions" (04/15/26) https://www.koaspeer.com/pdfs/Appendix_B.pdf p.1 (figure: A gap, B overall, C pad width, D pad length): UR73V 2A: A 1.2, B 3.4, C 1.3, D 1.1. UR73VD 2A (20-36 mOhm): A 0.8, B 3.4, C 1.3, D 1.3. UR73VD 2A (10-18 mOhm): 0.6/3.4/1.3/1.4.
### 20/50 mOhm fit analysis (Panasonic ERJ6BW land: gap 0.9, overall 3.2-3.8, width 1.1-1.4)
- KOA UR73VD2ATTD20L0F (gap 0.8, overall 3.4, 1.3 x 1.3 pads): inside Panasonic's ranges, gap within 0.1 mm. FITS AS-IS (best match).
- Bourns CRF0805-FZ-R020ELF (gap 1.2, overall 3.5, pads 1.15 x 1.4): overall and width inside Panasonic's range; gap 0.3 mm narrower on Panasonic land. Mounts; near match.
- Vishay WSLP0805 (gap 0.50, overall 2.54, pads 1.02 x 1.27): Panasonic land is 0.7-1.3 mm longer overall and 0.4 mm wider gap than Vishay recommends. Terminals (T 0.381) land on the pads (inner terminal edge ~0.63 mm from center vs Panasonic pad inner edge 0.45). Mounts; worst land match of the set.
- KOA UR73V2ATTD50L0F (gap 1.2, overall 3.4, pads 1.1 x 1.3): overall and width inside Panasonic's range; gap 0.3 mm narrower on Panasonic land. Mounts; best 50 mOhm option found.

## Q4 Precision 10 kOhm 0.1 % 0603 (DK US, 2026-11-10)
| MPN | DK PN (CT) | Stock | @10 | @100 | Spec | Lead | URL |
|---|---|---|---|---|---|---|---|
| Bourns CRT0603-BY-1002ELF | CRT0603-BY-1002ELFCT-ND | 66,734 | $0.07800 | $0.06440 | 0.1 %, +/-25 ppm, 0.1 W | 20 wk | https://www.digikey.com/en/products/result?keywords=CRT0603-BY-1002ELF |
| Susumu RG1608P-103-B-T5 | RG16P10.0KBCT-ND | 551,979 | $0.07700 | $0.06390 | 0.1 %, +/-25 ppm, 0.1 W | 18 wk | https://www.digikey.com/en/products/detail/susumu/RG1608P-103-B-T5/1240450 |
- Note: DK keyword-search page for RG1608P-103-B-T5 rendered a marketplace-style stub without stock; the product page (ID 1240450) gives the figures above.

## Recommendations
- Q1: LM66100DCKR stock 386 (unchanged), $0.251 @10, $0.1927 @100, 26 wk lead. Alternates: LM66100QDCKRQ1 (AEC-Q100, 5,822, $0.26/$0.1998, DCK package by its orderable name; pinout not checked against the Q1 datasheet) and LM66100DCKT (1,389, $0.78/$0.6208). Other distributors not checked (Mouser timed out, Octopart/Findchips 403).
- Q2: Murata GRM155R71H103KA88D (primary), Samsung CL05B103KB5NNNC (secondary). TPS22917 sole CT requirement: VCT rating MIN 7 V. No 10 nF C0G 0402 found at DK.
- Q3: R10 -> Vishay WFC08053L000FE66 (same 0.80 gap) or Eaton MSMA0805R0030FSM (more stock, +/-50 ppm, gap 1.2). R72/R73/R75 -> KOA UR73VD2ATTD20L0F (fits as-is). R74 -> KOA UR73V2ATTD50L0F (gap 1.2 vs 0.9).
- Q4: both confirmed in stock.

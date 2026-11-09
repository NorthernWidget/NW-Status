COMPLETE

# Resistor primary and secondary parts, Digi-Key US, 2026-11-09

Input: `2026-11-09-resistor-bom-lines.tsv`, plus the planned lines (R21 1M 0603; R13 to the 180k 0603 line; R22/R69/R70/R71 charger dividers on the dual land; 2k line removed, R15 on 1k 0402).

## Lines

| value | footprint | refs | primary MPN | primary maker | primary DK CT | primary stock | primary lead | primary $1/$100 | primary tol | primary TCR | primary power | secondary MPN | secondary maker | secondary DK CT | secondary stock | secondary lead | secondary $1/$100 | secondary tol | secondary TCR | secondary power | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 220 | R0402 | O:R9 R53 R60 R64 R76 R77 R78 R79 R80 | CRGCQ0402F220R (kept) | TE | A129619CT-ND | 28,186 | 15 wk | $0.10000/$0.01490 | 1 % | 100 ppm | 0.063 W | RC0402FR-07220RL | Yageo | 311-220LRCT-ND | 1,193,867 | 24 wk | $0.10000/$0.01080 | 1 % | 100 ppm | 0.063 W | Kept: meets the bar (about 3,000 boards of stock). The Yageo has 40 times the stock if a large build is planned. |
| 3m | R0805 | O:R10 | PMR10EZPFV3L00 (kept) | Rohm | RHM.003AJCT-ND | 80,963 | 8 wk | $0.93000/$0.41160 | 1 % | 150 ppm | 0.5 W | MSMA0805R0030FSM | Eaton | 283-MSMA0805R0030FSMCT-ND | 9,341 | 20 wk | $0.35000/$0.14740 | 1 % | 50 ppm | 0.5 W | Both metal element, 2 terminations. Eaton body 2.00 x 1.25 mm. Check the Eaton land pattern against the Rohm one before treating it as a drop-in (metal-element shunts can want wider pads). |
| 27 | R0402 | O:R11 R34 R35 M:R3 M:R4 | RC0402FR-0727RL (kept) | Yageo | YAG3086CT-ND | 470,207 | 24 wk | $0.10000/$0.01080 | 1 % | 100 ppm | 0.063 W | ERJ-2RKF27R0X | Panasonic | P27.0LCT-ND | 371,675 | 15 wk | $0.11000/$0.01640 | 1 % | 100 ppm | 0.1 W | |
| 1k | R0402 (and R48 on R0402_0603, fitted 0402) | O:R12 O:R15 O:R48 | RC0402FR-071KL (kept) | Yageo | 311-1.00KLRCT-ND | 2,753,657 | 24 wk | $0.10000/$0.01080 | 1 % | 100 ppm | 0.063 W | ERJ-2RKF1001X | Panasonic | P1.00KLCT-ND | 5,028,631 | 15 wk | $0.10000/$0.01550 | 1 % | 100 ppm | 0.1 W | R48 (dual land) already used this MPN; the dual-land 1k line merges here. |
| 100 | R0402 | O:R14 | RC0402FR-07100RL (kept) | Yageo | 311-100LRCT-ND | 2,547,562 | 24 wk | $0.10000/$0.01080 | 1 % | 100 ppm | 0.063 W | RMCF0402FT100R | Stackpole | RMCF0402FT100RCT-ND | 2,013,674 | 22 wk | $0.10000/$0.00910 | 1 % | 100 ppm | 0.063 W | Panasonic ERJ-2RKF1000X shows 0 stock (from the Yageo page's substitute table), so Stackpole. |
| 91k | R0603 | O:R16 | ERJ-3EKF9102V (kept) | Panasonic | P91.0KHCT-ND | 52,578 | 15 wk | $0.10000/$0.01950 | 1 % | 100 ppm | 0.1 W | RC0603FR-0791KL | Yageo | 311-91.0KHRCT-ND | 89,106 | 24 wk | $0.10000/$0.01360 | 1 % | 100 ppm | 0.1 W | |
| 330k | R0603 | O:R17 O:R3 O:R62 | ERJ-3EKF3303V (kept) | Panasonic | P330KHCT-ND | 60,202 | 15 wk | $0.10000/$0.01950 | 1 % | 100 ppm | 0.1 W | RMCF0603FT330K | Stackpole | RMCF0603FT330KCT-ND | 50,607 | 22 wk | $0.10000/$0.00960 | 1 % | 100 ppm | 0.1 W | Yageo RC0603FR-07330KL showed only 2,659. |
| 20m | R0805 | O:R72 O:R73 O:R75 | ERJ-6BWFR020V (kept) | Panasonic | P.02AQCT-ND | 41,559 | 15 wk | $0.63000/$0.25530 | 1 % | 0/+200 ppm | 0.5 W | CRF0805-FZ-R020ELF | Bourns | CRF0805-FZ-R020ELFCT-ND | 44,020 | 18 wk | $0.37000/$0.15980 | 1 % | 50 ppm | 0.5 W | Bourns is metal element, 2.00 x 1.25 mm, 2 terminations; cheaper and better TCR than the Panasonic thick film. Stackpole CSR0805FK20L0 rejected (0.25 W). |
| 50m | R0805 | O:R74 | ERJ-6BWFR050V (kept) | Panasonic | P17581CT-ND | 162,077 | 15 wk | $0.63000/$0.25530 | 1 % | 0/+200 ppm | 0.5 W | WSLP0805R0500FEA | Vishay Dale | 541-10040-1-ND | 27,138 | 21 wk | $1.10000/$0.51230 | 1 % | 75 ppm | 0.5 W | Vishay's cut-tape number has the 541-xxxxx-1-ND form, not CT-ND. WSLP0805 body 2.03 x 1.27 mm (read on the 20m page). No Bourns CRF0805 50m at DK; Stackpole CSR0805FK50L0 rejected (0.25 W). |
| 1M | R0603 | O:R21 (new; replaces the 470k 5 % line) | ERJ-3EKF1004V | Panasonic | P1.00MHCT-ND | 1,284,750 | 15 wk | $0.10000/$0.01950 | 1 % | 100 ppm | 0.1 W | RC0603FR-071ML | Yageo | 311-1.00MHRCT-ND | 1,747,638 | 24 wk | $0.10000/$0.01360 | 1 % | 100 ppm | 0.1 W | New line. Both huge; Panasonic primary on the shorter lead. |
| 1.62M | R0603 | O:R4 O:R2 | CRCW06031M62FKEA (changed) | Vishay Dale | 541-1.62MHCT-ND | 12,095 | 21 wk | $0.10000/$0.01590 | 1 % | 100 ppm | 0.1 W | RC0603FR-071M62L | Yageo | 13-RC0603FR-071M62LCT-ND | 7,980 | 24 wk | $0.10000/$0.01360 | 1 % | 100 ppm | 0.1 W | Current RMCF0603FT1M62 is ±200 ppm, which fails the 100 ppm rule (60,715 in stock otherwise). Panasonic ERJ-3EKF1624V is Obsolete; CRCW06031M62FKEB is Discontinued at DigiKey; no Bourns. Stock is thin for both picks (fine for 2 per board). |
| 180k | R0402 | O:R5 O:R7 O:R65 O:R66 | RC0402FR-07180KL (kept) | Yageo | 311-180KLRCT-ND | 482,108 | 24 wk | $0.10000/$0.01080 | 1 % | 100 ppm | 0.063 W | ERJ-2RKF1803X | Panasonic | P180KLCT-ND | 312,976 | 15 wk | $0.10000/$0.01550 | 1 % | 100 ppm | 0.1 W | |
| 100k | R0402 (and R70 on R0402_0603, fitted 0402) | O:R23 O:R57 O:R58 O:R61 O:R63 O:R18 O:R19 O:R70 | RC0402FR-07100KL (kept) | Yageo | 311-100KLRCT-ND | 4,668,266 | 24 wk | $0.10000/$0.01080 | 1 % | 100 ppm | 0.063 W | ERJ-2RKF1003X | Panasonic | P100KLCT-ND | 3,520,780 | 15 wk | $0.10000/$0.01550 | 1 % | 100 ppm | 0.1 W | Charger-divider 100k joins this line. Ref R70 per the brief's order; the TSV has the 100k at R69 and the 200k at R70 (check which). |
| 180k | R0603 | O:R1 O:R8 O:R13 | ERJ-3EKF1803V (kept) | Panasonic | P180KHCT-ND | 21,218 | 15 wk | $0.10000/$0.01950 | 1 % | 100 ppm | 0.1 W | RMCF0603FT180K | Stackpole | RMCF0603FT180KCT-ND | 76,591 | 22 wk | $0.10000/$0.00960 | 1 % | 100 ppm | 0.1 W | R13 joins (182k line removed). TE CRG0603F180K is not stocked by DK (Marketplace only); Yageo RC0603FR-07180KL showed 1. |
| 820k | R0603 | O:R6 | RC0603FR-07820KL (kept) | Yageo | 311-820KHRCT-ND | 51,726 | 24 wk | $0.10000/$0.01360 | 1 % | 100 ppm | 0.1 W | ERJ-3EKF8203V | Panasonic | P820KHCT-ND | 54,119 | 15 wk | $0.10000/$0.01950 | 1 % | 100 ppm | 0.1 W | |
| 10k | R0402 | O:R67 R52 R45 R41 R86 R87 R54 R46 R47 R24 R25; M:R1 R2 R15 R16 R14 R17 R18 R19 R20 R21 | RC0402FR-0710KL (kept) | Yageo | 311-10.0KLRCT-ND | 6,860,194 | 24 wk | $0.10000/$0.01080 | 1 % | 100 ppm | 0.063 W | ERJ-2RKF1002X | Panasonic | P10.0KLCT-ND | 793,254 | 15 wk | $0.10000/$0.01550 | 1 % | 100 ppm | 0.1 W | Shared Okapi and Margay. |
| 1M | R0402 (and R22, R71 on R0402_0603, fitted 0402) | O:R55 O:R56 O:R59 O:R68 O:R22 O:R71 | RC0402FR-071ML (kept) | Yageo | 311-1.00MLRCT-ND | 698,637 | 24 wk | $0.10000/$0.01080 | 1 % | 100 ppm | 0.063 W | ERJ-2RKF1004X | Panasonic | P1.00MLCT-ND | 551,002 | 15 wk | $0.11000/$0.01640 | 1 % | 100 ppm | 0.1 W | Charger-divider 1M pair joins this line. ERJ-2RKF1004X stock is the single "In-Stock" figure on its page and matches the figure the Yageo page gives for it; re-check on order. |
| 330 | R0402 | O:R36 R37 R38 R39 R40 R42 R43 R44; M:R7 R9 R5 R6 R8 R11 R12 R13 | RC0402FR-07330RL (kept) | Yageo | 311-330LRCT-ND | 2,769,795 | 24 wk | $0.10000/$0.01080 | 1 % | 100 ppm | 0.063 W | ERJ-2RKF3300X | Panasonic | P330LCT-ND | 337,016 | 15 wk | $0.10000/$0.01550 | 1 % | 100 ppm | 0.1 W | Shared Okapi and Margay. |
| 5.1k | R0402 | O:R84 R85 R81 R82 R83; M:R31 R32 | RC0402FR-075K1L (kept) | Yageo | 311-5.10KLRCT-ND | 431,935 | 24 wk | $0.10000/$0.01080 | 1 % | 100 ppm | 0.063 W | ERJ-2RKF5101X | Panasonic | P5.10KLCT-ND | 831,362 | 15 wk | $0.11000/$0.01640 | 1 % | 100 ppm | 0.1 W | The TSV's two 5.1k rows (Okapi "5.1k", Margay "5.1K") are the same MPN; merged into one line. |
| 200k | R0402_0603, fitted 0402 | O:R69 (new value) | ERJ-2RKF2003X | Panasonic | P200KLCT-ND | 518,358 | 15 wk | $0.11000/$0.01640 | 1 % | 100 ppm | 0.1 W | RC0402FR-07200KL | Yageo | 311-200KLRCT-ND | 1,149,434 | 24 wk | $0.10000/$0.01080 | 1 % | 100 ppm | 0.063 W | New line. Panasonic primary on the shorter lead; Yageo would keep it in the same family as the other 0402 lines (owner's call). Ref R69 per the brief; see the 100k note. |
| 0 | R0402 | O:R51 | ERJ-2GE0R00X (changed) | Panasonic | P0.0JCT-ND | 14,161,449 | 15 wk | $0.10000/$0.00950 | jumper | n/a | 1/10 W (description) | RC0402JR-070RP | Yageo | YAG1279CT-ND | 1,368,528 | 24 wk | $0.10000/$0.01160 | jumper | n/a | not listed | Current RC0402JR-070RL shows 0 in stock (10,000 expected 09-Nov-2026). RC0402JR-070RP is the same Yageo jumper in another packaging suffix. Jumper current rating not read on either page (UNVERIFIED). |
| 130k | R0603 | O:R20 M:R10 | ERJ-3EKF1303V (changed) | Panasonic | P130KHCT-ND | 59,870 | 15 wk | $0.10000/$0.01950 | 1 % | 100 ppm | 0.1 W | RMCF0603FT130K | Stackpole | RMCF0603FT130KCT-ND | 79,761 | 22 wk | $0.10000/$0.00960 | 1 % | 100 ppm | 0.1 W | Current RC0603FR-07130KL shows 0 in stock (5,000 expected 09-Nov-2026, backorder). Shared Okapi and Margay. |
| 232 | R0402 | O:R26 R27 R28 R29 | RC0402FR-07232RL (kept) | Yageo | YAG3063CT-ND | 27,105 | 24 wk | $0.10000/$0.01080 | 1 % | 100 ppm | 0.063 W | RMCF0402FT232R | Stackpole | RMCF0402FT232RCT-ND | 280,714 | 22 wk | $0.10000/$0.00910 | 1 % | 100 ppm | 0.063 W | |
| 464 | R0402 | O:R30 R31 R32 R33 | RC0402FR-07464RL (kept) | Yageo | 311-464LRCT-ND | 62,653 | 24 wk | $0.11000/$0.01140 | 1 % | 100 ppm | 0.063 W | ERJ-2RKF4640X | Panasonic | P464LCT-ND | 13,443 | 15 wk | $0.10000/$0.01550 | 1 % | 100 ppm | 0.1 W | |
| 10k 0.1 % | R0603 | O:R49 O:R50 M:R22 M:R23 M:R24 | CRT0603-BY-1002ELF (confirmed) | Bourns | CRT0603-BY-1002ELFCT-ND | 66,794 | 20 wk | $0.10000/$0.06440 | 0.1 % | 25 ppm | 0.1 W | RG1608P-103-B-T5 | Susumu | RG16P10.0KBCT-ND | 552,197 | 18 wk | $0.11000/$0.06390 | 0.1 % | 25 ppm | 0.1 W | One line for both boards. Bourns primary confirmed (thin film, current Margay part). Panasonic ERA-3AEB103V **cannot be the secondary**: 0 in stock, 55 wk lead. Susumu has 8 times Bourns' stock and a shorter lead, so on the numbers alone it would be primary; Vishay TNPW060310K0BEEA (199,404, 14 wk, $0.28/$0.19210, 0.21 W) is a third option. |

## Notes on the line set

- Dual land (R0402_0603): all four charger-divider parts and R48 are fitted **0402**. The 1M pair (R22, R71), the 100k and R48's 1k join existing 0402 lines, and only the 200k is a new line. The 0402 parts have the same tolerance and TCR as their 0603 counterparts here; their power is 0.063 W (Yageo) or 0.1 W (Panasonic). Voltage rating was not read on any page (UNVERIFIED); check it against the charger input if that is above about 25 V.
- Lines removed against the TSV: 182k 0603 (R13 moved to 180k 0603), 143k dual (R22 is now 1M), 470k 5 % 0603 (R21 is now 1M 0603 1 %), the two dual-land 100k and 200k rows and the dual 1k row (merged as above), and the duplicate Margay 5.1K row (merged). No 2k line was present in the TSV.
- R69/R70: the brief lists the dividers as "1M, 200k, 100k, 1M" for R22/R69/R70/R71, which puts 200k at R69 and 100k at R70. The TSV has R69 = 100k and R70 = 200k. The rows follow the brief; check which is intended.
- Substitute tables on Digi-Key pages can include Marketplace stock (TE CRG0603F180K showed 195,000 there but is not stocked by Digi-Key). Every chosen part was read on its own page.
- Lead time is Digi-Key's "Manufacturer Standard Lead Time". Stock is the page's "In-Stock" figure, read 2026-11-09.

## Count

25 lines. 20 keep the current part as primary (including the merged precision 10k, which keeps Margay's Bourns). 3 change primary: 1.62M (TCR), 0 ohm (out of stock), 130k (out of stock). 2 are new values: 1M 0603 and 200k 0402. Every line has an in-stock secondary from a different manufacturer.

## Pages checked (log)

All pages fetched 2026-11-09 with WebFetch through `https://www.digikey.com/en/products/result?keywords=<MPN>`, which lands on the product detail page for an exact MPN. Stock is the page's "In-Stock" figure (all packagings); lead time is "Manufacturer Standard Lead Time"; prices are cut tape at 1 and 100.

- DEAD END: `https://www.digikey.com/en/products/detail/bourns-inc/CRT0603-BY-1002ELF/3438893` (guessed product ID) redirected to an unrelated Nichicon capacitor page. Do not guess numeric IDs; use the keyword search URL.
- CRT0603-BY-1002ELF: Active; 66,794; 20 wk; $0.10000/$0.06440; 0.1 %, 25 ppm, 0.1 W. Substitutes shown: ERA-3AEB103V 0 stock; RT0603BRD0710KL 0 stock; TNPW060310K0BEEA 199,404.
- CRGCQ0402F220R (TE, A129619CT-ND): Active; 28,186; 15 wk; $0.10000/$0.01490; 1 %, 100 ppm, 0.063 W.
- PMR10EZPFV3L00 (Rohm, RHM.003AJCT-ND): Active; 80,963; 8 wk; $0.93000/$0.41160; 1 %, 150 ppm, 0.5 W, metal element. No substitutes shown.
- RC0402FR-0727RL (YAG3086CT-ND): Active; 470,207; 24 wk; $0.10000/$0.01080; 1 %, 100 ppm, 0.063 W. Substitute shown: CRCW0402270RFKED 63,802 (sic, as read; the MPN for 27 ohm is CRCW040227R0FKED, check).
- RC0402FR-071KL (311-1.00KLRCT-ND): Active; 2,753,657; 24 wk; $0.10000/$0.01080; 1 %, 100 ppm. Substitutes: ERJ-2RKF1001X 5,028,631; CR0402-FX-1001GLF 938,102.
- RC0402FR-07100RL (311-100LRCT-ND): Active; 2,547,562; 24 wk; $0.10000/$0.01080; 1 %, 100 ppm. Substitutes: ERJ-2RKF1000X 0 stock; ERJ-2RHD1000X 53,221.
- ERJ-3EKF9102V (P91.0KHCT-ND): Active; stock read as 52,578 on the product block but 92,578 in the substitutes table (re-check); 15 wk; $0.10000/$0.01950; 1 %, 100 ppm, 0.1 W. Substitutes: RC0603FR-0791KL 89,106; CRCW060391K0FKEA 70,784.
- DEAD END: keyword search for ERJ-3EKF3303V returned a 2-result list without stock. Detail page `https://www.digikey.com/en/products/detail/panasonic-electronic-components/ERJ-3EKF3303V/1746380` worked: P330KHCT-ND; Active; 60,202; 15 wk; $0.10000/$0.01950; 1 %, 100 ppm, 0.1 W. Substitutes: RC0603FR-07330KL 2,659; CRCW0603330KFKEA 3,170; RMCF0603FT330K 50,607; CRG0603F330K 28,561.
- ERJ-6BWFR020V (P.02AQCT-ND): Active; 41,559; 15 wk; $0.63000/$0.25530; 1 %, 0/+200 ppm, 0.5 W, thick film. Substitute: Stackpole CSR0805FK20L0 6,833 (Direct).
- ERJ-6BWFR050V (P17581CT-ND): Active; 162,077; 15 wk; $0.63000/$0.25530; 1 %, 0/+200 ppm, 0.5 W, thick film. No substitutes listed.
- RMCF0603FT1M62 (RMCF0603FT1M62CT-ND): Active; 60,715; 22 wk; $0.10000/$0.01230; 1 %, **±200 ppm** (fails the 100 ppm rule), 0.1 W. No substitutes listed.
- RC0402FR-07180KL (311-180KLRCT-ND): Active; 482,108; 24 wk; $0.10000/$0.01080; 1 %, 100 ppm. Substitutes: ERJ-2RKF1803X 312,976; CRCW0402180KFKED 79,344; CRG0402F180K 70,000.
- RC0402FR-07100KL (311-100KLRCT-ND): Active; 4,668,266; 24 wk; $0.10000/$0.01080; 1 %, 100 ppm. Substitutes: ERJ-2RKF1003X 3,520,780; CRCW0402100KFKED 4,085,699.
- ERJ-3EKF1803V (P180KHCT-ND): Active; 21,218; 15 wk; $0.10000/$0.01950; 1 %, 100 ppm, 0.1 W. Substitutes: RC0603FR-07180KL 1; CRCW0603180KFKEA 97,547; RMCF0603FT180K 76,591; CRG0603F180K 195,000.
- RC0603FR-07820KL (311-820KHRCT-ND): Active; 51,726; 24 wk; $0.10000/$0.01360; 1 %, 100 ppm, 0.1 W. Substitutes: ERJ-3EKF8203V 54,119; CR0603-FX-8203ELF 37,203.
- RC0402FR-0710KL (311-10.0KLRCT-ND): Active; 6,860,194; 24 wk; $0.10000/$0.01080; 1 %, 100 ppm. Substitutes: ERJ-2RKF1002X 793,254; ERJ-2RHD1002X 26,664.
- RC0402FR-071ML (311-1.00MLRCT-ND): Active; 698,637; 24 wk; $0.10000/$0.01080; 1 %, 100 ppm. Substitutes: ERJ-2RKF1004X 551,002; CR0402-FX-1004GLF 178,784.
- RC0402FR-07330RL (311-330LRCT-ND): Active; 2,769,795; 24 wk; $0.10000/$0.01080; 1 %, 100 ppm. Substitutes: ERJ-2RKF3300X 337,016; CRCW0402330RFKED 131,907; CR0402-FX-3300GLF 2,074.
- RC0402FR-075K1L (311-5.10KLRCT-ND): Active; 431,935; 24 wk; $0.10000/$0.01080; 1 %, 100 ppm. Substitutes: ERJ-2RKF5101X 831,362; CRCW04025K10FKED 375,788; CR0402-FX-5101GLF 45,180.
- ERA-3AEB103V (P10KDBCT-ND): Active; **0 in stock** (5,000 past due, estimated 26-Oct-2026); **55 wk**; $0.10000/$0.06040; 0.1 %, 25 ppm, 0.1 W. Substitutes in stock: CRT0603-BY-1002ELF 66,794; Susumu RG1608P-103-B-T5 552,197; TNPW060310K0BEEA 199,404; RNCF0603BTE10K0 54,317; MCT06030D1002BP500 13,148; RG1608N-103-B-T5 18,912; RT0603WRB0710KL 2,080.
- RC0402JR-070RL (311-0.0JRCT-ND): Active; **0 in stock** (10,000 expected 09-Nov-2026); 24 wk; $0.10000/$0.00570; jumper, 1/16 W. Substitutes: ERJ-2GE0R00X 14,161,449; RMCF0402ZT0R00 4,666,593; AC0402JR-070RL 3,444,926; CRCW04020000Z0ED 2,451,291; RC0402JR-070RP 1,368,528; RC0402FR-070RL 208,929.
- RC0603FR-07130KL (311-130KHRCT-ND): Active; **0 in stock** (5,000 expected 09-Nov-2026, backorder); 24 wk; $0.10000/$0.01360; 1 %, 100 ppm, 0.1 W. Substitutes: ERJ-3EKF1303V 59,870; RMCF0603FT130K 79,761; CRCW0603130KFKEA 47,639; CRG0603F130K 0.
- RC0402FR-07232RL (YAG3063CT-ND): Active; 27,105; 24 wk; $0.10000/$0.01080; 1 %, 100 ppm. Substitutes: RMCF0402FT232R 280,714; CRCW0402232RFKED 9,176.
- RC0402FR-07464RL (311-464LRCT-ND): Active; 62,653; 24 wk; $0.11000/$0.01140; 1 %, 100 ppm. Substitutes: ERJ-2RKF4640X 13,443; CRCW0402464RFKED 10,292.
- ERJ-3EKF1624V: **Obsolete**, bulk only (10-ERJ-3EKF1624V-ND), no stock or lead shown. Not usable. Its listed substitute is RMCF0603FT1M62 (200 ppm).
- RC0603FR-071M62L (13-RC0603FR-071M62LCT-ND): Active; 7,980; 24 wk; $0.10000/$0.01360; 1 %, 100 ppm, 0.1 W. Substitutes: CRCW06031M62FKEB 18,890; CRCW06031M62FKEA 12,095; RC1608F1624CS 0.
- RC0603FR-071ML (311-1.00MHRCT-ND): Active; 1,747,638; 24 wk; $0.10000/$0.01360; 1 %, 100 ppm, 0.1 W.
- ERJ-3EKF1004V (P1.00MHCT-ND): Active; 1,284,750; 15 wk; $0.10000/$0.01950; 1 %, 100 ppm, 0.1 W.
- RC0402FR-07200KL (311-200KLRCT-ND): Active; 1,149,434; 24 wk; $0.10000/$0.01080; 1 %, 100 ppm, 0.063 W. Substitutes: ERJ-2RKF2003X 518,358; CR0402-FX-2003GLF 427,500.
- ERJ-2RKF2003X (P200KLCT-ND): Active; 518,358; 15 wk; $0.11000/$0.01640; 1 %, 100 ppm, 0.1 W.
- DEAD END: keyword search for CRCW06031M62FKEA and CRCW06031M62FKEB returned result lists without stock; detail pages used instead.
- CRCW06031M62FKEA (`/en/products/detail/vishay-dale/CRCW06031M62FKEA/1175032`, 541-1.62MHCT-ND): Active; 12,095; 21 wk; $0.10000/$0.01590; 1 %, 100 ppm, 0.1 W.
- CRCW06031M62FKEB (`/en/products/detail/vishay-dale/CRCW06031M62FKEB/5071362`, 541-CRCW06031M62FKEBCT-ND): **Discontinued at DigiKey**; 18,890; lead "unavailable due to constrained supply"; $0.10000/$0.01400; 1 %, 100 ppm. Not chosen (not Active at DK).
- DEAD END: CR0603-FX-1624ELF (Bourns 1.62M): no results on Digi-Key.
- ERJ-3EKF1303V (P130KHCT-ND): Active; 59,870; 15 wk; $0.10000/$0.01950; 1 %, 100 ppm, 0.1 W.
- RMCF0603FT130K (RMCF0603FT130KCT-ND): Active; 79,761; 22 wk; $0.10000/$0.00960; 1 %, 100 ppm, 0.1 W.
- ERJ-2GE0R00X (P0.0JCT-ND): Active; 14,161,449; 15 wk; $0.10000/$0.00950; jumper; 1/10 W per description.
- RC0402JR-070RP (YAG1279CT-ND): Active; 1,368,528; 24 wk; $0.10000/$0.01160; jumper; power not listed.
- RMCF0402ZT0R00 (RMCF0402ZT0R00CT-ND): Active; 4,666,593; 22 wk; $0.11000/$0.00450; jumper; 1/16 W per description.
- DEAD END: keyword search for RG1608P-103-B-T5 gave a 2-result list without stock; detail URL `/en/products/detail/susumu/RG1608P-103-B-T5/1240450` to fetch.
- TNPW060310K0BEEA (TNP10.0KAACT-ND): Active; 199,404; 14 wk; $0.28000/$0.19210; 0.1 %, 25 ppm, 0.21 W, thin film.
- RG1608P-103-B-T5 (`/en/products/detail/susumu/RG1608P-103-B-T5/1240450`, RG16P10.0KBCT-ND): Active; 552,197; 18 wk; $0.11000/$0.06390; 0.1 %, 25 ppm, 0.1 W, thin film.
- RC0603FR-0791KL (311-91.0KHRCT-ND): Active; 89,106; 24 wk; $0.10000/$0.01360; 1 %, 100 ppm, 0.1 W.
- RMCF0603FT330K (RMCF0603FT330KCT-ND): Active; 50,607; 22 wk; $0.10000/$0.00960; 1 %, 100 ppm, 0.1 W.
- DEAD END: CRG0603F180K is **not stocked by Digi-Key** (the 195,000 in substitute tables is Marketplace stock; T&R only, 720,000 minimum). Lesson: substitute-table stock can include Marketplace; every chosen part below was checked on its own page.
- ERJ-3EKF8203V (P820KHCT-ND): Active; 54,119; 15 wk; $0.10000/$0.01950; 1 %, 100 ppm, 0.1 W.
- ERJ-2RKF1002X (P10.0KLCT-ND): Active; 793,254; 15 wk; $0.10000/$0.01550; 1 %, 100 ppm, 0.1 W.
- ERJ-2RKF27R0X (P27.0LCT-ND): Active; "In-Stock: 371,675" (one extraction also saw 531,675 in a substitutes table; the verbatim quote gives 371,675); plus 160,000 from a Marketplace supplier (WEC), not counted; 15 wk; $0.11000/$0.01640; 1 %, 100 ppm, 0.1 W.
- ERJ-2RKF1001X (P1.00KLCT-ND): Active; 5,028,631; 15 wk; $0.10000/$0.01550; 1 %, 100 ppm, 0.1 W.
- DEAD END: keyword search for CRCW0402100RFKED returned a 4-result list without stock.
- ERJ-2RKF1803X (P180KLCT-ND): Active; 312,976; 15 wk; $0.10000/$0.01550; 1 %, 100 ppm, 0.1 W.
- ERJ-2RKF1003X (P100KLCT-ND): Active; verbatim "In-Stock: 3,520,780" (matches the figure the RC0402FR-07100KL page gave for this part); 15 wk; $0.10000/$0.01550; 1 %, 100 ppm, 0.1 W.
- ERJ-2RKF1004X (P1.00MLCT-ND): Active; verbatim "In-Stock: 551,002" (matches the figure the RC0402FR-071ML page gave for this part; the first extraction attributed it to a substitute, so treat as likely but re-check on order); 15 wk; $0.11000/$0.01640; 1 %, 100 ppm, 0.1 W.
- RMCF0402FT100R (RMCF0402FT100RCT-ND): Active; 2,013,674; 22 wk; $0.10000/$0.00910; 1 %, 100 ppm, 0.063 W.
- ERJ-2RKF3300X (P330LCT-ND): Active; 337,016; 15 wk; $0.10000/$0.01550; 1 %, 100 ppm, 0.1 W.
- ERJ-2RKF5101X (P5.10KLCT-ND): Active; 831,362; 15 wk; $0.11000/$0.01640; 1 %, 100 ppm, 0.1 W.
- ERJ-2RKF4640X (P464LCT-ND): Active; 13,443; 15 wk; $0.10000/$0.01550; 1 %, 100 ppm, 0.1 W.
- RMCF0402FT232R (RMCF0402FT232RCT-ND): Active; 280,714; 22 wk; $0.10000/$0.00910; 1 %, 100 ppm, 0.063 W.
- RC0402FR-07220RL (311-220LRCT-ND): Active; 1,193,867; 24 wk; $0.10000/$0.01080; 1 %, 100 ppm, 0.063 W.
- CSR0805FK20L0 (Stackpole, CSR0805FK20L0CT-ND): Active; 6,833 (factory stock 43,000); 19 wk; $0.54000/$0.20620; 1 %, 200 ppm, **0.25 W** (fails the 0.5 W rule). Rejected.
- CSR0805FK50L0 (CSR0805FK50L0CT-ND): Active; 10,459; 19 wk; $0.39000/$0.16870; 1 %, 200 ppm, **0.25 W**. Rejected.
- DEAD END: PMR10EZPFU20L0 and PMR10EZPFU50L0 (guessed Rohm MPNs): no results.
- DEAD END: CRCW0603180KFKEA keyword search gave a 3-result list without stock (detail `/en/products/detail/vishay-dale/CRCW0603180KFKEA/1174923` not fetched; Stackpole used instead).
- RMCF0603FT180K (RMCF0603FT180KCT-ND): Active; 76,591; 22 wk; $0.10000/$0.00960; 1 %, 100 ppm, 0.1 W.
- WebSearch "digikey 0805 current sense resistor 0.02 ohm 1% 0.5W..." found CRF0805-FZ-R020ELF, WSLP0805R0200FEA, PE0805FRF470R02L, D1MPC0805QR020FF-T5.
- CRF0805-FZ-R020ELF (`/en/products/detail/bourns-inc/CRF0805-FZ-R020ELF/6210980`, CRF0805-FZ-R020ELFCT-ND): Active; 44,020; 18 wk; $0.37000/$0.15980; 1 %, 50 ppm, 0.5 W, metal element, 2.00 x 1.25 mm, 2 terminations.
- PE0805FRF470R02L (`/en/products/detail/yageo/PE0805FRF470R02L/5914072`, 13-PE0805FRF470R02LCT-ND): Active; **no stock figure for this part** (1,742 is the substitute PE0805FRM470R02L); 20 wk; $1.34000/$0.60560; 1 %, 100 ppm, 0.5 W. Not chosen.
- WSLP0805R0200FEA (`/en/products/detail/vishay-dale/WSLP0805R0200FEA/9758303`, 541-10035-1-ND): Active; 21,942; 21 wk; $1.10/$0.51230; 1 %, 75 ppm, 0.5 W, metal element, 2.03 x 1.27 mm.
- DEAD END: CRF0805-FZ-R050ELF: no results (Bourns has no 50 mOhm in that series at DK).
- PE0805FRF470R05L (13-PE0805FRF470R05LCT-ND): Active; no stock figure for the part (256 is the substitute); 20 wk; $1.34000/$0.60560. Not chosen.
- WSLP0805R0500FEA (541-10040-1-ND): Active; 27,138; 21 wk; $1.10000/$0.51230; 1 %, 75 ppm, 0.5 W, metal element.
- MSMA0805R0030FSM (`/en/products/detail/eaton-electronics-division/MSMA0805R0030FSM/16713397`, 283-MSMA0805R0030FSMCT-ND): Active; 9,341; 20 wk; $0.35000/$0.14740; 1 %, 50 ppm, 0.5 W, metal element, 2.00 x 1.25 mm, 2 terminations.
- PA0805FRF470R003L (`/en/products/detail/yageo/PA0805FRF470R003L/17010697`, 13-PA0805FRF470R003LCT-ND): Active; no stock figure for this part (5,000 is the substitute PA0805FRE470R003L); 20 wk; $0.34000/$0.14470; 1 %, 100 ppm, 0.5 W. Not chosen.
- WFC08053L000FE66 (`/en/products/detail/vishay-dale/WFC08053L000FE66/15908482`, 541-WFC08053L000FE66CT-ND): Active; 3,420; 35 wk; $0.56000/$0.24180; 1 %, 100 ppm, 0.5 W, metal foil, 2.10 x 1.40 mm. Not chosen (larger body, low stock, long lead).
- ERJ-3EKF9102V re-check, verbatim: "In-Stock: 52,578"; plus "40,000 In Stock" from Other Suppliers (Marketplace). The 92,578 seen earlier is the sum. Digi-Key's own stock is 52,578.
- CRT0603-BY-1002ELF re-check, verbatim: Composition "Thin Film"; "In-Stock: 66,794"; lead "20 Weeks".

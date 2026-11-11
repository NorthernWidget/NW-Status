# Sourcing brands: what the 2026-11-11 survey found

Andy's criteria, in his order (2026-11-11):
1. geopolitical resilience: multiple sources, and countries that keep exporting through instability;
2. quality across wide temperature ranges;
3. consistent quality, with no ruined batches at low volume;
4. workers' rights.

Standing preferences: Digi-Key first, and Würth Elektronik as a preferred brand.

Four survey reports sit beside this file, with a verification of the part table (`2026-11-11-part-problems-verification-agent-report.md`) and a USB-UART bridge survey (`2026-11-11-usb-uart-bridge-agent-report.md`), each with every fact cited and a log of the sources checked:
- `2026-11-11-passives-agent-report.md`
- `2026-11-11-semiconductors-agent-report.md`
- `2026-11-11-connectors-agent-report.md`
- `2026-11-11-geopolitics-labor-agent-report.md`

Numbers below are the agents' unless marked "checked", meaning I confirmed them against the BoM or the KiCad files in this session. The six standing rules were adopted by Andy on 2026-11-11.

## Part problems on the boards (act on these first)

| Board | Part | Problem | Fix | Source |
|---|---|---|---|---|
| Okapi | U38 MLX90393**S**LW (checked) | rated −20 °C | E grade MLX90393ELW-ABA-011-RE: same package and address, −40 °C | semiconductors, verification |
| Okapi | U44 VEML6030 (checked) | rated −25 °C, storage also −25 °C | no cold grade; Vishay VEML6031X00 (−40 °C) needs a new footprint | semiconductors, verification |
| Okapi | U4 LT3652**E**DD (checked) | guaranteed from 0 °C; −40 °C "assured by design" | I grade LT3652IDD#PBF, guaranteed to −40 °C, same package | semiconductors, verification |
| Okapi, Margay | BT1 Linx BAT-HLD-012-SMT (checked in both KiCad files) | obsolete; the active -TR twin is rated −30 °C | the -TR version now; a −40 °C holder to find | connectors |
| Okapi | C&K PCM12SMTR (checked in the KiCad files) | obsolete (2,726 left); rated −20 °C | a −40 °C switch to find | connectors |
| Okapi | J8 JST S2B-PH-SM4-TB | **corrected:** JST's datasheet says −40 to +105 °C; −25 °C is Digi-Key's listing | none needed | connectors, verification |
| Okapi, Margay | On Shore screw terminals | drawing says −40 °C, Digi-Key −30 °C; maker publishes no plant or quality certificate | ask On Shore, or a documented second source | connectors |
| Margay | Würth 693063010911 SD holder | rated −25 °C | **kept** (Andy, 2026-11-11): used in deployments at −40 °C | SD survey |
| Okapi, Margay | FTDI FT231XQ-R (U23, U2) | single source; 0 in stock at Digi-Key (2026-11-11); UK order of November 2024 followed by one approving a sale to Willow Vision (in force 1 July 2026, completion unverified) | CP2102N proposed as second source (board change) | semiconductors, verification, bridge survey |
| Okapi | 2021 BoM rows | MCP23018 listed as TI (it is Microchip, checked), still so in the v0.8 KiCad files; 12 other rows fixed in v0.8 | U41's manufacturer field | semiconductors, passives, verification |

Already fixed: the TXC crystal (−20 °C, obsolete) was replaced by ECS in Project-Okapi 47a944d.

## What the boards depend on

| Category | Main brands, by BoM lines |
|---|---|
| Passives | Yageo (25 of 45 on Margay, 61 of 143 on Okapi; thick-film resistors), Murata (15 and 39), then small counts |
| Semiconductors | TI (26 of 61 lines, 43 %), Microchip 10, Diodes 7, ADI 5 |
| Connectors and electromechanical | On Shore (2 + 4), C&K, GCT, Amphenol FCI, Linx/TE, Molex |

## Findings by criterion

**1. Geopolitics.** Every recorded case of a government stopping finished parts or materials from leaving was Chinese: gallium and germanium (2023), a US-specific ban (2024), and Nexperia's Dongguan back end (October–November 2025). Japan's 2019 controls aimed at Korea are the one other case. Japan, Taiwan, Malaysia, Thailand and the US lost output to fires, floods, storms and COVID rules, but kept exporting. The longest outages came from single sites: the Renesas fire took about four months to recover, the Thailand floods about three for Western Digital. A second source protects against both kinds of failure only if it is assembled in a different country, not merely sold under a different brand.

Exposure on the boards:
- **GCT** (USB-C connectors) makes everything in mainland China.
- **Diodes Inc.** is US-owned, but most of its plants are in China.
- **FTDI** is the single source for the USB interface.
- **Nexperia** has been split since 2025.
- **TI** mostly runs its own fabs and assembly sites. **TE** and **Molex** spread production widely. **Vishay** builds in Israel, the Czech Republic, Portugal, India and Mexico. **Murata** builds in Japan and Southeast Asia.

**2. Wide temperature.** The problems are in the part table above. On brands: TI parts checked on the BoMs are all rated −40 °C. Murata's automotive GCM capacitors on both boards are AEC-Q200. Würth's AEC-Q200 inductors stop at −40 °C, with no margin.

**3. Consistency.** No recall or quality escape from 2022 to 2026 was found for any brand. The evidence is thin, not clean. What protects a small buyer: buying only from authorized distributors (Digi-Key), keeping obsolete parts off the BoM, using automotive grades (whose change notices are stricter), and getting change notices.

**4. Workers' rights.**
- **RBA tiers with audit commitments:**
  - Full: Microchip, ST, NXP, onsemi.
  - Regular: Murata, Vishay, Molex, TI, ADI, Infineon, Renesas, Epson.
  - Tier not stated: TDK, Panasonic, KYOCERA AVX, Bourns, TE, Amphenol, Nexperia, Toshiba.
- **Not members:** Yageo/KEMET, Würth, Diodes, Taiyo Yuden, Walsin, JST, Hirose, Phoenix, Rohm and Digi-Key. KEMET, Würth and Diodes follow the RBA Code without being members. Würth also runs a reporting channel under Germany's supply-chain law.
- **KnowTheChain 2025 forced-labor scores (out of 100):** NXP 36, ST 20, TI 12, Microchip 11, ADI 11, Panasonic 10, Murata 10, Infineon 8, Amphenol 8, Kyocera 6. Every one sits low.
- **Documented cases:** the 2019–2021 Malaysia forced-labor cases name NXP, Infineon, ST and Vishay, and ended in remedy through the RBA. ASPI (2020) lists TDK, Toshiba and Panasonic among companies linked to Uyghur labor transfers through suppliers.

**Würth, on the same evidence:**
- **Temperature:** good automotive-grade inductors, though they stop at −40 °C.
- **Supply:** it does not publish where its catalog lines are made. One known inductor plant is in Shenyang, China.
- **Labor:** not an RBA member, but it follows the RBA Code and runs a legal reporting channel.
- **Field record:** the SD holder has wintered at −40 °C in Andy's deployments, which no survey can supply.

## Standing rules (adopted, Andy 2026-11-11)

1. Approve two sources for each part that matters, assembled in different countries.
2. Hold buffer stock of the single-source and long-lead parts only. How many months of builds to hold is still Andy's number to set.
3. Require −40 °C ratings on every part for field boards, and use automotive (AEC-Q) grades where they exist at Digi-Key.
4. Keep obsolete parts off the BoM. Enable Digi-Key's end-of-life alerts, which fire only for parts bought through the account.
5. Record country of origin from the Digi-Key packing slip for each lot. Digi-Key shows it per lot, not on the product page.
6. On labor: where two parts are otherwise equal, prefer a maker with an RBA Regular or Full membership.

## Open questions

- The tiers of the eight RBA members whose tier is not stated, and why Samsung Electro-Mechanics, which announced it joined in 2023, is not on the current list.
- Where Würth makes the four Okapi inductors and its connectors.
- Who owns RAMXEED (the FRAM maker) and where its wafers are made.
- Country-level production shares for passives and connectors (paid reports only).
- Whether the 2026 replacement tariffs on Chinese parts took effect.

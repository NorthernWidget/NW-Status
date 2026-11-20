# Lineage of the Northern Widget open-hardware designs

Status 2026-11-20. Each Northern Widget board traced back to the openly licensed work it came from: earlier Northern Widget boards, and the Arduino, SparkFun, Adafruit and Particle designs and Eagle libraries. Eight agents read the repositories, their git histories and the Eagle files; a ninth checked the evidence and closed gaps. Every link cites a file and line or a commit in `raw/`. Confidence: **verified** means a file or the git history shows it outright; **likely** means strong indirect evidence (shared parts and net names).

## Upstream licenses

| Source | License | Report |
|---|---|---|
| Arduino board designs (Uno, Mega 2560, Leonardo, Nano) | CC BY-SA 4.0 on current schematics; CC BY-SA 2.5 on the 2007 Eagle reference designs | `raw/upstream.md` |
| SparkFun Eagle libraries | CC BY-SA 4.0 since December 2014, CC BY-SA 3.0 before | `raw/upstream.md` |
| SparkFun MS5803-14BA breakout (Casey Kuhns) | SparkFun's CC BY-SA frame is carried in the derived files; the breakout's own release not checked | `raw/tlog-tp.md` |
| Adafruit Feather board designs | CC BY-SA 3.0 | `raw/upstream.md` |
| Adafruit Eagle library (`adafruit.lbr`) | no license stated | `raw/upstream.md`, `raw/critic.md` C3 |
| Particle `hardware-libraries` (Eagle) | CC BY-SA, with an exception for commercial products using it as a reference design | `raw/critic.md` |
| microBuilder.eu Eagle library | public domain | `raw/margay.md` |
| MightyCore (firmware and board definitions only) | GPL v2 and LGPL | `raw/margay.md`, `raw/upstream.md` |

CC BY-SA 4.0 licenses copyright only; Section 2(b)(2) says "Patent and trademark rights are not licensed". GPL v3 Section 11 carries an explicit patent grant from each contributor.

## The logger line

```
Arduino reference designs (CC BY-SA)          SparkFun and Adafruit Eagle libraries (CC BY-SA)
        |                                                  |  (used throughout)
ALog BottleLogger, 2012 design, public 2013-09-11, CC BY-SA 3.0
        |-- ALog LogMega, 2013 (spliced with the Arduino Mega 2560)     verified
        |-- ALog Shield, 2016 (Arduino Uno shield)                      verified
        |
network-logger-umn "Logger v2", 2017-03 (Bobby Schulz; GPL v3)
        |   135 of 137 part lines and all 92 net names carried over      verified
TLog BETA 2017-07 -> TLog Mrk 1.x 2018-02 (LGPL v3)                     verified
        |   21 of 26 devicesets and 22 net names shared                  likely
Margay "Blackfoot", 2018-02-28 (CC BY-SA from 2018-06-28)
        |   40 of 44 net names of Margay v2 in the first Okapi schematic; "Keep convention w/Margay"   likely
Okapi ("Resnik"), 2018-10-23 (CC BY-SA 4.0 from the repository's first day)
```

Margay also descends from the BottleLogger through the shared ALog circuit (likely; 14 devicesets and 10 net names in common).

## Each design

| Design | First public, license | Northern Widget parent | Outside open sources, verified |
|---|---|---|---|
| ALog BottleLogger | 2013-09-11, CC BY-SA 3.0 (4.0 from 2018-06-16) | – | Arduino reference-design libraries (likely); SparkFun and Adafruit libraries |
| ALog LogMega | 2013-09-11, CC BY-SA 3.0 (4.0 on GitHub 2018) | BottleLogger | Arduino Mega 2560; SparkFun and Adafruit libraries |
| ALog Shield | 2016-03-17, CC BY-SA 4.0 | BottleLogger | Arduino Uno shield form factor; SparkFun and Adafruit libraries |
| TLog | 2017-07, LGPL v3 | network-logger-umn Logger v2 | SparkFun and Adafruit libraries |
| Margay | 2018-02-28, CC BY-SA 4.0 (MIT for its first four months) | TLog, BottleLogger (likely) | SparkFun libraries; Adafruit SD-card part; microBuilder USB-C |
| Okapi | 2018-10-18, CC BY-SA 4.0 | Margay v2 (likely) | Adafruit Feather footprint and symbol (byte-identical to `adafruit.lbr`); Particle B-SoM connector; SparkFun libraries |
| TP-DownHole | 2017-01-26, CC BY-SA 4.0 | – | Direct modification of SparkFun's MS5803-14BA breakout |
| TP-DownHole-No2 | 2017, CC BY-SA 4.0 | TP-DownHole | SparkFun MS5803 breakout (through TP-DownHole) |
| Walrus | 2018-10-27, CC BY-SA 4.0 | TP-DownHole (Longbow Mountable) | SparkFun MS5803 breakout (grandparent); SparkFun libraries |
| Apis | 2019-07-10, CC BY-SA 4.0 | Walrus and Haar family (possible) | SparkFun libraries |
| Haar | 2019-03-26, CC BY-SA 4.0 | Walrus and Apis family (possible) | SparkFun parts in the house library |
| Liasis | CC BY-SA 4.0 from 2018-06-28 (MIT before) | Dyson / Monarch | SparkFun libraries |
| Libelle | CC BY-SA 4.0 from 2018-06-28 (MIT before) | Dyson / Monarch | SparkFun libraries |
| Ophiura | CC BY-SA 4.0 from 2018-12-18 (MIT before) | Heptapod | SparkFun libraries |
| SCA100T inclinometer | 2016-04-26, CC BY-SA 4.0 | – | SparkFun libraries, including the sensor's own part |
| Instrumentation amplifier | CC BY-SA 4.0 (2018-06-17) | its own v1 | SparkFun libraries |
| 18650 Li-ion holder | 2020-02-04, CC BY-SA 4.0 | – | SparkFun power symbols |
| Lux (MAX44009) | CC BY-SA 4.0 (2018-06-17) | its own 3.3 V version | SparkFun libraries and design rules |
| RockBLOCK Feather | CC BY-SA 4.0 | Okapi's RockBlock breakout (byte-identical) | – |

The KiCad conversions of Margay and Okapi take every part from NW-Cold-Silicon, which carries the same SparkFun, Adafruit and Particle content forward.

## License problems found

1. **Margay's license file held the wrong license for four and a half years.** From 2018-06-28 to 2023-01-22 (296967a), the file named `CC-BY-SA-4.0.txt` contained the text of CC BY-NC-SA 4.0 (NonCommercial). The README and GitHub said CC BY-SA throughout.
2. **TLog is LGPL v3 only**, though it carries SparkFun CC BY-SA parts. Its parent, network-logger-umn, is GPL v3 with no hardware license.
3. **Several designs began under MIT** and moved to CC BY-SA in 2018: Margay, Liasis, Libelle, Ophiura.
4. **The Adafruit Eagle library states no license.** Okapi's Feather footprint and symbol come from it unchanged, and NW-Cold-Silicon's `PROVENANCE.md` does not record that origin.
5. **Some repositories declare no license on GitHub:** 10 of the 80 in the NorthernWidget organization have none, and TP-DownHole reads NOASSERTION, though its `LICENSE.md` names CC BY-SA 4.0.
6. **ALog Shield's schematic frame still says CC BY-SA 3.0**, where its LICENSE file says 4.0.

## Not yet traced

- Thirteen public repositories with board files: ALog_telemeter, Project-Raven, Project-Longbow, Project-Astron, Project-Calypso, Project-Tally, Project-ThermalStake, ICSP-half-size-adapter, Project-Monarch__Archive, AtlasShield, MaxBotix-Helper, Break44 and ALog-BottleLogger2 (quick looks in `raw/critic.md` C1 and after).
- Derivatives outside both organizations, in RTGS-Lab: Project-Kestrel's main logger (Bobby Schulz, house library and Particle parts) and "Haar v2.0" (`raw/critic.md`).
- The likely links (Margay from TLog, Okapi from Margay) rest on shared parts and net names; no file says "based on" in words.

## Files

`raw/` holds one report per group (`alog`, `tlog-tp`, `margay`, `okapi`, `sensors-a`, `sensors-b`, `small`), the upstream licenses (`upstream.md`), and the completeness check (`critic.md`), each with the sources it checked, dead ends included.

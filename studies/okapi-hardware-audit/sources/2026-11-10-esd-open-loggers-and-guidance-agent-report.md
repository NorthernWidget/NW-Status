COMPLETE

# ESD and surge protection: open loggers, guidance, field evidence

Started 2026-11-10. Each finding: source title, date, URL, exact quote. [INFERENCE] marks my own reading.

## Findings

### SDI-12 specification
- SDI-12 v1.3, "A Serial-Digital Interface Standard for Microprocessor-Based Sensors", July 18, 2005, https://www.sdi-12.org/archives.php?file_id=8 (PDF fetched, read locally).
  - Sec. 3.2.1: "Transient protection is recommended on the SDI-12 bus. See appendix A for a suggested SDI-12 transient protection method."
  - Sec. 3.3: "SDI-12 does not require voltage limiting for transient protection in the sensor. Transient protection is, however, recommended."
  - Appendix A (figure, read from rendered page A-1): data line = spark gap (<1 kV) at the bus, 510 ohm series, 0.0033 uF to ground, 200k to ground, 1N4737 7.5 V zener, 510 ohm series to CMOS 3-state buffer. 12 V line: series diode, 1.5KE20A TVS, 10 uF, then 5 V regulator.

## Sources checked (incl. dead ends)

### EnviroDIY Mayfly (verified from Eagle .sch XML netlists, fetched 2026-11-10)
Source: https://github.com/EnviroDIY/EnviroDIY_Mayfly_Logger/tree/master/hardware (files Mayfly_v0p5b/Mayfly_v0p5b.sch, Mayfly_v1p0/Mayfly_v1p0_revA3_public.sch, Mayfly_v1p1/Mayfly_v1p1_revB.sch). Parsed with python ElementTree; nets traced by pinref.
- v0.5b: no TVS/ESD part anywhere. Only "protection-like" parts: Schottky diodes (20V 1A SOD-123, D1-D4) used as power ORing, and ferrites FB1 (3.3V->VCC of ADS1115) / FB2 (GND->GNDA), which are analog-supply filtering, not protection.
- v1.0 revA3 and v1.1 revB: D6 = SP0503BAHTG (Littelfuse 3-channel TVS array) with pin 1 GND, pin 2 VUSB, pin 3 D-, pin 4 D+. That is the only TVS. USB only.
- v1.1 Grove/sensor ports: SDA/SCL go MCU pin -> J14/J15/J16 directly (net SDA: U2, R7 pull-up, U1, ADS1115, header, J14, SHT40, J15, J16, PCA9536). Digital D4/D5/D6/D7/D10/D11 nets go MCU pin -> header -> Grove J10-J13 with no series resistor and no clamp. Analog AIN0-AIN3 go ADS1115 pin -> J8/J9 directly. Battery (BAT1) and solar (V_SOLAR, D2 MSS2P2 Schottky into BQ24074) have Schottky diodes but no TVS.
- [INFERENCE] Mayfly's design protects the port a person plugs into by hand (USB) and leaves every field-cable port to the MCU/ADC internal ESD diodes.

### METER Group: "Lightning Surge and Grounding Practices" (PDF, file metadata create 2025-09-18, earlier 2017-04-27; no printed date)
URL: https://publications.metergroup.com/Sales%20and%20Support/METER%20Environment/Website%20Articles/Lightning-surge-grounding-practices.pdf
- "In one test, a lightning strike at a distance of almost 5 km from an installation induced an 80 volt (peak to peak) common mode spike on an insulated cable."
- "Generally speaking, it is the common mode voltage that most adversely affects product reliability. Poor grounding is usually the root cause for this class of failures."
- "WITHOUT A ROBUST GROUNDING SYSTEM, THERE IS NO WAY TO PROTECT AGAINST LIGHTNING SURGES"
- "METER soil sensors have built-in circuitry, which protect them against common surge conditions. Installations in lightning-prone areas, however, require special precautions, especially when sensors are connected to a well-grounded Campbell Scientific logger."
- Differential-mode: "Most designers simply place a surge protection device (SPD) between the two conductors."

### METER / Environmental Biophysics: "The Scientific Instrumentation Museum of Horrors", Chris Chambers, 2015-04-22
URL: https://environmentalbiophysics.org/the-scientific-instrumentation-museum-of-horrors
- "Long cable runs act like lightning harvesting antennae."
- "The best thing to do is to keep the cables shorter and do not spread them out in lots of different directions."
- "The single most important thing you can do to prevent damage from animals is to protect your cables." (field failure mode other than electrical)

### Campbell Scientific CR350 manual: "Electrostatic discharge and lightning protection" (online help, no date)
URL: https://help.campbellsci.com/CR350/shared/installation/lightning.htm
- "All critical inputs and outputs on the data logger are protected."
- "To be effective, the earth ground lug must be properly connected to earth (chassis) ground."
- "Lightning strikes may damage or destroy the data logger, associated sensors and power supplies."

## Source log
- sdi-12.org v1.3 PDF: read OK
- Mayfly GitHub hardware .sch: read OK
- METER lightning PDF: read OK
- environmentalbiophysics museum of horrors: read OK
- Campbell CR350 lightning help: read OK
- onsetcomp/hobodataloggers ESD tech note: 404 after redirect (dead end)
- Search 'Cave Pearl ESD lightning': no Cave Pearl incident page surfaced (keep looking)
- Search 'EnviroDIY forum lightning Mayfly': no EnviroDIY thread surfaced

### Cave Pearl Project (Ed Mallon, Patricia Beddows)
- Site searches (thecavepearlproject.org ?s=static+discharge, ?s=lightning, ?s=ESD, ?s=cable+length): no post found that reports an ESD or lightning failure. "lightning" matched only the rain-gauge post; "ESD" matched 7 posts with no ESD text in snippets [probably substring match, not checked further].
- "Too Ugly to Steal & Too Heavy to Carry": Insights from a decade of rain gauge deployment, 2023-04-15, https://thecavepearlproject.org/2023/04/15/insights-from-a-decade-of-tipping-bucket-rain-gauge-deployment/
  - "After six years in service I'm surprised this rooftop unit hasn't been zapped by lightning." (photo caption)
  - Failures reported are environmental/mechanical: "RH sensors are so prone to failure that we no longer combine them with anything else."; leaf-cutter ants. Protection advice is corrosion: "Sand & coat those internal screw terminals" (grease, conformal, or nail polish).
- "Field Report 2016-07-09: I2C pressure sensors work on 20m long cables!", 2016-09-21, https://thecavepearlproject.org/2016/09/21/field-report-2016-07-09-i2c-pressure-sensors-work-on-20m-cables/
  - "with one on the end of an 18m cable, both sensors will read OK with 4K7 pull-ups if you lower the bus speed to 100 kHz"; "Slowing things down to 50kHz ... let's me extend that out to 25m". No protection components mentioned (fetch summary).
- "The e360: A DIY Classroom Data Logger for Science [2023]", 2023-12-01, https://thecavepearlproject.org/2023/12/01/the-e360-a-classroom-data-logger-for-science/
  - first 100k chars: no ESD/static mention; failures are bumps, solder bridges, DOA cheap parts: "Expect 15% of the parts from cheap suppliers like eBay or Amazon to be high drain, or simply DOA."; "Random logger quits are usually hardware connection or bus-timing related".
- [INFERENCE] Cave Pearl loggers run long I2C cables unprotected and the blog does not attribute failures to ESD or lightning; their deployments are mostly in caves/underwater, which limits lightning exposure.
- Cave Pearl site searches and 3 posts: read; no ESD/lightning failure reports found (negative result)

### Schematic audits (Eagle .sch XML, parsed 2026-11-10; script scratchpad/esd/scripts/parts.py plus raw grep for esd|tvs|prtr|usblc|tpd|pesd|sp05|smaj|smf|rclamp: zero hits in all six)
- Adafruit Feather M0 Adalogger, https://github.com/adafruit/Adafruit-Feather-M0-Adalogger-PCB (master, "Adafruit Feather M0 Adalogger.sch"): no TVS/ESD part. Only MBR120 Schottky VBUS<-VBAT.
- Adafruit Feather 32u4 Adalogger, https://github.com/adafruit/Adafruit-Feather-32u4-Adalogger-PCB: same; MBR120 only.
- Adafruit Feather RP2040 Adalogger, https://github.com/adafruit/Adafruit-Feather-RP2040-Adalogger-PCB (main): no TVS/ESD; PMEG2020AEA Schottky on VBUS, DMG3415 P-FET (battery/USB switchover).
- SparkFun OpenLog Artemis, https://github.com/sparkfun/OpenLog_Artemis Hardware/SparkFun_Artemis_OpenLog.sch: no TVS/ESD; Schottkys (BAT60A, BAT20J) for power ORing; CH340E USB bridge unprotected.
- Riffle (OpenWaterProject riffle_328 v0.1.8), https://github.com/OpenWaterProject/riffle_328 hardware/riffle_0.1.8.0/riffle-beta-0.1.8.sch: no TVS/ESD; 500 mA PTC fuse (L1) on VBUS; MBR120 Schottkys ORing VBUS/VBAT.
- ALog BottleLogger (Northern Widget), local /home/awickert/Dropbox/NorthernWidget/github/ALog-BottleLogger/ALog-BottleLogger.sch: no TVS/ESD; two PPTC "HALF-AMP" polyfuses F1, F2 on the EXT_3.3V and EXT_5V sensor-supply outputs; 27 ohm series resistors on USB D+/D- (FT231X); BAT54C used as a diode-OR for RTC_INT/MANUAL_LOG, not protection.
- [INFERENCE] Of the small open loggers checked, none puts a TVS on a sensor port; overcurrent (PTC) on supplies is the only field-facing protection seen (ALog, Riffle VBUS).
- OpenOBS (tedlanghorst/OpenOBS): no schematic files in the repo tree (only firmware, deploy GUI, documentation PDFs). Not audited.
- Adafruit 3 Adalogger, SparkFun OLA, Riffle, ALog-BottleLogger .sch: audited OK
- OpenOBS GitHub: no hardware files (dead end for schematic)

### Arduino MKR family (official schematic PDFs, docs.arduino.cc, rendered and read)
- MKR Zero ABX00012, https://docs.arduino.cc/resources/schematics/ABX00012-schematics.pdf (sheet dated 28/01/19, "MKRZero_V5.0"): D1 PRTR5V0U2X,215 (Nexperia 2-line USB ESD array with VBUS rail clamp) on USB D+/D-/VBUS; F2 MF-FSMF050X-2 (Bourns 0.5 A PTC) on VUSB; L2 BLM18PG471SN1D ferrite; PMEG2005EL Schottky. Header I/O (A0-A6, I2C, SPI, UART) run from SAMD21 pins to J4/J5 with no clamps visible.
- MKR WAN 1310 ABX00029, https://docs.arduino.cc/resources/schematics/ABX00029-schematics.pdf (27/06/2019, "MKRWAN1310V3.0"): PRTR5V0U2X on USB at J1. Header I/O unprotected.
- [INFERENCE] Arduino's own pattern: one cheap ESD array + PTC on USB, nothing on user I/O.
- Arduino MKR Zero & MKR WAN 1310 schematic PDFs: read OK (vector text, rendered)

### Particle Boron
- Boron Datasheet, https://docs.particle.io/reference/datasheets/b-series/boron-datasheet/ (fetched 2026-11-10): absolute max table "ESD Susceptibility HBM (Human Body Mode)" 1 kV; "The Boron contains highly sensitive electronic circuitry and is an Electrostatic Sensitive Device (ESD)."; "ESD precautions should be implemented on the application board where the Boron is mounted."
- Schematic https://github.com/particle-iot/boron eagle/boron-v1.00/boron-v1.00.sch (parsed): no TVS, ESD array, or PTC anywhere; USB goes to connector directly; only diode D4 VBUS_NRF->VIN.
- [INFERENCE] Particle pushes ESD responsibility to the carrier board explicitly; 1 kV HBM is low (typical MCU pins are 2 kV HBM; IEC 61000-4-2 contact level 4 is 8 kV, a different and harsher model).
- Particle Boron datasheet + Eagle sch v1.00: read OK

### METER HYDROS 21 (CTD) GEN 1 Integrator Guide, rev 01, 11.2021
URL: https://library.metergroup.com/Integrator%20Guide/18281_HYDROS21(CTD)_GEN1.pdf (pdftotext)
- "Figure 2 provides a low-impedance variant of the recommended SDI-12 specification." Figure 2 labels (text layer, topology not checked visually): L1 10UH, R1 510, 220PF, R2 100K on the DATA line.
- "SURGE CONDITIONS: Sensors have built-in circuitry that protects them against common surge conditions. Installations in lightning-prone areas, however, require special precautions, especially when sensors are connected to a well-grounded third-party logger."
- "The sensor protection circuitry may be insufficient if the data logger is improperly powered or grounded."
- "Improperly protected cables can lead to severed cables or disconnected sensors. Cabling issues can be caused by many factors, including rodent damage, driving over sensor cables, tripping over the cable, not leaving enough cable slack during installation, or poor sensor wiring connections."
- [INFERENCE] The sensor end carries its own series-R/RC protection; the logger side is expected to match the SDI-12 Appendix A style circuit.
- METER HYDROS 21 Gen1 integrator guide PDF: read OK
- Search EnviroDIY forum lightning: no envirodiy.org thread surfaced (dead end so far)

### EnviroDIY forum field-failure evidence
- "Could Mayfly have been damaged during storm event?", envirodiy.org forum, OP Cheryl Nolan 2021-09-03, replies neilh20, https://www.envirodiy.org/topic/could-mayfly-have-been-damaged-during-storm-event/ (fetch summary with short quotes; not read raw)
  - OP: unit stopped recording on "8/12/2021", the day of a storm; ran "for more than a year and working well all along". Setup: CTD in remote headwater stream, Pelican box on bank on an iron pipe, sensor cable "partly underground", solar + battery. No visible burn.
  - neilh20 (reply #15852): "any form of excess voltage on processor pins can cause the device to fail"; lightning protection is "1) protecting the processor with electrical clamps and diodes, and 2) diverting the electrical energy into the ground."
  - Outcome: thread judged the processor failed (no records at all); OP planned to swap in a spare. Cause never confirmed. [INFERENCE] this is circumstantial: a storm-coincident MCU death on an unprotected sensor port, not a diagnosed surge failure.
- Site searches envirodiy.org ?s=lightning (2 hits, irrelevant), ?s=static (36 hits, none relevant on page 1), ?s=surge (9 hits; "Major Set Back" reply 15301 suggests board touching metal caused "a jolt in the power on the USB"), ?s=fried (13 hits; above thread found there).
- envirodiy.org searches lightning/static/surge/fried + storm thread: read

### IEC levels (secondary sources; the standards themselves are paywalled)
- PR electronics "4000 EMC specifications - immunity" V2R0, https://www.prelectronics.com/filearkiv/PDF-FTP/Certificates/EMC/4000_EMC_data.pdf : IEC 61326-1 column lists ESD IEC 61000-4-2 "4 kV / 8 kV Contact / Air"; I/O signal surge IEC 61000-4-5 "1 kV / 2 kV, Diff. / Comm."; DC power surge "1 kV / 2 kV, Diff. / Comm."; I/O burst 2 kV. [UNVERIFIED against the standard; vendor transcription.]
- NTS, "EN 61326-1: EMC Emissions/Immunity Requirement Changes for Laboratory Equipment", https://nts.com/?p=5171 (search snippet only): ESD levels went from "±4 kV contact discharge and ±4 kV air discharge in EN 61636-1:2006 to ±4 kV contact discharge and ±8 kV air discharge in EN 61326-1:2013" (sic, 61636 typo in source).
- Dead ends: VDE preview of IEC 61326-1 ed1 1997 (TOC only, no table); IEC webstore preview of 61000-6-2 (returned HTML, not PDF). The commonly cited ">30 m" cable-length applicability of surge tests on signal ports is NOT verified from any fetched source. [UNVERIFIED]

### TI, "Protecting Field Transmitters from Surge Transients", German Aguirre, SSZT962, September 2017 (PDF reissued 2023)
URL: https://ti.com/lit/pdf/sszt962
- "As with all systems with an externally exposed interface, your system must have International Electrotechnical Commission (IEC) 61000-4-2 ESD and IEC 61000-4-5 surge protection. The IEC 61000-4-5 surge standard is the most severe transient immunity test in terms of higher current and longer duration, and its application is often limited to long signal and power lines."
- "A typical requirement for industrial field transmitters is to be tested for (and to withstand) 25A (8/20µs) at 1kV, with a 42Ω coupling network during the IEC 61000-4-5 surge immunity test."
- "Typical TVS diodes clamp at voltages too high to protect your system"; recommends "low and flat clamping voltage" TVS (TVS3300 marketing).
- PR electronics EMC data: read; NTS 61326 page: snippet only; VDE/IEC previews: dead ends
- TI SSZT962: read OK

### NXP UM10204 "I2C-bus specification and user manual", Rev. 7.0, 1 October 2021
URL: https://www.nxp.com/docs/en/user-guide/UM10204.pdf (pdftotext)
- Sec. 7.3 "Series protection resistors": "As shown in Figure 45, series resistors (Rs) of, for example, 300 Ω can be used for protection against high-voltage spikes on the SDA and SCL lines (resulting from the flash-over of a TV picture tube, for example). If series resistors are used, designers must add the additional resistance into their calculations for Rp and allowable bus capacitance."
- "Series resistors Rs are optional. They protect the I/O stages of the I2C-bus devices from high-voltage spikes on the bus lines, and minimize crosstalk and undershoot of the bus line signals."
- Table 10 note [5]: the 300 ns tf vs 250 ns tof margin "allows series protection resistors (Rs) to be connected between the SDA/SCL pins and the SDA/SCL bus lines ... without exceeding the maximum specified tf."
- NXP UM10204 rev 7: read OK
- Wurth ANP121 PDF URL: returned HTML (dead end via curl)
- Sensirion SHTxx ESD PDF via mouser: timeout (retry)

### Campbell Scientific, "SunSentry Surge Protection: Applying Industry Best Practices for Reliable, Cost-Effective Solar Monitoring", application note, Revision 09/2026
URL: https://s.campbellsci.com/documents/us/technical-papers/sunsentry-surge-protection.pdf (pdftotext)
- "Protecting electronic equipment from a direct lightning strike is extremely difficult, and the immense energy of a lightning strike can overwhelm most protection devices. However, the probability of a direct lightning strike to a monitoring station is relatively low. A more likely scenario is a lightning strike in close proximity to the station."
- FIELD CASE: "a cable and rain gauge from a general environmental monitoring meteorological station (not a SunSentry station). Both devices were catastrophically damaged by a nearby lightning strike." "This rain gauge was located a few meters from the meteorological station. The lightning jumped from a nearby fence to the rain gauge, destroying it. Because the rain gauge was not grounded, the electrical energy traveled through the cable to the meteorological station, causing damage to the station."
- "Energy from a nearby lightning strike can also jump to a cable, causing the cable to act as an antenna and conduct surge energy toward the station, even when the cable is shielded and grounded."
- CR1000Xe: "built-in surge protection on all measurement, control, and power terminals. The CR1000Xe also uses fast-acting gas-discharge tubes to protect the data lines." Meets "IEC 61000-4-5 standard for class 4 surge immunity"; table: "I/O signal/control (unsymmetrical) ±1 kV line-to-line, ±2 kV line-to-ground".
- [INFERENCE] This is the commercial ceiling for a professional logger (GDT + TVS, earth lug, class-4 surge); it is designed for mains-adjacent solar plants, not a 3-cell battery logger.
- Campbell SunSentry surge app note (rev 09/2026): read OK
- NOAA DCP best practices PDF: curl failed (retry via WebFetch)

### NETLAKE (EU COST Action) "Guidelines for automated monitoring system development", fact sheet "005 How to cope with lightning" (PDF created 2016-08-31; Lake Erken, Sweden authors' experience)
URL: https://eprints.dkit.ie/512/1/AMSD%20005%20how%20to%20cope%20with%20lightning.pdf
- "Lightning induced voltage transients are much more common than direct lightning strikes. In our experience at Lake Erken, these occur multiple times each year, while direct strikes have rarely occurred."
- "However ESD transients are also induced in sensor cables. The longer the cable the greater the risk."
- "If the system data logger does not have in built transient protection, it is recommended that sensors with leads longer than 3-4 m be protected with some type of transient protection."
- "Underwater sensors are in effect submerged in the ground, so even long cable lengths (i.e. thermistor strings) should be safe."
- "ESD transients are more problematic on land based sites since instruments tend to be spread out more providing longer cables to collect transients."
- Campbell loggers "use both gas discharge tubes and Zener diodes as part of the wiring panel transient protection circuitry."
- Long AC/telecom cables grounded elsewhere: "Direct connection of the AC power ground to the local station ground sets up the perfect situation for transients"
- NETLAKE AMSD 005 lightning fact sheet: read OK

### NOAA NWS Manual 30-4106, "Lightning Protection, Grounding, Bonding, Shielding, and Surge Protection Requirements", April 25, 2017
URL: https://www.weather.gov/media/directives/030_pdfs/pd03041006curr.pdf (186 pp., pdftotext)
- Sec 2.6: "Transient protection should be provided for all signal, data, and control lines, both at facility entrances and at entrances to electronic equipment. This protection will limit transients at the equipment entrance to below the equipment susceptibility level."
- Table 2-3 "Conducted Landline Transient Levels" (source FAA-STD-019d), 8x1000 us waveform, lines not in ferrous conduit: 1,000 transients at 100V/50A; 500 at 500V/100A; 50 at 750V/375A; 5 at 1000V/1000A. In ferrous conduit: 50V/10A ... 100V/50A.
- Sec 2.6.4: suppressors replaceable, ground bus bar bonded to earth electrode with "No. 4 AWG or larger copper wire".
- [INFERENCE] This is facility-grade guidance (staffed NWS sites, landlines between buildings); its levels are far beyond what a board-level TVS on a battery logger can absorb, but it documents the design philosophy: protect at every cable entrance, keep the protector replaceable, give it a real earth.
- NWS 30-4106 (2017): read relevant sections OK

### Lessons-learned papers on low-cost environmental loggers (negative result for ESD/lightning)
- Chan et al. 2020, "Low-cost electronic sensors for environmental research: pitfalls and opportunities", Progress in Physical Geography, doi:10.1177/0309133320956567, PDF https://researchonline.lse.ac.uk/id/eprint/106639/1/0309133320956567.pdf . grep for lightning/static/ESD/electrostatic/surge/transient: zero relevant hits. Failures reported: FreeStation "Promisingly, there have been zero sensor failures in field deployment. Occasional data loss has occurred due to faulty SD cards, loss of power or external interference from animals (rabbits in the UK; crocodiles in Burkina Faso!) or extreme weather." and cites commercial loggers "report failure rates of 7–27% (Mickley et al., 2018)". A well logger design failed from exposure: "overly susceptible to humidity and insects, resulting in failure or heavy degradation of all units."
- Filhol et al. 2023, "A new approach to ... " (open-source IoT met network on Svalbard glaciers), Frontiers in Environmental Science, doi:10.3389/fenvs.2023.1085708, PDF https://www.frontiersin.org/journals/environmental-science/articles/10.3389/fenvs.2023.1085708/pdf . No ESD/lightning mention. "Out of 15 nodes, 6 collected data for the whole year." Failures: "1) a hardware design problem on the version V1 nodes, 2) an unknown instability leading the node to stop all activities."
- [INFERENCE] In the published low-cost-logger literature found, failures are dominated by moisture/ingress, power, SD cards, animals, and unexplained lockups; ESD and lightning are not reported as identified causes. This does not show they never occur (an unexplained death is often never diagnosed).
- Chan 2020, Filhol 2023: read via pdftotext; no ESD/lightning (negative)

### Arduino Forum, "Surviving (nearby) lightning strike", started 2018-06-18 by Smajdalf (read via Discourse JSON https://forum.arduino.cc/t/532268.json; HTML page returned 403 to WebFetch)
URL: https://forum.arduino.cc/t/surviving-nearby-lightning-strike/532268
- FIELD CASE: well water-level sensor, 20 wires of different length into a well, 74HC4052 muxes, 100 nF 16 V ceramic blocking caps per wire. "Everything worked well until a storm not so long ago - after the storm I started to get wrong data. I dissected the device and found two of the 100 u nF caps damaged (they are short circuit) and two of the multiplexers damaged". "only 2 out of 20 caps and 2 out of 6 multiplexers were damaged. So the circuit 'nearly survived'." Later: no evidence of a strike closer than ~200 m.
- MorganS 2018-06-20: "I think the TVS diode is good. If you can place the TVS just after a protection resistor, that helps. Even if the resistor is a very low value, like 10 ohms."
- DVDdoug 2018-06-18: "There are protection diodes inside the Arduino, but they are low-current ... Normally, you can add a series resistor to limit the current (and the diodes limit the voltage)"
- MarkT 2018-06-20: "use spark gaps, TVS, series resistor, the works - ultimately you can't prevent lightning damage, but being more robust means surviving more events that aren't direct hits."
- No follow-up reporting whether a fix worked (20 posts read).
- Arduino forum 532268 via JSON: read OK; switchdoc thread: HTTP 400 (dead end); hobodataloggers smart-sensor-cable-fix: 404 (dead end)

### TI, "Protecting RS-485 Interfaces Against Lethal Electrical Transients", SLLA292A, May 2009, revised March 2011
URL: https://www.ti.com/lit/pdf/slla292 (WebFetch saved PDF, pdftotext)
- Table 1 "EMC Test Requirements" ("a typical set of requirements and their applied test levels for industrial applications"): Burst IEC 61000-4-4 power ±4 kV, signal ±2 kV (level 4); Surge IEC 61000-4-5 signal lines ±0.5 kV (level 1, 42 Ω–0.5 µF), power lines ±1 kV (level 2, 2 Ω–18 µF); ESD IEC 61000-4-2 air ±15 kV, contact ±8 kV (level 4).
- "The test of least importance is the one for ESD immunity. It is proven that the main cause of ESD failures in the field is due to human involvement during the rare events of network installation and maintenance."
- "relying solely on a transceiver's integrated ESD structure when designing a data link for real world application, may fail. A robust data link requires external protection circuitry to absorb the much higher impact of burst and surge transients."
- "While the data sheets of many transceiver devices claim high ESD protection levels of up to 30kV, they often fail to state the pass-criterion applied."
- "Do not treat transient protection as an add-on feature, instead plan for it at the beginning of the design."
- TVS "stand-off voltage is above the expected common-mode voltage range".
- TI SLLA292A: read OK
- curl to ti.com with blank UA: denied by permission classifier (no UA spoofing; used WebFetch instead)

### Microchip/Atmel AVR182 "Zero Cross Detector", sec 1.1 Hardware (online docs)
URL: https://onlinedocs.microchip.com/oxy/GUID-6AC9F79C-CD9D-4DEE-B7A9-57FB68C0D274-en-US-3/GUID-C94F9D0C-A2A7-461E-B1D6-48B2AD6585B2.html
- "It is not recommended that the clamping diodes are conducting more than maximum 1mA" (with a 1 MΩ series resistor on mains). [Relevant because ATmega internal clamps are the only protection on most open loggers' sensor pins; their safe continuous injection is ~1 mA by the vendor's own guidance.]

### TI SLAA530B (MSP430 ESD, rev July 2021), sec 2.3.3 "ESD Protection Using Series Resistor"
URL: https://ti.com/document-viewer/lit/html/SLAA530B/GUID-2527A157-A308-4FEA-911E-36BFFD8D6121
- "The simple series resistor protection technique works for low levels of ESD stress"; for higher stress "suppression devices such as TVS diodes, varistors, and polymers should be considered."; "If standalone resistors are used for primary ESD protection, they must withstand the full electrostatic voltage."

### Microchip TB3013 "Using the ESD Parasitic Diodes on Mixed Signal Microcontrollers" (Julicher, 2008) - search-snippet only via dtsheet mirror; not read. [UNVERIFIED] reported to suggest external Schottky clamps plus ~100 Ω series resistors.
- AVR182 online doc: read OK; TI SLAA530B section: read OK; SiLabs AN376: 403 (dead end); TB3013: snippet only

### Campbell Scientific CRVW3 manual, "Electrostatic discharge protection" (online help, no date)
URL: https://help.campbellsci.com/crvw3/crvw3/install-indv-crvw3-stations/esd-protection.htm
- "Electrostatic discharge (ESD) can originate from several sources, the most common and destructive being lightning strikes."; "secondary strikes induce a high voltage in power lines or sensor wires."
- "The CRVW3 must be properly earth grounded to take advantage of its built-in protection to prevent damage from ESD."
- Minimum field earth: "a 5-ft copper-sheathed grounding rod driven into the earth" to the brass lug with "a low-gauge wire (8 to 12 AWG)".
- Campbell CRVW3 ESD page: read OK; Wayback (web.archive.org) not fetchable (dead end for Onset ESD note)

### Wurth Elektronik ANP121 "Filter and surge protection for I2C bus", press page dated 2023-08-03
URL: https://www.we-online.com/en/news-center/press?d=anp121 (PDF at we-online.com returned HTML to curl; element14 blog timed out)
- Recommends SMT multilayer ferrites (WE-CBF) plus ESD protection diodes (WE-TVS-SS) on SDA/SCL where I2C crosses connectors or cables. Test: 400 kHz, "A 20 cm data cable", 400 pF parasitic. Result (page summary): ferrites + ESD diodes "practically no effect" on SDA/SCL while improving immunity. [Fetch summary, not raw quote.]

### Interference Technology, "The Importance of Layout in ESD Suppressing Diodes", Aziz Yuldashev, 2017-04-10
URL: https://interferencetechnology.com/importance-layout-esd-suppressing-diodes/
- "Clamping (TVS) diode must be placed as close to the IC pin as possible."; "The trace leading to ground return from the anode of the diode must be as short as possible."
- [NOTE] This conflicts with the more common vendor advice to place the TVS at the connector (Semtech SI99-01 snippet: protect "all external connections"); the reconciling practice is TVS at the connector with a short ground, plus a series R between TVS and IC. [INFERENCE]
- WE ANP121 press page: read; interferencetechnology layout article: read; Semtech SI99-01 via mouser: timeout

### Trout Unlimited / Stroud EnviroDIY station manual ("TU_EnviroDIYmanual_Ver1", 2022)
URL: https://www.tu.org/wp-content/uploads/2022/06/TU_EnviroDIYmanual_Ver1.pdf (2190 lines pdftotext)
- grep lightning / ground rod / grounding / static / ESD / surge: zero hits. Only "storm" hits are about high flow and cellular signal (e.g. "to avoid storm flow damage, it is necessary to position sensors on the inside ...").
- [INFERENCE] The EnviroDIY/Stroud deployment practice as published for volunteer stations contains no grounding or lightning guidance; the station is a battery+solar box with a sensor cable into the stream.

### Other loggers requested
- OpenOBS (tedlanghorst/OpenOBS): README mentions custom PCB (hardware/PCB_gerber images) but no schematic source in repo tree; no ESD/surge text in README. Not audited further.
- Sodaq / Pycom: gh search "sodaq hardware schematic" returned nothing; not audited (time-boxed; pending).
- PurpleAir: not relevant (mains-powered air sensor); not checked.
- Littelfuse "Smart Building Application Guide" PDF: >10 MB, WebFetch refused (dead end).
- TU EnviroDIY manual: read (negative); Sodaq: not found; Littelfuse smart building guide: too large

## Synthesis (written 2026-11-10; [INFERENCE] throughout unless a source is named)

Open designs: of nine boards audited from source (Mayfly v0.5b, v1.0, v1.1; Adafruit M0/32u4/RP2040 Adaloggers; SparkFun OpenLog Artemis; Riffle; ALog BottleLogger; Particle Boron; Arduino MKR Zero and MKR WAN 1310), none puts a TVS, clamp, or series resistor on any sensor port. The only TVS parts found are on USB: Mayfly v1.x (SP0503BAHTG on D+/D-/VBUS) and Arduino MKR (PRTR5V0U2X on D+/D-/VBUS, plus a 0.5 A PTC). Overcurrent PTCs appear on Riffle VBUS and on ALog's switched sensor-supply outputs. Particle publishes 1 kV HBM and pushes ESD to the carrier board.

Field failures: published low-cost-logger lessons (Chan et al. 2020; Filhol et al. 2023; Cave Pearl blog; TU/Stroud manual) attribute failures to moisture, animals, power, SD cards, cheap parts and unexplained lockups, and do not name ESD or lightning. The specific electrical cases found are storm-coincident deaths on unprotected long-cable inputs (EnviroDIY 2021 Mayfly with a partly buried CTD cable; Arduino forum 2018 well-probe with 20 wires, 2 of 6 muxes and 2 of 20 caps killed) and Campbell's nearby-strike case through an ungrounded rain-gauge cable. NETLAKE (Lake Erken) reports induced transients "multiple times each year" with direct strikes rare; METER measured 80 V p-p common-mode on a cable from a strike ~5 km away. TI SLLA292A states handling ESD occurs mainly during installation and maintenance.

Guidance: the interface standards themselves ask for modest, cheap protection on the field lines: SDI-12 v1.3 Appendix A (510 Ω + 7.5 V zener + 3.3 nF + 510 Ω, plus spark gap; 1.5KE20A on 12 V), NXP UM10204 (optional ~300 Ω series Rs on SDA/SCL). Vendor notes converge on TVS at the connector plus a series resistor before the IC (TI SLAA530B, TI SLLA292A, ADI snippet, Arduino forum advice), and on the MCU clamps being good only to ~1 mA (AVR182). Lightning protection that works is grounding and short, bundled cables (METER, Campbell, NETLAKE); NETLAKE suggests transient protection on sensor leads longer than 3-4 m when the logger has none. IEC targets quoted by vendors: 61000-4-2 4 kV contact / 8 kV air (61326-1) to 8/15 kV (industrial level 4); 61000-4-5 surge 0.5-1 kV on signal lines, applied to long lines.

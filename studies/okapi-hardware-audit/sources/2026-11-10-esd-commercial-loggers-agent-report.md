COMPLETE

# Commercial logger ESD/surge protection survey (2026-11-10)

## Findings


### Campbell Scientific

C1. CR1000X/CR1000Xe comparison sheet (PDF, created 2024-10-24, no rev number), https://s.campbellsci.com/documents/us/product-brochures/comparison-cr1000x-cr1000xe.pdf
 - CR1000X column: "Fully CE compliant for surge and ESD protection". CR1000Xe column: "Enhanced ESD and surge protection on Ethernet port"; "gold dipped pins on RJ45 connector".

C2. "SunSentry Surge Protection" application note, Revision 09/2026, (c) 2025-2026, https://s.campbellsci.com/documents/us/technical-papers/sunsentry-surge-protection.pdf
 - "the CR1000Xe data logger, which provides built-in surge protection on all measurement, control, and power terminals. The CR1000Xe also uses fast-acting gas-discharge tubes to protect the data lines."
 - "The CR1000Xe meets the IEC 61000-4-5 standard for class 4 surge immunity. The CR1000Xe also meets or exceeds the IEC 61000-4-2, 61000-4-3, 61000-4-4, 61000-4-6 standards for ESD, Radiated RF, EFT, and Conducted RF."
 - Table: "I/O signal/control (unsymmetrical) +/-1 kV line-to-line, +/-2 kV line-to-ground"; "(symmetrical) +/-1 kV line-to-line, +/-1 kV line-to-ground".
 - "For locations with a high risk of lightning, additional surge protection devices (SPDs) can be installed in the main meteorological enclosure."
 - ISP10/ISP11 inline SPDs: "three-stage protection to earth ground on the signal lines ... and single-stage protection to earth ground on the power lines". "Best practices recommend locating surge protection devices (SPDs) as close to the equipment they protect as possible."
 - Shield: "Shielded cables with the shields terminated to earth ground provide a level of protection"; "For signal-noise immunity, best practice is to terminate the cable shield at only one end of the cable to avoid ground loops, typically at the measurement-device end."
 - "the effectiveness of this protection depends heavily on proper grounding." Ungrounded rain gauge example: lightning "traveled through the cable to the meteorological station".
 - "The sensor should also be electrically isolated from conductive mounting structures." (isolation plates for pyranometers)

C3. Campbell help, CR350 "Electrostatic discharge and lightning protection", https://help.campbellsci.com/CR350/shared/installation/lightning.htm (online, undated)
 - "All critical inputs and outputs on the data logger are" ESD protected [WebFetch paraphrase-quote; verify wording].
 - Lightning system: "a lightning rod, metal mast, heavy-gauge ground wire, and ground rod" to "direct damaging current away from the data logger." "This system, however, is not infallible."
 - "To be effective, the earth ground lug must be properly connected to earth (chassis) ground."
 - "You should provide communications paths, such as telephone or short-haul modem lines, with spark-gap protection." "Spark-gap protection is usually an option with these products; so, request it when ordering."

C4. CR1000X/Xe spec sheets. (a) "CR1000X Specifications | August 23, 2019", https://s.campbellsci.com/documents/fr/product-brochures/s_cr1000x.pdf ; (b) CR1000Xe specifications, "Revision: 05/2026", https://s.campbellsci.com/documents/us/product-brochures/s_cr1000xe.pdf . Both state:
 - Power: "Power inputs are protected against surge, over-voltage, over-current, and reverse power. IEC 61000-4 Class 4 level."
 - EMI and ESD immunity (CR1000X: "Immunity: Meets or exceeds following standards"): "ESD: per IEC 61000-4-2; +/-15 kV air, +/-8 kV contact discharge"; "Radiated RF: per IEC 61000-4-3; 10 V/m, 80-1000 MHz"; "EFT: per IEC 61000-4-4; 4 kV power, 4 kV I/O"; "Surge: per IEC 61000-4-5; 4 kV power, 4kV I/O"; "Conducted RF: per IEC 61000-4-6; 10 V power, 10 V I/O"; "Emissions and immunity performance criteria available on request."
 - Ethernet: "Auto-MDIX, magnetic isolation, and TVS surge protection."
 - CR1000Xe: "Sustained Logic Input Voltage without Damage: +16/-12 VDC" (C terminals). Ingress: wiring panel IP40, measurement module IP65 when connected.
 - EU Declarations of Conformity referenced at www.campbellsci.com/cr1000x.
 - NOTE (my observation): the spec sheets say surge "4kV I/O", the SunSentry note C2 tabulates I/O signal lines at +/-1 kV line-line, +/-2 kV line-ground. The sources disagree or quote different port classes; unresolved.
 - USB on CR1000X is a Micro-B device port; no USB-specific protection is stated in the spec sheet.

C5. CR1000X Product Manual, "Revision: 09/2026", https://s.campbellsci.com/documents/us/manuals/cr1000x-product-manual.pdf
 - Sec 8.3 "Electrostatic discharge and lightning protection" is word-for-word the CR350 help page text (C3).
 - CR1000X specs: "Transient voltage suppressor (TVS) diodes at the POWER IN terminal clamps transients to 36 to 40 V. ... Sustained input voltages in excess of 32 V can damage the TVS diodes. If the voltage on the POWER IN terminals exceeds 19 V, power is shut off to certain parts of the data logger to prevent damaging connected sensors or peripherals." "Sustained Input Voltage without Damage: 30 VDC".
 - Modbus: "Consideration should be given to proper surge protection of any cabled connection. Between systems of significantly different ground potential, optical isolation may be appropriate."
 - Watchdog errors listed as possibly due to "Transient voltage" and "Poor ground connection on the power supply".
 - Safety page: "Protect from electrostatic discharge (ESD)." "Protect from lightning."

C6. Campbell help "Grounds" pages: CR350 https://help.campbellsci.com/CR350/shared/components/grounds.htm and CR6 https://help.campbellsci.com/CR6/Content/shared/Components/Grounds.htm (same text, online, undated)
 - "Proper grounding will ensure maximum ESD protection and measurement accuracy. It is the easiest and least expensive insurance against data loss, and often the most neglected."
 - "Earth Ground Lug ... connection point for heavy-gauge earth-ground wire. A good earth connection is necessary to secure the ground potential of the data logger and shunt transients away from electronics. Campbell Scientific recommends 14 AWG wire, minimum."
 - "Campbell Scientific recommends that all data loggers be earth grounded. All components of the system (data loggers, sensors, external power supplies, mounts, housings) should be referenced to one common earth ground."
 - "In the field, at a minimum, a proper earth ground will consist of a 5-foot copper-sheathed grounding rod driven into the earth and connected to the large brass ground lug on the wiring panel with a 14 AWG wire."
 - "In low-conductive substrates, such as sand, very dry soil, ice, or rock, a single ground rod will probably not provide an adequate earth ground."
 - Signal ground terminals: "a ground for sensor shield wires". RG: "used for decoupling ground on RS-485 signals. Includes 100 ohm resistance to ground."
 - So the CR350 and CR6 both have an earth-ground lug and the same guidance.

C7. CR6 Specifications, "Revision: 05/2026" ("CR6 Specifications | May 6, 2026"), https://s.campbellsci.com/documents/us/product-brochures/s_cr6.pdf
 - Same power-protection sentence ("IEC 61000-4 Class 4 level") and the same EMI/ESD table as CR1000X (ESD +/-15 kV air, +/-8 kV contact; surge 4 kV power, 4 kV I/O; EFT 4 kV). Ethernet "magnetic isolation, and TVS surge protection." Analog U terminals "Sustained Input Voltage without Damage: +/-20 VDC". USB: "Micro-B device for computer connectivity" (no USB-specific protection stated).

C8. CR300 Series Product Manual (CR300/CR310), "Revision: 09/2026", https://s.campbellsci.com/documents/us/manuals/cr300.pdf ; and CR350 Product Manual, "Revision: 09/2026", https://s.campbellsci.com/documents/us/manuals/cr350.pdf
 - Both: "Protection: Power inputs are protected against surge, over-voltage, over-current, and reverse power. IEC 61000-4 Class 4 level." Both list "ESD: per IEC 61000-4-2; +/-15 kV air, +/-8 kV contact discharge", "EFT: per IEC 61000-4-4; 4 kV power, 4 kV I/O", "Surge: per IEC 61000-4-5; 4 kV power, 4kV I/O", "Conducted RF: per IEC 61000-4-6; 10 V power, 10 V I/O".
 - Both carry the same ESD-and-lightning section ("All critical inputs and outputs on the data logger are ESD protected. To be effective, the earth ground lug must be properly connected to earth (chassis) ground.") and the Grounds section with "Earth Ground Lug".
 - CR300 manual, Severing a ground loop: "Connect the shield wire of a signal cable to ground only at one end of the cable. Leave the other end floating (not connected to ground)." "Never intentionally use the shield (or drain wire) of a cable as a signal ground or power ground." "Use the mechanical support structure only as a connection for the safety ground (usually the ground lug). Do not intentionally return power ground through the structure." "For long distance communications protocols such as RS-485, RS-422, and CAN, use a Resistive Ground (RG) terminal ... 100-ohm resistor in series with ground".
 - CR300 manual: "The creation of an electromagnetic pulse can induce a surge that damages attached electronic devices." "If the ground voltage differences reach several volts, damaging effects may occur at the terminals".
 - The older CR300 spec sheet (https://s.campbellsci.com/documents/us/product-brochures/s_cr300.pdf, undated in text) lists only "PROTECTION: IP30" and an EU DoC link; the IEC table appears in the current manual, not that sheet.

C9. CR800/CR850 spec sheet, dated "October 17, 2017", https://s.campbellsci.com/documents/us/product-brochures/s_cr800.pdf : only "Power connection is reverse polarity protected." and "SUSTAINED INPUT VOLTAGE W/O DAMAGE: +/-16 Vdc max." No ESD/surge standard listed in the spec sheet. (Discontinued product line; manual not checked.)

C10. External accessories (optional, sold separately):
 - SVP48 Surge Voltage Protector manual, "Revision: 3/03", https://s.campbellsci.com/documents/es/manuals/svp48.pdf : used "to supplement the datalogger's built in surge protection." "Surge protection is provided by gas filled arrestors that trigger at 110 VAC or 156 VDC. Each surge protector protects one conductor and provides a terminal for shield wires." Supplied "green 14 AWG ground wire" to the enclosure grounding chuck; "Ground the enclosure to earth".
 - SVP100 Surge Voltage Protector manual, "Revision: 12/16", https://s.campbellsci.com/documents/us/manuals/svp100.pdf : "three-stage surge protection to analog and digital circuits"; "used to supplement the built-in surge protection provided by the datalogger." "Periodically (at least yearly) check electrical ground connections."
 - ISP10 brochure, https://s.campbellsci.com/documents/us/product-brochures/b_isp10.pdf : inline M12 SPD for Modbus RTU sensors; "Surge protection to IEC 61000-4-5, level 4 (4 kV, 2000 A)"; "Maximum DC Operating Voltage 27.5 Vdc"; "Number of Surge Events 10 maximum (replacement frequency based upon frequency of lighting in the region)"; "Mount the ISP10 to an earth-grounded, conductive part for proper surge protection."
 - "Surge protector kits: installation and troubleshooting" white paper, 04/27/2021, CSL I.D. 1369, https://s.campbellsci.com/documents/eu/technical-papers/surge-protector-kits%20-%201369.pdf : antenna-line Polyphaser kits, "a capacitive-coupled gas tube protector with multi-strike capability"; ground lug wire to the enclosure ground.
 - Sensors are also surge-tested: "CS240 Cable Surge Testing Summary", https://s.campbellsci.com/documents/us/miscellaneous/CS240%20Cable%20Surge%20Testing%20Summary.pdf , log dated 9/12/2019, 1000/2000/4000 V, 2 ohm, "10 Pulses", "Passed".

### Onset (HOBO)

O1. HOBO RX3000 Remote Monitoring Station User Guide, doc 18255-U (posted 2025-02, (c) 2015-2024), https://www.onsetcomp.com/sites/default/files/2025-02/18255-U%20RX3000%20Manual.pdf
 - Spec table lists no ESD or surge rating; compliance is "The CE Marking identifies this product as complying with all relevant directives in the European Union (EU)" plus FCC/IC IDs. Enclosure "NEMA 4X".
 - Included: "Grounding wire". Accessory: "Grounding kit (M-GKA) ... required if using wind speed or wind direction smart sensor".
 - "If you are using a wind speed/direction sensor or if the station will be installed on a roof or in a location with exposure to lightning, use the grounding wire included with this station and ground the tripod or mast using appropriate grounding, such as the Grounding Kit (M-GKA). A grounding wire may also reduce potential sensor errors that can result from installing near other radio or electrical equipment or antennas."
 - "The grounding wire must be connected to a properly grounded mast (typically on one side of the U-bolt) when the station is mounted."
 - Analog module pinout carries a "SHIELD" pin; "All four input channels share the same common ground."

O2. HOBO Micro Station (H21-USB) Manual, doc 20875-E, (c) 2016-2018, https://www.onsetcomp.com/sites/default/files/resources-documents/20875-E%20H21-USB%20Manual.pdf
 - CE marking statement only; no ESD/surge rating stated.
 - "Ground Wire Port: Use this port on the back of the logger to connect a ground wire (CABLE-MICRO-G)." Ground wire is an optional accessory.
 - "If you are using a wind speed/direction sensor or if the station will be installed on a roof or in a location with exposure to lightning, use a ground wire (CABLE-MICRO-G)." Mast: under a U-bolt nut; metal post: hose clamp; flat surface: "attach the ground wire to a proper ground."
 - "If possible, avoid sites immediately adjacent to radio/television/microwave towers and equipment."
O3. External Grounding Wire Adapter Cable (CABLE-HWS-G) manual, doc 7788-A, (c) 2003, https://www.onsetcomp.com/sites/default/files/resources-documents/7788-A%20MAN-CAB-HWSG.pdf : "The grounding wire is required if you will be using a wind speed or wind speed and direction sensor with the logger or if the logger will be placed in an exposed location on a tripod or tower."

O4. Handling ESD note, repeated across HOBO U/UX/MX standalone logger manuals:
 - HOBO MX1104/MX1105 Manual, doc 23968-H, https://onsetcomp.com/sites/default/files/2023-01/23968-H%20MX1104%20and%20MX1105%20Manual.pdf : "Note: Static electricity may cause the logger to stop logging. The logger has been tested to 8 KV, but avoid electrostatic discharge by grounding yourself to protect the logger. For more information, search for "static discharge" on onsetcomp.com."
 - HOBO UX120-014M Manual, doc 17031-D, https://www.onsetcomp.com/sites/default/files/resources-documents/17031-D%20UX120-014M%20Manual.pdf : same sentence ("tested to 8 KV").
 - HOBO U12 Temp/RH (U12-011), doc 13127-B, https://www.onsetcomp.com/sites/default/files/resources-documents/13127-B%20MAN-U12011.pdf : "Note! Static electricity may cause the logger to stop logging. To avoid electrostatic discharge, transport the logger in an anti-static bag, and ground yourself by touching an unpainted metal surface before handling the logger."
 - Inference (mine): Onset's "tested to 8 KV" matches the IEC 61000-4-2 level-4 contact value, but the manuals do not name the standard or say contact vs air. The failure mode they describe is a soft one (logging stops), not damage.

### METER Group

M1. ZL6 Data Logger manual, doc 18258-17, https://publications.metergroup.com/Manuals/18258_ZL6_Print.pdf
 - Compliance appendix: FCC Part 15, IC, "R&TTED and European Conformance CE mark"; "A full CE declaration of conformity for the ZL6 is available on request from METER Group." No ESD, surge or IEC 61000-4-x rating stated anywhere in the manual text (grep for ESD/surge/lightning/61000/61326/static: no hits).
 - No grounding instructions or ground lug in the manual (grep "ground": no installation hits). Installation advice is mechanical: "Thread cables near the ground through conduit or plastic cladding to avoid" rodent damage; logger upright; condensation.
 - ZL6 Pro vs ZL6 comparison in the manual: "USB micro-B" vs "USB-C"; "No shorted-sensor dection" vs "Shorted-sensor detection".
M2. EM60 manual, doc 18206-02, https://library.metergroup.com/Manuals/18206_EM60_Pages.pdf
 - Compliance: "Manufactured under ISO 9001:2015"; "EM ISO/IEC 17050:2010 (CE Mark)". No ESD/surge rating, no grounding instruction. "Thread cables in conduit or plastic cladding when near the ground to avoid rodent damage."
M3. METER article "Lightning Surge and Grounding Practices" (PDF metadata: saved Sept 2025, no revision), https://publications.metergroup.com/Sales%20and%20Support/METER%20Environment/Website%20Articles/Lightning-surge-grounding-practices.pdf
 - "In one test, a lightning strike at a distance of almost 5 km from an installation induced an 80 volt (peak to peak) common mode spike on an insulated cable."
 - "Generally speaking, it is the common mode voltage that most adversely affects product reliability. Poor grounding is usually the root cause for this class of failures."
 - "WITHOUT A ROBUST GROUNDING SYSTEM, THERE IS NO WAY TO PROTECT AGAINST LIGHTNING SURGES"; "Grounding straps or wires must be large to facilitate the discharge of all surge currents."
 - "METER soil sensors have built-in circuitry, which protect them against common surge conditions. Installations in lightning-prone areas, however, require special precautions, especially when sensors are connected to a well-grounded Campbell Scientific logger."
 - "a single ground point for the system should be established at the data logger using a ground rod. The ground rod should be made from a metal that will not tarnish or corrode (such as stainless steel)."
 - "By installing ground rods in the vicinity of soil moisture sensors and running a separate #6 AWG copper wire from that rod back to the central ground rod, earth current transients from nearby lightning strikes are minimized". Fig 1: "Ground rods should be driven at least 2 meters into the ground, if possible".
 - Inference (mine): METER's own ZL6/EM60 documentation puts no protection rating on the logger; the protection story is the sensors' built-in circuitry plus installer grounding, and the article is written for METER sensors on a Campbell logger.

### Geokon

G1. Model 8600 Series Micro-6000 Dataloggers manual, "Document Revision: H.1 | Release Date: 9/24/26", https://www.geokon.com/content/manuals/8600-Series-Dataloggers.pdf
 - The 8600 is built around a Campbell CR6 ("A.2 CR6 MEASUREMENT AND CONTROL MODULE"; "CR6 built in charge regulator"), so its logger-level ESD/surge rating is the CR6's (C7).
 - "An earth grounding lug is supplied on the exterior of the data logger enclosure to connect the system to earth ground (Figure 3). A copper grounding rod at least six feet in length should be driven into the soil to a minimum depth of three feet, as close to the device as possible. ... Connect the grounding rod to the mounting bracket or the copper grounding lug on the exterior of the device with a 12 AWG or larger wire."
 - Troubleshooting, program/data loss: "The surge originated as a result of lightning. Install appropriate grounding. Install lightning protection devices on all incoming and outgoing lines."
G2. 8600 Series datasheet, "Rev-D-01/26/2026", https://www.geokon.com/content/datasheets/8600_Series_Dataloggers.pdf
 - Model 8032 multiplexer: "Each channel is protected by an integrated lightning protection system to protect against lightning or EMI/RFI induced transients." Enclosure "NEMA 4X fiberglass reinforced polyester ... protection against lightning damage".
G3. Model 4999-12 Surge Protection Circuit Boards (LAB3) manual, "Document Revision: L | Release Date: 9/15/26", https://www.geokon.com/content/manuals/4999-12L-LE(LAB3)_Surge_Module.pdf  (optional accessory, sold separately)
 - Variants: "4999-12L-A for 5 Volt signals", "-B for 12 Volt power and signals", "-C for 24 Volt power and signals". "designed for installation in the cable leading from the sensor to the data logger, or in the data logger itself."
 - Topology: "The primary protection is provided by a tripolar gas tube protection device." "The tripolar plasma surge arrestor (rated at 5 kA) will begin shunting the energy to ground when the nominal breakdown voltage, ~230 V is exceeded. (Typically, 184-276 Volts.) The inductors L1 and L2 (or L3 and L4) delay the 230 Volt pulse to the secondary stage protection ... The transzorbs, TZ1 and TZ3,(rated at 1500 Watts), clamp the common mode voltage to a nominal 7.5 Volts (4999-12L-A), 16 Volts (4999-12L-B), or 30 Volts (4999-12L-C). The transzorb TZ2, (rated at 1500 Watts), completes the secondary stage protection by clamping the normal mode voltage". "The shield is protected by a plasma surge arrestor rated at 2 kA surge absorption with a 150-Volt breakdown."
 - Placement: "installed as close to the sensor as is practical"; for a logger, "as close to the multiplexer or data logger as possible."
 - Grounding: "For best results, the resistance to ground should be 20 ohms or less." Rods "at least two meters"; "1/2" diameter copper pipe will suffice". "The lightning needs to encounter high impedance through the sensor and low impedance to earth ground."
 - Disclaimer: "nothing can protect a system from a direct lightning strike".

### Vaisala

V1. AWS310 Automatic Weather Station brochure/spec, "B211729EN-F (c) Vaisala 2024", fetched from https://docs.vaisala.com/api/khub/documents/aidfohzYNkHlF6_dRiUywA/content
 - EMC table: "Immunity to electrical fast transient EN 61000-4-4 2 kV AC, 1 kV I/O"; "Immunity to surge EN 61000-4-5 2 kV / 1 kV AC, 1 kV I/O"; "Immunity to RF field ... EN 61000-4-3 11 V/m (80 MHz - 1 GHz)"; "Immunity to conducted RF EN 61000-4-6 4 V e.m.f."; emissions CISPR 32 / EN 55032 Class B. No ESD (61000-4-2) row found in the extracted text.
 - A search snippet attributes to an AWS310-SITE document "AWS310-SITE includes surge protection for the power input, sensor connections, and output data connections." UNVERIFIED (not opened).
V2. Surge Protector WSP150 datasheet, "B210654EN-E (c) Vaisala 2018" (copy hosted by a distributor, fluid.yodify.com), https://fluid.yodify.com/Documentation/Document/VLYpq/WSP150-Datasheet-B210654EN.pdf  (optional external accessory)
 - "A lightning strike nearby may induce a high voltage surge, which the integral transient suppressor of the instrument may not tolerate. Additional protection is needed, especially where frequent and severe thunderstorms are common and where cables longer than 30 m (98 ft 5 in) are used. Also use WSP150 if you have unshielded, open-wire lines."
 - "Each channel uses a threestage protection scheme: first there are discharge tubes, then voltage dependent resistors (VDR), and finally transient zener diodes. Between each stage, there are either series inductors or resistors." "Both differential and common mode protection is provided for each channel: across the wire pairs, against the operating voltage ground, and against the earth."
 - "Vaisala recommends using WSP150 when wind and weather instruments are installed on top of high buildings or masts and in open grounds, that is, anywhere with an elevated risk of lightning."
 - "EMC surge tolerance EN 61000-4-5 (4 kV, 2 kA) IEEE C62.45 (6 kV, 3 kA)".
V3. "Grounding and Lightning Protection in Vaisala Outdoor Installations Technical Reference", M211786EN-B, docs.vaisala.com (online, JS-rendered; quotes via WebFetch, exact wording of fragments in quotes only):
 - https://docs.vaisala.com/r/M211786EN-B/en-US/GUID-C18A8373-9837-4CEE-8C51-4585F2B6A964/GUID-6FA54F6D-8C6B-4921-B3B8-7792C968288A : "Every Vaisala outdoor system has a capable two-stage transient protection in all external signal cables" [leaving the site] and power connection cables; "Local sensors with short cables may rely on the built-in protection on the signal interfaces." "Surge protection devices (SPD) cannot protect equipment against direct lightning strikes."
 - https://docs.vaisala.com/r/M211786EN-B/en-US/GUID-950C5868-D1BE-4AD6-BE85-1A489519F1E1 : "Lightning protection grounding enables the lightning protection systems and transient protection devices to operate"; "install a lightning protection system, including an air terminal, down conductor, and a ground electrode". Cites IEC 62305, NFPA 780 and others (search snippet).
 - Related: Technical Note "Improving Weather Station Grounding" M212202EN-A (2018): checks that "the sensor cable shields have been grounded to the cable glands" (stainless flanges) or "to the grounding rail" (rubber flanges). UNVERIFIED (search snippet only; distributor copy 404).

### NexSens

N1. "X-Series Data Logger Grounding" knowledge-base page, https://www.nexsens.com/?p=15465 (undated; footer (c) 2026), via WebFetch:
 - "Grounding a data logger is critically important to ensure measurement accuracy and prevent damage to a data logging system." "X-Series data loggers come standard with a grounding kit recommended for installation." Path runs "from the logger through the PM2 mounting accessory"; "To establish a proper ground the mounting pipe must be buried in the ground or connected to an earth ground." Buoys: "the electrical ground connection will not be reliable if made through the tower hubs"; route the wire to the "stainless steel buoy hull top plate or battery well lid."
 - No built-in protection rating stated on that page. Search results for the X2 spec gave no ESD/surge rating (snippet: X3 guide lists "reverse polarity protection, over-voltage protection (OVP), and under voltage lockout (UVLO)" on power; UNVERIFIED, not opened).

### Sutron (OTT HydroMet / Hach)

S1. Sutron SatLink 3 Operations & Maintenance Manual, "Part No. 8800-1207 Rev 8.77.0 May 9, 2025", https://cdn.hach.com/1XMCM0ZF/at/9kvcqv4x6b53fxgtq8j3pwt4/sl3_O_M.pdf (Hach CDN; Hach/OTT are the current owner)
 - "Any time a sensor cable is attached to the terminal strip, the unit may be exposed to electrical surges such as those that come from nearby lightning strikes. The SL3 includes spark gaps and other protection devices that shunt the energy to the earth ground. If there is no connection to the earth ground point on SL3, the energy has nowhere to go, and the unit can be damaged."
 - "Failure to properly connect the Earth ground point will lead to failures in the field due to surges."
 - "Use a copper ground rod driven into the ground at least 6 feet." "Attach a heavy gauge (#4 Solid Copper) wire between the rod and the SatLink 3 Earth ground point." "Do not rely on AC power ground connections as they are not always properly grounded and may introduce other surges."
 - "SatLink 3 features gas tube protection on all sensor inputs."
 - "Users are encouraged to use a separate lightning arrestor for the antenna"; accessories "8111-1113-1 RF COAX lightning protection, Bulkhead", "8111-1099-1 RF COAX lightning protection, panel mount".
 - Symbol legend: "Protective earth ground. Connect to an earth ground electrode for lightning protection of internal components."
 - On SL3-LITE and SL3-XMTR-1, "the chassis is the earth ground point."
S2. Sutron XLink 100/500 Operational Manual, "8800-1218, Rev.4 | 02-2025", https://cdn.hach.com/1XMCM0ZF/at/7p6zcgff7kqrqx3kgxgg5m9/Operational_Manual_Data_logger_XLink100_500_V4.pdf
 - "Damage due to surges! If the earth ground point is not connected properly, this may result in surges that can damage the device." "Use a copper ground rod driven into the ground at least 2 m (6 feet)." "Attach a 4-gauge copper wire between the rod and the earth ground point on the device." Terminal table: "Earth ground Attached via a heavy gauge wire of 5.26 to 21.2 mm2 (4 to 10 AWG)".
 - Terminal "PROT +12V" (protected 12 V output) listed.
 - CE: "The equipment meets the essential requirements of EMC Directive 2014/30/EU and RED 2014/53/EU." No IEC 61000-4-x levels stated (grep: none).
 - Handling: "Dirt accumulation can damage the modem and cause Electro Static Discharge (ESD). Handle the modem in a clean environment."
 - Externally mounted RF coaxial lightning arrestor 8111-1113-1 listed as an accessory.

C11. CR1000 (predecessor of CR1000X) brochure, dated 03/19/2026 in footer, https://s.campbellsci.com/documents/us/product-brochures/b_cr1000.pdf : "Gas Discharge Tube (GDT) protected inputs"; "The wiring panel includes switchable 12 V, redistributed analog grounds ..., gas-tube spark gaps". (Current CR1000X/CR6/CR300/CR350 spec sheets do not name the device type; only CR1000Xe app note C2 names GDTs on "data lines".)

### Xylem / YSI (Storm 3)

Y1. Storm 3 Getting Started Guide, Rev D, (c) 2020 Xylem, https://www.ysi.com/File%20Library/Documents/Guides/Storm-Getting-Started-Guide-Rev-D-with-crop-marks--Item--360427-dwg--360427-.pdf : "Ground Lug Proper shield or earth grounding should be used to protect the equipment from exposure to Electrostatic Discharge and other induced interference." No ESD/surge rating found in the guide.
Y2. YSI technical note D114 "Making the Connection: EXO2 and Storm 3", Rev A, (c) 2017, https://www.ysi.com/File%20Library/Documents/Technical%20Notes/Making-the-Connection-EXO2-and-Storm-3-D114.pdf : "Next we need an earth-ground connection tied to the central location of the system and either the gauge house or a grounding rod." Also: "It is not uncommon for users to use the logging in the sonde for added redundancy, in case lightning, vandalism, or some other incident incapacitates the Storm 3 unit."
 - DEAD END: Storm 3 spec sheet URL (DL-300-Series-Data-Loggers-Specification-Sheet.pdf) returned JavaScript/HTML, not PDF.

### In-Situ
 - DEAD END: two searches (general and in-situ.com-restricted) found no lightning, surge, ESD or grounding guidance for Level TROLL/Aqua TROLL/VuLink. RuggedCable spec sheet mentions a metal shield "to guard against electrical interference" (search snippet, UNVERIFIED wording).

## Synthesis (my reading of the sources above; inference, not maker statements)

Standard (nearly everyone):
- CE marking under the EMC Directive is universal (Campbell, Onset, METER, Vaisala, Sutron). Only Campbell and Vaisala print IEC 61000-4-x test levels in the spec sheet.
- A dedicated earth-ground point plus an instruction to run it to a ground rod: Campbell (lug, 14 AWG min, 5 ft rod), Sutron (lug, #4 solid Cu, 6 ft rod, "failures in the field" without it), Geokon (lug, 12 AWG+, 6 ft rod), Storm 3 (lug), NexSens (grounding kit ships standard), Onset RX3000/H21-USB (ground-wire port, required only with wind sensors, roofs or lightning exposure). METER ZL6/EM60 are the exception: no ground point and no rating in the manuals.
- Field loggers with screw terminals protect every terminal internally and depend on that lug to work: Campbell ("All critical inputs and outputs ... are ESD protected", TVS on POWER IN clamping at 36-40 V, GDTs on CR1000 / CR1000Xe data lines), Sutron SatLink 3 ("spark gaps" and "gas tube protection on all sensor inputs"), Vaisala ("two-stage transient protection in all external signal cables").
- Reverse-polarity protection on the power input (Campbell all models incl. CR800).

Premium:
- Published ESD/surge levels: Campbell CR1000X/CR1000Xe/CR6/CR300/CR350 at IEC 61000-4-2 +/-8 kV contact, +/-15 kV air, and IEC 61000-4-5 4 kV power and 4 kV I/O (the SunSentry note lists I/O at +/-1/+/-2 kV; unresolved). Vaisala AWS310: surge 1 kV I/O. Onset only says "tested to 8 KV" on small loggers.
- Ethernet with magnetics and TVS (Campbell); "enhanced" Ethernet ESD/surge on the CR1000Xe.
- External multi-stage SPDs sold as accessories: GDT -> inductor/VDR -> TVS. Campbell SVP48 (GDT, 156 VDC), SVP100 (3-stage), ISP10 (4 kV/2000 A, M12 inline, 10-surge life); Vaisala WSP150 (GDT/VDR/TVS, 4 kV/2 kA); Geokon LAB3 (230 V tripolar GDT, 1500 W TVS at 7.5/16/30 V by supply voltage, shield GDT 150 V). Coax antenna arrestors (Campbell Polyphaser kits, Sutron 8111-1113-1).
- Triggers the makers give for adding them: lightning-prone sites, masts/roofs/open ground, "cables longer than 30 m", "unshielded, open-wire lines" (Vaisala); place SPDs "as close to the equipment they protect as possible" (Campbell) or near the sensor (Geokon).

Left to the installer (all makers):
- The ground rod, the wire, a single-point ground at the logger, and in high-risk sites extra rods near sensor clusters (METER: #6 AWG back to the central rod; Geokon: <= 20 ohm).
- Shield practice: terminate shield at one end only (Campbell CR300 manual: logger end, to signal-ground terminal; SunSentry note: "typically at the measurement-device end"); never use the shield as a signal or power return; RS-485 ground through a 100 ohm resistive ground (Campbell RG).
- Isolate sensors from conductive structures and do not return power through the structure (Campbell).
- Lightning rod / air terminal (Campbell, Vaisala).
- Handling: Onset is the only maker with a handling ESD procedure ("ground yourself by touching an unpainted metal surface", "anti-static bag"); Campbell's safety page says only "Protect from electrostatic discharge (ESD)". No maker found asks for wrist straps.
- USB: no maker states USB-specific protection. Campbell lists USB as a "Micro-B device" port and covers it only by the logger-wide ESD rating; Onset, METER and Sutron say nothing. (Inference: USB is treated as an attended service port.)

## Sources checked (incl. dead ends)
- comparison-cr1000x-cr1000xe.pdf: OK (WebFetch could not parse PDF; extracted locally with pdftotext)
- sunsentry-surge-protection.pdf: OK (local pdftotext)
- help.campbellsci.com CR350 lightning page: OK via WebFetch
- s_cr1000x.pdf (2019-08-23), s_cr1000xe.pdf (rev 05/2026), cr1000x-product-manual.pdf (rev 09/2026), CR350+CR6 Grounds help pages: OK via curl + pdftotext
- s_cr6.pdf, s_cr300.pdf, s_cr800.pdf, cr300.pdf manual, cr350.pdf manual, svp48, svp100, b_isp10, surge-protector-kits 1369, CS240 surge summary: OK
- DEAD END: https://s.campbellsci.com/documents/us/product-brochures/s_cr350.pdf -> 404 (used CR350 manual instead)
- Onset: RX3000 18255-U, H21-USB 20875-E, CABLE-HWS-G 7788-A, MX1104 23968-H, UX120-014M 17031-D, U12-011 13127-B: OK
- DEAD END: Onset MX2300 manual 20923-N URL returned HTML, not PDF (not needed; same note found elsewhere)
- METER: ZL6 manual 18258-17, EM60 manual 18206-02, Lightning article: OK. ZL6 web tech-specs page not fetched (search snippet showed no EMC data).
- Geokon: 8600 manual H.1, 8600 datasheet Rev D, LAB3 manual Rev L: OK. 8900 maintenance page downloaded, not used.
- Vaisala: AWS310 B211729EN-F OK; WSP150 B210654EN-E OK; M211786EN-B via WebFetch only (site is JS; curl gets nothing). DEAD END: yodify copy of M212202EN-A -> 404; docs.vaisala.com M211788EN-F ground electrodes page -> 404.
- NexSens: grounding KB page OK via WebFetch; X2 spec search found no ESD/surge rating.
- Sutron XLink/SatLink3: first search found no protection spec.
- Sutron: SatLink 3 8800-1207 Rev 8.77.0, XLink 8800-1218 Rev 4: OK (Hach CDN).
- In-Situ: first search found no lightning/surge guidance (only RuggedCable shield spec).
- Campbell CR1000 brochure OK. YSI Storm 3 GSG Rev D and D114 OK; Storm 3 spec sheet dead end. In-Situ dead end (2 searches).
- Not covered: Hach (other than as Sutron host), HOBOnet RXW stations, Campbell CR800 manual.

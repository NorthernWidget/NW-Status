# COMPLETE

# USB inrush and bulk-capacitance rules for a USB-C Default-power sink (agent report, 2026-11-09)

Question: what USB requires of a device's inrush current and VBUS bulk capacitance at attach, for a Margay-class logger (USB-C receptacle, Rd 5.1 kOhm on CC1/CC2, sink only, USB 2.0 data via FT231X; about 10 uF on VBUS ahead of an LM66100 ideal diode, about 70 uF effective behind it).

## Conclusions for Margay (read first; each traces to a numbered section below)

1. **Binding limit.** As an Rd-only USB-C sink with a USB 2.0 data function, Margay is not a Power Sinking Device and cannot use PD (Type-C R2.5 4.5.2.2.5, 4.6.2.1; section 2). Type-C hands it to USB 2.0, and USB 2.0 7.2.4.1 sets the attach load at no more than 10 µF in parallel with 44 Ω, where the 10 µF counts "any capacitive effects visible through the regulator" (section 1a). Three further conditions hold: (1) Type-C Table 4-3 caps the receptacle's VBUS capacitance at 10 µF while not attached (2a); (2) the Device Capacitance ECN requires at least 1 µF across 0-5.25 V (1c); and (3) the device draws no more than one unit load, 100 mA, until configured (1d). The compliance test judges this as an inrush charge under 50 µC (4b, 4c; USB-IF's own wording in the OTG supplement is "an inrush charge equivalent to that stored on a capacitance of CRPB max", 4e). PD's 100 µF cSnkBulkPd needs a negotiated contract and does not apply (3a). BC 1.2 adds nothing (3b).

2. **Margay as described fails it.** The caller's 70 µF behind the LM66100 plus 10 µF ahead of it is 80 µF x 5 V = 400 µC (computed), 8 times the 50 µC limit. The LM66100 closes in about 27 µs with no slew control, and no source is required to slew-limit VBUS at attach (PD R3.3 4.1.4; 5f). The 10 µF ahead of the diode alone is 50 µC at 5 V: at the limit with no margin, and at the Type-C 10 µF ceiling.

3. **Soft-start does make more capacitance compliant.** USB 2.0 7.2.4.1: "If more bypass capacitance is required in the device, then the device must incorporate some form of VBUS surge current limiting, such that it matches the characteristics of the above load." PD 4.2.2 says the same: capacitance beyond the limit "is permitted provided it is isolated from VBUS through current-limiting circuitry". The condition, from the test method (4b, 4c): the total VBUS current at attach, capacitor charging plus the board's own load, stays at or below 100 mA. Current above 100 mA opens the integration window, and then the whole charge counts. Charging 80 µF to 5 V at 100 mA takes at least 4 ms (computed), and longer since the board load shares the 100 mA. Capacitance ahead of the limiter still counts in full against the 10 µF.

4. **What happens if the limit is exceeded.** Nothing dramatic at a protected port, but VBUS droops. Host and hub port switches current-limit, at 0.75-1.25 A for the TPS2051B, and deglitch their overcurrent flag for 4-15 ms (TPS2051B) or 7.5 ms typical (TPS2553-1 latch) "to eliminate false overcurrent reporting [...] starting into a heavy capacitive load" (5a, 5b). Charging 80 µF at 0.75-1.25 A takes 0.32-0.53 ms (computed), so the port neither flags nor latches. A PPTC trips on a scale of 0.1 s or more (MF-MSMF110: 0.3 s max at 8 A) and will not trip on 400 µC (5g). The cost is the droop: the 330 mV hub budget exists to protect other devices on the hub (1a). Idealized charge sharing from a 120 µF hub bulk into 80 µF gives 3.0 V, against 4.62 V for a 10 µF device (computed, upper bound; 5d). TI measured an unslewed 100 µF pulling a 3.3 V rail to 960 mV and warns that neighbors "may reset themselves" (5i). Type-C sources current-limit at their advertised level (Type-C 4.6.2.1: "A Source [...] shall protect itself"); TI notes a USB-C source may detect overcurrent and drop to a lower power state (5e). TI's own reading of the 10 µF receptacle rule is protection of "legacy USB sources that are not designed to handle the larger inrush capacitance" via A-to-C cables (5h).

5. **Not found (open).** No source located measures how real hosts or wall chargers behave with a 70-100 µF attach load. The practice statements above rest on switch and PPTC datasheets and arithmetic, not on host measurements. Nor was the USB-IF's Type-C-specific inrush test condition found ("Type-C SNK and DRP Inrush testing need to be do under different conditions", testusb.com, 4c).

## Quoted rules

### 1. USB 2.0 Specification

Document: Universal Serial Bus Specification, Revision 2.0, April 27, 2000 (`usb_20.pdf`), from the USB-IF package `usb_20_20250603.zip`, downloaded directly from https://usb.org/sites/default/files/usb_20_20250603.zip (linked from https://www.usb.org/document-library/usb-20-specification; no terms page in the way). Text extracted with `pdftotext -layout`.

**1a. Section 7.2.4.1 Inrush Current Limiting (p. 177), verbatim:**

> When a function or hub is plugged into the network, it has a certain amount of on-board capacitance between VBUS and ground. In addition, the regulator on the device may supply current to its output bypass capacitance and to the function as soon as power is applied. Consequently, if no measures are taken to prevent it, there could be a surge of current into the device which might pull the VBUS on the hub below its minimum operating level. [...] An additional motivation for limiting inrush current is to minimize contact arcing, thereby prolonging connector contact life.
>
> The maximum droop in the hub VBUS is 330 mV, or about 10% of the nominal signal swing from the function. In order to meet this requirement, the following conditions must be met:
>
> - The maximum load (CRPB) that can be placed at the downstream end of a cable is 10 µF in parallel with 44 Ω. The 10 µF capacitance represents any bypass capacitor directly connected across the VBUS lines in the function plus any capacitive effects visible through the regulator in the device. The 44 Ω resistance represents one unit load of current drawn by the device during connect.
> - If more bypass capacitance is required in the device, then the device must incorporate some form of VBUS surge current limiting, such that it matches the characteristics of the above load.
> - The hub downstream facing port VBUS power lines must be bypassed (CHPB) with no less than 120 µF of low-ESR capacitance per hub. [...]
>
> [...] A high-power bus-powered device that is switching from a lower power configuration to a higher power configuration must not cause droop > 330 mV on the VBUS at its upstream hub. The device can meet this by ensuring that changes in the capacitive load it presents do not exceed 10 µF.

Reading (mine, not the spec's): the 10 µF counts "any capacitive effects visible through the regulator", so capacitance behind a switch that closes during attach (the LM66100 at about 27 µs) is part of CRPB. More than 10 µF is allowed only with surge limiting that makes the device "match the characteristics of" 10 µF parallel 44 Ω. The spec itself states no charge (µC) number; see 1d.

**1b. Table 7-7 DC Electrical Characteristics (p. 178), Decoupling Capacitance rows, verbatim:**

> Downstream Facing Port Bypass Capacitance (per hub) | CHPB | VBUS to GND, Section 7.2.4.1 | min 120 µF
> Upstream Facing Port Bypass Capacitance | CRPB | VBUS to GND; Note 9, Section 7.2.4.1 | min 1.0, max 10.0 µF
>
> Note 9: The maximum load specification is the maximum effective capacitive load allowed that meets the target VBUS drop of 330 mV.

**1c. Device Capacitance ECN** (`Device Capacitance ECN.pdf`, same package), applies to USB 2.0. Changes 7.2.4.2 from "A minimum of 1.0uF is recommended" to:

> A USB device is required to expose a capacitance on the VBUS pin of its connector of CRPB. This capacitance shall be greater than CRPB min for voltages on the VBUS pin from 0V to 5.25V, regardless of whether the USB device is powered or unpowered.

and Table 7-7 CRPB to "VBUS to GND across the whole VBUS voltage range (0 - 5.25V); Note 9, Section 7.2.4.1 | 1.0 | 10.0 µF". The ECN states: "Method of testing this is inrush." Consequence: the 1 µF floor must hold at 0 V bias as well as at 5 V (DC bias derating applies to the minimum too).

**1d. Unit load and current during attach.** Section 7.2.1 (p. 172):

> A unit load is defined to be 100 mA. The number of unit loads a device can draw is an absolute maximum, not an average over time. [...] All devices default to low-power. [...] Self-powered functions: May draw up to one unit load from VBUS [...] Devices must also ensure that the maximum operating current drawn by a device is one unit load, until configured.

Section 7.2.3 (p. 176, on wake from suspend, the same principle stated for a transient): "The device must have sufficient on-board bypass capacitance or a controlled power-on sequence such that the current drawn from the hub does not exceed the maximum current capability of the port at any time while the device is waking up."

The 44 Ω in 7.2.4.1 is the attach-time 100 mA (5 V / 44 Ω = 114 mA at 5 V, computed). So the spec's position for a device with more than 10 µF: limit the surge so the port sees no worse than 10 µF || 44 Ω; the steady attach draw is one unit load (100 mA) until configured.

Grep of every PDF in the USB 2.0 package for "inrush", "CRPB" and "µC" found hits only in `usb_20.pdf`, the Device Capacitance ECN, and the OTG/EH supplement; no errata or ECN changes 7.2.4.1 itself.

### 2. USB Type-C Cable and Connector Specification

Document: USB Type-C Cable and Connector Specification, Release 2.5, March 2026 (`USB Type-C Spec R2.5 - March 2026.pdf`), from `USB Type-C 2.5 Release 202603.zip`, downloaded directly from https://usb.org/sites/default/files/USB%20Type-C%202.5%20Release%20202603.zip (linked from https://www.usb.org/document-library/usb-type-cr-cable-and-connector-specification-release-24, which now serves R2.5; no terms page). Page numbers are the printed ones.

**Finding: cSnkBulk, cSnkBulkPd and any tSnkInrush are not Type-C parameters.** A search of the R2.5 text for "cSnkBulk" finds one mention only, in an informative appendix on EPR disconnect arcing (line "voltage is determined by the Sink load current and the Sink VBUS and USB PD bulk capacitance (cSnkBulkPd)"). "tSnkInrush" does not occur. Type-C defines no inrush limit of its own for a Default-power sink; it hands that to USB 2.0 (2b, 2c).

**2a. Table 4-3 VBUS Sink Characteristics (p. 153), row verbatim:**

> VBUS Capacitance | Maximum 10 μF | Capacitance between VBUS and GND pins on receptacle when not in Attached.SNK.

(The table's Note 1, "See Section 4.5.2.2.5.2 with regard to applicability of this requirement", attaches to the vSinkDisconnect rows.) For comparison, Table 4-2 (p. 152) limits a DRP's receptacle VBUS capacitance to 10 μF and a source-only port's to 3000 μF "when VBUS is not being sourced".

**2b. Section 4.5.2.2.3 (p. 182) and 4.5.2.2.5 (p. 183), on a simple Rd-only sink, verbatim:**

> A USB 2.0 only Sink that doesn't support accessories and is self-powered or requires only default power and does not support USB PD may transition directly to Attached.SNK when VBUS is detected.
>
> A port that entered this state directly from Unattached.SNK due to detecting VBUS shall not determine orientation or availability of higher than Default USB Power and shall not use USB PD.

Section 4.5.2.3.1.1 PowerDefault.SNK (p. 201): "The port shall draw no more than the default USB power from VBUS. See Section 4.6.2.1."

**2c. Section 4.6.2.1 USB Type-C Current (pp. 227-228; the "shall protect itself" sentence is on p. 228), verbatim:**

> Default USB voltage and current are defined by the USB 2.0 and USB 3.2 specifications. [...] Default is the as-configured for high-power operation current value as defined by the USB Specification (500 mA for USB 2.0 ports [...]).
>
> When a Source is advertising USB Type-C Default current, the Sink behavior is defined as follows:
> - It connects as a USB 2.0 or USB 3.2 device, after which the Sink shall follow the appropriate USB specification. [...]
> - It attaches as a USB Type-C Power Sinking Device (PSD), after which the Sink may draw up to 500 mA and shall meet the inrush requirement for USB 2.0.
>
> [...] A PSD shall not have a USB or USB Type-C Alternate Mode communications function.
>
> A Source (port supplying VBUS) shall protect itself from a Sink that draws current more than the port's USB Type-C Current advertisement.

Reading (mine): Margay has a USB data function (FT231X), so it is not a PSD; it "connects as a USB 2.0 device" and follows USB 2.0, including 7.2.4.1 (10 µF || 44 Ω, or surge limiting to match it) and one unit load until configured. Even a data-less PSD is held to "the inrush requirement for USB 2.0". Type-C Table 4-3 adds a separate 10 µF cap on what the receptacle shows before the sink is attached; the 10 µF ahead of the LM66100 is at that ceiling with no margin, and the 70 µF behind the diode joins once VBUS appears, which is the inrush case of 7.2.4.1.

**2d. Source timing, Table 4-32 (p. 248):** "tVBUSON 0 ms min, 275 ms max: From entry to Attached.SRC until VBUS reaches the minimum vSafe5V threshold as measured at the source's receptacle." Type-C sources apply VBUS only after CC detects Rd, through a switch whose ramp the source controls; this bounds the source's own dV/dt but is not a sink inrush limit.

The R2.5 package also holds nine R2.4 ECNs (all incorporated into R2.5); their titles concern CC voltages, Ra, Rp, Attached.SRC VBUS duration, PDP and accessory states. None is titled on inrush or sink capacitance (titles checked; contents not read).

### 3. USB Power Delivery and Battery Charging

**3a. USB Power Delivery Specification, Revision 3.3, Version 1.0, October 2026** (`USB_PD_R3.3_V1.0_2026_10_16.pdf`), from https://www.usb.org/sites/default/files/USB_PD_R3.3_V1.0.zip (linked from https://www.usb.org/document-library/usb-power-delivery; no terms page).

Table 4.8 Sink Electrical Parameters (Section 4.7.2, p. 87), verbatim:

> cSnkBulk | Max: See [USB3] | Sink bulk capacitance on VBUS at Attach and during FRS after the Initial Source stops sourcing and prior to establishing the First Explicit Contract.
> cSnkBulkPd | Max: 100 µF | Bulk Capacitance that a Sink is allowed to present on VBUS after a successful Negotiation.
> iLoadStepRate | Max: 150 mA/µs | Load step di/dt.
>
> Note 1. If more bypass capacitance than cSnkBulk (max) or cSnkBulkPd (max) is required in the Device, then the Device Shall incorporate some form of VBUS surge current limiting as described in [USB3].

[USB3] is "Universal Serial Bus 3.2 Specification" (PD reference list). Section 4.2.2 Sink Bulk Capacitance (p. 66), verbatim:

> The total Sink bulk capacitance Connected to VBUS Shall not exceed cSnkBulk or cSnkBulkPd limits. The capacitance value May be changed at any time, provided the change: does not cause a transient current on VBUS that violates the maximum allowed current of the present Contract; does not cause iSnkStdby to be exceeded during positive load transitions; Guarantees the rate of change of currents stays below iLoadStepRate.
>
> Capacitance beyond the cSnkBulk or cSnkBulkPd limit is permitted provided it is isolated from VBUS through current-limiting circuitry as described in [USB3].

Table 4.7 Source Electrical Parameters (p. 82): cSrcBulk min 10 µF ("when a Port is powered from a dedicated supply"); cSrcBulkShared min 120 µF ("when a Port is powered from a shared supply").

Does PD change the answer? No. The 100 µF cSnkBulkPd is allowed only "after a successful Negotiation"; an Rd-only sink "shall not use USB PD" (Type-C 2b) and never negotiates, so it stays at cSnkBulk, which PD defers to the USB 3.2 figure (10 µF; see 3c). PD's useful contribution is the explicit statement that capacitance beyond the limit is allowed only behind current-limiting circuitry, and the 150 mA/µs di/dt figure used inside PD contracts. cSrcBulk is relevant to practice: a PD source from a dedicated supply is required to carry only 10 µF minimum, against USB 2.0's 120 µF per hub.

**3b. Battery Charging Specification, Revision 1.2, March 15, 2012** (`BC1.2 plus errata 2012-3-15.pdf`), from https://www.usb.org/sites/default/files/BCv1.2_070312_0.zip (linked from https://www.usb.org/document-library/battery-charging-v12-spec-and-adopters-agreement; no terms page). Section 2.2 (Dead Battery Provision, unconfigured clause, p. 4): "Passes inrush test: PD with Dead or Weak Battery shall pass USB-IF compliance inrush test." BC 1.2 adds no capacitance number of its own (grep for "inrush", "capacitance", "µF" finds only this line and D+/D- or ACA capacitances). It does not change the answer; it only confirms the compliance inrush test applies even under the dead-battery allowance.

**3c. Universal Serial Bus 3.2 Specification, Revision 1.1, June 2022** (`USB 3.2 Revision 1.1.pdf`), from https://www.usb.org/sites/default/files/usb_32_202206_1.zip (linked from https://www.usb.org/document-library/usb-32-revision-11-june-2022; no terms page). Read because PD's cSnkBulk points to [USB3]. Section 11.4.4.1 Inrush Current Limiting (pp. 469-470), verbatim on the points that differ from USB 2.0:

> The maximum droop possible in the bus-powered hub VBUS is 330 mV. [...] The maximum load (CRPB) that can be placed at the downstream end of a cable is 10 µF in parallel with as small as a 27 Ω resistance. The 10 µF capacitance represents any bypass capacitor directly connected across the VBUS lines in the device plus any capacitive effects visible through the regulator in the device. The 27 Ω resistance represents one unit load of current drawn by the device during connect.
>
> If more bypass capacitance is required in the device, then the device must incorporate some form of VBUS surge current limiting, such that it matches the characteristics of the above load.

The USB 3.2 unit load is 150 mA (5 V / 27 Ω = 185 mA, computed; USB 3.2 Section 11.4.1: "unit load [...] for single-lane operation is 150 mA"). The 10 µF figure is the same as USB 2.0. Margay is a USB 2.0 device, so the USB 2.0 version (10 µF || 44 Ω, 100 mA unit load) is the one that applies to it.

### 4. Where the 50 µC figure comes from (compliance test, not the specification)

The USB 2.0 specification text states no charge limit (grep of `usb_20.pdf` for "µC" and "coulomb": no hits). The 50 µC is the pass criterion of the USB-IF compliance inrush test, which integrates the current drawn at attach.

**4a. USB 2.0 Electrical Compliance Test Specification, Version 1.08, April 2026** (USB-IF), https://www.usb.org/sites/default/files/USB2%20Electrical%20Compliance%20Specification%20v1.08.pdf (direct, 12 pages). Section 2 lists "Inrush" among the Upstream Facing Port tests, and notes "Multiple upstream facing ports are only allowed on USB products with USB Type-C connectors". It gives no limit or procedure for inrush. Dead end for the number.

**4b. Siglent, USB 2.0 Electrical Compliance Test User Manual, EN01A** (oscilloscope vendor procedure; third party, not USB-IF), https://www.int.siglent.com/u_file/download/24_03_22/USB%202.0%20Electrical%20Compliance%20Test%20User%20Manual_EN01A.pdf, Section 8.11.2 Test Results Reference (p. 73), verbatim:

> Inrush current test results are calculated by taking the first 100mA as the starting point and 100us after the last 100mA as the end point, and calculating the charge between the two, which is required to be less than 50uC.

Section 2 of the same manual names USBET20 as the "USB IF official electrical analysis tool that to analyze the signal data captured by the oscilloscope, including signal quality and inrush analysis" (https://www.usb.org/document-library/usbet20).

**4c. testusb.com, "Inrush Current"** (third-party compliance-test site, not USB-IF), http://testusb.com/inrush_issue.htm (https redirects to http), verbatim:

> The USB 2.0 Spec allows a maximum capacity of 10uF and therefore a maximum Inrush of 50uC.
> Inrush current is measured for a minimum of 100 milliseconds after attach. Attach is defined as voltage rising to a valid level on the peripherals USB power line.
> Pass/Fail determination is done by the region having the highest charge value.
> [The device] cannot consume more that 100mA during this 100ms of the start up.
> The failures for Inrush mostly occur due to a too large capacity between Vbus and GND.
> Note that for Type-C SNK and DRP Inrush testing need to be do under different conditions.

The page refers to an "Inrush Test procedure V9.pdf" for the Type-C conditions but does not state them.

Reading of the test (mine, from 4b and 4c): the test integrates all the current inside a window that opens at the first crossing of 100 mA and closes 100 µs after the last crossing. Current held at or below 100 mA (one unit load) for the whole attach opens no window, and the measured inrush is then near zero whatever the capacitance. A soft-start that charges at, say, 150 mA still opens a window spanning the whole ramp, and the whole charge counts. So the operative condition for soft-start is a peak attach current at or below 100 mA, not merely a slow ramp. This is how "surge current limiting, such that it matches the characteristics of" 10 µF || 44 Ω (USB 2.0 7.2.4.1) is judged in practice. The 50 µC equals 10 µF times 5 V (computed), i.e. the charge into the largest allowed capacitor. USB-IF does not publish the USBET20 algorithm in any document found here; the window description is Siglent's.

**4d. Margay numbers against this test (computed, from the caller's figures):** 70 µF effective plus 10 µF on VBUS, charged 0 to 5 V, is 80 µF x 5 V = 400 µC, against the 50 µC pass limit (8x over). Even the 10 µF ahead of the LM66100 alone is 50 µC at 5 V, at the limit with no margin. The LM66100 turning on in about 27 µs with no slew control means the 70 µF charges at whatever current the source and cable allow; the current is expected to sit far above 100 mA for the whole charge (an inference, not measured), so all of it lands in the measured window.

**4e. The USB-IF's own charge statement: On-The-Go and Embedded Host Supplement to the USB Revision 2.0 Specification, Revision 2.0 version 1.1a, July 27, 2012** (`USB_OTG_and_EH_2-0-version 1_1a.pdf`, in the same usb.org USB 2.0 package as 1). Section 4.3.3 VBUS Inrush and Transient Current (p. 15), verbatim:

> Upon being attached to an A-device, an SRP-capable B-device is allowed to draw an inrush charge equivalent to that stored on a capacitance of CRPB max ([USB2.0] Table 7-7) when charged to a voltage of VA_VBUS_AVG_LO max.

Table (p. 16): "VBUS Average Voltage | VA_VBUS_AVG_LO | 4.4 min, 5.25 max V". So in USB-IF's own words the inrush allowance is a charge, 10 µF x 5.25 V = 52.5 µC (computed). This clause is written for SRP-capable B-devices, which Margay is not; it is quoted because it is the only USB-IF text found that states the rule as a charge. The 50 µC compliance figure (4b, 4c) is the same quantity at 5 V.

### 5. Practice: what the host port does with an oversized capacitive load

**5a. TI TPS20xxB (TPS2041B-TPS2054B) Current-Limited Power-Distribution Switches, SLVS514Q, revised October 2026**, https://www.ti.com/lit/ds/symlink/tps2051b.pdf. A common host/hub port switch. Features: "500mA continuous current"; "Accurate current limit (0.75A minimum, 1.25A maximum)". Section 8.3.7.2, verbatim:

> In the second condition, a short or an overload occurs while the device is enabled. At the instant the overload occurs, high currents can flow for a short period of time before the current-limit circuit can react. After the short-circuit output current threshold (IOS) is reached, the device switches into constant-current mode.

Section 9.2.1.2.2 OC Response, verbatim:

> The OCx open-drain output is asserted (active low) when an overcurrent or overtemperature shutdown condition is encountered after a 10ms deglitch timeout. [...] Connecting a heavy capacitive load to an enabled device can cause a momentary overcurrent condition; however, no false reporting on OCx occurs due to the 10ms deglitch circuit.

Electrical table: "OC deglitch | OCx assertion or deassertion | 4 min, 8 typ, 15 max ms". USB application section (p. 28), verbatim:

> Hosts and self-powered hubs must: Current-limit downstream ports; Report overcurrent conditions on USB VBUS. Bus-powered hubs must: [...] Limit inrush current (<44Ω and 10µF). Functions must: Limit inrush currents; Power up at <100mA.

**5b. TI TPS2552/TPS2553 (and -1 latch-off variants), SLVS841G, revised October 2026**, https://www.ti.com/lit/ds/symlink/tps2553.pdf. Section 8.3.1, verbatim:

> The TPS255x-1 limits the current to IOS until the overload condition is removed or the internal deglitch time is reached and the device is latched off.
>
> [Section 8.3.3] The TPS255x and TPS255x-1 are designed to eliminate false FAULT reporting by using an internal delay de-glitch circuit for overcurrent (7.5ms typical) [...] This confirms that FAULT is not accidentally asserted due to normal operation such as starting into a heavy capacitive load.

Section 9.3.2, verbatim: "High-power functions must draw less than 100mA at power up and can draw up to 500mA after enumeration. If the load of the function is more than the parallel combination of 44Ω and 10µF at power up, the device must implement inrush current limiting."

**5c. Applying 5a and 5b to Margay (computed, my arithmetic, not from the sources):** at a constant-current limit I, 80 µF charges to 5 V in t = C·V/I. At the TPS2051B minimum 0.75 A: 80e-6 x 5 / 0.75 = 0.53 ms; at 1.25 A: 0.32 ms. Both are more than an order of magnitude below the 4 ms minimum OC deglitch of the TPS2051B and the 7.5 ms typical of the TPS2553-1 latch. So a switch-protected host port rides through: it current-limits for under a millisecond, does not flag overcurrent, and does not latch off. The cost is on the port's own VBUS: during that time the port output is in current limit and its voltage sags, so other loads on the same switch (a ganged hub port pair) see the dip.

**5d. Hub-side droop by charge sharing (computed, an idealization):** the USB 2.0 hub-side bulk is CHPB at least 120 µF (1a). If the port capacitance discharged into the device faster than the switch or regulator could replace charge, ideal charge sharing gives V = 5 V x 120 / (120 + C_device). For C_device = 10 µF: 4.62 V (0.38 V droop, close to the spec's 330 mV target, which the 44 Ω and cable resistance soften). For C_device = 80 µF: 3.0 V (2.0 V droop). Cable resistance and inductance slow the transfer and the regulator refills during it, so the real dip is smaller; but this is the mechanism by which a large device capacitance pulls VBUS out of tolerance for the other ports of a hub (USB 2.0 7.2.4.1 rationale).

**5e. TI SDAA479, "Inrush Current Control for the BQ2579X Input MUX FETs", August 2026**, https://www.ti.com/lit/pdf/SDAA479. Section 1, verbatim:

> For example, if a USB-C source has negotiated only 500mA output current but the inrush current is 1.5A, the USB-C source detects over current and drops to a lower power state. Designers often consider adding soft start circuitry to slowly charge high capacitive nodes to reduce the current spike. If the component preceding a capacitor is a MOSFET, a common method to reduce this current spike is to slow the FET's turn on time or slew rate and limit the downstream capacitor charging current.

Section 2.2 gives the sizing relation "IIN-RUSH = (CVBUS+CPMID) * dVBUS/dt" and claims "USB-C ports regulate the output voltage slew rate to 30mV/us." **That claim does not hold at attach, per the PD specification itself (5f).**

**5f. USB PD R3.3 V1.0 on source slew at attach** (same document as 3a). Table 4.7 (p. 85): "vSrcSlewPos | Max 30 mV/µs | Maximum slew rate allowed for positive voltage transitions. Limits current based on a 3 A connector rating and maximum Sink bulk capacitance of 100 µF." Section 4.1.4 Non-application of VBUS Slew Rate Limits (p. 62), verbatim:

> Scenarios where vSrcSlewPos and vPpsSlewPos VBUS slew rate limits do not apply and VBUS May transition faster than specified are as follows: When first applying VBUS after an Attach. [...]

Table 4.7 also: "tSrcTurnOn | Max 275 ms | Transition time from vSafe0V to vSafe5V" (a ceiling on how slow, not how fast). So no USB document bounds how fast a source brings VBUS up at attach; the sink cannot rely on the source to soft-start it. With a legacy Standard-A host and an A-to-C cable, VBUS is live before contact (Type-C R2.5 Section 4.4.2 exempts "Legacy hosts/chargers that by default source VBUS when connected using any legacy USB connector"), so attach is a hot-plug step limited only by cable and switch.

Reading (mine): if a source did ramp at 30 mV/µs, 80 µF would draw 80e-6 x 30e3 = 2.4 A (computed), which is why PD caps cSnkBulkPd at 100 µF against a 3 A connector. That same arithmetic says a Default-power USB 2.0 port (500 mA configured, 100 mA unconfigured) is the wrong place for 80 µF without a limiter.

**5g. Polyfuse (PPTC) host protection.** Bourns MF-MSMF Series PTC Resettable Fuses datasheet, Rev. BE, 09/26, https://www.bourns.com/docs/product-datasheets/mf-msmf.pdf, Electrical Characteristics table, row MF-MSMF110 (a typical single-port USB part): Ihold 1.10 A; Itrip 2.20 A; resistance 0.06 Ω min, 0.21 Ω R1max at 23 °C; max time to trip 0.3 s at 8.0 A. Bourns, "Protecting Powerful USB 3.0 Interfaces", e/CPK1051, 10/10, https://www.bourns.com/docs/technical-documents/technical-library/circuit-protection/application-notes/bourns_cpk1051_usb3_appnote.pdf, verbatim: "the USB interface must withstand the threats of hot plugging, short circuits, faulty equipment, and user error. Polymer Positive Temperature Coefficient (PPTC) devices have typically been used to help protect the power port from overcurrent conditions [...] One requirement of USB is that the overcurrent solution be resettable."

Reading (computed, mine): a PPTC trips on heat, on a scale of 0.1 s or more at several amps. Charging 80 µF to 5 V moves 400 µC; even at 8 A that takes 50 µs, roughly three orders of magnitude shorter than the 0.3 s figure. A polyfuse-protected port will not trip on this inrush. Its 0.06-0.21 Ω series resistance, with the cable, is what bounds the peak current, and the host's own bulk capacitance supplies it; the droop then falls on whatever else shares that port's VBUS rail.

**5h. TI TPS25740B USB Type-C source controller, SLVSDR6C, revised March 2018**, https://www.ti.com/lit/ds/symlink/tps25740b.pdf, Section 8.1.1 VBUS Capacitance, verbatim (TI's reading of the Type-C 10 µF receptacle rule):

> The USB Type-C specification requires that the capacitance on the VBUS pin of an empty receptacle be below 10 µF. This is to protect legacy USB sources that are not designed to handle the larger inrush capacitance and which may be connected via an A-to-C cable. For applications with USB Type-C receptacles and large bulk capacitance, this means back-to-back blocking FETs are required as shown in Figure 21.

**5i. TI SLVA670A, "Managing Inrush Current", August 2014, revised May 2015**, https://www.ti.com/lit/pdf/slva670, Sections 1.1 and 4.1.1, verbatim (bench measurements of an unslewed 100 µF on a regulated rail):

> Figure 4 is an example of a 100 µF capacitance being applied to a voltage supply without any slew rate control. The capacitance generates 6.88 A of inrush current and forces the voltage rail to drop from 3.3 V down to 960 mV. [...] If other modules are connected to this power rail and the voltage drops, then these modules may reset themselves and put the rest of the system into an undesired state.
>
> The inrush current generated by the 100 µF capacitor peaks at 6.46 A and brings the 1.8 V rail down to 320 mV.

These are TI's measurements on their own test rails, not USB ports; they show the scale of an unslewed 100 µF step, and the failure mode for neighbors on the rail (reset), which is the hub-port case.

**5j. TI TPS25810 USB Type-C DFP controller and power switch, SLVSCR1C, revised July 2017**, https://www.ti.com/lit/ds/symlink/tps25810.pdf, Section 7.3.2 Current Capability Advertisement and Overload Protection, verbatim: "Under overload conditions, the internal current-limit regulator limits the output current to selected ILIM [...] the device maintains a constant output current, with the output voltage determined by (iOS x RLOAD)." A Type-C source of this kind current-limits and thermal-cycles rather than latching; at the 1.5-3 A class limits a 400 µC charge completes in well under a millisecond (computed: 400 µC / 1.5 A = 0.27 ms).

## Sources checked (including dead ends)

- usb.org USB 2.0 package (above): reached, direct download, no terms acceptance.
- usb.org Type-C R2.5 package (above): reached, direct download, no terms acceptance. Contains R2.5 and a redline against R2.4.
- usb.org USB PD R3.3 V1.0 package: reached, direct download. Contains R3.3 and its ECNs; ECN titles checked, none on sink bulk capacitance or inrush (one is titled "Updates and clarifications on source and sink requirements during transitions"; not read).
- usb.org BC 1.2 package: reached, direct download.
- usb.org USB 3.2 R1.1 package: reached, direct download.
- usb.org USB2 Electrical Compliance Test Specification v1.08: reached; lists the inrush test, gives no limit (dead end for the number).
- Siglent USB 2.0 compliance manual EN01A: reached; gives the 50 uC criterion and integration window.
- testusb.com inrush page: reached (https 301 to http); states 10 uF / 50 uC; refers to an unlinked "Inrush Test procedure V9.pdf" for Type-C conditions (not found).
- Web searches for a USB-IF document stating 50 uC: none found on usb.org.
- USB-IF USB Type-C Functional Test Specification, Chapters 4 and 5, Rev 0.91, March 3, 2024, https://www.usb.org/sites/default/files/USB%20Type%20C%20Functional%20Test%20Specification%202024%2003%2003.pdf: reached (direct). It carries assertion 4.4.2#2 on the Source's VBUS capacitance and 4.4.3#4 on 10 uF VCONN inrush capacitance for cables, but no sink VBUS inrush test or Type-C-specific inrush conditions. Dead end for the "different conditions" testusb.com mentions.
- ti.com/lit/ds/symlink/tps2051b.pdf and tps2553.pdf: reached (the ti.com/lit/pdf/<part> form returned 404 for datasheets; the symlink path works).
- ti.com/lit/pdf/slva892 (USB PD Compliance Tests, SLVA892A) and slvafr4 (TPS257xx-Q1 Pass Compliance): reached; no inrush text (grep for inrush, 44 ohm, 10 uF, droop). Dead ends.
- ti.com/lit/ds/symlink/tps2065c.pdf: reached; 6-12 ms FLT deglitch, nothing beyond 5a.
- ti.com/lit/pdf/SDAA479: reached.
- Bourns MF-MSMF datasheet and CPK1051 note (bourns.com): reached. Bourns USB OTG note (USBOTGAppNote.pdf): reached, no inrush text. Bourns high-speed comm ports note via ttiinc.com: HTTP 403, dead end. Mouser USB 3.0 circuit-protection page: fetch timed out, dead end. Micrel Application Note 17 (1998): found only on a third-party datasheet site, not fetched (old, and not an official host).
- OTG and EH Supplement 2.0 v1.1a (in the usb.org USB 2.0 package): read for the charge statement.
- ti.com TPS25740B, TPS25810, SLVA670: reached.
- analog.com LTC4160 datasheet (search snippet said it states a 33 uC OTG inrush limit and 6.5 uF): curl returned no file, WebFetch timed out. Dead end; the 33 uC figure is UNVERIFIED.
- Web search restricted to analog.com, st.com, microchip.com, onsemi.com, nxp.com for a USB device inrush app note: no on-topic hit beyond LTC4160. No ST or Microchip note was found that adds to the TI material.

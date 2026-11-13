# NW-Sim: DS3231M revision option, ATmega1284P sleep modes, Margay watchdog (agent report)

**COMPLETE**

Started 2026-11-10. NW-Sim HEAD at start: 7324ae5.

## Findings (appended as confirmed)

### Task 1: a non-A1 DS3231M option

- T0, before any change (NW-Sim 7324ae5): run.sh margay-3.0 OK=19, margay-3.1 OK=19; in_the_loop 2 + 2; chip_conformance 34 ok; usi_conformance 12 ok.
- D1. Errata 19-5311 Rev 0 6/10, read as pages (2 pages). Item 2, "BBSQW BIT FUNCTION IS NOT IDENTICAL TO DS3231": "DS3231 BBSQW bit (if = 1) enables SQW when operating on VBAT supply. DS3231M BBSQW bit (if = 1) enables SQW and RTC alarm interrupt when operating on VBAT supply. Workaround: Write BBSQW = 1 if user desires an RTC alarm interrupt during battery operation." Applies "only ... to DS3231M revision A1 components", top mark yywwA1.
- D2. Datasheet 19-5312 Rev 5, p.13 (read as a page image), Control register bit 6: "When BBSQW is logic 0, INT/SQW goes high impedance when VCC falls below VPF." No INTCN condition.
- D3. No primary source found that states the non-A1 behavior directly. The DS3231 (non-M) datasheet was not available locally and was not fetched; its BBSQW wording is known only as quoted in a forum post (BBSQW agent report, UNVERIFIED there). Default therefore stays revision A1 = the literal p.13 reading.
- M1. Part: `ds3231_revision_t revision` in ds3231_t, DS3231M_REV_A1 (0, default) or DS3231M_REV_NON_A1. Non-A1: the alarm drives INT/SQW on VBAT whatever BBSQW holds (BBSQW gates only the square wave, which is not modeled). Commit 7ac7f90.
- C1. Conformance: 6 new checks in tests/chip_conformance/check.c. With the revision field present and the behavior absent: "BBSQW = 0: an alarm match pulls INT/SQW low" FAILED (expected 0, got 1) and "BBSQW = 0: an asserted alarm stays low as VCC falls" FAILED (expected 0, got 1). With the behavior: 40 ok. The HEAD check.c against the new part: 34 ok. Commit a2992b8.
- M2. Flag `--ds3231m-rev a1|non-a1` in nw_sim, carried by board_margay_env_t.rtc_revision; stderr says so when non-a1.
- X1. With DS3231_Logger 2d6925b (BBSQW = 0) on margay-3.0, 25 s, simulator before the sleep model: --ds3231m-rev a1 gives "4 INT low on VCC" (each after the core had already woken and switched the rail on); non-a1 gives "4 INT low on VBAT". Both log 5 rows, because the core does not yet sleep (task 2).

### Task 2: ATmega1284P sleep modes

- S1. simavr d6aed536 has no sleep-mode model: SLEEP (sim_core.c, opcode 0x9588) sets cpu_Sleeping without reading SE or SMCR; avr_raise_interrupt() (sim_interrupts.c) sets cpu_Running for any enabled vector; nothing under simavr/sim or simavr/cores reads SMCR.
- D4. ATmega164A/PA/324A/PA/644A/PA/1284/P datasheet DS40002070B (Microchip 2020), read as pages 50-55 and 75-77. p.50: "To enter any of the sleep modes, the SE bit in SMCR must be written to logic one and a SLEEP instruction must be executed." Table 10-1 (p.50), wake sources: Idle all; ADC NR: INT2:0 and pin change, TWI address, Timer2 (note 2: if asynchronous), SPM/EEPROM, ADC, WDT; Power-down: INT2:0 and pin change, TWI address, WDT; Power-save: those plus Timer2; Standby as Power-down; Extended Standby as Power-save. p.52, 10.6: "Only an External Reset, a Watchdog Reset, a Brown-out Reset, two-wire Serial Interface address match, an external interrupt on INT2:0, or a pin change interrupt can wake up the MCU." p.55 Table 10-2: SM2:0 = 100, 101 Reserved. p.76: "Edges on INT2:INT0 are registered asynchronously."
- M3. simavr patch patches/simavr-atmega1284p-sleep.patch (187 lines): avr_t.sleep_ctl (SE, SM2:0, mode), avr_int_vector_t.wake_modes; SLEEP honors SE and records SM2:0; a sleeping core wakes only for a vector whose wake_modes holds the mode; other interrupts stay pending and are serviced after a legitimate wake; avr_service_interrupts() takes nothing while asleep; x4 core declares SMCR and fills wake_modes from Table 10-1. A core that does not declare SMCR behaves as upstream. Verified: upstream d6aed53 + USI patch + sleep patch reproduces the working tree byte for byte (12 files compared with cmp).
- M3 limits, stated in patches/README.md: counters keep counting in a stopped clock domain (TCNT0 moves, one held Timer0 overflow runs after the wake, so millis() gains one tick per sleep); start-up delay not modeled; asynchronous Timer2 in ADC NR not modeled; reserved SM2:0 values wake as upstream (a choice for Andy).
- C2. tests/sleep_conformance (firmware.c + check.c + run.sh), 24 checks. Against simavr with the USI patch only (a scratch tree): 13 ok, 11 FAILED (Timer0 wakes the core from Power-down, Power-save, ADC NR, Standby; Timer2 wakes it from Power-down; SLEEP without SE sleeps). With the patch: 24 ok.
- T3. simavr's Makefile does not track header dependencies: a plain make after the patch rebuilt only the changed sources while sim_avr.h's avr_t had grown. Rebuilt clean (make clean; make). Recorded in patches/README.md.
- X2. Margay Basic, today's DS3231_Logger (4179b06), margay-3.0, 25 s: "aux rail off" 293 times without the patch, 6 with it; 5 rows either way; INT low 4 times, all on VBAT.
- B1. Baselines with the patch: run.sh 11 OK, 8 FAIL on each board; in_the_loop 2 OK; transcripts identical except margay_nocard. Moved: LED edge times in margay_basic, walrus_margay, margay_programmed, margay_discovered, margay_missing, margay_overrun, margay_blank; margay_nocard lost its last row (00:00:24).
- B2. Cause, measured with a scratch nw_sim that timestamps the rail and INT (no-card Basic, margay-3.0): without the patch the core was already awake in a spurious Timer0 wake when the 00:00:23 alarm came (rail on at 22.394 s), so the cycle finished at 24.620 s; with the patch it wakes at 23.000 s and finishes at 25.226 s. 2.226 s of work either way; the 0.606 s head start was the spurious wake. The row is timestamped 00:00:25 and falls past the 25 s run (a 40 s run logs 00:00:25, 32, 39 against 24, 30, 37 before). The LED edges now sit a fixed 204 ms after each alarm second (6204, 11204, 16204, 21204 ms in margay_basic) where they drifted (6216, 11213, 16212, 21211 ms). Baselines re-recorded on both boards for this cause; the .commits files change only in simavr's patch hash (9134cd10e62ed202 -> 7f42185ce1508297).
- X3. Demonstration, committed sleep model, DS3231_Logger 2d6925b (BBSQW = 0), Basic, 25 s: margay-3.0 --ds3231m-rev a1: 1 row (00:00:01 LoggingStarted), INT low 0 times, rail off twice, never wakes again. margay-3.0 non-a1: 5 rows, INT low 4 times on VBAT. margay-3.1 a1 and non-a1: 5 rows, INT low 4 times on VCC.

### Task 1 addendum: the TPS7A05 EN fact

- D5. TI SBVS254D, p.8 (read as a page): IEN, "EN pin current", VEN = VIN = 5.5 V, 10 nA in the TYP column (no MAX given); RPULLDOWN 120 ohm, "VIN = 3.3 V, P version only". The caller's brief said "10 nA max"; the datasheet gives it as typical. Netlist: 3V3_AUX_CTRL = U1 pin 25 (PC6) and U7 pin 3 (EN) only. Recorded as an assumption in src/boards/margay.c and README (commit 6fb24c2).

### Task 3: the Margay's hardware watchdog

- N1. Netlist: Project-Margay a8a4a6f, `kicad-cli sch export netlist --format kicadxml` of Hardware/KiCAD/Margay.kicad_sch into scratchpad sw/net/margay.xml. U3 = TPL5010DDC (value and libsource "TPL5010DDC").
- N2. U3 pin 1 VDD on 3V3 (always-on, U6 TPS797 VOUT); pin 2 GND; pin 3 DELAY on Net-(U3-DELAY) = R10 pin 2, R10 = 130k, R10 pin 1 on GND; pin 4 DONE on net WD_HOLD = U1 pin 26, PC7 (PCINT23/TOSC2), Arduino D23; pin 5 WAKE unconnected ("unconnected-(U3-WAKE-Pad5)"); pin 6 RSTN on net RST = U1 pin 4 RESET, R2 10k pull-up to 3V3, S1 (reset button), ISP1 pin 5, and C1 0.1 uF whose other side is /Digital_Core/DTR (U2 FT231X DTR#, the auto-reset).
- D6. TPL5010, TI SNAS651A, read as pages 4-14. Pin functions p.4. p.6: t_Rext 100 ms typ (120 max), tRSTn 320 ms typ, tWAKE 20 ms typ, tDONE 100 ns min. p.9, 8.3: "After receiving the WAKE pulse, the uC must issue a DONE signal to the TPL5010 at least 20 ms before the rising edge of the next WAKE pulse. If the DONE signal is not asserted, the TPL5010 asserts the RSTn signal to reset the uC." 8.3.1: WAKE is sent "when the programmed time interval starts (except at the beginning of the first cycle or if in the previous interval the DONE has not been received)". 8.3.2: "a valid DONE signal as a low to high transition"; DONE while WAKE high ends WAKE. p.10, 8.3.3: "During the POR and the reading of the REXT, the RSTn signal is LOW." 8.5.1: REXT 500 ohm to 170 kohm. p.13, Table 1 coefficients, Equation 2 example "8 s ... 10.18 kOhm", Table 2 (500 ohm to 4.5 kohm = 100-900 ms). p.14, Equation 3: T_ADC = INT[(a RD^2 + b RD + c)/100], RD = REXT/100.
- D7. Period for R10 = 130 kohm, set 5: (0.3177 x 1300^2 - 136.2571 x 1300 + 34522.4680)/100 = 3943.01, INT 3943 s (65.7 min); computed by python in this session. Set 4 would give 3751 s, outside its 100-1000 s range. Agrees with resistor-minimum-set.md and with Margay_Library's comment (3943 s nominal); the model takes its value from the datasheet equation, not from the library.
- D8. Table 3's "closest real values" do not all reproduce under Equation 3's INT (11.199 kohm gives 9 s against the table's 10 s; 124.856 kohm gives 3596 s against 1 h): the table follows Equation 1's continuous curve, the device quantizes by Equation 3. The model uses Equation 3; the checks use only the worked example, Table 2, and Equation 3 for 130 kohm.
- D9. ATmega1284P reset, DS40002070B pp.58-60, 66 (read as pages): "During reset, all I/O Registers are set to their initial values, and the program starts execution from the Reset Vector." "The I/O ports of the AVR are immediately reset to their initial state when a reset source goes active." External reset: MCU starts tTOUT after RESET rises. Figure 11-3, "MCU Start-up, RESET Extended Externally". EXTRF: "This bit is set if an External Reset occurs."
- S2. simavr's avr_reset() (sim_avr.c) empties every cycle timer (avr_cycle_timer_reset) and sets avr->cycle = 0: a whole-simulation reset that would stop the DS3231's clock tick. And avr_cycle_timer_process() requeues the slot it is running after the callback returns, so a reset taken inside a timer callback corrupts the queue. Hence src/mcu_reset.c (keeps timers whose param lies outside the core's allocation, restores the cycle count, sets EXTRF) applied from nw_sim's run loop, not from the TPL5010's callback.
- C3. TPL5010 conformance, tests/chip_conformance (23 checks: 5 on the period, 18 on the watchdog with 10.18 kohm, tIP 8 s). All pass: chip_conformance 63 ok (40 before). Shown to bite, each against a scratch copy of tpl5010.c with one behavior broken: missed DONE gives WAKE not RSTn: 7 checks FAIL; no 20 ms margin: 1 FAIL ("a DONE 10 ms before the end is too late"); no POR hold: 8 FAIL; DONE not ending WAKE: 1 FAIL; Table 1 set 4 used for 130 kohm: 1 FAIL ("130 kohm gives 3943 s").
- C4. External reset checks, 8 new in tests/sleep_conformance (32 ok in all): time runs on, TIMSK0 and SMCR to 0, EXTRF set, core runs nothing while held (1000 avr_run calls), a board part's 1 ms timer keeps ticking, released core restarts from the reset vector and sleeps again. Shown to bite against scratch copies of src/mcu_reset.c: plain avr_reset (no timer keep, no cycle restore): 2 FAIL; no EXTRF: 1 FAIL; no hold: 3 FAIL.
- T4. Two defects found and fixed before commit, both in the first draft of the reset path: (1) the hold loop checked the RESET line before processing timers, so release at 0.420 s was seen only at the next timer (1.000 s): fixed by processing due timers after each advance; (2) avr_reset() sets IRQ_FLAG_INIT on every pin IRQ (measured: flags 0x6 -> 0xe on PC4), so the firmware's first write to each pin notified the board even when unchanged (spurious "led on" lines); the power-up hold therefore holds the core without avr_reset().
- X4. Basic, today's DS3231_Logger, margay-3.0, 25 s, with the watchdog: RSTn released at 0.420 s; every LED edge of the boot exactly 420 ms later (248 -> 668 ms, 1878 -> 2298 ms, 1992 -> 2412 ms); first row 00:00:02 instead of 00:00:01 and every later row 1 s later (boot now crosses a second boundary later); 5 rows; DONE at 4.016 s.
- X5. Demonstration, DS3231_Logger 2d6925b (BBSQW = 0), margay-3.0, --ds3231m-rev a1, 8000 s (2.3 s wall): row 00:00:02 LoggingStarted; one DONE in interval 1 (from the first row's resetWDT); interval 1 ends at 3943.42 s with a WAKE (unconnected); interval 2 has no DONE; "margay: the watchdog resets the MCU at 7886.420 s"; RSTn released 7886.740 s; on reboot the rail comes on, the clock returns to VCC with A1F still set and asserts INT at once, the firmware rewrites control 0x24 and clears it; second row 2026/01/01 02:11:28 LoggingStarted. 2 rows in 8000 s.
- X6. Same firmware (2d6925b), 8000 s: margay-3.1 (a1) and margay-3.0 with --ds3231m-rev non-a1 each log 1600 rows, INT low 1599 times, and are never reset (0 "watchdog resets" lines).
- B3. Baselines with the watchdog: run.sh 6 OK, 13 FAIL per board before re-recording. Cause: the 420 ms power-up hold. LED edges move by exactly 420 ms at boot; rows on a 5 s or shorter schedule move by 1 s (first row 00:00:02 for 00:00:01: margay_basic, margay_blank, margay_nocard, margay_overrun's first row); 60 s cases keep their row times. Row counts unchanged; .commits files unchanged; in_the_loop passed unchanged. Re-recorded on both boards (c09ef48).

## Final test counts (code at 1fb1c0e)

| Suite | margay-3.0 | margay-3.1 | Before (7324ae5) |
|---|---|---|---|
| tests/run.sh | 19 OK | 19 OK | 19 / 19 |
| tests/in_the_loop.sh | 2 OK | 2 OK | 2 / 2 |
| tests/chip_conformance/run.sh | 63 ok | – | 34 |
| tests/usi_conformance/run.sh | 12 ok | – | 12 |
| tests/sleep_conformance/run.sh (new) | 32 ok | – | – |

## Commits (NW-Sim, local, nothing pushed)

7ac7f90, a2992b8, 22feeb3 (task 1); ab0977d, 1089c6e, 4fcd010, 8cbf41d (task 2 and docs for 1-2); 6fb24c2 (rail assumption); c17da45, 4b8620a, e76ab52, 8cc1016, 4d1df36, c09ef48, 1fb1c0e (task 3).

## Proposal (not built)

A recorded case `margay_nobbsqw`: Margay Basic built against DS3231_Logger pinned at 2d6925b through the --pinned mechanism, on margay-3.0, run 8000 s (2.3 s wall). Its transcript pins both the missed alarm (one row) and the watchdog's recovery (a second LoggingStarted at 02:11:28). On margay-3.1 it would log 1600 rows, which is long for a baseline; a 25 s run there (5 rows) would carry the contrast.

## Open questions for Andy

1. Non-A1 DS3231M: no Maxim document states the behavior directly; the default stays A1 (literal datasheet). A bench check with BBSQW = 0 on a part whose top mark is not yywwA1 would settle it.
2. Reserved SM2:0 values (100, 101) wake on any interrupt, as upstream did: a choice, not a datasheet fact.
3. Not modeled: tTOUT after RESET rises (fuses unknown here), a bootloader after a watchdog reset, Timer0 counters frozen in Power-down (one held overflow runs after each wake), asynchronous Timer2 in ADC Noise Reduction, the SD card losing power with 3V3_AUX.
4. On a watchdog reset the model takes the floating EN of U7 as rail off and the floating select of U4 as the internal bus, the same assumption as at power-up.
5. Margay#61 (WAKE to PA7 on v3.1) is not in the netlist; the model leaves WAKE unconnected on both versions until it is.
6. The README "State" section's sample transcript (rows at 00:00:04, 00:00:08) predates this session and no longer matches the baselines; not changed here.
7. Brief correction: TPS7A05 IEN is 10 nA typical (SBVS254D p.8), not maximum.

## Sources checked (dead ends included)

- TPS7A05 datasheet TI SBVS254D (Feb 2018, rev Aug 2019), scratchpad cc/dl/tps7a05.pdf, read p.8 as a page.
- Project-Margay a8a4a6f KiCad schematic, exported netlist (see N1). NW-Status MARGAY-TODO.md section G: v3.1.0 plans TPL5010 WAKE to PA7 (Margay#61), not in the netlist; the model leaves WAKE unconnected on both versions.
- Dead end: no DS3231 (non-M) datasheet fetched; no Maxim statement of non-A1 VBAT alarm behavior found locally.

- DS3231M datasheet 19-5312 Rev 5 and errata 19-5311 Rev 0: the copies beside this report (sha256 as in 2026-11-10-nwsim-clock-rail-agent-report.md).
- ATmega164A/PA/324A/PA/644A/PA/1284/P datasheet, Microchip, PDF dated 2020-01-17 (scratchpad vrate_dl/atmega1284p.pdf, sha256 b5ee49362803dc705961f724da40af85ec14fbc03102b1716f0092775a679561).
- TPL5010 datasheet, TI SNAS651A (Jan 2015, rev Sep 2018), 27 pages, scratchpad cc/dl/tpl5010.pdf (sha256 a62ae27e1c3dd0cef4549fe4e7d10c637359804a09c74791e4814f6aa26a0f39); read as pages 4-14.
- simavr d6aed53 (../simavr): sim_interrupts.c avr_raise_interrupt() sets cpu_Running on any enabled interrupt; sim_core.c SLEEP (0x9588) enters cpu_Sleeping without reading SE or SMCR; no file under sim/ or cores/ references SMCR. simavr has no sleep-mode model.


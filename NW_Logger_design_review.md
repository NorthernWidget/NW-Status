# NW_Logger design review, 2026-09-24

Read-only review of the logger core extracted from Margay_Library, asked for by Andy on
2026-09-24: "Aim for something generalizable. If it needs special treatment in places, then it
should probably be split out into the individual repos. On the other hand, perhaps the repos
could be brought closer together." Nothing here is implemented and nothing is decided.

Sources read: `NW_Logger/src/NW_Logger.{h,cpp}`, `Margay_Library/src/Margay.{h,cpp}`,
`Okapi_Library/src/Okapi.{h,cpp}`, `NW_Core/src/{NW_Core.h,NW_Sensor.h,NW_Pages.h}`,
`NW-Device-Specification/LIBRARY-DESIGN.md` §12 and `README.md` (Margay and Okapi appendices),
`NW-Tests/results.md` and the 18 test sketches, and the pre-extraction sources under
`NorthernWidget-libraries/`.

Provenance: the review was produced by a subagent. Every finding marked **verified** below was
re-read in the source afterwards, at the line given. Judgments of shape are argument, not
measurement.

## 1. Verdict

The extraction generalizes the *mechanism* of logging well and the *board* badly.

The mechanism half — the card layout, the numbered `log`/`sta` pair, the status-file stack
written against `NW_Sensor` and `NW_Pages`, `run()`'s three triggers, the ISR trampolines, the
atomic external-interrupt counter — reads cleanly and would carry a third board unchanged.

The board half did not come out. The base holds ten mutable pin fields carrying Margay's values
as defaults, a `BME bme280` member and an `NW_BME280` dependency the base never touches,
`BatError`/`BatWarning` that only Margay can set but that the base's `ledReport()` acts on, and a
hard-coded `analogRead(A7)`. The six `begin()` pieces are not a seam: they are a checklist the
board is trusted to call in the right order, and each board then re-types the same twenty lines of
report-latching and return value around them.

## 2. Leaks into the base (verified)

| Leak | Where |
|------|-------|
| Ten pin fields defaulting to Margay's pins | `NW_Logger.h:243-252` |
| `BME bme280` member, `#include <NW_BME280.h>`, `depends=NW_BME280` – zero references in the base | `NW_Logger.h:24,285`, `library.properties:10`, `NW_Logger.cpp` (grep count 0) |
| `ledReport()` acts on `BatError`/`BatWarning`, which only `Margay::batTest()` sets | `NW_Logger.cpp:156-173`; Okapi's `BatTest` is commented out at `Okapi.cpp:87` |
| `SDtest()` seeds from `analogRead(A7)` and assumes an active-low card-detect pin | `NW_Logger.cpp:246-247,273` |
| `clockTest()` assumes `I2C_ADR_OB[0]` is a DS3231 and writes `0xFF` to it | `NW_Logger.cpp:319-321` |
| `readIdentity()`'s Schema 0 fallback (`EEPROMLen - 8`) is a Margay convention | `NW_Logger.cpp` |
| Unprefixed globals (`manualLog`, `ExtIntPin`, `ExtIntTripped`, `ExtInt_count`) and colour macros exported from a shared base, against NW_Core's own `NW_` rule | `NW_Logger.h:38-50,75-79`; rule at `NW_Core.h:17` |

## 3. Bugs found (verified, listed separately from design)

1. **`WDHold` collides with `Sw_Bus_Prime` on Okapi.** The base defaults `WDHold = 23`
   (`NW_Logger.h:252`); `Okapi.h:167` is `Sw_Bus_Prime = 23`; Okapi's `// WDHold = 255;` is
   commented out (`Okapi.cpp:23`). `resetWDT()` drives the pin HIGH for 5 µs and leaves it LOW,
   and `run()` calls it at every trigger. This is [Okapi_Library #4](https://github.com/NorthernWidget/Okapi_Library/issues/4),
   pre-existing, now living in shared code behind a Margay default. Not verified on hardware.
2. **`Okapi.h:28` `#define EXTERNAL 1`** collides with MightyCore's `#define EXTERNAL 0` for the
   1284P (`.arduino15/packages/NorthernWidget/hardware/avr/*/cores/MightyCore/Arduino.h:77`).
   Latent: nothing calls `analogReference()` today.
3. **`Okapi.h:30-31` `#define MODEL_1v0` / `#define MODEL_0v0`** are empty object-like macros that
   erase those tokens downstream; `Margay.h:44` uses `MODEL_1v0` as an enumerator.
4. **`keep_ADCSRA` is dead:** declared `NW_Logger.h:331`, written at `Margay.cpp:562` and
   `Okapi.cpp:431`, read nowhere; both wake paths write the literal `ADCSRA = 135` instead.
5. **`externalI2COn` is write-only** and `farmGateI2C` is a pass-through — vestiges of the
   pre-extraction Margay, which read the flag.
6. **Both boards print the BME280 failure before `Serial.begin()`** (Margay 173 against 181, Okapi
   70 against 75), so the diagnostic cannot appear.
7. **`Okapi::readStr()` falls off the end without returning** on the file-open failure path
   (`Okapi.cpp:196-199`; the `else` branch's `return` is commented out).
8. **Page 3 Block 0 disagrees between the two loggers** for the same three quantities: Margay
   `0x60` FileNum, `0x62` LogInterval, `0x66` ExtIntCount (`Margay.cpp:504-506`); Okapi `0x60`
   ExtIntCount, `0x62` FileNum, `0x64` LogInterval (`Okapi.cpp:374-376`). The spec carries the
   disagreement.
9. **`NumADR_OB` is never bounds-checked** against `I2C_ADR_OB`'s capacity of 6.
10. **`Margay.cpp:87,133` write the global `ExtIntPin = 11`** for the old models while models 2 and
    3 set the member `ExtInt`, so an old-model Margay attaches an ISR on pin 11 and takes the
    empty-header branch. Pre-existing; the extraction moved it into shared state.

## 4. Real hardware differences against accidents

Real: `RTCInt`/`LogInt` pins (Margay 2/28, Okapi 2/27); Okapi's six on-board chips against
Margay's one or two; Okapi's ADS1115 pair, MCP4725, MCP23018 and Feather backhaul; Margay's
MCP3421, thermistor and battery divider.

Accidents: `Okapi::i2cState(bool)` against the base's `switchExternalI2C(bool)` — same pin, same
polarity, Okapi's drops the `pinMode`, the `delay(1)` and the bookkeeping; `powerAux(uint8_t)`
against `powerAux(bool)` — one name, incompatible signatures, neither virtual;
`turnOffSDcard`/`turnOnSDcard` duplicated; `sleepNow` duplicated at ~120 lines per board including
a verbatim-copied twenty-line comment about the ATmega8 datasheet, differing only in the rails;
the boot-report latch chain, differing by one line; `attachExtInt()` called at a different point of
each `begin()`; Page 3 Block 0's field order; Okapi's PascalCase locals.

## 5. The power model

Andy, 2026-09-24: alkaline primary cells (as on the Margay), a Li-Ion or other rechargeable, and a
solar panel attached to it. The Margay's model is a subset of the Okapi's, so the rails generalize
as a source selector plus an aux-rail switch: `virtual uint8_t powerSelect()` (Margay returns 0,
always primary; Okapi arbitrates as it does at `Okapi.cpp:303-330`) with
`virtual void railsOff()` / `railsOn()`. `PowerState` moves from an Okapi member to the base.

The conflict is Page 2 Block 1: Margay's `0x4B-0x4C` is thermistor temperature and Okapi's would
be solar input, and Margay's appendix is normative while Okapi's is hypothetical.

## 6. Three shapes

**A. Subtraction only.** Move `bme280`, `BMEError`, `BatError`, `BatWarning` and `keep_ADCSRA`
down to the boards; delete `externalI2COn` and `farmGateI2C`; set Okapi's ten pins explicitly;
prefix the globals and macros; converge `i2cState` onto the base. Touches both libraries'
headers, `NW_Logger/library.properties` (the `NW_BME280` dependency goes), `keywords.txt` if the
colour macros are renamed, any sketch using `RED`/`ON`/`OFF` (grep first), LIBRARY-DESIGN §12's
"As built" paragraph, and a `results.md` re-run. No spec change. Kills bugs 1 and 2.

**B. Board-description record and a template-method `begin()`.** The base constructor takes a
`NW_LoggerPins` record; `NW_Logger::begin(vals, n, header)` becomes non-virtual and runs the
sequence, calling named board hooks (`boardPowerUp`, `boardChipsBegin`, `boardCalibration`,
`boardSelfTests`, `boardChipFaults`); `addDataPoint()` becomes non-virtual with `onBoardVals()` as
the hook, as §12 first proposed. Margay must build its record in a static function called from the
member-initializer list, because base constructors run before derived bodies: that is a mechanical
rewrite of `Margay.cpp:25-155` into a table. **This changes Margay's public surface** – its pin
fields are documented as readable (`Margay.h:210-215`) – and rewrites the mature board's
constructor. RAM-neutral. Makes the `WDHold` class of bug unrepresentable.

**C. B plus convergence.** `railsOff()`/`railsOn()` replace both boards' `sleepNow` and
`turnOff/OnSDcard`; `powerSelect()` generalizes `powerAuto`; Okapi's Page 3 Block 0 takes Margay's
field order; Okapi's `EXTERNAL`/`INTERNAL`/`MODEL_*` macros go. Adds the Okapi appendix (cheap:
hypothetical) and, if the power block is unified too, the normative Margay appendix and Margay's
`fillPages`. Hooks drop from five to about four, ~120 duplicated lines collapse, and a third
board's job becomes: hand over a pin record, name your columns, switch your rails.

## 7. Recommendation, and the case against it

A now; then C's convergences that are free because no Okapi is deployed; B last, because it is the
only one that changes the mature board's public surface.

Against: the loggers have no host harness. Apis has `extras/test/run.sh` with a byte-identical
recorded baseline; the loggers have `NW-Tests/compile.py`, which proves only that they build. A
restructure of `begin()` and `sleepNow()` — the two functions where an ordering mistake costs a
deployment rather than a compile error — would be verified by "it compiles" and then by hardware,
with nothing in between. Build a stub-based logger harness (stub `Arduino.h`, `Wire.h`, `SdFat.h`;
recorded serial transcript and recorded card writes) before B.

Second argument against B: today someone tracing Margay's boot reads `Margay::begin()` top to
bottom. After B they read a base sequence and jump into five board hooks. That is a real loss in
reading, worth paying only because the present shape has already let one board skip a pin and
another reorder `attachExtInt()`.

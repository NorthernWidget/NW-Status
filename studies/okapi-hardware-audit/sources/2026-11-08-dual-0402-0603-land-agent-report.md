STATUS: COMPLETE

# Dual 0402/0603 land research

## Candidates

## Sources checked
- LOCAL nw-cold-silicon.pretty: no dual 0402/0603 footprint. R0402 pads 0.7x0.9 at +-0.65 (gap 0.6, extent 2.0); R0603 pads 1.0x1.0 at +-0.85 (gap 0.7, extent 2.7). Same for C0402/C0603.
- LOCAL Eagle libs (45 .lbr under github/, incl. SparkFun-Eagle-Libraries @5213feb 2021, Adafruit, Cold-Silicon, NorthernWidget-Eagle-Libraries): no package name containing both 0402 and 0603, none "dual"/"combo" for chip passives. Dead end.
- SparkFun-Eagle-Libraries @2354dae (2024-08-23), SparkFun-KiCad-Libraries @ff1d7db (2026-10-29), Adafruit-Eagle-Library @4abf84c (2015): no dual/combo 0402-0603 chip package. Dead end.
- KiCad official kicad-footprints master (GitLab API tree, Resistor_SMD 67 files, Capacitor_SMD 103): no dual footprint. Reference lands (IPC-7351 nominal per descr):
  - R_0402_1005Metric: roundrect 0.54x0.64 at +-0.51 -> inner gap 0.48, outer extent 1.56
  - R_0603_1608Metric: roundrect 0.80x0.95 at +-0.825 -> inner gap 0.85, outer extent 2.45
  - R_0402 HandSolder: 0.715x0.64 at +-0.5975 -> gap 0.48, extent 1.91
  - R_0603 HandSolder: 0.975x0.95 at +-0.9125 -> gap 0.85, extent 2.80
- Web search "dual footprint 0402 0603 combined land" (extended): no combined-land source. Dead ends: US8664541B2 (IBM/Lenovo modified 0402 under BGA, single size); KiCad/kicad-footprints#711 (0805 gap, not dual). Gherkin/netdaq#29 reports 0402 in 0603 land rejected by placement check/tombstone risk (secondary).

### Candidate A: Blues MN_0402_0603 (Notecarrier-XI v1.4)
- Source: github.com/blues/note-hardware Notecarrier-XI/v1.4/KiCad_format/Notecarrier-XI-altium-import.pretty/MN_0402_0603.kicad_mod (last commit d77cf1a 2026-07-31, KiCad 9 port of the Altium design); copy in blues/blues-kicad-lib @6304cae.
- Pads: rect, 0.75 (x) x 0.80 (y) (file: size 0.8 0.75 rotated 90/270), centers +-0.725 -> inner gap 0.70, outer extent 2.20, paste margin -0.025.
- Production evidence: v1.4 BOM (BOM-ActiveBOM, rag-extracted html) puts BOTH sizes on this land: C24 2.2p/C25 1p/C26 0.5p "0402", L3 LQW15AN2N3G80D (0402), L4-L6 LQW18AN (0603), R20-R23 0R0 "0603". RF matching network use.

### Candidate B: TTI L_0402_0603_Compatible_Footprint (Generic Node SE)
- Source: github.com/TheThingsIndustries/generic-node-se Hardware/lib/node-lib.pretty/L_0402_0603_Compatible_Footprint.kicad_mod (befed45, 2020-12-09).
- Pads: roundrect (rratio 0.05) 1.00 x 1.00 at +-0.75 -> inner gap 0.50, outer extent 2.50; solder_paste_margin -0.05 (paste 0.90x0.90).
- Production evidence: NOT placed in Hardware/pcb-stm32wl/pcb-stm32wl.kicad_pcb (rev 1.1b, 2020-10-12) or fab/bom/pcb-stm32wl.html (grep "0402_0603": 0 hits). Library-only.

### Candidate C: natsfr SM0402_0603 (hobby library, overlapping pads)
- Source: github.com/natsfr/kicad-components Pretty_Footprints/General_SMD.pretty/SM0402_0603.kicad_mod (ca513a5, 2023-06-24).
- Pads: two overlapping rects per terminal: 0402 pad 0.50x0.60 at +-0.50 (x 0.25-0.75) + 0603 pad 0.635x1.143 at +-0.762 (x 0.445-1.080). Union: inner gap 0.50, outer extent 2.16, T/stepped shape (0.6 tall inner, 1.143 tall outer).
- Production evidence: none found.

### Candidate D: pscorbett RES_COMBO_0402_0603_0805_1206_THT
- github.com/pscorbett/kicad-library footprints/RES_COMBO_0402_0603_0805_1206_THT.kicad_mod (53ac1ed 2025-08-02). Nested KiCad pads (0402 handsolder 0.715x0.64 at +-0.5975, 0805/1206 pads, THT) -- a prototyping/hand-solder universal pad; not reflow-oriented. No production evidence.

### Candidate E: CalSol R_0603_0402_combo (UC Berkeley solar-car team library)
- Source: github.com/CalSol/calsol-hw-libs layout.pretty/R_0603_0402_combo.kicad_mod (ab84c13, 2018-08-25); descr "Resistor SMD 0603, from DipTrace + hand soldering - DC".
- Pads: overlapping rects: 0603 0.889x1.0 at +-0.85 (x 0.406-1.295) + 0402 0.508x0.711 at +-0.567 (x 0.313-0.821). Union: inner gap 0.626, outer extent 2.59, stepped.
- Hand-solder oriented per descr. Usage not yet checked.

- Dead ends (no dual package): mjbots/moteus hw/controller/controller.lbr @0d4217b; jankae/LibreVNA Hardware/Eagle/VNA.lbr @83e9488; waywardgeek/infnoise eagle/infnoise.lbr @0eef725; WurthElektronik WE-MCI.lbr (match was ferrite part number, not dual land).

## Recommended lands (references)
- Panasonic "Surface Mount Resistors Land Pattern" (industrial.panasonic.com/cdbs/www-data/pdf/RDM0000/DMM0000COL17.pdf), general-purpose ERJ, a = inner gap, b = outer extent, c = pad width (from drawing; pdftotext):
  - 1005 (0402): a 0.5-0.6, b 1.4-1.6, c 0.4-0.6  -> pad length (b-a)/2 = 0.40-0.55
  - 1608 (0603): a 0.7-0.9, b 2.0-2.2, c 0.8-1.0  -> pad length 0.55-0.75
  - NOTE: gap windows do NOT overlap (0402 max 0.6 < 0603 min 0.7); extent windows do not overlap (1.6 < 2.0).
- KiCad IPC-7351 nominal (above): 0402 gap 0.48/extent 1.56/width 0.64; 0603 gap 0.85/extent 2.45/width 0.95.
- Yageo RC body (search snippet, Yageo datasheet copies; official PDF URL returned HTML): RC0402 L 1.00+-0.05, W 0.50+-0.05, I1 0.20+-0.10, I2 0.25+-0.10; RC0603 L 1.60+-0.10, W 0.80+-0.10, I1/I2 0.25+-0.15. UNVERIFIED against yageo.com original.
- Dead end: yageo.com PYu-RC_Group_51_RoHS_L_12.pdf returned an HTML page, not the PDF.
- Suntron "The Low Mass Solution to 0402 Tombstoning", Eric Reno, July 2011 (globalspec.com/Suntron/ref/FinalTombstone0402Whitepaper.pdf): tombstoning driven by thermal/copper-density imbalance between the two pads and by part-to-part dimensional variation; IPC-7351 0402 land "only good for the component selected". Its recommended geometry is in Appendix B (image; dimensions not extracted).
- Secondary only: edaboard (0402 on 0603 land "hand solder only"); Gherkin/netdaq#29; AVX 0402 mirror (pad ext ~0.5 mm beyond part, UNVERIFIED). Dead end: Panasonic/Yageo/Suntron PDFs unreadable by WebFetch, read with pdftotext instead.
- GitHub code search hit rate limit before CalSol usage could be checked.

## Overlap table
Computed by scripts/overlap.py (Yageo Table 1 part dims; output in overlap_table.txt):
land                             gap   ext | pkg  ovl_nom ovl_min   heel   toe   side
A Blues MN_0402_0603           0.700 2.200 | 0402   0.150   0.100 -0.050 0.600  0.150
A Blues MN_0402_0603           0.700 2.200 | 0603   0.250   0.100  0.200 0.300  0.000
B TTI L_0402_0603_Compat       0.500 2.500 | 0402   0.200   0.100  0.050 0.750  0.250
B TTI L_0402_0603_Compat       0.500 2.500 | 0603   0.250   0.100  0.300 0.450  0.100
C natsfr SM0402_0603           0.500 2.159 | 0402   0.200   0.100  0.050 0.579  0.322
C natsfr SM0402_0603           0.500 2.159 | 0603   0.250   0.100  0.300 0.279  0.171
E CalSol R_0603_0402_combo     0.626 2.590 | 0402   0.187   0.100 -0.013 0.795  0.250
E CalSol R_0603_0402_combo     0.626 2.590 | 0603   0.250   0.100  0.237 0.495  0.100
ws nw-cold-silicon R0402       0.600 2.000 | 0402   0.200   0.100  0.000 0.500  0.200
ws nw-cold-silicon R0402       0.600 2.000 | 0603   0.250   0.100  0.250 0.200  0.050
ws nw-cold-silicon R0603       0.700 2.700 | 0402   0.150   0.100 -0.050 0.850  0.250
ws nw-cold-silicon R0603       0.700 2.700 | 0603   0.250   0.100  0.200 0.550  0.100
ref KiCad R_0402 IPC nom       0.480 1.560 | 0402   0.200   0.100  0.060 0.280  0.070
ref KiCad R_0402 IPC nom       0.480 1.560 | 0603   0.250   0.100  0.310 -0.020 -0.080
ref KiCad R_0603 IPC nom       0.850 2.450 | 0402   0.075   0.050 -0.125 0.725  0.225
ref KiCad R_0603 IPC nom       0.850 2.450 | 0603   0.250   0.100  0.125 0.425  0.075
ref Panasonic 0402 (mid)       0.550 1.500 | 0402   0.200   0.100  0.025 0.250  0.000
ref Panasonic 0402 (mid)       0.550 1.500 | 0603   0.250   0.100  0.275 -0.050 -0.150
ref Panasonic 0603 (mid)       0.800 2.100 | 0402   0.100   0.075 -0.100 0.550  0.200
ref Panasonic 0603 (mid)       0.800 2.100 | 0603   0.250   0.100  0.150 0.250  0.050
ovl = bottom-termination length on pad; heel>0: pad runs inward of termination under body; toe = pad beyond part end; side = (pad width - part width)/2

## Recommendation (judgment)
Blues MN_0402_0603 (pads 0.75 x 0.80 at +-0.725; gap 0.70, extent 2.20). Only candidate with production evidence of BOTH sizes reflowed on one land (Notecarrier-XI v1.4 BOM). Measured against Panasonic ERJ: 0603 land window gap 0.7-0.9 / extent 2.0-2.2 / width 0.8-1.0 -> Blues sits inside it on all three (at the corners). For 0402 it is off-window (gap +0.10 over max 0.6, extent +0.6 over max 1.6, width +0.2 over max 0.6): 0402 toe 0.60 mm vs IPC nominal 0.28.

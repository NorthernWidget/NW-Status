#!/bin/sh
# Re-run the whole audit, read-only. usage: run.sh <workspace dir> <scratch dir>
# Writes JSON, text reports, Gerber/drill exports and PNG diffs into the scratch dir; prints the summary lines.
W=${1:-/home/awickert/Dropbox/NorthernWidget/github}; S=${2:-/tmp/eagle-audit}; D=$(cd "$(dirname "$0")" && pwd); mkdir -p $S/fab/okapi $S/fab/margay $S/kicad/okapi $S/kicad/margay $S/render
OK=$W/Project-Okapi/Hardware; MG=$W/Project-Margay/Hardware; LIB=$W/NW-Cold-Silicon/nw-cold-silicon.pretty
OKP=$OK/KiCAD-10import/Okapi.kicad_pcb; MGP=$MG/KiCAD/Margay.kicad_pcb
ODX=116.1261; ODY=-172.5036; MDX=123.4286; MDY=-120.2056   # KiCad minus Eagle, from the element positions (249 and 80 elements agree)
q() { grep -v 'Debug\|assert'; }
python3 $D/inventory.py $OK/Okapi.brd $OKP $LIB $S/okapi.json 'U$4=LOGO1' 2>&1 | q
python3 $D/inventory.py $MG/Margay.brd $MGP $LIB $S/margay.json 'U$2=LOGO1' 2>&1 | q
for b in okapi margay; do
  python3 $D/layers.py $S/$b.json > $S/${b}_layers.txt
  python3 $D/pads.py $S/$b.json > $S/${b}_pads.txt; tail -1 $S/${b}_pads.txt
  python3 $D/instances.py $S/$b.json 2>&1 | q | tail -1
done
python3 $D/geometry.py $OK/Okapi.brd $S/okapi.json $LIB 2>&1 | q > $S/okapi_geom.txt; tail -1 $S/okapi_geom.txt
python3 $D/geometry.py $MG/Margay.brd $S/margay.json $LIB 2>&1 | q > $S/margay_geom.txt; tail -1 $S/margay_geom.txt
unzip -q -o $OK/Okapi_2024-11-02.zip -d $S/fab/okapi; unzip -q -o $W/Project-Margay/Production/Margay_3v0_2023-08-01.zip -d $S/fab/margay
L=F.Mask,B.Mask,F.Paste,B.Paste,F.Cu,B.Cu,Edge.Cuts
kicad-cli pcb export gerbers -o $S/kicad/okapi/ -l $L $OKP >/dev/null 2>&1; kicad-cli pcb export drill -o $S/kicad/okapi/ $OKP >/dev/null 2>&1
kicad-cli pcb export gerbers -o $S/kicad/margay/ -l $L $MGP >/dev/null 2>&1; kicad-cli pcb export drill -o $S/kicad/margay/ $MGP >/dev/null 2>&1
for s in top bottom; do
  python3 $D/gerber_vias.py eagle $OK/Okapi.brd $S/fab/okapi/CAMOutputs/GerberFiles/soldermask_$s.gbr
  python3 $D/gerber_vias.py eagle $MG/Margay.brd $S/fab/margay/CAMOutputs/GerberFiles/soldermask_$s.gbr
done
for m in F_Mask.gts B_Mask.gbs; do python3 $D/gerber_vias.py kicad $OKP $S/kicad/okapi/Okapi-$m 2>&1 | q; python3 $D/gerber_vias.py kicad $MGP $S/kicad/margay/Margay-$m 2>&1 | q; done
for pair in copper_top:F_Cu.gtl copper_bottom:B_Cu.gbl soldermask_top:F_Mask.gts soldermask_bottom:B_Mask.gbs solderpaste_top:F_Paste.gtp solderpaste_bottom:B_Paste.gbp; do
  python3 $D/render_diff.py $OK/Okapi.brd $S/fab/okapi/CAMOutputs/GerberFiles/${pair%%:*}.gbr $S/kicad/okapi/Okapi-${pair#*:} $ODX $ODY $S/render/okapi_${pair%%:*} 1000 200 --skip-vias
  python3 $D/render_diff.py $MG/Margay.brd $S/fab/margay/CAMOutputs/GerberFiles/${pair%%:*}.gbr $S/kicad/margay/Margay-${pair#*:} $MDX $MDY $S/render/margay_${pair%%:*} 1000 200 --skip-vias
done
python3 $D/drills.py $S/fab/okapi/CAMOutputs/DrillFiles/drill_1_16.xln $S/kicad/okapi/Okapi.drl $ODX $ODY
python3 $D/drills.py $S/fab/margay/CAMOutputs/DrillFiles/drill_1_16.xln $S/kicad/margay/Margay.drl $MDX $MDY
python3 $D/board_items.py $OK/Okapi.brd $OKP $ODX $ODY 2>&1 | q
python3 $D/board_items.py $MG/Margay.brd $MGP $MDX $MDY 2>&1 | q
python3 $D/islands.py $OKP $S 2>&1 | q

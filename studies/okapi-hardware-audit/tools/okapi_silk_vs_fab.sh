#!/bin/bash
# silk.sh <board> <outdir>: Eagle-only and KiCad-only silkscreen ink against the 2024 fab, top and bottom
B=$1; O=$2; mkdir -p $O; G=/home/awickert/Dropbox/NorthernWidget/github/Project-Okapi/Hardware/Okapi_2024-11-02/CAMOutputs/GerberFiles
kicad-cli pcb export gerbers --no-x2 -l F.SilkS,B.SilkS -o $O/ $B >/dev/null
W=2.6378; H=5.3937
r(){ gerbv -x png -D 600 -a -B 0 --window_inch=${W}x${H} --origin=$2 -f '#000000FF' -b '#FFFFFF' -o $3 $1 ; }
EO=$(python3 -c "print('%fx%f'%(-1/25.4,-1/25.4))"); KO=$(python3 -c "print('%fx%f'%(115.1261/25.4,-173.5036/25.4))")
r $G/silkscreen_top.gbr $EO $O/e_top.png; r $O/*-F_Silkscreen.gto $KO $O/k_top.png
r $G/silkscreen_bottom.gbr $EO $O/e_bot.png; r $O/*-B_Silkscreen.gbo $KO $O/k_bot.png
python3 - $O <<'P'
import sys,numpy as np
from PIL import Image
from scipy import ndimage
O=sys.argv[1]; px=25.4/600; tol=int(round(0.15/px))
st=ndimage.generate_binary_structure(2,1)
for s in ('top','bot'):
    e=np.array(Image.open(f'{O}/e_{s}.png').convert('L'))<128; k=np.array(Image.open(f'{O}/k_{s}.png').convert('L'))<128
    ed=ndimage.binary_dilation(e,st,tol); kd=ndimage.binary_dilation(k,st,tol)
    eo=e&~kd; ko=k&~ed
    np.save(f'{O}/eo_{s}.npy',eo); np.save(f'{O}/ko_{s}.npy',ko)
    a=lambda m:m.sum()*px*px
    print(s,'eagle ink %.2f kicad ink %.2f eagle-only %.2f kicad-only %.2f mm2'%(a(e),a(k),a(eo),a(ko)))
P

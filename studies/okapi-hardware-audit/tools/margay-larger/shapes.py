# Outline shapes meeting a required usable top area.
# usable(W,H) = (W-0.8)(H-0.8) - CORNER - HOLES, calibrated on today's board:
#   inset outline 1458.9 mm2 vs (50.145-0.8)(30.404-0.8)=1460.8 -> CORNER 1.9 mm2 (three r=2 mm corners);
#   HOLES = 1458.9-1423.6 = 35.3 mm2 (two 5.56 mm keepouts at today's corner offsets, partly outside the inset).
W0,H0=50.145,30.404
CORNER=(W0-0.8)*(H0-0.8)-1458.9; HOLES=1458.9-1423.6
u=lambda W,H:(W-0.8)*(H-0.8)-CORNER-HOLES
print('check today: usable %.1f (measured 1423.6); CORNER %.2f HOLES %.1f'%(u(W0,H0),CORNER,HOLES))
targets={'A, today density, pads proxy':1598,'A, today density, body proxy':1564,'A, 90%, pads':1776,'A, 90%, body':1738,'A, 80%, pads':1998,'A, 80%, body':1955}
for name,T in targets.items():
    H_same_W=(T+CORNER+HOLES)/(W0-0.8)+0.8
    W_same_H=(T+CORNER+HOLES)/(H0-0.8)+0.8
    k=((T+CORNER+HOLES)/((W0-0.8)*(H0-0.8)))**0.5   # both grown by the same factor on the inset rectangle
    print('%-30s usable %5d: same length -> %.1f x %.1f | same height -> %.1f x %.1f | both x%.3f -> %.1f x %.1f'%(name,T,W0,H_same_W,W_same_H,H0,k,(W0-0.8)*k+0.8,(H0-0.8)*k+0.8))
for W,H in ((50.1,34),(50.1,36),(50.1,38),(55,34),(55,35),(56,36),(60,30.4),(60,35)):
    print('candidate %.1f x %.1f: outline %.0f mm2, usable %.0f mm2 (x%.3f today)'%(W,H,W*H,u(W,H),u(W,H)/1423.6))

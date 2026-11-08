"""Minimum set of resistor values for Okapi (v0.8.0 plan) and Margay (KiCad v3.1).
Each constraint: kind, refs, range or equation, source ('D' datasheet, 'P' proposal).
Solver: pulp/CBC; minimize distinct standard values (E24 preferred over E96)."""
import pulp, math, itertools, json, sys
E24=[1.0,1.1,1.2,1.3,1.5,1.6,1.8,2.0,2.2,2.4,2.7,3.0,3.3,3.6,3.9,4.3,4.7,5.1,5.6,6.2,6.8,7.5,8.2,9.1]
E96=[1.00,1.02,1.05,1.07,1.10,1.13,1.15,1.18,1.21,1.24,1.27,1.30,1.33,1.37,1.40,1.43,1.47,1.50,1.54,1.58,1.62,1.65,1.69,1.74,1.78,1.82,1.87,1.91,1.96,2.00,2.05,2.10,2.15,2.21,2.26,2.32,2.37,2.43,2.49,2.55,2.61,2.67,2.74,2.80,2.87,2.94,3.01,3.09,3.16,3.24,3.32,3.40,3.48,3.57,3.65,3.74,3.83,3.92,4.02,4.12,4.22,4.32,4.42,4.53,4.64,4.75,4.87,4.99,5.11,5.23,5.36,5.49,5.62,5.76,5.90,6.04,6.19,6.34,6.49,6.65,6.81,6.98,7.15,7.32,7.50,7.68,7.87,8.06,8.25,8.45,8.66,8.87,9.09,9.31,9.53,9.76]
vals={}
for d in range(0,7):
    for m in E24: vals[round(m*10**d,6)]='E24'
    for m in E96: vals.setdefault(round(m*10**d,6),'E96')
V=sorted(v for v in vals if 1<=v<=2.2e6)
def rng(lo,hi): return [v for v in V if lo-1e-9<=v<=hi+1e-9]
# ---- constraints ----
SINGLE=[ # (refs, lo, hi, src, note)
 ('Okapi R26-R29 ILIM default',209,256,'D+P','MIC2544 230 V/R, 0.9-1.1 A (P); R range 154-2290 (D)'),
 ('Okapi R9 BQ2980 RVDD',100,300,'D+P','max 300 (D), min 100 (P)'),
 ('Okapi R11 BQ2980 RBAT',10,47,'P','typ 20 (D); larger hurts OV/UV accuracy (D)'),
 ('Okapi R15 BQ2980 RPACK',1000,2000,'D+P','max 2k (D)'),
 ('Okapi R14 BQ2980 RCTR',47,220,'P','typ 100 (D), optional ESD'),
 ('Okapi R12 CTR pull-down',1000,100e3,'P',''),
 ('USB series R34/R35 Okapi, R3/R4 Margay',22,33,'P','FTDI reference 27'),
 ('UART series R38/R40 Okapi, R7/R9 Margay',100,1000,'P',''),
 ('Status RGB LEDs D4/D5 Okapi, D2/D3 Margay (12)',220,680,'P','brightness'),
 ('Okapi LED grid D10-D17 (8)',150,470,'P','brightness'),
 ('Okapi B-SoM RGB LED R81-R83',3000,10e3,'P','dim indicator'),
 ('USB-C CC Rd R84/R85 Okapi, R31/R32 Margay',4590,5610,'P','5.1 k, +/-10 % (P; USB-C band to verify)'),
 ('Logic pull-ups/downs, 3.3 V (Okapi R18,R19,R24,R25,R41,R45,R46,R47,R57,R61,R86,R87,R54; Margay R1,R14,R19,R20,R21)',10e3,100e3,'P',''),
 ('Reset pull-up Okapi R52, Margay R2',4700,10e3,'D+P','AN2519 shows 10 k'),
 ('I2C pull-ups Margay R15/R16',2200,10e3,'P','bus speed and capacitance'),
 ('Weak pull-ups R55,R56 (LT3652 CHRG/FAULT), R59 (LDO PG)',100e3,1e6,'D+P','Q8 gate leakage 150 nA (D)'),
 ('Pull-ups 5V_AUX into 3.3 V expander R1,R8,R58; series R68',100e3,1e6,'P','limit clamp current'),
 ('Bleeds R23,R63,R65,R66 Okapi',10e3,1e6,'P',''),
 ('5V_AUX bleed R67 Okapi',10e3,100e3,'P','purpose to confirm'),
 ('LTC4412 STAT pull-up R21',470e3,2.2e6,'D+P','10 uA sink must pull V_BETA low: R >= 420 k'),
 ('Timer DELAY: TPL5111 R20, TPL5010 (#35), Margay R10',120e3,150e3,'P','66 min nominal; ~55-90 min (TPL5111 table, to verify)'),
 ('Margay R17/R18 comparator 1:1 divider (equal pair)',1000,100e3,'P','ratio exactly 1 by equal values'),
]
FIXED={ # positions held to one value, outside the standard set
 'R48 reference bias 1 k (Andy, user-swappable)':1000,
}
DIVIDERS=[ # (name, ratio t/b lo, hi, top range, bottom range, src)
 ('TLV61220 5V_LP R4/R5: 0.5(1+t/b)=5.0 V +/-2 %',8.8,9.2,(100e3,4.7e6),(50e3,500e3),'D(0.5 V, b<500k)+P(+/-2 %)'),
 ('TPS62822 3V3_AUX R6/R7: 0.6(1+t/b)=3.3 V +/-3 %',4.33,4.67,(200e3,1e6),(60e3,180e3),'D(0.6 V)+P'),
 ('TPS61032 LBI R2/R3: 0.5(1+t/b) in 2.6-3.0 V',4.2,5.0,(100e3,4.7e6),(100e3,1e6),'D(0.5 V)+P'),
 ('LT3652 VIN_REG R22/R69: 2.7(1+t/b) in 6.3-6.8 V',1.333,1.519,(10e3,1e6),(10e3,1e6),'D(2.7 V)+P'),
 ('LT3652 SHDN R71/R70: 1.2(1+t/b) in 6.8-7.5 V',4.667,5.25,(100e3,4.7e6),(20e3,1e6),'D(1.2 V)+P'),
]
FLOAT=('LT3652 float R16/R17: 3.3(1+t/b) in 4.178-4.200 V; R13 + t||b in 225-275 k',0.2660,0.2727,(30e3,300e3),(100e3,1e6),(225e3,275e3),'D(3.3 V)+P(window); 250 k bias-compensation target inferred from the fitted values')
ILIM2=('ILIM jumper R30-R33 with R26: R26||R30 in 154-160',154,160)
prob=pulp.LpProblem('rset',pulp.LpMinimize)
y={v:pulp.LpVariable(f'y_{i}',cat='Binary') for i,v in enumerate(V)}
prob+=pulp.lpSum(y[v]*(1.0 if vals[v]=='E24' else 1.001) for v in V)
for name,lo,hi,src,note in SINGLE:
    prob+=pulp.lpSum(y[v] for v in rng(lo,hi))>=1, name[:40]
pairs={}
def pairvars(tag,cands):
    ps=[]
    for (t,b) in cands:
        p=pulp.LpVariable(f'p_{tag}_{len(ps)}',cat='Binary'); prob.addConstraint(p<=y[t]); prob.addConstraint(p<=y[b]); ps.append((p,t,b))
    prob.addConstraint(pulp.lpSum(p for p,_,_ in ps)>=1); return ps
for i,(name,rlo,rhi,tr,br,src) in enumerate(DIVIDERS):
    c=[(t,b) for t in rng(*tr) for b in rng(*br) if rlo<=t/b<=rhi]
    pairs[name]=pairvars(f'd{i}',c)
name,rlo,rhi,tr,br,sr,src=FLOAT
c=[(t,b) for t in rng(*tr) for b in rng(*br) if rlo<=t/b<=rhi]
ps=pairvars('fl',c); pairs[name]=ps
for p,t,b in ps:
    par=t*b/(t+b); prob.addConstraint(p<=pulp.lpSum(y[s] for s in rng(sr[0]-par,sr[1]-par)))
c=[(a,b) for a in rng(209,256) for b in rng(154,10e3) if 154<=a*b/(a+b)<=160]
pairs['ILIM jumper']=pairvars('il',c)
prob.solve(pulp.PULP_CBC_CMD(msg=0,timeLimit=600))
print('status',pulp.LpStatus[prob.status])
S=sorted(v for v in V if y[v].value()>0.5)
def fmt(v): return ('%gM'%(v/1e6) if v>=1e6 else '%gk'%(v/1e3) if v>=1e3 else '%g'%v)
print('chosen set (%d):'%len(S),', '.join(fmt(v)+('' if vals[v]=='E24' else '*') for v in S))
print('assignments:')
for name,lo,hi,src,note in SINGLE:
    opts=[v for v in S if lo<=v<=hi]; print('  %-70s -> %s'%(name[:70],'/'.join(fmt(v) for v in opts)))
for name,ps in pairs.items():
    ok=[(t,b) for p,t,b in ps if y[t].value()>0.5 and y[b].value()>0.5]
    print('  %-70s -> %s'%(name[:70],'; '.join(f'{fmt(t)}/{fmt(b)}' for t,b in ok[:4])))
json.dump([fmt(v) for v in S],open('chosen.json','w'))

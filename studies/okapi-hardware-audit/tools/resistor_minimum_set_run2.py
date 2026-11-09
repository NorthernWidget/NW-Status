"""Run 2: minimum set of resistor values for Okapi (v0.8.0 plan) and Margay (KiCad v3.1),
modeled per position so that churn (positions whose value changes) can be counted.
Holds the couplings run 1 broke: USB-C Rd at 5.1 k, TPS62822 R7 at 180 k (C6 feed-forward),
the TPL5111/TPL5010 timer at 130 k (66 min by TPL5010 Equation 1, set 5), MPPT 6.4-6.7 V.
Objective: for each cap N on the count of distinct values, the fewest changed positions.
Current values are from the KiCad netlists (kicad-cli sch export netlist), 2026-11-09."""
import pulp, json, sys
E24=[1.0,1.1,1.2,1.3,1.5,1.6,1.8,2.0,2.2,2.4,2.7,3.0,3.3,3.6,3.9,4.3,4.7,5.1,5.6,6.2,6.8,7.5,8.2,9.1]
E96=[1.00,1.02,1.05,1.07,1.10,1.13,1.15,1.18,1.21,1.24,1.27,1.30,1.33,1.37,1.40,1.43,1.47,1.50,1.54,1.58,1.62,1.65,1.69,1.74,1.78,1.82,1.87,1.91,1.96,2.00,2.05,2.10,2.15,2.21,2.26,2.32,2.37,2.43,2.49,2.55,2.61,2.67,2.74,2.80,2.87,2.94,3.01,3.09,3.16,3.24,3.32,3.40,3.48,3.57,3.65,3.74,3.83,3.92,4.02,4.12,4.22,4.32,4.42,4.53,4.64,4.75,4.87,4.99,5.11,5.23,5.36,5.49,5.62,5.76,5.90,6.04,6.19,6.34,6.49,6.65,6.81,6.98,7.15,7.32,7.50,7.68,7.87,8.06,8.25,8.45,8.66,8.87,9.09,9.31,9.53,9.76]
vals={}
for d in range(0,7):
    for m in E24: vals[round(m*10**d,6)]='E24'
    for m in E96: vals.setdefault(round(m*10**d,6),'E96')
V=sorted(v for v in vals if 1<=v<=2.2e6)
def rng(lo,hi): return [v for v in V if lo*(1-1e-9)<=v<=hi*(1+1e-9)]
k=1e3; M=1e6
# ---- positions: (group, lo, hi, src, [(board, ref, current)]) ----
O='Okapi'; G='Margay'
LED=(100,10*k) if 'ledwide' in sys.argv else None  # run 3: LED brightness free (Andy), 100 R-10 k (P)
R5='run5' in sys.argv  # run 5: run 4 plus the v0.8.0 charger dividers of Project-Okapi #46
R4='run4' in sys.argv or R5  # run 4: Andy 2026-11-09: R21 1M, R13 180k; R15 held; MPPT/SHDN held pending the panel survey; LEDs no dimmer than now (P)
SINGLE=[
 ('BQ2980 RVDD',100,300,'D+P',[(O,'R9',220)]),
 ('BQ2980 RBAT',10,47,'P',[(O,'R11',27)]),
 ('BQ2980 RPACK',*((2000,2000) if R4 else (1000,2000)),'D+P',[(O,'R15',2*k)]),
 ('BQ2980 RCTR',47,220,'P',[(O,'R14',100)]),
 ('CTR pull-down',1000,100*k,'P',[(O,'R12',1*k)]),
 ('USB series',22,33,'P',[(O,'R34',27),(O,'R35',27),(G,'R3',27),(G,'R4',27)]),
 ('UART series',100,1000,'P',[(O,'R38',330),(O,'R40',330),(G,'R7',330),(G,'R9',330)]),
 ('Status RGB LEDs',*(LED or ((100,330) if R4 else (220,680))),'P',[(O,r,330) for r in ('R36','R37','R39','R42','R43','R44')]+[(G,r,330) for r in ('R5','R6','R8','R11','R12','R13')]),
 ('LED grid D10-D17',*(LED or ((100,220) if R4 else (150,470))),'P',[(O,r,220) for r in ('R53','R60','R64','R76','R77','R78','R79','R80')]),
 ('B-SoM RGB LED',*(LED or ((100,5.1*k) if R4 else (3*k,10*k))),'P',[(O,r,5.1*k) for r in ('R81','R82','R83')]),
 ('USB-C CC Rd (held 5.1 k)',5.1*k,5.1*k,'P',[(O,'R84',5.1*k),(O,'R85',5.1*k),(G,'R31',5.1*k),(G,'R32',5.1*k)]),
 ('Logic pull-ups/downs 3.3 V',10*k,100*k,'P',[(O,r,10*k) for r in ('R24','R25','R41','R45','R46','R47','R86','R87','R54')]+[(O,r,100*k) for r in ('R18','R19','R57','R61')]+[(G,r,10*k) for r in ('R1','R14','R19','R20','R21')]),
 ('Reset pull-up',4.7*k,10*k,'D+P',[(O,'R52',10*k),(G,'R2',10*k)]),
 ('I2C pull-ups',2.2*k,10*k,'P',[(G,'R15',10*k),(G,'R16',10*k)]),
 ('Weak pull-ups CHRG/FAULT/PG',100*k,1*M,'D+P',[(O,'R55',1*M),(O,'R56',1*M),(O,'R59',1*M)]),
 ('5V_AUX pull-ups into expander; series',100*k,1*M,'P',[(O,'R1',180*k),(O,'R8',180*k),(O,'R58',100*k),(O,'R68',1*M)]),
 ('Bleeds',10*k,1*M,'P',[(O,'R23',100*k),(O,'R63',100*k),(O,'R65',180*k),(O,'R66',180*k)]),
 ('5V_AUX bleed R67',10*k,100*k,'P',[(O,'R67',10*k)]),
 ('LTC4412 STAT pull-up',*((1*M,1*M) if R4 else (470*k,2.2*M)),'D+P',[(O,'R21',470*k)]),
 ('R48 reference bias (held 1 k, Andy)',1*k,1*k,'Andy',[(O,'R48',1*k)]),
 ('Timer DELAY (held 130 k, 66 min)',130*k,130*k,'D+Andy',[(O,'R20',130*k),(G,'R10',130*k)]),
]
EQUAL=[('Margay comparator 1:1 pair',1*k,100*k,'P',[(G,'R17',10*k),(G,'R18',10*k)])]
DIVIDERS=[ # (name, t/b lo, hi, top range, bottom range, src, top pos, bottom pos)
 ('TLV61220 5V_LP: 0.5(1+t/b)=5.0 V +/-2 %',8.8,9.2,(100*k,4.7*M),(50*k,500*k),'D+P',[(O,'R4',1.62*M)],[(O,'R5',180*k)]),
 ('TPS62822 3V3_AUX: 0.6(1+t/b)=3.3 V +/-3 %, R7 held 180 k',4.33,4.67,(200*k,1*M),(180*k,180*k),'D+P',[(O,'R6',820*k)],[(O,'R7',180*k)]),
 ('TPS61032 LBI: 0.5(1+t/b) in 2.6-3.0 V',4.2,5.0,(100*k,4.7*M),(100*k,1*M),'D+P',[(O,'R2',1.62*M)],[(O,'R3',330*k)]),
 ('LT3652 VIN_REG (MPPT): 2.7(1+t/b) in 6.4-6.7 V (run 5: 16.2 V, #46)',*((5,5) if R5 else (6.4/2.7-1,6.7/2.7-1)),*(((1*M,1*M),(200*k,200*k)) if R5 else ((143*k,143*k),(100*k,100*k)) if R4 else ((10*k,1*M),(10*k,1*M))),'D+P',[(O,'R22',143*k)],[(O,'R69',100*k)]),
 ('LT3652 SHDN: 1.2(1+t/b) in 6.8-7.5 V (run 5: 13.2 V, #46)',*((10,10) if R5 else (4.667,5.25)),*(((1*M,1*M),(100*k,100*k)) if R5 else ((1*M,1*M),(200*k,200*k)) if R4 else ((100*k,4.7*M),(20*k,1*M))),'D+P',[(O,'R71',1*M)],[(O,'R70',200*k)]),
 ('ILIM: 230/R26 in 0.9-1.1 A; R26||R30 in 154-160',None,None,(209,256),(154,10*k),'D+P',[(O,r,232) for r in ('R26','R27','R28','R29')],[(O,r,464) for r in ('R30','R31','R32','R33')]),
]
FW=float(sys.argv[2]) if len(sys.argv)>2 and sys.argv[2] not in ('ledwide','run4','run5') else 4.200
FLOAT=('LT3652 float: 3.3(1+t/b) in 4.178-%.3f V; R13 + t||b in 225-275 k'%FW,4.178/3.3-1,FW/3.3-1,(30*k,300*k),(100*k,1*M),(225*k,275*k),[(O,'R16',91*k)],[(O,'R17',330*k)],[(O,'R13',182*k)])

def solve(Nmax=None, churn=True):
    prob=pulp.LpProblem('rset2',pulp.LpMinimize)
    y={v:pulp.LpVariable(f'y_{i}',cat='Binary') for i,v in enumerate(V)}
    terms=[]; picks=[]
    def choose(tag,cands,positions):
        xs={v:pulp.LpVariable(f'x_{tag}_{i}',cat='Binary') for i,v in enumerate(cands)}
        prob.addConstraint(pulp.lpSum(xs.values())==1)
        for v,x in xs.items():
            prob.addConstraint(x<=y[v])
            terms.append(x*sum(1 for _,_,cur in positions if abs(cur-v)>1e-6))
        picks.append((tag,positions,xs)); return xs
    n=0
    for name,lo,hi,src,pos in SINGLE:
        for p in pos: choose(f's{n}',rng(lo,hi),[p]); n+=1
    for name,lo,hi,src,pos in EQUAL: choose(f'e{n}',rng(lo,hi),pos); n+=1
    def pairs(tag,cands,tpos,bpos):
        ps={}
        for i,(t,b) in enumerate(cands):
            p=pulp.LpVariable(f'p_{tag}_{i}',cat='Binary'); prob.addConstraint(p<=y[t]); prob.addConstraint(p<=y[b]); ps[(t,b)]=p
            terms.append(p*(sum(1 for _,_,c in tpos if abs(c-t)>1e-6)+sum(1 for _,_,c in bpos if abs(c-b)>1e-6)))
        prob.addConstraint(pulp.lpSum(ps.values())==1); picks.append((tag,tpos+bpos,ps)); return ps
    for i,(name,rlo,rhi,tr,br,src,tp,bp) in enumerate(DIVIDERS):
        if rlo is None: c=[(a,b) for a in rng(*tr) for b in rng(*br) if 0.9<=230/a<=1.1 and 154<=a*b/(a+b)<=160]
        else: c=[(t,b) for t in rng(*tr) for b in rng(*br) if rlo<=t/b<=rhi]
        pairs(f'd{i}',c,tp,bp)
    name,rlo,rhi,tr,br,sr,tp,bp,cp=FLOAT
    ps=pairs('fl',[(t,b) for t in rng(*tr) for b in rng(*br) if rlo<=t/b<=rhi],tp,bp)
    xs=choose('r13',[180*k] if R4 else rng(sr[0]-300*k,sr[1]),cp)
    for (t,b),p in ps.items():
        par=t*b/(t+b); ok=set(rng(sr[0]-par,sr[1]-par))
        prob.addConstraint(p+pulp.lpSum(x for v,x in xs.items() if v not in ok)<=1)
    count=pulp.lpSum(y.values())
    if Nmax is not None: prob.addConstraint(count<=Nmax)
    e96=pulp.lpSum(y[v] for v in V if vals[v]=='E96')
    prob+=(pulp.lpSum(terms)+0.001*e96) if churn else (count+0.001*e96)
    prob.solve(pulp.PULP_CBC_CMD(msg=0,timeLimit=900))
    S=sorted(v for v in V if y[v].value()>0.5)
    asg={}
    for tag,pos,xs in picks:
        for key,x in xs.items():
            if x.value()>0.5:
                asg[tag]=key
    return pulp.LpStatus[prob.status],S,picks,asg,(pulp.value(pulp.lpSum(terms)) if terms else 0)

def fmt(v): return ('%gM'%(v/1e6) if v>=1e6 else '%gk'%(v/1e3) if v>=1e3 else '%g'%v)
def report(st,S,picks,asg,ch):
    print('status',st,'| values %d:'%len(S),', '.join(fmt(v)+('' if vals[v]=='E24' else '*') for v in S),'| changed positions %d'%round(ch))
    changes=[]
    for tag,pos,xs in picks:
        key=asg[tag]
        if isinstance(key,tuple):
            t,b=key; n=len(pos)//2  # divider positions: top half, then bottom half
            new=[t]*n+[b]*n
        else: new=[key]*len(pos)
        for (bd,ref,cur),v in zip(pos,new):
            if abs(cur-v)>1e-6: changes.append(f'{bd} {ref} {fmt(cur)}->{fmt(v)}')
    print('  changes:',', '.join(changes) if changes else 'none')

if __name__=='__main__':
    mode=sys.argv[1] if len(sys.argv)>1 else 'min'
    if mode=='min':
        report(*solve(churn=False))
    else:
        for N in [int(x) for x in mode.split(',')]:
            report(*solve(Nmax=N))

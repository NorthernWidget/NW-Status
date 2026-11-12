# Required top area for the larger Margay: (today's top parts - removed + added) / density.
import json
lib=json.load(open('libareas.json')); P=json.load(open('parts_v4.json')); R=json.load(open('removed_v4.json'))
for proxy in ('pads','body'):
    D=json.load(open('density_%s.json'%proxy)); rows={r[0]:r[2] for r in D['rows']}
    rem=sum(rows[r[1]] for r in R)
    add_base=sum(lib[p[3]]['area'] for p in P if p[4]=='base')
    add_opt=sum(lib[p[3]]['area'] for p in P if p[4]=='option')
    elig_base=sum(lib[p[3]]['area'] for p in P if p[4]=='base' and p[5].startswith('yes'))
    S0=D['sum']; d0=D['density']; A0=D['usable']
    print('== PROXY=%s: today top sum %.1f mm2, usable %.1f mm2, density %.3f'%(proxy,S0,A0,d0))
    print('   removed %.1f mm2 (%s)'%(rem,', '.join('%s %.2f'%(r[1],rows[r[1]]) for r in R)))
    print('   added base %.1f mm2 (%d parts), options %.1f mm2 (%d parts); bottom-eligible within base %.1f mm2'%(add_base,sum(p[4]=='base' for p in P),add_opt,sum(p[4]=='option' for p in P),elig_base))
    for case,S in (('A all new on top, base',S0-rem+add_base),('B all new on top, base+options',S0-rem+add_base+add_opt),('C base, eligible parts on bottom',S0-rem+add_base-elig_base)):
        out=[]
        for f in (1.0,0.9,0.8):
            d=d0*f; out.append('d=%.3f (%.0f%% of today): usable %.0f mm2 (x%.3f)'%(d,f*100,S/d,S/d/A0))
        print('   %-36s S=%.1f | %s'%(case,S,' | '.join(out)))
for p in P: print('%-9s %-9s %-16s %7.3f %-36s %-6s %s | %s'%(p[0],p[1],p[3],lib[p[3]]['area'],lib[p[3]]['src'],p[4],p[5],p[2]))

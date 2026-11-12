# Build a scratch board with a placement plan, for KiCad's DRC: python3 build.py placed_X.json out.kicad_pcb
import pcbnew, json, sys
LIB='/home/awickert/Dropbox/NorthernWidget/github/nw-cold-silicon/nw-cold-silicon.pretty'
plan=json.load(open(sys.argv[1])); out=sys.argv[2]
b=pcbnew.LoadBoard('Okapi.kicad_pcb')
io=pcbnew.PCB_IO_KICAD_SEXPR()
for issue,ref,fp,side,rot,x,y,d,why in plan:
    if side is None: continue
    f=io.FootprintLoad(LIB,fp); f.SetReference(ref); f.SetValue(issue)
    f.SetFPID(pcbnew.LIB_ID('nw-cold-silicon',fp)); b.Add(f)
    f.SetOrientationDegrees(rot)
    f.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(x),pcbnew.FromMM(y)))
b.Save(out)

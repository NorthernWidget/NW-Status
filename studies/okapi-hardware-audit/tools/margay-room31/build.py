import pcbnew, json, sys
LIB='/home/awickert/Dropbox/NorthernWidget/github/nw-cold-silicon/nw-cold-silicon.pretty'
plan=json.load(open(sys.argv[1])); out=sys.argv[2]
b=pcbnew.LoadBoard('KiCAD/Margay.kicad_pcb')
b.RemoveNative(b.FindFootprintByReference('C20'))
io=pcbnew.PCB_IO_KICAD_SEXPR()
for issue,ref,fp,side,rot,x,y,d,why in plan:
    if side is None: continue
    f=io.FootprintLoad(LIB,fp); f.SetReference(ref); f.SetValue(issue)
    f.SetFPID(pcbnew.LIB_ID('nw-cold-silicon',fp)); b.Add(f)
    f.SetOrientationDegrees(rot)
    if side=='B': f.SetLayerAndFlip(pcbnew.B_Cu)
    f.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(x),pcbnew.FromMM(y)))
b.Save(out)

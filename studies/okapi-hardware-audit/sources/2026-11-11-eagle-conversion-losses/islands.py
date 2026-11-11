"""The Okapi bottom GND zone that Eagle drew with orphans="yes": its fill as committed, and refilled with islands kept.
Works on a copy in the scratch dir. usage: python3 islands.py <Okapi.kicad_pcb> <scratch dir>"""
import sys,shutil,os,pcbnew
src,S=sys.argv[1:3]; dst=os.path.join(S,'okapi_islands.kicad_pcb'); shutil.copy(src,dst)
pro=src[:-len('.kicad_pcb')]+'.kicad_pro'
if os.path.exists(pro): shutil.copy(pro,dst[:-len('.kicad_pcb')]+'.kicad_pro')
b=pcbnew.LoadBoard(dst)
def bottom(): return [z for z in b.Zones() if not z.GetIsRuleArea() and 'B.Cu' in [pcbnew.BOARD.GetStandardLayerName(l) for l in z.GetLayerSet().Seq()]]
def report(tag):
    for z in bottom(): print(tag,z.GetNetname(),'island removal mode',z.GetIslandRemovalMode(),'fill outlines',z.GetFilledPolysList(pcbnew.B_Cu).OutlineCount(),'fill area %.2f mm2'%(z.GetFilledPolysList(pcbnew.B_Cu).Area()/1e12))
report('as committed:')
for z in bottom():
    if z.GetMinThickness()<pcbnew.FromMM(0.08): z.SetIslandRemovalMode(pcbnew.ISLAND_REMOVAL_MODE_NEVER)   # the 0.1524 mm Eagle polygon (min width 0.0762)
pcbnew.ZONE_FILLER(b).Fill(b.Zones()); report('refilled, that zone keeping islands:')

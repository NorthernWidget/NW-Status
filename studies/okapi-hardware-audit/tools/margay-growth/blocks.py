"""Functional blocks of today's Margay (the grouping is this study's proposal) and their bounding boxes."""
import json
F = {d['ref']: d for d in json.load(open('fps.json'))}
BLOCKS = {
 'J2 (10-pos terminal)': ['J2'],
 'MCU (U1, crystal, buttons, LEDs, SD buffer U5, battery divider)': ['U1','C4','XTAL1','C2','C3','S1','S2','R14','R22','R23','U5','D3','R11','R12','R13'],
 'USB/FT231X (J4, U2, Q2/Q3, VBUS caps)': ['J4','U2','R3','R4','R7','R8','R9','C1','C7','C8','C9','D1','D2','R5','R6','R31','R32','C5','C6','Q2','Q3','R19','R21','U10'],
 'Power (U6, U7, U8, U9, Q1, U11, caps)': ['U6','U7','U8','U9','R17','R18','C10','C11','C12','C13','C14','C15','R20','Q1','U11','JP2'],
 'Clock (RTC1, BT1, C19, C20, D4)': ['RTC1','BT1','C19','C20','D4'],
 'ADC/reference (U14, U13)': ['U14','U13','C16','C17','C18','R24','JP3'],
 'I2C switch (U4, R15, R16, JP1)': ['U4','R15','R16','JP1'],
 'BME280 U12': ['U12'],
 'Watchdog/reset (U3, R10, R2)': ['U3','R10','R2'],
 'ISP1': ['ISP1'],
 'SD (J1 bottom, R1)': ['J1','R1'],
 'J3 (6-pos terminal)': ['J3'],
}
if __name__ == '__main__':
    used = set()
    for name, refs in BLOCKS.items():
        bb = [F[r]['bbox'] for r in refs]
        used |= set(refs)
        print(f"{name:66s} x {min(b[0] for b in bb):6.2f}-{max(b[2] for b in bb):6.2f}  y {min(b[1] for b in bb):6.2f}-{max(b[3] for b in bb):6.2f}  ({len(refs)} parts)")
    print('not in a block:', sorted(set(F) - used))

"""Check P2.8 endpoint extension and the actual endpoint marks in chapter2."""
from fractions import Fraction as F
from pathlib import Path
import json
from bspline_math import piece,evaluate

root=Path(__file__).resolve().parents[1]
families=[('2.6','06',2,(0,0,0,1,2,3,4,4,5,5,5)),
          ('2.9','11',3,(0,0,0,0,2,4,6,8,8,8,8)),
          ('2.10','12',3,(0,0,0,0,2,4,4,6,6,6,8,8,8,8)),
          ('2.12','14',3,(0,0,0,0,1,5,6,8,8,8,8))]
report={}
for figure,number,p,knots in families:
    n=len(knots)-p-2
    left=next(s for s in range(len(knots)-1) if knots[s]<knots[s+1])
    right=max(s for s in range(len(knots)-1) if knots[s]<knots[s+1])
    a,b=F(knots[0]),F(knots[-1])
    lv=[evaluate(piece(knots,i,p,left),a) for i in range(n+1)]
    rv=[evaluate(piece(knots,i,p,right),b) for i in range(n+1)]
    assert lv==[1]+[0]*n and rv==[0]*n+[1]
    source=(root/f'image_tex/ch02/fig_2_{number}.tex').read_text(encoding='utf-8-sig')
    marker=rf'\fill (axis cs:{int(b)},1) circle[radius=1.5pt];'
    assert marker in source
    report[figure]={'degree':p,'knots':knots,'last_index':n,
                    'left_endpoint':list(map(int,lv)),'right_endpoint':list(map(int,rv)),
                    'actual_native_endpoint_mark':'filled, P2.8/FindSpan'}
# Lower-degree functions of the same over-repeated vector retain half-open support.
assert r'\draw (\b,1) circle' in (root/'image_tex/ch02/fig_2_04.tex').read_text(encoding='utf-8')
assert r'\draw (axis cs:5,1) circle' in (root/'image_tex/ch02/fig_2_05.tex').read_text(encoding='utf-8')
# Derivative jumps remain open and do not acquire filled point values.
repeated=(root/'image_tex/ch02/fig_2_12.tex').read_text(encoding='utf-8')
for y in ('1.5','-1.5'):
    assert rf'\draw (axis cs:6,{y}) circle' in repeated
(root/'image_tex/build/clamped-endpoint-check.json').write_text(json.dumps(report,indent=2)+'\n')
print('PASS: four clamped endpoint families; lower-degree half-open supports and derivative jumps preserved.')

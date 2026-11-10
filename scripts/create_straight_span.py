"""Fig3.6: collinear active quadratic controls produce a straight curve interval."""
from pathlib import Path
from fractions import Fraction as F
import json
from native_bspline import segments,check,point,cubic_path

root=Path(__file__).resolve().parents[1];target=root/'image_tex/ch03/fig_3_06.tex'
assert not target.exists()
knots=(F(0),)*3+tuple(F(i,5) for i in range(1,5))+(F(1),)*3
controls=((0,0),(-1,3),(6,F(7,2)),(4,0),(2,F(-7,2)),(9,F(-7,2)),(8,0))
segs=segments(knots,controls,2);count=check(knots,controls,2,segs)
assert all(c[2]==0 for c in segs[2]['power'])
assert segs[1]['bern'][-1]==(F(5),F(7,4)) and segs[2]['bern'][-1]==(F(3),F(-7,4))
lines=['% Fig3.6: p=2, U=(0,0,0,1/5,2/5,3/5,4/5,1,1,1).',
       '% Representative controls with exactly collinear, equally spaced P2,P3,P4.',
       '% C(2/5)..C(3/5) has exactly zero quadratic coefficient; native straight line.',
       r'\begin{tikzpicture}[book line,x=1cm,y=1cm]']
for i,p in enumerate(controls): lines.append(r'\coordinate (P'+str(i)+') at '+point(p)+';')
lines.append(r'\draw[book grid] (P0)--(P1)--(P2)--(P3)--(P4)--(P5)--(P6);')
for j,seg in enumerate(segs):
    lines.append(r'\draw '+point(seg['bern'][0])+'--'+point(seg['bern'][-1])+';' if j==2 else cubic_path(seg))
for j,seg in enumerate(segs[:-1]):
    lines.append(r'\fill '+point(seg['bern'][-1])+' circle[radius=1.7pt];')
    if j in (1,2): lines.append(r'\node[right=7pt] at '+point(seg['bern'][-1])+r' {$\mathbf C\!\left(\frac{'+str(j+1)+r'}{5}\right)$};')
lines.append(r'\foreach \i in {0,...,6} \node[book point] at (P\i) {};')
for i,pos in enumerate(['below','above left','above right','right','below left','below right','above right']):
    lines.append(r'\node['+pos+'=4pt] at (P'+str(i)+r') {$\mathbf P_{'+str(i)+'}$};')
lines.append(r'\end{tikzpicture}')
target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/straight-span-check.json').write_text(json.dumps({'figure':'3.6',
    'knots':list(map(str,knots)),'representative_controls':[[str(v) for v in p] for p in controls],
    'exact_deboor_comparisons':count,'straight_span':["2/5","3/5"],
    'quadratic_coefficients_zero':True,'straight_endpoints':[['5','7/4'],['3','-7/4']]},indent=2)+'\n')
print(f'PASS: {count} exact curve checks; [2/5,3/5] is exactly linear.')

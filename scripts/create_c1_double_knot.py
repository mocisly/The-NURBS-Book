"""Fig3.11: geometric constraints restore C1 at a quadratic double knot."""
from pathlib import Path
from fractions import Fraction as F
import json
from bspline_math import derivative,evaluate
from native_bspline import segments,check,point,cubic_path

root=Path(__file__).resolve().parents[1];target=root/'image_tex/ch03/fig_3_11.tex'
assert not target.exists()
knots=(F(0),)*3+tuple(F(i,5) for i in (1,2,3,4,4))+(F(1),)*3
controls=((0,0),(F(2,5),3),(4,5),(6,3),(6,0),(9,0),(12,0),(11,4))
segs=segments(knots,controls,2);count=check(knots,controls,2,segs)
u=F(4,5);left,right=segs[-2],segs[-1]
assert left['bern'][-1]==right['bern'][0]==controls[5]
dl=tuple(evaluate(derivative(c),u) for c in left['power']);dr=tuple(evaluate(derivative(c),u) for c in right['power'])
ddl=tuple(evaluate(derivative(derivative(c)),u) for c in left['power']);ddr=tuple(evaluate(derivative(derivative(c)),u) for c in right['power'])
assert dl==dr==(30,0) and ddl!=ddr
assert tuple(b-a for a,b in zip(controls[4],controls[5]))==tuple(b-a for a,b in zip(controls[5],controls[6]))
lines=['% Fig3.11: same double-knot vector as Fig3.10; representative controls.',
       '% P4,P5,P6 collinear and equally spaced; C1 but not C2 at u=4/5.',
       '% Exact native quadratic segments, no contour tracing.',
       r'\begin{tikzpicture}[book line,x=1cm,y=1cm]']
for i,p in enumerate(controls): lines.append(r'\coordinate (P'+str(i)+') at '+point(p)+';')
lines.append(r'\draw[book grid] '+'--'.join('(P'+str(i)+')' for i in range(8))+';')
for seg in segs: lines.append(cubic_path(seg))
lines.append(r'\foreach \i in {0,...,7} \node[book point] at (P\i) {};')
for seg in segs[:-1]: lines.append(r'\fill '+point(seg['bern'][-1])+' circle[radius=1.7pt];')
for i,pos in enumerate(['below','above left','above','right','below','below','below right','above']):
    lines.append(r'\node['+pos+'=4pt] at (P'+str(i)+r') {$\mathbf P_{'+str(i)+'}$};')
lines.append(r'\end{tikzpicture}')
target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/c1-double-knot-check.json').write_text(json.dumps({'figure':'3.11',
    'knots':list(map(str,knots)),'representative_controls':[[str(v) for v in p] for p in controls],
    'exact_curve_checks':count,'knot_parameter':'4/5','interpolated_control':5,
    'left_derivative':list(map(str,dl)),'right_derivative':list(map(str,dr)),
    'left_second_derivative':list(map(str,ddl)),'right_second_derivative':list(map(str,ddr)),
    'C1_not_C2':True,'P4_P5_P6_equally_spaced':True},indent=2)+'\n')
print(f'PASS: {count} exact curve checks; equal first and unequal second derivatives at4/5.')

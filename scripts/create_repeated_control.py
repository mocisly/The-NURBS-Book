"""Fig3.13: a repeated control creates a C1 zero-speed cusp with straight sides."""
from pathlib import Path
from fractions import Fraction as F
import json
from bspline_math import derivative,evaluate
from native_bspline import segments,check,point,cubic_path

root=Path(__file__).resolve().parents[1];target=root/'image_tex/ch03/fig_3_13.tex'
assert not target.exists()
knots=(F(0),)*3+(F(1,4),F(1,2),F(3,4))+(F(1),)*3
controls=((0,4),(3,-1),(6,3),(6,3),(9,-1),(12,5))
segs=segments(knots,controls,2);count=check(knots,controls,2,segs)
assert segs[1]['bern'][-1]==segs[2]['bern'][0]==controls[2]==controls[3]
for seg in segs[1:3]: assert tuple(evaluate(derivative(c),F(1,2)) for c in seg['power'])==(0,0)
for seg,indices in [(segs[1],(1,2)),(segs[2],(3,4))]:
    a,b=[controls[i] for i in indices]
    for q in seg['bern']: assert (q[0]-a[0])*(b[1]-a[1])==(q[1]-a[1])*(b[0]-a[0])
lines=['% Fig3.13: quadratic caption knots, representative controls with P2=P3.',
       '% C(1/2)=P2=P3; exact straight intervals [1/4,1/2] and [1/2,3/4].',
       '% Both one-sided first derivatives vanish at1/2; no tracing.',
       r'\begin{tikzpicture}[book line,x=1cm,y=1cm]']
for i,p in enumerate(controls): lines.append(r'\coordinate (P'+str(i)+') at '+point(p)+';')
lines.append(r'\draw[book grid] (P0)--(P1)--(P2)--(P4)--(P5);')
for j,seg in enumerate(segs):
    lines.append(r'\draw '+point(seg['bern'][0])+'--'+point(seg['bern'][-1])+';' if j in (1,2) else cubic_path(seg))
for i in (0,1,4,5): lines.append(r'\node[book point] at (P'+str(i)+') {};')
for seg in segs[:-1]: lines.append(r'\fill '+point(seg['bern'][-1])+' circle[radius=1.7pt];')
lines += [r'\node[above=5pt] at (P2) {$\mathbf P_2=\mathbf P_3$};',
          r'\node[below right=6pt] at '+point(segs[0]['bern'][-1])+r' {$\mathbf C\!\left(\frac14\right)$};',
          r'\node[above right=6pt] at '+point(segs[2]['bern'][-1])+r' {$\mathbf C\!\left(\frac34\right)$};']
for i,pos in [(0,'above left'),(1,'below'),(4,'below'),(5,'above right')]:
    lines.append(r'\node['+pos+'=4pt] at (P'+str(i)+r') {$\mathbf P_{'+str(i)+'}$};')
lines.append(r'\end{tikzpicture}')
target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/repeated-control-check.json').write_text(json.dumps({'figure':'3.13',
    'knots':list(map(str,knots)),'representative_controls':controls,
    'exact_curve_checks':count,'repeated_controls':[2,3],'C_half_interpolates_repeated_control':True,
    'left_right_first_derivatives_at_half':[0,0],'two_exact_straight_intervals':True,
    'quarter_point':list(map(str,segs[0]['bern'][-1])),'three_quarter_point':list(map(str,segs[2]['bern'][-1]))},indent=2)+'\n')
print(f'PASS: {count} exact checks, two straight intervals and C1 zero-speed cusp.')

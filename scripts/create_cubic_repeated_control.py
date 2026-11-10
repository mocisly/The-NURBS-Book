"""Fig3.14: identical repeated controls, distinct cubic knot multiplicities."""
from pathlib import Path
from fractions import Fraction as F
import json
from bspline_math import evaluate,derivative
from native_bspline import segments,check,point,cubic_path

root=Path(__file__).resolve().parents[1];target=root/'image_tex/ch03/fig_3_14.tex'
assert not target.exists()
controls=((2,0),(0,F(9,2)),(5,F(15,2)),(5,F(15,2)),(10,F(9,2)),(8,0))
ka=(F(0),)*4+(F(1,4),F(3,4))+(F(1),)*4
kb=(F(0),)*4+(F(1,2),F(1,2))+(F(1),)*4
sa,sb=segments(ka,controls,3),segments(kb,controls,3)
count=check(ka,controls,3,sa)+check(kb,controls,3,sb)
half_a=tuple(evaluate(c,F(1,2)) for c in sa[1]['power'])
assert half_a!=controls[2] and half_a[0]==5 and half_a[1]<controls[2][1]
da=tuple(evaluate(derivative(c),F(1,2)) for c in sa[1]['power'])
assert da[0]!=0 and da[1]==0
assert sb[0]['bern'][-1]==sb[1]['bern'][0]==controls[2]
for seg in sb: assert tuple(evaluate(derivative(c),F(1,2)) for c in seg['power'])==(0,0)
lines=['% Fig3.14: cubic repeated control, identical representative polygon in(a),(b).',
       '% Knots copied from caption: (a)1/4,3/4; (b)1/2,1/2, clamped ends.',
       '% Exact native cubic segments; rounded apex(a), zero-speed C1 cusp(b). No tracing.',
       r'\begin{tikzpicture}[book line,x=1cm,y=1cm]']
for panel,segs,shift in [('a',sa,11),('b',sb,1)]:
    lines.append(r'\begin{scope}[yshift='+str(shift)+'cm]')
    for i,p in enumerate(controls): lines.append(r'\coordinate (P'+str(i)+') at '+point(p)+';')
    lines.append(r'\draw[book grid] (P0)--(P1)--(P2)--(P4)--(P5);')
    for seg in segs: lines.append(cubic_path(seg))
    for i in (0,1,2,4,5): lines.append(r'\node[book point] at (P'+str(i)+') {};')
    for seg in segs[:-1]: lines.append(r'\fill '+point(seg['bern'][-1])+' circle[radius=1.7pt];')
    lines.append(r'\node[above=5pt] at (P2) {$\mathbf P_2=\mathbf P_3$};')
    for i,pos in [(0,'below left'),(1,'left'),(4,'right'),(5,'below right')]:
        lines.append(r'\node['+pos+'=4pt] at (P'+str(i)+r') {$\mathbf P_{'+str(i)+'}$};')
    lines.append(r'\end{scope}')
    lines.append(r'\node at (5,'+str(shift-1)+') {('+panel+')};')
lines.append(r'\end{tikzpicture}')
target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/cubic-repeated-control-check.json').write_text(json.dumps({'figure':'3.14',
    'representative_controls':[[str(v) for v in p] for p in controls],
    'knots_a':list(map(str,ka)),'knots_b':list(map(str,kb)),'exact_curve_checks':count,
    'a_half_point':list(map(str,half_a)),'a_half_tangent':list(map(str,da)),
    'a_does_not_interpolate_repeated_control':True,'b_interpolates_repeated_control':True,
    'b_one_sided_derivatives_at_half':[0,0],'identical_control_polygons':True},indent=2)+'\n')
print(f'PASS: {count} exact curve checks; rounded apex(a) vs zero-speed cusp(b).')

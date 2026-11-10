"""Fig3.12: C2 at simple knots, C1 at the doubled three-quarter knot."""
from pathlib import Path
from fractions import Fraction as F
import json
from bspline_math import derivative,evaluate
from native_bspline import segments,check,point,cubic_path

root=Path(__file__).resolve().parents[1];target=root/'image_tex/ch03/fig_3_12.tex'
assert not target.exists()
knots=(F(0),)*4+tuple(F(i,4) for i in (1,2,3,3))+(F(1),)*4
controls=((0,0),(F(2,5),3),(4,5),(6,3),(6,0),(F(21,2),0),(12,2),(10,4))
segs=segments(knots,controls,3);count=check(knots,controls,3,segs)
joins={}
for left,right in zip(segs,segs[1:]):
    u=left['b'];a,b=left['power'],right['power'];orders=[]
    for order in range(4):
        dl=tuple(evaluate(c,u) for c in a);dr=tuple(evaluate(c,u) for c in b)
        orders.append({'order':order,'left':list(map(str,dl)),'right':list(map(str,dr)),'equal':dl==dr})
        a,b=tuple(map(derivative,a)),tuple(map(derivative,b))
    joins[str(u)]=orders
assert all(joins[u][order]['equal'] for u in ('1/4','1/2') for order in range(3))
assert joins['3/4'][0]['equal'] and joins['3/4'][1]['equal'] and not joins['3/4'][2]['equal']
lines=['% Fig3.12: cubic caption knots with double3/4.',
       '% Representative controls; simple knots C2, double knot C1 but not C2.',
       '% Exact native cubic Bezier segments, no tracing.',
       r'\begin{tikzpicture}[book line,x=1cm,y=1cm]']
for i,p in enumerate(controls): lines.append(r'\coordinate (P'+str(i)+') at '+point(p)+';')
lines.append(r'\draw[book grid] '+'--'.join('(P'+str(i)+')' for i in range(8))+';')
for seg in segs: lines.append(cubic_path(seg))
lines.append(r'\foreach \i in {0,...,7} \node[book point] at (P\i) {};')
for seg in segs[:-1]: lines.append(r'\fill '+point(seg['bern'][-1])+' circle[radius=1.7pt];')
for i,pos in enumerate(['below','above left','above','right','below','below','right','above']):
    lines.append(r'\node['+pos+'=4pt] at (P'+str(i)+r') {$\mathbf P_{'+str(i)+'}$};')
lines.append(r'\end{tikzpicture}')
target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/cubic-continuity-check.json').write_text(json.dumps({'figure':'3.12',
    'knots':list(map(str,knots)),'representative_controls':[[str(v) for v in p] for p in controls],
    'exact_curve_checks':count,'one_sided_derivatives':joins,'C2_simple_C1_double':True},indent=2)+'\n')
print(f'PASS: {count} exact curve checks; C2 simple knots and C1(not C2) at3/4.')

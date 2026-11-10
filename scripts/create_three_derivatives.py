"""Printed Fig3.18 (source19): exact first three derivatives at u=2/5."""
from pathlib import Path
from fractions import Fraction as F
import json
from bspline_math import derivative,evaluate
from native_bspline import segments,check,point,cubic_path

root=Path(__file__).resolve().parents[1];target=root/'image_tex/ch03/fig_3_19.tex';assert not target.exists()
knots=(F(0),)*4+(F(1,4),F(3,4))+(F(1),)*4
controls=((2,0),(0,5),(F(7,2),F(15,2)),(F(15,2),F(15,2)),(11,5),(9,0))
families=[];k,p,c=knots,3,controls;count=0
for order in range(4):
    segs=segments(k,c,p);count+=check(k,c,p,segs);families.append((k,c,p,segs))
    if p:
        c=tuple(tuple(p*F(c[i+1][d]-c[i][d],k[i+p+1]-k[i+1]) for d in range(2)) for i in range(len(c)-1))
        k,p=k[1:-1],p-1
u=F(2,5);polys=families[0][3][1]['power'];values=[]
for order in range(4):
    v=tuple(evaluate(c,u) for c in polys);values.append(v)
    recursive=next(s for s in families[order][3] if s['a']<=u<s['b'])
    assert v==tuple(evaluate(c,u) for c in recursive['power'])
    polys=tuple(map(derivative,polys))
assert values==[(F(9517,2250),F(319,45)),(F(958,75),F(8,3)),(F(-32,15),F(-80,3)),(F(64,3),F(0))]
lines=['% Printed Fig3.18, source19: representative symmetric six-control polygon.',
       '% Clamped cubic needs10 knots: U=(0,0,0,0,1/4,3/4,1,1,1,1).',
       '% All three derivative arrows at u=2/5, display scale2/5 from text.',
       '% Exact recursive derivative controls and native cubic segments, no tracing.',
       r'\begin{tikzpicture}[book line,x=1cm,y=1cm]']
for i,p in enumerate(controls): lines.append(r'\coordinate (P'+str(i)+') at '+point(p)+';')
lines.append(r'\draw[book grid] (P0)--(P1)--(P2)--(P3)--(P4)--(P5);')
for seg in families[0][3]: lines.append(cubic_path(seg))
for order,v in enumerate(values[1:],1):
    end=tuple(values[0][d]+F(2,5)*v[d] for d in range(2))
    lines += [r'\draw[book axis] '+point(values[0])+'--'+point(end)+';',
              r'\node['+('above right' if order==1 else 'right')+'=5pt] at '+point(end)+r' {$\mathbf C^{('+str(order)+r')}\!\left(\frac25\right)$};']
lines.append(r'\foreach \i in {0,...,5} \node[book point] at (P\i) {};')
for seg in families[0][3][:-1]: lines.append(r'\fill '+point(seg['bern'][-1])+' circle[radius=1.7pt];')
lines += [r'\node[book point] at '+point(values[0])+' {};',
          r'\node[below right=6pt] at '+point(values[0])+r' {$\mathbf C\!\left(\frac25\right)$};']
for i,pos in enumerate(['below left','left','above','above','right','below right']):
    gap='14pt' if i==3 else '5pt'
    lines.append(r'\node['+pos+'='+gap+'] at (P'+str(i)+r') {$\mathbf P_{'+str(i)+'}$};')
lines.append(r'\end{tikzpicture}')
target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/three-derivatives-check.json').write_text(json.dumps({'figure':'3.18','source_index':19,
    'knots':list(map(str,knots)),'knots_count_matches_degree_and_controls':True,
    'representative_controls':[[str(v) for v in q] for q in controls],
    'exact_curve_checks_all_four_orders':count,'parameter':'2/5',
    'point_and_three_derivatives':[[str(v) for v in q] for q in values],
    'polynomial_vs_recursive_derivative_controls':True,'display_scale':'2/5'},indent=2)+'\n')
print(f'PASS: {count} exact curve checks; three derivative orders and all10knots verified.')

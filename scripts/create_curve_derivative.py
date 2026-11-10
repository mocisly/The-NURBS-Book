"""Fig3.15: a quadratic curve, tangents, and its exact linear derivative curve."""
from pathlib import Path
from fractions import Fraction as F
import json
from bspline_math import derivative,evaluate
from native_bspline import segments,check,point,cubic_path

root=Path(__file__).resolve().parents[1];target=root/'image_tex/ch03/fig_3_15.tex'
assert not target.exists()
knots=(F(0),)*3+(F(2,5),F(3,5))+(F(1),)*3
controls=((1,1),(2,3),(F(9,2),3),(5,1),(6,2))
q=tuple(tuple(2*F(controls[i+1][d]-controls[i][d],knots[i+3]-knots[i+1]) for d in range(2)) for i in range(4))
assert q==((5,10),(F(25,3),0),(F(5,3),F(-20,3)),(5,5))
dk=knots[1:-1];curve=segments(knots,controls,2);dc=segments(dk,q,1)
count=check(knots,controls,2,curve)+check(dk,q,1,dc)
for a,b in zip(curve,dc):
    assert a['a']==b['a'] and a['b']==b['b']
    assert tuple(map(derivative,a['power']))==b['power']
def at(segs,u,der=0):
    s=next((s for s in segs if s['a']<=u<s['b']),segs[-1])
    return tuple(evaluate(derivative(c) if der else c,u) for c in s['power'])
parameters=(F(0),F(1,5),F(2,5),F(3,5),F(1))
labels=('0',r'\frac15',r'\frac25',r'\frac35','1')
vectors={str(u):at(curve,u,1) for u in parameters}
assert all(vectors[str(u)]==at(dc,u) for u in parameters)
lines=['% Fig3.15: exact caption U=(0,0,0,2/5,3/5,1,1,1), derivative Uprime.',
       '% Representative controls P=(1,1),(2,3),(9/2,3),(5,1),(6,2).',
       '% Panel(a) tangent arrows uniformly displayed at1/2 length, stated in caption.',
       '% Panel(b) controls computed by Eq3.4; actual derivative curve. No tracing.',
       r'\begin{tikzpicture}[book line]',
       r'\begin{scope}[yshift=12cm,x=1cm,y=1cm]',
       r'\draw[book axis] (0,0)--(8.8,0) node[right=4pt] {$x$};',
       r'\draw[book axis] (0,0)--(0,4.7) node[above=4pt] {$y$};']
for i,p in enumerate(controls): lines.append(r'\coordinate (P'+str(i)+') at '+point(p)+';')
lines.append(r'\draw[book grid] (P0)--(P1)--(P2)--(P3)--(P4);')
for seg in curve: lines.append(cubic_path(seg))
for u,label in zip(parameters,labels):
    a=at(curve,u);v=vectors[str(u)];b=tuple(a[d]+v[d]/2 for d in range(2))
    lines.append(r'\draw[book axis'+(',dashed' if u==F(1,5) else '')+'] '+point(a)+'--'+point(b)+';')
    pos='above right' if u in (0,F(1,5),1) else 'right'
    lines.append(r'\node['+pos+'=5pt] at '+point(b)+r" {$\mathbf C'\!\left("+label+r'\right)$};')
lines.append(r'\foreach \i in {0,...,4} \node[book point] at (P\i) {};')
for seg in curve[:-1]: lines.append(r'\fill '+point(seg['bern'][-1])+' circle[radius=1.7pt];')
lines.append(r'\node[book point] at '+point(at(curve,F(1,5)))+' {};')
for i,pos in enumerate(['below left','above left','above','below left','below right']):
    lines.append(r'\node['+pos+'=4pt] at (P'+str(i)+r') {$\mathbf P_{'+str(i)+'}$};')
lines += [r'\end{scope}',r'\node at (5cm,10.2cm) {(a)};',
          r'\begin{scope}[xshift=1cm,yshift=4cm,x=.5cm,y=.5cm]',
          r'\draw[book axis] (0,0)--(14,0) node[right=4pt] {$x$};',
          r'\draw[book axis] (0,0)--(0,8) node[above=4pt] {$y$};']
for i,p in enumerate(q): lines.append(r'\coordinate (Q'+str(i)+') at '+point(p)+';')
for i in range(4): lines.append(r'\draw[book grid,-{Stealth[length=5pt]}] (0,0)--(Q'+str(i)+');')
lines.append(r'\draw (Q0)--(Q1)--(Q2)--(Q3);')
v=vectors['1/5']
lines += [r'\draw[book axis,dashed] (0,0)--'+point(v)+';',
          r'\node[right=7pt] at '+point(v)+r" {$\mathbf C'\!\left(\frac15\right)$};",
          r'\foreach \i in {0,...,3} \node[book point] at (Q\i) {};']
for i,pos in enumerate(['above right','below right','below left','above left']):
    lines.append(r'\node['+pos+'=4pt] at (Q'+str(i)+r') {$\mathbf Q_{'+str(i)+'}$};')
lines += [r'\end{scope}',r'\node at (5cm,0cm) {(b)};',r'\end{tikzpicture}']
target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
report={'figure':'3.15','knots':list(map(str,knots)),'derivative_knots':list(map(str,dk)),
    'representative_controls':[[str(v) for v in p] for p in controls],
    'derivative_controls':[[str(v) for v in p] for p in q],
    'Eq3_4_multipliers':['5','10/3','10/3','5'],'exact_curve_checks':count,
    'piecewise_derivative_identity':True,'tangent_vectors':{u:list(map(str,v)) for u,v in vectors.items()},
    'panel_a_tangent_display_scale':'1/2'}
(root/'image_tex/build/curve-derivative-check.json').write_text(json.dumps(report,indent=2)+'\n')
print(f'PASS: {count} exact checks, polynomial derivative identity, five tangent vectors, Eq3.4 controls.')

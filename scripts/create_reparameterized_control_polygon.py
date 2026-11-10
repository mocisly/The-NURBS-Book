"""6.10: exact quadratic-to-quartic composition, control polygons and uniform parameter markers."""
from pathlib import Path
from fractions import Fraction as F
import json
from polynomial_native import compose,bernstein
from bspline_math import evaluate,derivative
from native_bspline import segments,check,point,de_boor

root=Path(__file__).resolve().parents[1];target=root/'image_tex/ch06/fig_6_10.tex'
data=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in data['images'] if e['tex']=='image_tex/ch06/fig_6_10.tex')['applied']
C=((F(0),F(1)),(F(0),F(2),-F(2)));f=(F(0),F(7,12),F(5,12));D=tuple(compose(c,f) for c in C)
P=bernstein(C);Q=bernstein(D);U=(F(0),)*3+(F(1),)*3;S=(F(0),)*5+(F(1),)*5
assert P==((F(0),F(0)),(F(1,2),F(1)),(F(1),F(0)))
assert Q==((F(0),F(0)),(F(7,48),F(7,24)),(F(13,36),F(263,432)),(F(31,48),F(17,24)),(F(1),F(0)))
checks=check(U,P,2,segments(U,P,2))+check(S,Q,4,segments(S,Q,4))
for i in range(101):
    s=F(i,100);u=evaluate(f,s)
    assert de_boor(U,P,2,u)==de_boor(S,Q,4,s)==tuple(evaluate(d,s) for d in D)
    assert tuple(evaluate(derivative(d),s) for d in D)==tuple(evaluate(derivative(c),u)*evaluate(derivative(f),s) for c in C)
old=[de_boor(U,P,2,F(i,20)) for i in range(21)]
new=[de_boor(S,Q,4,F(i,20)) for i in range(21)]
lines=['% Exact Ex6.6 controls, including Q2=(13/36,263/432).',
       '% Plus markers are C(i/20), square markers are C(f(i/20)); one common geometry.',
       r'\begin{tikzpicture}[book line,x=12cm,y=12cm]',r'\path[use as bounding box] (-.16,-.16) rectangle (1.24,1.2);',
       r'\draw[book axis] (0,0)--(1.18,0) node[right=4pt] {$x$};',
       r'\draw[book axis] (0,0)--(0,1.15) node[above=4pt] {$y$};',
       r'\draw[book grid,dashed] '+'--'.join(map(point,P))+';',
       r'\draw[book grid] '+'--'.join(map(point,Q))+';']
for a in old:
    lines += [r'\begin{scope}[shift={'+point(a)+'}]',r'\draw[book grid] (-1.8pt,0)--(1.8pt,0) (0,-1.8pt)--(0,1.8pt);',r'\end{scope}']
for a in new:lines.append(r'\node[rectangle,draw,line width=.35pt,inner sep=1.4pt] at '+point(a)+' {};')
for i,(a,anchor) in enumerate(zip(Q,('below','left','above right','above right','below'))):
    label=(r'\mathbf P_0=\mathbf Q_0' if i==0 else r'\mathbf P_2=\mathbf Q_4' if i==4 else r'\mathbf Q_'+str(i))
    lines.append(r'\draw '+point(a)+r' circle[radius=2pt] node['+anchor+r'=6pt] {$'+label+'$};')
lines += [r'\draw '+point(P[1])+r' circle[radius=2pt] node[above=6pt] {$\mathbf P_1$};',r'\end{tikzpicture}']
target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/reparameterized-control-polygon-check.json').write_text(json.dumps({
    'figure':'6.10','original_degree':2,'composed_degree':4,'original_controls':[[str(x) for x in p] for p in P],
    'new_controls':[[str(x) for x in p] for p in Q],'native_basis_checks':checks,
    'exact_composition_identities':101,'exact_chain_rule_checks':101,
    'uniform_parameter_step':'1/20','original_plus_points':[[str(x) for x in p] for p in old],
    'new_square_points':[[str(x) for x in p] for p in new]},indent=2)+'\n')
print(f'PASS:{checks} exact native basis checks,101 composition+101 chain-rule identities; all printed Q controls verified.')

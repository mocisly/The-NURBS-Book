"""6.8: composition diagram with an exact monotone nonlinear parameter mapping."""
from pathlib import Path
from fractions import Fraction as F
import json
from bspline_math import evaluate,derivative
from polynomial_native import compose,bernstein
from native_bspline import cubic_path,point

root=Path(__file__).resolve().parents[1];target=root/'image_tex/ch06/fig_6_08.tex'
data=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in data['images'] if e['tex']=='image_tex/ch06/fig_6_08.tex')['applied']
f=(F(0),F(1,2),F(1,2));C=((F(6),F(8)),(F(7),F(9),-F(24),F(18)))
D=tuple(compose(c,f) for c in C);s=F(1,2);u=evaluate(f,s);P=tuple(evaluate(c,u) for c in C)
assert u==F(3,8) and evaluate(f,F(0))==0 and evaluate(f,F(1))==1
for i in range(101):
    t=F(i,100);v=evaluate(f,t)
    assert evaluate(derivative(f),t)>=F(1,2)
    assert tuple(evaluate(c,v) for c in C)==tuple(evaluate(d,t) for d in D)
lines=['% Exact representative composition f(s)=(s+s^2)/2 on[0,1].',
       '% Chosen s=1/2 maps to u=3/8; curve point evaluated exactly.',
       r'\begin{tikzpicture}[book line]',r'\path[use as bounding box] (-.7,-.7) rectangle (14.6,10.6);',
       cubic_path({'bern':bernstein(C)}),
       r'\draw[book grid] (0,3)--(9,3);',r'\draw[book grid] (6,0)--(12,0);',
       r'\foreach \x in {0,3,6,9} {\draw[book grid] (\x,2.91)--(\x,3.09);}',
       r'\foreach \x in {6,8,10,12} {\draw[book grid] (\x,-.09)--(\x,.09);}',
       r'\node[below=5pt] at (0,3) {$a$};',r'\node[below=5pt] at (9,3) {$b$};',
       r'\node[below=5pt] at (6,0) {$c$};',r'\node[below=5pt] at (12,0) {$d$};',
       r'\draw '+point((9*u,F(3)))+r' circle[radius=2pt] node[above=5pt] {$u$};',
       r'\draw (9,0) circle[radius=2pt] node[below=5pt] {$s$};',
       r'\draw '+point(P)+r' circle[radius=2pt] node[above=6pt] {$\mathbf C(f(s))$};',
       r'\draw[book axis] (8.7,.4)--(3.75,2.6);',r'\node at (6.6,1.9) {$f$};',
       r'\draw[book axis] (3.75,3.5)--'+point((P[0]-F(2,5),P[1]-F(2,5)))+';',
       r'\node at (5.8,6.2) {$\mathbf C$};',r'\end{tikzpicture}']
target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/reparameterization-diagram-check.json').write_text(json.dumps({
    'figure':'6.8','representative_mapping':'(s+s^2)/2','s':str(s),'u':str(u),
    'point':list(map(str,P)),'exact_composition_checks':101,
    'global_derivative_lower_bound':'1/2','endpoint_mapping_exact':True},indent=2)+'\n')
print('PASS:101 exact composition identities, endpoints preserved, f prime >=1/2 globally.')

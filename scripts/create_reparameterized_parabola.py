"""6.9: use the exact Ex6.4 parabola and both unscaled endpoint derivatives."""
from pathlib import Path
from fractions import Fraction as F
import json
from polynomial_native import compose,bernstein
from bspline_math import evaluate,derivative
from native_bspline import cubic_path,point

root=Path(__file__).resolve().parents[1];target=root/'image_tex/ch06/fig_6_09.tex'
data=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in data['images'] if e['tex']=='image_tex/ch06/fig_6_09.tex')['applied']
C=((F(0),F(1)),(F(0),F(2),-F(2)));f=(F(0),F(7,12),F(5,12))
D=tuple(compose(c,f) for c in C)
assert D==((F(0),F(7,12),F(5,12)),(F(0),F(7,6),F(11,72),-F(35,36),-F(25,72)))
assert evaluate(f,F(3,5))==F(1,2)
assert tuple(evaluate(d,F(1)) for d in D)==(F(1),F(0))
Cu=tuple(evaluate(derivative(c),F(0)) for c in C);Ds=tuple(evaluate(derivative(c),F(0)) for c in D)
assert Cu==(F(1),F(2)) and Ds==(F(7,12),F(7,6))
for i in range(101):
    s=F(i,100);u=evaluate(f,s)
    assert tuple(evaluate(c,u) for c in C)==tuple(evaluate(d,s) for d in D)
    assert tuple(evaluate(derivative(c),u)*evaluate(derivative(f),s) for c in C)==tuple(evaluate(derivative(d),s) for d in D)
    assert evaluate(derivative(f),s)>=F(7,12)
lines=['% Exact equations6.24-6.27. Endpoint at u=s=1 is(1,0), not OCR(0,0).',
       '% Both derivative arrows drawn at true length in the same isotropic coordinates.',
       r'\begin{tikzpicture}[book line,x=6cm,y=6cm]',r'\path[use as bounding box] (-.18,-.18) rectangle (1.68,2.2);',
       r'\draw[book axis] (0,0)--(1.52,0) node[right=4pt] {$x$};',
       r'\draw[book axis] (0,0)--(0,1.75) node[above=4pt] {$y$};',
       cubic_path({'bern':bernstein(C)}),
       r'\draw[book axis] (0,0)--'+point(Cu)+r' node[above right=6pt] {$\mathbf C^{\prime}(u=0)$};',
       r'\draw[book axis] (0,0)--'+point(Ds)+r' node[right=7pt] {$\mathbf C^{\prime}(s=0)$};',
       r'\draw (.5,.5) circle[radius=2pt] node[above right=7pt] {$\mathbf C(u=\tfrac12)=\mathbf C(s=\tfrac35)$};',
       r'\draw[book grid] (1,-.015)--(1,.015) node[below=6pt] {$1$};',r'\end{tikzpicture}']
target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/reparameterized-parabola-check.json').write_text(json.dumps({
    'figure':'6.9','exact_composed_power_coefficients':[[str(x) for x in c] for c in D],
    'old_endpoint_derivative':list(map(str,Cu)),'new_endpoint_derivative':list(map(str,Ds)),
    'midpoint_mapping':['3/5','1/2'],'correct_endpoint_at_one':['1','0'],
    'exact_composition_checks':101,'exact_chain_rule_checks':101,'f_prime_lower_bound':'7/12'},indent=2)+'\n')
print('PASS:Ex6.4 exact quartic coefficients,101 composition+101 chain-rule identities, both derivative lengths and midpoint correspondence.')

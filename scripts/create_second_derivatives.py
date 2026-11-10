"""Printed Fig3.17 (source18): same curve as3.15, exact endpoint second derivatives."""
from fractions import Fraction as F
from pathlib import Path
import json,re,argparse
from bspline_math import derivative,evaluate
from native_bspline import segments,check,point,cubic_path

parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check-only',action='store_true');args=parser.parse_args()
root=Path(__file__).resolve().parents[1];target=root/'image_tex/ch03/fig_3_18.tex';assert args.check_only or not target.exists()
# Read declared mathematical controls from the already reviewed native Fig3.15.
source=(root/'image_tex/ch03/fig_3_15.tex').read_text(encoding='utf-8')
found=re.findall(r'\\coordinate \(P(\d+)\) at \(([^,]+),([^)]+)\);',source)
assert [int(i) for i,_,_ in found]==list(range(5))
controls=tuple((F(x),F(y)) for _,x,y in found)
assert controls==((1,1),(2,3),(F(9,2),3),(5,1),(6,2))
knots=(F(0),)*3+(F(2,5),F(3,5))+(F(1),)*3
q=tuple(tuple(2*F(controls[i+1][d]-controls[i][d],knots[i+3]-knots[i+1]) for d in range(2)) for i in range(4))
dk=knots[1:-1]
r=tuple(tuple(F(q[i+1][d]-q[i][d],dk[i+2]-dk[i+1]) for d in range(2)) for i in range(3))
curve,dc,ddc=segments(knots,controls,2),segments(dk,q,1),segments(dk[1:-1],r,0)
count=check(knots,controls,2,curve)+check(dk,q,1,dc)+check(dk[1:-1],r,0,ddc)
for a,b,c in zip(curve,dc,ddc):
    assert tuple(map(derivative,a['power']))==b['power']
    assert tuple(map(derivative,b['power']))==c['power']
assert r[0]==(F(25,3),-25) and r[-1]==(F(25,3),F(175,6))
# Independently evaluate the printed endpoint expressions (3.9) and (3.10).
a,b=F(2,5),F(3,5)
f9=tuple(2/a*(controls[0][d]/a-(a+b)*controls[1][d]/(a*b)+controls[2][d]/b) for d in range(2))
f10=tuple(2/(1-b)*(controls[4][d]/(1-b)-(2-b-a)*controls[3][d]/((1-b)*(1-a))+controls[2][d]/(1-a)) for d in range(2))
assert f9==r[0] and f10==r[-1]
lines=['% Printed Fig3.17, source18: exact same controls and knots as reviewed Fig3.15.',
       '% Endpoint second derivatives=(25/3,-25) and(25/3,175/6).',
       '% Arrows at1/10 display scale, stated in caption. Native mathematical geometry, no tracing.',
       r'\begin{tikzpicture}[book line,x=1cm,y=1cm]']
for i,p in enumerate(controls): lines.append(r'\coordinate (P'+str(i)+') at '+point(p)+';')
lines.append(r'\draw[book grid] (P0)--(P1)--(P2)--(P3)--(P4);')
for seg in curve: lines.append(cubic_path(seg))
for i,u,v in [(0,'0',r[0]),(4,'1',r[-1])]:
    end=tuple(controls[i][d]+v[d]/10 for d in range(2))
    lines += [r'\draw[book axis] (P'+str(i)+')--'+point(end)+';',
              r'\node[right=5pt] at '+point(end)+r' {$\mathbf C^{(2)}('+u+')$};']
lines.append(r'\foreach \i in {0,...,4} \node[book point] at (P\i) {};')
for seg in curve[:-1]: lines.append(r'\fill '+point(seg['bern'][-1])+' circle[radius=1.7pt];')
for i,pos in enumerate(['left','above left','above','below','right']):
    lines.append(r'\node['+pos+'=4pt] at (P'+str(i)+r') {$\mathbf P_{'+str(i)+'}$};')
lines.append(r'\end{tikzpicture}')
if not args.check_only: target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/second-derivatives-check.json').write_text(json.dumps({'figure':'3.17','source_index':18,
    'same_controls_as_native_3_15':True,'knots':list(map(str,knots)),
    'controls':[[str(v) for v in p] for p in controls],'exact_curve_checks':count,
    'polynomial_derivative_identity_two_orders':True,'Eq3_9_and_Eq3_10_verified':True,
    'three_constant_second_derivatives':[[str(v) for v in p] for p in r],
    'display_scale':'1/10'},indent=2)+'\n')
print(f'PASS: {count} exact checks, two derivative identities and three constant second derivatives.')

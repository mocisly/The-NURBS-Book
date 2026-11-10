"""7.15: exact Ex7.1 semicircle with a genuinely nonzero zero-weight control."""
from pathlib import Path
from fractions import Fraction as F
import json
from polynomial_native import multiply
from bspline_math import add
from rational_geometry import approximate,evaluate,project
from native_bspline import cubic_path,point

root=Path(__file__).resolve().parents[1];manifest=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in manifest['images'] if e['tex']=='image_tex/ch07/fig_7_15.tex')['applied']
r=F(3);H=((r,F(0),F(1)),(F(0),r,F(0)),(-r,F(0),F(1)))
X=(r,-2*r);Y=(F(0),2*r,-2*r);W=(F(1),-F(2),F(2))
identity=add(add(multiply(X,X),multiply(Y,Y)),tuple(-r*r*x for x in multiply(W,W)));assert all(x==0 for x in identity)
for i in range(101):
    u=F(i,100);x,y=project(evaluate(H,u));den=1-2*u+2*u*u;assert den>=F(1,2)
    assert (x,y)==(r*(1-2*u)/den,2*r*u*(1-u)/den) and x*x+y*y==r*r and y>=0
mid=project(evaluate(H,F(1,2)));assert mid==(F(0),r)
dh=tuple(tuple(2*(y-x) for x,y in zip(a,b)) for a,b in zip(H,H[1:]));d=evaluate(dh,F(1,2));h=evaluate(H,F(1,2))
tangent=tuple((d[k]*h[-1]-h[k]*d[-1])/h[-1]**2 for k in range(2));assert tangent==(-4*r,F(0))
paths=approximate(H,F(1,100000))
lines=['% Exact Ex7.1: H0(r,0,1),H1(0,r,0),H2(-r,0,1),displayr3.',
       '% Coefficientwise X^2+Y^2-r^2*W^2=0, W>=1/2, shoulder(0,r).',
       r'\begin{tikzpicture}[book line,x=1.4cm,y=1.4cm]',r'\path[use as bounding box] (-5.2,-1) rectangle (5.2,4.5);',
       r'\draw[book axis] (-4.1,0)--(4.1,0) node[right=4pt] {$x$};',
       r'\draw[book axis] (0,-.4)--(0,4.1) node[above=4pt] {$y$};',
       r'\draw[book axis,book grid] (-3,0)--(-3,3);',r'\draw[book axis,book grid] (3,0)--(3,3);',
       r'\draw[book grid,dashed] (-3,3)--(3,3);']
lines.extend(cubic_path(p) for p in paths)
lines += [r'\draw (-3,0) circle[radius=2pt] node[below left=6pt] {$\mathbf P_2=(-r,0)$};',
          r'\draw (3,0) circle[radius=2pt] node[below right=6pt] {$\mathbf P_0=(r,0)$};',
          r'\node[rectangle,draw,line width=.35pt,inner sep=1.8pt] at (0,3) {};',
          r'\node[above left=8pt] at (0,3) {$\mathbf C(\tfrac12)$};',
          r'\node[above=6pt] at (2.4,3.3) {$\overrightarrow{\mathbf P}_1$};',r'\end{tikzpicture}']
(root/'image_tex/ch07/fig_7_15.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/infinite-semicircle-check.json').write_text(json.dumps({'figure':'7.15','display_radius':str(r),'homogeneous_controls':[[str(x) for x in pt] for pt in H],'circle_polynomial_identity_coefficients':list(map(str,identity)),'global_denominator_lower_bound':'1/2','exact_circle_and_formula_checks':101,'midpoint':list(map(str,mid)),'midpoint_tangent':list(map(str,tangent)),'native_paths':len(paths),'certified_native_L1_error':str(max(p['certified_l1_error'] for p in paths))},indent=2)+'\n')
print('PASS:coefficientwise circle identity,101 exact formulas,W>=1/2,midpoint(0,r) and horizontal tangent(-4r,0).')

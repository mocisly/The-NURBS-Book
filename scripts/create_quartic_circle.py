"""7.31: exact quartic full circle obtained by squaring the rational semicircle."""
from fractions import Fraction as F
from pathlib import Path
import json
from native_bspline import segments,check,de_boor,cubic_path,point
from rational_geometry import approximate,project
from polynomial_native import multiply
from bspline_math import add,derivative,evaluate
root=Path(__file__).resolve().parents[1];d=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in d['images'] if e['tex']=='image_tex/ch07/fig_7_39.tex')['applied']
H=tuple(tuple(map(F,h)) for h in [(3,0,3),(0,3,0),(-3,0,1),(0,-3,0),(3,0,3)]);U=(F(0),)*5+(F(1),)*5
ss=segments(U,H,4);X,Y,W=ss[0]['power'];g=(F(1),-F(2));h=(F(0),F(2),-F(2));z=(F(1),-F(2),F(2))
expectedX=add(multiply(g,g),tuple(-v for v in multiply(h,h)));expectedY=tuple(2*v for v in multiply(g,h));expectedW=multiply(z,z)
def pad(p):return tuple(p)+(F(0),)*(5-len(p))
assert tuple(map(pad,(X,Y,W)))==tuple(pad(tuple(3*v for v in p)) for p in (expectedX,expectedY,expectedW))
identity=add(add(multiply(X,X),multiply(Y,Y)),tuple(-v for v in multiply(W,W)));assert all(v==0 for v in identity)
def velocity(u):
    a=[evaluate(p,u) for p in (X,Y,W)];b=[evaluate(derivative(p),u) for p in (X,Y,W)]
    return tuple((b[k]*a[-1]-a[k]*b[-1])/a[-1]**2 for k in range(2))
assert velocity(F(0))==velocity(F(1))==(0,4)
for i in range(401):
    u=F(i,400);q=de_boor(U,H,4,u);x,y=project(q);zz=evaluate(z,u);assert q[-1]==3*zz*zz>=F(3,4) and x*x+y*y==1
    dx,dy=velocity(u);assert x*dy-y*dx==4/zz
assert project(de_boor(U,H,4,F(1,2)))==(-1,0)
nc=check(U,H,4,ss);paths=approximate(H,F(1,200000))
lines=['% Exact Ex7.9 quartic homogeneous controls(3,0,3),(0,3,0),(-3,0,1),(0,-3,0),(3,0,3).',
       '% Q2=(-3,0) is correct; curve is squared rational semicircle, X^2+Y^2=W^2, W>=3/4.',
       r'\begin{tikzpicture}[book line,x=4cm,y=4cm]',r'\path[use as bounding box] (-3.8,-2.4) rectangle (2.1,2.4);',
       r'\draw[book axis,book grid] (-3.45,0)--(1.75,0) node[right=4pt] {$x$};',
       r'\draw[book axis,book grid] (0,-1.35)--(0,2.05) node[above=4pt] {$y$};']
lines.extend(cubic_path(s) for s in paths)
lines += [r'\draw[book axis,book grid] (1,0)--(1,1.75) node[above right=7pt] {$\overrightarrow{\mathbf Q}_1$};',
          r'\draw[book axis,book grid] (-3,0)--(-3,-1.75) node[below right=7pt] {$\overrightarrow{\mathbf Q}_3$};',
          r'\draw (1,0) circle[radius=2pt] node[below right=7pt] {$\mathbf Q_0=\mathbf Q_4$};',
          r'\draw (-3,0) circle[radius=2pt] node[above left=7pt] {$\mathbf Q_2$};',r'\end{tikzpicture}']
(root/'image_tex/ch07/fig_7_39.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/quartic-circle-check.json').write_text(json.dumps({'figure':'7.31','homogeneous_controls':[[str(v) for v in h] for h in H],'exact_complex_square_power_coefficients_verified':True,'exact_circle_polynomial_identity':list(map(str,identity)),'exact_circle_denominator_and_positive_angular_velocity_checks':401,'global_denominator_lower_bound':'3/4','angular_velocity':'4/(1-2u+2u^2)>0','closure_derivative':['0','4'],'native_checks':nc,'native_L1_error':str(max(s['certified_l1_error'] for s in paths))},indent=2)+'\n')
print('PASS:exact complex-square polynomial coefficients and circle identity,401positive angular velocity checks,closedC1,W>=3/4,two true infinite control vectors.')

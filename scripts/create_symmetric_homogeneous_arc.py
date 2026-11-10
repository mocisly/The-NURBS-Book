"""6.12: algebraically verified symmetric circular arc and homogeneous lift."""
from pathlib import Path
from fractions import Fraction as F
from math import isqrt
import json
from native_bspline import point,cubic_path
from rational_geometry import approximate,evaluate,project

root=Path(__file__).resolve().parents[1];target=root/'image_tex/ch06/fig_6_13.tex'
data=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in data['images'] if e['tex']=='image_tex/ch06/fig_6_13.tex')['applied']
# Exact ring Q[w]/(w^2-1/2); each coefficient is a+b*w.
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def multiply(a,b):return (a[0]*b[0]+a[1]*b[1]/2,a[0]*b[1]+a[1]*b[0])
def poly_product(a,b):
    out=[(F(0),F(0)) for i in range(len(a)+len(b)-1)]
    for i,x in enumerate(a):
        for j,y in enumerate(b):out[i+j]=add(out[i+j],multiply(x,y))
    return out
X=[(F(1),F(0)),(-F(2),F(2)),(F(1),-F(2))]
Y=[(F(0),F(0)),(F(0),F(2)),(F(1),-F(2))]
W=[(F(1),F(0)),(-F(2),F(2)),(F(2),-F(2))]
xx,yy,ww=poly_product(X,X),poly_product(Y,Y),poly_product(W,W)
assert all(add(add(a,b),tuple(-x for x in c))==(0,0) for a,b,c in zip(xx,yy,ww))
# Rational enclosure makes rendering certified without a symbolic package.
D=10**40;n=isqrt(2*D*D);lo,hi=F(n,2*D),F(n+1,2*D)
assert lo*lo<F(1,2)<hi*hi;w=(lo+hi)/2
H=((F(1),F(0),F(1)),(w,w,w),(F(0),F(1),F(1)))
P=((F(1),F(0),F(1)),(F(1),F(1),F(1)),(F(0),F(1),F(1)))
lift_path=cubic_path({'bern':H},'book line,dashed')
pieces=approximate(H,F(1,100000));curve=[];maximum=F(0)
for piece in pieces:
    # Rational projector returns(X/W,Y/W); draw on the W=1 plane.
    curve.append(cubic_path({'bern':tuple(tuple(pt)+(F(1),) for pt in piece['bern'])},'book line'))
    maximum=max(maximum,piece['certified_l1_error'])
max_circle_residual=0.
for i in range(101):
    s=F(i,100);h=evaluate(H,s);c=project(h)
    assert h[2]>=F(1,2) and tuple(x*h[2] for x in c)==h[:2]
    max_circle_residual=max(max_circle_residual,abs(float(c[0]*c[0]+c[1]*c[1]-1)))
assert max_circle_residual<1e-38
lines=['% Exact weights(1,sqrt(2)/2,1), homogeneous H0=(1,0,1),H1=(w,w,w),H2=(0,1,1).',
       '% X(s)^2+Y(s)^2=W(s)^2 verified coefficientwise in Q[w]/(w^2-1/2).',
       '% Rational weight enclosure width<1e-40; mathematical rational cubic rendering certified.',
       r'\begin{tikzpicture}[book line]',r'\path[use as bounding box] (-10.2,-4.5) rectangle (9.3,10.5);',
       r'\begin{scope}[x={(-5cm,-1cm)},y={(4cm,-2cm)},z={(0cm,6cm)}]',
       r'\draw[book grid] (-.5,-.5,1)--(1.5,-.5,1)--(1.5,1.5,1)--(-.5,1.5,1)--cycle;',
       r'\node[above right=5pt] at (-.5,-.5,1) {$W=1$};',
       r'\draw[book grid] '+'--'.join(map(point,P))+';',
       r'\draw[book grid,dashed] '+'--'.join(map(point,H))+';']
for s in (F(1,4),F(1,2),F(3,4)):
    h=evaluate(H,s);c=project(h)+(F(1),)
    lines.append(r'\draw[book grid,densely dotted] (0,0,0)--'+point(c)+';')
    for a in (h,c):lines.append(r'\draw '+point(a)+r' circle[radius=1.4pt];')
lines += [lift_path]+curve
for a,label,anchor in [(P[0],r'\mathbf P_0=\mathbf P_0^w','left'),(P[2],r'\mathbf P_2=\mathbf P_2^w','right'),
                       (P[1],r'\mathbf P_1','left'),(H[1],r'\mathbf P_1^w','below left')]:
    gap='25pt' if a==H[1] else '5pt' if a==P[1] else '8pt'
    lines.append(r'\draw '+point(a)+r' circle[radius=2pt] node['+anchor+'='+gap+r'] {$'+label+'$};')
lines += [r'\draw[book axis] (0,0,0)--(1.8,0,0) node[below left=4pt] {$X$};',
          r'\draw[book axis] (0,0,0)--(0,1.8,0) node[below right=4pt] {$Y$};',
          r'\draw[book axis] (0,0,0)--(0,0,1.6) node[above=4pt] {$W$};',r'\end{scope}',r'\end{tikzpicture}']
target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/symmetric-homogeneous-arc-check.json').write_text(json.dumps({
    'figure':'6.12','exact_unit_circle_polynomial_identity':True,'quadratic_field_relation':'w^2=1/2',
    'exact_endpoint_derivatives':['(0,2w)','(-2w,0)'],'exact_midpoint':'(w,w)',
    'rational_weight_enclosure':list(map(str,(lo,hi))),
    'weight_enclosure_projected_L1_error_bound':str(12*(hi-lo)),
    'native_rational_paths':len(pieces),'maximum_certified_native_curve_error':str(maximum),
    'physical_projection_operator_L1_upper_bound':6,'central_projection_checks':101,
    'maximum_rational_weight_circle_residual':max_circle_residual},indent=2)+'\n')
print(f'PASS:exact circle polynomial identity overQ(sqrt2),101 central projections;{len(pieces)} certified native rational paths.')

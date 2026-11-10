"""7.18: prescribed negative-weight240deg arc and all three signed rational bases."""
from pathlib import Path
from fractions import Fraction as F
from math import isqrt
import json
from native_bspline import segments,check,de_boor,point
from rational_geometry import project
from polynomial_native import multiply
from bspline_math import add,derivative,evaluate
from native_rational_basis import graphs

root=Path(__file__).resolve().parents[1];manifest=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
for name in ('fig_7_20.tex','fig_7_21.tex'):
    assert not next(e for e in manifest['images'] if e['tex']=='image_tex/ch07/'+name)['applied']
U=(F(0),)*3+(F(1),)*3;W=(F(1),-F(1,2),F(1))
X=(F(1),-F(2));Y=(F(1,2),-F(3),F(3));Z=(F(1),-F(3),F(3))
identity=add(add(tuple(F(3,4)*x for x in multiply(X,X)),multiply(Y,Y)),tuple(-z for z in multiply(Z,Z)));assert all(x==0 for x in identity)
cross=add(multiply(X,derivative(Y)),tuple(-x for x in multiply(Y,derivative(X))))
assert cross==tuple(-2*z for z in Z) # C cross C'=-2a/W<0 throughout.
D=10**40;n=isqrt(3*D*D);lo,hi=F(n,2*D),F(n+1,2*D);assert lo*lo<F(3,4)<hi*hi;a=(lo+hi)/2
P=((a,F(1,2)),(F(0),F(2)),(-a,F(1,2)));H=tuple(tuple(w*x for x in p)+(w,) for p,w in zip(P,W))
ss=segments(U,H,2);nativechecks=check(U,H,2,ss)
for i in range(101):
    u=F(i,100);h=de_boor(U,H,2,u);assert h[-1]==3*(u-F(1,2))**2+F(1,4)>=F(1,4)
    R=tuple(w*b/h[-1] for w,b in zip(W,((1-u)**2,2*u*(1-u),u*u)))
    assert sum(R)==1 and R[0]>=0 and R[1]<=0 and R[2]>=0
    assert project(h)==tuple(sum(r*p[d] for r,p in zip(R,P)) for d in range(2))
    assert abs(float(sum(x*x for x in project(h))-1))<1e-38
assert project(de_boor(U,H,2,F(1,2)))==(F(0),-F(1))
def R(i,u):return W[i]*((1-u)**2,2*u*(1-u),u*u)[i]/evaluate(Z,u)
assert R(0,F(1,3))==R(2,F(2,3))==F(4,3) and R(1,F(1,2))==-1
lines=['% Exact Ex7.4, W1,-1/2,1,a=sqrt3/2; long circular arc traversed clockwise240deg.',
       '% W=3(u-1/2)^2+1/4, exact circle polynomial and negative orientation certified.',
       r'\begin{tikzpicture}[book line,x=4cm,y=4cm]',r'\path[use as bounding box] (-1.6,-1.75) rectangle (1.8,2.6);',
       r'\draw[book axis,book grid] (-1.4,0)--(1.5,0) node[right=4pt] {$x$};',
       r'\draw[book axis,book grid] (0,-1.35)--(0,2.35) node[above=4pt] {$y$};',
       r'\draw[book grid] '+'--'.join(map(point,P))+';']
for i in range(1,40):
    C=project(de_boor(U,H,2,F(i,40)));lines += [r'\begin{scope}[shift={'+point(C)+'}]',r'\draw (-1.5pt,0)--(1.5pt,0) (0,-1.5pt)--(0,1.5pt);',r'\end{scope}']
for i,(p,anchor) in enumerate(zip(P,('above right','above right','above left'))):
    lines.append(r'\draw '+point(p)+r' circle[radius=2pt] node['+anchor+r'=7pt] {$\mathbf P_'+str(i)+'$};')
lines += [r'\node at (0,-1.55) {(a)};',r'\end{tikzpicture}']
(root/'image_tex/ch07/fig_7_20.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
basis,proofs=graphs(U,W,height=F(3),allow_signed=True)
lines=['% Signed rational bases: R0/R2 attain4/3, R1 attains-1; sum remains1.',
       r'\begin{tikzpicture}[book line]',r'\path[use as bounding box] (-.6,-5) rectangle (13.1,5.4);',
       r'\draw[book axis] (-.1,0)--(12.7,0) node[right=4pt] {$u$};',
       r'\draw[book axis] (0,-3.6)--(0,4.9);',r'\node[left=5pt] at (0,3) {$1$};',
       r'\node[left=5pt] at (0,-3) {$-1$};']+basis
lines += [r'\node[above=7pt] at (4,4) {$R_{0,2}$};',r'\node[above=7pt] at (8,4) {$R_{2,2}$};',
          r'\node[below=8pt] at (6,-3) {$R_{1,2}$};']
for u,label in [(F(0),'0'),(F(1),'1')]:
    for k in range(3):
        x=12*u+F(7,100)*(k-1);lines.append(r'\draw[book grid] '+point((x,-F(1,10)))+'--'+point((x,F(1,10)))+';')
    anchor='below left' if u==0 else 'below'
    lines.append(r'\node['+anchor+r'=6pt] at '+point((12*u,-F(1,10)))+' {$'+label+'$};')
lines += [r'\node at (6,-4.55) {(b)};',r'\end{tikzpicture}']
(root/'image_tex/ch07/fig_7_21.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/negative-circle-arc-check.json').write_text(json.dumps({'figure':'7.18','weights':list(map(str,W)),'a_enclosure':list(map(str,(lo,hi))),'circle_polynomial_identity_coefficients':list(map(str,identity)),'global_denominator_lower_bound':'1/4','clockwise_angular_derivative_certificate':'C cross Cprime=-2*a/W<0','endpoints_angles_degrees':[30,150],'passes_lower_midpoint':[0,-1],'sweep_degrees_clockwise':240,'native_checks':nativechecks,'exact_signed_partition_curve_checks':101,'basis_extrema':{'R0_at_one_third':'4/3','R2_at_two_thirds':'4/3','R1_at_one_half':'-1'},'marker_grid':'u=i/40,i=0..40','native_basis_graph_certificates':proofs},indent=2)+'\n')
print('PASS:exact240deg circle/orientation certificate,W>=1/4,101signed partitions; extrema4/3,-1;3certified signed rational graphs.')

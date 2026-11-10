"""7.17: prescribed triangular full circle and its seven rational basis functions."""
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
for name in ('fig_7_18.tex','fig_7_19.tex'):
    assert not next(e for e in manifest['images'] if e['tex']=='image_tex/ch07/'+name)['applied']
U=(F(0),)*3+(F(1,3),)*2+(F(2,3),)*2+(F(1),)*3
W=(F(1),F(1,2),F(1),F(1,2),F(1),F(1,2),F(1))
scaledP=tuple((F(x),F(y)) for x,y in [(1,F(1,2)),(0,2),(-1,F(1,2)),(-2,-1),(0,-1),(2,-1),(1,F(1,2))])
HS=tuple(tuple(w*x for x in pt)+(w,) for pt,w in zip(scaledP,W));scaledpieces=segments(U,HS,2)
certificates=[]
for s in scaledpieces:
    X,Y,Z=s['power'];res=add(add(tuple(F(3,4)*x for x in multiply(X,X)),multiply(Y,Y)),tuple(-x for x in multiply(Z,Z)))
    assert all(x==0 for x in res);certificates.append({'interval':list(map(str,(s['a'],s['b']))),'circle_identity_coefficients':list(map(str,res))})
D=10**40;nn=isqrt(3*D*D);lo,hi=F(nn,2*D),F(nn+1,2*D);assert lo*lo<F(3,4)<hi*hi;a=(lo+hi)/2
P=tuple((a*x,y) for x,y in scaledP);H=tuple(tuple(w*x for x in pt)+(w,) for pt,w in zip(P,W))
ss=segments(U,H,2);nativechecks=check(U,H,2,ss)+check(U,HS,2,scaledpieces)
def tangent(s,u):
    h=tuple(evaluate(c,u) for c in s['power']);d=tuple(evaluate(derivative(c),u) for c in s['power'])
    return tuple((d[k]*h[-1]-h[k]*d[-1])/h[-1]**2 for k in range(2))
joins=[]
for l,r in zip(ss,ss[1:]):
    u=l['b'];assert tangent(l,u)==tangent(r,u)
    dl=evaluate(derivative(l['power'][-1]),u);dr=evaluate(derivative(r['power'][-1]),u);assert dl!=dr
    joins.append({'u':str(u),'projected_C1':True,'homogeneous_weight_derivative_jump':str(dr-dl)})
assert tangent(ss[-1],F(1))==tangent(ss[0],F(0))
for i in range(301):
    u=F(i,300);h=de_boor(U,H,2,u);R=[de_boor(U,tuple((w*F(k==j),) for k,w in enumerate(W)),2,u)[0]/h[-1] for j in range(7)]
    assert min(R)>=0 and sum(R)==1 and project(h)==tuple(sum(r*p[d] for r,p in zip(R,P)) for d in range(2))
    assert abs(float(sum(x*x for x in project(h))-1))<1e-38
lines=['% Exact Ex7.3 triangle controls with a=cos30=sqrt3/2; enclosure width<1e-40.',
       '% Circle identity checked coefficientwise on all3spans using3/4*(X/a)^2+Y^2=W^2.',
       '% XY4cm matches physical unit-circle scale of Fig7.16; actual u=i/60 sample markers.',
       r'\begin{tikzpicture}[book line,x=4cm,y=4cm]',r'\path[use as bounding box] (-2.3,-1.75) rectangle (2.5,2.6);',
       r'\draw[book axis,book grid] (-2.1,0)--(2.15,0) node[right=4pt] {$x$};',
       r'\draw[book axis,book grid] (0,-1.35)--(0,2.35) node[above=4pt] {$y$};',
       r'\draw[book grid] '+'--'.join(map(point,P))+';']
for i in range(60):
    if i%20==0:continue
    C=project(de_boor(U,H,2,F(i,60)));lines += [r'\begin{scope}[shift={'+point(C)+'}]',r'\draw (-1.5pt,0)--(1.5pt,0) (0,-1.5pt)--(0,1.5pt);',r'\end{scope}']
for i,(p,anchor) in enumerate(zip(P[:6],('above right','above right','above left','below left','below right','below right'))):
    label=r'\mathbf P_0=\mathbf P_6' if i==0 else r'\mathbf P_'+str(i)
    lines.append(r'\draw '+point(p)+r' circle[radius=2pt] node['+anchor+r'=7pt] {$'+label+'$};')
lines += [r'\node at (0,-1.55) {(a)};',r'\end{tikzpicture}']
(root/'image_tex/ch07/fig_7_18.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
basis,proofs=graphs(U,W)
lines=['% Same seven exact rational basis functions as Ex7.3 triangular circle.',
       r'\begin{tikzpicture}[book line]',r'\path[use as bounding box] (-.6,-1.9) rectangle (13.1,5.1);',
       r'\draw[book axis] (-.1,0)--(12.7,0) node[right=4pt] {$u$};',
       r'\draw[book axis] (0,0)--(0,4.7);',r'\node[left=5pt] at (0,4) {$1$};']+basis
for i in range(7):
    u=F(i,6);v=F(1,3) if i%2 else F(1);anchor='above right' if i==0 else 'above left' if i==6 else 'above';gap=20 if i%2 else 6
    lines.append(r'\node['+anchor+'='+str(gap)+'pt] at '+point((12*u,4*v))+' {$R_{'+str(i)+r',2}$};')
for u,label,m in [(F(0),'0',3),(F(1,3),r'\tfrac13',2),(F(2,3),r'\tfrac23',2),(F(1),'1',3)]:
    for k in range(m):
        x=12*u+F(7,100)*(F(k)-F(m-1,2));lines.append(r'\draw[book grid] '+point((x,-F(1,10)))+'--'+point((x,F(1,10)))+';')
    lines.append(r'\node[below=6pt] at '+point((12*u,-F(1,10)))+' {$'+label+'$};')
lines += [r'\node at (6,-1.55) {(b)};',r'\end{tikzpicture}']
(root/'image_tex/ch07/fig_7_19.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/seven-point-circle-check.json').write_text(json.dumps({'figure':'7.17','knots':list(map(str,U)),'weights':list(map(str,W)),'controls_x_as_multiple_of_a_and_y':[[str(x) for x in p] for p in scaledP],'a_enclosure':list(map(str,(lo,hi))),'root_enclosure_projected_L1_error_bound':str(2*(hi-lo)),'exact_circle_polynomial_certificates':certificates,'native_checks':nativechecks,'exact_partition_and_curve_basis_checks':301,'C1_joins':joins,'closed_C1_join_verified':True,'parameter_marker_grid':'u=i/60,i=0..59; knot markers shared with control circles','physical_coordinate_scale_cm':4,'native_basis_graph_certificates':proofs},indent=2)+'\n')
print('PASS:all3exact algebraic circle coefficients;301partition/curve checks;C1closure;7certified native rational bases;same physical circle scale as7.16.')

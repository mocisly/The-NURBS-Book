"""7.16: given nine-point circle, uniform-parameter markers and certified rational bases."""
from pathlib import Path
from fractions import Fraction as F
from math import isqrt
import json
from native_bspline import segments,check,de_boor,point
from rational_geometry import project
from bspline_math import derivative,evaluate
from native_rational_basis import graphs

root=Path(__file__).resolve().parents[1];manifest=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
for name in ('fig_7_16.tex','fig_7_17.tex'):
    assert not next(e for e in manifest['images'] if e['tex']=='image_tex/ch07/'+name)['applied']
# Exact algebraic circle certificate in Q[w]/(w^2-1/2), independent of rendering.
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def mul(a,b):return (a[0]*b[0]+a[1]*b[1]/2,a[0]*b[1]+a[1]*b[0])
def product(A,B):
    C=[(F(0),F(0)) for _ in range(len(A)+len(B)-1)]
    for i,a in enumerate(A):
        for j,b in enumerate(B):C[i+j]=add(C[i+j],mul(a,b))
    return C
XX=[(F(1),F(0)),(-F(2),F(2)),(F(1),-F(2))]
YY=[(F(0),F(0)),(F(0),F(2)),(F(1),-F(2))]
WW=[(F(1),F(0)),(-F(2),F(2)),(F(2),-F(2))]
assert all(add(add(x,y),tuple(-z for z in w))==(0,0) for x,y,w in zip(product(XX,XX),product(YY,YY),product(WW,WW)))
D=10**40;nn=isqrt(2*D*D);lo,hi=F(nn,2*D),F(nn+1,2*D);assert lo*lo<F(1,2)<hi*hi;w=(lo+hi)/2
U=(F(0),)*3+(F(1,4),)*2+(F(1,2),)*2+(F(3,4),)*2+(F(1),)*3
P=tuple(tuple(map(F,p)) for p in [(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1),(1,0)])
W=tuple(w if i%2 else F(1) for i in range(9));H=tuple(tuple(ww*x for x in p)+(ww,) for p,ww in zip(P,W))
ss=segments(U,H,2);nativechecks=check(U,H,2,ss)
def tangent(s,u):
    A=tuple(evaluate(c,u) for c in s['power']);d=tuple(evaluate(derivative(c),u) for c in s['power'])
    return tuple((d[k]*A[-1]-A[k]*d[-1])/A[-1]**2 for k in range(2))
joins=[]
for a,b in zip(ss,ss[1:]):
    u=a['b'];assert tangent(a,u)==tangent(b,u)
    dl=evaluate(derivative(a['power'][-1]),u);dr=evaluate(derivative(b['power'][-1]),u);assert dl!=dr
    joins.append({'u':str(u),'dehomogenized_derivatives_equal':True,'homogeneous_weight_derivative_jump':str(dr-dl)})
assert tangent(ss[-1],F(1))==tangent(ss[0],F(0))
for i in range(401):
    u=F(i,400);h=de_boor(U,H,2,u);weights=[]
    for j in range(9):weights.append(de_boor(U,tuple((ww*F(k==j),) for k,ww in enumerate(W)),2,u)[0]/h[-1])
    assert min(weights)>=0 and sum(weights)==1
    assert project(h)==tuple(sum(v*p[d] for v,p in zip(weights,P)) for d in range(2))
    assert abs(float(sum(x*x for x in project(h))-1))<1e-38
lines=['% Exact Ex7.2 controls/knots; w=sqrt2/2 enclosed to<1e-40 for native coordinates.',
       '% Plus markers are actual uniform B-spline parameter u=i/80; no circle-angle sampling.',
       r'\begin{tikzpicture}[book line,x=4cm,y=4cm]',r'\path[use as bounding box] (-1.6,-1.7) rectangle (1.8,1.7);',
       r'\draw[book axis,book grid] (-1.4,0)--(1.5,0) node[right=4pt] {$x$};',
       r'\draw[book axis,book grid] (0,-1.35)--(0,1.45) node[above=4pt] {$y$};',
       r'\draw[book grid] '+'--'.join(map(point,P))+';']
for i in range(80):
    if i%20==0:continue
    C=project(de_boor(U,H,2,F(i,80)));lines += [r'\begin{scope}[shift={'+point(C)+'}]',r'\draw (-1.5pt,0)--(1.5pt,0) (0,-1.5pt)--(0,1.5pt);',r'\end{scope}']
anchors=['below right','above right','above right','above left','above left','below left','below right','below right']
for i,(p,anchor) in enumerate(zip(P[:8],anchors)):
    label=r'\mathbf P_0=\mathbf P_8' if i==0 else r'\mathbf P_'+str(i)
    lines.append(r'\draw '+point(p)+r' circle[radius=2pt] node['+anchor+r'=7pt] {$'+label+'$};')
lines += [r'\node at (0,-1.55) {(a)};',r'\end{tikzpicture}']
(root/'image_tex/ch07/fig_7_16.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
basis,proofs=graphs(U,W)
lines=['% Same exact rational basis R_i,2 as circle panel; certified native graph geometry.',
       r'\begin{tikzpicture}[book line]',r'\path[use as bounding box] (-.6,-1.9) rectangle (13.1,5.1);',
       r'\draw[book axis] (-.1,0)--(12.7,0) node[right=4pt] {$u$};',
       r'\draw[book axis] (0,0)--(0,4.7);',r'\node[left=5pt] at (0,4) {$1$};']+basis
for i in range(9):
    u=F(i,8);v=w/(1+w) if i%2 else F(1);anchor='above right' if i==0 else 'above left' if i==8 else 'above'
    lines.append(r'\node['+anchor+r'=6pt] at '+point((12*u,4*v))+' {$R_{'+str(i)+r',2}$};')
for u,label,m in [(F(0),'0',3),(F(1,4),r'\tfrac14',2),(F(1,2),r'\tfrac12',2),(F(3,4),r'\tfrac34',2),(F(1),'1',3)]:
    for k in range(m):
        x=12*u+F(7,100)*(F(k)-F(m-1,2));lines.append(r'\draw[book grid] '+point((x,-F(1,10)))+'--'+point((x,F(1,10)))+';')
    lines.append(r'\node[below=6pt] at '+point((12*u,-F(1,10)))+' {$'+label+'$};')
lines += [r'\node at (6,-1.55) {(b)};',r'\end{tikzpicture}']
(root/'image_tex/ch07/fig_7_17.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/nine-point-circle-check.json').write_text(json.dumps({'figure':'7.16','given_controls':[[str(x) for x in p] for p in P],'knots':list(map(str,U)),'exact_algebraic_circle_identity_w_squared':'1/2','weight_enclosure':list(map(str,(lo,hi))),'projected_L1_weight_enclosure_error_bound':str(6*(hi-lo)),'native_checks':nativechecks,'exact_partition_and_curve_basis_checks':401,'C1_joins':joins,'closed_C1_join_verified':True,'marker_parameter_grid':'u=i/80,i=0..79; knot markers shared with control circles','native_basis_graph_certificates':proofs},indent=2)+'\n')
print('PASS:exact algebraic circle identity;401partition/curve checks;C1closed joins with nonC1 homogeneous weight;9certified rational basis graphs.')

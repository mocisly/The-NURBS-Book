"""7.28: recover a full nine-control ellipse from a given rational Bezier arc."""
from pathlib import Path
from fractions import Fraction as F
from math import isqrt
import json
from native_bspline import segments,check,de_boor,cubic_path,point
from rational_geometry import approximate,evaluate,project
from polynomial_native import multiply
from bspline_math import add,compose_affine,derivative,evaluate as polyvalue
root=Path(__file__).resolve().parents[1];d=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in d['images'] if e['tex']=='image_tex/ch07/fig_7_36.tex')['applied']
P=((F(12,5),F(8,5)),(-F(28,15),F(16,5)),(-F(468,125),F(88,125)));w=F(3,5)
H=tuple(tuple(ww*x for x in p)+(ww,) for p,ww in zip(P,(F(1),w,F(1))))
S=tuple(x-y for x,y in zip(P[0],P[1]));T=tuple(x-y for x,y in zip(P[2],P[1]));k=1/(w*w);eps=k/(2*(k-1))
center=tuple(p+eps*(s+t) for p,s,t in zip(P[1],S,T));assert center==(0,0)
given=segments((F(0),)*3+(F(1),)*3,H,2)[0];X,Y,Z=given['power'];res=add(add(tuple(x/16 for x in multiply(X,X)),tuple(y/4 for y in multiply(Y,Y))),tuple(-x for x in multiply(Z,Z)));assert all(x==0 for x in res)
Q=tuple(tuple(map(F,q)) for q in [(4,0),(4,2),(0,2),(-4,2),(-4,0),(-4,-2),(0,-2),(4,-2),(4,0)])
# These are precisely the geometric control formulas in the preceding section.
C=(F(0),F(0));A=(F(4),F(0));B=(F(0),F(2))
assert Q==(A,tuple(x+y for x,y in zip(A,B)),B,tuple(y-x for x,y in zip(A,B)),tuple(-x for x in A),tuple(-x-y for x,y in zip(A,B)),tuple(-y for y in B),tuple(x-y for x,y in zip(A,B)),A)
D=10**40;n=isqrt(2*D*D);lo,hi=F(n,2*D),F(n+1,2*D);assert lo*lo<F(1,2)<hi*hi;ww=(lo+hi)/2
W=tuple(ww if i%2 else F(1) for i in range(9));HQ=tuple(tuple(a*x for x in q)+(a,) for q,a in zip(Q,W));U=(F(0),)*3+(F(1,4),)*2+(F(1,2),)*2+(F(3,4),)*2+(F(1),)*3
ss=segments(U,HQ,2);nc=check(U,HQ,2,ss);bounds=[];paths=[]
for s in ss:
    X,Y,Z=s['power'];res=add(add(tuple(x/16 for x in multiply(X,X)),tuple(y/4 for y in multiply(Y,Y))),tuple(-x for x in multiply(Z,Z)))
    bound=sum(map(abs,compose_affine(res,s['a'],s['b']-s['a'])))/ww**2;assert bound<F(1,10**38);bounds.append(str(bound));paths+=approximate(s['bern'],F(1,200000))
def velocity(s,u):
    h=[polyvalue(p,u) for p in s['power']];dh=[polyvalue(derivative(p),u) for p in s['power']]
    return tuple((dh[k]*h[-1]-h[k]*dh[-1])/h[-1]**2 for k in range(2))
for l,r in zip(ss,ss[1:]):assert velocity(l,l['b'])==velocity(r,r['a'])
assert velocity(ss[-1],F(1))==velocity(ss[0],F(0))
for i in range(401):
    u=F(i,400);h=de_boor(U,HQ,2,u);x,y=project(h);assert abs(x*x/16+y*y/4-1)<F(1,10**38)
    R=[de_boor(U,tuple((a*F(j==k),) for j,a in enumerate(W)),2,u)[0]/h[-1] for k in range(9)];assert min(R)>=0 and sum(R)==1
    p=project(evaluate(H,u));assert p[0]*p[0]/16+p[1]*p[1]/4==1
originalpaths=approximate(H,F(1,200000))
lines=['% Exact given arc: P0(12/5,8/5),P1(-28/15,16/5),P2(-468/125,88/125),w1=3/5.',
       '% x^2/16+y^2/4=1, recovered center0, radii4/2. New nine-control NURBS dashed; given arc solid.',
       r'\begin{tikzpicture}[book line,x=1.7cm,y=1.7cm]',r'\path[use as bounding box] (-5,-3) rectangle (5.2,4.2);',
       r'\draw[book grid] '+'--'.join(map(point,Q))+';',r'\draw[book grid,dashed] '+'--'.join(map(point,P))+';']
lines.extend(cubic_path(s,'dashed') for s in paths);lines.extend(cubic_path(s) for s in originalpaths)
for i,(q,anchor) in enumerate(zip(Q[:8],['right','above right','above','above left','left','below left','below','below right'])):
    text=r'\mathbf Q_0=\mathbf Q_8' if i==0 else r'\mathbf Q_'+str(i)
    lines.append(r'\draw '+point(q)+r' circle[radius=2pt] node['+anchor+r'=7pt] {$'+text+'$};')
for i,(p,anchor) in enumerate(zip(P,['below left','above','below right'])):lines.append(r'\draw '+point(p)+r' circle[radius=2pt] node['+anchor+r'=7pt] {$\mathbf P_'+str(i)+'$};')
lines.append(r'\end{tikzpicture}');(root/'image_tex/ch07/fig_7_36.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/complete-ellipse-check.json').write_text(json.dumps({'figure':'7.28','given_controls':[[str(x) for x in p] for p in P],'given_weight':str(w),'recovered_center':list(map(str,center)),'principal_radii':['4','2'],'exact_given_ellipse_polynomial_identity':True,'nine_controls':[[str(x) for x in q] for q in Q],'weight_enclosure':list(map(str,(lo,hi))),'native_checks':nc,'curve_basis_partition_and_given_ellipse_checks':401,'whole_span_implicit_residual_bounds':bounds,'exact_projected_C1_joins_and_closure_for_enclosed_weight':True,'native_L1_error':str(max(s['certified_l1_error'] for s in paths+originalpaths))},indent=2)+'\n')
print('PASS:exact given ellipse and recovered center/radii,9geometric controls,401ellipse/partition checks,C1closure and whole-span residual<1e-38.')

"""Fig3.26: exact polynomial bicubic surface and five genuine partial vectors."""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations
from math import comb,prod
import json
from native_bspline import segments,check,cubic_path,point
from surface_geometry import verify_tensor,surface,isocurve

root=Path(__file__).resolve().parents[1]
target=root/'image_tex/ch03/fig_3_28.tex';assert not target.exists()
K=(F(0),)*4+(F(1,2),)+(F(1),)*4
def add(*ps):
    r={}
    for p in ps:
        for k,v in p.items():r[k]=r.get(k,F(0))+v
    return {k:v for k,v in r.items() if v}
def scale(p,c):return {k:v*c for k,v in p.items()}
def mul(a,b):
    r={}
    for (i,j),v in a.items():
        for (k,l),w in b.items():r[i+k,j+l]=r.get((i+k,j+l),F(0))+v*w
    return r
def diff(p,axis):
    r={}
    for (i,j),c in p.items():
        n=(i,j)[axis]
        if n:r[(i-1,j) if axis==0 else (i,j-1)]=n*c
    return r
def ev(p,u,v):return sum(c*u**i*v**j for (i,j),c in p.items())
u={(1,0):F(1)};v={(0,1):F(1)}
a=add(u,{(0,0):F(-3,4)});b=add(v,{(0,0):F(-2,5)})
c=add(v,{(0,0):F(-1,2)})
polys=(add({(0,0):F(2)},scale(v,-4),scale(mul(a,a),-1),scale(mul(a,b),-1)),
       add({(0,0):F(-2)},scale(u,4),mul(a,a),scale(mul(a,b),2),scale(mul(b,b),F(-1,2))),
       add({(0,0):F(2)},scale(u,6),scale(mul(u,u),-12),scale(mul(mul(u,u),u),F(20,3)),scale(mul(c,c),-6),scale(mul(a,b),-6)))
def monomial_control(i,r):
    if r==0:return F(1)
    return sum(prod(t,start=F(1)) for t in combinations(K[i+1:i+4],r))/comb(3,r)
M=tuple(tuple(monomial_control(i,r) for r in range(4)) for i in range(5))
P=tuple(tuple(tuple(sum(co*M[i][a]*M[j][b] for (a,b),co in poly.items()) for poly in polys) for j in range(5)) for i in range(5))
tensor_checks=verify_tensor(K,K,3,3,P,10)
def derived_net(U,V,p,q,R,axis):
    if axis==0:
        Q=tuple(tuple(tuple(p*(R[i+1][j][d]-R[i][j][d])/(U[i+p+1]-U[i+1]) for d in range(3)) for j in range(len(R[0]))) for i in range(len(R)-1))
        return U[1:-1],V,p-1,q,Q
    Q=tuple(tuple(tuple(q*(R[i][j+1][d]-R[i][j][d])/(V[j+q+1]-V[j+1]) for d in range(3)) for j in range(len(R[0])-1)) for i in range(len(R)))
    return U,V[1:-1],p,q-1,Q
values={};partial_checks=0;u0,v0=F(3,4),F(2,5)
for au,av in ((0,0),(1,0),(0,1),(2,0),(1,1),(0,2)):
    net=(K,K,3,3,P);pp=polys
    for axis,n in ((0,au),(1,av)):
        for _ in range(n):net=derived_net(*net,axis);pp=tuple(diff(poly,axis) for poly in pp)
    for i in range(11):
        for j in range(11):
            uu,vv=F(i,10),F(j,10)
            assert surface(*net,uu,vv)==tuple(ev(poly,uu,vv) for poly in pp)
            partial_checks+=1
    values[au,av]=surface(*net,u0,v0)
uv=derived_net(*derived_net(K,K,3,3,P,0),1)
vu=derived_net(*derived_net(K,K,3,3,P,1),0)
assert uv==vu
assert values=={(0,0):(F(2,5),F(1),F(1001,400)),(1,0):(F(0),F(4),F(-3,4)),
                (0,1):(F(-4),F(0),F(6,5)),(2,0):(F(-2),F(2),F(6)),
                (1,1):(F(-1),F(2),F(-6)),(0,2):(F(0),F(-1),F(-12))}
lines=['% Printed Fig3.26: representative polynomial bicubic in the stated simple-half-knot space.',
       '% Coefficients obtained by the exact monomial blossom, independently checked by recursive derivative nets.',
       '% Evaluation at(u,v)=(3/4,2/5); all five arrows are exactly one-half of the actual partial vector.',
       '% Exact native cubic isocurves; no contour conversion.',
       r'\begin{tikzpicture}[x={(-.9cm,-.6cm)},y={(1cm,-.35cm)},z={(0cm,1cm)},book line]',
       r'\path[use as bounding box] (canvas cs:x=-5.6cm,y=-5.5cm) rectangle (canvas cs:x=6.7cm,y=7.1cm);',
       r'\draw[book axis] (0,0,0)--(4.3,0,0) node[below left=4pt] {$x$};',
       r'\draw[book axis] (0,0,0)--(0,5.6,0) node[right=4pt] {$y$};',
       r'\draw[book axis] (0,0,0)--(0,0,6.4) node[above=4pt] {$z$};']
curves=0
for variable in ('u','v'):
    for h in range(6):
        t=F(h,5)
        if variable=='u' and t==v0:continue
        k,d,c=isocurve(K,K,3,3,P,variable,t);segs=segments(k,c,d);curves+=check(k,c,d,segs)
        for seg in segs:lines.append(cubic_path(seg,'book line' if h in (0,5) else 'book grid'))
for variable,fixed in [('u',v0),('v',u0)]:
    k,d,c=isocurve(K,K,3,3,P,variable,fixed);segs=segments(k,c,d);curves+=check(k,c,d,segs)
    for seg in segs:lines.append(cubic_path(seg,'book line,dashed'))
origin=values[0,0]
for key,anchor,label in [((1,0),'right',r'\mathbf S_u'),((0,1),'right',r'\mathbf S_v'),
                         ((2,0),'above right',r'\mathbf S_{uu}'),((1,1),'below right',r'\mathbf S_{uv}'),
                         ((0,2),'below left',r'\mathbf S_{vv}')]:
    end=tuple(origin[d]+values[key][d]/2 for d in range(3))
    lines.extend([r'\draw[book axis] '+point(origin)+'--'+point(end)+';',
                  r'\node['+anchor+'=5pt] at '+point(end)+' {$'+label+'$};'])
lines.append(r'\fill '+point(origin)+' circle[radius=1.6pt];')
for uu,vv,label,anchor,pos in [(u0,F(0),r'u=\frac34','left',r'(canvas cs:x=-2.2cm,y=.4cm)'),
                               (F(1),v0,r'v=\frac25','right',r'(canvas cs:x=4.1cm,y=1.7cm)')]:
    lines.append(r'\draw[book grid] '+point(surface(K,K,3,3,P,uu,vv))+'--'+pos+' node['+anchor+'=4pt] {$'+label+'$};')
lines.append(r'\end{tikzpicture}')
target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/surface-derivatives-check.json').write_text(json.dumps({
    'figure':'3.26','representative_polynomial_surface':True,'degrees':[3,3],'control_count':[5,5],
    'U_and_V':list(map(str,K)),'tensor_vs_nested_deboor_points':tensor_checks,
    'recursive_partial_vs_independent_polynomial_points':partial_checks,'mixed_derivative_nets_commute':True,
    'exact_isocurve_checks':curves,'parameter':['3/4','2/5'],'arrow_display_scale':'1/2',
    'polynomials':[{f'{i},{j}':str(c) for (i,j),c in poly.items()} for poly in polys],
    'point_and_partials':{f'{a},{b}':list(map(str,val)) for (a,b),val in values.items()}},indent=2)+'\n')
print(f'PASS:{tensor_checks} tensor points,{partial_checks} exact polynomial/recursive partial comparisons,{curves} curve checks; mixed nets commute and five half-scale arrows verified.')

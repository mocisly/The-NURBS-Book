"""11.31 actual parabolic radial bending, verified removal of two inflections."""
from pathlib import Path
from fractions import Fraction as F
from math import comb
import json
from circular_bending_data import sqrtq,sub,dot
from knot51_data import insert
from native_bspline import segments,check,cubic_path,point,de_boor
from bspline_math import derivative,evaluate,compose_affine
root=Path(__file__).resolve().parents[1];U=(F(0),)*4+tuple(F(i,8)for i in range(1,8))+(F(1),)*4;G=tuple(sum(U[i+1:i+4])/3 for i in range(11));P=tuple((8*u-4,F(y))for u,y in zip(G,('0','.8','1.5','2','1.5','1','1.5','2','1.5','.8','0')));us,ue=F(1,8),F(7,8);old=segments(U,P,3);roots=[]
for s in old:
    d=derivative(derivative(s['power'][1]));assert len(d)<=2
    if len(d)==2 and d[1]:
        t=-d[0]/d[1]
        if s['a']<=t<=s['b'] and 0<t<1:roots.append(t)
roots=sorted(set(roots))
assert len(roots)==2,roots
K,Q=U,P
for _ in range(2):
    mids=tuple((a+b)/2 for a,b in zip(K,K[1:])if a<b)
    for t in mids:K,Q,_=insert(K,Q,3,t)
O=(F(0),F(5));ids=tuple(i for i in range(len(Q))if K[i]>=us and K[i+4]<=ue);R=list(Q);rays=[]
for i in ids:
    x,y=sub(Q[i],O);a=x*x/8;b=y;c=F(2);D=b*b-4*a*c;assert D>=0;s=4/(-b+sqrtq(D)) if a else -c/b;R[i]=tuple(o+s*d for o,d in zip(O,(x,y)));residual=abs(R[i][1]-(3-R[i][0]**2/8));assert residual<F(1,10**13);rays.append(dict(index=i,s=s,t=s,intersection=R[i],parabola_residual=residual))
for boundary,neighbor,indices in[(ids[0],ids[0]+1,range(ids[0])),(ids[-1],ids[-1]-1,range(ids[-1]+1,len(Q)))]:
    a=sub(Q[neighbor],Q[boundary]);b=sub(R[neighbor],R[boundary]);den=sqrtq(dot(a,a)*dot(b,b));cs=dot(a,b)/den;sn=(a[0]*b[1]-a[1]*b[0])/den;assert abs(cs*cs+sn*sn-1)<F(1,10**12)
    for i in indices:
        x,y=sub(Q[i],Q[boundary]);R[i]=(R[boundary][0]+cs*x-sn*y,R[boundary][1]+sn*x+cs*y)
R=tuple(R)
def mul(a,b):
    c=[F(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):c[i+j]+=x*y
    return tuple(c)
def determinant(s):
    x,y=s['power'];a,b=mul(derivative(x),derivative(derivative(y))),mul(derivative(y),derivative(derivative(x)));n=max(len(a),len(b));return tuple((a[i]if i<len(a)else 0)-(b[i]if i<len(b)else 0)for i in range(n))
def negative_certificate(poly,a,b,depth=0):
    q=compose_affine(poly,a,b-a);n=len(q)-1;B=tuple(sum(q[k]*F(comb(i,k),comb(n,k))for k in range(i+1))for i in range(n+1))
    if max(B)<0:return 1
    assert depth<16,(float(a),float(b),list(map(float,B)))
    return negative_certificate(poly,a,(a+b)/2,depth+1)+negative_certificate(poly,(a+b)/2,b,depth+1)
ss=segments(K,R,3);certificates=sum(negative_certificate(determinant(s),s['a'],s['b'])for s in ss);assert all(min(s['bern'][i+1][0]-s['bern'][i][0]for i in range(3))>0 for s in ss)
nc=check(K,Q,3,segments(K,Q,3),steps=3)+check(K,R,3,ss,steps=3);xmin=min(p[0]for p in R+Q)-F(3,5);xmax=max(p[0]for p in R+Q)+F(3,5);ymin=min(p[1]for p in R+Q)-F(3,5)
lines=['% Real local lambda1 bending to parabola, with rigid exterior adjustment and whole curvature sign proof.',r'\begin{tikzpicture}[book line,x=2cm,y=2cm,font=\fontsize{10}{12}\selectfont]',r'\path[use as bounding box] '+point((xmin,ymin))+' rectangle '+point((xmax,F(18,5)))+';',cubic_path(dict(bern=((-F(4),F(1)),(F(0),F(5)),(F(4),F(1)))),'book grid,dashed')]
lines.extend(cubic_path(s)for s in segments(U,P,3));lines.extend(cubic_path(s)for s in ss)
for t in(us,ue):lines.append(r'\draw '+point(de_boor(U,P,3,t))+r' rectangle ++(.035,.035);')
lines.extend([r'\node[below=8pt] at '+point(de_boor(U,P,3,F(1,2)))+r' {$C(u)$};',r'\node[above=9pt] at '+point(de_boor(K,R,3,F(1,2)))+r' {$\widehat C(u)$};',r'\node[above right=6pt] at (4,1) {$B(w)$};',r'\end{tikzpicture}']);(root/'image_tex/ch11/fig_11_37.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8');(root/'image_tex/build/parabolic-inflection-bending-check.json').write_text(json.dumps(dict(knots=U,original_controls=P,original_inflection_parameters=roots,refined_knots=K,refined_controls=Q,modified_controls=R,interval=(us,ue),origin=O,bending_curve='y=3-x^2/8',lambda_value=1,ray_intersections=rays,strictly_negative_whole_curvature_Bernstein_certificates=certificates,mapped_curve_x_strictly_increasing=True,no_inflections_after_bending=True,native_checks=nc,no_contour_tracing=True),default=str,indent=2)+'\n',encoding='utf-8');print('PASS11.31',nc,'nativechecks;2exactoldinflections->0,',certificates,'strict wholecurvature certificates.')

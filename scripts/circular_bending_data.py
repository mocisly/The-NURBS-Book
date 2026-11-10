"""Actual Eq11.56-58 radial bending and rigid exterior-control repositioning."""
from fractions import Fraction as F
from decimal import Decimal,localcontext
from knot51_data import insert
from native_bspline import segments
def sqrtq(x):
    with localcontext()as c:
        c.prec=50;return F(str(round((Decimal(x.numerator)/Decimal(x.denominator)).sqrt(),18)))
U=(F(0),)*4+(F(1),)*4;P=((-F(4),-F(1)),(-F(4,3),F(1,3)),(F(4,3),F(1,3)),(F(4),-F(1)))
for t in(F(i,8)for i in range(1,8)):U,P,_=insert(U,P,3,t)
US,UE=F(1,4),F(3,4)
for _ in range(3):
    mid=tuple((a+b)/2 for a,b in zip(U,U[1:])if US<=a<b<=UE)
    for t in mid:U,P,_=insert(U,P,3,t)
IDS=tuple(i for i in range(len(P))if U[i]>=US and U[i+4]<=UE)
C=(F(0),F(3));RADIUS=F(2)
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def bend(lam,origin=C):
    assert dot(sub(origin,C),sub(origin,C))<RADIUS**2
    Q=list(P);proof=[]
    for i in IDS:
        d=sub(P[i],origin);o=sub(origin,C);a=dot(d,d);b=2*dot(o,d);c=dot(o,o)-RADIUS**2;s=(-b+sqrtq(b*b-4*a*c))/(2*a);t=lam*s/(1+(lam-1)*s);R=tuple(x+s*y for x,y in zip(origin,d));Q[i]=tuple(x+t*y for x,y in zip(origin,d));residual=abs(dot(sub(R,C),sub(R,C))-RADIUS**2)
        assert residual<F(1,10**14) and t*(1-s)/(s*(1-t))==lam
        proof.append(dict(index=i,s=s,t=t,R=R,circle_residual=residual))
    rigid=[]
    for boundary,neighbor,indices in[(IDS[0],IDS[0]+1,range(IDS[0])),(IDS[-1],IDS[-1]-1,range(IDS[-1]+1,len(P)))]:
        v=sub(P[neighbor],P[boundary]);w=sub(Q[neighbor],Q[boundary]);den=sqrtq(dot(v,v)*dot(w,w));cos=dot(v,w)/den;sin=(v[0]*w[1]-v[1]*w[0])/den
        assert abs(cos*cos+sin*sin-1)<F(1,10**12)
        for i in indices:
            x,y=sub(P[i],P[boundary]);Q[i]=(Q[boundary][0]+cos*x-sin*y,Q[boundary][1]+sin*x+cos*y)
        for i in indices:
            assert abs(dot(sub(Q[i],Q[boundary]),sub(Q[i],Q[boundary]))-dot(sub(P[i],P[boundary]),sub(P[i],P[boundary])))<F(1,10**10)
        rigid.append(dict(boundary=boundary,cos=cos,sin=sin,indices=list(indices)))
    return tuple(Q),dict(lambda_value=lam,origin=origin,circle_center=C,circle_radius=RADIUS,selected_indices=IDS,ray_crossratio_checks=proof,rigid_exterior_transforms=rigid,rigid_distance_squared_tolerance=F(1,10**10))

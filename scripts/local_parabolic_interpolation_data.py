"""Six representative data,five tangent intersections;exact G1andC1parameterizations9.20/21."""
from fractions import Fraction as F
from native_bspline import segments,check,de_boor
from inverse_knot_projection import remove_to
R=tuple(tuple(map(F,p)) for p in [('0','1.5'),('1.4','3.9'),('4.6','5'),('7.4','3.8'),('8.4','1.5')])
LAMBDA=tuple(map(F,['1/2','2/5','3/5','1/2']))
Q=((F(0),F(0)),)+tuple(tuple((1-l)*a+l*b for a,b in zip(A,B)) for A,B,l in zip(R,R[1:],LAMBDA))+((F('8.2'),F('.6')),)
FULL=(Q[0],)+tuple(t for i in range(5) for t in (R[i],Q[i+1]))
UNIFORM=tuple(F(i,5) for i in range(6))
def knots(params,repeated=True):return (F(0),)*3+tuple(x for t in params[1:-1] for x in ((t,t) if repeated else (t,)))+(F(1),)*3
UG=knots(UNIFORM)
increments=[F(1)]
for l in LAMBDA:increments.append(increments[-1]*(1-l)/l)
raw=(F(0),)+tuple(sum(increments[:i]) for i in range(1,6));C1PARAMS=tuple(x/raw[-1] for x in raw)
assert C1PARAMS==tuple(map(F,['0','2/11','4/11','7/11','9/11','1']))
UC_FULL=knots(C1PARAMS);UC,MINIMAL,REMOVAL=remove_to(UC_FULL,FULL,2,C1PARAMS[1:-1])
assert MINIMAL==(Q[0],)+R+(Q[-1],) and UC==knots(C1PARAMS,False)
for K,P,params in [(UG,FULL,UNIFORM),(UC_FULL,FULL,C1PARAMS),(UC,MINIMAL,C1PARAMS)]:
    ss=segments(K,P,2);check(K,P,2,ss)
    assert all(s['bern']==(Q[i],R[i],Q[i+1]) for i,s in enumerate(ss))
    assert all(de_boor(K,P,2,t)==q for t,q in zip(params,Q))
def cross(a,b):return a[0]*b[1]-a[1]*b[0]
DIRECTIONS=(tuple(b-a for a,b in zip(Q[0],R[0])),)+tuple(tuple(b-a for a,b in zip(A,B)) for A,B in zip(R,R[1:]))+(tuple(b-a for a,b in zip(R[-1],Q[-1])),)
INTERSECTIONS=[]
for i,(A,B) in enumerate(zip(Q,Q[1:])):
    ta,tb=DIRECTIONS[i:i+2];delta=tuple(b-a for a,b in zip(A,B));den=cross(ta,tb)
    a=cross(delta,tb)/den;b=cross(delta,ta)/den
    assert a>0 and b<0 and tuple(x+a*y for x,y in zip(A,ta))==R[i]==tuple(x+b*y for x,y in zip(B,tb))
    INTERSECTIONS.append((a,b))
for i in range(1,5):
    incoming=tuple(Q[i][j]-R[i-1][j] for j in range(2));outgoing=tuple(R[i][j]-Q[i][j] for j in range(2))
    assert cross(incoming,outgoing)==0 and sum(a*b for a,b in zip(incoming,outgoing))>0
    assert tuple(a/(C1PARAMS[i]-C1PARAMS[i-1]) for a in incoming)==tuple(b/(C1PARAMS[i+1]-C1PARAMS[i]) for b in outgoing)

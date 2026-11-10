"""Five representative data with specified unit tangents;Eq9.22/23 global Hermite solves."""
from fractions import Fraction as F
from math import isqrt
from inverse_knot_projection import solve
from surface_geometry import weights
from bspline_math import piece,derivative,evaluate
from native_bspline import segments,check,de_boor
Q=tuple(tuple(map(F,p)) for p in [('0','0'),('1','2.5'),('3','1'),('4','-.5'),('6','2')])
T=tuple(tuple(map(F,p)) for p in [('-3/5','4/5'),('1','0'),('0','-1'),('1','0'),('-3/5','4/5')])
assert all(sum(x*x for x in t)==1 for t in T)
squares=tuple(sum((b-a)**2 for a,b in zip(A,B)) for A,B in zip(Q,Q[1:]));scale=10**12
lo=tuple(F(isqrt(x.numerator*scale**2//x.denominator),scale) for x in squares);hi=tuple(x+F(1,scale) for x in lo)
assert all(a*a<=s<b*b for a,b,s in zip(lo,hi,squares))
TOTAL=sum(lo);PARAMS=(F(0),)+tuple(sum(lo[:i])/TOTAL for i in range(1,4))+(F(1),)
BOUNDS=tuple((sum(lo[:i])/sum(hi),sum(hi[:i])/sum(lo)) for i in range(1,4))
assert all(a<=t<=b and b-a<F(1,10**11) for t,(a,b) in zip(PARAMS[1:-1],BOUNDS))
def interpolate_all(p,alpha_scale=F(1)):
    assert p in (2,3)
    if p==2:
        internal=tuple(x for j in range(4) for x in ((PARAMS[j]+PARAMS[j+1])/2,PARAMS[j+1]) if x<1)
    else:
        internal=(PARAMS[1]/2,)+tuple(x for j in range(1,3) for x in ((2*PARAMS[j]+PARAMS[j+1])/3,(PARAMS[j]+2*PARAMS[j+1])/3))+((PARAMS[-2]+1)/2,)
    U=(F(0),)*(p+1)+internal+(F(1),)*(p+1);assert len(U)==10+p+1
    D=tuple(tuple(alpha_scale*TOTAL*x for x in t) for t in T)
    rows=[];rhs=[]
    for u,q,v in zip(PARAMS,Q,D):
        span=next((s for s in range(p,10) if U[s]<=u<U[s+1]),9)
        rows.extend([tuple(weights(U,p,u)),tuple(evaluate(derivative(piece(U,i,p,span)),u) for i in range(10))]);rhs.extend([q,v])
    P=solve(tuple(rows),tuple(rhs));ss=segments(U,P,p);nc=check(U,P,p,ss)
    assert all(de_boor(U,P,p,u)==q for u,q in zip(PARAMS,Q))
    for u,v in zip(PARAMS,D):
        seg=next((s for s in ss if s['a']<=u<s['b']),ss[-1])
        assert tuple(evaluate(derivative(c),u) for c in seg['power'])==v
    return U,P,D,ss,nc

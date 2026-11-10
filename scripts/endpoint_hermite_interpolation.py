"""Representative7point data and exact endpoint-derivative interpolation Eq9.9..12."""
from fractions import Fraction as F
from math import isqrt
from global_interpolation_data import solve,weights
from bspline_math import piece,derivative,evaluate
from native_bspline import segments,check,de_boor
Q=tuple(tuple(map(F,p)) for p in [('0','0'),('.4','1.4'),('2.4','2.1'),('3.8','.7'),('6','0'),('7.2','3.2'),('6','3.5')])
scale=10**12
squares=tuple(sum((b-a)**2 for a,b in zip(A,B)) for A,B in zip(Q,Q[1:]))
lo=tuple(F(isqrt(x.numerator*scale**2//x.denominator),scale) for x in squares)
hi=tuple(x+F(1,scale) for x in lo)
assert all(a*a<=s<b*b for a,b,s in zip(lo,hi,squares))
PARAMS=(F(0),)+tuple(sum(lo[:i])/sum(lo) for i in range(1,6))+(F(1),)
BOUNDS=tuple((sum(lo[:i])/sum(hi),sum(hi[:i])/sum(lo)) for i in range(1,6))
assert all(a<=t<=b and b-a<F(1,10**11) for t,(a,b) in zip(PARAMS[1:-1],BOUNDS))
U=(F(0),)*4+tuple(sum(PARAMS[j:j+3])/3 for j in range(5))+(F(1),)*4
ROWS=tuple(tuple(weights(U,3,t)) for t in PARAMS)+tuple(tuple(evaluate(derivative(piece(U,i,3,span)),u) for i in range(9)) for span,u in [(3,F(0)),(8,F(1))])
def interpolate_endpoints(D0,Dn):
    P=solve(ROWS,Q+(tuple(D0),tuple(Dn)));ss=segments(U,P,3);nc=check(U,P,3,ss)
    assert all(de_boor(U,P,3,t)==q for t,q in zip(PARAMS,Q))
    assert tuple(evaluate(derivative(c),F(0)) for c in ss[0]['power'])==tuple(D0)
    assert tuple(evaluate(derivative(c),F(1)) for c in ss[-1]['power'])==tuple(Dn)
    return P,ss,nc

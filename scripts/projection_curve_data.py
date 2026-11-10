"""Explicit representative spatial cubic used by the parallel/perspective diagrams."""
from fractions import Fraction as F

U=(F(0),)*4+(F(7,20),F(7,10))+(F(1),)*4
P=((F(4),F(3),F(0)),(F(3),F(5,2),F(3)),(F(1),F(7,2),F(2,5)),
   (-F(1),F(3),F(6,5)),(-F(2),F(13,5),F(23,5)),(-F(3),F(33,10),F(37,10)))
Q=(F(24,5),F(0),F(0));N=(F(0),F(1),F(0));W=(F(3,20),-F(1),F(3,5))
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def parallel(P):
    a=dot(N,tuple(q-p for q,p in zip(Q,P)))/dot(N,W)
    return tuple(p+a*w for p,w in zip(P,W))

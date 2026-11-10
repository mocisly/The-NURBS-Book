"""Exact normalized rational warping function, Eq11.43-45."""
from fractions import Fraction as F
from native_bspline import de_boor,segments
T=(F(0),)*4+(F(1,4),F(1,2),F(3,4))+(F(1),)*4
B=tuple((F(i==3),)for i in range(7));S=segments(T,B,3)
assert max(p[0]for s in S for p in s['bern'])==F(2,3)
assert tuple(s['bern'] for s in S)==tuple(tuple(reversed(s['bern']))for s in reversed(S))
def f(t,w):
    n=de_boor(T,B,3,t)[0];return n*(1+2*w)/(2*(1+(w-1)*n))
def homogeneous(w):
    peak=2*w/(1+2*w);W=tuple(w if i==3 else F(1) for i in range(7))
    return tuple((a*F(i==3)/peak,a) for i,a in enumerate(W))
for w in(F(1,5),F(1),F(30)):
    assert f(F(0),w)==f(F(1),w)==0 and f(F(1,2),w)==1

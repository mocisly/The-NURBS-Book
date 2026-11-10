"""Fig4.4 representative quadratic five-control family, not the unrelated Ex4.1.

The scan gives degree and weight cases but no numeric coordinates or knots.
Choose a documented uniform clamped thirds vector and its W-shaped polygon.
Only w1 changes, so all curves coincide on the final span[2/3,1].
"""
from fractions import Fraction as F
from surface_geometry import weights
from native_bspline import de_boor
K=(F(0),)*3+(F(1,3),F(2,3))+(F(1),)*3
P=tuple(tuple(map(F,p)) for p in [(0,3),(3,-2),(6,2),(9,-2),(12,4)])
def control_weights(w1):return (F(1),F(w1),F(1),F(1),F(1))
def homogeneous(w1):
    w=control_weights(w1)
    return tuple((w[i]*p[0],w[i]*p[1],w[i]) for i,p in enumerate(P))
def rational(u,w1):
    n=weights(K,2,u);w=control_weights(w1);den=sum(a*b for a,b in zip(n,w))
    assert den>=F(1,3)
    r=tuple(n[i]*w[i]/den for i in range(5));assert min(r)>=0 and sum(r)==1
    val=tuple(sum(r[i]*P[i][d] for i in range(5)) for d in range(2))
    h=de_boor(K,homogeneous(w1),2,u);assert val==tuple(x/h[-1] for x in h[:-1])
    return val,r

"""Representative seven-control polygon shared by printed Figs4.1-4.3."""
from fractions import Fraction as F
from surface_geometry import weights
from native_bspline import de_boor
K=(F(0),)*4+(F(1,4),F(1,2),F(3,4))+(F(1),)*4
P=tuple(tuple(map(F,p)) for p in [(0,0),(1,3),(5,F(17,5)),(3,-2),(9,-2),(8,F(8,5)),(11,2)])
def control_weights(w3):return (F(1),F(1),F(1),F(w3),F(1),F(1),F(1))
def homogeneous(w3):
    w=control_weights(w3)
    return tuple((w[i]*p[0],w[i]*p[1],w[i]) for i,p in enumerate(P))
def rational(u,w3):
    n=weights(K,3,u);w=control_weights(w3);den=sum(a*b for a,b in zip(n,w))
    assert den>0
    r=tuple(n[i]*w[i]/den for i in range(7));assert min(r)>=0 and sum(r)==1
    val=tuple(sum(r[i]*P[i][d] for i in range(7)) for d in range(2))
    h=de_boor(K,homogeneous(w3),3,u)
    assert val==tuple(x/h[-1] for x in h[:-1])
    return val,r

"""Exact rational representative planar arc for8.18 and stereographic composition."""
from fractions import Fraction as F
W=F(3,5)
ARC=((F(2),F(0),F(1)),(F(6,5),F(8,5),W),(-F(14,25),F(48,25),F(1)))
K=(F(0),)*3+(F(1),)*3
T=(F(0),F(0),F(1),F(1))
PLANAR_NET=tuple(((F(0),F(0),F(0),a),(u,v,F(0),a)) for u,v,a in ARC)
def meridian(endpoint):
    u,v=endpoint;g=u*u+v*v
    return ((F(0),F(0),F(0),F(4)),(2*u,2*v,F(0),F(4)),(4*u,4*v,2*g,g+4))
C1=meridian((F(2),F(0)))
C2=tuple((u/2,v/2,a,a) for u,v,a in ARC)
C3=meridian((-F(14,25),F(48,25)))

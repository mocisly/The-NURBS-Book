"""Exact representative data for the five8.5 compatibility/construction stages."""
from fractions import Fraction as F
from degree_elevation_geometry import elevate_spline
from knot51_data import insert
U1=(F(0),)*3+(F(1,4),F(1,2),F(3,4))+(F(1),)*3
U2=(F(0),)*4+(F(3,10),F(7,10))+(F(1),)*4
P1=tuple((F(str(x)),-F(3,4),F(str(z))) for x,z in [(1.6,2.3),(1,.8),(.2,1.2),(-.5,3.1),(-1.1,3.3),(-1.6,2.6)])
P2=tuple((F(str(x)),F(3,4),F(str(z))) for x,z in [(1.6,-.9),(1.3,1),(.2,2.5),(-.2,.8),(-1.2,1.4),(-1.6,3)])
E1,Q1,elevation=elevate_spline(U1,P1,2,1);assert len(Q1)==10
E2,Q2=U2,P2
K1,R1=E1,Q1
for u in (F(3,10),F(7,10)):K1,R1,_=insert(K1,R1,3,u)
K2,R2=U2,P2
for u in (F(1,4),F(1,2),F(3,4)):
    for repeat in range(2):K2,R2,_=insert(K2,R2,3,u)
U=(F(0),)*4+(F(1,4),)*2+(F(3,10),)+(F(1,2),)*2+(F(7,10),)+(F(3,4),)*2+(F(1),)*4
assert K1==K2==U and len(R1)==len(R2)==12
V=(F(0),F(0),F(1),F(1));NET=tuple(zip(R1,R2))
def camera(p):
    x,y,z=p;return (F(12,5)*(-F(39,50)*x+F(24,25)*y),F(12,5)*(-x/2-F(3,10)*y+z))

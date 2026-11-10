"""Representative six-control meridian shared by8.8 and8.9; true tensor revolution."""
from fractions import Fraction as F
from math import isqrt
P=tuple((F(str(r)),F(0),F(str(z))) for r,z in [(1.2,0),(2,.8),(1.8,1.5),(1.6,2.2),(.6,3.1),(1.7,3.9)])
V=(F(0),)*3+(F(1,3),)*2+(F(2,3),)+(F(1),)*3
PROFILE=tuple(p+(F(1),) for p in P)
D=10**40;n=isqrt(2*D*D);lo,hi=F(n,2*D),F(n+1,2*D);assert lo*lo<F(1,2)<hi*hi;w=(lo+hi)/2
CIRCLE=tuple((F(x)*a,F(y)*a,a) for i,(x,y) in enumerate([(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1),(1,0)]) for a in [w if i%2 else F(1)])
U=(F(0),)*3+(F(1,4),)*2+(F(1,2),)*2+(F(3,4),)*2+(F(1),)*3
NET=tuple(tuple((x*r,y*r,a*z,a*b) for r,_,z,b in PROFILE) for x,y,a in CIRCLE)
def camera(p):
    x,y,z=p;return (4*(-F(39,50)*x+F(24,25)*y),4*(-x/2-F(3,10)*y+z))

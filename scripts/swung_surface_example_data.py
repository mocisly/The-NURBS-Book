"""Shared explicitprofile/trajectorycontrols for10.1and10.2swung surfaces."""
from fractions import Fraction as F
P=tuple(tuple(map(F,p)) for p in [('3','0','0'),('1.5','0','.5'),('1.5','0','2.5'),('2.7','0','2.5'),('3','0','5'),('1.8','0','5')])
T=tuple(tuple(map(F,p)) for p in [('4','-2','0'),('4','-1','0'),('2.5','-1','0'),('3','2','0'),('4','2','0'),('3','6','0'),('1','4.5','0'),('.5','3','0'),('-1.5','3','0'),('-1.5','4.5','0'),('-3','4.5','0')])
U=(F(0),)*4+(F(1,3),F(2,3))+(F(1),)*4
V=(F(0),)*4+tuple(F(i,8) for i in range(1,8))+(F(1),)*4
ALPHA=F(3,25)
WP=tuple(F(5) if i in (1,4) else F(1) for i in range(6))
WT=tuple(F(5) if i in (1,4,6,9) else F(1) for i in range(11))
def homogeneous(points,weights):return tuple(tuple(w*x for x in p)+(w,) for p,w in zip(points,weights))
def net(weighted=False):
    a=WP if weighted else (F(1),)*6;b=WT if weighted else (F(1),)*11
    H=tuple(tuple((ALPHA*p[0]*t[0]*a[i]*b[j],ALPHA*p[0]*t[1]*a[i]*b[j],p[2]*a[i]*b[j],a[i]*b[j]) for j,t in enumerate(T)) for i,p in enumerate(P))
    return U,V,3,3,H

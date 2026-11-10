"""Exact representative4x4data and two-stage bicubic interpolation for9.14."""
from fractions import Fraction as F
from global_interpolation_data import interpolate
from surface_geometry import surface
X=tuple(map(F,['3','1.5','0','-1.5']));Y=tuple(map(F,['-2','-1','.5','2']))
Z=tuple(tuple(map(F,row)) for row in [('.8','2.8','3.5','2.2'),('.6','2.5','3.2','2'),('.1','1.3','2.4','1.8'),('-.3','.3','1.6','1.1')])
Q=tuple(tuple((x,y,Z[i][j]) for j,x in enumerate(X)) for i,y in enumerate(Y))
PARAMS=tuple(F(i,3) for i in range(4))
cols=[]
for j in range(4):
    U,C=interpolate(tuple(Q[i][j] for i in range(4)),PARAMS);cols.append(C)
R=tuple(tuple(cols[j][i] for j in range(4)) for i in range(4))
P=[]
for row in R:
    V,C=interpolate(row,PARAMS);P.append(C)
P=tuple(P)
# Reverse the interpolation order independently;the final16controls must agree.
opposite=tuple(interpolate(row,PARAMS)[1] for row in Q)
reversecols=tuple(interpolate(tuple(opposite[i][j] for i in range(4)),PARAMS)[1] for j in range(4))
assert P==tuple(tuple(reversecols[j][i] for j in range(4)) for i in range(4))
assert all(surface(U,V,3,3,P,u,v)==Q[i][j] for i,u in enumerate(PARAMS) for j,v in enumerate(PARAMS))
def camera(q):
    x,y,z=q;return (2*(-F(4,5)*x+F(9,10)*y),2*(-F(2,5)*x-F(7,20)*y+z))

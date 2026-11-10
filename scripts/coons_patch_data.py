"""Compatible representative nonrational boundaries and exact Coons blend.

No numeric data are specified for10.24. Same native cubic/quadratic spaces as
preceding network; all four corners and complete boundary coefficient identities
are exact. R1/R2/T raised to the common basis using affine precision.
"""
from fractions import Fraction as F
from gordon_network_data import UC as U,VC as V,view
from surface_geometry import isocurve,surface
from native_bspline import de_boor
GU=tuple(sum(U[i+1:i+4])/3 for i in range(6))
GV=tuple(sum(V[j+1:j+3])/2 for j in range(5))
X=tuple(8*u-4 for u in GU);Y=tuple(7*v-F(7,2) for v in GV)
C0U=tuple((x,Y[0],F(z)) for x,z in zip(X,('.2','-.6','-.9','-.2','.3','.5')))
C1U=tuple((x,Y[-1],F(z)) for x,z in zip(X,('1.7','.9','1.2','2.6','2','1.3')))
C0V=tuple((X[0],y,F(z)) for y,z in zip(Y,('.2','.8','.6','1.2','1.7')))
C1V=tuple((X[-1],y,F(z)) for y,z in zip(Y,('.5','.4','.8','2','1.3')))
CORNERS=((C0U[0],C1U[0]),(C0U[-1],C1U[-1]))
assert C0U[0]==C0V[0] and C0U[-1]==C1V[0] and C1U[0]==C0V[-1] and C1U[-1]==C1V[-1]
def mix(a,b,t):return tuple((1-t)*x+t*y for x,y in zip(a,b))
def bilinear(u,v):return mix(mix(*CORNERS[0],v),mix(*CORNERS[1],v),u)
def construct():
    R1=tuple(tuple(mix(C0U[i],C1U[i],v) for v in GV) for i in range(6))
    R2=tuple(tuple(mix(C0V[j],C1V[j],u) for j in range(5)) for u in GU)
    T=tuple(tuple(bilinear(u,v) for v in GV) for u in GU)
    P=tuple(tuple(tuple(a+b-c for a,b,c in zip(R1[i][j],R2[i][j],T[i][j])) for j in range(5)) for i in range(6))
    S=(U,V,3,2,P)
    for fixed,C in [(F(0),C0U),(F(1),C1U)]:assert isocurve(*S,'u',fixed)[2]==C
    for fixed,C in [(F(0),C0V),(F(1),C1V)]:assert isocurve(*S,'v',fixed)[2]==C
    assert any(P[i][j][2]!=T[i][j][2] for i in range(6) for j in range(5))
    return {name:(U,V,3,2,net) for name,net in [('R1',R1),('R2',R2),('T',T),('S',P)]}

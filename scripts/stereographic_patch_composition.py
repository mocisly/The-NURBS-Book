"""Exact equation8.23 composition and full4x2Bernstein net,without geometric tracing."""
from fractions import Fraction as F
from math import comb
from tensor_power_conversion import convert
def plus(a,b,scale=F(1)):
    out=dict(a)
    for k,v in b.items():out[k]=out.get(k,F(0))+scale*v
    return {k:v for k,v in out.items() if v}
def times(a,b):
    out={}
    for (i,j),x in a.items():
        for (k,l),y in b.items():out[i+k,j+l]=out.get((i+k,j+l),F(0))+x*y
    return {k:v for k,v in out.items() if v}
def scale(a,c):return {k:c*v for k,v in a.items() if c*v}
def compose_patch(K,T,plane,R=F(1)):
    _,_,A=convert(K,T,2,1,plane,2,1)
    U,V,H=({(i,j):A[i][j][d] for i in range(3) for j in range(2) if A[i][j][d]} for d in (0,1,3))
    G=plus(times(U,U),times(V,V))
    X=scale(times(U,H),4*R*R);Y=scale(times(V,H),4*R*R);Z=scale(G,2*R);W=plus(G,times(H,H),4*R*R)
    polys=(X,Y,Z,W);power=tuple(tuple(tuple(poly.get((i,j),F(0)) for poly in polys) for j in range(3)) for i in range(5))
    Q=tuple(tuple(tuple(sum(F(comb(i,k),comb(4,k))*F(comb(j,l),comb(2,l))*power[k][l][d] for k in range(i+1) for l in range(j+1)) for d in range(4)) for j in range(3)) for i in range(5))
    K4=(F(0),)*5+(F(1),)*5;T2=(F(0),)*3+(F(1),)*3
    _,_,recovered=convert(K4,T2,4,2,Q,4,2);assert recovered==power
    zbar=plus(Z,W,-R);identity=plus(plus(times(X,X),times(Y,Y)),plus(times(zbar,zbar),times(W,W),-R*R));assert not identity
    assert min(h[-1] for row in Q for h in row)>0
    return K4,T2,Q,{'all15_homogeneous_power_vectors_recovered_exactly':True,'whole_surface_sphere_coefficient_identity_exact':True,'minimum_Bernstein_weight':str(min(h[-1] for row in Q for h in row)),'homogeneous_power_coefficients':[[list(map(str,h)) for h in row] for row in power]}

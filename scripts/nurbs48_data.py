"""Fig4.8 representative5x5 net, with the four stated interior weights10."""
from fractions import Fraction as F
from surface_geometry import weights,surface,verify_tensor
xs=(3,1,0,-2,-2);ys=(-1,0,1,2,3)
zi=(F(3,2),F(3,2),F(0),F(-1,4),F(-1,2))
zj=(F(0),F(-1,2),F(1,2),F(0),F(6,5))
P=tuple(tuple((F(xs[j]),F(ys[i]),zi[i]+zj[j]) for j in range(5)) for i in range(5))
W=tuple(tuple(F(10 if i in (1,2) and j in (1,2) else 1) for j in range(5)) for i in range(5))
H=tuple(tuple(tuple(w*c for c in p)+(w,) for p,w in zip(row,ww)) for row,ww in zip(P,W))
CAMERA=((F(-9,10),F(1),F(0)),(F(-3,5),F(-7,20),F(1)))
CAMERA_L1_NORM=max(sum(abs(row[d]) for row in CAMERA) for d in range(3))
def knots(degree):
    assert degree in (2,3)
    return (F(0),)*(degree+1)+(tuple(F(j,3) for j in (1,2)) if degree==2 else (F(1,2),))+(F(1),)*(degree+1)
def rational(K,p,u,v):
    a,b=weights(K,p,u),weights(K,p,v)
    h=surface(K,K,p,p,H,u,v);assert 1<=h[-1]<=10
    r=tuple(tuple(a[i]*b[j]*W[i][j]/h[-1] for j in range(5)) for i in range(5))
    assert min(min(row) for row in r)>=0 and sum(map(sum,r))==1
    val=tuple(sum(r[i][j]*P[i][j][d] for i in range(5) for j in range(5)) for d in range(3))
    assert val==tuple(c/h[-1] for c in h[:-1])
    f=sum(a[i] for i in (1,2))*sum(b[j] for j in (1,2))
    assert h[-1]==1+9*f
    return val
def verify(degree):
    K=knots(degree);n=verify_tensor(K,K,degree,degree,H,10)
    for i in range(11):
        for j in range(11):rational(K,degree,F(i,10),F(j,10))
    for u,i in [(F(0),0),(F(1),4)]:
        for v,j in [(F(0),0),(F(1),4)]:assert rational(K,degree,u,v)==P[i][j]
    return {'degree':degree,'knots':list(map(str,K)),'homogeneous_tensor_vs_two_nested_deboor_points':n,
            'rational_basis_partition_projection_points':121,'corner_interpolation':True,
            'global_denominator_bounds':[1,10],'denominator_identity':'W=1+9*(N1(u)+N2(u))*(N1(v)+N2(v))'}

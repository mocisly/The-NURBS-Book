"""Fig4.11 representative7x8 net, exactly the cubic x quadratic space of4.10."""
from fractions import Fraction as F
from surface_geometry import weights,surface,verify_tensor,extraction
U=(F(0),)*4+(F(1,4),F(1,2),F(3,4))+(F(1),)*4
V=(F(0),)*3+tuple(F(j,5) for j in (1,2,3,3,4))+(F(1),)*3
p,q=3,2
# Original drawings show a nearly planar grid with raised and depressed controls,
# but give no coordinates. These representative values preserve that structure.
heights={(4,2):F(2),(3,2):F(6,5),(1,2):F(-3,2),(2,5):F(3,5)}
P=tuple(tuple((F(3-i),F(j-3),heights.get((i,j),F(0))) for j in range(8)) for i in range(7))
TARGET=P[4][2]
CAMERA_NORM=F(63,50)
DISPLAY_SHIFT=F(27,5)
def homogeneous(w):
    return tuple(tuple(tuple((w if (i,j)==(4,2) else 1)*c for c in P[i][j])+((w if (i,j)==(4,2) else F(1)),) for j in range(8)) for i in range(7))
def factor(u,v):return weights(U,p,u)[4]*weights(V,q,v)[2]
def rational(u,v,w):
    a,b=weights(U,p,u),weights(V,q,v);D=1+(w-1)*a[4]*b[2];assert D>0
    r=tuple(tuple(a[i]*b[j]*(w if (i,j)==(4,2) else 1)/D for j in range(8)) for i in range(7))
    assert min(min(row) for row in r)>=0 and sum(map(sum,r))==1
    val=tuple(sum(r[i][j]*P[i][j][d] for i in range(7) for j in range(8)) for d in range(3))
    H=surface(U,V,p,q,homogeneous(w),u,v)
    assert H[-1]==D and val==tuple(c/D for c in H[:-1])
    return val
def verify(w):
    checks=verify_tensor(U,V,p,q,homogeneous(w),10);identities=outside=0
    for a in range(11):
        for b in range(11):
            u,v=F(a,10),F(b,10);f=factor(u,v);val=rational(u,v,w)
            base=surface(U,V,p,q,P,u,v)
            assert val==tuple((base[d]+(w-1)*f*TARGET[d])/(1+(w-1)*f) for d in range(3))
            low,high=rational(u,v,F(2,5)),rational(u,v,F(6))
            assert sum((high[d]-TARGET[d])**2 for d in range(3))<=sum((low[d]-TARGET[d])**2 for d in range(3))
            identities+=1
            if u<=F(1,4) or v>=F(3,5):
                assert val==base;outside+=1
    for u,i in [(F(0),0),(F(1),6)]:
        for v,j in [(F(0),0),(F(1),7)]:assert rational(u,v,w)==P[i][j]
    return {'w42':str(w),'homogeneous_tensor_vs_nested_deboor_points':checks,
            'exact_rational_weight_identity_and_partition_points':identities,'unchanged_exterior_points':outside,
            'all_parameter_proof':'S_w=(S_1+(w-1)*f*P42)/(1+(w-1)*f); f=N4,3*N2,2; f=0 outside[1/4,1)x[0,3/5)',
            'four_corner_interpolation':True}

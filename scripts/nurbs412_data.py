"""Fig4.12 representative bicubic dome and its raised center control."""
from fractions import Fraction as F
from surface_geometry import weights,surface,verify_tensor,extraction
K=(F(0),)*4+(F(1,2),)+(F(1),)*4
P=tuple(tuple((F(3)-F(3,2)*i,F(-3)+F(3,2)*j,
               F(4) if (i,j)==(2,2) else F(3,2)-((F(3)-F(3,2)*i)**2+(F(-3)+F(3,2)*j)**2)/9)
              for j in range(5)) for i in range(5))
TARGET=P[2][2];CAMERA_NORM=F(3,2)
def homogeneous(w):
    return tuple(tuple(tuple((w if (i,j)==(2,2) else 1)*c for c in P[i][j])+((w if (i,j)==(2,2) else F(1)),) for j in range(5)) for i in range(5))
def factor(u,v):return weights(K,3,u)[2]*weights(K,3,v)[2]
def rational(u,v,w):
    a,b=weights(K,3,u),weights(K,3,v);f=a[2]*b[2];D=1+(w-1)*f;assert D>=F(3,4)
    R=tuple(tuple(a[i]*b[j]*(w if (i,j)==(2,2) else 1)/D for j in range(5)) for i in range(5))
    assert min(min(row) for row in R)>=0 and sum(map(sum,R))==1
    result=tuple(sum(R[i][j]*P[i][j][d] for i in range(5) for j in range(5)) for d in range(3))
    h=surface(K,K,3,3,homogeneous(w),u,v);assert h[-1]==D and result==tuple(c/D for c in h[:-1])
    return result
def verify(w):
    # Each N2 Bernstein extraction coefficient is <=1/2, so f<=1/4.
    assert max(extraction(K,3,s)[r][2] for s in (3,4) for r in range(4))==F(1,2)
    n=verify_tensor(K,K,3,3,homogeneous(w),10)
    for a in range(11):
        for b in range(11):
            u,v=F(a,10),F(b,10);f=factor(u,v);value=rational(u,v,w);B=rational(u,v,0)
            alpha=w*f/(1-f+w*f)
            assert value==tuple((1-alpha)*B[d]+alpha*TARGET[d] for d in range(3))
    return {'w22':str(w),'homogeneous_tensor_vs_nested_deboor_points':n,'rational_partition_and_weight_line_identity_points':121,
            'global_denominator_lower_bound':'3/4','basis_bound_proof':'N2,3 Bernstein coefficients<=1/2; f=N2(u)*N2(v)<=1/4; W0=1-f>=3/4'}

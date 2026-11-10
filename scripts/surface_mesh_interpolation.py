"""Certified mesh parameters and exact tensor interpolation of16shared data."""
from fractions import Fraction as F
from math import isqrt
from global_interpolation_data import interpolate
from surface_geometry import surface
from mesh_interpolation_example_data import Q
SCALE=10**12
def sqrt_interval(lo,hi):
    a=F(isqrt(lo.numerator*SCALE**2//lo.denominator),SCALE)
    b=F(isqrt(hi.numerator*SCALE**2//hi.denominator)+1,SCALE)
    assert a*a<=lo<=hi<b*b
    return a,b
def line_parameters(points,mode):
    if mode=='uniform':return tuple(F(i,3) for i in range(4)),tuple((F(i,3),F(i,3)) for i in range(4))
    lengths=[]
    for A,B in zip(points,points[1:]):
        square=sum((b-a)**2 for a,b in zip(A,B));lo,hi=sqrt_interval(square,square)
        if mode=='centripetal':lo,hi=sqrt_interval(lo,hi)
        else:assert mode=='chord'
        lengths.append((lo,hi))
    lower=tuple(x[0] for x in lengths);upper=tuple(x[1] for x in lengths)
    values=(F(0),)+tuple(sum(lower[:i])/sum(lower) for i in (1,2))+(F(1),)
    bounds=((F(0),F(0)),)+tuple((sum(lower[:i])/sum(upper),sum(upper[:i])/sum(lower)) for i in (1,2))+((F(1),F(1)),)
    assert all(a<=t<=b and b-a<F(1,10**10) for t,(a,b) in zip(values,bounds))
    return values,bounds
def mesh_parameters(mode):
    result=[];proof=[]
    for lines in (tuple(zip(*Q)),Q):
        each=tuple(line_parameters(line,mode) for line in lines)
        values=tuple(sum(e[0][i] for e in each)/4 for i in range(4))
        bounds=tuple(tuple(sum(e[1][i][j] for e in each)/4 for j in (0,1)) for i in range(4))
        assert all(a<b for a,b in zip(values,values[1:]))
        result.append(values);proof.append(bounds)
    return tuple(result),tuple(proof)
def interpolate_mesh(mode,p=2,q=3):
    (upar,vpar),proof=mesh_parameters(mode);knot_mode='uniform' if mode=='uniform' else 'average'
    cols=[]
    for j in range(4):
        U,C=interpolate(tuple(Q[i][j] for i in range(4)),upar,p,knot_mode);cols.append(C)
    R=tuple(tuple(cols[j][i] for j in range(4)) for i in range(4));P=[]
    for row in R:
        V,C=interpolate(row,vpar,q,knot_mode);P.append(C)
    P=tuple(P)
    reverse=tuple(interpolate(row,vpar,q,knot_mode)[1] for row in Q)
    reverse_cols=tuple(interpolate(tuple(reverse[i][j] for i in range(4)),upar,p,knot_mode)[1] for j in range(4))
    assert P==tuple(tuple(reverse_cols[j][i] for j in range(4)) for i in range(4))
    assert all(surface(U,V,p,q,P,u,v)==Q[i][j] for i,u in enumerate(upar) for j,v in enumerate(vpar))
    return (U,V,p,q,P),(upar,vpar),proof

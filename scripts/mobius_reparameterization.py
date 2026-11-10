"""Exact degree-preserving rational B-spline reparameterization by a Mobius map."""
from fractions import Fraction as F
from math import prod
from native_bspline import de_boor
from rational_geometry import project

def transform(U,H,p,coefficients):
    a,b,c,d=map(F,coefficients);det=a*d-b*c;assert det>0
    assert min(c*U[0]+d,c*U[-1]+d)>0
    def g(u):return (a*u+b)/(c*u+d)
    def inverse(s):return (b-d*s)/(c*s-a)
    K=tuple(map(g,U));factors=tuple(prod(c*U[i+j]+d for j in range(1,p+1)) for i in range(len(H)))
    Q=tuple(tuple(x/f for x in row) for row,f in zip(H,factors))
    assert all(row[-1]>0 for row in Q)
    for i in range(101):
        u=U[0]+(U[-1]-U[0])*F(i,100);s=g(u)
        assert inverse(s)==u
        assert project(de_boor(U,H,p,u))==project(de_boor(K,Q,p,s))
    return K,Q,g,inverse,{'exact_parameter_and_projected_curve_checks':101,
                         'positive_determinant':str(det),'positive_denominator_minimum':str(min(c*U[0]+d,c*U[-1]+d)),
                         'homogeneous_divisors':list(map(str,factors))}

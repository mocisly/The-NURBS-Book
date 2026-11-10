"""Exact local Bezier/global power conversion for polynomial tensor B-spline patches."""
from fractions import Fraction as F
from math import comb
from surface_geometry import local_patch
from bspline_math import piece

def matrix(p):
    return tuple(tuple(F((-1)**(i-j)*comb(p,j)*comb(p-j,i-j)) if i>=j else F(0) for j in range(p+1)) for i in range(p+1))

def affine_matrix(p,a,b):
    h=b-a;offset,scale=-a/h,1/h
    return tuple(tuple(F(comb(j,i))*scale**i*offset**(j-i) if j>=i else F(0) for j in range(p+1)) for i in range(p+1))

def convert(U,V,p,q,P,us,vs):
    Q,_,_=local_patch(U,V,p,q,P,us,vs);M,N=matrix(p),matrix(q)
    A=tuple(tuple(tuple(sum(M[k][i]*N[l][j]*Q[i][j][d] for i in range(p+1) for j in range(q+1)) for d in range(len(P[0][0]))) for l in range(q+1)) for k in range(p+1))
    R,T=affine_matrix(p,*U[us:us+2]),affine_matrix(q,*V[vs:vs+2])
    B=tuple(tuple(tuple(sum(R[k][i]*T[l][j]*A[i][j][d] for i in range(p+1) for j in range(q+1)) for d in range(len(P[0][0]))) for l in range(q+1)) for k in range(p+1))
    # Independent Cox-de Boor basis-polynomial tensor product, no extraction matrices.
    uscal=[piece(U,i,p,us) for i in range(len(P))]
    vscal=[piece(V,j,q,vs) for j in range(len(P[0]))]
    for k in range(p+1):
        for l in range(q+1):
            direct=tuple(sum((u[k] if k<len(u) else 0)*(v[l] if l<len(v) else 0)*P[i][j][d] for i,u in enumerate(uscal) for j,v in enumerate(vscal)) for d in range(len(P[0][0])))
            assert B[k][l]==direct
    return Q,A,B

def evaluate(B,u,v):
    return tuple(sum(B[i][j][d]*u**i*v**j for i in range(len(B)) for j in range(len(B[0]))) for d in range(len(B[0][0])))

"""Exact tensor B-spline evaluation, isocurves and local Bezier extraction."""
from fractions import Fraction as F
from math import comb
from bspline_math import basis,piece,compose_affine
from native_bspline import de_boor

def weights(k,p,t):
    n=len(k)-p-1
    return [F(i==n-1) for i in range(n)] if t==k[-1] else [basis(k,i,p,t) for i in range(n)]

def surface(U,V,p,q,P,u,v):
    a,b=weights(U,p,u),weights(V,q,v)
    return tuple(sum(a[i]*b[j]*P[i][j][d] for i in range(len(a)) for j in range(len(b))) for d in range(len(P[0][0])))

def isocurve(U,V,p,q,P,variable,fixed):
    if variable=='u':
        b=weights(V,q,fixed)
        controls=tuple(tuple(sum(b[j]*P[i][j][d] for j in range(len(b))) for d in range(len(P[0][0]))) for i in range(len(P)))
        return U,p,controls
    a=weights(U,p,fixed)
    controls=tuple(tuple(sum(a[i]*P[i][j][d] for i in range(len(a))) for d in range(len(P[0][0]))) for j in range(len(P[0])))
    return V,q,controls

def verify_tensor(U,V,p,q,P,steps=20):
    u0,u1=U[p],U[-p-1];v0,v1=V[q],V[-q-1]
    for a in range(steps+1):
        u=u0+(u1-u0)*F(a,steps);wu=weights(U,p,u);assert min(wu)>=0 and sum(wu)==1
        for b in range(steps+1):
            v=v0+(v1-v0)*F(b,steps);wv=weights(V,q,v);assert min(wv)>=0 and sum(wv)==1
            x=surface(U,V,p,q,P,u,v)
            first=[de_boor(U,[P[i][j] for i in range(len(P))],p,u) for j in range(len(P[0]))]
            second=[de_boor(V,row,q,v) for row in P]
            assert x==de_boor(V,first,q,v)==de_boor(U,second,p,u)
    for u,i in [(u0,0),(u1,len(P)-1)]:
        for v,j in [(v0,0),(v1,len(P[0])-1)]: assert surface(U,V,p,q,P,u,v)==P[i][j]
    return (steps+1)**2

def extraction(k,p,span):
    a,b=k[span:span+2];assert a<b
    cols=[compose_affine(piece(k,i,p,span),a,b-a) for i in range(len(k)-p-1)]
    matrix=tuple(tuple(sum((c[l] if l<len(c) else 0)*F(comb(r,l),comb(p,l)) for l in range(r+1)) for c in cols) for r in range(p+1))
    assert all(min(row)>=0 and sum(row)==1 for row in matrix)
    assert all(matrix[r][i]==0 for r in range(p+1) for i in range(len(cols)) if not span-p<=i<=span)
    return matrix

def local_patch(U,V,p,q,P,uspan,vspan):
    a,b=extraction(U,p,uspan),extraction(V,q,vspan)
    Q=tuple(tuple(tuple(sum(a[r][i]*b[s][j]*P[i][j][d] for i in range(len(P)) for j in range(len(P[0]))) for d in range(len(P[0][0]))) for s in range(q+1)) for r in range(p+1))
    # Every extracted control is an exact convex combination of only active controls.
    assert all(sum(a[r][i]*b[s][j] for i in range(len(P)) for j in range(len(P[0])))==1 for r in range(p+1) for s in range(q+1))
    return Q,a,b

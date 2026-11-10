"""Exact midpoint insertion and a certified control-polygon approximation bound."""
from fractions import Fraction as F
from math import comb
from knot51_data import insert
from bspline_math import compose_affine

def refine(U,P,p):
    additions=tuple((a+b)/2 for a,b in zip(U,U[1:]) if a<b)
    for u in additions:U,P,_=insert(U,P,p,u)
    return U,P,additions

def polygon_error_bound(U,P,p,segs):
    """L1 bound for C(u)-linear Greville control-polygon interpolation."""
    G=tuple(sum(U[i+1:i+p+1])/p for i in range(len(P)))
    assert all(a<b for a,b in zip(G,G[1:]))
    breaks=sorted(set(U[p:len(P)+1])|set(G));bound=F(0)
    for a,b in zip(breaks,breaks[1:]):
        mid=(a+b)/2;seg=next(s for s in segs if s['a']<=mid<s['b']);j=next(j for j in range(len(P)-1) if G[j]<=mid<G[j+1])
        local=[]
        for d,power in enumerate(seg['power']):
            slope=(P[j+1][d]-P[j][d])/(G[j+1]-G[j]);res=list(power)
            res[0]-=P[j][d]-slope*G[j];res[1]-=slope
            local.append(compose_affine(res,a,b-a))
        bern=[tuple(sum((co[k] if k<len(co) else 0)*F(comb(r,k),comb(p,k)) for k in range(r+1)) for co in local) for r in range(p+1)]
        bound=max(bound,max(sum(map(abs,row)) for row in bern))
    return bound

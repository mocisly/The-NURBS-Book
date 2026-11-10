"""Exact homogeneous derivative nets and rational quotient recurrence."""
from math import comb
from surface_geometry import surface

def derived_net(U,V,p,q,R,axis):
    dim=len(R[0][0])
    if axis==0:
        Q=tuple(tuple(tuple(p*(R[i+1][j][d]-R[i][j][d])/(U[i+p+1]-U[i+1]) for d in range(dim)) for j in range(len(R[0]))) for i in range(len(R)-1))
        return U[1:-1],V,p-1,q,Q
    Q=tuple(tuple(tuple(q*(R[i][j+1][d]-R[i][j][d])/(V[j+q+1]-V[j+1]) for d in range(dim)) for j in range(len(R[0])-1)) for i in range(len(R)))
    return U,V[1:-1],p,q-1,Q

def jets(U,V,p,q,H,u,v,order=2):
    homogeneous={};values={}
    for total in range(order+1):
        for r in range(total+1):
            s=total-r;net=(U,V,p,q,H)
            for axis,n in ((0,r),(1,s)):
                for _ in range(n):net=derived_net(*net,axis)
            h=surface(*net,u,v);homogeneous[r,s]=h
            values[r,s]=tuple((h[d]-sum(comb(r,i)*comb(s,j)*homogeneous[i,j][-1]*values[r-i,s-j][d]
                for i in range(r+1) for j in range(s+1) if i+j))/homogeneous[0,0][-1] for d in range(len(h)-1))
    return values

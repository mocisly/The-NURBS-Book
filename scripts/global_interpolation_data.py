"""Exact representative seven-point data shared by9.3/9.4 and interpolation helpers."""
from fractions import Fraction as F
from inverse_knot_projection import solve
from surface_geometry import weights
Q=tuple(tuple(map(F,p)) for p in [(0,0),(0,1),(F(6,5),F(13,5)),(F(18,5),F(19,10)),(F(24,5),F(3,10)),(6,F(4,5)),(F(36,5),F(3,10))])
LENGTHS=tuple(map(F,('1','2','5/2','2','13/10','13/10')))
assert all(sum((x-y)**2 for x,y in zip(b,a))==ell*ell for a,b,ell in zip(Q,Q[1:],LENGTHS))
TOTAL=sum(LENGTHS);PARAMS=(F(0),)+tuple(sum(LENGTHS[:i])/TOTAL for i in range(1,len(Q)))
def interpolate(points,parameters,p=3,mode='average'):
    n=len(points)-1;assert len(parameters)==n+1 and parameters[0]==0 and parameters[-1]==1
    assert all(a<b for a,b in zip(parameters,parameters[1:]))
    internal=tuple(sum(parameters[j:j+p])/p for j in range(1,n-p+1)) if mode=='average' else tuple(F(j,n-p+1) for j in range(1,n-p+1))
    U=(F(0),)*(p+1)+internal+(F(1),)*(p+1)
    matrix=tuple(tuple(weights(U,p,t)) for t in parameters);controls=solve(matrix,points)
    assert all(tuple(sum(a*c[d] for a,c in zip(row,controls)) for d in range(len(points[0])))==point for row,point in zip(matrix,points))
    return U,controls
U,P=interpolate(Q,PARAMS)

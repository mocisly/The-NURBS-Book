"""Exact rational implementation of the symmetric Bezier reduction5.41/5.42."""
from fractions import Fraction as F
from rational_geometry import elevate

def reduce_bezier(Q):
    p=len(Q)-1;r=(p-1)//2;assert p>=2
    P=[None]*p;P[0],P[-1]=Q[0],Q[-1]
    def left(i):
        a=F(i,p);return tuple((x-a*y)/(1-a) for x,y in zip(Q[i],P[i-1]))
    def right(i):
        a=F(i+1,p);return tuple((x-(1-a)*y)/a for x,y in zip(Q[i+1],P[i+1]))
    for i in range(1,r+1 if p%2==0 else r):P[i]=left(i)
    for i in range(p-2,r,-1):P[i]=right(i)
    if p%2:
        L,R=left(r),right(r);P[r]=tuple((x+y)/2 for x,y in zip(L,R))
    P=tuple(P);A=elevate(P);D=tuple(tuple(x-y for x,y in zip(a,b)) for a,b in zip(Q,A))
    n=p//2;assert all(not any(d) for d in D[:n]+D[-n:])
    if p%2:assert D[r]==tuple(-t for t in D[r+1])
    return P,{'original_degree':p,'reduced_degree':p-1,
              'exact_re_elevation_residuals':[[str(t) for t in pt] for pt in D],
              'whole_parameter_L1_error_bound':str(max(sum(map(abs,d)) for d in D)),
              'endpoint_controls_and_derivative_orders_preserved':p//2-1,
              'formula':'5.41' if p%2==0 else '5.42'}

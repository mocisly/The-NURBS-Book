"""Representative geometric controls; printed knot vector and constraint data.

All constraints are solved over exact rational numbers. No scan coordinates.
"""
from fractions import Fraction as F
from bspline_math import piece,evaluate,derivative
from inverse_knot_projection import solve
from native_bspline import de_boor

U=(F(0),)*4+tuple(F(i,5) for i in range(1,5))+(F(1),)*4
P=tuple(tuple(F(str(x)) for x in p) for p in
        [(0,0),(.12,0),(.2,.12),(.2,.3),(.38,.36),(.52,.24),(.48,0),(.34,0)])

def row(u,k=0):
    span=next(s for s in range(3,8) if U[s]<=u<U[s+1])
    out=[]
    for i in range(8):
        c=piece(U,i,3,span)
        for _ in range(k):c=derivative(c)
        out.append(evaluate(c,u))
    return tuple(out)

def constrained(free,constraints):
    B=tuple(tuple(row(u,k)[i] for i in free) for u,k,_ in constraints)
    D=tuple(tuple(d) for _,_,d in constraints)
    G=tuple(tuple(sum(a*b for a,b in zip(x,y)) for y in B) for x in B)
    L=solve(G,D)
    delta=tuple(tuple(sum(B[j][i]*L[j][d] for j in range(len(B))) for d in range(2)) for i in range(len(free)))
    assert all(sum(B[j][i]*delta[i][d] for i in range(len(free)))==D[j][d]
               for j in range(len(B)) for d in range(2))
    # delta=B^T L proves orthogonality to every null vector, hence minimum norm.
    Q=list(P)
    for i,dp in zip(free,delta):Q[i]=tuple(a+b for a,b in zip(P[i],dp))
    Q=tuple(Q)
    for u,k,d in constraints:
        r=row(u,k)
        assert tuple(sum(r[i]*(Q[i][a]-P[i][a]) for i in range(8)) for a in range(2))==tuple(d)
    assert all(Q[i]==P[i] for i in range(8) if i not in free)
    return Q,dict(free=free,B=B,gram=G,multipliers=L,delta=delta,constraints=constraints,minimum_norm_certificate='delta = B^T (B B^T)^-1 D; exact constraint identities')

POSITION=(F(1,25),-F(2,25))
POSITION_CASES=[constrained(free,[(F(1,2),0,POSITION)]) for free in [(2,3,4,5),(3,4),(3,)]]

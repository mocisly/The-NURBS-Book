"""Representative 6x5 tensor surface for11.37--39, exact minimum-norm constraints."""
from fractions import Fraction as F
from bspline_math import piece,evaluate,derivative
from surface_geometry import surface,local_patch,extraction
from inverse_knot_projection import solve
U=(F(0),)*4+(F(1,3),F(2,3))+(F(1),)*4
V=(F(0),)*3+(F(1,3),F(2,3))+(F(1),)*3
GU=tuple(sum(U[i+1:i+4])/3 for i in range(6));GV=tuple(sum(V[j+1:j+3])/2 for j in range(5))
ZU=tuple(map(F,('0','.2','1','.4','.2','0')));ZV=tuple(map(F,('0','.2','-.4','.2','0')))
P=tuple(tuple((8*u-4,7*v-F(7,2),ZU[i]+ZV[j])for j,v in enumerate(GV))for i,u in enumerate(GU))
BASE=(U,V,3,2,P);UV=(F(1,2),F(1,2))
def derivatives(K,p,t,k):
    n=len(K)-p-1;span=next(s for s in range(p,n)if K[s]<=t<K[s+1]);out=[]
    for i in range(n):
        c=piece(K,i,p,span)
        for _ in range(k):c=derivative(c)
        out.append(evaluate(c,t))
    return tuple(out)
def row(k=0,l=0):
    a,b=derivatives(U,3,UV[0],k),derivatives(V,2,UV[1],l)
    return {(i,j):a[i]*b[j] for i in range(6)for j in range(5)}
ACTIVE=tuple(ij for ij,w in row().items()if w)
def value(net,k=0,l=0):
    return tuple(sum(w*net[i][j][d]for(i,j),w in row(k,l).items())for d in range(3))
def constrained(free,constraints):
    B=tuple(tuple(row(k,l)[ij] for ij in free)for k,l,d in constraints)
    D=tuple(d for k,l,d in constraints);G=tuple(tuple(sum(a*b for a,b in zip(x,y))for y in B)for x in B);L=solve(G,D)
    delta={ij:tuple(sum(B[r][c]*L[r][d]for r in range(len(B)))for d in range(3))for c,ij in enumerate(free)}
    Q=tuple(tuple(tuple(p[d]+delta.get((i,j),(0,0,0))[d]for d in range(3))for j,p in enumerate(rowp))for i,rowp in enumerate(P))
    for k,l,d in constraints:assert tuple(b-a for a,b in zip(value(P,k,l),value(Q,k,l)))==tuple(d)
    assert all(Q[i][j]==P[i][j]for i in range(6)for j in range(5)if(i,j)not in free)
    assert Q[0]==P[0]and Q[-1]==P[-1]and all(a[0]==b[0]and a[-1]==b[-1]for a,b in zip(P,Q))
    # Whole tensor patch identities against the exact basis displacement field.
    checks=0
    for s in range(3,6):
        for t in range(2,5):
            A=local_patch(*BASE,s,t)[0];Z=local_patch(U,V,3,2,Q,s,t)[0]
            E,H=extraction(U,3,s),extraction(V,2,t)
            for a,(oldrow,newrow) in enumerate(zip(A,Z)):
                for b,(old,new) in enumerate(zip(oldrow,newrow)):
                    assert tuple(y-x for x,y in zip(old,new))==tuple(sum(E[a][i]*H[b][j]*d[k]for(i,j),d in delta.items())for k in range(3))
                    if all(d[0]==d[1]==0 for d in delta.values()):assert new[:2]==old[:2]
                    checks+=1
    return Q,dict(free=free,B=B,gram=G,multipliers=L,delta=[(ij,d)for ij,d in delta.items()],constraints=constraints,old_point=value(P),new_point=value(Q),whole_boundary_curves_unchanged=True,tensor_coefficients_checked=checks,minimum_norm_certificate='delta=B^T(BB^T)^-1D, exact constraints')

"""Exact rational local least-squares inverse of Boehm knot insertion.

Unaffected controls remain fixed. New controls minimize the squared residual of
the original control equations. Reinserting removed knots yields a common basis;
its nonnegative partition gives a certified whole-parameter L1 curve error bound.
This is an explicitly documented representative approximation, not raster fitting.
"""
from fractions import Fraction as F
from knot51_data import insert

def solve(A,B):
    """Solve a nonsingular square system with multiple exact right-hand sides."""
    n=len(A);dim=len(B[0]);R=[list(row)+list(b) for row,b in zip(A,B)]
    for j in range(n):
        pivot=next(i for i in range(j,n) if R[i][j]);R[j],R[pivot]=R[pivot],R[j]
        value=R[j][j];R[j]=[v/value for v in R[j]]
        for i in range(n):
            if i==j:continue
            factor=R[i][j]
            if factor:R[i]=[a-factor*b for a,b in zip(R[i],R[j])]
    assert all(R[i][j]==F(i==j) for i in range(n) for j in range(n))
    return tuple(tuple(row[n:n+dim]) for row in R)

def remove_to(U,P,p,removed):
    U=tuple(map(F,U));P=tuple(tuple(map(F,t)) for t in P);K=list(U)
    for t in removed:
        assert U[p]<t<U[len(P)] and t in K;K.remove(t)
    K=tuple(K);n=len(K)-p-1;dim=len(P[0])
    A=tuple(tuple(F(i==j) for j in range(n)) for i in range(n));W=K
    for t in sorted(removed):W,A,_=insert(W,A,p,t)
    assert W==U and len(A)==len(P)
    assert all(min(row)>=0 and sum(row)==1 for row in A)
    fixed={}
    for row,pt in zip(A,P):
        if row.count(F(1))==1:
            j=row.index(F(1));assert j not in fixed or fixed[j]==pt;fixed[j]=pt
    free=[j for j in range(n) if j not in fixed]
    residual=tuple(tuple(pt[d]-sum(row[j]*q[d] for j,q in fixed.items()) for d in range(dim)) for row,pt in zip(A,P))
    if free:
        gram=tuple(tuple(sum(row[i]*row[j] for row in A) for j in free) for i in free)
        rhs=tuple(tuple(sum(row[i]*r[d] for row,r in zip(A,residual)) for d in range(dim)) for i in free)
        solution=solve(gram,rhs);fixed.update(zip(free,solution))
    Q=tuple(fixed[j] for j in range(n))
    reconstructed=tuple(tuple(sum(row[j]*Q[j][d] for j in range(n)) for d in range(dim)) for row in A)
    errors=tuple(tuple(a-b for a,b in zip(old,new)) for old,new in zip(P,reconstructed))
    # Orthogonality verifies the exact local least-squares solution.
    assert all(sum(row[j]*e[d] for row,e in zip(A,errors))==0 for j in free for d in range(dim))
    bound=max(sum(map(abs,e)) for e in errors)
    return K,Q,{'removed_knots':list(map(str,removed)),
                'fixed_unaffected_control_indices':sorted(j for j in range(n) if j not in free),
                'solved_control_indices':free,'exact_normal_equation_residuals_zero':True,
                'common_basis_control_residuals':[[str(t) for t in pt] for pt in errors],
                'certified_whole_domain_L1_error_bound_cm':str(bound),
                'curve_exactly_unchanged':bound==0,'method':'local least-squares inverse knot insertion; unaffected controls fixed'}

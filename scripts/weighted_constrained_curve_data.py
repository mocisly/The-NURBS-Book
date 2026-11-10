"""Shared representative21data and exact weighted/constrained least-squares solver."""
from fractions import Fraction as F
from math import isqrt
from least_squares_curve_data import knots
from surface_geometry import weights as basis_weights
from inverse_knot_projection import solve
from native_bspline import segments,check,de_boor
from bspline_math import piece,derivative,evaluate
Q=tuple(tuple(map(F,p)) for p in [('0','0'),('.4','.8'),('.8','1.6'),('1.2','2.3'),('1.5','3'),('2.1','3'),('2.8','3'),('3.4','3'),('3.6','2.4'),('3.7','1.8'),('3.8','1.2'),('4.1','.6'),('4.3','0'),('4.6','-.6'),('5.2','-.6'),('5.8','-.6'),('6.4','-.6'),('6.8','.2'),('7.2','1'),('7.5','1.8'),('7.8','2.5')])
SCALE=10**12;squares=tuple(sum((a-b)**2 for a,b in zip(x,y)) for x,y in zip(Q,Q[1:]))
LO=tuple(F(isqrt(s.numerator*SCALE*SCALE//s.denominator),SCALE) for s in squares);HI=tuple(x+F(1,SCALE) for x in LO)
assert all(a*a<=s<b*b for a,b,s in zip(LO,HI,squares))
PARAMS=(F(0),)+tuple(sum(LO[:i])/sum(LO) for i in range(1,len(Q)-1))+(F(1),)
BOUNDS=tuple((sum(LO[:i])/sum(HI),sum(HI[:i])/sum(LO)) for i in range(1,len(Q)-1))
assert all(a<=t<=b and b-a<F(1,10**11) for t,(a,b) in zip(PARAMS[1:-1],BOUNDS))
COUNT=10;U=knots(PARAMS,COUNT)
ROWS=tuple(tuple(basis_weights(U,3,t)) for t in PARAMS)
def derivative_row(t):
    span=next((i for i in range(3,COUNT) if U[i]<=t<U[i+1]),COUNT-1)
    return tuple(evaluate(derivative(piece(U,i,3,span)),t) for i in range(COUNT))
def fit(point_weights=None,point_constraints=(),derivative_constraints=None):
    w=tuple(F(1 if point_weights is None else point_weights.get(i,1)) for i in range(len(Q)));assert min(w)>0
    point_constraints=tuple(point_constraints);derivative_constraints=derivative_constraints or {}
    ids=tuple(i for i in range(len(Q)) if i not in point_constraints)
    G=tuple(tuple(sum(w[k]*ROWS[k][i]*ROWS[k][j] for k in ids) for j in range(COUNT)) for i in range(COUNT))
    R=tuple(tuple(sum(w[k]*ROWS[k][i]*Q[k][d] for k in ids) for d in range(2)) for i in range(COUNT))
    M=tuple(ROWS[k] for k in point_constraints)+tuple(derivative_row(PARAMS[k]) for k in derivative_constraints)
    targets=tuple(Q[k] for k in point_constraints)+tuple(tuple(map(F,D)) for D in derivative_constraints.values());nc=len(M)
    # The Gram matrix is positive definite for each chosen sampling/constraint set.
    L=[[F(i==j) for j in range(COUNT)] for i in range(COUNT)];D=[]
    for j in range(COUNT):
        dj=G[j][j]-sum(L[j][k]**2*D[k] for k in range(j));assert dj>0;D.append(dj)
        for i in range(j+1,COUNT):L[i][j]=(G[i][j]-sum(L[i][k]*L[j][k]*D[k] for k in range(j)))/dj
    if nc:
        K=tuple(tuple(G[i])+tuple(row[i] for row in M) for i in range(COUNT))+tuple(tuple(row)+(F(0),)*nc for row in M)
        solution=solve(K,R+targets);P=solution[:COUNT];multipliers=solution[COUNT:]
    else:P=solve(G,R);multipliers=()
    assert all(tuple(sum(row[i]*P[i][d] for i in range(COUNT)) for d in range(2))==target for row,target in zip(M,targets))
    assert all(sum(G[i][j]*P[j][d] for j in range(COUNT))+sum(M[j][i]*multipliers[j][d] for j in range(nc))==R[i][d] for i in range(COUNT) for d in range(2))
    residual=tuple(tuple(a-b for a,b in zip(de_boor(U,P,3,t),q)) for t,q in zip(PARAMS,Q))
    objective=sum(w[k]*sum(x*x for x in residual[k]) for k in ids)
    ss=segments(U,P,3);native=check(U,P,3,ss)
    report=dict(point_weights={str(i):str(x) for i,x in enumerate(w) if x!=1},point_constraints=list(point_constraints),derivative_constraints={str(k):list(map(str,D)) for k,D in derivative_constraints.items()},all_hard_constraints_exact=True,KKT_gradient_equations_exact=True,Gram_LDL_positive_pivots=True,weighted_objective_decimal=float(objective),point_residuals=[list(map(str,r)) for r in residual],point_squared_residuals=[str(sum(x*x for x in r)) for r in residual],endpoint_residual_lengths=[float(sum(x*x for x in residual[k]))**.5 for k in (0,-1)],controls=[list(map(str,p)) for p in P],native_C2_checks=native)
    return P,ss,report

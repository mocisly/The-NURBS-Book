"""Exact endpoint-constrained least-squares fits with Eq9.68/69knots."""
from fractions import Fraction as F
from math import isqrt
from surface_geometry import weights
from inverse_knot_projection import solve
from native_bspline import segments,check,de_boor
Q=tuple(tuple(map(F,p)) for p in [('0','0'),('.9','.2'),('1.5','.5'),('1.8','1.5'),('2','2.3'),('2.2','3'),('2.35','3.5'),('2.65','3.5'),('3.3','3.5'),('3.8','3.5'),('3.8','2.8'),('3.8','1.9'),('3.8','1.2'),('4.1','.6'),('4.8','0'),('5.7','0'),('6.4','0'),('7','0')])
SCALE=10**12
squares=tuple(sum((x-y)**2 for x,y in zip(a,b)) for a,b in zip(Q,Q[1:]))
LO=tuple(F(isqrt(s.numerator*SCALE*SCALE//s.denominator),SCALE) for s in squares);HI=tuple(x+F(1,SCALE) for x in LO)
assert all(a*a<=s<b*b for a,b,s in zip(LO,HI,squares))
PARAMS=(F(0),)+tuple(sum(LO[:i])/sum(LO) for i in range(1,len(Q)-1))+(F(1),)
BOUNDS=tuple((sum(LO[:i])/sum(HI),sum(HI[:i])/sum(LO)) for i in range(1,len(Q)-1))
assert all(a<=t<=b and b-a<F(1,10**11) for t,(a,b) in zip(PARAMS[1:-1],BOUNDS))
def knots(params,count,p=3):
    m=len(params)-1;n=count-1;d=F(m+1,n-p+1);inside=[]
    for j in range(1,n-p+1):
        x=j*d;i=x.numerator//x.denominator;alpha=x-i;inside.append((1-alpha)*params[i-1]+alpha*params[i])
    U=(F(0),)*(p+1)+tuple(inside)+(F(1),)*(p+1)
    assert all(a<b for a,b in zip((F(0),)+tuple(inside),tuple(inside)+(F(1),)))
    assert all(any(a<=t<=b for t in params) for a,b in zip(U[p:count],U[p+1:count+1]) if a<b)
    return U
def fit(count):
    U=knots(PARAMS,count);W=tuple(tuple(weights(U,3,t)) for t in PARAMS[1:-1]);A=tuple(row[1:-1] for row in W)
    rhs=tuple(tuple(q[d]-row[0]*Q[0][d]-row[-1]*Q[-1][d] for d in range(2)) for q,row in zip(Q[1:-1],W))
    G=tuple(tuple(sum(row[i]*row[j] for row in A) for j in range(count-2)) for i in range(count-2))
    R=tuple(tuple(sum(row[i]*r[d] for row,r in zip(A,rhs)) for d in range(2)) for i in range(count-2))
    # Exact LDL^Tpositive pivots establish strict convexity/unique minimizer.
    L=[[F(i==j) for j in range(count-2)] for i in range(count-2)];D=[]
    for j in range(count-2):
        dj=G[j][j]-sum(L[j][k]**2*D[k] for k in range(j));assert dj>0;D.append(dj)
        for i in range(j+1,count-2):L[i][j]=(G[i][j]-sum(L[i][k]*L[j][k]*D[k] for k in range(j)))/dj
    inner=solve(G,R);P=(Q[0],)+inner+(Q[-1],);residual=[]
    for q,t in zip(Q,PARAMS):residual.append(tuple(x-y for x,y in zip(de_boor(U,P,3,t),q)))
    assert residual[0]==residual[-1]==(0,0)
    assert all(sum(row[i]*e[d] for row,e in zip(A,residual[1:-1]))==0 for i in range(count-2) for d in range(2))
    sse=sum(sum(x*x for x in e) for e in residual);assert sse>0
    ss=segments(U,P,3);nc=check(U,P,3,ss)
    return U,P,ss,dict(control_count=count,knots=list(map(str,U)),controls=[list(map(str,p)) for p in P],normal_equation_gradient_exactly_zero=True,LDL_positive_pivots=True,endpoint_constraints_exact=True,sum_squared_residual=str(sse),sum_squared_residual_decimal=float(sse),RMS_same_parameter_residual=(float(sse)/len(Q))**.5,native_C2_checks=nc)

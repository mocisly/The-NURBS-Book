"""A9.7 tensor least squares, shared certified parameters for9.45..47."""
from fractions import Fraction as F
from math import isqrt
from functools import lru_cache
from surface_approximation_example_data import Q
from least_squares_curve_data import knots
from surface_geometry import weights,surface
from inverse_knot_projection import solve
SCALE=10**12
GRID=10**10

def sqrt_bounds(s):
    a=F(isqrt(s.numerator*SCALE*SCALE//s.denominator),SCALE)
    b=a+F(1,SCALE)
    assert a*a<=s<b*b
    return a,b

def mesh_parameters():
    result=[];proof=[]
    for lines in (tuple(zip(*Q)),Q):
        all_values=[];all_bounds=[]
        for row in lines:
            lengths=[sqrt_bounds(sum((b-a)**2 for a,b in zip(A,B))) for A,B in zip(row,row[1:])]
            lo=[a for a,b in lengths];hi=[b for a,b in lengths]
            all_values.append((F(0),)+tuple(sum(lo[:i])/sum(lo) for i in range(1,8))+(F(1),))
            all_bounds.append(((F(0),F(0)),)+tuple((sum(lo[:i])/sum(hi),sum(hi[:i])/sum(lo)) for i in range(1,8))+((F(1),F(1)),))
        raw=tuple(sum(row[i] for row in all_values)/len(lines) for i in range(9))
        values=tuple(F((t*GRID+F(1,2)).numerator//(t*GRID+F(1,2)).denominator,GRID) for t in raw)
        bounds=tuple(tuple(sum(row[i][j] for row in all_bounds)/len(lines) for j in (0,1)) for i in range(9))
        errors=tuple(max(abs(t-a),abs(t-b)) for t,(a,b) in zip(values,bounds))
        assert all(e<F(1,10**10) for e in errors)
        assert values[0]==0 and values[-1]==1 and all(a<b for a,b in zip(values,values[1:]))
        result.append(values);proof.append(dict(values=list(map(str,values)),true_parameter_enclosures=[[str(a),str(b)] for a,b in bounds],maximum_error_bound=float(max(errors))))
    return tuple(result),proof

(UP,VP),PARAMETER_PROOF=mesh_parameters()

@lru_cache(None)
def operator(params,count,p):
    U=knots(params,count,p);W=tuple(tuple(weights(U,p,t)) for t in params)
    A=tuple(row[1:-1] for row in W[1:-1]);n=count-2;m=len(params)
    G=tuple(tuple(sum(row[i]*row[j] for row in A) for j in range(n)) for i in range(n))
    L=[[F(i==j) for j in range(n)] for i in range(n)];D=[]
    for j in range(n):
        dj=G[j][j]-sum(L[j][k]**2*D[k] for k in range(j));assert dj>0;D.append(dj)
        for i in range(j+1,n):L[i][j]=(G[i][j]-sum(L[i][k]*L[j][k]*D[k] for k in range(j)))/dj
    R=tuple(tuple(sum(A[k][i]*(F(k+1==j)-W[k+1][0]*F(j==0)-W[k+1][-1]*F(j==m-1)) for k in range(m-2)) for j in range(m)) for i in range(n))
    T=(tuple(F(j==0) for j in range(m)),)+solve(G,R)+(tuple(F(j==m-1) for j in range(m)),)
    E=tuple(tuple(sum(W[k][i]*T[i][j] for i in range(count))-F(k==j) for j in range(m)) for k in range(m))
    assert not any(E[0]) and not any(E[-1])
    assert all(sum(A[k][i]*E[k+1][j] for k in range(m-2))==0 for i in range(n) for j in range(m))
    return U,T,dict(control_count=count,degree=p,knots=list(map(str,U)),positive_LDL_pivots=True,linear_operator_normal_equations_exact=True,endpoint_constraints_exact=True)

def fit(nu,nv,p=2,q=3):
    U,A,pa=operator(UP,nu,p);V,B,pb=operator(VP,nv,q)
    temp=tuple(tuple(tuple(sum(A[a][i]*Q[i][j][d] for i in range(9)) for d in range(3)) for j in range(9)) for a in range(nu))
    P=tuple(tuple(tuple(sum(B[b][j]*temp[a][j][d] for j in range(9)) for d in range(3)) for b in range(nv)) for a in range(nu))
    other=tuple(tuple(tuple(sum(B[b][j]*Q[i][j][d] for j in range(9)) for d in range(3)) for b in range(nv)) for i in range(9))
    reverse=tuple(tuple(tuple(sum(A[a][i]*other[i][b][d] for i in range(9)) for d in range(3)) for b in range(nv)) for a in range(nu))
    assert P==reverse
    base=(U,V,p,q,P)
    E=tuple(tuple(tuple(a-b for a,b in zip(surface(*base,u,v),Q[i][j])) for j,v in enumerate(VP)) for i,u in enumerate(UP))
    squares=tuple(tuple(sum(x*x for x in e) for e in row) for row in E)
    assert all(squares[i][j]==0 for i in (0,8) for j in (0,8))
    sse=sum(map(sum,squares));assert sse>0
    report=dict(control_shape=[nu,nv],degrees=[p,q],u_fit=pa,v_fit=pb,common_parameters=PARAMETER_PROOF,reverse_order_controls_exactly_identical=True,four_corner_interpolations_exact=True,squared_error_values=[[str(s) for s in row] for row in squares],sum_squared_error=float(sse),RMS_same_parameter_3D_error=(float(sse)/81)**.5,maximum_same_parameter_3D_error=float(max(map(max,squares)))**.5)
    return base,squares,report

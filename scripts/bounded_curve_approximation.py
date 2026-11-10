"""Degree1->3,greedy bounded removal/refits;conservative L1point error budgets.

Follows A9.10's stages,with explicitly documented conservative bound variant:
each removal uses exact common-basis inverse insertion and per-datum L1change,
accumulated by the triangle inequality. Projection is numerical only for choosing
parameters; every candidate distance/budget is re-evaluated with exact rationals.
"""
from fractions import Fraction as F
from math import isqrt
from collections import Counter
from inverse_knot_projection import remove_to,solve
from degree_elevation_geometry import elevate_spline
from native_bspline import de_boor,segments
from surface_geometry import weights
from bspline_math import evaluate,derivative

def chord_parameters(Q):
    scale=10**12;grid=10**8;lengths=[]
    for a,b in zip(Q,Q[1:]):
        s=sum((x-y)**2 for x,y in zip(a,b));lo=F(isqrt(s.numerator*scale*scale//s.denominator),scale);hi=lo+F(1,scale)
        assert lo*lo<=s<hi*hi;lengths.append((lo,hi))
    lo=[a for a,b in lengths];hi=[b for a,b in lengths];raw=(F(0),)+tuple(sum(lo[:i])/sum(lo) for i in range(1,len(Q)-1))+(F(1),)
    params=tuple(F((t*grid+F(1,2)).numerator//(t*grid+F(1,2)).denominator,grid) for t in raw)
    bounds=((F(0),F(0)),)+tuple((sum(lo[:i])/sum(hi),sum(hi[:i])/sum(lo)) for i in range(1,len(Q)-1))+((F(1),F(1)),)
    err=max(max(abs(t-a),abs(t-b)) for t,(a,b) in zip(params,bounds));assert err<F(1,10**8)
    assert all(a<b for a,b in zip(params,params[1:]))
    return params,float(err)

def point_errors(U,P,p,Q,params):
    return tuple(sum(abs(x-y) for x,y in zip(de_boor(U,P,p,t),q)) for t,q in zip(params,Q))

def consistent_solve(A,B):
    """Exact compatible singular system,zero free increments about baseline."""
    n=len(A);dim=len(B[0]);R=[list(a)+list(b) for a,b in zip(A,B)];pivots=[];r=0
    for j in range(n):
        pivot=next((i for i in range(r,n) if R[i][j]),None)
        if pivot is None:continue
        R[r],R[pivot]=R[pivot],R[r];value=R[r][j];R[r]=[x/value for x in R[r]]
        for i in range(n):
            if i==r:continue
            factor=R[i][j]
            if factor:R[i]=[a-factor*b for a,b in zip(R[i],R[r])]
        pivots.append(j);r+=1
    assert all(not any(row[n:]) for row in R[r:])
    X=[[F(0)]*dim for _ in range(n)]
    for i,j in enumerate(pivots):X[j]=R[i][n:]
    return tuple(map(tuple,X))

def fit(Q,params,U,p,baseline):
    count=len(U)-p-1;n=count-2;W=tuple(tuple(weights(U,p,t)) for t in params[1:-1]);A=tuple(row[1:-1] for row in W)
    residual=tuple(tuple(q[d]-row[0]*Q[0][d]-row[-1]*Q[-1][d] for d in range(len(q))) for row,q in zip(W,Q[1:-1]))
    G=tuple(tuple(sum(row[i]*row[j] for row in A) for j in range(n)) for i in range(n))
    R=tuple(tuple(sum(row[i]*q[d] for row,q in zip(A,residual)) for d in range(len(Q[0]))) for i in range(n))
    base=baseline[1:-1]
    delta=tuple(tuple(q[d]-sum(row[j]*base[j][d] for j in range(n)) for d in range(len(q))) for row,q in zip(A,residual))
    if n>len(A):
        # Under-determined stages use the least control change about the exact
        # elevated curve. This is an actual LS minimizer,not a rank failure.
        H=tuple(tuple(sum(a*b for a,b in zip(row,col)) for col in A) for row in A)
        try:
            multipliers=solve(H,delta)
            increments=tuple(tuple(sum(A[k][j]*multipliers[k][d] for k in range(len(A))) for d in range(len(Q[0]))) for j in range(n))
        except StopIteration:
            rhs=tuple(tuple(sum(row[j]*v[d] for row,v in zip(A,delta)) for d in range(len(Q[0]))) for j in range(n));increments=consistent_solve(G,rhs)
    else:
        rhs=tuple(tuple(sum(row[j]*v[d] for row,v in zip(A,delta)) for d in range(len(Q[0]))) for j in range(n))
        try:increments=solve(G,rhs)
        except StopIteration:increments=consistent_solve(G,rhs)
    inner=tuple(tuple(a+b for a,b in zip(x,y)) for x,y in zip(base,increments));P=(Q[0],)+inner+(Q[-1],)
    assert all(sum(row[i]*(sum(row[j]*inner[j][d] for j in range(n))-q[d]) for row,q in zip(A,residual))==0 for i in range(n) for d in range(len(Q[0])))
    return P

def refit(Q,params,U,p,P,hard_indices=()):
    if not hard_indices:return fit(Q,params,U,p,P)
    ends=[(0,0)]
    for i in hard_indices:
        t=params[i];w=weights(U,p,t);assert U.count(t)==p and w.count(F(1))==1
        ends.append((i,w.index(F(1))))
    ends.append((len(Q)-1,len(P)-1));result=()
    for (a,i),(b,j) in zip(ends,ends[1:]):
        K=(params[a],)*(p+1)+tuple(t for t in U if params[a]<t<params[b])+(params[b],)*(p+1)
        C=fit(Q[a:b+1],params[a:b+1],K,p,P[i:j+1]);result+=C if not result else C[1:]
    assert len(result)==len(P)
    assert all(de_boor(U,result,p,params[i])==Q[i] for i in hard_indices)
    return result

def project(Q,U,P,p,params,hard_indices=()):
    """Search each polynomial span for improving stationary points; exact acceptance."""
    ss=segments(U,P,p);pieces=[([tuple(map(float,c)) for c in s['power']],float(s['a']),float(s['b'])) for s in ss]
    result=[]
    for i,(q,old) in enumerate(zip(Q,params)):
        if i in (0,len(Q)-1) or i in hard_indices:result.append(old);continue
        best=old;best_sq=sum((x-y)**2 for x,y in zip(de_boor(U,P,p,best),q))
        if best_sq==0:result.append(old);continue
        low=float((params[i-1]+old)/2);high=float((old+params[i+1])/2)
        for coeff,a,b in pieces:
            a=max(a,low);b=min(b,high)
            if a>=b:continue
            d=[derivative(c) for c in coeff];dd=[derivative(c) for c in d]
            for start in (a,(a+b)/2,b):
                t=start
                for _ in range(12):
                    v=[evaluate(c,t)-float(x) for c,x in zip(coeff,q)];dv=[evaluate(c,t) for c in d];ddv=[evaluate(c,t) for c in dd]
                    first=sum(x*y for x,y in zip(v,dv));second=sum(x*x for x in dv)+sum(x*y for x,y in zip(v,ddv))
                    if abs(second)<1e-14:break
                    nxt=max(a,min(b,t-first/second))
                    if abs(nxt-t)<1e-12:t=nxt;break
                    t=nxt
                candidate=F(round(t*10**8),10**8)
                if not params[i-1]<candidate<params[i+1]:continue
                sq=sum((x-y)**2 for x,y in zip(de_boor(U,P,p,candidate),q))
                if sq<best_sq:best,best_sq=candidate,sq
        result.append(best)
    result=tuple(result)
    assert all(a<b for a,b in zip(result,result[1:]))
    return result

def reduce(Q,params,U,P,p,E,errors,protected=()):
    history=[]
    while True:
        choices=[];old_values=tuple(de_boor(U,P,p,t) for t in params)
        for t in sorted(set(U[p+1:-p-1])):
            if t in protected:continue
            V,C,proof=remove_to(U,P,p,(t,))
            changes=tuple(sum(abs(x-y) for x,y in zip(de_boor(V,C,p,s),old)) for s,old in zip(params,old_values))
            budget=tuple(a+b for a,b in zip(errors,changes));maximum=max(budget)
            if maximum<=E:choices.append((max(changes),t,V,C,budget,maximum))
        if not choices:break
        _,t,U,P,errors,maximum=min(choices,key=lambda x:(x[0],x[1]));history.append(dict(knot=str(t),remaining_controls=len(P),accumulated_L1_error_bound=float(maximum)))
        assert all(a<=b<=E for a,b in zip(point_errors(U,P,p,Q,params),errors))
    return U,P,errors,history

def smooth_triples(Q,params,U,P,E,hard_indices=()):
    """Optional final remove/refit check for artificial C0 joins in smooth data."""
    history=[]
    for t in sorted(set(U[4:-4])):
        if t in tuple(params[i] for i in hard_indices):continue
        if U.count(t)<3:continue
        V,C,_=remove_to(U,P,3,(t,));C=refit(Q,params,V,3,C,hard_indices);TP=project(Q,V,C,3,params,hard_indices);err=point_errors(V,C,3,Q,TP)
        if max(err)<=E and all(min(q[d] for q in Q)-2<=c[d]<=max(q[d] for q in Q)+2 for c in C for d in range(len(Q[0]))):
            U,P,params=V,C,TP;history.append(dict(knot=str(t),multiplicity_reduced_to=U.count(t),exact_normal_equations=True,maximum_exact_L1_error=float(max(err))))
    return U,P,params,history

def approximate(Q,E,hard_indices=()):
    params,paramerr=chord_parameters(Q);U=(F(0),F(0))+params[1:-1]+(F(1),F(1));P=Q;errors=(F(0),)*len(Q);stages=[]
    protected=tuple(params[i] for i in hard_indices)
    hull=tuple((min(q[d] for q in Q)-2,max(q[d] for q in Q)+2) for d in range(len(Q[0])))
    def regular(C):return all(a<=c[d]<=b for c in C for d,(a,b) in enumerate(hull))
    for p in (1,2,3):
        U,P,errors,history=reduce(Q,params,U,P,p,E,errors,protected)
        stages.append(dict(degree=p,controls=len(P),removed=history,maximum_accumulated_L1_bound=float(max(errors))))
        print('degree',p,'controls',len(P),'removed',len(history),'bound',float(max(errors)),flush=True)
        if p==3:break
        U,P,elevate_proof=elevate_spline(U,P,p,1);stages[-1]['exact_elevation']=elevate_proof
        try:
            candidate=refit(Q,params,U,p+1,P,hard_indices);new_params=project(Q,U,candidate,p+1,params,hard_indices);candidate_errors=point_errors(U,candidate,p+1,Q,new_params)
            accept=max(candidate_errors)<=E and regular(candidate)
            if accept:P,params,errors=candidate,new_params,candidate_errors
            stages[-1]['least_squares_refit_accepted']=accept
            stages[-1]['refit_exact_normal_equations']=True
        except StopIteration:
            stages[-1]['least_squares_refit_accepted']=False;stages[-1]['reason']='rank deficient data collocation; retained exact elevated bounded curve'
    # Final endpoint-constrained refit and exact-distance-checked parameter update.
    candidate=refit(Q,params,U,3,P,hard_indices);candidate_params=project(Q,U,candidate,3,params,hard_indices);candidate_errors=point_errors(U,candidate,3,Q,candidate_params)
    final_accept=max(candidate_errors)<=E and regular(candidate)
    if final_accept:P,params,errors=candidate,candidate_params,candidate_errors
    U,P,errors,history=reduce(Q,params,U,P,3,E,errors,protected)
    U,P,params,smoothing=smooth_triples(Q,params,U,P,E,hard_indices)
    if smoothing:errors=point_errors(U,P,3,Q,params)
    actual=point_errors(U,P,3,Q,params);assert max(actual)<=max(errors)<=E and regular(P)
    assert all(de_boor(U,P,3,params[i])==Q[i] and U.count(params[i])==3 for i in hard_indices)
    return U,P,params,dict(tolerance=str(E),chord_parameter_error_bound=paramerr,stages=stages,final_refit_accepted=final_accept,final_removals=history,final_smoothness_refits=smoothing,actual_maximum_L1_error=float(max(actual)),certified_maximum_accumulated_L1_bound=float(max(errors)),actual_same_parameter_L1_errors=list(map(str,actual)),parameters=list(map(str,params)),internal_multiplicities={str(t):U.count(t) for t in sorted(set(U[4:-4]))},variant='A9.10stages,exact inverse insertion,conservative accumulated per-datum L1error budget;final C0join removal/refit accepted only after exact datum error check;float stationary search used only to choose exact-checked rational parameters')

"""Planar A9.12point+tangent LS,average handles,actual checked deviations.

Individual LS constructions may have nonzero point residuals. Therefore the
Eq9.110 shortcut is not assumed: ALL accepted distances are evaluated directly.
"""
from fractions import Fraction as F
from math import sqrt
from bounded_curve_approximation import chord_parameters
from local_quadratic_interpolator import unit,length,cross,dot,add,mul
from inverse_knot_projection import solve,remove_to
from native_bspline import de_boor

def closest_candidate(P,q):
    C=tuple(tuple(map(float,p)) for p in P);Q=tuple(map(float,q))
    def distance(t):
        s=1-t;B=(s*s*s,3*s*s*t,3*s*t*t,t*t*t)
        return sum((sum(B[i]*C[i][d] for i in range(4))-Q[d])**2 for d in range(len(Q)))
    j=min(range(65),key=lambda j:distance(j/64));a=max(0,(j-1)/64);b=min(1,(j+1)/64);ratio=(sqrt(5)-1)/2
    x=b-ratio*(b-a);y=a+ratio*(b-a);fx,fy=distance(x),distance(y)
    for _ in range(75):
        if fx<fy:b,y,fy=y,x,fx;x=b-ratio*(b-a);fx=distance(x)
        else:a,x,fx=x,y,fy;y=a+ratio*(b-a);fy=distance(y)
    t=F(round((a+b)/2*10**14),10**14);point=de_boor((F(0),)*4+(F(1),)*4,P,3,t)
    return t,sum((x-y)**2 for x,y in zip(point,q))

def round_scalar(x):return F((x*10**12+F(1,2)).numerator//(x*10**12+F(1,2)).denominator,10**12)

def fit_planar_segment(Q,T,params,start,end,E):
    A,B=Q[start],Q[end];Ts,Te=T[start],T[end];aa=[];bb=[];individual=[]
    if end==start+1:
        alpha=length(add(B,A,-1))/3;beta=-alpha
    else:
        for k in range(start+1,end):
            t=(params[k]-params[start])/(params[end]-params[start]);s=1-t;Tp=T[k]
            matrix=[(3*s*s*t*Ts[d],3*s*t*t*Te[d]) for d in range(2)]
            rhs=[Q[k][d]-(s**3+3*s*s*t)*A[d]-(t**3+3*s*t*t)*B[d] for d in range(2)]
            matrix.append((s*(s-2*t)*cross(Tp,Ts),t*(2*s-t)*cross(Tp,Te)));rhs.append(2*s*t*cross(Tp,add(A,B,-1)))
            G=tuple(tuple(sum(row[i]*row[j] for row in matrix) for j in range(2)) for i in range(2));R=tuple((sum(row[i]*r for row,r in zip(matrix,rhs)),) for i in range(2))
            try:solution=solve(G,R)
            except StopIteration:return None
            a,b=(x[0] for x in solution)
            if a<=0 or b>=0:return None
            residual=tuple(row[0]*a+row[1]*b-r for row,r in zip(matrix,rhs));assert all(sum(row[i]*r for row,r in zip(matrix,residual))==0 for i in range(2))
            ar,br=round_scalar(a),round_scalar(b)
            if ar<=0 or br>=0:return None
            assert abs(ar-a)<=F(1,2*10**12) and abs(br-b)<=F(1,2*10**12)
            aa.append(ar);bb.append(br);individual.append(dict(index=k,parameter=str(t),normal_gradient_exactly_zero=True,point_tangent_constraints_compatible=not any(residual),handle_rounding_error_bound='5e-13'))
        alpha=sum(aa)/len(aa);beta=sum(bb)/len(bb)
    P=(A,add(A,Ts,alpha),add(B,Te,beta),B);projections=[F(0)];squares=[F(0)]
    for q in Q[start+1:end]:
        t,sq=closest_candidate(P,q)
        if sq>(E-F(1,10**7))**2:return None
        projections.append(t);squares.append(sq)
    projections.append(F(1));squares.append(F(0))
    if not all(a<b for a,b in zip(projections,projections[1:])):return None
    return dict(start=start,end=end,controls=P,alpha=alpha,beta=beta,individual_LS=individual,projection_parameters=tuple(projections),squared_distances=tuple(squares),maximum_distance=float(max(squares))**.5)

def stitch_C1(pieces):
    spans=[F(1)]
    for a,b in zip(pieces,pieces[1:]):spans.append(spans[-1]*b['alpha']/(-a['beta']))
    total=sum(spans);spans=tuple(x/total for x in spans);knots=tuple(sum(spans[:i]) for i in range(len(spans)+1))
    assert knots[0]==0 and knots[-1]==1 and min(spans)>0
    P=pieces[0]['controls']+tuple(q for p in pieces[1:] for q in p['controls'][1:]);U=(F(0),)*4+tuple(t for t in knots[1:-1] for _ in range(3))+(F(1),)*4
    for i,(a,b) in enumerate(zip(pieces,pieces[1:])):
        left=mul(add(a['controls'][-1],a['controls'][-2],-1),3/spans[i]);right=mul(add(b['controls'][1],b['controls'][0],-1),3/spans[i+1]);assert left==right
    if knots[1:-1]:
        U,P,proof=remove_to(U,P,3,knots[1:-1]);assert proof['curve_exactly_unchanged']
    else:proof=dict(curve_exactly_unchanged=True)
    checks=0
    for i,piece in enumerate(pieces):
        for j in range(11):
            t=F(j,10);assert de_boor(U,P,3,knots[i]+spans[i]*t)==de_boor((F(0),)*4+(F(1),)*4,piece['controls'],3,t);checks+=1
    assert all(U.count(t)==2 for t in knots[1:-1])
    return U,P,knots,dict(exact_C1_every_join=True,all_internal_knots_double=True,exact_knot_removal=proof,global_local_piece_checks=checks)

def approximate_planar(Q,D,E,Kmax):
    T=tuple(unit(d) for d in D);params,paramerr=chord_parameters(Q);pieces=[];start=0;trials=0
    while start<len(Q)-1:
        for end in range(min(start+Kmax,len(Q)-1),start,-1):
            trials+=1;piece=fit_planar_segment(Q,T,params,start,end,E)
            if piece is not None:break
        assert piece is not None;pieces.append(piece);start=end
    U,P,knots,proof=stitch_C1(pieces)
    return U,P,pieces,dict(tolerance=str(E),Kmax=Kmax,segments=len(pieces),control_count=len(P),common_chord_parameter_error_bound=paramerr,maximum_exact_checked_datum_distance=max(p['maximum_distance'] for p in pieces),all_datum_distance_squares_exactly_checked=True,individual_point_tangent_LS_normal_gradients_exact=True,individual_LS_may_have_nonzero_point_residual=True,all_actual_distances_checked_without_9_110_shortcut=True,joins=proof,segment_boundaries=[0]+[p['end'] for p in pieces],segment_global_parameters=list(map(str,knots)),candidate_trials=trials)

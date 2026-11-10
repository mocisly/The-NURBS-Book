"""A9.11shoulder-average conics;exhaustive longest segment search withinKmax.

Numerical distance search only supplies rational candidate parameters. Every
accepted datum distance is then checked exactly with a margin for analytic-data
rounding and native plotting. This certifies an upper distance bound,without
claiming every search value is the exact global nearest point.
"""
from fractions import Fraction as F
from math import isqrt,sqrt
from rational_geometry import evaluate,project
from local_quadratic_interpolator import cross,add,dot
from bounded_curve_approximation import chord_parameters
from native_bspline import de_boor
from log_spiral_data import Q,DIRECTIONS,TRUE_POINT_L1_ERROR_BOUND
PARAMS,PARAM_ERROR=chord_parameters(Q)

def sqrt_bounds(s):
    scale=10**30;a=F(isqrt(s.numerator*scale*scale//s.denominator),scale);b=a+F(1,scale)
    assert a*a<=s<b*b;return a,b

def closest_candidate(H,q):
    controls=tuple(tuple(map(float,p)) for p in H);qq=tuple(map(float,q))
    def distance(t):
        a,b=(1-t)**2,t*t;c=2*t*(1-t)
        W=a*controls[0][-1]+c*controls[1][-1]+b*controls[2][-1]
        return sum(((a*controls[0][d]+c*controls[1][d]+b*controls[2][d])/W-qq[d])**2 for d in range(2))
    j=min(range(65),key=lambda j:distance(j/64));a=max(0,(j-1)/64);b=min(1,(j+1)/64)
    ratio=(sqrt(5)-1)/2;x=b-ratio*(b-a);y=a+ratio*(b-a);fx=distance(x);fy=distance(y)
    for _ in range(75):
        if fx<fy:b,y,fy=y,x,fx;x=b-ratio*(b-a);fx=distance(x)
        else:a,x,fx=x,y,fy;y=a+ratio*(b-a);fy=distance(y)
    t=F(round((a+b)/2*10**14),10**14);p=project(evaluate(H,t));sq=sum((x-y)**2 for x,y in zip(p,q))
    return t,sq

def fit_segment(start,end,E):
    A,B=Q[start],Q[end];Ts,Te=DIRECTIONS[start],DIRECTIONS[end];den=cross(Ts,Te)
    if not den:return None
    delta=add(B,A,-1);alpha=cross(delta,Te)/den;beta=cross(delta,Ts)/den
    if alpha<=0 or beta>=0:return None
    R=add(A,Ts,alpha);assert R==add(B,Te,beta)
    tri=cross(add(R,A,-1),delta);values=[];errors=[]
    for q in Q[start+1:end]:
        v=add(q,A,-1);lr=cross(v,delta)/tri;lb=cross(add(R,A,-1),v)/tri;la=1-lr-lb
        if min(la,lb,lr)<=0:return None
        lo,hi=sqrt_bounds(la*lb);lower=lr/(lr+2*hi);upper=lr/(lr+2*lo);mid=(lower+upper)/2
        s=F((mid*10**16+F(1,2)).numerator//(mid*10**16+F(1,2)).denominator,10**16)
        error=max(abs(s-lower),abs(s-upper));assert error<F(1,10**14)
        values.append(s);errors.append(error)
    s=sum(values)/len(values) if values else F(1,2);w=s/(1-s)
    if not F(1,100)<w<100:return None
    H=(A+(F(1),),tuple(w*x for x in R)+(w,),B+(F(1),));params=[F(0)];squares=[F(0)]
    for point in Q[start+1:end]:
        t,sq=closest_candidate(H,point)
        if sq>(E-F(1,10**6))**2:return None
        params.append(t);squares.append(sq)
    params.append(F(1));squares.append(F(0))
    if not all(a<b for a,b in zip(params,params[1:])):return None
    assert all(sq<(E-TRUE_POINT_L1_ERROR_BOUND)**2 for sq in squares)
    return dict(start=start,end=end,R=R,weight=w,H=H,shoulder_mean=s,shoulder_rounding_bound=max(errors,default=F(0)),projection_parameters=tuple(params),squared_distances=tuple(squares),max_distance=float(max(squares))**.5,positive_tangent_intersection=True)

def approximate(E,Kmax):
    start=0;pieces=[];trials=0
    while start<len(Q)-1:
        for end in range(min(start+Kmax,len(Q)-1),start,-1):
            trials+=1;piece=fit_segment(start,end,E)
            if piece is not None:break
        assert piece is not None and 1<=piece['end']-piece['start']<=Kmax
        pieces.append(piece);start=piece['end']
    for a,b in zip(pieces,pieces[1:]):
        va=add(a['H'][-1][:2],project(a['H'][1]),-1);vb=add(project(b['H'][1]),b['H'][0][:2],-1)
        assert cross(va,vb)==0 and dot(va,vb)>0
    internal=tuple(PARAMS[p['end']] for p in pieces[:-1]);U=(F(0),)*3+tuple(t for t in internal for _ in range(2))+(F(1),)*3
    H=pieces[0]['H']+tuple(h for p in pieces[1:] for h in p['H'][1:]);assert len(U)==len(H)+3
    checks=0
    for piece in pieces:
        a,b=PARAMS[piece['start']],PARAMS[piece['end']]
        for j in range(11):
            t=F(j,10);assert de_boor(U,H,2,a+(b-a)*t)==evaluate(piece['H'],t);checks+=1
    return U,H,pieces,dict(tolerance=str(E),Kmax=Kmax,segments=len(pieces),controls=len(H),segment_boundaries=[0]+[p['end'] for p in pieces],maximum_exact_checked_datum_distance=max(p['max_distance'] for p in pieces),all_true_analytic_sample_distances_below_tolerance=True,exact_G1_all_joins=True,native_global_piece_homogeneous_identity_checks=checks,common_chord_parameter_error_bound=PARAM_ERROR,search='exhaustive descending segment end,so maximum feasible end withinKmax for this distance check',candidate_trials=trials,analytic_sample_L1_rounding_bound=str(TRUE_POINT_L1_ERROR_BOUND),rounding_and_rendering_acceptance_margin='1e-6')

"""Mixed coplanar/noncoplanar A9.12and exact pair interpolation forE0."""
from fractions import Fraction as F
from local_quadratic_interpolator import unit,add,mul,dot,length
from local_cubic_approximation import closest_candidate,round_scalar,stitch_C1
from bounded_curve_approximation import chord_parameters
from inverse_knot_projection import solve
from local_cubic_planar_data import casteljau
from local_cubic_spatial_data import Q,D,PIECES,COUNTS
from native_bspline import de_boor
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def det(a,b,c):return dot(a,cross(b,c))
T=tuple(unit(d) for d in D);PARAMS,PARAM_ERROR=chord_parameters(Q)

def gamma_parameter(lam):
    if lam==F(1,2):return F(1,2)
    a=F(0);b=F(1)
    for _ in range(80):
        u=(a+b)/2;value=3*u*u-2*u*u*u
        if value==lam:return u
        if value<lam:a=u
        else:b=u
    u=F(round(float((a+b)/2)*10**14),10**14);assert abs(3*u*u-2*u*u*u-lam)<F(1,10**12)
    return u

def fit_segment(start,end,E):
    A,B=Q[start],Q[end];Ts,Te=T[start],T[end];chord=add(B,A,-1);independent=det(chord,Ts,Te)!=0;aa=[];bb=[];proof=[]
    if end==start+1:alpha=length(chord)/3;beta=-alpha
    else:
        for k in range(start+1,end):
            if independent:
                M=tuple((chord[d],Ts[d],Te[d]) for d in range(3));rhs=tuple((Q[k][d]-A[d],) for d in range(3))
                lam,a,b=(x[0] for x in solve(M,rhs))
                if not 0<lam<1:return None
                u=gamma_parameter(lam);s=1-u;alpha=a/(3*s*s*u);beta=b/(3*s*u*u)
                item=dict(index=k,case='noncoplanar',unique_parameter=str(u),linear_point_decomposition_exact=True)
            else:
                u=(PARAMS[k]-PARAMS[start])/(PARAMS[end]-PARAMS[start]);s=1-u;Tp=T[k]
                matrix=[(3*s*s*u*Ts[d],3*s*u*u*Te[d]) for d in range(3)]
                rhs=[Q[k][d]-(s**3+3*s*s*u)*A[d]-(u**3+3*s*u*u)*B[d] for d in range(3)]
                a,b,c=cross(Tp,Ts),cross(Tp,Te),cross(Tp,add(A,B,-1))
                matrix.extend((s*(s-2*u)*a[d],u*(2*s-u)*b[d]) for d in range(3));rhs.extend(2*s*u*x for x in c)
                G=tuple(tuple(sum(row[i]*row[j] for row in matrix) for j in range(2)) for i in range(2));R=tuple((sum(row[i]*r for row,r in zip(matrix,rhs)),) for i in range(2))
                try:alpha,beta=(x[0] for x in solve(G,R))
                except StopIteration:return None
                residual=tuple(row[0]*alpha+row[1]*beta-r for row,r in zip(matrix,rhs));assert all(sum(row[i]*r for row,r in zip(matrix,residual))==0 for i in range(2))
                item=dict(index=k,case='coplanar',normal_gradient_exactly_zero=True,point_residual_may_be_nonzero=any(residual))
            if alpha<=0 or beta>=0:return None
            ar,br=round_scalar(alpha),round_scalar(beta)
            if ar<=0 or br>=0:return None
            aa.append(ar);bb.append(br);proof.append(item)
        alpha=sum(aa)/len(aa);beta=sum(bb)/len(bb)
    P=(A,add(A,Ts,alpha),add(B,Te,beta),B);parameters=[F(0)];squares=[F(0)]
    for q in Q[start+1:end]:
        u,sq=closest_candidate(P,q)
        if sq>(E-F(1,10**7))**2:return None
        parameters.append(u);squares.append(sq)
    parameters.append(F(1));squares.append(F(0))
    if not all(a<b for a,b in zip(parameters,parameters[1:])):return None
    return dict(start=start,end=end,controls=P,alpha=alpha,beta=beta,individual=proof,projection_parameters=tuple(parameters),squared_distances=tuple(squares),maximum_distance=float(max(squares))**.5)

def exact_pair_interpolation():
    pieces=[];offset=0
    for original,n in zip(PIECES,COUNTS):
        derivative=tuple(tuple(3*(b-a) for a,b in zip(A,B)) for A,B in zip(original,original[1:]))
        for j in range(0,n,2):
            a,b=F(j,n),F(j+2,n);start=offset+j;end=start+2;h=b-a
            A,B=Q[start],Q[end];P=(A,add(A,casteljau(derivative,a),h/3),add(B,casteljau(derivative,b),-h/3),B)
            assert de_boor((F(0),)*4+(F(1),)*4,P,3,F(1,2))==Q[start+1]
            idx=next(i for i,x in enumerate(T[start]) if x);idy=next(i for i,x in enumerate(T[end]) if x)
            alpha=(P[1][idx]-A[idx])/T[start][idx];beta=(P[2][idy]-B[idy])/T[end][idy]
            assert add(A,T[start],alpha)==P[1] and add(B,T[end],beta)==P[2] and alpha>0 and beta<0
            pieces.append(dict(start=start,end=end,controls=P,alpha=alpha,beta=beta,maximum_distance=0.,exact_midpoint_interpolation=True,projection_parameters=(F(0),F(1,2),F(1)),squared_distances=(F(0),F(0),F(0))))
        offset+=n
    assert len(pieces)==25
    return pieces

def approximate(E,Kmax=20):
    if E==0:pieces=exact_pair_interpolation();trials=25
    else:
        pieces=[];start=0;trials=0
        while start<len(Q)-1:
            for end in range(min(start+Kmax,len(Q)-1),start,-1):
                trials+=1;piece=fit_segment(start,end,E)
                if piece is not None:break
            assert piece is not None;pieces.append(piece);start=end
    U,P,knots,proof=stitch_C1(pieces)
    return U,P,pieces,dict(tolerance=str(E),Kmax=Kmax,segments=len(pieces),control_count=len(P),maximum_exact_checked_3D_datum_distance=max(p['maximum_distance'] for p in pieces),all_exact_checked_distances_within_tolerance=True,common_chord_parameter_error_bound=PARAM_ERROR,joins=proof,segment_boundaries=[0]+[p['end'] for p in pieces],candidate_trials=trials,zero_tolerance_method='25exact cubic restrictions,each covers2samplingintervals;all51pointsinterpolated;validwithinKmax20,notaminimalityclaim' if E==0 else None)

"""10.17actual Eq10.27forward projected normals versus true Frenet frames."""
from fractions import Fraction as F
from math import isqrt,comb
from bspline_math import compose_affine,evaluate,derivative
from frenet_flip_data import D,N,CF,cross
from native_bspline import segments
PARAMS=tuple(map(F,('0','3/20','3/10','1/2','7/10','17/20','1')))
PLANAR_T=((F(0),)*6,(F(0),F(4),F(0),F(0),F(0),-F(4,5)),(F(0),F(0),F(0),-F(8,3),F(0),F(0)))
SPATIAL_T=((F(0),F(4),F(0),-F(7,12)),(F(0),F(0),F(12,5),-F(8,5)),(F(0),F(0),F(16,5),F(6,5)))
def padded(p,n):return tuple(p)+(F(0),)*(n-len(p))
PLANAR=tuple(padded(compose_affine(p,-1,2),6) for p in PLANAR_T)
SPATIAL=tuple(padded(compose_affine(p,1,-2),4) for p in SPATIAL_T)
def curve(case):
    power=PLANAR if case=='a' else SPATIAL;p=len(power[0])-1;K=(F(0),)*(p+1)+(F(1),)*(p+1)
    P=tuple(tuple(sum(power[d][k]*F(comb(i,k),comb(p,k)) for k in range(i+1)) for d in range(3)) for i in range(p+1))
    assert segments(K,P,p)[0]['power']==power
    return K,p,P,power
def trajectory(case,v):return tuple(evaluate(p,v) for p in (PLANAR if case=='a' else SPATIAL))
def tangent(case,v):
    if case=='a':
        t=2*v-1;den=1+t**4;T=(F(0),(1-t**4)/den,-2*t*t/den)
    else:
        t=1-2*v;den=evaluate(N,t);T=tuple(-evaluate(p,t)/den for p in D)
    assert sum(x*x for x in T)==1
    actual=tuple(evaluate(derivative(p),v) for p in (PLANAR if case=='a' else SPATIAL))
    assert actual==tuple(8*den*x for x in T)
    return T
def frenet(case,v):
    T=tangent(case,v)
    power=PLANAR if case=='a' else SPATIAL
    actual_cross=cross(tuple(evaluate(derivative(p),v) for p in power),tuple(evaluate(derivative(derivative(p)),v) for p in power))
    if case=='a':
        if v==F(1,2):
            assert actual_cross==(F(0),)*3
            return None
        B=(F(1 if v<F(1,2) else -1),F(0),F(0))
    else:
        t=1-2*v;den=evaluate(N,t);B=tuple(-evaluate(p,t)/(2*den) for p in CF)
    assert cross(actual_cross,B)==(F(0),)*3 and sum(x*y for x,y in zip(actual_cross,B))>0
    axes=(T,cross(B,T),B)
    assert all(sum(x*y for x,y in zip(a,b))==F(i==j) for i,a in enumerate(axes) for j,b in enumerate(axes))
    return axes
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def normalize_certified(b,previous_error):
    sq=dot(b,b);assert sq>0;rn,rd=isqrt(sq.numerator),isqrt(sq.denominator)
    if rn*rn==sq.numerator and rd*rd==sq.denominator:lo=hi=F(rn,rd)
    else:
        scale=10**30;lo=F(isqrt(sq.numerator*scale*scale//sq.denominator),scale);hi=lo+F(1,scale)
    assert lo>previous_error and lo*lo<=sq<=hi*hi
    mid=(lo+hi)/2;B=tuple(x/mid for x in b);local=(hi-lo)/(lo+hi)
    raw=local+2*previous_error/(lo-previous_error);grid=10**40;s=raw*grid;bound=F(-(-s.numerator//s.denominator),grid)
    assert abs(dot(B,B)-1)<=2*local+local*local
    return B,bound,dict(projected_length_interval=[str(lo),str(hi)],local_normalization_direction_error_bound=str(local),accumulated_algorithm_direction_error_bound=str(bound))
def construct(case):
    tangents=tuple(tangent(case,v) for v in PARAMS);Fframes=tuple(frenet(case,v) for v in PARAMS)
    B=Fframes[0][2];assert dot(B,B)==1 and dot(B,tangents[0])==0
    normals=[B];errors=[F(0)];steps=[]
    for T in tangents[1:]:
        old=B;projection=tuple(x-dot(old,T)*t for x,t in zip(old,T));assert dot(projection,T)==0
        B,bound,proof=normalize_certified(projection,errors[-1]);assert dot(B,T)==0
        normals.append(B);errors.append(bound);steps.append(proof)
    assert max(errors)<F(1,10**18)
    lower=[]
    for A,B,a,b in zip(normals,normals[1:],errors,errors[1:]):
        L=dot(A,B)-a-b-a*b;assert L>0;lower.append(L)
    if case=='a':assert normals==[(F(1),F(0),F(0))]*7 and max(errors)==0
    rows=[]
    for v,T,B,ff,e in zip(PARAMS,tangents,normals,Fframes,errors):
        rows.append(dict(v=str(v),point=list(map(str,trajectory(case,v))),unit_tangent=list(map(str,T)),projected_normal=list(map(str,B)),Frenet_axes=[list(map(str,a)) for a in ff] if ff else None,projected_direction_error_bound=str(e),exact_projected_normal_orthogonality=(dot(B,T)==0)))
    K,p,P,power=curve(case)
    r=dict(panel=case,trajectory_degree=p,trajectory_knots=list(map(str,K)),trajectory_controls=[[str(x) for x in p] for p in P],trajectory_global_power=[[str(x) for x in p] for p in power],nodes=rows,method='open-curve forward projection and normalization Eq10.27',initial_B_equals_initial_Frenet_binormal_exact=True,all7projected_normals_exactly_orthogonal_to_exact_unit_tangents=True,normalization_square_root_enclosure_width_at_most='1e-30',maximum_accumulated_projected_direction_error_bound=str(max(errors)),certified_positive_adjacent_projected_normal_dot_lower_bound=str(min(lower)),planar_projected_normals_exactly_constant=(case=='a'),Frenet_frame_undefined_at_v_half=(case=='a'),all_defined_Frenet_frames_exactly_orthonormal=True,normalization_steps=steps)
    return r
def view(P):
    x,y,z=P;return(F(13,10)*(-F(4,5)*x+F(3,5)*y),F(13,10)*(-F(9,25)*x-F(12,25)*y+F(4,5)*z))

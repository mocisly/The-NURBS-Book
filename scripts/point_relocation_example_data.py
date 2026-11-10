"""Shared representative curve for printed11.2/11.3/11.4 and later comparisons."""
from fractions import Fraction as F
from control_relocation_data import U,GRE
from native_bspline import segments,de_boor
from bspline_math import derivative,evaluate
P=tuple(tuple(map(F,p)) for p in [(0,0),('1.5',0),('1.5','1.3'),('2.5','2.6'),('4.5','3.1'),(6,'2.6'),(7,'1.3'),(7,0),(8,0)])
DIRECTION=(F(7,25),-F(24,25));DISTANCE=F(6,5)
assert sum(c*c for c in DIRECTION)==1
def peak(K,k):
    B=tuple((F(i==k),) for i in range(len(K)-4));ss=segments(K,B,3);found=None;falling=False
    for s in ss:
        q=tuple(3*(b[0]-a[0])/(s['b']-s['a']) for a,b in zip(s['bern'],s['bern'][1:]))
        if not any(q):continue
        if min(q)>=0:assert not falling
        elif max(q)<=0:falling=True
        else:
            assert q[0]>0 and q[-1]<0 and found is None and not falling
            # q(t)/(1-t)^2 has positive constant and negative leading term,
            # hence its two roots have opposite signs: exactly one positive root.
            found=s;falling=True
    assert found is not None;a,b=found['a'],found['b'];dp=derivative(found['power'][0])
    for _ in range(64):
        t=(a+b)/2
        if evaluate(dp,t)>0:a=t
        else:b=t
    t=(a+b)/2;return t,de_boor(K,B,3,t)[0],(a,b)
def relocate(K,controls,k,t,d=DISTANCE):
    B=tuple((F(i==k),) for i in range(len(controls)));R=de_boor(K,B,3,t)[0];alpha=d/R;delta=tuple(alpha*c for c in DIRECTION)
    Q=tuple(tuple(a+b for a,b in zip(p,delta)) if i==k else p for i,p in enumerate(controls));A=de_boor(K,controls,3,t);Z=de_boor(K,Q,3,t)
    assert tuple(b-a for a,b in zip(A,Z))==tuple(d*c for c in DIRECTION)
    identities=unchanged=0
    for a,b,c in zip(segments(K,controls,3),segments(K,Q,3),segments(K,B,3)):
        for axis in range(2):
            assert all(y-x==delta[axis]*n for x,y,n in zip(a['power'][axis],b['power'][axis],c['power'][0]));identities+=4
        if a['b']<=K[k] or a['a']>=K[k+4]:assert a['power']==b['power'];unchanged+=1
    maximum,height,bracket=peak(K,k)
    return Q,dict(degree=3,ubar=t,moved_index=k,knots=K,controls=controls,new_controls=Q,unit_direction=DIRECTION,requested_distance=d,basis_at_selected=R,alpha=alpha,delta_control=delta,selected_point=A,new_selected_point=Z,greville=sum(K[k+1:k+4])/3,peak_parameter=maximum,peak_parameter_bracket=bracket,maximum_displacement=alpha*height,maximum_to_requested_ratio=height/R,exact_whole_power_coefficient_identities=identities,entire_unmodified_spans=unchanged,all_point_displacements_parallel_to_unit_direction=True,exact_target_distance_squared=d*d)

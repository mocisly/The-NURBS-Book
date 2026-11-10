"""Generate exact rational equal-three-speed cubics from chosen unit directions."""
from fractions import Fraction as F
from local_quadratic_interpolator import add,mul,dot
from native_bspline import segments,check,de_boor
from inverse_knot_projection import remove_to
from bspline_math import derivative,evaluate

def construct(T,MIDT,ALPHA,start=(F(0),F(0))):
    assert len(T)==len(MIDT)+1==len(ALPHA)+1
    assert all(dot(t,t)==1 for t in tuple(T)+tuple(MIDT)) and min(ALPHA)>0
    Q=[start];B=[];report=[];total=sum(ALPHA);n=len(ALPHA)
    for i,a in enumerate(ALPHA):
        tsum=add(T[i],T[i+1]);delta=add(mul(tsum,a/6),MIDT[i],2*a/3);end=add(Q[-1],delta)
        P=(Q[-1],add(Q[-1],T[i],a/3),add(end,T[i+1],-a/3),end)
        s=segments((F(0),)*4+(F(1),)*4,P,3)[0]
        for t in (F(0),F(1,2),F(1)):
            D=tuple(evaluate(derivative(c),t) for c in s['power']);assert dot(D,D)==a*a
        aa=16-dot(tsum,tsum);bb=12*dot(delta,tsum);cc=-36*dot(delta,delta)
        assert aa*a*a+bb*a+cc==0 and aa>0 and cc<0
        B.append(P);Q.append(end);report.append(dict(segment=i,alpha=str(a),positive_root_and_three_local_speeds_exact=True))
    Q=tuple(Q);B=tuple(B);params=tuple(sum(ALPHA[:i])/total for i in range(n+1))
    UF=(F(0),)*4+tuple(x for u in params[1:-1] for x in (u,u,u))+(F(1),)*4
    full=(Q[0],)+tuple(q for b in B for q in b[1:]);U,P,removal=remove_to(UF,full,3,params[1:-1]);assert removal['curve_exactly_unchanged']
    ss=segments(U,P,3);nc=check(U,P,3,ss,steps=17)
    assert tuple(s['bern'] for s in ss)==B and all(de_boor(U,P,3,u)==q for u,q in zip(params,Q))
    for s in ss:
        for u in (s['a'],(s['a']+s['b'])/2,s['b']):
            D=tuple(evaluate(derivative(c),u) for c in s['power']);assert dot(D,D)==total*total
    return Q,params,U,P,ss,dict(segments=report,zero_error_removal=removal,native_C1_checks=nc,normalized_endpoint_midpoint_speed=str(total))

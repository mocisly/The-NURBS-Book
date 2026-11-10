"""Renner interpolation of given data; certified roots, exact rational C1 joins."""
from fractions import Fraction as F
from math import isqrt
from local_quadratic_interpolator import tangents,unit,add,mul,dot
from native_bspline import segments,check,de_boor
from inverse_knot_projection import remove_to
from bspline_math import derivative,evaluate

def positive_alpha(A,B,Ts,Te):
    delta=add(B,A,-1);total=add(Ts,Te);a=16-dot(total,total);b=12*dot(delta,total);c=-36*dot(delta,delta)
    assert a>0 and c<0
    disc=b*b-4*a*c;n,d=isqrt(disc.numerator),isqrt(disc.denominator)
    if n*n==disc.numerator and d*d==disc.denominator:alpha=(-b+F(n,d))/(2*a);root_error=F(0)
    else:
        S=10**32;lo=F(isqrt(disc.numerator*S*S//disc.denominator),S);hi=lo+F(1,S)
        assert lo*lo<disc<hi*hi
        rl,rh=(-b+lo)/(2*a),(-b+hi)/(2*a)
        alpha=F(round((rl+rh)/2*10**24),10**24);root_error=max(abs(alpha-rl),abs(alpha-rh))
        assert root_error<F(1,10**23)
    residual=abs(a*alpha*alpha+b*alpha+c);assert alpha>0 and residual<F(1,10**20)
    return alpha,dict(coefficients=list(map(str,(a,b,c))),positive_root_error_bound=str(root_error),quadratic_residual=str(residual))

def interpolate(Q):
    T=tuple(unit(v) for v in tangents(Q,'akima'));ALPHA=[];B=[];reports=[];n=len(Q)-1
    for k,(A,Z) in enumerate(zip(Q,Q[1:])):
        a,proof=positive_alpha(A,Z,T[k],T[k+1]);ALPHA.append(a)
        P=(A,add(A,T[k],a/3),add(Z,T[k+1],-a/3),Z)
        s=segments((F(0),)*4+(F(1),)*4,P,3)[0]
        residuals=[]
        for u in (F(0),F(1,2),F(1)):
            D=tuple(evaluate(derivative(c),u) for c in s['power']);residuals.append(abs(dot(D,D)-a*a))
        assert max(residuals)<F(1,10**20)
        reports.append(dict(interval=k,alpha=str(a),root=proof,three_speed_squared_residuals=list(map(str,residuals))))
        B.append(P)
    total=sum(ALPHA);params=tuple(sum(ALPHA[:i])/total for i in range(n+1))
    UF=(F(0),)*4+tuple(x for u in params[1:-1] for x in (u,u,u))+(F(1),)*4
    full=(Q[0],)+tuple(q for b in B for q in b[1:]);U,P,removal=remove_to(UF,full,3,params[1:-1]);assert removal['curve_exactly_unchanged']
    ss=segments(U,P,3);nc=check(U,P,3,ss,steps=13)
    assert tuple(s['bern'] for s in ss)==tuple(B) and all(de_boor(U,P,3,u)==q for u,q in zip(params,Q))
    for k,(a,b) in enumerate(zip(ss,ss[1:]),1):
        u=a['b'];da=tuple(evaluate(derivative(c),u) for c in a['power']);db=tuple(evaluate(derivative(c),u) for c in b['power'])
        assert da==db==mul(T[k],total)
    return U,P,ss,params,dict(method='Akima unit tangent estimates plus positive Eq9.50 roots',unit_residual_bound='1e-21',root_error_bound='1e-23',local_speed_squared_residual_bound='1e-20',segments=reports,all_data_interpolated_exact=True,C1_join_derivative_equalities_exact=True,zero_error_knot_removal=removal,native_checks=nc)

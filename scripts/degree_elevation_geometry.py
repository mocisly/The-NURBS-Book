"""Exact clamped B-spline degree elevation by Bezier extraction and removal."""
from fractions import Fraction as F
from native_bspline import segments
from rational_geometry import elevate
from inverse_knot_projection import remove_to

def elevate_spline(U,P,p,t):
    assert t>=1 and U.count(U[0])==U.count(U[-1])==p+1
    degree=p+t;ss=segments(U,P,p);pieces=[]
    for s in ss:
        q=s['bern']
        for j in range(t):q=elevate(q)
        pieces.append(q)
    internal=sorted(set(U[p+1:-p-1]));Q=pieces[0]
    for q in pieces[1:]:Q+=q[1:]
    K=(U[0],)*(degree+1)+tuple(u for u in internal for j in range(degree))+(U[-1],)*(degree+1)
    removed=[u for u in internal for j in range(p-U.count(u))]
    if removed:
        K,Q,proof=remove_to(K,Q,degree,removed);assert proof['curve_exactly_unchanged']
    else:proof={'curve_exactly_unchanged':True,'removed_knots':[]}
    assert all(K.count(u)==U.count(u)+t for u in set(U))
    elevated=segments(K,Q,degree)
    for old,new in zip(ss,elevated):
        assert (old['a'],old['b'])==(new['a'],new['b'])
        assert all(tuple(x)+(F(0),)*t==tuple(y) for x,y in zip(old['power'],new['power']))
    return K,Q,{'degree':degree,'increment':t,'all_global_power_coefficients_identical':True,
                'internal_multiplicities_increased_by_increment':True,'removal':proof}

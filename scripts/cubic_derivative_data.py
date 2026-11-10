"""Shared exact mathematical data for the two original pieces of Fig3.16."""
from fractions import Fraction as F
from bspline_math import evaluate,derivative
from native_bspline import segments,check

knots=(F(0),)*4+(F(2,5),F(3,5),F(3,5))+(F(1),)*4
controls=((0,0),(F(1,2),2),(3,F(27,10)),(4,2),(F(21,4),0),(7,0),(F(15,2),1))
q=tuple(tuple(3*F(controls[i+1][d]-controls[i][d],knots[i+4]-knots[i+1]) for d in range(2)) for i in range(6))
dk=knots[1:-1];curve=segments(knots,controls,3);dc=segments(dk,q,2)
assert q==((F(15,4),15),(F(25,2),F(7,2)),(5,F(-7,2)),(F(25,4),-10),(F(105,8),0),(F(15,4),F(15,2)))
def at(segs,u,order=0):
    s=next((s for s in segs if s['a']<=u<s['b']),segs[-1]);polys=s['power']
    for _ in range(order): polys=tuple(map(derivative,polys))
    return tuple(evaluate(c,u) for c in polys)

def verify():
    count=check(knots,controls,3,curve)+check(dk,q,2,dc)
    for a,b in zip(curve,dc):
        assert a['a']==b['a'] and a['b']==b['b']
        assert tuple(map(derivative,a['power']))==b['power']
    u=F(3,5);left,right=dc[-2:]
    assert left['bern'][-1]==right['bern'][0]==q[3]
    dl=tuple(evaluate(derivative(c),u) for c in left['power'])
    dr=tuple(evaluate(derivative(c),u) for c in right['power'])
    assert dl[0]*dr[1]-dl[1]*dr[0]!=0
    return {'figure':'3.16','knots':list(map(str,knots)),'derivative_knots':list(map(str,dk)),
        'representative_controls':[[str(v) for v in p] for p in controls],
        'derivative_controls':[[str(v) for v in p] for p in q],
        'Eq3_4_multipliers':['15/2','5','5','5','15/2','15/2'],
        'exact_curve_checks':count,'polynomial_derivative_identity':True,
        'derivative_corner_parameter':'3/5','derivative_corner_control':3,
        'corner_left_tangent':list(map(str,dl)),'corner_right_tangent':list(map(str,dr)),
        'display_scale':'1/3'}

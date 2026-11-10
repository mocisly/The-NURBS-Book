"""Exact three-piece Renner example shared by9.29 and9.30.

Choose rational unit endpoint/midpoint derivative directions, then derive the
chords from Eq9.47..50. This makes all three local speeds exact, not rounded.
"""
from fractions import Fraction as F
from local_quadratic_interpolator import add,mul,dot
from native_bspline import segments,check,de_boor
from inverse_knot_projection import remove_to
from bspline_math import derivative,evaluate
T=((F(5,13),F(12,13)),(F(12,13),-F(5,13)),(F(12,13),-F(5,13)),(F(5,13),F(12,13)))
MIDT=((F(3,5),F(4,5)),(F(3,5),-F(4,5)),(F(3,5),F(4,5)))
ALPHA=tuple(map(F,(3,4,3)))
assert all(dot(t,t)==1 for t in T+MIDT)
Q=[(F(0),F(0))];BEZIER=[];REPORT=[]
for i,a in enumerate(ALPHA):
    tsum=add(T[i],T[i+1]);delta=add(mul(tsum,a/6),MIDT[i],2*a/3);B=add(Q[-1],delta)
    P=(Q[-1],add(Q[-1],T[i],a/3),add(B,T[i+1],-a/3),B)
    s=segments((F(0),)*4+(F(1),)*4,P,3)[0]
    for t in (F(0),F(1,2),F(1)):
        D=tuple(evaluate(derivative(c),t) for c in s['power']);assert dot(D,D)==a*a
    aa=16-dot(tsum,tsum);bb=12*dot(delta,tsum);cc=-36*dot(delta,delta)
    assert aa*a*a+bb*a+cc==0 and aa>0 and cc<0
    REPORT.append(dict(segment=i,alpha=str(a),equal_endpoint_midpoint_speeds_exact=True,quadratic_root_coefficients=list(map(str,(aa,bb,cc)))))
    Q.append(B);BEZIER.append(P)
Q=tuple(Q);BEZIER=tuple(BEZIER);TOTAL=sum(ALPHA)
PARAMS=(F(0),F(3,10),F(7,10),F(1));assert PARAMS==tuple(sum(ALPHA[:i])/TOTAL for i in range(4))
UF=(F(0),)*4+tuple(u for t in PARAMS[1:-1] for u in (t,t,t))+(F(1),)*4
FULL=(Q[0],)+tuple(q for b in BEZIER for q in b[1:])
U,P,REMOVAL=remove_to(UF,FULL,3,PARAMS[1:-1]);assert REMOVAL['curve_exactly_unchanged']
assert P==(Q[0],)+tuple(q for b in BEZIER for q in b[1:3])+(Q[-1],)
SS=segments(U,P,3);NATIVE_CHECKS=check(U,P,3,SS)
assert tuple(s['bern'] for s in SS)==BEZIER and all(de_boor(U,P,3,u)==q for u,q in zip(PARAMS,Q))
for i,s in enumerate(SS):
    for u in (s['a'],(s['a']+s['b'])/2,s['b']):
        D=tuple(evaluate(derivative(c),u) for c in s['power']);assert dot(D,D)==TOTAL*TOTAL
for a,b in zip(SS,SS[1:]):
    u=a['b'];assert tuple(evaluate(derivative(c),u) for c in a['power'])==tuple(evaluate(derivative(c),u) for c in b['power'])

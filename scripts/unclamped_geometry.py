"""Exact polynomial geometry checks without clamped-endpoint assumptions."""
from fractions import Fraction as F
from bspline_math import basis,evaluate,derivative,piece
from native_bspline import segments,de_boor
def verified_segments(K,P,p,steps=9):
    ss=segments(K,P,p);checks=0
    for s in ss:
        for j in range(steps):
            t=F(j,steps);u=s['a']+(s['b']-s['a'])*t
            w=[basis(K,i,p,u)for i in range(len(P))];assert min(w)>=0 and sum(w)==1
            q=list(s['bern'])
            for _ in range(p):q=[tuple((1-t)*x+t*y for x,y in zip(a,b))for a,b in zip(q,q[1:])]
            assert q[0]==de_boor(K,P,p,u)==tuple(evaluate(c,u)for c in s['power'])
            checks+=1
    for left,right in zip(ss,ss[1:]):
        u=left['b']
        for c,d in zip(left['power'],right['power']):
            for _ in range(p-K.count(u)+1):
                assert evaluate(c,u)==evaluate(d,u);c,d=derivative(c),derivative(d)
    assert ss[0]['bern'][0]==de_boor(K,P,p,K[p])
    assert ss[-1]['bern'][-1]==de_boor(K,P,p,K[len(P)])
    return ss,checks

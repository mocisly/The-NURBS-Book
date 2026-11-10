"""Common representative7-control cubic for Fig5.18/5.19 Bezier decomposition."""
from fractions import Fraction as F
from knot51_data import insert
U=tuple(map(F,[0,0,0,0,1,2,3,4,4,4,4]))
P=tuple(tuple(F(str(c)) for c in pt) for pt in [(0,.3),(.3,4),(4,4.5),(5.5,0),(8.8,0),(10.5,2.8),(8,5.4)])
def decomposed():
    K,R=U,P
    for t in (F(1),F(2),F(3)):
        while K.count(t)<3:K,R,_=insert(K,R,3,t)
    return K,R

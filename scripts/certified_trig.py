"""Rational sine/cosine coordinates from Machin's pi and Taylor remainder bounds."""
from fractions import Fraction as F
from functools import lru_cache

def atan_bounds(x,n):
    s=sum(((-1)**k*x**(2*k+1)/F(2*k+1) for k in range(n)),F(0))
    t=s+(-1)**n*x**(2*n+1)/F(2*n+1)
    return min(s,t),max(s,t)
a,b=atan_bounds(F(1,5),30);c,d=atan_bounds(F(1,239),10)
PI_LO,PI_HI=16*a-4*d,16*b-4*c
D=10**30
@lru_cache(None)
def cos_sin(degrees):
    degrees=F(degrees);q=int((degrees+45)//90);t=(degrees-90*q)*(PI_LO+PI_HI)/360
    assert abs(t)<1
    cos=F(1);sin=t;tc=F(1);ts=t
    for k in range(1,25):
        tc*=-t*t/F((2*k-1)*(2*k));ts*=-t*t/F((2*k)*(2*k+1));cos+=tc;sin+=ts
    remainder=max(abs(tc*t*t/F(49*50)),abs(ts*t*t/F(50*51)))
    pi_error=abs(degrees-90*q)*(PI_HI-PI_LO)/360
    def rounded(x):return F(round(x*D),D)
    cc,ss=rounded(cos),rounded(sin)
    assert max(abs(cc-cos),abs(ss-sin))+remainder+pi_error<F(1,10**29)
    return [(cc,ss),(-ss,cc),(-cc,-ss),(ss,-cc)][q%4]

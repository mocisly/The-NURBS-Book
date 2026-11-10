"""Small exact power-polynomial operations and native Bernstein conversion."""
from fractions import Fraction as F
from math import comb
from bspline_math import add,compose_affine

def multiply(a,b):
    result=[F(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):result[i+j]+=x*y
    return tuple(result)

def compose(a,b):
    result=(F(0),)
    for x in reversed(a):result=add(multiply(result,b),(x,))
    return result

def bernstein(power,a=F(0),b=F(1)):
    local=[compose_affine(c,a,b-a) for c in power];p=max(map(len,local))-1
    return tuple(tuple(sum((c[k] if k<len(c) else F(0))*F(comb(j,k),comb(p,k)) for k in range(j+1)) for c in local) for j in range(p+1))

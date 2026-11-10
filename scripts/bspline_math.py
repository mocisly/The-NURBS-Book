"""Exact polynomial pieces from Cox-de Boor; no image geometry is sampled."""
from fractions import Fraction as F
from functools import lru_cache


def add(a,b):
    c=[F(0)]*max(len(a),len(b))
    for i,v in enumerate(a): c[i]+=v
    for i,v in enumerate(b): c[i]+=v
    while len(c)>1 and c[-1]==0: c.pop()
    return tuple(c)


def linear(a,c,d):
    result=[F(0)]*(len(a)+1)
    for i,v in enumerate(a):
        result[i]+=v*c
        result[i+1]+=v*d
    return tuple(result)


@lru_cache(None)
def piece(knots,i,p,span):
    if p==0: return (F(i==span),)
    left=right=(F(0),)
    d=knots[i+p]-knots[i]
    if d: left=linear(piece(knots,i,p-1,span),-F(knots[i],d),F(1,d))
    d=knots[i+p+1]-knots[i+1]
    if d: right=linear(piece(knots,i+1,p-1,span),F(knots[i+p+1],d),-F(1,d))
    return add(left,right)


def evaluate(coeffs,x):
    result=F(0)
    for c in reversed(coeffs): result=result*x+c
    return result


def basis(knots,i,p,x):
    """Independent numerical recurrence, preserving half-open intervals."""
    if p==0: return F(knots[i]<=x<knots[i+1])
    result=F(0)
    d=knots[i+p]-knots[i]
    if d: result+=(x-knots[i])/d*basis(knots,i,p-1,x)
    d=knots[i+p+1]-knots[i+1]
    if d: result+=(knots[i+p+1]-x)/d*basis(knots,i+1,p-1,x)
    return result


def derivative(coeffs):
    return tuple(i*c for i,c in enumerate(coeffs) if i) or (F(0),)


def compose_affine(coeffs,offset,scale):
    """Change from global u to local t: u=offset+scale*t, exactly."""
    result=(F(0),)
    for c in reversed(coeffs):
        result=add(linear(result,F(offset),F(scale)),(c,))
    return result


def expression(coeffs):
    """Horner expression for PGFPlots; exact rational coefficients."""
    def number(c): return f'({c.numerator}/{c.denominator})'
    result=number(coeffs[-1])
    for c in reversed(coeffs[:-1]): result=f'({result}*x+{number(c)})'
    return result

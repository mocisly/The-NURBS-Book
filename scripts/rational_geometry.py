"""Positive-weight rational Bezier geometry with certified native cubic previews.

This approximates mathematical rational functions, never raster contours.
For each Hermite cubic H, (A-W*H)/W is bounded using the exact Bernstein
coefficients of its numerator and the positive minimum denominator control.
"""
from fractions import Fraction as F
from math import comb

def split(controls):
    levels=[list(controls)]
    while len(levels[-1])>1:
        row=levels[-1]
        levels.append([tuple((a+b)/2 for a,b in zip(row[i],row[i+1])) for i in range(len(row)-1)])
    return tuple(row[0] for row in levels),tuple(row[-1] for row in reversed(levels))

def elevate(controls):
    p=len(controls)-1
    return (controls[0],)+tuple(tuple(F(i,p+1)*a+(1-F(i,p+1))*b for a,b in zip(controls[i-1],controls[i])) for i in range(1,p+1))+(controls[-1],)

def evaluate(controls,t):
    row=list(controls)
    while len(row)>1:row=[tuple((1-t)*a+t*b for a,b in zip(row[i],row[i+1])) for i in range(len(row)-1)]
    return row[0]

def project(h):return tuple(a/h[-1] for a in h[:-1])

def hermite(controls):
    p=len(controls)-1;A,B=controls[0],controls[-1];a,b=project(A),project(B)
    aa,bb=project(controls[1]),project(controls[-2])
    return (a,tuple(x+F(p,3)*controls[1][-1]/A[-1]*(y-x) for x,y in zip(a,aa)),
            tuple(x-F(p,3)*controls[-2][-1]/B[-1]*(x-y) for x,y in zip(b,bb)),b)

def error_bound(controls,H):
    p=len(controls)-1;dim=len(H[0]);minimum=min(c[-1] for c in controls)
    assert minimum>0
    residual=[[F(0)]*dim for _ in range(p+4)]
    for i,A in enumerate(controls):
        for j,B in enumerate(H):
            factor=F(comb(p,i)*comb(3,j),comb(p+3,i+j))
            for d in range(dim):residual[i+j][d]+=factor*(A[d]-A[-1]*B[d])
    return max(sum(map(abs,row)) for row in residual)/minimum

def approximate(controls,tolerance=F(1,10000),depth=0):
    controls=tuple(tuple(map(F,c)) for c in controls)
    assert min(c[-1] for c in controls)>=0 and controls[0][-1]>0 and controls[-1][-1]>0
    if min(c[-1] for c in controls)==0:
        # A zero interior homogeneous weight need not make W(t) zero.
        # Positive endpoint weights make both half-pieces strictly positive.
        assert depth<18
        a,b=split(controls)
        return approximate(a,tolerance,depth+1)+approximate(b,tolerance,depth+1)
    H=hermite(controls);bound=error_bound(controls,H)
    if bound<=tolerance:return [{'bern':H,'certified_l1_error':bound}]
    assert depth<18,'Rational preview subdivision failed to reach tolerance'
    a,b=split(controls)
    return approximate(a,tolerance,depth+1)+approximate(b,tolerance,depth+1)

def graph_controls(a,b,numerator,denominator,xscale=F(1),yscale=F(1)):
    """Exact homogeneous degree-(p+1) graph of u=a+(b-a)t, y=A(t)/W(t)."""
    p=len(denominator)-1
    assert len(numerator)==p+1
    elevated=elevate(tuple((F(y),F(w)) for y,w in zip(numerator,denominator)))
    result=[]
    for i,(yy,ww) in enumerate(elevated):
        tw=F(i,p+1)*denominator[i-1] if i else F(0)
        result.append((xscale*(a*ww+(b-a)*tw),yscale*yy,ww))
    return tuple(result)

"""Certified spline composition for a strictly monotone scalar spline.

An irrational inverse knot is enclosed by rational bisection. Exact polynomial
composition is assembled on the rational midpoint cuts, with a global error
certificate for the tiny branch mismatch, endpoint joining and inverse insertion.
This handles mathematical control data only, never raster geometry.
"""
from fractions import Fraction as F
from native_bspline import segments,de_boor,check
from polynomial_native import compose,bernstein
from bspline_math import evaluate,derivative
from inverse_knot_projection import remove_to

def reparameterize(U,P,p,S,scalars,q):
    old=segments(U,P,p);mapping=segments(S,tuple((v,) for v in scalars),q)
    # Strict positivity is certified from derivative Bernstein coefficients.
    lower=min(x[0] for seg in mapping for x in bernstein((derivative(seg['power'][0]),),seg['a'],seg['b']))
    assert lower>0
    assert de_boor(S,tuple((v,) for v in scalars),q,F(0))==(U[0],)
    assert de_boor(S,tuple((v,) for v in scalars),q,F(1))==(U[-1],)
    roots=[]
    for knot in sorted(set(U[p+1:-p-1])):
        lo,hi=F(0),F(1)
        for iteration in range(105):
            mid=(lo+hi)/2;value=de_boor(S,tuple((v,) for v in scalars),q,mid)[0]
            if value==knot:lo=hi=mid;break
            if value<knot:lo=mid
            else:hi=mid
        roots.append((knot,(lo+hi)/2,lo,hi))
    cuts=sorted({F(0),F(1),*S[q+1:-q-1],*(r[1] for r in roots)})
    degree=p*q;pieces=[];joining=F(0)
    for a,b in zip(cuts,cuts[1:]):
        mid=(a+b)/2;fseg=next(t for t in mapping if t['a']<=mid<=t['b']);f=fseg['power'][0]
        u=evaluate(f,mid);cseg=next(t for t in old if t['a']<=u<=t['b'])
        power=tuple(compose(c,f) for c in cseg['power']);B=bernstein(power,a,b)
        assert len(B)==degree+1
        if pieces:
            delta=sum(abs(x-y) for x,y in zip(pieces[-1][-1],B[0]));joining=max(joining,delta)
            B=(pieces[-1][-1],)+B[1:]
        pieces.append(B)
    controls=pieces[0]
    for B in pieces[1:]:controls+=B[1:]
    K=(F(0),)*(degree+1)+tuple(t for t in cuts[1:-1] for j in range(degree))+(F(1),)*(degree+1)
    removed=[];multiplicities={}
    for t in cuts[1:-1]:
        mu=next((U.count(k) for k,r,lo,hi in roots if r==t),0);ms=S.count(t)
        target=max(degree-p+mu if mu else 0,degree-q+ms if ms else 0)
        assert 1<=target<=degree;multiplicities[str(t)]=target
        removed.extend([t]*(degree-target))
    if removed:K,controls,removal=remove_to(K,controls,degree,removed)
    else:removal={'certified_whole_domain_L1_error_bound_cm':'0','curve_exactly_unchanged':True}
    mismatch=F(0)
    for knot,r,lo,hi in roots:
        left=next(seg for seg in old if seg['b']==knot);right=next(seg for seg in old if seg['a']==knot)
        delta=[]
        for c,d in zip(left['power'],right['power']):
            e=tuple(x-y for x,y in zip(c,d));assert evaluate(e,knot)==0;delta.append(e)
        M=sum(sum(map(abs,derivative(c))) for c in delta)
        fr=de_boor(S,tuple((v,) for v in scalars),q,r)[0]
        mismatch+=M*abs(fr-knot)
        assert hi-lo<=F(1,2**100)
    bound=joining+mismatch+F(removal['certified_whole_domain_L1_error_bound_cm'])
    assert bound<F(1,10**24)
    for i in range(101):
        s=F(i,100);u=de_boor(S,tuple((v,) for v in scalars),q,s)[0]
        original=de_boor(U,P,p,u);new=de_boor(K,controls,degree,s)
        assert sum(abs(x-y) for x,y in zip(original,new))<=bound
    checks=check(K,controls,degree,segments(K,controls,degree),steps=11)
    return K,controls,degree,{
        'inverse_knot_brackets':[[str(x) for x in r] for r in roots],
        'strict_mapping_derivative_lower_bound':str(lower),'basis_multiplicities':multiplicities,
        'branch_switch_error_bound':str(mismatch),'endpoint_joining_bound':str(joining),
        'inverse_insertion_error_bound':removal['certified_whole_domain_L1_error_bound_cm'],
        'certified_whole_parameter_L1_composition_error_bound':str(bound),
        'exact_basis_checks':checks,'exact_error_checks':101,'new_control_count':len(controls),
        'method':'exact rational polynomial composition; rational enclosure of inverse knots; certified inverse insertion'}

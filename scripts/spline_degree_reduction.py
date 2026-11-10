"""Representative B-spline approximation: Bezier reduction, inverse knot fit.

The Bezier step follows5.41/5.42. The assembly uses an exact rational
least-squares inverse of insertion and is documented separately from A5.11.
Whole-curve errors are bounded against the original Bezier coefficients.
"""
from fractions import Fraction as F
from native_bspline import segments,de_boor
from rational_geometry import elevate,split,evaluate
from degree_reduction_geometry import reduce_bezier
from inverse_knot_projection import remove_to

def reduce_spline(U,P,p):
    original=segments(U,P,p);q=p-1;pieces=[];proofs=[]
    for s in original:
        b,proof=reduce_bezier(s['bern']);pieces.append(b);proofs.append(proof)
    internal=sorted(set(U[p+1:-p-1]));assert all(U.count(u)<=p for u in internal)
    Q=pieces[0]
    for b in pieces[1:]:assert Q[-1]==b[0];Q+=b[1:]
    K=(U[0],)*(q+1)+tuple(u for u in internal for j in range(q))+(U[-1],)*(q+1)
    removed=[u for u in internal for j in range(p-U.count(u))]
    if removed:K,Q,removal=remove_to(K,Q,q,removed)
    else:removal={'removed_knots':[],'curve_exactly_unchanged':True}
    for u in internal:assert K.count(u)==U.count(u)-1
    spans=segments(K,Q,q);reports=[];whole=F(0);identities=0
    # A removed simple knot can merge spans. Restrict the resulting polynomial
    # to every original span before comparing its Bernstein coefficients.
    from bspline_math import compose_affine
    from math import comb
    for old in original:
        new=next(s for s in spans if s['a']<=old['a'] and s['b']>=old['b'])
        local=[compose_affine(c,old['a'],old['b']-old['a']) for c in new['power']]
        bern=tuple(tuple(sum((local[d][k] if k<len(local[d]) else 0)*F(comb(j,k),comb(q,k)) for k in range(j+1)) for d in range(len(local))) for j in range(q+1))
        D=tuple(tuple(a-b for a,b in zip(x,y)) for x,y in zip(old['bern'],elevate(bern)))
        for i in range(41):
            t=F(i,40);u=old['a']+(old['b']-old['a'])*t
            assert evaluate(D,t)==tuple(a-b for a,b in zip(de_boor(U,P,p,u),de_boor(K,Q,q,u)));identities+=1
        refined=[D]
        for j in range(4):refined=[half for b in refined for half in split(b)]
        bound=max(sum(map(abs,pt)) for b in refined for pt in b);whole=max(whole,bound)
        reports.append({'interval':[str(old['a']),str(old['b'])],'residual_Bernstein_controls':[[str(x) for x in pt] for pt in D],
                        'whole_interval_L1_error_bound':str(bound)})
    return K,Q,{'Bezier_reductions':proofs,'assembly_inverse_insertion':removal,
                'exact_error_identity_points':identities,'interval_error_proofs':reports,
                'certified_whole_curve_L1_error_bound':str(whole),
                'method':'5.41/5.42 Bezier reduction followed by rational least-squares inverse knot insertion; representative approximation'}

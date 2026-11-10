"""Exact tensor midpoint refinement and directional polynomial identity checks."""
from knot59_data import insert_surface
from native_bspline import segments,check

def refine_surface(net,axis,rounds):
    additions=[]
    for _ in range(rounds):
        K=net[0 if axis=='u' else 1];midpoints=tuple((a+b)/2 for a,b in zip(K,K[1:]) if a<b);additions.append(midpoints)
        for t in midpoints:net=insert_surface(*net,axis,t)
    return net,additions

def verify_directional_identity(before,after,axis):
    U,V,p,q,P=before;A,B,_,_,Q=after;spans=checks=0
    pairs=[(U,A,p,tuple(row[j] for row in P),tuple(row[j] for row in Q)) for j in range(len(P[0]))] if axis=='u' else [(V,B,q,a,b) for a,b in zip(P,Q)]
    for K,L,d,R,S in pairs:
        old,new=segments(K,R,d),segments(L,S,d);checks+=check(L,S,d,new,steps=11)
        for s in new:
            t=next(t for t in old if t['a']<=s['a'] and s['b']<=t['b']);assert s['power']==t['power'];spans+=1
    return {'identical_directional_polynomial_spans':spans,'exact_curve_checks':checks}

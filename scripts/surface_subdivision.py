"""Exact clamped tensor-product restrictions by directional knot insertion."""
from fractions import Fraction as F
from knot59_data import insert_surface
from native_bspline import segments,check
from surface_geometry import surface

def split(net,axis,value):
    U,V,p,q,P=net;degree=p if axis=='u' else q;K=U if axis=='u' else V
    refined=net
    while K.count(value)<degree:
        refined=insert_surface(*refined,axis,value);K=refined[0 if axis=='u' else 1]
    U,V,p,q,R=refined;last=max(i for i,t in enumerate(K) if t==value);shared=last-degree
    left=tuple(t for t in K if t<=value)+(value,);right=(value,)+tuple(t for t in K if t>=value)
    if axis=='u':
        children=((left,V,p,q,R[:shared+1]),(right,V,p,q,R[shared:]))
        assert children[0][-1][-1]==children[1][-1][0]
    else:
        children=((U,left,p,q,tuple(row[:shared+1] for row in R)),(U,right,p,q,tuple(row[shared:] for row in R)))
        assert all(a[-1]==b[0] for a,b in zip(children[0][-1],children[1][-1]))
    for A,B,p,q,S in children:assert len(A)==len(S)+p+1 and len(B)==len(S[0])+q+1
    return children,refined

def verify_restrictions(parent,children,axis):
    U,V,p,q,P=parent;spans=curvechecks=points=0
    for child in children:
        A,B,_,_,S=child
        pairs=[(U,A,p,tuple(row[j] for row in P),tuple(row[j] for row in S)) for j in range(len(P[0]))] if axis=='u' else [(V,B,q,a,b) for a,b in zip(P,S)]
        for K,L,d,R,T in pairs:
            old,new=segments(K,R,d),segments(L,T,d);curvechecks+=check(L,T,d,new,steps=11)
            for s in new:
                t=next(t for t in old if t['a']<=s['a'] and s['b']<=t['b']);assert s['power']==t['power'];spans+=1
        for i in range(11):
            u=A[p]+(A[len(S)]-A[p])*F(i,10)
            for j in range(11):
                v=B[q]+(B[len(S[0])]-B[q])*F(j,10);assert surface(*child,u,v)==surface(*parent,u,v);points+=1
    return {'identical_directional_polynomial_spans':spans,'native_directional_curve_checks':curvechecks,'child_vs_original_surface_points':points,'shared_boundary_controls_equal':True}

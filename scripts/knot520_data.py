"""Representative Fig5.20 surface, using the exact printed degrees and knots.

The original supplies no control coordinates. These explicit coordinates reproduce
its two-direction bent sheet; Fig5.21 uses its exact Bezier patches, not new data.
"""
from fractions import Fraction as F

U=(F(0),)*4+(F(3,5),)+(F(1),)*4
V=(F(0),)*3+(F(2,5),)+(F(1),)*3
xs=tuple(map(F,(3,1,-1,-3)))
ys=tuple(F(str(t)) for t in (-3,-1.8,-.2,1.4,3))
zu=tuple(F(str(t)) for t in (2,2,0,-1.4,-1.4))
zv=tuple(F(str(t)) for t in (0,0,2.6,2.6))
P=tuple(tuple((xs[j],ys[i],zu[i]+zv[j]) for j in range(4)) for i in range(5))
BASE=(U,V,3,2,P)

def decomposition():
    from surface_subdivision import split,verify_restrictions
    from surface_geometry import local_patch
    strips,refined_u=split(BASE,'u',F(3,5))
    proofs=[verify_restrictions(BASE,strips,'u')];patches=[]
    for i,strip in enumerate(strips):
        children,_=split(strip,'v',F(2,5))
        proofs.append(verify_restrictions(strip,children,'v'))
        for j,child in enumerate(children):
            Q,_,_=local_patch(U,V,3,2,P,3+i,2+j)
            assert child[-1]==Q
            assert len(Q)==4 and len(Q[0])==3
            patches.append((i,j,child))
    # The whole refined 7x5 net and the independently extracted patch controls agree.
    from knot59_data import insert_surface
    refined=insert_surface(*refined_u,'v',F(2,5))
    assert len(refined[-1])==7 and len(refined[-1][0])==5
    for i,j,child in patches:
        assert child[-1]==tuple(tuple(row[2*j:2*j+3]) for row in refined[-1][3*i:3*i+4])
    return patches,proofs,refined

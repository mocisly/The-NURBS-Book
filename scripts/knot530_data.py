"""Common representative9x8 cubic-by-quadratic surface for Fig5.30-5.34.

Printed knots are exact; the source provides no numeric control coordinates.
Two refined planar curves define a translation surface with explicit small
height perturbations, providing genuine geometric scales for knot removal.
"""
from fractions import Fraction as F
from knot51_data import insert
from surface_geometry import weights

def refine(K,P,p,changes):
    operations=[]
    for knot,delta in changes:
        t=F(knot);K,P,_=insert(K,P,p,t);values=weights(K,p,t)
        i=max(range(1,len(P)-1),key=lambda j:values[j]);Q=list(P)
        Q[i]=(Q[i][0],Q[i][1]+F(delta));P=tuple(Q)
        operations.append({'inserted':str(t),'perturbed_control':i,'height_delta':str(F(delta))})
    return K,P,operations

U,R,U_OPERATIONS=refine((F(0),)*4+(F('.52'),)+(F(1),)*4,
                       tuple(tuple(F(str(t)) for t in pt) for pt in [(-3,1.4),(-1.5,1.4),(0,-.7),(1.5,-1.2),(3,-1.2)]),3,
                       [('.22','.03'),('.3','.09'),('.7','.27'),('.79','.55')])
V,S,V_OPERATIONS=refine((F(0),)*3+(F('.5'),)+(F(1),)*3,
                       tuple(tuple(F(str(t)) for t in pt) for pt in [(3,0),(1,0),(-1,2.6),(-3,2.6)]),2,
                       [('.2','.04'),('.42','.14'),('.81','.32'),('.9','.015')])
assert U==(F(0),)*4+tuple(F(t) for t in ('.22','.3','.52','.7','.79'))+(F(1),)*4
assert V==(F(0),)*3+tuple(F(t) for t in ('.2','.42','.5','.81','.9'))+(F(1),)*3

def tensor(A,B):return tuple(tuple((x,y,zu+zv) for x,zv in B) for y,zu in A)
P=tensor(R,S);BASE=(U,V,3,2,P)
CAMERA=r'x={(-.75cm,-.75cm)},y={(.85cm,-.3cm)},z={(0cm,.7cm)}'

def projection_slopes(A,B):
    us=[];vs=[]
    for (y,z),(yy,zz) in zip(A,A[1:]):
        assert yy>y;us.append((-F(3,10)*(yy-y)+F(7,10)*(zz-z))/(F(17,20)*(yy-y)))
    for (x,z),(xx,zz) in zip(B,B[1:]):
        assert xx<x;vs.append((-F(3,4)*(xx-x)+F(7,10)*(zz-z))/(-F(3,4)*(xx-x)))
    assert max(us)<min(vs),(max(us),min(vs))
    return {'maximum_projected_u_tangent_slope':str(max(us)),'minimum_projected_v_tangent_slope':str(min(vs)),
            'strict_separation_certifies_no_projection_fold':True}

PROJECTION=projection_slopes(R,S)

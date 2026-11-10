"""Exact planar bicubic and polygon-selected control displacement for11.22+.

Uniform cubic refinement preserves the plane by exact linear precision. Its
normalized chord parameters from A9.3 equal the Greville abscissae exactly.
"""
from fractions import Fraction as F
from native_bspline import segments
K=(F(0),)*4+tuple(F(i,32)for i in range(1,32))+(F(1),)*4
G=tuple(sum(K[i+1:i+4])/3 for i in range(35))
PLANE=tuple(tuple((8*u-4,8*v-4,F(0))for v in G)for u in G)
POLYGON=tuple(tuple(map(F,p))for p in [('.2','.35'),('.5','.35'),('.5','.2'),('.65','.2'),('.65','.5'),('.8','.5'),('.8','.65'),('.5','.65'),('.5','.8'),('.35','.8'),('.35','.5'),('.2','.5')])
linear=segments(K,tuple((8*t-4,)for t in G),3)
assert all(s['power']==( (F(-4),F(8),F(0),F(0)),)for s in linear)
def inside(x,y,polygon):
    result=False
    for (a,b),(c,d)in zip(polygon,polygon[1:]+polygon[:1]):
        if (c-a)*(y-b)==(d-b)*(x-a) and min(a,c)<=x<=max(a,c) and min(b,d)<=y<=max(b,d):return True
        if (b>y)!=(d>y) and x<a+(y-b)*(c-a)/(d-b):result=not result
    return result
def crank_union(x,y):
    return any(a<=x<=b and c<=y<=d for a,b,c,d in [tuple(map(F,r))for r in [('.2','.5','.35','.5'),('.35','.5','.35','.8'),('.5','.65','.2','.65'),('.5','.8','.5','.65')]])
def make(polygon=POLYGON,distance=F(6,5),verify_crank=True):
    selected=tuple((i,j)for i,u in enumerate(G)for j,v in enumerate(G)if inside(u,v,polygon))
    if verify_crank:assert all(inside(u,v,polygon)==crank_union(u,v) for u in G for v in G)
    selected_set=set(selected);P=tuple(tuple((x,y,distance if(i,j)in selected_set else F(0))for j,(x,y,z)in enumerate(row))for i,row in enumerate(PLANE))
    assert P[0]==PLANE[0] and P[-1]==PLANE[-1] and all(a[0]==b[0]and a[-1]==b[-1]for a,b in zip(P,PLANE))
    support=(min(K[i]for i,j in selected),max(K[i+4]for i,j in selected),min(K[j]for i,j in selected),max(K[j+4]for i,j in selected))
    return P,dict(degrees=(3,3),knots=K,control_shape=(35,35),selected_controls=selected,selected_count=len(selected),chord_parameters=G,original_plane_exact_linear_precision_coefficients=256,polygon=polygon,distance=distance,modified_support_bbox=support,whole_four_boundary_curves_unchanged=True,global_z_bounds=(0,distance),selection_rule='exact rational even-odd including boundary; A9.3 chord parameters equalGreville on plane')

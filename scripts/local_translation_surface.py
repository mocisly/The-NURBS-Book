"""Local bicubic tensor translation of two chord-parameter Hermite interpolants.

For Qij=A_i+B_j, common Eq9.57 boundary derivatives depend on only one
parameter. Both mixed estimates in Eq9.59 vanish exactly. The tensor sum of
the two minimal cubic control polygons is therefore the actual local bicubic
Hermite surface, including any C1periodic seams of the component curves.
"""
from fractions import Fraction as F
from local_quadratic_interpolator import add,mul,length,tangents,unit
from native_bspline import segments,check,de_boor
from inverse_knot_projection import remove_to
from surface_geometry import surface,local_patch
from bspline_math import derivative,evaluate

def curve(data,axes,closed=False):
    projected=tuple((p[axes[0]],p[axes[1]]) for p in data)
    direction=tangents(projected,'akima',closed=closed);T=[]
    for d in direction:
        a,b=unit(d);v=[F(0)]*3;v[axes[0]]=a;v[axes[1]]=b;T.append(tuple(v))
    ell=tuple(length(add(b,a,-1)) for a,b in zip(data,data[1:]));total=sum(ell);n=len(ell)
    params=tuple(sum(ell[:i])/total for i in range(n+1));B=[]
    for k,(a,b) in enumerate(zip(data,data[1:])):
        h=(params[k+1]-params[k])*total/3;B.append((a,add(a,T[k],h),add(b,T[k+1],-h),b))
    full=(data[0],)+tuple(x for b in B for x in b[1:]);UF=(F(0),)*4+tuple(t for u in params[1:-1] for t in (u,u,u))+(F(1),)*4
    U,P,removal=remove_to(UF,full,3,params[1:-1]);assert removal['curve_exactly_unchanged']
    ss=segments(U,P,3);nc=check(U,P,3,ss,steps=11)
    assert tuple(s['bern'] for s in ss)==tuple(B) and all(de_boor(U,P,3,u)==q for u,q in zip(params,data))
    if closed:
        assert data[0]==data[-1] and T[0]==T[-1]
        assert tuple(evaluate(derivative(c),F(0)) for c in ss[0]['power'])==tuple(evaluate(derivative(c),F(1)) for c in ss[-1]['power'])
    return U,P,params,dict(closed=closed,parameters=list(map(str,params)),native_checks=nc,zero_error_knot_removal=removal,endpoint_derivative_magnitude_represented_total_chord=str(total),periodic_position_and_first_derivative_exact=closed)

def construct(A,B,axes_a=(0,2),axes_b=(1,2),closed_a=False,closed_b=False):
    U,PA,up,ra=curve(A,axes_a,closed_a);V,PB,vp,rb=curve(B,axes_b,closed_b)
    P=tuple(tuple(add(a,b) for b in PB) for a in PA);Q=tuple(tuple(add(a,b) for b in B) for a in A)
    base=(U,V,3,3,P)
    assert all(surface(*base,u,v)==Q[i][j] for i,u in enumerate(up) for j,v in enumerate(vp))
    # The full tensor identity follows coefficientwise from partition of unity;
    # independently check every whole patch against the component Bezier sums.
    sa=segments(U,PA,3);sb=segments(V,PB,3);checks=0
    for a in sa:
        for b in sb:
            patch=local_patch(U,V,3,3,P,a['span'],b['span'])[0]
            assert patch==tuple(tuple(add(x,y) for y in b['bern']) for x in a['bern']);checks+=1
    return base,Q,(up,vp),dict(method='Eq9.57local boundary Hermite interpolation;both9.59mixed estimates identically zero for tensor translation',component_a=ra,component_b=rb,all_data_interpolated_exact=True,whole_patch_coefficient_identities=checks,control_net_shape=[len(P),len(P[0])],C1_in_both_directions_exact=True,closed_directions=[closed_a,closed_b])

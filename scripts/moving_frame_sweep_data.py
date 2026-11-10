"""Exact planar PH frames; actual A10.1/A10.2 section-column interpolation."""
from fractions import Fraction as F
from itertools import combinations
from spine_skinning_example_data import SPINE_K,SPINE_P,SPINE_POWER,spine,tangent,frame,view
from native_bspline import segments,de_boor
from knot51_data import insert
from surface_geometry import weights,verify_tensor
from inverse_knot_projection import solve
from global_interpolation_data import interpolate
from bounded_curve_approximation import chord_parameters
U=(F(0),)*4+(F(1,4),F(1,2),F(3,4))+(F(1),)*4
RAW_C=tuple((F(0),-2+4*sum(U[i+1:i+4])/3,z) for i,z in enumerate(map(F,('.9','.3','.7','.4','.8','1.2','1'))))
T_K,T_P=SPINE_K,SPINE_P
for t in (F(1,5),F(2,5),F(3,5),F(4,5)):T_K,T_P,_=insert(T_K,T_P,5,t)
assert len(T_P)==10 and all(s['power']==SPINE_POWER for s in segments(T_K,T_P,5))
def arc(v):return 9*v+12*v**3-18*v**4+F(36,5)*v**5
def arc_parameters(count):
    result=[F(0)];errors=[]
    for k in range(1,count-1):
        target=arc(F(1))*F(k,count-1);a,b=F(0),F(1)
        for _ in range(45):
            mid=(a+b)/2
            if arc(mid)<target:a=mid
            else:b=mid
        v=F(round((a+b)/2*10**10),10**10);err=abs(arc(v)-target)
        assert err<F(1,10**8);result.append(v);errors.append(str(err))
    result.append(F(1));return tuple(result),errors
def section(through_origin=False):
    anchor=de_boor(U,RAW_C,3,F(1,2)) if through_origin else (F(0),)*3
    return tuple(tuple(a-b for a,b in zip(p,anchor)) for p in RAW_C)
def placed(C,v,scaling=None):
    s=(F(1),)*3 if scaling is None else scaling(v);T,N,B=frame(v);center=spine(v)
    return tuple(tuple(center[d]+s[0]*p[0]*T[d]+s[1]*p[1]*N[d]+s[2]*p[2]*B[d] for d in range(3)) for p in C)
def construct(mode='free',through_origin=False,scaling=None):
    assert mode in ('free','trajectory');C=section(through_origin)
    if mode=='trajectory':
        q=5;V=T_K;vhat=tuple(sum(V[i+1:i+q+1])/q for i in range(len(T_P)));VP=vhat;arc_errors=[];paramerror=0
    else:
        q=3;vhat,arc_errors=arc_parameters(7)
    rows=tuple(placed(C,v,scaling) for v in vhat);rigid=0
    for row,v in zip(rows,vhat):
        center=spine(v);D=tangent(v)
        assert all(sum((p[d]-center[d])*D[d] for d in range(3))==0 for p in row)
        if scaling is None:
            for i,j in combinations(range(7),2):
                assert sum((a-b)**2 for a,b in zip(row[i],row[j]))==sum((a-b)**2 for a,b in zip(C[i],C[j]));rigid+=1
    if mode=='free':
        param=[chord_parameters(tuple(row[i] for row in rows)) for i in range(7)]
        VP=tuple(sum(row[0][k] for row in param)/7 for k in range(7));paramerror=max(row[1] for row in param)
    net=[];identities=0
    if mode=='trajectory':
        matrix=tuple(tuple(weights(V,q,v)) for v in VP)
        for i in range(7):net.append(solve(matrix,tuple(row[i] for row in rows)))
    else:
        for i in range(7):V,P=interpolate(tuple(row[i] for row in rows),VP,q);net.append(P)
    net=tuple(net);base=(U,V,3,q,net)
    for row,v in zip(rows,VP):
        w=weights(V,q,v)
        assert all(tuple(sum(a*p[d] for a,p in zip(w,column)) for d in range(3))==row[i] for i,column in enumerate(net));identities+=7
    if scaling is None:
        assert all(p[2]==C[i][2] for i,row in enumerate(net) for p in row)
    if through_origin:
        assert de_boor(U,C,3,F(1,2))==(0,0,0)
        assert all(de_boor(U,row,3,F(1,2))==spine(v) for row,v in zip(rows,vhat))
    r=dict(method='A10.1' if mode=='trajectory' else 'A10.2',requested_K=6,instance_count=len(rows),v_degree=q,spine_placement_parameters=list(map(str,vhat)),interpolation_parameters=list(map(str,VP)),arc_position_residuals=arc_errors,parameter_error_bound=paramerror,u_knots=list(map(str,U)),v_knots=list(map(str,V)),local_section_controls=[[str(x) for x in p] for p in C],placed_section_controls=[[[str(x) for x in p] for p in row] for row in rows],surface_controls=[[[str(x) for x in p] for p in row] for row in net],surface_control_shape=[7,len(net[0])],all_section_control_interpolation_vector_identities=identities,all_whole_section_instances_interpolated=True,all_normal_planes_exact=True,exact_rigid_control_distance_identities=rigid,section_through_origin=through_origin,trajectory_basis_inherited=(mode=='trajectory'),tensor_checks=verify_tensor(*base,steps=3),all_surface_Z_controls_equal_local_section_Z=(scaling is None),whole_surface_Z_positive_lower_bound=str(min(p[2] for p in C)) if scaling is None and not through_origin else None,trajectory_disjoint_from_entire_surface_by_positive_Z=(scaling is None and not through_origin))
    return base,VP,vhat,rows,r

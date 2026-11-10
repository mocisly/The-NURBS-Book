"""Exact whole-section interpolation, with or without spine-derived derivatives."""
from fractions import Fraction as F
from spine_skinning_example_data import SECTION_K,V_HAT,U_HAT
from spine_skinning_derivatives import construct as derivatives
from bounded_curve_approximation import chord_parameters
from inverse_knot_projection import solve
from global_interpolation_data import interpolate
from surface_geometry import weights,verify_tensor
from bspline_math import piece,derivative,evaluate
def construct(with_derivatives=True,vhat=V_HAT,uhat=U_HAT):
    Q,P,D,C,DV,r=derivatives(vhat,uhat)
    parameter_results=[chord_parameters(tuple(Q[k][i] for k in range(5))) for i in range(7)]
    VP=tuple(sum(row[0][k] for row in parameter_results)/7 for k in range(5));assert VP[0]==0 and VP[-1]==1 and all(a<b for a,b in zip(VP,VP[1:]))
    q=3;net=[];constraint_count=0
    if with_derivatives:
        internal=(VP[1]/2,)+tuple(x for j in range(1,3) for x in ((2*VP[j]+VP[j+1])/3,(VP[j]+2*VP[j+1])/3))+((VP[-2]+1)/2,)
        V=(F(0),)*4+internal+(F(1),)*4;assert len(V)-4==10
        matrix=[]
        for v in VP:
            span=next((s for s in range(3,10) if V[s]<=v<V[s+1]),9)
            matrix.extend((tuple(weights(V,3,v)),tuple(evaluate(derivative(piece(V,j,3,span)),v) for j in range(10))))
        for i in range(7):
            rhs=tuple(row for k in range(5) for row in (Q[k][i],DV[i][k]));controls=solve(tuple(matrix),rhs)
            assert all(tuple(sum(a*p[d] for a,p in zip(row,controls)) for d in range(3))==pt for row,pt in zip(matrix,rhs));constraint_count+=10
            net.append(controls)
    else:
        for i in range(7):V,controls=interpolate(tuple(Q[k][i] for k in range(5)),VP,3);net.append(controls);constraint_count+=5
    net=tuple(net);base=(SECTION_K,V,3,3,net)
    for k,v in enumerate(VP):
        W=weights(V,3,v)
        assert all(tuple(sum(a*p[d] for a,p in zip(W,row)) for d in range(3))==Q[k][i] for i,row in enumerate(net))
    r.update(with_derivative_constraints=with_derivatives,degrees=[3,3],surface_control_shape=[7,len(net[0])],all_linear_constraint_vector_identities_exact=constraint_count,all5whole_section_curves_interpolated=True,all5whole_section_derivatives_positive_parallel_to_spine=with_derivatives,derivative_parallel_positive_scalar_bounds_per_section=[[str(min(row[k] for row in C)),str(max(row[k] for row in C))] for k in range(5)],v_parameters=list(map(str,VP)),parameter_error_bound=max(row[1] for row in parameter_results),u_knots=list(map(str,SECTION_K)),v_knots=list(map(str,V)),surface_controls=[[[str(x) for x in p] for p in row] for row in net],tensor_checks=verify_tensor(*base,steps=3),same_input_sections_as='10.4/10.5/10.6')
    return base,VP,Q,r

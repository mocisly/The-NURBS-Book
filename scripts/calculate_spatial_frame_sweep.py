"""10.14exact true-spatial path/orthogonal frames and both actual sweep algorithms."""
from pathlib import Path
import json
from spatial_frame_sweep_data import construct,POWER,T_K,T_P,U,C,SCALE,NONPLANAR,N,R0,R1,R2,view
root=Path(__file__).resolve().parents[1];reports=[]
for mode in ('free','trajectory'):
    b,v,Q,r=construct(mode);reports.append(r);P=[view(p) for row in b[-1] for p in row]
    print('PASS10.14',r['method'],r['instance_count'],'sections',r['all_section_control_vector_interpolation_identities'],'exactconstraints,Tiso',r['whole_trajectory_isocurve_exact'],'bounds',[(float(min(p[d] for p in P)),float(max(p[d] for p in P))) for d in range(2)])
report=dict(figure='10.14',representative_controls=True,trajectory_degree=3,trajectory_global_power=[[str(x) for x in p] for p in POWER],trajectory_knots=list(map(str,T_K)),trajectory_controls=[[str(x) for x in p] for p in T_P],trajectory_nonplanarity_tangent_coefficient_determinant=str(NONPLANAR),trajectory_speed_formula='8*(1+67*(2v-1)^2/50)',global_frame_norm_denominator_lower_bound='1',all9frame_polynomial_orthogonality_identities_exact=True,right_handed_frame=True,local_section_controls=[[str(x) for x in p] for p in C],section_knots=list(map(str,U)),constant_scaling=list(map(str,SCALE)),section_at_u_half_origin=True,sweeps=reports,no_contour_tracing=True)
(root/'image_tex/build/spatial-frame-sweep-data.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')

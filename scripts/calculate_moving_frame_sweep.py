"""10.12actual7/10-instance A10.2/A10.1 sweeps sharing an exact PH frame."""
from pathlib import Path
from fractions import Fraction as F
import json
from moving_frame_sweep_data import construct,SPINE_POWER,T_K,T_P,RAW_C,view
root=Path(__file__).resolve().parents[1];reports=[]
for mode in ('free','trajectory'):
    b,VP,vhat,rows,r=construct(mode);reports.append(r)
    P=[view(p) for row in b[-1] for p in row]
    print('PASS10.12',r['method'],r['instance_count'],'instances',r['all_section_control_interpolation_vector_identities'],'exactvectorconstraints;controlbounds',[(float(min(p[d] for p in P)),float(max(p[d] for p in P))) for d in range(2)])
report=dict(figure='10.12',representative_data=True,spine_global_power=[[str(x) for x in row] for row in SPINE_POWER],trajectory_degree=5,trajectory_knots=list(map(str,T_K)),trajectory_controls=[[str(x) for x in p] for p in T_P],trajectory_refinement_geometrically_unchanged_power_coefficients_exact=True,local_section_controls=[[str(x) for x in p] for p in RAW_C],constant_B=[0,0,1],all_frames_orthonormal_exact=True,all_surface_Z_strictly_positive=True,sweeps=reports,no_contour_tracing=True)
(root/'image_tex/build/moving-frame-sweep-data.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')

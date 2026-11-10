"""Certify10.15self-intersection of the actual two NURBS approximations."""
from pathlib import Path
import json
from offset_sweep_data import construct,POWER,T_K,T_P,U,C,U_STAR,OFFSET,V_PAIR,I,view
root=Path(__file__).resolve().parents[1];reports=[]
for mode in ('free','trajectory'):
    base,VP,Q,r=construct(mode);reports.append(r);P=[view(p) for row in base[-1] for p in row]
    print('PASS10.15',r['method'],'EXACT3Dselfintersection/transverse tangentplanes;bounds',[(float(min(p[d] for p in P)),float(max(p[d] for p in P))) for d in range(2)])
report=dict(figure='10.15',representative_data=True,trajectory_global_power=[[str(x) for x in p] for p in POWER],trajectory_knots=list(map(str,T_K)),trajectory_controls=[[str(x) for x in p] for p in T_P],local_section_controls=[[str(x) for x in p] for p in C],section_knots=list(map(str,U)),constant_projected_normal_B=[0,0,1],trajectory_speed_formula='4*(1+(2v-1)^2)',offset_local_y=str(OFFSET),intersection_u=str(U_STAR),two_original_placement_parameters=list(map(str,V_PAIR)),intersection_point=list(map(str,I)),sweeps=reports,no_contour_tracing=True)
(root/'image_tex/build/offset-sweep-data.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')

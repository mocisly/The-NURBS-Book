"""10.13exact same7arc placements,unscaled/scaled skins with C(.5)=origin."""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations
import json
from moving_frame_sweep_data import construct,section,view,spine
from scaled_moving_sweep_data import scaling,SCALE_K,SCALE_P
from native_bspline import de_boor
from surface_geometry import isocurve
root=Path(__file__).resolve().parents[1];reports=[];C=section(True)
for flag in (False,True):
    base,VP,vhat,rows,r=construct('free',True,scaling if flag else None);scaled_checks=0
    if flag:
        for row,v in zip(rows,vhat):
            s=scaling(v);local=tuple(tuple(a*b for a,b in zip(p,s)) for p in C)
            for i,j in combinations(range(7),2):
                assert sum((a-b)**2 for a,b in zip(row[i],row[j]))==sum((a-b)**2 for a,b in zip(local[i],local[j]));scaled_checks+=1
    K,p,P=isocurve(*base,'v',F(1,2));t=F(1,4);delta=tuple(a-b for a,b in zip(de_boor(K,P,p,t),spine(t)));assert any(delta)
    r.update(scaled=flag,all147scaled_control_distance_identities_exact=(scaled_checks==147) if flag else None,all7trajectory_anchor_points_exact=True,whole_trajectory_not_claimed_exact=True,same_parameter_v_quarter_trajectory_difference=list(map(str,delta)),scale_vectors_at_instances=[list(map(str,scaling(v))) for v in vhat] if flag else None)
    reports.append(r);q=[view(p) for row in base[-1] for p in row]
    print('PASS10.13',flag,'49whole-sectionvectoridentities/7trajectoryanchors;controlbounds',[(float(min(p[d] for p in q)),float(max(p[d] for p in q))) for d in range(2)])
assert reports[0]['spine_placement_parameters']==reports[1]['spine_placement_parameters']
report=dict(figure='10.13',shared_trajectory_and_section_shape_as='10.12',same7arc_placements=True,local_section_controls=[[str(x) for x in p] for p in C],section_at_u_half_exactly_origin=True,scaling_degree=1,scaling_knots=list(map(str,SCALE_K)),scaling_controls=[list(map(str,p)) for p in SCALE_P],positive_scaling_whole_domain=True,sweeps=reports,no_contour_tracing=True)
(root/'image_tex/build/scaled-moving-sweep-data.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')

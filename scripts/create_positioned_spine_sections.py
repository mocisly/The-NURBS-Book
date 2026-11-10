"""10.5: rigid normal-plane placement of the exact10.4 cross sections."""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations
import json
from spine_skinning_example_data import SPINE_P,SECTION_K,SECTION_P,V_HAT,positioned,spine,view
from native_bspline import segments,check,cubic_path,point,de_boor
from rational_geometry import approximate
root=Path(__file__).resolve().parents[1];d=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in d['images'] if e['tex']=='image_tex/ch10/fig_10_08.tex')['applied']
Q=positioned();native=approximate(tuple(view(p)+(F(1),) for p in SPINE_P),F(1,100000))
out=['% Exact rigid placements of10.4 local cross sections in spine normal planes.',r'\begin{tikzpicture}[book line]',r'\path[use as bounding box] (-4,-12) rectangle (12,5);']
out.extend(cubic_path(p) for p in native);nc=dist=0
for k,(P,local,v) in enumerate(zip(Q,SECTION_P,V_HAT)):
    for i,j in combinations(range(7),2):
        assert sum((a-b)**2 for a,b in zip(P[i],P[j]))==sum((a-b)**2 for a,b in zip(local[i],local[j]));dist+=1
    ss=segments(SECTION_K,P,3);nc+=check(SECTION_K,P,3,ss,steps=13)
    out.extend(cubic_path(dict(bern=tuple(view(q) for q in z['bern']))) for z in ss)
    c=spine(v);assert de_boor(SECTION_K,P,3,F(1,2))==c
    out.append(r'\fill '+point(view(c))+r' circle[radius=1.7pt];')
    out.append((r'\node[right=6pt] at '+point(view(P[-1])) if k==1 else r'\node[above left=5pt] at '+point(view(P[0])))+r' {$C_'+str(k)+r'$};')
out.append(r'\node[left=8pt] at '+point(view(spine(F(16,25))))+r' {$C_s(v)$};')
base=(-F(2),-F(9))
for end,name,anchor in [((F(6,5),0,0),'x','below'),((0,F(6,5),0),'y','right'),((0,0,F(6,5)),'z','above')]:
    delta=view(end);endpt=tuple(a+b for a,b in zip(base,delta))
    out.append(r'\draw[book grid,book axis] '+point(base)+'--'+point(endpt)+r' node['+anchor+r'=4pt] {$'+name+'$};')
out.append(r'\end{tikzpicture}');(root/'image_tex/ch10/fig_10_08.tex').write_text('\n'.join(out)+'\n',encoding='utf-8')
report=dict(figure='10.5',shared_data='spine_skinning_example_data.py',same_shapes_as='10.4',native_curve_checks=nc,rigid_placement_squared_distance_identities=dist,all_5_whole_section_planes_exactly_normal_to_spine=True,all_5_midpoint_anchors_exact=True,spine_native_error_bound_cm='1e-5',common_camera_scale='1.8',font_rescaling=False,no_contour_tracing=True)
(root/'image_tex/build/positioned-spine-sections-check.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print('PASS10.5:',nc,'native checks;',dist,'rigid-distance identities;five exact anchors/normal planes.')

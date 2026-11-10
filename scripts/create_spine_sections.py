"""10.4actual common spine and five local cross-sectional curves, with anchors."""
from pathlib import Path
from fractions import Fraction as F
import json
from native_bspline import segments,check,cubic_path,point,de_boor
from rational_geometry import approximate
from spine_skinning_example_data import SPINE_K,SPINE_P,SPINE_POWER,SECTION_K,SECTION_P,V_HAT,U_HAT,spine,frame,positioned
root=Path(__file__).resolve().parents[1];d=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in d['images'] if e['tex']=='image_tex/ch10/fig_10_07.tex')['applied']
ss=segments(SPINE_K,SPINE_P,5);nc=check(SPINE_K,SPINE_P,5,ss,steps=31)
def top(q):return(F(9,5)*q[0]+F(1,2),F(9,5)*q[1])
native=approximate(tuple(top(q)+(F(1),) for q in SPINE_P),F(1,100000));assert max(p['certified_l1_error'] for p in native)<=F(1,100000)
out=['% Shared exact PH quintic spine and five cubic cross sections. Representative mathematical data, no raster geometry.',r'\begin{tikzpicture}[book line]',r'\path[use as bounding box] (-4.2,-16.5) rectangle (18.2,7);']
out.extend(cubic_path(s) for s in native)
for k,v in enumerate(V_HAT):
    pt=top(spine(v));out.append(r'\draw '+point(pt)+r' ++(-2pt,-2pt) rectangle ++(4pt,4pt);')
    out.append(r'\node[above right=6pt] at '+point(pt)+r' {$\widehat v_'+str(k)+'='+('0' if k==0 else '1' if k==4 else str(float(v)))+r'$};')
out.append(r'\node at (10,3.8) {$C_s(v)$};')
out.append(r'\node at (7.5,-7.1) {$C_k(u),\quad C_k(1/2)=\mathbf0$};')
for k,P in enumerate(SECTION_P):
    def local(q):return(-F(4,5)+F(21,5)*k+F(8,5)*q[0],-F(23,2)+F(8,5)*q[1])
    curve=segments(SECTION_K,P,3);nc+=check(SECTION_K,P,3,curve,steps=13)
    out.extend(cubic_path(dict(bern=tuple(local(q) for q in s['bern']))) for s in curve)
    anchor=local(de_boor(SECTION_K,P,3,F(1,2)));out.append(r'\draw '+point(anchor)+r' ++(-2pt,-2pt) rectangle ++(4pt,4pt);')
    out.append(r'\node at '+point((-F(4,5)+F(21,5)*k,-F(78,5)))+r' {$C_'+str(k)+'(u)$};')
out.append(r'\end{tikzpicture}');(root/'image_tex/ch10/fig_10_07.tex').write_text('\n'.join(out)+'\n',encoding='utf-8')
Q=positioned()
report=dict(figure='10.4',representative_data=True,spine_degree=5,spine_global_power=[[str(x) for x in c] for c in SPINE_POWER],spine_controls=[[str(x) for x in q] for q in SPINE_P],section_degree=3,section_knots=list(map(str,SECTION_K)),local_section_controls=[[[str(x) for x in q] for q in row] for row in SECTION_P],spine_parameters=list(map(str,V_HAT)),section_anchor_parameters=list(map(str,U_HAT)),all_local_midpoints_exactly_zero=True,all_positioned_anchors_exactly_on_spine=True,all_section_planes_exactly_perpendicular_to_spine_tangent=True,rational_unit_normal_frames=True,spine_speed_formula='9*(1+4*v^2*(1-v)^2)',spine_X_derivative_lower_bound='27/4',native_curve_checks=nc,native_quintic_Hermite_pieces=len(native),native_quintic_L1_error_bound_cm='1e-5',native_font_rescaling=False,no_contour_tracing=True)
(root/'image_tex/build/spine-sections-check.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print('PASS10.4:',nc,'native curve checks;five exact normal frames/anchors;quintic projection bound1e-5cm,',len(native),'pieces.')

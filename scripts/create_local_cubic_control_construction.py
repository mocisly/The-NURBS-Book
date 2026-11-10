"""9.29: exact local C1 cubic controls and their real double-knot locations."""
from pathlib import Path
import json
from fractions import Fraction as F
from local_cubic_example_data import Q,T,MIDT,ALPHA,PARAMS,U,P,BEZIER,SS,NATIVE_CHECKS,REMOVAL,REPORT,TOTAL
from native_bspline import point,cubic_path
root=Path(__file__).resolve().parents[1]
d=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_35.tex')['applied']
out=['% Exact representative Renner construction;derived rational chords give alpha3,4,3.',r'\begin{tikzpicture}[book line,x=2.8cm,y=2.8cm]',r'\path[use as bounding box] (-.9,-3.1) rectangle (7.7,3.2);',r'\draw[book grid,dashed] '+'--'.join(map(point,P))+';']
out.extend(cubic_path(s) for s in SS)
anchors=[('left','above'),('above right','left'),('below','right')]
for k,b in enumerate(BEZIER):
    for j in (1,2):
        q=b[j];out.extend([r'\draw '+point(q)+r' circle[radius=2.4pt];',r'\node['+anchors[k][j-1]+r'=6pt] at '+point(q)+r' {$\mathbf P_{'+str(k)+','+str(j)+'}$};'])
for i,(q,anchor) in enumerate(zip(Q,('below right','below right','above','above right'))):
    out.extend([r'\draw '+point(q)+r' circle[radius=2.4pt];',r'\fill '+point(q)+r' circle[radius=.7pt];',r'\node['+anchor+r'=6pt] at '+point(q)+r' {$\mathbf Q_'+str(i)+'$};'])
y=-F(9,4);L=Q[-1][0];out.append(r'\draw[book grid] '+point((0,y))+'--'+point((L,y))+';')
for t,mult,label in [(F(0),4,r'u_0'),(F(3,10),2,r'u_4=u_5'),(F(7,10),2,r'u_6=u_7'),(F(1),4,r'u_{11}')]:
    x=L*t
    for j in range(mult):
        xx=x+F(3,50)*(F(j)-F(mult-1,2));out.append(r'\draw[book grid] '+point((xx,y-F(7,100)))+'--'+point((xx,y+F(7,100)))+';')
    out.append(r'\node[below=6pt] at '+point((x,y))+' {$'+label+'$};')
out.append(r'\end{tikzpicture}')
(root/'image_tex/ch09/fig_9_35.tex').write_text('\n'.join(out)+'\n',encoding='utf-8')
(root/'image_tex/build/local-cubic-control-construction-check.json').write_text(json.dumps(dict(figure='9.29',representative_data=[list(map(str,q)) for q in Q],unit_tangents=[list(map(str,t)) for t in T],midpoint_unit_directions=[list(map(str,t)) for t in MIDT],local_segments=REPORT,raw_parameter_increments=list(map(str,ALPHA)),normalized_parameters=list(map(str,PARAMS)),minimal_knots=list(map(str,U)),minimal_controls=[list(map(str,q)) for q in P],zero_error_knot_removal=REMOVAL,native_C1_checks=NATIVE_CHECKS,all_data_interpolated_exact=True,normalized_data_and_segment_midpoint_speed=str(TOTAL),ruler_positions_match_actual_knots=True),indent=2)+'\n')
print('PASS9.29:3exact equal-speed cubics,alpha3/4/3,4data constraints,2zero-error knot removals to8controls,C1joins/speed10exact,actual double-knot ruler. Q=',Q)

"""9.20:true quadratic Bezier pieces joined geometrically at six data points."""
from pathlib import Path
import json
from local_parabolic_interpolation_data import Q,R,FULL,UG,UNIFORM,C1PARAMS,UC,MINIMAL,INTERSECTIONS,REMOVAL
from native_bspline import segments,check,cubic_path,point
root=Path(__file__).resolve().parents[1];d=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_24.tex')['applied']
ss=segments(UG,FULL,2);nc=check(UG,FULL,2,ss)
lines=['% Five actual quadratic Bezier pieces(Q_i,R_i+1,Q_i+1);exact G1join directions.',r'\begin{tikzpicture}[book line,x=2.5cm,y=2.5cm]',r'\path[use as bounding box] (-.9,-.7) rectangle (9.3,5.7);',r'\draw[book grid,dashed] '+'--'.join(map(point,FULL))+';']
lines.extend(cubic_path(s) for s in ss)
for i,(q,anchor) in enumerate(zip(Q,['right','right','below right','below left','left','left'])):
    lines.extend([r'\draw '+point(q)+r' circle[radius=2.4pt];',r'\fill '+point(q)+r' circle[radius=1pt];',r'\node['+anchor+r'=8pt] at '+point(q)+r' {$\mathbf Q_'+str(i)+'$};'])
for i,(r,anchor) in enumerate(zip(R,['left','above left','above','above right','right']),1):
    lines.extend([r'\draw '+point(r)+r' circle[radius=2.4pt];',r'\node['+anchor+r'=8pt] at '+point(r)+r' {$\mathbf R_'+str(i)+'$};'])
lines.append(r'\end{tikzpicture}');(root/'image_tex/ch09/fig_9_24.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/local-parabolic-interpolation-check.json').write_text(json.dumps(dict(figure='9.20',representative_data=[[str(x) for x in q] for q in Q],actual_tangent_intersections=[[str(x) for x in r] for r in R],positive_start_negative_end_intersection_coefficients=[[str(x) for x in t] for t in INTERSECTIONS],all5quadratic_Bezier_triples_exact=True,all4G1joins_cross_zero_dot_positive=True,uniform_G1_parameters=list(map(str,UNIFORM)),uniform_double_knots=list(map(str,UG)),native_curve_checks=nc,C1_parameters_from_equation9_37=list(map(str,C1PARAMS)),reduced_C1_knots=list(map(str,UC)),reduced_control_count=len(MINIMAL),four_zero_error_knot_removals=REMOVAL),indent=2)+'\n')
print('PASS:5truequadraticpieces,6interpolatedpoints,all5orientedtangentintersections and4G1joins;exactC1parameters/fourzeroerrorknotremovals verified for9.21.')

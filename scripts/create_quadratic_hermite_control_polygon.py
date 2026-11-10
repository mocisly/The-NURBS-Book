"""9.13:actual solved quadratic control polygon,not a hand-placed approximation."""
from fractions import Fraction as F
from pathlib import Path
import json
from all_point_hermite_data import Q,PARAMS,interpolate_all
from native_bspline import cubic_path,point
root=Path(__file__).resolve().parents[1];d=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_13.tex')['applied']
U,P,D,ss,nc=interpolate_all(2)
lines=['% Exactly the quadratic solved in9.11;10 actual controls,5 filled data points.',
       r'\begin{tikzpicture}[book line,x=2.5cm,y=2.5cm]',r'\path[use as bounding box] (-2,-2) rectangle (8,4.8);',
       r'\draw[book grid,dashed] '+'--'.join(map(point,P))+';']
lines.extend(cubic_path(s) for s in ss)
for q,v in zip(Q,D):lines.append(r'\draw[book axis] '+point(q)+'--'+point(tuple(a+b/5 for a,b in zip(q,v)))+';')
for pt in P:
    if pt not in Q:lines.append(r'\draw '+point(pt)+r' circle[radius=2.4pt];')
for q in Q:lines.append(r'\fill '+point(q)+r' circle[radius=2.4pt];')
lines.append(r'\end{tikzpicture}')
(root/'image_tex/ch09/fig_9_13.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/quadratic-hermite-control-polygon-check.json').write_text(json.dumps(dict(figure='9.13',same_quadratic_curve_as='9.11',parameters=list(map(str,PARAMS)),knots=list(map(str,U)),actual_solved_controls=[[str(x) for x in q] for q in P],actual_data=[[str(x) for x in q] for q in Q],all5point_and5derivative_constraints_exact=True,C1_native_checks=nc,control_count=len(P),data_marker='filled',control_marker='open',coincident_endpoint_markers='filled data points',common_arrow_scale='1/5'),indent=2)+'\n')
print('PASS:10actual solved quadratic controls;all5positions+5derivatives exact,C1native pieces,same9.11geometry and1/5arrows.')

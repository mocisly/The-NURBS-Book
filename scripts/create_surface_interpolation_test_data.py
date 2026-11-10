"""9.15:sixteen semantic3Ddata points;shared numeric input for later comparisons."""
from fractions import Fraction as F
from pathlib import Path
import json
import sys
from mesh_interpolation_example_data import X,Y,Q,H,A,G,camera
from native_bspline import point
root=Path(__file__).resolve().parents[1];d=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_17.tex')['applied'] or '--refresh' in sys.argv
assert len(set(q for row in Q for q in row))==16
assert all(q[2]>=3 for row in Q[:2] for q in row) and all(q[2]<=F(1,10) for row in Q[2:] for q in row)
lines=['% Representative4x4step data with small transverse variation:z_ij=H_i+A_i*G_j;shared9.16/17.',r'\begin{tikzpicture}[book line]',r'\path[use as bounding box] (-13,-7) rectangle (13,17);']
for end,name,anchor in [((F(3),0,0),'x','below left'),((0,F(3),0),'y','below right'),((0,0,F(22,5)),'z','above')]:
    lines.append(r'\draw[book grid,book axis] (0,0)--'+point(camera(end))+r' node['+anchor+r'=5pt] {$'+name+'$};')
for row in Q:lines.append(r'\draw[book grid,dashed] '+'--'.join(point(camera(q)) for q in row)+';')
for col in zip(*Q):lines.append(r'\draw[book grid,dashed] '+'--'.join(point(camera(q)) for q in col)+';')
for row in Q:
    for q in row:lines.append(r'\fill '+point(camera(q))+r' circle[radius=2.4pt];')
lines.append(r'\end{tikzpicture}')
(root/'image_tex/ch09/fig_9_17.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/surface-interpolation-test-data-check.json').write_text(json.dumps(dict(figure='9.15',representative_data=[[[str(x) for x in q] for q in row] for row in Q],x_coordinates=list(map(str,X)),y_coordinates=list(map(str,Y)),distinct_data_count=16,height_formula='H_i+A_i*G_j',H=list(map(str,H)),A=list(map(str,A)),G=list(map(str,G)),step_profile_with_small_transverse_variation=True,dashed_lines='data adjacency only,not spline control net',camera_scale='7/2',shared_input_for_later_figures=['9.16','9.17']),indent=2)+'\n')
print('PASS:16distinct exact3Dstep data,8low/8high,small transverse height variation;shared input for parameter/degree comparisons.')

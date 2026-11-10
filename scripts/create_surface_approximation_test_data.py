"""9.44: explicitly chosen9x9staircase data,not a fitted/traced image."""
from pathlib import Path
from fractions import Fraction as F
import json
from surface_approximation_example_data import X,Y,H,B,Q,camera
from native_bspline import point
root=Path(__file__).resolve().parents[1];d=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_52.tex')['applied']
plateaus=[]
for a in range(3):
    row=[]
    for b in range(3):
        heights={Q[i][j][2] for i in range(3*a,3*a+3) for j in range(3*b,3*b+3)};assert len(heights)==1;row.append(str(heights.pop()))
    plateaus.append(row)
assert len({p for row in Q for p in row})==81
out=['% Representative81point3x3staircase blocks;shared exact data for9.44..47.',r'\begin{tikzpicture}[book line]',r'\path[use as bounding box] (-11,-6) rectangle (11,13);']
for rows in (Q,tuple(zip(*Q))):
    for row in rows:out.append(r'\draw[book grid,dashed] '+'--'.join(point(camera(p)) for p in row)+';')
out.extend(r'\fill '+point(camera(p))+r' circle[radius=1.2pt];' for row in Q for p in row)
for end,name,anchor in [((F(3),0,0),'x','below left'),((0,F(3),0),'y','below right'),((0,0,F(4)),'z','above')]:
    out.append(r'\draw[book grid,book axis] (0,0)--'+point(camera(end))+r' node['+anchor+r'=5pt] {$'+name+'$};')
out.append(r'\end{tikzpicture}')
(root/'image_tex/ch09/fig_9_52.tex').write_text('\n'.join(out)+'\n',encoding='utf-8')
(root/'image_tex/build/surface-approximation-test-data-check.json').write_text(json.dumps(dict(figure='9.44',representative=True,data_shape=[9,9],distinct_data_count=81,X=list(map(str,X)),Y=list(map(str,Y)),step_heights=list(map(str,H)),coupling_selector=list(map(str,B)),height_formula='H_i+H_j+B_i*B_j/10',flat_three_by_three_block_heights=plateaus,data=[[[str(x) for x in p] for p in row] for row in Q],camera_scale='3',common_data_for_figures=['9.44','9.45','9.46','9.47']),indent=2)+'\n')
print('PASS9.44:81distinct exact data,nine3x3constant-height blocks,shared representative staircase dataset for subsequent fits/interpolant.')

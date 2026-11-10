"""7.7: actual uniform-u samples from the polynomial parametrization7.10."""
from pathlib import Path
from fractions import Fraction as F
import json
from native_bspline import point

root=Path(__file__).resolve().parents[1];manifest=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in manifest['images'] if e['tex']=='image_tex/ch07/fig_7_07.tex')['applied']
points=[]
for i in range(21):
    u=F(i,10);x,y=u*u,2*u;assert y*y==4*x;points.append((x,y))
lines=['% Eq7.10 representative a1; u=i/10,i0..20; exact polynomial samples.',
       r'\begin{tikzpicture}[book line,x=1.5cm,y=1.5cm]',r'\path[use as bounding box] (-.7,-.8) rectangle (5.9,5.1);',
       r'\draw[book axis] (-.35,0)--(5.4,0) node[right=4pt] {$x$};',
       r'\draw[book axis] (0,-.4)--(0,4.8) node[above=4pt] {$y$};']
for pt in points[1:-1]:
    lines += [r'\begin{scope}[shift={'+point(pt)+'}]',r'\draw (-2pt,0)--(2pt,0) (0,-2pt)--(0,2pt);',r'\end{scope}']
lines += [r'\draw '+point(points[0])+r' circle[radius=2pt] node[below left=6pt] {$0$};',
          r'\draw '+point(points[-1])+r' circle[radius=2pt] node[above left=7pt] {$u=2$};',r'\end{tikzpicture}']
(root/'image_tex/ch07/fig_7_07.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/parabola-samples-check.json').write_text(json.dumps({'figure':'7.7','a':'1','parameter_grid':'u=i/10,i=0..20','exact_implicit_equation_checks':21,'points':[[str(x) for x in pt] for pt in points]},indent=2)+'\n')
print('PASS:21 exact uniform-parameter parabola samples; vertex and u2 endpoint exact.')

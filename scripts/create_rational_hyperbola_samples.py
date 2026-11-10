"""7.6: exact uniformly spaced rational parameters on the right hyperbola branch."""
from pathlib import Path
from fractions import Fraction as F
import json
from native_bspline import point

root=Path(__file__).resolve().parents[1];manifest=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in manifest['images'] if e['tex']=='image_tex/ch07/fig_7_06.tex')['applied']
points=[]
for i in range(21):
    u=F(i,25);w=1-u*u;x=(1+u*u)/w;y=2*u/w
    assert w>=F(9,25) and x*x-y*y==1;points.append((x,y))
lines=['% Eq7.9 representative a=b=1; u=i/25,i0..20, hence0<=u<=4/5<1.',
       '% Exact rational points show nonuniform geometric spacing without crossing the pole.',
       r'\begin{tikzpicture}[book line,x=1.5cm,y=1.5cm]',r'\path[use as bounding box] (-.7,-.8) rectangle (5.9,5.4);',
       r'\draw[book axis] (-.35,0)--(5.4,0) node[right=4pt] {$x$};',
       r'\draw[book axis] (0,-.4)--(0,5) node[above=4pt] {$y$};']
for pt in points[1:-1]:
    lines += [r'\begin{scope}[shift={'+point(pt)+'}]',r'\draw (-1.5pt,0)--(1.5pt,0) (0,-1.5pt)--(0,1.5pt);',r'\end{scope}']
lines += [r'\draw '+point(points[0])+r' circle[radius=2pt] node[below=6pt] {$(a,0)$};',
          r'\draw '+point(points[-1])+r' circle[radius=2pt] node[above left=7pt] {$u=\frac45$};',r'\end{tikzpicture}']
(root/'image_tex/ch07/fig_7_06.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/rational-hyperbola-samples-check.json').write_text(json.dumps({'figure':'7.6','a':'1','b':'1','parameter_grid':'u=i/25,i=0..20','exact_implicit_equation_checks':21,'denominator_lower_bound':'9/25','points':[[str(x) for x in pt] for pt in points]},indent=2)+'\n')
print('PASS:21 exact rational hyperbola samples, denominator>=9/25 and endpoint finite at u4/5.')

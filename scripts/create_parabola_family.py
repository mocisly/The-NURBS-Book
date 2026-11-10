"""7.4: the four given parabolas as exact native polynomial paths."""
from pathlib import Path
from fractions import Fraction as F
import json
from polynomial_native import bernstein
from native_bspline import cubic_path
from bspline_math import evaluate

root=Path(__file__).resolve().parents[1];manifest=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in manifest['images'] if e['tex']=='image_tex/ch07/fig_7_04.tex')['applied']
aa=(F(5),F(3,2),F(7,10),F(3,10))
lines=['% Exact prescribed family y^2=4ax with a5,3/2,7/10,3/10.',
       r'\begin{tikzpicture}[book line,x=1.6cm,y=1.6cm]',r'\path[use as bounding box] (-.8,-3.1) rectangle (7,3.5);',
       r'\draw[book axis] (-.4,0)--(6.3,0) node[right=4pt] {$x$};',
       r'\draw[book axis] (0,-2.9)--(0,3.1) node[above=4pt] {$y$};']
for a in aa:
    power=((F(0),F(0),1/(4*a)),(F(0),F(1)))
    for i in range(101):
        t=-F(5,2)+5*F(i,100);x,y=(evaluate(c,t) for c in power);assert y*y==4*a*x
    lines.append(cubic_path({'bern':bernstein(power,-F(5,2),F(5,2))}))
lines += [r'\draw (0,0) circle[radius=1.8pt] node[below left=5pt] {$0$};',
          r'\node[anchor=north west] at (3.1,3.15) {$a=5,\ \frac32,\ \frac7{10},\ \frac3{10}$};',r'\end{tikzpicture}']
(root/'image_tex/ch07/fig_7_04.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/parabola-family-check.json').write_text(json.dumps({'figure':'7.4','a':list(map(str,aa)),'display_y_domain':['-5/2','5/2'],'exact_implicit_equation_checks':404,'native_paths':'4 exact quadratic polynomials degree elevated to cubic'},indent=2)+'\n')
print('PASS:404 exact parabola identities; four exact native quadratic paths.')

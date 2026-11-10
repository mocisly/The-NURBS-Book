"""7.1: exact parabola example satisfying the focus/directrix definition."""
from pathlib import Path
from fractions import Fraction as F
import json
from polynomial_native import bernstein
from native_bspline import cubic_path,point
from bspline_math import evaluate

root=Path(__file__).resolve().parents[1];d=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in d['images'] if e['tex']=='image_tex/ch07/fig_7_01.tex')['applied']
power=((F(1),F(0),F(1,4)),(F(0),F(1)))
for i in range(101):
    t=-F(16,5)+F(33,5)*F(i,100);x,y=(evaluate(c,t) for c in power)
    assert (x-2)**2+y*y==x*x and x>0
P=(F(13,4),F(3));D=(F(0),F(3));focus=(F(2),F(0))
assert sum((a-b)**2 for a,b in zip(P,focus))==P[0]**2
lines=['% Focus(2,0),directrix x=0,e=1: x=1+y^2/4 exactly.',
       '% The y-axis coincides with the directrix as required by Eq7.1; vertex is x=1.',
       r'\begin{tikzpicture}[book line,x=1.3cm,y=1.3cm]',
       r'\path[use as bounding box] (-2,-4.2) rectangle (5.8,4.8);',
       r'\draw[book axis] (-.6,0)--(5.2,0) node[right=4pt] {$x$};',
       r'\draw[book axis] (0,-3.8)--(0,4.1) node[above right=4pt] {$y$};',
       r'\node[above left=5pt] at (0,4.1) {$x=0$};',
       cubic_path({'bern':bernstein(power,-F(16,5),F(17,5))}),
       r'\draw[book grid] '+point(D)+'--'+point(P)+'--'+point(focus)+';',
       r'\draw[book grid] (0,2.84)--(.16,2.84)--(.16,3);',
       r'\draw '+point(D)+r' circle[radius=1.8pt] node[left=6pt] {$\mathbf D(0,y)$};',
       r'\draw '+point(P)+r' circle[radius=1.8pt] node[above left=8pt] {$\mathbf P(x,y)$};',
       r'\draw '+point(focus)+r' circle[radius=1.8pt] node[below right=6pt] {$\mathbf F(k,0)$};',
       r'\node[below left=4pt] at (0,0) {$0$};',r'\end{tikzpicture}']
(root/'image_tex/ch07/fig_7_01.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/focus-directrix-check.json').write_text(json.dumps({'figure':'7.1','example':'parabola e=1,k=2','focus':list(map(str,focus)),'point':list(map(str,P)),'directrix':'x=0,coincident with y axis','vertex':['1','0'],'exact_squared_distance_equalities':101,'native_curve':'exact quadratic Bernstein elevated to cubic'},indent=2)+'\n')
print('PASS:101 exact PF^2=PD^2 identities; y-axis/directrix coincide; native quadratic geometry.')

"""7.5: actual uniform-u samples of Eq7.8, independent of raster marker locations."""
from pathlib import Path
from fractions import Fraction as F
import json
from native_bspline import point

root=Path(__file__).resolve().parents[1];manifest=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in manifest['images'] if e['tex']=='image_tex/ch07/fig_7_05.tex')['applied']
a,b=F(4),F(2);points=[]
for i in range(21):
    u=F(i,20);x=a*(1-u*u)/(1+u*u);y=2*b*u/(1+u*u)
    assert x*x/(a*a)+y*y/(b*b)==1;points.append((x,y))
assert points[0]==(a,0) and points[-1]==(0,b)
lines=['% Eq7.8 with representative a4,b2; plus signs are u=i/20, i1..19.',
       '% Endpoint circles at (a,0),(0,b); positions computed exactly, never raster sampled.',
       r'\begin{tikzpicture}[book line,x=1.8cm,y=1.8cm]',r'\path[use as bounding box] (-.9,-.8) rectangle (5,3);',
       r'\draw[book axis] (-.35,0)--(4.6,0) node[right=4pt] {$x$};',
       r'\draw[book axis] (0,-.4)--(0,2.7) node[above=4pt] {$y$};']
for pt in points[1:-1]:
    lines += [r'\begin{scope}[shift={'+point(pt)+'}]',r'\draw (-2pt,0)--(2pt,0) (0,-2pt)--(0,2pt);',r'\end{scope}']
lines += [r'\draw (4,0) circle[radius=2pt] node[below=6pt] {$(a,0)$};',
          r'\draw (0,2) circle[radius=2pt] node[left=6pt] {$(0,b)$};',r'\end{tikzpicture}']
(root/'image_tex/ch07/fig_7_05.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/rational-ellipse-samples-check.json').write_text(json.dumps({'figure':'7.5','a':str(a),'b':str(b),'parameter_grid':'u=i/20,i=0..20','exact_implicit_equation_checks':21,'points':[[str(x) for x in pt] for pt in points]},indent=2)+'\n')
print('PASS:21 exact uniform rational-parameter samples on the prescribed elliptic arc formula; endpoint identities exact.')

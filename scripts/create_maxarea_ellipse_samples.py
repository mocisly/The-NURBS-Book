"""7.8: uniform angular samples of Eq7.15, matching7.5's representative ellipse."""
from pathlib import Path
from math import sin,cos,pi
from fractions import Fraction as F
import json
from native_bspline import point

root=Path(__file__).resolve().parents[1];manifest=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in manifest['images'] if e['tex']=='image_tex/ch07/fig_7_08.tex')['applied']
a,b=4,2;points=[(a*cos(i*pi/40),b*sin(i*pi/40)) for i in range(21)]
points[0]=(4.,0.);points[-1]=(0.,2.)
residual=max(abs(x*x/(a*a)+y*y/(b*b)-1) for x,y in points);assert residual<1e-14
cross=[x*v-y*u for (x,y),(u,v) in zip(points,points[1:])]
area_residual=max(abs(c-a*b*sin(pi/40)) for c in cross);assert area_residual<1e-13
rounded=[tuple(F(f'{x:.10f}') for x in pt) for pt in points]
rounding=max(sum(abs(float(x)-y) for x,y in zip(q,p)) for q,p in zip(rounded,points));assert rounding<1e-10
lines=['% Eq7.15 on same representative a4,b2 ellipse as Fig7.5; u=i*pi/40.',
       '% Analytic trigonometric samples; numerical residuals and ten-decimal rounding in report.',
       r'\begin{tikzpicture}[book line,x=1.8cm,y=1.8cm]',r'\path[use as bounding box] (-.9,-.8) rectangle (5,3);',
       r'\draw[book axis] (-.35,0)--(4.6,0) node[right=4pt] {$x$};',
       r'\draw[book axis] (0,-.4)--(0,2.7) node[above=4pt] {$y$};']
for pt in rounded[1:-1]:
    lines += [r'\begin{scope}[shift={'+point(pt)+'}]',r'\draw (-2pt,0)--(2pt,0) (0,-2pt)--(0,2pt);',r'\end{scope}']
lines += [r'\draw (4,0) circle[radius=2pt] node[below=6pt] {$(a,0)$};',
          r'\draw (0,2) circle[radius=2pt] node[left=6pt] {$(0,b)$};',r'\end{tikzpicture}']
(root/'image_tex/ch07/fig_7_08.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/maxarea-ellipse-samples-check.json').write_text(json.dumps({'figure':'7.8','a':a,'b':b,'parameter_grid':'u=i*pi/40,i=0..20','implicit_equation_numerical_max_residual':residual,'adjacent_cross_product_ab_sin_delta_max_residual':area_residual,'native_coordinate_rounding_max_L1_error':rounding,'points':points},indent=2)+'\n')
print(f'PASS:21 analytic angular samples; implicit residual{residual:.2g}, equal-sector cross residual{area_residual:.2g}, native rounding{rounding:.2g}.')

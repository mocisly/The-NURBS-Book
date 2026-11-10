"""7.9: uniform hyperbolic parameters at precisely7.6's geometric endpoints."""
from pathlib import Path
from math import sinh,cosh,log
from fractions import Fraction as F
import json
from native_bspline import point

root=Path(__file__).resolve().parents[1];manifest=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in manifest['images'] if e['tex']=='image_tex/ch07/fig_7_09.tex')['applied']
h=log(9);points=[(cosh(i*h/20),sinh(i*h/20)) for i in range(21)]
points[0]=(1.,0.);points[-1]=(41/9,40/9)
residual=max(abs(x*x-y*y-1) for x,y in points);assert residual<1e-13
cross=[x*v-y*u for (x,y),(u,v) in zip(points,points[1:])]
sector_residual=max(abs(c-sinh(h/20)) for c in cross);assert sector_residual<1e-13
rounded=[tuple(F(f'{x:.10f}') for x in pt) for pt in points]
rounding=max(sum(abs(float(x)-y) for x,y in zip(q,p)) for q,p in zip(rounded,points));assert rounding<1e-10
assert abs(cosh(h)-41/9)<1e-14 and abs(sinh(h)-40/9)<1e-14
lines=['% Eq7.16,a=b1,uniform u=i*ln9/20. Same geometric endpoint as rational u4/5 in Fig7.6.',
       '% cosh(ln9)=41/9,sinh(ln9)=40/9; native scale identical to Fig7.6.',
       r'\begin{tikzpicture}[book line,x=1.5cm,y=1.5cm]',r'\path[use as bounding box] (-.7,-.8) rectangle (5.9,5.4);',
       r'\draw[book axis] (-.35,0)--(5.4,0) node[right=4pt] {$x$};',
       r'\draw[book axis] (0,-.4)--(0,5) node[above=4pt] {$y$};']
for pt in rounded[1:-1]:
    lines += [r'\begin{scope}[shift={'+point(pt)+'}]',r'\draw (-1.5pt,0)--(1.5pt,0) (0,-1.5pt)--(0,1.5pt);',r'\end{scope}']
lines += [r'\draw (1,0) circle[radius=2pt] node[below=6pt] {$(a,0)$};',
          r'\draw '+point(rounded[-1])+r' circle[radius=2pt] node[above left=7pt] {$u=\ln9$};',r'\end{tikzpicture}']
(root/'image_tex/ch07/fig_7_09.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/maxarea-hyperbola-samples-check.json').write_text(json.dumps({'figure':'7.9','a':1,'b':1,'parameter_grid':'u=i*ln9/20,i=0..20','same_endpoint_as_figure7_6':['41/9','40/9'],'implicit_equation_numerical_max_residual':residual,'adjacent_cross_product_sinh_delta_max_residual':sector_residual,'native_coordinate_rounding_max_L1_error':rounding,'points':points},indent=2)+'\n')
print(f'PASS:21 analytic hyperbolic samples;implicit residual{residual:.2g},equal-sector residual{sector_residual:.2g}; endpoint matches7.6 exactly.')

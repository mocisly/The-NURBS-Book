"""Fig4.9: the Fig4.8 net/weights with a representative clamped bicubic space."""
from pathlib import Path
from fractions import Fraction as F
import json
from native_bspline import segments,check,cubic_path,de_boor
from rational_geometry import approximate,project
from surface_geometry import isocurve
from nurbs48_data import P,W,H,knots,rational,verify,CAMERA_L1_NORM

root=Path(__file__).resolve().parents[1];target=root/'image_tex/ch04/fig_4_09.tex';assert not target.exists()
p=3;K=knots(p);report=verify(p)
lines=['% Fig4.9: EXACT SAME representative5x5 positions and four weights10 as Fig4.8.',
       '% Bicubic clamped K=(0,0,0,0,1/2,1,1,1,1); interior knot position representative.',
       '% Same camera, axis lengths and lower-panel bounds as Fig4.8.',
       '% Exact homogeneous rational isolines -> native cubic Hermite pieces with certified projected error<=0.0001cm.',
       '% The curve geometry is computed from Pij,wij and Cox bases, never scan contours.',
       r'\begin{tikzpicture}[x={(-.9cm,-.6cm)},y={(1cm,-.35cm)},z={(0cm,1cm)},book line]',
       r'\path[use as bounding box] (canvas cs:x=-5.2cm,y=-4.8cm) rectangle (canvas cs:x=6.6cm,y=5.7cm);',
       r'\draw[book axis] (0,0,0)--(4.7,0,0) node[below left=4pt] {$x$};',
       r'\draw[book axis] (0,0,0)--(0,5.4,0) node[right=4pt] {$y$};',
       r'\draw[book axis] (0,0,0)--(0,0,5) node[above=4pt] {$z$};']
curve_checks=tensor_checks=paths=0;max_error=F(0)
for variable in ('u','v'):
    for j in range(11):
        fixed=F(j,10);k,d,c=isocurve(K,K,p,p,H,variable,fixed)
        segs=segments(k,c,d);curve_checks+=check(k,c,d,segs)
        for h in range(21):
            t=F(h,20);actual=project(de_boor(k,c,d,t))
            assert actual==(rational(K,p,t,fixed) if variable=='u' else rational(K,p,fixed,t));tensor_checks+=1
        for seg in segs:
            for a in approximate(seg['bern'],F(1,10000)/CAMERA_L1_NORM):
                lines.append(cubic_path(a,'book line' if j in (0,10) else 'book grid'))
                paths+=1;max_error=max(max_error,a['certified_l1_error']*CAMERA_L1_NORM)
lines.append(r'\end{tikzpicture}')
target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
report.update(figure='4.9',same_controls_and_weights_as='4.8',
              representative_controls=[[[str(c) for c in pt] for pt in row] for row in P],weights=[[str(w) for w in row] for row in W],
              exact_homogeneous_isocurve_checks=curve_checks,isocurve_vs_rational_tensor_points=tensor_checks,
              native_cubic_isocurve_paths=paths,camera_l1_operator_norm=str(CAMERA_L1_NORM),
              maximum_certified_projected_l1_error_cm=str(max_error))
(root/'image_tex/build/nurbs-cubic-surface-check.json').write_text(json.dumps(report,indent=2)+'\n')
print(f'PASS:121 homogeneous tensor+121 rational basis points,{curve_checks} exact isocurve checks,{tensor_checks} curve/surface comparisons,{paths} certified paths; same net/weights/camera as4.8.')

"""Fig4.8: indexed control net and exact rational tensor-product isolines."""
from pathlib import Path
from fractions import Fraction as F
import json
from native_bspline import segments,check,point,cubic_path,de_boor
from rational_geometry import approximate,project
from surface_geometry import isocurve
from nurbs48_data import P,W,H,knots,rational,verify,CAMERA_L1_NORM

root=Path(__file__).resolve().parents[1];target=root/'image_tex/ch04/fig_4_08.tex';assert not target.exists()
p=2;K=knots(p);report=verify(p)
lines=['% Fig4.8: representative5x5 control positions; original degree2, thirds knots and weights retained.',
       '% w11=w12=w21=w22=10; all remaining21 weights1. Four rings mark those controls.',
       '% Upper net and lower rational surface share coordinates, camera and bounds.',
       '% Native polynomial Hermite paths approximate exact homogeneous rational isocurves.',
       '% Screen L1 error certified<=0.0001cm using3D bound and camera operator norm3/2; no scan outlines.',
       r'\begin{tikzpicture}[x={(-.9cm,-.6cm)},y={(1cm,-.35cm)},z={(0cm,1cm)},book line]',
       r'\path[use as bounding box] (canvas cs:x=-5.2cm,y=-4.8cm) rectangle (canvas cs:x=6.6cm,y=17.2cm);']
curve_checks=tensor_checks=paths=0;max_error=F(0)
for tag,shift in [('a','11.5'),('b','0')]:
    lines += [r'\begin{scope}[yshift='+shift+'cm]',
              r'\draw[book axis] (0,0,0)--(4.7,0,0) node[below left=4pt] {$x$};',
              r'\draw[book axis] (0,0,0)--(0,5.4,0) node[right=4pt] {$y$};',
              r'\draw[book axis] (0,0,0)--(0,0,5) node[above=4pt] {$z$};']
    if tag=='a':
        for row in P:lines.append(r'\draw[book grid,dashed] '+'--'.join(map(point,row))+';')
        for j in range(5):lines.append(r'\draw[book grid,dashed] '+'--'.join(point(P[i][j]) for i in range(5))+';')
        for i,row in enumerate(P):
            for j,pt in enumerate(row):
                lines.append(r'\fill '+point(pt)+' circle[radius=1.15pt];')
                if W[i][j]==10:lines.append(r'\draw '+point(pt)+' circle[radius=2.5pt];')
        for i,j,anchor in [(0,0,'above left'),(1,0,'below left'),(0,1,'above left'),(0,4,'above right'),(4,0,'below right'),(4,4,'above right')]:
            lines.append(r'\node['+anchor+'=5pt] at '+point(P[i][j])+r' {$\mathbf P_{'+str(i)+','+str(j)+'}$};')
    else:
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
    lines += [r'\node at (canvas cs:x=.5cm,y=-4.3cm) {('+tag+')};',r'\end{scope}']
lines.append(r'\end{tikzpicture}')
target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
report.update(figure='4.8',representative_controls=[[[str(c) for c in pt] for pt in row] for row in P],
              weights=[[str(w) for w in row] for row in W],exact_homogeneous_isocurve_checks=curve_checks,
              isocurve_vs_rational_tensor_points=tensor_checks,native_cubic_isocurve_paths=paths,
              camera_l1_operator_norm=str(CAMERA_L1_NORM),maximum_certified_projected_l1_error_cm=str(max_error))
(root/'image_tex/build/nurbs-quadratic-surface-check.json').write_text(json.dumps(report,indent=2)+'\n')
print(f'PASS:121 homogeneous tensor+121 rational basis points,{curve_checks} exact isocurve checks,{tensor_checks} curve/surface comparisons,{paths} certified native paths; projected error{float(max_error):.8f}cm.')

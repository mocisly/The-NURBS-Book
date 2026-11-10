"""Fig3.20(b), source22: exact isoparametric curves of the same native control net."""
from pathlib import Path
from fractions import Fraction as F
import json
from native_bspline import segments,check,cubic_path,de_boor
from surface320_data import U,V,P,weights,tensor,verify

root=Path(__file__).resolve().parents[1];target=root/'image_tex/ch03/fig_3_22.tex';assert not target.exists()
report=verify();curve_checks=surface_checks=0
lines=['% Printed Fig3.20(b), source22: same representative5x4 bicubic control net as(a).',
       '% Exact tensor-product isoparametric curves, represented by native cubic Bezier pieces.',
       '% Same camera and plot bounds as(a); no tracing or bitmap wrapper.',
       r'\begin{tikzpicture}[x={(-.9cm,-.6cm)},y={(1cm,-.35cm)},z={(0cm,1cm)},book line]',
       r'\path[use as bounding box] (canvas cs:x=-5cm,y=-4.8cm) rectangle (canvas cs:x=6.1cm,y=5.2cm);',
       r'\draw[book axis] (0,0,0)--(4.5,0,0) node[below left=4pt] {$x$};',
       r'\draw[book axis] (0,0,0)--(0,5.2,0) node[right=4pt] {$y$};',
       r'\draw[book axis] (0,0,0)--(0,0,4.5) node[above=4pt] {$z$};']
for j in range(11):
    fixed=F(j,10)
    wu,wv=weights(U,3,fixed),weights(V,3,fixed)
    qv=tuple(tuple(sum(wu[i]*P[i][k][d] for i in range(5)) for d in range(3)) for k in range(4))
    qu=tuple(tuple(sum(wv[k]*P[i][k][d] for k in range(4)) for d in range(3)) for i in range(5))
    style='book line' if j in (0,10) else 'book grid'
    for axis,k,controls in [('u',V,qv),('v',U,qu)]:
        lines.append('% Exact '+axis+'='+str(fixed)+' isoparametric curve')
        segs=segments(k,controls,3);curve_checks+=check(k,controls,3,segs)
        for h in range(21):
            t=F(h,20);actual=de_boor(k,controls,3,t)
            assert actual==(tensor(fixed,t) if axis=='u' else tensor(t,fixed));surface_checks+=1
        for seg in segs: lines.append(cubic_path(seg,style))
lines += [r'\node at (canvas cs:x=.5cm,y=-4.45cm) {(b)};',r'\end{tikzpicture}']
target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
report.update(exact_isocurve_checks=curve_checks,isocurve_vs_surface_points=surface_checks,
    isoparametric_lines_per_direction=11)
(root/'image_tex/build/surface320-mesh-check.json').write_text(json.dumps(report,indent=2)+'\n')
print(f'PASS: {curve_checks} exact isocurve checks,{surface_checks} tensor comparisons and shared441-point check.')

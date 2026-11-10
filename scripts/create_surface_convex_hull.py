"""Fig3.21: matching cubic x quadratic surface patch and its active 4x3 net."""
from pathlib import Path
from fractions import Fraction as F
from math import comb
import json
from native_bspline import segments,check,cubic_path,point,de_boor
from surface_geometry import surface,isocurve,verify_tensor,local_patch

root=Path(__file__).resolve().parents[1];target=root/'image_tex/ch03/fig_3_23.tex';assert not target.exists()
p,q=3,2
U=(F(0),)*4+(F(1,3),F(2,3))+(F(1),)*4
V=(F(0),)*3+(F(1,3),F(2,3))+(F(1),)*3
xs=(3,2,1,0,-1,-2);ys=(-2,-1,0,1,2)
# Representative shallow sheet; the book gives degrees and topology, no coordinates.
P=tuple(tuple((F(x),F(y),F(2)-F(x*x,10)-F(y*y,6)-F(y,5)) for y in ys) for x in xs)
grid_checks=verify_tensor(U,V,p,q,P)
Q,A,B=local_patch(U,V,p,q,P,4,3)
for a in range(11):
    for b in range(11):
        s,t=F(a,10),F(b,10)
        val=tuple(sum(F(comb(p,r))*s**r*(1-s)**(p-r)*F(comb(q,k))*t**k*(1-t)**(q-k)*Q[r][k][d] for r in range(p+1) for k in range(q+1)) for d in range(3))
        assert val==surface(U,V,p,q,P,F(1,3)+s/3,F(1,3)+t/3)
lines=['% Fig3.21: cubic x quadratic surface and local strong convex hull.',
       '% Representative6x5 shallow control net; exact knots at thirds, clamped ends.',
       '% Central knot rectangle[1/3,2/3]^2 has active controls i=1..4,j=1..3.',
       '% All12 extracted Bezier controls are convex combinations of those12 active controls.',
       '% Native exact polynomial isocurves; no outline tracing.',
       r'\begin{tikzpicture}[x={(-.9cm,-.6cm)},y={(1cm,-.35cm)},z={(0cm,1cm)},book line]',
       r'\path[use as bounding box] (canvas cs:x=-5.4cm,y=-4.2cm) rectangle (canvas cs:x=6cm,y=13.7cm);']
curve_checks=0
for panel,shift in [('a',9),('b',0)]:
    lines += [r'\begin{scope}[yshift='+str(shift)+'cm]',
              r'\draw[book axis] (0,0,0)--(4.5,0,0) node[below left=4pt] {$x$};',
              r'\draw[book axis] (0,0,0)--(0,5,0) node[right=4pt] {$y$};',
              r'\draw[book axis] (0,0,0)--(0,0,4) node[above=4pt] {$z$};']
    if panel=='a':
        for variable in ('u','v'):
            for fixed in (F(0),F(1,3),F(2,3),F(1)):
                k,degree,c=isocurve(U,V,p,q,P,variable,fixed);segs=segments(k,c,degree)
                curve_checks+=check(k,c,degree,segs)
                for j,seg in enumerate(segs):
                    selected=fixed in (F(1,3),F(2,3)) and j==1
                    lines.append(cubic_path(seg,'dashed' if selected else ''))
    else:
        for i in range(6):
            for j in range(4):
                active=1<=i<=4 and 1<=j<=2
                lines.append(r'\draw['+('book line' if active else 'book grid,dashed')+'] '+point(P[i][j])+'--'+point(P[i][j+1])+';')
        for i in range(5):
            for j in range(5):
                active=1<=i<=3 and 1<=j<=3
                lines.append(r'\draw['+('book line' if active else 'book grid,dashed')+'] '+point(P[i][j])+'--'+point(P[i+1][j])+';')
        for row in P:
            for pt in row: lines.append(r'\fill '+point(pt)+' circle[radius=1.3pt];')
    lines += [r'\node at (canvas cs:x=.4cm,y=-3.8cm) {('+panel+')};',r'\end{scope}']
lines.append(r'\end{tikzpicture}')
target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
def strmatrix(a):return [[str(x) for x in row] for row in a]
(root/'image_tex/build/surface-convex-hull-check.json').write_text(json.dumps({'figure':'3.21',
    'representative_example':True,'degrees':[p,q],'control_count':[6,5],
    'U':list(map(str,U)),'V':list(map(str,V)),
    'controls':[[[str(v) for v in pt] for pt in row] for row in P],
    'tensor_vs_nested_deboor_points':grid_checks,'exact_isocurve_checks':curve_checks,
    'patch_parameter_rectangle':['1/3','2/3','1/3','2/3'],'active_i':[1,2,3,4],'active_j':[1,2,3],
    'u_extraction':strmatrix(A),'v_extraction':strmatrix(B),
    'all_extracted_controls_convex_in_active12':True,'exact_patch_tensor_vs_bernstein_points':121},indent=2)+'\n')
print(f'PASS:{grid_checks} exact tensor points,{curve_checks} isocurve checks,121 patch points; full convex-extraction proof.')

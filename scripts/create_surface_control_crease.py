"""Fig3.25: C2 bicubic parametrization with a geometric crease from coincident rows."""
from pathlib import Path
from fractions import Fraction as F
import json
from native_bspline import segments,check,cubic_path,point
from bspline_math import evaluate,derivative
from surface_geometry import verify_tensor,isocurve

root=Path(__file__).resolve().parents[1]
target=root/'image_tex/ch03/fig_3_27.tex';assert not target.exists()
p=q=3
U=(F(0),)*4+(F(1,4),F(1,2),F(3,4))+(F(1),)*4
V=(F(0),)*4+(F(1,2),)+(F(1),)*4
xs=(3,2,0,0,0,-2,-3);ys=(-2,-1,0,1,2)
zu=(0,F(-1,2),3,3,3,F(-1,2),0);zv=(0,F(-1,4),0,F(-1,4),F(1,2))
P=tuple(tuple((F(xs[i]),F(ys[j]),F(zu[i]+zv[j])) for j in range(5)) for i in range(7))
assert P[2]==P[3]==P[4]
tensor_checks=verify_tensor(U,V,p,q,P,10)
lines=['% Printed Fig3.25: representative bicubic7x5 net, P_2,j=P_3,j=P_4,j.',
       '% All internal knots simple: C2 parametrization, but S_u=S_uu=0 at u=1/2.',
       '% Distinct limiting tangent planes form a geometric crease at the singular line.',
       '% Exact native isocurves, no scan-contour conversion.',
       r'\begin{tikzpicture}[x={(-1cm,-.25cm)},y={(.25cm,-.9cm)},z={(0cm,.7cm)},book line]',
       r'\path[use as bounding box] (canvas cs:x=-5.5cm,y=-5.4cm) rectangle (canvas cs:x=6cm,y=6.2cm);',
       r'\draw[book axis] (0,0,0)--(4.8,0,0) node[below left=4pt] {$x$};',
       r'\draw[book axis] (0,0,0)--(0,5.3,0) node[right=4pt] {$y$};',
       r'\draw[book axis] (0,0,0)--(0,0,7) node[above=4pt] {$z$};']
for i in (0,1,2,5,6):lines.append(r'\draw[book grid,dashed] '+'--'.join(map(point,P[i]))+';')
for j in range(5):lines.append(r'\draw[book grid,dashed] '+'--'.join(point(P[i][j]) for i in (0,1,2,5,6))+';')
curves=0;zero_jets=0
for variable in ('u','v'):
    for h in range(9):
        k,d,c=isocurve(U,V,p,q,P,variable,F(h,8));segs=segments(k,c,d);curves+=check(k,c,d,segs)
        if variable=='u':
            left,right=segs[1],segs[2]
            assert left['bern'][-1]==right['bern'][0]
            for s in (left,right):
                for poly in s['power']:
                    assert evaluate(derivative(poly),F(1,2))==0
                    assert evaluate(derivative(derivative(poly)),F(1,2))==0
                    zero_jets+=2
            # On these spans, S-R=N1(P1-R) or N5(P5-R), so each side has
            # a constant transverse tangent direction despite zero parameter speed.
            for j in range(5):
                assert tuple(P[1][j][d]-P[2][j][d] for d in range(3))==(2,0,F(-7,2))
                assert tuple(P[5][j][d]-P[2][j][d] for d in range(3))==(-2,0,F(-7,2))
        for s in segs:lines.append(cubic_path(s,'book line' if h in (0,8) or (variable=='v' and h==4) else 'book grid'))
for i in (0,1,2,5,6):
    for pt in P[i]:lines.append(r'\fill '+point(pt)+' circle[radius=1.25pt];')
for pt,anchor,label in [(P[0][0],'above left',r'\mathbf P_{0,0}'),
                        (P[6][4],'above right',r'\mathbf P_{6,4}'),
                        (P[2][0],'above left',r'\mathbf P_{2,0}=\mathbf P_{3,0}=\mathbf P_{4,0}')]:
    lines.append(r'\node['+anchor+'=5pt] at '+point(pt)+' {$'+label+'$};')
lines.append(r'\end{tikzpicture}')
target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/surface-control-crease-check.json').write_text(json.dumps({
    'figure':'3.25','representative_example':True,'degrees':[p,q],'indexed_control_count':[7,5],
    'U':list(map(str,U)),'V':list(map(str,V)),'coincident_rows':[2,3,4],
    'tensor_vs_nested_deboor_points':tensor_checks,'exact_isocurve_checks':curves,
    'exact_zero_first_second_partial_components':zero_jets,
    'regularity':'C2 everywhere; S_u=S_uu=0 at u=1/2, singular parametrization on crease',
    'geometric_crease_proof':'Each central span uses R+N1*(P1-R) or R+N5*(P5-R), transverse directions (2,0,-7/2),(-2,0,-7/2); S_v has nonzero y component, hence distinct limiting tangent planes'},indent=2)+'\n')
print(f'PASS:{tensor_checks} tensor points,{curves} exact curve checks,{zero_jets} zero-jet components; simple knots, all-v distinct tangent-plane proof.')

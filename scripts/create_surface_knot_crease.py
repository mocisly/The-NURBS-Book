"""Fig3.24: quadratic x cubic surface with a genuine C0 repeated-knot crease."""
from pathlib import Path
from fractions import Fraction as F
import json
from native_bspline import segments,check,cubic_path,point
from bspline_math import evaluate,derivative
from surface_geometry import verify_tensor,isocurve,weights

root=Path(__file__).resolve().parents[1]
target=root/'image_tex/ch03/fig_3_26.tex';assert not target.exists()
p,q=2,3
U=(F(0),)*3+(F(1,2),)*2+(F(1),)*3
V=(F(0),)*4+(F(1,2),)+(F(1),)*4
x=(3,F(3,2),0,-1,-2);y=(-2,-1,0,1,2)
zu=(0,0,2,2,F(7,2));zv=(0,F(-1,2),F(3,5),0,F(3,2))
P=tuple(tuple((F(x[i]),F(y[j]),F(zu[i]+zv[j])) for j in range(5)) for i in range(5))
tensor_checks=verify_tensor(U,V,p,q,P,10)
lines=['% Printed Fig3.24: representative5x5 quadratic x cubic control net.',
       '% U=(0,0,0,1/2,1/2,1,1,1), V=(0,0,0,0,1/2,1,1,1,1).',
       '% Left/right u derivatives at1/2 are(-6,0,8) and(-4,0,0), for every v.',
       '% Exact native polynomial isocurves; genuine crease, no outline tracing.',
       r'\begin{tikzpicture}[x={(-.9cm,-.6cm)},y={(1cm,-.35cm)},z={(0cm,1cm)},book line]',
       r'\path[use as bounding box] (canvas cs:x=-5.3cm,y=-4.3cm) rectangle (canvas cs:x=5.6cm,y=7.8cm);',
       r'\draw[book axis] (0,0,0)--(4.6,0,0) node[below left=4pt] {$x$};',
       r'\draw[book axis] (0,0,0)--(0,4.5,0) node[right=4pt] {$y$};',
       r'\draw[book axis] (0,0,0)--(0,0,7) node[above=4pt] {$z$};']
for row in P:lines.append(r'\draw[book grid,dashed] '+'--'.join(map(point,row))+';')
for j in range(5):lines.append(r'\draw[book grid,dashed] '+'--'.join(point(P[i][j]) for i in range(5))+';')
curves=0;derivatives=[]
for variable in ('u','v'):
    for h in range(11):
        k,d,c=isocurve(U,V,p,q,P,variable,F(h,10));segs=segments(k,c,d);curves+=check(k,c,d,segs)
        if variable=='u':
            left,right=segs
            assert left['bern'][-1]==right['bern'][0]
            a=tuple(evaluate(derivative(poly),F(1,2)) for poly in left['power'])
            b=tuple(evaluate(derivative(poly),F(1,2)) for poly in right['power'])
            assert a==(-6,0,8) and b==(-4,0,0)
            derivatives.append([str(F(h,10)),list(map(str,a)),list(map(str,b))])
        for s in segs:lines.append(cubic_path(s,'book line' if h in (0,10) or (variable=='v' and h==5) else 'book grid'))
for row in P:
    for pt in row:lines.append(r'\fill '+point(pt)+' circle[radius=1.2pt];')
lines.append(r'\end{tikzpicture}')
target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/surface-knot-crease-check.json').write_text(json.dumps({
    'figure':'3.24','representative_example':True,'degrees':[p,q],'control_count':[5,5],
    'U':list(map(str,U)),'V':list(map(str,V)),
    'tensor_vs_nested_deboor_points':tensor_checks,'exact_isocurve_checks':curves,
    'one_sided_derivatives':derivatives,'crease_u':'1/2',
    'all_v_derivative_identity':'S_u(left)=4*(P_2,j-P_1,j)=(-6,0,8); S_u(right)=4*(P_3,j-P_2,j)=(-4,0,0), independent of j',
    'continuity':'C0 with distinct tangent planes at u=1/2; S_v has nonzero y component'},indent=2)+'\n')
print(f'PASS:{tensor_checks} tensor points,{curves} exact curve checks,11 one-sided derivative pairs and all-v crease identity.')

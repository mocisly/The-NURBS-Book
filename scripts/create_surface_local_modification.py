"""Fig3.23: one-control local change, exact quadratic x cubic tensor surface."""
from pathlib import Path
from fractions import Fraction as F
import json
from native_bspline import segments,check,cubic_path,point
from surface_geometry import surface,isocurve,verify_tensor,weights

root=Path(__file__).resolve().parents[1]
target=root/'image_tex/ch03/fig_3_25.tex';assert not target.exists()
p,q=2,3
U=(F(0),)*3+(F(1,4),F(1,2),F(3,4))+(F(1),)*3
V=(F(0),)*4+tuple(F(j,5) for j in range(1,5))+(F(1),)*4
P=tuple(tuple((F(3-i),F(j-2),F(0)) for j in range(8)) for i in range(6))
Q=tuple(tuple((a,b,c+2) if (i,j)==(3,5) else (a,b,c) for j,(a,b,c) in enumerate(row)) for i,row in enumerate(P))
tensor_checks=sum(verify_tensor(U,V,p,q,R,10) for R in (P,Q))
identity_checks=outside_checks=0
for a in range(21):
    for b in range(21):
        u,v=F(a,20),F(b,20)
        old,new=surface(U,V,p,q,P,u,v),surface(U,V,p,q,Q,u,v)
        f=weights(U,p,u)[3]*weights(V,q,v)[5]
        assert tuple(new[d]-old[d] for d in range(3))==(0,0,2*f)
        identity_checks+=1
        if not (F(1,4)<u<1 and F(2,5)<v<1):
            assert old==new;outside_checks+=1
# Exact support follows from the two Cox basis supports, not merely samples.
assert (U[3],U[3+p+1],V[5],V[5+q+1])==(F(1,4),F(1),F(2,5),F(1))
lines=['% Printed Fig3.23: representative6x8 planar control net, only P_{3,5} moves.',
       '% U quadratic quarter knots; V cubic fifth knots (four repeated end knots).',
       '% Exact tensor isocurves; displayed control net translated upward by4.3 solely for visibility.',
       '% Surface difference = N_{3,2}(u) N_{5,3}(v) (0,0,2). No tracing.',
       r'\begin{tikzpicture}[x={(-.9cm,-.36cm)},y={(1cm,-.21cm)},z={(0cm,1cm)},book line]',
       r'\path[use as bounding box] (canvas cs:x=-5.5cm,y=-3.3cm) rectangle (canvas cs:x=8cm,y=19cm);']
curves=0
for tag,shift,R in [('a','12',P),('b','0',Q)]:
    lines += [r'\begin{scope}[yshift='+shift+'cm]',
              r'\draw[book axis] (0,0,0)--(4.5,0,0) node[below left=4pt] {$x$};',
              r'\draw[book axis] (0,0,0)--(0,6.3,0) node[right=4pt] {$y$};',
              r'\draw[book axis] (0,0,0)--(0,0,6.8) node[above=4pt] {$z$};']
    for variable in ('u','v'):
        for h in range(11):
            k,d,c=isocurve(U,V,p,q,R,variable,F(h,10))
            segs=segments(k,c,d);curves+=check(k,c,d,segs)
            for s in segs:lines.append(cubic_path(s,'book line' if h in (0,10) else 'book grid'))
    displayed=tuple(tuple((a,b,c+F(43,10)) for a,b,c in row) for row in R)
    for i in range(6):
        lines.append(r'\draw[book grid,dashed] '+'--'.join(point(x) for x in displayed[i])+';')
    for j in range(8):
        lines.append(r'\draw[book grid,dashed] '+'--'.join(point(displayed[i][j]) for i in range(6))+';')
    for row in displayed:
        for x in row:lines.append(r'\fill '+point(x)+' circle[radius=1.1pt];')
    if tag=='b':
        old=(P[3][5][0],P[3][5][1],F(43,10))
        lines += [r'\draw[book axis] '+point(old)+'--'+point(displayed[3][5])+';',
                  r'\node[above right=4pt] at '+point(displayed[3][5])+r' {$\mathbf P_{3,5}$};']
    lines += [r'\node at (canvas cs:x=.8cm,y=-2.9cm) {('+tag+')};',r'\end{scope}']
lines.append(r'\end{tikzpicture}')
target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/surface-local-modification-check.json').write_text(json.dumps({
    'figure':'3.23','representative_example':True,'degrees':[p,q],'control_count':[6,8],
    'U':list(map(str,U)),'V':list(map(str,V)),'moved_control':[3,5],'delta':[0,0,2],
    'displayed_net_vertical_translation':'43/10',
    'tensor_vs_nested_deboor_points':tensor_checks,'exact_isocurve_checks':curves,
    'exact_difference_identity_points':identity_checks,'unchanged_exterior_points':outside_checks,
    'exact_support_from_basis_knots':['1/4','1','2/5','1'],
    'identity':'S_new-S_old=N_3,2(u)*N_5,3(v)*(0,0,2)'},indent=2)+'\n')
print(f'PASS:{tensor_checks} tensor checks,{curves} exact curve checks,{identity_checks} difference identities,{outside_checks} unchanged exterior points; exact support proof.')

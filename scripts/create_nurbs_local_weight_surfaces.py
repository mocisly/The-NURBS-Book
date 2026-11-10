"""Fig4.11(a,b): identical shifted control nets, changing only one rational weight."""
from pathlib import Path
from fractions import Fraction as F
import json
from native_bspline import segments,check,de_boor,point,cubic_path
from rational_geometry import approximate,project
from surface_geometry import isocurve
from nurbs411_data import U,V,p,q,P,TARGET,CAMERA_NORM,DISPLAY_SHIFT,homogeneous,rational,verify

root=Path(__file__).resolve().parents[1];targets=[root/f'image_tex/ch04/fig_4_{n}.tex' for n in (12,13)]
assert not any(t.exists() for t in targets)
displayed=tuple(tuple((x,y,z+DISPLAY_SHIFT) for x,y,z in row) for row in P)
net=[]
for row in displayed:net.append(r'\draw[book grid,dashed] '+'--'.join(map(point,row))+';')
for j in range(8):net.append(r'\draw[book grid,dashed] '+'--'.join(point(displayed[i][j]) for i in range(7))+';')
for row in displayed:
    for pt in row:net.append(r'\fill '+point(pt)+' circle[radius=1.1pt];')
net += [r'\draw '+point(displayed[4][2])+' circle[radius=2.7pt];',
        r'\node[above right=6pt] at '+point(displayed[4][2])+r' {$\mathbf P_{4,2}$};']
reports=[]
for target,tag,w in zip(targets,('a','b'),(F(2,5),F(6))):
    report=verify(w);H=homogeneous(w)
    lines=['% Fig4.11('+tag+'): same representative7x8 control positions as the other panel, only w42='+str(w)+'.',
           '% Exact U/V, degrees3x2 and rational target basis from Fig4.10.',
           '% Display control net translated upward by27/5 only for visibility; actual surface uses untranslated P.',
           '% Same camera, diagram bounds and native control-net commands in both panels.',
           '% Native cubic rational-isoline approximations have certified projected L1 error<=0.0001cm; no scan outlines.',
           r'\begin{tikzpicture}[x={(-.9cm,-.36cm)},y={(1cm,-.21cm)},z={(0cm,1cm)},book line]',
           r'\path[use as bounding box] (canvas cs:x=-6.8cm,y=-3.9cm) rectangle (canvas cs:x=8.3cm,y=9.5cm);',
           r'\draw[book axis] (0,0,0)--(5,0,0) node[below left=4pt] {$x$};',
           r'\draw[book axis] (0,0,0)--(0,7.3,0) node[right=4pt] {$y$};',
           r'\draw[book axis] (0,0,0)--(0,0,8.8) node[above=4pt] {$z$};']
    exact=points=paths=0;maximum=F(0)
    for var in ('u','v'):
        for j in range(11):
            fixed=F(j,10);k,d,c=isocurve(U,V,p,q,H,var,fixed);ss=segments(k,c,d);exact+=check(k,c,d,ss)
            for h in range(21):
                t=F(h,20);val=project(de_boor(k,c,d,t))
                assert val==(rational(t,fixed,w) if var=='u' else rational(fixed,t,w));points+=1
            for seg in ss:
                for a in approximate(seg['bern'],F(1,10000)/CAMERA_NORM):
                    lines.append(cubic_path(a,'book line' if j in (0,10) else 'book grid'))
                    paths+=1;maximum=max(maximum,a['certified_l1_error']*CAMERA_NORM)
    lines.extend(net)
    label=r'\frac25' if w==F(2,5) else '6'
    lines += [r'\node at (canvas cs:x=5.5cm,y=-3cm) {$w_{4,2}='+label+'$};',
              r'\node at (canvas cs:x=.4cm,y=-3.55cm) {('+tag+')};',r'\end{tikzpicture}']
    target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
    report.update(panel=tag,exact_homogeneous_isocurve_checks=exact,isocurve_vs_rational_tensor_points=points,
                  native_cubic_paths=paths,maximum_certified_projected_l1_error_cm=str(maximum))
    reports.append(report)
(root/'image_tex/build/nurbs-local-weight-surfaces-check.json').write_text(json.dumps({
    'figure':'4.11','representative_controls':[[[str(c) for c in pt] for pt in row] for row in P],
    'degrees':[p,q],'control_count':[7,8],'U':list(map(str,U)),'V':list(map(str,V)),
    'modified_weight':[4,2],'other55weights':1,'displayed_control_net_vertical_translation':str(DISPLAY_SHIFT),
    'same_displayed_net_commands_for_both_panels':True,'camera_l1_operator_norm':str(CAMERA_NORM),'panels':reports},indent=2)+'\n')
print('PASS: matching7x8 nets; each panel121 tensor/weight identity points,4059 homogeneous curve checks,462 curve/tensor points; '+', '.join(str(r['native_cubic_paths'])+' certified paths' for r in reports)+'.')
